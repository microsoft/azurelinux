%define LICENSE_PATH LICENSE.PTR
Summary:        Python Lex & Yacc
Name:           python-ply
Version:        3.11
Release:        8%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://www.dabeaz.com/ply/
#Source0:       http://www.dabeaz.com/ply/ply-%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/e5/69/882ee5c9d017149285cab114ebeab373308ef0f874fcdac9beb90e0ac4da/ply-%{version}.tar.gz
Source1:        LICENSE.PTR
BuildArch:      noarch

%description
Python Lex & Yacc

%package -n     python3-ply
Summary:        Python Lex & Yacc
BuildRequires:  python3-devel
Requires:       python3
%if %{with_check}
BuildRequires:  python3-six
%endif

%description -n python3-ply
PLY is yet another implementation of lex and yacc for Python. Some notable
features include the fact that its implemented entirely in Python and it
uses LALR(1) parsing which is efficient and well suited for larger grammars.

PLY provides most of the standard lex/yacc features including support for empty
productions, precedence rules, error recovery, and support for ambiguous grammars.

PLY is extremely easy to use and provides very extensive error checking.
It is compatible with both Python 2 and Python 3.

%prep
%autosetup -n ply-%{version}

%build
%py3_build
cp %{SOURCE1} ./

%install
%py3_install
chmod a-x test/*

%check
pushd test
%{python3} testlex.py
%{python3} testyacc.py
%{python3} testcpp.py
popd

%files -n python3-ply
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.7.11-6
- Remove python2 package
- Lint spec
- License verified

* Fri May 29 2020 Mateusz Malisz <mamalisz@microsoft.com> - 3.11-7
- Added %%license macro.

* Tue Apr 21 2020 Eric Li <eli@microsoft.com> - 3.11-6
- Fix Source0: and #Source0: Fixed URL.

* Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.11-5
- Fixing "Source0" tag and comment.
- Switching to using https for source URL.

* Thu Apr 09 2020 Nick Samson <nisamson@microsoft.com> - 3.11-4
- Removed %%define sha1 line. Updated Source0. License validated.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.11-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> - 3.11-2
- Add %check

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 3.11-1
- Update to version 3.11

* Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> - 3.10-1
- Initial packaging.
