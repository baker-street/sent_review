# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__title__ = 'sent_review'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '01/20/2016'
__copyright__ = "sent_review  Copyright (C) 2015  Steven Cutting"

import os

from tyr.filesystem import name_to_id, list_files, new_dir
from tyr.interpreter import interpreter
from tyr.setssytem import init_new_set_file, add_to_set


SENT_SETS_DIR = "sent_sets"


# -----------------------------------------------------------------------------

def init_set_sent_dir():
    new_dir(name=SENT_SETS_DIR, parentid=name_to_id('/'), ownerid="ubuntu")


def get_sent_set_dir_id():
    return name_to_id(SENT_SETS_DIR)


def sent_set_dir_id():
    try:
        return get_sent_set_dir_id()
    except AssertionError:
        init_set_sent_dir()
        return sent_set_dir_id()


# -----------------------------------------------------------------------------


def create_new_sent_set_file(name):
    init_new_set_file(name=name, settype="sent_based_sent", parentid=sent_set_dir_id())


def sent_set_file_id(name):
    return name_to_id(os.path.join('/', SENT_SETS_DIR, name))


def check_if_sent_set_file_exists(name):
    try:
        sent_set_file_id(name)
        return True
    except AssertionError:
        return False


def create_sent_set_file_if_missing(name):
    if not check_if_sent_set_file_exists(name):
        create_new_sent_set_file(name)


# --------------------------------------


def load_sent_set_doc_ids(name):
    return interpreter(os.path.join('/', SENT_SETS_DIR, name))


def sent_set_doc_ids(name):
    try:
        return load_sent_set_doc_ids(name)
    except AssertionError:
        return set()


# --------------------------------------


def add_to_sent_set_file(setname, docids):
    add_to_set(list(docids), setid=sent_set_file_id(setname))
