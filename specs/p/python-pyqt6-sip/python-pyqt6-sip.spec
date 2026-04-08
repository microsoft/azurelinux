# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkg_name pyqt6-sip
%global pypi_name pyqt6_sip
%global _sip_api_major 13
%global _sip_api_minor 10
%global _sip_api %{_sip_api_major}.%{_sip_api_minor}

Name:           python-%{pkg_name}
Version:        13.10.2
Release:        4%{?dist}
Summary:        The sip module support for PyQt6

License:        GPL-2.0-only OR GPL-3.0-only
URL:            https://www.riverbankcomputing.com/software/sip/
Source0:        %{pypi_source}

BuildRequires:  gcc
BuildRequires:  python3-devel

%global _description %{expand:
The sip extension module provides support for the PyQt6 package.
}

%description %_description

%package -n     python3-%{pkg_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkg_name}}
Provides: python3-pyqt6-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python3-pyqt6-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}

%description -n python3-%{pkg_name} %_description
%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l PyQt6


%check
%pyproject_check_import


%files -n python3-%{pkg_name} -f %{pyproject_files}
%doc README


%changelog
* Fri Jul 25 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 13.10.2-4
- Convert to pyproject macros

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 13.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 08 2025 Python Maint <python-maint@redhat.com> - 13.10.2-2
- Rebuilt for Python 3.14

* Sat Jun 07 2025 Jan Grulich <jgrulich@redhat.com> - 13.10.2-1
- 13.10.2

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 13.9.1-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 13.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Jan Grulich <jgrulich@redhat.com> - 13.9.1-1
- 13.9.1

* Sun Jul 21 2024 Kevin Fenzi <kevin@scrye.com> - 13.8.0-1
- Update to 13.8.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 13.6.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 16 2023 Jan Grulich <jgrulich@redhat.com> - 13.6.0-1
- 13.6.0

* Thu Oct 12 2023 Richard Fontana <rfontana@redhat.com> - 13.4.0-6
- Migrate License: tag to SPDX
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 21 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 13.4.0-4
- Backport patches needed for compatibility with Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 13.4.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 05 2022 Onuralp Sezer <thunderbirdtr@fedoraproject.org> - 13.4.0-1
- 13.4.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 13.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 13.3.0-2
- Rebuilt for Python 3.11

* Wed Apr 13 2022 Onuralp Sezer <thunderbirdtr@fedoraproject.org> - 13.3.0-1
- Initial Package
