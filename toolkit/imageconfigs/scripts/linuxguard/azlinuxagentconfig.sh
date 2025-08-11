#!/usr/bin/env bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

sha_keys_dir="/etc/ssh"
echo "Updating AzureLinuxAgent config"
sed -i "/OS.SshDir/c\OS.SshDir=${sha_keys_dir}" /etc/waagent.conf
if ! grep -q "OS.SshDir" /etc/waagent.conf; then
    sed -i "$ a OS.SshDir=${sha_keys_dir}" /etc/waagent.conf
fi
sed -i "/AutoUpdate.Enabled/d" /etc/waagent.conf
sed -i "/AutoUpdate.UpdateToLatestVersion=y/c\AutoUpdate.UpdateToLatestVersion=n" /etc/waagent.conf
if ! grep -q "AutoUpdate.UpdateToLatestVersion=n" /etc/waagent.conf; then
    sed -i "$ a AutoUpdate.UpdateToLatestVersion=n" /etc/waagent.conf
fi
