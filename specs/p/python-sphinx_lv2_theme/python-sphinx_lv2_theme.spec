# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name sphinx_lv2_theme

%global common_description %{expand:
This is a minimal pure-CSS theme for Sphinx that uses the documentation
style of the LV2 plugin specification and related projects.

This theme is geared toward producing beautiful API documentation for C, C++,
and Python that is documented using the standard Sphinx domains.
The output does not use Javascript at all, and some common features are not
implemented, so this theme should not be considered a drop-in replacement
for typical Sphinx themes.}


Name:           python-%{pypi_name}
Version:        1.4.2
Release: 8%{?dist}
Summary:        A minimal pure-CSS theme for Sphinx
License:        ISC
URL:            https://gitlab.com/lv2/%{pypi_name}
Source0:        %{url}/-/archive/v%{version}/%{pypi_name}-v%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel

%description %{common_description}


%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}


%description -n python%{python3_pkgversion}-%{pypi_name} %{common_description}


%prep
%autosetup -p1 -n %{pypi_name}-v%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}


%check
%pyproject_check_import


%files -n  python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.4.2-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.4.2-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Guido Aulisi <guido.aulisi@gmail.com> - 1.4.2-4
- Migrate to pyproject macros (#2378238)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.4.2-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 23 2024 Guido Aulisi <guido.aulisi@gmail.com> - 1.4.2-1
- Update to 1.4.2

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.4.0-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Guido Aulisi <guido.aulisi@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.2.2-2
- Rebuilt for Python 3.12

* Mon Jan 30 2023 Guido Aulisi <guido.aulisi@gmail.com> - 1.2.2-1
- Update to 1.2.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 01 2022 Guido Aulisi <guido.aulisi@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.0-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 15:54:29 CET 2021 Guido Aulisi <guido.aulisi@gmail.com> - 1.0.0-2
- Spec cleanup

* Fri Jan 15 08:38:05 CET 2021 Guido Aulisi <guido.aulisi@gmail.com> - 1.0.0-1
- Initial package release
