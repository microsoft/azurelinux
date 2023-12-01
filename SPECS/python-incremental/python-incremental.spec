Summary:        Incremental is a small library that versions your Python projects.
Name:           python-incremental
Version:        21.3.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/incremental
Source0:        https://files.pythonhosted.org/packages/source/i/incremental/incremental-%{version}.tar.gz
BuildArch:      noarch

%description
Incremental is a small library that versions your Python projects.

%package -n     python3-incremental
Summary:        python-incremental
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-incremental
Incremental is a small library that versions your Python projects.

%prep
%autosetup -n incremental-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} setup.py test

%files -n python3-incremental
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Thu Feb 24 2022 Nick Samson <nisamson@microsoft.com> - 21.3.0-1
- Update to 21.3.0.

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 17.5.0-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 17.5.0-4
- Added %%license line automatically

* Fri Apr 24 2020 Andrew Phelps <anphel@microsoft.com> - 17.5.0-3
- Updated Source0. Remove sha1 definition. Verified license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 17.5.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 17.5.0-1
- Update to version 17.5.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 16.10.1-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> - 16.10.1-1
- Initial packaging for Photon.
