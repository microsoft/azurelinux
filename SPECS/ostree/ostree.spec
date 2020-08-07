Summary:        Git for operating system binaries
Name:           ostree
Version:        2019.2
Release:        9%{?dist}
License:        LGPLv2+
URL:            https://ostree.readthedocs.io/en/latest
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Manually created Source tar which is equal to
# Source0 + .git as it requires git hooks at build time
#Source0:       https://github.com/ostreedev/ostree/releases/download/v2019.2/libostree-2019.2.tar.xz
Source0:        %{name}-%{version}-withsubmodules.tar.gz
ExclusiveArch:  x86_64
Source1:        91-ostree.preset
Patch0:         dualboot-support.patch
Patch1:         0001-ostree-Copying-photon-config-to-boot-directory.patch
Patch2:         0002-ostree-Adding-load-env-to-menuentry.patch
Patch3:         0003-ostree-converting-osname-to-mariner.patch
BuildRequires:  git
BuildRequires:  autoconf automake libtool which
BuildRequires:  gtk-doc
BuildRequires:  glib-devel
BuildRequires:  gobject-introspection
BuildRequires:  gobject-introspection-devel
BuildRequires:  gobject-introspection-python
BuildRequires:  xz-devel
BuildRequires:  icu-devel
BuildRequires:  sqlite-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  libpsl-devel
BuildRequires:  zlib-devel
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  libsoup-devel
BuildRequires:  attr-devel
BuildRequires:  libarchive-devel
BuildRequires:  fuse-devel
BuildRequires:  libcap-devel
BuildRequires:  gpgme-devel
BuildRequires:  systemd-devel
BuildRequires:  dracut
BuildRequires:  bison
Requires: dracut
Requires: systemd
Requires: libassuan
Requires: gpgme

%description
OSTree is a tool for managing bootable, immutable, versioned
filesystem trees. While it takes over some of the roles of tradtional
"package managers" like dpkg and rpm, it is not a package system; nor
is it a tool for managing full disk images. Instead, it sits between
those levels, offering a blend of the advantages (and disadvantages)
of both.

%package libs
Summary: Development headers for %{name}
Group: Development/Libraries
Requires: libpsl
Requires: libsoup
Requires: icu


%description libs
The %{name}-libs provides shared libraries for %{name}.

%package devel
Summary: Development headers for %{name}
Group: Development/Libraries
Requires: %{name}-libs

%description devel
The %{name}-devel package includes the header files for the %{name} library.

%package grub2
Summary: GRUB2 integration for OSTree
Group: Development/Libraries
Requires: grub2
Requires: grub2-efi
Requires: %{name}

%description grub2
GRUB2 integration for OSTree

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
find %{buildroot} -name '*.la' -delete
install -D -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/91-ostree.preset
install -vdm 755 %{buildroot}/etc/ostree/remotes.d
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/
cp -R %{buildroot}/lib/systemd/system/*.service %{buildroot}%{_prefix}/lib/systemd/system/
cp -R %{buildroot}/lib/systemd/system/ostree-finalize-staged.path %{buildroot}%{_prefix}/lib/systemd/system/
mkdir -p %{buildroot}%{_libdir}/systemd/system-generators/
cp -R %{buildroot}/lib/systemd/system-generators/ostree-system-generator %{buildroot}%{_libdir}/systemd/system-generators/
rm -rf %{buildroot}/lib

%post
%systemd_post ostree-remount.service

%preun
%systemd_preun ostree-remount.service

%postun
%systemd_postun_with_restart ostree-remount.service

%files
%license COPYING
%doc COPYING
%doc README.md
%{_bindir}/ostree
%{_bindir}/rofiles-fuse
%{_datadir}/ostree
%dir %{_libdir}/dracut/modules.d/98ostree
%{_libdir}/systemd/system/ostree*.service
%{_libdir}/systemd/system/ostree-finalize-staged.path
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
%{_prefix}/share/bash-completion/completions/ostree
%{_datadir}/gtk-doc/html/ostree
%{_datadir}/gir-1.0/OSTree-1.0.gir
%exclude %{_mandir}/man1/ostree-admin*
%{_mandir}/man1/*.gz
%{_mandir}/man5/*.gz

%files grub2
%{_sysconfdir}/grub.d/*ostree
%{_libexecdir}/libostree/grub2*

%changelog
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
