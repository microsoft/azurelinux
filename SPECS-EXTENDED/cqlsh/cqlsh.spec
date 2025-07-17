%define srcname cqlsh

Summary:        A Python-based command-line client for running simple CQL commands on a Cassandra cluster.
Name:           %{srcname}
Version:        6.1.2
Release:        2%{?dist}
License:        Apache License Version 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Url:            https://pypi.python.org/pypi/cqlsh

Source0: https://files.pythonhosted.org/packages/source/c/cqlsh/%{srcname}-%{version}.tar.gz

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3
Requires: python3-six
Requires: cassandra
Requires: cassandra-driver

BuildArch: noarch

%description
cqlsh is a Python-based command-line tool, and the most direct way to run simple CQL commonds on a Cassandra cluster.
This is a simple re-bundling of the open source tool that comes bundled with Cassandra to allow for cqlsh to be installed and run inside of virtual environments..

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root)
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Thu May 22 2025 Jyoti kanase <v-jykanase@microsoft.com> - 6.1.2-2
- Initial Azure Linux import from Photon (license: Apache2).
- License verified.

* Sat Aug 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.2-1
- Upgrade to v6.1.2
- Remove python3-cql dependency
* Tue Feb 21 2023 Ankit Jain <ankitja@vmware.com> 6.1.0-1
- Update to 6.1.0
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 6.0.0-1
- Automatic Version Bump
* Thu Nov 11 2021 Shreenidhi Shedi <sshedi@vmware.com> 6.0.0ga-1
- Update to 6.0.0
* Wed Jun 09 2021 Ankit Jain <ankitja@vmware.com> 6.0.0b4-1
- Update to 6.0.0b4 to support python3
* Mon Jul 10 2017 Xiaolin Li <xiaolinl@vmware.com> 5.0.4-1
- Initial packaging for Photon
