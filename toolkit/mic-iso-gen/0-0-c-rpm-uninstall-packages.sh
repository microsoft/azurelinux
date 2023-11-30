#!/bin/bash

set -x

ls -la init

cat > init <<EOF
mount -t proc proc /proc
/lib/systemd/systemd
EOF
chmod 775 init

rpm -e policycoreutils-devel-3.2-1.cm2.x86_64
rpm -e policycoreutils-python-utils-3.2-1.cm2.noarch
rpm -e policycoreutils-python3-3.2-1.cm2.noarch
rpm -e python3-audit-3.0.6-8.cm2.x86_64
rpm -e audit-3.0.6-8.cm2.x86_64
rpm -e core-packages-base-image-2.0-8.cm2.x86_64
rpm -e bc-1.07.1-4.cm2.x86_64
rpm -e chrony-4.1-3.cm2.x86_64
rpm -e bind-utils-9.16.44-1.cm2.x86_64
rpm -e bind-libs-9.16.44-1.cm2.x86_64
rpm -e bind-license-9.16.44-1.cm2.noarch
rpm -e bridge-utils-1.7.1-2.cm2.x86_64
rpm -e ca-certificates-2.0.0-13.cm2.noarch
rpm -e selinux-policy-devel-2.20221101-5.cm2.noarch
rpm -e checkpolicy-3.2-1.cm2.x86_64
rpm -e core-packages-container-2.0-8.cm2.x86_64
rpm -e ca-certificates-base-1:2.0.0-13.cm2.noarch
rpm -e ca-certificates-tools-1:2.0.0-13.cm2.noarch
rpm -e p11-kit-trust-0.24.1-1.cm2.x86_64
rpm -e chkconfig-1.20-4.cm2.x86_64
rpm -e cloud-init-23.3-1.cm2.noarch
rpm -e cronie-anacron-1.5.7-3.cm2.x86_64
rpm -e cronie-1.5.7-3.cm2.x86_64
rpm -e cryptsetup-2.4.3-4.cm2.x86_64
rpm -e curl-8.3.0-2.cm2.x86_64
rpm -e sudo-1.9.14p3-1.cm2.x86_64
rpm -e openldap-2.4.57-8.cm2.x86_64
rpm -e cyrus-sasl-lib-2.1.28-4.cm2.x86_64
rpm -e dbus-1.15.2-4.cm2.x86_64
rpm -e lvm2-2.03.15-3.cm2.x86_64
# rpm -e device-mapper-event-2.03.15-3.cm2.x86_64
# rpm -e device-mapper-event-libs-2.03.15-3.cm2.x86_64
rpm -e dhcp-client-4.4.2-6.cm2.x86_64
rpm -e dhcp-libs-4.4.2-6.cm2.x86_64
rpm -e policycoreutils-3.2-1.cm2.x86_64
rpm -e diffutils-3.8-2.cm2.x86_64
# rpm -e dracut-megaraid-055-99.cm2.x86_64
rpm -e file-5.40-2.cm2.x86_64
rpm -e gawk-5.1.1-1.cm2.x86_64
rpm -e gzip-1.12-2.cm2.x86_64
rpm -e iptables-1.8.7-4.cm2.x86_64
rpm -e iana-etc-20211115-2.cm2.noarch
rpm -e initramfs-2.0-13.cm2.x86_64
rpm -e iproute-5.15.0-3.cm2.x86_64
rpm -e irqbalance-1.8.0-4.cm2.x86_64
rpm -e libaio-0.3.112-4.cm2.x86_64
rpm -e libdb-5.3.28-7.cm2.x86_64
rpm -e libedit-3.1.20210910-1.cm2.x86_64
rpm -e libmnl-1.0.4-6.cm2.x86_64
rpm -e libselinux-utils-3.2-1.cm2.x86_64
rpm -e libsemanage-python3-3.2-2.cm2.x86_64
rpm -e libtasn1-4.19.0-1.cm2.x86_64
rpm -e libtool-2.4.6-8.cm2.x86_64
rpm -e libuv-1.43.0-1.cm2.x86_64
rpm -e lmdb-libs-0.9.29-1.cm2.x86_64
# rpm -e logrotate-3.20.1-1.cm2.x86_64
rpm -e m4-1.4.19-2.cm2.x86_64
rpm -e make-4.3-3.cm2.x86_64
rpm -e mariner-repos-2.0-8.cm2.noarch
rpm -e mariner-repos-extras-2.0-8.cm2.noarch
rpm -e mariner-repos-microsoft-2.0-8.cm2.noarch
rpm -e mariner-repos-shared-2.0-8.cm2.noarch
rpm -e mpfr-4.1.0-2.cm2.x86_64
rpm -e nettle-3.7.3-3.cm2.x86_64
rpm -e net-tools-2.10-3.cm2.x86_64
rpm -e newt-0.52.21-5.cm2.x86_64
rpm -e openssh-clients-8.9p1-2.cm2.x86_64
rpm -e p11-kit-0.24.1-1.cm2.x86_64
rpm -e procps-ng-3.3.17-2.cm2.x86_64
rpm -e python3-configobj-5.0.6-7.cm2.noarch
rpm -e python3-jinja2-3.0.3-2.cm2.noarch
rpm -e python3-jsonpatch-1.32-1.cm2.noarch
rpm -e python3-jsonpointer-2.2-1.cm2.noarch
rpm -e python3-jsonschema-2.6.0-6.cm2.noarch
rpm -e python3-markupsafe-2.1.0-1.cm2.x86_64
rpm -e python3-netifaces-0.11.0-1.cm2.x86_64
rpm -e python3-oauthlib-2.1.0-7.cm2.noarch
rpm -e python3-prettytable-3.2.0-2.cm2.noarch
rpm -e python3-requests-2.27.1-6.cm2.noarch
rpm -e python3-urllib3-1.26.18-1.cm2.noarch
rpm -e python3-wcwidth-0.2.5-1.cm2.noarch
rpm -e PyYAML-5.4.1-1.cm2.x86_64
rpm -e secilc-3.2-1.cm2.x86_64
rpm -e selinux-policy-modules-2.20221101-5.cm2.noarch
rpm -e selinux-policy-2.20221101-5.cm2.noarch
rpm -e setools-console-4.4.0-2.cm2.x86_64
rpm -e setools-python3-4.4.0-2.cm2.x86_64
rpm -e slang-2.3.2-4.cm2.x86_64
rpm -e tar-1.34-2.cm2.x86_64
rpm -e tzdata-2023c-1.cm2.noarch
rpm -e which-2.21-8.cm2.x86_64
echo "--- success 1 ---"
rpm -e libselinux-python3-3.2-1.cm2.x86_64
rpm -e python3-certifi-2023.05.07-1.cm2.noarch
rpm -e python3-charset-normalizer-2.0.11-2.cm2.noarch
rpm -e python3-pyOpenSSL-18.0.0-8.cm2.noarch
rpm -e python3-setuptools-3.9.14-8.cm2.noarch
echo "--- success 2 ---"
rpm -e python3-cryptography-3.3.2-5.cm2.x86_64
rpm -e python3-idna-3.3-1.cm2.noarch
rpm -e python3-packaging-21.3-1.cm2.noarch
rpm -e python3-pyasn1-0.4.8-1.cm2.noarch
rpm -e python3-pyparsing-3.0.7-1.cm2.noarch
rpm -e python3-six-1.16.0-2.cm2.noarch
echo "--- success 3 ---"
rpm -e python3-asn1crypto-1.5.1-1.cm2.noarch
rpm -e python3-cffi-1.15.0-3.cm2.x86_64
rpm -e python3-pycparser-2.21-1.cm2.noarch
echo "--- success 4 ---"

