# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-uc-micro-py
Version:        1.0.3
Release:        8%{?dist}
Summary:        Micro subset of Unicode data files for linkify-it.py projects

License:        MIT
URL:            https://github.com/tsutsu3/uc.micro-py
VCS:            git:%{url}.git
Source:         %{url}/archive/v%{version}/uc.micro-py-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
Micro subset of Unicode data files for linkify-it.py projects.  This is
a Python port of uc.micro (https://github.com/markdown-it/uc.micro).}

%description %_description

%package     -n python3-uc-micro-py
Summary:        Micro subset of Unicode data files for linkify-it.py projects

%description -n python3-uc-micro-py %_description

%prep
%autosetup -n uc.micro-py-%{version}

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l uc_micro

%check
%pytest -v

%files -n python3-uc-micro-py -f %{pyproject_files}
%doc CHANGELOG.md README.md

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.3-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.3-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.0.3-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.3-2
- Rebuilt for Python 3.13

* Fri Feb  9 2024 Jerry James <loganjerry@gmail.com> - 1.0.3-1
- Version 1.0.3

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.0.2-2
- Rebuilt for Python 3.12

* Tue May  2 2023 Jerry James <loganjerry@gmail.com> - 1.0.2-1
- Version 1.0.2

* Thu Feb 23 2023 Jerry James <loganjerry@gmail.com> - 1.0.1-2
- Dynamically generate BuildRequires

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 25 2022 Jerry James <loganjerry@gmail.com> - 1.0.1-1
- Initial RPM
