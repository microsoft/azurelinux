## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/ostree.azl.macros}

# We haven't tried to ship the tests on RHEL
%if 0%{?rhel}
    %bcond_with tests
%else
    %bcond_without tests
%endif

Summary: Tool for managing bootable, immutable filesystem trees
Name: ostree
Version: 2025.7
Release: %autorelease
Source0: https://github.com/ostreedev/%{name}/releases/download/v%{version}/libostree-%{version}.tar.xz
Source9999: ostree.azl.macros
License: LGPL-2.0-or-later
URL: https://ostreedev.github.io/ostree/

# Conditional to ELN right now to reduce blast radius; xref
# https://github.com/containers/composefs/pull/229#issuecomment-1838735764
%if 0%{?rhel} >= 10
ExcludeArch:    %{ix86}
%endif

BuildRequires: make
BuildRequires: git
# We always run autogen.sh
BuildRequires: autoconf automake libtool
# For docs
BuildRequires: gtk-doc
# Core requirements
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libcurl)
BuildRequires: openssl-devel
BuildRequires: pkgconfig(composefs)
%if %{with tests}
BuildRequires: pkgconfig(libsoup-3.0)
%endif
BuildRequires: libattr-devel
# The tests require attr
BuildRequires: attr
# Extras
BuildRequires: pkgconfig(libarchive)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libselinux)
BuildRequires: pkgconfig(mount)
%if 0%{?fedora} <= 36
BuildRequires: pkgconfig(fuse)
%else
BuildRequires: pkgconfig(fuse3)
%endif
BuildRequires: pkgconfig(e2p)
BuildRequires: libcap-devel
BuildRequires: gpgme-devel
BuildRequires: pkgconfig(libsystemd)
BuildRequires: /usr/bin/g-ir-scanner
BuildRequires: dracut
BuildRequires:  bison

# Runtime requirements
Requires: dracut
Requires: /usr/bin/gpgv2
Requires: systemd-units
Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# Strictly speaking, this is not a current hard requirement, but it will
# be in the future.
Requires: composefs

%description
libostree is a shared library designed primarily for
use by higher level tools to manage host systems (e.g. rpm-ostree),
as well as container tools like flatpak and the atomic CLI.

%package libs
Summary: C shared libraries %{name}

%description libs
The %{name}-libs provides shared libraries for %{name}.

%package devel
Summary: Development headers for %{name}
Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package includes the header files for the %{name} library.

%ifnarch s390 s390x
%package grub2
Summary: GRUB2 integration for OSTree
%ifnarch aarch64 %{arm}
Requires: grub2
%else
Requires: grub2-efi
%endif
Requires: ostree

%description grub2
GRUB2 integration for OSTree
%endif

%if %{with tests}
%package tests
Summary: Tests for the %{name} package
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description tests
This package contains tests that can be used to verify
the functionality of the installed %{name} package.
%endif

%prep
%autosetup -Sgit -n libostree-%{version}

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules \
           --enable-gtk-doc \
           --with-selinux \
           --with-curl \
           --with-openssl \
           --without-soup \
           --with-composefs \
           %{?with_tests:--with-soup3} \
           %{?!with_tests:--without-soup3} \
           %{?with_tests:--enable-installed-tests=exclusive} \
           --with-dracut=yesbutnoconf
%make_build

%install
%make_install INSTALL="install -p -c"
find %{buildroot} -name '*.la' -delete

# Needed to enable the service at compose time currently
%post
%systemd_post ostree-remount.service

