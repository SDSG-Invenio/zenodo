# -*- coding: utf-8 -*-
##
## This file is part of ZENODO.
## Copyright (C) 2012, 2013, 2014 CERN.
##
## ZENODO is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## ZENODO is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with ZENODO. If not, see <http://www.gnu.org/licenses/>.
##
## In applying this licence, CERN does not waive the privileges and immunities
## granted to it by virtue of its status as an Intergovernmental Organization
## or submit itself to any jurisdiction.

""" Zenodo specific authors printing. """

#import re
#from urllib import quote
import six
#from cgi import escape
from flask import current_app
#from invenio.base.i18n import gettext_set_language


def format_element(bfo, limit, separator=' ; ',
                   extension='[...]',
                   print_links="yes",
                   prefix=' (',
                   suffix=')'):
    """
    Prints the list of authors of a record.

    @param extension: a text printed if more authors than 'limit' exist
    @param print_links: if yes, prints the authors as HTML link to their publications
    @param prefix: prefix printed before each affiliation
    @param suffix: suffix printed after each affiliation
    """
#    _ = gettext_set_language(bfo.lang)    # load the right message language

    CFG_SITE_URL = current_app.config['CFG_SITE_SECURE_URL']
    if isinstance(CFG_SITE_URL, six.text_type):
        CFG_SITE_URL = CFG_SITE_URL.encode('utf8')

    trns = bfo.fields('912__')

    nb_trns = len(trns)

    return "Number of records: %s" % str(nb_trns)


def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
