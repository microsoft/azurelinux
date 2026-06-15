#!/bin/bash

set -euxo pipefail

# Reported upstream as https://github.com/util-linux/util-linux/issues/2896,
# requires systemd updated to v256. The workaround is to remove the ImportCredential lines.
sed -i /ImportCredential=/d /usr/lib/systemd/system/getty@.service
sed -i /ImportCredential=/d /usr/lib/systemd/system/serial-getty@.service
