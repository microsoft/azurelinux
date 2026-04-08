# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global desc %{expand: \
Pyflakes is similar to PyChecker in scope, but differs in that it does\
not execute the modules to check them. This is both safer and faster,\
although it does not perform as many checks. Unlike PyLint, Pyflakes\
checks only for logical errors in programs; it does not perform any\
check on style.}

Name:           pyflakes
# WARNING: When updating pyflakes, check not to break flake8!
Version:        3.1.0
Release:        8%{?dist}
Summary:        A simple program which checks Python source files for errors

License:        MIT
URL:            https://github.com/PyCQA/pyflakes
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        http://cdn.debian.net/debian/pool/main/p/pyflakes/pyflakes_2.5.0-1.debian.tar.xz
# Support Python 3.14
Patch:          https://github.com/PyCQA/pyflakes/pull/842.patch

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest

%py_provides python3-%{name}

%description %{desc}

%package -n python%{python3_pkgversion}-%{name}
Summary:        %{summary}

%description -n python%{python3_pkgversion}-%{name}
%{desc}

%prep
%autosetup -p1 -a1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{name}

mv %{buildroot}%{_bindir}/pyflakes %{buildroot}%{_bindir}/pyflakes-%{python3_version}
ln -s pyflakes-%{python3_version} %{buildroot}%{_bindir}/pyflakes-3
ln -s pyflakes-3 %{buildroot}%{_bindir}/pyflakes

install -Dpm 644 debian/pyflakes3.1 %{buildroot}%{_mandir}/man1/pyflakes-%{python3_version}.1
ln -s pyflakes-%{python3_version}.1 %{buildroot}%{_mandir}/man1/pyflakes-3.1
ln -s pyflakes-3.1 %{buildroot}%{_mandir}/man1/pyflakes.1

%check
# test_errors_syntax fails on Python 3.13 because of a changed error message
# https://github.com/PyCQA/pyflakes/issues/811
%pytest -v -k "not test_errors_syntax"

%files -n python%{python3_pkgversion}-%{name} -f %{pyproject_files}
%doc AUTHORS NEWS.rst README.rst
%{_bindir}/pyflakes-%{python3_version}
%{_bindir}/pyflakes-3
%{_bindir}/pyflakes
%{_mandir}/man1/pyflakes-%{python3_version}.1*
%{_mandir}/man1/%{name}-3.1.gz
%{_mandir}/man1/pyflakes.1*
%exclude %{python3_sitelib}/pyflakes/test

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.1.0-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.1.0-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.1.0-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.1.0-2
- Rebuilt for Python 3.13

* Sun Feb 18 2024 Orion Poplawski <orion@nwra.com> - 3.1.0-1
- Update to 3.1.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Adam Williamson <awilliam@redhat.com> - 3.0.1-2
- Backport another Python 3.12 fix and several required precursors

