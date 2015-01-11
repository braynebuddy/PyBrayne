#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# WordNet.py - Interface to the NLTK implementation of Princeton's WordNet
#              project. http://wordnet.princeton.edu
#
# Copyright 2013-2014 Robert B. Hawkins
#
"""
SYNOPSIS
    WordNet

DESCRIPTION
    WordNet.py contains functions that are intended to be used from other
    modules to make access to Princeton's WordNet database easier. 
    (http://wordnet.princeton.edu)
    It requires that the Natural Language Toolkit (NLTK) has already been
    installed. (http://www.nltk.org)

AUTHOR
    Rob Hawkins <webwords@txhawkins.net>

LICENSE
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

VERSION
    1.0.2
"""
__author__    = "Rob Hawkins <webwords@txhawkins.net>"
__version__   = "1.0.2"
__date__      = "2014.08.17"

# Version   Date        Notes
# -------   ----------  -------------------------------------------------------
# 1.0.0     2013.12.01  Starting script template
# 1.0.1     2014-01-01  Basic shell for process_text function, switch to
#                       argParse from 
# 1.0.2     2014-08-17  Update to include in the Willie IRC bot version 
#                       of PyBrain

# get synsets
def getSynSets(word):
    from nltk.corpus import wordnet as wn
    ssets = wn.synsets(word)
    res = []
    for ss in ssets:
        res.append(ss.name)
    return res

# get part-of-speech
def getPOS(word):
    from nltk.corpus import wordnet as wn
    ssets = wn.synsets(word)
    res = []
    for ss in ssets:
        res.append(wn.synset(ss.name).pos)
    return res

def wordinfo(word):    # Look up a word's lexical information
    """Look up the lexical information for a word
        [0] = The word
        [1] = Part of speech
        [2] = WordNet synset object
        [3] = Other words (lemmas)
        [4] = Definition
    """
    from nltk.corpus import wordnet as wn
    ssets = wn.synsets(word)
    res = []
    for ss in ssets:
        s = []
        s.append(word)           # 0 - The original word
        s.append(ss.pos)         # 1 - Part of speech
        s.append(ss)             # 2 - The WordNet synset
        s.append(ss.lemma_names) # 3 - Other names
        s.append(ss.definition)  # 4 - Definition string
        res.append(s)
    return res

def SSinfo(ssName):    # Look up a word's lexical information
    """Look up the lexical information for a synset name
        [0] = The word
        [1] = Part of speech
        [2] = WordNet synset object
        [3] = Other words (lemmas)
        [4] = Definition
    """
    from nltk.corpus import wordnet as wn
    ss = wn.synset(ssName)
    res = []
    res.append(ss.lemma_names[0]) # 0 - The most common word
    res.append(ss.pos)            # 1 - Part of speech
    res.append(ss)                # 2 - The WordNet synset
    res.append(ss.lemma_names)    # 3 - Other names
    res.append(ss.definition)     # 4 - Definition string
    return res

def synonyms(word, part):    # Look up a word's synonyms
    from nltk.corpus import wordnet as wn
    ssets = wn.synsets(word)
    res = []
    for ss in ssets:
        if ss.pos == part:
            res.extend(ss.lemma_names)
    return res

def hnSSNames(ssName):
    """
    Return a list of the synset names of the immediate hypernyms of ssName
    """
    from nltk.corpus import wordnet as wn
    hnset = wn.synset(ssName).hypernyms()
    return [h.name for h in hnset]
    
def hnPathSSNames(ssName):
    """
    Return a list of lists of the synset names of the hypernym paths of ssName
    """
    from nltk.corpus import wordnet as wn
    hnpaths = wn.synset(ssName).hypernym_paths()
    return [[hp.name for hp in list(reversed(hnpaths[i]))] for i in range(len(hnpaths))]
    
def hypernyms(ss, part, found):
    """
    Return a list of the first lemma name of all of a synset's hypernyms
    """
    from nltk.corpus import wordnet as wn
    res = []
    hnset = ss.hypernyms()
    if len(hnset) > 0:
        for hn in hnset:
            if not(hn in found):
                found.append(hn)
                newword = hn.lemma_names[0]
                res.append(newword)
                res.extend(hypernyms(hn, part, found))
    return res

def hyponyms(ss, part):    # Look up a synset's hyponyms
    from nltk.corpus import wordnet as wn
    res = []
    hnset = ss.hyponyms()
    if len(hnset) > 0:
        for hn in hnset:
            res.append(hn.lemma_names[0])
    return res

def hyperpaths(ss):    # Look up a synset's hypernym paths
    from nltk.corpus import wordnet as wn
    res = []
    paths = ss.hypernym_paths()
    if len(paths) > 0:
        for p in paths:
            #p.reverse()
            s = p[-1].lemma_names[0]
            for ps in reversed(p[:-1]):
                s += '->'
                s += ps.lemma_names[0]
            res.append(s)
    return res

def isa(word1, word2):
    res = False
    pword = wordinfo(word1)
    if len(pword) > 0:
        for w in pwords:
            if w[1] == 'n':
                htree = [w[2], ]
                hypers = hypernyms(w[2], w[1], htree)
                if len(hypers) > 0:
                    for h in hypers:
                        if h == word2: res = True
    return res

if __name__ == '__main__':
    from nltk.corpus import wordnet as wn
    wnPOS = [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV]
    myword = raw_input('Enter a word: ')
    parsed_words = wordinfo(myword)
    if len(parsed_words)==0:
        print "Sorry, I don't know '%s'" % myword
    else:
        for w in parsed_words:
            print "%s (%s)" % (w[0],w[1])
            print w[2], w[3]
            print w[4]
            print "Synonyms:"
            syns = synonyms(w[0],w[1])
            if len(syns)>0:
                for s in syns[:-1]:
                    print "%s," % s,
                print syns[-1]
                if w[1] == 'n':
                    htree = [w[2], ]
                    hypers = hypernyms(w[2], w[1], htree)
                    if len(hypers) > 0:
                        print 'Hypernyms:'
                        for h in hypers[:-1]:
                            print '%s,' % h,
                        print hypers[-1]
                        print 'Hypernym Paths:'
                        hpaths = hyperpaths(w[2])
                        for p in hpaths:
                            print p
                    hypos = hyponyms(w[2], w[1])
                    if len(hypos) > 0:
                        print 'Hyponyms:'
                        for h in hypos[:-1]:
                            print '%s,' % h,
                        print hypos[-1]
            print '---------------------'

