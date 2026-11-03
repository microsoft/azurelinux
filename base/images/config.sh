#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,distroless-minimal,*|*,distroless-base,*|*,distroless-debug,*)
        exec /image/config-container-base.sh
        ;;
esac

case ",${kiwi_profiles:-}," in
    *,marketplace-gen2,*)
        kernel_arch="$(rpm -q --qf '%{ARCH}\n' kernel)"
        case "$kernel_arch" in
            aarch64) exit 0 ;;
            x86_64) ;;
            *)
                echo "Experimental Marketplace boot requires one x86_64 kernel; found: $kernel_arch" >&2
                exit 1
                ;;
        esac

        install -d /etc/cloud/cloud.cfg.d /etc/modules-load.d /etc/sysctl.d
        printf 'datasource_list: [Azure, NoCloud, None]\n' \
            > /etc/cloud/cloud.cfg.d/90-azure-datasource.cfg
        printf 'kernel.printk = 4 4 1 7\n' > /etc/sysctl.d/10-console-messages.conf
        printf 'net.ipv6.conf.eth0.accept_dad = 0\n' > /etc/sysctl.d/90-eth0-no-dad.conf
        printf 'hv_netvsc\nhv_sock\n' > /etc/modules-load.d/90-noinitrd-hyperv.conf
        grep -qE '^[[:space:]]*nodelay([[:space:]]*(#.*)?)?$' /etc/dhcpcd.conf || {
            status=$?
            if [[ "$status" != 1 ]]; then
                exit "$status"
            fi
            printf '\nnodelay\n' >> /etc/dhcpcd.conf
        }
        ;;
esac
