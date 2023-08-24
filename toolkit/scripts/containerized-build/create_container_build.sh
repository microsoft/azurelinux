#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

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

help() {
echo "
Usage:
sudo make containerized-rpmbuild [REPO_PATH=/path/to/CBL-Mariner] [MODE=test|build] [VERSION=1.0|2.0] [MOUNTS=/path/in/host:/path/in/container] [ENABLE_REPO=y] [SPECS_DIR=/path/to/SPECS_DIR/to/use]

Starts a docker container with the specified version of mariner.

Optional arguments:
    REPO_PATH:      path to the CBL-Mariner repo root directory. default: "current directory"
    SPECS_DIR:      The SPECS_DIR variable is reused from base Makefile. By Default it points to 'CBL-Mariner/SPECS'
                    We can override the SPECS_DIR to extended e.g by appeneding: SPECS_DIR=path/to/SPECS-EXTENDED
    MODE            build or test. default:"build"
                        In 'test' mode it will use a pre-built mariner chroot image.
                        In 'build' mode it will use the latest published container.
    VERISION        1.0 or 2.0. default: "2.0"
    MOUNTS          Mount a host directory into container. Should be of form '/host/dir:/container/dir'. For multiple mounts, please use space (\" \") as delimiter
                        e.g. MOUNTS=\"/host/dir1:/container/dir1 /host/dir2:/container/dir2\"
    ENABLE_REPO:    Set to 'y' to use local RPMs to satisfy package dependencies. default: "n"

To see help, run 'sudo make containerized-rpmbuild-help'
"
}

build_chroot() {
    pushd "${repo_path}/toolkit"
    echo "Building worker chroot..."
    make graph-cache REBUILD_TOOLS=y > /dev/null
    popd
}

build_tools() {
    pushd "${repo_path}/toolkit"
    echo "Building required tools..."
    make go-srpmpacker REBUILD_TOOLS=y > /dev/null
    make go-depsearch REBUILD_TOOLS=y > /dev/null
    make go-grapher REBUILD_TOOLS=y > /dev/null
    make go-specreader REBUILD_TOOLS=y > /dev/null
    popd
}

build_graph() {
    pushd "${repo_path}/toolkit"
    echo "Building dependency graph..."
    make workplan > /dev/null
    popd
}

# exit if not running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "\033[31mThis requires running as root\033[0m "
  exit
fi

script_dir=$(realpath $(dirname "${BASH_SOURCE[0]}"))
tmp_dir=${script_dir%'/toolkit'*}/build/containerized-rpmbuild/tmp
mkdir -p ${tmp_dir}
topdir=/usr/src/mariner
enable_local_repo=false
specs_dir=""

while (( "$#")); do
  case "$1" in
    -m ) mode="$2"; shift 2 ;;
    -v ) version="$2"; shift 2 ;;
    -p ) repo_path="$(realpath $2)"; shift 2 ;;
    -mo ) extra_mounts="$2"; shift 2 ;;
    -r ) enable_local_repo=true; shift ;;
    -s ) specs_dir="$(realpath $2)"; shift 2;;
    -h ) help; exit 1 ;;
    ? ) echo -e "ERROR: INVALID OPTION.\n\n"; help; exit 1 ;;
  esac
done

# Assign default values
[[ -z "${repo_path}" ]] && repo_path=${script_dir} && repo_path=${repo_path%'/toolkit'*}
[[ ! -d "${repo_path}" ]] && { print_error " Directory ${repo_path} does not exist"; exit 1; }
[[ -z "${mode}" ]] && mode="build"
[[ -z "${version}" ]] && version="2.0"

cd "${script_dir}"  || { echo "ERROR: Could not change directory to ${script_dir}"; exit 1; }

# ==================== Setup ====================

# Get Mariner GitHub branch at $repo_path
repo_branch=$(git -C ${repo_path} rev-parse --abbrev-ref HEAD)

# Generate text based on mode (Use figlet to generate splash text once available on Mariner)
if [[ "${mode}" == "build" ]]; then
    echo -e "\033[31m -----------------------------------------------------------------------------------------\033[0m" > ${tmp_dir}/splash.txt
    echo -e "\033[31m ----------------------------------- MARINER BUILDER ! ----------------------------------- \033[0m" >> ${tmp_dir}/splash.txt
    echo -e "\033[31m -----------------------------------------------------------------------------------------\033[0m" >> ${tmp_dir}/splash.txt
else
    echo -e "\033[31m -----------------------------------------------------------------------------------------\033[0m" > ${tmp_dir}/splash.txt
    echo -e "\033[31m ----------------------------------- MARINER TESTER ! ------------------------------------ \033[0m" >> ${tmp_dir}/splash.txt
    echo -e "\033[31m -----------------------------------------------------------------------------------------\033[0m" >> ${tmp_dir}/splash.txt
fi

# ============ Populate SRPMS ============
# Populate ${repo_path}/build/INTERMEDIATE_SRPMS with SRPMs, that can be used to build RPMs in the container
pushd "${repo_path}/toolkit"
echo "Populating Intermediate SRPMs..."
if [[ ( ! -f "${repo_path}/toolkit/out/tools/srpmpacker" ) ]]; then build_tools; fi
make input-srpms SRPM_FILE_SIGNATURE_HANDLING="update" > /dev/null
popd

