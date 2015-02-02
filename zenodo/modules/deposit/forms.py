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

from __future__ import absolute_import

import json
from datetime import datetime
#from jinja2 import Markup
from flask import request
from wtforms import validators, widgets
from wtforms.validators import ValidationError

#from invenio.config import CFG_SITE_NAME, CFG_SITE_SUPPORT_EMAIL
from invenio.config import CFG_DATACITE_DOI_PREFIX

from invenio.base.i18n import _
from invenio.utils.html import CFG_HTML_BUFFER_ALLOWED_TAG_WHITELIST
from invenio.modules.knowledge.api import get_kb_mapping
from invenio.modules.deposit.form import WebDepositForm
from invenio.modules.deposit.field_widgets import plupload_widget, \
    ExtendedListWidget, TagListWidget, TagInput, ItemWidget, \
    CKEditorWidget, ColumnInput
#    date_widget, ButtonWidget
from invenio.modules.deposit.filter_utils import strip_string, sanitize_html
from invenio.modules.deposit.validation_utils import DOISyntaxValidator, \
    invalid_doi_prefix_validator, required_if, \
    pid_validator, minted_doi_validator, unchangeable
#    list_length, not_required_if, pre_reserved_doi_validator
from invenio.modules.deposit.processor_utils import datacite_lookup, \
    PidSchemeDetection, PidNormalize, replace_field_data
from invenio.modules.deposit.autocomplete_utils import kb_autocomplete
#from ...legacy.utils.zenodoutils import create_doi, filter_empty_helper

from .autocomplete import community_autocomplete
from .validators import community_validator
from . import fields as zfields


from invenio.modules.deposit import fields


__all__ = ('ZenodoForm', )


#
# Local processors
#
local_datacite_lookup = datacite_lookup(mapping=dict(
    get_titles='title',
    get_dates='publication_date',
    get_description='description',
))


#
# Local autocomplete mappers
#
def map_result(func, mapper):
    def inner(form, field, term, limit=50):
        prefix = form._prefix
        return map(
            lambda x: mapper(x, prefix),
            func(form, field, term, limit=limit)
        )
    return inner


def communityform_mapper(obj, prefix):
    obj.update({
        'fields': {
            '%sidentifier' % prefix: obj['id'],
            '%stitle' % prefix: obj['value'],
        }
    })
    return obj


def community_obj_value(key_name):
    from invenio.modules.communities.models import Community

    def _getter(field):
        if field.data:
            obj = Community.query.filter_by(id=field.data).first()
            if obj:
                return getattr(obj, key_name)
        return None
    return _getter


def authorform_mapper(obj, prefix):
    obj.update({
        'value': "%s: %s" % (obj['name'], obj['affiliation']),
        'fields': {
            '%sname' % prefix: obj['name'],
            '%saffiliation' % prefix: obj['affiliation'],
        }
    })
    return obj


def json_projects_kb_mapper(val):
    data = json.loads(val['value'])
    grant_id = data.get('grant_agreement_number', '')
    acronym = data.get('acronym', '')
    title = data.get('title', '')
    return {
        'value': "%s - %s (%s)" % (acronym, title, grant_id),
        'fields': {
            'id': grant_id,
            'acronym': acronym,
            'title': title,
        }
    }


def grants_validator(form, field):
    if field.data:
        for item in field.data:
            val = get_kb_mapping('json_projects', str(item['id']))
            if val:
                data = json_projects_kb_mapper(val)
                item['acronym'] = data['fields']['acronym']
                item['title'] = data['fields']['title']
                continue
            raise ValidationError("Invalid grant identifier %s" % item['id'])


def grant_kb_value(key_name):
    def _getter(field):
        if field.data:
            val = get_kb_mapping('json_projects', str(field.data))
            if val:
                data = json_projects_kb_mapper(val)
                return data['fields'][key_name]
        return ''
    return _getter


#
# Subforms
#
class RelatedIdentifierForm(WebDepositForm):
    scheme = fields.StringField(
        label="",
        default='',
        widget_classes='',
        widget=widgets.HiddenInput(),
    )
    identifier = fields.StringField(
        label="",
        placeholder="e.g. 10.1234/foo.bar...",
        validators=[
            validators.optional(),
            pid_validator(),
        ],
        processors=[
            PidSchemeDetection(set_field='scheme'),
            PidNormalize(scheme_field='scheme'),
        ],
        widget_classes='form-control',
        widget=ColumnInput(class_="col-xs-4"),
    )
    relation = fields.SelectField(
        label="",
        choices=[
            ('isCitedBy', 'cites this upload'),
            ('cites', 'is cited by this upload'),
            ('isSupplementTo', 'is supplemented by this upload'),
            ('isSupplementedBy', 'is a supplement to this upload'),
            ('isNewVersionOf', 'is previous version of this upload'),
            ('isPreviousVersionOf', 'is new version of this upload'),
            ('isPartOf', 'has this upload as part'),
            ('hasPart', 'is part of this upload'),
            ('isIdenticalTo', 'is identical to upload'),
            ('isAlternativeIdentifier', 'is alternate identifier'),
        ],
        default='isSupplementTo',
        widget_classes='form-control',
        widget=ColumnInput(
            class_="col-xs-6 col-pad-0", widget=widgets.Select()
        ),
    )

    def validate_scheme(form, field):
        """Set scheme based on value in identifier."""
        from invenio.utils import persistentid
        schemes = persistentid.detect_identifier_schemes(
            form.data.get('identifier') or ''
        )
        if schemes:
            field.data = schemes[0]
        else:
            field.data = ''


