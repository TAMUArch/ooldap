from os.path import dirname, join

from distutils.core import setup

from setuptools import find_packages


version = '0.0.8'

setup(
    name='ooldap',
    version=version,
    packages=find_packages(),
    url='http://github.com/TAMUArch/ooldap',
    author='John',
    author_email='johnphillips@arch.tamu.edu',
    description='Object Oriented LDAP',
    license='Apache License 2.0',
    long_description = open(join(dirname(__file__), 'README.md')).read() + "\n" + 
                       open(join(dirname(__file__), 'HISTORY.rst')).read(),
)
