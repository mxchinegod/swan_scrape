<center>

<img style="width:150px" src="https://huggingface.co/datasets/dylanalloy/swan/resolve/main/swan.png">

# 🦢 swan

<small>🐍 toolkit for S-tier data acquisition</small>

<small>high-efficiency text & file scraper with smart tracking for building language model datasets</small>

<a href="https://huggingface.co/datasets/dylanalloy/swan" target="_blank">dataset repo on 🤗</a>

</center>

## usage

#### single file & receipt creation, then deletion

```python
from swan.copier import Copier
from swan.receipts import Receipts
data = []
copy = Copier(url='https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm')
if copy.download('./fed.txt'):
    data.append({"file":copy.url, "path":f'{copy.path}'})
receipts = Receipts(path='./fed.csv', data=data)
receipts.create(True)
receipts.write(False)
copy.destroy(confirm=copy.path.split('/')[-1])
receipts.destroy(confirm=receipts.path.split('/')[-1])
```
```shell
ℹ️ INFO: written - ./fed.txt
☕️ WAIT: no header set - attempting `.keys()`
🌊 SUCCESS: headers detected as ['file', 'path'] from `.keys()`
ℹ️ INFO: [file, path, ts] header used
ℹ️ INFO: created ./fed.csv
ℹ️ INFO: timestamped - 2023-08-31 17:07:19.544208
🌊 SUCCESS: 1 written to ./fed.csv
🚨 WARN: fed.txt destroyed from ./fed.txt
🚨 WARN: fed.csv destroyed from ./fed.csv
```

#### seek through receipts

```python
integer = receipts.seek(line=0)
string = receipts.seek(line='monetarypolicy')
by_date = receipts.seek(line='2023-08-31')
print(integer)
print(string)
print(by_date)
```
```shell
ℹ️ INFO: found monetarypolicy in data
ℹ️ INFO: found 2023-08-31 in data
{'file': 'https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', 'path': './fed.txt', 'ts': '2023-08-31 19:57:02.593086'}
[{'file': 'https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', 'path': './fed.txt', 'ts': '2023-08-31 19:57:02.593086'}]
[{'file': 'https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', 'path': './fed.txt', 'ts': '2023-08-31 19:57:02.593086'}]
```

#### recursive mode with three filetypes, and whole directory deletion

```python
from swan.copier import Copier
from swan.receipts import Receipts

copy = Copier(url='https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', recurse=True)
data=[]
files = copy.download('./fed', types=['csv','xml','pdf'])[0]
for file in files:
    data.append({"file":file, "path":f'{copy.path}/{file.split("/")[-1]}'})
receipts = Receipts('./fed.csv', data=data)
receipts.create(False)
receipts.write(False)
copy.destroy(confirm=copy.path.split('/')[-1])
receipts.destroy(confirm=receipts.path.split('/')[-1])
```
```shell
☕️ WAIT: processing https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm
100%|██████████| 326/326 [00:00<00:00, 154066.83it/s]
ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/beigebook/files/Beigebook_20170118.pdf
ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170201tealbooka20170123.pdf
ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170201tealbookb20170126.pdf
...
ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20171213SEPcompilation.pdf
ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20171213SEPkey.pdf
ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20171213meeting.pdf
ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20171213material.pdf

Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

ℹ️ INFO: written - ./fed/Beigebook_20170118.pdf
ℹ️ INFO: written - ./fed/FOMC20170201tealbooka20170123.pdf
ℹ️ INFO: written - ./fed/FOMC20170201tealbookb20170126.pdf
ℹ️ INFO: written - ./fed/FOMC20170201Agenda.pdf
ℹ️ INFO: written - ./fed/FOMC_LongerRunGoals_201701.pdf
ℹ️ INFO: written - ./fed/fomcminutes20170201.pdf
ℹ️ INFO: written - ./fed/FOMC20170201meeting.pdf
ℹ️ INFO: written - ./fed/FOMC20170201material.pdf
ℹ️ INFO: written - ./fed/Beigebook_20170301.pdf
ℹ️ INFO: written - ./fed/FOMC20170315tealbooka20170303.pdf
ℹ️ INFO: written - ./fed/FOMC20170315tealbookb20170309.pdf
ℹ️ INFO: written - ./fed/FOMC20170315Agenda.pdf
...
ℹ️ INFO: timestamped - 2023-08-31 16:40:37.573578
🌊 SUCCESS: 65 written to ./fed.csv
🚨 WARN: 65 destroyed from ./fed
🚨 WARN: fed.csv destroyed from ./fed.csv
```

#### example custom anonymous function

```python
from swan.supplies import Custom
data = 'linkbase:hello there'
SECSifter = Custom(copy=data)

SECSifter.sift = lambda _: '' if _.startswith('linkbase:') else _

sifted = SECSifter.sift(data)
print(sifted)
```
```shell
```

#### rendering markdown handler

