
%global pkgname qrcode

Name:           python-%{pkgname}
Version:        7.4.2
Release:        16%{?dist}
Summary:        Python QR Code image generator

License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/lincolnloop/python-qrcode
Source0:        https://files.pythonhosted.org/packages/source/q/qrcode/qrcode-7.4.2.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires: 	python3-pip
BuildRequires: 	python3-wheel
BuildRequires: 	python3-pluggy
BuildRequires:  python3-typing-extensions

# Explicit requires (#2271500)
Requires:       python3-pypng

# Comment out failing test
Patch0:         qrcode_test.patch
# Fix failure with Python3.12
Patch1:         qrcode_assert-has-calls.patch
# Make pypng requirement optional
# https://github.com/lincolnloop/python-qrcode/pull/338
Patch2:         qrcode-optional-pypng.patch

%description
This module uses the Python Imaging Library (PIL) to allow for the\
generation of QR Codes.

%package -n python3-%{pkgname}
Summary:        Python QR Code image generator
Obsoletes:      python3-qrcode-core < 7.4.2-2
Provides:       python3-qrcode-core = %{version}-%{release}

%description -n python3-%{pkgname}
This module uses the Python Imaging Library (PIL) to allow for the
generation of QR Codes. Python 3 version.

%generate_buildrequires
# RHEL does not include the extra test dependencies (coverage, pillow)
%pyproject_buildrequires %{?!rhel:-x test -x pil -x png}

%prep
%autosetup -n qrcode-%{version} -p1
# Remove shebang
sed -i '1d' qrcode/console_scripts.py

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files qrcode

#
# In previous iterations of the package, the qr script had been
# renamed to qrcode. This was an unnecessary change from upstream.
#
# We cary this symlink to maintain compat with old packages.
#
ln -s qr %{buildroot}%{_bindir}/qrcode

%check
%pytest -v

%files -n python3-%{pkgname} -f %{pyproject_files}
%doc README.rst CHANGES.rst
%license LICENSE
%{_bindir}/qr
%{_bindir}/qrcode
%{_mandir}/man1/qr.1*

%changelog
* Thu Feb 20 2025 Akhila Guruju <v-guakhila@microsoft.com> - 7.4.2-16
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified
- Added `BuildRequires: python3-pluggy python3-typing-extensions` to fix build.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 7.4.2-14
- Rebuilt for Python 3.13

* Thu Apr 25 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 7.4.2-13
- Skip more sys.stdout mock tests

* Tue Mar 26 2024 Sandro Mani <manisandro@gmail.com> - 7.4.2-12
- Fix requires

* Tue Mar 26 2024 Sandro Mani <manisandro@gmail.com> - 7.4.2-11
- Requires: python-pypng (#2271500)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Florence Blanc-Renaud <frenaud@redhat.com> - 7.4.2-8
- migrated to SPDX license

* Tue Jul 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 7.4.2-7
- Make pypng requirement optional

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 7.4.2-5
- Rebuilt for Python 3.12

* Tue May 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 7.4.2-4
- Migrate from tox to pytest, avoid unwanted deps in RHEL builds

* Fri May 12 2023 Sandro Mani <manisandro@gmail.com> - 7.4.2-3
- Add patch to fix test failures with py3.12

* Mon May 01 2023 Sandro Mani <manisandro@gmail.com> - 7.4.2-2
- Switch to pyproject macros

* Mon May 01 2023 Sandro Mani <manisandro@gmail.com> - 7.4.2-1
- Update to 7.4.2

* Tue Jan 04 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 7.3.1-3
- Opt in to rpmautospec

* Tue Jan 04 2022 Christian Heimes <cheimes@redhat.com> - 7.3.1-2
- Remove python-imaging build requirements for RHEL (#1935839)
- Run unit tests during build

* Thu Dec 09 2021 Sandro Mani <manisandro@gmail.com> - 7.3.1-1
- Update to 7.3.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 6.1-9
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 6.1-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 6.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 6.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 26 2019 Fabian Affolter <mail@fabian-affolter.ch> - 6.1-1
- Update to latest upstream release 6.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.1-14
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.1-12
- Rebuilt for Python 3.7

* Fri Mar 23 2018 Iryna Shcherbina <ishcherb@redhat.com> - 5.1-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Mar 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.1-10
- Also rename python-qrcode-core to python2-qrcode-core

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.1-8
- Python 2 binary package renamed to python2-qrcode
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 5.1-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jul 10 2015 Miro Hrončok <mhroncok@redhat.com> - 5.1-1
- Update to 5.1
- Introduce python3 subpackages (#1237118)
- Moved LICENSE from %%doc to %%license

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 16 2014 Nathaniel McCallum <npmccallum@redhat.com> - 5.0.1-2
- Make python-qrcode-core conflicts with python-qrcode < 5.0

* Wed Sep 10 2014 Nathaniel McCallum <npmccallum@redhat.com> - 5.0.1-1
- Update to 5.0.1

* Tue Sep 09 2014 Nathaniel McCallum <npmccallum@redhat.com> - 2.4.1-7
- Create -core subpackage for minimal dependencies

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Michel Salim <salimma@fedoraproject.org> - 2.4.1-2
- Clean up spec, removing unnecessary declarations
- Rename tool in %%{_bindir} to the less ambiguous qrcode

* Sat Jun  2 2012 Michel Salim <salimma@fedoraproject.org> - 2.4.1-1
- Initial package

