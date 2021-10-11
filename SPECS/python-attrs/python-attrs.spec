Summary:        Attributes without boilerplate.
Name:           python-attrs
Version:        18.2.0
Release:        8%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/attrs
Source0:        https://files.pythonhosted.org/packages/0f/9e/26b1d194aab960063b266170e53c39f73ea0d0d3f5ce23313e0ec8ee9bdf/attrs-%{version}.tar.gz
BuildArch:      noarch

%description
Attributes without boilerplate.

%package -n     python3-attrs
Summary:        Attributes without boilerplate.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-pip
BuildRequires:  python3-zope-interface
%endif
Requires:       python3

%description -n python3-attrs
Attributes without boilerplate.

%prep
%autosetup -n attrs-%{version}

%build
%py3_build

%install
%py3_install

%check
# Tests are only supported with Python3
pip3 install pytest hypothesis==4.38.0 tox
LANG=en_US.UTF-8 tox -e py37

%files -n python3-attrs
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 18.2.0-8
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue Jan 05 2021 Andrew Phelps <anphel@microsoft.com> - 18.2.0-7
- Use tox to run tests.

* Wed Jul 08 2020 Henry Beberman <henry.beberman@microsoft.com> - 18.2.0-6
- Fix typo in BuildRequires for python3-zope-interface

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 18.2.0-5
- Added %%license line automatically

* Fri Apr 24 2020 Nick Samson <nisamson@microsoft.com> - 18.2.0-4
- Updated Source0, license verified. Removed %%define sha1

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 18.2.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 13 2018 Tapas Kundu <tkundu@vmware.com> - 18.2.0-2
- Fixed the makecheck errors

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 18.2.0-1
- Update to version 18.2.0

* Thu Jul 06 2017 Chang Lee <changlee@vmware.com> - 16.3.0-3
- Updated %check

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 16.3.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 16.3.0-1
- Initial packaging for Photon
