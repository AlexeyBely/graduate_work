# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import roles_control_pb2 as roles__control__pb2


class RolesControlStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:S
            channel: A grpc.Channel.
        """
        self.GetUserInfo = channel.unary_unary(
                '/rolescontrol.RolesControl/GetUserInfo',
                request_serializer=roles__control__pb2.Uuid.SerializeToString,
                response_deserializer=roles__control__pb2.UserInfo.FromString,
                )
        self.CreateRole = channel.unary_unary(
                '/rolescontrol.RolesControl/CreateRole',
                request_serializer=roles__control__pb2.NewRole.SerializeToString,
                response_deserializer=roles__control__pb2.Uuid.FromString,
                )
        self.UpdateRole = channel.unary_unary(
                '/rolescontrol.RolesControl/UpdateRole',
                request_serializer=roles__control__pb2.Role.SerializeToString,
                response_deserializer=roles__control__pb2.OperationResult.FromString,
                )
        self.ProvideRoleUser = channel.unary_unary(
                '/rolescontrol.RolesControl/ProvideRoleUser',
                request_serializer=roles__control__pb2.ProvideRole.SerializeToString,
                response_deserializer=roles__control__pb2.OperationResult.FromString,
                )
        self.RevokeRoleUser = channel.unary_unary(
                '/rolescontrol.RolesControl/RevokeRoleUser',
                request_serializer=roles__control__pb2.ProvideRole.SerializeToString,
                response_deserializer=roles__control__pb2.OperationResult.FromString,
                )


class RolesControlServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUserInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProvideRoleUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RevokeRoleUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RolesControlServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUserInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserInfo,
                    request_deserializer=roles__control__pb2.Uuid.FromString,
                    response_serializer=roles__control__pb2.UserInfo.SerializeToString,
            ),
            'CreateRole': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateRole,
                    request_deserializer=roles__control__pb2.NewRole.FromString,
                    response_serializer=roles__control__pb2.Uuid.SerializeToString,
            ),
            'UpdateRole': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateRole,
                    request_deserializer=roles__control__pb2.Role.FromString,
                    response_serializer=roles__control__pb2.OperationResult.SerializeToString,
            ),
            'ProvideRoleUser': grpc.unary_unary_rpc_method_handler(
                    servicer.ProvideRoleUser,
                    request_deserializer=roles__control__pb2.ProvideRole.FromString,
                    response_serializer=roles__control__pb2.OperationResult.SerializeToString,
            ),
            'RevokeRoleUser': grpc.unary_unary_rpc_method_handler(
                    servicer.RevokeRoleUser,
                    request_deserializer=roles__control__pb2.ProvideRole.FromString,
                    response_serializer=roles__control__pb2.OperationResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rolescontrol.RolesControl', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RolesControl(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUserInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rolescontrol.RolesControl/GetUserInfo',
            roles__control__pb2.Uuid.SerializeToString,
            roles__control__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rolescontrol.RolesControl/CreateRole',
            roles__control__pb2.NewRole.SerializeToString,
            roles__control__pb2.Uuid.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rolescontrol.RolesControl/UpdateRole',
            roles__control__pb2.Role.SerializeToString,
            roles__control__pb2.OperationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ProvideRoleUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rolescontrol.RolesControl/ProvideRoleUser',
            roles__control__pb2.ProvideRole.SerializeToString,
            roles__control__pb2.OperationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RevokeRoleUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rolescontrol.RolesControl/RevokeRoleUser',
            roles__control__pb2.ProvideRole.SerializeToString,
            roles__control__pb2.OperationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
