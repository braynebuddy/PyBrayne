#!/usr/bin/env python
#
# brain.py - The functions of a brain
#
# Version  Date        Notes
# -------  --------    -------------------------------------------------------
#   1.0.0  2009-07-09  Separate i/o from brain functions
#	
__author__    = "Rob Hawkins (webwords@txhawkins.net)"
__version__   = "ver: 1.0.0"
__date__      = "07/09/2009 8:15 PM"
__copyright__ = "Copyright 2009 Robert B. Hawkins"

import WordNet      # WordNet interface
import lang         # Grammar and sentence parsing
import SemNet       # The Semantic Network
import ConceptNet   # MIT's ConceptNet RESTful client

# -------------------------------------------------------------------------
#class brain (object):
# -------------------------------------------------------------------------
#    """
#    A brain is a collection of data structures and functions that permit
#    understanding, learning, and reasoning about sensory inputs.
#    """
#    def __init__(self,name):

def command(sn, cmd):
    res = []
    running = True
    cwords = cmd.split()

    if cwords[0].lower() == 'shutdown':
        running = False
        res = ['Shutting down the brain...']
        sn.save_network()

    elif cwords[0].lower() == 'create':
        if len(cwords) > 1:
            sn.name = cwords[1]
        sn.create_network()
        res = ['Created brain "%s"' % sn.name]

    elif cwords[0].lower() == "shownodes":
        res = sn.show_nodes()

    elif cwords[0].lower() == "showlinks":
        res = sn.show_links()

    elif cwords[0].lower() == "shownet":
        res = sn.show_network()

    elif cwords[0].lower() == "save":
        sn.save_network()
        res = ['Saved brain "%s"' % sn.name]
    else:
        res = ['Unknown brain command: "%s"' % cmd]

    return (running, res)

def process(sn, sentence):
    res = []
    talking = True

    if len(sentence.split()) == 1:
        # a single word, so define it
        defs = lang.define(sentence)
        for d in defs:
            res.append(d)

    elif len(sentence.split()) > 1:
        # A multi-word entry, so parse it
        tree = lang.semparse(sentence)
        res.append(tree)
        res.append(lang.get_verbs(tree))
        #sNoun, rVerb, oNoun = lang.sro(sn, tree)

    if sentence.lower() == 'bye':
        talking = False
        
    return (talking, res)
