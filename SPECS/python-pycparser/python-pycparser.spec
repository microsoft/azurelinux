Summary:        Python C parser
Name:           python-pycparser
Version:        2.21
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/pycparser
Source0:        https://github.com/eliben/pycparser/archive/refs/tags/release_v%{version}.tar.gz#/pycparser-release_v%{version}.tar.gz
BuildRequires:  python3-devel
BuildArch:      noarch

%description
Python C parser

%package -n     python3-pycparser
Summary:        Python C parser
Requires:       python3

%description -n python3-pycparser
pycparser is a complete parser of the C language, written in pure Python using the PLY parsing library. It parses C code into an AST and can serve as a front-end for C compilers or analysis tools.

%prep
%autosetup -n pycparser-release_v%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 -m unittest discover

%files -n python3-pycparser
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Tue Mar 15 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.21-1
- Upgrade to latest upstream version
- Switch tests to be automatically discovered by the unittest module

* Thu Feb 10 2022 Muhammad Falak <mwani@microsoft.com> - 2.18-5
- Fix test path `tests/all_tests.py` instead of `all_tests.py` to enable ptest
- Drop unnecessary `pushd/popd`

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.18-4
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.18-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.18-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.18-1
- Update to version 2.18

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.17-3
- Use python2 instead of python

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.17-2
- Fix arch

* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.17-1
- Updated to version 2.17.

* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.14-4
- Added python3 site-packages.

* Mon Oct 04 2016 ChangLee <changlee@vmware.com> - 0.14-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.14-2
- GA - Bump release of all rpms

* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> - 0.14-1
- Initial packaging for Photon
