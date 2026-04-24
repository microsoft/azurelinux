# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-sphinx-pytest
Version:        0.2.0
Release: 11%{?dist}
Summary:        Helpful pytest fixtures for sphinx extensions

# SPDX
License:        MIT
URL:            https://github.com/sphinx-extensions2/sphinx-pytest
Source:         %{pypi_source sphinx_pytest}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
Helpful pytest fixtures for sphinx extensions.
This extension provides pytest fixtures to "simulate" converting
some source text to docutils AST at different stages; before transforms,
after transforms, etc.}


%description %_description

%package -n     python3-sphinx-pytest
Summary:        %{summary}

%description -n python3-sphinx-pytest %_description


%prep
%autosetup -p1 -n sphinx_pytest-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files sphinx_pytest


%check
%pytest


%files -n python3-sphinx-pytest -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.2.0-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.2.0-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.2.0-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.2.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Karolina Surma <ksurma@redhat.com> - 0.2.0-1
- Update to 0.2.0 (rhbz#2239833)

* Mon Aug 21 2023 Karolina Surma <ksurma@redhat.com> - 0.1.1-3
- Fix tests with Sphinx 7.1+

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Karolina Surma <ksurma@redhat.com> - 0.1.1-1
- Update to 0.1.1

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.0.3-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 22 2022 Karolina Surma <ksurma@redhat.com> - 0.0.3-1
- Initial package
Resolves: rhbz#2100032
