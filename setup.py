from setuptools import setup
import subprocess
import os
from version import get_version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
   name='burner_process',
   version=get_version(),
   description="A wrapper that runs a function inside a new process, that is not a child of the main process.",
   license="MIT",
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='benvigano',
   author_email='beniamino.vigano@protonmail.com',
   url="https://github.com/benvigano/burner_process",
   keywords='subprocessing, subprocess, process, multiprocessing, processify, processifier, memory leak',
   packages=['burner_process'],
)
