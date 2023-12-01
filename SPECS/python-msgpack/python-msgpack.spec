%global debug_package %{nil}
Summary:        MessagePack (de)serializer.
Name:           python-msgpack
Version:        1.0.3
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://msgpack.org/
Source0:        https://github.com/msgpack/msgpack-python/archive/v%{version}.tar.gz#/msgpack-python-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-Cython
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
MessagePack (de)serializer.

%package -n     python3-msgpack
Summary:        MessagePack (de)serializer.
Requires:       python3

%description -n python3-msgpack
MessagePack is a fast, compact binary serialization format, suitable for similar data to JSON. This package provides CPython bindings for reading and writing MessagePack data.

%prep
%autosetup -n msgpack-python-%{version}

%build
%py3_build

%install
%py3_install

%check
# v1.0.3 does not have a tox env for newer versions of python, so we add it ourselves
sed -i 's/    {py35,py36,py37,py38}-{c,pure},/    {py35,py36,py37,py38,py%{python3_version_nodots}}-{c,pure},/g' tox.ini
pip3 install tox
tox -e py%{python3_version_nodots}-c,py%{python3_version_nodots}-pure

%files -n python3-msgpack
%defattr(-,root,root)
%license COPYING
%{python3_sitelib}/*

%changelog
* Thu Apr 07 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.0.3-1
- Upgrade to latest upstream version
- Use tox as test runner

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.6.2-3
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.6.2-2
- Added %%license line automatically

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> - 0.6.2-1
- Update to version 0.6.2.  License verified. Source0 fixed.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.5.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.5.6-1
- Update to version 0.5.6

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.4.8-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu May 25 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.4.8-1
- Initial version
