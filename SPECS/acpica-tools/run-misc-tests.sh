#!/bin/bash
#
#       run the misc tests: we need to do this in a script since
#       some of these are expected to fail which would normally cause
#	the %check step to stop.  however, this is expected behavior.
#	we are running iasl precisely because we expect it to stop when
#	presented with faulty ASL.
#
#       this script assumes it is in the source 'tests' directory at
#       start.
#

set -x

BINDIR="$1"
VERSION="$2"

# create files to compare against
$BINDIR/iasl -h

sed -e "s/VVVVVVVV/$VERSION/" \
    ../badcode.asl.result > misc/badcode.asl.expected
sed -e "s/VVVVVVVV/$VERSION/" \
    ../grammar.asl.result > misc/grammar.asl.expected
sed -e "s/VVVVVVVV/$VERSION/" \
    ../converterSample.asl.result > misc/converterSample.asl.expected

cd misc

# see if badcode.asl failed as expected
# NB: the -f option is required so we can see all of the errors
$BINDIR/iasl -f badcode.asl 2>&1 | tee badcode.asl.actual
diff badcode.asl.actual badcode.asl.expected >/dev/null 2>&1
[ $? -eq 0 ] || exit 1

# see if grammar.asl failed as expected
# NB: the -f option is required so we can see all of the errors
$BINDIR/iasl -f -of grammar.asl 2>&1 | tee grammar.asl.actual
diff grammar.asl.actual grammar.asl.expected >/dev/null 2>&1
[ $? -eq 0 ] || exit 1

# see if converterSample.asl succeeded as expected
$BINDIR/iasl converterSample.asl 2>&1 | tee converterSample.asl.actual
diff converterSample.asl.actual converterSample.asl.expected >/dev/null 2>&1
[ $? -ne 0 ] && exit 1

exit 0
