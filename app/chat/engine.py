import os

import chromadb
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.core.tools import QueryEngineTool
from llama_index.embeddings.openai import (
    OpenAIEmbedding,
    OpenAIEmbeddingMode,
    OpenAIEmbeddingModelType,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index_client import SentenceSplitter
from llama_index.agent.openai import OpenAIAgent

from app.core.config import settings
from app.chat.system_message import SYSTEM_MESSAGE
from app.chat.qa_response_synth import get_custom_response_synth


def get_chat_engine(db_path: str) -> OpenAIAgent:
    index = _load_index_from_db(db_path)
    query_engine_tool = QueryEngineTool(query_engine=_index_to_query_engine(index))

    llm = OpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        streaming=True,
        api_key=settings.OPENAI_API_KEY,
    )

    chat_engine = OpenAIAgent.from_tools(
        tools=[query_engine_tool],
        llm=llm,
        chat_history=[],
        verbose=settings.VERBOSE,
        system_prompt=SYSTEM_MESSAGE,
    )

    return chat_engine


def _load_index_from_db(db_path: str) -> VectorStoreIndex:
    """
    Load the index from the database located at the given path.

    Args:
        db_path (str): The path to the database.

    Returns:
        VectorStoreIndex: The loaded index from the database.

    Raises:
        ValueError: If the database is not found at the specified path.
    """
    if not os.path.exists(db_path):
        raise ValueError(f"Database not found at {db_path}")

    db = chromadb.PersistentClient(path=db_path)
    chroma_collection = db.get_or_create_collection("quickstart")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    embed_model = OpenAIEmbedding(
        mode=OpenAIEmbeddingMode.SIMILARITY_MODE,
        model_type=OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
        api_key=settings.OPENAI_API_KEY,
    )

    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    return index


def _index_to_query_engine(index: VectorStoreIndex) -> RetrieverQueryEngine:
    """
    Converts a VectorStoreIndex to a RetrieverQueryEngine.

    Args:
        index (VectorStoreIndex): The VectorStoreIndex to convert.

    Returns:
        RetrieverQueryEngine: The converted RetrieverQueryEngine object.
    """
    llm = OpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        streaming=False,
        api_key=settings.OPENAI_API_KEY,
    )

    retriever = index.as_retriever(similarity_top_k=settings.TOP_K)

    tool_service_context = _get_tool_service_context()

    response_synthesizer = get_custom_response_synth(service_context=tool_service_context)

    return RetrieverQueryEngine.from_args(
        retriever,
        llm=llm,
        response_synthesizer=response_synthesizer,
        service_context=tool_service_context,
    )


def _get_tool_service_context() -> ServiceContext:
    """
    Retrieves the service context for the tool.

    Returns:
        ServiceContext: The service context object containing the necessary tools for the chat engine.
    """
    llm = OpenAI(
        temperature=0,
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
