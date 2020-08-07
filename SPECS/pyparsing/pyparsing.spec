%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python package with an object-oriented approach to text processing
Name:           pyparsing
Version:        2.2.0
Release:        7%{?dist}
Url:            https://github.com/pyparsing/pyparsing
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/pyparsing/pyparsing/archive/pyparsing_%{version}.tar.gz
Source0:        pyparsing-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

%package -n     python3-pyparsing
Summary:        Python package with an object-oriented approach to text processing
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-pyparsing

Python 3 version.

%prep
%setup -q -n pyparsing-%{version}
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

#%check
#Tests are not available

%files
%license LICENSE
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-pyparsing
%license LICENSE
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.2.0-7
-   Adding the "%%license" macro.
*   Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.2.0-6
-   Rename python-pyparsing to pyparsing.
-   Update description.
-   Update summary.
*   Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> 2.2.0-5
-   Update URL.
-   Update Source0 with valid URL.
-   Remove sha1 macro.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.2.0-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 2.2.0-3
-   Disabled check section as tests are not available
*   Tue Jun 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.0-2
-   Add build dependency with python-setuptools to handle 1.0 update
*   Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 2.2.0-1
-   Update to 2.2.0 and remove build dependency with python-setuptools
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.10-1
-   Initial packaging for Photon
