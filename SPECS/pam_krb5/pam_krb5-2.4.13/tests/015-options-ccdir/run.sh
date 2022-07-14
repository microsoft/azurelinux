#!/bin/sh

. $testdir/testenv.sh

echo "";echo Checking handling of options.
setpw $test_principal foo
pwexpire $test_principal never

echo "";echo Ccache directory = testdir/kdc.
test_run -auth -setcred $test_principal -run klist_c $pam_krb5 $test_flags ccache_dir=${testdir}/kdc -- foo
