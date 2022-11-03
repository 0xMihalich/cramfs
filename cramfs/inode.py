from io import BytesIO

from .base import base
from .chunk import ChunkedDataInode
from .filetype import FileType
from .reader import is_eof, read_u2le, read_u4le, size


class Inode(base):
    def _read(self):
        self.mode = read_u2le(self._io)
        self.uid = read_u2le(self._io)
        self.size_gid = read_u4le(self._io)
        self.namelen_offset = read_u4le(self._io)
        self.name = (self._io.read(self.namelen)).decode('utf-8').replace('\x00', '')

    @property
    def attr(self):
        if not hasattr(self, '_m_attr'):
            self._m_attr = ((self.mode >> 9) & 7)
        return self._m_attr

    @property
    def as_reg_file(self):
        if not hasattr(self, '_m_as_reg_file'):
            io = self._root._io
            _pos = io.tell()
            io.seek(self.offset)
            self._m_as_reg_file = ChunkedDataInode(io, self, self._root)
            io.seek(_pos)
        return self._m_as_reg_file

    @property
    def perm_u(self):
        if not hasattr(self, '_m_perm_u'):
            self._m_perm_u = ((self.mode >> 6) & 7)
        return self._m_perm_u

    @property
    def as_symlink(self):
        if not hasattr(self, '_m_as_symlink'):
            io = self._root._io
            _pos = io.tell()
            io.seek(self.offset)
            self._m_as_symlink = ChunkedDataInode(io, self, self._root)
            io.seek(_pos)
        return self._m_as_symlink

    @property
    def perm_o(self):
        if not hasattr(self, '_m_perm_o'):
            self._m_perm_o = (self.mode & 7)
        return self._m_perm_o

    @property
    def size(self):
        if not hasattr(self, '_m_size'):
            self._m_size = (self.size_gid & 16777215)
        return self._m_size

    @property
    def gid(self):
        if not hasattr(self, '_m_gid'):
            self._m_gid = (self.size_gid >> 24)
        return self._m_gid

    @property
    def perm_g(self):
        if not hasattr(self, '_m_perm_g'):
            self._m_perm_g = ((self.mode >> 3) & 7)
        return self._m_perm_g

    @property
    def namelen(self):
        if not hasattr(self, '_m_namelen'):
            self._m_namelen = ((self.namelen_offset & 63) << 2)
        return self._m_namelen

    @property
    def as_dir(self):
        if not hasattr(self, '_m_as_dir'):
            io = self._root._io
            _pos = io.tell()
            io.seek(self.offset)
            self._raw__m_as_dir = io.read(self.size)
            _io__raw__m_as_dir = BytesIO(self._raw__m_as_dir)
            self._m_as_dir = DirInode(_io__raw__m_as_dir, self, self._root)
            io.seek(_pos)
        return self._m_as_dir

    @property
    def type(self):
        if not hasattr(self, '_m_type'):
            self._m_type = FileType((self.mode >> 12) & 15)
        return self._m_type

    @property
    def offset(self):
        if not hasattr(self, '_m_offset'):
            self._m_offset = (((self.namelen_offset >> 6) & 67108863) << 2)
        return self._m_offset


class DirInode(base):
    def _read(self):
        if size(self._io) > 0:
            self.children = []
            i = 0
            while not is_eof(self._io):
                self.children.append(Inode(self._io, self, self._root))
                i += 1
