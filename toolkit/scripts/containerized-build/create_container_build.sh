#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

script_dir=$( realpath "$(dirname "$0")" )
specs_dir=/usr/src/mariner/SPECS
sources_dir=/usr/src/mariner/SOURCES
chroot_dir=/usr/src/mariner/BUILD
chroot_dir2=/usr/src/mariner/BUILDROOT
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
echo "Usage: sudo make containerized-rpmbuild [REPO_PATH=/path/to/CBL-Mariner] [MODE=test|build] [VERSION=1.0|2.0] [MOUNTS= /src/path:/dst/path] [ENABLE_REPO=y] [--help]

Starts a docker container with the specified version of mariner. Mounts REPO_PATH/out/RPMS
to /mnt/RPMS.

In the 'build' mode, mounts REPO_PATH/build/INTERMEDIATE_SRPMS at /mnt/INTERMEDIATE_SRPMS;
REPO_PATH/SPECS at ${specs_dir} and REPO_PATH/build/container-chroot at ${chroot_dir}

Optional arguments:
    REPO_PATH:      path to the CBL-Mariner repo root directory. default: "current directory"
    MODE            build or test. In 'test' mode it will use a pre-built mariner chroot image. 
                                In 'build' mode it will use the latest published container.default:"build"
    VERISION        1.0 or 2.0........................................................default: "2.0"
    MOUNTS          mount a directory into the container. Should be of the form '/src/dir:/dest/dir'. 
                                Can be specified multiple times..........default: ""
    ENABLE_REPO:    Set to 'y' to use local RPMs to satisfy package dependencies. default: "n"
    --help          print this help message
"
}

function build_chroot() {
    cd "${repo_path}/toolkit"
    echo "Building worker chroot"
    sudo make graph-cache REBUILD_TOOLS=y > /dev/null
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

#echo "***** mode is ${mode}"
#echo "***** repo_path is ${repo_path}"
#echo "***** extra_mounts is ${extra_mounts}"
#echo "***** version is ${version}"

[[ -z "${repo_path}" ]] && repo_path="$(dirname $0)" && repo_path=${repo_path%'/toolkit'*}
[[ ! -d "${repo_path}" ]] && { print_error " Directory ${repo_path} does not exist"; exit 1; }
[[ -z "${mode}" ]] && mode="build"
[[ -z  "${version}" ]] && version="2.0"
#echo "***** mode is ${mode}"
#echo "***** repo_path is ${repo_path}"
#echo "***** extra_mounts is ${extra_mounts}"
#echo "***** version is ${version}"

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
    if [ -d "${repo_path}/build/container-chroot" ]; then rm -Rf ${repo_path}/build/container-chroot; fi
    if [ -d "${repo_path}/build/container-chroot2" ]; then rm -Rf ${repo_path}/build/container-chroot2; fi
    mkdir ${repo_path}/build/container-chroot
    mkdir ${repo_path}/build/container-chroot2
    mounts="${mounts} ${repo_path}/build/container-chroot:${chroot_dir} ${repo_path}/build/container-chroot2:${chroot_dir2}"
fi

# ========= Setup mounts + Welcome file =========
cd "${script_dir}"
echo "Creating welcome message and checking mounts..."
cat "${script_dir}/resources/welcome_1.txt.template" > "${build_dir}/welcome.txt"

mounts="${mounts} ${repo_path}/out/RPMS:/mnt/RPMS"
if [[ "${mode}" == "build" ]]; then
    # Add extra build mounts
    mounts="${mounts} ${repo_path}/build/INTERMEDIATE_SRPMS:/mnt/INTERMEDIATE_SRPMS ${repo_path}/SPECS:${specs_dir}"
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

sed -i "s~<REPO_PATH>~${repo_path}~" "${build_dir}/welcome.txt"
sed -i "s~<SPECS_DIR>~${specs_dir}~" "${script_dir}/resources/add_shell_functions.txt"
sed -i "s~<SOURCES_DIR>~${sources_dir}~" "${script_dir}/resources/add_shell_functions.txt"

# ============ Build the dockerfile ============
echo "Updating dockerfile from template..."
dockerfile="${build_dir}/mariner.Dockerfile"
#echo "***** dockerfile is ${dockerfile}"
#echo "***** build_dir is ${build_dir}"
#echo "***** script_dir is ${script_dir}"
#echo "***** repo_path is ${repo_path}"
#echo "***** mounts is ${mounts}"
#echo "***** version is ${version}"
#echo "***** mount_arg is ${mount_arg}"

if [[  "${mode}" == "build" ]]; then # Select the correct dockerfile
    cp "${script_dir}/resources/build.Dockerfile.template" "${dockerfile}"
else
    cp "${script_dir}/resources/test.Dockerfile.template" "${dockerfile}"
fi
sed -i "s/<VER>/${version}/" "${dockerfile}"

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

if [[ "${enable_local_repo}" == "true" ]]; then
    echo "RUN echo "enable_local_repo" >> /root/.bashrc" >> "${dockerfile}"
fi

# ================== Launch Container ==================
echo "Checking if build env is up-to-date..."
docker_image_name="mcr.microsoft.com/cbl-mariner/${USER}_tmp_pkgtest_${version}"
sudo docker build -q -f "${dockerfile}" -t "${docker_image_name}" .

echo "***** docker_image_name is ${docker_image_name}..."
sudo bash -c "docker run --rm \
                    ${mount_arg} \
                    -it ${docker_image_name} /bin/bash; \
                    [[ -d ${repo_path}/out/RPMS/repodata ]] && { rm -r ${repo_path}/out/RPMS/repodata; echo 'Clearing repodata' ; }"