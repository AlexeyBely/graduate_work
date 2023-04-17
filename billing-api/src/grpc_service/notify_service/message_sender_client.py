import uuid
from enum import IntEnum
from datetime import datetime
from grpc.aio import insecure_channel

from grpc_service.notify_service import message_sender_pb2_grpc
from grpc_service.notify_service import message_sender_pb2
from core.config import settings


grpc_url = f'{settings.notify_grpc_host}:{settings.notify_grpc_port}'


class SubscribeMessage(IntEnum):
    """Subscribe message type."""
    SUBSCRIBED = 1
    SUBSCRIBE_BLOKED = 2
    SUBSCRIBE_END = 3


async def grpc_notify_send_message(message_type: int, user_id: uuid.UUID, 
                                   role_descript: str, end_subscribe: datetime) -> None:
    """Send message to notification service."""
    async with insecure_channel(grpc_url) as channel:
        stub = message_sender_pb2_grpc.MessageSenderStub(channel)
        result = await stub.SendBillingMessage(
            message_sender_pb2.BillingMessage(
                template_num=message_type,
                user_id=str(user_id),
                role_description=role_descript,
                end_payment=end_subscribe.ctime(),
            )
        )
