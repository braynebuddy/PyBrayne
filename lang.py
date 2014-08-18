#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# lang.py - The language parser/interpreter
#
"""
SYNOPSIS
    lang.py [-h,--help] [-v,--verbose] [--version]

DESCRIPTION
    lang.py contains functions that are intended to be used from other
    modules for natural language processing

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
# Version  Date        Notes
# -------  ----------  -------------------------------------------------------
#   0.0.1  2009-02-23  NLTK recursive-descent parser with WordNet POS info and
#                      a simple context-free grammar
#   1.0.0  2009-04-16  Add basic sentence parser for 3rd-grade grammar to be
#                      the foundation for addition of semantic parsing
#   1.0.1  2009-05-14  Subject-relation-object routine based on semantic
#                      parse results
#   1.1.0  2009-07-03  Use new semantic network class
#   1.2.0  2013-11-25  Add support for ConceptNet
#   1.2.1  2014-08-17  Update to include in the Willie IRC bot version 
#                      of PyBrain
#
__author__    = "Rob Hawkins (webwords@txhawkins.net)"
__version__   = "ver: 1.2.1"
__date__      = "08/17/2014"
__copyright__ = "Copyright 2013-2014 Robert B. Hawkins"

import nltk
import WordNet
import SemNet

# Define a single word using both WordNet and the current sematic memory
def define(word):
    res = []
    parsed_words = WordNet.wordinfo(word)
    for entry in parsed_words:
        res.append("%s (%s) [%s] %s" % (entry[0], entry[1], entry[2].name, entry[4]))
    return res

# Removes duplicates (from  http://code.activestate.com/recipes/52560)
def unique(s):
    n = len(s)
    if n == 0:
        return []
    
    u = {}
    try:
        return [u.setdefault(e,e) for e in s if e not in u]
    except TypeError:
        del u  # move on to the next method

    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()
        
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()
        
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u        

def get_verbs(tree):
    """
    Find all of the possible verbs in a parse tree. Return them in order of likelihood
    if possible
    """
    res = []
    verbs = ['VP', 'BE', 'BEZ', 'HV']
    # First, we'll simply look for the parsed verb(s) in 'tree'
    for phrase in tree:
        try:
            phrase.node
        except AttributeError:
            # it's not a node, so treat it like a tuple
            if phrase[1] in verbs:
                res.append(phrase[0])
        else:
            # phrase.node is defined, so see if it's a verb
            if phrase.node in verbs:
                s = ''
                for word in phrase.leaves():
                    s = s + word[0] + ' '
                res.append(s.strip())
    # Now look for other words in 'tree' that could be verbs
    for phrase in tree:
        try:
            phrase.leaves()
        except AttributeError:
            # it's not a node, so treat it like a tuple
            words = WordNet.wordinfo(phrase[0])
            for w in words:
                if w[1].lower() == 'v':
                    res.append(w[0])
        else:
            # phrase.leaves() is defined, so see if it might be a verb
            for word in phrase.leaves():
                words = WordNet.wordinfo(word[0])
                for w in words:
                    if w[1].lower() == 'v':
                        res.append(w[0])
    # Magic return line removes duplicates (from  http://code.activestate.com/recipes/52560)!
    #return [ u for u in res if u not in locals()['_[1]'] ]
    return unique(res)

# Identify a likely subject, verb, and object from a parse tree
def svo(sn, tree):
    s = ''
    v = ''
    o = ''
    nouns = ['NN', 'NP', 'NNS', 'PN', 'PPSS', 'PPL', 'PPO', 'PPS']

    #entity = semMem.semMem('Entities')
    #relation = semMem.semMem('Relations')
    #fact = semMem.semMem('Facts')

    for phrase in tree:
        if phrase not in tree.leaves():
            if s == '' and phrase.node == 'NX':
                for t in phrase.leaves():
                    s = s + t[0] + ' '
                    #if t[1] in nouns:
                    #    s = t[0]
            elif r == '' and phrase.node == 'VP':
                neg = False
                v = ''
                for t in phrase.leaves():
                    v = v + t[0] + ' '
                    if '~' in t[1]:
                        neg = True
                for t in phrase.leaves():
                    if neg:
                        verb = t[1][:-1]
                        if len(verb) < 1: verb = "None"
                        for k in relation.keys():
                            if verb in relation[k][1] or t[1] in relation[k][1]:
                                r = [v.strip(), str(relation[k][0])+'*']
                    else:
                        for k in relation.keys():
                            if t[1] in relation[k][1]:
                                r = [v.strip(), str(relation[k][0])]
            elif o == '' and phrase.node == 'NX':
                for t in phrase.leaves():
                    o = o + t[0] + ' '
                    #if t[1] in nouns:
                    #    o = t[0]
    #entity.shut()
    #relation.shut()
    #fact.shut()
    
    return (s.strip(), r, o.strip())

def semsplit(sentence):
    temp = nltk.wordpunct_tokenize(sentence)
    words = []
    i = 0
    while i < len(temp):
        if i<len(temp)-2 and temp[i+1]=="'":
            if temp[i+2].lower() == 're':
               words.append(temp[i])
               words.append('are')
            elif temp[i].lower() == 'i' and temp[i+2].lower() == 'm':
               words.append(temp[i])
               words.append('am')
            elif temp[i+2].lower() == 've':
               words.append(temp[i])
               words.append('have')
            else:
                words.append(temp[i]+temp[i+1]+temp[i+2])
            i += 3
        else:
            words.append(temp[i])
            i += 1
    return words

def semparse(sentence):
    import shelve

    tagdb = shelve.open('tagger.shelve')
    t2 = tagdb['t2']
    tagdb.close()

    words = semsplit(sentence)
    tagged_words = t2.tag(words)
    
    cp = nltk.RegexpParser(r"""
        NX: {<AT.*|AP\$|PP\$|NP\$|NN\$>?<JJ.*|AX>*<NN.*>+} # Article-adjective-noun
            {<PP.*[^\$]>}   # Personal pronoun
            {<DT|NN>+}      # Determiners and nouns
            {<NP>+}         # Proper nouns
        VP: {<MD.*>?<\*>?<TO>?<VB.*><\*>?}   # General verbs
            {<MD.*>?<\*>?<TO>?<BE.*><\*>?}   # Be verbs
            {<MD.*>?<\*>?<TO>?<DO.*><\*>?}   # Do verbs
            {<MD.*>?<\*>?<TO>?<HV.*><\*>?}   # Have verbs
        AX: {<QL><JJ>}      # Adjective qualifiers
            {<JJR><CS>}     # Adjective comparative
        PP: {<IN><NX>}      # Prepositional phrase
        """)
    tree = cp.parse(tagged_words, 0)

    vp = False
    for ph in tree:
        if ph not in tree.leaves() and ph.node == 'VP':
            vp = True

    tw2 = []
    for i in range(len(tagged_words)):
        if '+BE' in tagged_words[i][1]:
            pos = tagged_words[i][1][:tagged_words[i][1].find('+BE')]
            if vp:
                tw2.append((tagged_words[i][0],pos+'$'))
            else:
                tw2.append((tagged_words[i][0][:-2],pos))
                tw2.append(('is','BEZ'))
        else:
            tw2.append(tagged_words[i])
    
    return cp.parse(tw2, 0)

def qparse(sentence):
    import shelve

    tagdb = shelve.open('tagger.shelve')
#    t0 = tagdb['t0']
#    t1 = tagdb['t1']
    t2 = tagdb['t2']
    tagdb.close()

    words = nltk.wordpunct_tokenize(sentence)

    tagged_words = t2.tag(words)
    cp = nltk.RegexpParser(r"""
        NX: {<AT.*|AP|PP\$>?<JJ.*>*<NN.*>+}
            {<DT|NN>+}
            {<NP>+}
        VP: {<TO>?<VB.*>}   # General verbs
            {<BE.*>}        # Be verbs
            {<DO.*>}        # Do verbs
            {<HV.*>}        # Have verbs
        AX: {<QL><JJ><CS>}
            {<JJR><CS>}
        PP: {<IN><NX>}
        """)
    return cp.parse(tagged_words)

def qtag(word):
    import shelve

    tagdb = shelve.open('tagger.shelve')
#    t0 = tagdb['t0']
#    t1 = tagdb['t1']
    t2 = tagdb['t2']
    tagdb.close()
    return t2.tag(word)

def MakeTagger():
    import shelve
    from nltk.corpus import brown
    
    sz = int(len(brown.tagged_sents())* 0.9)
    print 'Size =', sz

    train = brown.tagged_sents()[:sz]
    test = brown.tagged_sents()[sz:]

    t0 = nltk.DefaultTagger('NN')
    print 'Default Tagger: %4.1f%%' % (100*t0.evaluate(test))

    t1 = nltk.UnigramTagger(train, backoff=t0)
    print 'Unigram Tagger: %4.1f%%' % (100*t1.evaluate(test))

    t2 = nltk.BigramTagger(train, backoff=t1)
    print 'Bigram Tagger: %4.1f%%' % (100*t2.evaluate(test))

    tagdb = shelve.open('tagger.shelve')
    tagdb['t0'] = t0
    tagdb['t1'] = t1
    tagdb['t2'] = t2
    tagdb.close()

# Words that are not in WordNet 
def SpecialWords():
    g = {}
    # Adverbs
    g['Adv'] = ['what', 'which', 'whose', 'where', 'when', 'how']
    # Determiners
    g['Det'] = ['the', 'a', 'an', "this", "that", "these", "those", "my", \
                "your", "our", "his", "her", "their", "its", "what", "which", \
                "whose", "where", "when", "most", "many", "few", "half", \
                "some", "all", "no", "one", "two", "three", "four", "five", \
                "six", "seven", "eight", "nine", "ten"]
    # Prepositions
    g['P'] = ["aboard", "about", "above", "across", "after", "against", \
              "along", "amid", "among", "anti", "around", "as", "at", \
              "before", "behind", "below", "beneath", "beside", "besides", \
              "between", "beyond", "but", "by", "concerning", \
              "considering", "despite", "down", "during", "except", \
              "excepting", "excluding", "following", "for", "from", \
              "in", "inside", "into", "like", "minus", "near", "of", \
              "off", "on", "onto", "opposite", "outside", "over", "past", \
              "per", "plus", "regarding", "round", "save", "since", \
              "than", "through", "to", "toward", "towards", "under", \
              "underneath", "unlike", "until", "up", "upon", "versus", \
              "via", "with", "within", "without"]
    # Conjunctions
    g['C'] = ["and", "or", "but", "nor", "for", "so", "yet"]
    # Proper names
    g['PropN'] = ["Rob", "Buddy"]
    # Pronouns
    g['ProN'] = ["I", "he", "she", "they", "we", "you", "it", \
                 "me", "him", "her", "them", "us", "this", \
                 "mine", "yours", "theirs", "ours", "its"]
    # Punctuation Marks
    g['Punc'] = [".", "?", ";", ":", "..."]
    return g    

def qparse1(sentence):
    words = nltk.wordpunct_tokenize(sentence)
    #wdict = {'Sentence': words}
    wdict = {}
    pos = SpecialWords()

    # translation key for WordNet POS tags
    WN_part_name = {'n':'N','v':'V','a':'Adj','s':'Adj','r':'Adv'}
    BR_part_name = {}
    

    # Look up the POS of the words
    for w in words:
        # get special POS
        for p in pos.keys():
            if (w in pos[p]) or (w.lower() in pos[p]): 
                if wdict.has_key(w):
                    if not (p in wdict[w]):
                        wdict[w].append(p)
                else:
                    wdict[w] = [p]
        # get WordNet POS
        parts = WordNet.getPOS(w)
        for p in parts:
            pn = WN_part_name[p]
            if wdict.has_key(w):
                if not (pn in wdict[w]):
                    wdict[w].append(pn)
            else:
                wdict[w] = [pn]

    print str(wdict)
    
    chunks = {'NP':[], 'VP':[], 'Unknown':[]}

    # Chunk up the NPs going from left to right using these rules:
    # NP = Det-N, (Adj)-N, Det-(Adj)-N, PropN, ProN, N
    NP = {}
    newNP = ['PropN', 'ProN', 'N', 'Det', 'Adj']
    nextNP = []

    for w in words:
        print
        print 'chunks =', str(chunks)
        print 'NP: Processing "%s" ...' % w
        chunked = False

        # Try to add the word to the current NP chunk
        for p in nextNP:
            if p in wdict[w]:
                chunked = True
                NP.append((w,p)) # Add word as a tuple
                if (p == 'Det') or (p == 'Adj'):
                    nextNP = ['N', 'Adj']
                else:
                    nextNP = []
        #if not chunked:
            
        # Try to add the word to the current VP chunk
        #if looking:
        for p in nextVP:
            if p in wdict[w]:
                looking = False
                VP.append(w)
                nextVP = []            
                break            
        
        # Try to start a new NP chunk
        #if looking:
        for p in newNP:
            if p in wdict[w]:
                looking = False
                # Save NP/VP if necessary     
                if len(NP)>0:
                    chunks['NP'].append(NP)
                #if len(VP)>0:
                #    chunks['VP'].append(VP)
                #VP = []
                #nextVP = []
                NP = [w]
                if (p == 'Det') or (p == 'Adj'):
                    nextNP = ['N', 'Adj']
                else:
                    nextNP = []            
                break            
                    
        # Try to start a new VP chunk
        #if looking:
        for p in newVP:
            if p in wdict[w]:
                looking = False
                # Save NP/VP if necessary     
                if len(nextVP)==0 and len(VP)>0:
                    chunks['VP'].append(VP)
                #if len(NP)>0:
                #    chunks['NP'].append(NP)
                #NP = []
                #nextNP = []
                VP = [w]
                if p == 'Adv':
                    nextVP = ['V']
                else:
                    nextVP = ['Adv']
                break            
    
        # Put it in unknown
        if looking:
            Unknown.append(w)
            nextNP = []
            nextVP = []            
            # Save and reset NP/VP if necessary     
            if len(NP)>0:
                chunks['NP'].append(NP)
                NP = []
            if len(VP)>0:
                chunks['VP'].append(VP)
                VP = []

        print 'NP =', str(NP)
        print 'VP =', str(VP)
        print 'Unknown =', str(Unknown)

        print 'chunks =', str(chunks)

    if len(NP)>0:
        chunks['NP'].append(NP)
    if len(VP)>0:
        chunks['VP'].append(VP)

    return chunks

def yes(word):
    from nltk.corpus import wordnet as wn
    if word.lower() == 'y':
        word = 'yes'
    if word.lower() == 'n':
        word = 'no'
    ysets = wn.synsets('affirmative')
    ysets.extend(wn.synsets('true'))
    ysets.extend(wn.synsets('agree'))
    nsets = wn.synsets('negative')
    nsets.extend(wn.synsets('false'))
    nsets.extend(wn.synsets('disagree'))
    wsets = wn.synsets(word)
    yval = -1
    nval = -1
    for w in wsets:
        for y in ysets:
            yval = max(yval, y.path_similarity(w))
        for n in nsets:
            nval = max(nval, n.path_similarity(w))
    if yval > 0 and yval > nval:
        return True
    else:
        return False

def main():
    sentence = 'Hello, my name is Buddy.'
    while sentence.lower() != 'bye':
        tree = semparse(sentence)
        sNoun, rVerb, oNoun = svo(tree)

        print 
        print tree
        print
        print 'Subject =', sNoun
        print 'Verb    =', rVerb
        print 'Object  =', oNoun
        print
        sentence = raw_input('Type a sentence: ')


if __name__ == '__main__':
    main()
