# -*- coding: utf-8 -*-
#
## This file is part of Zenodo.
## Copyright (C) 2012, 2013, 2014 CERN.
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


@with_app_context(new_context=True)
def post_handler_database_create(sender, default_data='', *args, **kwargs):
    """Load data after demosite creation."""
    from invenio.modules.communities.models import Community

    print(">>> Creating collections for communities...")

    c = Community.query.filter_by(id="AFG").first()
    c.save_collections()

    c = Community.query.filter_by(id="ALB").first()
    c.save_collections()

    c = Community.query.filter_by(id="DZA").first()
    c.save_collections()

    c = Community.query.filter_by(id="ARG").first()
    c.save_collections()

    c = Community.query.filter_by(id="ARM").first()
    c.save_collections()

    c = Community.query.filter_by(id="AUS").first()
    c.save_collections()

    c = Community.query.filter_by(id="AUT").first()
    c.save_collections()

    c = Community.query.filter_by(id="AZE").first()
    c.save_collections()

    c = Community.query.filter_by(id="BGD").first()
    c.save_collections()

    c = Community.query.filter_by(id="BLR").first()
    c.save_collections()

    c = Community.query.filter_by(id="BEL").first()
    c.save_collections()

    c = Community.query.filter_by(id="BEN").first()
    c.save_collections()

    c = Community.query.filter_by(id="BOL").first()
    c.save_collections()

    c = Community.query.filter_by(id="BIH").first()
    c.save_collections()

    c = Community.query.filter_by(id="BWA").first()
    c.save_collections()

    c = Community.query.filter_by(id="BRA").first()
    c.save_collections()

    c = Community.query.filter_by(id="BGR").first()
    c.save_collections()

    c = Community.query.filter_by(id="BFA").first()
    c.save_collections()

    c = Community.query.filter_by(id="CMR").first()
    c.save_collections()

    c = Community.query.filter_by(id="CAN").first()
    c.save_collections()

    c = Community.query.filter_by(id="CAF").first()
    c.save_collections()

    c = Community.query.filter_by(id="TCD").first()
    c.save_collections()

    c = Community.query.filter_by(id="CHL").first()
    c.save_collections()

    c = Community.query.filter_by(id="CHN").first()
    c.save_collections()

    c = Community.query.filter_by(id="COL").first()
    c.save_collections()

    c = Community.query.filter_by(id="CRI").first()
    c.save_collections()

    c = Community.query.filter_by(id="HRV").first()
    c.save_collections()

    c = Community.query.filter_by(id="CUB").first()
    c.save_collections()

    c = Community.query.filter_by(id="CYP").first()
    c.save_collections()

    c = Community.query.filter_by(id="CZE").first()
    c.save_collections()

    c = Community.query.filter_by(id="CIV").first()
    c.save_collections()

    c = Community.query.filter_by(id="COD").first()
    c.save_collections()

    c = Community.query.filter_by(id="DNK").first()
    c.save_collections()

    c = Community.query.filter_by(id="ECU").first()
    c.save_collections()

    c = Community.query.filter_by(id="EGY").first()
    c.save_collections()

    c = Community.query.filter_by(id="SLV").first()
    c.save_collections()

    c = Community.query.filter_by(id="EST").first()
    c.save_collections()

    c = Community.query.filter_by(id="ETH").first()
    c.save_collections()

    c = Community.query.filter_by(id="FIN").first()
    c.save_collections()

    c = Community.query.filter_by(id="FRA").first()
    c.save_collections()

    c = Community.query.filter_by(id="GAB").first()
    c.save_collections()

    c = Community.query.filter_by(id="GEO").first()
    c.save_collections()

    c = Community.query.filter_by(id="DEU").first()
    c.save_collections()

    c = Community.query.filter_by(id="GHA").first()
    c.save_collections()

    c = Community.query.filter_by(id="GRC").first()
    c.save_collections()

    c = Community.query.filter_by(id="GTM").first()
    c.save_collections()

    c = Community.query.filter_by(id="HTI").first()
    c.save_collections()

    c = Community.query.filter_by(id="HUN").first()
    c.save_collections()

    c = Community.query.filter_by(id="IND").first()
    c.save_collections()

    c = Community.query.filter_by(id="IDN").first()
    c.save_collections()

    c = Community.query.filter_by(id="IRN").first()
    c.save_collections()

    c = Community.query.filter_by(id="IRQ").first()
    c.save_collections()

    c = Community.query.filter_by(id="IRL").first()
    c.save_collections()

    c = Community.query.filter_by(id="ISR").first()
    c.save_collections()

    c = Community.query.filter_by(id="ITA").first()
    c.save_collections()

    c = Community.query.filter_by(id="JPN").first()
    c.save_collections()

    c = Community.query.filter_by(id="JOR").first()
    c.save_collections()

    c = Community.query.filter_by(id="KAZ").first()
    c.save_collections()

    c = Community.query.filter_by(id="KEN").first()
    c.save_collections()

    c = Community.query.filter_by(id="PRK").first()
    c.save_collections()

    c = Community.query.filter_by(id="KWT").first()
    c.save_collections()

    c = Community.query.filter_by(id="KGZ").first()
    c.save_collections()

    c = Community.query.filter_by(id="LVA").first()
    c.save_collections()

    c = Community.query.filter_by(id="LBN").first()
    c.save_collections()

    c = Community.query.filter_by(id="LBY").first()
    c.save_collections()

    c = Community.query.filter_by(id="LTU").first()
    c.save_collections()

    c = Community.query.filter_by(id="LUX").first()
    c.save_collections()

    c = Community.query.filter_by(id="MDG").first()
    c.save_collections()

    c = Community.query.filter_by(id="MYS").first()
    c.save_collections()

    c = Community.query.filter_by(id="MLI").first()
    c.save_collections()

    c = Community.query.filter_by(id="MRT").first()
    c.save_collections()

    c = Community.query.filter_by(id="MUS").first()
    c.save_collections()

    c = Community.query.filter_by(id="MEX").first()
    c.save_collections()

    c = Community.query.filter_by(id="MNG").first()
    c.save_collections()

    c = Community.query.filter_by(id="MAR").first()
    c.save_collections()

    c = Community.query.filter_by(id="MOZ").first()
    c.save_collections()

    c = Community.query.filter_by(id="MMR").first()
    c.save_collections()

    c = Community.query.filter_by(id="NAM").first()
    c.save_collections()

    c = Community.query.filter_by(id="NLD").first()
    c.save_collections()

    c = Community.query.filter_by(id="NZL").first()
    c.save_collections()

    c = Community.query.filter_by(id="NIC").first()
    c.save_collections()

    c = Community.query.filter_by(id="NER").first()
    c.save_collections()

    c = Community.query.filter_by(id="NGA").first()
    c.save_collections()

    c = Community.query.filter_by(id="NOR").first()
    c.save_collections()

    c = Community.query.filter_by(id="OMN").first()
    c.save_collections()

    c = Community.query.filter_by(id="PAK").first()
    c.save_collections()

    c = Community.query.filter_by(id="PAN").first()
    c.save_collections()

    c = Community.query.filter_by(id="PRY").first()
    c.save_collections()

    c = Community.query.filter_by(id="PER").first()
    c.save_collections()

    c = Community.query.filter_by(id="PHL").first()
    c.save_collections()

    c = Community.query.filter_by(id="POL").first()
    c.save_collections()

    c = Community.query.filter_by(id="PRT").first()
    c.save_collections()

    c = Community.query.filter_by(id="QAT").first()
    c.save_collections()

    c = Community.query.filter_by(id="MDA").first()
    c.save_collections()

    c = Community.query.filter_by(id="ROU").first()
    c.save_collections()

    c = Community.query.filter_by(id="RUS").first()
    c.save_collections()

    c = Community.query.filter_by(id="SAU").first()
    c.save_collections()

    c = Community.query.filter_by(id="SEN").first()
    c.save_collections()

    c = Community.query.filter_by(id="SRB").first()
    c.save_collections()

    c = Community.query.filter_by(id="SYC").first()
    c.save_collections()

    c = Community.query.filter_by(id="SLE").first()
    c.save_collections()

    c = Community.query.filter_by(id="SGP").first()
    c.save_collections()

    c = Community.query.filter_by(id="SVK").first()
    c.save_collections()

    c = Community.query.filter_by(id="SVN").first()
    c.save_collections()

    c = Community.query.filter_by(id="ZAF").first()
    c.save_collections()

    c = Community.query.filter_by(id="ESP").first()
    c.save_collections()

    c = Community.query.filter_by(id="LKA").first()
    c.save_collections()

    c = Community.query.filter_by(id="SDN").first()
    c.save_collections()

    c = Community.query.filter_by(id="SWE").first()
    c.save_collections()

    c = Community.query.filter_by(id="CHE").first()
    c.save_collections()

    c = Community.query.filter_by(id="SYR").first()
    c.save_collections()

    c = Community.query.filter_by(id="TJK").first()
    c.save_collections()

    c = Community.query.filter_by(id="THA").first()
    c.save_collections()

    c = Community.query.filter_by(id="MKD").first()
    c.save_collections()

    c = Community.query.filter_by(id="TUN").first()
    c.save_collections()

    c = Community.query.filter_by(id="TUR").first()
    c.save_collections()

    c = Community.query.filter_by(id="UGA").first()
    c.save_collections()

    c = Community.query.filter_by(id="UKR").first()
    c.save_collections()

    c = Community.query.filter_by(id="ARE").first()
    c.save_collections()

    c = Community.query.filter_by(id="GBR").first()
    c.save_collections()

    c = Community.query.filter_by(id="TZA").first()
    c.save_collections()

    c = Community.query.filter_by(id="USA").first()
    c.save_collections()

    c = Community.query.filter_by(id="URY").first()
    c.save_collections()

    c = Community.query.filter_by(id="UZB").first()
    c.save_collections()

    c = Community.query.filter_by(id="VEN").first()
    c.save_collections()

    c = Community.query.filter_by(id="VNM").first()
    c.save_collections()

    c = Community.query.filter_by(id="YEM").first()
    c.save_collections()

    c = Community.query.filter_by(id="ZMB").first()
    c.save_collections()

    c = Community.query.filter_by(id="ZWE").first()
    c.save_collections()

    c = Community.query.filter_by(id="AU").first()
    c.save_collections()

    c = Community.query.filter_by(id="AAEA").first()
    c.save_collections()

    c = Community.query.filter_by(id="ABACC").first()
    c.save_collections()

    c = Community.query.filter_by(id="EC").first()
    c.save_collections()

    c = Community.query.filter_by(id="CERN").first()
    c.save_collections()

    c = Community.query.filter_by(id="FAO").first()
    c.save_collections()

    c = Community.query.filter_by(id="IAEA").first()
    c.save_collections()

    c = Community.query.filter_by(id="ICSTI").first()
    c.save_collections()

    c = Community.query.filter_by(id="ICRP").first()
    c.save_collections()

    c = Community.query.filter_by(id="IIASA").first()
    c.save_collections()

    c = Community.query.filter_by(id="ISO").first()
    c.save_collections()

    c = Community.query.filter_by(id="JINR").first()
    c.save_collections()

    c = Community.query.filter_by(id="MERRCAC").first()
    c.save_collections()

    c = Community.query.filter_by(id="NEA").first()
    c.save_collections()

    c = Community.query.filter_by(id="CTBTO").first()
    c.save_collections()

    c = Community.query.filter_by(id="SESAME").first()
    c.save_collections()

    c = Community.query.filter_by(id="UNIDO").first()
    c.save_collections()

    c = Community.query.filter_by(id="UNSCEAR").first()
    c.save_collections()

    c = Community.query.filter_by(id="WONUC").first()
    c.save_collections()

    c = Community.query.filter_by(id="WEC").first()
    c.save_collections()

    c = Community.query.filter_by(id="WHO").first()
    c.save_collections()

    c = Community.query.filter_by(id="WMO").first()
    c.save_collections()

    c = Community.query.filter_by(id="WNA").first()
    c.save_collections()

    c = Community.query.filter_by(id="WNU").first()
    c.save_collections()

    print(">>> Fixing dbquery for root collection.")

    from invenio.modules.search.models import Collection
    from invenio.ext.sqlalchemy import db
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
