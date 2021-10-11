Summary:        Python Atomic file writes
Name:           python-atomicwrites
Version:        1.2.1
Release:        6%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/untitaker/python-atomicwrites
#Source0:       https://github.com/untitaker/python-atomicwrites/archive/%{version}.tar.gz
Source0:        atomicwrites-%{version}.tar.gz
BuildArch:      noarch

%description
Python Atomic file writes

%package -n     python3-atomicwrites
Summary:        Python Atomic file writes
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-attrs
BuildRequires:  python3-pytest
BuildRequires:  python3-six
%endif

%description -n python3-atomicwrites
Python Atomic file writes

%prep
%autosetup -n atomicwrites-%{version}

%build
%py3_build

%install
%py3_install

%check
easy_install_3=$(ls %{_bindir} |grep easy_install |grep 3)
$easy_install_3 funcsigs pathlib2 pluggy more-itertools
cp tests/test_atomicwrites.py .
%python3 test_atomicwrites.py

%files -n python3-atomicwrites
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 1.2.1-6
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
