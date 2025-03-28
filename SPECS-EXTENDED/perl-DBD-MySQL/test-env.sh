#!/usr/bin/bash

# MariaDB setup
export MYSQL_DIR=$PWD/t/testdb
export MYSQL_UNIX_PORT=$MYSQL_DIR/mysql.sock
export MYSQL_PIDFILE=$MYSQL_DIR/mysql.pid

# DBD::mysql test setup
export DBD_MYSQL_TESTDB=test
export DBD_MYSQL_TESTHOST=localhost
export DBD_MYSQL_TESTSOCKET=$MYSQL_UNIX_PORT
export DBD_MYSQL_TESTUSER=testuserdbd
export DBD_MYSQL_TESTPASSWORD=testpasswordDBD

