%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Measures number of Terminal column cells of wide-character codes.
Name:           python-wcwidth
Version:        0.1.7
Release:        4%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/wcwidth
Source0:        https://files.pythonhosted.org/packages/source/w/wcwidth/wcwidth-%{version}.tar.gz
%define         sha1 wcwidth=28df2f5e8cd67ec182d822350252fea9bc3a91c8

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
This Library is mainly for those implementing a Terminal Emulator, or programs that carefully produce output to be interpreted by one.

%package -n     python3-wcwidth
Summary:        python-wcwidth
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-wcwidth
Python 3 version.

%prep
%setup -q -n wcwidth-%{version}
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
%license LICENSE.txt
%{python2_sitelib}/*

%files -n python3-wcwidth
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:20:59 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.1.7-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.1.7-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.7-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.7-1
-   Initial packaging for Photon
