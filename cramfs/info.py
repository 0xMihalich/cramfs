from struct import unpack

from .base import base
from .reader import read_u4le


class Info(base):
    def _read(self):
        self.crc = read_u4le(self._io)
        self.edition = read_u4le(self._io)
        self.blocks = read_u4le(self._io)
        self.files = read_u4le(self._io)
