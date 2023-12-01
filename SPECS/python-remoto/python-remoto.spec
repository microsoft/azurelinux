%define pkgname remoto
Summary:        A very simplistic remote-command-executor
Name:           python-%{pkgname}
Version:        1.2.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/alfredodeza/remoto
Source0:        https://pypi.io/packages/source/r/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-execnet
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
A very simplistic remote-command-executor.

%package -n python3-%{pkgname}
Summary:        A very simplistic remote-command-executor
Requires:       python3
Requires:       python3-execnet

%description -n python3-%{pkgname}
A very simplistic remote-command-executor using connections to hosts (ssh, local, containers,
and several others are supported) and Python in the remote end. All the heavy lifting is done
by execnet, while this minimal API provides the bare minimum to handle easy logging and connections
from the remote end.

remoto is a bit opinionated as it was conceived to replace helpers and remote utilities for ceph-deploy,
a tool to run remote commands to configure and setup the distributed file system Ceph. ceph-medic uses
remoto as well to inspect Ceph clusters.

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest mock
python3 -m pytest -v remoto/tests

%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Wed Mar 30 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.2.1-1
- Upgrade to latest upstream version
- Pass check section with newer python environment
- Lint spec

* Wed Jun 23 2021 Neha Agarwal <nehaagarwal@microsoft.com> 1.2.0-2
- Pass check section

* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> 1.2.0-1
- Original version for CBL-Mariner
- License verified
