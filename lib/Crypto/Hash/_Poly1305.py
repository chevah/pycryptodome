# -*- coding: utf-8 -*-
#
# Hash/_Poly1305.py - Implements the Poly1305 MAC
#
# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# No rights are reserved.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================

from binascii import unhexlify

from Crypto.Util.py3compat import bord, tobytes

from Crypto.Hash import BLAKE2s
from Crypto.Random import get_random_bytes
from Crypto.Util._raw_api import (load_pycryptodome_raw_lib,
                                  VoidPointer, SmartPointer,
                                  create_string_buffer,
                                  get_raw_buffer, c_size_t,
                                  c_uint8_ptr)


_raw_poly1305 = load_pycryptodome_raw_lib("Crypto.Hash._Poly1305",
                        """
                        int poly1305_init(void **state,
                                          const uint8_t *key,
                                          size_t key_size);
                        int poly1305_destroy(void *state);
                        int poly1305_update(void *state,
                                            const uint8_t *in,
                                            size_t len);
                        int poly1305_digest(const void *state,
                                            uint8_t digest[16]);
                        """)


class Poly1305(object):

    def __init__(self, key, data):

        self._mac_tag = None

        state = VoidPointer()
        result = _raw_poly1305.poly1305_init(state.address_of(),
                                             c_uint8_ptr(key),
                                             c_size_t(len(key))
                                             )
        if result:
            raise ValueError("Error %d while instantiating Poly1305" % result)
        self._state = SmartPointer(state.get(),
                                   _raw_poly1305.poly1305_destroy)
        if data:
            self.update(data)

    def update(self, data):
        
        if self._mac_tag:
            raise TypeError("You can only call 'digest' or 'hexdigest' on this object")

        result = _raw_poly1305.poly1305_update(self._state.get(),
                                               c_uint8_ptr(data),
                                               c_size_t(len(data)))
        if result:
            raise ValueError("Error %d while hashing Poly1305 data" % result)
        return self

    def copy(self):
        raise NotImplementedError()

    def digest(self):

        if self._mac_tag:
            return self._mac_tag
        
        bfr = create_string_buffer(16)
        result = _raw_poly1305.poly1305_digest(self._state.get(),
                                               bfr)
        if result:
            raise ValueError("Error %d while creating Poly1305 digest" % result)

        self._mac_tag = get_raw_buffer(bfr)
        return self._mac_tag

    def hexdigest(self):

        return "".join(["%02x" % bord(x)
                        for x in tuple(self.digest())])

    def verify(self, mac_tag):

        secret = get_random_bytes(16)

        mac1 = BLAKE2s.new(digest_bits=160, key=secret, data=mac_tag)
        mac2 = BLAKE2s.new(digest_bits=160, key=secret, data=self.digest())

        if mac1.digest() != mac2.digest():
            raise ValueError("MAC check failed")

    def hexverify(self, hex_mac_tag):

        self.verify(unhexlify(tobytes(hex_mac_tag)))


def new(key, msg):
    """Create a new Poly1305 MAC object.

    Args:
        key (byte string/byte array/memoryview):
            key for the Poly1305 object, 32 bytes.
        msg (byte string/byte array/memoryview):
            Optional. The very first chunk of the message to authenticate.
            It is equivalent to an early call to `_Poly1305.update`. Optional.

    Returns:
        A :class:`_Poly1305` object
    """

    if len(key) != 32:
        raise ValueError("Poly1305 key must be 32 bytes long")

    return Poly1305(key, msg)