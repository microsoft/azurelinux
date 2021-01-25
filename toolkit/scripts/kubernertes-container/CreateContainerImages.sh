#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_FOLDER="$(git rev-parse --show-toplevel)"

BASE_IMAGE_NAME="cbl-mariner-base"
BASE_IMAGE_FULL_NAME="$BASE_IMAGE_NAME:1.0"
DISTROLESS_IMAGE_NAME="cbl-mariner-distroless"
DISTROLESS_IMAGE_FULL_NAME="$DISTROLESS_IMAGE_NAME:1.0"

K8S_CONTAINER_PREFIX_BASE="k8s-container-base"
K8S_CONTAINER_PREFIX_DISTROLESS="k8s-container-distroless"

# parse script parameters:
#
# -d -> distroless image tarball
# -b -> base image tarball
# -f -> folder where RPMs file are stored
# -o -> output folder
#
while getopts ":d:b:f:o:" OPTIONS; do
    case ${OPTIONS} in
    d ) 
        DISTROLESS_IMAGE_TARBALL=$OPTARG 
        echo "+++ DISTROLESS_IMAGE_TARBALL  -> $DISTROLESS_IMAGE_TARBALL";;
    b ) 
        BASE_IMAGE_TARBALL=$OPTARG
        echo "+++ BASE_IMAGE_TARBALL        -> $BASE_IMAGE_TARBALL";;
    f ) 
        RPMS_FOLDER=$OPTARG
        echo "+++ RPMS_FOLDER               -> $RPMS_FOLDER";;
    o ) 
        OUTPUT_FOLDER=$OPTARG
        echo "+++ OUTPUT_FOLDER             -> $OUTPUT_FOLDER";;

    \? )
        echo "Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
    esac
done

if [[ (! -n $BASE_IMAGE_TARBALL) || \
      (! -f $BASE_IMAGE_TARBALL) ]]; then
    echo "Error - NO base image tarball"
    exit 1
fi

if [[ (! -n $DISTROLESS_IMAGE_TARBALL) || \
      (! -f $DISTROLESS_IMAGE_TARBALL) ]]; then
    echo "Error - NO distroless image tarball"
    exit 1
fi

if [[ (! -n $RPMS_FOLDER) || \
      (! -d $RPMS_FOLDER) ]]; then
    echo "Error - NO RPMs folder"
    exit 1
fi

if [[ (! -n $OUTPUT_FOLDER) || \
      (! -d $OUTPUT_FOLDER) ]]; then
    echo "Error - NO output folder"
    exit 1
fi

TEMPDIR=$(mktemp -d)

function cleanup {
    echo "+++ remove $TEMPDIR"
    rm -rf $TEMPDIR

    echo "+++ cleanup docker containers"
    BASE_CONTAINER_IDS=$(docker ps -a -f "name=$K8S_CONTAINER_PREFIX_BASE*" --format="{{.ID}}")
    for CONTAINER_ID in $BASE_CONTAINER_IDS ; do
        docker rm -f $CONTAINER_ID
    done

    echo "+++ cleanup docker images"
    K8S_DISTROLESS_IMAGE_IDS=$(docker images $K8S_CONTAINER_PREFIX_DISTROLESS* --format="{{.ID}}")
    for K8S_IMAGE_ID in $K8S_DISTROLESS_IMAGE_IDS ; do
        docker rmi -f $K8S_IMAGE_ID
    done

    BASE_IMAGE_ID=$(docker images $BASE_IMAGE_NAME --format="{{.ID}}")
    if [[ -n $BASE_IMAGE_ID ]]; then
        docker rmi -f $BASE_IMAGE_ID
    fi

    DISTROLESS_IMAGE_ID=$(docker images $DISTROLESS_IMAGE_NAME --format="{{.ID}}")
    if [[ -n $DISTROLESS_IMAGE_ID ]]; then
        docker rmi -f $DISTROLESS_IMAGE_ID
    fi

    docker system prune -f
}
trap cleanup EXIT

RPM_NAME=""
RPM_VERSION=""
RPM_REVISION=""

