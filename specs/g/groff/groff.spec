# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?with_x:%global with_x 1}

Summary: A document formatting system
Name: groff
Version: 1.23.0
Release: 12%{?dist}
# Everything is under GPL-3.0-or-later, except for the following files:
# MIT license
#  -- tmac/hyphen.den
#     tmac/hyphen.det
# GFDL license
#  -- contrib/mom/momdoc/*
#     contrib/pdfmark/pdfmark.ms
#     contrib/pdfmark/pdfroff.1.man
#     contrib/hdtbl/groff_hdtbl.7.man
#     tmac/groff_trace.7.man
#     src/roff/groff/groff.1.man
#     src/roff/troff/troff.1.man
#     man/groff_diff.7.man
#     man/ditroff.7.man
#     man/groff_out.5.man
#     man/groff_tmac.5.man
#     man/groff.7.man
#     man/roff.7.man
#     doc/fdl.texi
#     doc/groff.texi
# BSD-4-Clause-UC
#  -- tmac/doc.tmac
#     tmac/doc-old.tmac
#     tmac/doc-common
#     tmac/doc-ditroff
#     tmac/doc-nroff
#     tmac/doc-syms
#     tmac/groff_mdoc.man
#     tmac/e.tmac
#     tmac/groff_me.man
#     doc/meintro.me
#     doc/meintro_fr.me
#     doc/meref.me
# X11 license
#  -- src/devices/xditview/*
# Public domain
#  -- src/preproc/grn
#     contrib/grap2graph/grap2graph.sh
#     contrib/pic2graph/pic2graph.sh
#     contrib/eqn2graph/eqn2graph.sh
License: GPL-3.0-or-later AND GFDL-1.3-or-later AND BSD-4-Clause-UC AND MIT AND X11 AND LicenseRef-Fedora-Public-Domain
URL: http://www.gnu.org/software/groff/
Source: https://ftp.gnu.org/gnu/groff/groff-%{version}.tar.gz

# resolves: #530788
Patch0: 0001-missing-groff-x11-info-message-when-gxditview-not-fo.patch
Patch1: 0002-load-site-font-and-site-tmac-from-etc-groff.patch
# resolves: #709413, #720058, #720057
Patch2: 0003-various-security-fixes.patch
# resolves: #987069
Patch3: 0004-don-t-use-usr-bin-env-in-shebang.patch
# allow to specify custom docdir
Patch4: 0005-do-not-overwrite-docdir.patch
# Revert upstream change of mapping special characters for UTF-8 devices
# Debian commit: https://salsa.debian.org/debian/groff/-/commit/d5394c68d70e6c5199b01d2522e094c8fd52e64e
Patch5: 0006-Revert-upstream-change-of-mapping-special-characters.patch

Requires: coreutils, groff-base = %{version}-%{release}

Recommends: psutils

Requires(post): /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
Requires(preun): /usr/sbin/update-alternatives

BuildRequires: gcc, gcc-c++
BuildRequires: bison, texinfo
# psutils is required for the "psselect" command
BuildRequires: git, netpbm-progs, perl-generators, psutils, ghostscript

Provides: nroff-i18n = %{version}-%{release}
Provides: bundled(gnulib)

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\([^.]*\\.pl\\)

%description
Groff is a document formatting system. Groff takes standard text and
formatting commands as input and produces formatted output. The
created documents can be shown on a display or printed on a printer.
Groff's formatting commands allow you to specify font type and size,
bold type, italic type, the number and size of columns on a page, and
more.

Groff can also be used to format man pages. If you are going to use
groff with the X Window System, you will also need to install the
groff-x11 package.

%package base
Summary: Parts of the groff formatting system required to display manual pages
Requires(post): /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
Requires(preun): /usr/sbin/update-alternatives

%description base
The groff-base package contains only necessary parts of groff formatting
system which are required to display manual pages, and the groff's default
display device (PostScript).

%package perl
Summary: Parts of the groff formatting system that require Perl
Requires: groff-base = %{version}-%{release}

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl. These include the afmtodit (font processor
for creating PostScript font files), groffer (tool for displaying groff
files), grog (utility that can be used to automatically determine groff
command-line options), chem (groff preprocessor for producing chemical
structure diagrams), mmroff (reference preprocessor) and roff2dvi
roff2html roff2pdf roff2ps roff2text roff2x (roff code converters).

%if %{with_x}
%package x11
Summary: Parts of the groff formatting system that require X Windows System
Requires: groff-base = %{version}-%{release}
BuildRequires: libXaw-devel, libXmu-devel
BuildRequires: make
Provides: groff-gxditview = %{version}-%{release}
Obsoletes: groff-gxditview < 1.20.1

%description x11
The groff-x11 package contains the parts of the groff text processor
package that require X Windows System. These include gxditview (display
groff intermediate output files on X Window System display) and
xtotroff (converts X font metrics into groff font metrics).
%endif

%package doc
Summary: Documentation for groff document formatting system
BuildArch: noarch
Requires: groff = %{version}-%{release}

