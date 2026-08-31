# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name isoduration

Name:           python-%{pypi_name}
Version:        20.11.0
Release:        15%{?dist}
Summary:        Operations with ISO 8601 durations

License:        ISC
URL:            https://github.com/bolsote/isoduration
Source0:        %{url}/releases/download/%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel

%description
ISO 8601 is most commonly known as a way to exchange datetimes in textual
format. A lesser known aspect of the standard is the representation of
durations. They have a shape similar to this: P3Y6M4DT12H30M5S

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
ISO 8601 is most commonly known as a way to exchange datetimes in textual
format. A lesser known aspect of the standard is the representation of
durations. They have a shape similar to this: P3Y6M4DT12H30M5S

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
# upstream does not bundle any tests in released tarball
%pyproject_check_import

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 20.11.0-15
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 20.11.0-14
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20.11.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 20.11.0-12
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20.11.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20.11.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 20.11.0-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20.11.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20.11.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Parag Nemade <pnemade@fedoraproject.org> - 20.11.0-6
- Mark this as SPDX license expression converted

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Python Maint <python-maint@redhat.com> - 20.11.0-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Parag Nemade <pnemade@fedoraproject.org> - 20.11.0-1
- Initial package.
