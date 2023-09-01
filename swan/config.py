import os, json, shutil
from swan.utils import _f, readthis, likethis, check

class Config:
    def __init__(self, path: str = None):
        self._schema = {
            "type": "object"
            , "properties": {
                "role": { "type": "string" }
                , "settings": {
                    "name": { "type": "string" }
                    , "data_dir": { "type": "string" }
                    , "jobs": {
                        "type": "object"
                        , "properties": {
                            "url": { "type": "string" }
                            , "files": { "type": "array" }
                            , "janitor": { "type": "boolean" }
                            , "custom": { "type": "array" }
                        }
                    }
                }
            }
        }
        self.p = path if path else _f('fatal', 'path not set')
        _f('warn', f'config not found - {self.p}') if not check(self.p) else None
    def use(self):
        _c = readthis(self.p)
        _c = json.load(_c)
        if likethis(_c, self._schema):
            _f('success', f'config loaded from - {self.p}')
            self.c=_c
            return self.c
    def save(self):
        if likethis(self.c, self._schema):
            f = open(self.p, 'w')
            json.dump(self.c, f)
            return _f('success', f'config saved to - {self.p} {" (overwrite)" if check(self.p) else None}')
    def unbox(self, o: bool = False):
        if likethis(self.c, self._schema):
            _p = f'{self.c["settings"]["data_dir"]}{self.c["settings"]["name"]}'
            _f('success', f'unboxed! 🦢📦 - {_p} ') if not check(_p) or o else _f('fatal',f'exists - {_p}')