%description doc
The groff-doc package includes additional documentation for groff
text processor package. It contains examples, documentation for PIC
language and documentation for creating PDF files.

%prep
%setup -q
git init
git config user.email groff-owner@fedoraproject.org
git config user.name "groff owner"
git add .
git commit -n -m "release %{version}"
git am %{patches}

for file in NEWS src/devices/grolbp/grolbp.1.man doc/webpage.ms \
                contrib/mm/*.man contrib/mom/examples/{README.txt,*.mom,mom.vim}; do
    iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
    mv "${file}_" "$file"
done

%build
%configure \
    --docdir=%{_pkgdocdir} \
    --with-appdefdir=%{_datadir}/X11/app-defaults \
    --with-grofferdir=%{_datadir}/%{name}/%{version}/groffer
%make_build

%install
%make_install

# rename files for alternative usage
mv %{buildroot}%{_bindir}/soelim %{buildroot}%{_bindir}/soelim.%{name}
touch %{buildroot}%{_bindir}/soelim
mv %{buildroot}%{_mandir}/man1/soelim.1 %{buildroot}%{_mandir}/man1/soelim.%{name}.1
touch %{buildroot}%{_mandir}/man1/soelim.1
mv %{buildroot}%{_mandir}/man7/roff.7 %{buildroot}%{_mandir}/man7/roff.%{name}.7
touch %{buildroot}%{_mandir}/man7/roff.7

# some binaries need alias with 'g' or 'z' prefix
for file in g{nroff,troff,tbl,pic,eqn,neqn,refer,lookbib,indxbib,soelim} zsoelim; do
    ln -s ${file#?} %{buildroot}%{_bindir}/${file}
    ln -s ${file#?}.1.gz %{buildroot}%{_mandir}/man1/${file}.1.gz
done

# fix absolute symlink to relative symlink
rm -f %{buildroot}%{_pkgdocdir}/pdf/mom-pdf.pdf
ln -s ../examples/mom/mom-pdf.pdf %{buildroot}%{_pkgdocdir}/pdf/mom-pdf.pdf

# rename groff downloadable postscript fonts to meet Fedora Font Packaging guidelines,
# as these files are more PS instructions, than general-purpose fonts (bz #477394)
for file in $(find %{buildroot}%{_datadir}/%{name}/%{version}/font/devps -name "*.pfa"); do
    mv ${file} ${file}_
done
sed --in-place 's/\.pfa$/.pfa_/' %{buildroot}%{_datadir}/%{name}/%{version}/font/devps/download

# remove unnecessary files
rm -f %{buildroot}%{_infodir}/dir

# remove CreationDate from documentation
pushd %{buildroot}%{_pkgdocdir}
    find -name "*.html" | xargs sed -i "/^<!-- CreationDate: /d"
    find -name "*.ps"   | xargs sed -i "/^%%%%CreationDate: /d"
popd

# /bin/sed moved to /usr/bin/sed in Fedora
sed --in-place 's|#! /bin/sed -f|#! /usr/bin/sed -f|' %{buildroot}%{_datadir}/groff/%{version}/font/devps/generate/symbol.sed

%pre
# remove alternativized files if they are not symlinks
[ -L %{_mandir}/man7/roff.7.gz ] || %{__rm} -f %{_mandir}/man7/roff.7.gz >/dev/null 2>&1 || :

%post
# set up the alternatives files
/usr/sbin/update-alternatives --install %{_mandir}/man7/roff.7.gz roff.7.gz %{_mandir}/man7/roff.%{name}.7.gz 300 \
    >/dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ]; then
    /usr/sbin/update-alternatives --remove roff.7.gz %{_mandir}/man7/roff.%{name}.7.gz >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ]; then
    if [ "$(readlink /etc/alternatives/roff.7.gz)" == "%{_mandir}/man7/roff.%{name}.7.gz" ]; then
        /usr/sbin/update-alternatives --set roff.7.gz %{_mandir}/man7/roff.%{name}.7.gz >/dev/null 2>&1 || :
    fi
fi

%pre base
# remove alternativized files if they are not symlinks
[ -L %{_bindir}/soelim ] || %{__rm} -f %{_bindir}/soelim >/dev/null 2>&1 || :
[ -L %{_mandir}/man1/soelim.1.gz ] || %{__rm} -f %{_mandir}/man1/soelim.1.gz >/dev/null 2>&1 || :

%post base
# set up the alternatives files
/usr/sbin/update-alternatives --install %{_bindir}/soelim soelim %{_bindir}/soelim.%{name} 300 \
    --slave %{_mandir}/man1/soelim.1.gz soelim.1.gz %{_mandir}/man1/soelim.%{name}.1.gz \
    >/dev/null 2>&1 || :

%preun base
if [ $1 -eq 0 ]; then
    /usr/sbin/update-alternatives --remove soelim %{_bindir}/soelim.%{name} >/dev/null 2>&1 || :
fi

%postun base
if [ $1 -ge 1 ]; then
    if [ "$(readlink /etc/alternatives/soelim)" == "%{_bindir}/soelim.%{name}" ]; then
        /usr/sbin/update-alternatives --set soelim %{_bindir}/soelim.%{name} >/dev/null 2>&1 || :
    fi
fi

%files
# data
%{_datadir}/%{name}/%{version}/font/devcp1047/
%{_datadir}/%{name}/%{version}/font/devdvi/
%{_datadir}/%{name}/%{version}/font/devlbp/
%{_datadir}/%{name}/%{version}/font/devlj4/
%{_datadir}/%{name}/%{version}/oldfont/
%{_datadir}/%{name}/%{version}/pic/
%{_datadir}/%{name}/%{version}/tmac/62bit.tmac
%{_datadir}/%{name}/%{version}/tmac/dvi.tmac
%{_datadir}/%{name}/%{version}/tmac/e.tmac
%{_datadir}/%{name}/%{version}/tmac/ec.tmac
%{_datadir}/%{name}/%{version}/tmac/hdmisc.tmac
%{_datadir}/%{name}/%{version}/tmac/hdtbl.tmac
%{_datadir}/%{name}/%{version}/tmac/lbp.tmac
%{_datadir}/%{name}/%{version}/tmac/lj4.tmac
%{_datadir}/%{name}/%{version}/tmac/m.tmac
%{_datadir}/%{name}/%{version}/tmac/me.tmac
%{_datadir}/%{name}/%{version}/tmac/mm.tmac
%{_datadir}/%{name}/%{version}/tmac/mm/
%{_datadir}/%{name}/%{version}/tmac/mmse.tmac
%{_datadir}/%{name}/%{version}/tmac/mom.tmac
%{_datadir}/%{name}/%{version}/tmac/ms.tmac
%{_datadir}/%{name}/%{version}/tmac/mse.tmac
%{_datadir}/%{name}/%{version}/tmac/om.tmac
%{_datadir}/%{name}/%{version}/tmac/pdfmark.tmac
%{_datadir}/%{name}/%{version}/tmac/refer-me.tmac
%{_datadir}/%{name}/%{version}/tmac/refer-mm.tmac
%{_datadir}/%{name}/%{version}/tmac/refer-ms.tmac
%{_datadir}/%{name}/%{version}/tmac/refer.tmac
%{_datadir}/%{name}/%{version}/tmac/s.tmac
%{_datadir}/%{name}/%{version}/tmac/spdf.tmac
%{_datadir}/%{name}/%{version}/tmac/trace.tmac
%{_datadir}/%{name}/%{version}/tmac/zh.tmac
# programs
%{_bindir}/addftinfo
%{_bindir}/eqn2graph
%{_bindir}/gdiffmk
%{_bindir}/grap2graph
%{_bindir}/grn
%{_bindir}/grodvi
%{_bindir}/grolbp
%{_bindir}/grolj4
%{_bindir}/hpftodit
%{_bindir}/indxbib
%{_bindir}/lkbib
%{_bindir}/lookbib
%{_bindir}/pdfroff
%{_bindir}/pfbtops
%{_bindir}/pic2graph
%{_bindir}/refer
%{_bindir}/tfmtodit
%{_mandir}/man1/addftinfo.*
%{_mandir}/man1/eqn2graph.*
%{_mandir}/man1/gdiffmk.*
%{_mandir}/man1/grap2graph.*
%{_mandir}/man1/grn.*
%{_mandir}/man1/grodvi.*
%{_mandir}/man1/grohtml.*
%{_mandir}/man1/grolbp.*
%{_mandir}/man1/grolj4.*
%{_mandir}/man1/hpftodit.*
%{_mandir}/man1/indxbib.*
%{_mandir}/man1/lkbib.*
%{_mandir}/man1/lookbib.*
%{_mandir}/man1/pdfroff.*
%{_mandir}/man1/pfbtops.*
%{_mandir}/man1/pic2graph.*
%{_mandir}/man1/refer.*
%{_mandir}/man1/tfmtodit.*
# compatibility symlinks
%{_bindir}/grefer
%{_bindir}/glookbib
%{_bindir}/gindxbib
%{_mandir}/man1/grefer.*
%{_mandir}/man1/glookbib.*
%{_mandir}/man1/gindxbib.*
# groff processor documentation
%{_mandir}/man5/*
%ghost %{_mandir}/man7/roff.7*
%{_mandir}/man7/*
%{_infodir}/groff.info*

%files base
%{!?_licensedir:%global license %%doc}
%license COPYING FDL LICENSES
%doc BUG-REPORT MORE.STUFF NEWS PROBLEMS
# configuration
%dir %{_sysconfdir}/groff/
%config(noreplace) %{_sysconfdir}/groff/*
# data
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/%{version}/
%dir %{_datadir}/%{name}/%{version}/font/
%dir %{_datadir}/%{name}/%{version}/tmac/
%{_datadir}/%{name}/current
%{_datadir}/%{name}/%{version}/eign
%{_datadir}/%{name}/%{version}/font/devascii/
%{_datadir}/%{name}/%{version}/font/devlatin1/
%{_datadir}/%{name}/%{version}/font/devps/
%{_datadir}/%{name}/%{version}/font/devutf8/
%{_datadir}/%{name}/%{version}/font/devhtml/
%{_datadir}/%{name}/%{version}/tmac/an-ext.tmac
%{_datadir}/%{name}/%{version}/tmac/an.tmac
%{_datadir}/%{name}/%{version}/tmac/andoc.tmac
%{_datadir}/%{name}/%{version}/tmac/composite.tmac
%{_datadir}/%{name}/%{version}/tmac/cp1047.tmac
%{_datadir}/%{name}/%{version}/tmac/cs.tmac
%{_datadir}/%{name}/%{version}/tmac/de.tmac
%{_datadir}/%{name}/%{version}/tmac/den.tmac
%{_datadir}/%{name}/%{version}/tmac/en.tmac
%{_datadir}/%{name}/%{version}/tmac/devtag.tmac
%{_datadir}/%{name}/%{version}/tmac/doc-old.tmac
%{_datadir}/%{name}/%{version}/tmac/doc.tmac
%{_datadir}/%{name}/%{version}/tmac/eqnrc
%{_datadir}/%{name}/%{version}/tmac/europs.tmac
%{_datadir}/%{name}/%{version}/tmac/fallbacks.tmac
%{_datadir}/%{name}/%{version}/tmac/fr.tmac
%{_datadir}/%{name}/%{version}/tmac/html-end.tmac
%{_datadir}/%{name}/%{version}/tmac/html.tmac
%{_datadir}/%{name}/%{version}/tmac/hyphen.cs
%{_datadir}/%{name}/%{version}/tmac/hyphen.den
%{_datadir}/%{name}/%{version}/tmac/hyphen.det
%{_datadir}/%{name}/%{version}/tmac/hyphen.fr
%{_datadir}/%{name}/%{version}/tmac/hyphen.sv
%{_datadir}/%{name}/%{version}/tmac/hyphen.en
%{_datadir}/%{name}/%{version}/tmac/hyphen.it
%{_datadir}/%{name}/%{version}/tmac/hyphenex.cs
%{_datadir}/%{name}/%{version}/tmac/hyphenex.en
%{_datadir}/%{name}/%{version}/tmac/ja.tmac
%{_datadir}/%{name}/%{version}/tmac/ptx.tmac
%{_datadir}/%{name}/%{version}/tmac/it.tmac
%{_datadir}/%{name}/%{version}/tmac/rfc1345.tmac
%{_datadir}/%{name}/%{version}/tmac/sanitize.tmac
%{_datadir}/%{name}/%{version}/tmac/sboxes.tmac
%{_datadir}/%{name}/%{version}/tmac/latin1.tmac
%{_datadir}/%{name}/%{version}/tmac/latin2.tmac
%{_datadir}/%{name}/%{version}/tmac/latin5.tmac
%{_datadir}/%{name}/%{version}/tmac/latin9.tmac
%{_datadir}/%{name}/%{version}/tmac/man.tmac
%{_datadir}/%{name}/%{version}/tmac/mandoc.tmac
%{_datadir}/%{name}/%{version}/tmac/mdoc.tmac
%{_datadir}/%{name}/%{version}/tmac/mdoc/
%{_datadir}/%{name}/%{version}/tmac/papersize.tmac
%{_datadir}/%{name}/%{version}/tmac/pdfpic.tmac
%{_datadir}/%{name}/%{version}/tmac/pic.tmac
%{_datadir}/%{name}/%{version}/tmac/ps.tmac
%{_datadir}/%{name}/%{version}/tmac/psatk.tmac
%{_datadir}/%{name}/%{version}/tmac/psold.tmac
%{_datadir}/%{name}/%{version}/tmac/pspic.tmac
%{_datadir}/%{name}/%{version}/tmac/sv.tmac
%{_datadir}/%{name}/%{version}/tmac/trans.tmac
%{_datadir}/%{name}/%{version}/tmac/troffrc
%{_datadir}/%{name}/%{version}/tmac/troffrc-end
%{_datadir}/%{name}/%{version}/tmac/tty-char.tmac
%{_datadir}/%{name}/%{version}/tmac/tty.tmac
%{_datadir}/%{name}/%{version}/tmac/www.tmac
# programs
%{_bindir}/eqn
%{_bindir}/groff
%{_bindir}/grops
%{_bindir}/grotty
%{_bindir}/neqn
%{_bindir}/nroff
%{_bindir}/pic
%{_bindir}/post-grohtml
%{_bindir}/pre-grohtml
%{_bindir}/preconv
%ghost %{_bindir}/soelim
%{_bindir}/soelim.%{name}
%{_bindir}/tbl
%{_bindir}/troff
%{_mandir}/man1/eqn.*
%{_mandir}/man1/groff.*
%{_mandir}/man1/grops.*
%{_mandir}/man1/grotty.*
%{_mandir}/man1/neqn.*
%{_mandir}/man1/nroff.*
%{_mandir}/man1/pic.*
%{_mandir}/man1/preconv.*
%ghost %{_mandir}/man1/soelim.1*
%{_mandir}/man1/soelim.%{name}.*
%{_mandir}/man1/tbl.*
%{_mandir}/man1/troff.*
# compatibility symlinks
%{_bindir}/gnroff
%{_bindir}/gtroff
%{_bindir}/gtbl
%{_bindir}/gpic
%{_bindir}/geqn
%{_bindir}/gneqn
%{_bindir}/gsoelim
%{_bindir}/zsoelim
%{_mandir}/man1/gnroff.*
%{_mandir}/man1/gtroff.*
%{_mandir}/man1/gtbl.*
%{_mandir}/man1/gpic.*
%{_mandir}/man1/geqn.*
%{_mandir}/man1/gneqn.*
%{_mandir}/man1/gsoelim.*
%{_mandir}/man1/zsoelim.*

%files perl
# data
%{_datadir}/%{name}/%{version}/font/devpdf/
%{_datadir}/%{name}/%{version}/tmac/pdf.tmac
# programs
%{_bindir}/afmtodit
%{_bindir}/chem
%{_bindir}/gperl
%{_bindir}/gpinyin
%{_bindir}/glilypond
%{_bindir}/grog
%{_bindir}/gropdf
%{_bindir}/mmroff
%{_bindir}/pdfmom
%{_mandir}/man1/afmtodit.*
%{_mandir}/man1/chem.*
%{_mandir}/man1/gperl.*
%{_mandir}/man1/gpinyin.*
%{_mandir}/man1/glilypond.*
%{_mandir}/man1/grog.*
%{_mandir}/man1/gropdf.*
%{_mandir}/man1/mmroff.*
%{_mandir}/man1/pdfmom.*

%if %{with_x}
%files x11
# data
%{_datadir}/%{name}/%{version}/font/devX*/
%{_datadir}/%{name}/%{version}/tmac/X.tmac
%{_datadir}/%{name}/%{version}/tmac/Xps.tmac
%{_datadir}/X11/app-defaults/GXditview
%{_datadir}/X11/app-defaults/GXditview-color
%{_datadir}/%{name}/%{version}/font/FontMap-X11
# programs
%{_bindir}/gxditview
%{_bindir}/xtotroff
%{_mandir}/man1/gxditview.*
%{_mandir}/man1/xtotroff.*
%endif

