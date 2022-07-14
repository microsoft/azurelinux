#!/bin/sh

. $testdir/testenv.sh

setpw $test_principal foo
pwexpire $test_principal never

# Anonymous PKINIT armor.
echo ""
test_run -auth -session -run grepenvc.sh -authtok foo $test_principal $pam_krb5 $test_flags use_first_pass preauth_options=X509_anchors=FILE:$testdir/kdc/ca.crt test_environment armor armor_strategy=pkinit

# Use a keytab.
echo ""
test_run -auth -session -run grepenvc.sh -authtok foo $test_principal $pam_krb5 $test_flags use_first_pass keytab=$testdir/kdc/krb5.keytab test_environment armor armor_strategy=keytab
