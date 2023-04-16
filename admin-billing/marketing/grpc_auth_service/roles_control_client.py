import uuid
import grpc

from . import roles_control_pb2
from . import roles_control_pb2_grpc

from config.components.env_setting import env_settings as _es


def get_stub_grpc():
    channel = grpc.insecure_channel(f'{_es.auth_grpc_host}:{_es.auth_grpc_port}')
    return roles_control_pb2_grpc.RolesControlStub(channel)


def create_new_role(name: str) -> uuid.UUID:
    stub = get_stub_grpc()
    auth_role_id = stub.CreateRole(roles_control_pb2.NewRole(name=name))
    return uuid.UUID(auth_role_id.id)


def update_role(role_id: uuid.UUID, name: str) -> bool:
    stub = get_stub_grpc()
    result = stub.UpdateRole(roles_control_pb2.Role(role_id=str(role_id),name=name))
    return result.successful
    
