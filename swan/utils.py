from .fancy_print import _f
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

def check_headers(receipts):
    if receipts._schema['header'] is None:
        _f('wait','no header set - attempting `.keys()`')
        try:
            receipts._schema['header'] = list(receipts._schema['data'][0].keys())
            _f('success', f'headers detected as {receipts._schema["header"]} from `.keys()`')
            return receipts._schema['header']
        except Exception as e:
            _f('fatal', f'{e}')
            return False
    else:
        return True

def dateme(receipt):
    _t = datetime.now()
    receipt['ts']=_t
    return _f('info',f'timestamped - {_t}')

def writeme(content, path):
    with open(path, "wb") as _:
        _.write(content)
    return _f('info',f'written - {path}')

def files(content, url, types):
    _=[]
    soup = BeautifulSoup(content, "html.parser")
    urls = soup.find_all("a", href=True)
    for _u in tqdm(urls, desc=_f('wait',f'processing {url}')):
        _u = urljoin(url, _u["href"])
        if list(filter(_u.endswith, types)) != []:
            _.append(_u)
            _f('info',f'found - {_u}')
    return _