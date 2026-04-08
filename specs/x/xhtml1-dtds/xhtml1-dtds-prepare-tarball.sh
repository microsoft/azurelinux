#!/bin/sh

set -e

# Prune content from upstream tarball:
# https://www.redhat.com/archives/fedora-legal-list/2009-February/msg00015.html

# While at it, prune docs as well; the W3C Documentation License is not an
# acceptable one per Fedora licensing guidelines.

date="20020801"
url="http://www.w3.org/TR/2002/REC-xhtml1-$date/xhtml1.tgz"

curl -O $url
tar zxf $(basename $url)
find xhtml1-$date -type f | grep -vF /DTD/ | xargs rm
rm $(basename $url)

tar Jcvf xhtml1-dtds-$date.tar.xz xhtml1-$date
rm -r xhtml1-$date
