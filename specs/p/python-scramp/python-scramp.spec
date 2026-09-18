# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name scramp

Name:           python-%{pypi_name}
Version:        1.4.6
Release:        4%{?dist}
Summary:        Implementation of the SCRAM protocol

License:        MIT-0
URL:            https://github.com/tlocke/scramp
Source0:        %{pypi_source %{pypi_name} %{version}}
BuildArch:      noarch

%description
Scramp is pure-Python implementation of the SCRAM authentication protocol.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
# The dependencies needed for testing don’t get auto-generated.
BuildRequires:  python3dist(passlib)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-mock)

%description -n python3-%{pypi_name}
Scramp is a pure-Python implementation of the SCRAM authentication protocol.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pytest -v

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.4.6-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.4.6-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.6-1
- Update to latest upstream release (closes rhbz#2376515)

* Wed Jun 11 2025 Python Maint <python-maint@redhat.com> - 1.4.5-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 29 2024 Python Maint <python-maint@redhat.com> - 1.4.5-2
- Rebuilt for Python 3.13

* Sat Apr 13 2024 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.5-1
- Update to latest upstream release (closes rhbz#2274889)

* Tue Feb 06 2024 Nils Philippsen <nils@tiptoe.de> - 1.4.4-1
- Update to latest upstream release 1.4.4

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.4.1-6
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.4.1-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 25 2021 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.1-1
- Update to latest upstream release 1.4.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.0-1
- Update to latest upstream release 1.2.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-2
- Rebuilt for Python 3.9

* Sun Mar 29 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.1.1-1
- Update to latest upstream release 1.1.1

* Mon Mar 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.1.0-1
- Initial package for Fedora
