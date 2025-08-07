#!/usr/bin/env bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

sed -i "/AutoUpdate.Enabled/d" /etc/waagent.conf
sed -i "/AutoUpdate.UpdateToLatestVersion=y/c\AutoUpdate.UpdateToLatestVersion=n" /etc/waagent.conf
if ! grep -q "AutoUpdate.UpdateToLatestVersion=n" /etc/waagent.conf; then
    sed -i "$ a AutoUpdate.UpdateToLatestVersion=n" /etc/waagent.conf
fi
