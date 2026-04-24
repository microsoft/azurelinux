# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global oname  pyinotify

Summary:       Monitor filesystem events with Python under Linux
Name:          python-inotify
Version:       0.9.6
Release: 43%{?dist}
License:       MIT
URL:           https://github.com/seb-m/pyinotify
Source0:       http://seb.dbzteam.org/pub/pyinotify/releases/pyinotify-%{version}.tar.gz
Patch:         pyinotify-0.9.6-epoint.patch
# Upstream pull request https://github.com/seb-m/pyinotify/pull/205
# Upstream issue https://github.com/seb-m/pyinotify/issues/204
Patch:         pyinotify-python-3.12-fix.patch
BuildRequires: gmp-devel
BuildRequires: python%{python3_pkgversion}-devel
BuildArch:     noarch
%global _description \
This is a Python module for watching filesystems changes. pyinotify \
can be used for various kind of fs monitoring. Based on inotify which \
is an event-driven notifier, where notifications are exported from \
kernel space to user space.
%description %_description

%package    -n python%{python3_pkgversion}-inotify
Summary:       %{summary}
%description -n python%{python3_pkgversion}-inotify %_description

%prep
%autosetup -p1 -n %{oname}-%{version}
sed -i '1c#! %{__python3}' python3/pyinotify.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l '%{oname}*'

%check
%pyproject_check_import
%py3_check_import pyinotify

%files -n python%{python3_pkgversion}-inotify -f %{pyproject_files}
%doc ACKS README.md
%{_bindir}/%{oname}

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.9.6-42
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.9.6-41
- Rebuilt for Python 3.14.0rc2 bytecode

* Sun Aug 03 2025 Terje Rosten <terje.rosten@ntnu.no> - 0.9.4-40
- Use correct python macros

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.9.6-38
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.9.6-35
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Troy Curtis, Jr <troycurtisjr@fedoraproject.org> - 0.9.6-32
- Fixes build for Python 3.12 (#2219556)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.9.6-30
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.9.6-27
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.6-24
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.6-21
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 29 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.6-19
- Subpackages python2-inotify, python2-inotify-examples have been removed
  See https://fedoraproject.org/wiki/Changes/RetirePython2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.6-18
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.6-17
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 06 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.6-14
- Only ship one executable (#1646926)

* Sun Jul 15 2018 Terje Rosten <terje.rosten@ntnu.no> - 0.9.4-14
- Use correct python macros

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.6-12
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.9.6-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.9.6-7
- rebuilt

* Tue Sep 20 2016 Terje Rosten <terje.rosten@ntnu.no> - 0.9.6-6
- Add entry point script

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 6 2015 Jakub Filak <jfilak@redhat.com> - 0.9.6-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Terje Rosten <terje.rosten@ntnu.no> - 0.9.6-1
- 0.9.6

* Mon Apr 13 2015 Terje Rosten <terje.rosten@ntnu.no> - 0.9.5-1
- 0.9.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Jakub Filak <jfilak@redhat.com> - 0.9.4-3
- make with_python3 be conditional on fedora

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Terje Rosten <terje.rosten@ntnu.no> - 0.9.4-1
- 0.9.4

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.9.3-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Terje Rosten <terje.rosten@ntnu.no> - 0.9.3-1
- 0.9.3

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 02 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.9.2-1
- 0.9.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.9.1-1
- 0.9.1

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.9.0-3
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jun 19 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.9.0-1
- 0.9.0
- Add python 3 subpackage
- License changed to MIT

* Sun Dec 06 2009 Terje Rosten <terje.rosten@ntnu.no> - 0.8.8-1
- 0.8.8

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2.git20090518
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Terje Rosten <terje.rosten@ntnu.no> - 0.8.6-1.git20090518
- Update to latest git, fixing bz #500934.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2.git20090208
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb  8 2009 Terje Rosten <terje.rosten@ntnu.no> - 0.8.1-1.git20090208
- 0.8.1

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.0-4.r
- Rebuild for Python 2.6

* Sun Jun 22 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.8.0-3.r
- rebuild 

* Tue Jun 17 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.8.0-2.r
- 0.8.0r
- add wrapper in /usr/bin

* Mon Jun 16 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.8.0-1.q
- 0.8.0q
- Update url, license and source url

* Sat Feb  9 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.1-2
- Rebuild

* Wed Aug 08 2007 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.1-1
- New upstream release: 0.7.1
- Fix license tag

* Mon Jun 25 2007 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.0-3
- Remove autopath from example package (bz #237464)

* Tue Mar 27 2007 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.0-2
- Fix email address

* Tue Mar  6 2007 Terje Rosten <terjeros@phys.ntnu.no> - 0.7.0-1
- Initial build

