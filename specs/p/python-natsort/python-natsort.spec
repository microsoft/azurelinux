# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname natsort

Name:           python-%{srcname}
Version:        8.4.0
Release:        8%{?dist}
Summary:        Python library that sorts lists using the "natural order" sort

License:        MIT
URL:            https://github.com/SethMMorton/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/n/%{srcname}/%{srcname}-%{version}.tar.gz

Suggests:       python3-pyicu

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  python3dist(hypothesis)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(semver)

%global _description \
Python module which provides "natural sorting".\
\
Under natural sorting, numeric sub-strings are compared numerically,\
and the other word characters are compared lexically.\
\
Example:\
unsorted:           ['a2', 'a9', 'a1', 'a4', 'a10']\
lexicographic sort: ['a1', 'a10', 'a2', 'a4', 'a9']\
natural sort:       ['a1', 'a2', 'a4', 'a9', 'a10']

%description %{_description}

%package -n python3-%{srcname}
Summary:	%{summary}
%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{srcname}

%check
%pyproject_check_import
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%{_bindir}/%{srcname}

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 8.4.0-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 8.4.0-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Robert Scheck <robert@fedoraproject.org> - 8.4.0-5
- Stop using deprecated %%py3_build/%%py3_install macros (#2377922)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 8.4.0-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Robert Scheck <robert@fedoraproject.org> - 8.4.0-1
- Update to 8.4.0 (#2020067)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 7.1.1-13
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Python Maint <python-maint@redhat.com> - 7.1.1-9
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 7.1.1-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 7.1.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 José Matos <jamatos@fedoraproject.org> - 7.1.1-1
- update to 7.1.1

* Sun Dec 13 2020 José Matos <jamatos@fedoraproject.org> - 7.1.0-1
- Update to 7.1.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 7.0.1-2
- Rebuilt for Python 3.9

* Thu Mar 19 2020 José Matos <jamatos@fedoraproject.org> - 7.0.1-1
- Update to 7.0.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 6.0.0-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 6.0.0-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 José Matos <jamatos@fedoraproject.org> - 6.0.0-5
- drop unneeded BR (pytest-flakes and pytest-cov)

* Fri Jul 19 2019 José Matos <jamatos@fedoraproject.org> - 6.0.0-4
- drop pytest-pep8 BR

* Sun May 12 2019 Orion Poplawski <orion@nwra.com> - 6.0.0-3
- Drop unneeded BR on pytest-cache

* Wed Apr 17 2019 José Matos <jamatos@fedoraproject.org> - 6.0.0-2
- Suggests: pyICU, to sort in a locale-dependent manner

* Wed Apr 17 2019 José Matos <jamatos@fedoraproject.org> - 6.0.0-1
- update to 6.0.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.3.3-2
- Subpackage python2-natsort has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Aug 28 2018 José Matos <jamatos@fedoraproject.org> - 5.3.3-1
- update to 5.3.3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.0.3-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 5.0.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May  4 2017 José Matos <jamatos@fedoraproject.org> - 5.0.3-1
- update to 5.0.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 5.0.1-2
- Rebuild for Python 3.6

* Fri Aug 12 2016 Igor Gnatenko <ignatenko@redhat.com> - 5.0.1-1
- Update to 5.0.1
- Trivial fixes in spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Feb  6 2016 José Matos <jamatos@fedoraproject.org> - 4.0.4-1
- update to 4.0.4
- add BR: python-pathlib, python-mock and python-hypothesis to run tests
- clean spec file to take advantage of the new available macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr  6 2015 José Matos <jamatos@fedoraproject.org> - 3.5.5-1
- update to 3.5.5 (3.5.2+ required by nikola)
- add new dependencies to deal with tests (python?-execnet)

* Fri Sep 26 2014 José Matos <jamatos@fedoraproject.org> - 3.5.1-1
- update to 3.5.1
- add check (tests) section

* Fri May 30 2014 José Matos <jamatos@fedoraproject.org> - 3.2.0-2
- change references to __python to __python2
- fix typo in the list of files of the python3 subpackage that
  referenced the version 2 directory

* Thu May 22 2014 José Matos <jamatos@fedoraproject.org> - 3.2.0-1
- initial package
