import abc

class base(metaclass=abc.ABCMeta):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    @abc.abstractmethod
    def _read(self):
        ''' абстрактная функция, задается в каждом классе '''
        
        return
