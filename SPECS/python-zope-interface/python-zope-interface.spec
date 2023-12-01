%define pypi_name zope.interface
Summary:        Interfaces for Python
Name:           python-zope-interface
Version:        5.4.0
Release:        1%{?dist}
License:        ZPLv2.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/zopefoundation/zope.interface
Source0:        https://pypi.python.org/packages/source/z/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
Interfaces for Python

%package -n     python3-zope-interface
Summary:        python3-zope-interface
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-zope-interface
This package is intended to be independently reusable in any Python project. It is maintained by the Zope Toolkit project.
This package provides an implementation of “object interfaces” for Python. Interfaces are a mechanism for labeling objects as conforming to a given API or contract. So, this package can be considered as implementation of the Design By Contract methodology support in Python.
For detailed documentation, please see http://docs.zope.org/zope.interface

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-zope-interface
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Fri Mar 25 2022 Andrew Phelps <anphel@microsoft.com> - 5.4.0-1
- Updated to version 5.4.0

* Sat Feb 12 2022 Muhammad Falak <mwani@microsoft.com> - 4.7.2-3
- Add an explicit BR on `pip` to enable ptest

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.7.2-2
- Add license to python3 package
- Remove python2 package

* Wed Nov 11 2020 Olivia Crain <oliviacrain@microsoft.com> - 4.7.2-1
- Update to 4.7.2 to fix setuptools compatibility issues
- Update Source0
- Lint to Mariner style

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.6.0-3
- Added %%license line automatically

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.6.0-2
- Renaming python-zope.interface to python-zope-interface

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 4.6.0-1
- Initial CBL-Mariner import from Photon (license: Apache2).
- Update to 4.6.0. Source0 URL fixed. License verified.

* Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> - 4.5.0-1
- Updated to release 4.5.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.3.3-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.3.3-1
- Updated to version 4.3.3.

* Mon Oct 04 2016 ChangLee <changlee@vmware.com> - 4.1.3-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.1.3-2
- GA - Bump release of all rpms

* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> - 4.1.3-1
- Initial packaging for Photon
