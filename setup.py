#/usr/bin/env python
import codecs
import os

from setuptools import setup, find_packages

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


setup(name="rottentomatoes",
    version="1.0.2",
    description="Rotten Tomatoes Python API",
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.md')),
    keywords="rottentomatoes movies rotten tomatoes",
    author="Zach Williams",
    author_email="hey@zachwill.com",
    url="https://github.com/zachwill/rottentomatoes",
    license="Unlicense (a.k.a. Public Domain)",
    packages=find_packages(),
    install_requires=[
      'requests==1.2.0',
    ],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'Topic :: Internet',
                 'Topic :: Internet :: WWW/HTTP',
                ],
    test_suite="test.py",
    tests_require=["mock", "Mock"])
