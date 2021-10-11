Summary:        Measures number of Terminal column cells of wide-character codes.
Name:           python-wcwidth
Version:        0.1.7
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/wcwidth
Source0:        https://files.pythonhosted.org/packages/source/w/wcwidth/wcwidth-%{version}.tar.gz
BuildArch:      noarch

%description
This Library is mainly for those implementing a Terminal Emulator, or programs that carefully produce output to be interpreted by one.

%package -n     python3-wcwidth
Summary:        python-wcwidth
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-wcwidth
This Library is mainly for those implementing a Terminal Emulator, or programs that carefully produce output to be interpreted by one.

%prep
%autosetup -n wcwidth-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-wcwidth
%defattr(-,root,root)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 0.1.7-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.1.7-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.1.7-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.1.7-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.1.7-1
- Initial packaging for Photon
