#!/bin/sh

. $testdir/testenv.sh

echo "";echo Checking handling of options.
setpw $test_principal foo
pwexpire $test_principal never

echo "";echo Banner = K3RB3R05 S
setpw $test_principal foo
test_run -chauthtok $test_principal $pam_krb5 $test_flags banner="K3RB3R05 S" -- foo bar bar
