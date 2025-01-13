#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
set -e

# first arg is `-f` or `--some-option`
# or first arg is `something.conf`
if [ "${1#-}" != "$1" ] || [ "${1%.conf}" != "$1" ]; then
    set -- valkey-server "$@"
fi

# allow the container to be started with `--user`
if [ "$1" = 'valkey-server' -a "$(id -u)" = '0' ]; then
    find . \! -user valkey -exec chown valkey '{}' +
    exec setpriv --reuid=valkey --regid=valkey --init-groups --inh-caps=-all "$BASH_SOURCE" "$@"
fi

# set an appropriate umask (if one isn't set already)
# - https://github.com/docker-library/redis/issues/305
# - https://github.com/redis/redis/blob/bb875603fb7ff3f9d19aad906bd45d7db98d9a39/utils/systemd-redis_server.service#L37
um="$(umask)"
if [ "$um" = '0022' ]; then
	umask 0077
fi

exec "$@" $VALKEY_EXTRA_FLAGS