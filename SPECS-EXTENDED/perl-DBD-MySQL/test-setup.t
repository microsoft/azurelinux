#!/usr/bin/perl

use strict;
use warnings;

use Test::More tests => 7;

# MySQL setup
my $MYSQL_DIR       = $ENV{'MYSQL_DIR'};
my $MYSQL_UNIX_PORT = $ENV{'MYSQL_UNIX_PORT'};
my $MYSQL_PIDFILE   = $ENV{'MYSQL_PIDFILE'};

# DBD::MariaDB test setup
my $DBD_MYSQL_TESTDB       = $ENV{'DBD_MYSQL_TESTDB'};
my $DBD_MYSQL_TESTHOST     = $ENV{'DBD_MYSQL_TESTHOST'};
my $DBD_MYSQL_TESTSOCKET   = $ENV{'DBD_MYSQL_TESTSOCKET'};
my $DBD_MYSQL_TESTUSER     = $ENV{'DBD_MYSQL_TESTUSER'};
my $DBD_MYSQL_TESTPASSWORD = $ENV{'DBD_MYSQL_TESTPASSWORD'};

my $MYSQLD = '/usr/sbin/mysqld';
# Initialize MySQL data directory
system("$MYSQLD --no-defaults --initialize-insecure --user=mysql --datadir=$MYSQL_DIR >/dev/null 2>&1");
is($?, 0);

# Starting the server
my $cmd = "$MYSQLD --no-defaults --socket=$MYSQL_UNIX_PORT --datadir=$MYSQL_DIR --pid-file=$MYSQL_PIDFILE --explicit_defaults_for_timestamp --skip-networking >/dev/null 2>&1 &";
system($cmd);
is($?, 0);

my $attempts = 0;
while (system("/usr/bin/mysqladmin --socket=$MYSQL_UNIX_PORT ping >/dev/null 2>&1") != 0) {
    sleep 3;
    $attempts++;
    if ($attempts > 10) {
        fail("skipping test, mysql server could not be contacted after 30 seconds\n");
    }
}
ok(1);

# Create database
system("mysql -u root --skip-password --execute \"CREATE DATABASE IF NOT EXISTS $DBD_MYSQL_TESTDB CHARACTER SET='utf8mb4';\" 2>&1");
is($?, 0);

# The test user has to have the proper privileges that these tests require
system("mysql -u root --skip-password --execute \"CREATE USER '$DBD_MYSQL_TESTUSER'\@'localhost' IDENTIFIED BY '$DBD_MYSQL_TESTPASSWORD'; \" 2>&1");
is($?, 0);
system("mysql -u root --skip-password --execute \"GRANT ALL PRIVILEGES ON $DBD_MYSQL_TESTDB.* TO '$DBD_MYSQL_TESTUSER'\@'localhost';\" 2>&1");
is($?, 0);

system("/usr/bin/mysqladmin --user=$DBD_MYSQL_TESTUSER --password=$DBD_MYSQL_TESTPASSWORD --socket=$DBD_MYSQL_TESTSOCKET ping >/dev/null 2>&1");
is($?, 0);
