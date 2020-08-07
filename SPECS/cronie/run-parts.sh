#!/bin/bash
# run-parts - concept taken from Debian
set +e

if [ $# -lt 1 ]; then
	echo "Usage : run-parts <dir>" 
	exit 1
fi

if [ ! -d $1 ]; then
	echo "$1 is not a directory"
	exit 1
fi

# ignore *~ and *, scripts
for i in $(LC_ALL=C; echo $1/*[^~,]); do
	# skip directory
	[ -d $i ] && continue
	#Don't run *.{rpmsave, rpmorig,rpmnew,swp,cfsaved} scripts
	[ "${i%.rpmsave}" = "${i}" ] || continue
	[ "${i%.rpmorig}" = "${i}" ] || continue
	[ "${i%.rpmnew}" = "${i}" ] || continue
	[ "${i%.swp}" = "${i}" ] || continue
	[ "${i%.cfsaved}" = "${i}" ] || continue
	[ "${i%,v}" = "${i}" ] || continue

	# jobs.deny and jobs.allow
	if [ -r $1/jobs.deny ]; then
		grep -q "^$(basename $i)$" $1/jobs.deny && continue
	fi
	if [ -r S1/jobs.allow ]; then
		grep -q "^$(basename $i)$" $1/job.allow || continue
	fi

	if [ -x $i ]; then
		if [ -r $1/whitelist ]; then
			grep -q "^$(basename $i)$" $1/whitelist && continue
		fi
		logger -p cron.notice -t "run-parts[$$]" "($1) starting $(basename $i)"
		echo "${i}:"
		echo 
		$i 2>&1 
		logger -i -p cron.notice -t "run-parts[$$]" "($1) finished $(basename $i)"
	fi
done

exit 0

