## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        Enhanced TeX modes for Emacs
Name:           emacs-auctex
Version:        14.1.2
Release:        %autorelease

# The project as a whole is GPL-3.0-or-later.  Exceptions:
# - doc/intro.texi is FSFAP
# - doc/auctex* and doc/preview* are GFDL-1.3-no-invariants-or-later
# - the generated PDF file contains fonts distributed under Knuth-CTAN
License:        GPL-3.0-or-later AND FSFAP AND GFDL-1.3-no-invariants-or-later AND Knuth-CTAN
URL:            https://www.gnu.org/software/auctex/
VCS:            git:https://git.savannah.gnu.org/cgit/auctex.git
Source:         https://github.com/emacsmirror/auctex/archive/auctex-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  emacs-nw
BuildRequires:  ghostscript
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  tex(german.ldf)
BuildRequires:  tex(tex)
BuildRequires:  texinfo
BuildRequires:  texinfo-tex
BuildRequires:  texlive-latex
BuildRequires:  texlive-mylatex

Requires:       dvipng
Requires:       emacs(bin) >= %{?_emacs_version}%{!?_emacs_version:0}
Requires:       ghostscript
Requires:       tex-preview = %{version}-%{release}
Requires:       texlive-dvips
Requires:       texlive-latex

Recommends:     texlive-mylatex

# This can be removed when F48 reaches EOL
Obsoletes:      %{name}-doc < 14.0.0
Provides:       %{name}-doc = %{version}-%{release}

%description
AUCTeX is an extensible package that supports writing and formatting TeX files
for most variants of Emacs.

AUCTeX supports many different TeX macro packages, including AMS-TeX, LaTeX,
Texinfo and basic support for ConTeXt.  Documentation can be found under
/usr/share/doc, e.g. the reference card (tex-ref.pdf) and the FAQ.  The AUCTeX
manual is available in Emacs info (C-h i d m AUCTeX RET).  On the AUCTeX home
page, we provide manuals in various formats.

AUCTeX includes preview-latex support which makes LaTeX a tightly integrated
component of your editing workflow by visualizing selected source chunks (such
as single formulas or graphics) directly as images in the source buffer.

This package is for GNU Emacs.

%package -n tex-preview
# The content is GPL-3.0-or-later.  The remaining licenses cover the various
# fonts embedded in PDFs.
# CM: Knuth-CTAN
License:        GPL-3.0-or-later AND Knuth-CTAN
Summary:        Preview style files for LaTeX
Requires:       texlive-base
Requires:       texlive-kpathsea
# This is the latest build we accidentally provided from texlive
Obsoletes:      texlive-preview <= 12:svn78824-5
Provides:       texlive-preview = 12:svn78824-5

%description -n tex-preview
The preview package for LaTeX allows for the processing of selected parts of a
LaTeX input file.  This package extracts indicated pieces from a source file
(typically displayed equations, figures and graphics) and typesets with their
base point at the (1in,1in) magic location, shipping out the individual pieces
on separate pages without any page markup.  You can produce either DVI or PDF
files, and options exist that will set the page size separately for each page.
In that manner, further processing (as with Ghostscript or dvipng) will be
able to work in a single pass.

The main purpose of this package is the extraction of certain environments
(most notably displayed formulas) from LaTeX sources as graphics.  This works
with DVI files postprocessed by either Dvips and Ghostscript or dvipng, but it
also works when you are using PDFTeX for generating PDF files (usually also
postprocessed by Ghostscript).

The tex-preview package is generated from the AUCTeX package for Emacs.

%prep
%autosetup -n auctex-auctex-%{version}

%build
%make_build TEX=tex
%make_build preview.pdf TEX=tex

%install
# The makefile no longer has an install target, so install by hand
mkdir -p %{buildroot}%{_emacs_sitelispdir}/auctex
cp -a *.el *.elc images style %{buildroot}%{_emacs_sitelispdir}/auctex

# The tex-site file needs to be one directory higher
mv %{buildroot}%{_emacs_sitelispdir}/auctex/tex-site.el \
   %{buildroot}%{_emacs_sitelispdir}

# The startup files go in _emacs_sitestartdir
mkdir -p %{buildroot}%{_emacs_sitestartdir}
mv %{buildroot}%{_emacs_sitelispdir}/auctex/auctex{,-autoloads}.el* \
   %{buildroot}%{_emacs_sitestartdir}

# Install the info files
mkdir -p %{buildroot}%{_infodir}
cp -p doc/{auctex,preview-latex}.info* %{buildroot}%{_infodir}