%preun
%systemd_preun ostree-remount.service

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{_bindir}/ostree
%{_bindir}/rofiles-fuse
%{_datadir}/ostree
%{_datadir}/bash-completion/completions/*
%dir %{_prefix}/lib/dracut/modules.d/50ostree
%{_prefix}/lib/systemd/system/ostree*.*
%{_prefix}/lib/dracut/modules.d/50ostree/*
%{_mandir}/man*/*.gz
%{_prefix}/lib/systemd/system-generators/ostree-system-generator
%exclude %{_sysconfdir}/grub.d/*ostree
%exclude %{_libexecdir}/libostree/grub2*
%{_prefix}/lib/tmpfiles.d/*
%{_prefix}/lib/ostree
# Moved in git master
%{_libexecdir}/libostree/*

%files libs
%{_sysconfdir}/ostree
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/OSTree-1.0.typelib

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%dir %{_datadir}/gtk-doc/html/ostree
%{_datadir}/gtk-doc/html/ostree
%{_datadir}/gir-1.0/OSTree-1.0.gir

%ifnarch s390 s390x
%files grub2
%{_sysconfdir}/grub.d/*ostree
%dir %{_libexecdir}/libostree
%{_libexecdir}/libostree/grub2*
%endif

%if %{with tests}
%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests
%endif

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 azldev <azurelinux@microsoft.com> - 2025.7-2
- Latest state for ostree

* Fri Nov 14 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.7-1
- Release 2025.7

* Mon Sep 08 2025 Colin Walters <walters@verbum.org> - 2025.6-1
- Update to 2025.6

* Sun Sep 07 2025 Colin Walters <walters@verbum.org> - 2025.5-2
- Update to 2025.6

* Mon Aug 25 2025 Colin Walters <walters@verbum.org> - 2025.5-1
- Release v2025.5

* Wed Jul 30 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.4-3
- Backport https://github.com/ostreedev/ostree/pull/3487

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2025.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Colin Walters <walters@verbum.org> - 2025.4-1
- Release v2025.4

* Mon Jul 14 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.3-2
- sources: include test-signed-commit-ed25519.sh

* Thu Jul 10 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.3-1
- Release v2025.3

* Sat Mar 22 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.2-2
- Rev bump

* Fri Mar 21 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.2-1
- Release 2025.2

* Thu Jan 16 2025 Joseph Marrero Corchado <jmarrero@redhat.com> - 2025.1-1
- Rebase to ostree 2025.1

* Fri Dec 20 2024 Colin Walters <walters@verbum.org> - 2024.10-1
- https://github.com/ostreedev/ostree/releases/tag/v2024.10

* Tue Nov 05 2024 Colin Walters <walters@verbum.org> - 2024.9-1
- https://github.com/ostreedev/ostree/releases/tag/v2024.9

* Thu Oct 24 2024 HuijingHei <hhei@redhat.com> - 2024.8-3
- Backport https://github.com/ostreedev/ostree/pull/3323

* Mon Sep 23 2024 Christian Stadelmann <a.fp.o@genodeftest.de> - 2024.8-2
- Spec file: Update upstream URL to avoid hacked website

* Thu Sep 19 2024 Colin Walters <walters@verbum.org> - 2024.8-1
- https://github.com/ostreedev/ostree/releases/tag/v2024.8

* Sun Sep 15 2024 Timothée Ravier <tim@siosm.fr> - 2024.7-3
- Backport https://github.com/ostreedev/ostree/pull/3300 (fedora#2312453)

* Sun Sep 15 2024 Timothée Ravier <tim@siosm.fr> - 2024.7-2
- Cleanup old patches

* Fri Jul 19 2024 Colin Walters <walters@verbum.org> - 2024.7-1
- https://github.com/ostreedev/ostree/releases/tag/v2024.7

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 17 2024 Joseph Marrero <jmarrero@redhat.com> - 2024.6-1
- Release 2024.6

* Sat Mar 16 2024 Colin Walters <walters@verbum.org> - 2024.5-3
- Cherry pick https://github.com/ostreedev/ostree/pull/3216

* Thu Mar 14 2024 Colin Walters <walters@verbum.org> - 2024.5-2
- https://github.com/ostreedev/ostree/releases/tag/v2024.5

* Thu Mar 14 2024 Colin Walters <walters@verbum.org> - 2024.5-1
- https://github.com/ostreedev/ostree/releases/tag/v2024.5

* Fri Feb 23 2024 Colin Walters <walters@verbum.org> - 2024.4-1
- https://github.com/ostreedev/ostree/releases/tag/v2024.4

* Fri Feb 16 2024 Colin Walters <walters@verbum.org> - 2024.3-3
- Unconditionally use composefs

* Thu Feb 15 2024 Colin Walters <walters@verbum.org> - 2024.3-2
- BR composefs-devel

* Wed Feb 14 2024 Colin Walters <walters@verbum.org> - 2024.3-1
- https://github.com/ostreedev/ostree/releases/tag/v2024.3

* Thu Feb 08 2024 Colin Walters <walters@verbum.org> - 2024.2-1
- https://github.com/ostreedev/ostree/releases/tag/v2024.2

* Thu Feb 01 2024 Timothée Ravier <tim@siosm.fr> - 2024.1-3
- grub2-15_ostree: Graceful exit if /etc/default/grub doesn't exist

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Colin Walters <walters@verbum.org> - 2024.1-1
- https://github.com/ostreedev/ostree/releases/tag/v2024.1

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Joseph Marrero <jmarrero@redhat.com> - 2023.8-5
- Backport https://github.com/ostreedev/ostree/pull/3130

* Thu Jan 04 2024 Colin Walters <walters@verbum.org> - 2023.8-4
- Backport https://github.com/ostreedev/ostree/pull/3129/commits/a1c1c0b500
  d23ff129adbfe9486a067788b24969 To aid https://github.com/coreos/fedora-
  coreos-config/pull/2783

* Wed Dec 06 2023 Colin Walters <walters@verbum.org> - 2023.8-2
- https://github.com/ostreedev/ostree/releases/tag/v2023.8

* Mon Dec 04 2023 Colin Walters <walters@verbum.org> - 2023.7-4
- Enable composefs only on fedora/rhel10 to fix COPR builds
  which pull from this dist-git
- Exclude x86 on FedoraELN since composefs is
- Always disable soup to re-sync with ostree upstream logic

* Sun Dec 03 2023 Colin Walters <walters@verbum.org> - 2023.7-3
- Add a composefs requirement; this is not actually a requirement
  right now, but will be in the near future, so let's prepare for it.

* Fri Oct 20 2023 Colin Walters <walters@verbum.org> - 2023.7-2
- https://github.com/ostreedev/ostree/releases/tag/v2023.7

* Fri Oct 06 2023 Colin Walters <walters@verbum.org> - 2023.6-2
- Cherry pick
  https://github.com/ostreedev/ostree/pull/3060/commits/3b2fd6e9ff0a3a91a2b72f524492e4f198069dec

* Fri Aug 25 2023 Colin Walters <walters@verbum.org> - 2023.6-1
- https://github.com/ostreedev/ostree/releases/tag/v2023.6

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Colin Walters <walters@verbum.org> - 2023.5-2
- https://github.com/ostreedev/ostree/releases/tag/v2023.5

* Mon Jun 26 2023 Colin Walters <walters@verbum.org> - 2023.4-2
- Cherry pick patch to fix flatpak

* Tue Jun 20 2023 Colin Walters <walters@verbum.org> - 2023.4-1
- https://github.com/ostreedev/ostree/releases/tag/v2023.4

* Tue Jun 13 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 2023.3-4
- Switch License tags to SPDX

* Thu Jun 1 2023 Dusty Mabe <dusty@dustymabe.com> - 2023.3-3
- Backport log message fix in https://github.com/ostreedev/ostree/pull/2870
- Backport fallocate fix in https://github.com/ostreedev/ostree/pull/2871

* Tue May 30 2023 Dusty Mabe <dusty@dustymabe.com> - 2023.3-2
- Backport OSTree Autoprune fixes in https://github.com/ostreedev/ostree/pull/2866

* Thu May 18 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 2023.3-1
- https://github.com/ostreedev/ostree/releases/tag/v2023.3

* Wed Mar 22 2023 Colin Walters <walters@verbum.org> - 2023.2-2
- https://github.com/ostreedev/ostree/releases/tag/v2023.2

* Fri Feb 17 2023 Colin Walters <walters@verbum.org> - 2023.1-2
- https://github.com/ostreedev/ostree/releases/tag/v2023.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2022.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Colin Walters <walters@verbum.org> - 2022.7-2
- https://github.com/ostreedev/ostree/releases/tag/v2022.7

* Mon Oct 10 2022 Luca BRUNO <lucab@lucabruno.net> - 2022.6-1
- New upstream version
  https://github.com/ostreedev/ostree/releases/tag/v2022.6

* Fri Jul 22 2022 Colin Walters <walters@verbum.org> - 2022.5-2
- https://github.com/ostreedev/ostree/releases/tag/v2022.5

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 06 2022 Colin Walters <walters@verbum.org> - 2022.4-2
- https://github.com/ostreedev/ostree/releases/tag/v2022.4

* Thu May 19 2022 Jonathan Lebon <jonathan@jlebon.com> - 2022.3-3
- Only use FUSE 3 for rofiles-fuse on f37+

* Wed May 04 2022 Colin Walters <walters@verbum.org> - 2022.3-2
- https://github.com/ostreedev/ostree/releases/tag/v2022.3

* Fri Apr 01 2022 Debarshi Ray <rishi@fedoraproject.org> - 2022.2-2
- Use FUSE 3 for rofiles-fuse

* Fri Apr 01 2022 Luca BRUNO <lucab@lucabruno.net> - 2022.2-1
- New upstream version
  https://github.com/ostreedev/ostree/releases/tag/v2022.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Luca BRUNO <lucab@lucabruno.net> - 2022.1-1
- New upstream version
  https://github.com/ostreedev/ostree/releases/tag/v2022.1

* Thu Dec 09 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.6-3
- Summary locking fix (GH PR 2493)

* Mon Dec 06 2021 Joseph Marrero <jmarrero@fedoraproject.org> - 2021.6-2
- Add attr as a build dependency as we use it for running the tests

* Tue Nov 23 2021 Luca BRUNO <lucab@lucabruno.net> - 2021.6-1
- New upstream version
  https://github.com/ostreedev/ostree/releases/tag/v2021.6

* Wed Oct 06 2021 Colin Walters <walters@verbum.org> - 2021.5-2
- https://github.com/coreos/ostree/releases/tag/v2021.5

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2021.4-3
- Rebuilt with OpenSSL 3.0.0

* Thu Sep 09 2021 Colin Walters <walters@verbum.org> - 2021.4-2
- https://github.com/ostreedev/ostree/releases/tag/v2021.4

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Luca BRUNO <lucab@lucabruno.net> - 2021.3-1
- New upstream version
  https://github.com/ostreedev/ostree/releases/tag/v2021.3

* Mon May 10 2021 Jeff Law <jlaw@tachyum.com> - 2021.2-3
- Re-enable LTO

* Thu Apr 15 2021 Colin Walters <walters@verbum.org> - 2021.2-2
- https://github.com/coreos/ostree/releases/tag/v2021.2

* Tue Mar 23 2021 Colin Walters <walters@verbum.org> - 2021.1-2
- https://github.com/ostreedev/ostree/releases/tag/v2021.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 18 08:42:24 UTC 2020 Luca BRUNO <lucab@lucabruno.net> - 2020.8-1
- New upstream version
- https://github.com/ostreedev/ostree/releases/tag/v2020.8

* Fri Oct 30 2020 Jeff Law <law@redhat.com> - 2020.7-4
- Fix volatile issues exposed by gcc-11

* Thu Oct 15 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.7-3
- Backport https://github.com/ostreedev/ostree/pull/2219 for
  https://bugzilla.redhat.com/show_bug.cgi?id=1888436

* Wed Oct 14 2020 Colin Walters <walters@verbum.org> - 2020.7-2
- https://github.com/ostreedev/ostree/releases/tag/v2020.7

* Wed Oct 07 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.6-5
- Backport https://github.com/ostreedev/ostree/pull/2211 for
  https://bugzilla.redhat.com/show_bug.cgi?id=1886149

* Thu Sep 24 2020 Colin Walters <walters@verbum.org> - 2020.6-4
- Backport https://github.com/ostreedev/ostree/pull/2202

* Fri Sep 18 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.6-3
- Revert support for devicetrees
  https://github.com/ostreedev/ostree/issues/2154
  https://bugzilla.redhat.com/show_bug.cgi?id=1880499

* Thu Sep 03 2020 Colin Walters <walters@verbum.org> - 2020.6-2
- https://github.com/ostreedev/ostree/releases/tag/v2020.6

* Tue Aug 18 2020 Colin Walters <walters@verbum.org> - 2020.5-2
- https://github.com/ostreedev/ostree/releases/tag/v2020.5

* Sat Aug 01 2020 Colin Walters <walters@verbum.org> - 2020.4-4
- Backport patch for https://bugzilla.redhat.com/show_bug.cgi?id=1862568

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Colin Walters <walters@verbum.org> - 2020.4-2
- https://github.com/ostreedev/ostree/releases/tag/v2020.4

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 2020.3-6
Disable LTO

* Thu Jun 18 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.3-5
- Backport patch to handle EOPNOTSUPP on NFS:
  https://gitlab.gnome.org/GNOME/libglnx/-/merge_requests/18

* Thu May 21 2020 Jonathan Lebon <jonathan@jlebon.com> - 2020.3-4
- Backport patch to neuter sysroot.readonly for FCOS
  https://github.com/coreos/fedora-coreos-tracker/issues/488
  https://github.com/ostreedev/ostree/pull/2108

* Fri Apr 17 2020 Dusty Mabe <dusty@dustymabe.com> - 2020.3-3
- Backport patchset that should help us with concurrently pulling
  https://github.com/ostreedev/ostree/pull/2077

* Sat Mar 14 2020 Colin Walters <walters@verbum.org> - 2020.3-2
- https://github.com/ostreedev/ostree/releases/tag/v2020.3

* Fri Feb 21 2020 Colin Walters <walters@verbum.org> - 2020.2-2
- https://github.com/ostreedev/ostree/releases/tag/v2020.2

* Thu Feb 20 2020 Colin Walters <walters@verbum.org> - 2020.1-2
- https://github.com/ostreedev/ostree/releases/tag/v2020.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 10 2019 Colin Walters <walters@verbum.org> - 2019.6-2
- https://github.com/ostreedev/ostree/releases/tag/v2019.6

* Wed Oct 30 2019 Colin Walters <walters@verbum.org> - 2019.5-2
- https://github.com/ostreedev/ostree/releases/tag/v2019.5

* Thu Sep 26 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.4-2
- Revert ostree-grub2 patch to fix duplicate entries
  https://github.com/ostreedev/ostree/pull/1929#issuecomment-539022174

* Thu Sep 26 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.4-2
- Backport patch to fix duplicate GRUB2 entries when using BLS
  https://bugzilla.redhat.com/show_bug.cgi?id=1751272#c27

* Wed Sep 25 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.4-1
- https://github.com/ostreedev/ostree/releases/tag/v2019.4

* Thu Aug 22 2019 Colin Walters <walters@verbum.org> - 2019.3-3
- https://github.com/ostreedev/ostree/releases/tag/v2019.3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Jonathan Lebon <jonathan@jlebon.com> - 2019.2-1
- https://github.com/ostreedev/ostree/releases/tag/v2019.2

* Sat Feb 09 2019 Dusty Mabe <dusty@dustymabe.com> - 2019.1-5
- Re-enable http2 in ostree build

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Sinny Kumari <ksinny@gmail.com> - 2019.1-3
- Backport patch to fix bare → bare imports
- Backport patch to Set xattr on correct fd for bare-user → bare-user imports

* Fri Jan 11 2019 Colin Walters <walters@verbum.org> - 2019.1-2
- https://github.com/ostreedev/ostree/releases/tag/v2019.1

* Fri Jan 11 2019 Colin Walters <walters@verbum.org> - 2018.9-2
- Work around https://src.fedoraproject.org/rpms/nfs-utils/pull-request/7

* Thu Oct 25 2018 Colin Walters <walters@verbum.org> - 2018.9-1
- https://github.com/ostreedev/ostree/releases/tag/v2018.9

* Wed Oct 17 2018 Jonathan Lebon <jonathan@jlebon.com>
- Add conditional for tests and disable by default on RHEL > 7

* Wed Aug 22 2018 Colin Walters <walters@verbum.org> - 2018.8-1
- https://github.com/ostreedev/ostree/releases/tag/v2018.8

* Sun Aug 12 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.7-2
- Enable grub2 support on ARMv7

* Fri Jul 20 2018 Colin Walters <walters@verbum.org> - 2018.7-1
- https://github.com/ostreedev/ostree/releases/tag/v2018.7

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Jonathan Lebon <jonathan@jlebon.com> - 2018.6-4
- Backport patch to fix /var mountpoints
  https://github.com/ostreedev/ostree/issues/1667

* Thu Jun 21 2018 Colin Walters <walters@redhat.com> - 2018.6-3
- https://github.com/ostreedev/ostree/releases/tag/v2018.6

* Fri May 11 2018 Colin Walters <walters@verbum.org> - 2018.5-1
- https://github.com/ostreedev/ostree/releases/tag/v2018.5

* Tue Apr 03 2018 Kalev Lember <klember@redhat.com> - 2018.3-2
- Backport a patch to avoid writing to parent repo

* Wed Mar 21 2018 Colin Walters <walters@verbum.org> - 2018.3-1
- https://github.com/ostreedev/ostree/releases/tag/v2018.3

* Fri Mar 02 2018 Jonathan Lebon <jlebon@redhat.com> - 2018.2-2
- Drop ostree-remount systemd service preset, already in fedora-release
  https://bugzilla.redhat.com/show_bug.cgi?id=1550799

* Thu Feb 15 2018 Colin Walters <walters@verbum.org> - 2018.2-1
- https://github.com/ostreedev/ostree/releases/tag/v2018.2

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Colin Walters <walters@verbum.org> - 2018.1-1
- https://github.com/ostreedev/ostree/releases/tag/v2018.1

* Wed Dec 20 2017 Colin Walters <walters@verbum.org> - 2017.15-1
- https://github.com/ostreedev/ostree/releases/tag/v2017.15
- Drop upstreamed patches; note this build disabled HTTP2 by
  default for now since we are hitting it with koji.  For more
  information see https://github.com/ostreedev/ostree/issues/1362

* Mon Dec 18 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.14-2
- Backport patch to drop HTTP2

* Mon Dec 04 2017 Colin Walters <walters@verbum.org> - 2017.14-1
- https://github.com/ostreedev/ostree/releases/tag/v2017.14
- Update description

* Mon Nov 27 2017 Colin Walters <walters@verbum.org> - 2017.13-4
- Backport patch to drop curl low speed checks; requested by flatpak

* Tue Nov 07 2017 Kalev Lember <klember@redhat.com> - 2017.13-3
- Backport a patch to fix a gnome-software crash when installing flatpaks
  (#1497642)

* Thu Nov 02 2017 Colin Walters <walters@verbum.org> - 2017.13-2
- https://github.com/ostreedev/ostree/releases/tag/v2017.13

* Tue Oct 03 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.12-2
- Let tests subpackage own ostree-trivial-httpd

* Mon Oct 02 2017 Colin Walters <walters@verbum.org> - 2017.12-1
- New upstream version
- https://github.com/ostreedev/ostree/releases/tag/v2017.12

* Thu Sep 14 2017 Colin Walters <walters@verbum.org> - 2017.11-1
- New upstream version
- Add tests subpackage, prep for https://fedoraproject.org/wiki/CI

* Tue Aug 22 2017 Ville Skyttä <ville.skytta@iki.fi> - 2017.10-3
- Own the %%{_libexecdir}/libostree dir

* Thu Aug 17 2017 Colin Walters <walters@verbum.org> - 2017.10-2
- New upstream version

* Sat Aug 12 2017 Ville Skyttä <ville.skytta@iki.fi> - 2017.9-5
- Own the %%{_datadir}/ostree dir

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2017.9-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Colin Walters <walters@verbum.org> - 2017.9-2
- New upstream version

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Colin Walters <walters@verbum.org> - 2017.8-3
- Switch to libcurl for F26+
  I think it works well; to recap the arguments below:
  It has various advantages like HTTP2, plus now that NetworkManager
  switched we are the last thing left in Fedora Atomic Host depending
  on libsoup.

* Thu Jul 06 2017 Colin Walters <walters@verbum.org> - 2017.8-2
- New upstream version

* Mon Jun 19 2017 Colin Walters <walters@verbum.org> - 2017.7-2
- Update to new upstream

* Fri Jun 02 2017 Colin Walters <walters@verbum.org> - 2017.6-4
- Fix previous commit to actually work

* Thu May 18 2017 Colin Walters <walters@verbum.org> - 2017.6-3
- Enable curl+openssl on f27+
  It has various advantages like HTTP2, plus now that NetworkManager
  switched we are the last thing left in Fedora Atomic Host depending
  on libsoup.

* Wed May 17 2017 Colin Walters <walters@verbum.org> - 2017.6-2
- New upstream version

* Wed Apr 19 2017 Colin Walters <walters@verbum.org> - 2017.5-2
- New upstream version

* Wed Apr 12 2017 Colin Walters <walters@verbum.org> - 2017.4-2
- New upstream version

* Fri Mar 10 2017 Colin Walters <walters@verbum.org> - 2017.3-2
- New upstream version

* Fri Mar 03 2017 Colin Walters <walters@redhat.com> - 2017.2-4
- Add patch for ppc64le grub2

* Thu Feb 23 2017 Colin Walters <walters@verbum.org> - 2017.2-3
- Backport libmount unref patch

* Tue Feb 14 2017 Colin Walters <walters@verbum.org> - 2017.2-2
- New upstream version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 07 2017 Jonathan Lebon <jlebon@redhat.com> - 2017.1-4
- Make ostree-grub2 require ostree

* Tue Feb 07 2017 Colin Walters <walters@verbum.org> - 2017.1-3
- Split off ostree-libs.  This is the inverse of upstream
  https://github.com/ostreedev/ostree/pull/659
  but renaming the package would be hard for low immediate gain.
  With this at least, flatpak could theoretically depend just on libostree.
  And similarly for rpm-ostree compose tree (when that gets split out).

* Mon Jan 23 2017 Colin Walters <walters@verbum.org> - 2017.1-2
- New upstream version

* Wed Jan 18 2017 Colin Walters <walters@verbum.org> - 2016.15-2
- Enable libmount for /boot readonly

* Mon Dec 12 2016 walters@redhat.com - 2016.15-1
- New upstream version

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2016.14-3
- Rebuild for gpgme 1.18

* Tue Nov 29 2016 Kalev Lember <klember@redhat.com> - 2016.14-2
- Backport a patch to remove an accidental print statement

* Wed Nov 23 2016 walters@redhat.com - 2016.14-1
- New upstream version

* Tue Nov 15 2016 walters@redhat.com - 2016.13-2
- New upstream version
- Require glib-networking to fix https://pagure.io/pungi-fedora/pull-request/103

* Sun Oct 23 2016 walters@verbum.org - 2016.12-1
- New upstream release

* Fri Oct 07 2016 walters@redhat.com - 2016.11-1
- New upstream version

* Tue Sep 20 2016 walters@redhat.com - 2016.10-8
- Backport another patch for systemd journal
  Resolves: #1265295

* Fri Sep 16 2016 walters@verbum.org - 2016.10-6
- Set --with-dracut=yesbutnoconf
  Resolves: #1331369

* Thu Sep 15 2016 walters@verbum.org - 2016.10-4
- Backport patch to fix bug#1265295

* Mon Sep 12 2016 Kalev Lember <klember@redhat.com> - 2016.10-3
- pull: Do allow executing deltas when mirroring into bare{,-user}

* Fri Sep 09 2016 Kalev Lember <klember@redhat.com> - 2016.10-2
- Drop libgsystem dependency

* Thu Sep 08 2016 walters@redhat.com - 2016.10-1
- New upstream version

* Wed Aug 31 2016 Colin Walters <walters@verbum.org> - 2016.9-1
- New upstream version

* Tue Aug 09 2016 walters@redhat.com - 2016.8-1
- New upstream version

* Tue Aug 09 2016 Colin Walters <walters@verbum.org> - 2016.7-4
- Add pending patch to fix date-based pruning

* Fri Jul 08 2016 walters@redhat.com - 2016.7-1
- New upstream version

* Mon Jun 20 2016 Colin Walters <walters@redhat.com> - 2016.6-1
- New upstream version

* Sun May  8 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.5-3
- aarch64 only has grub2-efi
- Use %%license

* Fri Apr 15 2016 Colin Walters <walters@redhat.com> - 2016.5-2
- New upstream version

* Wed Mar 23 2016 Colin Walters <walters@redhat.com> - 2016.4-2
- New upstream version

* Fri Feb 26 2016 Colin Walters <walters@redhat.com> - 2016.3-1
- New upstream version

* Tue Feb 23 2016 Colin Walters <walters@redhat.com> - 2016.2-1
- New upstream version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2016.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Colin Walters <walters@redhat.com> - 2016.1-2
- New upstream version

* Fri Dec 04 2015 Colin Walters <walters@redhat.com> - 2015.11-2
- New upstream version

* Sun Nov 22 2015 Colin Walters <walters@redhat.com> - 2015.10-1
- New upstream version

* Thu Nov 12 2015 Matthew Barnes <mbarnes@redhat.com> - 2015.9-3
- Add ostree-tmp-chmod.service to fix /tmp permissions on existing installs.
  Resolves: #1276775

* Fri Oct 30 2015 Colin Walters <walters@redhat.com> - 2015.9-2
- Add patch to fix permissions of /tmp
  Resolves: #1276775

* Wed Sep 23 2015 Colin Walters <walters@redhat.com> - 2015.9-1
- New upstream version

* Wed Aug 26 2015 Colin Walters <walters@redhat.com> - 2015.8-1
- New upstream version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Colin Walters <walters@redhat.com> - 2015.7-1
- New upstream version

* Thu May 28 2015 Colin Walters <walters@redhat.com> - 2015.6-4
- Add patch to ensure reliable bootloader ordering
  See: #1225088

* Thu Apr 30 2015 Colin Walters <walters@redhat.com> - 2015.6-3
- Close sysroot fd in finalize to fix Anaconda
  https://bugzilla.redhat.com/show_bug.cgi?id=1217578

* Fri Apr 17 2015 Colin Walters <walters@redhat.com> - 2015.6-2
- New upstream release

* Sun Apr 12 2015 Colin Walters <walters@redhat.com> - 2015.5-4
- (Really) Handle null epoch as well; this was injected for https://github.com/cgwalters/rpmdistro-gitoverlay

* Tue Apr 07 2015 Colin Walters <walters@redhat.com> - 2015.5-2
- New upstream release

* Mon Mar 30 2015 Dan Horák <dan[at]danny.cz> - 2015.4-5
- ExcludeArch is a build restriction and is global, switching to %%ifnarch

* Fri Mar 27 2015 Colin Walters <walters@redhat.com> - 2015.4-4
- Have grub2 subpackage match ExcludeArch with grub2

* Fri Mar 27 2015 Colin Walters <walters@redhat.com> - 2015.4-3
- Handle null epoch as well; this was injected for https://github.com/cgwalters/rpmdistro-gitoverlay

* Wed Mar 25 2015 Colin Walters <walters@redhat.com> - 2015.4-2
- New upstream release

* Mon Feb 16 2015 Colin Walters <walters@redhat.com> - 2015.3-3
- Require latest libgsystem to ensure people have it

* Fri Jan 23 2015 Colin Walters <walters@redhat.com> - 2015.3-2
- New upstream release

* Thu Jan 08 2015 Colin Walters <walters@redhat.com> - 2015.2-1
- New upstream release

* Sun Jan 04 2015 Colin Walters <walters@redhat.com> - 2014.13-2
- Add patch to ensure correct xattrs on modified config files
  Fixes: #1178208

* Wed Dec 17 2014 Colin Walters <walters@redhat.com> - 2014.13-1
- New upstream release

* Wed Nov 26 2014 Colin Walters <walters@redhat.com> - 2014.12-1
- New upstream version

* Thu Oct 30 2014 Colin Walters <walters@redhat.com> - 2014.11-1
- New upstream release

* Wed Oct 29 2014 Colin Walters <walters@redhat.com> - 2014.10.1.gedc3b9a-1
- New upstream release

* Fri Oct 24 2014 Colin Walters <walters@redhat.com> - 2014.9-2
- New upstream release

* Thu Oct 16 2014 Colin Walters <walters@redhat.com>
- New upstream release

* Mon Sep 08 2014 Colin Walters <walters@redhat.com> - 2014.6-1
- New upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2014.5-4
- Rebuilt for gobject-introspection 1.41.4

* Wed Jun 25 2014 Colin Walters <walters@verbum.org>
- Rebuild to pick up new libsoup

* Fri Jun 13 2014 Colin Walters <walters@verbum.org> - 2014.4-2
- Include /etc/ostree, even though it is empty

* Mon Jun 09 2014 Colin Walters <walters@verbum.org> - 2014.4-1
- New upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 13 2014 Colin Walters <walters@verbum.org> - 2014.4-1
- New upstream release

* Mon Mar 31 2014 Colin Walters <walters@verbum.org>
- New git snapshot for rpm-ostree

* Fri Mar 21 2014 Colin Walters <walters@verbum.org> - 2014.3-1
- New upstream release

* Fri Mar 14 2014 Colin Walters <walters@verbum.org> - 2014.2-3
- Move trusted.gpg.d to main runtime package, where it should be

* Fri Mar 07 2014 Colin Walters <walters@verbum.org> - 2014.2-2
- Depend on gpgv2
- Resolves: #1073813

* Sat Mar 01 2014 Colin Walters <walters@verbum.org> - 2014.2-1
- New upstream release
- Depend on libselinux
- Explicitly depend on libarchive too, we were actually failing
  to disable it before

* Fri Jan 24 2014 Colin Walters <walters@verbum.org> - 2014.1-1
- New upstream release

* Mon Jan 13 2014 Colin Walters <walters@verbum.org> - 2013.7-2
- Add preset file so ostree-remount is enabled by default, since
  it needs to be.

* Tue Oct 15 2013 Colin Walters <walters@verbum.org> - 2013.7-1
- New upstream release
- Now LGPLv2+ only
- Enable libarchive since it might be useful for people
- Enable new gpgme dependency

* Thu Sep 12 2013 Colin Walters <walters@verbum.org> - 2013.6-3
- Enable introspection

* Mon Sep 09 2013 Colin Walters <walters@verbum.org> - 2013.6-2
- Tweak description

* Mon Sep 09 2013 Colin Walters <walters@verbum.org> - 2013.6-1
- New upstream release

* Sat Aug 25 2013 Colin Walters <walters@verbum.org> - 2013.5-3
- And actually while we are here, drop all the embedded dependency
  goop from this spec file; it may live on in the EPEL branch.

* Sat Aug 25 2013 Colin Walters <walters@verbum.org> - 2013.5-2
- Drop requirement on linux-user-chroot
  We now require triggers to be processed on the build server
  by default, so ostree does not runtime-depend on linux-user-chroot.

* Sat Aug 17 2013 Colin Walters <walters@verbum.org> - 2013.5-1
- New upstream release
- Add devel package

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Colin Walters <walters@verbum.org> - 2013.4-1
- New upstream release

* Sun Jul 07 2013 Colin Walters <walters@verbum.org> - 2013.3-1
- New upstream release

* Mon Apr 01 2013 Colin Walters <walters@verbum.org> - 2013.1-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 23 2012 Colin Walters <walters@verbum.org> - 2012.13-1
- New upstream release

* Tue Dec 18 2012 Colin Walters <walters@verbum.org> - 2012.12-2
- Explicitly enable grub2 hook; otherwise we pick up whatever
  the buildroot has, which is not what we want.

* Mon Nov 19 2012 Colin Walters <walters@verbum.org> - 2012.12-1
- Initial import; thanks to Michel Alexandre Salim for review
  https://bugzilla.redhat.com/show_bug.cgi?id=819951

## END: Generated by rpmautospec
