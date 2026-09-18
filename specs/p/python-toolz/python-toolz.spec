# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname toolz
%global desc Toolz provides a set of utility functions for iterators, functions, and\
dictionaries. These functions interoperate well and form the building blocks\
of common data analytic operations. They extend the standard libraries\
itertools and functools and borrow heavily from the standard libraries of\
contemporary functional languages.\
\
Toolz provides a suite of functions which have the following functional\
virtues:\
\
    Composable: They interoperate due to their use of core data structures.\
    Pure: They don’t change their inputs or rely on external state.\
    Lazy: They don’t run until absolutely necessary, allowing them to support\
          large streaming data sets.\
\
Toolz functions are pragmatic. They understand that most programmers have\
deadlines.\
\
    Low Tech: They’re just functions, no syntax or magic tricks to learn\
    Tuned: They’re profiled and optimized\
    Serializable: They support common solutions for parallel computing\
\
This gives developers the power to write powerful programs to solve complex\
problems with relatively simple code. This code can be easy to understand\
without sacrificing performance. Toolz enables this approach, commonly\
associated with functional programming, within a natural Pythonic style\
suitable for most developers.

Name:           python-%{srcname}
Version:        1.0.0
Release:        6%{?dist}
Summary:        A functional standard library for Python

# The project is released under the BSD-3-Clause license.
# The _version.py file created by versioneer is licensed CC0-1.0; this will
# change to Unlicense when versioneer is updated to a newer version.
License:        BSD-3-Clause AND CC0-1.0
URL:            https://github.com/pytoolz/%{srcname}/
Source0:        https://github.com/pytoolz/toolz/archive/%{version}/%{srcname}-%{version}.tar.gz
# Add python 3.14 support
Patch:          %{url}/pull/592.patch
BuildArch:      noarch

%description
%{desc}


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        A functional standard library for Python %{python3_version}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest

%description -n python%{python3_pkgversion}-%{srcname}
%{desc}


%prep
%autosetup -p1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l toolz tlz


%check
# shakespeare test downloads a file
%pytest -v -k 'not test_shakespeare'


%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%license LICENSE.txt


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 25 2025 Jerry James  <loganjerry@gmail.com> - 1.0.0-3
- Add upstream patch for python 3.14 compatibility
- Update License field
- Use modern python build macros

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.0.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Oct 05 2024 Orion Poplawski <orion@nwra.com> - 1.0.0-1
- Update to 1.0.0

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.12.1-3
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Orion Poplawski <orion@nwra.com> - 0.12.1-1
- Update to 0.12.1

* Fri Jun 14 2024 Adam Williamson <awilliam@redhat.com> - 0.12.0-7
- Backport PR #582 to fix tests with Python 3.13
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.12.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 15 2022 Orion Poplawski <orion@nwra.com> - 0.12.0-1
- Update to 0.12.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Orion Poplawski <orion@nwra.com> - 0.11.2-5
- Add upstream patch for Python 3.11 support

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.11.2-4
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Orion Poplawski <orion@nwra.com> - 0.11.2-2
- Switch to pytest

* Fri Nov 12 2021 Orion Poplawski <orion@nwra.com> - 0.11.2-1
- Update to 0.11.2

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Orion Poplawski <orion@nwra.com> - 0.11.1-4
- Add upstream patch to fix python 3.10 test failure

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.11.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Orion Poplawski <orion@nwra.com> - 0.11.1-1
- Update to 0.11.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-2
- Rebuilt for Python 3.8

* Tue Jul 30 2019 Orion Poplawski <orion@nwra.com> - 0.10.0-1
- Update to 0.10.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 Carl George <carl@george.computer> - 0.9.0-8
- EPEL compatibility

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 27 2018 Orion Poplawski <orion@nwra.com> - 0.9.0-6
- Drop python 2 for Fedora 30+

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.9.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 30 2017 Orion Poplawski <orion@nwra.com> - 0.9.0-1
- Update to 0.9.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.8.0-2
- Rebuild for Python 3.6

* Thu Oct 20 2016 Orion Poplawski <orion@cora.nwra.com> - 0.8.0-1
- Update to 0.8.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr 5 2016 Orion Poplawski <orion@cora.nwra.com> - 0.7.4-1
- Initial package
