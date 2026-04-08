#!/usr/bin/bash 
set -eu -o pipefail
# Detect existing non-conforming host keys and perform the permissions migration
# https://fedoraproject.org/wiki/Changes/SSHKeySignSuidBit
# 
# Example output looks like:
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Permissions 0640 for '/etc/ssh/ssh_host_rsa_key' are too open.
# It is required that your private key files are NOT accessible by others.
# This private key will be ignored.
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Permissions 0640 for '/etc/ssh/ssh_host_ecdsa_key' are too open.
# It is required that your private key files are NOT accessible by others.
# This private key will be ignored.
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Permissions 0640 for '/etc/ssh/ssh_host_ed25519_key' are too open.
# It is required that your private key files are NOT accessible by others.
# This private key will be ignored.
# sshd: no hostkeys available -- exiting.
#
output="$(sshd -T 2>&1 || true)" # expected to fail
while read line; do
    if [[ $line =~ ^Permissions\ [0-9]+\ for\ \'(.*)\'\ are\ too\ open. ]]; then
        keyfile=${BASH_REMATCH[1]}
        echo $line
        echo -e "\t-> changing permissions on $keyfile"
        chmod --verbose g-r $keyfile
        chown --verbose root:root $keyfile
    fi
done <<< "$output"
