#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# cleanup
rm -rf /boot/*
rm -rf /usr/src/
rm -rf /home/*
rm -rf /var/log/*

echo removing tdnf cache
tdnf -y clean all
rm -rf /var/cache/tdnf
