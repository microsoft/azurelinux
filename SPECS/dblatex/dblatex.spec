## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 29;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       dblatex
Version:    0.3.12
Release:    %autorelease
Summary:    DocBook to LaTeX/ConTeXt Publishing
BuildArch:  noarch
# Most of package is GPLv2+, except:
# xsl/ directory is DMIT
# lib/dbtexmf/core/sgmlent.txt is Public Domain
# latex/misc/enumitem.sty, multirow2.sry and ragged2e.sty are LPPL
# latex/misc/lastpage.sty is GPLv2 (no +)
# latex/misc/passivetex is MIT (not included in binary RPM so not listed)
License:    GPL-2.0-or-later AND GPL-2.0-only AND LPPL-1.3a AND LicenseRef-DMIT AND LicenseRef-Fedora-Public-Domain
URL:        http://dblatex.sourceforge.net/
Source0:    http://downloads.sourceforge.net/%{name}/%{name}3-%{version}.tar.bz2
# Source1 is from http://docbook.sourceforge.net/release/xsl/current/COPYING
Source1:    COPYING-docbook-xsl
Patch0:     dblatex-0.3.11-disable-debian.patch
Patch1:     dblatex-0.3.11-which-shutil.patch
Patch2:     dblatex-0.3.11-replace-inkscape-by-rsvg.patch
# Patch3 sent upstream: https://sourceforge.net/p/dblatex/patches/12/
Patch3:     dblatex-0.3.12-replace-imp-by-importlib.patch
# Patch4 sent upstream: https://sourceforge.net/p/dblatex/patches/13/
Patch4:     dblatex-0.3.12-adjust-submodule-imports.patch
# Upstreamable
Patch5:     dblatex-0.3.12-remove-shebangs-from-non-scripts.patch

BuildRequires:  python3-devel
BuildRequires:  libxslt
BuildRequires:  texlive-base
BuildRequires:  texlive-collection-latex
BuildRequires:  texlive-collection-xetex
BuildRequires:  texlive-xmltex-bin
BuildRequires:  texlive-anysize
BuildRequires:  texlive-appendix
BuildRequires:  texlive-changebar
BuildRequires:  texlive-fancybox
BuildRequires:  texlive-jknapltx
BuildRequires:  texlive-multirow
BuildRequires:  texlive-overpic
BuildRequires:  texlive-passivetex
BuildRequires:  texlive-pdfpages
BuildRequires:  texlive-subfigure
BuildRequires:  texlive-stmaryrd
BuildRequires:  texlive-wasysym
Requires:       texlive-base
Requires:       texlive-collection-latex
Requires:       texlive-collection-xetex
Requires:       texlive-collection-fontsrecommended
Requires:       texlive-xmltex texlive-xmltex-bin
Requires:       texlive-anysize
Requires:       texlive-appendix
Requires:       texlive-bibtopic
Requires:       texlive-changebar
Requires:       texlive-ec
Requires:       texlive-fancybox
Requires:       texlive-jknapltx
Requires:       texlive-multirow
Requires:       texlive-overpic
Requires:       texlive-passivetex
Requires:       texlive-pdfpages
Requires:       texlive-subfigure
Requires:       texlive-stmaryrd
Requires:       texlive-wasysym
Requires:       texlive-xmltex-bin
Requires:       libxslt docbook-dtds
Recommends:     ImageMagick
Recommends:     texlive-epstopdf-bin
Recommends:     transfig
Recommends:     librsvg2-tools

%description
dblatex is a program that transforms your SGML/XMLDocBook
documents to DVI, PostScript or PDF by translating them
into pure LaTeX as a first process.  MathML 2.0 markups
are supported, too. It started as a clone of DB2LaTeX.

Authors:
--------
   Benoît Guillon <marsgui at users dot sourceforge dot net>
   Andreas Hoenen <andreas dot hoenen at arcor dot de>


%prep
%autosetup -n %{name}3-%{version} -p 1
# build_scripts uses install command arguments
sed -i -e "/if not(install.install_data)/i \        install.install_data = '%{_prefix}'" setup.py
sed -i -e "s|self._install_lib = .*|self._install_lib = '%{python3_sitelib}'|" setup.py

# We do not ship contrib parts:
rm -rf lib/contrib

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -L dbtexmf

