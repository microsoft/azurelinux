#!/bin/perl
#
# install script for man-pages-ja-0.5-20011115
#
# Will never work on other man pages!!
#
# By Yukihiro Nakai <ynakai@redhat.com>

print "$ARGV[0]/usr/share/man/ja\n";
print "1\n";
print "root\n";
print "root\n";
print "C\n";

###
# Maintainer should update these number according to the original Makefile
###
my $n=`grep -v -E "^#.*" $ARGV[1] | wc -l`;
for($i=0; $i<=$n; $i++) {
  print "\n";
}
print "C\n";

for($i=0; $i<=145; $i++) {
  print "0\n";
}
print "C\n";
