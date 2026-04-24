# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pyqt_builder

Name:           PyQt-builder
Version:        1.19.0
Release: 2%{?dist}
Summary:        The PEP 517 compliant PyQt build system

License:        BSD-2-Clause
URL:            https://www.riverbankcomputing.com/software/pyqt/
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel

%description
PyQt-builder is the PEP 517 compliant build system for PyQt and projects that
extend PyQt. It extends the sip build system and uses Qt's qmake to perform the
actual compilation and installation of extension modules.Projects that use
PyQt- builder provide an appropriate pyproject.toml file and an optional
project.py.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pyqtbuild
# These dll files are from openssl and microsoft visiual studio
# While we can redistribute them, we don't have source and it's 
# unlikely anyone will want to bundle a windows executable from linux.
rm -rf %{buildroot}/%{python3_sitelib}/pyqtbuild/bundle/dlls
sed -r -i '/\/pyqtbuild\/bundle\/dlls/d' %{pyproject_files}

%check
%py3_check_import pyqtbuild

%files -f %{pyproject_files}
%license LICENSE
%{_bindir}/pyqt-bundle
%{_bindir}/pyqt-qt-wheel

%changelog
* Mon Oct 13 2025 Jan Grulich <jgrulich@redhat.com> - 1.19.0-1
- 1.19.0

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.18.2-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.18.2-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 08 2025 Python Maint <python-maint@redhat.com> - 1.18.2-2
- Rebuilt for Python 3.14

* Sat Jun 07 2025 Jan Grulich <jgrulich@redhat.com> - 1.18.2-1
- 1.18.2

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.18.1-2
- Rebuilt for Python 3.14

* Wed Mar 19 2025 Scott Talbert <swt@techie.net> - 1.18.1-1
- Update to new upstream release 1.18.1 (#2347432)

* Fri Mar 14 2025 Lumír Balhar <lbalhar@redhat.com> - 1.18.0-2
- Fix compatibility with the latest setuptools

* Wed Feb 19 2025 Scott Talbert <swt@techie.net> - 1.18.0-1
- Update to new upstream release 1.18.0 (#2343425)

* Wed Jan 22 2025 Scott Talbert <swt@techie.net> - 1.17.2-1
- Update to new upstream release 1.17.2 (#2334704)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Jan Grulich <jgrulich@redhat.com> - 1.17.0-1
- 1.17.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Scott Talbert <swt@techie.net> - 1.16.4-1
- Update to new upstream release 1.16.4 (#2293673)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.16.2-2
- Rebuilt for Python 3.13

* Wed May 01 2024 Scott Talbert <swt@techie.net> - 1.16.2-2
- Update to new upstream release 1.16.2 (#2272990)

* Sun Feb 04 2024 Scott Talbert <swt@techie.net> - 1.15.4-1
- Update to new upstream release 1.15.4 (#2252258)

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Nov 18 2023 Scott Talbert <swt@techie.net> - 1.15.3-1
- Update to new upstream release 1.15.3 (#2244187)

* Mon Jul 24 2023 Scott Talbert <swt@techie.net> - 1.15.2-1
- Update to new upstream release 1.15.2 (#2225119)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Scott Talbert <swt@techie.net> - 1.15.1-1
- Update to new upstream release 1.15.1 (#2210072)

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.15.0-2
- Rebuilt for Python 3.12

* Wed Apr 26 2023 Scott Talbert <swt@techie.net> - 1.15.0-1
- Update to new upstream release 1.15.0 (#2185560)

* Tue Jan 31 2023 Scott Talbert <swt@techie.net> - 1.14.1-1
- Update to new upstream release 1.14.1 (#2131649)
- Modernize python packaging

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Scott Talbert <swt@techie.net> - 1.13.0-1
- Update to new upstream release 1.13.0 (#2098289)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.12.2-3
- Rebuilt for Python 3.11

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Oct 30 2021 Scott Talbert <swt@techie.net> - 1.12.2-1
- Update to new upstream release 1.12.2 (#2018190)

* Tue Oct 12 2021 Scott Talbert <swt@techie.net> - 1.12.1-1
- Update to new upstream release 1.12.1 (#2013246)

* Mon Oct 04 2021 Scott Talbert <swt@techie.net> - 1.11.0-1
- Update to new upstream release (#2010060)

* Fri Sep 24 2021 Scott Talbert <swt@techie.net> - 1.10.3-2
- Fix license info (#2007385)

* Wed Jul 21 2021 Scott Talbert <swt@techie.net> - 1.10.3-1
- Update to new upstream release 1.10.3 (#1984602)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.10.0-2
- Rebuilt for Python 3.10

* Mon May 24 2021 Scott Talbert <swt@techie.net> - 1.10.0-1
- Update to latest upstream release; remove hard-code on sip5

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 29 2020 Kevin Fenzi <kevin@scrye.com> - 1.6.0-2
- Remove shipped dlls.

* Tue Dec 15 2020 Kevin Fenzi <kevin@scrye.com> - 1.6.0-1
- Initial package.
