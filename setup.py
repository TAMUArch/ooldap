from distutils.core import setup

from setuptools import find_packages


version = '0.0.3'

setup(
    name='ooldap',
    version=version,
    packages=find_packages(),
    url='http://github.com/TAMUArch/ooldap',
    author='John',
    author_email='st_jphillips@tamu.edu',
    description='Object Oriented LDAP',
)
