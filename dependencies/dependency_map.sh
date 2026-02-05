#!/usr/bin/env bash
set -euo pipefail

# Output: dependency_map.csv
# CSV format:
#   package,dependency
# One dependency per line; packages with no deps get a single line with empty dependency.
#
# This version IGNOREs version/release constraints in Requires lines and outputs only dependency PACKAGE NAMES.

out_csv="${1:-dependency_map.csv}"

csv_escape() {
  local s="$1"
  s="${s//$'\r'/}"
  if [[ "$s" == *['",\n']* ]]; then
    s="${s//\"/\"\"}"
    printf '"%s"' "$s"
  else
    printf '%s' "$s"
  fi
}

# Strip version operators/constraints from an rpm requires line, keeping only the capability name.
# Examples:
#   "config(bash) = 5.3.0-2.fc43"  -> "config(bash)"
#   "glibc(x86-64) >= 2.38"        -> "glibc(x86-64)"
#   "/bin/sh"                       -> "/bin/sh"
strip_req_version() {
  # Trim leading/trailing whitespace then cut at first version operator token.
  # Operators in rpm requires output are typically separated by spaces.
  sed -E 's/^[[:space:]]+|[[:space:]]+$//g; s/[[:space:]]+(>=|<=|=|<|>)[[:space:]].*$//'
}

# Package list (from KIWI XML; unique, including bootstrap)
pkgs=(
  azurelinux-repos
  basesystem
  bash
  bash-completion
  coreutils
  cpio
  filesystem
  findutils
  glibc
  glibc-langpack-en
  ncurses
  ncurses-base
  ncurses-libs
  pam
  readline
  sed
  shadow-utils
  shadow-utils-subid
  system-release
  systemd
  systemd-libs
  util-linux
  which
  audit
  audit-libs
  cyrus-sasl-lib
  gnutls
  gpgme
  libacl
  libattr
  libgcrypt
  libgpg-error
  libselinux
  openssh
  openssh-clients
  openssh-server
  openssl
  openssl-libs
  policycoreutils
  selinux-policy-targeted
  sudo
  WALinuxAgent
  azure-vm-utils
  cloud-init
  cloud-utils-growpart
  hyperv-daemons
  hyperv-daemons-license
  hypervfcopyd
  hypervkvpd
  hypervvssd
  dracut
  dracut-kiwi-oem-repart
  grub2-tools-minimal
  grubby
  kernel
  kernel-modules
  kmod
  grub2
  dnf
  dnf-data
  dnf-plugins-core
  libdnf
  rpm
  rpm-build-libs
  rpm-libs
  curl
  dhcpcd
  iproute
  iputils
  systemd-networkd
  iptables
  bzip2-libs
  gzip
  tar
  xz
  xz-libs
  zstd
  e2fsprogs
  e2fsprogs-libs
  lvm2
  parted
  xfsprogs
  cryptsetup
  dbus
  device-mapper
  device-mapper-event
  device-mapper-event-libs
  device-mapper-libs
  pciutils-libs
  systemd-udev
  python3
  python3-charset-normalizer
  python3-configobj
  python3-dbus
  python3-distro
  python3-dnf
  python3-hawkey
  python3-idna
  python3-jinja2
  python3-jsonpatch
  python3-jsonpointer
  python3-jsonschema
  python3-libcomps
  python3-libdnf
  python3-libs
  python3-markupsafe
  python3-oauthlib
  python3-requests
  python3-rpm
  python3-setuptools
  python3-six
  python3-urllib3
  libaio
  libarchive
  libassuan
  libbpf
  libcap
  libcap-ng
  libcomps
  libedit
  libevent
  libffi
  libgomp
  libidn2
  libksba
  libmnl
  libmodulemd
  libnftnl
  libnl3
  libpkgconf
  libpwquality
  librepo
  libseccomp
  libsemanage
  libsepol
  libsolv
  libstdc++
  libtasn1
  libunistring
  libxcrypt
  libxkbcommon
  libxml2
  libyaml
  diffutils
  libgcc
  gawk
  grep
  less
  nano
  chrony
  tzdata
  ca-certificates
  p11-kit
  p11-kit-trust
  logrotate
  procps-ng
  psmisc
  expat
  sqlite-libs
  man-db
  cracklib
  cracklib-dicts
  cryptsetup-libs
  elfutils-default-yama-scope
  elfutils-libelf
  file
  file-libs
  gdbm
  gmp
  gnupg2
  groff-base
  hostname
  json-c
  kbd
  lmdb-libs
  lua-libs
  mpfr
  nettle
  npth
  openldap
  pcre2
  pinentry
  pkgconf
  pkgconf-m4
  pkgconf-pkg-config
  popt
  rsync
  systemd-pam
  systemd-resolved
  tpm2-tss
  userspace-rcu
  xkeyboard-config
  zchunk-libs
  acl
  attr
  cyrus-sasl
  shim
  kernel-devel
  kernel-headers
  kernel-tools
  rpm-devel
  systemd-rpm-macros
  bind-libs
  bind-license
  bind-utils
  net-tools
  wget
  brotli
  bzip2
  lz4
  unzip
  zlib
  emacs-filesystem
  python3-pyyaml
  python3-asn1crypto
  python3-blinker
  python3-certifi
  python3-cffi
  python3-cryptography
  python3-gpg
  python3-jwt
  python3-netifaces
  python3-packaging
  python3-prettytable
  python3-pyOpenSSL
  python3-pyasn1
  python3-pycparser
  python3-pyparsing
  python3-wcwidth
  perl-Carp
  perl-Class-Struct
  perl-DynaLoader
  perl-Encode
  perl-Errno
  perl-Exporter
  perl-Fcntl
  perl-File-Basename
  perl-File-Path
  perl-File-Temp
  perl-Getopt-Long
  perl-Getopt-Std
  perl-HTTP-Tiny
  perl-IO
  perl-IPC-Open3
  perl-MIME-Base64
  perl-NDBM_File
  perl-POSIX
  perl-PathTools
  perl-Pod-Escapes
  perl-Pod-Perldoc
  perl-Pod-Simple
  perl-Pod-Usage
  perl-Scalar-List-Utils
  perl-SelectSaver
  perl-Socket
  perl-Storable
  perl-Symbol
  perl-Term-ANSIColor
  perl-Term-Cap
  perl-Text-ParseWords
  perl-Text-Tabs+Wrap
  perl-Time-Local
  perl-constant
  perl-if
  perl-interpreter
  perl-libs
  perl-locale
  perl-macros
  perl-mro
  perl-overload
  perl-overloading
  perl-parent
  perl-podlators
  perl-vars
  libcgroup
  libdb
  libestr
  libfastjson
  liblognorm
  librdkafka
  librelp
  libssh2
  libtraceevent
  libuv
  autogen-libopts
  libtool
  make
  vim
  rsyslog
  cronie
  cronie-anacron
  tini
  postgresql-libs
  bc
  chkconfig
  elfutils
  emacs
  libgc
  gdb
  gdbm-devel
  glib
  irqbalance
  iw
  ncurses-term
  newt
  nghttp2
  pcre2-tools
  popt-devel
  slang
  strace
  tmux
  wireless-regdb
  zchunk
  libzstd
  libcurl
  krb5-libs
  dracut-network
  grub2-efi-x64-modules
  grub2-efi-x64
)

