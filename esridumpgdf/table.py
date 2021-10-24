from .layer import Layer


class Table(Layer):
    def __init__(self, url: str, **kwargs):
        super(Table, self).__init__(url, **kwargs)

