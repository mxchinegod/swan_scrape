import os, requests
from .fancy_print import _f
from .utils import writeme, files

class Copier:
    def __init__(self, url=None, recurse=False, custom=False):
        """
        The function initializes an object with optional parameters and checks if a URL is provided.
        
        :param url: The `url` parameter is used to specify the URL of a webpage that you want to process
        or scrape data from
        :param recurse: The `recurse` parameter is a boolean flag that determines whether the code
        should recursively process the URL. If `recurse` is set to `True`, the code will process the URL
        and all its subpages recursively. If `recurse` is set to `False`, the code will only, defaults
        to False (optional)
        :param custom: The "custom" parameter is a boolean flag that indicates whether the code should
        use custom settings or not. If it is set to True, the code will use custom settings. If it is
        set to False, the code will use default settings, defaults to False (optional)
        :return: If the `url` parameter is `None`, the function will return a call to `_f('fatal', 'no
        url passed')`. Otherwise, it will return `None`.
        """
        self.custom = custom
        self.recurse = recurse
        self.url = url
        return _f('fatal', 'no url passed') if self.url is None else None
    def check(self, path):
        """
        The function checks if a given path exists.
        
        :param path: The path parameter is a string that represents the file or directory path that you
        want to check for existence
        :return: a boolean value indicating whether the given path exists or not.
        """
        return os.path.exists(path)
    def download(self, path=None, sneaky=True, types=None, o=False):
        """
        The `download` function is used to download files from a given URL, with options for specifying
        the download path, headers, and file types.
        
        :param path: The `path` parameter is used to specify the directory where the downloaded file
        will be saved. If no path is provided, a warning message will be displayed
        :param sneaky: The `sneaky` parameter is a boolean flag that determines whether to use sneaky
        headers when making the HTTP request. If `sneaky` is `True`, the request will include headers
        that mimic a common user agent (PostmanRuntime/7.23.3) and accept various, defaults to True
        (optional)
        :param types: The `types` parameter is used to specify the file types that you want to download.
        It is used in conjunction with the `recurse` parameter to recursively download files of the
        specified types from the URL
        :param o: The 'o' parameter is a boolean flag that determines whether to overwrite existing
        files when downloading. If 'o' is set to True, existing files will be overwritten. If 'o' is set
        to False, a warning message will be displayed and the file will not be downloaded if it already
        exists, defaults to False (optional)
        :return: either a tuple containing the downloaded files and a success message, or it returns an
        error message and False.
        """
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
        """
        The `destroy` function deletes files or directories based on a confirmation and a specified
        path.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of files or
        directories. It should be set to the name of the parent directory that you want to confirm the
        destruction of
        :return: The code is returning a list comprehension that removes files from a directory if the
        confirmation matches the last part of the directory path. If the confirmation does not match, it
        returns a fatal error message.
        """
        if confirm==self.path.split('/')[-1]:
            _f('warn', f'{confirm if not self.recurse else len(self._files)} destroyed from {self.path}') if confirm is not None else None
            return [os.remove(f'{self.path}/{_file.split("/")[-1]}') for _file in self._files] if self.recurse else os.remove(self.path)
        else:
            return _f('fatal','you did not confirm - `SP.destroy(confirm="parent_dir")`')
