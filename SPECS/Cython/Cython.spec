%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:       C extensions for Python 2
Name:          Cython
Version:       0.28.5
Release:       8%{?dist}
Group:         Development/Libraries
License:       ASL 2.0
URL:           https://cython.org
#Source0:      https://github.com/cython/cython/archive/%{version}.tar.gz
Source0:       %{name}-%{version}.tar.gz
Patch0:        fix_abc_tests.patch
Patch1:        cython_testfix_with_outer_raising.patch
Vendor:        Microsoft Corporation
Distribution:  Mariner
BuildRequires: python2-devel
BuildRequires: python2-libs
BuildRequires: python-xml
Requires:      python2
Provides:      python2-%{name}
Provides:      cython

%description
Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language (based on Pyrex). It makes writing C extensions for Python as easy as Python itself.

%package -n python3-%{name}
Summary:       C extensions for Python 3
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-libs
BuildRequires: python3-xml
Requires:      python3

%description -n python3-%{name}
Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language (based on Pyrex). It makes writing C extensions for Python as easy as Python itself.

%prep
%autosetup -p1 -n cython-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/cygdb %{buildroot}/%{_bindir}/cygdb3
mv %{buildroot}/%{_bindir}/cython %{buildroot}/%{_bindir}/cython3
mv %{buildroot}/%{_bindir}/cythonize %{buildroot}/%{_bindir}/cythonize3
python2 setup.py install --skip-build --root %{buildroot}

%check
# Skip lvalue_refs test which was fixed in a later release: https://github.com/cython/cython/pull/2783
echo "lvalue_refs" >> tests/bugs.txt
python2 runtests.py -vv
python3 runtests.py -vv

%files
%defattr(-,root,root,-)
%license LICENSE.txt
%{_bindir}/cygdb
%{_bindir}/cython
%{_bindir}/cythonize
%{python2_sitelib}/Cython-%{version}-*.egg-info
%{python2_sitelib}/Cython/*
%{python2_sitelib}/cython.py*
%{python2_sitelib}/pyximport/*

%files -n python3-%{name}
%license LICENSE.txt
%{_bindir}/cygdb3
%{_bindir}/cython3
%{_bindir}/cythonize3
%{python3_sitelib}/Cython-%{version}-*.egg-info
%{python3_sitelib}/Cython/*
%{python3_sitelib}/cython.py*
%{python3_sitelib}/pyximport/*
%{python3_sitelib}/__pycache__/*

%changelog
*   Wed Apr 28 2021 Andrew Phelps <anphel@microsoft.com> 0.28.5-8
-   Build for python3.
-   Add patch to fix python3.7 test failure.
*   Mon Dec 07 2020 Andrew Phelps <anphel@microsoft.com> 0.28.5-7
-   Fix check tests.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.28.5-6
-   Added %%license line automatically
*   Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 0.28.5-5
-   Renaming cython to Cython
*   Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> 0.28.5-4
-   Update URL.
-   Update Source0 with valid URL.
-   Update license.
-   Remove sha1 macro.
-   Fix changelog styling.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.28.5-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Jan 10 2019 Michelle Wang <michellew@vmware.com> 0.28.5-2
-   Add fix_abc_tests.patch to fix make check test.
*   Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 0.28.5-1
-   Upgraded to version 0.28.5.
*   Thu Jul 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.25.2-2
-   Build using python2 explicity.
*   Mon Apr 24 2017 Bo Gan <ganb@vmware.com> 0.25.2-1
-   Update to 0.25.2.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.23.4-3
-   Modified %check.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.23.4-2
-   GA - Bump release of all rpms.
*   Wed Oct 28 2015 Divya Thaluru <dthaluru@vmware.com> 0.23.4-1
-   Initial build.
