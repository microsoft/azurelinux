%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Python C parser
Name:           python-pycparser
Version:        2.18
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/pycparser
License:        BSD
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.python.org/packages/source/p/pycparser/pycparser-%{version}.tar.gz
%define sha1    pycparser=1c75af69ae6273b1f1f531744f87d060965ed85d

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs
BuildArch:      noarch


%description
pycparser is a complete parser of the C language, written in pure Python using the PLY parsing library. It parses C code into an AST and can serve as a front-end for C compilers or analysis tools.

%package -n     python3-pycparser
Summary:        python-pycparser
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n python3-pycparser
Python 3 version.

%prep
%setup -q -n pycparser-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
cd tests
python2 all_tests.py

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-pycparser
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.18-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.18-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.18-1
-   Update to version 2.18
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.17-3
-   Use python2 instead of python
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.17-2
-   Fix arch
*   Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.17-1
-   Updated to version 2.17.
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.14-4
-   Added python3 site-packages.
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 2.14-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.14-2
-   GA - Bump release of all rpms
*   Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.14-1
-   Initial packaging for Photon
