# -*- coding: utf-8 -*-
#
## This file is part of ZENODO.
## Copyright (C) 2014 CERN.
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

import unittest
from invenio.testsuite import iter_suites


def suite():
    """Create the testsuite that has all the tests."""
    packages = [
        #'zenodo.base',
        #'zenodo.modules.github',
        'zenodo.modules.deposit',
    ]
    suite = unittest.TestSuite()
    for other_suite in iter_suites(packages=packages):
        suite.addTest(other_suite)
    return suite
