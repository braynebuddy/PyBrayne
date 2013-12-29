#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# TODO prog_base.py - A starting template for Python scripts
#
# Copyright 2013 Robert B. Hawkins
#
"""
SYNOPSIS

    TODO prog_base [-h,--help] [-v,--verbose] [--version]

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

    1.0.0
"""
__author__    = "Rob Hawkins <webwords@txhawkins.net>"
__version__   = "1.0.0"
__date__      = "2013.12.01"

# Version   Date        Notes
# -------   ----------  -------------------------------------------------------
# 1.0.0     2013.12.01  Starting script template
#

import sys, os, traceback, optparse
import time
import re
#from pexpect import run, spawn

def test ():

    global options, args
    # TODO: Do something more interesting here...
    print 'Hello from the test() function!'

def main ():

    global options, args
    # TODO: Do something more interesting here...
    print 'Hello world!'

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

