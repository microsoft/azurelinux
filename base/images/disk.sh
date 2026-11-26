#!/bin/bash

set -euo pipefail

# RPM triggers generate derived state while packages are installed. Record that
# /etc and /var are current with the final /usr state in the assembled disk.
touch -r /usr /etc/.updated /var/.updated
