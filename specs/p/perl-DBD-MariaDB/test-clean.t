#!/usr/bin/perl

use strict;
use warnings;

use File::Path;
use Test::More tests => 2;

my $MARIADB_DIR       = $ENV{'MARIADB_DIR'};
my $MARIADB_UNIX_PORT = $ENV{'MARIADB_UNIX_PORT'};
my $MARIADB_PIDFILE   = $ENV{'MARIADB_PIDFILE'};

ok(system("mariadb-admin --user=root --socket=$MARIADB_UNIX_PORT shutdown 2>&1 || [ ! -s \"$MARIADB_PIDFILE\" ] || /bin/kill `cat \"$MARIADB_PIDFILE\"`") == 0);
my $removed_count = rmtree($MARIADB_DIR, 1, 1);
ok($removed_count > 0);

