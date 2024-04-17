"""
We suppose that we have a pkl file `{root_directory}/final_result.pkl` that contains raw data of FAQ @ NAVER Smart Store Platform.
"""

import os
import pickle
import time
import logging

import numpy as np
import chromadb

from llama_index.core import Document, VectorStoreIndex, ServiceContext, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModelType


from app.core.config import settings

logger = logging.getLogger(__name__)


def time_logger(func):
    def wrapper(*args, **kwargs):
        logging.debug(f"Starting {func.__name__}")

        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time

        logging.debug(f"Finished {func.__name__} in {elapsed_time:.2f} seconds")

        return result

    return wrapper


def extract_transform_load(pkl_path: str, db_path: str, collection_name: str) -> None:
    if os.path.exists(db_path) and os.listdir(db_path):
        logging.debug(f"Already existing database from {db_path}")
        logging.debug("Skip saving the database")
        return
    raw_data = _load_raw_data(pkl_path)
    documents = _preprocess_raw_data(raw_data)
    _save_db(db_path, collection_name, documents)


def _get_outlier_bound(nums):
    Q1 = np.percentile(nums, 25)
    Q3 = np.percentile(nums, 75)
    IQR = Q3 - Q1

    # Determine outliers
    outlier_lower_bound = Q1 - 1.5 * IQR
    outlier_upper_bound = Q3 + 1.5 * IQR

    return outlier_lower_bound, outlier_upper_bound


@time_logger
def _load_raw_data(pkl_path: str) -> dict[str, str]:
    if not os.path.exists(pkl_path):
        raise FileNotFoundError(f"{pkl_path} not found.")

    with open(pkl_path, "rb") as file:
        raw_data = pickle.load(file)

    return raw_data


@time_logger
def _preprocess_raw_data(raw_data: dict[str, str]) -> list[Document]:
    """
    1. Remove unnecessary parts from the raw data.
    2. Parse categories, question, and answer.
    3. Remove too long data.
    """
    documents = []

    for i, (question, answer) in enumerate(raw_data.items()):
        # remove unnecessary parts
        cut_position = answer.find("위 도움말이 도움이 되었나요?")  # ending message
        answer = answer[:cut_position].strip() if cut_position != -1 else answer.strip()

        # parse categories, question
        parts = question.strip().split("]")
        categories = ", ".join([p.replace("[", "").strip() for p in parts[:-1]])
        question = parts[-1].strip()

        document = Document(
            text=f"질문: {question}\n대답: {answer}",
            metadata={
                "question": question,
                "answer": answer,
                "categories": categories,
            },
            excluded_llm_metadata_keys=["question", "answer"],
            metadata_seperator=settings.METADATA_SEPERATOR,
            metadata_template=settings.METADATA_TEMPLATE,
            text_template=settings.TEXT_TEMPLATE,
        )

    documents.append(document)

    # remove outliers
    lower_bound, upper_bound = _get_outlier_bound([len(document.get_content()) for document in documents])
    lower_outliers = [document for document in documents if len(document.get_content()) < lower_bound]
    upper_outliers = [document for document in documents if len(document.get_content()) > upper_bound]
    logging.debug(f"The number of too short docs: {len(lower_outliers)}")
    logging.debug(f"The number of too long docs: {len(upper_outliers)}")
    documents = [
        document
        for document in documents
        if len(document.get_content()) >= lower_bound and len(document.get_content()) <= upper_bound
    ]

    # stat
    logging.debug(f"The number of docs remaining: {len(documents)}")
    logging.debug(f"Mimimum length: {min(len(document.get_content()) for document in documents)}")
    logging.debug(f"Maximum length: {max(len(document.get_content()) for document in documents)}")
    logging.debug(f"Mean length: {int(sum(len(document.get_content()) for document in documents) / len(documents))}")

    return documents


# @time_logger
# def _chunk_documents(documents: list[Document]) -> list[BaseNode]:
#     parser = SentenceSplitter.from_defaults(
#         chunk_size=settings.CHUNK_SIZE,
#         chunk_overlap=settings.CHUNK_OVERLAP,
#     )
#     return parser.get_nodes_from_documents(documents)


def _get_tool_service_context() -> ServiceContext:
    llm = OpenAI(
        temperature=0,
        # todo: save model name in settings
        model="gpt-3.5-turbo",
        streaming=False,
        api_key=settings.OPENAI_API_KEY,
    )

    embedding_model = OpenAIEmbedding(
        mode=OpenAIEmbeddingMode.SIMILARITY_MODE,
        model_type=OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
        api_key=settings.OPENAI_API_KEY,
    )

    # Use a smaller chunk size to retrieve more granular results
    node_parser = SentenceSplitter.from_defaults(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embedding_model,
        node_parser=node_parser,
    )

    return service_context


@time_logger
def _save_db(db_path: str, collection_name: str, documents: list[Document]) -> None:
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    client = chromadb.PersistentClient(path=db_path)
    chroma_collection = client.create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, service_context=_get_tool_service_context(), show_progress=True
    )
