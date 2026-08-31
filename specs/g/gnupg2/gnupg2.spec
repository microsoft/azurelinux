# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

%global split_min_version 2.4.9-4.fc42.1

Summary: Utility for secure communication and data storage
Name:    gnupg2
Version: 2.4.9
Release: 5%{?dist}

License: CC0-1.0 AND GPL-2.0-or-later AND GPL-3.0-or-later AND LGPL-2.1-or-later AND LGPL-3.0-or-later AND (BSD-3-Clause OR LGPL-3.0-or-later OR GPL-2.0-or-later) AND CC-BY-4.0 AND MIT
Source0: https://gnupg.org/ftp/gcrypt/%{?pre:alpha/}gnupg/gnupg-%{version}%{?pre}.tar.bz2
Source1: https://gnupg.org/ftp/gcrypt/%{?pre:alpha/}gnupg/gnupg-%{version}%{?pre}.tar.bz2.sig
Source2: https://gnupg.org/signature_key.asc
# initialize small amount of secmem for list of algorithms in help
# (#598847) (necessary in the FIPS mode of libgcrypt)
Patch1:  gnupg-2.4.7-secmem.patch
# non-upstreamable patch adding file-is-digest option needed for Copr
# https://dev.gnupg.org/T1646
Patch2:  gnupg-2.4.7-file-is-digest.patch
# Disable brainpool tests as they are not built into our libgcrypt
# Disable MD160 in FIPS mode (#879047)
Patch3:  gnupg-2.4.7-fips-algo.patch
# CVE-2026-24882: Stack-based buffer overflow in tpm2daemon allows arbitrary code execution
# https://dev.gnupg.org/T8045
Patch4:  gnupg-2.4.9-tpm2daemon.patch

# Patches from FreePG:
# https://gitlab.com/freepg/gnupg/-/tree/main/STABLE-BRANCH-2-4-freepg
Patch20: 0002-gpg-accept-subkeys-with-a-good-revocation-but-no-sel.patch
Patch21: 0003-gpg-allow-import-of-previously-known-keys-even-witho.patch
Patch22: 0004-tests-add-test-cases-for-import-without-uid.patch
Patch23: 0005-gpg-drop-import-clean-from-default-keyserver-import-.patch
Patch24: 0006-Do-not-use-OCB-mode-even-if-AEAD-OCB-key-preference-.patch
Patch25: 0007-Revert-the-introduction-of-the-RFC4880bis-draft-into.patch
Patch26: 0008-avoid-systemd-deprecation-warning.patch
Patch27: 0009-Add-systemd-support-for-keyboxd.patch
Patch28: 0010-Ship-sample-systemd-unit-files.patch
Patch29: 0011-el-gamal-default-to-3072-bits.patch
Patch30: 0012-gpg-default-digest-algorithm-SHA512.patch
Patch31: 0013-gpg-Prefer-SHA-512-and-SHA-384-in-personal-digest.patch
Patch32: 0018-Avoid-simple-memory-dumps-via-ptrace.patch
Patch34: 0029-Add-keyboxd-systemd-support.patch
Patch35: 0033-Support-large-RSA-keygen-in-non-batch-mode.patch

# Fixes for issues found in Coverity scan - reported upstream
Patch40: gnupg-2.4.7-coverity.patch

# add a root certificate bundle due to changes in ca-certificates (#2380121)
Patch45: gnupg-2.4.8-ca-certificates-bundle.patch

URL:     https://www.gnupg.org/

BuildRequires: gcc
BuildRequires: bzip2-devel
BuildRequires: curl-devel
BuildRequires: docbook-utils
BuildRequires: gettext
%if %{without bootstrap}
# Require gnupg2 to verify sources, unless bootstrapping
BuildRequires: gnupg2
%endif
BuildRequires: libassuan-devel >= 2.5.0
BuildRequires: libgcrypt-devel >= 1.9.1
BuildRequires: libgpg-error-devel >= 1.46
BuildRequires: libksba-devel >= 1.6.3
BuildRequires: openldap-devel
BuildRequires: pcsc-lite-libs
BuildRequires: ncurses-devel
BuildRequires: npth-devel
BuildRequires: readline-devel
BuildRequires: zlib-devel
BuildRequires: gnutls-devel
BuildRequires: sqlite-devel
BuildRequires: fuse
BuildRequires: make
BuildRequires: systemd-rpm-macros
BuildRequires: texinfo
BuildRequires: tpm2-tss-devel
# for tests
BuildRequires: openssh-clients
BuildRequires: swtpm

Requires: libgcrypt >= 1.9.1
Requires: libgpg-error >= 1.46

Requires: gnupg2-dirmngr%{?_isa} = %{version}-%{release}
Requires: gnupg2-gpgconf%{?_isa} = %{version}-%{release}
Requires: gnupg2-gpg-agent%{?_isa} = %{version}-%{release}
Requires: gnupg2-keyboxd%{?_isa} = %{version}-%{release}
Requires: gnupg2-verify%{?_isa} = %{version}-%{release}

Recommends: pinentry

# pgp-tools, perl-GnuPG-Interface requires 'gpg' (not sure why) -- Rex
Provides: gpg = %{version}-%{release}
# Obsolete GnuPG-1 package
Provides: gnupg = %{version}-%{release}
Obsoletes: gnupg < 1.4.24

# ensures upgrade path for existing installs
Obsoletes: gnupg2 < %{split_min_version}

