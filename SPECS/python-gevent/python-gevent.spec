Summary:        Coroutine-based network library
Name:           python-gevent
Version:        23.9.1
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://www.gevent.org
Source0:        https://github.com/gevent/gevent/archive/%{version}.tar.gz#/gevent-%{version}.tar.gz
Patch0:         CVE-2024-24806.patch
Patch1:         skip-irrelevant-tests.patch
Patch2:         CVE-2024-25629.patch

%description
gevent is a coroutine-based Python networking library.

%package -n     python3-gevent
Summary:        Coroutine-based network library
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
Requires:       python3
Requires:       python3-greenlet
Requires:       python3-zope-interface
Requires:       python3-zope-event
%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  lsof
BuildRequires:  openssl-devel
BuildRequires:  python3-test
BuildRequires:  python3-greenlet
BuildRequires:  python3-zope-interface
BuildRequires:  python3-zope-event
BuildRequires:  python3-requests
%endif

%description -n python3-gevent
gevent is a coroutine-based Python networking library.
Features include:
    Fast event loop based on libev.
    Lightweight execution units based on greenlet.
    Familiar API that re-uses concepts from the Python standard library.
    Cooperative sockets with SSL support.
    DNS queries performed through c-ares or a threadpool.
    Ability to use standard library and 3rd party modules written for standard blocking sockets

%prep
%autosetup -p 1 -n gevent-%{version}

%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-t}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files gevent

%check
# freeze packaging since we already have it available
pip3 install packaging==23.2 tox tox-current-env 
%tox

%files -n python3-gevent -f %{pyproject_files}
%defattr(-,root,root,-)
%license LICENSE

%changelog
* Mon Oct 14 2024 Sumedh Sharma <sumsharma@microsoft.com> - 23.9.1-4
- Add patch to resolve CVE-2024-25629

* Mon Jul 01 2024 Nick Samson <nisamson@microsoft.com> - 23.9.1-3
- Patch to address CVE-2024-24806
- Migrate tests to use tox
- Migrate to pyproject build

* Tue May 21 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 23.9.1-2
- Bump release to build with new libuv to fix CVE-2024-24806

* Mon Nov 27 2023 Tobias Brick <tobiasb@microsoft.com> - 23.9.1-1
- Update to 23.9.1

* Wed Oct 04 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.6-9
- Add patch for CVE-2023-41419

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 1.3.6-8
- Regenerate C sources at build-time to fix build break with Python 3.9

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.3.6-7
- Add license to python3 package
- Remove python2 package
- Make python byte compilation errors fatal again
- Lint spec

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.3.6-6
- Make python byte compilation errors non-fatal due to python2 errors.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.3.6-5
- Added %%license line automatically

* Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> - 1.3.6-4
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.3.6-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com>1.3.6-2
- Fix make check

* Wed Sep 12 2018 Tapas Kundu <tkundu@vmware.com> - 1.3.6-1
- Updated to version 1.3.6

* Wed Sep 20 2017 Bo Gan <ganb@vmware.com> - 1.2.1-6
- Fix build and make check issues

* Wed Sep 13 2017 Rongrong Qiu <rqiu@vmware.com> - 1.2.1-5
- Update make check for bug 1900401

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.2.1-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.2.1-3
- Removed erroneous line

* Tue May 16 2017 Rongrong Qiu <rqiu@vmware.com> - 1.2.1-2
- Add requires python-greenlet and python3-greenlet

* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.2.1-1
- Initial packaging for Photon
