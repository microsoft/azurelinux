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
VENDOR_TARBALL_NAME="rabbitmq-server-hex-vendor-3.13.0"

# Create Hex Packag arrays and link
HEX_PM_LINK="https://repo.hex.pm/tarballs"
declare -a HEX_PACKAGES
# HEX_PACKAGES+=("<package>-<version>")

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

