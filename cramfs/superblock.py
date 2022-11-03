from .base import base
from .error import cramfs_exception
from .info import Info
from .inode import Inode
from .reader import read_u4le


class SuperBlockStruct(base):
    def _read(self):
        self.magic = self._io.read(4)
        if not self.magic == b'\x45\x3d\xcd\x28':
            raise cramfs_exception('bad magic')
        self.size = read_u4le(self._io)
        self.flags = read_u4le(self._io)
        self.future = read_u4le(self._io)
        self.signature = self._io.read(16)
        if not self.signature == b'Compressed ROMFS':
            raise cramfs_exception('bad signature')
        self.fsid = Info(self._io, self, self._root)
        self.name = (self._io.read(16)).decode('ascii')
        self.root = Inode(self._io, self, self._root)

    @property
    def flag_fsid_v2(self):
        if not hasattr(self, '_m_flag_fsid_v2'):
            self._m_flag_fsid_v2 = ((self.flags >> 0) & 1)
        return self._m_flag_fsid_v2

    @property
    def flag_holes(self):
        if not hasattr(self, '_m_flag_holes'):
            self._m_flag_holes = ((self.flags >> 8) & 1)
        return self._m_flag_holes

    @property
    def flag_wrong_signature(self):
        if not hasattr(self, '_m_flag_wrong_signature'):
            self._m_flag_wrong_signature = ((self.flags >> 9) & 1)
        return self._m_flag_wrong_signature

    @property
    def flag_sorted_dirs(self):
        if not hasattr(self, '_m_flag_sorted_dirs'):
            self._m_flag_sorted_dirs = ((self.flags >> 1) & 1)
        return self._m_flag_sorted_dirs

    @property
    def flag_shifted_root_offset(self):
        if not hasattr(self, '_m_flag_shifted_root_offset'):
            self._m_flag_shifted_root_offset = ((self.flags >> 10) & 1)
        return self._m_flag_shifted_root_offset
