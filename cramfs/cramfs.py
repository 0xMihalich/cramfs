from .base import base
from .superblock import SuperBlockStruct


class Cramfs(base):
    def _read(self):
        self.super_block = SuperBlockStruct(self._io, self, self._root)

    @property
    def page_size(self):
        return 4096
