#!/bin/bash
if [[ $# -eq 0 ]] ; then
    echo 'Usage: generate_source_tarball.sh <MariaDB version>'
    echo 'Example: generate_source_tarball.sh 10.6.7'
    exit 0
fi

echo 'Starting MariaDB source tarball creation'
sudo rm -rf mariadb-$1
sudo git clone --depth 1 https://github.com/MariaDB/server.git -b mariadb-$1
pushd server
sudo git submodule update --depth 1 --init --recursive 
popd
sudo mv server mariadb-$1
sudo tar -zcvf mariadb-$1.tar.gz mariadb-$1
echo "Source tarball mariadb-$1.tar.gz successfully created!"