Provides: dirmngr = %{version}-%{release}
Obsoletes: dirmngr < 1.2.0-1

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
GnuPG is GNU's tool for secure communication and data storage.  It can
be used to encrypt data and to create digital signatures.  It includes
an advanced key management facility and is compliant with the proposed
OpenPGP Internet standard as described in RFC2440 and the S/MIME
standard as described by several RFCs.

GnuPG 2.0 is a newer version of GnuPG with additional support for
S/MIME.  It has a different design philosophy that splits
functionality up into several modules. The S/MIME and smartcard functionality
is provided by the gnupg2-smime package.

%package dirmngr
Summary: GnuPG network certificate management service
Requires: gnupg2-gpgconf%{?_isa} = %{version}-%{release}
Conflicts: gnupg2 < %{split_min_version}

%description dirmngr
GnuPG is GNU's tool for secure communication and data storage. This
package contains the network certificate management service.

%package g13
Summary: GnuPG tool for managing encrypted file system containers
Requires: gnupg2%{?_isa} = %{version}-%{release}
Conflicts: gnupg2 < %{split_min_version}
Obsoletes: gnupg2 < %{split_min_version}

%description g13
GnuPG is GNU's tool for secure communication and data storage. This
package contains the g13 tool managing encrypted file system containers.

%package gpgconf
Summary: GnuPG core configuration utilities
Conflicts: gnupg2 < %{split_min_version}

%description gpgconf
GnuPG is GNU's tool for secure communication and data storage. This
package contains the core configuration utilities.

%package gpg-agent
Summary: GnuPG cryptographic agent
Requires: gnupg2-gpgconf%{?_isa} = %{version}-%{release}
Conflicts: gnupg2 < %{split_min_version}

%description gpg-agent
GnuPG is GNU's tool for secure communication and data storage. This
package contains the cryptographic agent.

%package keyboxd
Summary: GnuPG public key material service
Conflicts: gnupg2 < %{split_min_version}

%description keyboxd
GnuPG is GNU's tool for secure communication and data storage. This
package contains the public key material service.

%package scdaemon
Summary: GnuPG SmartCard daemon
Requires: gnupg2%{?_isa} = %{version}-%{release}
Conflicts: gnupg2 < %{split_min_version}
Obsoletes: gnupg2 < %{split_min_version}
# for USB smart card support
Recommends: pcsc-lite-ccid

%description scdaemon
GnuPG is GNU's tool for secure communication and data storage. This
package contains the SmartCard daemon.

%package smime
Summary: CMS encryption and signing tool and smart card support for GnuPG
Requires: gnupg2%{?_isa} = %{version}-%{release}

%description smime
GnuPG is GNU's tool for secure communication and data storage. This
package adds support for smart cards and S/MIME encryption and signing
to the base GnuPG package.

%package utils
Summary: GnuPG utilities
Requires: gnupg2%{?_isa} = %{version}-%{release}
Conflicts: gnupg2 < %{split_min_version}
Obsoletes: gnupg2 < %{split_min_version}

%description utils
GnuPG is GNU's tool for secure communication and data storage. This
package includes additional utilities.

%package verify
Summary: GnuPG signature verification tool
Conflicts: gnupg2 < %{split_min_version}

%description verify
GnuPG is GNU's tool for secure communication and data storage. This
package contains the signature verification tool.

%package wks
Summary: GnuPG Web Key Service client and server
Requires: gnupg2%{?_isa} = %{version}-%{release}
Conflicts: gnupg2 < %{split_min_version}
Obsoletes: gnupg2 < %{split_min_version}

%description wks
GnuPG is GNU's tool for secure communication and data storage. This
package contains the GnuPG Web Key Service client and server.


%prep
%if ! %{with bootstrap}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%endif
%setup -q -n gnupg-%{version}

%patch 1 -p1 -b .secmem
%patch 2 -p1 -b .file-is-digest
%patch 3 -p1 -b .fips
%patch 4 -p1 -b .tpm2d

%patch 20 -p1 -b .good_revoc
%patch 21 -p1 -b .prev_known_key
%patch 22 -p1 -b .test_missing_uid
%patch 23 -p1 -b .import-clean
%patch 24 -p1 -b .do-not-use-OCB
%patch 25 -p1 -b .revert-rfc4880bis
%patch 26 -p1 -b .systemd-deprecation
%patch 27 -p1 -b .systemd-keybox
%patch 28 -p1 -b .systemd-units
%patch 29 -p1 -b .elgamal-3k
%patch 30 -p1 -b .default-sha512
%patch 31 -p1 -b .prefer-sha512
%patch 32 -p1 -b .dump-ptrace
%patch 34 -p1 -b .keyboxd-units
%patch 35 -p1 -b .large-rsa

%patch 40 -p1 -b .coverity

# pcsc-lite library major: 0 in 1.2.0, 1 in 1.2.9+ (dlopen()'d in pcsc-wrapper)
# Note: this is just the name of the default shared lib to load in scdaemon,
# it can use other implementations too (including non-pcsc ones).
%global pcsclib %(basename $(ls -1 %{_libdir}/libpcsclite.so.? 2>/dev/null ) 2>/dev/null )

sed -i -e 's/"libpcsclite\.so"/"%{pcsclib}"/' scd/scdaemon.c


%build
%configure \
  --disable-rpath \
  --enable-g13 \
  --disable-ccid-driver \
  --with-tss=intel \
  --enable-large-secmem

# need scratch gpg database for tests
mkdir -p $HOME/.gnupg

%make_build


