Summary:        The Swiss Army knife of Python web development
Name:           python-werkzeug
Version:        2.3.7
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/pallets/werkzeug
Source0:        https://github.com/pallets/werkzeug/archive/%{version}.tar.gz#/werkzeug-%{version}.tar.gz
Patch0:         0001-enable-tests-in-rpm-env.patch
# Necessary because RPM build environment creates specific scenario that violates a core 
# assumption the testing infrastructure of werkzeug makes
Patch1:         0002-disable-stat-test.patch
Patch2:         CVE-2023-46136.patch
BuildArch:      noarch

%description
The Swiss Army knife of Python web development

%package -n     python3-werkzeug
Summary:        The Swiss Army knife of Python web development
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
Requires:       python3
Requires:       python3-markupsafe
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-requests
BuildRequires:  python3-markupsafe
%endif

%description -n python3-werkzeug
Werkzeug started as simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility modules. It includes a powerful debugger, full featured request and response objects, HTTP utilities to handle entity tags, cache control headers, HTTP dates, cookie handling, file uploads, a powerful URL routing system and a bunch of community contributed addon modules.

%prep
%autosetup -n werkzeug-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-t}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files werkzeug

%check
pip3 install tox==4.6.3 tox-current-env
pip3 install -r requirements/tests.txt
%tox

%files -n python3-werkzeug -f %{pyproject_files}
%defattr(-,root,root)
%doc README.rst
%doc CHANGES.rst
%license LICENSE.rst

%changelog
* Mon Nov 06 2023 Nick Samson <nisamson@microsoft.com> - 2.3.7-1
- Upgraded to version 2.3.7
- Migrated to pyproject build
- Added required MarkupSafe dependency
- Added patch for CVE-2023-46136

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
