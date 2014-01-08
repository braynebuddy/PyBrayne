#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# process_text.py - Process some text. Extract the meanings and/or 
# concepts contained in the text.
#
# Copyright 2014 Robert B. Hawkins
#
"""
SYNOPSIS

    process_text [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    process_text takes a text string as input. It extracts the "meaning"
    in the form of:
	    - intents (per wit.ai)
        - concepts
        - entities or values ("objects" perhaps?)

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

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

    1.0.0
"""
__author__    = "Rob Hawkins <webwords@txhawkins.net>"
__version__   = "1.0.1"
__date__      = "2014.01.01"

# Version   Date        Notes
# -------   ----------  -------------------------------------------------------
# 1.0.0     2013.12.01  Starting script template
# 1.0.1     2014-01-01  Basic shell for process_text function, switch to
#                       argParse from 
#

import sys, os, traceback, argparse
import time
import re

import witAI

wolfram_appname = 'brainbuddy'
wolfram_appid = 'E2W845-J3UWUE2UK9'

def connect_wit():
    creds = os.path.expanduser('~/.wit_credentials')
    return witAI.witAI(creds)
    
def show_processed(ans):
    if not isinstance(ans, dict):
        return
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
    
def test ():
    global args
    print 'Hello from the test() function!'
    print 'Here is the text you sent me:', args.text_in

def main ():

    global args

    w = connect_wit()
    show_processed(w.get_parse(args.text_in))

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description='Process some text. Extract the meanings and/or concepts contained in the text.')
        parser.add_argument ('--version', action='version', version='%(prog)s '+__version__)
        parser.add_argument ('-v', '--verbose', action='store_true', help='produce verbose output')
        parser.add_argument ('-t', '--test', action='store_true', help='run test suite')
        parser.add_argument ("text_in", help='the text string to be processed')
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
