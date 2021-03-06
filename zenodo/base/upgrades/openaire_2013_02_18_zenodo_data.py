# -*- coding: utf-8 -*-
#
## This file is part of Zenodo.
## Copyright (C) 2012, 2013 CERN.
##
## Zenodo is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Zenodo is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Zenodo. If not, see <http://www.gnu.org/licenses/>.
##
## In applying this licence, CERN does not waive the privileges and immunities
## granted to it by virtue of its status as an Intergovernmental Organization
## or submit itself to any jurisdiction.

from invenio.legacy.dbquery import run_sql


depends_on = ['openaire_release_initial']


def info():
    return "Zenodo data migration"


def do_upgrade():
    from invenio import config

    # Portalboxes upgrade
    run_sql("""DELETE FROM collection_portalbox WHERE id_portalbox=1 or id_portalbox=2;""")
    run_sql("""DELETE FROM portalbox WHERE id=1 or id=2;""")

    # Main collection name
    run_sql("UPDATE collection SET name=%s WHERE id=1", (config.CFG_SITE_NAME,))

    # Available tabs
    run_sql("""DELETE FROM collectiondetailedrecordpagetabs;""")
    for r in run_sql("""SELECT id FROM collection"""):
        run_sql("""INSERT INTO collectiondetailedrecordpagetabs VALUES (%s,'usage;comments;metadata;files')""", r)


def estimate():
    return 1
