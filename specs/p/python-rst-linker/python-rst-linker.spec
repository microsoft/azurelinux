# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Created by pyp2rpm-3.2.2
%global pypi_name rst.linker
%global pkg_name rst-linker
# This package is interdependant on jaraco-packaging to build docs
# will build both with out docs and add docs in later
%bcond_with docs

Name:           python-%{pkg_name}
Version:        2.4.0
Release: 15%{?dist}
Summary:        Can add links and perform other custom replacements to rst

License:        MIT
URL:            https://github.com/jaraco/rst.linker
Source0:        https://files.pythonhosted.org/packages/source/r/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
 rst.linker provides a routine for adding links and performing other custom
replacements to restructured text files as a Sphinx extension.License License
is indicated in the project metadata (typically one or more of the Trove
classifiers). For more details, see this explanation < In your sphinx
configuration file, include rst.linker as an extension and then add a
link_files configuration section...

%package -n python3-%{pkg_name}
Summary:        %{summary}

Requires:       python3dist(six)

BuildRequires:  python3-devel
BuildRequires:  python3dist(path) >= 13
BuildRequires:  python3dist(pytest)

%{?python_provide:%python_provide python3-%{pkg_name}}

%description -n python3-%{pkg_name}
%{description}

%if %{with docs}
%package -n python-%{pkg_name}-doc
Summary:        rst.linker documentation
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(jaraco-packaging)

%description -n python-%{pkg_name}-doc
Documentation for rst.linker
%endif

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel
%if %{with docs}
# generate html docs
# this package requires itself to build docs :/
PYTHONPATH=./ sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install
%pyproject_save_files rst

%check
%pytest

%files -n python3-%{pkg_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%if %{with docs}
%files -n python-%{pkg_name}-doc
%license LICENSE
%doc html
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.4.0-14
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.4.0-13
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.4.0-11
- Rebuilt for Python 3.14

* Fri Mar 14 2025 Lumír Balhar <lbalhar@redhat.com> - 2.4.0-10
- Fix compatibility with the latest setuptools

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Nov 02 2024 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-8
- Generate BuildRequires dynamically
- Drop unneeded build dependency on python3dist(toml)
- Drop duplicate runtime dependency on python3-dateutil

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 2.4.0-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.4.0-2
- Rebuilt for Python 3.12

* Wed Feb 08 2023 Dan Radez <dradez@redhat.com> - 2.4.0-1
- update to 2.4.0 rhbz#2165203

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Aug 28 2022 Dan Radez <dradez@redhat.com> - 2.3.1-1
Update to 2.3.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.3.0-2
- Rebuilt for Python 3.11

* Thu Mar 31 2022 Dan Radez <dradez@redhat.com> - 2.3.0-1
Update to 2.3.0

* Tue Feb 08 2022 Dan Radez <dradez@redhat.com> - 2.2.0-6
- Don't delete egginfo

* Tue Jan 25 2022 Dan Radez <dradez@redhat.com> - 2.2.0-5
- re-enabling checks

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.2.0-2
- Rebuilt for Python 3.10

* Fri Apr 30 2021 Dan Radez <dradez@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Dan Radez <dradez@redhat.com> - 2.1.1-1
- Update to 2.1.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-2
- Rebuilt for Python 3.9

* Wed Feb 12 2020 Dan Radez <dradez@redhat.com> - 2.0.0-1
- Update to 2.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.11-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Tue Aug 20 2019 Dan Radez <dradez@redhat.com> - 1.11-2
- removing the sed . to _ it's confusing and not needed

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.11-2
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Dan Radez <dradez@redhat.com> - 1.11-1
- updating to 1.11

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 08 2019 Dan Radez <dradez@redhat.com> - 1.10-4
- fixing egg info

* Mon Apr 08 2019 Dan Radez <dradez@redhat.com> - 1.10-3
- fixing dep to prep for enabling docs build

* Fri Apr 05 2019 Dan Radez <dradez@redhat.com> - 1.10-2
- adding py3 subpackage.

* Wed May 02 2018 Dan Radez <dradez@redhat.com> - 1.10-1
- Initial package.
