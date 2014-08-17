#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# witAI.py - A Class to handle the interface with the Wit API 
#
# Copyright 2014 Robert B. Hawkins
#
"""
SYNOPSIS

    witAI [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    This class creates an interface to the Wit web API  at
    https://api.wit.ai. It allows an app to call to send natural 
    language sentences (text) and get structured information (JSON) 
    in return.

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
    Foundation, Inc., 51 Franklin Street, Fifth Floor, 
    Boston, MA  02110-1301, USA.

VERSION

    1.0.0
"""
__author__    = "Rob Hawkins <webwords@txhawkins.net>"
__version__   = "1.0.0"
__date__      = "2014.01.01"

# Version   Date        Notes
# -------   ----------  -------------------------------------------------------
# 1.0.0     2014.01.01  Starting script template
#                       Implement simple class based on iTwitter pattern
#

import sys, os, traceback, argparse
import time
import re

import urllib, urllib2
import json
import pprint

class witAI (object):
    def __init__ (self, token_file, user_name=""):
        self.wit_token = ''
        self.wit_id = ''
        if os.path.exists(token_file):
            f = open(token_file, 'r')
            self.wit_token = f.readline().rstrip('\n')
            self.wit_id = f.readline().rstrip('\n')
            f.close()

    def get_parse (self, text_in=""):
        auth = 'Bearer ' + self.wit_token
        url = 'https://api.wit.ai/message?q=' + urllib.quote(text_in)
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/json')
        req.add_header('Authorization', auth)
        res = urllib2.urlopen(req)
        return json.load(res)

def test ():
    global args
    print 'Input string:', args.text_in
    print
    w = witAI(os.path.expanduser('~/.wit_credentials'))
    if not w:
        print 'Failed to connect to api.wit.ai'
        return

    ans = w.get_parse(args.text_in)
    print 'Full response from api.wit.ai:'
    pp = pprint.PrettyPrinter()
    pp.pprint(ans)
    if 'outcome' in ans:
        if 'intent' in ans['outcome']:
            print '\nIntent:', ans['outcome']['intent'], \
                        '(', ans['outcome']['confidence'], ')'
        if 'entities' in ans['outcome']:
            for ent in ans['outcome']['entities']:
                print 'Entity:', ent
                if isinstance(ans['outcome']['entities'][ent]['value'], dict):
                    for v in ans['outcome']['entities'][ent]['value']:
                        print 'Value',v,'=', \
                            ans['outcome']['entities'][ent]['value'][v]
                else:
                    print 'Value =', ans['outcome']['entities'][ent]['value']
    
def main ():

    global args
    print 'Hello world!'

    print 'Input string:', args.text_in
    w = witAI(os.path.expanduser('~/.wit_credentials'))
    if not w:
        print 'Failed to connect to api.wit.ai'
        return

    ans = w.get_parse(args.text_in)
    if 'outcome' in ans:
        if 'intent' in ans['outcome']:
            print 'Intent:', ans['outcome']['intent'], \
                        '(', ans['outcome']['confidence'], ')'
        if 'entities' in ans['outcome']:
            for ent in ans['outcome']['entities']:
                print 'Entity:', ent
                if isinstance(ans['outcome']['entities'][ent]['value'], dict):
                    for v in ans['outcome']['entities'][ent]['value']:
                        print 'Value',v,'=', \
                            ans['outcome']['entities'][ent]['value'][v]
                else:
                    print 'Value =', ans['outcome']['entities'][ent]['value']


if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description='This is the program description')
        parser.add_argument('--version', action='version', version='%(prog)s '+__version__)
        parser.add_argument ('-v', '--verbose', action='store_true', help='produce verbose output')
        parser.add_argument ('-t', '--test', action='store_true', help='run test suite')
        parser.add_argument ("text_in", help='a text string for testing')
        args = parser.parse_args()
        if args.verbose: print time.asctime()
        if args.test: 
            test()
        else:
            main()
        if args.verbose: print time.asctime()
        if args.verbose: print 'TOTAL TIME IN MINUTES:',
        if args.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
