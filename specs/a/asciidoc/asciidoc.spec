# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           asciidoc
Version:        10.2.0
Release:        17%{?dist}
Summary:        Text based document generation

License:        GPL-2.0-or-later
URL:            http://asciidoc.org
Source0:        https://github.com/asciidoc-py/asciidoc-py/archive/%{version}/%{name}-py-%{version}.tar.gz

BuildArch:      noarch

Patch1:         asciidoc-table-separator.patch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  (python3-wheel if python3-setuptools < 71)
BuildRequires:  dblatex
BuildRequires:  docbook-style-xsl
BuildRequires:  graphviz
BuildRequires:  libxslt
BuildRequires:  source-highlight
BuildRequires:  texlive-dvipng-bin
BuildRequires:  texlive-dvisvgm-bin
BuildRequires:  symlinks
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  make

Requires:       python3
Requires:       docbook-style-xsl
Requires:       graphviz
Requires:       libxslt
Requires:       source-highlight

%description
AsciiDoc is a text document format for writing short documents,
articles, books and UNIX man pages. AsciiDoc files can be translated
to HTML and DocBook markups using the asciidoc(1) command.

%package doc
Summary:  Additional documentation and examples for asciidoc

Requires: %{name} = %{version}-%{release}

%description doc
%{summary}.

%package latex
Summary:  Support for asciidoc latex output

Requires: %{name} = %{version}-%{release}
Requires: dblatex
Requires: texlive-dvipng-bin

%description latex
%{summary}.

%prep
%autosetup -n %{name}-py-%{version} -p1

%build
autoreconf -v
%configure
%make_build

%install
make install docs manpages DESTDIR=%{buildroot} PIP_NO_BUILD_ISOLATION=0
mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}/share/doc/doc/{asciidoc.1,a2x.1,testasciidoc.1} %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}/%{_pkgdocdir}/doc
mv %{buildroot}/share/doc/doc/ %{buildroot}/%{_pkgdocdir}/doc
mkdir -p %{buildroot}/%{_pkgdocdir}/doc/images
mv %{buildroot}/share/doc/images/ %{buildroot}/%{_pkgdocdir}/doc/images
rm  %{buildroot}/share/doc/{BUGS.adoc,CHANGELOG.adoc,INSTALL.adoc,README.md,dblatex/dblatex-readme.txt,docbook-xsl/asciidoc-docbook-xsl.txt}

# Some tests are failing
#%%check
#export PATH="../:$PATH"
#cd tests
#%%{__python3} testasciidoc.py update
#%%{__python3} testasciidoc.py run

