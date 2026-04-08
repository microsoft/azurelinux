#! /usr/bin/sh
# Author: Jan Vcelak <jvcelak@redhat.com>

. /usr/libexec/openldap/functions

function check_config_syntax()
{
	retcode=0
	tmp_slaptest=`mktemp --tmpdir=/var/run/openldap`
	run_as_ldap "/usr/sbin/slaptest $SLAPD_GLOBAL_OPTIONS -u" &>$tmp_slaptest
	if [ $? -ne 0 ]; then
		error "Checking configuration file failed:"
		cat $tmp_slaptest >&2
		retcode=1
	fi
	rm $tmp_slaptest
	return $retcode
}

function check_certs_perms()
{
	retcode=0
	for cert in `certificates`; do
		run_as_ldap "/usr/bin/test -e \"$cert\""
		if [ $? -ne 0 ]; then
			error "TLS certificate/key/DB '%s' was not found." "$cert"
			retcoder=1
			continue
		fi
		run_as_ldap "/usr/bin/test -r \"$cert\""
		if [ $? -ne 0 ]; then
			error "TLS certificate/key/DB '%s' is not readable." "$cert"
			retcode=1
		fi
	done
	return $retcode
}

function check_db_perms()
{
	retcode=0
	for dbdir in `databases`; do
		[ -d "$dbdir" ] || continue
		for dbfile in `find ${dbdir} -maxdepth 1 -name "*.mdb"` ; do
			run_as_ldap "/usr/bin/test -r \"$dbfile\" -a -w \"$dbfile\""
			if [ $? -ne 0 ]; then
				error "Read/write permissions for DB file '%s' are required." "$dbfile"
				retcode=1
			fi
		done
	done
	return $retcode
}

function check_everything()
{
	retcode=0
	check_config_syntax || retcode=1
	check_certs_perms || retcode=1
	check_db_perms || retcode=1
	return $retcode
}

if [ `id -u` -ne 0 ]; then
	error "You have to be root to run this script."
	exit 4
fi

load_sysconfig

if [ -n "$SLAPD_CONFIG_DIR" ]; then
	if [ ! -d "$SLAPD_CONFIG_DIR" ]; then
		error "Configuration directory '%s' does not exist." "$SLAPD_CONFIG_DIR"
	else
		check_everything
		exit $?
	fi
fi

if [ -n "$SLAPD_CONFIG_FILE" ]; then
	if [ ! -f "$SLAPD_CONFIG_FILE" ]; then
		error "Configuration file '%s' does not exist." "$SLAPD_CONFIG_FILE"
	else
		error "Warning: Usage of a configuration file is obsolete!"
		check_everything
		exit $?
	fi
fi

exit 1
