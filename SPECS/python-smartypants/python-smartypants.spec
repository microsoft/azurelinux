# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name smartypants

Name:           python-%{pypi_name}
Version:        2.0.1
Release:        27%{?dist}
Summary:        plug-in that easily translates ASCII punctuation characters into smart entities

License:        BSD-3-Clause AND BSD-2-Clause
URL:            https://github.com/leohemsted/smartypants.py
Source0:        %url/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

# https://github.com/leohemsted/smartypants.py/pull/21
Patch:          0001-Fix-regexps-and-tests-for-python3.12.patch

BuildRequires: make
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  python3-sphinx


%description
SmartyPants is a free web publishing plug-in for Movable
Type, Blosxom, and BBEdit that easily translates plain ASCII
punctuation characters into “smart” typographic punctuation HTML
entities.


%package -n     python3-%{pypi_name}
Summary:        %{summary}


%description -n python3-%{pypi_name}
SmartyPants is a free web publishing plug-in for Movable
Type, Blosxom, and BBEdit that easily translates plain ASCII
punctuation characters into “smart” typographic punctuation HTML
entities.


%package -n python-%{pypi_name}-doc
Summary:        python-smartypants documentation
%description -n python-%{pypi_name}-doc
Documentation for python-smartypants


%prep
%autosetup -p 1 -n %{pypi_name}.py-%{version}
# This is automatically on scripts in %%{_bindir}, but the tests run this
# script from the working directory so we need to fix it earlier.
%py3_shebang_fix smartypants


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel
# generate html documentation
cd docs
make html
# remove the sphinx-build leftovers
rm -rf _build/html/.{doctrees,buildinfo}


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}


%check
%{py3_test_envvars} %{python3} -m unittest discover --verbose --start-directory tests


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%doc CHANGES.rst
%{_bindir}/%{pypi_name}


%files -n python-%{pypi_name}-doc
%doc docs/_build/html
%license COPYING

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.0.1-27
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.0.1-26
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.0.1-24
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 15 2024 Carl George <carlwgeorge@fedoraproject.org> - 2.0.1-22
- Convert to pyproject macros
- Fix test invocation

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.1-20
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.0.1-16
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.1-13
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.1-10
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 José Matos <jamatos@fedoraproject.org> - 2.0.1-2
- fix source url, license short hand, description and summary.
- remove shebang lines and make smartypants a shebang line use python3.

* Sat Sep  1 2018 José Matos <jamatos@fedoraproject.org> - 2.0.1-1
- initial package.
