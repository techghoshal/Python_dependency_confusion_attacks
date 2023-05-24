from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.0'
DESCRIPTION = 'Dependency confiuse Attack'
LONG_DESCRIPTION = 'Python package dependency confiuse vulnerability POC. Impact this vulnerability is Remote code execution(RCE) '

# Setting up
setup(
    name="Python_dependency_confusion_attacks",
    version=VERSION,
    author="techghoshal",
    author_email="techghoshal@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'discord'],
    keywords=[]
   )
