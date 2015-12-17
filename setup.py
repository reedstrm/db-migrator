# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import sys
from setuptools import setup, find_packages

install_requires = (
    'psycopg2>=2.5',
    )

tests_require = [
    ]

setup(
    name='db-migrator',
    version='0.0.1',
    author='Connexions',
    author_email='info@cnx.org',
    url='https://github.com/Connexions/db-migrator',
    license='LGPL, see also LICENSE.txt',
    description='',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'dbmigrator = dbmigrator.cli:main',
            ],
        },
    )