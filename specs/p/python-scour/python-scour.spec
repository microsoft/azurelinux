# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global modname scour
%global sum     An SVG scrubber

Name:               python-scour
Version:            0.38.2
Release: 17%{?dist}
Summary:            %{sum}

# All files are Apache-2.0 except scour/svg_regex.py
# which is BSD-3-Clause
License:            Apache-2.0 AND BSD-3-Clause
URL:                https://github.com/scour-project/scour
Source0:            %{url}/archive/v%{version}/%{modname}-%{version}.tar.gz

BuildRequires:      python3-devel
BuildRequires:      python3-setuptools
# Tests
BuildRequires:      python3-six
BuildRequires:      python3-pytest
BuildArch: noarch

%global _description %{expand:
Scour is an SVG optimizer/cleaner written in Python that reduces the
size of scalable vector graphics by optimizing structure and removing
unnecessary data.

It can be used to create streamlined vector graphics suitable for web
deployment, publishing/sharing or further processing.

The goal of Scour is to output a file that renders identically at a
fraction of the size by removing a lot of redundant information created
by most SVG editors. Optimization options are typically lossless but can
be tweaked for more aggressive cleaning.}


%description %_description


%package -n python3-%{modname}
Summary:            %{sum}
%{?python_provide:%python_provide python3-%{modname}}
Requires: python3-packaging

%description -n python3-%{modname}
%_description


%prep
%autosetup -n %{modname}-%{version}

# Better safe than sorry
find . -type f -name '*.py' -exec sed -i /env\ python/d {} ';'
find . -type f -name '*.py' -exec sed -i /env\ python/d {} ';'

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{modname}


%check
%pyproject_check_import
%pytest


%files -n python3-%{modname} -f %{pyproject_files}
%{_bindir}/scour
%doc README.md
%doc HISTORY.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.38.2-16
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.38.2-15
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.38.2-13
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 14 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.38.2-11
- Modernize packaging.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.38.2-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Sep 09 2023 Benson Muite <benson_muite@emailplus.org> - 0.38.2-6
- Use new Python build macros

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.38.2-4
- Rebuilt for Python 3.12

* Sun Mar 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.38.2-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.38.2-1
- 0.38.2

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.38.1-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.38.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.38.1
- 0.38.1

* Tue Aug 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.38-1
- 0.38

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 0.37-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.37-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 28 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.37-4
- Drop Python 2.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.37-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Gwyn Ciesla <limburgher@gmail.com> - 0.37-1
- 0.37

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.35-8
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.35-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.35-3
- Rebuild for Python 3.6

* Fri Oct 28 2016 Jon Ciesla <limburgher@gmail.com> - 0.35-2
- Fix Source0.

* Fri Oct 28 2016 Jon Ciesla <limburgher@gmail.com> - 0.35-1
- Initial package.
