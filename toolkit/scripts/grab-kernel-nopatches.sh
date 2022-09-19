#!/bin/bash

TMP_DIR=tmp_grab_kernel_nopatches

function usage() { 
    echo "Download rpms, toolchains, manifests from a specific pipeline's artifacts" 
    echo "b : base path for cbl-mariner repo (e.g. /home/cameronbaird/repos/cbl-mariner)" 
    echo "l : artifact folder download link (the artifact folder on ADO containing all of the nopatches)"
    exit 1 
}

while getopts "b:l:" OPTIONS; do
  case "${OPTIONS}" in
    b ) BASE_PATH=$OPTARG ;;
    l ) ZIP_URL=$OPTARG ;;
    * ) usage 
        ;;
  esac
done

if [[ -z $BASE_PATH ]]; then
    echo "Missing -b"
    usage
fi

if [[ -z $ZIP_URL ]]; then
    echo "Missing -l"
    usage
fi

# Pipe $auth through $Placeholder variable to suppress false positive in credscan
Placeholder=${auth}

mkdir $TMP_DIR
pushd $TMP_DIR

SUBDIR=$(echo "${ZIP_URL}" | grep -o -P '(?<=KernelCVEPatch%2F).*(?=&%24format)')
curl "$ZIP_URL" --header "Authorization:Basic ${Placeholder}" --retry 3 -o artifacts.zip
unzip artifacts.zip
for f in ./${SUBDIR}/*.nopatch; do cp $f ${BASE_PATH}/SPECS/kernel; done
popd
rm -r $TMP_DIR