# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pyqt5_sip
%global _sip_api_major 12
%global _sip_api_minor 17
%global _sip_api %{_sip_api_major}.%{_sip_api_minor}

Name:           python-pyqt5-sip
Version:        12.17.1
Release:        1%{?dist}
Summary:        The sip module support for PyQt5

License:        BSD-2-Clause
URL:            https://www.riverbankcomputing.com/software/sip/
Source0:        %{pypi_source}

BuildRequires:  gcc
BuildRequires:  python3-devel

%global _description %{expand:
The sip extension module provides support for the PyQt5 package.
}

%description %_description

%package -n     python3-pyqt5-sip
Summary:        %{summary}
Provides: python3-pyqt5-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python3-pyqt5-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}

%description -n python3-pyqt5-sip %_description

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files PyQt5

%check
%py3_check_import PyQt5.sip

%files -n python3-pyqt5-sip -f %{pyproject_files}
%doc README

%changelog
* Wed Nov 05 2025 Jan Grulich <jgrulich@redhat.com> - 12.17.1-1
- 12.17.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 12.17.0-3
- Rebuilt for Python 3.14

* Fri Mar 14 2025 Lumír Balhar <lbalhar@redhat.com> - 12.17.0-1
- Fix compatibility with the latest setuptools

* Wed Feb 19 2025 Scott Talbert <swt@techie.net> - 12.17.0-1
- Update to new upstream release 12.17.0 (#2343423)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Dec 14 2024 Scott Talbert <swt@techie.net> - 12.16.1-1
- Update to new upstream release 12.16.1 (#2330773)

* Thu Aug 01 2024 Scott Talbert <swt@techie.net> - 12.15.0-3
- Update License tag to use SPDX identifiers

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Scott Talbert <swt@techie.net> - 12.15.0-1
- Update to new upstream release 12.15.0 (#2297896)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 12.13.0-4
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Scott Talbert <swt@techie.net> - 12.13.0-3
- Fix FTBFS with GCC 14

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Nov 18 2023 Scott Talbert <swt@techie.net> - 12.13.0-1
- Update to new upstream release 12.13.0 (#2244185)

* Mon Jul 24 2023 Scott Talbert <swt@techie.net> - 12.12.2-1
- Update to new upstream release 12.12.2 (#2225114)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 12.12.1-4
- Fix segfault with subclasses

* Fri Jun 16 2023 Scott Talbert <swt@techie.net> - 12.12.1-3
- Fix segfault at exit with Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 12.12.1-2
- Rebuilt for Python 3.12

* Wed Apr 26 2023 Scott Talbert <swt@techie.net> - 12.12.1-1
- Update to new upstream release 12.12.1 (#2185558)

* Tue Jan 31 2023 Scott Talbert <swt@techie.net> - 12.11.1-1
- Update to new upstream release 12.11.1 (#2165212)
- Modernize python packaging

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Scott Talbert <swt@techie.net> - 12.11.0-1
- Update to new upstream release 12.11.0 (#2074708)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 12.9.1-3
- Rebuilt for Python 3.11

* Sat Mar 12 2022 Scott Talbert <swt@techie.net> - 12.9.1-2
- Fix FTBFS with Python 3.11.0a6 (#2062145)

* Fri Feb 18 2022 Scott Talbert <swt@techie.net> - 12.9.1-1
- Update to new upstream release 12.9.1 (#2049165)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Scott Talbert <swt@techie.net> - 12.9.0-1
- Update to latest upstream release for sip 6

* Tue Jul 06 2021 Scott Talbert <swt@techie.net> - 12.8.1-2
- Correct sip-api provides (#1979409)

* Mon May 24 2021 Scott Talbert <swt@techie.net> - 12.8.1-1
- Initial package
