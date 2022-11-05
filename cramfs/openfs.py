from io import BytesIO
from typing import Union

from .error import cramfs_exception


class openfs:
    '''
    Данный класс решает две проблемы: 
    1. работа по смещению без правки методов основной библиотеки
    2. не читаем файл заново и не храним мусор в оперативной памяти
    '''

    def __init__(self, fileobject: Union[str, bytes, BytesIO], offset: int=0):
        if type(fileobject) == str:
            self.fileobject =  open(fileobject, "rb")
        elif type(fileobject) == bytes:
            self.fileobject = BytesIO(fileobject)
        elif type(fileobject) == BytesIO:
            self.fileobject = fileobject
        else:
            raise cramfs_exception(f"bad file type {fileobject}")
        self.offset = offset
        self.fileobject.seek(self.offset)

    def seek(self, pos: int, whence=0):
        if whence == 0:
            pos += self.offset
        return self.fileobject.seek(pos, whence)

    def read(self, size: int=-1):
        return self.fileobject.read(size)

    def tell(self):
        return self.fileobject.tell()

    def close(self):
        del self.offset
        return self.fileobject.close()




