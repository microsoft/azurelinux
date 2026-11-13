%global debug_package %{nil}
Summary:        MessagePack (de)serializer.
Name:           python-msgpack
Version:        1.2.3
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://msgpack.org/
# PyPI sdist ships the pre-generated msgpack/_cmsgpack.c; the .pyx sources need Cython >= 3.1.
Source0:        https://files.pythonhosted.org/packages/source/m/msgpack/msgpack-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif

%description
MessagePack (de)serializer.

%package -n     python3-msgpack
Summary:        MessagePack (de)serializer.
Requires:       python3

%description -n python3-msgpack
MessagePack is a fast, compact binary serialization format, suitable for similar data to JSON. This package provides CPython bindings for reading and writing MessagePack data.

%prep
%autosetup -p1 -n msgpack-%{version}
# setuptools < 77 does not support PEP 639 SPDX license strings.
sed -i 's/^license = "Apache-2.0"$/license = {text = "Apache-2.0"}/' pyproject.toml
grep -q '^license = {text = "Apache-2.0"}$' pyproject.toml

%build
%py3_build

%install
%py3_install

%check
%pytest

%files -n python3-msgpack
%defattr(-,root,root)
%license COPYING
%{python3_sitelib}/*

%changelog
* Tue Oct 27 2026 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.3-1
- Auto-upgrade to 1.2.3 - for CVE-2026-114613
- Build from the PyPI sdist, which ships the Cython-generated C sources
- Use the table form of project.license for compatibility with setuptools 69
- Drop unused python3-Cython BuildRequires

* Fri Jul 03 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.0.5-3
- Patch for CVE-2026-57585

* Tue Apr 29 2025 Riken Maharjan <rmaharjan@microsoft.com> -  1.0.5-2
- Use pytest instead of tox to fix the ptest

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.5-1
- Auto-upgrade to 1.0.5 - Azure Linux 3.0 - package upgrades

* Thu Apr 07 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.0.3-1
- Upgrade to latest upstream version
- Use tox as test runner

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.6.2-3
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.6.2-2
- Added %%license line automatically

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> - 0.6.2-1
- Update to version 0.6.2.  License verified. Source0 fixed.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.5.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.5.6-1
- Update to version 0.5.6

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.4.8-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu May 25 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.4.8-1
- Initial version
