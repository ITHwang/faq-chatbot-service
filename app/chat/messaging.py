import logging
from typing import AsyncGenerator

from llama_index.core.chat_engine.types import StreamingAgentChatResponse

from app.chat.engine import get_chat_engine


logger = logging.getLogger(__name__)


async def handle_chat_message(user_message: str) -> AsyncGenerator[str, None]:
    chat_engine = get_chat_engine()
    logger.debug("Engine received")

    streaming_chat_response: StreamingAgentChatResponse = await chat_engine.astream_chat(
        user_message
    )

    response_str = ""
    async for text in streaming_chat_response.async_response_gen():
        response_str += text
        yield text

    if response_str.strip() == "":
        yield "Sorry, I either wasn't able to understand your question or I don't have an answer for it."
