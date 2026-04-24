# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without tests

Name:		python-lexicon
Version:	3.0.0
Release: 4%{?dist}
Summary:	Powerful dict subclass(es) with aliasing and attribute access
License:	BSD-2-Clause
URL:		https://github.com/bitprophet/lexicon
Source0:	https://github.com/bitprophet/lexicon/archive/%{version}/lexicon-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python3-devel

%if %{with tests}
# For test suite
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-relaxed
%endif

%description
Lexicon is a simple collection of dict sub-classes providing extra power.

%package -n python3-lexicon
Summary:	Powerful dict subclass(es) with aliasing and attribute access

%description -n python3-lexicon
Lexicon is a simple collection of dict sub-classes providing extra power.

%prep
%setup -q -n lexicon-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%if %{with tests}
%check
%pytest
%endif

%files -n python3-lexicon
%license LICENSE
%doc docs/changelog.rst README.rst
%{python3_sitelib}/lexicon/
%{python3_sitelib}/lexicon-%{version}.dist-info/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.0.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.0.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug  4 2025 Paul Howarth <paul@city-fan.org> - 3.0.0-1
- Update to 3.0.0
  - Dropped support for Python <3.9
  - Modernized project metadata re: Python interpreters, development

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul  8 2025 Paul Howarth <paul@city-fan.org> - 2.0.1-17
- Stop using deprecated %%py3_build/%%py3_install macros (rhbz#2377852)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.0.1-16
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.1-13
- Rebuilt for Python 3.13

* Thu Apr 11 2024 Paul Howarth <paul@city-fan.org> - 2.0.1-12
- Attempt to fix for pytest 8 (rhbz#2274500)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.1-8
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 02 2022 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-6
- Use pytest-relaxed, to avoid a transitive dependency on deprecated nose

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.1-4
- Rebuilt for Python 3.11

* Thu Apr 28 2022 Major Hayden <major@mhtx.net> - 2.0.1-3
- Disable spec-based tests in EPEL 9.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Sep 11 2021 Paul Howarth <paul@city-fan.org> - 2.0.1-1
- Update to 2.0.1
  - Dropped support for Python <3.6
  - Added a _version submodule and imported its dunder-attributes into the top
    level module
  - Migrated CI to CircleCI (from Travis)
  - Migrated tests to pytest(-relaxed)
  - Moved changelog to stub Sphinx project for Releases plugin
  - Changed README to ReStructured Text (from Markdown)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.0.0-14
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 11 2019 Paul Howarth <paul@city-fan.org> - 1.0.0-9
- Run the test suite
- Cosmetic spec changes

* Tue Oct 01 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-8
- Subpackage python2-lexicon has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 11 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0
- Revamp the spec to use the new python guidelines

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 01 2014 Athmane Madjoudj <athmane@fedoraproject.org> - 0.2.0-1
- Initial spec
