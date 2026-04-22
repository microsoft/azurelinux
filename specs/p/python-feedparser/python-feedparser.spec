# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name feedparser

Name:           python-feedparser
Version:        6.0.12
Release: 3%{?dist}
Summary:        Parse RSS and Atom feeds in Python

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/kurtmckee/feedparser
Source0:        %{pypi_source}

BuildArch:      noarch

%description
Universal Feed Parser is a Python module for downloading and parsing
syndicated feeds. It can handle RSS 0.90, Netscape RSS 0.91,
Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94, RSS 1.0, RSS 2.0,
Atom 0.3, Atom 1.0, and CDF feeds. It also parses several popular extension
modules, including Dublin Core and Apple's iTunes extensions.

%package -n python3-%{pypi_name}
Summary:        Parse RSS and Atom feeds in Python
BuildRequires:  python3-devel
BuildRequires:  python3-sgmllib3k

## TODO: Decide on these, also with regard to explicit "Requires".
## Optional imports at run-time and influence the test-suite, too,
## and causes additional tests to fail.
#
#BuildRequires:  python3-beautifulsoup
#  usage removed in > 5.1.3
#
## the preferred XML parser
#BuildRequires:  python3-libxml2

## TODO: python3-chardet BR and Req
# fixes included in > 5.1.3


%description -n python3-%{pypi_name}
Universal Feed Parser is a Python module for downloading and parsing
syndicated feeds. It can handle RSS 0.90, Netscape RSS 0.91,
Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94, RSS 1.0, RSS 2.0,
Atom 0.3, Atom 1.0, and CDF feeds. It also parses several popular extension
modules, including Dublin Core and Apple's iTunes extensions.


%package doc
BuildRequires: python3-sphinx
BuildArch: noarch
Summary: Documentation for the Python feedparser

%description doc
This documentation describes the behavior of Universal Feed Parser %{version}.

The documentation is also included in source form (Sphinx ReST).


%prep
%autosetup -p1 -n %{pypi_name}-%{version}

find -type f -exec sed -i 's/\r//' {} ';'
find -type f -exec chmod 0644 {} ';'


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

# build documentation
rm -rf __tmp_docs ; mkdir __tmp_docs
sphinx-build -b html -d __tmp_docs/ docs/ __tmp_docs/html/


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}


%check
%pyproject_check_import

PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} tests/runtests.py || :


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst NEWS

%files doc
%doc LICENSE __tmp_docs/html/
# the original Sphinx ReST tree
%doc docs


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 6.0.12-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Sep 10 2025 Christiano Anderson <chris@christiano.dev> - 6.0.12-1
- New upstream version, closes RHBZ#2394388

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 6.0.11-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 19 2025 Christiano Anderson <chris@christiano.dev> - 6.0.11-7
- Removing deprecated py_build Fixes rhbz#2377701

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 6.0.11-6
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 6.0.11-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 6.0.11-2
- Rebuilt for Python 3.13

* Wed Feb 14 2024 Johannes Lips <hannes@fedoraproject.org> - 6.0.11-1
- Update to 6.0.11. Fixes rhbz#2262610

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 6.0.10-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 6.0.10-2
- Rebuilt for Python 3.11

* Sun May 29 2022 Kevin Fenzi <kevin@scrye.com> - 6.0.10-1
- Update to 6.0.10. Fixes rhbz#2088451

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Kevin Fenzi <kevin@scrye.com> - 6.0.8-1
- Update to 6.0.8. Fixes rhbz#1974555

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.6-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Kevin Fenzi <kevin@scrye.com> - 6.0.6-1
- Update to 6.0.6. Fixes rhbz#1971225

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 6.0.2-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Kevin Fenzi <kevin@scrye.com> - 6.0.2-1
- Update to 6.0.3. Upstream is python3 only now.
- re-enable tests, since they now all pass.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.2.1-16
- Rebuilt for Python 3.9

* Fri May 15 2020 Adam Williamson <awilliam@redhat.com> - 5.2.1-15
- Backport PR #206 to fix with Python 3.9 (Karthikeyan Singaravelan)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 Miro Hrončok <mhroncok@redhat.com> - 5.2.1-13
- Subpackage python2-feedparser has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 5.2.1-12
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 5.2.1-11
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 30 2019 Matěj Cepl <mcepl@cepl.eu> - 5.2.1-9
- Use python3-Sphinx instead of the Python2 version. It really doesn't matter
  in the end.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.2.1-6
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 5.2.1-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 17 2017 Petr Viktorin <pviktori@redhat.com> - 5.2.1-3
- Python 2 binary package renamed to python2-feedparser

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr  8 2017 Peter Robinson <pbrobinson@fedoraproject.org> 5.2.1-1
- Upstream 5.2.1
- Cleanup spec
- Use %%license

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 5.2.0-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Jun 29 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 5.2.0-1
- Upstream 5.2.0
- Cleanup spec

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 5.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.3-4
- Conditionalize the -doc package, because python-sphinx is not new
  enough for EL6.

* Sun May 26 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.3-3
- BR python-sphinx and build pregenerated HTML documentation to be
  included in a python-feedparser-doc package together with the sources
  for the documentation

* Sat Mar  9 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.3-2
- Add BuildRequires/Requires python-chardet because if it's installed
  as a dependency of other Python module packages, it would be imported
  and used anyway, and it doesn't make any tests fail.

* Sat Mar  9 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.3-1
- Update to 5.1.3 (50k diff).
- Patch test-suite minimally for python3 to show that it fails early.
- Fix file permissions and line delimiters at end of %%prep section.
- Fix python3 sitelib path in %%check section.

* Fri Mar  8 2013 Michael Schwendt <mschwendt@fedoraproject.org>
- Update URL to new location at Google code (#880138).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 5.1.2-5
- remove rhel logic from with_python3 conditional (RHBZ #902896)

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 5.1.2-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.2-2
- Also package NEWS files as documentation.
- 5.1.2 fixes CVE-2012-2921
  (DoS via memory consumption processing ENTITY declarations).

* Tue May 22 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.2-1
- Update to 5.1.2 and its security fix (#787401).
- Ignore testsuite results for now (#787401).
- Set PYTHONPATH in %%check section to include files in %%buildroot.
- Drop CFLAGS usage from spec file, because this is Python.

* Sat Feb  4 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 5.1-1
- upstream 5.1 (#787401)
- spec cleanup
- tests disabled
- python3 support

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 05 2011 Luke Macken <lmacken@redhat.com> - 5.0.1-1
- Latest upstream release
- Remove feedparser_utf8_decoding.patch
- Remove democracynow_feedparser_fix.patch
- Run the test suite

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Dec 14 2009 Haïkel Guémar <karlthered@gmail.com> - 4.1-11
- rebuild for Fedora 13

* Fri Aug 07 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-10
- Apply patch for title munging issue (#491373)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 04 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-8
- Fix source URL (moved to googlecode).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 27 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-6
- Patch for a utf8 decoding issue (#477024)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.1-5
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.1-4
- fix license tag

* Thu Jun 28 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-3
- Ghostbusting (#205413).
- Remove manual python-abi Requires.
- Appease rpmlint.

* Sat Dec 23 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 4.1-2
- Rebuild for new Python.

* Wed Jan 11 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-1
- Version 4.1

* Sat Jan 07 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.0.2-2
- Set sane permissions on doc files.

* Wed Jan 04 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.0.2-1
- Initial build.
