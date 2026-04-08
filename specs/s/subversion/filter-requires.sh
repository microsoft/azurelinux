#!/bin/sh
# Munge Perl requirements:
# - remove dependency on Config::Inifiles
# - only require File::Path >= 1.04, not >= 1.404
#   (since rpmvercmp thinks 04 < 1.404, not unreasonably)
# - filter out requirements for SVN:: modules; otherwise
#   subversion requires subversion-perl
/usr/lib/rpm/perl.req $* | 
sed -e '/perl(Config::IniFiles)/d' \
    -e '/perl(SVN::/d' \
    -e 's/perl(File::Path) >= 1.0404/perl(File::Path) >= 1.04/'

    
