import logging

from fastapi import APIRouter
from llama_index.llms.openai import OpenAI

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def root():
    # response = OpenAI().complete("Paul Graham is ")
    response = "df"
    return {"response": response}