function get_rpm_info {
    # $1: rpm file name
    RPM_FILE=$1

    # get component name, version and revision from RPM file name
    # file name pattern: 'component-name-x.y.z-r.cm1.arch.rpm'
    #   - component-name   -> name of the component (can contain '-')
    #   - x.y.z            -> version (cannot contain '-')
    #   - r                -> revision number
    #   - cm1.arch.rpm     -> RPM file extension (arch is the architecture: noarch, x86_64 or aarch64)
    FILE_NAME=$(basename $RPM_FILE)

    OLDIFS=$IFS
    IFS='-'
    read -ra NAME_PARTS <<< $FILE_NAME

    RPM_NAME=""
    for (( i=0; i<${#NAME_PARTS[@]}-2; i++ )); do
        if [[ $i == 0 ]]; then
            RPM_NAME="${NAME_PARTS[$i]}"
        else
            RPM_NAME="$RPM_NAME-${NAME_PARTS[$i]}"
        fi
    done

    RPM_VERSION=${NAME_PARTS[${#NAME_PARTS[@]}-2]}
    IFS='.'
    read -ra EXTENSION_PARTS <<< ${NAME_PARTS[${#NAME_PARTS[@]}-1]}
    RPM_REVISION=${EXTENSION_PARTS[0]}
    IFS=$OLDIFS
}

function create_container_image_base {
    # $1: kubernetes component name
    # $2: rpm file name
    K8S_COMPONENT=$1
    RPM_FILE=$2

    get_rpm_info $RPM_FILE

    echo
    echo "----------------------------------------------------------------------"
    echo "+++ create base container for $K8S_COMPONENT version $RPM_VERSION-$RPM_REVISION"
    echo "----------------------------------------------------------------------"

    K8S_CONTAINER_NAME="$K8S_CONTAINER_PREFIX_BASE-$K8S_COMPONENT-$RPM_VERSION"
    K8S_IMAGE_NAME="$K8S_CONTAINER_NAME-$RPM_REVISION"

    cp $SCRIPT_FOLDER/InstallComponentsBase.sh $TEMPDIR
    cp $ROOT_FOLDER/toolkit/resources/manifests/package/local.repo $TEMPDIR

    pushd $TEMPDIR
    docker run \
      --name $K8S_CONTAINER_NAME \
      -v $RPMS_FOLDER:/upstream-cached-rpms \
      -v $TEMPDIR:/temp \
      -di $BASE_IMAGE_FULL_NAME /temp/InstallComponentsBase.sh -c $RPM_NAME-$RPM_VERSION -r /temp/local.repo
    docker wait $K8S_CONTAINER_NAME
    docker logs $K8S_CONTAINER_NAME

    echo "+++ export container $K8S_CONTAINER_NAME -> $K8S_IMAGE_NAME"
    docker export -o "$OUTPUT_FOLDER/$K8S_IMAGE_NAME.tar.gz" $K8S_CONTAINER_NAME
    popd

    # clean up temp folder
    rm -rf $TEMPDIR/*
}

function create_container_image_distroless {
    # $1: kubernetes component name
    # $2: rpm file name
    K8S_COMPONENT=$1
    RPM_FILE=$2

    get_rpm_info $RPM_FILE

    echo
    echo "----------------------------------------------------------------------"
    echo "+++ create distroless container for $K8S_COMPONENT version $RPM_VERSION-$RPM_REVISION"
    echo "----------------------------------------------------------------------"

    FOLDERS_TO_INSTALL_DIR=folder-to-install
    mkdir -p $TEMPDIR/$FOLDERS_TO_INSTALL_DIR
    cp $SCRIPT_FOLDER/Dockerfile-Distroless $TEMPDIR/Dockerfile
    cp $RPM_FILE $TEMPDIR/$FOLDERS_TO_INSTALL_DIR

    # expand RPM so folders it contains can be copied into the container
    echo "+++ extract $RPM_FILE into $TEMPDIR/$FOLDERS_TO_INSTALL_DIR"
    pushd $TEMPDIR/$FOLDERS_TO_INSTALL_DIR
    rpm2cpio *.rpm | cpio -idm
    rm *.rpm
    popd

    K8S_IMAGE_BASE_NAME="$K8S_CONTAINER_PREFIX_DISTROLESS-$K8S_COMPONENT"
    K8S_IMAGE_NAME_FULL="$K8S_IMAGE_BASE_NAME:$RPM_VERSION-$RPM_REVISION"
    
    pushd $TEMPDIR
    docker image build -t $K8S_IMAGE_NAME_FULL .
    TARBALL_FILE="$OUTPUT_FOLDER/$K8S_IMAGE_BASE_NAME-$RPM_VERSION-$RPM_REVISION.tar.gz"
    echo "+++ save docker image to $TARBALL_FILE"
    docker image save -o $TARBALL_FILE $K8S_IMAGE_NAME_FULL
    popd
    
    # clean up temp folder
    rm -rf $TEMPDIR/*
}

# import base and distroless images
echo "+++ import container image $BASE_IMAGE_FULL_NAME"
cat $BASE_IMAGE_TARBALL | docker import - $BASE_IMAGE_FULL_NAME
echo "+++ import container image $DISTROLESS_IMAGE_FULL_NAME"
cat $DISTROLESS_IMAGE_TARBALL | docker import - $DISTROLESS_IMAGE_FULL_NAME

cd $RPMS_FOLDER
DISTROLESS_COMPONENTS="kube-apiserver kube-controller-manager kube-scheduler pause"
BASE_ONLY_COMPONENTS="kube-proxy"

# create container based on cbl-mariner base
echo "======================================================================"
KUBERNETES_COMPONENTS="$DISTROLESS_COMPONENTS $BASE_ONLY_COMPONENTS"
echo "+++ create containers based on $BASE_IMAGE_FULL_NAME for $KUBERNETES_COMPONENTS"
for KUBERNETES_COMPONENT in $KUBERNETES_COMPONENTS ; do
    for KUBERNETES_COMPONENT_RPM in $(find -name "kubernetes-$KUBERNETES_COMPONENT-*") ; do
        create_container_image_base $KUBERNETES_COMPONENT $KUBERNETES_COMPONENT_RPM
    done
done

echo

# create container based on cbl-mariner distroless
echo "======================================================================"
KUBERNETES_COMPONENTS="$DISTROLESS_COMPONENTS"
echo "+++ create containers based on $DISTROLESS_IMAGE_FULL_NAME for $KUBERNETES_COMPONENTS"
for KUBERNETES_COMPONENT in $KUBERNETES_COMPONENTS ; do
    for KUBERNETES_COMPONENT_RPM in $(find -name "kubernetes-$KUBERNETES_COMPONENT-*") ; do
        create_container_image_distroless $KUBERNETES_COMPONENT $KUBERNETES_COMPONENT_RPM
    done
done
