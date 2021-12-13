Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname pydbus

Name:           python-%{srcname}
Version:        0.6.0
Release:        13%{?dist}
Summary:        Pythonic DBus library

License:        LGPLv2+
URL:            https://pypi.python.org/pypi/pydbus
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz#/python-%{srcname}-%{version}.tar.gz

# upstream fix, not yet in release
# https://github.com/LEW21/pydbus/commit/ff792feb45bbdc0dd6a9ff7453825e34b6554865
Patch1: 0001-make-direction-attribute-conforming-to-introspect.dt.patch

# patch submitted for upstream inclusion, not yet merged
# https://github.com/LEW21/pydbus/pull/63
Patch2: 0002-Support-asynchronous-calls-58.patch

# patch submitted for upstream inclusion, not yet merged
# https://github.com/LEW21/pydbus/pull/64
Patch3: 0003-Support-transformation-between-D-Bus-errors-and-exce.patch

BuildArch:      noarch

%global _description \
The pydbus module provides pythonic DBUS bindings.\
It is based on PyGI, the Python GObject Introspection bindings,\
which is the recommended way to use GLib from Python.

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-gobject-base
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version} -p1

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.0-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-11
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-10
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Vendula Poncova <vponcova@redhat.com> - 0.6.0-4
- Drop the python2 support.

* Tue Sep 05 2017 Martin Kolman <mkolman@redhat.com> - 0.6.0-3
- add patch for DTD fix
- add patch with support for asynchronous calls (vponcova)
- add patch with support for transformation between D-Bus errors and exceptions (vponcova)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 15 2017 Martin Kolman <mkolman@redhat.com> - 0.6.0-1
- Initial package
