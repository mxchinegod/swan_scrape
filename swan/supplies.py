import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
from .fancy_print import _f
import docx, PyPDF2
from io import BytesIO
from swan.utils import writeme

class Broom:
    def __init__(self, copy=None):
        if copy==None:
            return _f('fatal', 'no copy/data set - `Broom(copy=text_data)`')
        else:
            self.ml=copy
    def sweep(self, xml=False):
        if xml:
            r = ET.fromstring(self.ml)
            _r = ""
            for e in r.iter():
                if e.text and e.tag:
                    try:
                        _r += f"{e.tag.split('}')[1]}: {e.text}\n"
                    except:
                        _r += f"{e.tag}: {e.text}\n"
        else:
            _s = bs(self.ml, 'html.parser')
            _r = _s.get_text(separator=' ')
        return _r
    
class Chemicals():
    def __init__(self, path=None):
        self.path = path
        return _f('fatal', 'path was not set') if path==None else None
    
    def bleach(self):
        with open(self.path, 'rb') as f:
            _r = f.read()
            try:
                if self.path.endswith('.pdf'):
                    p = PyPDF2.PdfReader(BytesIO(_r))
                    _t = "\n".join([_p.extract_text() for _p in p.pages])
                elif self.path.endswith('.docx'):
                    _d = docx.Document(BytesIO(_r))
                    _t = ""
                    for paragraph in _d.paragraphs:
                        _t += paragraph.text + '\n'
                # maybe don't need to sweep?
                # return Broom(copy=text).sweep()
                return _t
            except Exception as e:
                _f('fatal', f'document: {e} | {self.path}')

class Custom:
    def __init__(self, copy=None):
        if copy==None:
            return _f('fatal', 'no copy/data set - `Custom(copy=text_data)`')