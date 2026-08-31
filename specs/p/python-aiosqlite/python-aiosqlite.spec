# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name aiosqlite

Name:           python-%{pypi_name}
Version:        0.22.1
Release:        1%{?dist}
Summary:        Asyncio bridge to the standard SQLite3 module

License:        MIT
URL:            https://github.com/jreese/aiosqlite
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
aiosqlite AsyncIO bridge to the standard SQLite3 module for Python 3.5+.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
aiosqlite AsyncIO bridge to the standard SQLite3 module for Python 3.5+.

%generate_buildrequires
%pyproject_buildrequires -r

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%{py3_test_envvars} %{python3} -m %{pypi_name}.tests

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc CHANGELOG.md README.rst

%changelog
* Thu Dec 25 2025 Federico Pellegrin <fede@evolware.org> - 0.22.1-1
- Bump to 0.22.1 (rhbz#2424699)

* Mon Dec 15 2025 Federico Pellegrin <fede@evolware.org> - 0.22.0-1
- Bump to 0.22.0 (rhbz#2421994)

* Sun Sep 21 2025 Federico Pellegrin <fede@evolware.org> - 0.21.0-3
- Rebuilt for Python 3.14.0rc3 bytecode (rhbz#2396748)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.21.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Aug 15 2025 Federico Pellegrin <fede@evolware.org> - 0.21.0-1
- Bump to 0.21.0 (rhbz#2343484)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.20.0-6
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.20.0-4
- Run the tests

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.20.0-2
- Rebuilt for Python 3.13

* Sun Apr 07 2024 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.0-1
- Update to latest upstream version 0.20.0 (closes rhbz#2265069)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 07 2023 Lumír Balhar <lbalhar@redhat.com> - 0.19.0-1
- Update to 0.19.0 (rhbz#2154748)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.17.0-8
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.17.0-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.17.0-2
- Rebuilt for Python 3.10

* Wed Feb 24 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.17.0-1
- Update to latest upstream release 0.17.0 (#1919588)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.16.1-1
- Update to latest upstream release 0.16.1 (#1919588)

* Thu Dec 03 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.16.0-1
- Update to latest upstream release 0.16.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-2
- Rebuilt for Python 3.9

* Sun May 03 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.12.0-1
- Update to latest upstream release 0.12.0

* Thu Jan 30 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.11.0-4
- Fix ownership

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.11.0-2
- Use var for souce URL
- Better use of wildcards (rhbz#1786955)

* Sun Dec 29 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.11.0-1
- Initial package for Fedora
