%global srcname werkzeug
%global modname werkzeug

Summary:        The Swiss Army knife of Python web development
Name:           python-werkzeug
Version:        3.0.1
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://github.com/pallets/werkzeug
Source0:        https://github.com/pallets/werkzeug/archive/%{version}.tar.gz#/werkzeug-%{version}.tar.gz
# Fixes PYTHONPATH handling in tests
# Upstream: https://github.com/pallets/werkzeug/pull/2172
Patch0:         preserve-any-existing-PYTHONPATH-in-tests.patch
BuildArch:      noarch

%description
The Swiss Army knife of Python web development

%package -n     python3-werkzeug
Summary:        The Swiss Army knife of Python web development
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip
Requires:       python3
%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-requests
%endif

%description -n python3-werkzeug
Werkzeug started as simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility modules. It includes a powerful debugger, full featured request and response objects, HTTP utilities to handle entity tags, cache control headers, HTTP dates, cookie handling, file uploads, a powerful URL routing system and a bunch of community contributed addon modules.

%package -n python3-werkzeug-doc
Summary:        Documentation for python3-werkzeug
Requires:       python3-werkzeug = %{version}-%{release}
 
%description -n python3-werkzeug-doc
Documentation and examples for python3-werkzeug.

%generate_buildrequires
%if 0%{?with_check}
# -t picks test.txt by default which contains too tight pins
%pyproject_buildrequires requirements/tests.in requirements/docs.in
%else
%pyproject_buildrequires -r requirements/docs.in
%endif

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{modname}

%check
pip3 install --ignore-installed -r requirements/tests.txt
pip3 install markupsafe
%py3_check_import %{modname}
%if 0%{?with_check}
# deselect the test_exclude_patterns test case as it's failing
# when we set PYTHONPATH: https://github.com/pallets/werkzeug/issues/2404
%pytest -Wdefault --deselect tests/test_serving.py::test_exclude_patterns
%endif

%files -n python3-%{modname} -f %{pyproject_files}
%license LICENSE.rst
%doc CHANGES.rst README.rst
%files -n python3-werkzeug-doc

%changelog
* Thu Apr 04 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.1-1
- Auto-upgrade to 3.0.1 - 3.0 package upgrade
- Import build, install and check section from Fedora 40 (license: MIT).

* Tue Mar 14 2023 Rakshaa Viswanathan <rviswanathan@microsoft.com> - 2.2.3-1
- Updated to version 2.2.3 for CVE-2023-23934 adn CVE-2023-25577
- Remove patch for CVE-2023-25577

* Fri Feb 24 2023 Minghe Ren <mingheren@microsoft.com> - 2.0.3-2
- Add patch for CVE-2023-25577

* Fri Mar 25 2022 Andrew Phelps <anphel@microsoft.com> - 2.0.3-1
- Updated to version 2.0.3
- Switch to github source and URL

* Mon Dec 27 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.0.1-1
- Updated to version 1.0.1

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.14.1-7
- Add license to python3 package
- Remove python2 package, switch check section to python3
- Lint spec

* Wed Mar 03 2021 Andrew Phelps <anphel@microsoft.com> - 0.14.1-6
- Remove test_cache.py tests. Use tox for tests.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.14.1-5
- Added %%license line automatically

* Tue Apr 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.1-4
- Fixed "Source0" tag.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.14.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> - 0.14.1-2
- Fix make check
- Moved buildrequires from subpackage

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.14.1-1
- Update to version 0.14.1

* Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> - 0.12.1-2
- Fixed rpm check errors

* Thu Mar 30 2017 Siju Maliakkal <smaliakkal@vmware.com> - 0.12.1-1
- Updating package to latest

* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.11.15-1
- Initial packaging for Photon.
