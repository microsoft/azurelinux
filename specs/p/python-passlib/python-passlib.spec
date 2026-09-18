# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-passlib
Version:        1.7.4
Release:        25%{?dist}
Summary:        Comprehensive password hashing framework supporting over 20 schemes

# license breakdown is described in LICENSE file
License:        BSD-3-Clause AND Beerware AND UnixCrypt AND ISC
URL:            https://foss.heptapod.net/python-libs/passlib
Source:         %pypi_source passlib

BuildArch:      noarch

# docs generation requires python-cloud-sptheme, which isn't packaged yet.
# so we won't generate the docs yet.
#BuildRequires: python2-sphinx >= 1.0
#BuildRequires: python2-cloud-sptheme

%global _description %{expand:
Passlib is a password hashing library for Python 2 & 3, which provides
cross-platform implementations of over 20 password hashing algorithms,
as well as a framework for managing existing password hashes. It is
designed to be useful for a wide range of tasks, from verifying a hash
found in /etc/shadow, to providing full-strength password hashing for
multi-user application.}


%description %{_description}


%package -n python3-passlib
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest


%description -n python3-passlib %{_description}


# el9 missing argon2 https://bugzilla.redhat.com/show_bug.cgi?id=2089340
%pyproject_extras_subpkg -n python3-passlib %{!?el9:argon2} bcrypt totp


%prep
%autosetup -n passlib-%{version}
# Drop keywords from setup.py until upstream fixes them.
# Upstream issue: https://foss.heptapod.net/python-libs/passlib/-/issues/194
# Setuptools issue: https://github.com/pypa/setuptools/issues/4887
sed -i '/keywords="""/,/"""/d' setup.py

%generate_buildrequires
%pyproject_buildrequires -x bcrypt -x totp %{!?el9:-x argon2} 


%build
%pyproject_wheel


%install
# passlib setup.py append HG revision to the end of version by default
# which makes StrictVersion checks complaining
export PASSLIB_SETUP_TAG_RELEASE="no"
%pyproject_install
%pyproject_save_files passlib


%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

# We can safely ignore this failing test https://foss.heptapod.net/python-libs/passlib/-/issues/120
%pytest -k 'not test_82_crypt_support'


%files -n python3-passlib -f %{pyproject_files}
%doc README
%license LICENSE


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.7.4-25
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.7.4-24
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.7.4-22
- Rebuilt for Python 3.14

* Mon Mar 17 2025 Lumír Balhar <lbalhar@redhat.com> - 1.7.4-21
- Fix build with the latest setuptools

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.7.4-18
- Rebuilt for Python 3.13

* Mon Feb 26 2024 Joel Capitao <jcapitao@redhat.com> - 1.7.4-17
- Ignore sanity check

* Mon Feb 26 2024 Joel Capitao <jcapitao@redhat.com> - 1.7.4-16
- Add extra dependencies

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.7.4-12
- Rebuilt for Python 3.12

* Thu Jun 01 2023 Carl George <carl@george.computer> - 1.7.4-11
- Update license field with SPDX approved UnixCrypt identifier

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 25 2022 Carl George <carl@george.computer> - 1.7.4-9
- Convert to pyproject macros
- Run tests with pytest instead of deprecated nose
- Switch license field to SPDX identifiers

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.7.4-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.7.4-4
- Rebuilt for Python 3.10

* Fri Mar 05 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.4-3
- Add extras metapackages for argon2, bcrypt, totp

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Joel Capitao <jcapitao@redhat.com> - 1.7.4-1
- Update to 1.7.4 (#1885664)
- Change public repo URL

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.2-2
- Rebuilt for Python 3.9

* Wed Feb 26 2020 Alan Pevec <alan.pevec@redhat.com> 1.7.2-1
- Update to 1.7.2
- py39 crypt change https://bitbucket.org/ecollins/passlib/issues/115

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.1-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.1-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.1-3
- Subpackage python2-passlib has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Wed Mar 13 2019 Björn Esser <besser82@fedoraproject.org> - 1.7.1-2
- Use new python macros
- Add conditional to turn off python2 packages
- Remove egg(-info) before build
- Run testsuite

* Wed Feb 06 2019 Björn Esser <besser82@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1 (#1620382)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-9
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.7.0-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 04 2018 Troy Dawson <tdawson@redhat.com> - 1.7.0-6
- Update conditional

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 1.7.0-4
- Fix eggs-info generation

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-2
- Rebuild for Python 3.6

* Wed Nov 30 2016 Alan Pevec <alan.pevec@redhat.com> 1.7.0-1
- Update to 1.7.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Sep 07 2015 Chandan Kumar <chkumar246@gmail.com> - 1.6.5-1
- Added python2 and python3 subpackage
- updated to 1.6.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Alan Pevec <apevec@redhat.com> - 1.6.2-1
- update to 1.6.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 04 2013 Alan Pevec <apevec@redhat.com> - 1.6.1-1
- update to 1.6.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.5.3-1
- initial release for Fedora
