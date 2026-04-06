#!/bin/sh

set -e

# @1: archive basename
# @*: paths to strip
function repack {
    basename=$1
    shift

    archive=$basename.tar.gz
    newarchive=$basename-repacked.tar.gz

    echo "Re-packing $archive"
    rm -rf repack
    mkdir repack
    (
	cd repack
	tar zxf ../$archive

	echo "Begin stripping files"
	for arg in $@
	do
	    find -name $arg -delete -print
	done
	echo "Done stripping files"

	tar zcf ../$newarchive *
    )
    rm -rf repack
    echo "Wrote $newarchive"
}

dcap_version=$(grep dcap_version linux-sgx*spec | head -1 | awk '{print $3}')

repack prebuilt_dcap_${dcap_version} \
       libcrypto.a \
       policy.wasm \
       libsgx_pce.signed.so \
       libsgx_id_enclave.signed.so \
       libsgx_qe3.signed.so \
       libsgx_tdqe.signed.so \
       libsgx_qve.signed.so
