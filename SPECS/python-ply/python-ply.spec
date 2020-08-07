%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define LICENSE_PATH LICENSE.PTR

Name:           python-ply
Version:        3.11
Release:        7%{?dist}
Summary:        Python Lex & Yacc
License:        BSD
Group:          Development/Languages/Python
Url:            https://www.dabeaz.com/ply/
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       http://www.dabeaz.com/ply/ply-%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/e5/69/882ee5c9d017149285cab114ebeab373308ef0f874fcdac9beb90e0ac4da/ply-%{version}.tar.gz
Source1:        LICENSE.PTR
BuildRequires:  python2-devel
%if %{with_check}
BuildRequires:  python-six
%endif
Requires:       python2
BuildArch:      noarch

%description
PLY is yet another implementation of lex and yacc for Python. Some notable
features include the fact that its implemented entirely in Python and it
uses LALR(1) parsing which is efficient and well suited for larger grammars.

PLY provides most of the standard lex/yacc features including support for empty
productions, precedence rules, error recovery, and support for ambiguous grammars.

PLY is extremely easy to use and provides very extensive error checking.
It is compatible with both Python 2 and Python 3.

%package -n     python3-ply
Summary:        python3 version
BuildRequires:  python3-devel
%if %{with_check}
BuildRequires:  python3-six
%endif
Requires:       python3

%description -n python3-ply
Python 3 version.

%prep
%setup -q -n ply-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
CFLAGS="%{optflags}" python2 setup.py build
pushd ../p3dir
CFLAGS="%{optflags}" python3 setup.py build
popd
cp %{SOURCE1} ./

%install
rm -rf %{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
chmod a-x test/*
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
chmod a-x test/*
popd

%check
pushd test

python2 testlex.py
python2 testyacc.py
python2 testcpp.py

python3 testlex.py
python3 testyacc.py
python3 testcpp.py

popd

%clean
rm -rf %{buildroot}

%files
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-ply
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Fri May 29 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.11-7
-   Added %%license macro.
*   Tue Apr 21 2020 Eric Li <eli@microsoft.com> 3.11-6
-   Fix Source0: and #Source0: Fixed URL.
*   Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.11-5
-   Fixing "Source0" tag and comment.
-   Switching to using https for source URL.
*   Thu Apr 09 2020 Nick Samson <nisamson@microsoft.com> 3.11-4
-   Removed %%define sha1 line. Updated Source0. License validated.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.11-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> 3.11-2
-   Add %check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.11-1
-   Update to version 3.11
*   Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.10-1
-   Initial packaging.
