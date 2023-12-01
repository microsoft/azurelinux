Summary:        Git for operating system binaries
Name:           ostree
Version:        2022.1
Release:        3%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://ostree.readthedocs.io/en/latest
Source0:        https://github.com/ostreedev/ostree/releases/download/v%{version}/lib%{name}-%{version}.tar.xz
Source1:        91-ostree.preset
Patch0:         dualboot-support.patch
Patch1:         0001-ostree-Copying-photon-config-to-boot-directory.patch
Patch2:         0002-ostree-Adding-load-env-to-menuentry.patch
Patch3:         0003-ostree-converting-osname-to-mariner.patch
BuildRequires:  attr-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  curl-devel
BuildRequires:  dracut
BuildRequires:  e2fsprogs-devel
BuildRequires:  fuse-devel
BuildRequires:  git
BuildRequires:  glib-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-gobject-introspection
BuildRequires:  gpgme-devel
BuildRequires:  gtk-doc
BuildRequires:  icu-devel
BuildRequires:  libarchive-devel
BuildRequires:  libcap-devel
BuildRequires:  libpsl-devel
BuildRequires:  libsoup-devel
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  sqlite-devel
BuildRequires:  systemd-devel
BuildRequires:  which
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
Requires:       dracut
Requires:       gpgme
Requires:       libassuan
Requires:       systemd

%description
OSTree is a tool for managing bootable, immutable, versioned
filesystem trees. While it takes over some of the roles of tradtional
"package managers" like dpkg and rpm, it is not a package system; nor
is it a tool for managing full disk images. Instead, it sits between
those levels, offering a blend of the advantages (and disadvantages)
of both.

%package libs
Summary:        Development headers for %{name}
Group:          Development/Libraries
Requires:       icu
Requires:       libpsl
Requires:       libsoup

%description libs
The %{name}-libs provides shared libraries for %{name}.

%package devel
Summary:        Development headers for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs

%description devel
The %{name}-devel package includes the header files for the %{name} library.

%package grub2
Summary:        GRUB2 integration for OSTree
Group:          Development/Libraries
Requires:       %{name}
Requires:       grub2
Requires:       grub2-efi

%description grub2
GRUB2 integration for OSTree

%prep
%autosetup -p 1 -n lib%{name}-%{version}

%build
env NOCONFIGURE=1 ./autogen.sh

%configure \
     --disable-silent-rules \
     --enable-gtk-doc \
     --with-dracut \
     --without-selinux \
     --enable-libsoup-client-certs
make %{?_smp_mflags}

%check
make check

%install
make DESTDIR=%{buildroot} INSTALL="install -p -c" install
find %{buildroot} -type f -name "*.la" -delete -print
install -D -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system-preset/91-ostree.preset
install -vdm 755 %{buildroot}%{_sysconfdir}/ostree/remotes.d

%post
%systemd_post ostree-remount.service

%preun
%systemd_preun ostree-remount.service

%postun
%systemd_postun_with_restart ostree-remount.service

%files
%license COPYING
%license COPYING
%doc README.md
%{_bindir}/ostree
%{_bindir}/rofiles-fuse
%{_datadir}/ostree
%dir %{_libdir}/dracut/modules.d/98ostree
%{_unitdir}/ostree*.service
%{_unitdir}/ostree-finalize-staged.path
%{_libdir}/dracut/modules.d/98ostree/*
%{_mandir}/man1/ostree-admin*
%{_libdir}/systemd/system-generators/ostree-system-generator
%{_libdir}/systemd/system-preset/91-ostree.preset
%exclude %{_sysconfdir}/grub.d/*ostree
%exclude %{_libexecdir}/libostree/grub2*
%{_libdir}/ostree/ostree-prepare-root
%{_sysconfdir}/dracut.conf.d/ostree.conf
%{_libdir}/ostree/ostree-remount
%{_libdir}/tmpfiles.d/ostree-tmpfiles.conf
%{_libexecdir}/libostree/*

%files libs
%{_sysconfdir}/ostree
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/OSTree-1.0.typelib

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/bash-completion/completions/ostree
%{_datadir}/gtk-doc/html/ostree
%{_datadir}/gir-1.0/OSTree-1.0.gir
%exclude %{_mandir}/man1/ostree-admin*
%{_mandir}/man1/*.gz
%{_mandir}/man5/*.gz

%files grub2
%{_sysconfdir}/grub.d/*ostree
%{_libexecdir}/libostree/grub2*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2022.1-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Jun 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2022.1-2
- Enabling package for ARM64 architectures.

* Thu Jan 27 2022 Henry Li <lihl@microsoft.com> - 2022.1-1
- Upgrade to version 2022.1
- Fix Source0 field to use macro to represent package version

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2021.4-2
- Remove unused gobject-introspection-python requirement
- Explicity specify python3-gobject-introspection requirement

* Thu Sep 30 2021 Olivia Crain <oliviacrain@microsoft.com> - 2021.4-1
- Upgrade to latest upstream and rebase patches

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2019.2-11
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Nov 03 2020 Ruying Chen <v-ruyche@microsoft.com> - 2019.2-10
- Systemd supports merged /usr. Update installation and unit file directory macro.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2019.2-9
-   Added %%license line automatically

*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 2019.2-8
-   Replace BuildArch with ExclusiveArch

*   Wed Apr 15 2020 Andrew Phelps <anphel@microsoft.com> 2019.2-7
-   Update Source0 with git submodules included for offline build.

*   Tue Apr 14 2020 Emre Girgin <mrgirgin@microsoft.com> 2019.2-6
-   Remove mkinitcpio from build.

*   Tue Apr 7 2020 Paul Monson <paulmon@microsoft.com> 2019.2-5
-   Add #Source0. License verified.

*   Mon Dec 2 2019 Saravanan Somasundaram <sarsoma@microsoft.com> 2019.2-4
-   Adding Mariner Patch - converting os name to Mariner

*   Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> 2019.2-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Fri Sep 13 2019 Ankit Jain <ankitja@vmware.com> 2019.2-2
-   Added support to get kernel and systemd commandline param
-   from photon.cfg and systemd.cfg

*   Tue May 14 2019 Ankit Jain <ankitja@vmware.com> 2019.2-1
-   Initial build. First version
