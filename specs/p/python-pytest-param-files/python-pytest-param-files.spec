# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-pytest-param-files
Version:        0.6.0
Release: 8%{?dist}
Summary:        Create pytest parametrize decorators from external files

# SPDX
License:        MIT
URL:            https://pypi.org/project/pytest_param_files/
Source:         %{pypi_source pytest_param_files}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
A package to generate parametrized pytests from external files.
Create a text file with the dot format, then use the `param_file` pytest marker
to create a parametrized test.}


%description %_description

%package -n     python3-pytest-param-files
Summary:        %{summary}

%description -n python3-pytest-param-files %_description


%prep
%autosetup -p1 -n pytest_param_files-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files pytest_param_files


%check
%pytest


%files -n python3-pytest-param-files -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.6.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.6.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.6.0-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Karolina Surma <ksurma@redhat.com> - 0.6.0-1
- Update to 0.6.0

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.3.4-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.3.4-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Karolina Surma <ksurma@redhat.com> - 0.3.4-1
- Initial package
