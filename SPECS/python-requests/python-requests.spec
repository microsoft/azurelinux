Summary:        Awesome Python HTTP Library That's Actually Usable
Name:           python-requests
Version:        2.22.0
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            http://python-requests.org
#Source0:       https://github.com/requests/requests/archive/v%{version}/requests-v%{version}.tar.gz
Source0:        requests-%{version}.tar.gz
Patch0:         test_requests_typeerror_testfix.patch
Patch1:         test_requests_support_pytest_4.patch

%description
Awesome Python HTTP Library That's Actually Usable

%package -n     python3-requests
Summary:        python-requests
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-certifi
Requires:       python3-chardet
Requires:       python3-idna
Requires:       python3-libs
Requires:       python3-pyOpenSSL
Requires:       python3-urllib3
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-certifi
BuildRequires:  python3-chardet
BuildRequires:  python3-idna
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-urllib3
%endif

%description -n python3-requests
Requests is an Apache2 Licensed HTTP library, written in Python, for human
beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most of
the HTTP capabilities you should need, but the api is thoroughly broken.
It requires an enormous amount of work (even method overrides) to
perform the simplest of tasks.

%prep
%autosetup -p 1 -n requests-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
LANG=en_US.UTF-8 tox -e py37

%files -n python3-requests
%defattr(-,root,root)
%license LICENSE
%doc README.md HISTORY.md
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 2.22.0-3
- Remove python2 package
- Lint spec

* Mon Mar 01 2021 Andrew Phelps <anphel@microsoft.com> - 2.22.0-2
- Add patches for test issues and run tests with tox

* Thu Dec 31 2020 Thomas Crain <thcrain@microsoft.com> - 2.22.0-1
- Upgrade to version 2.22.0
- Fix Source0 URL

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.20.0-4
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.20.0-3
- Renaming python-pytest to pytest

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.20.0-2
- Renaming python-pyOpenSSL to pyOpenSSL

* Thu Mar 19 2020 Paul Monson <paulmon@microsoft.com> - 2.20.0-1
- Update to 2.20.0. Fix source0 URL. Fix license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.19.1-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Mar 28 2019 Tapas Kundu <tkundu@vmware.com> - 2.19.1-4
- Fix for CVE-2018-18074

* Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> - 2.19.1-3
- Add %check

* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 2.19.1-2
- Add a few missing runtime dependencies (urllib3, chardet,
- pyOpenSSL, certifi, idna).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 2.19.1-1
- Update to version 2.19.1

* Mon Aug 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.13.0-3
- Disabled check section as tests are not available

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.13.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.13.0-1
- Updated to version 2.13.0.

* Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.9.1-4
- Added python3 package.

* Mon Oct 04 2016 ChangLee <changlee@vmware.com> - 2.9.1-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.9.1-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 2.9.1-1
- Updated to version 2.9.1

* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
