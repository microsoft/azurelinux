# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-pam
Version:        2.0.2
Release: 17%{?dist}
Summary:        Pure Python interface to the Pluggable Authentication Modules system on Linux
License:        MIT
URL:            https://github.com/FirefighterBlu3/python-pam
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel

# https://github.com/FirefighterBlu3/python-pam/pull/49
# Don't ship pam/pam.py, which appears to be solely a footgun
Patch:          0001-Don-t-ship-pam.py-in-the-module.patch
# https://github.com/FirefighterBlu3/python-pam/pull/47
# Drop use of six, we haven't supported Python 2 for years
# This was an undeclared dependency, seems better to drop it
# than declare it
# Modified to correct the indent issue and drop changes to pam.py
# since the prior patch demotes it to an example
Patch:          47-mod.patch

%generate_buildrequires
%pyproject_buildrequires

%description
This module provides an authenticate function that allows the caller to
authenticate a given username / password against the PAM system on Linux.

%package -n python3-pam
Summary:        Pure Python interface to the Pluggable Authentication Modules system on Linux
%{?python_provide:%python_provide python3-pam}

%description -n python3-pam
This module provides an authenticate function that allows the caller to
authenticate a given username / password against the PAM system on Linux.

%prep
%autosetup -p1

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l pam

%check
%pyproject_check_import

%files -n python3-pam -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.0.2-16
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.0.2-15
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 04 2025 Adam Williamson <awilliam@redhat.com> - 2.0.2-13
- Backport PR #47 to drop use of (and undeclared dep on) six
- Backport PR #49 to drop unused footgun pam.py

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.0.2-12
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.2-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.2-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.2-2
- Rebuilt for Python 3.11

* Wed May 25 2022 Aurelien Bompard <abompard@fedoraproject.org> - 2.0.2-1
- Version 2.0.2

* Mon Mar 14 2022 Juan Orti Alcaine <jortialc@redhat.com> - 2.0.0-1
- Version 2.0.0 (#2063598)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.8.4-11
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.8.4-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 Juan Orti Alcaine <jortialc@redhat.com> - 1.8.4-6
- Drop python2 support

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.4-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.4-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Juan Orti Alcaine <jorti@fedoraproject.org> - 1.8.4-1
- Version 1.8.4

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.8.3-2
- Rebuilt for Python 3.7

* Wed May 16 2018 Juan Orti Alcaine <jorti@fedoraproject.org> - 1.8.3-1
- Version 1.8.3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 01 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 1.8.2-9
- Python3 changes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.8.2-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 1.8.2-4
- Use python_provide macro

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 1.8.2-1
- Switch to fork from David Ford, previous source was unmaintained since 2009
- Update to 1.8.2
- Add python3 subpackage

* Tue Aug 12 2014 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.1.4-2
- Add support for EPEL6.

* Wed Jun 11 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-1
- Bug #1104258 update to 0.1.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.1.3-1
- Initial packaging
