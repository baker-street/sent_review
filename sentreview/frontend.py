# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__title__ = 'sent_review'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '01/20/2016'
__copyright__ = "sent_review  Copyright (C) 2015  Steven Cutting"


from collections import namedtuple

from tyr.utils import ok_name

import backend


# --------------------------------------------------------------------------------------------------


def get_label_name():
    setfilein = unicode(raw_input('Name of Label: '))
    if ok_name(setfilein) and setfilein:
        return setfilein
    else:
        print("NAME NOT VALID! Valid Characters: a-z A-Z 0-9 _ - . @   NO-SPACES")
        return get_label_name()


def get_setfile_name():
    setfilein = unicode(raw_input('Name of Set: '))
    if ok_name(setfilein) and setfilein:
        return setfilein
    else:
        print("NAME NOT VALID! Valid Characters: a-z A-Z 0-9 _ - . @   NO-SPACES")
        return get_setfile_name()


LabelSet = namedtuple("LabelSet", ['label', 'setfile'])


def label_and_setfile_names_raw_input():
    """
    Asks the user for labels and corresponding setfile names.
    """
    print("".join(["\n",
                   "Provide a Label and then the name of the Set that will be",
                   "\n",
                   "associated with that Label.",
                   "\n",
                   "The Sets that are created will be available in the 'sent_sets' directory.",
                   "\n\n",
                   "ENTER 'done' once you are finished defining Labels.",
                   "\n"
                   ]))
    labelin = get_label_name()
    if labelin.lower() in {'done', 'exit', 'quit'}:
        return LabelSet(label="quit", setfile="quit")
    setfilein = get_setfile_name()
    return LabelSet(label=labelin, setfile=setfilein)


def _collect_label_and_setfile_names():
    labelandset = label_and_setfile_names_raw_input()
    if (labelandset.label in
        {'done', 'exit', 'quit'}) or (labelandset.setfile in
                                      {'done', 'exit', 'quit'}):
        return set()
    else:
        return {labelandset, }.union(_collect_label_and_setfile_names())


def collect_label_and_setfile_names():
    return {las.label: las.setfile for las in _collect_label_and_setfile_names()}


# --------------------------------------------------------------------------------------------------


def get_label(labelset):
    labelset = labelset.union({'done', 'exit', 'quit', 'skip'})
    label = unicode(raw_input("Label?: "))
    if label in labelset:
        return label
    else:
        print("NOT A VALID LABEL! Try again.")
        return get_label(labelset)


# --------------------------------------------------------------------------------------------------


def interface():
    label_and_setfile_names = collect_label_and_setfile_names()
    if label_and_setfile_names:
        engine = backend.Backend(**label_and_setfile_names)

        msg = "ENTER 'done' to stop."

        def apply_labels(count=0):
            # was using recursion, but this will hit the recursion limit
            while True:
                print('\n{msg}\n\n{count}\n--\n{sent}\n--\n'.format(msg=msg,
                                                                    sent=engine.sent,
                                                                    count=count))
                label = get_label(labelset=engine.labels)
                if label in {'done', 'exit', 'quit'}:
                    return True
                else:
                    if label != "skip":
                        engine.save_sent_matches(label=label)
                    try:
                        engine.next()
                        count += 1
                    except StopIteration:
                        print("Done!")
                        return True

        apply_labels(0)


# --------------------------------------------------------------------------------------------------

def reset_seen_pointers():
    backend.sents.clear_out_seen_pointers()
