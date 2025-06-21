#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

sed -i 's/#DUIDType=vendor/DUIDType=link-layer/' /etc/systemd/networkd.conf
