#!/bin/sh

version=$(grep '^Version:' bouncycastle.spec | sed -e 's/^Version:\W*//')

for bc in bcprov bcpkix bcpg bcmail bcjmail bctls bcutil ; do
  rm -f $bc-*.pom
  wget https://repo1.maven.org/maven2/org/bouncycastle/$bc-jdk18on/$version/$bc-jdk18on-$version.pom
done
