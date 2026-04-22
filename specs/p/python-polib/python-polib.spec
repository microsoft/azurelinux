# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname polib

Name:           python-%{srcname}
Version:        1.2.0
Release: 14%{?dist}
Summary:        A library to parse and manage gettext catalogs

License:        MIT
URL:            https://github.com/izimobil/polib
Source0:        %pypi_source

BuildArch:      noarch

%description
polib allows you to manipulate, create, modify gettext files (pot, po and
mo files). You can load existing files, iterate through it's entries, add,
modify entries, comments or metadata, etc... or create new po files from
scratch.

polib provides a simple and pythonic API, exporting only three convenience
functions 'pofile', 'mofile' and 'detect_encoding', and the 4 core classes:
POFile, MOFile, POEntry and MOEntry for creating new files/entries.

%package -n python3-%{srcname}
Summary:        A library to parse and manage gettext catalogs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
polib allows you to manipulate, create, modify gettext files (pot, po and
mo files). You can load existing files, iterate through it's entries, add,
modify entries, comments or metadata, etc... or create new po files from
scratch.

polib provides a simple and pythonic API, exporting only three convenience
functions 'pofile', 'mofile' and 'detect_encoding', and the 4 core classes:
POFile, MOFile, POEntry and MOEntry for creating new files/entries.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} tests/tests.py

