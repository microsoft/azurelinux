%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The fastest markdown parser in pure Python.
Name:           python-mistune
Version:        0.8.3
Release:        3%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/mistune/
Source0:        https://files.pythonhosted.org/packages/source/m/mistune/mistune-%{version}.tar.gz
%define sha1    mistune=993c67443f393f9645d5f969492a8a107d9edc5f

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
The fastest markdown parser in pure Python

The fastest markdown parser in pure Python with renderer features, inspired by marked.

%package -n     python3-mistune
Summary:        python-mistune
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-mistune
Python 3 version.

%prep
%setup -q -n mistune-%{version}
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

%files -n python3-mistune
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:21:37 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.8.3-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.8.3-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.8.3-1
-   Update to version 0.8.3
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-1
-   Initial packaging for Photon
