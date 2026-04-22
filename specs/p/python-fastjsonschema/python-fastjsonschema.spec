# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-fastjsonschema
Version:        2.21.2
Release: 3%{?dist}
Summary:        Fastest Python implementation of JSON schema

License:        BSD-3-Clause
URL:            https://github.com/horejsek/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
fastjsonschema implements validation of JSON documents by JSON schema.
The library implements JSON schema drafts 04, 06 and 07.
The main purpose is to have a really fast implementation.}

%description %_description

%package -n     python3-fastjsonschema
Summary:        %{summary}

%description -n python3-fastjsonschema %_description

%prep
%autosetup -p1 -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files fastjsonschema

%check
%pytest -m "not benchmark"

%files -n python3-fastjsonschema -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.21.2-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Sep 03 2025 Packit <hello@packit.dev> - 2.21.2-1
- Update to 2.21.2
- Resolves rhbz#2388669

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.21.1-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.21.1-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 02 2024 Packit <hello@packit.dev> - 2.21.1-1
- Update to 2.21.1
- Resolves rhbz#2329260

* Tue Sep 03 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.20.0-1
- Update to 2.20.0
- Fixes rhbz#2292496

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.19.1-3
- Rebuilt for Python 3.13

* Mon Apr 15 2024 Lumír Balhar <lbalhar@redhat.com> - 2.19.1-2
- Fixed compatibility with pytest 8

* Tue Feb 13 2024 Packit <hello@packit.dev> - 2.19.1-1
- Update to 2.19.1
- Resolves rhbz#2241605

* Fri Jan 26 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.18.0-4
- Avoid tox dependency

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 11 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.18.0-1
- Update to 2.18.0
- Fixes: rhbz#2128071

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.16.3-2
- Rebuilt for Python 3.12

* Mon Mar 20 2023 Jerry James <loganjerry@gmail.com> - 2.16.3-1
- Version 2.16.3
- Convert License tag to SPDX

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jul 25 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.16.1-1
- Update to 2.16.1
- Fixes: rhbz#2107889

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.15.3-3
- Rebuilt for Python 3.11

* Tue Apr 05 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.15.3-2
- Backport patch to fix failing test

* Mon Jan 31 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.15.3-1
- Update to 2.15.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.1-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Tomas Hrnciar <thrnciar@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.15.0-2
- Rebuilt for Python 3.10

* Thu Feb  4 09:47:59 CET 2021 Tomas Hrnciar <thrnciar@redhat.com> - 2.15.0-1
- Update 2.15.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 19 2020 Tomas Hrnciar <thrnciar@redhat.com> - 2.14.5-1
- Initial package
