# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

from .. import utils


__all__ = ('cli_loader',)


@utils.with_cursor
def cli_command(cursor, migrations_directory='', db_connection_string='',
                **kwargs):
    migrated_versions = dict(list(
        utils.get_schema_versions(cursor, versions_only=False)))
    migrations = utils.get_migrations(migrations_directory)

    print('{:<25} | is applied | date applied'.format('name'))
    print('-' * 70)
    for version, migration_name in migrations:
        print('{: <25}   {!s: <10}   {}'.format(
            '_'.join([version, migration_name])[:25],
            bool(version in migrated_versions),
            migrated_versions.get(version, '')))


def cli_loader(parser):
    return cli_command
