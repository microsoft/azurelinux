Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           python-deprecated
Version:        1.2.18
Release:        2%{?dist}
Summary:        Python decorator to deprecate old python classes, functions or methods
License:        MIT
URL:            https://github.com/laurent-laporte-pro/deprecated
Source:         %{pypi_source deprecated}#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%global _description %{expand:
Python @deprecated decorator to deprecate old python classes,
functions or methods.}

%description %{_description}

%package -n python3-deprecated
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3dist(wheel)
BuildRequires:  python3-wrapt

%description -n python3-deprecated %{_description}

%prep
%autosetup -n deprecated-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files deprecated

%check
%pytest

%files -n python3-deprecated -f %{pyproject_files}
%doc README.md


%changelog
* Mon Sep 29 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.2.18-2
- Initial Azure Linux import from Fedora 42 (license: MIT).
- License verified

* Mon Feb 10 2025 Matej Focko <mfocko@fedoraproject.org> - 1.2.18-1
- Update to version 1.2.18

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Nov 23 2024 Carl George <carlwgeorge@fedoraproject.org> - 1.2.15-1
- Update to version 1.2.15
- Convert to pyproject macros
- Run test suite in %%check

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2.14-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.2.14-2
- Rebuilt for Python 3.12

* Sat May 27 2023 Packit <hello@packit.dev> - 1.2.14-1
- Drops seemingly unused importlib-metadata dev dep (Colin Dean)
- Fixes comment on which version is development branch (Colin Dean)
- Adds Pythons dropped notice to changelog (Colin Dean)
- Drops limitation on tox < 4 since bug was fixed (Colin Dean)
- Adds srpm_build_deps to Packit config (Colin Dean)
- Try explicitly setting AppVeyor image to VS2022 (Colin Dean)
- Exclude pypy3 on ppc64le on Travis builds (Colin Dean)
- Drops old Pythons and adds newer ones for Appveyor build (Colin Dean)
- Drop the .9 from pypy3 in tox.ini (Colin Dean)
- Use specifically pypy3.9 v7.3.9 (Colin Dean)
- Adds Python 3.12 config to tox (Colin Dean)
- Limit tox to <4 on Travis because of outdatedness (Colin Dean)
- Try installing importlib_metadata for tox run (Colin Dean)
- Use newer Travis environment, Focal (Ubuntu 20.04) (Colin Dean)
- Adds importlib-metadata to dev deps (Colin Dean)
- Split and fix tox config for more better coverage (Colin Dean)
- Dropping support for Python older than v3.7 in build systems like pytest and tox, while ensuring the library remains production-compatible. (Colin Dean)
- Drops Python 2.7, 3.5, 3.6 builds from Travis; add 3.12 (Colin Dean)
- Upgrades some actions versions in Actions python builds (Colin Dean)
- Drops Actions builds for Python 2.7, 3.5, 3.6; condense 3.7+ (Colin Dean)
- Bump checkout to v3 in CodeQL Analysis workflow (Colin Dean)
- Add support for Python 3.11 (Hugo van Kemenade)
- edit changelog (Pierrick Rambaud)
- add test for D213 docstrings (Pierrick Rambaud)
- work with empty docstring (Pierrick Rambaud)
- fix: digest D212 and D213 docstring (Pierrick Rambaud)
- Add support for Python 3.10 (Hugo van Kemenade)
- Prepare next version 1.2.14 (unreleased) (Laurent LAPORTE)
- Minor change in bumpversion  configuration to also bump the project version in "appveyor.xml". (Laurent LAPORTE)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.2.13-2
- Rebuilt for Python 3.11

* Fri Apr 29 2022 Hunor Csomortáni <csomh@redhat.com> - 1.2.13-1
- Update to version 1.2.13

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.12-2
- Rebuilt for Python 3.10

* Sat Mar 13 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 1.2.12-1
- new upstream release: 1.2.12

* Sat Feb 06 2021 Hunor Csomortáni <csomh@redhat.com> - 1.2.11-1
- new upstream release: 1.2.11

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 07 2020 Hunor Csomortáni <csomh@redhat.com> - 1.2.10-1
- new upstream release: 1.2.10

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.6-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.6-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.6-4
- Rebuilt for Python 3.8

* Thu Aug 01 2019 Petr Hracek <phracek@redhat.com> - 1.2.6-3
- Enable python dependency generator

* Fri Jul 26 2019 Petr Hracek <phracek@redhat.com> - 1.2.6-2
- Fix python3_sitelib issue

* Fri Jul 26 2019 Petr Hracek <phracek@redhat.com> - 1.2.6-1
- Initial package
