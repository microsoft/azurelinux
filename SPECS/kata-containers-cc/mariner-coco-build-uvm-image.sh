#!/bin/bash

set -o errexit

[ -n "${DEBUG:-}" ] && set -o xtrace

readonly SCRIPT_NAME="$0"
readonly SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
readonly IMAGE_BUILD_ROOT=`mktemp --directory -t mariner-coco-build-uvm-image-XXXXXX`
readonly IMAGE_LINK="/opt/confidential-containers/share/kata-containers/kata-containers.img"
readonly IMAGE_LINK_TARGET="/var/cache/mariner/uvm/kata-containers.img"
readonly KERNEL_LINK="/opt/confidential-containers/share/kata-containers/vmlinux.container"
readonly KERNEL_LINK_TARGET="/usr/share/cloud-hypervisor/vmlinux.bin"

COMMAND=""

usage()
{
    cat << EOF

Usage: ${SCRIPT_NAME} [options]

This script builds the kata UVM image for Mariner.

This script is called at via mariner-coco-build-uvm-image.service.

Options:
  -h            Show this help message

  -c            Check if an image is already generated for the current
                kernel, and if so, simply exit
EOF

    exit $1
}

parse_args()
{
    while getopts "ch:" opt
    do
        case $opt in
            c) COMMAND="check" ;;
            h) usage 0 ;;
            *) usage 1 ;;
        esac
    done
    shift $(($OPTIND - 1))

    if [ -n "$*" ]; then
        error "Unhandled options: '$*'"
        usage 1
    fi
}

main()
{
    parse_args $*

    if [ "$COMMAND" = "check" ]; then
        local linked_image=$(readlink -n "${IMAGE_LINK}" || :)
        if [ "${IMAGE_LINK_TARGET}" = "${linked_image}" ] ; then
            if [ -f "${linked_image}" ] ; then
                echo "symlink=${IMAGE_LINK} already points to UVM kernel=${IMAGE_LINK_TARGET}"
                echo "Nothing to generate. Exiting."
                rm -rf "${IMAGE_BUILD_ROOT}"
                exit 0
            fi
        fi
    fi
    
    cd "${IMAGE_BUILD_ROOT}"
    sudo tar --same-owner -xvf "${SCRIPT_DIR}/mariner-uvm-rootfs.tar.gz"

    DEBUG=1 \
    NSDAX_BIN=/opt/confidential-containers/share/kata-containers/scripts/nsdax \
    /opt/confidential-containers/share/kata-containers/scripts/image_builder.sh ./mariner_rootfs

    install -D -m 0644 kata-containers.img "$IMAGE_LINK_TARGET"
    ln -sf "${IMAGE_LINK_TARGET}" "${IMAGE_LINK}"
    ln -sf "${KERNEL_LINK_TARGET}" "${KERNEL_LINK}"

    # TODO: don't leak these files when exiting due to an error.
    rm -rf "${IMAGE_BUILD_ROOT}"

    sed -i -e "s|kernel = .*$|kernel = \"$KERNEL_LINK_TARGET\"|" /opt/confidential-containers/share/defaults/kata-containers/configuration-clh.toml
    sed -i -e "s|image = .*$|image = \"$IMAGE_LINK_TARGET\"|" /opt/confidential-containers/share/defaults/kata-containers/configuration-clh.toml
}

echo "$0 args: $*"
main $*
