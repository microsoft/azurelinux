# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name jaraco_text
%global pkg_name jaraco-text

# there's an issue with sphinx dep resolution
# turining off docs build for now
%bcond_with docs
# Not all test dependencies are available yet
%bcond_with tests
# Change the build backend in EPEL9 because `setuptools>=61.2`
# is needed for PEP621
%if 0%{?epel} == 9
%bcond_without hatch
%else
%bcond_with    hatch
%endif

Name:           python-%{pkg_name}
Version:        4.0.0
Release:        7%{?dist}
Summary:        Module for text manipulation

License:        MIT
URL:            https://github.com/jaraco/jaraco.text
Source0:        %{pypi_source}
BuildArch:      noarch
 
BuildRequires:  python3-devel
%if %{with hatch}
BuildRequires:  tomcli
%endif
%generate_buildrequires
%pyproject_buildrequires

%if %{with tests}
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(pytest-checkdocs)
BuildRequires: python3dist(pytest-flake8)
BuildRequires: python3dist(pytest-black-multipy)
BuildRequires: python3dist(pytest-cov)
# with tests
%endif

%description
%{summary}

%package -n     python3-%{pkg_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkg_name}}

%description -n python3-%{pkg_name}
%{summary}

%package -n python-%{pkg_name}-doc
Summary:        jaraco.text documentation
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(rst-linker) >= 1.9
BuildRequires:  python3dist(jaraco-packaging)

%description -n python-%{pkg_name}-doc
Documentation for jaraco.text

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%if %{with hatch}
tomcli set pyproject.toml lists str "build-system.requires" "hatchling" "hatch-vcs"
tomcli set pyproject.toml str "build-system.build-backend" "hatchling.build"
tomcli set pyproject.toml str "tool.hatch.version.source" "vcs"
tomcli set pyproject.toml lists str "tool.hatch.build.targets.wheel.packages" "jaraco"
%endif

%build
%pyproject_wheel

%if %{with docs}
# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# with docs
%endif

%install
%pyproject_install
install -pm 0644 jaraco/text/Lorem\ ipsum.txt \
    %{buildroot}%{python3_sitelib}/jaraco/text/
%pyproject_save_files jaraco

%if 0%{?with_tests}
%check
%pytest
# with tests
%endif

%files -n python3-%{pkg_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%if %{with docs}
%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE
# with docs
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.0.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.0.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 4.0.0-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Oct 05 2024 Ondrej Mosnáček <omosnacek@gmail.com> - 4.0.0-2
- Fix the install command to comply with guidelines
- Use %%{pyproject_[save_]files}
- Fix EPEL9 build

* Thu Aug 01 2024 Dan Radez <dradez@redhat.com> - 4.0.0-1
- update to upstream 4.0.0 rhbz#2300119

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Dan Radez <dradez@redhat.com> - 3.14.0-1
- update to upstream 3.14.0 rhbz#2292660

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 3.12.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Dan Radez <dradez@redhat.com> - 3.12.0-1
- update to upstream 3.12 rhbz#2251804

* Wed Aug 16 2023 Dan Radez <dradez@redhat.com> - 3.11.1-1
- update to upstream 3.11 rhbz#2232234

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 3.2.0-12
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 3.2.0-9
- Rebuilt for Python 3.11

* Wed May 04 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.2.0-8
- Backport patch to fix DeprecationWarning

* Thu Apr 07 2022 Dan Radez - 3.2.0-7
- Switched to pyproject macros
- disabled docs. Sphinx can't resolve deps properly
- Fixes: rhbz#2069541

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.2.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar 13 2020 Matthias Runge <mrunge@redhat.com> - 3.2.0-1
- Initial package.
