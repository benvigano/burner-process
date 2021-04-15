from setuptools import setup
import subprocess
import os
from version import get_version

cf_remote_version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
assert "." in cf_remote_version

assert os.path.isfile("cf_remote/version.py")
with open("cf_remote/VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{cf_remote_version}\n")

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
   keywords='processify, processifier, script, scriptify, scriptify',
   packages=['scriptifier'],
)