rpm -e dnf-4.8.0-2.cm2.noarch
rpm -e python3-dnf-4.8.0-2.cm2.noarch
rpm -e dnf-data-4.8.0-2.cm2.noarch
rpm -e python3-curses-3.9.14-8.cm2.x86_64
rpm -e python3-gpg-1.16.0-2.cm2.x86_64
rpm -e python3-hawkey-0.63.1-2.cm2.x86_64
rpm -e python3-libcomps-0.1.18-2.cm2.x86_64
rpm -e python3-libdnf-0.63.1-2.cm2.x86_64
rpm -e libdnf-0.63.1-2.cm2.x86_64

rpm -e libmodulemd-2.13.0-2.cm2.x86_64
rpm -e librepo-1.15.1-1.cm2.x86_64
rpm -e libyaml-0.2.5-3.cm2.x86_64
rpm -e zchunk-1.1.16-3.cm2.x86_64
rpm -e zchunk-libs-1.1.16-3.cm2.x86_64

echo "--- success 5 ---"

rpm -e tdnf-plugin-repogpgcheck-3.5.2-2.cm2.x86_64
rpm -e tdnf-3.5.2-2.cm2.x86_64
rpm -e tdnf-cli-libs-3.5.2-2.cm2.x86_64
rpm -e libsolv-0.7.24-1.cm2.x86_64
rpm -e ca-certificates-shared-2.0.0-13.cm2.noarch

