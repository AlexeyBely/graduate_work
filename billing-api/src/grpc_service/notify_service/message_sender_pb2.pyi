from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BillingMessage(_message.Message):
    __slots__ = ["end_payment", "role_description", "template_num", "user_id"]
    END_PAYMENT_FIELD_NUMBER: _ClassVar[int]
    ROLE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_NUM_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    end_payment: str
    role_description: str
    template_num: int
    user_id: str
    def __init__(self, template_num: _Optional[int] = ..., user_id: _Optional[str] = ..., role_description: _Optional[str] = ..., end_payment: _Optional[str] = ...) -> None: ...

class OperationResult(_message.Message):
    __slots__ = ["successful"]
    SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    successful: bool
    def __init__(self, successful: bool = ...) -> None: ...
