import os, csv
from .fancy_print import _f
from .utils import check_headers, dateme

class Receipts:
    def __init__(self, path, data=None, head=None):
        self.path = path
        self._schema = {
            "data": data
            , "header": head
        }
        return _f('fatal', 'data not found') if data==None else _f('warn', 'path not found') if not self.check() else None
    def check(self):
        return os.path.exists(self.path)
    def create(self, o=False, ts=True):
        _e = self.check()
        if _e and not o:
            _f('warn', f'{self.path} exists')
        with open(self.path, 'w') as _:
            io = csv.writer(_)
            check_headers(self) if self._schema['data'] is not None else None
            self._schema['header'].append('ts') if ts else None
            io.writerow(self._schema['header']) if self._schema['data'] is not None else None, _f('info', f'[{", ".join(self._schema["header"])}] header used')
        _f('info', f'created {self.path}')
    def seek(self, line=None, all=False):
        if all:
            if line is not None:
                return _f('fatal','you have `line` and `all` set')
            with open(self.path, 'r') as _:
                o = [x for x in csv.DictReader(_)]
                return o
        check_headers(self)
        _ = [x for x in csv.DictReader(open(self.path, 'r'))]
        if self._schema['data'] is None:
            return _f('fatal', 'no data passed')
        _r = []
        if isinstance(line, int):
            try:
                return _[line]
            except Exception as e:
                _f('fatal', 'index error')
        if isinstance(line, str):
            for datum in _:
                if line in datum.values():
                    _r.append(datum)
                _f('info', f'found {line} in data')
        return [x for x in _r]
    def write(self, o=False, ts=True, v=False):
        _e = self.check()
        _h = check_headers(self)
        self._schema['header'].append('ts') if ts and 'ts' not in self._schema['header'] else None
        if _e:
            with open(self.path, 'w+' if o else 'a') as _:
                io = csv.DictWriter(_) if isinstance(self._schema['data'], dict) else csv.writer(_)
                io.writerow(self._schema['header']) if _h and o else None
                [dateme(x) for x in self._schema['data']]
                [io.writerow(x.values()) for x in self._schema['data']]
                _f('success', f'{self._schema}' if v else f'{len(self._schema["data"])} written to {self.path}')
        else:
            _f('fatal', 'path not found')
    def destroy(self, confirm=None):
        if confirm==self.path.split('/')[-1]:
            os.remove(self.path), _f('warn', f'{confirm} destroyed from {self.path}') 
        else:
            _f('fatal','you did not confirm - `Receipts.destroy(confirm="file_name")`')
        