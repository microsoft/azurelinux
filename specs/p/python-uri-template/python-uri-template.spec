# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name uri-template
%global pypi_version 1.3.0

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release: 6%{?dist}
Summary:        RFC 6570 URI Template Processor

License:        MIT
URL:            https://github.com/plinss/uri_template/
Source:         %{url}/archive/refs/tags/v%{pypi_version}.tar.gz#/%{name}-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel

%description
An implementation of RFC 6570 URI Templates.This packages implements
URI Template expansion in strict adherence to RFC 6570, but adds a
few extensions.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
An implementation of RFC 6570 URI Templates.This packages implements
URI Template expansion in strict adherence to RFC 6570, but adds a
few extensions.

%prep
%autosetup -n %{pypi_name}-%{pypi_version}

%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION="%{pypi_version}"
%pyproject_buildrequires

%build
export SETUPTOOLS_SCM_PRETEND_VERSION="%{pypi_version}"
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l uri_template

%check
%{python3} test.py

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.3.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.3.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.3.0-2
- Rebuilt for Python 3.14

* Sun Mar 16 2025 Romain Geissler <romain.geissler@amadeus.com> - 1.3.0-1
- Update to upstream version 1.3.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2.0-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Parag Nemade <pnemade AT redhat DOT com> - 1.2.0-6
- Mark this as SPDX license expression converted

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.2.0-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 29 2022 Parag Nemade <pnemade AT redhat DOT com> - 1.2.0-2
- Fix as per suggested in package review (#2102060)

* Wed Jun 29 2022 Parag Nemade <pnemade AT redhat DOT com> - 1.2.0-1
- Initial package.
