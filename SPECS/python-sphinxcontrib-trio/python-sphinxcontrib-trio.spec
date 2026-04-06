# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname sphinxcontrib-trio

Name:           python-%{srcname}
Version:        1.1.2
Release:        26%{?dist}
Summary:        Make Sphinx better at documenting Python functions and methods
# Automatically converted from old format: MIT or ASL 2.0 - review is highly recommended.
License:        LicenseRef-Callaway-MIT OR Apache-2.0
URL:            https://github.com/python-trio/sphinxcontrib-trio
Source0:        %{pypi_source}
Patch0:         python-sphinxcontrib-trio-1.1.2.patch
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-cssselect
BuildRequires:  python3-lxml
BuildRequires:  python3-pytest
BuildRequires:  %{_bindir}/rst2html
BuildRequires:  make
BuildArch:      noarch

%global desc                                                            \
This sphinx extension helps you document Python code that uses          \
async/await, or abstract methods, or context managers, or generators,   \
or ... you get the idea. It works by making sphinx's regular            \
directives for documenting Python functions and methods smarter and     \
more powerful. The name is because it was originally written for the    \
Trio project, and I'm not very creative. But don't be put off –         \
there's nothing Trio- or async-specific about this extension; any       \
Python project can benefit. (Though projects using async/await          \
probably benefit the most, since sphinx's built-in tools are            \
especially inadequate in this case.)

%description
%desc


%package -n python3-%{srcname}
Summary: %{summary}

%description -n python3-%{srcname}
%desc


%prep
%autosetup -p1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel
make -C docs html SPHINXBUILD=%{_bindir}/sphinx-build-3
rm -f docs/build/html/.buildinfo
rst2html README.rst README.html

%install
%pyproject_install
%pyproject_save_files -l sphinxcontrib_trio


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst README.html
%doc docs/build/html


%check
%pyproject_check_import

# https://github.com/python-trio/sphinxcontrib-trio/issues/398
%pytest -k 'not test_end_to_end'


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.1.2-26
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.1.2-25
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.2-23
- Update for current Python packaging guidelines.

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.1.2-22
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 23 2024 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.2-20
- Run tests (excluding one known to fail).
- Avoid globs in %%files.

* Tue Oct 22 2024 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.2-19
- Remove %%check section, as there are no tests.

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.1.2-18
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.1.2-16
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.1.2-12
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1.2-9
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep  2 2021 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.2-7
- Fix FTBFS with Sphinx 4.0.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.1.2-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.2-2
- Rebuilt for Python 3.9

* Wed May  6 2020 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.2-1
- Update to 1.1.2.

* Fri Apr 10 2020 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.1-1
- Update to 1.1.1.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-1
- Update to 1.1.0.
- Build docs.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 15 2019 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.2-1
- Update to 1.0.2.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-2
- Rebuilt for Python 3.7

* Wed Apr 25 2018 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.1-1
- New package.
