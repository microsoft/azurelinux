#!/bin/sh

version=$(rpm -q --specfile --qf='%{version}\n' yarnpkg.spec | head -n1)
timestamp=$(date +%Y%m%d)
if [ ! -e v$version.tar.gz ]; then
wget https://github.com/yarnpkg/yarn/archive/v$version.tar.gz
fi
rm -rf yarn-$version
tar -zxf v$version.tar.gz
cd yarn-$version
for file in $(ls -1 ../*.prebundle.patch 2>/dev/null); do
patch -p1 < $file
done
rm yarn.lock
yarn install
yarn autoclean --force
yarn audit fix
# Delete all binary files in node_modules
echo "Deleting binary files..."
find node_modules -type f -not -name '*.js' -exec file {} \; | grep ELF | awk -F':' '{print $1}' | xargs rm
cd ..
tar -zcf yarnpkg-v$version-bundled-$timestamp.tar.gz yarn-$version
