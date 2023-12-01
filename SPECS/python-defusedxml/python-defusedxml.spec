Summary:        XML bomb protection for Python stdlib modules
Name:           python-defusedxml
Version:        0.7.1
Release:        1%{?dist}
License:        Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/defusedxml
Source0:        https://github.com/tiran/defusedxml/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildArch:      noarch

%description
XML bomb protection for Python stdlib modules

%package -n     python3-defusedxml
Summary:        XML bomb protection for Python stdlib modules
Requires:       python3

%description -n python3-defusedxml
XML bomb protection for Python stdlib modules

%prep
%autosetup -n defusedxml-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-defusedxml
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Mon Mar 14 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.7.1-1
- Upgrade to latest upstream version
- Switch source from PyPI to GitHub

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.6.0-3
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.6.0-2
- Added %%license line automatically

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 0.6.0-1
- Update to 0.6.0. License fixed.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.5.0-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Aug 01 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.5.0-3
- Added python-xml to requires of python-defusedxml.
- Added python3-xml to requires of python3-defusedxml.

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.5.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Mar 09 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.5.0-1
- Initial packaging for Photon
