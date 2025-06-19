# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
%bcond_without doc_pdf
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:           python-pyperclip
Version:        1.8.2
Release:        12%{?dist}
Summary:        A cross-platform clipboard module for Python

License:        BSD-3-Clause
URL:            https://github.com/asweigart/pyperclip
Source0:        %{pypi_source pyperclip}
BuildArch:      noarch

%global common_description %{expand:
Pyperclip is a cross-platform Python module for copy and paste clipboard
functions.}

%description %{common_description}


%package -n     python3-pyperclip
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools

# While upstream runs tests directly with Python/unittest, using pytest as the
# runner allows us to more easily skip tests.
BuildRequires:  python3dist(pytest)

%description -n python3-pyperclip %{common_description}

%package -n python-pyperclip-doc
Summary:        Pyperclip documentation
BuildRequires:  python3dist(sphinx)
BuildRequires:  make

%description -n python-pyperclip-doc
Documentation for pyperclip


%prep
%autosetup -p1 -n pyperclip-%{version}
# Fix ends of line encoding
sed -i 's/\r$//' README.md docs/*

%build
%py3_build
# generate html docs 
PYTHONPATH=${PWD} sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

%check
%global __pytest /usr/bin/xvfb-run -a %{python3} -m pytest
# Explicitly skip backends that we know will fail in the mock environment if
# their dependencies happen to be present. See notes in the BuildRequires.
k="${k-}${k+ and }not TestGtk"
k="${k-}${k+ and }not TestKlipper"
k="${k-}${k+ and }not TestWlCLipboard"
k="${k-}${k+ and }not TestXSel"
%pytest -k "${k-}" -v

%files -n python3-pyperclip
%license LICENSE.txt
%doc AUTHORS.txt
%doc CHANGES.txt
%doc README.md
%{python3_sitelib}/pyperclip
%{python3_sitelib}/pyperclip-%{version}-py%{python3_version}.egg-info

%files -n python-pyperclip-doc
%license LICENSE.txt

%changelog
* Mon Jun 16 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.8.2-12
- Initial Azure Linux import from Fedora 42 (license: MIT).
- License verified

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.8.2-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 1.8.2-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.2-3
- Update License to SPDX

* Fri Aug 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.2-2
- Enable running most of the graphical tests
- Switch Sphinx documentation to PDF to sidestep guidelines issues

* Mon Aug 08 2022 Jonathan Wright <jonathan@almalinux.org> - 1.8.2-1
- Update to 1.8.2

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.8.0-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.8.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Ken Dreyer <kdreyer@redhat.com> - 1.8.0-1
- Update to 1.8.0 (rhbz#1697423)
- Use non-git autosetup for simplicity

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-3
- Subpackage python2-pyperclip has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 25 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.6.4-1
- Initial package.
