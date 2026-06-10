Summary:        Network daemon for managing OpenPGP and X.509 keyservers from GnuPG
Name:           dirmngr
Version:        2.4.9
Release:        3%{?dist}
License:        BSD and CC0 and GPLv2+ and LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Cryptography
URL:            https://gnupg.org/index.html
# This spec is built from the GnuPG source tarball but ships ONLY the dirmngr
# daemon and its helpers. The companion gnupg2 package owns everything else
# from the same tarball.
#
# Why a separate spec instead of a gnupg2 subpackage:
#   * dirmngr needs a TLS backend (gnutls) to talk to HKPS/HTTPS keyservers
#     and gpg silently drops dirmngr from the install set when one is not
#     present. Adding `BuildRequires: gnutls-devel` to gnupg2.spec is not an
#     option because gnupg2 is part of the bootstrap toolchain
#     (see toolkit/scripts/toolchain/build_official_toolchain_rpms.sh) and
#     pulling gnutls (plus nettle, gmp, p11-kit, ...) into bootstrap would
#     cascade into a full toolchain regeneration on x86_64 and aarch64.
#   * Building dirmngr out-of-toolchain in its own spec keeps the bootstrap
#     untouched while restoring `gpg --recv-keys` from HKPS keyservers.
#
# Version and Release are kept in lockstep with gnupg2 via
# toolkit/scripts/check_entangled_specs.py; bump them together when gnupg2
# changes.
#
# NOTE: gnupg2.spec must NOT start linking against gnutls while this spec
# exists, or both packages will try to own /usr/bin/dirmngr and conflict.
# If that ever changes, retire this spec instead of keeping both.
Source0:        https://gnupg.org/ftp/gcrypt/gnupg/gnupg-%{version}.tar.bz2
Patch0:         CVE-2026-24882.patch
Patch1:         CVE-2026-57062.patch

BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
BuildRequires:  npth-devel >= 1.2
BuildRequires:  libassuan-devel >= 2.5.0
BuildRequires:  libksba-devel >= 1.3.4
BuildRequires:  libgcrypt-devel > 1.9.1
BuildRequires:  libgpg-error-devel >= 1.48
# TLS backend that lets dirmngr talk to HKPS/HTTPS keyservers. Without one,
# gnupg's configure silently disables dirmngr.
BuildRequires:  gnutls-devel
# HKP/HTTP keyserver transport via libcurl.
BuildRequires:  curl-devel
# LDAP keyserver helper (/usr/libexec/dirmngr_ldap).
BuildRequires:  openldap-devel

Requires:       gnupg2 = %{version}-%{release}
Requires:       libksba > 1.3.4
Requires:       libgcrypt >= 1.9.1
Requires:       libgpg-error >= 1.48
Requires:       npth >= 1.2
Requires:       libassuan >= 2.5.0

Provides:       gnupg2-dirmngr = %{version}-%{release}

%description
GnuPG's dirmngr daemon takes care of accessing OpenPGP keyservers (HKP, HKPS),
X.509 CRL/OCSP responders, and LDAP directories on behalf of gpg and gpgsm.
It is required by `gpg --keyserver ... --recv-keys` and other keyserver
operations.

This package is built from the same GnuPG source tarball as the `gnupg2`
package but ships only the dirmngr binary, the dirmngr-client utility, the
dirmngr_ldap LDAP helper and their manual pages. Its Version and Release are
kept in lockstep with `gnupg2`.

%prep
%autosetup -p1 -n gnupg-%{version}
# The CVE-2026-24882 patch carried by SPECS/gnupg2/gnupg2.spec only touches
# tpm2d/tpm2.c, which is unrelated to dirmngr and not shipped by this spec,
# so it is intentionally not applied here.

%build
# Keep configure flags aligned with SPECS/gnupg2/gnupg2.spec so the produced
# dirmngr matches the gnupg2 build it co-installs with. --enable-gpg-is-gpg2
# and --disable-keyboxd are inherited from that spec for the same reasons.
%configure \
  --enable-gpg-is-gpg2 \
  --disable-keyboxd
%make_build

%install
ln -sf gpg2.1 doc/gpg.1
ln -sf gpgv2.1 doc/gpgv.1

%make_install

# This spec is scoped to dirmngr only. Prune every file produced by the
# upstream build that is already owned by the gnupg2 package, using a
# whitelist of dirmngr-related names so the prune is resilient to upstream
# adding or removing unrelated helpers in the future.
find %{buildroot}%{_bindir} -mindepth 1 -maxdepth 1 \
    ! -name 'dirmngr' ! -name 'dirmngr-client' -delete
[ -d %{buildroot}%{_sbindir} ] && find %{buildroot}%{_sbindir} -mindepth 1 -delete
find %{buildroot}%{_libexecdir} -mindepth 1 -maxdepth 1 \
    ! -name 'dirmngr*' -delete
rm -rf %{buildroot}%{_datadir}/gnupg
rm -rf %{buildroot}%{_docdir}/gnupg
rm -rf %{buildroot}%{_datadir}/locale
rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_sysconfdir}/gnupg
find %{buildroot}%{_mandir}/man1 -mindepth 1 ! -name 'dirmngr*' -delete
[ -d %{buildroot}%{_mandir}/man7 ] && find %{buildroot}%{_mandir}/man7 -mindepth 1 -delete
find %{buildroot}%{_mandir}/man8 -mindepth 1 ! -name 'dirmngr*' -delete

%files
%defattr(-,root,root)
%license COPYING COPYING.CC0 COPYING.GPL2 COPYING.LGPL3 COPYING.LGPL21 COPYING.other
%{_bindir}/dirmngr
%{_bindir}/dirmngr-client
%{_libexecdir}/dirmngr_ldap
%{_mandir}/man8/dirmngr.*
%{_mandir}/man1/dirmngr-client.*

%changelog
* Wed Jun 10 2026 Muhammad Falak <mwani@microsoft.com> - 2.4.9-3
- Initial Azure Linux 3.0 packaging of dirmngr as a standalone spec sharing
  the gnupg source tree, restoring HTTPS keyserver functionality lost when
  gnutls was dropped from the toolchain. Version and Release are entangled
  with gnupg2 via check_entangled_specs.py, so the first release is 2 to
  match the current gnupg2 Release.
- Fixes ADO 62225284 / GH#3142.
