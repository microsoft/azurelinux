Summary:        PyNaCl is a Python binding to libsodium
Name:           python-pynacl
Version:        1.5.0
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/pyca/pynacl
Source0:        https://github.com/pyca/pynacl/archive/refs/tags/%{version}.tar.gz#/pynacl-%{version}.tar.gz
BuildRequires:  libsodium-devel
BuildRequires:  python3-cffi
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
Good password hashing for your software and your servers.

%package -n     python3-pynacl
Summary:        PyNaCl is a Python binding to libsodium
Requires:       python3
Requires:       python3-cffi

%description -n python3-pynacl
Good password hashing for your software and your servers.

%prep
%autosetup -n pynacl-%{version}

%build
export SODIUM_INSTALL=system
%py3_build

%install
%py3_install

%check
pip3 install 'tox>=3.27.1,<4.0.0'
tox -e py%{python3_version_nodots}

%files -n python3-pynacl
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.5.0-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 1.5.0-2
- Update version of tox used for package tests

* Mon Mar 14 2022 Thomas Crain <thcrain@microsoft.com> - 1.5.0-1
- Upgrade to latest upstream version
- Use system libsodium instead of bundled version
- Switch source from PyPI to GitHub
- Use tox to run package tests
- Remove test patches meant for previous releases

 Thu Mar 10 2022 Bala <balakumaran.kannan@microsoft.com> - 1.3.0-8
- BR necessary packages for PTest
- Patch test cases written with older verion libraries

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.3.0-7
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sun Dec 05 2020 Thomas Crain <thcrain@microsoft.com> - 1.3.0-6
- Enable package tests

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.3.0-5
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.3.0-4
- Renaming python-PyNaCl to python-pynacl

* Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.0-3
- Fixed 'Source0' and 'URL' tags.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.3.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 1.3.0-1
- Initial packaging for Photon