: > "$out_csv"
printf "package,dependency\n" >> "$out_csv"

for pkg in "${pkgs[@]}"; do
  if ! rpm -q "$pkg" >/dev/null 2>&1; then
    printf "%s,%s\n" "$(csv_escape "$pkg")" "" >> "$out_csv"
    continue
  fi

  # Get requires lines, strip versions, then map to provider package names (if installed).
  mapfile -t deps < <(
    dnf repoquery --requires "$pkg" 2>/dev/null \
      | sed '/^$/d' \
      | grep -v '^rpmlib(' \
      | strip_req_version \
      | sed '/^$/d' \
      | sort -u \
      | while IFS= read -r cap; do
          # Try to find an installed provider for the unversioned capability
          prov_nevra="$(dnf repoquery --whatprovides "$cap" 2>/dev/null | head -n1 || true)"
          [[ -z "$prov_nevra" ]] && continue
          dnf repoquery --qf '%{NAME}\n' "$prov_nevra" 2>/dev/null || true
        done \
      | sed '/^$/d' \
      | sort -u \
      | grep -vxF "$pkg" || true
  )

  if [[ ${#deps[@]} -eq 0 ]]; then
    printf "%s,%s\n" "$(csv_escape "$pkg")" "" >> "$out_csv"
  else
    for dep in "${deps[@]}"; do
      printf "%s,%s\n" "$(csv_escape "$pkg")" "$(csv_escape "$dep")" >> "$out_csv"
    done
  fi
done

echo "Wrote: $out_csv" >&2