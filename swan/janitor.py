import chardet
from .supplies import Broom
from .utils import writeme, _f, check
import os

class Janitor:
    def __init__(self, path: str = None, o: str = None):
        """
        The function initializes an object with a path and an output path, and checks for invalid path
        and missing output path.
        
        :param path: The `path` parameter is used to specify a file path. It is an optional parameter,
        meaning it can be set to `None` if not needed
        :param o: The parameter "o" represents the output path. It is used to specify the location where
        the output of the code will be saved or written to
        """
        self.path = path
        self.o = o
        _f('warn', 'invalid path') if path is None or not check(self.path) else None
        _f('warn', 'no output path set') if o is None else None
    def process(self):
        """
        The function processes a file by reading its contents, detecting the encoding, and performing
        specific actions based on the file type.
        :return: the result of the `writeme` function call, which is not shown in the provided code.
        """
        if check(self.path):
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
    def destroy(self, confirm: str = None):
        """
        The function `destroy` removes a file if the confirmation matches the file name.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It should
        be set to the name of the file that you want to destroy
        :return: a message indicating whether the file was successfully destroyed or not.
        """
        if not check(self.o):
            return _f('fatal', 'invalid path')
        if confirm==self.o.split('/')[-1]:
            os.remove(self.o), _f('warn', f'{confirm} destroyed from {self.o}')
        else:
            _f('fatal','you did not confirm - `Receipts.destroy(confirm="file_name")`')
        