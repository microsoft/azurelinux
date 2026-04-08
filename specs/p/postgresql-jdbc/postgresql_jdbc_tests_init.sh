#!/usr/bin/bash

# Before running tests, source this file.
# Call the function `setup_build_local_properties` and redirect its output into
# the file `build.local.properties` and run the tests in the same directory.

. /usr/share/postgresql-setup/postgresql_pkg_tests.sh

PGTESTS_LOCALE=C.UTF-8

function setup_build_local_properties
{
cat << EOF
test.url.PGHOST=localhost
test.url.PGPORT=$PGTESTS_PORT
test.url.PGDBNAME=test
user=test
password=test
privilegedUser=$PGTESTS_ADMIN
privilegedPassword=$PGTESTS_ADMINPASS
preparethreshold=5
loglevel=0
EOF
}
