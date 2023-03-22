#!/bin/bash

TEMP_TARBALL_DIR="TempRabbitmqTarball"
VENDOR_TARBALL_NAME="rabbitmq-server-hex-vendor-3.11.11"

#Create Hex Packag arrays and link
HEX_PM_LINK="https://repo.hex.pm/tarballs"
declare -a HEX_PACKAGES
declare -A HEX_VERSIONS
HEX_PACKAGES+=("amqp")
HEX_VERSIONS[amqp]="2.1.2"

HEX_PACKAGES+=("benchfella")
HEX_VERSIONS[benchfella]="0.3.5"

HEX_PACKAGES+=("bunt")
HEX_VERSIONS[bunt]="0.2.1"

HEX_PACKAGES+=("certifi")
HEX_VERSIONS[certifi]="2.9.0"

HEX_PACKAGES+=("cesso")
HEX_VERSIONS[cesso]="0.1.3"

HEX_PACKAGES+=("credo")
HEX_VERSIONS[credo]="1.7.0"

HEX_PACKAGES+=("csv")
HEX_VERSIONS[csv]="2.4.1"

HEX_PACKAGES+=("csvlixir")
HEX_VERSIONS[csvlixir]="2.0.4"

HEX_PACKAGES+=("dialyxir")
HEX_VERSIONS[dialyxir]="0.5.1"

HEX_PACKAGES+=("dialyzex")
HEX_VERSIONS[dialyzex]="1.3.0"

HEX_PACKAGES+=("earmark")
HEX_VERSIONS[earmark]="1.4.37"

HEX_PACKAGES+=("earmark_parser")
HEX_VERSIONS[earmark_parser]="1.4.31"

HEX_PACKAGES+=("excoveralls")
HEX_VERSIONS[excoveralls]="0.16.0"

HEX_PACKAGES+=("ex_csv")
HEX_VERSIONS[ex_csv]="0.1.5"

HEX_PACKAGES+=("ex_doc")
HEX_VERSIONS[ex_doc]="0.29.3"

HEX_PACKAGES+=("file_system")
HEX_VERSIONS[file_system]="0.2.10"

HEX_PACKAGES+=("hackney")
HEX_VERSIONS[hackney]="1.18.1"

HEX_PACKAGES+=("idna")
HEX_VERSIONS[idna]="6.1.1"

HEX_PACKAGES+=("inch_ex")
HEX_VERSIONS[inch_ex]="0.5.6"

HEX_PACKAGES+=("jason")
HEX_VERSIONS[jason]="1.4.0"

HEX_PACKAGES+=("json")
HEX_VERSIONS[json]="1.4.1"

HEX_PACKAGES+=("makeup")
HEX_VERSIONS[makeup]="1.1.0"

HEX_PACKAGES+=("makeup_elixir")
HEX_VERSIONS[makeup_elixir]="0.16.0"

HEX_PACKAGES+=("makeup_erlang")
HEX_VERSIONS[makeup_erlang]="0.1.1"

HEX_PACKAGES+=("metrics")
HEX_VERSIONS[metrics]="1.0.1"

HEX_PACKAGES+=("mimerl")
HEX_VERSIONS[mimerl]="1.2.0"

HEX_PACKAGES+=("nimble_parsec")
HEX_VERSIONS[nimble_parsec]="1.2.3"

HEX_PACKAGES+=("observer_cli")
HEX_VERSIONS[observer_cli]="1.7.4"

HEX_PACKAGES+=("parse_trans")
HEX_VERSIONS[parse_trans]="3.3.1"

HEX_PACKAGES+=("poison")
HEX_VERSIONS[poison]="3.1.0"

HEX_PACKAGES+=("ssl_verify_fun")
HEX_VERSIONS[ssl_verify_fun]="1.1.6"

HEX_PACKAGES+=("stdout_formatter")
HEX_VERSIONS[stdout_formatter]="0.2.4"

HEX_PACKAGES+=("temp")
HEX_VERSIONS[temp]="0.4.7"

HEX_PACKAGES+=("unicode_util_compat")
HEX_VERSIONS[unicode_util_compat]="0.7.0"

HEX_PACKAGES+=("x509")
HEX_VERSIONS[x509]="0.8.5"

# Create Git Links
ELIXIR_HEX_VERSION="2.0.6"
ELIXIR_HEX_LINK="https://github.com/hexpm/hex/archive/refs/tags/v$ELIXIR_HEX_VERSION.tar.gz"

# Create temp directory
mkdir $TEMP_TARBALL_DIR
pushd $TEMP_TARBALL_DIR


# Pull un-compress sources
echo "[BEGIN] Retrieve all deps"
for package in "${HEX_PACKAGES[@]}"
do
    echo "  [BEGIN] Get dependency $package from hex.pm repo"
    curl -Lo ./$package.tar $HEX_PM_LINK/$package-${HEX_VERSIONS[$package]}.tar
    echo "  [END] Get dependency $package"
    echo ""
done

echo "  [BEGIN] Get hex tarball from github release"
curl  -Lo ./hex-$ELIXIR_HEX_VERSION.tar.gz $ELIXIR_HEX_LINK
echo "  [END] Get hex tarball"
echo ""

echo "[END] Retrieve all deps"

# tar pulled dependencies
tar -czf $VENDOR_TARBALL_NAME.tar.gz hex-$ELIXIR_HEX_VERSION.tar.gz *.tar
mv $VENDOR_TARBALL_NAME.tar.gz ../$VENDOR_TARBALL_NAME.tar.gz

# Clean up files
popd
rm -r $TEMP_TARBALL_DIR

