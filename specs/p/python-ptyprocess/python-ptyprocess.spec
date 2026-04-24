# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname ptyprocess

%bcond_without tests

Name:           python-ptyprocess
Version:        0.7.0
Release: 15%{?dist}
Summary:        Run a subprocess in a pseudo terminal

License:        ISC
URL:            https://github.com/pexpect/ptyprocess
Source:         %{pypi_source}

# Remove unittest.makeSuite, gone from Python 3.13
Patch:          https://github.com/pexpect/ptyprocess/pull/75.patch

BuildArch:      noarch

%description
Launch a subprocess in a pseudo terminal (pty), and interact with both the
process and its pty.

%package -n python3-ptyprocess
Summary:        Run a subprocess in a pseudo terminal
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-pytest
%endif

%description -n python3-ptyprocess
Launch a subprocess in a pseudo terminal (pty), and interact with both the
process and its pty.

%prep
%autosetup -p1 -n ptyprocess-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files ptyprocess

%if %{with tests}
%check
%{__python3} -m pytest -v
%endif

%files -n python3-ptyprocess -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.7.0-14
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7.0-13
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.7.0-11
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.7.0-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.7.0-4
- Rebuilt for Python 3.12

* Tue Jan 24 2023 Adam Williamson <awilliam@redhat.com> - 0.7.0-3
- Build with modern pyproject macros, fixes #2164207

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 31 2022 Orion Poplawski <orion@nwra.com> - 0.7.0-1
- Update to 0.7.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.6.0-16
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.6.0-13
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-10
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 01 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-8
- Subpackage python2-ptyprocess has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-7
- Rebuilt for Python 3.8

* Mon Jul 29 07:16:43 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.0-6
- Fix FTBFS

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.6.0-3
- Drop explicit locale setting
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Orion Poplawski <orion@nwra.com> - 0.6.0-1
- Update to 0.6.0

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.2-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Charalampos Stratakis <cstratak@redhat.com> - 0.5.2-1
- Update to 0.5.2 (#1467330)

* Thu Feb 23 2017 Orion Poplawski <orion@cora.nwra.com> - 0.5.1-6
- Really build python3 on EPEL

* Thu Feb 23 2017 Orion Poplawski <orion@cora.nwra.com> - 0.5.1-5
- Build python3 on EPEL
- Run tests verbosely

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.5.1-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 04 2016 Thomas Spura <tomspur@fedoraproject.org> - 0.5.1-1
- update to 0.5.1 (#1304136)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Thomas Spura <tomspur@fedoraproject.org> - 0.5-3
- Use new python macros

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Thomas Spura <tomspur@fedoraproject.org> - 0.5-1
- update to 0.5 (#1223718)

* Wed Jan 07 2015 Thomas Spura <tomspur@fedoraproject.org> - 0.4-1
- update to 0.4

* Wed Dec 03 2014 Thomas Spura <tomspur@fedoraproject.org> - 0.3.1-2
- Generalize with_python3 macro
- Add comment to tests section

* Tue Nov 25 2014 Thomas Spura <tomspur@fedoraproject.org> - 0.3.1-1
- initial spec for ptyprocess (#1167830)
