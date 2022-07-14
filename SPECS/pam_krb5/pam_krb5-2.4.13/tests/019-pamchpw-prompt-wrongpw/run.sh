#!/bin/sh

. $testdir/testenv.sh

echo "";echo Fail: incorrect password.
setpw $test_principal foo
pwexpire $test_principal now
test_run -auth -account $test_principal $pam_krb5 $test_flags chpw_prompt -- bar
