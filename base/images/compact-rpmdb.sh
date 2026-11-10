#!/bin/bash
# Compact retained RPM databases after KIWI's final package transactions.
set -euo pipefail

echo "Compacting container RPM database"
rpmdb --verifydb
rpmdb --rebuilddb
rpmdb --verifydb
