from setuptools import setup
import subprocess
import os
from version import get_version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
   name='scriptifier',
   version=get_version(),
   description='A Python package that allows to run a function in a separated script, seamlessly.',
   license="MIT",
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='ben981',
   author_email='beniamino.vigano@protonmail.com',
   url="https://github.com/ben981/scriptifier",
   keywords='scriptify, processify, processifier, subprocess, multiprocessing, memory, leak',
   packages=['scriptifier'],
)
