# Created by pyp2rpm-3.3.6
%global pypi_name resolvelib
Summary:        Resolve abstract dependencies into concrete ones
Name:           python-%{pypi_name}
Version:        1.0.1
Release:        1%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/sarugaku/resolvelib
Source0:        %{pypi_source}#/python-resolvelib-1.0.1.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildArch:      noarch

%description
ResolveLib at the highest level provides a Resolver class that
includes dependency resolution logic. You give it some things, and a little
information on how it should interact with them, and it will spit out a
resolution result. Intended Usage :: import resolvelib Things I want to
resolve. requirements [...] Implement logic so the resolver understands the
requirement format. class...

%package -n     python3-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:        %{summary}

%description -n python3-%{pypi_name}
ResolveLib at the highest level provides a Resolver class that
includes dependency resolution logic. You give it some things, and a little
information on how it should interact with them, and it will spit out a
resolution result. Intended Usage :: import resolvelib Things I want to
resolve. requirements [...] Implement logic so the resolver understands the
requirement format. class...


%prep
%autosetup -n resolvelib-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Fri Jun 23 2023 Sam Meluch <sammeluch@microsoft.com> - 1.0.1-1
- Initial CBL-Mariner import from Fedora 38 (license: ISC).
- License verified
- upgrade spec to version 1.0.1

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.5.5-8
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.5.5-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.5.5-2
- Rebuilt for Python 3.10

* Sat Apr 10 2021 Kevin Fenzi <kevin@scrye.com> - 0.5.5-1
- Initial package.
