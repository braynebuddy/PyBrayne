#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# iTwitter.py - An interface class for the Twitter REST API
#
# Copyright 2013 Robert B. Hawkins
#
"""
SYNOPSIS

    iTwitter [-h,--help] [-v,--verbose] [-t, --test] [--version]

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
__version__   = "1.0.2"
__date__      = "11/30/2013 09:10:00 AM"

# Version   Date        Notes
# -------   ----------  -------------------------------------------------------
# 1.0.0     11/29/2013  Starting script template
# 1.0.1     11/29/2013  Interact through Twitter REST API v1.1 on RaspberryPi
#                       (https://dev.twitter.com/docs/api/1.1) using
#                       Python Twitter Tools (http://mike.verdone.ca/twitter)
# 1.0.2     11/30/2013  Separate iTwitter class from sense-act logic
#
import sys, os, traceback, optparse
import time
import re

import twitter

#
#
#
class iTwitter (object):
    def __init__ (self, ckey, csecret, token_file, user_name=""):
        if not os.path.exists(token_file):
            twitter.oauth_dance(user_name, ckey, csecret, token_file)
        
        self.oauth_token, self.oauth_token_secret = twitter.read_token_file(token_file)
        
        self.handle = twitter.Twitter(
                      auth=twitter.OAuth(self.oauth_token, self.oauth_token_secret, 
                                         ckey, csecret))

    def get_mentions (self, num=20):
        return self.handle.statuses.mentions_timeline(count=num)

    def get_timeline (self, num=20):
        return self.handle.statuses.home_timeline(count=num)

    def get_direct_message (self, num=20):
        return self.handle.direct_messages(count=num)

    def set_status (self, msg):
        return self.handle.statuses.update(status=msg)

    def send_direct_message (self, usr, msg):
        return self.handle.direct_messages.new(user=usr, status=msg)
#
#
#
def test ():
    global options, args
    t = iTwitter("yujC3tyTWH6q7XAgIvAGg", "FqVBCDdF4B3cA7dPKBFxwZmq2jD9hAq1dub7eRBHaY",
                       os.path.expanduser('~/.brayne_twitter_credentials'), "Brayne Buddy")
    print 'Hello from iTwitter test()!'
                      
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
    if options.verbose: print 'There is no main(). Running test()...'
    test()

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version="%prog "+__version__)
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_option ('-t', '--test', default=False, help='Run test suite')
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

