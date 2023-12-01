Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
Name:           python-iniparse
Version:        0.5
Release:        1%{?dist}
License:        MIT OR Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/candlepin/python-iniparse
Source0:        https://files.pythonhosted.org/packages/4c/9a/02beaf11fc9ea7829d3a9041536934cd03990e09c359724f99ee6bd2b41b/iniparse-%{version}.tar.gz 
BuildArch:      noarch

%description
Python Module for Accessing and Modifying Configuration Data in INI files

%package -n     python3-iniparse
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
BuildRequires:  python3-devel
BuildRequires:  python3-six
BuildRequires:  python3-test
Requires:       python3
Requires:       python3-pycparser
Requires:       python3-six

%description -n python3-iniparse
iniparse is an INI parser for Python which is API compatible
with the standard library's ConfigParser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.

%prep
%autosetup -p 1 -n iniparse-%{version}

%build
%py3_build

%install
%py3_install
# fixes
chmod 644 %{buildroot}%{_docdir}/iniparse-%{version}/index.html
mv %{buildroot}%{_docdir}/iniparse-%{version} %{buildroot}%{_docdir}/%{name}-%{version}

%check
%{python3} runtests.py

%files -n python3-iniparse
%defattr(-,root,root,-)
%license LICENSE
%doc %{_docdir}/python-iniparse-%{version}/*
%{python3_sitelib}/*

%changelog
* Thu Mar 03 2022 Nick Samson <nisamson@microsoft.com> - 0.5-1
- Updated to 0.5
- Removed unnecessary compatibility patch
- Updated URL

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.4-10
- Add license, docs to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.4-9
- Added %%license line automatically

* Tue Apr 14 2020 Nick Samson <nisamson@microsoft.com> - 0.4-8
- Updated Source0, URL, license info. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.4-7
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jul 11 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.4-6
- Fix python3 and make check issues.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.4-5
- Use python2 explicitly to build

* Mon May 22 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.4-4
- Added python3 subpackage.

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> - 0.4-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.4-2
- GA - Bump release of all rpms

* Sat Jun 12 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.4-1
- Release 0.4

* Sat Apr 17 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.2-1
- Release 0.3.2

* Mon Mar 2 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.1-1
- Release 0.3.1

* Fri Feb 27 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.0-1
- Release 0.3.0

* Tue Dec 6 2008 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.4-1
- Release 0.2.4
- added egg-info file to %%files

* Tue Dec 11 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.3-1
- Release 0.2.3

* Tue Sep 24 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.2-1
- Release 0.2.2

* Tue Aug 7 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.1-1
- Release 0.2.1

* Fri Jul 27 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-3
- relocated doc to %{_docdir}/python-iniparse-%{version}

* Thu Jul 26 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-2
- changed name from iniparse to python-iniparse

* Tue Jul 17 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-1
- Release 0.2
- Added html/* to %%doc

* Fri Jul 13 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.1-1
- Initial build.
