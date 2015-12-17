# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

try:
    import configparser
except ImportError:
    # python 2
    import ConfigParser as configparser
import functools
import glob
import os
import psycopg2
import re


def get_settings_from_config(filename, config_names, settings):
    config = configparser.ConfigParser()
    config.read(filename)
    for name in config_names:
        setting_name = name.replace('-', '_')
        if settings.get(setting_name):
            # don't overwrite settings given from the CLI
            continue

        for section_name in config.sections():
            try:
                value = config.get(section_name, name)
                settings[setting_name] = value
                break
            except configparser.NoOptionError:
                pass


def with_cursor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not kwargs.get('db_connection_string'):
            raise Exception('db-connection-string missing')
        db_conn_str = kwargs.get('db_connection_string')
        with psycopg2.connect(db_conn_str) as db_conn:
            with db_conn.cursor() as cursor:
                return func(cursor, *args, **kwargs)
    return wrapper


def import_migration(path):
    dirname, basename = os.path.split(path)
    package_name = dirname.replace('/', '.')
    module_name = basename.rsplit('.', 1)[0]
    __import__(package_name, fromlist=[module_name])
    module = sys.modules['{}.{}'.format(package_name, module_name)]
    return module


def get_migrations(migration_directory, import_modules=False):
    python_files = os.path.join(migration_directory, '*.py')
    for path in sorted(glob.glob(python_files)):
        filename = os.path.basename(path)
        m = re.match('([0-9]+)_(.+).py$', filename)
        if m:
            version, migration_name = m.groups()
            if import_modules:
                yield version, migration_name, import_migration(path)
            else:
                yield version, migration_name