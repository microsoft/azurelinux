Summary:        PyNaCl is a Python binding to libsodium
Name:           python-pynacl
Version:        1.3.0
Release:        8%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/pyca/pynacl
# The official source is under https://github.com/pyca/pynacl/archive/1.3.0.tar.gz.
# Source to be fixed as part of https://microsoft.visualstudio.com/OS/_workitems/edit/25936171.
Source0:        https://files.pythonhosted.org/packages/61/ab/2ac6dea8489fa713e2b4c6c5b549cc962dd4a842b5998d9e80cf8440b7cd/PyNaCl-%{version}.tar.gz
Patch1:         fix_import_unlimited_error.patch
Patch2:         fix_average_value_hypothesis_error.patch

%description
Good password hashing for your software and your servers.

%package -n     python3-pynacl
Summary:        PyNaCl is a Python binding to libsodium
BuildRequires:  python3-cffi
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-atomicwrites
# Need newer version. Use pip3 untils pkg upgrade
#BuildRequires:  python3-attrs
BuildRequires:  python3-hypothesis
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-wheel
%endif
Requires:       python3
Requires:       python3-libs

%description -n python3-pynacl
Good password hashing for your software and your servers.

%prep
%autosetup -n PyNaCl-%{version} -p1

%build
%py3_build

%install
%py3_install

%check
%{python3} -m pip install pluggy more-itertools sortedcontainers attrs
PYTHONPATH=%{buildroot}%{python3_sitelib} py.test3 -v

%files -n python3-pynacl
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Thu Mar 10 2022 Bala <balakumaran.kannan@microsoft.com> - 1.3.0-8
- BR necessary packages for PTest
- Patch test cases written with older verion libraries

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.3.0-7
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sun Dec 05 2020 Thomas Crain <thcrain@microsoft.com> - 1.3.0-6
- Enable package tests

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.3.0-5
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.3.0-4
- Renaming python-PyNaCl to python-pynacl

* Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.0-3
- Fixed 'Source0' and 'URL' tags.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.3.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 1.3.0-1
-   Initial packaging for Photon