%files
%doc BUGS.adoc CHANGELOG.adoc COPYRIGHT README.md
%{_mandir}/man1/*.1*
%{_bindir}/a2x
%{_bindir}/asciidoc
%{python3_sitelib}/asciidoc-%{version}.dist-info/
%{python3_sitelib}/asciidoc/
%exclude %{python3_sitelib}/asciidoc/resources/filters/latex
%exclude %{python3_sitelib}/asciidoc/resources/filters/music
%exclude %{_pkgdocdir}/doc

%files doc
%doc COPYRIGHT
%{_pkgdocdir}/doc/

%files latex
%doc COPYRIGHT
%dir %{python3_sitelib}/asciidoc/resources/filters/latex

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 10.2.0-17
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Aug 27 2025 Miro Hrončok <mhroncok@redhat.com> - 10.2.0-16
- Drop unnecessary BuildRequires for python3-wheel when python3-setuptools is new enough

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 10.2.0-15
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 10.2.0-13
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 10.2.0-10
- Rebuilt for Python 3.13

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 27 2023 Josef Ridky <jridky@redhat.com> - 10.2.0-7
- fix SPDX license

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Josef Ridky <jridky@redhat.com> - 10.2.0-5
- fix invalid escape sequence (#2220936)

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 10.2.0-4
- Rebuilt for Python 3.12

* Fri May 26 2023 Miro Hrončok <mhroncok@redhat.com> - 10.2.0-3
- Fix build with pip 23.1.2+
- Fixes: rhbz#2209018

* Tue May 02 2023 Josef Ridky <jridky@redhat.com> - 10.2.0-2
- move to SPDX license format

* Sat Feb 11 2023 Fabian Affolter <mail@fabian-affolter.ch> - 10.2.0-1
- Update to latest upstream release 10.2.0

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 9.1.0-5
- Rebuilt for Python 3.11

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 9.1.0-2
- Rebuilt for Python 3.10

* Tue Feb 16 2021 Josef Ridky <jridky@redhat.com> - 9.1.0-1
- update source url
- new upstream release 9.1.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Josef Ridky <jridky@redhat.com> - 9.0.4-4
- remove asciidoc-music sub-package (lilypond requirement)

* Thu Jan 14 2021 Josef Ridky <jridky@redhat.com> - 9.0.4-3
- remove ImageMagic requirement

* Sun Dec 06 2020 Richard Shaw <hobbes1069@gmail.com> - 9.0.4-2
- Add patch to fix problem with not respecting newline configuration.
- Remove unused patches.

* Sat Oct 31 2020 Fabian Affolter <mail@fabian-affolter.ch> - 9.0.4-1
- Detection of latest Python releases (#1889725)
- Update to latest upstream release 9.0.4

* Wed Oct 14 2020 Fabian Affolter <mail@fabian-affolter.ch> - 9.0.2-1
- Remove patches
- Remove Vim support
- Update to latest upstream release 9.0.2

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.10-0.16.20180605git986f99d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 8.6.10-0.15.20180605git986f99d
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.10-0.14.20180605git986f99d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 8.6.10-0.13.20180605git986f99d
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 8.6.10-0.12.20180605git986f99d
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.10-0.10.20180605git986f99d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.10-0.9.20180605git986f99d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Josef Ridky <jridky@redhat.com> - 8.6.10-0.8.20180605git986f99d
- Fix deprecation warning (#165537)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.10-0.7.20180605git986f99d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 8.6.10-0.6.20180605git986f99d
- Rebuilt for Python 3.7

* Sat Jun 16 2018 Todd Zullinger <tmz@pobox.com> - 8.6.10-0.5.20180605git986f99d
- Add some a2x decoding fixes from upstream PR#5
  (https://github.com/asciidoc/asciidoc-py3/pull/5)

* Fri Jun 15 2018 Todd Zullinger <tmz@pobox.com> - 8.6.10-0.4.20180605git986f99d
- Restore BUGS.txt and CHANGELOG.txt doc files

* Wed Jun 13 2018 Todd Zullinger <tmz@pobox.com> - 8.6.10-0.3.20180605git986f99d
- Use upstream tarball
- Various rpmlint fixes

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 8.6.10-0.2.20180605git986f99d
- Rebuilt for Python 3.7

* Wed Jun 06 2018 Josef Ridky <jridky@redhat.com> - 8.6.10-0.1.20180605git986f99d
- Fix versioning, Source and Url label information to align with Fedora Packaging Guidelines

* Tue Jun 05 2018 Josef Ridky <jridky@redhat.com> - 8.6.8-16.986f99d
- New upstream version with Python3 support - asciidoc-py3 (commit 986f99d)

* Wed Feb 14 2018 Josef Ridky <jridky@redhat.com> - 8.6.8-15
- spec file cleanup (remove Group tag, use autosetup)
- add python2 build support for RHEL

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 06 2017 Todd Zullinger <tmz@pobox.com> - 8.6.8-13
- Explicitly use python2, in preparation for python3 becoming the default
  python

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.6.8-10
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 30 2015 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.6.8-8
- Fix build due to doc files (rhbz#1266596)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.6.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.6.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Nils Philippsen <nils@redhat.com> - 8.6.8-5
- explicitly use system copy of Python 2.x
- fix broken and remove dangling symlinks

* Tue Dec 03 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.6.8-3
- Fix duplicate documentation files (#1001234)
- Fix encoding of manifests being written (#968308)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.6.8-1
- Update to latest upstream version
- Move things around make docs dir actually working
- Add proper requires on vim-filesystem
- Run testsuite
- Split music and latex support to subpackages

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 8.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Sep  8 2009 Ville Skyttä <ville.skytta@iki.fi> - 8.4.5-4
- Remaining improvements from #480288:
- Add dependencies on libxslt and docbook-style-xsl.
- Install dblatex style sheets.
- Exclude unneeded *.py[co].
- Install python API.
- Specfile cleanups.

* Thu Aug 13 2009 Todd Zullinger <tmz@pobox.com> - 8.4.5-3
- Use 'unsafe' mode by default (bug 506953)
- Install filter scripts in %%{_datadir}/asciidoc
- Convert spec file, CHANGELOG, and README to utf-8
- Preserve timestamps on installed files, where feasible
- s/$RPM_BUILD_ROOT/%%{buildroot} and drop duplicated /'s
- Fix rpmlint mixed-use-of-spaces-and-tabs and end-of-line-encoding warnings

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Dave Airlie <airlied@redhat.com> 8.4.5-1
- new upstream version 8.4.5 - required by X.org libXi to build

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 8.2.5-3
- fix license tag

* Wed Dec 05 2007 Florian La Roche <laroche@redhat.com> - 8.2.5-2
- remove doc/examples from filelist due to dangling symlinks

* Tue Nov 20 2007 Florian La Roche <laroche@redhat.com> - 8.2.5-1
- new upstream version 8.2.5

* Mon Oct 22 2007 Florian La Roche <laroche@redhat.com> - 8.2.3-1
- new upstream version 8.2.3

* Sat Sep 01 2007 Florian La Roche <laroche@redhat.com> - 8.2.2-1
- new upstream version 8.2.2

* Mon Mar 19 2007 Chris Wright <chrisw@redhat.com> - 8.1.0-1
- update to asciidoc 8.1.0

* Thu Sep 14 2006 Chris Wright <chrisw@redhat.com> - 7.0.2-3
- rebuild for Fedora Extras 6

* Tue Feb 28 2006 Chris Wright <chrisw@redhat.com> - 7.0.2-2
- rebuild for Fedora Extras 5

* Mon Aug 29 2005 Chris Wright <chrisw@osdl.org> - 7.0.2-1
- convert spec file to UTF-8
- Source should be URL
- update to 7.0.2

* Fri Aug 19 2005 Chris Wright <chrisw@osdl.org> - 7.0.1-3
- consistent use of RPM_BUILD_ROOT

* Thu Aug 18 2005 Chris Wright <chrisw@osdl.org> - 7.0.1-2
- Update BuildRoot
- use _datadir
- use config and _sysconfdir

* Wed Jun 29 2005 Terje Røsten <terje.rosten@ntnu.no> - 7.0.1-1
- 7.0.1
- Drop patch now upstream
- Build as noarch (Petr Klíma)

* Sat Jun 11 2005 Terje Røsten <terje.rosten@ntnu.no> - 7.0.0-0.3
- Add include patch

* Fri Jun 10 2005 Terje Røsten <terje.rosten@ntnu.no> - 7.0.0-0.2
- Fix stylesheets according to Stuart

* Fri Jun 10 2005 Terje Røsten <terje.rosten@ntnu.no> - 7.0.0-0.1
- Initial package
- Based on Debian package, thx!
