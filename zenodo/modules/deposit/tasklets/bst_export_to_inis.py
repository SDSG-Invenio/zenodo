# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2014 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Invenio Tasklet.

Export records to be consumed by INIS
"""

import os
from datetime import datetime, date
from tempfile import mkstemp
from shutil import copy2
from invenio.config import CFG_TMPDIR, CFG_SITE_URL
from invenio.legacy.dbquery import run_sql
from invenio.legacy.search_engine import perform_request_search, get_fieldvalues
from invenio.legacy.bibdocfile.api import BibRecDocs
from invenio.legacy.bibsched.bibtask import write_message, \
    task_sleep_now_if_required, task_update_progress, task_low_level_submission
from invenio.modules.messages.query import create_message, send_message


def generate_msg(recid):
    msg = """A batch (record %(recid)s) that you uploaded has not passed the verification process. \n
            Please check your uploads page.\n\n
            %(site_url)s/record/%(recid)s""" % {'recid': str(recid), 'site_url': CFG_SITE_URL}
    subject = "Failed submission (record %(recid)s)" % {'recid': str(recid)}
    return (subject, msg)


def create_marcxml_header():
    """
    Creates the MARC xml header
    @return: the marcxml header
    @rtype: string
    """

    marcxml_output = '<?xml version="1.0" encoding="UTF-8"?>\n'
    marcxml_output += '<collection xmlns="http://www.loc.gov/MARC21/slim">'
    return marcxml_output


def create_marcxml_footer(marcxml_output):
    """
    Creates the MARC xml footer.
    @param marcxml_output: the final marcxml output
    @type param: string
    @return: the final marcxml output plus marcxml footer
    @rtype: string
    """

    marcxml_output += '\n</collection>\n'
    return marcxml_output


def create_marxml_validation_tag(recid, valid):
    record_spam_xml = """
                      <record>
                        <controlfield tag="001">%(recid)s</controlfield>
                        <datafield tag="911" ind1=" " ind2=" ">
                          <subfield code="a">%(valid)s</subfield>
                        </datafield>
                      </record>
                      """ % {'recid': str(recid), 'valid': str(bool(valid))}
    return record_spam_xml


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


def get_TRNs(recid):
    TRNs = []
    bibarchive = BibRecDocs(recid)
    for name in bibarchive.get_bibdoc_names():
        bibdoc = bibarchive.get_bibdoc(name)
        for bibdocfile in bibdoc.list_latest_files():
            if bibdocfile.format == '.ttf':
                f = open(bibdocfile.get_path(), 'r')
                ttf = f.read()
                f.close()
                TRNs += [ttf[i + 4:i + 13] for i in list(find_all(ttf, '001^'))]
    return TRNs


def get_fulltext_names(recid):
    names = []
    bibarchive = BibRecDocs(recid)
    for name in bibarchive.get_bibdoc_names():
        bibdoc = bibarchive.get_bibdoc(name)
        for bibdocfile in bibdoc.list_latest_files():
            if bibdocfile.format == '.pdf':
                names.append(name)
    return names


def all_file_names_in_TRNs(recid):
    TRNs = set(get_TRNs(recid))
    names = set(get_fulltext_names(recid))
    return names - TRNs == set()


def get_last_export_date():
    """
    Gets the last date in which the exporting
    task was run (date format= "%Y-%m-%d %H:%M:%S").
    """

    if os.path.isfile(CFG_TMPDIR + "/last_export_date"):
        f = open(CFG_TMPDIR + "/last_export_date", "r")
        date = f.read()
        last_export_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        f.close()
    else:
        last_export_date = "0000-00-00 00:00:00"

    return last_export_date


def store_last_export_date():
    """
    Stores the last date in which the exporting
    task was run (date format= "%Y-%m-%d %H:%M:%S").
    """

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f = open(CFG_TMPDIR + "/last_export_date", "w")
    f.write(today)
    f.close()


def get_records_to_check(recids, colls, last_checking_date):
    """
    Gets the recids of those records to be exported.
    @param recids: list of integer numbers (record ids)
    but can also contain intervals (recids='1,2-56,72')
    @param colls: list of collections (colls=',')
    """

    if not recids and not colls:
        recids_to_check = run_sql("select id from bibrec where modification_date > %s",
                                  (last_checking_date, ))
        recids_to_check = [result[0] for result in recids_to_check]

    if recids:
        recid_list = []
        cli_recid_list = recids.strip().split(',')
        for recid in cli_recid_list:
            if recid.find('-') > 0:
                rec_range = recid.split('-')
                try:
                    recid_min = rec_range[0]
                    recid_max = rec_range[1]
                    for rec in perform_request_search(p="recid:" + recid_min + "->" + recid_max):
                        recid_list.append(rec)
                except:
                    write_message("Error while trying to parse the recids argument.")
                    return False
            else:
                recid_list.append(int(recid))
        recids_to_check = recid_list

    if colls:
        cli_coll_list = colls.strip().split(',')
        recids_to_check = perform_request_search(c=cli_coll_list, )

    return recids_to_check


def bst_export_to_inis(recids="", colls="", directory=None, force=0):
    """
    Export records in redis to the especified directory.

    @param recids: the record IDs to consider
    @type recids: list
    @param directory: absolute path to the local directory.
    @type docnames: string
    @param force: do we force the creation even if the exported record already exists (1) or not (0)?
    @type force: int
    """
    force = int(force) and True or False
    if directory is None:
        directory = '/shared/'
    elif directory[-1] != '/':
        directory = directory + '/'

    directory += 'W' + str(date.today().year)[2:] + str(date.today().isocalendar()[1]) + '/'

    if not os.path.exists(directory):
        os.makedirs(directory)

    recids_to_check = get_records_to_check(recids, colls, get_last_export_date())
    store_last_export_date()

    i = 0
    marcxml_output = create_marcxml_header()

    for recid in recids_to_check:
        if all_file_names_in_TRNs(recid):
            i += 1
            try:
                bibarchive = BibRecDocs(recid)
            except Exception, e:
                write_message("Could not instantiate record #%s: %s" % (recid, e))

            write_message("Going to export record #%s" % recid)

            task_sleep_now_if_required()
            msg = "Processing recid  %s (%i/%i)" % (str(recid), i, len(recids_to_check))
            write_message(msg)
            task_update_progress(msg)

            for docname in bibarchive.get_bibdoc_names():
                try:
                    bibdoc = bibarchive.get_bibdoc(docname)
                except Exception, e:
                    write_message("Could not process docname %s: %s" % (docname, e))
                    continue

                # List all files that are not icons or subformats
                current_files = [bibdocfile.get_path() for bibdocfile in bibdoc.list_latest_files() if
                                 not bibdocfile.get_subformat() and not bibdocfile.is_icon()]

                for current_filepath in current_files:
                    if bibdocfile.format == '.ttf':
                        filename = "INIS.CC."+str(recid)+".inp"
                    else:
                        filename = docname + bibdocfile.format
                    copy2(current_filepath, directory + filename)

            marcxml_output += create_marxml_validation_tag(recid, True)

    #        f = open(str(recid) + '.xml', 'w')
    #        f.write(get_marcxml_from_record(recid))
    #        f.close()

        else:
            write_message("pdfs and TRN don't match in recid: " + str(recid))
            (subject, body) = generate_msg(recid)
            message_id = create_message(uid_from=1, users_to_str=get_fieldvalues(recid, "8560_y"), msg_subject=subject, msg_body=body)
            send_message(get_fieldvalues(recid, "8560_w"), message_id)
            marcxml_output += create_marxml_validation_tag(recid, False)

    if len(recids_to_check) > 0:
        marcxml_output = create_marcxml_footer(marcxml_output)
        current_date = datetime.now()
        file_path_fd, file_path_name = mkstemp(suffix='.xml',
                                               prefix="records_with_validation_tag_%s" %
                                               current_date.strftime("%Y-%m-%d_%H:%M:%S"),
                                               dir=CFG_TMPDIR)
        os.write(file_path_fd, marcxml_output)
        os.close(file_path_fd)
        task_low_level_submission('bibupload', 'deposit', '-a', file_path_name)

    write_message("All records successfully exported")

    return 1
