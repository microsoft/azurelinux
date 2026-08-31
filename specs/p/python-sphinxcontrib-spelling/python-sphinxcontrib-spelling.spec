# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name sphinxcontrib-spelling
%global sum  A spelling checker for Sphinx-based documentation
%global desc This package contains sphinxcontrib.spelling, a spelling checker for \
Sphinx-based documentation. It uses PyEnchant to produce a report showing \
misspelled words.

# Disable dependency generator
%{?python_disable_dependency_generator}

%bcond_without python3

Name:           python-%{pypi_name}
Version:        7.3.3
Release:        16%{?dist}
Summary:        %{sum}

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/sphinx-contrib/spelling
Source0:        %{pypi_source}
BuildArch:      noarch

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pbr
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-enchant
BuildRequires:  python%{python3_pkgversion}-sphinx
%endif

%if 0%{?with_python3_other}
BuildRequires:  python%{python3_other_pkgversion}-setuptools
BuildRequires:  python%{python3_other_pkgversion}-devel
BuildRequires:  python%{python3_other_pkgversion}-pbr
BuildRequires:  python%{python3_other_pkgversion}-pytest
BuildRequires:  python%{python3_other_pkgversion}-enchant
BuildRequires:  python%{python3_other_pkgversion}-sphinx
%endif


%description
%{desc}

# Python 3 package
%if %{with python3}
%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
Requires:       python%{python3_pkgversion}-enchant
Requires:       python%{python3_pkgversion}-sphinx

%description -n python%{python3_pkgversion}-%{pypi_name}
%{desc}
%endif

# Python 3 other package
%if 0%{?with_python3_other}
%package -n     python%{python3_other_pkgversion}-%{pypi_name}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{pypi_name}}
Requires:       python%{python3_other_pkgversion}-enchant
Requires:       python%{python3_other_pkgversion}-sphinx

%description -n python%{python3_other_pkgversion}-%{pypi_name}
%{desc}
%endif


%prep
%autosetup -p0 -n %{pypi_name}-%{version}

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%if %{with python3}
%py3_build
%endif

%if 0%{?with_python3_other}
%py3_other_build
%endif


%install
%if 0%{?with_python3_other}
%py3_other_install
%endif

%if %{with python3}
%py3_install
%endif


%check
%if %{with python3}
%pytest
%endif

%if 0%{?with_python3_other}
%{__python3_other} -m pytest
%endif


%if %{with python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README
%license LICENSE
%{python3_sitelib}/sphinxcontrib
%{python3_sitelib}/sphinxcontrib_spelling*
%endif

%if 0%{?with_python3_other}
%files -n python%{python3_other_pkgversion}-%{pypi_name}
%doc README
%license LICENSE
%{python3_other_sitelib}/sphinxcontrib
%{python3_other_sitelib}/sphinxcontrib_spelling*
%endif


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 7.3.3-16
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.3.3-15
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 7.3.3-13
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 7.3.3-11
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 7.3.3-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 7.3.3-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 7.3.3-2
- Rebuilt for Python 3.11

* Mon May 02 2022 Avram Lubkin <aviso@rockhopper.net> - 7.3.3-1
- Updated to 7.3.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.3.0-8
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.3.0-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Avram Lubkin <aviso@rockhopper.net> - 4.3.0-3
- Fix changelog

* Wed Nov 27 2019 Avram Lubkin <aviso@rockhopper.net> - 4.3.0-2
- Disable python dependency generator

* Mon Oct 28 2019 Avram Lubkin <aviso@rockhopper.net> - 4.3.0-1
- Updated to 4.3.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 02 2019 Avram Lubkin <aviso@rockhopper.net> - 4.2.1-1
- Updated to 4.2.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Avram Lubkin <aviso@rockhopper.net> - 4.2.0-1
- Updated to 4.2.0
- Remove Python 2 from Fedora 30+ and EL8+

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.0.1-4
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.0.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018  Avram Lubkin <aviso@rockhopper.net> - 4.0.1-1
- Updated to 4.0.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 01 2017  Avram Lubkin <aviso@rockhopper.net> - 2.3.0-1
- Update to 2.3.0

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.1.2-3
- Rebuild for Python 3.6

* Wed Jul 20 2016 Avram Lubkin <aviso@rockhopper.net> - 2.1.2-2
- Added build support for EPEL 6 and 7

* Wed Jun 15 2016 Avram Lubkin <aviso@rockhopper.net> - 2.1.2-1
- Initial package.
