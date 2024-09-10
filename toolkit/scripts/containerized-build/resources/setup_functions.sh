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

## Create $SOURCES_DIR
mkdir -p $SOURCES_DIR

# Create symlink from SPECS/ to SOURCES/ when rpm is called
rpm() {
    local args=("$@")
    command "$FUNCNAME" "${args[@]}"
    local command_return=$?
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
    return $command_return
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
    echo -e "`cat /azl_setup_dir/welcome.txt`"
    cat /azl_setup_dir/mounts.txt
    echo -e "* \n* \e[31mLocal repo information:\e[0m"
    if [[ "${IS_REPO_ENABLED}" == "true" ]]; then
        echo -e "*\tLocal repo is enabled. Package dependencies will be installed from $RPMS_DIR, /repo and upstream server"
    else
        echo -e "*\tLocal repo is not enabled. Package dependencies will be installed from upstream server"
    fi
    echo "******************************************************************************************"
}

# Refresh repo cache with newly built RPM
rpmbuild() {
    local args=("$@")
    command "$FUNCNAME" "${args[@]}"
    local command_return=$?
    if [[ ${IS_REPO_ENABLED} = true ]] ; then
        refresh_local_repo
        tdnf makecache
    fi
    return $command_return
}

# Refresh metadata for local RPMs' repo
refresh_local_repo() {
    echo "-------- refreshing the local repo ---------"
    pushd $RPMS_DIR
    createrepo --compatibility .
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
        createrepo --compatibility .
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
    /azl_setup_dir/specreader --dir=$SPECS_DIR  --srpm-dir="/mnt/INTERMEDIATE_SRPMS/" --output=/azl_setup_dir/specs.json --dist-tag="containerized" --rpm-dir="/mnt/RPMS/"
    # update graph.dot
    /azl_setup_dir/grapher --input=/azl_setup_dir/specs.json --output=/azl_setup_dir/graph.dot
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
    /azl_setup_dir/depsearch --input=/azl_setup_dir/graph.dot  --packages=$PKG --reverse
}

# Install package dependencies listed as BuildRequires in spec
install_dependencies() {
    # Accept a single argument, which is a pattern to find spec files.
    if [ "$#" -ne 1 ]; then
        echo "Usage: $0 <pkg_pattern>"
        return 1
    fi

    local PKG="$1"

    echo "-------- installing build dependencies ---------"

    # Find all spec files for the package pattern given.
    spec_file_pattern=$SPECS_DIR/$PKG/$PKG.spec
    echo "using spec file pattern: '$spec_file_pattern'"
    spec_files=($spec_file_pattern)

    # Install dependencies for each spec file found, preserving tdnf error codes.
    echo "found ${#spec_files[@]} spec files; installing dependencies for each spec file sequentially"
    exit_code=0
    for spec_file in "${spec_files[@]}"
    do
        echo "installing dependencies for spec file: '$spec_file'"

        # Get the list of dependencies from the spec file.
        mapfile -t dep_list < <(rpmspec -q --buildrequires $spec_file)

        # Install all the dependencies.
        tdnf install -y "${dep_list[@]}" || exit_code=$?
    done

    return $exit_code
}
