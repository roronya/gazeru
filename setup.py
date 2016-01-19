from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gazeru',
    version = '1.0.0a1',
    description='A crawler for niconico',
    long_description=long_description,
    url = 'http://github.com/roronya/gazeru',
    author='roronya',
    author_email='roronya628@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='niconico crawler',
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests', 'pyquery'],
    scripts=['bin/gazeru']
)