%bcond_without docs

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           python-testpath
Version:        0.6.0
Release:        19%{?dist}
Summary:        Test utilities for code working with files and commands

License:        BSD-3-Clause
URL:            https://github.com/jupyter/testpath

Source0:        %{pypi_source testpath}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core

#Test requirement
BuildRequires:  python3dist(pytest)

%if %{with docs}
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
%endif

%global _description %{expand:
Testpath is a collection of utilities for Python code working with files and
commands.

It contains functions to check things on the filesystem, and tools for
mocking system commands and recording calls to those.}

%description %_description

%package -n     python3-testpath
Summary:        %summary

%description -n python3-testpath %_description

%if %{with docs}
%package        doc
Summary:        %{name} documentation
%description doc
Documentation for %{name}.
%endif

%prep
%autosetup -n testpath-%{version}

# The exe files are only needed on Microsoft Windows
rm -f testpath/*.exe

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%if %{with docs}
# generate html docs
sphinx-build-3 doc html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install
%pyproject_save_files testpath

%check
%pytest

%files -n python3-testpath -f %{pyproject_files}
%doc README.rst
%license LICENSE

%if %{with docs}
%files doc
%doc html
%endif

%changelog
* Tue Feb 11 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.6.0-19
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.6.0-17
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 15 2023 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-8
- Fix the License tag (from MIT to BSD-3-Clause)
- The upstream project was relicensed in 0.4.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.6.0-6
- Rebuilt for Python 3.12

* Mon Feb 13 2023 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-5
- Convert to pyproject-rpm-macros
- The INSTALLER file now says "rpm" instead of "pip"

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.6.0-2
- Rebuilt for Python 3.11

* Wed Mar 09 2022 Charalampos Stratakis <cstratak@redhat.com> - 0.6.0-1
- Update to 0.6.0
- Fixes: rhbz#2058443

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Tomas Hrnciar <thrnciar@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.4.4-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.4-2
- Rebuilt for Python 3.9

* Thu May 14 2020 Tomas Hrnciar <thrnciar@redhat.com> - 0.4.4-1
- Update to 0.4.4

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-7
- Subpackage python2-testpath has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-1
- New version 0.3.1 (#1455375)
- Uses pathlib2 instead of pathlib

* Wed Mar 08 2017 Miro Hrončok <mhroncok@redhat.com> - 0.3-1
- initial package
