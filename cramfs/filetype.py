from enum import Enum


class FileType(Enum):
    fifo = 1
    chrdev = 2
    dir = 4
    blkdev = 6
    file = 8
    link = 10
    socket = 12
