from distutils.core import setup

from setuptools import find_packages


version = '0.0.7'

setup(
    name='ooldap',
    version=version,
    packages=find_packages(),
    url='http://github.com/TAMUArch/ooldap',
    author='John',
    author_email='johnphillips@arch.tamu.edu',
    description='Object Oriented LDAP',
    license='Apache License 2.0',
)
