# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

Name:           python-iniparse
Version:        0.5.1
Release: 7%{?dist}
Summary:        Accessing and Modifying INI files

# From LICENSE:
#   iniparse/compat.py and tests/test_compat.py contain code derived from
#   lib/python-2.3/ConfigParser.py and lib/python-2.3/test/test_cfgparse.py
#   respectively.  Other code may contain small snippets from those two files
#   as well.  The Python license (LICENSE-PSF) applies to that code.
License:        MIT AND Python-2.0.1
URL:            https://github.com/candlepin/python-iniparse
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# Python 3.14 support: Avoid the multiprocessing forkserver method
Patch:          https://github.com/candlepin/python-iniparse/pull/38.patch

BuildArch: noarch

BuildRequires:  python3-devel
BuildRequires:  python3-test

%global _description %{expand: \
iniparse is an INI parser for Python which is API compatible with the standard
library’s ConfigParser, preserves structure of INI files (order of sections &
options, indentation, comments, and blank lines are preserved when data is
updated), and is more convenient to use.}

%description
%{_description}

%package -n python3-iniparse
Summary:        %{summary}

%description -n python3-iniparse
%{_description}

%prep
%autosetup -p1
chmod -c -x html/index.html

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
rm -vfr %{buildroot}%{_docdir}/*
%pyproject_save_files iniparse

%check
%{py3_test_envvars} %{python3} ./runtests.py

%files -n python3-iniparse -f %{pyproject_files}
# pyproject_files handles both license files; verify with “rpm -qL -p …”
%doc README.md Changelog html/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.5.1-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.5.1-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.5.1-3
- Rebuilt for Python 3.14

* Wed May 28 2025 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-2
- Fix build with Python 3.14

* Mon Jan 20 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.5-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.5-5
- Rebuilt for Python 3.12
- Fixes: rhbz#2176142

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5-2
- Port to pyproject-rpm-macros
- Mention license breakdown in a spec file comment
- Update summary and description from upstream

* Mon Jun 13 2022 Jiri Hnidek <jhnidek@redhat.com> - 0.5-1
- Release 0.5
- Moved project to https://github.com/candlepin/python-iniparse
- Added support for Python 3 to upstream project

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.4-47
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.4-44
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4-41
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-39
- Subpackage python2-iniparse has been removed
  See https://fedoraproject.org/wiki/Changes/RetirePython2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-38
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 31 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-37
- Drop build dependency on python2-test

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-36
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4-31
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Iryna Shcherbina <ishcherb@redhat.com> - 0.4-29
- Fix ambiguous Python 2 dependency declarations
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4-28
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4-27
- Remove platform-python subpackage

* Thu Aug 10 2017 Miro Hrončok <mhroncok@redhat.com> - 0.4-26
- Add platform-python package
- Add bconds
- Remove %%{?system_python_abi}

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 11 2016 Neal Gompa <ngompa13@gmail.com> - 0.4-23
- Add patch to update setup.py to use setuptools and declare install dependencies

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.4-22
- Rebuild for Python 3.6

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.4-21
- Cleanups
- Add %%{?system_python_abi}

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-20
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr 12 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.4-19
- Make python3 builds conditionally
- Adopt to new packaging guidelines
- Remove setuptools from BRs as it's not needed
- Cleanup spec

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.4-17
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 0.4-15
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Mar 07 2014 Tim Lauridsen <timlau@fedoraproject.org> - 0.4-12
- added python3-test to buildreq for python3 
- run unittest with python3 also

* Fri Mar 07 2014 Tim Lauridsen <timlau@fedoraproject.org> - 0.4-11
- added python-test to buildreq, for unittests

* Fri Mar 07 2014 Tim Lauridsen <timlau@fedoraproject.org> - 0.4-10
- added %%check to run unittests when build
- updated fix-issue-28.patch, so test cases dont fail

* Fri Sep 20 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4-9
- Introduce python3 subpackage.
- Use %%__python2 instead of %%__python.

* Mon Jul 29 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.4-8
- Install docs to %%{_pkgdocdir} where available.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-6
- fix for upstream issue 28

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild


* Sat Nov 7 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.4-1
- Release 0.4

* Sat Nov 7 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.3.1-2
- removed patch

* Sat Nov 7 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.3.1-1
- Release 0.3.1
-   Fix empty-line handling bugs introduced in 0.3.0 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 2 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.3.0-2
- added patch from upstream to fix regrestion :

* Sat Feb 28 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.3.0-1
- Release 0.3.0
-  Fix handling of continuation lines
-  Fix DEFAULT handling
-  Fix picking/unpickling 

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 7 2008 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.4-1
- Release 0.2.4:
-   Updated to work with Python-2.6 (Python-2.4 and 2.5 are still supported)
-   Support for files opened in unicode mode
-   Fixed Python-3.0 compatibility warnings
-   Minor API cleanup 
* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.3-5
- Rebuild for Python 2.6
* Tue Jan 8 2008 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.3-4
- own the %%{_docdir}/python-iniparse-%%{version} directory
* Tue Dec 11 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.3-3
- handle egg-info too
* Tue Dec 11 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.3-2
- removed patch source line
* Tue Dec 11 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.3-1
- Updates to release 0.2.3
- removed empty ini file patch, it is included in 0.2.3
* Mon Nov 19 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.2-2
- Added upstream patch to fix problems with empty ini files.
* Tue Sep 25 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.2-1
- Updated to release 0.2.2
- removed patch to to fix problems with out commented lines, included in upstream source
* Wed Sep 12 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.1-4
- Added some logic to get the right python-setuptools buildrequeres
- based on the fedora version, to make the same spec file useful in
- all fedora releases.
* Mon Sep 10 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.1-3
- Added patch from upstream svn to fix problems with out commented lines.
* Tue Aug 28 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.1-2
- Changed BuildRequires python-setuptools to python-setuptools-devel
* Tue Aug 7 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.1-1
- Release 0.2.1
* Fri Jul 27 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-3
- relocated doc to %%{_docdir}/python-iniparse-%%{version}
* Thu Jul 26 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-2
- changed name from iniparse to python-iniparse
* Tue Jul 17 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-1
- Release 0.2
- Added html/* to %%doc
* Fri Jul 13 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.1-1
- Initial build.
