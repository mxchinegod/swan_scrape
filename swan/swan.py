from .utils import _f
from os import path
from swan.config import Config
from swan.copier import Copier
from swan.receipts import Receipts
from swan.janitor import Janitor

class Swan:
    def __init__(self, config: str | dict = None):
        self.config = Config(config)
    def go(self):
        self.config.use()
        self.config.unbox()
        _f('wait', f'swanning with "{self.config.conf["settings"]["name"]}"')
        copy = Copier(self.config)
        r = Receipts(self.config)
        j = Janitor(self.config)
        data = copy.download()
        r.create(data)
        r.write()
        j.process(data)
        if self.config and copy and r and j:
            return _f('success', '🦢 done')