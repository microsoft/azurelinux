#!/bin/sh

. $testdir/testenv.sh

setpw $test_principal foo
pwexpire $test_principal never

CCSAVE=${testdir}/kdc/krb5cc_save; export CCSAVE
test_run -auth -session $test_principal -run save_cc_file.sh $pam_krb5 $test_flags ccname_template=FILE:${testdir}/kdc/krb5cc_%U_XXXXXX -- foo
klist -c FILE:$CCSAVE > ${testdir}/kdc/klist.before

echo ""; sleep 5

KRB5CCNAME=FILE:$CCSAVE ; export KRB5CCNAME
test_run -auth -refreshcred $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=FILE:${testdir}/kdc/krb5cc_%U_XXXXXX -- foo
klist > ${testdir}/kdc/klist.after

# They should be different.
if cmp -s ${testdir}/kdc/klist.before ${testdir}/kdc/klist.after ; then
	cat ${testdir}/kdc/klist.before
fi

# Shouldn't find any if we destroy the saved one
kdestroy
echo "";find ${testdir} -name "krb5cc*" -print
