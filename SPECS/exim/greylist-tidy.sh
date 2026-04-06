#!/bin/bash

if [ -s /var/spool/exim/db/greylist.db ]; then
    sqlite3 /var/spool/exim/db/greylist.db <<EOF
.timeout 5000
DELETE FROM greylist WHERE expire < $((`date +%s` - 604800));
EOF
fi
