class cramfs_exception(Exception):
    def __init__(self, text: str="cramfs error"):
        self.text = text
