from .base import base
from .reader import read_u4le


class ChunkedDataInode(base):
    def _read(self):
        self.block_end_index = [None] * (((self._parent.size + self._root.page_size) - 1) // self._root.page_size)
        for i in range(((self._parent.size + self._root.page_size) - 1) // self._root.page_size):
            self.block_end_index[i] = read_u4le(self._io)
        self.raw_blocks = self._io.read()
