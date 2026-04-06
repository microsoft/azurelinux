# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkgname repoze.sphinx.autointerface
%global srcname %(tr . - <<< %{pkgname})

Name:           python-%{srcname}
Version:        1.0.0
Release:        11%{?dist}
Summary:        Auto-generate Sphinx API docs from Zope interfaces

License:        BSD-3-Clause-Modification
URL:            https://github.com/repoze/%{pkgname}
Source0:        https://github.com/repoze/%{pkgname}/archive/%{version}/%{pkgname}-%{version}.tar.gz
# Adapt to Sphinx 7.2+ and 8.2+
Patch0:         https://github.com/repoze/repoze.sphinx.autointerface/pull/22.patch

BuildArch:      noarch

BuildRequires:  python3-devel

# There is a test dependency loop, so we need a way to build this without tests
# repoze.sphinx.autointerface -> zope.testrunner -> zope.exceptions -> repoze.sphinx.autointerface
%bcond tests 1

%global common_desc %{expand:
This package defines an extension for the Sphinx documentation system.
The extension allows generation of API documentation by introspection of
zope.interface instances in code.}

%description %{common_desc}

%package -n python3-%{srcname}
Summary:        Auto-generate Sphinx API docs from Zope interfaces

%description -n python3-%{srcname} %{common_desc}

%prep
%autosetup -n %{pkgname}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-x test}

%build
%pyproject_wheel
rst2html --no-datestamp CHANGES.rst CHANGES.html
rst2html --no-datestamp README.rst README.html

%install
%pyproject_install
%pyproject_save_files -L repoze

%check
%pyproject_check_import
%if %{with tests}
export PYTHONPATH=$PWD/build/lib
zope-testrunner --test-path=$PWD/build/lib
%endif

%files -n python3-%{srcname}
%doc CHANGES.html CONTRIBUTORS.txt README.html
%license COPYRIGHT.txt LICENSE.txt
%{python3_sitelib}/repoze*

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.0-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.0-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 1.0.0-8
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.0-7
- Bootstrap for Python 3.14

* Thu Mar 20 2025 Jerry James <loganjerry@gmail.com> - 1.0.0-6
- Fix tests with Sphinx 8.2 (rhbz#2353342)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 1.0.0-3
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.0-2
- Bootstrap for Python 3.13

* Mon Jan 29 2024 Jerry James <loganjerry@gmail.com> - 1.0.0-1
- Version 1.0.0
- Drop upstreamed Sphinx 4 patch
- Convert License tag to SPDX
- Run the tests now that upstream provides some
- Add patch for compatibility with Sphinx 7.2.x

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.8-26
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.8-23
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Jerry James <loganjerry@gmail.com> - 0.8-20
- Add upstream patch for Sphinx 4 compatibility

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.8-19
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.8-16
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8-14
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8-13
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8-10
- Subpackage python2-repoze-sphinx-autointerface has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8-8
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.8-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.8-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Mar 29 2016 Jerry James <loganjerry@gmail.com> - 0.8-1
- New upstream version
- Use the license macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb  2 2016 Jerry James <loganjerry@gmail.com> - 0.7.1-5
- Comply with latest python packaging guidelines

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  3 2014 Jerry James <loganjerry@gmail.com> - 0.7.1-3
- Do not use the py3dir macro; see https://fedorahosted.org/fpc/ticket/435
- Remove the %%clean script

* Mon Jun  2 2014 Jerry James <loganjerry@gmail.com> - 0.7.1-2
- Conditionalize the python3 package

* Thu May 29 2014 Jerry James <loganjerry@gmail.com> - 0.7.1-1
- Initial RPM (bz 1102858)
