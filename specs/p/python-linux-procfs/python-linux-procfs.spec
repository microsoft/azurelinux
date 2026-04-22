# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora}
%else
%global without_python3 1
%endif

Name: python-linux-procfs
Version: 0.7.4
Release: 2%{?dist}
License: GPL-2.0-only
Summary: Linux /proc abstraction classes
Source: https://cdn.kernel.org/pub/software/libs/python/%{name}/%{name}-%{version}.tar.xz
URL: https://www.kernel.org/pub/software/libs/python/python-linux-procfs
BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros

# Patches

%global _description\
Abstractions to extract information from the Linux kernel /proc files.

%description %_description

%package -n python3-linux-procfs
Summary: %summary
%{?python_provide:%python_provide python3-linux-procfs}

%description -n python3-linux-procfs %_description

%prep
%autosetup -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files procfs

%files -n python3-linux-procfs
%defattr(0755,root,root,0755)
%{_bindir}/pflags
%{python3_sitelib}/procfs/
%defattr(0644,root,root,0755)
%{python3_sitelib}/python_linux_procfs*.dist-info
%license COPYING

%changelog
* Fri Oct 10 2025 John Kacur <jkacur@redhat.com> - 0.7.4-1
- Rebase to v0.7.4 upstream and use pyproject.toml

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.7.3-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7.3-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.7.3-8
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.7.3-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 02 2023 John Kacur <jkacur@redhat.com> - 0.7.3-2
- Update the SPDX license tag in the specfile

* Sat Dec 02 2023 John Kacur <jkacur@redhat.com> - 0.7.3-1
- Update to the latest upstream version v0.7.3
- Use an SPDX license tag in the specfile

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.7.1-2
- Rebuilt for Python 3.12

* Thu Feb 16 2023 John Kacur <jkacur@redhat.com> - 0.7.1-1
- Rebase to 0.7.1 upstream
- Add upstream patch to remove use of distutils

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Jiri Kastner <jkastner@fedoraproject.org> - 0.7.0-4
- Rebuilt for Python 3.11 - episodfe ii

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.7.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Federico Pellegrin <fede@evolware.org> - 0.7.0-1
- update to 0.7.0 (various fixes and cleanups)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.6.3-2
- Rebuilt for Python 3.10

* Fri May 28 2021 Jiri Kastner <jkastner@fedoraproject.org> - 0.6.3-1
- update to 0.6.3

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-2
- Subpackage python2-linux-procfs has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Feb  5 2019 Jiri Kastner <jkastner@redhat.com> - 0.6.1-1
- update to 0.6.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Nov 21 2017 Jiri Kastner <jkastner@redhat.com> - 0.5.1-2
- missing defattr for _bindir

* Tue Nov 21 2017 Jiri Kastner <jkastner@redhat.com> - 0.5.1-1
- missed snippet in specfile for python2 only
- added scripts to setup.py, pflags renamed and added to setup.py

* Mon Nov 20 2017 Jiri Kastner <jkastner@redhat.com> - 0.5-1
- update to 0.5

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.4.10-4
- Python 2 binary package renamed to python2-linux-procfs
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Jiri Kastner <jkastner@redhat.com> - 0.4.10-1
- update to latest release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 10 2014 Jiri Kastner <jkastner@redhat.com> - 0.4.6-4
- fix source and url

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Jiri Kastner <jkastner@redhat.com> - 0.4.6-1
- updated to 0.4.6

* Thu Jun  6 2013 Jiri Kastner <jkastner@redhat.com> - 0.4.5-1
- Added support for parsing cgroups as a per thread attribute

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.4.4-1
- Even more fixes due to the fedora review process

* Mon Feb  9 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.4.3-1
- Fixups due to the fedora review process

* Tue Aug 12 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.4.2-1
- interrupts: Add find_by_user_regex
- process: Always set the "cmdline" array, even if empty
- pidstats: Remove dead processes in find_by_name()
- pidstats: Add process class to catch dict references for late parsing
- pidstats: Move the /proc/PID/{stat,status} parsing to classes
- pidstats: Introduce process_flags method

* Tue Aug 12 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.4-1
- Per process flags needed by tuna

* Fri Jun 13 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.3-1
- Support CPU hotplug

* Mon Feb 25 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-1
- package created
