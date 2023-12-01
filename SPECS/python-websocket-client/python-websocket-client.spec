Summary:        WebSocket client for python
Name:           python-websocket-client
Version:        1.3.1
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/websocket-client
Source0:        https://github.com/websocket-client/websocket-client/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
WebSocket client for python

%package -n     python3-websocket-client
Summary:        WebSocket client for python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-coverage
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-six
%endif

%description -n python3-websocket-client
WebSocket client for python3

%prep
%autosetup -n websocket-client-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install \
    more-itertools \
    pluggy
# do not execute 'echo-server' test since it requires python websockets
# which do not work well from a chroot
pytest3 -vv websocket/tests -k "not echo-server"

%files -n python3-websocket-client
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/wsdump

%changelog
* Fri Mar 25 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.3.1-1
- Upgrade to 1.3.1

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.56.0-3
- Add license, wsdump.py binary to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.56.0-2
- Added %%license line automatically

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 0.56.0-1
- Initial CBL-Mariner import from Photon (license: Apache2).
- Update to 0.56.0. Update Vendor and Distribution. Source0 URL Fixed. License fixed.

* Fri Dec 07 2018 Ashwin H <ashwinh@vmware.com> - 0.53.0-2
- Add %check

* Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> - 0.53.0-1
- Updated to release 0.53.0

* Thu Nov 30 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.44.0-1
- Update websocket_client to version 0.44.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 0.7.0-1
- Initial version of python WebSocket for PhotonOS.
