import chardet
from .fancy_print import _f
from .supplies import Broom, Custom
from .utils import writeme
import os, re, html

class Janitor:
    def __init__(self, path=None, o=None):
        self.path = path
        self.o = o
        _f('warn', 'invalid path') if path is None or not self.check() else None
        _f('warn', 'no output path set') if o is None else None
    def check(self):
        return os.path.exists(self.path)
    def process(self):
        if self.check():
            with open(self.path, 'rb') as f:
                _ = f.read()
                enc = chardet.detect(_)['encoding']
                if enc is None:
                    enc = 'utf-8'
                try:
                    if self.path.endswith('.xml'):
                        _t = Broom(copy=_.decode(enc)).sweep(xml=True)
                    else:
                        _t = Broom(copy=_.decode(enc)).sweep()
                    return writeme(_t.encode(), self.o)
                except Exception as e:
                    _f('fatal', f'markup encoding - {e} | {_}')
        else:
            return _f('fatal', 'invalid path')
    def destroy(self, confirm=None):
        _e = self.check()
        if not _e:
            return _f('fatal', 'invalid path')
        if confirm==self.o.split('/')[-1] and _e:
            os.remove(self.o), _f('warn', f'{confirm} destroyed from {self.o}')
        else:
            _f('fatal','you did not confirm - `Receipts.destroy(confirm="file_name")`')
        