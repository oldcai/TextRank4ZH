# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup


LONGDOC = """
Please go to https://github.com/someus/TextRank4ZH for more info.
"""

install_requires = []
dependency_links = []
with open('requirements.txt') as reqs:
    for line in reqs.read().split('\n'):
        if line and not line.startswith('#'):
            if '#' in line:
                dependency_links.append(line)
            else:
                install_requires.append(line)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

packages = find_packages()

setup(
    name='textrank4zh',
    version='0.4',
    description='Extract keywords and abstract Chinese article',
    long_description=LONGDOC,
    author='Letian Sun',
    author_email='sunlt1699@gmail.com',
    url='https://github.com/someus/TextRank4ZH',
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='NLP,Chinese,Keywords extraction, Abstract extraction',
    install_requires=install_requires,
    dependency_links=dependency_links,
    packages=packages,
    package_dir={'textrank4zh': 'textrank4zh'},
    package_data={'textrank4zh': ['*.txt']},
)