Summary:        Python package for providing Mozilla's CA Bundle
Name:           python-certifi
Version:        2021.10.08
Release:        2%{?dist}
License:        MPL-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/certifi
#Source0:       https://github.com/certifi/python-certifi/archive/refs/tags/%{version}.tar.gz
Source0:        certifi-%{version}.tar.gz
BuildArch:      noarch

%description
Python package for providing Mozilla's CA Bundle

%package -n     python3-certifi
Summary:        Python package for providing Mozilla's CA Bundle
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description -n python3-certifi
Certifi is a carefully curated collection of
Root Certificates for validating the trustworthiness of
SSL certificates while verifying the identity of TLS hosts

%prep
%autosetup -n python-certifi-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest
%pytest

%files -n python3-certifi
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Sat Feb 12 2022 Muhammad Falak <mwani@microsoft.com> - 2021.10.08-2
- Add an explict BR on pip
- Drop un-needed dependencies
- Use `%pytest` to enable ptest

* Wed Feb 09 2022 Nick Samson <nisamson@microsoft.com> - 2021.10.08-1
- Updated URL, updated to 2021.10.08

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 2018.10.15-6
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue Oct 20 2020 Andrew Phelps <anphel@microsoft.com> - 2018.10.15-5
- Fix check test

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2018.10.15-4
- Added %%license line automatically

* Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2018.10.15-3
- Removing *Requires for "ca-certificates".

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 2018.10.15-2
- Renaming python-pytest to pytest

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 2018.10.15-1
- Update to 2018.10.15. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2018.08.24-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> - 2018.08.24-1
- Initial packaging
