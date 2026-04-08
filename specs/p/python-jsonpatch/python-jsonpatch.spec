# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name jsonpatch

Name:           python-%{pypi_name}
Version:        1.33
Release:        11%{?dist}
Summary:        Applying JSON Patches in Python

License:        BSD-3-Clause
URL:            https://github.com/stefankoegl/python-json-patch
Source0:        https://pypi.io/packages/source/j/jsonpatch/%{pypi_name}-%{version}.tar.gz
# tarball from pypi does not include file tests.js required for a specific test.
# upstream issue https://github.com/stefankoegl/python-json-patch/issues/82
Patch0:         0001-Skip-unit-test-in-packaging.patch
# Avoid usage of unittest.makeSuite, removed from Python 3.13
Patch1:         https://github.com/stefankoegl/python-json-patch/pull/159.patch

BuildArch:      noarch

%description
Library to apply JSON Patches according to RFC 6902 - Python 2 build.

%package -n python3-%{pypi_name}
Summary:        Applying JSON Patches in Python 3

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-jsonpointer
Requires:       python3-jsonpointer

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Library to apply JSON Patches according to RFC 6902 - Python 3 build.

%prep
%setup -qn %{pypi_name}-%{version}
%patch -P 0 -p1
%patch -P 1 -p1


%build
%py3_build

%install
%py3_install
# remove jsondiff binary conflicting with python-jsondiff
# https://bugzilla.redhat.com/show_bug.cgi?id=2029805
rm %{buildroot}%{_bindir}/jsondiff
mv %{buildroot}%{_bindir}/jsonpatch %{buildroot}%{_bindir}/jsonpatch-%{python3_version}
ln -s ./jsonpatch-%{python3_version} %{buildroot}%{_bindir}/jsonpatch-3
ln -s ./jsonpatch-%{python3_version} %{buildroot}%{_bindir}/jsonpatch

%check
%{__python3} tests.py

%files -n python3-%{pypi_name}
%doc README.md
%license LICENSE
%{_bindir}/jsonpatch
%{_bindir}/jsonpatch-3*
%{python3_sitelib}/%{pypi_name}.py*
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.33-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.33-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.33-8
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.33-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 15 2023 Orion Poplawski <orion@nwra.com> - 1.33-1
- Update to 1.33

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.21-23
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.21-20
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec  7 2021 Alan Pevec <apevec AT redhat.com> - 1.21-18
- Drop conflicting jsondiff binary rhbz#2029805

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.21-16
- Rebuilt for Python 3.10

* Thu Mar  4 2021 Tim Landscheidt <tim@tim-landscheidt.de> - 1.21-15
- Fix mangled URL

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.21-12
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.21-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.21-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 27 2019 Yatin Karel <ykarel@redhat.com> - 1.21-7
- Disable python2 build in Fedora

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.21-5
- Drop explicit locale setting
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.21-3
- Rebuilt for Python 3.7

* Thu Mar 15 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.21-2
- Don't build Python 2 subpackage on EL > 7

* Tue Feb 6 2018 Alfredo Moralejo <amoralej@redhat.com> - 1.21-1
- Update to 1.21

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 1.14-5
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.14-2
- Rebuild for Python 3.6
- Added upstream patch for fixing python3 tests failures

* Mon Sep  5 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.14-1
- Upstream 1.14
- Update to latest python packaging guidelines

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 29 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2-5
- Introduce python3- subpackage.

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 1.2-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 15 2013 Alan Pevec <apevec@gmail.com> - 1.2-2
- add runtime dep on jsonpointer

* Fri Oct 11 2013 Alan Pevec <apevec@gmail.com> - 1.2-1
- Update to 1.2

* Fri Sep 13 2013 Alan Pevec <apevec@gmail.com> - 1.1-2
- review feedback: move %%check section, add missing build requirements

* Mon Jul 01 2013 Alan Pevec <apevec@gmail.com> - 1.1-1
- Initial package.
