#!/bin/sh

. $testdir/testenv.sh

echo "";echo Succeed: correct password, warn about expiration.
setpw $test_principal foo
pwexpire $test_principal now
test_settle
test_run -auth -account $test_principal $pam_krb5 $test_flags -- foo bar bar
