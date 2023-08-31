import os
import matplotlib.pyplot as plt
from swan.fancy_print import _f

class SP:
    def __init__(self, copy=None, save=None):
        if copy==None:
            return _f('warn', 'no data set')
        else:
            self.path=copy
            self.save=save
    def r(self, c):
        wc, fs = len(set(c.split())), len(c)
        return wc, fs
    def p(self, n, w, s):
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 1, 1)
        plt.bar(n, [_/1000 for _ in w], color='skyblue')
        plt.ylabel('Vocab Size in thousands')
        plt.title('Vocab Size (K)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.subplot(2, 1, 2)
        plt.bar(n, [_/(1024**3) for _ in s], color='lightgreen')
        plt.ylabel('File Size in GB')
        plt.title('File Size (GB)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
    def g(self, fp):
        if os.path.exists(fp):
            with open(fp, 'r') as f:
                content = f.read()
                wc, fs = self.r(content)
                return [(os.path.basename(fp), wc, fs)]
        else:
            return _f('fatal', f"File '{fp}' not found.")
    def generate(self, show):
        fd = self.g(self.path)
        n = [f[0] for f in fd]
        w = [f[1] for f in fd]
        s = [f[2] for f in fd]
        self.p(n, w, s)
        plt.savefig(self.save) if self.save else None
        plt.show() if show else None
    def destroy(self, confirm=None):
        if confirm==self.save.split('/')[-1]:
            os.remove(self.save), _f('warn', f'{confirm} destroyed from {self.save}') 
        else:
            _f('fatal','you did not confirm - `SP.destroy(confirm="file_name")`')
