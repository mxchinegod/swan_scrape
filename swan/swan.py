from .utils import _f, check
import os, shutil
from swan.config import Config
from swan.copier import Copier
from swan.receipts import Receipts
from swan.janitor import Janitor

class Swan:
    def __init__(self, config: str | dict = None):
        self.runs = []
        self.config = Config(config)
    def go(self):
        self.config.use()
        self.config.unbox()
        _f('wait', f'swanning with "{self.config.conf["settings"]["name"]}"')
        copy = Copier(self.config)
        r = Receipts(self.config)
        j = Janitor(self.config)
        data = copy.download()
        print(data)
        r.create(data)
        r.write()
        j.process(data)
        if self.config and copy and r and j:
            _f('success', '🦢 done')
            self.runs.append({
                "config": self.config
                , "copier": copy
                , "receipts": r
                , "janitor": j
                , "data": data
                , "status": 'complete'
            })
            return {
                "config": self.config
                , "copier": copy
                , "receipts": r
                , "janitor": j
                , "data": data
                , "status": 'complete'
            }
            # handle missing or broken objects in the runs
    def destroy(self, confirm:str = None):
        if not check(os.path.join(self.config.conf['settings']['proj_dir'], self.config.conf['settings']['name'])):
            return _f('fatal', f'invalid path - {self.p}')
        if confirm==self.config.conf["settings"]["name"]:
            shutil.rmtree(os.path.join(self.config.conf['settings']['proj_dir'], self.config.conf['settings']['name'])), _f('warn', f'{confirm} destroyed')
        else:
            _f('fatal','you did not confirm - `Swan.destroy("your_config_name")`')