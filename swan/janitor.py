import chardet
from .fancy_print import _f
from .supplies import Broom, Custom
from .utils import writeme

class Janitor:
    def __init__(self, path=None, o=None):
        self.path = path
        self.o = o
        _f('fatal', 'no file passed to clean') if path is None else None
        _f('warn', 'no output path set') if o is None else None

    def process(self):
        with open(self.path, 'rb') as f:
            _ = f.read()
            enc = chardet.detect(_)['encoding']
            if enc is None:
                enc = 'utf-8'
            try:
                if self.path.endswith('.xml'):
                    _t = Broom.sweep(_.decode(enc))
                else:
                    _t = _.decode(enc, errors='replace')
                return writeme(_t.encode(), self.o)
            except Exception as e:
                _f('fatal', f'markup encoding - {e} | {_}')