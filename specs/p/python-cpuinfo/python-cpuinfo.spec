# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname cpuinfo
%global sum Getting CPU info

Name:           python-%{srcname}
Version:        9.0.0
Release: 17%{?dist}
Summary:        %{sum}

License:        MIT
URL:            https://github.com/workhorsy/py-cpuinfo
Source0:        https://files.pythonhosted.org/packages/source/p/py-%{srcname}/py-%{srcname}-%{version}.tar.gz

# s390x support
Patch0:         py-cpuinfo-s390x.patch

BuildArch:      noarch

# https://github.com/workhorsy/py-cpuinfo/issues/55
# ExclusiveArch:  %%{ix86} x86_64 %%{power64} s390x noarch

BuildRequires:  python3-devel

%description
Py-cpuinfo gets CPU info with pure Python. Py-cpuinfo should work without
any extra programs or libraries, beyond what your OS provides.

These approaches are used for getting info:
    Windows Registry
    /proc/cpuinfo
    sysctl
    dmesg
    isainfo and psrinfo
    Querying x86 CPUID register


%package -n python3-%{srcname}
Summary:        %{sum}

%description -n python3-%{srcname}
Py-cpuinfo gets CPU info with pure Python. Py-cpuinfo should work without
any extra programs or libraries, beyond what your OS provides.

These approaches are used for getting info:
    Windows Registry
    /proc/cpuinfo
    sysctl
    dmesg
    isainfo and psrinfo
    Querying x86 CPUID register

%prep
%setup -q -n py-%{srcname}-%{version}
rm -rf *.egg-info

sed -i -e '/^#!\//, 1d' cpuinfo/cpuinfo.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{srcname}


%check
%pyproject_check_import

%{python3} -m unittest test_suite.py

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst ChangeLog
%{_bindir}/cpuinfo


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 9.0.0-16
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 9.0.0-15
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Parag Nemade <pnemade AT redhat DOT com> - 9.0.0-13
- Convert a spec to use pyproject macros (rh#2377586)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 9.0.0-12
- Rebuilt for Python 3.14

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 29 2024 Parag Nemade <pnemade AT redhat DOT com> - 9.0.0-10
- Use unittest to run test_suite

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 9.0.0-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Parag Nemade <pnemade AT redhat DOT com> - 9.0.0-5
- Mark this as SPDX license expression converted

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 9.0.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 26 2022 Parag Nemade <pnemade AT redhat DOT com> - 9.0.0-1
- Update to 9.0.0 version (#2137734)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 8.0.0-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 8.0.0-2
- Rebuilt for Python 3.10

* Thu Apr 15 2021 Parag Nemade <pnemade AT redhat DOT com> - 8.0.0-1
- Update to 8.0.0 version (#1949623)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 06 2020 Parag Nemade <pnemade AT redhat DOT com> - 7.0.0-1
- Update to 7.0.0 version (#1853940)

* Thu Jun 11 2020 Parag Nemade <pnemade AT redhat DOT com> - 6.0.0-1
- Update to 6.0.0 version (#1846323)

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Parag Nemade <pnemade AT redhat DOT com> - 5.0.0-2
- Drop the versioned binary and restore to original path name

* Sat Mar 23 2019 Parag Nemade <pnemade AT redhat DOT com> - 5.0.0-1
- Update to 5.0.0 version (#1691106)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Parag Nemade <pnemade AT redhat DOT com> - 4.0.0-4
- Remove python2 subpackage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-2
- Rebuilt for Python 3.7

* Wed Apr 04 2018 Parag Nemade <pnemade AT redhat DOT com> - 4.0.0-1
- Update to 4.0.0 version (#1563228)

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.3.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.3.0-1
- Update to 3.3.0 version

* Thu Apr 20 2017 Than Ngo <than@redhat.com> - 3.2.0-2
- added s390x support
- enable all supported archs

* Thu Apr 20 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.2.0-1
- Update to 3.2.0 version

* Sun Apr 09 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.0.0-1
- Update to 3.0.0 version

* Tue Mar 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.7-3
- One more attempt to fix the ExclusiceArch: tag (Thanks sharckcz)

* Tue Mar 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.7-2
- Resolves:rh#1409636 - python-cpuinfo does not support aarch64, ppc64
  and ppc64le, and s390/s390x 

* Tue Mar 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.7-1
- Update to 0.2.7 version

* Sun Mar 12 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.6-1
- Update to 0.2.6 version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 25 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.2.3-2
- Thanks to Petr Viktorin (rh#1330005) for correcting dependencies

* Sat Apr 23 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.2.3-1
- Update to 0.2.3 release (rh#1311530)
- Added %%license tag

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.1.8-1
- Update to 0.1.8 release (rh#1292653)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Jul 13 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.1.6-1
- Update to 0.1.6 release (rh#1242523)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 12 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.1.4-1
- Update to 0.1.4 release
- Resolves:rh#1190549 - cpuinfo failed to run

* Tue Feb 03 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.1.2-3
- Resolves:rh#1178548, follow dnf way to use py3 binary

* Fri Oct 03 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.2-2
- Clean the spec to follow py3 guidelines

* Wed Oct 01 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.2-1
- Update to 0.1.2 release

* Mon Sep 22 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.0-2
- fix rpmlint messages
- Added upstream LICENSE file not in tarball

* Mon Sep 22 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.1.0-1
- Initial packaging

