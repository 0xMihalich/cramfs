from io import BytesIO
from struct import unpack


def read_u2le(_io: BytesIO) -> int:
    return unpack('<H', _io.read(2))[0]


def read_u4le(_io: BytesIO) -> int:
    return unpack('<I', _io.read(4))[0]


def size(_io: BytesIO) -> int:
    cur_pos = _io.tell()
    full_size = _io.seek(0, 2)
    _io.seek(cur_pos)
    return full_size


def is_eof(_io: BytesIO) -> bool:
    t = _io.read(1)
    if t == b'':
        return True

    _io.seek(-1, 1)
    return False
