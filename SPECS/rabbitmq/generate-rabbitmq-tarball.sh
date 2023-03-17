#!/bin/bash

TEMP_TARBALL_DIR="TempRabbitmqTarball"
VENDOR_TARBALL_NAME="rabbitmq-vendor-3.11.9"

#Create Hex Packag arrays and link
HEX_PM_LINK="https://repo.hex.pm/tarballs"
declare -a HEX_PACKAGES
declare -A HEX_VERSIONS
HEX_PACKAGES+=("accept")
HEX_VERSIONS[accept]="0.3.5"

HEX_PACKAGES+=("aten")
HEX_VERSIONS[aten]="0.5.8"

HEX_PACKAGES+=("base64url")
HEX_VERSIONS[base64url]="1.0.1"

HEX_PACKAGES+=("cowboy")
HEX_VERSIONS[cowboy]="2.8.0"

HEX_PACKAGES+=("cowlib")
HEX_VERSIONS[cowlib]="2.9.1"

HEX_PACKAGES+=("credentials_obfuscation")
HEX_VERSIONS[credentials_obfuscation]="3.2.0"

HEX_PACKAGES+=("cuttlefish")
HEX_VERSIONS[cuttlefish]="3.1.0"

HEX_PACKAGES+=("eetcd")
HEX_VERSIONS[eetcd]="0.3.6"

HEX_PACKAGES+=("enough")
HEX_VERSIONS[enough]="0.1.0"

HEX_PACKAGES+=("gen_batch_server")
HEX_VERSIONS[gen_batch_server]="0.8.8"

HEX_PACKAGES+=("getopt")
HEX_VERSIONS[getopt]="1.0.2"

HEX_PACKAGES+=("gun")
HEX_VERSIONS[gun]="1.3.3"

HEX_PACKAGES+=("jose")
HEX_VERSIONS[jose]="1.11.2"

HEX_PACKAGES+=("observer_cli")
HEX_VERSIONS[observer_cli]="1.7.3"

HEX_PACKAGES+=("prometheus")
HEX_VERSIONS[prometheus]="4.10.0"

HEX_PACKAGES+=("quantile_estimator")
HEX_VERSIONS[quantile_estimator]="0.2.1"

HEX_PACKAGES+=("ra")
HEX_VERSIONS[ra]="2.4.6"

HEX_PACKAGES+=("ranch")
HEX_VERSIONS[ranch]="2.1.0"

HEX_PACKAGES+=("recon")
HEX_VERSIONS[recon]="2.5.3"

HEX_PACKAGES+=("redbug")
HEX_VERSIONS[redbug]="2.0.7"

HEX_PACKAGES+=("seshat")
HEX_VERSIONS[seshat]="0.4.0"

HEX_PACKAGES+=("stdout_formatter")
HEX_VERSIONS[stdout_formatter]="0.2.4"

HEX_PACKAGES+=("syslog")
HEX_VERSIONS[syslog]="4.0.0"

HEX_PACKAGES+=("sysmon_handler")
HEX_VERSIONS[sysmon_handler]="1.3.0"

HEX_PACKAGES+=("systemd")
HEX_VERSIONS[systemd]="0.6.1"

HEX_PACKAGES+=("thoas")
HEX_VERSIONS[thoas]="1.0.0"

# Create Git Links
ELVIS_MK_GITHUB_LINK="https://github.com/inaka/elvis.mk/archive/refs/heads/master.zip"
OSIRIS_GITHUB_LINK="https://github.com/rabbitmq/osiris/archive/refs/tags/v1.4.3.tar.gz"

# Create temp directory
mkdir $TEMP_TARBALL_DIR
pushd $TEMP_TARBALL_DIR


# Pull un-compress sources
echo "[BEGIN] Retrieve all deps"
for package in "${HEX_PACKAGES[@]}"
do
    echo "  [BEGIN] Get dependency $package from hex.pm repo"
    curl -Lo ./$package.tar $HEX_PM_LINK/$package-${HEX_VERSIONS[$package]}.tar
    tar -xf ./$package.tar contents.tar.gz
    mkdir ./$package
    tar -C ./$package -xzf contents.tar.gz
    rm contents.tar.gz
    rm $package.tar
    echo "  [END] Get dependency $package"
    echo ""
done

echo "  [BEGIN] Get dependency elvis.mk from github source"
wget $ELVIS_MK_GITHUB_LINK
unzip master.zip
mv elvis.mk-master elvis_mk
echo "  [END] Get dependency elvis.mk"
echo ""

echo "  [BEGIN] Get dependency osiris from github source"
wget $OSIRIS_GITHUB_LINK
tar -zxf v1.4.3.tar.gz
mv osiris-1.4.3 osiris
rm v1.4.3.tar.gz
echo "  [END] Get dependency osiris"
echo "[END] Retrieve all deps"

# tar pulled dependencies
tar -czf $VENDOR_TARBALL_NAME.tar.gz elvis_mk osiris ${HEX_PACKAGES[@]}
mv $VENDOR_TARBALL_NAME.tar.gz ../$VENDOR_TARBALL_NAME.tar.gz

# Clean up files
popd
rm -r $TEMP_TARBALL_DIR

