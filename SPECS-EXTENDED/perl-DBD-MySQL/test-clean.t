#!/usr/bin/perl

use strict;
use warnings;

use File::Path;
use Test::More tests => 2;

my $MYSQL_DIR       = $ENV{'MYSQL_DIR'};
my $MYSQL_UNIX_PORT = $ENV{'MYSQL_UNIX_PORT'};
my $MYSQL_PIDFILE   = $ENV{'MYSQL_PIDFILE'};

ok(system("/usr/bin/mysqladmin --user=root --socket=$MYSQL_UNIX_PORT shutdown 2>&1 || [ ! -s \"$MYSQL_PIDFILE\" ] || /bin/kill `cat \"$MYSQL_PIDFILE\"`") == 0);
my $removed_count = rmtree($MYSQL_DIR, 1, 1);
ok($removed_count > 0);

