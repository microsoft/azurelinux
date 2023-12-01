Summary:        WebOb provides objects for HTTP requests and responses.
Name:           python-webob
Version:        1.8.7
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/WebOb
Source0:        https://github.com/Pylons/webob/archive/refs/tags/%{version}.tar.gz#/webob-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pytest
%endif
BuildArch:      noarch

%description
WebOb provides objects for HTTP requests and responses.

%package -n     python3-webob
Summary:        WebOb provides objects for HTTP requests and responses.
Requires:       python3


%description -n python3-webob
WebOb provides objects for HTTP requests and responses. Specifically it does this by wrapping the WSGI request environment and response status/headers/app_iter(body).
The request and response objects provide many conveniences for parsing HTTP request and forming HTTP responses. Both objects are read/write: as a result, WebOb is also a nice way to create HTTP requests and parse HTTP responses.

%prep
%autosetup -n webob-%{version}
rm -f tests/performance_test.py

%build
%py3_build

%install
%py3_install

%check
%{python3} setup.py test

%files -n python3-webob
%defattr(-,root,root,-)
%license docs/license.txt
%{python3_sitelib}/*

%changelog
* Mon Feb 07 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.7-1
- Upgrade to latest upstream version
- Use github source tarball

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.8.5-4
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.8.5-3
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.8.5-2
- Renaming python-pytest to pytest

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.8.5-1
- Update to 1.8.5. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.8.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 1.8.2-1
- Update to version 1.8.2

* Mon Aug 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.7.2-3
- Fixed make check errors

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.7.2-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Mar 30 2017 Siju Maliakkal <smaliakkal@vmware.com> - 1.7.2-1
- Updating package to 1.7.2-1

* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.7.1-1
- Initial packaging for Photon
