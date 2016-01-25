# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__title__ = 'sent_review'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '01/20/2016'
__copyright__ = "sent_review  Copyright (C) 2015  Steven Cutting"


from collections import defaultdict
import copy

from textquant.models.modelIO import semantic_search

import sents
import setfileIO


# --------------------------------------------------------------------------------------------------
# Load


def load_seen_set():
    return sents.past_seen_sent_pointers()


def load_sent_stream():
    return sents.random_sentences()


# --------------------------------------------------------------------------------------------------
# Get Sent


def create_get_sent(sentstream):
    """
    Create get sent function.
    """
    def get_sent():
        return sentstream.next()
    return get_sent


def new_sentence(get_sent, seenset={}):
    """
    Calls get_sent to get a new sentence and it's pointer. (excluding those in seenset)
    (pointer, sentence)
    """
    for _ in xrange(100000000):  # Basically 'while True' but with an end.
        sent = get_sent()
        if sent.pointer not in seenset:
            return sent


# --------------------------------------------------------------------------------------------------


def find_sent_semantic_matches(sentence):
    """
    Accepts the sentence text.
    Finds documents that are semantically similar and
    returns a generator that streams the document id's.
    """
    return (m for m in semantic_search(sentence))


# --------------------------------------------------------------------------------------------------


def add_sent_result(pointer, setname, seenset, docids):
    """
    Adds the resulting doc id's to the given result set.
    Adds the pointer to the seen list.
    Returns the seen list.
    """
    setfileIO.add_to_sent_set_file(setname=setname, docids=docids)
    sents.save_pointer(pointer)
    return sents.add_pointer_to_set(pointer=pointer, pointerset=seenset)


# --------------------------------------------------------------------------------------------------


class Backend(object):

    def __init__(self, **label_to_setnames):

        self.label_to_setnames = copy.deepcopy(label_to_setnames)
        self.labels = set(label_to_setnames.keys())
        self.setfiles = set(label_to_setnames.values())
        self.setfiles_docids = defaultdict(set)

        for setname in self.setfiles:
            setfileIO.create_sent_set_file_if_missing(setname)
            self.setfiles_docids[setname] = setfileIO.sent_set_doc_ids(setname)

        self.seenset = load_seen_set()
        self.get_sent = create_get_sent(load_sent_stream())
        self.current_sent = new_sentence(get_sent=self.get_sent,
                                         seenset=self.seenset)

    @property
    def sent(self):
        """
        Current sentence.
        """
        return self.current_sent.sent

    def setfile_docids_union(self, setfile, docids):
        current = self.setfiles_docids[setfile]
        self.setfiles_docids[setfile] = current.union(docids)

    def save_sent_matches(self, label):
        setname = self.label_to_setnames[label]
        setfile = self.label_to_setnames[label]
        _docids = set(find_sent_semantic_matches(self.current_sent.sent))
        docids = list(copy.deepcopy(_docids - self.setfiles_docids[setfile]))
        self.setfile_docids_union(setfile, _docids)
        self.seenset = add_sent_result(pointer=self.current_sent.pointer,
                                       setname=setname,
                                       seenset=self.seenset,
                                       docids=docids)

    def next(self):
        self.current_sent = new_sentence(get_sent=self.get_sent,
                                         seenset=self.seenset)
