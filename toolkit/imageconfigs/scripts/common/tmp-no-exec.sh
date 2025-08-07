#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -euxo pipefail

sed -i 's/^Options=/Options=noexec,/' /usr/lib/systemd/system/tmp.mount
