# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		python-fluidity-sm
Version:	0.2.0
Release:	41%{?dist}
Summary:	State machine implementation for Python objects
License:	MIT
URL:		https://github.com/nsi-iff/fluidity
Source0:	https://github.com/nsi-iff/fluidity/archive/%{version}/fluidity-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python3-devel
# For test suite
BuildRequires:	python3-should_dsl

%description
State machine implementation for Python objects.

%package -n python3-fluidity-sm
Summary:	State machine implementation for Python objects

%description -n python3-fluidity-sm
State machine implementation for Python objects.

%prep
%setup -q -n fluidity-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%check
%{py3_test_envvars} %{python3} -m unittest spec/*.py

%files -n python3-fluidity-sm
%license LICENSE
%doc CHANGELOG README.rst
%{python3_sitelib}/fluidity/
%{python3_sitelib}/fluidity_sm-%{version}.dist-info/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.2.0-41
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.2.0-40
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul  8 2025 Paul Howarth <paul@city-fan.org> - 0.2.0-38
- Stop using deprecated %%py3_build/%%py3_install macros (rhbz#2377723)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.2.0-37
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 11 2024 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-35
- Drop unneeded BuildRequires for python3-spec and python3-nose, use unittest
- https://fedoraproject.org/wiki/Changes/DeprecateNose

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.2.0-33
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.2.0-29
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.2.0-26
- Rebuilt for Python 3.11

* Fri Apr 29 2022 Major Hayden <major@mhtx.net> - 0.2.0-25
- Disable spec-based tests in EPEL 9.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-23
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.2.0-22
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-19
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Paul Howarth <paul@city-fan.org> - 0.2.0-17
- Run the test suite
- Cosmetic spec changes

* Tue Oct 01 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-16
- Subpackage python2-fluidity-sm has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-15
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-11
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 11 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 0.2.0-9
- Revamp the spec file to use new python packaging guidelines

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

* Mon Dec 01 2014 Athmane Madjoudj <athmane@fedoraproject.org> 0.2.0-1
- Initial spec
