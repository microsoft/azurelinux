Summary:        XML bomb protection for Python stdlib modules
Name:           python-defusedxml
Version:        0.6.0
Release:        3%{?dist}
License:        Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/defusedxml
Source0:        https://files.pythonhosted.org/packages/a4/5f/f8aa58ca0cf01cbcee728abc9d88bfeb74e95e6cb4334cfd5bed5673ea77/defusedxml-%{version}.tar.gz
BuildArch:      noarch

%description
XML bomb protection for Python stdlib modules

%package -n     python3-defusedxml
Summary:        XML bomb protection for Python stdlib modules
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-xml

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
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 0.6.0-3
- Add license to python3 package
- Remove python2 package
- Lint spec

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