# Install the LaTeX files
mkdir -p %{buildroot}%{_texmf_main}/tex/latex/preview
cp -p latex/*.{cfg,def,sty} %{buildroot}%{_texmf_main}/tex/latex/preview
mkdir -p %{buildroot}%{_texmf_main}/doc/latex/preview
cp -p latex/{README,preview.pdf} %{buildroot}%{_texmf_main}/doc/latex/preview

%check
make -C tests

%files
%doc ChangeLog.1 NEWS.org
%doc %{_infodir}/*.info*
%license COPYING
%{_emacs_sitestartdir}/*
%{_emacs_sitelispdir}/auctex/
%{_emacs_sitelispdir}/tex-site.el

%files -n tex-preview
%license COPYING
%{_texmf_main}/tex/latex/preview/
%{_texmf_main}/doc/latex/preview/

%changelog
## START: Generated by rpmautospec
* Tue Sep 01 2026 Unknown User <please-configure-git-user@example.com> - 14.1.2-2
- Uncommitted changes

* Thu May 14 2026 Jerry James <loganjerry@gmail.com> - 14.1.2-1
- Version 14.1.2
- Merge the doc subpackage into the main package
- Recommend texlive-mylatex (needed for preview)
- Add a %%check script

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 13.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 13.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 13.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Jerry James <loganjerry@gmail.com> - 13.3-1
- Version 13.3

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 24 2023 Jerry James <loganjerry@gmail.com> - 13.2-1
- Version 13.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 16 2022 Jerry James <loganjerry@gmail.com> - 13.1-2
- Convert License tags to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Feb 21 2022 Jerry James <loganjerry@gmail.com> - 13.1-1
- Version 13.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 19 2021 Jerry James <loganjerry@gmail.com> - 12.3-1
- Version 12.3
- Drop upstreamed patch to fix FSF address
- Drop ancient obsoletes/provides

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 24 2018 Tom Callaway <spot@fedoraproject.org> - 12.1-4
- Provide/Obsolete texlive-preview in tex-preview subpackage

* Sun Feb 25 2018 Jonathan Underwood <jonathan.underwood@gmail.com> - 12.1-3
- Add patch to fix FSF address in some files

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Than Ngo <than@redhat.com> - 12.1-1
- update to 12.1

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.89-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.89-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 11.89-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.89-2
- Add Provides tex(preview.sty) to preview sub-package

* Sat Nov 14 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.89-1
- Update to 11.89
- Use http for Source location
- Create the .nosearch files with touch, as Makefile no longer does

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.88-1
- Update to 11.88

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.87-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 28 2014 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.87-8
- Add patch to fix BZ 995245

* Wed Feb 12 2014 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.87-7
- Really Fix up installation location of doc files

* Thu Feb  6 2014 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.87-6
- Fix up installation location of doc files

* Thu Feb  6 2014 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.87-5
- Move preview files to be installed under %%{_datadir}/texlive/texmf-dist (BZ 995544)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.87-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.87-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec  4 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.87-2
- Fix the install location of the preview tex files
- Fix the BuildRequires for latex

* Mon Dec  3 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.87-1
- Update to new upstream version 11.87

* Wed Oct  3 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-10
- Fix the Obsoletes and Provides to allow package updating (BZ 862398)

* Wed Sep 19 2012 Karel Klíč <kklic@redhat.com> - 11.86-9
- ELisp source code is no longer distributed in a separate package
- License filed includes GFDL for the documentation

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.86-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.86-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar  8 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-6
- Replace define with global in macro definitions
- Add patch to fix previewing of equations courtesy of Sato Ichi (BZ 646632)
- Add defattr to doc sub-package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 16 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-4
- Duplicate only the COPYING file and not the other docs in the tex-preview
  subpackage

* Fri Jul 16 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-3
- Add COPYING file and other docs to the tex-preview subpackage to comply with
  updated licensing guidelines
- Remove the no longer needed BuildRoot, %%clean and cleaning of Buildroot
  inside %%install

* Sun May 23 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-2
- Drop Requires for evince (rhbz 595104)

* Sat Mar  6 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-1
- Update to 11.86
- Drop unneeded patch for PDF and HTML viewing

* Thu Jan 28 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-11
- Add patch to use evince for PDF file viewing and xdg-open for html file
  viewing
- Add Requires for evince

* Sat Nov  7 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-10
- Update spec file to use macros defined in /etc/rpm/macros.emacs
- Fix typo in spec comments

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.85-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.85-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 24 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-7
- Add Requires for dvipng

* Sat Feb 16 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-6
- Preserve timestamp of RELEASE when converting to UTF8

* Wed Feb 13 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-5
- Re-add creation of emacs_startdir

* Tue Feb 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-4
- Remove BuildRequires for pkgconfig - not needed
- Clean out uneeded creation of site start directory
- Remove /usr/share/doc/auctex directory from buildroot

* Tue Feb 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-3
- Bump release and rebuild - had forgotten to upload the new sources

* Tue Feb 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-2
- Add BuilddRequires for pkgconfig

* Tue Feb 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-1
- Update to version 11.85
- Change license to GPLv3+ accordingly

* Wed Jan 23 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-7
- tex-preview no longer Requires ghostscript (#429811)
- Use virtual provides for tex(latex) etc.

* Tue Dec 25 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-6
- Add Obsolotes and Provides for tetex-preview to tex-preview (#426758)

* Sun Dec 23 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-5
- Enable building of separate tex-preview package
- Remove a few residual tetex references

* Sun Dec 16 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-4
- Add macros for automatic detection of Emacs version, site-lisp directory etc
- Make building of tex-preview subpackage optional, and disable for now
- Adjust Requires and BuildRequires for texlive
- Remove auctex-init.el since not needed
- Make RELEASE utf8

* Sat Aug  4 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-3
- Clarify license version
- Correct version and release requirement for the el package

* Sat Jan 13 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-2
- Update BuildRequires for texinfo-tex package

* Sat Jan 13 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-1
- Update to version 11.84
- Build all documentation and package in a -doc package

* Mon Aug 28 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-7
- Bump release for FC-6 mass rebuild

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-6
- Remove debug patch entry

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-5
- Bump release

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-4
- Bump release

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-3
- Sync with FC-5 spec file which includes the following changes
- No longer use makeinstall macro
- No longer specify texmf-dir, tex-dir for configure
- Main package now owns the site-lisp auctex and styles directories
- Place preview.dvi in correct directory, and have tetex-preview own
  it
- General cleanups

* Sat Jun 10 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-4
- Bump release

* Sat Jun 10 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-3
- Bump release. Wrap descriptions at column 70.

* Sat Jun 10 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-1
- Update to 11.83
- Add specific release requirement to tetex-preview Requires of main package

* Wed May 24 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-12
- Bump version number.

* Wed May 24 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-11
- Fix up whitespace for Ed. Bump version number.

* Thu May 18 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-9
- Split out tetex-preview subpackage
- Split out source elisp files
- Update package descriptions

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-8
- Add tetex-latex to BuildRequires

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-7
- Add ghostscript to Requires and BuildRequires

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-6
- Leave .nosearch file in styles directory - this directory shouldn't be in the load-path

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-5
- Move installation of the preview style files out of the texmf tree for now

* Mon Apr 24 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-4
- Added preview-latex
- Removed INSTALL document from package (not necessary)
- Clean up generation of startup files from spec file

* Thu Apr 20 2006 Ed Hill <ed@eh3.com> - 11.82-3
- fix startup file per bug# 189488

* Sun Apr  9 2006 Ed Hill <ed@eh3.com> - 11.82-2
- rebuild

* Sun Apr  9 2006 Ed Hill <ed@eh3.com> - 11.82-1
- update to 11.82

* Fri Sep 30 2005 Ed Hill <ed@eh3.com> - 11.81-2
- fix stupid tagging mistake

* Fri Sep 30 2005 Ed Hill <ed@eh3.com> - 11.81-1
- update to 11.81
- disable preview for now since it needs some packaging work

* Tue Sep  6 2005 Ed Hill <ed@eh3.com> - 11.55-5
- bugzilla 167439

* Tue Aug  9 2005 Ed Hill <ed@eh3.com> - 11.55-4
- call it BuildArch

* Tue Aug  9 2005 Ed Hill <ed@eh3.com> - 11.55-3
- add Requires and BuildRequires

* Mon Aug  8 2005 Ed Hill <ed@eh3.com> - 11.55-2
- modify for acceptance into Fedora Extras

* Fri Jan 21 2005 David Kastrup <dak@gnu.org>
- Conflict with outdated Emacspeak versions

* Fri Jan 14 2005 David Kastrup <dak@gnu.org>
- Install and remove auctex.info, not auctex

* Thu Aug 19 2004 David Kastrup <dak@gnu.org>
- Change tex-site.el to overwriting config file mode.  New naming scheme.

* Mon Aug 16 2004 David Kastrup <dak@gnu.org>
- Attempt a bit of SuSEism.  Might work if we are lucky.

* Sat Dec  7 2002 David Kastrup <David.Kastrup@t-online.de>
- Change addresses to fit move to Savannah.

* Mon Apr 15 2002 Jan-Ake Larsson <jalar@imf.au.dk>
- Adjusted TeX-macro-global and put autoactivation in preinstall
  script so that it can be chosen at install time.

* Tue Feb 19 2002 Jan-Ake Larsson <jalar@imf.au.dk>
- Added site-start.el support

* Sat Feb 16 2002 Jan-Ake Larsson <jalar@imf.au.dk>
- Prerelease 11.11

## END: Generated by rpmautospec
