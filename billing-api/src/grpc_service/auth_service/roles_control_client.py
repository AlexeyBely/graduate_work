import uuid

from grpc.aio import insecure_channel

from core.config import settings
from grpc_service.auth_service import roles_control_pb2, roles_control_pb2_grpc

grpc_url = f'{settings.auth_grpc_host}:{settings.auth_grpc_port}'


async def grpc_auth_user_email(user_id: uuid.UUID) -> str:
    """Read user email from ID user."""
    async with insecure_channel(grpc_url) as channel:
        stub = roles_control_pb2_grpc.RolesControlStub(channel)
        user_info = await stub.GetUserInfo(roles_control_pb2.Uuid(id=str(user_id)))
        return user_info.email


async def grpc_auth_provide_role(user_id: uuid.UUID, role_id: uuid.UUID, 
                                 jti: str) -> bool:
    """Adds a privileged role to the user in the authorization service.
    
    jti - access-token identifier to add to compromised
    Returns True when successful adds.
    """
    async with insecure_channel(grpc_url) as channel:
        stub = roles_control_pb2_grpc.RolesControlStub(channel)
        result = await stub.ProvideRoleUser(
            roles_control_pb2.ProvideRole(
                user_id=str(user_id),
                role_id=str(role_id),
                jti_to_compromised=str(jti) 
            )
        )
        return result.successful
  

async def grpc_auth_revoke_role(user_id: uuid.UUID, role_id: uuid.UUID, 
                                jti: str) -> bool:
    """Deletes a privileged role to the user in the authorization service.
    
    jti - access-token identifier to add to compromised
    Returns True when successful adds.
    """
    async with insecure_channel(grpc_url) as channel:
        stub = roles_control_pb2_grpc.RolesControlStub(channel)
        result = await stub.RevokeRoleUser(
            roles_control_pb2.ProvideRole(
                user_id=str(user_id),
                role_id=str(role_id),
                jti_to_compromised=str(jti)
            )
        )
        return result.successful

