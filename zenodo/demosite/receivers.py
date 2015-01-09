# -*- coding: utf-8 -*-
#
## This file is part of Zenodo.
## Copyright (C) 2012, 2013, 2014, 2015 CERN.
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

import os
import shutil
from flask import current_app
from invenio.base.factory import with_app_context
from invenio.ext.sqlalchemy import db


@with_app_context(new_context=True)
def post_handler_database_create(sender, default_data='', *args, **kwargs):
    """Load data after demosite creation."""
    from invenio.modules.communities.models import Community
    from zenodo.config import CFG_MEMBER_STATES_CODES

    print(">>> Creating collections for communities...")

    for member_code in CFG_MEMBER_STATES_CODES:
        c = Community.query.filter_by(id=member_code).first()
        c.save_collections()

    print(">>> Adding user groups.")

    from invenio.modules.accounts.models import Usergroup, UserUsergroup
    from zenodo.config import CFG_MEMBER_STATES_NAMES

    for member_name in CFG_MEMBER_STATES_NAMES:
        ug = Usergroup(name=member_name, join_policy='VM', description="Submissions from %s." % member_name)
        ug.users.append(UserUsergroup(id_user=1, user_status=UserUsergroup.USER_STATUS['ADMIN']))
        db.session.add(ug)

    print(">>> Fixing dbquery for root collection.")

    from invenio.modules.search.models import Collection

    c = Collection.query.filter_by(id=1).first()
    c.dbquery = '980__a:0->Z AND NOT 980__a:PROVISIONAL AND NOT ' \
                '980__a:PENDING AND NOT 980__a:SPAM AND NOT 980__a:REJECTED ' \
                'AND NOT 980__a:DARK'
    db.session.commit()


@with_app_context(new_context=True)
def clean_data_files(sender, *args, **kwargs):
    """Clean data in directories."""
    dirs = [
        current_app.config['DEPOSIT_STORAGEDIR'],
        current_app.config['CFG_TMPDIR'],
        current_app.config['CFG_TMPSHAREDDIR'],
        current_app.config['CFG_LOGDIR'],
        current_app.config['CFG_CACHEDIR'],
        current_app.config['CFG_RUNDIR'],
        current_app.config['CFG_BIBDOCFILE_FILEDIR'],
    ]

    for d in dirs:
        print(">>> Cleaning {0}".format(d))
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)


@with_app_context(new_context=True)
def post_handler_demosite_populate(sender, default_data='', *args, **kwargs):
    """Load data after records are created."""