```python
data = '<html>hello there</html>'
from swan.supplies import Broom
clean = Broom(copy=data).sweep()
print(clean)
xml = '<TITLE>hello there</TITLE>'
clean = Broom(copy=xml).sweep(xml=True)
print(clean)
```
```shell
hello there
TITLE: hello there
```

#### pure text formatter

```python
from swan.janitor import Janitor
worker = Janitor(path='./fed.txt', o='./fed_processed.txt')
worker.process()
worker.destroy(confirm=worker.o.split('/')[-1])
```
```shell
ℹ️ INFO: written - ./fed_processed.txt
🚨 WARN: fed_processed.txt destroyed from ./fed_processed.txt
```

#### dataset statistics

```python
from swan.teacher import SP

copy = './fed.txt'
save='./plot.png'

p = SP(copy, save)
p.generate(show=True)
p.destroy(confirm=p.save.split('/')[-1])
```
![SP](plot.png)
```shell
🚨 WARN: plot.png destroyed from ./plot.png
```

### advanced configuration & job planning

##### declare existing config from file
```python
from swan.config import Config
example = Config("./config.json")
```
##### put it in memory
```python
conf = example.use()
_l = lambda _: list(_)
print(_l(conf.keys()))
print(conf["settings"]["name"])
```
##### change a value & save
```python
conf["settings"]["name"] = 'example'
example.save()
```
##### remove from memory
```python
c, conf = (None, None)
```
##### load from f/s again
```python
c = Config("./config.json")
conf = c.use()
role, name = conf['role'], conf['settings']['name']
```
##### see that the value has changed
```python
print(f'{role}: {name}')
```
```shell
🌊 SUCCESS: config loaded from - ./config.json
['role', 'settings']
example
🌊 SUCCESS: config saved to - ./config.json (overwrite)
🌊 SUCCESS: config loaded from - ./config.json
server: example
```

##### overrides
```python
example.unbox(True)
example.unbox()
```

##### initialize from memory i.e. API response
```python
fin_conf = {
    "role": "server",
    "settings": {
        "name": "fin-swan",
        "proj_dir": "/Users/dylanmoore/VSCode/LLM/swan_scrape.git/",
        "jobs": [
            {
                "url": "https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm",
                "types": [],
                "janitor": 0,
                "custom": [
                    {
                        "func": ""
                        , "types": [""]
                    }
                ]
            }
        ]
    }
}
direct_load = Config(fin_conf)
direct_load.use()
direct_load.destroy('fin-swan')
```
```shell
🌊 SUCCESS: unboxed! 🦢📦 using - /Users/dylanmoore/VSCode/LLM/swan_scrape.git/fin-swan 
🌊 SUCCESS: config loaded from - /Users/dylanmoore/VSCode/LLM/swan_scrape.git/fin-swan/config.json
🚨 WARN: fin-swan destroyed
```

#### all together now 🎶
```python
# all together now 🎶
from swan.copier import Copier
from swan.receipts import Receipts
from swan.config import Config
import os

fin_conf = {
    "role": "server",
    "settings": {
        "name": "fin-swan",
        "proj_dir": "/Users/dylanmoore/VSCode/LLM/swan_scrape.git/",
        "jobs": [
            {
                "url": "https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm",
                "types": [],
                "janitor": 0,
                "custom": [
                    {
                        "func": ""
                        , "types": [""]
                    }
                ]
            }
        ]
    }
}
direct_load = Config(fin_conf)
c = direct_load.use()
p = os.path.join(c['settings']['proj_dir'], c['settings']['name'])
data = []
for job in c['settings']['jobs']:
    copy = Copier(url=job['url'])
    if copy.download(p+'/fed.txt'):
        data.append({"file":copy.url, "path":f'{copy.path}'})
receipts = Receipts(path=p+'/fed.csv', data=data)
receipts.create(True)
receipts.write(False)
```
```shell
🌊 SUCCESS: unboxed! 🦢📦 using - /Users/dylanmoore/VSCode/LLM/swan_scrape.git/fin-swan 
🌊 SUCCESS: config loaded from - /Users/dylanmoore/VSCode/LLM/swan_scrape.git/fin-swan/config.json
ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/swan_scrape.git/fin-swan/fed.txt
🚨 WARN: path not found
☕️ WAIT: no header set - attempting `.keys()`
🌊 SUCCESS: headers detected as ['file', 'path'] from `.keys()`
ℹ️ INFO: [file, path, ts] header used
ℹ️ INFO: created /Users/dylanmoore/VSCode/LLM/swan_scrape.git/fin-swan/fed.csv
ℹ️ INFO: timestamped - 2023-09-01 17:28:27.786525
🌊 SUCCESS: 1 written to /Users/dylanmoore/VSCode/LLM/swan_scrape.git/fin-swan/fed.csv
```

### 💣

```python
# that easy
direct_load.destroy('fin-swan')
```
```shell
🚨 WARN: fin-swan destroyed
```