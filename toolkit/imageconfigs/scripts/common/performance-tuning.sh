#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -euxo pipefail

# Remove the dracut-cmdline-ask service because it isn't used and slows down
# the boot time.
rm /usr/lib/dracut/modules.d/98dracut-systemd/dracut-cmdline-ask.service
