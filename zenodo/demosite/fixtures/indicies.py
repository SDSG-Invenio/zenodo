# -*- coding: utf-8 -*-
#
## This file is part of Zenodo.
## Copyright (C) 2014 CERN.
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

from __future__ import absolute_import

from invenio.modules.indexer import fixtures
from zenodo.demosite.fixtures import search


class IdxINDEX_27:
        last_updated = None
        description = u'This index contains words/phrases from access rights fields.'
        stemming_language = u''
        id = 27
        indexer = u'native'
        name = u'accessrights'
        synonym_kbrs = u''
        remove_stopwords = u'No'
        remove_html_markup = u'No'
        remove_latex_markup = u'No'
        tokenizer = u'BibIndexDefaultTokenizer'
fixtures.IdxINDEXData.IdxINDEX_27 = IdxINDEX_27


class IdxINDEX_28:
        last_updated = None
        description = u'This index contains words/phrases from EU projects fields.'
        stemming_language = u''
        id = 28
        indexer = u'native'
        name = u'project'
        synonym_kbrs = u''
        remove_stopwords = u'No'
        remove_html_markup = u'No'
        remove_latex_markup = u'No'
        tokenizer = u'BibIndexDefaultTokenizer'
fixtures.IdxINDEXData.IdxINDEX_28 = IdxINDEX_28


class IdxINDEX_29:
        last_updated = None
        description = u'This index contains words/phrases from DOIs.'
        stemming_language = u''
        id = 29
        indexer = u'native'
        name = u'doi'
        synonym_kbrs = u''
        remove_stopwords = u'No'
        remove_html_markup = u'No'
        remove_latex_markup = u'No'
        tokenizer = u'BibIndexDOITokenizer'
fixtures.IdxINDEXData.IdxINDEX_29 = IdxINDEX_29


class IdxINDEX_30:
        last_updated = None
        description = u'This index TRNs.'
        stemming_language = u''
        id = 30
        indexer = u'native'
        name = u'trn'
        synonym_kbrs = u''
        remove_stopwords = u'No'
        remove_html_markup = u'No'
        remove_latex_markup = u'No'
        tokenizer = u'BibIndexDefaultTokenizer'
fixtures.IdxINDEXData.IdxINDEX_30 = IdxINDEX_30


class IdxINDEXField_27_45:
    regexp_alphanumeric_separators = u''
    regexp_punctuation = u'[.,:;?!"]'
    id_idxINDEX = fixtures.IdxINDEXData.IdxINDEX_27.id
    id_field = search.fixtures.FieldData.Field_45.id
fixtures.IdxINDEXFieldData.IdxINDEXField_27_45 = IdxINDEXField_27_45


class IdxINDEXField_28_46:
    regexp_alphanumeric_separators = u''
    regexp_punctuation = u'[.,:;?!"]'
    id_idxINDEX = fixtures.IdxINDEXData.IdxINDEX_28.id
    id_field = search.fixtures.FieldData.Field_46.id
fixtures.IdxINDEXFieldData.IdxINDEXField_28_46 = IdxINDEXField_28_46


class IdxINDEXField_29_18:
    regexp_alphanumeric_separators = u''
    regexp_punctuation = u'[.,:;?!"]'
    id_idxINDEX = fixtures.IdxINDEXData.IdxINDEX_29.id
    id_field = search.fixtures.FieldData.Field_18.id
fixtures.IdxINDEXFieldData.IdxINDEXField_29_18 = IdxINDEXField_29_18


class IdxINDEXField_30_47:
    regexp_alphanumeric_separators = u''
    regexp_punctuation = u'[.,:;?!"]'
    id_idxINDEX = fixtures.IdxINDEXData.IdxINDEX_30.id
    id_field = search.fixtures.FieldData.Field_47.id
fixtures.IdxINDEXFieldData.IdxINDEXField_30_47 = IdxINDEXField_30_47
