# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='MKBRUTUS',
    version='1.0.2',
    scripts=['mkbrutus.py'],
    description='Password bruteforcer for MikroTik devices',
    url='https://github.com/mkbrutusproject/mkbrutus',
    author='Ramiro Caire',
    author_email='ramiro.caire@gmail.com',
    license='AGPL',
    install_requires=[
        'docopt==0.6.2',
        'PyPrind==2.9.3',
        'RouterOS-api==0.13'
    ]
)
