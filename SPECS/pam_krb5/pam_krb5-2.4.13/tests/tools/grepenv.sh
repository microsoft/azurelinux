#!/bin/sh
env | grep ^pam_krb5_ | sort
klist_c