class CreatorForm(WebDepositForm):
    name = fields.StringField(
        placeholder="Family name, First name",
        widget_classes='form-control',
        widget=ColumnInput(class_="col-xs-6"),
        validators=[
            required_if(
                'affiliation',
                [lambda x: bool(x.strip()), ],  # non-empty
                message="Creator name is required if you specify affiliation."
            ),
        ],
    )
    affiliation = fields.StringField(
        placeholder="Affiliation",
        widget_classes='form-control',
        widget=ColumnInput(class_="col-xs-4 col-pad-0"),
    )
    orcid = fields.StringField(
        widget=widgets.HiddenInput(),
        processors=[
            PidNormalize(scheme='orcid'),
        ],
    )

    def validate_orcid(form, field):
        if field.data:
            from invenio.utils import persistentid
            schemes = persistentid.detect_identifier_schemes(
                field.data or ''
            )
            if 'orcid' not in schemes:
                raise ValidationError("Not a valid ORCID-identifier.")


class CommunityForm(WebDepositForm):
    identifier = fields.StringField(
        widget=widgets.HiddenInput(),
        processors=[
            replace_field_data('title', community_obj_value('title')),
        ],
    )
    title = fields.StringField(
        placeholder="Start typing a community name...",
        autocomplete=community_autocomplete,
        widget=TagInput(),
        widget_classes='form-control',
    )
    provisional = fields.BooleanField(
        default=True,
        widget=widgets.HiddenInput(),
        processors=[
            replace_field_data('provisional', lambda x: x.object_data),
        ]
    )


class GrantForm(WebDepositForm):
    id = fields.StringField(
        widget=widgets.HiddenInput(),
        processors=[
            replace_field_data('acronym', grant_kb_value('acronym')),
            replace_field_data('title', grant_kb_value('title'))
        ],
    )
    acronym = fields.StringField(
        widget=widgets.HiddenInput(),
    )
    title = fields.StringField(
        placeholder="Start typing a grant number, name or abbreviation...",
        autocomplete=kb_autocomplete(
            'json_projects',
            mapper=json_projects_kb_mapper
        ),
        widget=TagInput(),
        widget_classes='form-control',
    )


#
# Form
#
class ZenodoForm(WebDepositForm):

    """Zenodo Upload Form."""

    #
    # Fields
    #
#    upload_type = zfields.UploadTypeField(
#        validators=[validators.required()],
#        hidden=True,
#        export_key='upload_type.type',
#        default='batch',
#    )
#    publication_type = fields.SelectField(
#        label='Type of publication',
#        choices=[
#            ('book', 'Book'),
#            ('section', 'Book section'),
#            ('conferencepaper', 'Conference paper'),
#            ('article', 'Journal article'),
#            ('patent', 'Patent'),
#            ('preprint', 'Preprint'),
#            ('report', 'Report'),
#            ('softwaredocumentation', 'Software documentation'),
#            ('thesis', 'Thesis'),
#            ('technicalnote', 'Technical note'),
#            ('workingpaper', 'Working paper'),
#            ('other', 'Other'),
#        ],
#        validators=[
#            required_if('upload_type', ['batch']),
#            validators.optional()
#        ],
#        #hidden=True,
#        #disabled=True,
#        export_key='upload_type.subtype',
#    )
#    image_type = fields.SelectField(
#        choices=[
#            ('figure', 'Figure'),
#            ('plot', 'Plot'),
#            ('drawing', 'Drawing'),
#            ('diagram', 'Diagram'),
#            ('photo', 'Photo'),
#            ('other', 'Other'),
#        ],
#        validators=[
#            required_if('upload_type', ['single']),
#            validators.optional()
#        ],
#        #hidden=True,
#        #disabled=True,
#        export_key='upload_type.subtype',
#    )
#
#    embargo_date = fields.Date(
#        label=_('Embargo date'),
#        icon='fa fa-calendar fa-fw',
#        description='Required only for Embargoed Access uploads. Format: '
#        'YYYY-MM-DD. The date your upload will be made publicly available '
#        'in case it is under an embargo period from your publisher.',
#        default=date.today(),
#        validators=[
#            required_if('upload_type', ['single']),
#            validators.optional()
#        ],
#        widget=date_widget,
#        widget_classes='input-small',
#        hidden=True,
#        disabled=True,
#    )