# ============ Map chroot mount ============
if [[ "${mode}" == "build" ]]; then
    # Create a new directory and map it to chroot directory in container
    build_mount="${repo_path}/build/container-build"
    buildroot_mount="${repo_path}/build/container-buildroot"
    if [ -d "${build_mount}" ]; then rm -Rf ${build_mount}; fi
    if [ -d "${buildroot_mount}" ]; then rm -Rf ${buildroot_mount}; fi
    mkdir ${build_mount}
    mkdir ${buildroot_mount}
    mounts="${mounts} ${build_mount}:${topdir}/BUILD ${buildroot_mount}:${topdir}/BUILDROOT"
fi

# ============ Setup tools ============
# Copy relavant build tool executables from ${repo_path}/tools/out
echo "Setting up tools..."
if [[ ( ! -f "${repo_path}/toolkit/out/tools/depsearch" ) || ( ! -f "${repo_path}/toolkit/out/tools/grapher" ) || ( ! -f "${repo_path}/toolkit/out/tools/specreader" ) ]]; then build_tools; fi
if [[ ! -f "${repo_path}/build/pkg_artifacts/graph.dot" ]]; then build_graph; fi
cp ${repo_path}/toolkit/out/tools/depsearch ${tmp_dir}/
cp ${repo_path}/toolkit/out/tools/grapher ${tmp_dir}/
cp ${repo_path}/toolkit/out/tools/specreader ${tmp_dir}/
cp ${repo_path}/build/pkg_artifacts/graph.dot ${tmp_dir}/

# ========= Setup mounts =========
echo "Setting up mounts..."

mounts="${mounts} ${repo_path}/out/RPMS:/mnt/RPMS ${tmp_dir}:/mariner_setup_dir"
# Add extra 'build' mounts
if [[ "${mode}" == "build" ]]; then
    mounts="${mounts} ${repo_path}/build/INTERMEDIATE_SRPMS:/mnt/INTERMEDIATE_SRPMS $specs_dir:${topdir}/SPECS"
fi

rm -f ${tmp_dir}/mounts.txt
for mount in $mounts $extra_mounts; do
    host_mount_path=$(realpath ${mount%%:*}) #remove suffix starting with ":"
    container_mount_path="${mount##*:}"      #remove prefix ending in ":"
    if [[ -d $host_mount_path ]]; then
        echo "$host_mount_path -> $container_mount_path"  >> "${tmp_dir}/mounts.txt"
        mount_arg=" $mount_arg -v '$host_mount_path:$container_mount_path' "
    else
        echo "WARNING: '$host_mount_path' does not exist. Skipping mount."
        echo "WARNING: '$host_mount_path' does not exist. Skipping mount."  >> "${tmp_dir}/mounts.txt"
    fi
done

# Copy resources into container
cp resources/welcome.txt $tmp_dir
sed -i "s~<REPO_PATH>~${repo_path}~" $tmp_dir/welcome.txt
sed -i "s~<REPO_BRANCH>~${repo_branch}~" $tmp_dir/welcome.txt
cp resources/setup_functions.sh $tmp_dir/setup_functions.sh
sed -i "s~<TOPDIR>~${topdir}~" $tmp_dir/setup_functions.sh

# ============ Build the dockerfile ============
dockerfile="${script_dir}/resources/mariner.Dockerfile"

if [[ "${mode}" == "build" ]]; then # Configure base image
    echo "Importing chroot into docker..."
    chroot_file="${repo_path}/build/worker/worker_chroot.tar.gz"
    if [[ ! -f "${chroot_file}" ]]; then build_chroot; fi
    chroot_hash=$(sha256sum "${chroot_file}" | cut -d' ' -f1)
    # Check if the chroot file's hash has changed since the last build
    if [[ ! -f "${tmp_dir}/hash" ]] || [[ "$(cat "${tmp_dir}/hash")" != "${chroot_hash}" ]]; then
        echo "Chroot file has changed, updating..."
        echo "${chroot_hash}" > "${tmp_dir}/hash"
        docker import "${chroot_file}" "mcr.microsoft.com/cbl-mariner/containerized-rpmbuild:${version}"
    else
        echo "Chroot is up-to-date"
    fi
    container_img="mcr.microsoft.com/cbl-mariner/containerized-rpmbuild:${version}"
else
    container_img="mcr.microsoft.com/cbl-mariner/base/core:${version}"
fi

# ================== Launch Container ==================
echo "Checking if build env is up-to-date..."
docker_image_tag="mcr.microsoft.com/cbl-mariner/${USER}-containerized-rpmbuild:${version}"
docker build -q \
                -f "${dockerfile}" \
                -t "${docker_image_tag}" \
                --build-arg container_img="$container_img" \
                --build-arg version="$version" \
                --build-arg enable_local_repo="$enable_local_repo" \
                --build-arg mariner_repo="$repo_path" \
                .

echo "docker_image_tag is ${docker_image_tag}"

bash -c "docker run --rm \
                    ${mount_arg} \
                    -it ${docker_image_tag} /bin/bash; \
                    [[ -d ${repo_path}/out/RPMS/repodata ]] && { rm -r ${repo_path}/out/RPMS/repodata; echo 'Clearing repodata' ; }"