* Tue Jul 11 2023 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1 (RHBZ #2220224)

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.5.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 02 2022 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0 (RHBZ #2112576)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.4.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 20 2021 Daniel P. Berrangé <berrange@redhat.com> - 2.4.0-1
- Update to 2.4.0 release

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 05 2021 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1
- Update patch for py3.10 compatibility

* Mon Jun 07 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2.2.0-5
- Backport upstream commit f3b1b44b to fix Python 3.10 build (fix RHBZ#1927152)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.2.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 31 2020 Miro Hrončok <mhroncok@redhat.com> - 2.2.0-1
- Update to 2.2.0 (#1822843)
- Workaround Python 3.9 problems (#1831248)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-5
- Drop the backwards compatible python3-pyflakes command to clean python... tab completion

* Tue Oct 01 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-4
- Subpackage python2-pyflakes has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 01 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-1
- Update to 2.1.1 (#1669006)

* Tue Feb 26 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-1
- Update to 2.1.0 (#1669006)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 18 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 2.0.0-7
- fix usage of python macros

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-5
- Rebuilt for Python 3.7

* Tue Jun 26 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 2.0.0-4
- Fixed check section on RHEL > 7

* Fri Jun 22 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 2.0.0-3
- Drop python2 support on RHEL 8
- Resolves: BZ#1594150

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-2
- Rebuilt for Python 3.7

* Mon May 21 2018 Sandro Bonazzola <sandro.bonazzola@gmail.com> - 2.0.0-1
- Rebase on upstream 2.0.0
- Refresh Debian additions tarball to 1.6.0-1.
- Resolves: BZ#1580183

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.6.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.6.0-2
- Python 2 binary package renamed to python2-pyflakes
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug  3 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.6.0-1
- Update to 1.6.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.5.0-4
- Point unversioned pyflakes executable to Python 3 in F27+ and EL8+
- Provide python2-pyflakes

* Fri May 26 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.5.0-3
- Run tests with -Wall

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.5.0-1
- Update to 1.5.0

* Sun Jan  1 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.4.0-1
- Update to 1.4.0

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.3.0-4
- Rebuild for Python 3.6

* Thu Dec  8 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.3.0-3
- Unconditionalize python3 build

* Wed Sep 14 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.3.0-2
- Add standard versioned names for executables and man pages (#1374381)

* Fri Sep  2 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.3.0-1
- Update to 1.3.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri May 13 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.2.3-1
- Update to 1.2.3
- Build python3 on EL7

* Sat May  7 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.2.2-1
- Update to 1.2.2

* Fri May  6 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.2.1-1
- Update to 1.2.1

* Wed May  4 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.2.0-1
- Update to 1.2.0

* Tue Mar  1 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.1.0-1
- Update to 1.1.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov  4 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.0.0-2
- Rebuild

* Mon Sep 21 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.0.0-1
- Update to 1.0.0
- Specfile cleanups per current guidelines

* Wed Jun 17 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.9.2-1
- Update to 0.9.2

* Wed Jun 10 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.9.1-1
- Update to 0.9.1

* Mon Jun  1 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.9.0-1
- Update to 0.9.0
- Specfile cleanup and guidelines update
- Improve python3-pyflakes manpage

* Sat Jan 31 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.8.1-4
- Ship LICENSE as %%license where available
- Don't try to build with python3 on EL7 by default

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 31 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.8.1-1
- Update to 0.8.1

* Wed Mar 26 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.8-1
- Update to 0.8

* Wed Dec 11 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-4
- Avoid interfering with pies in version check (#1039706, Timothy Crosley).
- Refresh Debian additions tarball.

* Mon Sep  9 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-3
- Build Python 3 version (#1004668).
- Add dependency on setuptools.
- Update summary and description.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul  7 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-1
- Update to 0.7.3.

* Mon Apr 29 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.2-1
- Update to 0.7.2.

* Tue Apr 23 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.1-1
- Update to 0.7.1.

* Thu Apr 18 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7-1
- Update to 0.7.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Feb  5 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.6.1-1
- Update to 0.6.1.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep  5 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.5.0-2
- Bring back null byte input traceback patch.
- Include LICENSE and NEWS.txt in docs.

* Sun Sep  4 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.0-1
- Update to 0.5.0
- Remove patches that no longer apply

* Mon Apr  4 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.4.0-5
- Avoid traceback on input with null bytes (#691164).

* Sun Feb 13 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.4.0-4
- Backport upstream changes for set and dict comprehension support (#677032).
- Add man page and file descriptor close patch from Debian.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Mar 19 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.4.0-1
- Update to 0.4.0.

* Wed Nov  4 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.3.0-1
- Update to 0.3.0 (#533015).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.1-4
- Rebuild for Python 2.6

* Sat Dec  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.2.1-3
- Correctly identify the license

* Sat Dec  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.2.1-2
- Revert to released tarball

* Fri Dec  8 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.2.1-1.10526svn
- Fix version number

* Fri Dec  8 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-1.10526svn
- Fix up versioning

* Tue Dec  5 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-0.1.10526
- First version for Fedora Extras
