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
                    , "proj_dir": { "type": "string" }
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
            _p = os.path.join(self.c["settings"]["proj_dir"],self.c["settings"]["name"])
            if o and check(_p):
                shutil.rmtree(_p)
                os.mkdir(_p)
                shutil.copy(self.p, _p)
            elif not check(_p):
                os.mkdir(_p)
                shutil.copy(self.p, _p)
            else:
                return _f('fatal',f'exists - {_p}')
            return _f('success', f'unboxed! 🦢📦 - {_p} ')
    def create(self, config: dict = None):
        if likethis(config, self._schema):
            _p = os.path.join(config["settings"]["proj_dir"],config["settings"]["name"])
            if check(_p):
                return _f('fatal',f'exists - {_p}')
            else:
                os.mkdir(_p)
                f = open(os.path.join(_p, 'config.json'), 'w')
                json.dump(config, f)
            return _f('success', f'unboxed! 🦢📦 using - {_p} ')
        else:
            return _f('fatal', 'your config schema does not match the requirements')
    def destroy(self, confirm: str = None):
        """
        The function `destroy` removes a file if the confirmation matches the file name.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It should
        be set to the name of the file that you want to destroy
        :return: a message indicating whether the file was successfully destroyed or not.
        """
        if not check(self.p):
            return _f('fatal', f'invalid path - {self.p}')
        if confirm==self.c["settings"]["name"]:
            shutil.rmtree(self.p.replace('config.json','')), _f('warn', f'{confirm} destroyed')
        else:
            _f('fatal','you did not confirm - `Config.destroy(confirm="your_config_name")`')
        