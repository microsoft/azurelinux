#!/usr/bin/perl

use strict;
use warnings;

use Test::More tests => 7;

# MySQL setup
my $MARIADB_BASE      = $ENV{'MARIADB_BASE'};
my $MARIADB_DIR       = $ENV{'MARIADB_DIR'};
my $MARIADB_UNIX_PORT = $ENV{'MARIADB_UNIX_PORT'};
my $MARIADB_PIDFILE   = $ENV{'MARIADB_PIDFILE'};
my $MARIADB_USER      = $ENV{'MARIADB_USER'};
chomp($MARIADB_USER);

# DBD::MariaDB test setup
my $DBD_MARIADB_TESTDB       = $ENV{'DBD_MARIADB_TESTDB'};
my $DBD_MARIADB_TESTHOST     = $ENV{'DBD_MARIADB_TESTHOST'};
my $DBD_MARIADB_TESTSOCKET   = $ENV{'DBD_MARIADB_TESTSOCKET'};
my $DBD_MARIADB_TESTUSER     = $ENV{'DBD_MARIADB_TESTUSER'};
my $DBD_MARIADB_TESTPASSWORD = $ENV{'DBD_MARIADB_TESTPASSWORD'};

system("mariadb-install-db --no-defaults --datadir=$MARIADB_DIR --force --skip-name-resolve --explicit_defaults_for_timestamp >/dev/null 2>&1");
is($?, 0);

my $cmd = "mariadbd-safe --no-defaults --user=$MARIADB_USER --socket=$MARIADB_UNIX_PORT --datadir=$MARIADB_DIR --pid-file=$MARIADB_PIDFILE --ssl_cert=$MARIADB_BASE/t/certs/service.pem --ssl_key=$MARIADB_BASE/t/certs/service-key.pem --ssl_ca=$MARIADB_BASE/t/certs/ca.crt --skip-networking >/dev/null 2>&1 &";
system($cmd);
is($?, 0);

my $attempts = 0;
while (system("mariadb-admin --user=root --socket=$MARIADB_UNIX_PORT ping >/dev/null 2>&1") != 0) {
    sleep 3;
    $attempts++;
    if ($attempts > 10) {
        fail("skipping test, mariadb/mysql server could not be contacted after 30 seconds\n");
    }
}
ok(1);

system("mariadb --socket=$MARIADB_UNIX_PORT --execute \"CREATE USER '$DBD_MARIADB_TESTUSER\@localhost';\" 2>&1");
is($?, 0);
system("mariadb --socket=$MARIADB_UNIX_PORT --execute \"CREATE DATABASE IF NOT EXISTS $DBD_MARIADB_TESTDB CHARACTER SET='utf8mb4';\" 2>&1");
is($?, 0);
system("mariadb --socket=$MARIADB_UNIX_PORT --execute \"GRANT ALL PRIVILEGES ON $DBD_MARIADB_TESTDB.* TO '$DBD_MARIADB_TESTUSER\@localhost' IDENTIFIED BY '$DBD_MARIADB_TESTPASSWORD';\" 2>&1");
is($?, 0);
system("mariadb-admin --user=$DBD_MARIADB_TESTUSER --password=$DBD_MARIADB_TESTPASSWORD --socket=$DBD_MARIADB_TESTSOCKET ping >/dev/null 2>&1");
is($?, 0);
