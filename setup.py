#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="qbittorrent-statistics",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'notify=qbittorrent_statistics.main:main',
        ],
    },
)
