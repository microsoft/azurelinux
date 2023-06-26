#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

script_dir=$( realpath "$(dirname "$0")" )
topdir=/usr/src/mariner
enable_local_repo=false

function switch_to_red_text() {
    printf "\e[31m"
}

function switch_to_normal_text() {
    printf "\e[0m"
}

function print_error() {
    echo ""
    switch_to_red_text
    echo ">>>> ERROR: $1"
    switch_to_normal_text
    echo ""
}

function help {
echo "
Usage: sudo make containerized-rpmbuild [REPO_PATH=/path/to/CBL-Mariner] [MODE=test|build] [VERSION=1.0|2.0] [MOUNTS= /src/path:/dst/path] [ENABLE_REPO=y]

Starts a docker container with the specified version of mariner. Mounts REPO_PATH/out/RPMS
to /mnt/RPMS.

In the 'build' mode, mounts REPO_PATH/build/INTERMEDIATE_SRPMS at /mnt/INTERMEDIATE_SRPMS;
REPO_PATH/SPECS at ${topdir}/SPECS; REPO_PATH/build/container-build at ${topdir}/BUILD and
REPO_PATH/build/container-buildroot at ${topdir}/BUILDROOT

Optional arguments:
    REPO_PATH:      path to the CBL-Mariner repo root directory. default: "current directory"
    MODE            build or test. In 'test' mode it will use a pre-built mariner chroot image. 
                                In 'build' mode it will use the latest published container.default:"build"
    VERISION        1.0 or 2.0........................................................default: "2.0"
    MOUNTS          mount a directory into the container. Should be of the form '/src/dir:/dest/dir'. 
                                Can be specified multiple times..........default: ""
    ENABLE_REPO:    Set to 'y' to use local RPMs to satisfy package dependencies. default: "n"

To see help, run 'sudo make containerized-rpmbuild-help'
"
}

function build_chroot() {
    cd "${repo_path}/toolkit"
    echo "Building worker chroot"
    sudo make graph-cache REBUILD_TOOLS=y > /dev/null
}

function build_tools() {
    cd "${repo_path}/toolkit"
    echo "Building tools"
    sudo make go-depsearch REBUILD_TOOLS=y
    sudo make go-grapher REBUILD_TOOLS=y
    sudo make go-specreader REBUILD_TOOLS=y
}

function build_graph() {
    cd "${repo_path}/toolkit"
    echo "Building dependency graph"
    sudo make workplan
}

while (( "$#")); do
  case "$1" in
    -m ) mode="$2"; shift 2 ;;
    -v ) version="$2"; shift 2 ;;
    -p ) repo_path="$2"; shift 2 ;;
    --enable-local-repo ) enable_local_repo=true; shift ;;
    --help ) help; exit 1 ;;
    ? ) echo -e "ERROR: INVALID OPTION.\n\n"; help; exit 1 ;;
  esac
done

# Assign default values
[[ -z "${repo_path}" ]] && repo_path="$(dirname $0)" && repo_path=${repo_path%'/toolkit'*}
[[ ! -d "${repo_path}" ]] && { print_error " Directory ${repo_path} does not exist"; exit 1; }
[[ -z "${mode}" ]] && mode="build"
[[ -z  "${version}" ]] && version="2.0"

echo "Running in ${mode} mode, requires root..."
sudo echo "Running as root!"

# ==================== Setup ====================
cd "${script_dir}"
build_dir="${script_dir}/build_container"
mkdir -p "${build_dir}"

# ============ Populate SRPMS ============
# Populate ${repo_path}/build/INTERMEDIATE_SRPMS with SRPMs, that can be used to build RPMs in the container
cd "${repo_path}/toolkit"
echo "Populating Intermediate SRPMs"
sudo make input-srpms SRPM_FILE_SIGNATURE_HANDLING="update" > /dev/null

# ============ Map chroot mount ============
if [[ "${mode}" == "build" ]]; then
    # Create a new directory and map it to chroot directory in container
    if [ -d "${repo_path}/build/container-build" ]; then rm -Rf ${repo_path}/build/container-build; fi
    if [ -d "${repo_path}/build/container-buildroot" ]; then rm -Rf ${repo_path}/build/container-buildroot; fi
    mkdir ${repo_path}/build/container-build
    mkdir ${repo_path}/build/container-buildroot
    mounts="${mounts} ${repo_path}/build/container-build:${topdir}/BUILD ${repo_path}/build/container-buildroot:${topdir}/BUILDROOT"
