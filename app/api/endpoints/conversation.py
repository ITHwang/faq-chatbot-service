import logging

from fastapi import APIRouter
from llama_index.llms.openai import OpenAI

logger = logging.getLogger(__name__)

router = APIRouter()


# @router.get("/message")
# async def message_conversation(
#     conversation_id: UUID,
#     user_message: str,
#     db: AsyncSession = Depends(get_db),
# ) -> EventSourceResponse:
#     """
#     Send a message from a user to a conversation, receive a SSE stream of the assistant's response.
#     Each event in the SSE stream is a Message object. As the assistant continues processing the response,
#     the message object's sub_processes list and content string is appended to. While the message is being
#     generated, the status of the message will be PENDING. Once the message is generated, the status will
#     be SUCCESS. If there was an error in processing the message, the final status will be ERROR.
#     """
#     conversation = await crud.fetch_conversation_with_messages(db, str(conversation_id))
#     if conversation is None:
#         raise HTTPException(status_code=404, detail="Conversation not found")

#     user_message = Message(
#         created_at=datetime.datetime.utcnow(),
#         updated_at=datetime.datetime.utcnow(),
#         conversation_id=conversation_id,
#         content=user_message,
#         role=MessageRoleEnum.user,
#         status=MessageStatusEnum.SUCCESS,
#     )

#     send_chan, recv_chan = anyio.create_memory_object_stream(100)

#     async def event_publisher():
#         async with send_chan:
#             task = asyncio.create_task(handle_chat_message(conversation, user_message, send_chan))
#             message_id = str(uuid4())
#             message = Message(
#                 id=message_id,
#                 conversation_id=conversation_id,
#                 content="",
#                 role=MessageRoleEnum.assistant,
#                 status=MessageStatusEnum.PENDING,
#                 sub_processes=[],
#             )
#             final_status = MessageStatusEnum.ERROR
#             event_id_to_sub_process = OrderedDict()
#             try:
#                 async for message_obj in recv_chan:
#                     if isinstance(message_obj, StreamedMessage):
#                         message.content = message_obj.content
#                     elif isinstance(message_obj, StreamedMessageSubProcess):
#                         status = (
#                             MessageSubProcessStatusEnum.FINISHED
#                             if message_obj.has_ended
#                             else MessageSubProcessStatusEnum.PENDING
#                         )
#                         if message_obj.event_id in event_id_to_sub_process:
#                             created_at = event_id_to_sub_process[message_obj.event_id].created_at
#                         else:
#                             created_at = datetime.datetime.utcnow()
#                         sub_process = MessageSubProcess(
#                             # NOTE: By setting the created_at to the current time, we are
#                             # no longer able to use the created_at field to determine the
#                             # time at which the subprocess was inserted into the database.
#                             created_at=created_at,
#                             message_id=message_id,
#                             source=message_obj.source,
#                             metadata_map=message_obj.metadata_map,
#                             status=status,
#                         )
#                         event_id_to_sub_process[message_obj.event_id] = sub_process

#                         message.sub_processes = list(event_id_to_sub_process.values())
#                     else:
#                         logger.error(f"Unknown message object type: {type(message_obj)}")
#                         continue
#                     yield schema.Message.from_orm(message).json()
#                 await task
#                 if task.exception():
#                     raise ValueError("handle_chat_message task failed") from task.exception()
#                 final_status = MessageStatusEnum.SUCCESS
#             except:
#                 logger.error("Error in message publisher", exc_info=True)
#                 final_status = MessageStatusEnum.ERROR
#             message.status = final_status
#             db.add(user_message)
#             db.add(message)
#             await db.commit()
#             final_message = await crud.fetch_message_with_sub_processes(db, message_id)
#             yield final_message.json()

#     return EventSourceResponse(event_publisher())
