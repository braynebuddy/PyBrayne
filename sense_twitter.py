#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sense_twitter.py - A sensor for Twitter "mentions"
#
# Copyright 2013 Robert B. Hawkins
#
"""
SYNOPSIS

    sense_twitter [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    TODO This describes how to use this script. This docstring
    will be printed by the script if there is an error or
    if the user requests help (-h or --help).

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

    1.0.2
"""
__author__    = "Rob Hawkins <webwords@txhawkins.net>"
__version__   = "1.0.3"
__date__      = "12/07/2013 7:40 PM"

# Version   Date        Notes
# -------   ----------  -------------------------------------------------------
# 1.0.0     11/29/2013  Starting script template
# 1.0.1     11/29/2013  Interact through Twitter REST API v1.1 on RaspberryPi
#                       (https://dev.twitter.com/docs/api/1.1) using
#                       Python Twitter Tools (http://mike.verdone.ca/twitter)
# 1.0.2     11/30/2013  Separate REST API logic from sense-act logic
# 1.0.3     12//7/2013  Set up some small functions instead of a massive main()
#

import sys, os, traceback, optparse
import time
import re

import iTwitter


# Open the connection to Twitter
def connect_to_twitter():
    key1 = "yujC3tyTWH6q7XAgIvAGg"
    key2 = "FqVBCDdF4B3cA7dPKBFxwZmq2jD9hAq1dub7eRBHaY"
    creds = os.path.expanduser('~/.brayne_twitter_credentials')
    myname = "Buddy Brayne"
    return(iTwitter.iTwitter(key1, key2, creds, myname))

# Open a connection to the main brain server
def connect_to_brain()
    return

def connect_to_memory()
    
# The main test routine
def test ():
    global options, args
    print 'Hello from sense_twitter.test()!'

    t = connect_to_twitter()
    
    print
    print 'Mentions:'
    for r in t.get_mentions(num=4):
        print r['user']['screen_name'] + " (" + r['created_at'] + "): " + r['text']

    print
    print 'Timeline:'
    for r in t.get_timeline(num=3):
        print r['user']['screen_name'] + " (" + r['created_at'] + "): " + r['text']

    print
    print 'Direct Messages:'
    for r in t.get_direct_message(num=2):
        print r['sender']['screen_name'] + " (" + r['created_at'] + "): " + r['text']

def main ():
    global options, args
    if options.verbose: print 'Connecting to Twitter...'

    key1 = "yujC3tyTWH6q7XAgIvAGg"
    key2 = "FqVBCDdF4B3cA7dPKBFxwZmq2jD9hAq1dub7eRBHaY"
    creds = os.path.expanduser('~/.brayne_twitter_credentials')
    myname = "Brayne Buddy"

    t = iTwitter.iTwitter(key1, key2, creds, myname)

    if options.verbose: print 'Getting most recent mention...'
    resp = t.get_mentions(num=1)
    for r in resp:
        print r['user']['screen_name'] + " (" + r['created_at'] + "): " + r['text']

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(),
                                       usage=globals()['__doc__'],
                                       version="%prog "+__version__)
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_option ('-t', '--test', action='store_true', default=False, help='Run test suite')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        if options.test: 
            test()
        else:
            main()
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
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

