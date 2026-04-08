#!/bin/sh
version=$(cat freerdp.spec | grep "Version: " | tr --squeeze-repeats " " | cut --delimiter " " --fields 2)

echo "Downloading FreeRDP-$version.tar.gz"
curl --silent --location "https://github.com/FreeRDP/FreeRDP/archive/$version/FreeRDP-$version.tar.gz" --output "FreeRDP-$version.tar.gz" || exit 1

echo "Removing unicode_builtin.c"
gzip --decompress "FreeRDP-$version.tar.gz" || exit 1
tar --file "FreeRDP-$version.tar" --delete "*/winpr/libwinpr/crt/unicode_builtin.c" || exit 1
gzip --best "FreeRDP-$version.tar" --stdout > FreeRDP-$version-repack.tar.gz
rm FreeRDP-$version.tar

echo "FreeRDP-$version-repack.tar.gz is prepared"
exit 0
