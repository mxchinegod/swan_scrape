import os, json, shutil
from .utils import _f, readthis, likethis, check

class Config:
    def __init__(self, config: str | dict = None):
        """
        The above function is the initialization method for a class that takes a configuration parameter
        and sets up a schema for the configuration.
        
        :param config: The `config` parameter is used to specify the configuration for the object. It
        can be either a string representing the path to a configuration file or a dictionary containing
        the configuration directly. If the `config` parameter is not provided or is set to `None`, a
        default configuration will be used
        :type config: str | dict
        """
        if type(config)==dict:
            _ = self._create(config)
            self.p = os.path.join(_,'config.json')
        else:
            self.p = os.path.abspath(config) if config else _f('fatal', 'path not set')
        _f('warn', f'config not found - {self.p}') if not check(self.p) else None
    def use(self):
        """
        The function loads a configuration file, validates it against a schema, and returns the loaded
        configuration if it is valid.
        :return: The `self.c` variable is being returned.
        """
        _c = readthis(self.p)
        _c = json.load(_c)
        if likethis(_c):
            _f('success', f'config loaded from - {self.p}')
            self.c=_c
            return self.c
    def save(self):
        """
        The function saves the configuration data to a file in JSON format and returns a success message
        with the file path.
        :return: a success message indicating that the configuration has been saved to a file. The
        message includes the file path and whether it was overwritten or not.
        """
        if likethis(self.c):
            f = open(self.p, 'w')
            json.dump(self.c, f)
            return _f('success', f'config saved to - {self.p}{" (overwrite)" if check(self.p) else None}')
    def unbox(self, o: bool = False):
        """
        The `unbox` function checks if a directory exists, and if not, creates it and copies a file into
        it.
        
        :param o: The parameter `o` is a boolean flag that determines whether to overwrite an existing
        directory when unboxing. If `o` is `True` and the directory already exists, it will be deleted
        and recreated before copying the file. If `o` is `False` (default), and the directory, defaults
        to False
        :type o: bool (optional)
        :return: a tuple containing a status and a message. The status can be either "fatal" or
        "success", and the message provides information about the result of the unboxing process.
        """
        if likethis(self.c):
            _p = os.path.join(self.c["settings"]["proj_dir"],self.c["settings"]["name"])
            if o and check(_p):
                shutil.rmtree(_p)
                os.makedirs(_p)
                shutil.copy(self.p, _p)
            elif not check(_p):
                os.makedirs(_p)
                shutil.copy(self.p, _p)
            else:
                return _f('fatal',f'exists - {_p}')
            return _f('success', f'unboxed! 🦢📦 - {_p} ')
    def _create(self, config: dict = None):
        """
        The function `_create` creates a directory based on the provided configuration and saves the
        configuration as a JSON file within the directory.
        
        :param config: The `config` parameter is a dictionary that contains the configuration settings
        for creating a project. It is an optional parameter and can be set to `None` if no configuration
        is provided
        :type config: dict
        :return: either the path `_p` if the `config` matches the schema, or a message indicating a
        fatal error if the `config` does not match the schema.
        """
        if likethis(config):
            _p = os.path.join(config["settings"]["proj_dir"],config["settings"]["name"])+'/config.json'
            if check(_p):
                return _f('fatal',f'exists - {_p}')
            else:
                os.makedirs(_p)
                f = open(os.path.join(_p, 'config.json'), 'w')
                json.dump(config, f)
            _f('success', f'unboxed! 🦢📦 using - {_p} ')
            return _p
        else:
            return _f('fatal', 'your config schema does not match the requirements')
    def destroy(self, confirm: str = None):
        """
        The `destroy` function removes a file if the confirmation matches the file name.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It should
        be set to the name of the file that you want to destroy
        :type confirm: str
        :return: a message indicating whether the file was successfully destroyed or not.
        """
        """
        The function `destroy` removes a file if the confirmation matches the file name.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It should
        be set to the name of the file that you want to destroy
        :return: a message indicating whether the file was successfully destroyed or not.
        """
        if likethis(self.c):
            if not check(self.p):
                return _f('fatal', f'invalid path - {self.p}')
            if confirm==self.c["settings"]["name"]:
                shutil.rmtree(self.p.replace('config.json','')), _f('warn', f'{confirm} destroyed')
            else:
                _f('fatal','you did not confirm - `Config.destroy(confirm="your_config_name")`')
        