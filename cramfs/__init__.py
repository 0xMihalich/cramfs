from typing import Tuple

from .cramfs import Cramfs
from .entryes import cramfs_entryes
from .error import cramfs_exception
from .inode import Inode
from .openfs import openfs
from .uncompress import uncompress


'''
Класс для работы с CramFS
Доступен просмотр содержимого и чтение файлов
'''


class cramFS:
    def __init__(self, cramfs_bytes: bytes, offset=0, size=0):
        self.cramfs = Cramfs(openfs(cramfs_bytes, offset, size))
        self.superblock = self.cramfs.super_block
        self.root = self.superblock.root
        self.fs = self.root.as_reg_file._io
        self.path = self.root

    def obj_info(self, file: Inode) -> cramfs_entryes:
        mode = oct(file.mode)[-3:]
        if file.type.name == 'link':
            exec = uncompress(self.fs, file.offset, file.size).decode()
        elif mode in ('755', '777'):
            exec = True
        else:
            exec = False
        return cramfs_entryes(file.name, file.type.name, file.size, file.uid, exec, mode)

    def get_inode(self, path: str) -> Inode:
        search = [dirs for dirs in path.split("/") if dirs]
        if not search:
            return self.root
        inode = self.path
        def find_inode(inode, name, last):
            if inode.type.name == 'dir' and not last:
                for names in inode.as_dir.children:
                    if name == names.name:
                        return names
            return inode
        last = False
        for num, name in enumerate(search):
            if num == len(search):
                last = True
            inode = find_inode(inode, name, last)
        if inode.name != search[-1]:
            raise cramfs_exception(f"{path} not found")
        return inode

    def ls(self, path: str=None) -> Tuple[cramfs_entryes, ...]:
        path = path or self.path
        if not path is self.path:
            if path[0] == '/':
                path = self.root
            path = self.get_inode(path.type.name)
        if path.type.name != 'dir':
            return self.obj_info(path)
        return tuple(self.obj_info(file) for file in path.as_dir.children)

    def cd(self, path: str=None) -> str:
        if path:
            self.path = self.get_inode(path)
        return self.pwd()

    def pwd(self) -> str:
        if not self.path.name:
            return "/"
        return self.path.name

    def read(self, source: str) -> bytes:
        file = self.get_inode(source)
        if file.type.name == 'dir':
            raise cramfs_exception("Can't read directory")
        return uncompress(self.fs, file.offset, file.size)