%files doc
%doc %{_pkgdocdir}/*.me
%doc %{_pkgdocdir}/*.ps
%doc %{_pkgdocdir}/*.ms
%doc %{_pkgdocdir}/groff*
%doc %{_pkgdocdir}/me-revisions
%doc %{_pkgdocdir}/automake.pdf
%doc %{_pkgdocdir}/examples/
%doc %{_pkgdocdir}/html/
%doc %{_pkgdocdir}/pdf/

%changelog
* Wed Sep 24 2025 Lukas Javorsky <ljavorsk@redhat.com> - 1.23.0-11
- Revert the `psutils` removal

* Tue Sep 02 2025 Lukas Javorsky <ljavorsk@redhat.com> - 1.23.0-10
- Remove psutils from BuildRequires as it's not needed

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.23.0-4
- Fix alternatives usage

* Thu Nov 02 2023 Lukas Javorsky <ljavorsk@redhat.com> - 1.23.0-3
- Revert upstream change of mapping special characters for UTF-8 devices
- Resolves: BZ#2224123

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Lukas Javorsky <ljavorsk@redhat.com> - 1.23.0-1
- Rebase to version 1.23.0
- Several files were removed from groff package
- Several files were added to groff package

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 17 2021 Nikola Forró <nforro@redhat.com> - 1.22.4-7
- Make psutils a weak dependency

* Mon Feb 22 2021 Nikola Forró <nforro@redhat.com> - 1.22.4-6
- Add psutils as a runtime dependency (needed for groff -Thtml)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 03 2020 Nikola Forró <nforro@redhat.com> - 1.22.4-4
- Move pdfpic.tmac to groff-base
  resolves: #1888370

* Fri Oct 02 2020 Nikola Forró <nforro@redhat.com> - 1.22.4-3
- Use make macros

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 05 2020 Nikola Forró <nforro@redhat.com> - 1.22.4-1
- Update to version 1.22.4
  resolves: #1808072

* Sun Mar 01 2020 Nikola Forró <nforro@redhat.com> - 1.22.3-24
- Fix %pre scriptlets

* Fri Feb 28 2020 Nikola Forró <nforro@redhat.com> - 1.22.3-23
- Fix upgrades from non-alternativized versions

* Wed Feb 26 2020 Nikola Forró <nforro@redhat.com> - 1.22.3-22
- Use alternatives for soelim and roff.7

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Nikola Forró <nforro@redhat.com> - 1.22.3-18
- Add missing "bundled(gnulib)" provides

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Nikola Forró <nforro@redhat.com> - 1.22.3-16
- Remove install-info from scriptlets

* Tue Feb 27 2018 Nikola Forró <nforro@redhat.com> - 1.22.3-15
- Add unowned directories to groff-base and groff-perl
  resolves: #1548688

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 1.22.3-14
- Add missing gcc and gcc-c++ build dependencies

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 21 2017 Nikola Forró <nforro@redhat.com> - 1.22.3-12
- Move grog/subs.pl to groff-perl subpackage where it belongs
  resolves: #1515167

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Nikola Forró <nforro@redhat.com> - 1.22.3-8
- Make groff-base depend on /usr/bin/sed rather than /bin/sed

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.22.3-5
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.22.3-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Nov 14 2014 Colin Walters <walters@redhat.com> - 1.22.3-3
- Move more binaries which depend on perl to the -perl subpackage (bug #1165356)

* Wed Nov 12 2014 Petr Pisar <ppisar@redhat.com> - 1.22.3-2
- Do not require private Perl modules (bug #1163011)

* Tue Nov 04 2014 jchaloup <jchaloup@redhat.com> - 1.22.3-1
- Update to 1.22.3
  resolves: #1160256

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 1.22.2-10
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct  1 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-8
- resolves: #993806
  removed versioned docdir from .spec file

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.22.2-7
- Perl 5.18 rebuild

* Tue Jul 23 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-6
- don't use /usr/bin/env in shebang

* Mon Jul 22 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-5
- removed BSD and MIT license files - the text is already included
  in the upstream tarball

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.22.2-4
- Perl 5.18 rebuild

* Tue Jul  9 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-3
- added BSD and MIT license files

* Mon Mar 11 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-2
- resolves: #915682
  moved html device to the groff-base subpackage

* Tue Feb 12 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-1
- resolves: #909154
  updated to 1.22.2
- cleaned .spec file

* Tue Jan 01 2013 Jan Vcelak <jvcelak@redhat.com> 1.22.1-1
- new upstream release (#890973)
  + various fixes in manual pages
  + various fixes and improvements in macros
  + new gropdf driver for generating PDF files
- fix: backslash-period escape does not work (#682857)
- fix: groff ftbfs - patch does not apply (#885225)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Jan Vcelak <jvcelak@redhat.com> 1.21-9
- older security fixes (#709415, #720060):
  + CVE-2009-5044: insecure temporary file handling in pdfroff
  + CVE-2009-5080: improper handling of failed attempts to create temporary directories in eqn2graph/pic2graph/grap2graph
  + CVE-2009-5081: roff2.pl and groffer.pl use easy-to-guess temporary file names

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-7
- update: move local configuration from /usr/share/groff/site-* to /etc/groff/*
  (change the paths in the app instead of symlinking to avoid RPM issues)
- fix groff package: add install-info to %%post and %%preun

* Tue Oct 11 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-6
- fix build warnings: File listed twice

* Tue Sep 20 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-5
- fix #739318: fix upgrade from previous versions (workaround for RPM bug)

* Fri Sep 16 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-4
- new subpackage: groff-base (minimal for manual page rendering)
- move shared data used by gxditview to groff-x11 subpackage
- move groff reference manual to groff-doc subpackage
- make groff-doc an architecture independent package
- move local configuration from /usr/share/groff/site-* to /etc/groff/*

* Fri Jun 17 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-3
- fix #678572: groffer libdir is incorrect
- fix #709474: unowned groff doc dir
- fix #712904: Japanese bold/underline text not displayed correctly (Daiki Ueno <dueno@redhat.com>)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-1
- package rebase to 1.21

* Fri Nov 26 2010 Jan Vcelak <jvcelak@redhat.com> 1.20.1-3
- experimental support of Japanese (charclass and wcwidth patches)
  thanks to Daiki Ueno (dueno@redhat.com)

* Fri Jul 30 2010 Jan Vcelak <jvcelak@redhat.com> 1.20.1-2
- Resolves: #477394 - Please convert to new font packaging guidelines

* Fri Mar 19 2010 Jan Vcelak <jvcelak@redhat.com> - 1.20.1-1
- Resolves: #530788

* Fri Mar 12 2010 Jan Vcelak <jvcelak@redhat.com> - 1.20.1-0
- Package rebase to upstream 1.20.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.1.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.1.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 19 2008 Robert Scheck <robert@fedoraproject.org> - 1.18.1.14-16
- Fixed wrong symlinking of man pages into %%{_bindir} after simplifying

* Mon Sep 29 2008 Stepan Kasal <skasal@redhat.com> - 1.18.1.14-15
- Replace groff-1.18-nohtml.patch by a code in spec file
- fix groff-1.18-gzip.patch to apply cleanly
- simplify the code for symlinking in %%install

* Wed Mar 26 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-14
- 175459 warning goes on stderr

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.18.1.4-13
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-12
- rewrite nroff for using -Tencoding with main support of utf8
- Resolves: rhbz#251064

* Thu Jan  3 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-11
- fix for gcc4.3.0

* Mon Oct  8 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-10
- path for groffer wasn't set correctly #89210

* Mon Sep 17 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-9
- fix license

* Tue Sep 11 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-8
- another change in spec for review

* Thu Aug 16 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-7
- rebuild
- another encoding are print correct with nroff
- Resolves: rhbz#251064

* Mon Jul  2 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-5
- Resolves: rhbz#245934

* Tue Feb 27 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-4
- merge review
- rhbz#225859 review

* Mon Jan 22 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-2
- changes in spec, remove patches groff-1.18.1.1-bigendian.patch, groff-xlibs.patch
 
* Mon Oct 23 2006 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-1
- new version from upstream - update groffer

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1.1-11.1
- rebuild

* Wed Apr 26 2006 Adam Jackson <ajackson@redhat.com> - 1.18.1.1-11
- Rebuild for updated imake build rules.

* Thu Feb 16 2006 Miroslav Lichvar <mlichvar@redhat.com> - 1.18.1.1-10
- use mktemp for temporary files in pic2graph and eqn2graph scripts

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1.1-9.2
- bump again for double-long bug on ppc(64)
- bump again for double-long bug on ppc(64)
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1.1-9.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Miroslav Lichvar <mlichvar@redhat.com> - 1.18.1.1-9
- remove gxditview from groff package (#179684)
- remove obsolete "--enable-japanese" configure option

* Thu Jan 12 2006 Miroslav Lichvar <mlichvar@redhat.com> - 1.18.1.1-8
- fix segfault in grotty on 64-bit big endian machines (#176904)
- fix assertion failure on abort message (#141912)
- attempt to fix a space problem with several european languages (#137728)

* Fri Jan 06 2006 Jindrich Novy <jnovy@redhat.com> - 1.18.1.1-7
- require X dependencies only for gxditview (#177118)
- work if bash's noclobber is on (#127492)

* Thu Jan 05 2006 Jindrich Novy <jnovy@redhat.com> - 1.18.1.1-6
- add BuildRequires imake and update dependencies for modular X
- spec cleanup
- fix compilation with gcc-4.1.0

* Wed Nov 24 2004 Miloslav Trmac <mitr@redhat.com> - 1.18.1.1-5
- Convert also mmroff.1 to UTF-8

* Sat Nov 20 2004 Miloslav Trmac <mitr@redhat.com> - 1.18.1.1-4
- Convert man pages to UTF-8

* Tue Oct 19 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1.1-3
- fixed groffer scripte security problem (#136314)

* Thu Sep 16 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1.1-2
- fixed DoCharacter calls in xditview (#110812)
- fixed fclose called once too often (#132690): thanks to Ulrich Drepper for
  the bug hunting

* Tue Jun 29 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1.1-1
- new version 1.18.1.1 (fixed groffer script)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-35
- fixed build prereq and requires

* Mon Mar  8 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-34
- new debian groff patch: groff_1.18.1-15.diff
- new fix for debian patch: groff-1.18.1-fix15.patch
- fixed width in devutf8 font M: groff-1.18.1-devutf8.patch
- removed iconv patch

* Mon Mar  1 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-33
- fixed nroff script: convert output to locale charmap

* Wed Feb 25 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-32
- fixed nroff script input (#116596)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 09 2004 Adrian Havill <havill@redhat.com>
- provide I18N version of nroff that accepts --legacy parameter
  (used by man-1.5m2-2)

* Thu Dec 18 2003 Thomas Woerner <twoerner@redhat.com>
- fixed missing BuildRequires (#110574)

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling this without XFree86

* Wed Aug  6 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-28.2
- new devutf8 font description
- use -Tutf8 for ru_*.UTF-8 in nroff.sh
- fixes #88618 (ru_RU man pages in cambridge are using UTF-8, now)

* Fri Jun 13 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-28
- rebuild (debian-9)

* Tue Jun 10 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-27
- going back to 1.18.1-4 from debian (the newer versions did not work properly)
- fixed nroff.sh for ru_RU.(!UTF-8)

* Mon May 19 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-26
- fix input and output handler for 1.18.1-9 to be compatible with 1.18.1-4

* Tue Apr 29 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.18.1-9 from debian

* Tue Apr 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.18.1-8 from debian: use latin1 instead of C locale

* Sun Mar 09 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to debian patch 1.18.1-7 located at
  ftp://ftp.debian.org/debian/pool/main/g/groff/

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 1.18.1-21
- groff-xlibs.patch to fix ppc64 builds

* Wed Feb 12 2003 Tim Waugh <twaugh@redhat.com> 1.18.1-20
- Make the iconv patch a little less broken (bug #84132).

* Tue Feb 11 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-19
- added new iconv patch

* Tue Feb 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- disable the iconv patch, this will go into a wrapper within the man rpm

* Mon Feb 10 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-17
- fixed source of gzipped files

* Mon Feb 10 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add Korean support from ynakai@redhat.com, #83933

* Sun Feb 09 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove automatic conversion for ru_* and cz_*
- add 8bit patch
- update to 1.18.1-4 debian patch
- disable Patch8: groff-1.18.1-multichar.patch for now
- add ugly patch within the iconv patch to partly fix display of russian
  man-pages with "-Tnippon"

* Thu Feb  6 2003 Tim Waugh <twaugh@redhat.com> 1.18.1-11
- Unbreak EUC-JP (bug #83608).

* Mon Feb  3 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-10
- fixed missing minus
- added iconv conversion script

* Fri Jan 31 2003 Tim Waugh <twaugh@redhat.com> 1.18.1-9
- Fix UTF-8.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- also add hyphen changes to man.local in addition to mdoc.local

* Tue Jan 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- really include mdoc.local changes from debian

* Sat Jan 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix #81401, maybe also #57410

* Fri Jan 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add more documentation #80729

* Wed Jan 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- hot fix for devascii8 breakage

* Sun Dec 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to debian patch 1.18.1-2 located at
  ftp://ftp.debian.org/debian/pool/main/g/groff/

* Mon Nov 18 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.18.1
- use newest debian patch on top of it

* Mon Nov 04 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add gzip decompression patch

* Sat Nov 02 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.18.1
- apply groff_1.18-7 from debian
- remove some not-packaged files
- rm old printfilters completely

* Fri Oct 04 2002 Elliot Lee <sopwith@redhat.com> 1.18-7
- Patch7 - move pfbtops to CCPROGDIRS (it needs to link to C++ stuff)

* Sat Aug 31 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch for #72924

* Mon Aug 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- remove README.A4  #65920

* Sun Aug 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- use info files as installed by groff package
- completely disable older printconf stuff

* Thu Aug  8 2002 Yukihiro Nakai <ynakai@redhat.com>
- link docj.tmac to doc.tmac #57560

* Thu Aug  1 2002 Harald Hoyer <harald@redhat.de>
- update to 1.18
- mmroff(7) is now mmroff(1)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com>
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 12 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- prereq install-info and add post/preun for info files

* Wed May 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add info files #64667

* Fri Feb 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild in new environment

* Sun Feb 17 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to newest debian patch 1.17.2-16
- patch4 is already included in that

* Thu Jan 31 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- disable printconf support, but do not yet delete it from the source rpm

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- check string input

* Sat Jan 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add URL tag

* Sat Jan 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to newest debian patch 1.17.2-13

* Thu Dec 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to newest debian patch 1.17.2-12

* Wed Aug 15 2001 Mike A. Harris <mharris@redhat.com> 1.17.2-3
- Added symlink from soelim to zsoelim, fixing bug (#51037)

* Tue Aug 14 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fixes security bug #50494

* Sun Aug 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.17.2
- strerror patch is not needed anymore
- apply newest debian patch

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64

* Tue Apr 03 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not change groff to use /etc/papersize. Deleted the changes
  in the debian patch.

* Fri Mar 30 2001 Trond Eivind GlomsrĹd <teg@redhat.com>
- Add hyphen.cs - file generated as described in Czech how-to, 6.7

* Wed Mar 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- updated to newest debian patch to get nippon/ascii8 support
  better working

* Fri Feb  9 2001 Crutcher Dunnavant <crutcher@redhat.com>
- switch to printconf filtration rules

* Tue Jan 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change app-defaults to /usr/X11R6/lib/X11/app-defaults/
  and do not mark it as config file

* Thu Dec 14 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese patch from RHL7J

* Fri Aug  4 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to bug-fix release 1.16.1

* Fri Jul 28 2000 Tim Waugh <twaugh@redhat.com>
- Install troff-to-ps.fpi in /usr/lib/rhs-printfilters (#13634).

* Wed Jul 19 2000 Jeff Johnson <jbj@redhat.com>
- rebuild with gcc-2.96-41.

* Mon Jul 17 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to fix miscompilation manifesting in alpha build of tcltk.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- move mmroff to -perl

* Wed Jun  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build
- FHS
- 1.16

* Sun May 14 2000 Jeff Johnson <jbj@redhat.com>
- install tmac.mse (FWIW tmac.se looks broken) to fix dangling symlink (#10757).
- add README.A4, how to set up for A4 paper (#8276).
- add other documents to package.

* Thu Mar  2 2000 Jeff Johnson <jbj@redhat.com>
- permit sourcing on regular files within cwd tree (unless -U specified).

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- fix incorrectly installed tmac.m file (#8362).

* Mon Feb  7 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- check if build system is sane again

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary
- man pages are compressed. This is ugly.

* Mon Jan 31 2000 Bill Nottingham <notting@redhat.com>
- put the binaries actually in the package *oops*

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- split perl components into separate subpackage

* Wed Dec 29 1999 Bill Nottingham <notting@redhat.com>
- update to 1.15

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)
* Tue Feb 16 1999 Cristian Gafton <gafton@redhat.com>
- glibc 2.1 patch for xditview (#992)

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- fix makefiles to work with bash2

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- use g++ for C++ code

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- manhattan and buildroot

* Mon Nov  3 1997 Michael Fulbright <msf@redhat.com>
- made xdefaults file a config file

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- split perl components into separate subpackage

* Tue Oct 21 1997 Michael Fulbright <msf@redhat.com>
- updated to 1.11a
- added safe troff-to-ps.fpi

* Tue Oct 14 1997 Michael Fulbright <msf@redhat.com>
- removed troff-to-ps.fpi for security reasons.

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

