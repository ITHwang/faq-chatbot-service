import logging

from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter

from app.chat.messaging import handle_chat_message

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/message")
async def message_conversation(
    user_message: str,
) -> EventSourceResponse:
    """
    Send a message from a user to a conversation, receive a SSE stream of the assistant's response.
    Each event in the SSE stream is a Message object. As the assistant continues processing the response,
    the message object's sub_processes list and content string is appended to. While the message is being
    generated, the status of the message will be PENDING. Once the message is generated, the status will
    be SUCCESS. If there was an error in processing the message, the final status will be ERROR.
    """

    async def event_publisher():
        async for text in handle_chat_message(user_message):
            yield text

    return EventSourceResponse(event_publisher())
