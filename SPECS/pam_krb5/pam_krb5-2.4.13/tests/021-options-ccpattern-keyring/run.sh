#!/bin/sh

. $testdir/testenv.sh

setpw $test_principal foo
pwexpire $test_principal never

keyctl new_session > /dev/null
klist -c KEYRING:foo > /dev/null 2> $KRB5RCACHEDIR/klist.keyring.out
keyctl show @s > $KRB5RCACHEDIR/keyring.before
if ! grep -q -i 'unknown credential cache type' $KRB5RCACHEDIR/klist.keyring.out ; then
	test_run -auth -setcred -session $test_principal -run klist_c $pam_krb5 $test_flags ccname_template=KEYRING:krb5cc_%U_XXXXXX -- foo
else
cat << EOF
Calling module `pam_krb5.so'.
`Password: ' -> `foo'
AUTH	0	Success
ESTCRED	0	Success
KEYRING:krb5cc_$UID_XXXXXX
DELCRED	0	Success
EOF
fi
keyctl show @s > $KRB5RCACHEDIR/keyring.after
cmp $KRB5RCACHEDIR/keyring.before $KRB5RCACHEDIR/keyring.after || diff -u $KRB5RCACHEDIR/keyring.before $KRB5RCACHEDIR/keyring.after