echo "--- success 6 ---"

rpm -e iputils-20211215-2.cm2.x86_64
rpm -e libcomps-0.1.18-2.cm2.x86_64
rpm -e gpgme-1.16.0-2.cm2.x86_64
rpm -e gnupg2-2.4.0-2.cm2.x86_64
rpm -e pinentry-1.2.0-1.cm2.x86_64
rpm -e npth-1.6-4.cm2.x86_64
rpm -e libksba-1.6.3-1.cm2.x86_64
rpm -e libassuan-2.5.5-2.cm2.x86_64

echo "--- success 7 ---"

#
# explicit packages we want to keep
#
# kernel-hci-5.15.137.1-1.cm2.x86_64
# systemd-250.3-19.cm2.x86_64
#
# rpms
#  mariner-rpm-macros-2.0-24.cm2.noarch
#  python3-rpm-4.18.0-4.cm2.x86_64
#  rpm-build-libs-4.18.0-4.cm2.x86_64
#  rpm-devel-4.18.0-4.cm2.x86_64
#

# --- rpm related packages
# rpm -e libgomp-11.2.0-7.cm2.x86_64 # needed by rpm-build
# rpm -e libxml2-2.10.4-2.cm2.x86_64 # needed by libgopm
# rpm -e popt-devel-1.18-1.cm2.x86_64 # needed by rpm-devel
# rpm -e zstd-1.5.0-1.cm2.x86_64 # needed by zstd-devel
# rpm -e zstd-devel-1.5.0-1.cm2.x86_64 # needed by rpm-devel, elfutils-devel

# rpm -e  elfutils-0.186-2.cm2.x86_64 # needed by rpm-build
# rpm -e  elfutils-default-yama-scope-0.186-2.cm2.noarch # needed by elfutils
# rpm -e  elfutils-devel-0.186-2.cm2.x86_64
# rpm -e  elfutils-libelf-devel-0.186-2.cm2.x86_64

# rpm -e xz-devel-5.2.5-1.cm2.x86_64 # needed by eftutils-dev
# rpm -e zlib-devel-1.2.13-2.cm2.x86_64 # needed by eftutils-dev
# --- ---

# ---- core packages required indirectly
# rpm -e libstdc++-11.2.0-7.cm2.x86_64
# rpm -e glibc-2.35-6.cm2.x86_64
# rpm -e bzip2-libs-1.0.8-1.cm2.x86_64
# rpm -e e2fsprogs-libs-1.46.5-3.cm2.x86_64
 
