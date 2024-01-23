#!/bin/bash

# takes one argument: the directory to recursively vendor
function vendor_all() {
  # Check if the argument is a valid directory
  if [ -d "$1" ]; then
    # Save the current directory
    local old_dir=$(pwd)
    # Change to the given directory
    cd "$1"
    # Loop through all the go.mod files in the current directory and its subdirectories
    for f in $(find . -name "go.mod"); do
      # Push the directory containing the go.mod file to the stack
      pushd $(dirname $f) > /dev/null
      # Run go mod vendor
      go mod vendor
      # Pop the directory from the stack
      popd > /dev/null
    done
    # Restore the original directory
    cd "$old_dir"
  else
    # Print an error message if the argument is not a valid directory
    echo "Invalid directory: $1"
    return 1
  fi
}

# takes two arguments: $1 - directory to search for vendors; $2 - output directory to build
function copy_vendor() {
  # Check if the arguments are valid directories
  if [ -d "$1" ]; then
    # Create the second argument directory if it does not exist
    mkdir -p "$2"
    # Loop through all the vendor directories in the first argument
    for f in $(find "$1" -type d -name vendor); do
      # Get the relative path of the vendor directory
      rel_path=${f#$1}
      # snip out vendor dir so we don't end up with vendor/vendor/github.com...
      rel_path="$(dirname $rel_path)"
      # Create the corresponding directory in the second argument
      mkdir -p "$2/$rel_path"
      # Copy the vendor directory to the second argument
      cp -a "$f" "$2/$rel_path"
    done
  else
    # Print an error message if the arguments are not valid directories
    echo "Invalid directory: $1"
    return 1
  fi
}

PKG_NAME="cert-manager"
DESIRED_VERSION="1.13.3"

vendor_all "${PKG_NAME}-${DESIRED_VERSION}"
copy_vendor "${PKG_NAME}-${DESIRED_VERSION}" "${PKG_NAME}-${DESIRED_VERSION}-govendor"
# output vendor tar
tar --sort=name --mtime="$(date -u +"%Y-%m-%d %H:%MZ")" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option="exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime" \
    -cf "${PKG_NAME}-${DESIRED_VERSION}-govendor.tar.gz" \
    -C "${PKG_NAME}-${DESIRED_VERSION}-govendor" .

if [ $? -eq 0 ]; then
    echo "Produced vendor tar: ${PKG_NAME}-${DESIRED_VERSION}-govendor.tar.gz"
    echo "sha256sum: $(sha256sum ${PKG_NAME}-${DESIRED_VERSION}-govendor.tar.gz)"
else
    echo "failure"
fi

# cleanup
rm -r "${PKG_NAME}-${DESIRED_VERSION}-govendor"