%install
%make_install \
  docdir=%{_pkgdocdir}

%find_lang %{name}

# gpgconf.conf
mkdir -p %{buildroot}%{_sysconfdir}/gnupg
touch %{buildroot}%{_sysconfdir}/gnupg/gpgconf.conf
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
echo "export GPG_TTY=\$(tty)" > %{buildroot}%{_sysconfdir}/profile.d/gnupg2.sh
echo "setenv GPG_TTY \`tty\`" > %{buildroot}%{_sysconfdir}/profile.d/gnupg2.csh

# more docs
install -m644 -p AUTHORS NEWS THANKS TODO \
  %{buildroot}%{_pkgdocdir}

# compat symlinks
ln -sf gpg %{buildroot}%{_bindir}/gpg2
ln -sf gpgv %{buildroot}%{_bindir}/gpgv2
ln -sf gpg.1 %{buildroot}%{_mandir}/man1/gpg2.1
ln -sf gpgv.1 %{buildroot}%{_mandir}/man1/gpgv2.1
ln -sf gnupg.7 %{buildroot}%{_mandir}/man7/gnupg2.7

# info dir
rm -f %{buildroot}%{_infodir}/dir

# drop the gpg scheme interpreter
rm -f %{buildroot}%{_bindir}/gpgscm

