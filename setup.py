from setuptools import setup, find_packages
import os
__dir__ = os.path.dirname(os.path.abspath(__file__))
ver = '0.1.0'
print 'building... pychecker %s install package' % ver
setup(
    name="pychecker",
    version=ver,
    description="stream check Python utils",
    author="Yuanjunjie",
    url="https://github.com/kedacomresearch/pychecker",
    license="LGPL",
    packages=find_packages()
)