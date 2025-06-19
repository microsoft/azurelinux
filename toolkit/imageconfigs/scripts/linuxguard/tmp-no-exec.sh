#!/bin/bash

set -euxo pipefail

sed -i 's/^Options=/Options=noexec,/' /usr/lib/systemd/system/tmp.mount