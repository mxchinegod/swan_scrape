from .fancy_print import _f

class Fax:
    def __init__(self, data=None):
        self.data = data 
        _f('fatal', 'no data passed to send') if data is None else None