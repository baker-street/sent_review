# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__title__ = 'sent_review'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '01/20/2016'
__copyright__ = "sent_review  Copyright (C) 2015  Steven Cutting"


from collections import namedtuple
from copy import copy
import csv
from os.path import expanduser
from random import shuffle

from superserial.utils import psql_query, json_load


SEEN_SENT_POINTERS = "~/.seen_sent_pointers.csv"


# --------------------------------------------------------------------------------------------------


def sentence_pointers():
    """
    Collects the locations of the sentences from the database.
    """
    return list(set(sent['sentence']
                    for sent in psql_query("SELECT sentence FROM sentence_to_topic;")))


def sentence_stream_from_pointers(pointers, sortfunc=lambda a: a):
    """
    Accepts pointers (the locations) of some sentences.
    Uses the pointers to load the sentences.
    Returns a lazy stream (generator) of the sentences and pointer in a namedtuple.

    Sent(pointer="pointer", sent="sentence")
    """
    Sent = namedtuple("Sent", ['pointer', 'sent'])
    return (Sent(pointer, json_load(pointer)[2]) for pointer in sortfunc(pointers))


def sentences():
    """
    Collects the pointers (locations) of the sentences from the database.
    Uses the pointers to load the sentences.
    Returns a lazy stream (generator) of the sentences.
    """
    return sentence_stream_from_pointers(sentence_pointers())


def randomize(some_list):
    """
    Randomizes the order of the list, but not in place.

    1. Accepts a list.
    2. Creates a new copy of the supplied list.
    3. Randomizes the order of the copy.
    4. Returns the copy.
    """
    new_list = copy(some_list)
    shuffle(new_list)
    shuffle(new_list)
    shuffle(new_list)
    return new_list


def random_sentences():
    """
    Collects the pointers (locations) of the sentences from the database.
    Randomizes the order of the pointers.
    Uses the pointers to load the sentences.
    Returns a lazy stream (generator) of the sentences.
    """
    return sentence_stream_from_pointers(sentence_pointers(), sortfunc=randomize)


# --------------------------------------------------------------------------------------------------


def init_past_seen_pointers_file():
    """
    Creates the {fname} file, with the headers.
    """.format(fname=SEEN_SENT_POINTERS)
    with open(expanduser(SEEN_SENT_POINTERS), 'w') as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerow(("pointer", ))


# -----------------
# Load Seen Pointers
def load_past_seen_sent_pointers():
    """
    loads the already seen sent pointers file, parses it.
    Then returns a generator that streams the pointers.
    """
    with open(expanduser(SEEN_SENT_POINTERS), 'r') as fp:
        rows = [r for r in csv.reader(fp)]
    return (row[0] for row in rows[1:])


def past_seen_sent_pointers():
    try:
        return set(load_past_seen_sent_pointers())
    except IOError:
        init_past_seen_pointers_file()
        return set()


# -----------------
# Add pointers


def save_pointer(pointer):
    with open(expanduser(SEEN_SENT_POINTERS), 'a') as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerow((pointer, ))


def add_pointer_to_set(pointer, pointerset):
    """
    Accepts a pointer and a set.
    Adds the pointer to the set, then returns the set.
    """
    c = copy(pointerset)
    c.add(pointer)
    return c


# -----------------
# Reset Seen pointers

def clear_out_seen_pointers():
    init_past_seen_pointers_file()