fi

# ============ Setup tools ============
# Copy relavant build tool executables from ${repo_path}/tools/out
echo "Setting up tools"
cd "${repo_path}/toolkit"
if [[ ( ! -f "out/tools/depsearch" ) || ( ! -f "out/tools/grapher" ) || ( ! -f "out/tools/specreader" ) ]]; then build_tools; fi

#if [[ ! -f "out/tools/depsearch" ]]; then build_tools; fi
cp ${repo_path}/toolkit/out/tools/depsearch ${build_dir}/depsearch
#if [[ ! -f "out/tools/grapher" ]]; then build_tools; fi
cp ${repo_path}/toolkit/out/tools/grapher ${build_dir}/grapher
#if [[ ! -f "out/tools/specreader" ]]; then build_tools; fi
cp ${repo_path}/toolkit/out/tools/specreader ${build_dir}/specreader
if [[ ! -f "../build/pkg_artifacts/graph.dot" ]]; then build_graph; fi
cp ${repo_path}/build/pkg_artifacts/graph.dot ${build_dir}/graph.dot

# ========= Setup mounts + Welcome file =========
cd "${script_dir}"
echo "Creating welcome message and checking mounts..."
cat "${script_dir}/resources/welcome_1.txt.template" > "${build_dir}/welcome.txt"

mounts="${mounts} ${repo_path}/out/RPMS:/mnt/RPMS"
if [[ "${mode}" == "build" ]]; then
    # Add extra build mounts
    mounts="${mounts} ${repo_path}/build/INTERMEDIATE_SRPMS:/mnt/INTERMEDIATE_SRPMS ${repo_path}/SPECS:${topdir}/SPECS"
fi

for mount in $mounts $extra_mounts; do
    if [[ -d "${mount%%:*}" ]]; then
        echo "Will mount '${mount%%:*}' to '${mount##*:}'"
        echo "${mount%%:*}' -> '${mount##*:}"  >> "${build_dir}/welcome.txt"
    else
        echo "WARNING: '${mount%%:*}' does not exist. Skipping mount."
        echo "WARNING: '${mount%%:*}' does not exist. Skipping mount."  >> "${build_dir}/welcome.txt"
        continue
    fi
    mount_arg=" $mount_arg -v '$mount' "
done

# ============ Build the dockerfile ============
dockerfile="${script_dir}/resources/mariner.Dockerfile"

if [[  "${mode}" == "build" ]]; then # Configure base image
    echo "Importing chroot into docker..."
    chroot_file="${repo_path}/build/worker/worker_chroot.tar.gz"
    if [[ ! -f "${chroot_file}" ]]; then build_chroot; fi
    chroot_hash=$(sha256sum "${chroot_file}" | cut -d' ' -f1)
    # Check if the chroot file's hash has changed since the last build
    if [[ ! -f "${script_dir}/build_container/hash" ]] || [[ "$(cat "${script_dir}/build_container/hash")" != "${chroot_hash}" ]]; then
        echo "Chroot file has changed, updating..."
        echo "${chroot_hash}" > "${script_dir}/build_container/hash"
        sudo docker import "${chroot_file}" "mcr.microsoft.com/cbl-mariner/tmp_pkgbuild_${version}"
    else
        echo "Chroot is up-to-date"
    fi
else
    echo "Checking for latest ${version} mariner image..."
    sudo docker pull -q "mcr.microsoft.com/cbl-mariner/base/core:${version}"
fi

# ================== Launch Container ==================
echo "Checking if build env is up-to-date..."
docker_image_tag="mariner-containerizedbuild"
tag=$(date +'%y%m%d.%H%M')
sudo docker build -q \
                -f "${dockerfile}" \
                -t "${docker_image_tag}:${tag}" \
                --build-arg version="$version" \
                --build-arg mode="$mode" \
                --build-arg enable_local_repo="$enable_local_repo" \
                --build-arg topdir="$topdir" \
                --build-arg mariner_repo="$repo_path" \
                --build-arg mariner_branch="" \
                .

sudo docker tag ${docker_image_tag}:${tag} ${docker_image_tag}:latest

echo "docker_image_tag is ${docker_image_tag}..."
sudo bash -c "docker run --rm \
                    ${mount_arg} \
                    -it ${docker_image_tag}:latest /bin/bash; \
                    [[ -d ${repo_path}/out/RPMS/repodata ]] && { rm -r ${repo_path}/out/RPMS/repodata; echo 'Clearing repodata' ; }"
