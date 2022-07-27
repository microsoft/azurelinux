%global _description \
A modern, feature-rich and highly-tunable Python client libraryfor Apache Cassandra (2.1+) using exclusively Cassandra's binary protocol and Cassandra Query Language v3.

%global pypi_name cassandra-driver

Summary:        A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
Name:           python-%{pypi_name}
Version:        3.25.0
Release:        1%{?dist}
URL:            https://github.com/datastax/python-driver#datastax-python-driver-for-apache-cassandra
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/datastax/python-driver/archive/refs/tags/%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz

%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  libev-devel
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       libev
Requires:       python3
Requires:       python3-six
Requires:       python3-geomet < 0.3
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  iana-etc
BuildRequires:  openssl-devel
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-packaging
%endif

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -n python-driver-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} -m pip install -r test-requirements.txt
%{python3} setup.py gevent_nosetests
%{python3} setup.py eventlet_nosetests

%files -n python3-%{pypi_name}
%license LICENSE
%doc CHANGELOG.rst README.rst
%{python3_sitelib}/*

%changelog
* Wed Jun 22 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.25.0-1
- Initial CBL-Mariner import from Photon (license: Apache2)
- Bumping version to 3.25.0
- Adding as run dependency for package cassandra medusa.
- License verified
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
