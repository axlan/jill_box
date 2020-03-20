#! /usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    import datetime
    import sys
    reload(sys).setdefaultencoding("UTF-8")
except:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    print('Please install or upgrade setuptools or pip to continue.')
    sys.exit(1)

kwargs = {}
kwargs = dict(
    version='0+d' + datetime.date.today().strftime('%Y%m%d'),
    setup_requires=['pytest-runner'], )

INSTALL_REQUIRES = [
    'flask-socketio>=4.2.1',
    'gunicorn >= 20.0.4',
]

setup(
    name='jill_box',
    description='Tools for analyzing GNSS algorithms and GNSS data',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    **kwargs)
