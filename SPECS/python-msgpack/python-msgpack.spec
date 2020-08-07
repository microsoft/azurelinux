%global debug_package %{nil}
%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        MessagePack (de)serializer.
Name:           python-msgpack
Version:        0.6.2
Release:        2%{?dist}
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            http://msgpack.org/
#Source0:        https://github.com/msgpack/msgpack-python/archive/v0.6.2.tar.gz
Source0:        https://github.com/msgpack/msgpack-python/archive/%{name}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2

%description
MessagePack is a fast, compact binary serialization format, suitable for similar data to JSON. This package provides CPython bindings for reading and writing MessagePack data.

%package -n     python3-msgpack
Summary:        Python3 msgpack
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-msgpack

%prep
%setup -q -n msgpack-python-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%license COPYING
%{python2_sitelib}/*

%files -n python3-msgpack
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:20:41 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.6.2-2
- Added %%license line automatically

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> 0.6.2-1
- Update to version 0.6.2.  License verified. Source0 fixed.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.5.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.5.6-1
- Update to version 0.5.6
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.8-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu May 25 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.8-1
- Initial version
