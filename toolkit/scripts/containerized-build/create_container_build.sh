#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

script_dir=$( realpath "$(dirname "$0")" )
script_name=$(basename "$0")
specs_dir=/usr/src/mariner/SPECS
sources_dir=/usr/src/mariner/SOURCES

echo "***** script_name is ${script_name}"
echo "***** script_dir is ${script_dir}"

switch_to_red_text() {
    printf "\e[31m"
}

switch_to_normal_text() {
    printf "\e[0m"
}

print_error() {
    echo ""
    switch_to_red_text
    echo ">>>> ERROR: $1"
    switch_to_normal_text
    echo ""
}

function help {
echo "Usage: ${script_name} [REPO_PATH=/path/to/CBL-Mariner] [MODE=test|build] [VERSION=1.0|2.0] [MOUNTS= /src/path:/dst/path] [--help]

Starts a docker container with the specified version of mariner. Mounts REPO_PATH/out/RPMS
to /mnt/RPMS. The mounted repo can be enabled by running /enable_repo.sh in the container.

In the 'build' mode, mounts REPO_PATH/build/INTERMEDIATE_SRPMS at /mnt/INTERMEDIATE_SRPMS
and REPO_PATH/SPECS at ${specs_dir}

Optional arguments:
    REPO_PATH:      path to the CBL-Mariner repo root directory. default: "current directory"
    MODE            build or test. In 'test' mode it will use a pre-built mariner chroot image. 
                                In 'build' mode it will use the latest published container.default:"build"
    VERISION        1.0 or 2.0........................................................default: "2.0"
    MOUNTS          mount a directory into the container. Should be of the form '/src/dir:/dest/dir'. 
                                Can be specified multiple times..........default: ""
    --help          print this help message
"
}

while getopts "m:v:p:mo:h" OPTIONS; do
    case ${OPTIONS} in
        m ) mode="$OPTARG" ;;
        v ) version="$OPTARG" ;;
        p ) repo_path="$OPTARG" ;;
        h ) help; exit 0 ;;
        ? ) echo -e "ERROR: INVALID OPTION.\n\n"; help; exit 1 ;;
    esac
done

echo "***** mode is ${mode}"
echo "***** repo_path is ${repo_path}"
echo "***** extra_mounts is ${extra_mounts}"
echo "***** version is ${version}"

[[ -z "${repo_path}" ]] && repo_path="$(dirname $0)" && repo_path=${repo_path%'/toolkit'*}
[[ ! -d "${repo_path}" ]] && { print_error " Directory ${repo_path} does not exist"; exit 1; }
[[ -z "${mode}" ]] && mode="build"
[[ -z  "${version}" ]] && version="2.0"
echo "***** mode is ${mode}"
echo "***** repo_path is ${repo_path}"
echo "***** extra_mounts is ${extra_mounts}"
echo "***** version is ${version}"

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
sudo make input-srpms

# ========= Setup mounts + Welcome file =========
cd "${script_dir}"
echo "Creating welcome message and checking mounts..."
cat "${script_dir}/resources/welcome_1.txt.template" > "${build_dir}/welcome.txt"

mounts="${repo_path}/out/RPMS:/mnt/RPMS"
if [[ "${mode}" == "build" ]]; then
    # Add extra build mounts
    mounts="${mounts} ${repo_path}/build/INTERMEDIATE_SRPMS:/mnt/INTERMEDIATE_SRPMS ${repo_path}/SPECS:${specs_dir}"
fi

for mount in $mounts $extra_mounts; do
    if [[ -d "${mount%%:*}" ]]; then
        echo "Will mount '${mount%%:*}' to '${mount##*:}'"
        echo "echo \"*        '${mount%%:*}' -> '${mount##*:}'\""  >> "${build_dir}/welcome.txt"
    else
        echo "WARNING: '${mount%%:*}' does not exist. Skipping mount."
        echo "echo \"*        WARNING: '${mount%%:*}' does not exist. Skipping mount.\""  >> "${build_dir}/welcome.txt"
        continue
    fi
    mount_arg=" $mount_arg -v '$mount' "
done

cat "${script_dir}/resources/welcome_2.txt.template" >> "${build_dir}/welcome.txt"
sed -i "s~<REPO_PATH>~${repo_path}~" "${build_dir}/welcome.txt"
sed -i "s~<SPECS_DIR>~${specs_dir}~" "${script_dir}/resources/add_shell_functions.txt"
sed -i "s~<SOURCES_DIR>~${sources_dir}~" "${script_dir}/resources/add_shell_functions.txt"

# ============ Build the dockerfile ============
echo "Updating dockerfile from template..."
dockerfile="${build_dir}/mariner.Dockerfile"
echo "***** dockerfile is ${dockerfile}"
echo "***** build_dir is ${build_dir}"
echo "***** script_dir is ${script_dir}"
echo "***** repo_path is ${repo_path}"
echo "***** mounts is ${mounts}"
echo "***** version is ${version}"
echo "***** mount_arg is ${mount_arg}"
echo "***** version is ${version}"

if [[  "${mode}" == "build" ]]; then # Select the correct dockerfile
    cp "${script_dir}/resources/build.Dockerfile.template" "${dockerfile}"
else
    cp "${script_dir}/resources/test.Dockerfile.template" "${dockerfile}"
fi
sed -i "s/<VER>/${version}/" "${dockerfile}"

if [[  "${mode}" == "build" ]]; then # Configure base image
    echo "Importing chroot into docker..."
    chroot_file="${repo_path}/build/worker/worker_chroot.tar.gz"
    [[ ! -f "${chroot_file}" ]] && { print_error "No chroot file found at '${chroot_file}'"; exit 1 ; }
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
docker_image_name="mcr.microsoft.com/cbl-mariner/${USER}_tmp_pkgtest_${version}"
sudo docker build -q -f "${dockerfile}" -t "${docker_image_name}" .

echo "***** docker_image_name is ${docker_image_name}..."
sudo bash -c "docker run --rm \
                    ${mount_arg} \
                    -it ${docker_image_name} /bin/bash; \
                    [[ -d ${repo_path}/out/RPMS/repodata ]] && { rm -r ${repo_path}/out/RPMS/repodata; echo 'Clearing repodata' ; }"