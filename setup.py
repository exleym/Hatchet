
from setuptools import setup

setup(
    name='hatchet',
    version='0.1dev',
    packages=['hatchet',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
