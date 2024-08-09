#!/bin/bash
# -*- mode: shell-script; indent-tabs-mode: true; tab-width: 4; -*-

# This script turns sysuser.d files into scriptlets mandated by Fedora
# packaging guidelines. The general idea is to define users using the
# declarative syntax but to turn this into traditional scriptlets.

user() {
	user="$1"
	uid="$2"
	desc="$3"
	group="$4"
	home="$5"
	shell="$6"

	[ "$desc" = '-' ] && desc=
	{ [ "$home" = '-' ] || [ "$home" = '' ]; } && home=/
	{ [ "$shell" = '-' ] || [ "$shell" = '' ]; } && shell=/usr/sbin/nologin

	if [ "$uid" = '-' ] || [ "$uid" = '' ]; then
		cat <<-EOF
		getent passwd '$user' >/dev/null || \\
		    useradd -r -g ${group@Q} -d ${home@Q} -s ${shell@Q} -c ${desc@Q} ${user@Q} || :
		EOF
	else
		cat <<-EOF
		if ! getent passwd ${user@Q} >/dev/null; then
		    if ! getent passwd ${uid@Q} >/dev/null; then
		        useradd -r -u ${uid@Q} -g ${group@Q} -d ${home@Q} -s ${shell@Q} -c ${desc@Q} ${user@Q} || :
		    else
		        useradd -r -g ${group@Q} -d ${home@Q} -s ${shell@Q} -c ${desc@Q} ${user@Q} || :
		    fi
		fi

		EOF
	fi
}

group() {
	group="$1"
	gid="$2"

	if [ "$gid" = '-' ]; then
		cat <<-EOF
		getent group ${group@Q} >/dev/null || groupadd -r ${group@Q} || :
		EOF
	else
		cat <<-EOF
		getent group ${group@Q} >/dev/null || groupadd -f -g ${gid@Q} -r ${group@Q} || :
		EOF
	fi
}

usermod() {
	user="$1"
	group="$2"

	cat <<-EOF
	if getent group ${group@Q} >/dev/null; then
	    usermod -a -G ${group@Q} '$user' || :
	fi
	EOF
}

parse() {
	while read -r line || [ -n "$line" ] ; do
		{ [ "${line:0:1}" = '#' ] || [ "${line:0:1}" = ';' ]; } && continue
		line="${line## *}"
		[ -z "$line" ] && continue
		eval "arr=( $line )"
		case "${arr[0]}" in
			('u')
				if [[ "${arr[2]}" == *":"* ]]; then
					user "${arr[1]}" "${arr[2]%:*}" "${arr[3]}" "${arr[2]#*:}" "${arr[4]}" "${arr[5]}"
				else
					group "${arr[1]}" "${arr[2]}"
					user "${arr[1]}" "${arr[2]}" "${arr[3]}" "${arr[1]}" "${arr[4]}" "${arr[5]}"
				fi
				;;
			('g')
				group "${arr[1]}" "${arr[2]}"
				;;
			('m')
				group "${arr[2]}" "-"
				user "${arr[1]}" "-" "" "${arr[1]}" "" ""
				usermod "${arr[1]}" "${arr[2]}"
				;;
		esac
	done
}

for fn in "$@"; do
	[ -e "$fn" ] || continue
	echo "# generated from $(basename "$fn")"
	parse <"$fn"
done
