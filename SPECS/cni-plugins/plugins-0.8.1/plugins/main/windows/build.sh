#!/usr/bin/env bash
set -e

PLUGINS=$(cat plugins/windows_only.txt)
for d in $PLUGINS; do
	if [ -d "$d" ]; then
	    plugin="$(basename "$d").exe"

		echo "  $plugin"
		CXX=x86_64-w64-mingw32-g++ CC=x86_64-w64-mingw32-gcc CGO_ENABLED=1 \
		    $GO build -o "${PWD}/bin/$plugin" "$@" "$REPO_PATH"/$d
	fi
done
