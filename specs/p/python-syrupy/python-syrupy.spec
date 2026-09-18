# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-syrupy
Version:        4.9.1
Release:        5%{?dist}
Summary:        Pytest snapshot plugin

License:        Apache-2.0
URL:            https://syrupy-project.github.io/syrupy/
Source:         https://github.com/syrupy-project/syrupy/archive/v%{version}/syrupy-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

# for tests
BuildRequires:  python3-pytest-xdist

%global _description %{expand:
Syrupy is a pytest snapshot plugin. It enables developers
to write tests which assert immutability of computed results.}

%description %_description

%package -n python3-syrupy
Summary:        %{summary}

%description -n python3-syrupy %_description


%prep
%autosetup -p1 -n syrupy-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files syrupy


%check
%pytest


%files -n python3-syrupy -f %{pyproject_files}
%doc README.* CHANGELOG.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.9.1-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.9.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 4.9.1-2
- Rebuilt for Python 3.14

* Tue Mar 25 2025 Jonathan Wright <jonathan@almalinux.org> - 4.9.1-1
- update to 4.9.1

* Tue Mar 25 2025 Jonathan Wright <jonathan@almalinux.org> - 4.8.3-1
- update to 4.8.3

* Tue Mar 25 2025 Jonathan Wright <jonathan@almalinux.org> - 4.7.2-1
- update to 4.7.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.6.1-2
- Rebuilt for Python 3.13

* Tue Apr 16 2024 Lumír Balhar <lbalhar@redhat.com> - 4.6.1-1
- Update to 4.6.1

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 15 2023 Jonathan Wright <jonathan@almalinux.org> - 4.5.0-1
- Update to 4.5.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 3.0.6-2
- Rebuilt for Python 3.12

* Thu Jan 12 2023 Jonathan Wright <jonathan@almalinux.org> - 3.0.6-1
- Initial package build