#    country = fields.TextField(
#	label=_('Member state'),
#	icon='fa fa-globe',
#	description='Memeber state that uploads the record',
#	validators=[validators.required()],
#    )

    title = fields.TitleField(
        #validators=[validators.required()],
        description='Name your upload to be able to refer to it later.',
        label='Upload name',
        filters=[
            strip_string,
        ],
        export_key='title',
        #hidden=True,
        default=datetime.isoformat(datetime.now()),
        icon='fa fa-book fa-fw',
    )

    description = fields.TextAreaField(
        label="Description",
        description='Optional.',
        default='',
        icon='fa fa-pencil fa-fw',
        #validators=[validators.required(), ],
        widget=CKEditorWidget(
            toolbar=[
                ['PasteText', 'PasteFromWord'],
                ['Bold', 'Italic', 'Strike', '-',
                 'Subscript', 'Superscript', ],
                ['NumberedList', 'BulletedList', 'Blockquote'],
                ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'RemoveFormat'],
              #  ['Mathjax', 'SpecialChar', 'ScientificChar'], ['Source'],
              #  ['Maximize'],
            ],
            disableNativeSpellChecker=False,
            extraPlugins='scientificchar,mathjax,blockquote',
            removePlugins='elementspath',
            removeButtons='',
            # Must be set, otherwise MathJax tries to include MathJax via the
            # http on CDN instead of https.
            mathJaxLib='https://cdn.mathjax.org/mathjax/latest/MathJax.js?'
                       'config=TeX-AMS-MML_HTMLorMML'
        ),
        filters=[
            sanitize_html(allowed_tag_whitelist=(
                CFG_HTML_BUFFER_ALLOWED_TAG_WHITELIST + ('span',)
            )),
            strip_string,
        ],
    )

    #
    # Collection
    #
    communities = fields.DynamicFieldList(
        fields.FormField(
            CommunityForm,
            widget=ExtendedListWidget(html_tag=None, item_widget=ItemWidget())
        ),
        validators=[
            community_validator,
            #validators.required()
        ],
        widget=TagListWidget(template="{{title}}"),
        widget_classes=' dynamic-field-list',
        icon='fa fa-globe fa-fw',
        label='Country',
        hidden=True,
        export_key='provisional_communities',
    )

    #
    # File upload field
    #

    def validate_plupload_file(form, field):
        """Ensure minimum one file is attached."""
        if not getattr(request, 'is_api_request', False):
            # Tested in API by a separate workflow task.
            if len(form.files) == 0:
                raise ValidationError("You must provide minimum one file.")
            elif sum(p.name.endswith('.ttf') for p in form.files) != 1:
                raise ValidationError("You must provide one TTF file.")

    plupload_file = fields.FileUploadField(
        label="",
        widget=plupload_widget,
        validators=[validate_plupload_file, ],
        export_key=False
    )

    #
    # Form configuration
    #
    _title = _('New upload')
    _drafting = True   # enable and disable drafting

    #
    # Grouping of fields
    #
    groups = [
    #    ('Type of file(s)', [
    #        'upload_type', 'publication_type', 'image_type', 'embargo_date',
    #    ], {'indication': 'required'}),

        ('Basic information', [
            'communities', 'title', 'description',
        ], {'indication': 'optional'}),
    ]


def filter_fields(groups):
    def _inner(element):
        element = list(element)
        element[1] = filter(lambda x: x in groups, element[1])
        return tuple(element)
    return _inner


class EditFormMixin(object):

    """Mixin class for forms that needs editing."""

    recid = fields.IntegerField(
        validators=[
            unchangeable(),
        ],
        widget=widgets.HiddenInput(),
        label=""
    )
    modification_date = fields.DateTimeField(
        validators=[
            unchangeable(),
        ],
        widget=widgets.HiddenInput(),
        label="",
    )


class ZenodoEditForm(ZenodoForm, EditFormMixin):

    """Specialized form for editing a record."""

    # Remove some fields.
#    doi = fields.DOIField(
#        label="Digital Object Identifier",
#        description="Optional. Did your publisher already assign a DOI to your"
#        " upload? If not, leave the field empty and we will register a new"
#        " DOI for you. A DOI allow others to easily and unambiguously cite"
#        " your upload.",
#        placeholder="e.g. 10.1234/foo.bar...",
#        validators=[
#            DOISyntaxValidator(),
#            minted_doi_validator(prefix=CFG_DATACITE_DOI_PREFIX),
#            invalid_doi_prefix_validator(prefix=CFG_DATACITE_DOI_PREFIX),
#        ],
#        processors=[
#            local_datacite_lookup
#        ],
#        export_key='doi',
#    )
#    prereserve_doi = None
#    plupload_file = None

    _title = _('Edit upload')
    template = "deposit/edit.html"
