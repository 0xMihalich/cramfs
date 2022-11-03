from typing import NamedTuple, Union


class cramfs_entryes(NamedTuple):
    name: str
    type: str
    size: int = 0
    uid: int = 0
    exec: Union[str, bool] = False
    chmod: str = ""
