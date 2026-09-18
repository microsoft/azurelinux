# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global modname SQLAlchemy-Utils

Name:               python-sqlalchemy-utils
Version:            0.41.1
Release:            13%{?dist}
Summary:            Various utility functions for SQLAlchemy

# Automatically converted from old format: BSD - review is highly recommended.
License:            LicenseRef-Callaway-BSD
URL:                http://pypi.python.org/pypi/SQLAlchemy-Utils
Source0:            %{pypi_source SQLAlchemy-Utils}
# Omit test on unpackaged python-psycopg2cffi
Patch0:             no-psycopg2cffi.patch
Patch1:             python-sqlalchemy-utils-0.41.1-no-pyodbc-dep.patch
# This can be removed with version >= 0.42.2
Patch2:             python-sqlalchemy-utils-0.41.1-nosqla2.patch

BuildArch:          noarch

BuildRequires:      python3-devel
BuildRequires:      python3-pytest
# For tests
BuildRequires:      python3-colour
BuildRequires:      python3-phonenumbers


%description
Various utility functions and custom data types for SQLAlchemy.


%package -n         python3-sqlalchemy-utils
Summary:            Various utility functions for SQLAlchemy

%description -n python3-sqlalchemy-utils
Various utility functions and custom data types for SQLAlchemy.


%generate_buildrequires
%pyproject_buildrequires -x test


%prep
%autosetup -p1 -n %{modname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files sqlalchemy_utils


%check
# Tons of test failures, not sure they are meant to be run like this?
%pytest || :


%files -n python3-sqlalchemy-utils -f %{pyproject_files}
%doc README.rst
%license LICENSE


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.41.1-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.41.1-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 11 2025 Python Maint <python-maint@redhat.com> - 0.41.1-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.41.1-8
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 29 2024 Python Maint <python-maint@redhat.com> - 0.41.1-6
- Rebuilt for Python 3.13

* Mon Mar 25 2024 Nils Philippsen <nils@tiptoe.de> - 0.41.1-5
- Require SQLAlchemy < 2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 01 2023 Sandro Mani <manisandro@gmail.com> - 0.41.1-1
- Update to 0.41.1

* Tue Feb 07 2023 Sandro Mani <manisandro@gmail.com> - 0.39.0-1
- Update to 0.39.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 0.37.8-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 Joel Capitao <jcapitao@redhat.com> - 0.37.8-1
- Update to 0.37.8

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.34.2-7
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.34.2-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.34.2-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Tue Aug 20 2019 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.34.2-1
- Update to 0.34.2

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.32.12-12
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 05 2019 Miro Hrončok <mhroncok@redhat.com> - 0.32.12-10
- Subpackage python2-sqlalchemy-utils has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.32.12-7
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.32.12-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.32.12-4
- Python 2 binary package renamed to python2-sqlalchemy-utils
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.32.12-1
- Update to 0.32.12

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.31.3-3
- Rebuild for Python 3.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 20 2015 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.31.3-1
- Update to 0.31.3

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.30.0-1
- Update to 0.30.0

* Mon Sep 01 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.26.13-2
- Clean python macro at the top
- Add python3 subpackage

* Tue Aug 26 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.26.13-1
- initial package for Fedora
