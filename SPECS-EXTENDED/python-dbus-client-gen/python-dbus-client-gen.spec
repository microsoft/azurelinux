Vendor:         Microsoft Corporation
Distribution:   Mariner
%{?python_enable_dependency_generator}
%global srcname dbus-client-gen

Name:           python-%{srcname}
Version:        0.4
Release:        7%{?dist}
Summary:        Library for Generating D-Bus Client Code

License:        MPLv2.0
URL:            https://github.com/stratis-storage/dbus-client-gen
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%global _description \
This library contains a few methods that consume an XML specification\
of a D-Bus interface and return classes or functions that may be useful\
in constructing a python D-Bus client. The XML specification has the format\
of the data returned by the Introspect() method\
of the Introspectable interface.

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-hypothesis
BuildRequires:  python3-hs-dbus-signature

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
PYTHONPATH=%{buildroot}%{python3_sitelib} py.test-%{python3_version} -v tests

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/dbus_client_gen/
%{python3_sitelib}/dbus_client_gen-*.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4-1
- Update to 0.4

* Wed Aug 8 2018 Andy Grover <agrover@redhat.com> - 0.3-4
* Bump version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3-2
- Rebuilt for Python 3.7

* Fri Jun 1 2018 Andy Grover <agrover@redhat.com> - 0.3-1
- New upstream release

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2-1
- Initial package
