#!/usr/bin/env python3

"""Setuptools"""

from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

setup(
    name='subtr',
    version='0.0.4',
    description='Subtitle Translator',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Ahmad Nurus S.',
    author_email='ahmadnurus.sh@gmail.com',
    url='https://github.com/prksu/subtr',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'subtr = subtr.__main__:main'
        ]
    },
    install_requires=[
        'google-cloud-translate==1.4.0',
        'tqdm==4.31.1'
    ]
)
