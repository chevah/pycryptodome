from types import ModuleType
from typing import Union, Any, Optional, Tuple

class OcbMode(object):
    block_size: int
    nonce: Union[bytes, bytearray, memoryview]
    def __init__(self, factory: ModuleType, nonce: Union[bytes, bytearray, memoryview], mac_len: int, cipher_params: Any) -> None: ...
    def update(self, assoc_data: Union[bytes, bytearray, memoryview]) -> OcbMode: ...
    def encrypt(self, plaintext: Optional[Union[bytes, bytearray, memoryview]]=None) -> bytes: ...
    def decrypt(self, ciphertext: Optional[Union[bytes, bytearray, memoryview]]=None) -> bytes: ...
    def digest(self) -> bytes: ...
    def hexdigest(self) -> str: ...
    def verify(self, received_mac_tag: Union[bytes, bytearray, memoryview]) -> None: ...
    def hexverify(self, hex_mac_tag: str) -> None: ...
    def encrypt_and_digest(self, plaintext: Union[bytes, bytearray, memoryview]) -> Tuple[bytes, bytes]: ...
    def decrypt_and_verify(self, ciphertext: Union[bytes, bytearray, memoryview], received_mac_tag: bytes) -> bytes: ...