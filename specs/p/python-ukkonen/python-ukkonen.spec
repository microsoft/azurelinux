# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-ukkonen
Version:        1.0.1
Release: 21%{?dist}
Summary:        Implementation of bounded Levenshtein distance (Ukkonen)

License:        MIT
URL:            https://www.github.com/asottile/ukkonen
Source0:        %{url}/archive/v%{version}/ukkonen-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  python3-devel

# We don’t use %%tox for testing because it brings in unnecessary and
# unpackaged coverage dependencies.
BuildRequires:  python3dist(pytest)

%description
Implementation of bounded Levenshtein distance (Ukkonen) port

%package -n     python3-ukkonen
Summary:        %{summary}

%description -n python3-ukkonen
Implementation of bounded Levenshtein distance (Ukkonen) port

%prep
%autosetup -n ukkonen-%{version}
cp -p licenses/LICENSE LICENSE-upstream

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files ukkonen

%check
%pytest

%files -n python3-ukkonen -f %{pyproject_files}
%license LICENSE-upstream LICENSE
%doc README.md
%{python3_sitearch}/_ukkonen.abi3.so

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.1-20
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.1-19
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.1-17
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.1-14
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.1-13
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.0.1-9
- Rebuilt for Python 3.12

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.0.1-8
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.1-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.0.1-3
- Port to pyproject-rpm-macros

* Tue Nov 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.0.1-2
- Review fixes.

* Fri Nov 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.0.1-1
- Initial package.
