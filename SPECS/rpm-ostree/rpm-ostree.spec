Summary:        Commit RPMs to an OSTree repository
Name:           rpm-ostree
Version:        2022.1
Release:        6%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/coreos/rpm-ostree
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz
Patch0:         rpm-ostree-libdnf-build.patch
Patch1:         rpm-ostree-disable-selinux.patch
Patch2:         CVE-2022-31394.patch
Patch3:         rpm-ostree-drop-lint-which-treats-warning-as-error.patch
Patch4:         CVE-2022-47085.patch
BuildRequires:  attr-devel
BuildRequires:  autoconf
BuildRequires:  autogen
BuildRequires:  automake
BuildRequires:  bubblewrap
BuildRequires:  check
BuildRequires:  cmake
BuildRequires:  cppunit-devel
BuildRequires:  createrepo_c
BuildRequires:  dbus-devel
BuildRequires:  docbook-style-xsl
BuildRequires:  git
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-gobject-introspection
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
BuildRequires:  azurelinux-release
BuildRequires:  mariner-repos
BuildRequires:  openssl-devel
BuildRequires:  ostree-devel
BuildRequires:  polkit-devel
BuildRequires:  popt-devel
BuildRequires:  python3-devel
BuildRequires:  python3-pygments
BuildRequires:  rpm-devel
BuildRequires:  rust
BuildRequires:  sqlite-devel
BuildRequires:  systemd-devel
BuildRequires:  which

%if %{with_check}
BuildRequires:  python3-gobject
%endif

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
%autosetup -p1

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
# Fixing tests:
# 1. Switching tests to use Python 3, since CBL-Mariner doesn't support pygobject for Python 2.
# 2. Using the 'uname -m' command instead of unsupported 'arch'.
# 3. Disabling 'ucontainer' tests. Upstream removes them in never versions along with the feature
#    related to the test as it is considered not ready: https://github.com/coreos/rpm-ostree/pull/2344.
sed -i 's|/usr/bin/python2|%{_bindir}/python3|g' tests/check/test-lib-introspection.sh
sed -i 's|$(arch)|$(uname -m)|g' tests/check/test-lib-introspection.sh
sed -i '/test-ucontainer.sh/d' Makefile-tests.am

make check

%files
%license LICENSE
%{_bindir}/*
%{_libdir}/%{name}/
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/dbus-1/system.d/*
%{_unitdir}/*.service
%{_libexecdir}/*
%{_datadir}/dbus-1/system-services/*
%config(noreplace) %{_sysconfdir}/rpm-ostreed.conf
%{_libdir}/systemd/system/rpm-ostreed-automatic.timer
%{_libdir}/systemd/system/rpm-ostree-countme.timer
%{_datadir}/bash-completion/completions/rpm-ostree
%{_datadir}/dbus-1/interfaces/org.projectatomic.rpmostree1.xml
%{_datadir}/polkit-1/actions/org.projectatomic.rpmostree1.policy
%{_mandir}/man1/rpm-ostree.1.gz
%{_mandir}/man5/rpm-ostreed*
%{_mandir}/man8/rpm-ostreed*
%{_mandir}/man8/rpm-ostree-countme*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*
%{_datadir}/gir-1.0/*-1.0.gir

%changelog
* Thu Sep 07 2023 Daniel McIlvaney <damcilva@microsoft.com> - 2022.1-6
- Bump package to rebuild with rust 1.72.0

* Tue Aug 01 2023 Sumedh Sharma <sumsharma@microsoft.com> - 2022.1-5
- Apply patch for CVE-2022-47085

* Mon Mar 20 2023 Muhammad Falak <mwani@microsoft.com> - 2022.1-4
- Drop a lint which treats a warning as error to enable build with rust 1.68.0

* Thu Mar 09 2023 Nan Liu <liunan@microsoft.com> - 2022.1-3
- Apply patch for CVE-2022-31394

* Wed Aug 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 2022.1-2
- Bump package to rebuild with stable Rust compiler
- Add missing dependency on python3-pygments (needed to build docs)

* Thu Jan 27 2022 Henry Li <lihl@microsoft.com> - 2022.1-1
- Upgrade to version 2022.1
- Remove patches that no longer apply
- Fix rpm-ostree-disable-selinux.patch
- Add new files to main package due to the version upgrade

* Mon Nov 29 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 2020.4-3
- Fix build issue due to gcc 11.2

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 2020.4-2
- Remove unused gobject-introspection-python requirement
- Explicity specify python3-gobject-introspection requirement

* Mon Sep 27 2021 Thomas Crain <thcrain@microsoft.com> - 2020.4-1
- Upgrade version and rebase patches
- Move all dbus files to reside under %%{_datadir}
- License verified

* Tue Apr 27 2021 Thomas Crain <thcrain@microsoft.com> - 2019.3-9
- Merge the following releases from dev to 1.0 spec
- v-ruyche@microsoft.com, 2019.3-7: Systemd supports merged /usr. Update unit file directory macro.

* Tue Apr 20 2021 Thomas Crain <thcrain@microsoft.com> - 2019.3-8
- Bump release to rebuild with rust 1.47.0-2 (security update)

* Tue Dec 08 2020 Pawel Wingrodzki <pawelwi@microsoft.com> - 2019.3-7
- Fixing 'lib-introspection' test.
- Skipping 'ucontainer' test.
- Removing 'sha1' macros.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2019.3-6
- Added %%license line automatically

* Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> - 2019.3-5
- Renaming docbook-xsl to docbook-style-xsl

* Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> - 2019.3-4
- Replace BuildArch with ExclusiveArch

* Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> - 2019.3-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 20 2019 Ankit Jain <ankitja@vmware.com> - 2019.3-2
- Added script to create repo data to act as ostree-server

* Tue May 14 2019 Ankit Jain <ankitja@vmware.com> - 2019.3-1
- Initial version of rpm-ostree
