Summary:        Commit RPMs to an OSTree repository
Name:           rpm-ostree
Version:        2019.3
Release:        7%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/projectatomic/rpm-ostree
Source0:        https://github.com/projectatomic/rpm-ostree/releases/download/v%{version}/rpm-ostree-%{version}.tar.xz
Source1:        libglnx-470af87.tar.gz
Source2:        libdnf-d8e481b.tar.gz
Patch0:         rpm-ostree-libdnf-build.patch
Patch1:         rpm-ostree-disable-selinux.patch
BuildRequires:  attr-devel
BuildRequires:  autoconf
BuildRequires:  autogen
BuildRequires:  automake
BuildRequires:  bubblewrap
BuildRequires:  check
BuildRequires:  cmake
BuildRequires:  cppunit-devel
BuildRequires:  createrepo_c
BuildRequires:  dbus
BuildRequires:  docbook-style-xsl
BuildRequires:  git
BuildRequires:  gobject-introspection-devel
BuildRequires:  gobject-introspection-python
BuildRequires:  gperf
BuildRequires:  gpgme-devel
BuildRequires:  gtk-doc
BuildRequires:  jq
BuildRequires:  json-c-devel
BuildRequires:  json-glib-devel
BuildRequires:  libarchive-devel
BuildRequires:  libcap-devel
BuildRequires:  libgsystem-devel
BuildRequires:  libmodulemd-devel
BuildRequires:  librepo-devel
BuildRequires:  libsolv
BuildRequires:  libsolv-devel
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  mariner-release
BuildRequires:  mariner-repos
BuildRequires:  openssl-devel
BuildRequires:  ostree-devel
BuildRequires:  polkit-devel
BuildRequires:  popt-devel
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  rpm-devel
BuildRequires:  rust
BuildRequires:  sqlite-devel
BuildRequires:  systemd-devel
BuildRequires:  which
Requires:       bubblewrap
Requires:       json-c
Requires:       json-glib
Requires:       libcap
Requires:       libgsystem
Requires:       libmodulemd
Requires:       librepo
Requires:       libsolv
Requires:       openssl
Requires:       ostree
Requires:       ostree-grub2
Requires:       ostree-libs
Requires:       polkit
ExclusiveArch:  x86_64

%description
This tool takes a set of packages, and commits them to an OSTree
repository.  At the moment, it is intended for use on build servers.

%package devel
Summary:        Development headers for rpm-ostree
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Includes the header files for the rpm-ostree library.

%package host
Summary:        File for rpm-ostree-host creation
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description host
Includes the scripts for rpm-ostree host creation

%package repo
Summary:        File for Repo Creation to act as server
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description repo
Includes the scripts for rpm-ostree repo creation to act as server

%prep
%setup -q
tar xf %{SOURCE1} --no-same-owner
tar xf %{SOURCE2} --no-same-owner
%patch0
%patch1

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules --enable-gtk-doc
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p -c"
find %{buildroot} -type f -name "*.la" -delete -print
install -d %{buildroot}%{_bindir}/rpm-ostree-host
install -d %{buildroot}%{_bindir}/rpm-ostree-server

%check
make check

%files
%license LICENSE
%{_bindir}/*
%{_libdir}/%{name}/
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/*.typelib
%{_sysconfdir}/dbus-1/system.d/*
%{_unitdir}/*.service
%{_libexecdir}/*
%{_datadir}/dbus-1/system-services/*
%config(noreplace) %{_sysconfdir}/rpm-ostreed.conf
%{_libdir}/systemd/system/rpm-ostreed-automatic.timer
%{_datadir}/bash-completion/completions/rpm-ostree
%{_datadir}/dbus-1/interfaces/org.projectatomic.rpmostree1.xml
%{_datadir}/polkit-1/actions/org.projectatomic.rpmostree1.policy
%{_mandir}/man1/rpm-ostree.1.gz
%{_mandir}/man5/rpm-ostreed*
%{_mandir}/man8/rpm-ostreed*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*
%{_datadir}/gir-1.0/*-1.0.gir

%changelog
* Wed Nov 04 2020 Ruying Chen <v-ruyche@microsoft.com> - 2019.3-7
- Systemd supports merged /usr. Update unit file directory macro.

* Sat May 09 00:20:55 PST 2020 Nick Samson <nisamson@microsoft.com> - 2019.3-6
- Added %%license line automatically

*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 2019.3-5
-   Renaming docbook-xsl to docbook-style-xsl

*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 2019.3-4
-   Replace BuildArch with ExclusiveArch

*   Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> 2019.3-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Fri Sep 20 2019 Ankit Jain <ankitja@vmware.com> 2019.3-2
-   Added script to create repo data to act as ostree-server

*   Tue May 14 2019 Ankit Jain <ankitja@vmware.com> 2019.3-1
-   Initial version of rpm-ostree
