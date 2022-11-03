from io import BytesIO
from typing import Union

from .error import cramfs_exception


# возвращаем файлоподобный объект cramfs размером не более 256МБ
def openfs(fileobject: Union[str, bytes, BytesIO], offset=0, size=0) -> BytesIO:
    if type(fileobject) == str:
        fileobject = open(fileobject, "rb")
    elif type(fileobject) == bytes:
        fileobject = BytesIO(fileobject)
    elif type(fileobject) != BytesIO:
        raise cramfs_exception(f"bad file type {fileobject}")
    fileobject.seek(offset)
    if size == 0:
        size = 268435456
    return BytesIO(fileobject.read(size))
