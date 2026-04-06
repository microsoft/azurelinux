# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name cppheaderparser

Name:           python-%{pypi_name}
Version:        2.7.4
Release:        21%{?dist}
Summary:        Parse C++ header files and generate a data structure

License:        BSD-3-Clause
URL:            http://senexcanis.com/open-source/cppheaderparser/
Source0:        %{pypi_source CppHeaderParser}
Patch0:         0001-cppheaderparser-silence-invalid-escape-sequence.patch

BuildArch:      noarch

%description
Parse C++ header files and generate a data structure representing the
class.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Parse C++ header files and generate a data structure representing the
class.

%prep
%autosetup -p1 -n CppHeaderParser-%{version}
rm -rf %{pypi_name}.egg-info
# Remove outdated parts (Python 2.x)
rm -rf CppHeaderParser/{examples,docs}
sed -i -e '/^#!\//, 1d' CppHeaderParser/CppHeaderParser.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files CppHeaderParser

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.txt README.html

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.7.4-21
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.7.4-20
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 14 2025 Tom Rix <Tom.Rix@amd.com> - 2.7.4-18
- Use pyproject macros

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.7.4-17
- Rebuilt for Python 3.14

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.7.4-14
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Tom Rix <trix@redhat.com> - 2.7.4-11
- Silence invalid escape sequence warnings
- Use spdx license

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.7.4-9
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.7.4-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.7.4-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 17 2020 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.4-1
- Initial package for Fedora
