%define srcname geomet
%global with_tests 0

Name:           python-geomet
Version:        1.1.0
Release:        1%{?dist}
Summary:        GeoJSON <-> WKT/WKB conversion utilities
License:        Apache Software License
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://github.com/geomet/geomet

Source0: https://github.com/geomet/geomet/archive/refs/tags/%{version}.tar.gz#/python-%{srcname}-%{version}.tar.gz

BuildRequires: python3-devel
BuildRequires: python3-setuptools

%if 0%{?with_check}
BuildRequires: python3-pip
%endif

Requires: python3
Requires: python3-six
Requires: python3-click
Requires: python3-setuptools

BuildArch: noarch

%description
Convert GeoJSON to WKT/WKB (Well-Known Text/Binary), and vice versa.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_tests}
%check
# this doesn't exist in current source archive
# will help in future
bash build-scripts/02-test.sh
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Thu May 22 2025 Jyoti kanase <v-jykanase@microsoft.com> -  1.1.0-1
- Initial Azure Linux import from Photon (license: Apache2).
- Upgrade  to 1.1.0
- License verified.

* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.3.0-1
- Automatic Version Bump
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 0.1.2-1
- Initial packaging for Photon
