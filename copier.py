import os, csv, requests
from fancy_print import _f
from utils import check_headers, dateme, writeme, files

class Copier:
    def __init__(self, url=None, recurse=False, custom=False):
        self.custom = custom
        self.recurse = recurse
        self.url = url
        return _f('fatal', 'no url passed') if self.url is None else None
    def check(self, path):
        return os.path.exists(path)
    def download(self, path=None, sneaky=True, types=None, o=False):
        _f('warn','no download path set') if path==None else None
        if sneaky:
            headers = {
                "User-Agent": "PostmanRuntime/7.23.3",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
        else:
            headers={}
        response = requests.get(self.url, headers=headers)
        safe = response.status_code==200
        self.path=path if safe else None
        if self.recurse and types and safe:
            _files = files(response.content, self.url, types)
            for _file in _files:
                _p = Copier(url=_file)
                if o and self.check(f'{self.path}/{_file.split("/")[-1]}'):
                    _p.download(f'{self.path}/{_file.split("/")[-1]}')
                elif not self.check(f'{self.path}/{_file.split("/")[-1]}'):
                    _p.download(f'{self.path}/{_file.split("/")[-1]}')
                else:
                    _f('warn',f'{_file.split("/")[-1]} already exists - set `o=True` to overwrite when downloading')
                    _files.remove(_file)
            self._files=_files
            return  _files, _f('success', f'{len(_files)} downloaded')
        return writeme(response.content, path) if safe else _f('fatal',response.status_code), False
    def destroy(self, confirm=None):
        if confirm==self.path.split('/')[-1]:
            _f('warn', f'{confirm if not self.recurse else len(self._files)} destroyed from {self.path}') if confirm is not None else None
            return [os.remove(f'{self.path}/{_file.split("/")[-1]}') for _file in self._files] if self.recurse else os.remove(self.path)
        else:
            return _f('fatal','you did not confirm - `Copier.destroy(confirm="parent_dir")`')
