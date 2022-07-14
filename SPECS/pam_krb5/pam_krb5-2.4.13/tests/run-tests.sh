#!/bin/sh

testdir=`dirname "$0"`
testdir=`cd "$testdir" ; pwd`
export testdir

. $testdir/testenv.sh
echo "Running tests using test principal \"$test_principal\"".
echo "Running tests using KDC on \"$test_host\"".
getent hosts "$test_host"

# Avoid leaking the keyring to tests if we can.
keyctl new_session > /dev/null 2> /dev/null

# Tell the caller where the binaries are.
test -n "$krb5kdc" && echo Using krb5kdc binary: $krb5kdc
test -n "$kpasswdd" && echo Using kpasswdd binary: $kpasswdd
test -n "$kadmin"  && echo Using kadmin.local binary: $kadmin

# Run each test with clear log files and a fresh copy of the KDC and kadmind.
for test in ${@:-"$testdir"/0*} ; do
	if ! test -s $test/run.sh ; then
		continue
	fi
	echo -n `basename "$test"` .
	test_kdcinitdb
	echo -n .
	test_kdcprep
	echo -n ." "
	meanwhile "$run_kdc" -w "waitforkdc.sh $test/../kdc/krb5kdc.log" "$run_kadmind" -w "waitforkpasswdd.sh $test/../kdc/kadmind.log" "$test/run.sh" > $test/stdout 2> $test/stderr
	kdcport=`expr $kdcport + 3`
	kadminport=`expr $kdcport + 1`
	kpasswdport=`expr $kadminport + 1`
	if test -s $test/stdout.expected ; then
		if ! cmp -s $test/stdout.expected $test/stdout ; then
			if ! test -s $test/stdout.expected.2 || ! cmp -s $test/stdout.expected.2 $test/stdout ; then
				echo ""
				diff -u $test/stdout.expected $test/stdout | sed "s|$testdir/||g"
				echo "Test $test stdout unexpected error!"
				exit 1
			fi
		fi
		if ! cmp -s $test/stderr.expected $test/stderr ; then
			echo ""
			diff -u $test/stderr.expected $test/stderr | sed "s|$testdir/||g"
			echo "Test $test stderr unexpected error!"
			exit 1
		fi
	fi
	echo OK
done
