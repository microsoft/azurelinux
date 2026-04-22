# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pymssql
%global _description %{expand:A simple database interface for Python that builds on top of FreeTDS to provide
a Python DB-API (PEP-249) interface to Microsoft SQL Server.}

Name:           python-%{pypi_name}
Version:        2.3.9
Release: 2%{?dist}
Summary:        DB-API interface to Microsoft SQL Server

License:        LGPL-2.0-or-later
URL:            http://pymssql.org/
Source0:        %{pypi_source}

BuildRequires:  freetds-devel
BuildRequires:  gcc
BuildRequires:  krb5-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist cython}
# For easy patching of pyproject.toml
BuildRequires:  tomcli

# Testing is only possible after sqlalchemy is built and BuildRequires pymssql.
# This bcond allows to build this package without tests when necessary.
%bcond tests 1

%description
%{_description}


%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{_description}


%prep
%autosetup -n %{pypi_name}-%{version}

# Drop version constraint on setuptools/setuptools_scm
tomcli set pyproject.toml arrays replace "build-system.requires" "(setuptools(_scm\[toml\])?)\s*[><=]+.*" "\1"
sed -i -E 's/^(\s*setuptools(_scm\[toml\])?)\s*[><=]+.*$/\1/' setup.cfg %{?with_tests:dev/requirements-dev.txt}

# Drop unneeded dependencies not available in Fedora
tomcli set pyproject.toml arrays delitem "build-system.requires" "standard-distutils\b.*"
%{?with_tests:sed -i -E '/^\s*standard-distutils\b/d' dev/requirements-dev.txt}

%if 0%{?fedora} < 43
# Drop version constraint on setuptools/setuptools_scm
tomcli set pyproject.toml arrays replace "build-system.requires" "(Cython)\s*[><=]+.*" "\1"
sed -i -E 's/^(\s*cython)\s*[><=]+.*$/\1/' setup.cfg %{?with_tests:dev/requirements-dev.txt}

# setuptools < 77.0.3 doesn't support PEP 639
tomcli set pyproject.toml del "project.license"
%endif


%generate_buildrequires
%pyproject_buildrequires -r %{?with_tests:dev/requirements-dev.txt}


%build
LINK_FREETDS_STATICALLY=no %pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%check
%pyproject_check_import
%if 0%{?with_tests}
%pytest
%endif


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc ChangeLog.rst README.rst
%license LICENSE


%changelog
* Mon Nov 10 2025 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.3.9-1
- Update to 2.3.9

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.3.2-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.3.2-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Aug 05 2025 Charalampos Stratakis <cstratak@redhat.com> - 2.3.2-5
- Fix compatibility with Cython >= 3.1
- Fixes: rhbz#2377048

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 05 2025 Python Maint <python-maint@redhat.com> - 2.3.2-3
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.3.2-2
- Bootstrap for Python 3.14

* Sat Jan 25 2025 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 30 2024 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.3.1-1
- new version

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 2.3.0-3
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.3.0-2
- Bootstrap for Python 3.13

* Sat May 11 2024 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Sun Jan 28 2024 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.2.11-1
- Update to 2.2.11

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.2.10-1
- Update to 2.2.10

* Sun Sep 24 2023 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.2.8-1
- Update to 2.2.8

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 2.2.7-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.2.7-1
- Update to 2.2.7
- Switch license tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 2.2.5-2
- Rebuilt for Python 3.11

* Mon May 16 2022 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.2.5-1
- Update to 2.2.5

* Sat Jan 29 2022 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.2.4-1
- Update to 2.2.4

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jul 26 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.2.1-2
- Rebuilt for Python 3.10

* Thu Apr 22 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Sep 20 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.1.4-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.4-4
- Rebuilt for Python 3.8

* Tue Jul 30 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.1.4-3
- Fix build with Python >= 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 09 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 09 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.3-7
- Remove remaining bits of Python 2 legacy

* Thu Oct 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.3-6
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.3-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 10 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.1.3-2
- Use python2- prefix for Fedora dependencies

* Sun Jul  2 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.1.3-1
- Initial RPM release
