# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# It is not currently possible to build the documentation, because Fedora
# lacks sphinx_book_theme.

%global giturl  https://github.com/tsutsu3/linkify-it-py

Name:           python-linkify-it-py
Version:        2.0.3
Release: 9%{?dist}
Summary:        Link recognition library with full Unicode support

License:        MIT
URL:            https://linkify-it-py.readthedocs.io/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/v%{version}/linkify-it-py-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
This is a Python port of linkify-it [1], a link recognition library with
FULL unicode support.  It is focused on high quality link pattern
detection in plain text.  See a JavaScript demo [2].

References:
[1] https://github.com/markdown-it/linkify-it
[2] https://markdown-it.github.io/linkify-it/}

%description %_description

%package     -n python3-linkify-it-py
Summary:        Link recognition library with full Unicode support

%description -n python3-linkify-it-py %_description

%prep
%autosetup -n linkify-it-py-%{version}

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l linkify_it

%check
%pytest -v

%files -n python3-linkify-it-py -f %{pyproject_files}
%doc CHANGELOG.md README.md

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.0.3-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.0.3-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.0.3-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.3-2
- Rebuilt for Python 3.13

* Sun Feb  4 2024 Jerry James <loganjerry@gmail.com> - 2.0.3-1
- Version 2.0.3

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 24 2023 Karolina Surma <ksurma@redhat.com> - 2.0.2-4
- Stop removing the SPECPARTS directory, it doesn't exist

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 21 2023 Orion Poplawski <orion@nwra.com> - 2.0.2-2
- Remove empty SPECPARTS directory that breaks build

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.0.2-2
- Rebuilt for Python 3.12

* Tue May  2 2023 Jerry James <loganjerry@gmail.com> - 2.0.2-1
- Version 2.0.2

* Mon May  1 2023 Jerry James <loganjerry@gmail.com> - 2.0.1-1
- Version 2.0.1

* Thu Feb 23 2023 Jerry James <loganjerry@gmail.com> - 2.0.0-2
- Dynamically generate BuildRequires

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 25 2022 Jerry James <loganjerry@gmail.com> - 2.0.0-1
- Initial RPM
