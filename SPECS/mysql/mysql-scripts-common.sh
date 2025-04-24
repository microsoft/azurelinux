#!/bin/sh

# Some useful functions used in other MySQL helper scripts
# This scripts defines variables datadir, errlogfile, socketfile

export LC_ALL=C

# extract value of a MySQL option from config files
# Usage: get_mysql_option VARNAME DEFAULT SECTION [ SECTION, ... ]
# result is returned in $result
# We use my_print_defaults which prints all options from multiple files,
# with the more specific ones later; hence take the last match.
get_mysql_option(){
	if [ $# -ne 3 ] ; then
		echo "get_mysql_option requires 3 arguments: section option default_value"
		return
	fi
	sections="$1"
	option_name="$2"
	default_value="$3"
	result=`@bindir@/my_print_defaults $my_print_defaults_extra_args $sections | sed -n "s/^--${option_name}=//p" | tail -n 1`
	if [ -z "$result" ]; then
	    # not found, use default
	    result="${default_value}"
	fi
}

# For the case of running more instances via systemd, scrits that source
# this file can get --default-group-suffix or similar option as the first
# argument. The utility my_print_defaults needs to use it as well, so the
# scripts sourcing this file work with the same options as the daemon.
my_print_defaults_extra_args=''
while echo "$1" | grep -q '^--defaults' ; do
	my_print_defaults_extra_args="${my_print_defaults_extra_args} $1"
	shift
done

# Defaults here had better match what mysqld_safe will default to
# The option values are generally defined on three important places
# on the default installation:
#  1) default values are hardcoded in the code of mysqld daemon or
#     mysqld_safe script
#  2) configurable values are defined in @sysconfdir@/my.cnf
#  3) default values for helper scripts are specified bellow
# So, in case values are defined in my.cnf, we need to get that value.
# In case they are not defined in my.cnf, we need to get the same value
# in the daemon, as in the helper scripts. Thus, default values here
# must correspond with values defined in mysqld_safe script and source
# code itself.

server_sections="mysqld_safe mysqld server mysqld-@MAJOR_VERSION@.@MINOR_VERSION@ client-server"

get_mysql_option "$server_sections" datadir "@MYSQL_DATADIR@"
datadir="$result"

# if there is log_error in the my.cnf, my_print_defaults still
# returns log-error
# log-error might be defined in mysqld_safe and mysqld sections,
# the former has bigger priority
get_mysql_option "$server_sections" log-error "$datadir/`hostname`.err"
errlogfile="$result"

get_mysql_option "$server_sections" socket "@MYSQL_UNIX_ADDR@"
socketfile="$result"

get_mysql_option "$server_sections" pid-file "$datadir/`hostname`.pid"
pidfile="$result"

