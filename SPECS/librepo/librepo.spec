%define _unpackaged_files_terminate_build 0
Summary:        Repodata downloading library
Name:           librepo
Version:        1.15.1
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/rpm-software-management/librepo
#Source0:       https://github.com/rpm-software-management/librepo/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  attr-devel
BuildRequires:  check
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  python3-devel
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  gpgme-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  zchunk-devel
Requires:       curl-libs
Requires:       gpgme
Requires:       zchunk

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package devel
Summary:        Repodata downloading library
Requires:       %{name} = %{version}-%{release}
Requires:       curl-devel
Requires:       curl-libs

%description devel
Development files for librepo.

%prep
%autosetup -p1
mkdir build-py3

%build
pushd build-py3
%cmake -DPYTHON_DESIRED:FILEPATH=%{python3} -DENABLE_PYTHON_TESTS=%{!?with_pythontests:OFF} ..
%make_build
popd

%install
pushd build-py3
%make_install
popd

%check
pushd build-py3
%make_build test
popd

%ldconfig_scriptlets

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.0*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/
%{python3_sitearch}/%{name}/*

%changelog
* Mon Nov 20 2023 Sam Meluch <sammeluch@microsoft.com> - 1.15.1-2
- Bump release, move python requires

* Wed Jun 21 2023 Sam Meluch <sammeluch@microsoft.com> - 1.15.1-1
- Upgrade to version 1.15.1 for dnf5

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.14.2-2
- Remove unused python2 build requirements

* Tue Sep 14 2021 Thomas Crain <thcrain@microsoft.com> - 1.14.2-1
- Update to latest upstream version
- Lint spec

* Mon Jan 04 2021 Thomas Crain <thcrain@microsoft.com> - 1.11.0-4
- Enable package tests for both major python versions

* Tue Nov 10 2020 Thomas Crain <thcrain@microsoft.com> - 1.11.0-3
- Patch CVE-2020-14352
- Lint to Mariner style

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.11.0-2
- Added %%license line automatically

* Tue May 05 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.0-1
- Update version to 1.11.0.

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> - 1.10.3-1
- Update to version 1.10.3. License verified.

* Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> - 1.10.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> - 1.10.2-1
- Initial build. First version
