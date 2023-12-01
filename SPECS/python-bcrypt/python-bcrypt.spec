Summary:        Good password hashing for your software and your servers.
Name:           python-bcrypt
Version:        3.2.0
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/pyca/bcrypt/
Source0:        https://pypi.io/packages/source/b/bcrypt/bcrypt-%{version}.tar.gz
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
Good password hashing for your software and your servers.

%package -n     python3-bcrypt
Summary:        Good password hashing for your software and your servers.
BuildRequires:  python3-cffi
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-bcrypt
Good password hashing for your software and your servers.

%prep
%autosetup -n bcrypt-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} setup.py test

%files -n python3-bcrypt
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.2.0-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Feb 10 2022 Muhammad Falak <mwani@microsoft.com> - 3.2.0-2
- Add an explicit BR on 'pip' to enable ptest

* Fri Feb 04 2022 Nick Samson <nisamson@microsoft.com> - 3.2.0-1
- Upgraded to 3.2.0

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.1.6-6
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue Jan 05 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.1.6-5
- Switch to package testing with python3
- Fix Source0 URL

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.1.6-4
- Added %%license line automatically

* Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> - 3.1.6-3
- Verified License. Fixed Source0 link. Fixed URL. Removed sha1.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.1.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> - 3.1.6-1
- Initial packaging for Photon
