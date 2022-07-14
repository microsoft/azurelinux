#!/bin/sh

. $testdir/testenv.sh

echo "";echo Checking handling of options.
setpw $test_principal foo
pwexpire $test_principal never

echo "";echo Password-change Help Text
setpw $test_principal foo
test_run -chauthtok $test_principal $pam_krb5 $test_flags pwhelp=$testdir/pwhelp.txt -- foo bar bar