# these are already in tetex-latex:
for file in bibtopic.sty enumitem.sty ragged2e.sty passivetex/ xelatex/; do
  rm -rf $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/misc/$file
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/texlive/texmf-dist/tex/latex/dblatex
for file in ` find $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/ -name '*.sty' ` ; do
  mv $file $RPM_BUILD_ROOT%{_datadir}/texlive/texmf-dist/tex/latex/dblatex/`basename $file`;
done

## also move .xetex files
for file in ` find $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/ -name '*.xetex' ` ; do
  mv $file $RPM_BUILD_ROOT%{_datadir}/texlive/texmf-dist/tex/latex/dblatex/`basename $file`;
done

rmdir $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/{misc,contrib/example,style}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dblatex
# shipped in %%docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/

sed -e 's/\r//' xsl/mathml2/README > README-xsltml
touch -r xsl/mathml2/README README-xsltml
cp -p %{SOURCE1} COPYING-docbook-xsl

%files -f %{pyproject_files}
%{_mandir}/man1/dblatex.1*
%doc COPYRIGHT docs/manual.pdf COPYING-docbook-xsl README-xsltml
%{_bindir}/dblatex
%{_datadir}/dblatex/
%{_datadir}/texlive/texmf-dist/tex/latex/dblatex/
%dir %{_sysconfdir}/dblatex

%post -p /usr/bin/texhash

