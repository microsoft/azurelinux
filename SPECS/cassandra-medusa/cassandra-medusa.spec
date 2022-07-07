Name:           cassandra-medusa
Version:        0.13.2
Release:        1%{?dist}
Summary:        A apache cassandra backup system
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/thelastpickle/cassandra-medusa
Source0:        https://github.com/thelastpickle/cassandra-medusa/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  libevent-devel
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  sudo
%endif
Requires:       python3-dateutil
Requires:       python3-click
Requires:       python-click-aliases
Requires:       python3-PyYAML
Requires:       python3-cassandra-driver
Requires:       python3-psutil
Requires:       python-ffwd-client
Requires:       python-apache-libcloud
Requires:       python3-lockfile
Requires:       python3-cryptography
Requires:       python-pycryptodome
Requires:       python3-retrying
Requires:       python3-parallel-ssh
Requires:       python3-ssh2-python
Requires:       python3-ssh-python
Requires:       python3-requests
Requires:       python3-gevent
Requires:       python3-greenlet
Requires:       python3-fasteners
Requires:       python3-datadog
Requires:       python3-botocore
Requires:       python3-dns

%description
Cassandra Medusa is Apache Cassandra backup system.
It is a command line tool that offers the following features:
- Single node backup
- Single node restore
- Cluster wide in place restore (restoring on the same cluster that was used for the backup)
- Cluster wide remote restore (restoring on a different cluster than the one used for the backup)
- Backup purge
- Support for local storage, Google Cloud Storage (GCS) and AWS S3 through Apache Libcloud. Can be extended to support other storage providers supported by Apache Libcloud.
- Support for clusters using single tokens or vnodes
- Full or differential backups -n python3-fasteners

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/medusa
%{_bindir}/medusa-wrapper
%{_sysconfdir}/medusa/medusa-example.ini

%changelog
* Thu Jun 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.13.2-1
- Original first spec draft of medusa for CBL-Mariner(License: ASL 2.0).
- Adding dependencies based on sources 'requirements.txt'.
- Not adding K8 integration runtime packages for now.
- License Verified.
