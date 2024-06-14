#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

virtqemud -d
echo "Virtqemud daemon has successfully been created. Starting virt-launcher process."

/usr/bin/virt-launcher
