#!/bin/bash
# Copyright (c) 2014 Docker, Inc.

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

set -euo pipefail

# allow the container to be started with `--user`
if [[ "$1" == rabbitmq* ]] && [ "$(id -u)" = '0' ]; then
	if [ "$1" = 'rabbitmq-server' ]; then
		find /var/lib/rabbitmq \! -user rabbitmq -exec chown rabbitmq '{}' +
	fi

    setpriv --reuid=rabbitmq --regid=rabbitmq --init-groups --inh-caps=-all "$BASH_SOURCE" "$@"
fi

deprecatedEnvVars=(
	RABBITMQ_DEFAULT_PASS_FILE
	RABBITMQ_DEFAULT_USER_FILE
	RABBITMQ_MANAGEMENT_SSL_CACERTFILE
	RABBITMQ_MANAGEMENT_SSL_CERTFILE
	RABBITMQ_MANAGEMENT_SSL_DEPTH
	RABBITMQ_MANAGEMENT_SSL_FAIL_IF_NO_PEER_CERT
	RABBITMQ_MANAGEMENT_SSL_KEYFILE
	RABBITMQ_MANAGEMENT_SSL_VERIFY
	RABBITMQ_SSL_CACERTFILE
	RABBITMQ_SSL_CERTFILE
	RABBITMQ_SSL_DEPTH
	RABBITMQ_SSL_FAIL_IF_NO_PEER_CERT
	RABBITMQ_SSL_KEYFILE
	RABBITMQ_SSL_VERIFY
	RABBITMQ_VM_MEMORY_HIGH_WATERMARK
)

hasOldEnv=
for old in "${deprecatedEnvVars[@]}"; do
	if [ -n "${!old:-}" ]; then
		echo >&2 "error: $old is set but deprecated"
		hasOldEnv=1
	fi
done

if [ -n "$hasOldEnv" ]; then
	echo >&2 'error: deprecated environment variables detected'
	echo >&2
	echo >&2 'Please use a configuration file instead; visit https://www.rabbitmq.com/configure.html to learn more'
	echo >&2
	exit 1
fi

# if long and short hostnames are not the same, use long hostnames
if [ -z "${RABBITMQ_USE_LONGNAME:-}" ] && [ "$(hostname)" != "$(hostname -s)" ]; then
	: "${RABBITMQ_USE_LONGNAME:=true}"
fi

exec "$@"