%postun -p /usr/bin/texhash

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 0.3.12-29
- Latest state for dblatex

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.3.12-28
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.3.12-27
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Michael J Gruber <mjg@fedoraproject.org> - 0.3.12-25
- switch to pyproject macros (rhbz#2378537)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.3.12-24
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.3.12-21
- Rebuilt for Python 3.13

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Michael J Gruber <mjg@fedoraproject.org> - 0.3.12-14
- Fix Py 3.12 imports (rhbz#2220636)

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.3.12-13
- Rebuilt for Python 3.12

* Tue Jun 06 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.3.12-12
- Remove obsolete texlive-collection-htmlxml dependency

* Wed Mar 29 2023 Michael J Gruber <mjg@fedoraproject.org> - 0.3.12-11
- Adjust patch macro usage to rpm >= 4.18 in a cleaner way

* Tue Mar 28 2023 Than Ngo <than@redhat.com> - 0.3.12-10
- Fix deprecated patch rpm macro

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 06 2022 Michael J Gruber <mjg@fedoraproject.org> - 0.3.12-8
- SPDX migration

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.3.12-6
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.3.12-3
- Rebuilt for Python 3.10

* Thu Feb 18 2021 Michael J Gruber <mjg@fedoraproject.org> - 0.3.12-2
- replace inkscape by rsvg (#bz 1833047)

* Thu Feb 18 2021 Michael J Gruber <mjg@fedoraproject.org> - 0.3.12-1
- rebase to 0.3.12
- follow yet another package/tree renaming

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Michael J Gruber <mjg@fedoraproject.org> - 0.3.11-6
- BR setuptools explicitly

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.11-5
- Rebuilt for Python 3.9

* Wed Feb 05 2020 Michael J Gruber <mjg@fedoraproject.org> - 0.3.11-4
- rebase to upstreamed py3 version (bz 1796232)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 23 2019 Michael J Gruber <mjg@fedoraproject.org> - 0.3.11-2
- port to python3 (bz #1737967)

* Sun Sep 22 2019 Michael J Gruber <mjg@fedoraproject.org> - 0.3.11-1
- bugfix release (bz #1753399)

* Tue Sep 10 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.3.10-12
- Rebundle python2-which.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Michael J Gruber <mjg@fedoraproject.org> - 0.3.10-10
- fix FTBFS on F30 (#1674789)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 10 2018 Michael J Gruber <mjg@fedoraproject.org> - 0.3.10-8
- make shebangs unambiguous

* Fri Jul 13 2018 Michael J Gruber <mjg@fedoraproject.org> - 0.3.10-7
- adjust to py2 packaging guidelines (fix FTBFS on rawhide)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 11 2018 Nikola Forró <nforro@redhat.com> - 0.3.10-5
- make non-critical graphic tools weak dependencies
- recommend inkscape, which can be used to convert SVG images

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.10-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 05 2017 Michael J Gruber <mjg@fedoraproject.org> - 0.3.10-1
- rebase with upstream

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 17 2016 Michael J Gruber <mjg@fedoraproject.org> - 0.3.9-1
- bugfix and feature release

* Mon Aug 01 2016 Michael J Gruber <mjg@fedoraproject.org> - 0.3.8-1
- bugfix and feature release

* Mon Aug 01 2016 Michael J Gruber <mjg@fedoraproject.org> - 0.3.7-1
- bugfix release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 jchaloup <jchaloup@redhat.com> - 0.3.6-1
- Update to 0.3.6
  resolves: #1222169

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 jchaloup <jchaloup@redhat.com> - 0.3.5-1
- Update to 0.3.5.

* Thu Aug 08 2013 Michael J Gruber <mjg@fedoraproject.org> - 0.3.4-8
- Merge in licensing changes from  Stanislav Ochotnicky <sochotnicky@redhat.com>:
-* Mon Jul 29 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.4-8
-- Add Public Domain license and licensing comment
-* Mon Jul 29 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.4-7
-- Add DMIT, GPLv2 and LPPL licenses
-- Fix space and tab mixing
-- Cleanup old spec file parts

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Michael J Gruber <mjg@fedoraproject.org> - 0.3.4-6
- Add mising R texlive-multirow.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Benjamin De Kosnik  <bkoz@redhat.com> - 0.3.4-1
- Update to 0.3.4.
- Adjust for texlive rebase.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Apr 12 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.3-1
- Update to 0.3
- Cleanup spec: drop some unnecessary conditionals for old releases (< F-11)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 10 2009 Neal Becker <ndbecker2@gmail.com> - 0.2.10-2
- remove dblatex-0.2.9-xetex.patch

* Sun May 10 2009 Neal Becker <ndbecker2@gmail.com> - 0.2.10-1
- Update to 0.2.10

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.9-3
- Rebuild for Python 2.6

* Fri Jul  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.2.9-2
- BR: texlive-xetex -> tex(xetex) for F-10 and later

* Thu Jun 12 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.2.9-1
- Update to latest upstream (0.2.9) (#448953)
- Remove some redundant Requires and BuildRequires (passivetex pulls
  in the tetex/tex requires, python dep added automatically)
- For F-9+ BR on tex(latex) and texlive-xetex, fix the installation
  scripts to install extra new files.
- Add patch from dblatex mailing list for better handling of a missing
  xetex.
- Conditionally add .egg-info file only if F9+ to allow for unified
  spec file

* Sun Dec 16 2007 Patrice Dumas <pertusus@free.fr> - 0.2.8-2.1
- don't install in docbook directory, it is a link to a versioned
  directory and may break upon docbook update (#425251,#389231)

* Sun Nov 25 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.8-1
- Update to 0.2.8

* Mon Nov 12 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-16
- convert spec to utf8
- change to gplv2+

* Mon Nov 12 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-15
- Add copyright info

* Mon Nov  5 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-14
- Req tetex-fonts for texhash
- Fix post, postun

* Sun Nov  4 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-13
- Add texhash

* Sun Nov  4 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-12
- Fix xsl link

* Sat Nov  3 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-12
- Various fixes from pertusus@free.fr:
- rm iconv stuff
- simplify docs installation

* Fri Nov  2 2007  <ndbecker2@gmail.com> - 0.2.7-11
- Various minor fixes

* Thu Nov  1 2007  <ndbecker2@gmail.com> - 0.2.7-10
- Add some reqs and brs
- rmdir /usr/share/dblatex/latex/{misc,contrib/example,style}

* Sat Oct 27 2007  <ndbecker2@gmail.com> - 0.2.7-9
- link /usr/share/dblatex/xsl -> /usr/share/sgml/docbook/xsl-stylesheets/dblatex
- rmdir /usr/share/dblatex/latex/{misc,specs,style}
- own /etc/dblatex
- change $(...) -> `...`
- Preserve timestamps on iconv

* Mon Oct 15 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-9
- mv all .sty files to datadir/texmf/tex/latex/dblatex
- Add Conflicts tetex-tex4ht
- mv all xsl stuff to datadir/sgml/docbook/xsl-stylesheets/dblatex/

* Mon Oct 15 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-8
- rm redundant latex files

* Tue Sep 25 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-8
- Fixed encodings in docs directory
- Install docs at correct location

* Fri Sep 21 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-7
- Revert back to GPLv2
- untabify

* Fri Sep 21 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-6
- Fix source URL
- Install all docs
- Tabify

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-5
- Add BR tetex-latex

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-4
- Add  BR tetex, ImageMagick

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-3
- Add BR libxslt

* Wed Sep 19 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-2
- Add BR python-devel

* Fri Sep  7 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-1
- Initial

## END: Generated by rpmautospec
