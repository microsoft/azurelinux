# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname pid

%global common_description %{expand:
pid provides a PidFile class that manages PID files. PidFile features:
  - stale detection
  - locking using fcntl
  - chmod (default is 0o644)
  - chown
  - custom exceptions

PidFile can also be used as a context manager or a decorator.}

Name:           python-%{srcname}
Version:        3.0.4
Release: 5%{?dist}
Summary:        PID file management library

License:        Apache-2.0
URL:            https://github.com/trbs/pid
Source0:        %pypi_source

BuildArch:      noarch

%description %{common_description}

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}

BuildRequires:  python%{python3_pkgversion}-devel

# Test dependencies
BuildRequires:  python3dist(pytest)

%description -n python%{python3_pkgversion}-%{srcname} %{common_description}

%prep
# This needs to have a blank line after because of a bug in the EL6 macros
%autosetup -p1 -n %{srcname}-%{version}

rm -rf %{srcname}.egg-info

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
%pytest

%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc AUTHORS CHANGELOG README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.0.4-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.0.4-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul  9 2025 David Shea <reallylongword@gmail.com> - 3.0.4-1
- Update to 3.0.4
- Remove python2 subpackage
- Switch to pyproject macros

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.2.3-25
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.2.3-22
- Rebuilt for Python 3.13

* Mon Jan 29 2024 David Shea <reallylongword@gmail.com> - 2.2.3-21
- Migrate to SPDX license identifier

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.2.3-17
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.2.3-14
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 2.2.3-11
- Rebuilt for Python 3.10

* Mon Feb 08 2021 Charalampos Stratakis <cstratak@redhat.com> - 2.2.3-10
- Switch the test run from nose to pytest

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 2.2.3-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2.3-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2.3-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 Troy Dawson <tdawson@redhat.com> - 2.2.3-2
- Rebuilt to change main python from 3.4 to 3.6

* Tue Mar 05 2019 Carl George <carl@george.computer> - 2.2.3-1
- Latest upstream
- Build python3 subpackage on el6
- Run tests correctly

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-8
- Rebuilt for Python 3.7

* Thu Mar 22 2018 David Shea <dshea@redhat.com> - 2.1.1-7
- Remove the python2 package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.1-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 2.1.1-2
- Rebuild for Python 3.6

* Tue Nov 29 2016 David Shea <dshea@redhat.com> - 2.1.1-1
- Update to 2.1.1, which adds an optional allow_samepid parameter

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 2.0.1-3
- Rebuilt for Python3.5 rebuild

* Wed Aug 05 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.1-2
- Update to modern python packaging guidelines

* Tue Aug  4 2015 David Shea <dshea@redhat.com> - 2.0.1-1
- Initial package
