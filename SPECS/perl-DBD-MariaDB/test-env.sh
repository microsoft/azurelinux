#!/usr/bin/bash

# MariaDB setup
export MARIADB_BASE=$PWD
export MARIADB_DIR=$MARIADB_BASE/t/testdb
export MARIADB_UNIX_PORT=$MARIADB_DIR/mysql.sock
export MARIADB_PIDFILE=$MARIADB_DIR/mysql.pid
export MARIADB_USER=`whoami`

# DBD::MariaDB test setup
export DBD_MARIADB_TESTDB=testdb
export DBD_MARIADB_TESTHOST=localhost
export DBD_MARIADB_TESTSOCKET=$MARIADB_UNIX_PORT
export DBD_MARIADB_TESTUSER=testuser
export DBD_MARIADB_TESTPASSWORD=testpassword

