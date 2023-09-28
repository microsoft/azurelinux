#! /bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

TOPDIR=<TOPDIR>
SPECS_DIR=$TOPDIR/SPECS
SOURCES_DIR=$TOPDIR/SOURCES
RPMS_DIR=$TOPDIR/RPMS
SRPMS_DIR=$TOPDIR/SRPMS
IS_REPO_ENABLED=false

# General setup

## Mariner macro files used during spec parsing (as defined in toolkit/scripts/rpmops.sh)
DEFINES=(-D "with_check 1")
MACROS=()
for macro_file in "$SPECS_DIR"/mariner-rpm-macros/macros* "$SPECS_DIR"/pyproject-rpm-macros/macros.pyproject "$SPECS_DIR"/perl/macros.perl
do
  MACROS+=("--load=$macro_file")
done

## Create SOURCES_DIR
mkdir -p SOURCES_DIR

# Create symlink from SPECS/ to SOURCES/ when rpm is called
rpm() {
    local args=("$@")
    command "$FUNCNAME" "${args[@]}"
    if [[ ${args} = *"i"* ]]; then
        for ((i = 0; i < ${#args[@]}; ++i)); do
            if [[ ${args[$i]} = *".src.rpm"* ]]; then
                local SPEC=${args[$i]}
                SPEC=${SPEC##*/} #remove prefix ending in "/"
                SPEC=${SPEC%-*} #remove last suffix of type -*
                SPEC=${SPEC%-*} #remove last suffix of type -*
                SPEC=${SPEC%\**}
                ln -sf $SPECS_DIR/$SPEC/* $SOURCES_DIR/
            fi
        done
    fi
    rm -f $SPECS_DIR/*.spec
    rm -f $SOURCES_DIR/*.spec
    rm -f $SOURCES_DIR/*.signatures.json
}

# Installs srpm, pkg dependencies and builds pkg
build_pkg() {
    local PKG=("$@")
    if [ -z "$PKG" ]; then echo "Please provide pkg name"; return; fi
    rpm -ihv /mnt/INTERMEDIATE_SRPMS/$PKG*.src.rpm
    $(install_dependencies $PKG)
    rpmbuild -ba $SPECS_DIR/$PKG/$PKG.spec
}

# Show help on useful commands
show_help() {
    echo -e "`cat /mariner_setup_dir/welcome.txt`"
    cat /mariner_setup_dir/mounts.txt
    echo -e "* \n* \e[31mLocal repo information:\e[0m"
    if [[ "${IS_REPO_ENABLED}" == "true" ]]; then
        echo -e "*\tLocal repo is enabled. Package dependencies will be installed from $RPMS_DIR, /repo and upstream server"
    else
        echo -e "*\tLocal repo is not enabled. Package dependencies will be installed from upstream server"
    fi
    echo "******************************************************************************************"
}

# Refresh repo cache with newly built RPM, use Mariner specific DEFINES
rpmbuild() {
    local args=("$@")
    command "$FUNCNAME" "${DEFINES[@]}" "${args[@]}"
    if [[ ${IS_REPO_ENABLED} = true ]] ; then
        refresh_local_repo
        tdnf makecache
    fi
}

# Refresh metadata for local RPMs' repo
refresh_local_repo() {
    echo "-------- refreshing the local repo ---------"
    pushd $RPMS_DIR
    createrepo .
    popd
}

# Satisfy dependencies from local RPMs
enable_local_repo() {
    echo "-------- enabling local repo ---------"
    IS_REPO_ENABLED=true
    tdnf install -y createrepo
    mv /etc/yum.repos.d/local_repo.disabled_repo /etc/yum.repos.d/local_repo.repo
    url_list=""
    baseurls=$(cat /etc/yum.repos.d/local_repo.repo | grep baseurl | cut -d '=' -f 2)
    prefixToRemove="file://"
    for urlWithPrefix in $baseurls
    do
        url="${urlWithPrefix#$prefixToRemove}" #remove 'file://' prefix
        mkdir -p $url || { echo -e "\033[31m WARNING: Could not mkdir at $url, continuing\033[0m"; continue; }
        pushd $url
        createrepo .
        popd
        url_list+=" $url"
    done
    echo "-------- The local repo is enabled ---------"
    echo "--- Package dependencies will be installed from $url_list and upstream server ---"
    #echo "You can install the following packages from it:"
    #tdnf repoquery --repoid=local_build_repo 2>/dev/null
}

# Update dependency graph using build tools
update_specs_metadata() {
    # update specs.json
    /mariner_setup_dir/specreader --dir=$SPECS_DIR  --srpm-dir="/mnt/INTERMEDIATE_SRPMS/" --output=/mariner_setup_dir/specs.json --dist-tag="containerized" --rpm-dir="/mnt/RPMS/"
    # update graph.dot
    /mariner_setup_dir/grapher --input=/mariner_setup_dir/specs.json --output=/mariner_setup_dir/graph.dot
}

# Install package dependencies using depsearch tool
install_dependencies_depsearch() {
    local PKG=("$@")
    if [ -z "$PKG" ]; then echo "Please provide pkg name"; return; fi
    echo "-------- installing dependencies ---------"
    dep_list=$(get_pkg_dependency $PKG)
    for dependency in $dep_list
    do
        tdnf install -y $dependency 2>&1
    done
}

# Get dependencies of a package using depsearch tool
get_pkg_dependency() {
    local PKG=("$@")
    if [ -z "$PKG" ]; then echo "Please provide pkg name"; return; fi
    /mariner_setup_dir/depsearch --input=/mariner_setup_dir/graph.dot  --packages=$PKG --reverse
}

# Install package dependencies listed as BuildRequires in spec
install_dependencies() {
    local PKG=("$@")
    if [ -z "$PKG" ]; then echo "Please provide pkg name"; return; fi
    echo "-------- installing build dependencies ---------"
    spec_file=$SPECS_DIR/$PKG/$PKG.spec
    dep_list=$(grep "BuildRequires:" $spec_file | cut -d ':' -f 2)
    for dependency in $dep_list
    do
        tdnf install -y $dependency 2>&1
    done
}

# use Mariner specific DEFINES
rpmspec() {
    local args=("$@")
    command "$FUNCNAME" "${DEFINES[@]}" "${args[@]}"
}
