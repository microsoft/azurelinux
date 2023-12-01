Summary:        Code coverage measurement for Python.
Name:           python-coverage
Version:        6.3.2
Release:        4%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/coverage
Source0:        https://files.pythonhosted.org/packages/source/c/coverage/coverage-%{version}.tar.gz

%description
Code coverage measurement for Python.

%package -n     python3-coverage
Summary:        Code coverage measurement for Python.
BuildRequires:  python3-devel >= 3.7
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-six
BuildRequires:  git
%endif
Requires:       python3
Requires:       python3-xml

%description -n python3-coverage
Code coverage measurement for Python.
Coverage.py measures code coverage, typically during test execution. It uses the code analysis
tools and tracing hooks provided in the Python standard library to determine which lines are
executable, and which have been executed.

%prep
%autosetup -n coverage-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install 'tox>=3.27.1,<4.0.0' PyContracts
LANG=en_US.UTF-8 tox -e py%{python3_version_nodots}

%files -n python3-coverage
%defattr(-,root,root)
%license LICENSE.txt
%{python3_sitelib}/*
%{_bindir}/coverage
%{_bindir}/coverage3
%{_bindir}/coverage-%{python3_version}

%changelog
* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 6.3.2-4
- Update version of tox used for package tests

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 6.3.2-3
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Fri Feb 25 2022 Muhammad Falak <mwani@microsoft.com> - 6.3.2-2
- Add an explicit BR on `git` to enable ptest

* Tue Feb 22 2022 Nick Samson <nisamson@microsoft.com> - 6.3.2-1
- Updated to 6.3.2. Updated python constraint.
- Updated check section to reflect python 3.7 as min version.

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.5.1-6
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.5.1-5
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.5.1-4
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.5.1-3
- Renaming python-pytest to pytest

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.5.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sat Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 4.5.1-1
- Updated to 4.5.1

* Thu Aug 10 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.3.4-5
- Fixed make check errors

* Fri Jul 07 2017 Chang Lee <changlee@vmware.com> - 4.3.4-4
- Add python-xml and pyhton3-xml to  Requires.

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.3.4-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 4.3.4-2
- Packaging python2 and oython3 scripts in bin directory

* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.3.4-1
- Initial packaging for Photon
