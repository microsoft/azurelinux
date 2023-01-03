#!/bin/sh
exec /usr/bin/php -C \
    -d include_path=/usr/share/pear \
    -d date.timezone=UTC \
    -d output_buffering=1 \
    -d variables_order=EGPCS \
    -d safe_mode=0 \
    -d register_argc_argv="On" \
    /usr/share/pear/peclcmd.php "$@"
