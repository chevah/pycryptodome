from typing import Union, Optional


class SHAKE128_XOF(object):
    oid: str
    def __init__(self, data: Optional[Union[bytes, bytearray, memoryview]]=None) -> None: ...
    def update(self, data: Union[bytes, bytearray, memoryview]) -> SHAKE128_XOF: ...
    def new(self, data: Optional[Union[bytes, bytearray, memoryview]]=None) -> SHAKE128_XOF: ...

def new(data: Optional[Union[bytes, bytearray, memoryview]]=None) -> SHAKE128_XOF: ...