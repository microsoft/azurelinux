%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-iniparse
Version:        0.4
Release:        9%{?dist}
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
Group:          Development/Libraries
License:        MIT or Python
URL:            https://github.com/candlepin/python-iniparse
Source0:        https://files.pythonhosted.org/packages/0f/d1/3090ef9be165da5ddb1b0cf2b332d3282588bdd2dd0967e94b547f10055f/iniparse-%{version}.tar.gz
Patch0:         0001-Add-python-3-compatibility.patch
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python2-test

Requires:       python2

%description
iniparse is an INI parser for Python which is API compatible
with the standard library's ConfigParser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.

%package -n     python3-iniparse
Summary:        python-iniparse
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-six
BuildRequires:  python3-test
Requires:       python3
Requires:       python3-libs
Requires:       python3-pycparser
Requires:       python3-six

%description -n python3-iniparse
Python 3 version.

%prep
%setup -q -n iniparse-%{version}
rm -rf ../p3dir
cp -a . ../p3dir
pushd ../p3dir
%patch0 -p1
popd

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
# fixes
chmod 644 %{buildroot}/usr/share/doc/iniparse-%{version}/index.html
mv %{buildroot}/usr/share/doc/iniparse-%{version} %{buildroot}/usr/share/doc/python-iniparse-%{version}


%check
python2 runtests.py

pushd ../p3dir
python3 runtests.py
popd


%files
%defattr(-,root,root,-)
%license LICENSE
%doc  %{_docdir}/python-iniparse-%{version}/*
%{python2_sitelib}/*

%files -n python3-iniparse
%defattr(-,root,root,-)
%{python3_sitelib}/*


%changelog
* Sat May 09 00:20:46 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.4-9
- Added %%license line automatically

*   Tue Apr 14 2020 Nick Samson <nisamson@microsoft.com> 0.4-8
-   Updated Source0, URL, license info. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.4-7
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Jul 11 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4-6
-   Fix python3 and make check issues.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.4-5
-   Use python2 explicitly to build
*   Mon May 22 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4-4
-   Added python3 subpackage.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 0.4-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.4-2
-   GA - Bump release of all rpms
*   Sat Jun 12 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.4-1
-   Release 0.4
*   Sat Apr 17 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.2-1
-   Release 0.3.2
*   Mon Mar 2 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.1-1
-   Release 0.3.1
*   Fri Feb 27 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.0-1
-   Release 0.3.0
*   Tue Dec 6 2008 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.4-1
-   Release 0.2.4
-   added egg-info file to %%files
*   Tue Dec 11 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.3-1
-   Release 0.2.3
*   Tue Sep 24 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.2-1
-   Release 0.2.2
*   Tue Aug 7 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.1-1
-   Release 0.2.1
*   Fri Jul 27 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-3
-   relocated doc to %{_docdir}/python-iniparse-%{version}
*   Thu Jul 26 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-2
-   changed name from iniparse to python-iniparse
*   Tue Jul 17 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-1
-   Release 0.2
-   Added html/* to %%doc
*   Fri Jul 13 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.1-1
-   Initial build.
