#!/bin/sh

VERSION=$1

tar -xzvf XML-SAX-$VERSION.tar.gz

# xmltest.xml could not be distributed due to copyright
rm XML-SAX-$VERSION/testfiles/xmltest.xml
rm XML-SAX-$VERSION/t/16large.t
sed -i -e '/testfiles\/xmltest.xml/ d' XML-SAX-$VERSION/MANIFEST
sed -i -e '/t\/16large.t/ d' XML-SAX-$VERSION/MANIFEST

tar -czvf XML-SAX-$VERSION-nopatents.tar.gz XML-SAX-$VERSION

