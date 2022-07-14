#!/bin/sh

. $testdir/testenv.sh

setpw $test_principal foo
pwexpire $test_principal never

test_run -auth -setcred -session $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=FILE:${testdir}/kdc/krb5_cc_%U -- foo | sed s,_`id -u`,_'$UID',g
find kdc -name "krb5*cc*" | sed s,_`id -u`,_'$UID',g
klist -c FILE:${testdir}/kdc/krb5_cc_`id -u` > ${testdir}/kdc/klist.before

KRB5CCNAME=FILE:${testdir}/kdc/krb5_cc_`id -u`
export KRB5CCNAME
sleep 2
test_run -auth -refreshcred $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=FILE:${testdir}/kdc/krb5_cc_%U -- foo | sed s,_`id -u`,_'$UID',g
export -n KRB5CCNAME
unset KRB5CCNAME
find kdc -name "krb5*cc*" | sed s,_`id -u`,_'$UID',g
klist -c FILE:${testdir}/kdc/krb5_cc_`id -u` > ${testdir}/kdc/klist.after

# They should look different, at least the timestamps.
if cmp -s ${testdir}/kdc/klist.before ${testdir}/kdc/klist.after ; then
	echo Credentials not refreshed.
	cat ${testdir}/kdc/klist.before
	exit 1
fi

rm -f ${testdir}/kdc/krb5_cc_`id -u`

test_run -auth -setcred -session $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=DIR:${testdir}/kdc/krb5cc -- foo
find kdc -name "krb5*cc*"
klist -c DIR:${testdir}/kdc/krb5cc > ${testdir}/kdc/klist.before

KRB5CCNAME=DIR:${testdir}/kdc/krb5cc
export KRB5CCNAME
sleep 2
test_run -auth -refreshcred $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=DIR:${testdir}/kdc/krb5cc -- foo
export -n KRB5CCNAME
unset KRB5CCNAME
find kdc -name "krb5*cc*"
klist -c DIR:${testdir}/kdc/krb5cc > ${testdir}/kdc/klist.after

# They should look different, at least the timestamps.
if cmp -s ${testdir}/kdc/klist.before ${testdir}/kdc/klist.after ; then
	echo Credentials not refreshed.
	cat ${testdir}/kdc/klist.before
	exit 1
fi

rm -f -r ${testdir}/kdc/krb5cc
