Summary:        Python Atomic file writes
Name:           python-atomicwrites
Version:        1.4.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/untitaker/python-atomicwrites
Source0:        https://github.com/untitaker/python-atomicwrites/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
Python Atomic file writes

%package -n     python3-atomicwrites
Summary:        Python Atomic file writes
Requires:       python3

%description -n python3-atomicwrites
Python Atomic file writes

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest
PYTHONPATH=%{buildroot}%{python3_sitelib} %python3 tests/test_atomicwrites.py

%files -n python3-atomicwrites
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Wed Mar 30 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.4.0-1
- Upgrade to latest upstream version
- Simplify dependencies and self-test invocations

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.2.1-7
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.2.1-6
- Remove python2 package
- Lint spec

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.2.1-5
- Renaming python-pytest to pytest

* Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> - 1.2.1-4
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.2.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Nov 12 2018 Tapas Kundu <tkundu@vmware.com> - 1.2.1-2
- Fixed make check

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 1.2.1-1
- Update to version 1.2.1

* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> - 1.1.5-2
- Fixed rpm check errors

* Fri Jul 07 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.1.5-1
- Initial packaging for Photon
