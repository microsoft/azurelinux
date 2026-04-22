#!/usr/bin/python
# Copyright 2015 Tomas Popela <tpopela@redhat.com>
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

try:
  import argparse
  optparse = False
except ImportError:
  from optparse import OptionParser
  optparse = True
import locale
import simplejson as json
import sys
import os

if __name__ == "__main__":

  added = []

  # Create the parser object
  if optparse:
    parser = OptionParser()
    parser_add_argument = parser.add_option
  else:
    parser = argparse.ArgumentParser()
    parser_add_argument = parser.add_argument

  parser_add_argument(
      '--check',
      help='Check the tests against given SPEC file')
  parser_add_argument(
      '--spec', action='store_true',
      help='Prints the test targets in format suitable for SPEC file')
  parser_add_argument(
      'path', nargs='?', default=os.getcwd(),
      help='Path to Chromium sources')

  # Parse the args
  if optparse:
    args, options = parser.parse_args()
  else:
    args = parser.parse_args()

  tests_path = "%s/testing/buildbot/chromium.linux.json" % args.path

  try:
    with open(tests_path, "r") as input_file:
      json_file = json.load(input_file)
  except IOError:
    print "Cannot find JSON file with tests in path '%s'!" % args.path
    sys.exit(1)


  for test in json_file['Linux Tests']['gtest_tests']:
    if isinstance(test, dict):
        added.append(test['test'])
    else:
        added.append(test)

  if args.check:
    removed = []
    disabled = []
    in_tests = False
    spec_file = None

    with open(args.check) as f:
      for line in f:
        if "CHROMIUM_BROWSER_UNIT_TESTS=" in line:
          in_tests = True
          continue

        if in_tests and line.endswith('"\n'):
          break

        if in_tests:
          found = False
          for test in added:
            if test in line:
              if "#" in line:
                disabled.append(test)
              added.remove(test)
              found = True
              break
          if not found:
            if not "%" in line:
              removed.append(line)

    for test in removed:
      print "REMOVED"
      print "\t" + test;
    for test in added:
      print "ADDED"
      print "\t" + test;
    for test in disabled:
      print "DISABLED"
      print "\t" + test;

    sys.exit(0)

  for name in added:
    if args.spec:
      print "\t" + name + " \\"
    else:
      print name