# Move the systemd user units to appropriate directory
install -d -m755 %{buildroot}%{_userunitdir}
install -p doc/examples/systemd-user/*.socket %{buildroot}%{_userunitdir}
install -p doc/examples/systemd-user/*.service %{buildroot}%{_userunitdir}

%check
# need scratch gpg database for tests
mkdir -p $HOME/.gnupg
make -k check


%post dirmngr
%systemd_user_post dirmngr.service

%preun dirmngr
%systemd_user_preun dirmngr.service

%postun dirmngr
%systemd_user_postun_with_restart dirmngr.service

%post gpg-agent
%systemd_user_post gpg-agent.service

%preun gpg-agent
%systemd_user_preun gpg-agent.service

%postun gpg-agent
%systemd_user_postun_with_restart gpg-agent.service

%post keyboxd
%systemd_user_post keyboxd.service

%preun keyboxd
%systemd_user_preun keyboxd.service

%postun keyboxd
%systemd_user_postun_with_restart keyboxd.service


%files -f %{name}.lang
%license COPYING
%{_sysconfdir}/profile.d/gnupg2.sh
%{_sysconfdir}/profile.d/gnupg2.csh
## docs say to install suid root, but fedora/rh security folk say not to
%{_bindir}/gpg
%{_bindir}/gpg2
%{_infodir}/gnupg.info*
%{_mandir}/man?/gpg.*
%{_mandir}/man?/gpg2.*
%{_mandir}/man?/gnupg.*
%{_mandir}/man?/gnupg2.*
%{_pkgdocdir}/
%{_datadir}/gnupg/help*.txt

%files dirmngr
%license COPYING
%{_bindir}/dirmngr
%{_bindir}/dirmngr-client
%{_libexecdir}/dirmngr_ldap
%{_userunitdir}/dirmngr.*
%{_mandir}/man?/dirmngr.*
%{_mandir}/man?/dirmngr-client.*
%dir %{_datadir}/gnupg/
%{_datadir}/gnupg/sks-keyservers.netCA.pem

%files g13
%{_bindir}/g13
%{_sbindir}/g13-syshelp

%files gpgconf
%license COPYING
%dir %{_sysconfdir}/gnupg
%ghost %config(noreplace) %{_sysconfdir}/gnupg/gpgconf.conf
%{_bindir}/gpgconf
%{_bindir}/gpg-connect-agent
%{_mandir}/man?/gpgconf*
%{_mandir}/man?/gpg-connect-agent.*
%dir %{_datadir}/gnupg
%{_datadir}/gnupg/distsigkey.gpg

%files gpg-agent
%license COPYING
%{_bindir}/gpg-agent
%{_libexecdir}/gpg-check-pattern
%{_libexecdir}/gpg-preset-passphrase
%{_libexecdir}/gpg-protect-tool
%{_libexecdir}/tpm2daemon
%{_userunitdir}/gpg-agent.*
%{_userunitdir}/gpg-agent-*.socket
%{_mandir}/man?/gpg-agent.*
%{_mandir}/man?/gpg-check-pattern.*
%{_mandir}/man?/gpg-preset-passphrase.*

%files keyboxd
%license COPYING
%{_libexecdir}/keyboxd
%{_userunitdir}/keyboxd.*

%files scdaemon
%{_bindir}/gpg-card
%{_libexecdir}/gpg-auth
%{_libexecdir}/scdaemon
%{_mandir}/man?/gpg-card.*
%{_mandir}/man?/scdaemon.*

%files smime
%{_bindir}/gpgsm
%{_mandir}/man?/gpgsm.*

%files utils
%{_bindir}/gpg-mail-tube
%{_bindir}/gpgparsemail
%{_bindir}/gpgsplit
%{_bindir}/gpgtar
%{_bindir}/kbxutil
%{_bindir}/watchgnupg
%{_sbindir}/addgnupghome
%{_sbindir}/applygnupgdefaults
%{_libexecdir}/gpg-pair-tool
%{_mandir}/man?/addgnupghome.*
%{_mandir}/man?/applygnupgdefaults.*
%{_mandir}/man?/gpg-mail-tube.*
%{_mandir}/man?/gpgparsemail.*
%{_mandir}/man?/gpgtar.*
%{_mandir}/man?/watchgnupg.*

%files verify
%license COPYING
%{_bindir}/gpgv
%{_bindir}/gpgv2
%{_mandir}/man?/gpgv.*
%{_mandir}/man?/gpgv2.*

%files wks
%{_bindir}/gpg-wks-client
%{_bindir}/gpg-wks-server
%{_libexecdir}/gpg-wks-client
%{_mandir}/man?/gpg-wks-client.*
%{_mandir}/man?/gpg-wks-server.*


%changelog
* Wed Jan 28 2026 Jakub Jelen <jjelen@redhat.com> - 2.4.9-5
- Fix CVE-2026-24882: Stack-based buffer overflow in tpm2daemon allows arbitrary code execution

* Wed Jan 21 2026 Jakub Jelen <jjelen@redhat.com> - 2.4.9-4
- Unbreak Release tag to make rpminspect in gating tests happy

* Wed Jan 21 2026 Jakub Jelen <jjelen@redhat.com> - 2.4.9-3
- Update split_min_version to provide clean update path from Fedora 42 (#2429875)

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jan 01 2026 Clemens Lang <cllang@redhat.com> - 2.4.9-1
- New upstream release 2.4.9
- Fixes CVE-2025-68973 (https://gpg.fail/memcpy)
- Fixes https://gpg.fail/sha1
- Fixes https://gpg.fail/detached

* Fri Jul 25 2025 Frantisek Krenzelok <fkrenzel@redhat.com> - 2.4.8-4
- add a root certificate bundle due to changes in ca-certificates (#2380121)
- https://fedoraproject.org/wiki/Changes/dropingOfCertPemFile

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed May 21 2025 Fabio Valentini <decathorpe@gmail.com> - 2.4.8-2
- Split tools from monolithic gnupg2 package into subpackages

* Fri May 16 2025 Jakub Jelen <jjelen@redhat.com> - 2.4.8-1
- New upstream release 2.4.8
- Remove problematic patch breaking Poppler

* Wed Mar 26 2025 Jakub Jelen <jjelen@redhat.com> - 2.4.7-3
- Pull more patches from FreePG project

* Thu Jan 23 2025 Jakub Jelen <jjelen@redhat.com> - 2.4.7-2
- Regenerate patches and pull new from FreePG project

* Wed Jan 22 2025 Jakub Jelen <jjelen@redhat.com> - 2.4.7-1
- New upstream release

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.5-5
- Rebuilt for the bin-sbin merge (2nd attempt)

* Wed Nov 13 2024 Michael J Gruber <mjg@fedoraproject.org> - 2.4.5-4
- rebuild against npth-1.8

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.5-2
- Rebuilt for the bin-sbin merge

* Fri Mar 08 2024 Jakub Jelen <jjelen@redhat.com> - 2.4.5-1
- New upstream release (#2268461)

* Wed Feb 28 2024 Jakub Jelen <jjelen@redhat.com> - 2.4.4-1
- Set GPG_TTY in profile.d (#2264985)

* Fri Jan 26 2024 Jakub Jelen <jjelen@redhat.com> - 2.4.4-1
- New upstream release (#2260333)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 10 2023 Jakub Jelen <jjelen@redhat.com> - 2.4.3-4
- Avoid creation of development versions (#2249037)

* Mon Nov 06 2023 Jakub Jelen <jjelen@redhat.com> - 2.4.3-3
- Restore systemd units and sockets (#2158627)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Jakub Jelen <jjelen@redhat.com> - 2.4.3-1
- New upstream release (#2193503)

* Thu Jun 01 2023 Michael J Gruber <mjg@fedoraproject.org> - 2.4.2-2
- fix emacs usage (rhbz#2212090)

* Wed May 31 2023 Jakub Jelen <jjelen@redhat.com> - 2.4.2-1
- New upstream release
- Build with TPM2 support

* Fri Apr 28 2023 Todd Zullinger <tmz@pobox.com> - 2.4.1-1
- update to 2.4.1 (#2193503)

* Fri Apr 28 2023 Todd Zullinger <tmz@pobox.com> - 2.4.0-4
- remove %%skip_verify, brainpool signatures are supported now

* Fri Mar 03 2023 Jakub Jelen <jjelen@redhat.com> - 2.4.0-3
- Revert introduction of the RFC4880bis draft into defaults

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Todd Zullinger <tmz@pobox.com> - 2.4.0-1
- update to 2.4.0 (#2155170)

* Mon Oct 17 2022 Todd Zullinger <tmz@pobox.com> - 2.3.8-1
- update to 2.3.8
- BR systemd-rpm-macros for %%{_userunitdir}

* Mon Oct 17 2022 Todd Zullinger <tmz@pobox.com> - 2.3.7-5
- verify upstream signatures in %%prep, unless bootstrapping

* Wed Oct 05 2022 Todd Zullinger <tmz@pobox.com> - 2.3.7-4
- update BR/R versions for libassuan, libgpg-error, and libksba
- drop with/without unversioned_gpg, last used with fedora-29

* Mon Aug 01 2022 Jakub Jelen <jjelen@redhat.com> - 2.3.7-3
- Fix yubikey 5 detection (#2107766)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Jakub Jelen <jjelen@redhat.com> - 2.3.7-1
- New upstream release (#2106045)

* Mon Jul 04 2022 Jakub Jelen <jjelen@redhat.com> - 2.3.6-2
- Fix for CVE-2022-34903 (#2103242)
- Fix focing AEAD through configuration files (#2093760)

* Mon Apr 25 2022 Jakub Jelen <jjelen@redhat.com> - 2.3.6-1
- New upstream release (#2078550)

* Mon Apr 25 2022 Jakub Jelen <jjelen@redhat.com> - 2.3.5-1
- New upstream release (#2077616)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 Jakub Jelen <jjelen@redhat.com> - 2.3.4-1
- New upstream release (#2034437)

* Mon Nov 15 2021 Jakub Jelen <jjelen@redhat.com> - 2.3.3-2
- Fix file-is-digest patch (#2022904)

* Wed Oct 13 2021 Jakub Jelen <jjelen@redhat.com> - 2.3.3-1
- New upstream release (2013388)

* Wed Oct 06 2021 Jakub Jelen <jjelen@redhat.com> - 2.3.2-3
- Fix crash in agent when deciphering (#2009978)
- Recommend pcsc-lite-ccid to support USB smart cards (#2007923)

* Mon Sep 20 2021 Jakub Jelen <jjelen@redhat.com> - 2.3.2-2
- Disable ccid driver to avoid clash with pcscd (#2005714)

* Wed Aug 25 2021 Jakub Jelen <jjelen@redhat.com> - 2.3.2-1
- New upstream relase (#1997276)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Apr 21 2021 Jakub Jelen <jjelen@redhat.com> - 2.3.1-1
- New upstream release (#1947159)

* Mon Mar 29 2021 Jakub Jelen <jjelen@redhat.com> - 2.2.27-4
- Add a configuration to not require exclusive access to PCSC

* Thu Feb 18 2021 Jakub Jelen <jjelen@redhat.com> - 2.2.27-3
- Bump required libgpg-error version (#1930110)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Jakub Jelen <jjelen@redhat.com> - 2.2.27-1
- New upstream release (#1909825)

* Mon Jan 04 2021 Jakub Jelen <jjelen@redhat.com> - 2.2.26-1
- New upstream release (#1909825)

* Tue Nov 24 2020 Jakub Jelen <jjelen@redhat.com> - 2.2.25-2
- Enable gpgtar (#1901103)

* Tue Nov 24 2020 Jakub Jelen <jjelen@redhat.com> - 2.2.25-1
- Update to 2.2.25 (#1900815)

* Thu Nov 19 2020 Jakub Jelen <jjelen@redhat.com> - 2.2.24-1
- Update to 2.2.24 (#1898504)

* Fri Sep  4 2020 Tomáš Mráz <tmraz@redhat.com> - 2.2.23-1
- upgrade to 2.2.23

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.21-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Tom Stellard <tstellar@redhat.com> - 2.2.21-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Jul 20 2020 Tomáš Mráz <tmraz@redhat.com> - 2.2.21-1
- upgrade to 2.2.21

* Mon May  4 2020 Tomáš Mráz <tmraz@redhat.com> - 2.2.20-3
- fixes for issues found in Coverity scan

* Thu Apr 30 2020 Tomáš Mráz <tmraz@redhat.com> - 2.2.20-2
- move systemd user units to _userunitdir (no activation by default)

* Tue Apr 14 2020 Tomáš Mráz <tmraz@redhat.com> - 2.2.20-1
- upgrade to 2.2.20

* Wed Jan 29 2020 Tomáš Mráz <tmraz@redhat.com> - 2.2.19-1
- upgrade to 2.2.19

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan  4 2020 Marcel Härry <mh+fedora@scrit.ch> - 2.2.18-3
- Add patches to be able to deal with keys without uids (#1787708)

* Fri Dec  6 2019 Tomáš Mráz <tmraz@redhat.com> - 2.2.18-2
- fix abort when decrypting data with anonymous recipient (#1780057)

* Tue Dec  3 2019 Tomáš Mráz <tmraz@redhat.com> - 2.2.18-1
- upgrade to 2.2.18

* Wed Nov  6 2019 Tomáš Mráz <tmraz@redhat.com> - 2.2.17-3
- fix the gnupg(7) manual page (#1769072)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Tomáš Mráz <tmraz@redhat.com> - 2.2.17-1
- upgrade to 2.2.17

* Mon Jul  1 2019 Tomáš Mráz <tmraz@redhat.com> - 2.2.16-1
- upgrade to 2.2.16

* Tue Feb 26 2019 Tomáš Mráz <tmraz@redhat.com> - 2.2.13-1
- upgrade to 2.2.13

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.2.12-3
- Rebuild for readline 8.0

* Mon Feb  4 2019 Tomáš Mráz <tmraz@redhat.com> - 2.2.12-2
- make it build with gcc-9

* Tue Jan  8 2019 Tomáš Mráz <tmraz@redhat.com> - 2.2.12-1
- upgrade to 2.2.12

* Sat Dec 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.2.11-2
- Provide unversioned GPG on F30+

* Fri Nov 30 2018 Tomáš Mráz <tmraz@redhat.com> - 2.2.11-1
- upgrade to 2.2.11

* Wed Aug  1 2018 Tomáš Mráz <tmraz@redhat.com> - 2.2.9-1
- upgrade to 2.2.9

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 11 2018 Tomáš Mráz <tmraz@redhat.com> - 2.2.8-1
- upgrade to 2.2.8 fixing CVE 2018-12020

* Wed Apr 11 2018 Tomáš Mráz <tmraz@redhat.com> - 2.2.6-1
- upgrade to 2.2.6

* Fri Mar  2 2018 Tomáš Mráz <tmraz@redhat.com> - 2.2.5-1
- upgrade to 2.2.5

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Tomáš Mráz <tmraz@redhat.com> - 2.2.4-1
- upgrade to 2.2.4

* Tue Nov 21 2017 Tomáš Mráz <tmraz@redhat.com> - 2.2.3-1
- upgrade to 2.2.3

* Wed Nov  8 2017 Tomáš Mráz <tmraz@redhat.com> - 2.2.2-1
- upgrade to 2.2.2

* Tue Oct  3 2017 Tomáš Mráz <tmraz@redhat.com> - 2.2.1-1
- upgrade to 2.2.1

* Tue Sep  5 2017 Tomáš Mráz <tmraz@redhat.com> - 2.2.0-1
- upgrade to 2.2.0

* Wed Aug  9 2017 Tomáš Mráz <tmraz@redhat.com> - 2.1.22-1
- upgrade to 2.1.22

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Fri Jul 28 2017 Tomáš Mráz <tmraz@redhat.com> - 2.1.21-4
- explictly remove gpgscm from the buildroot

* Tue Jul 18 2017 Tomáš Mráz <tmraz@redhat.com> - 2.1.21-3
- rebase the insttools patch
- enable large secure memory support

* Tue May 16 2017 Tomáš Mráz <tmraz@redhat.com> - 2.1.21-2
- scdaemon is now needed by gpg

* Tue May 16 2017 Tomáš Mráz <tmraz@redhat.com> - 2.1.21-1
- upgrade to 2.1.21

* Tue Apr 25 2017 Tomáš Mráz <tmraz@redhat.com> - 2.1.20-2
- libdns aliasing issues fixed

* Mon Apr 24 2017 Tomáš Mráz <tmraz@redhat.com> - 2.1.20-1
- upgrade to 2.1.20
- disable bundled libdns for now (#1444352)

* Fri Mar 24 2017 Tomáš Mráz <tmraz@redhat.com> - 2.1.19-1
- upgrade to 2.1.19
- shorten time waiting on gpg-agent/dirmngr to start by exponential
  backoff (#1431749)

* Wed Mar  1 2017 Tomáš Mráz <tmraz@redhat.com> - 2.1.18-2
- upgrade to 2.1.18

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.1.17-2
- Rebuild for readline 7.x

* Thu Dec 22 2016 Tomáš Mráz <tmraz@redhat.com> - 2.1.17-1
- upgrade to 2.1.17

* Mon Nov 28 2016 Tomáš Mráz <tmraz@redhat.com> - 2.1.16-1
- upgrade to 2.1.16

* Mon Aug 22 2016 Tomáš Mráz <tmraz@redhat.com> - 2.1.13-2
- avoid using libgcrypt without initialization (#1366909)

* Tue Jul 12 2016 Tomáš Mráz <tmraz@redhat.com> - 2.1.13-1
- upgrade to 2.1.13

* Thu May  5 2016 Tomáš Mráz <tmraz@redhat.com> - 2.1.12-1
- upgrade to 2.1.12

* Tue Apr 12 2016 Tomáš Mráz <tmraz@redhat.com> - 2.1.11-4
- make the pinentry dependency weak as for the public-key operations it
  is not needed (#1324595)

* Mon Mar  7 2016 Tomáš Mráz <tmraz@redhat.com> - 2.1.11-3
- add recommends weak dependency for gnupg2-smime

* Sat Mar  5 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.11-2
- Don't ship ChangeLog, core details already covered in NEWS

* Tue Feb 16 2016 Tomáš Mráz <tmraz@redhat.com> - 2.1.11-1
- upgrade to 2.1.11

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Dan Horák <dan[at]danny.cz> - 2.1.10-3
- fix the insttools patch

* Wed Jan 13 2016 Tomáš Mráz <tmraz@redhat.com> - 2.1.10-2
- rebase the insttools patch needed for full gpgv1 replacement

* Mon Dec  7 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.10-1
- upgrade to 2.1.10

* Mon Oct 12 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.9-1
- upgrade to 2.1.9

* Fri Sep 11 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.8-1
- upgrade to 2.1.8

* Thu Aug 13 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.7-1
- upgrade to 2.1.7

* Tue Aug 11 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.6-1
- upgrade to 2.1.6

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.5-1
- upgrade to 2.1.5

* Tue May 26 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.4-2
- use gnutls for TLS support in dirmngr (#1224816)

* Fri May 15 2015 Robert Scheck <robert@fedoraproject.org> - 2.1.4-1
- upgrade to 2.1.4 (#1192353)

* Thu Apr 16 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.3-1
- new upstream release fixing minor bugs

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.1.2-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 18 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.2-1
- new upstream release fixing two minor security issues

* Fri Jan 30 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.1-2
- resolve conflict with gnupg by renaming conflicting manual page (#1187472)

* Thu Jan 29 2015 Tomáš Mráz <tmraz@redhat.com> - 2.1.1-1
- new upstream release
- this release now includes the dirmngr which is obsoleted as separate package

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug  5 2014 Tomáš Mráz <tmraz@redhat.com> - 2.0.25-1
- new upstream release fixing a minor regression introduced by the previous one
- add --file-is-digest option needed for copr

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.24-2
- fix license handling

* Wed Jun 25 2014 Tomáš Mráz <tmraz@redhat.com> - 2.0.24-1
- new upstream release fixing CVE-2014-4617

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May  7 2014 Tomáš Mráz <tmraz@redhat.com> - 2.0.22-3
- do not dump core if hash algorithm not available in the FIPS mode

* Tue Mar  4 2014 Tomáš Mráz <tmraz@redhat.com> - 2.0.22-2
- rebuilt against new libgcrypt

* Tue Oct  8 2013 Tomáš Mráz <tmraz@redhat.com> - 2.0.22-1
- new upstream release fixing CVE-2013-4402

* Fri Aug 23 2013 Tomáš Mráz <tmraz@redhat.com> - 2.0.21-1
- new upstream release

* Wed Aug  7 2013 Tomas Mraz <tmraz@redhat.com> - 2.0.20-3
- adjust to the unversioned docdir change (#993785)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Tomas Mraz <tmraz@redhat.com> - 2.0.20-1
- new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Tomas Mraz <tmraz@redhat.com> - 2.0.19-7
- fix CVE-2012-6085 - skip invalid key packets (#891142)

* Thu Nov 22 2012 Tomas Mraz <tmraz@redhat.com> - 2.0.19-6
- use AES as default crypto algorithm in FIPS mode (#879047)

* Fri Nov 16 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.0.19-5
- rebuild for <f18 (#877106)

* Fri Jul 27 2012 Tomas Mraz <tmraz@redhat.com> - 2.0.19-4
- fix negated condition (#843842)

* Thu Jul 26 2012 Tomas Mraz <tmraz@redhat.com> - 2.0.19-3
- add compat symlinks and provides if built on RHEL

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Tomas Mraz <tmraz@redhat.com> - 2.0.19-1
- new upstream release
- set environment in protect-tool (#548528)
- do not reject OCSP signing certs without keyUsage (#720174)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.18-2
- build with --enable-standard-socket

* Wed Aug 17 2011 Tomas Mraz <tmraz@redhat.com> - 2.0.18-1
- new upstream release (#728481)

* Mon Jul 25 2011 Tomas Mraz <tmraz@redhat.com> - 2.0.17-2
- fix a bug that shows up with the new libgcrypt release (#725369)

* Thu Jan 20 2011 Tomas Mraz <tmraz@redhat.com> - 2.0.17-1
- new upstream release (#669611)

* Tue Aug 17 2010 Tomas Mraz <tmraz@redhat.com> - 2.0.16-3
- drop the provides/obsoletes for gnupg
- drop the man page file conflicting with gnupg-1.x

* Fri Aug 13 2010 Tomas Mraz <tmraz@redhat.com> - 2.0.16-2
- drop the compat symlinks as gnupg-1.x is revived

* Tue Jul 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.16-1
- gnupg-2.0.16

* Fri Jul 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.14-4
- gpgsm realloc patch (#617706)

* Fri Jun 18 2010 Tomas Mraz <tmraz@redhat.com> - 2.0.14-3
- initialize small amount of secmem for list of algorithms in help (#598847)
  (necessary in the FIPS mode of libgcrypt)

* Tue Feb  9 2010 Tomas Mraz <tmraz@redhat.com> - 2.0.14-2
- disable selinux support - it is too rudimentary and restrictive (#562982)

* Mon Jan 11 2010 Tomas Mraz <tmraz@redhat.com> - 2.0.14-1
- new upstream version
- fix a few tests so they do not need to execute gpg-agent

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.13-4
- Explicitly BR libassuan-static in accordance with the Packaging
  Guidelines (libassuan-devel is still static-only).

* Fri Oct 23 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.13-3
- drop s390 specific ifnarchs as all the previously missing dependencies
  are now there
- split out gpgsm into a smime subpackage to reduce main package dependencies

* Wed Oct 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.13-2
- provide/obsolete gnupg-1 and add compat symlinks to be able to drop
  gnupg-1

* Fri Sep 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.0.13-1
- gnupg-2.0.13
- Unable to use gpg-agent + input methods (#228953)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.0.12-1
- gnupg-2.0.12

* Wed Mar 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.0.11-1
- gnupg-2.0.11

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 31 2009 Karsten Hopp <karsten@redhat.com> 2.0.10-1
- don't require pcsc-lite-libs and libusb on mainframe where
  we don't have those packages as there's no hardware for that

* Tue Jan 13 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0.10-1
- gnupg-2.0.10

* Mon Aug 04 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.9-3
- workaround rpm quirks

* Sat May 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.9-2
- Patch from upstream to fix curl 7.18.1+ and gcc4.3+ compile error

* Mon May 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.9-1.1
- minor release bump for sparc rebuild

* Wed Mar 26 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.9-1
- gnupg2-2.0.9
- drop Provides: openpgp
- versioned Provides: gpg
- own %%_sysconfdir/gnupg

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.8-3
- respin (gcc43)

* Wed Jan 23 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.8-2
- avoid kde-filesystem dep (#427316)

* Thu Dec 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.8-1
- gnupg2-2.0.8

* Mon Dec 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.8-0.1.rc1
- gnupg2-2.0.8rc1

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.7-5
- respin for openldap

* Mon Nov 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.7-4
- Requires: kde-filesystem (#377841)

* Wed Oct 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.7-3
- %%build: (re)add mkdir -p $HOME/.gnupg

* Wed Oct 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.7-2
- Requires: dirmngr (#312831)

* Mon Sep 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.7-1
- gnupg-2.0.7

* Fri Aug 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.6-2
- respin (libassuan)

* Thu Aug 16 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.6-1
- gnupg-2.0.6
- License: GPLv3+

* Thu Aug 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.5-4
- License: GPLv3

* Mon Jul 16 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.5-3
- 2.0.5 too many open files fix

* Fri Jul 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.5-2
- gnupg-2.0.5
- gpg-agent not restarted after kde session crash/killed (#196327)
- BR: libassuan-devel > 1.0.2, libksba-devel > 1.0.2

* Fri May 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.4-1
- gnupg-2.0.4

* Thu Mar 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.3-1
- gnupg-2.0.3

* Fri Feb 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.2-1
- gnupg-2.0.2

* Wed Dec 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.1-2
- CVE-2006-6235 (#219934)

* Wed Nov 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.1-1
- gnupg-2.0.1
- CVE-2006-6169 (#217950)

* Sat Nov 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.1-0.3.rc1
- gnupg-2.0.1rc1

* Thu Nov 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.0-4
- update %%description
- drop dearmor patch

* Mon Nov 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.0-3
- BR: libassuan-static >= 1.0.0

* Mon Nov 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.0-2
- gnupg-2.0.0

* Fri Nov 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.95-3
- upstream 64bit patch

* Mon Nov 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.95-2
- fix (more) file conflicts with gnupg

* Mon Nov 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.95-1
- 1.9.95

* Wed Oct 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.94-1
- 1.9.94

* Wed Oct 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.93-1
- 1.9.93

* Wed Oct 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.92-2
- fix file conflicts with gnupg

* Wed Oct 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.92-1
- 1.9.92

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.91-4
- make check ||: (apparently checks return err even on success?)

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.91-3
- --enable-selinux-support
- x86_64: --disable-optimization (to avoid gpg2 segfaults), for now

* Thu Oct 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.91-1
- 1.9.91

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.22-8
- respin

* Tue Sep 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.90-1
- 1.9.90 (doesn't build, not released)

* Mon Sep 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.23-1
- 1.9.23 (doesn't build, not released)

* Mon Sep 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.22-7
- gpg-agent-startup.sh: fix case where valid .gpg-agent-info exists

* Mon Sep 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.22-6
- fix "syntax error in gpg-agent-startup.sh" (#206887)

* Thu Sep 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.22-3
- fc6 respin (for libksba-1.0)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.22-2
- fc6 respin

* Fri Jul 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.22-1
- 1.9.22

* Thu Jun 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.21-3
- fix "gpg-agent not restarted after kde session crash/killed (#196327)

* Thu Jun 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.21-2
- 1.9.21
- omit gpg2 binary to address CVS-2006-3082 (#196190)

* Mon Mar  6 2006 Ville Skyttä <ville.skytta at iki.fi>> 1.9.20-3
- Don't hardcode pcsc-lite lib name (#184123)

* Thu Feb 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.20-2
- fc4+: use /etc/kde/(env|shutdown) for scripts (#175744)

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Tue Dec 20 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.20-1
- 1.9.20

* Thu Dec 01 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.19-8
- include gpg-agent-(startup|shutdown) scripts (#136533)
- BR: libksba-devel >= 1.9.12
- %%check: be permissive about failures (for now)

* Wed Nov 30 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.19-3
- BR: libksba-devel >= 1.9.13

* Tue Oct 11 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.19-2
- back to BR: libksba-devel = 1.9.11

* Tue Oct 11 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.19-1
- 1.9.19

* Fri Aug 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.18-9
- configure: NEED_KSBA_VERSION=0.9.12 -> 0.9.11

* Fri Aug 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.18-7
- re-enable 'make check', rebuild against (older) libksba-0.9.11

* Tue Aug  9 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.18-6
- don't 'make check' by default (regular builds pass, but FC4/5+plague fails)

* Mon Aug  8 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.18-5
- 1.9.18
- drop pth patch (--enable-gpg build fixed)
- update description (from README)

* Fri Jul  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.9.17-1
- 1.9.17, signal info patch applied upstream (#162264).
- Patch to fix lvalue build error with gcc4 (upstream #485).
- Patch scdaemon and pcsc-wrapper to load the versioned (non-devel)
  pcsc-lite lib by default.

* Fri May 13 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.9.16-3
- Include upstream's patch for signal.c.

* Tue May 10 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.9.16-1
- Merge changes from Rex's 1.9.16-1 (Thu Apr 21):
-   opensc support unconditional
-   remove hard-coded .gz from %%post/%%postun
-   add %%check section
-   add pth patch
- Put back patch modified from 1.9.15-4 to make tests verbose
  and change signal.c to describe received signals better.

* Sun May  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- Drop patch0 again.

* Sun May  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.9.15-4
- Add patch0 temporarily to get some output from failing test.

* Sat May  7 2005 David Woodhouse <dwmw2@infradead.org> 1.9.15-3
- Rebuild.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Feb  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:1.9.15-1
- Make install-info in scriptlets less noisy.

* Tue Jan 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.15-0.fdr.1
- 1.9.15

* Fri Jan 07 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.14-0.fdr.2
- note patch/hack to build against older ( <1.0) libgpg-error-devel

* Thu Jan 06 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.14-0.fdr.1
- 1.9.14
- enable opensc support
- BR: libassuan-devel >= 0.6.9

* Thu Oct 21 2004 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.11-0.fdr.4
- remove suid.

* Thu Oct 21 2004 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.11-0.fdr.3
- remove Provides: newpg

* Wed Oct 20 2004 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.11-0.fdr.2
- Requires: pinentry
- gpg2 suid
- update description

* Tue Oct 19 2004 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.11-0.fdr.1
- first try
- leave out opensc support (for now), enable --with-opensc

