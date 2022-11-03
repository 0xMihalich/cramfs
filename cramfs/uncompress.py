from io import BytesIO
from zlib import decompress

from .reader import read_u4le


def uncompress(_io: BytesIO, offset: int, size: int) -> bytes:
    _pos = _io.tell()
    _io.seek(offset)
    nblocks = (size - 1) // 4096 + 1
    startofblock = offset + nblocks * 4
    blocks = list()
    for i in range(nblocks):
        endofblock = read_u4le(_io)
        blocks.append(endofblock - startofblock)
        startofblock = endofblock
    file_bytes = BytesIO()
    for blocksize in blocks:
        file_bytes.write(decompress(_io.read(blocksize)))
    _io.seek(_pos)
    del _pos, nblocks, startofblock, endofblock, blocks
    return file_bytes.getvalue()
