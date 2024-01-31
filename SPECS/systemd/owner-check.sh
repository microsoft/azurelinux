#!/bin/bash
set -e

verb="$1"

[ "$verb" = "-s" ] && do_send=1 || do_send=

[ -n "$do_send" ] && [ -z "$server" -o -z "login" ] && { echo '$server and $login need to be set'; exit 1; }

header=
from=systemd-maint@fedoraproject.org
time='2 years ago'
# time='1 day ago'
port=587

for user in "$@"; do
    echo "checking $user…"

    p=$(git log -1 --all --author "$user")
    if [ -z "$p" ]; then
	echo "No commits from $user, check spelling"
	exit 1
    fi

    t=$(git shortlog --all --author "$user" --since "@{$time}" | wc -l)
    if [ $t != 0 ]; then
	echo "$t commits in the last two years, OK"
	echo
	continue
    fi

    echo "$p" | head -n6
    echo ".. adding to list"

    if [ -z "$header" ]; then
	echo '$USER$;$EMAIL$' >.mail.list
	header=done
    fi

    echo "$user;$user@fedoraproject.org" >>.mail.list
    echo
done

[ -z "$header" ] && exit 0
[ -n "$do_send" ] || exit 0

echo "Sending mails…"
set -x
massmail -F "$from" \
	 -C "$from" \
	 -S 'write access to the fedora systemd package' \
	 -z "$server" -u "$login" -P "$port" \
	 .mail.list <owner-check.template
