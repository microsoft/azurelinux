# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

echo removing tdnf cache
tdnf -y clean all
rm -rf /var/cache/tdnf
