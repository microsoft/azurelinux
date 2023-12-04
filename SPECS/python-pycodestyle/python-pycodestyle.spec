Summary:        Simple Python style checker in one Python file
Name:           python-pycodestyle
Version:        2.11.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.org/project/pycodestyle/
Source0:        https://github.com/PyCQA/pycodestyle/archive/refs/tags/%{version}.tar.gz#/pycodestyle-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

%package -n     python3-pycodestyle
Summary:        Simple Python style checker in one Python file
Requires:       python3

%description -n python3-pycodestyle
pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

%prep
%autosetup -n pycodestyle-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
tox -e py%{python3_version_nodots}

%files -n python3-pycodestyle
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/pycodestyle

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.11.0-1
- Auto-upgrade to 2.11.0 - Azure Linux 3.0 - package upgrades

* Tue Mar 15 2022 Thomas Crain <thcrain@microsoft.com> - 2.8.0-1
- Upgrade to latest upstream release
- Switch source from PyPI to GitHub
- Switch package test to use tox as a test runner
- License verified

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 2.5.0-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.5.0-4
- Added %%license line automatically

* Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> - 2.5.0-3
- Add #Source0. License verified.

* Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> - 2.5.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> - 2.5.0-1
- Initial packaging for Photon
