#!/bin/sh

. $testdir/testenv.sh

setpw $test_principal foo
pwexpire $test_principal never

echo ""; echo "Forking, without use_shmem, with external:"
test_run -fork -auth -setcred -session $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=FILE:${testdir}/kdc/krb5cc_%U_XXXXXX external -- foo

echo ""; echo "Forking, with use_shmem, with external:"
test_run -fork -auth -setcred -session $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=FILE:${testdir}/kdc/krb5cc_%U_XXXXXX external use_shmem -- foo

find ${testdir}/kdc -name "krb5cc*" -ls
