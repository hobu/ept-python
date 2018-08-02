#!/usr/bin/env python


import logging
import platform
import sys
from distutils.version import StrictVersion

import numpy
from setuptools import setup
from setuptools.extension import Extension as DistutilsExtension

logging.basicConfig()
log = logging.getLogger(__file__)

# python -W all setup.py ...
if "all" in sys.warnoptions:
    log.level = logging.DEBUG

# Get the version from the ept module
module_version = None
with open("ept/__init__.py", "r") as fp:
    for line in fp:
        if line.startswith("__version__"):
            module_version = StrictVersion(line.split("=")[1].strip().strip("\"'"))
            break

if not module_version:
    raise ValueError("Could not determine ept's version")

# Handle UTF-8 encoding of certain text files.
open_kwds = {}
if sys.version_info >= (3,):
    open_kwds["encoding"] = "utf-8"

with open("VERSION.txt", "w", **open_kwds) as fp:
    fp.write(str(module_version))

with open("README.rst", "r", **open_kwds) as fp:
    readme = fp.read()

with open("CHANGES.rst", "r", **open_kwds) as fp:
    changes = fp.read()

long_description = readme + "\n\n" + changes



setup_args = dict(
    name="ept",
    version=str(module_version),
    install_requires=["requests","lazperf","laspy"],
    description="",
    license="BSD",
    keywords="point cloud data organization",
    author="Howard Butler",
    author_email="howard@hobu.co",
    maintainer="Howard Butler",
    maintainer_email="howard@hobu.co",
    url="https://github.com/hobu/ept-python",
    long_description=long_description,
    test_suite="test",
    include_package_data=True,
    packages=["ept"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: GIS",
    ],
)
setup(**setup_args)