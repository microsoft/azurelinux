#!/bin/sh

. $testdir/testenv.sh

setpw $test_principal foo
pwexpire $test_principal never

test_run -auth -setcred -session $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=FILE:${testdir}/kdc/krb5cc_%U_XXXXXX -- foo
find ${testdir}/kdc -name "krb5cc*" -ls
test_run -auth -setcred -session $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=DIR:${testdir}/kdc/krb5cc_%U_XXXXXX -- foo
find ${testdir}/kdc -name "krb5cc*" -ls
