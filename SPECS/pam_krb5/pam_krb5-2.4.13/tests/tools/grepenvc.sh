#!/bin/sh
env | grep ^pam_krb5_ | sort | cut -d: -f1
klist_c
