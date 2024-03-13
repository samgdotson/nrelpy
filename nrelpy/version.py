from __future__ import absolute_import, division, print_function
from os.path import join as pjoin

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 3
_version_micro = 1  # use '' for first of series, number for 1 and above
# _version_extra = 'dev'
_version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: BSD License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
description = "nrelpy: A tool for accessing NREL's rich library of data."
# Long description will go up on the pypi page

NAME = "nrelpy"
MAINTAINER = "Samuel Dotson"
MAINTAINER_EMAIL = "samgdotson@gmail.com"
DESCRIPTION = description
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
URL = "http://github.com/samgdotson/nrelpy"
DOWNLOAD_URL = ""
LICENSE = "BSD-3"
AUTHOR = "Samuel Dotson"
AUTHOR_EMAIL = "samgdotson@gmail.com"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGE_DATA = {'nrelpy': [pjoin('data', '*')]}
REQUIRES = [
    'numpy',
    'pandas',
    'matplotlib',
    'pytest',
    'dill',
    'openpyxl',
    'pathlib']
PYTHON_REQUIRES = ">= 3.7"
