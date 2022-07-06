Summary:        A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
Name:           python3-cassandra-driver
Version:        3.24.0
Release:        5%{?dist}
Url:            https://github.com/datastax/python-driver#datastax-python-driver-for-apache-cassandra
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/datastax/python-driver/archive/refs/tags/%{version}.tar.gz#/cassandra-driver-%{version}.tar.gz
BuildRequires:  python3
BuildRequires:  python3-Cython
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  libev-devel
BuildRequires:  libev
%if %{with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-packaging
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  iana-etc
%endif
Requires:       libev
Requires:       python3
Requires:       python3-libs
Requires:       python3-six
Requires:       python3-geomet < 0.3

%description
A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
using exclusively Cassandra's binary protocol and Cassandra Query Language v3. The driver
supports Python 2.7, 3.3, 3.4, 3.5, and 3.6.

%prep
%autosetup -n python-driver-%{version}

%build
%{py3_build "--no-cython"}

%install
%py3_install

%check
pip3 install nose scales mock ccm unittest2 pytz sure pure-sasl twisted gevent eventlet packaging Netbase
%python3 setup.py gevent_nosetests
%python3 setup.py eventlet_nosetests

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Jun 22 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.24.0-5
-   Initial CBL-D Mariner import from PhotonOs (License: ASL 2.0)
-   Adding as run dependency for package cassandra medusa needed by cosmosDb.
-   Use pip to download dependencies for %check section instead of easy_install.
-   License Verified
*   Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 3.24.0-4
-   Fixed install time dependency
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.24.0-3
-   Fix build with new rpm
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.24.0-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.24.0-1
-   Automatic Version Bump
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.15.1-3
-   Mass removal python2
*   Wed Dec 12 2018 Tapas Kundu <tkundu@vmware.com> 3.15.1-2
-   Fix make check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.15.1-1
-   Update to version 3.15.1
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 3.10.0-5
-   Remove BuildArch
*   Tue Sep 12 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.10.0-4
-   Do make check for python3 subpackage
*   Wed Aug 16 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10.0-3
-   Fix make check.
*   Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10.0-1
-   Initial packaging for Photon