%files -n python3-%{srcname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.2.0-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.2.0-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.2.0-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2.0-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 29 2023 Parag Nemade <pnemade AT redhat DOT com> - 1.2.0-4
- Mark this as SPDX license expression converted

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.2.0-2
- Rebuilt for Python 3.12

* Fri Feb 24 2023 Sundeep Anand <suanand@redhat.com> - 1.2.0-1
- Upgrade to 1.2.0 (rhbz#2173027)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1.1-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.1.1-2
- Rebuilt for Python 3.10

* Thu Apr  8 2021 Sundeep Anand <suanand@redhat.com> - 1.1.1-1
- Upgrade to 1.1.1 (rhbz#1943734)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Subpackage python2-polib has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 David Shea <dshea@redhat.com> - 1.1.0-1
- Upgrade to 1.1.0

* Mon Dec 10 2018 David Shea <dshea@redhat.com> - 1.0.7-13
- Run the testsuite in %%check (#1626861)
- Remove EPEL-related macros from the rawhide spec file
- Switch to the pypi source file

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-11
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.7-9
- Package must be noarch
- Skip tests on EPEL <= 8

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.7-8
- Improvements for Fedora and EPEL

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Ding-Yi Chen <dchen@redhat.com> - 1.0.7-2
- Add EPEL 6 and 7 support
- Revise Description

* Fri Jan 08 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.0.7-1
- Update to 1.0.7 upstream version
- Remove all the optional things like %%clean, %%defattr,
  buildroot and group tags
- use %%license tag 
- updated to use current python packaging guidelines

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 1.0.3-7
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Ding-Yi Chen <dchen@redhat.com> - 1.0.3-2
- Fix the build for EL6 and EL5 (without python3-polib)

* Tue Jul 16 2013 Ding-Yi Chen <dchen@redhat.com> - 1.0.3-1
- python3 binding is available (python3-polib)
- Fixed Bug 978672 - This package should be updated.
- Upstream update to 1.0.3
- Version 1.0.3 (2013/02/09)
  Fixed issue #38: POFile.append() raised a duplicate exception when you tried to add a new entry with the same msgid and a different msgctxt (only when check_for_duplicates option is set to True)
  Fixed issue #39: Added __init__.py file for convenience
  Fixed issue #41: UnicodeDecodeError when running setup.py build on python3 with C locale
  polib is now fully PEP8 compliant
  Small improvements: remove unused "typ" var (thanks Rodrigo Silva), mproved Makefile, Make sure _BaseFile.__contains__ returns a boolean value

- Version 1.0.2 (2012/10/23)
  allow empty comments, flags or occurences lines

- Version 1.0.1 (2012/09/11)
  speed up POFile.merge method (thanks @encukou)
  allow comments starting with two '#' characters (thanks @goibhniu)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 30 2012 Ding-Yi Chen <dchen@redhat.com> - 1.0.0-1
- Upstream update to 1.0.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 Ding-Yi Chen <dchen@redhat.com> - 0.7.0-2
- Update to upstream commit dbafdc621bf4, which include following:
  * Add check for unescaped quotes at the beginning of the string + unit tests
  * Fixed issue #27 (polib didn't check unescaped double quote) + better error handling
  * Fixed typos in previous commit
  * Fixed issue #26 IOError when parsing empty comments (thanks Türker Sezer)
  * Do not hardcode polib version in doc conf

* Fri Oct 28 2011 Ding-Yi Chen <dchen@redhat.com> - 0.7.0-1
- Correct URLs
- Replace README with README.rst
- Update to 0.7.0:
  From Version 0.7.0 (2011/07/14)
      This version adds support for python 3 (thanks to Vinay Sajip).
      polib now supports out-of-the-box any version of python ranging 
      from 2.4 to latest 3.X version.
  From Version 0.6.4 (2011/07/13)
      * Better api, autodetected_encoding is no longer required to 
        explicitely set the encoding (fixes issue #23),
      * Fixed issue #24 Support indented PO files (thanks to 
        François Poirotte).
  From Version 0.6.3 (2011/02/19)
      * Fixed issue #19 (Disappearing newline characters due to 
        textwrap module),
      * ensure wrapping works as expected.
  From Version 0.6.2 (2011/02/09)
      * Backported textwrap.TextWrapper._wrap_chunks that has support
        for the drop_whitespace parameter added in Python 2.6 (Fixes 
        #18: broken compatibility with python 2.5, thanks @jezdez).
  From Version 0.6.1 (2011/02/09)
      * fixed regression that prevented POFile initialization from 
        data to work (issue #17).
  From Version 0.6.0 (2011/02/07)
      * polib is now fully documented,
      * switched from doctests to unit tests to keep the polib.py 
        file clean,
      * fixed issue #7 (wrapping issues, thanks @jezdez),
      * added a __eq__ method to _BaseFile (thanks @kost BebiX),
      * handle msgctxt correctly when compiling mo files,
      * compiled mo files are now exactly the same as those compiled
        by msgfmt without using hash tables.
  From Version 0.5.5 (2010/10/30)
      * Removed multiline handling code, it was a mess and was the
        source of potential bugs like issue #11,
      * Fixed typo in README and CHANGELOG, fixes issue #13.
  From Version 0.5.4 (2010/10/02)
     * fixed an issue with detect_encoding(), in some cases it could
       return an invalid charset.
  From Version 0.5.3 (2010/08/29)
     * correctly unescape lines containing both \\n and \n 
      (thanks to Martin Geisler),
     * fixed issue #6: __str__() methods are returning unicode instead
       of str,
     * fixed issue #8: POFile.merge error when an entry is obsolete in
       a .po, that this entry reappears in the .pot and that we merge 
       the two,
     * added support to instanciate POFile objects using data instead 
       of file path (thanks to Diego Búrigo Zacarão),
     * fixed issue #9: POFile.merge drop fuzzy attributes from 
       translations (thanks to Tim Gerundt),
     * fixed issue #10: Finding entries with the same msgid and 
       different context (msgctxt).
  From Version 0.5.2 (2010/06/09)
     * fixed issue #1: untranslated_entries() also show fuzzy message,
     * write back the fuzzy header if present in the pofile,
     * added support for previous msgctxt, previous msgid and previous
       msgid_plural comments (fixes issue #5),
     * better handling of lines wrapping.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Dec 14 2009 Diego Búrigo Zacarão <diegobz@gmail.com> - 0.5.1-1
- Updated to 0.5.1 release

* Wed Aug 19 2009 Diego Búrigo Zacarão <diegobz@gmail.com> - 0.4.2-1
- Updated to 0.4.2 release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2.20080217svnr60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 18 2009 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.4.0-1.20080217svnr60
- Initial RPM release

