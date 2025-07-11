%define srcname cassandra-driver

Summary:        A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
Name:           %{srcname}
Version:        3.29.2
Release:        1%{?dist}
Url:            https://github.com/datastax/python-driver#datastax-python-driver-for-apache-cassandra
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/datastax/python-driver/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: libev-devel

Requires: libev
Requires: python3
Requires: python-geomet

%description
A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
using exclusively Cassandra's binary protocol and Cassandra Query Language v3. The driver
supports Python 3.8, 3.9, 3.10, 3.11 and 3.12.

%prep
%autosetup -p1 -n python-driver-%{version}

%build
%{python3} setup.py build --no-cython

%install
%{python3} setup.py install \
        --prefix=%{_prefix} --root=%{buildroot} --no-cython

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu May 22 2025 Jyoti kanase <v-jykanase@microsoft.com> - 3.29.2-1
- Initial Azure Linux import from Photon (license: Apache2).
- Upgrade to 3.29.2
- License verified.

* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 3.25.0-1
- Automatic Version Bump
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 3.24.0-4
- Fixed install time dependency
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.24.0-3
- Fix build with new rpm
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.24.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.24.0-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.15.1-3
- Mass removal python2
* Wed Dec 12 2018 Tapas Kundu <tkundu@vmware.com> 3.15.1-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.15.1-1
- Update to version 3.15.1
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 3.10.0-5
- Remove BuildArch
* Tue Sep 12 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.10.0-4
- Do make check for python3 subpackage
* Wed Aug 16 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10.0-3
- Fix make check.
* Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10.0-1
- Initial packaging for Photon
