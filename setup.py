from setuptools import setup, find_packages
with open('README.rst') as f:
readme = f.read()
with open('LICENSE') as f:
license = f.read()
setup(
name='python-image',
version='0.1.0',
description='project for OCT',
long_description=readme,
author='Alexander Sovetsky',
license=license,
packages=find_packages(exclude=('tests', 'docs'))
)
