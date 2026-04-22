#!/bin/bash
#
# shim-find-debuginfo.sh
# Copyright (C) 2017 Peter Jones <Peter Jones@random>
#
# Distributed under terms of the GPLv3 license.
#
set -e
set -u

mainarch=$1 && shift
if [ $# == 1 ]; then
    altarch=$1 && shift
fi
if ! [ -v RPM_BUILD_ROOT ]; then
    echo "RPM_BUILD_ROOT must be set" 1>&2
    exit 1
fi

findsource()
{
    (
        cd ${RPM_BUILD_ROOT}
        find usr/src/debug/ -type d | sed "s,^,%dir /,"
        find usr/src/debug/ -type f | sed "s,^,/,"
    )
}

finddebug()
{
    arch=$1 && shift
    declare -a dirs=()
    declare -a files=()
    declare -a excludes=()

    pushd ${RPM_BUILD_ROOT} >/dev/null 2>&1
    for x in $(find usr/lib/debug/ -type f -iname *.efi.debug); do
        if ! [ -e "${x}" ]; then
            break
        fi
        if [[ ${x} =~ ${arch}\.efi\.debug$ ]]; then
            files[${#files[@]}]=${x}
        else
            excludes[${#excludes[@]}]=${x}
        fi
    done
    for x in usr/lib/debug/.build-id/*/*.debug ; do
        if ! [ -e "${x}" ]; then
            break
        fi
        link=$(readlink "${x}")
        if [[ ${link} =~ ${arch}\.efi\.debug$ ]]; then
            files[${#files[@]}]=${x}
            files[${#files[@]}]=${x%%.debug}
        else
            excludes[${#excludes[@]}]=${x}
            excludes[${#excludes[@]}]=${x%%.debug}
        fi
    done
    for x in ${files[@]} ; do
        declare name=$(dirname /${x})
        while [ "${name}" != "/" ]; do
            case "${name}" in
            "/usr/lib/debug"|"/usr/lib"|"/usr")
                ;;
            *)
                dirs[${#dirs[@]}]=${name}
                ;;
            esac
            name=$(dirname ${name})
        done
    done

    popd >/dev/null 2>&1
    for x in ${dirs[@]} ; do
        echo "%dir ${x}"
    done | sort | uniq
    for x in ${files[@]} ; do
        echo "/${x}"
    done | sort | uniq
    for x in ${excludes[@]} ; do
        echo "%exclude /${x}"
    done
}

findsource > build-${mainarch}/debugsource.list
finddebug ${mainarch} > build-${mainarch}/debugfiles.list
if [ -v altarch ]; then
    finddebug ${altarch} > build-${altarch}/debugfiles.list
fi
