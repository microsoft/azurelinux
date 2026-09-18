# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-installer
Version:        0.7.0
Release:        13%{?dist}
Summary:        A library for installing Python wheels

# SPDX
License:        MIT
URL:            https://github.com/pypa/installer
Source:         %{pypi_source installer}

# Fix the build with Python 3.13 - merged upstream
# https://github.com/pypa/installer/commit/b23f89b10cf5
Patch:          Fix-removed-importlib.resources.read_binary-in-Pytho.patch

BuildArch:      noarch
BuildRequires:  python3-devel

# For tests
BuildRequires:  python3-pytest

%global _description %{expand:
This is a low-level library for installing a Python package from
a wheel distribution. It provides basic functionality and abstractions
for handling wheels and installing packages from wheels.}


%description %_description

%package -n     python3-installer
Summary:        %{summary}

%description -n python3-installer %_description


%prep
%autosetup -p1 -n installer-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files installer


%check
%pyproject_check_import
%pytest


%files -n python3-installer -f %{pyproject_files}
%license LICENSE
%doc CONTRIBUTING.md README.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.7.0-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7.0-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.7.0-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.7.0-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Karolina Surma <ksurma@redhat.com> - 0.7.0-4
- Fix the build with Python 3.13
Fixes: rhbz#2246052

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.7.0-2
- Rebuilt for Python 3.12

* Wed Mar 22 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 28 2022 Charalampos Stratakis <cstratak@redhat.com> - 0.5.1-1
- Initial package (rhbz#2111707)
