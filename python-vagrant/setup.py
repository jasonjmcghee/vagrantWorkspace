
import os
import re
from setuptools import setup, find_packages

# parse version from package/module without importing or evaluating the code
with open('vagrant.py') as fh:
    for line in fh:
        m = re.search(r"^__version__ = '(?P<version>[^']+)'$", line)
        if m:
            version = m.group('version')
            break

setup(
    name = 'python-vagrant',
    version = version,
    license = 'MIT',
    description = 'Python bindings for interacting with Vagrant virtual machines.',
    long_description = open(os.path.join(os.path.dirname(__file__), 
                                         'README.md')).read(),
    keywords = 'python virtual machine box vagrant virtualbox vagrantfile',
    url = 'https://github.com/todddeluca/python-vagrant',
    author = 'Todd Francis DeLuca',
    author_email = 'todddeluca@yahoo.com',
    classifiers = ['License :: OSI Approved :: MIT License',
                   'Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                  ],
    py_modules = ['vagrant'],
)

