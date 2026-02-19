%bcond_without check

Name:           cargo2rpm
Version:        0.3.2
Release:        2%{?dist}
Summary:        Translation layer between cargo and RPM
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://codeberg.org/rust2rpm/cargo2rpm
Source:         %{url}/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-devel
%if %{with check}
BuildRequires:  %{py3_dist pytest}
%endif

Requires:       cargo

%description
cargo2rpm implements a translation layer between cargo and RPM. It
provides a CLI interface (for implementing RPM macros and generators)
and a Python API (which rust2rpm is built upon).

%prep
%autosetup -n cargo2rpm -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files cargo2rpm

%check
%pyproject_check_import
%if %{with check}
%pytest
%endif

%files -f %{pyproject_files}
%doc README.md
%doc CHANGELOG.md
%{_bindir}/cargo2rpm

%changelog
* Fri Dec 26 2025 Aditya Singh <v-aditysing@microsoft.com> - 0.3.2-2
- Initial Azure Linux import from Fedora 44 (license: MIT).
- License verified. 

* Sat Dec 06 2025 Fabio Valentini <decathorpe@gmail.com> - 0.3.2-1
- Update to version 0.3.2; Fixes RHBZ#2419692

* Thu Nov 20 2025 Fabio Valentini <decathorpe@gmail.com> - 0.3.1-1
- Update to version 0.3.1; Fixes RHBZ#2416167

* Wed Nov 12 2025 Fabio Valentini <decathorpe@gmail.com> - 0.3.0-1
- Update to version 0.3.0; Fixes RHBZ#2403101

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.1.18-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.1.18-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.1.18-3
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 10 2024 Fabio Valentini <decathorpe@gmail.com> - 0.1.18-1
- Update to version 0.1.18; Fixes RHBZ#2317824

* Sun Sep 08 2024 Fabio Valentini <decathorpe@gmail.com> - 0.1.17-1
- Update to version 0.1.17; Fixes RHBZ#2310726

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.1.16-2
- Rebuilt for Python 3.13

* Fri May 24 2024 Fabio Valentini <decathorpe@gmail.com> - 0.1.16-1
- Update to version 0.1.16; Fixes RHBZ#2283015

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 08 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.15-1
- Update to version 0.1.15; Fixes RHBZ#2253432

* Fri Dec 01 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.14-1
- Update to version 0.1.14; Fixes RHBZ#2252412

* Thu Nov 02 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.13-1
- Update to version 0.1.13; Fixes RHBZ#2247679

* Fri Oct 06 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.12-1
- Update to version 0.1.12; Fixes RHBZ#2242404

* Sun Sep 24 2023 Robert-André Mauchin <zebob.m@gmail.com> - 0.1.9-1
- Update to version 0.1.9; Fixes RHBZ#2240213

* Mon Sep 18 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.8-1
- Update to version 0.1.8; Fixes RHBZ#2239513

* Mon Jul 31 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.7-1
- Update to version 0.1.7; Fixes RHBZ#2227751

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.1.5-2
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.5-1
- Update to version 0.1.5

* Thu Jun 01 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.4-2
- Avoid dependency on tox and run tests with pytest directly

* Wed May 17 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.4-1
- Update to version 0.1.4; Fixes RHBZ#2196881

* Mon Mar 06 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.3-1
- Update to version 0.1.3; Fixes RHBZ#2175302

* Thu Feb 16 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.2-1
- Update to version 0.1.2

* Thu Feb 16 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.1-2
- Update to more modern Python packaging

* Tue Feb 14 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.1-1
- Update to version 0.1.1

* Mon Feb 13 2023 Fabio Valentini <decathorpe@gmail.com> - 0.1.0-1
- Initial import (#2169233)
