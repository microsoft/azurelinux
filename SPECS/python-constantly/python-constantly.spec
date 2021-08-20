%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Symbolic constants in Python.
Name:           python-constantly
Version:        15.1.0
Release:        5%{?dist}
Url:            https://github.com/twisted/constantly
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Source to be fixed as part of https://microsoft.visualstudio.com/OS/_workitems/edit/25936171.
Source0:        https://files.pythonhosted.org/packages/95/f1/207a0a478c4bb34b1b49d5915e2db574cadc415c9ac3a7ef17e29b2e8951/constantly-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
A library that provides symbolic constant support. It includes collections and constants with text, numeric, and bit flag values. Originally twisted.python.constants from the Twisted project.

%package -n     python3-constantly
Summary:        python-constantly
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-constantly

Python 3 version.

%prep
%setup -q -n constantly-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

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

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-constantly
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 15.1.0-5
- Added %%license line automatically

*   Wed Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 15.1.0-4
-   Fixed "Source0" tag.
-   License verified.
-   Removed "%%define sha1".
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 15.1.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 15.1.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 15.1.0-1
-   Initial packaging for Photon
