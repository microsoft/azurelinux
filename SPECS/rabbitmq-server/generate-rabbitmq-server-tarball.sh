#!/bin/bash
# This script serves to generate the rabbitmq-server-hex-vendor-3.11.11.tar.gz
# used in rabbitmq-server.spec. to run this script, use the following command:
#   ./generate-rabbitmq-server-tarball.sh
#
# Running the above will execute the script, creating a temp directory for 
# all the packages, pull all required packages from hex and github (for hex
# source), then tar everything up into the name specified in 
# VENDOR_TARBALL_NAME. If the directory name in TEMP_TARBALL_DIR conflits 
# locally, adjust the variable contents as necessary.


# baseline variables for filename and temporary directory to avoid filenme collisions
TEMP_TARBALL_DIR="TempRabbitmqTarball"
VENDOR_TARBALL_NAME="rabbitmq-server-hex-vendor-3.11.11"

#Create Hex Packag arrays and link
HEX_PM_LINK="https://repo.hex.pm/tarballs"
declare -a HEX_PACKAGES
HEX_PACKAGES+=("benchfella-0.3.5")
HEX_PACKAGES+=("bunt-0.2.1")
HEX_PACKAGES+=("certifi-2.9.0")
HEX_PACKAGES+=("cesso-0.1.3")
HEX_PACKAGES+=("credo-1.7.0")
HEX_PACKAGES+=("csvlixir-2.0.4")
HEX_PACKAGES+=("dialyzex-1.3.0")
HEX_PACKAGES+=("earmark-1.4.37")
HEX_PACKAGES+=("earmark_parser-1.4.31")
HEX_PACKAGES+=("excoveralls-0.16.0")
HEX_PACKAGES+=("excoveralls-0.13.4")
HEX_PACKAGES+=("ex_csv-0.1.5")
HEX_PACKAGES+=("ex_doc-0.29.3")
HEX_PACKAGES+=("file_system-0.2.10")
HEX_PACKAGES+=("hackney-1.18.1")
HEX_PACKAGES+=("idna-6.1.1")
HEX_PACKAGES+=("inch_ex-0.5.6")
HEX_PACKAGES+=("jason-1.4.0")
HEX_PACKAGES+=("makeup-1.1.0")
HEX_PACKAGES+=("makeup_elixir-0.16.0")
HEX_PACKAGES+=("makeup_erlang-0.1.1")
HEX_PACKAGES+=("metrics-1.0.1")
HEX_PACKAGES+=("mimerl-1.2.0")
HEX_PACKAGES+=("nimble_parsec-1.2.3")
HEX_PACKAGES+=("parallel_stream-1.0.6")
HEX_PACKAGES+=("parse_trans-3.3.1")
HEX_PACKAGES+=("poison-3.1.0")
HEX_PACKAGES+=("ssl_verify_fun-1.1.6")
HEX_PACKAGES+=("unicode_util_compat-0.7.0")

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
    curl -Lo ./$package.tar $HEX_PM_LINK/$package.tar
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

