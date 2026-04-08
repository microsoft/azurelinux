# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-libnacl
Version:        2.1.0
Release:        12%{?dist}
Summary:        Python bindings for libsodium based on ctypes

# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://libnacl.readthedocs.org/
Source0:        %{pypi_source libnacl}

BuildArch:      noarch

Requires:       libsodium
BuildRequires:  python3-devel

# Testing
BuildRequires:  libsodium-devel
BuildRequires:  python3dist(pytest)

# Documentation
BuildRequires:  python3-sphinx
BuildRequires:  make

%global _description %{expand:
Python libnacl is used to gain direct access to the functions exposed by
Daniel J. Bernstein's nacl library via libsodium. It has been constructed to
maintain extensive documentation on how to use nacl as well as being completely
portable.}

%description %_description

%package -n python3-libnacl
Summary: %{summary}

%description -n python3-libnacl %_description


%prep
%autosetup -n libnacl-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

make -C doc man html

%install
%pyproject_install

%pyproject_save_files libnacl

install -D -m 644 doc/_build/man/libnacl.1 %{buildroot}%{_mandir}/man1/libnacl.1

%check
%{pytest}


%files -n python3-libnacl -f %{pyproject_files}
%license LICENSE
%doc README.rst
%doc doc/_build/html/
%{_mandir}/man1/libnacl.1*


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.1.0-12
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.1.0-11
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.1.0-9
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 2.1.0-7
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.1.0-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 07 2023 Jonny Heggheim <hegjon@gmail.com> - 2.1.0-2
- Include html documentation

* Sun Aug 06 2023 Jonny Heggheim <hegjon@gmail.com> - 2.1.0-1
- Updated to version 2.1.0

* Sat Aug 05 2023 Jonny Heggheim <hegjon@gmail.com> - 2.0.0-1
- Updated to version 2.0.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.8.0-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.8.0-2
- Rebuilt for Python 3.11

* Mon May 23 2022 Jonny Heggheim <hegjon@gmail.com> - 1.8.0-1
- Updated to version 1.8.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.7.2-4
- Rebuilt for Python 3.10

* Fri May 07 2021 Sérgio Basto <sergio@serjux.com> - 1.7.2-3
- (#1820150) Fix for TestRandomBytes.test_crypto_kdf_derive_from_key fails on
  32-bit x86

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 04 2020 Jonny Heggheim <hegjon@gmail.com> - 1.7.2-1
- Updated to version 1.7.2

* Mon Aug 31 2020 Sérgio Basto <sergio@serjux.com> - 1.7.1-6
- Please BuildRequire python3-setuptools explicitly

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 01 2020 Petr Viktorin <pviktori@redhat.com> - 1.7.1-3
- Remove encoding parameter json.loads for Python 3.9 compatibility

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Jonny Heggheim <hegjon@gmail.com> - 1.7.1-1
- Update to 1.7.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.1-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.1-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 Sérgio Basto <sergio@serjux.com> - 1.6.1-7
- Actually run unit tests

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Jonny Heggheim <hegjon@gmail.com> - 1.6.1-5
- Removed Python 2 sub-package
  https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.6.1-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 01 2017 Sérgio Basto <sergio@serjux.com> - 1.6.1-1
- Update to 1.6.1

* Thu Oct 05 2017 Sérgio Basto <sergio@serjux.com> - 1.6.0-1
- Update python-libnacl to 1.6.0
- Fix FTBFS with new libsodium

* Mon Oct 02 2017 Remi Collet <remi@fedoraproject.org> - 1.5.2-3
- rebuild for libsodium

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 (#1463028)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Jonny Heggheim <jonnyheggheim@sigaint.org> - 1.5.0-1
- inital package
