# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global package_name pyfakefs

Name:           python-%{package_name}
Version:        5.10.2
Release: 2%{?dist}
Summary:        pyfakefs implements a fake file system that mocks the Python file system modules.
License:        Apache-2.0
URL:            http://pyfakefs.org
Source0:        https://pypi.io/packages/source/p/%{package_name}/%{package_name}-%{version}.tar.gz
BuildArch:      noarch


%description
pyfakefs implements a fake file system that mocks the Python file system
modules.
Using pyfakefs, your tests operate on a fake file system in memory without
touching the real disk. The software under test requires no modification to
work with pyfakefs.

%package -n python3-%{package_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{package_name}}

BuildRequires:  git-core
BuildRequires:  python3-devel
# For import check
BuildRequires:  python3-pytest

Requires:       python3-pytest

%description -n python3-%{package_name}
pyfakefs implements a fake file system that mocks the Python file system
modules.
Using pyfakefs, your tests operate on a fake file system in memory without
touching the real disk. The software under test requires no modification to
work with pyfakefs.

%prep
%autosetup -n %{package_name}-%{version} -S git

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{package_name}

%check
%pyproject_check_import

%files -n python3-%{package_name} -f %{pyproject_files}
%doc README.md

%changelog
* Thu Dec 04 2025 Orion Poplawski <orion@nwra.com> - 5.10.2-1
- Update to 5.10.2

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.9.2-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.9.2-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 11 2025 Orion Poplawski <orion@nwra.com> - 5.9.2-1
- Update to 5.9.2
- Use pyproject macros

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 5.8.0-2
- Rebuilt for Python 3.14

* Thu Mar 13 2025 Orion Poplawski <orion@nwra.com> - 5.8.0-1
- Update to 5.8.0

* Mon Feb 17 2025 Orion Poplawski <orion@nwra.com> - 5.7.4-1
- Update to 5.7.4

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 23 2024 Lumír Balhar <lbalhar@redhat.com> - 5.6.0-1
- Update to 5.6.0 (rhbz#2221762)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.2.4-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Orion Poplawski <orion@nwra.com> - 5.2.4-1
- Update to 5.2.4

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Orion Poplawski <orion@nwra.com> - 5.2.3-1
- Update to 5.2.3

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 5.2.2-2
- Rebuilt for Python 3.12

* Thu Apr 13 2023 Jonathan Wright <jonathan@almalinux.org> - 5.2.2-1
- Update to 5.2.2

* Thu Apr 13 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 5.2.1-1
- Update to 5.2.1
Fixes: rhbz#2183600

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Jonathan Wright <jonathan@almalinux.org> - 5.1.0-1
- Update to 5.1.0 rhbz#2127704
- Update license to SPDX

* Sun Aug 14 2022 Orion Poplawski <orion@nwra.com> - 5.0.0-1
- Update to 5.0.0 rhbz#2127704

* Sun Aug 14 2022 Orion Poplawski <orion@nwra.com> - 4.6.3-1
- Update to 4.6.3

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.5.6-2
- Rebuilt for Python 3.11

* Sat May 21 2022 Orion Poplawski <orion@nwra.com> - 4.5.6-1
- Update to 4.5.6

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.4.0-2
- Rebuilt for Python 3.10

* Mon Mar 15 2021 Orion Poplawski <orion@nwra.com> - 4.4.0-1
- Update to 4.4.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.5.8-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.5.8-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.5.8-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 11 2019 Orion Poplawski <orion@nwra.com> - 3.5.8-1
- Update to 3.5.8

* Sat Apr 27 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1-7
- Subpackage python2-pyfakefs has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 1 2017 David Moreau Simard <dmsimard@redhat.com> - 3.1-1
- First packaged version of pyfakefs
