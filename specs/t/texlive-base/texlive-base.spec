# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global shortname texlive
%global source_date 20260301
%global tl_version %{sub %{source_date} 1 4}
# %%global source_svn svn66984
%global source_name texlive-%%{source_date}-source
# %%global source_name texlive-source-build-%{source_svn}
%{!?_texdir: %global _texdir %{_datadir}/%{shortname}}
%{!?_texmf_var: %global _texmf_var %{_var}/lib/texmf}

%global etc_fmtutil_cnf %{_sysconfdir}/texlive/web2c/fmtutil.cnf
%global usr_fmtutil_cnf %{_texmf_main}/web2c/fmtutil.cnf
%global fmtutil_cnf_d %{_texdir}/fmtutil.cnf.d

# don't export private perl modules
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((LatexIndent.*|PDF::Reuse.*|Pedigree.*|TeXLive.*|Tk::path_tre)\\)

# We do not want exec perms changing.
%global __brp_mangle_shebangs_exclude ^$

# We have a circular dep on latex due to xindy
%bcond_with bootstrap

# Upstream no longer supports poppler. We've been hacking it in, but... maybe we should stop?
%bcond_with poppler

# Automatically generate tex(filename.ext) Provides.
%define _local_file_attrs texlive
%define __texlive_path          ^%{_texdir}/texmf-dist/.*\\.(4ht|afm|bbx|bg2|bst|bug|cbx|cfg|clo|cls|csv|cnf|dat|dbx|def|enc|eps|fd|icc|ini|lbx|ldf|lua|map|mf|mp|otf|pfa|pfb|pro|sty|tex|tfm|ttf|vf)$
%define __texlive_exclude_path  ^%{_texdir}/texmf-dist/doc/
%define __texlive_provides()    tex(%{basename:%{1}}) = %{epoch}:%{source_date}-%{release}

Name: %{shortname}-base
Version: %{source_date}
Release: 111%{?dist}
Epoch: 12
Summary: TeX formatting system
# The only files in the base package are directories, cache, and license texts
# So we'll just list the license texts. This is also a bit of a lie, since most of these license texts do not apply to themselves.
License: Apache-2.0 AND Artistic-2.0 AND BSD-3-Clause AND GFDL-1.1-or-later AND GPL-1.0-or-later AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-only AND GPL-3.0-or-later AND Knuth-CTAN AND LGPL-2.1-or-later AND LGPL-3.0-or-later AND LPPL-1.3a AND LPPL-1.3c AND MIT AND OFL-1.1 AND LicenseRef-Fedora-Public-Domain
URL: http://tug.org/texlive/
Source0: https://ctan.math.illinois.edu/systems/texlive/Source/%{source_name}.tar.xz
Source1: macros.texlive
Source2: http://tug.ctan.org/systems/texlive/tlnet/tlpkg/texlive.tlpdb
Source3: texlive-licenses.tar.xz
Source4: generate-fmtutilcnf
# These noarch components are packed wrong upstream (do not unpack into texmf-dist)
Source5: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cslatex.tar.xz
Source6: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cyrillic.tar.xz
Source7: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cyrillic.doc.tar.xz
Source8: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/glyphlist.tar.xz
Source9: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex.tar.xz
Source10: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex.doc.tar.xz
Source11: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lyluatex.tar.xz
Source12: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lyluatex.doc.tar.xz
Source13: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/oberdiek.tar.xz
Source14: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/oberdiek.doc.tar.xz
Source15: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlive-en.doc.tar.xz

# These are the noarch components for the built binaries.
Source16: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/a2ping.doc.tar.xz
Source17: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/a2ping.tar.xz
Source18: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/accfonts.doc.tar.xz
Source19: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/accfonts.tar.xz
Source20: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/adhocfilelist.doc.tar.xz
Source21: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/adhocfilelist.tar.xz
Source22: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/afm2pl.tar.xz
Source23: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/aleph.doc.tar.xz
Source24: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/aleph.tar.xz
Source25: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/amstex.doc.tar.xz
Source26: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/amstex.tar.xz
Source27: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/arara.doc.tar.xz
Source28: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/arara.tar.xz
Source29: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/attachfile2.doc.tar.xz
Source30: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/attachfile2.tar.xz
Source31: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/authorindex.doc.tar.xz
Source32: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/authorindex.tar.xz
Source33: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/autosp.doc.tar.xz
Source34: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/axodraw2.doc.tar.xz
Source35: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/axodraw2.tar.xz
Source36: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bib2gls.doc.tar.xz
Source37: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bib2gls.tar.xz
Source38: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibexport.doc.tar.xz
Source39: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibexport.tar.xz
Source40: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibtex8.doc.tar.xz
Source41: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibtex8.tar.xz
Source42: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibtex.doc.tar.xz
Source43: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibtex.tar.xz
Source44: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibtexu.doc.tar.xz
Source45: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bundledoc.doc.tar.xz
Source46: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bundledoc.tar.xz
Source47: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cachepic.doc.tar.xz
Source48: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cachepic.tar.xz
Source49: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/checkcites.doc.tar.xz
Source50: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/checkcites.tar.xz
Source51: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/checklistings.doc.tar.xz
Source52: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/checklistings.tar.xz
Source53: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/chklref.doc.tar.xz
Source54: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/chklref.tar.xz
Source55: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/chktex.doc.tar.xz
Source56: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/chktex.tar.xz
Source57: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cjk-gs-integrate.doc.tar.xz
Source58: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cjk-gs-integrate.tar.xz
Source59: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cjkutils.tar.xz
Source60: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/clojure-pamphlet.doc.tar.xz
Source61: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/clojure-pamphlet.tar.xz
Source62: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cluttex.doc.tar.xz
Source63: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cluttex.tar.xz
Source64: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/context.doc.tar.xz
Source65: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/context.tar.xz
Source66: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/convbkmk.doc.tar.xz
Source67: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/convbkmk.tar.xz
Source68: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/crossrefware.doc.tar.xz
Source69: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/crossrefware.tar.xz
Source70: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/csplain.tar.xz
Source71: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ctanbib.doc.tar.xz
Source72: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ctanbib.tar.xz
Source73: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ctanify.doc.tar.xz
Source74: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ctanify.tar.xz
Source75: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ctan-o-mat.doc.tar.xz
Source76: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ctan-o-mat.tar.xz
Source77: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ctanupload.doc.tar.xz
Source78: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ctanupload.tar.xz
Source79: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ctie.doc.tar.xz
Source80: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cweb.doc.tar.xz
Source81: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cweb.tar.xz
Source82: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cyrillic-bin.doc.tar.xz
Source83: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/cyrillic-bin.tar.xz
Source84: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/de-macro.doc.tar.xz
Source85: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/de-macro.tar.xz
Source86: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/detex.doc.tar.xz
Source87: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/detex.tar.xz
Source88: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/diadia.doc.tar.xz
Source89: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/diadia.tar.xz
Source90: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dosepsbin.doc.tar.xz
Source91: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dosepsbin.tar.xz
Source92: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dtl.doc.tar.xz
Source93: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dtl.tar.xz
Source94: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dtxgen.doc.tar.xz
Source95: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dtxgen.tar.xz
Source96: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvi2tty.doc.tar.xz
Source97: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvi2tty.tar.xz
Source98: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dviasm.doc.tar.xz
Source99: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dviasm.tar.xz
Source100: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvicopy.doc.tar.xz
Source101: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvicopy.tar.xz
Source102: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvidvi.doc.tar.xz
Source103: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvidvi.tar.xz
Source104: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dviinfox.doc.tar.xz
Source105: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dviinfox.tar.xz
Source106: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dviljk.doc.tar.xz
Source107: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dviljk.tar.xz
Source108: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dviout-util.doc.tar.xz
Source109: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvipdfmx.doc.tar.xz
Source110: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvipdfmx.tar.xz
Source111: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvipng.doc.tar.xz
Source112: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvipng.tar.xz
Source113: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvipos.doc.tar.xz
Source114: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvipos.tar.xz
Source115: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvips.doc.tar.xz
Source116: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvips.tar.xz
Source117: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvisvgm.doc.tar.xz
Source118: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/dvisvgm.tar.xz
Source119: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ebong.doc.tar.xz
Source120: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ebong.tar.xz
Source121: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/eplain.doc.tar.xz
Source122: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/eplain.tar.xz
Source123: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/epspdf.doc.tar.xz
Source124: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/epspdf.tar.xz
Source125: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/epstopdf.doc.tar.xz
Source126: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/epstopdf.tar.xz
Source127: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/exceltex.doc.tar.xz
Source128: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/exceltex.tar.xz
Source129: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/fig4latex.doc.tar.xz
Source130: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/fig4latex.tar.xz
Source131: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/findhyph.doc.tar.xz
Source132: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/findhyph.tar.xz
Source133: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/fontinst.doc.tar.xz
Source134: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/fontinst.tar.xz
Source135: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/fontools.doc.tar.xz
Source136: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/fontools.tar.xz
Source137: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/fontware.doc.tar.xz
Source138: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/fragmaster.doc.tar.xz
Source139: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/fragmaster.tar.xz
Source140: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/getmap.doc.tar.xz
Source141: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/getmap.tar.xz
Source142: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/glossaries.doc.tar.xz
Source143: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/glossaries.tar.xz
Source144: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/gregoriotex.doc.tar.xz
Source145: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/gregoriotex.tar.xz
Source146: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/gsftopk.doc.tar.xz
Source147: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/gsftopk.tar.xz
Source148: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/installfont.doc.tar.xz
Source149: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/installfont.tar.xz
Source150: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/jadetex.doc.tar.xz
Source151: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/jadetex.tar.xz
Source152: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/jfmutil.doc.tar.xz
Source153: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/jfmutil.tar.xz
Source154: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ketcindy.doc.tar.xz
Source155: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ketcindy.tar.xz
Source156: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/kotex-utils.doc.tar.xz
Source157: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/kotex-utils.tar.xz
Source158: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/kpathsea.doc.tar.xz
Source159: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/kpathsea.tar.xz
Source160: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/l3build.tar.xz
Source161: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/l3build.doc.tar.xz
Source162: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lacheck.doc.tar.xz
Source163: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex2man.doc.tar.xz
Source164: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex2man.tar.xz
Source165: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex2nemeth.doc.tar.xz
Source166: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex2nemeth.tar.xz
Source167: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latexdiff.doc.tar.xz
Source168: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latexdiff.tar.xz
Source169: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latexfileversion.doc.tar.xz
Source170: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latexfileversion.tar.xz
Source171: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex-git-log.doc.tar.xz
Source172: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex-git-log.tar.xz
Source173: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latexindent.doc.tar.xz
Source174: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latexindent.tar.xz
Source175: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latexpand.doc.tar.xz
Source176: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latexpand.tar.xz
Source177: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex-papersize.doc.tar.xz
Source178: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/latex-papersize.tar.xz
Source179: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lcdftypetools.doc.tar.xz
Source180: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lilyglyphs.doc.tar.xz
Source181: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lilyglyphs.tar.xz
Source182: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/listbib.doc.tar.xz
Source183: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/listbib.tar.xz
Source184: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/listings-ext.doc.tar.xz
Source185: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/listings-ext.tar.xz
Source186: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lollipop.doc.tar.xz
Source187: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lollipop.tar.xz
Source188: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ltxfileinfo.doc.tar.xz
Source189: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ltxfileinfo.tar.xz
Source190: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ltximg.doc.tar.xz
Source191: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ltximg.tar.xz
Source192: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/luaotfload.doc.tar.xz
Source193: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/luaotfload.tar.xz
Source194: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/luahbtex.doc.tar.xz
Source195: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/luahbtex.tar.xz
Source196: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/luatex.doc.tar.xz
Source197: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/luatex.tar.xz
Source198: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lwarp.doc.tar.xz
Source199: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/lwarp.tar.xz
Source200: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/make4ht.doc.tar.xz
Source201: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/make4ht.tar.xz
Source202: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/makedtx.doc.tar.xz
Source203: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/makedtx.tar.xz
Source204: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/makeindex.doc.tar.xz
Source205: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/makeindex.tar.xz
Source206: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/match_parens.doc.tar.xz
Source207: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/match_parens.tar.xz
Source208: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mathspic.doc.tar.xz
Source209: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mathspic.tar.xz
Source210: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/metafont.doc.tar.xz
Source211: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/metafont.tar.xz
Source212: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/metapost.doc.tar.xz
Source213: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/metapost.tar.xz
Source214: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mex.doc.tar.xz
Source215: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mex.tar.xz
Source216: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mf2pt1.doc.tar.xz
Source217: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mf2pt1.tar.xz
Source218: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mflua.tar.xz
Source219: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mfware.doc.tar.xz
Source220: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mfware.tar.xz
Source221: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mkgrkindex.doc.tar.xz
Source222: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mkgrkindex.tar.xz
Source223: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mkjobtexmf.doc.tar.xz
Source224: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mkjobtexmf.tar.xz
Source225: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mkpic.doc.tar.xz
Source226: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mkpic.tar.xz
Source227: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mltex.doc.tar.xz
Source228: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mltex.tar.xz
Source229: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mptopdf.doc.tar.xz
Source230: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/mptopdf.tar.xz
Source231: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/m-tx.doc.tar.xz
Source232: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/m-tx.tar.xz
Source233: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/multibibliography.doc.tar.xz
Source234: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/multibibliography.tar.xz
Source235: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/musixtex.doc.tar.xz
Source236: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/musixtex.tar.xz
Source237: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/musixtnt.doc.tar.xz
Source238: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/musixtnt.tar.xz
Source239: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/omegaware.doc.tar.xz
Source240: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/patgen.doc.tar.xz
Source241: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/patgen.tar.xz
Source242: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pax.doc.tar.xz
Source243: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pax.tar.xz
Source244: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdfbook2.doc.tar.xz
Source245: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdfbook2.tar.xz
Source246: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdfcrop.doc.tar.xz
Source247: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdfcrop.tar.xz
Source248: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdfjam.doc.tar.xz
Source249: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdfjam.tar.xz
Source250: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdflatexpicscale.doc.tar.xz
Source251: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdflatexpicscale.tar.xz
Source252: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdftex.doc.tar.xz
Source253: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdftex.tar.xz
Source254: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdftex-quiet.doc.tar.xz
Source255: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdftex-quiet.tar.xz
Source256: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdfxup.doc.tar.xz
Source257: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdfxup.tar.xz
Source258: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pedigree-perl.doc.tar.xz
Source259: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pedigree-perl.tar.xz
Source260: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/perltex.doc.tar.xz
Source261: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/perltex.tar.xz
Source262: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/petri-nets.doc.tar.xz
Source263: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/petri-nets.tar.xz
Source264: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pfarrei.doc.tar.xz
Source265: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pfarrei.tar.xz
Source266: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pkfix.doc.tar.xz
Source267: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pkfix-helper.doc.tar.xz
Source268: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pkfix-helper.tar.xz
Source269: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pkfix.tar.xz
Source270: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pmxchords.doc.tar.xz
Source271: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pmxchords.tar.xz
Source272: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pmx.doc.tar.xz
Source273: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pmx.tar.xz
Source274: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ps2eps.doc.tar.xz
Source275: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ps2eps.tar.xz
Source276: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ps2pk.doc.tar.xz
Source277: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ps2pk.tar.xz
Source278: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pst2pdf.doc.tar.xz
Source279: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pst2pdf.tar.xz
Source280: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pst-pdf.doc.tar.xz
Source281: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pst-pdf.tar.xz
Source282: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/psutils.doc.tar.xz
Source283: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/psutils.tar.xz
Source284: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ptex2pdf.doc.tar.xz
Source285: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ptex2pdf.tar.xz
Source286: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ptex.doc.tar.xz
Source287: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ptex-fontmaps.doc.tar.xz
Source288: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ptex-fontmaps.tar.xz
Source289: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ptex.tar.xz
Source290: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/purifyeps.doc.tar.xz
Source291: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/purifyeps.tar.xz
Source292: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pygmentex.doc.tar.xz
Source293: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pygmentex.tar.xz
Source294: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pythontex.doc.tar.xz
Source295: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pythontex.tar.xz
Source296: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/rubik.doc.tar.xz
Source297: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/rubik.tar.xz
Source298: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/seetexk.doc.tar.xz
Source299: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/seetexk.tar.xz
Source300: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/splitindex.doc.tar.xz
Source301: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/splitindex.tar.xz
Source302: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/srcredact.doc.tar.xz
Source303: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/srcredact.tar.xz
Source304: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/sty2dtx.doc.tar.xz
Source305: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/sty2dtx.tar.xz
Source306: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/svn-multi.doc.tar.xz
Source307: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/svn-multi.tar.xz
Source308: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/synctex.doc.tar.xz
Source309: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/synctex.tar.xz
Source310: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tex4ebook.doc.tar.xz
Source311: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tex4ebook.tar.xz
Source312: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tex4ht.doc.tar.xz
Source313: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tex4ht.tar.xz
Source314: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texcount.doc.tar.xz
Source315: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texcount.tar.xz
Source316: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdef.doc.tar.xz
Source317: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdef.tar.xz
Source318: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdiff.doc.tar.xz
Source319: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdiff.tar.xz
Source320: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdirflatten.doc.tar.xz
Source321: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdirflatten.tar.xz
Source322: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdoc.doc.tar.xz
Source323: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tex.doc.tar.xz
Source324: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdoc.tar.xz
Source325: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdoctk.tar.xz
Source326: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texdoctk.doc.tar.xz
Source327: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texfot.doc.tar.xz
Source328: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texfot.tar.xz
Source329: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlive.infra.doc.tar.xz
Source330: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlive.infra.tar.xz
Source331: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texliveonfly.doc.tar.xz
Source332: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texliveonfly.tar.xz
Source333: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlive-scripts.doc.tar.xz
Source334: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlive-scripts.tar.xz
Source335: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlive-scripts-extra.doc.tar.xz
Source336: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlive-scripts-extra.tar.xz
Source337: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texloganalyser.doc.tar.xz
Source338: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texloganalyser.tar.xz
Source339: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texosquery.doc.tar.xz
Source340: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texosquery.tar.xz
Source341: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texplate.doc.tar.xz
Source342: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texplate.tar.xz
Source343: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texsis.doc.tar.xz
Source344: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texsis.tar.xz
Source345: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tex.tar.xz
Source346: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texware.doc.tar.xz
Source347: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texware.tar.xz
Source348: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/thumbpdf.doc.tar.xz
Source349: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/thumbpdf.tar.xz
Source350: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tie.doc.tar.xz
Source351: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tie.tar.xz
Source352: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tpic2pdftex.doc.tar.xz
Source353: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tpic2pdftex.tar.xz
Source354: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ttfutils.doc.tar.xz
Source355: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ttfutils.tar.xz
Source356: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/typeoutfileinfo.doc.tar.xz
Source357: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/typeoutfileinfo.tar.xz
Source358: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ulqda.doc.tar.xz
Source359: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ulqda.tar.xz
Source360: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/uplatex.doc.tar.xz
Source361: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/uptex.doc.tar.xz
Source362: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/urlbst.doc.tar.xz
Source363: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/urlbst.tar.xz
Source364: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/velthuis.doc.tar.xz
Source365: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/velthuis.tar.xz
Source366: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/vlna.doc.tar.xz
Source367: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/vpe.doc.tar.xz
Source368: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/vpe.tar.xz
Source369: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/web.doc.tar.xz
Source370: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/web.tar.xz
Source371: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/webquiz.doc.tar.xz
Source372: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/webquiz.tar.xz
Source373: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/wordcount.doc.tar.xz
Source374: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/wordcount.tar.xz
Source375: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xdvi.doc.tar.xz
Source376: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xdvi.tar.xz
Source377: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xetex.doc.tar.xz
Source378: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xetex.tar.xz
Source379: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xindex.doc.tar.xz
Source380: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xindex.tar.xz
Source381: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xindy.doc.tar.xz
Source382: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xindy.tar.xz
Source383: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xmltex.doc.tar.xz
Source384: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xmltex.tar.xz
Source385: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xpdfopen.doc.tar.xz
Source386: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/yplan.doc.tar.xz
Source387: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/yplan.tar.xz
Source388: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/optex.tar.xz
Source389: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/optex.doc.tar.xz
# 2021
Source390: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/albatross.tar.xz
Source391: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/albatross.doc.tar.xz
Source392: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/git-latexdiff.tar.xz
Source393: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/git-latexdiff.doc.tar.xz
Source394: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/hyperxmp.tar.xz
Source395: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/hyperxmp.doc.tar.xz
Source396: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/light-latex-make.tar.xz
Source397: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/light-latex-make.doc.tar.xz
Source398: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/spix.tar.xz
Source399: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/spix.doc.tar.xz
Source400: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tikztosvg.tar.xz
Source401: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tikztosvg.doc.tar.xz
Source402: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xml2pmx.tar.xz
Source403: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xml2pmx.doc.tar.xz
Source404: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/luajittex.doc.tar.xz
Source405: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdftosrc.doc.tar.xz
# 2022
Source406: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/citation-style-language.tar.xz
Source407: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/citation-style-language.doc.tar.xz
Source408: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/hitex.tar.xz
Source409: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/hitex.doc.tar.xz
Source410: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/luafindfont.doc.tar.xz
Source411: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/optexcount.tar.xz
Source412: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/optexcount.doc.tar.xz
Source413: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlogfilter.doc.tar.xz
Source414: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlogsieve.doc.tar.xz
Source415: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texlogsieve.tar.xz
# 2023
Source416: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/digestif.tar.xz
Source417: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/digestif.doc.tar.xz
Source418: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibcop.tar.xz
Source419: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibcop.doc.tar.xz
Source420: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pagelayout.tar.xz
Source421: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pagelayout.doc.tar.xz
Source422: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texaccents.tar.xz
Source423: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texaccents.doc.tar.xz
Source424: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/upmendex.doc.tar.xz
Source425: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texaccents.source.tar.xz
# 2025
Source426: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/aomart.tar.xz
Source427: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/aomart.doc.tar.xz
# We don't unpack this because we have the perl files from separate packaging
# SourceNNN: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibtexperllibs.tar.xz
Source428: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bibtexperllibs.doc.tar.xz
Source429: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bookshelf.tar.xz
Source430: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/bookshelf.doc.tar.xz
Source431: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/context-legacy.tar.xz
Source432: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/context-legacy.doc.tar.xz
Source433: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/easydtx.tar.xz
Source434: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/easydtx.doc.tar.xz
Source435: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/eolang.tar.xz
Source436: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/eolang.doc.tar.xz
Source437: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/expltools.tar.xz
Source438: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/expltools.doc.tar.xz
Source439: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/extractbb.tar.xz
Source440: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/extractbb.doc.tar.xz
Source441: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/l3sys-query.tar.xz
Source442: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/l3sys-query.doc.tar.xz
Source443: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/markdown.tar.xz
Source444: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/markdown.doc.tar.xz
Source445: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/memoize.tar.xz
Source446: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/memoize.doc.tar.xz
Source447: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/minted.tar.xz
Source448: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/minted.doc.tar.xz
Source449: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ppmcheckpdf.tar.xz
Source450: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/ppmcheckpdf.doc.tar.xz
Source451: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/runtexshebang.tar.xz
Source452: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/runtexshebang.doc.tar.xz
Source453: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/sqltex.tar.xz
Source454: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/sqltex.doc.tar.xz
Source455: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texblend.tar.xz
Source456: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texblend.doc.tar.xz
Source457: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texfindpkg.tar.xz
Source458: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/texfindpkg.doc.tar.xz
Source459: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/typog.tar.xz
Source460: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/typog.doc.tar.xz
# 2026
# runtexfile and show-pdf-tags came from collection-binextra
Source461: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/runtexfile.tar.xz
Source462: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/runtexfile.doc.tar.xz
Source463: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/show-pdf-tags.tar.xz
Source464: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/show-pdf-tags.doc.tar.xz
Source465: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xdvipsk.tar.xz
Source466: https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/xdvipsk.doc.tar.xz


Patch1: tl-kpfix.patch
Patch2: tl-format.patch
Patch5: texlive-2016-kpathsea-texlive-path.patch
# fixes from arch and upstream texlive
Patch7: texlive-20210325-new-poppler.patch
# fix texmf.cnf so that it finds texinfo bits in Fedora
Patch8: texlive-base-20260301-texinfo-path-fix.patch
# fix annocheck issue detected by rpmdiff
Patch17: texlive-20180414-annocheck.patch
Patch18: texlive-20210325-poppler-0.73.patch
# Since we need to include tlmgr.pl for texconfig
# lets try to keep people from shooting themselves with it
Patch21: texlive-20190410-tlmgr-ignore-warning.patch
Patch23: texlive-20210325-poppler-0.84.patch
# Fixes for poppler 0.90 (f33+)
Patch29: texlive-20200327-poppler-0.90.patch
# Fix pdflatex run out of memory
Patch30: texlive-base-20220321-out-of-memory.patch
# Fix configure to properly detect poppler
Patch31: texlive-base-20210325-configure-poppler-xpdf-fix.patch

# Poppler 22
Patch34: texlive-base-20210325-poppler-22.01.0.patch
# Fix crash in handling Group
Patch35: texlive-base-20210325-pdftoepdf-fix-crash.patch
# Poppler 22.08.0
Patch36: texlive-base-20220321-poppler-22.08.0.patch

# libpaper v2 changes
# 1. one psutils test needs adjustment, see https://github.com/rrthomas/libpaper/issues/23
Patch37: texlive-base-libpaperv2.patch

# Fix issue where off_t could be set incorrectly on i686 due to order of header load
Patch44: texlive-base-20220321-pdf-header-order-fix.patch

# Fix texmfcnf.lua for Fedora layout (thanks to Preining Norbert)
Patch45: texlive-2026-fedora-texmfcnf.lua.patch

# Fix interpreter on perl scripts (thanks again to Debian)
Patch46: texlive-base-20230311-fix-scripts.patch

# fix FTBFS with gcc-16
Patch51: texlive-base-ftbfs-gcc16.patch

# Can't do this because it causes everything else to be noarch
# BuildArch: noarch
BuildRequires: make
BuildRequires: gcc gcc-c++
BuildRequires: xz libXaw-devel libXi-devel ncurses-devel bison flex file perl(Digest::MD5) texinfo gcc-c++
BuildRequires: gd-devel
BuildRequires: teckit-devel >= 2.5.7
BuildRequires: freetype-devel libpng-devel t1lib-devel zlib-devel t1utils
%if %{with poppler}
BuildRequires: poppler-devel
%else
BuildRequires: xpdf-devel >= 4.03
BuildRequires: glib2-devel fontconfig-devel
%endif
BuildRequires: zziplib-devel libicu-devel cairo-devel harfbuzz-devel perl-generators pixman-devel graphite2-devel
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires: libgs-devel
%else
BuildRequires: ghostscript-devel
%endif
BuildRequires: libpaper-devel potrace-devel autoconf automake libtool
BuildRequires: gmp-devel mpfr-devel
# This is really for macros.
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%if %{without bootstrap}
# This is for xindy
BuildRequires: clisp-devel
BuildRequires: texlive-cyrillic, texlive-latex, texlive-metafont, texlive-cm-super, texlive-ec
%endif
# This is temporary to fix build while missing kpathsea dep is active
BuildRequires: texlive-texlive-scripts
# This is needed for a test
BuildRequires: texlive-amsfonts
# RPATH DIE DIE DIE
BuildRequires: chrpath
# Break an ugly dep loop
BuildRequires: tex(expl3.sty)


# Cleanup Provides/Obsoletes
# texlive-cjk-gs-integrate (depackaged 2018-03-09)
Provides: texlive-cjk-gs-integrate = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cjk-gs-integrate <= 7:20170520
Provides: tex-cjk-gs-integrate = %{epoch}:%{source_date}-%{release}
Obsoletes: tex-cjk-gs-integrate <= 7:20170520
Provides: texlive-cjk-gs-integrate-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-cjk-gs-integrate-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cjk-gs-integrate-bin <= 7:20170520
Obsoletes: tex-cjk-gs-integrate-bin <= 7:20170520
Provides: texlive-cjk-gs-integrate-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cjk-gs-integrate-doc <= 7:20170520
# Removed between TL2023 and TL2025
Provides: texlive-ms = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ms <= 11:svn57473
Provides: texlive-ms-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ms-doc <= 11:svn57473
# All of these context components got marked as obsolete upstream and removed from TL
Provides: texlive-context-account = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-account-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-account <= 11:svn47085
Obsoletes: texlive-context-account-doc <= 11:svn47085
Provides: texlive-context-algorithmic = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-algorithmic <= 11:svn47085
Provides: texlive-context-annotation = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-annotation-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-annotation <= 11:svn47085
Obsoletes: texlive-context-annotation-doc <= 11:svn47085
Provides: texlive-context-bnf = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-bnf-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-bnf <= 11:svn47085
Obsoletes: texlive-context-bnf-doc <= 11:svn47085
Provides: texlive-context-chromato = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-chromato-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-chromato <= 11:svn47085
Obsoletes: texlive-context-chromato-doc <= 11:svn47085
Provides: texlive-context-cmscbf = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-cmscbf <= 11:svn47085
Provides: texlive-context-cmttbf = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-cmttbf <= 11:svn47085
Provides: texlive-context-construction-plan = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-construction-plan-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-construction-plan <= 11:svn47085
Obsoletes: texlive-context-construction-plan-doc <= 11:svn47085
Provides: texlive-context-degrade = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-degrade-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-degrade <= 11:svn47085
Obsoletes: texlive-context-degrade-doc <= 11:svn47085
Provides: texlive-context-fancybreak = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-fancybreak-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-fancybreak <= 11:svn47085
Obsoletes: texlive-context-fancybreak-doc <= 11:svn47085
Provides: texlive-context-french = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-french-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-french <= 11:svn54215
Obsoletes: texlive-context-french-doc <= 11:svn54215
Provides: texlive-context-fullpage = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-fullpage-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-fullpage <= 11:svn47085
Obsoletes: texlive-context-fullpage-doc <= 11:svn47085
Provides: texlive-context-gantt = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-gantt-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-gantt <= 11:svn47085
Obsoletes: texlive-context-gantt-doc <= 11:svn47085
Provides: texlive-context-inifile = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-inifile <= 11:svn47085
Provides: texlive-context-layout = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-layout <= 11:svn47085
Provides: texlive-context-lettrine = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-lettrine-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-lettrine <= 11:svn47085
Obsoletes: texlive-context-lettrine-doc <= 11:svn47085
Provides: texlive-context-rst = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-rst-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-rst <= 11:svn47085
Obsoletes: texlive-context-rst-doc <= 11:svn47085
Provides: texlive-context-ruby = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-ruby-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-ruby <= 11:svn47085
Obsoletes: texlive-context-ruby-doc <= 11:svn47085
Provides: texlive-context-simplefonts = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-simplefonts-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-simplefonts <= 11:svn47085
Obsoletes: texlive-context-simplefonts-doc <= 11:svn47085
Provides: texlive-context-title = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-title-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-title <= 11:svn47085
Obsoletes: texlive-context-title-doc <= 11:svn47085
Provides: texlive-context-typearea = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-typearea-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-typearea <= 11:svn47085
Obsoletes: texlive-context-typearea-doc <= 11:svn47085
# collection-texworks is windows only and we don't package it anymore
Provides: texlive-collection-texworks = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-collection-texworks <= 11:20230311
# These components are under non-free licenses and should not have been packaged before
# (whoops)
Provides: texlive-aalok = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-aalok <= 11:svn61719
Provides: texlive-axessibility = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-axessibility <= 11:svn57105
Provides: texlive-chhaya = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-chhaya <= 11:svn61719
Provides: texlive-gentle = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-gentle <= 11:svn15878.0
Provides: texlive-gentle-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-gentle-doc <= 11:svn15878.0
Provides: texlive-hep = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-hep <= 11:svn15878.1.0
Provides: texlive-hep-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-hep-doc <= 11:svn15878.1.0
Provides: texlive-marathi = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-marathi <= 11:svn61719
# These components were empty and we've stopped packaging them
Provides: texlive-gustprog-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-gustprog-doc <= 11:svn54074
Provides: texlive-metatype1 = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-metatype1 <= 11:svn37105
# We do not currently package "dev" binaries because
# managing them is a headache and can break user expectations.
# If you really know what you're doing, this should be straightforward
# to shove in by hand.
Provides: texlive-latex-bin-dev = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex-bin-dev <= 11:svn66186
Provides: texlive-xelatex-dev = %{epoch}:%{source_date}-%{release}
# Not marked as obsolete upstream, but not pulled in by anything anymore
Provides: texlive-luaintro-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-luaintro-doc <= 11:svn35490.0.03
# These components are obsolete and removed from TL
Provides: texlive-afparticle = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-afparticle <= 11:svn35900.1.3
Provides: texlive-afparticle-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-afparticle-doc <= 11:svn35900.1.3
Provides: texlive-babel-bahasa = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-babel-bahasa <= 11:svn30255.1.0l.metapackage
Provides: texlive-babel-bahasa-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-babel-bahasa-doc <= 11:svn30255.1.0l.metapackage
Provides: texlive-baskervald = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-baskervald <= 11:svn19490.1.016
Provides: texlive-baskervald-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-baskervald-doc <= 11:svn19490.1.016
Provides: texlive-electrum = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-electrum <= 11:svn19705.1.005_b
Provides: texlive-electrum-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-electrum-doc <= 11:svn19705.1.005_b
Provides: texlive-gentium-tug = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-gentium-tug <= 11:svn63470
Provides: texlive-gentium-tug-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-gentium-tug-doc <= 11:svn63470
Provides: texlive-iwhdp = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-iwhdp <= 11:svn37552.0.50
Provides: texlive-iwhdp-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-iwhdp-doc <= 11:svn37552.0.50
Provides: texlive-lualatex-doc-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-lualatex-doc-doc <= 11:svn30473.0
Provides: texlive-mendex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mendex-doc <= 11:svn15878.1.5
Provides: texlive-padauk = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-padauk <= 11:svn42617
Provides: texlive-penrose = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-penrose <= 11:svn57508
Provides: texlive-romande = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-romande <= 11:svn19537.1.008_v7_sc
Provides: texlive-romande-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-romande-doc <= 11:svn19537.1.008_v7_sc
Provides: texlive-substitutefont = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-substitutefont <= 11:svn32066.0.1.4
Provides: texlive-substitutefont-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-substitutefont-doc <= 11:svn32066.0.1.4
Provides: texlive-tex-refs-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tex-refs-doc <= 11:svn57349
Provides: texlive-xmltexconfig = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-xmltexconfig <= 11:svn45845
Provides: texlive-xput = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-xput <= 11:svn65325

%description
The TeX Live software distribution offers a complete TeX system for a
variety of Unix, Macintosh, Windows and other platforms. It
encompasses programs for editing, typesetting, previewing and printing
of TeX documents in many different languages, and a large collection
of TeX macros and font libraries.

The distribution includes extensive general documentation about TeX,
as well as the documentation for the included software packages.

%package -n %{shortname}-a2ping
Version: svn52964
Provides: texlive-a2ping = %{epoch}:%{source_date}-%{release}
Provides: tex-a2ping = %{epoch}:%{source_date}-%{release}
Provides: texlive-a2ping-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-a2ping-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-a2ping-bin < 7:20170520
License: GPL-1.0-or-later
Summary: Advanced PS, PDF, EPS converter
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-a2ping
a2ping is a Perl script command line utility written for Unix
that converts many raster image and vector graphics formats to
EPS or PDF and other page description formats. Accepted input
file formats are: PS (PostScript), EPS, PDF, PNG, JPEG, TIFF,
PNM, BMP, GIF, LBM, XPM, PCX, TGA. Accepted output formats are:
EPS, PCL5, PDF, PDF1, PBM, PGM, PPM, PS, markedEPS, markedPS,
PNG, XWD, BMP, TIFF, JPEG, GIF, XPM. a2ping delegates the low-
level work to Ghostscript (GS), pdftops and sam2p. a2ping fixes
many glitches during the EPS to EPS conversion, so its output
is often more compatible and better embeddable than its input.

%package -n %{shortname}-accfonts
Version: svn18835
Provides: texlive-accfonts = %{epoch}:%{source_date}-%{release}
Provides: tex-accfonts = %{epoch}:%{source_date}-%{release}
Provides: texlive-accfonts-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-accfonts-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-accfonts-bin < 7:20170520
Provides: tex-accfonts-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-accfonts-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-accfonts-doc < 7:20170520
License: GPL-1.0-or-later
Summary: Utilities to derive new fonts from existing ones
Requires: texlive-base
Requires: texlive-kpathsea
BuildArch: noarch

%description -n %{shortname}-accfonts
The accfonts package contains three utilities to permit easy
manipulation of fonts, in particular the creation of unusual
accented characters. Mkt1font works on Adobe Type 1 fonts,
vpl2vpl works on TeX virtual fonts and vpl2ovp transforms a TeX
font to an Omega one. All three programs read in a font (either
the font itself or a property list), together with a simple
definition file containing lines such as '128 z acute'; they
then write out a new version of the font with the requested new
characters in the numerical slots specified. Great care is
taken over the positioning of accents, and over the provision
of kerning information for new characters; mkt1font also
generates suitable "hints" to enhance quality at small sizes or
poor resolutions. The programs are written in Perl.

%package -n %{shortname}-adhocfilelist
Version: svn29349
Provides: texlive-adhocfilelist = %{epoch}:%{source_date}-%{release}
Provides: tex-adhocfilelist = %{epoch}:%{source_date}-%{release}
Provides: texlive-adhocfilelist-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-adhocfilelist-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-adhocfilelist-bin < 7:20170520
Provides: tex-adhocfilelist-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-adhocfilelist-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-adhocfilelist-doc < 7:20170520
License: LPPL-1.3c
Summary: '\listfiles' entries from the command line
Requires: texlive-base
Requires: texlive-kpathsea
# shell
BuildArch: noarch

%description -n %{shortname}-adhocfilelist
The package provides a Unix shell script to display a list of
LaTeX \Provides...-command contexts on screen. Provision is
made for controlling the searches that the package does. The
package was developed on a Unix-like system, using (among other
things) the gnu variant of the find command.

%package -n %{shortname}-afm2pl
Version: svn71515
Provides: texlive-afm2pl = %{epoch}:%{source_date}-%{release}
Provides: tex-afm2pl = %{epoch}:%{source_date}-%{release}
Provides: texlive-afm2pl-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-afm2pl-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-afm2pl-bin < 7:20170520
License: GPL-2.0-only
Summary: Convert AFM to TeX property list (.pl) metrics
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-afm2pl
afm2pl is an open source font utility for easy installation of commercial fonts
in TeX. Afm2pl is meant to be a partial alternative to afm2tfm, on which it is
based. Its default action is to convert an afm file to a pl file, which in its
turn can be converted to a tfm file, with preservation of kerns and ligatures
(with afm2tfm, preserving kerns and ligatures is possible only in a roundabout
way).

%package -n %{shortname}-albatross
Version: svn73436
Provides: texlive-albatross = %{epoch}:%{source_date}-%{release}
Summary: Find fonts that contain a given glyph
License: BSD-3-Clause
Requires: texlive-base texlive-kpathsea

%description -n %{shortname}-albatross
This is a command line tool for finding fonts that contain a
given (Unicode) glyph. It relies on Fontconfig.

%package -n %{shortname}-aleph
Summary: Extended TeX
Version: svn77830
Provides: texlive-aleph = %{epoch}:%{source_date}-%{release}
Provides: tex-aleph = %{epoch}:%{source_date}-%{release}
Provides: texlive-aleph-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-aleph-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-aleph-bin < 7:20170520
Provides: tex-aleph-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-aleph-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-aleph-doc < 7:20170520
# NOTE: The tlpkg is wrong, it says "GPL"
# Source code is definitely LGPL-2.1-or-later
License: LGPL-2.1-or-later
Requires(post,postun): coreutils
Requires: texlive-antomega
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-l3kernel
Requires: texlive-lambda
Requires: texlive-latex
Requires: texlive-latex-fonts
Requires: texlive-omega
Requires: texlive-plain

%description -n %{shortname}-aleph
An development of omega, using most of the extensions of TeX itself developed
for e-TeX.

%package -n %{shortname}-amstex
Summary: American Mathematical Society plain TeX macros
Version: svn77830
Provides: texlive-amstex = %{epoch}:%{source_date}-%{release}
Provides: tex-amstex = %{epoch}:%{source_date}-%{release}
Provides: texlive-amstex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-amstex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-amstex-bin < 7:20170520
Provides: tex-amstex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-amstex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-amstex-doc < 7:20170520
License: LPPL-1.3c
# symlinks only
BuildArch: noarch
Requires(post,postun): coreutils
Requires: texlive-amsfonts
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-pdftex
Requires: texlive-plain
Requires: texlive-tex

%description -n %{shortname}-amstex
AMS-TeX is a TeX macro package, originally written by Michael Spivak for the
American Mathematical Society (AMS) during 1983-1985 and is described in the
book 'The Joy of TeX'. It is based on Plain TeX, and provides many features for
producing more professional-looking maths formulas with less burden on authors.
This is the final archival distribution of AMS-TeX. AMS-TeX is no longer
supported by the AMS, nor is it used by the AMS publishing program. The AMS
does not recommend creating any new documents using AMS-TeX; this distribution
will be left on CTAN to facilitate processing of legacy documents and as a
historical record of a pioneering TeX macro collection that played a key role
in popularizing TeX and revolutionizing mathematics publishing. In addition to
the "User's Guide to AMS-TeX", the AMS has also made the full text of the most
recent reprint of the second edition of "The Joy of TeX" by Michael Spivak
available as a pdf file. AMS-TeX is the historical basis of amslatex, which
should now be used to prepare submissions for the AMS.

%package -n %{shortname}-aomart
Summary: Typeset articles for the Annals of Mathematics
Version: svn76110
Provides: tex-aomart = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-aomart
The package provides a class for typesetting articles for The Annals of
Mathematics.

%package -n %{shortname}-arara
Summary: Automation of LaTeX compilation
Version: svn75653
Provides: texlive-arara = %{epoch}:%{source_date}-%{release}
Provides: tex-arara = %{epoch}:%{source_date}-%{release}
Provides: texlive-arara-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-arara-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-arara-bin < 7:20170520
Provides: tex-arara-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-arara-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-arara-doc < 7:20170520
Provides: bundled(slf4j) = 1.7.36
Provides: bundled(annotations) = 13.0
Provides: bundled(apache-commons-collections) = 3.2.1
Provides: bundled(apache-commons-exec) = 1.1
Provides: bundled(apache-commons-lang3) = 3.1
Provides: bundled(apache-commons-cli) = 1.2
Provides: bundled(log4j) = 2.17.2
Provides: bundled(mvel2) = 2.4.14
Provides: bundled(snakeyaml-engine) = 2.3
Provides: bundled(logback) = 1.0.1
License: BSD-3-Clause
# shell
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-arara
Arara is comparable with other well-known compilation tools like latexmk and
rubber. The key difference is that arara determines its actions from metadata
in the source code, rather than relying on indirect resources, such as log file
analysis. Arara requires a Java virtual machine.

%package -n %{shortname}-attachfile2
Summary: Attach files into PDF
Version: svn77682
Provides: texlive-attachfile2 = %{epoch}:%{source_date}-%{release}
Provides: tex-attachfile2 = %{epoch}:%{source_date}-%{release}
Provides: tex-attachfile2-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-attachfile2-bin = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
# perl
BuildArch: noarch
Requires: tex(color.sty)
Requires: tex(hycolor.sty)
Requires: tex(hyperref.sty)
Requires: tex(iftex.sty)
Requires: tex(infwarerr.sty)
Requires: tex(keyval.sty)
Requires: tex(kvoptions.sty)
Requires: tex(ltxcmds.sty)
Requires: tex(pdfescape.sty)
Requires: tex(pdftexcmds.sty)
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-attachfile2
This package can be used to attach files to a PDF document. It is a further
development of Scott Pakin's package attachfile for pdfTeX. Apart from bug
fixes, this package adds support for dvips, some new options, and gets and
writes meta information data about the attached files.

%package -n %{shortname}-authorindex
Version: svn51757
Provides: texlive-authorindex = %{epoch}:%{source_date}-%{release}
Provides: tex-authorindex = %{epoch}:%{source_date}-%{release}
Provides: texlive-authorindex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-authorindex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-authorindex-bin < 7:20170520
Provides: tex-authorindex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-authorindex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-authorindex-doc < 7:20170520
License: LPPL-1.3c
Summary: Index citations by author names
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-authorindex
This package allows the user to create an index of all authors
cited in a LaTeX document. Each author entry in the index
contains the pages where these citations occur. Alternatively,
the package can list the labels of the citations that appear in
the references rather than the text pages. The package relies
on BibTeX being used to handle citations. Additionally, it
requires Perl (version 5 or higher).

%package -n %{shortname}-autosp
Summary: A Preprocessor that generates note-spacing commands for MusiXTeX scores
Version: svn77851
Provides: texlive-autosp = %{epoch}:%{source_date}-%{release}
Provides: tex-autosp = %{epoch}:%{source_date}-%{release}
Provides: texlive-autosp-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-autosp-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-autosp-bin < 7:20170520
Provides: tex-autosp-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-autosp-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-autosp-doc < 7:20170520
License: GPL-2.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-autosp
This program simplifies the creation of MusiXTeX scores by converting
(non-standard) commands of the form \anotes ... \en into one or more
conventional note-spacing commands, as determined by the note values
themselves, with \sk spacing commands inserted as necessary. The coding for an
entire measure can be entered one part at a time, without concern for
note-spacing changes within the part or spacing requirements of other parts.
For example, \anotes\qa J\qa K&\ca l\qa m\ca n\en generates \Notes\qa J\sk\qa
K\sk&\ca l\qa m\sk\ca n\en .

%package -n %{shortname}-axodraw2
Summary: Feynman diagrams in a LaTeX document
Version: svn77682
Provides: texlive-axodraw2 = %{epoch}:%{source_date}-%{release}
Provides: tex-axodraw2 = %{epoch}:%{source_date}-%{release}
Provides: texlive-axodraw2-bin = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
Requires: tex(color.sty)
Requires: tex(graphicx.sty)
Requires: tex(ifthen.sty)
Requires: tex(ifxetex.sty)
Requires: tex(keyval.sty)
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-axodraw2
This package defines macros for drawing Feynman graphs in LaTeX documents. It
is an important update of the axodraw package, but since it is not completely
backwards compatible, we have given the style file a changed name. Many new
features have been added, with new types of line, and much more flexibility in
their properties. In addition, it is now possible to use axodraw2 with
pdfLaTeX, as well as with the LaTeX-dvips method. However with pdfLaTeX (and
also LuaLaTeX and XeLaTeX), an external program, axohelp, is used to perform
the geometrical calculations needed for the pdf code inserted in the output
file. The processing involves a run of pdfLaTeX, a run of axohelp, and then
another run of pdfLaTeX.

%package -n %{shortname}-bib2gls
Summary: Command line application to convert .bib files to glossaries-extra.sty resource files
Version: svn76845
Provides: texlive-bib2gls = %{epoch}:%{source_date}-%{release}
Provides: tex-bib2gls = %{epoch}:%{source_date}-%{release}
Provides: texlive-bib2gls-bin = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
# Java and shell
BuildArch: noarch
Requires: texlive-base
Requires: texlive-glossaries-extra
Requires: texlive-kpathsea

%description -n %{shortname}-bib2gls
This Java command line application may be used to extract glossary information
stored in a .bib file and convert it into glossary entry definition commands.
This application should be used with glossaries-extra.sty's 'record' package
option. It performs two functions in one: selects entries according to records
found in the .aux file (similar to bibtex), hierarchically sorts entries and
collates location lists (similar to makeindex or xindy). The glossary entries
can then be managed in a system such as JabRef, and only the entries that are
actually required will be defined, reducing the resources required by TeX. The
supplementary application convertgls2bib can be used to convert existing .tex
files containing definitions (\newglossaryentry etc.) to the .bib format
required by bib2gls.

%package -n %{shortname}-bibcop
Summary: Style checker for .bib files
Version: svn75042
License: MIT
Requires: texlive-base texlive-kpathsea
Requires: tex(iexec.sty)
Requires: tex(pgfopts.sty)
# perl
BuildArch: noarch

%description -n %{shortname}-bibcop
This LaTeX package checks the quality of your .bib file and
emits warning messages if any issues are found. For this, the
TeX processor must be run with the --shell-escape option, and
Perl must be installed. bibcop.pl can also be used as a
standalone command line tool. The package does not work on
Windows.

%package -n %{shortname}-bibexport
Version: svn50677
Provides: texlive-bibexport = %{epoch}:%{source_date}-%{release}
Provides: tex-bibexport = %{epoch}:%{source_date}-%{release}
Provides: texlive-bibexport-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-bibexport-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bibexport-bin < 7:20170520
Provides: tex-bibexport-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-bibexport-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bibexport-doc < 7:20170520
License: LPPL-1.3c
Summary: Extract a BibTeX file based on a .aux file
Requires: texlive-base
Requires: texlive-kpathsea
BuildArch: noarch

%description -n %{shortname}-bibexport
A Bourne shell script that uses BibTeX to extract bibliography
entries that are \cite'd in a document. It can also expand a
BibTeX file, expanding the abbreviations (other than the built-
in ones like month names) and followig the cross-references.

%package -n %{shortname}-bibtex
Summary: Process bibliographies (bib files) for LaTeX or other formats
Version: svn77830
Provides: texlive-bibtex = %{epoch}:%{source_date}-%{release}
Provides: tex-bibtex = %{epoch}:%{source_date}-%{release}
Provides: texlive-bibtex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-bibtex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bibtex-bin < 7:20170520
Provides: tex-bibtex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-bibtex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bibtex-doc < 7:20170520
License: Knuth-CTAN
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-bibtex
BibTeX allows the user to store his citation data in generic form, while
printing citations in a document in the form specified by a BibTeX style, to be
specified in the document itself (one often needs a LaTeX citation-style
package, such as natbib, as well). BibTeX knows nothing about Unicode sorting
algorithms or scripts, although it will pass on whatever bytes it reads. Its
descendant bibtexu does support Unicode, via the ICU library. The older
alternative bibtex8 supports 8-bit character sets. Another Unicode-aware
alternative is the (independently developed) biber program, used with the
BibLaTeX package to typeset its output.

%package -n %{shortname}-bibtexperllibs
Summary: BibTeX Perl Libraries
Version: svn76255
Provides: tex-bibtexperllibs = %{epoch}:%{source_date}-%{release}
License: GPL-1.0-or-later OR Artistic-1.0-Perl
# perl
BuildArch: noarch
# So... we've got these modules packaged up from CPAN.
Requires: perl(BibTeX::Parser::Author)
Requires: perl(BibTeX::Parser::Entry)
Requires: perl(LaTeX::ToUnicode::Tables)
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-bibtexperllibs
This package provides BibTeX related Perl libraries by Gerhard Gossen, repacked
by Boris Veytsman, for TeX Live and other TDS-compliant distributions. The
libraries are written in pure Perl, so should work out of the box on any
architecture. They have been packaged here mostly for Boris Veytsman's BibTeX
suite, but can be used in any other Perl script.

%package -n %{shortname}-bibtexu
Version: svn66186
Provides: texlive-bibtexu = %{epoch}:%{source_date}-%{release}
Provides: tex-bibtexu = %{epoch}:%{source_date}-%{release}
Provides: texlive-bibtexu-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-bibtexu-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bibtexu-bin < 7:20170520
Provides: tex-bibtexu-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-bibtexu-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bibtexu-doc < 7:20170520
License: LPPL-1.3c
Summary: BibTeX variant supporting Unicode (UTF-8), via ICU
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-bibtexu
An enhanced, portable C version of BibTeX. Unicode is supported
via the ICU library. Originally written by Yannis Haralambous
and his students, and derived from bibtex8, with substantial
updates from the Japanese TeX Development Community, it is now
maintained as part of TeX Live.

%package -n %{shortname}-bibtex8
Summary: BibTeX variant supporting 8-bit encodings
Version: svn75712
Provides: texlive-bibtex8 = %{epoch}:%{source_date}-%{release}
Provides: tex-bibtex8 = %{epoch}:%{source_date}-%{release}
Provides: texlive-bibtex8-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-bibtex8-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bibtex8-bin < 7:20170520
Provides: tex-bibtex8-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-bibtex8-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bibtex8-doc < 7:20170520
License: GPL-1.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-bibtex8
An enhanced, portable C version of BibTeX. Enhanced by conversion to larger
(32-bit) capacity, addition of run-time selectable capacity and 8-bit support
extensions. National character set and sorting order are controlled by an
external configuration file. Various examples are included. Originally written
by Niel Kempson and Alejandro Aguilar-Sierra, it is now maintained as part of
TeX Live.

%package -n %{shortname}-bookshelf
Version: svn72521
Provides: tex-bookshelf = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
Summary: Create a nice image from a BibTeX file
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-bookshelf
This package turns a BibTeX bibliography file into a
randomly-coloured, randomly-sized shelf of books, with the
title and author in a randomly-chosen typeface.

%package -n %{shortname}-bundledoc
Version: svn74306
Provides: texlive-bundledoc = %{epoch}:%{source_date}-%{release}
Provides: tex-bundledoc = %{epoch}:%{source_date}-%{release}
Provides: texlive-bundledoc-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-bundledoc-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bundledoc-bin < 7:20170520
Provides: tex-bundledoc-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-bundledoc-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-bundledoc-doc < 7:20170520
License: LPPL-1.3c
Summary: Bundle together all the files needed to build a LaTeX document
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-bundledoc
The bundledoc package is a post-processor for the snapshot
package that bundles together all the classes, packages and
files needed to build a given LaTeX document. It reads the .dep
file that snapshot produces, finds each of the files mentioned
therein, and archives them into a single .tar.gz (or .zip, or
whatever) file, suitable for moving across systems,
transmitting to a colleague, etc. A script, arlatex, provides
an alternative "archiving" mechanism, creating a single LaTeX
file that contains all of the ancillary files of a LaTeX
document, together with the document itself, using the
filecontents* environment.

%package -n %{shortname}-cachepic
Version: svn26313
Provides: texlive-cachepic = %{epoch}:%{source_date}-%{release}
Provides: tex-cachepic = %{epoch}:%{source_date}-%{release}
Provides: texlive-cachepic-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-cachepic-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cachepic-bin < 7:20170520
Provides: tex-cachepic-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-cachepic-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cachepic-doc < 7:20170520
License: LPPL-1.3c
Summary: Convert document fragments into graphics
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(graphicx.sty)
Requires: tex(verbatim.sty)
# lua
BuildArch: noarch

%description -n %{shortname}-cachepic
The bundle simplifies and automates conversion of document
fragments into external EPS or PDF files. The bundle consists
of two parts: a LaTeX package that implements a document level
interface, and a command line tool (written in lua) that
generates the external graphics.

%package -n %{shortname}-checkcites
Version: svn73120
Provides: texlive-checkcites = %{epoch}:%{source_date}-%{release}
Provides: tex-checkcites = %{epoch}:%{source_date}-%{release}
Provides: texlive-checkcites-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-checkcites-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-checkcites-bin < 7:20170520
Provides: tex-checkcites-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-checkcites-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-checkcites-doc < 7:20170520
License: LPPL-1.3c
Summary: Check citation commands in a document
Requires: texlive-base
Requires: texlive-kpathsea
# lua script
BuildArch: noarch

%description -n %{shortname}-checkcites
The package provides a lua script written for the sole purpose
of detecting undefined and unused references from LaTeX
auxiliary or bibliography files.

%package -n %{shortname}-checklistings
Version: svn38300
Provides: texlive-checklistings = %{epoch}:%{source_date}-%{release}
Provides: tex-checklistings = %{epoch}:%{source_date}-%{release}
Provides: texlive-checklistings-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-checklistings-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-checklistings-bin < 7:20170520
Provides: tex-checklistings-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-checklistings-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-checklistings-doc < 7:20170520
License: LPPL-1.3a
Summary: Pass verbatim contents through a compiler and reincorporate the resulting output
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(keyval.sty)
Requires: tex(kvoptions.sty)
Requires: tex(fancyvrb.sty)
Requires: tex(color.sty)
Requires: tex(listings.sty)
# shell script
BuildArch: noarch

%description -n %{shortname}-checklistings
This package augments the fancyvrb and listings packages to
allow the source code they contain to be checked by an external
tool (like a compiler). The external tool's messages can be
automatically reincorporated into the original document. The
package does not focus on a specific programming language, but
it is designed to work well with languages and compilers in the
ML family.

%package -n %{shortname}-chklref
Version: svn52649
Provides: texlive-chklref = %{epoch}:%{source_date}-%{release}
Provides: tex-chklref = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
Summary: Check for problems with labels in LaTeX
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(afterpackage.sty)
Requires: tex(auxhook.sty)
Requires: tex(currfile.sty)
# perl
BuildArch: noarch

%description -n %{shortname}-chklref
It is quite common that after modifying a TeX file, many unused
labels remain in it. The purpose of chklref is to automatically
find these useless labels. It also looks for "non starred"
mathematical environments with no labels and advises the user
to use a starred version instead.

%package -n %{shortname}-chktex
Summary: Check for errors in LaTeX documents
Version: svn78219
Provides: texlive-chktex = %{epoch}:%{source_date}-%{release}
Provides: tex-chktex = %{epoch}:%{source_date}-%{release}
Provides: texlive-chktex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-chktex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-chktex-bin < 7:20170520
Provides: tex-chktex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-chktex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-chktex-doc < 7:20170520
License: GPL-2.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-chktex
The program reports typographic and other errors in LaTeX documents. Filters
are also provided for checking the LaTeX parts of CWEB documents.

%package -n %{shortname}-citation-style-language
Summary: Bibliography formatting with Citation Style Language
Version: svn77682
Provides: texlive-citation-style-language = %{epoch}:%{source_date}-%{release}
Provides: texlive-citation-style-language-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-citation-style-language-doc = %{epoch}:%{source_date}-%{release}
License: MIT AND CC0-1.0 AND CC-BY-SA-3.0
# lua
BuildArch: noarch
Requires: tex(filehook.sty)
Requires: tex(url.sty)
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-l3kernel
Requires: texlive-l3packages
Requires: texlive-lua-tinyyaml
Requires: texlive-lua-uca
Requires: texlive-lualibs
Requires: texlive-luatex
Requires: texlive-luaxml
Requires: texlive-url

%description -n %{shortname}-citation-style-language
The Citation Style Language (CSL) is an XML-based language that defines the
formats of citations and bibliography. There are currently thousands of styles
in CSL including the most widely used APA, Chicago, Vancouver, etc. The
citation-style-language package is aimed to provide another reference
formatting method for LaTeX that utilizes the CSL styles. It contains a
citation processor implemented in pure Lua (citeproc-lua) which reads
bibliographic metadata and performs sorting and formatting on both citations
and bibliography according to the selected CSL style. A LaTeX package
(citation-style-language.sty) is provided to communicate with the processor.

%if 0
%package -n %{shortname}-cjk-gs-integrate
Version: svn59705
Provides: texlive-cjk-gs-integrate = %{epoch}:%{source_date}-%{release}
Provides: tex-cjk-gs-integrate = %{epoch}:%{source_date}-%{release}
Provides: texlive-cjk-gs-integrate-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-cjk-gs-integrate-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cjk-gs-integrate-bin < 7:20170520
Provides: tex-cjk-gs-integrate-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-cjk-gs-integrate-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cjk-gs-integrate-doc < 7:20170520
License: GPL-3.0-or-later
Summary: Tools to integrate CJK fonts into Ghostscript
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-cjk-gs-integrate
This script searches a list of directories for CJK fonts, and
makes them available to an installed GhostScript. In the
simplest case with sufficient privileges, a run without
arguments should effect in a complete setup of GhostScript.
%endif

%package -n %{shortname}-cjkutils
Version: svn60833
Provides: texlive-cjkutils = %{epoch}:%{source_date}-%{release}
Provides: tex-cjkutils = %{epoch}:%{source_date}-%{release}
Provides: texlive-cjkutils-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-cjkutils-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cjkutils-bin < 7:20170520
License: LPPL-1.3c
Summary: cjkutils package
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-cjkutils
cjkutils package.

%package -n %{shortname}-clojure-pamphlet
Summary: A simple literate programming tool based on clojure's pamphlet system
Version: svn77682
Provides: texlive-clojure-pamphlet = %{epoch}:%{source_date}-%{release}
Provides: tex-clojure-pamphlet = %{epoch}:%{source_date}-%{release}
Provides: texlive-clojure-pamphlet-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-clojure-pamphlet-bin = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
# perl
BuildArch: noarch
Requires: tex(hyperref.sty)
Requires: tex(listings.sty)
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-clojure-pamphlet
The Clojure pamphlet system is a system based on the Clojure literate system.
In the Clojure's pamphlet system you have your main LaTeX file, which can be
compiled regularly. This file contains documentation and source code (just like
in other forms of literate programming). These code snippets are wrapped in the
chunk environment, hence they can be recognized by the tangler in order to
extract them. Chunks can be included inside each other by the getchunk command
(which will be typeset accordingly). Finally, the LaTeX file will be run
through the tangler to get the desired chunk of code.

%package -n %{shortname}-cluttex
Version: svn74655
Provides: texlive-cluttex = %{epoch}:%{source_date}-%{release}
Provides: tex-cluttex = %{epoch}:%{source_date}-%{release}
Provides: texlive-cluttex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-cluttex-bin = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
Summary: An automation tool for running LaTeX
Requires: texlive-base
Requires: texlive-kpathsea
# lua
BuildArch: noarch

%description -n %{shortname}-cluttex
This is another tool for the automation of LaTeX document
processing, like latexmk or arara. The main feature of this
tool is that it does not clutter your working directory with
.aux or .log or other auxiliary files. It has of course the
usual features of automation tools: It automatically re-runs
(La)TeX for cross-references. MakeIndex, BibTeX, Biber, or
makeglossaries will be executed if a corresponding option is
set. Furthermore, cluttex can watch input files for changes
(using an external program).

%package -n %{shortname}-context
Summary: The ConTeXt macro package
Version: svn78010
Provides: texlive-context = %{epoch}:%{source_date}-%{release}
Provides: tex-context = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-context-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-bin < 7:20170520
Provides: tex-context-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-context-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-context-doc < 7:20170520
License: GPL-1.0-or-later OR LPPL-1.3c
Requires(post,postun): coreutils, lua
# for /usr/bin/realpath
Requires: coreutils
Requires: lua
Requires: ruby
Requires: tex(pstricks.sty)
Requires: tex(pst-plot.sty)
Requires: texlive-amsfonts
Requires: texlive-base
Requires: texlive-dejavu
Requires: texlive-kpathsea
Requires: texlive-lm
Requires: texlive-lm-math
Requires: texlive-luatex
Requires: texlive-manfnt-font
Requires: texlive-metapost
Requires: texlive-mflogo-font
Requires: texlive-mptopdf
Requires: texlive-stmaryrd
%if %{without bootstrap}
Requires: texlive-pdftex
Requires: texlive-xetex
%endif
# shell and lua
BuildArch: noarch

%description -n %{shortname}-context
A full featured, parameter driven macro package, which fully supports advanced
interactive documents. See the ConTeXt Wiki for more information. This content
on CTAN is packaged independently of the ConTeXt project, so if you have a
problem with ConTeXt itself, it is best to report it to the official
ntg-context@ntg.nl mailing list. If you notice that ConTeXt is mispackaged in
TeX Live or CTAN, then please open a new issue on GitHub, email the public
ntg-context@ntg.nl or tex-live@tug.org mailing lists, or email me privately at
tex@maxchernoff.ca. Pull requests are also gladly accepted.

# This package exists because it is 90M and most people do not need it

%package -n %{shortname}-context-doc
Version: svn75454
Provides: texlive-context-doc = %{epoch}:%{source_date}-%{release}
Requires: texlive-context
Provides: tex-context-doc = %{epoch}:%{source_date}-%{release}
Summary: Documentation for context
License: GPL-1.0-or-later OR LPPL-1.3c

%description -n %{shortname}-context-doc
Documentation for context.

%package -n %{shortname}-context-legacy
Summary: The ConTeXt macro package, MkII
Version: svn78010
Provides: texlive-context-legacy-doc = %{epoch}:%{source_date}-%{release}
Provides: tex-context-legacy = %{epoch}:%{source_date}-%{release}
License: LicenseRef-Fedora-Public-Domain
# just shell stubs
BuildArch: noarch
Requires: texlive-amsfonts
Requires: texlive-base
Requires: texlive-context
Requires: texlive-kpathsea
Requires: texlive-lm
Requires: texlive-ly1
Requires: texlive-manfnt-font
Requires: texlive-mflogo-font
Requires: texlive-mptopdf
Requires: texlive-pdftex
Requires: texlive-stmaryrd

%description -n %{shortname}-context-legacy
In TeX Live, ConTeXt MkII is split from current ConTeXt (MkIV and newer). We
use the ConTeXt repackaging as distributed from
https://github.com/gucci-on-fleek/context-packaging. See
https://contextgarden.net and https://pragma-ade.com for information about
ConTeXt.

%package -n %{shortname}-convbkmk
Version: svn49252
Provides: texlive-convbkmk = %{epoch}:%{source_date}-%{release}
Provides: tex-convbkmk = %{epoch}:%{source_date}-%{release}
Provides: texlive-convbkmk-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-convbkmk-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-convbkmk-bin < 7:20170520
Provides: tex-convbkmk-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-convbkmk-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-convbkmk-doc < 7:20170520
License: MIT
Summary: Correct platex/uplatex bookmarks in PDF created with hyperref
Requires: texlive-base
Requires: texlive-kpathsea
Requires: ruby
# ruby script
BuildArch: noarch

%description -n %{shortname}-convbkmk
The package provides a small Ruby script that corrects
bookmarks in PDF files created by platex/uplatex, using
hyperref.

%package -n %{shortname}-crossrefware
Version: svn76407
Provides: texlive-crossrefware = %{epoch}:%{source_date}-%{release}
Provides: tex-crossrefware = %{epoch}:%{source_date}-%{release}
Provides: texlive-crossrefware-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-crossrefware-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-crossrefware-bin < 7:20170520
Provides: tex-crossrefware-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-crossrefware-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-crossrefware-doc < 7:20170520
License: GPL-1.0-or-later
Summary: Scripts for working with crossref.org
# Just perl.
BuildArch: noarch

%description -n %{shortname}-crossrefware
This bundle contains the following scripts: bibdoiadd.pl: add
DOI numbers to papers in a given bib file, bibzbladd.pl: add
Zbl numbers to papers in a given bib file, ltx2crossrefxml.pl:
a tool for the creation of XML files for submitting to the
parent site

%package -n %{shortname}-cslatex
Version: svn67494
Provides: texlive-cslatex = %{epoch}:%{source_date}-%{release}
Provides: tex-cslatex = %{epoch}:%{source_date}-%{release}
Provides: texlive-cslatex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-cslatex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cslatex-bin < 7:20170520
License: GPL-1.0-or-later
Summary: LaTeX support for Czech/Slovak typesetting
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(atbegshi.sty)
Requires: tex(atveryend.sty)
Requires: texlive-cm
Requires: texlive-csplain
Requires: tex(everyshi.sty)
Requires: texlive-firstaid
Requires: texlive-hyphen-base
Requires: texlive-l3kernel
Requires: texlive-l3packages
Requires: texlive-latex
Requires: texlive-latex-fonts
Requires: texlive-tex-ini-files
Requires: texlive-unicode-data
Requires(post,postun): coreutils
Requires: tex(czech.ldf)
Requires: tex(slovak.ldf)
# symlinks
BuildArch: noarch

%description -n %{shortname}-cslatex
LaTeX support for Czech/Slovak typesetting

%package -n %{shortname}-csplain
Summary: Plain TeX multilanguage support
Version: svn76924
Provides: texlive-csplain = %{epoch}:%{source_date}-%{release}
Provides: tex-csplain = %{epoch}:%{source_date}-%{release}
Provides: texlive-csplain-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-csplain-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-csplain-bin < 7:20170520
License: GPL-2.0-or-later
# symlinks
BuildArch: noarch
Requires(post,postun): coreutils
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-cs
Requires: texlive-enctex
Requires: texlive-hyph-utf8
Requires: texlive-hyphen-base
Requires: texlive-kpathsea
Requires: texlive-luatex
Requires: texlive-luatex85
Requires: texlive-pdftex
Requires: texlive-plain
Requires: texlive-tex
Requires: texlive-tex-ini-files
Requires: texlive-xetex

%description -n %{shortname}-csplain
CSplain is a small extension of basic Plain TeX macros, the formats csplain and
pdfcsplain can be generated. It supports: hyphenation of words for 50+
languages, simple and powerful font loading system (various sizes of fonts),
TeX, pdfTeX, XeTeX and LuaTeX engines, math fonts simply loaded with full
amstex-like features, three internal encodings (IL2 for Czech/Slovak languages,
T1 for many languages with latin alphabet and Unicode in new TeX engines),
natural UTF-8 input in pdfTeX using encTeX without any active characters, Czech
and Slovak special typesetting features. An important part of the package is
OPmac, which implements most of LaTeX's features (sectioning, font selection,
color, hyper reference and urls, bibliography, index, toc, tables,etc.) by
Plain TeX macros. The OPmac macros can generate and bibliography without any
external program.

%package -n %{shortname}-ctan-o-mat
Version: svn51578
Provides: texlive-ctan-o-mat = %{epoch}:%{source_date}-%{release}
Provides: tex-ctan-o-mat = %{epoch}:%{source_date}-%{release}
Provides: texlive-ctan-o-mat-bin = %{epoch}:%{source_date}-%{release}
License: BSD-3-Clause
Summary: Upload or validate a package for CTAN
Requires: texlive-base
Requires: texlive-kpathsea
Requires: perl-interpreter
#perl
BuildArch: noarch

%description -n %{shortname}-ctan-o-mat
This program can be used to automate the upload of a package to
CTAN. The description of the package is contained in a
configuration file. The provided information is validated in
any case. If the validation succeeds and not only the
validation is requested, then the provided archive file will be
placed in the incoming area of the CTAN for further processing
by the CTAN team. In any case any finding during the validation
is reported at the end of the processing. Note that the
validation is the default and an official submission has to be
requested by an appropriate command line option. ctan-o-mat
requires an Internet connection to the CTAN server. Even the
validation retrieves the known attributes and the basic
constraints from the server.

%package -n %{shortname}-ctanbib
Version: svn68650
Provides: texlive-ctanbib = %{epoch}:%{source_date}-%{release}
Provides: tex-ctanbib = %{epoch}:%{source_date}-%{release}
Provides: texlive-ctanbib-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-ctanbib-bin = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
Summary: Export ctan entries to bib format
Requires: texlive-base
Requires: texlive-kpathsea
#lua
BuildArch: noarch

%description -n %{shortname}-ctanbib
This script can generate BibTeX records for LaTeX packages hosted on CTAN.

%package -n %{shortname}-ctanify
Version: svn44129
Provides: texlive-ctanify = %{epoch}:%{source_date}-%{release}
Provides: tex-ctanify = %{epoch}:%{source_date}-%{release}
Provides: texlive-ctanify-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-ctanify-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ctanify-bin < 7:20170520
Provides: tex-ctanify-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ctanify-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ctanify-doc < 7:20170520
License: LPPL-1.3c
Summary: Prepare a package for upload to CTAN
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-ctanify
Given a list of filenames, ctanify creates a tarball (a .tar.gz
file) with the files laid out in CTAN's preferred structure.
The tarball additionally contains a ZIP (.zip) file with copies
of all files laid out in the standard TeX Directory Structure
(TDS), which may be used by those intending to install the
package, or by those who need to incorporate it in a
distribution. (The TDS ZIP file will be installed in the CTAN
install/ tree.)

%package -n %{shortname}-ctanupload
Version: svn26313
Provides: texlive-ctanupload = %{epoch}:%{source_date}-%{release}
Provides: tex-ctanupload = %{epoch}:%{source_date}-%{release}
Provides: texlive-ctanupload-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-ctanupload-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ctanupload-bin < 7:20170520
Provides: tex-ctanupload-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ctanupload-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ctanupload-doc < 7:20170520
License: GPL-3.0-or-later
Summary: Support for users uploading to CTAN
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-ctanupload
The package provides a Perl script that allows the uploads of a
contribution to CTAN from the command line. The aim is to
simplify the release process for LaTeX package authors.

%package -n %{shortname}-ctie
Summary: C version of tie (merging Web change files)
Version: svn77830
Provides: texlive-ctie = %{epoch}:%{source_date}-%{release}
Provides: tex-ctie = %{epoch}:%{source_date}-%{release}
Provides: texlive-ctie-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-ctie-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ctie-bin < 7:20170520
License: GPL-1.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-ctie
This is a version of tie converted for use with cweb.

%package -n %{shortname}-cweb
Summary: CWEB for ANSI-C/C++ compilers
Version: svn77830
Provides: texlive-cweb = %{epoch}:%{source_date}-%{release}
Provides: tex-cweb = %{epoch}:%{source_date}-%{release}
Provides: texlive-cweb-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-cweb-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cweb-bin < 7:20170520
Provides: tex-cweb-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-cweb-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cweb-doc < 7:20170520
License: Knuth-CTAN
Requires: tex(iftex.sty)
Requires: texlive-base
Requires: texlive-iftex
Requires: texlive-kpathsea

%description -n %{shortname}-cweb
A highly portable and extended version of Levy/Knuth CWEB 3.64c for UNIX,
Windows, Mac (and possibly other operating systems). TeX macros, CWEB macros,
and NLS catalogs are included for German, French (partially), and Italian
program documentation on any machine. Major features: Thoroughly updated code
base; several bug fixes; clean compilation (with both C and TeX) on at least
four different architectures. Added CTWILL program with tools and utilities for
brave users; including introductory manpage. Internationalization of CTANGLE,
CWEAVE, and CTWILL with "GNU gettext utilities". New code base for CWEB in TeX
Live 2019, incorporating all features of the TL 2018 version and adding new
features from CWEBbin. As of November 2019 CTAN no longer holds a copy of this
material. Please go to the package's github repository for more information.

%package -n %{shortname}-cyrillic
Version: svn71408
Provides: texlive-cyrillic = %{epoch}:%{source_date}-%{release}
Provides: tex-cyrillic = %{epoch}:%{source_date}-%{release}
Provides: texlive-cyrillic-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-cyrillic-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cyrillic-bin < 7:20170520
Provides: tex-cyrillic-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-cyrillic-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cyrillic-doc < 7:20170520
Provides: texlive-cyrillic-bin-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-cyrillic-bin-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-cyrillic-bin-bin < 7:20170520
License: LPPL-1.3c
Summary: Support for Cyrillic fonts in LaTeX
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(fontenc.sty)
# shell
BuildArch: noarch

%description -n %{shortname}-cyrillic
This bundle of macros files provides macro support (including
font encoding macros) for the use of Cyrillic characters in
fonts encoded under the T2* and X2 encodings. These encodings
cover (between them) pretty much every language that is written
in a Cyrillic alphabet.

%package -n %{shortname}-de-macro
Version: svn66746
Provides: texlive-de-macro = %{epoch}:%{source_date}-%{release}
Provides: tex-de-macro = %{epoch}:%{source_date}-%{release}
Provides: texlive-de-macro-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-de-macro-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-de-macro-bin < 7:20170520
Provides: tex-de-macro-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-de-macro-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-de-macro-doc < 7:20170520
License: AFL-2.1
Summary: Expand private macros in a document
Requires: texlive-base
Requires: texlive-kpathsea
# python
BuildArch: noarch

%description -n %{shortname}-de-macro
De-macro is a Python script that helps authors who like to use
private LaTeX macros (for example, as abbreviations). A
technical editor or a cooperating author may balk at such a
manuscript; you can avoid manuscript rejection misery by
running de-macro on it. De-macro will expand macros defined in
\(re)newcommand or \(re)newenvironment commands, within the
document, or in the document's "private" package file.

%package -n %{shortname}-detex
Version: svn70015
Provides: texlive-detex = %{epoch}:%{source_date}-%{release}
Provides: tex-detex = %{epoch}:%{source_date}-%{release}
Provides: texlive-detex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-detex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-detex-bin < 7:20170520
License: NCSA
Summary: Strip TeX from a source file
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-detex
Detex is a program to remove TeX constructs from a text file.
It recognizes the \input command. The program assumes it is
dealing with LaTeX input if it sees the string \begin{document}
in the text. In this case, it also recognizes the \include and
\includeonly commands. The author now considers this program to
be "retired" and Piotr Kubowicz's OpenDetex as its successor.

%package -n %{shortname}-diadia
Version: svn37656
Provides: texlive-diadia = %{epoch}:%{source_date}-%{release}
Provides: tex-diadia = %{epoch}:%{source_date}-%{release}
Provides: texlive-diadia-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-diadia-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-diadia-bin < 7:20170520
Provides: tex-diadia-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-diadia-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-diadia-doc < 7:20170520
License: LPPL-1.3c
Summary: Package to keep a diabetes diary
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(xkeyval.sty)
Requires: tex(pgfplots.sty)
Requires: tex(pgfplotstable.sty)
Requires: tex(pgfcalendar.sty)
Requires: tex(tabularx.sty)
Requires: tex(booktabs.sty)
Requires: tex(colortbl.sty)
Requires: tex(ifthen.sty)
Requires: tex(calc.sty)
Requires: tex(translations.sty)
Requires: tex(amsmath.sty)
Requires: tex(tcolorbox.sty)
Requires: tex(environ.sty)
Requires: tex(multicol.sty)
Requires: tex(amssymb.sty)
# lua
BuildArch: noarch

%description -n %{shortname}-diadia
The diadia package allows you to keep a diabetes diary.
Usually, this means keeping record of certain medical values
like blood sugar, blood pressure, pulse or weight. It might
also include other medical, pharmaceutical or nutritional data
(HbA1c, insulin doses, carbohydrate units). The diadia package
supports all of this plus more - simply by adding more columns
to the data file! It is able to evaluate the data file and
typesets formatted tables and derived plots. Furthermore, it
supports medication charts and info boxes. Supported languages:
English, German. Feel free to provide other translation files!

%package -n %{shortname}-digestif
Summary: Editor plugin for LaTeX, ConTeXt etc.
Version: svn72163
License: GPL-3.0-or-later AND LPPL-1.3c AND GFDL-1.3-no-invariants-or-later
Requires: texlive-base texlive-kpathsea
# lua
BuildArch: noarch

%description -n %{shortname}-digestif
Digestif is a code analyzer, and a language server, for LaTeX,
plain TeX, ConTeXt and Texinfo. It provides context-sensitive
completion, documentation, code navigation, and related
functionality to any text editor that speaks the LSP protocol.

%package -n %{shortname}-dosepsbin
Version: svn29752
Provides: texlive-dosepsbin = %{epoch}:%{source_date}-%{release}
Provides: tex-dosepsbin = %{epoch}:%{source_date}-%{release}
Provides: texlive-dosepsbin-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dosepsbin-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dosepsbin-bin < 7:20170520
Provides: tex-dosepsbin-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-dosepsbin-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dosepsbin-doc < 7:20170520
License: GPL-2.0-only
Summary: Deal with DOS binary EPS files
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-dosepsbin
A Encapsulated PostScript (EPS) file may given in a special
binary format to support the inclusion of a thumbnail. This
file format, commonly known as DOS EPS format starts with a
binary header that contains the positions of the possible
sections: Postscript (PS); Windows Metafile Format (WMF); and
Tag Image File Format (TIFF). The PS section must be present
and either the WMF file or the TIFF file should be given. The
package provides a Perl program that will extract any of the
sections of such a file, in particular providing a 'text'-form
EPS file for use with (La)TeX.

%package -n %{shortname}-dtl
Version: svn62387
Provides: texlive-dtl = %{epoch}:%{source_date}-%{release}
Provides: tex-dtl = %{epoch}:%{source_date}-%{release}
Provides: texlive-dtl-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dtl-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dtl-bin < 7:20170520
License: LicenseRef-Fedora-Public-Domain
Summary: Tools to dis-assemble and re-assemble DVI files
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dtl
DTL (DVI Text Language) is a means of expressing the content of
a DVI file, which is readily readable by humans. The DTL bundle
contains an assembler dt2dv (which produces DVI files from DTL
files) and a disassembler dv2dt (which produces DTL files from
DVI files). The DTL bundle was developed so as to avoid some
infelicities of dvitype (among other pressing reasons).

%package -n %{shortname}-dtxgen
Summary: Creates a template for a self-extracting .dtx file
Version: svn75946
Provides: texlive-dtxgen = %{epoch}:%{source_date}-%{release}
Provides: tex-dtxgen = %{epoch}:%{source_date}-%{release}
Provides: texlive-dtxgen-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dtxgen-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dtxgen-bin < 7:20170520
Provides: tex-dtxgen-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-dtxgen-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dtxgen-doc < 7:20170520
License: GPL-1.0-or-later
# bash
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dtxgen
The bash script dtxgen creates a template for a self-extracting .dtx file. It
is useful for those who plan to create a new Documented LaTeX Source (.dtx)
file.

%package -n %{shortname}-dvi2tty
Version: svn66186
Provides: texlive-dvi2tty = %{epoch}:%{source_date}-%{release}
Provides: tex-dvi2tty = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvi2tty-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dvi2tty-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvi2tty-bin < 7:20170520
License: GPL-1.0-or-later
Summary: Produce ASCII from DVI
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dvi2tty
A DVI driver to produce an ASCII representation of the
document. The original version was written in Pascal, and the
present author translated the program to C.

%package -n %{shortname}-dviasm
Version: svn71902
Provides: texlive-dviasm = %{epoch}:%{source_date}-%{release}
Provides: tex-dviasm = %{epoch}:%{source_date}-%{release}
Provides: texlive-dviasm-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dviasm-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dviasm-bin < 7:20170520
Provides: tex-dviasm-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-dviasm-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dviasm-doc < 7:20170520
License: GPL-3.0-or-later
Summary: A utility for editing DVI files
Requires: texlive-base
Requires: texlive-kpathsea
# python
BuildArch: noarch

%description -n %{shortname}-dviasm
A Python script to support changing or creating DVI files via
disassembling into text, editing, and then reassembling into
binary format. It supports advanced features such as adding a
preprint number or watermarks.

%package -n %{shortname}-dvicopy
Summary: Copy DVI files while expanding VF (virtual font) references
Version: svn77830
Provides: texlive-dvicopy = %{epoch}:%{source_date}-%{release}
Provides: tex-dvicopy = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvicopy-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dvicopy-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvicopy-bin < 7:20170520
License: GPL-1.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dvicopy
DVIcopy is a utility program that allows one to convert a DVI file that
references composite fonts (VF) into an equivalent DVI file that does not
contain such references. It also serves as a basis for writing DVI drivers
(much like DVItype). The ODVIcopy variant does the same job for Omega/Aleph's
output, modified to support their .ofm font format.

%package -n %{shortname}-dvidvi
Summary: Convert one DVI file into another
Version: svn75712
Provides: texlive-dvidvi = %{epoch}:%{source_date}-%{release}
Provides: tex-dvidvi = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvidvi-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dvidvi-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvidvi-bin < 7:20170520
License: LicenseRef-Fedora-UltraPermissive
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dvidvi
The output DVI file's contents are specified by page selection commands; series
of pages and page number ranges may be specified, as well as inclusions and
exclusions. It is now maintained as part of TeX Live.

%package -n %{shortname}-dviinfox
Version: svn59216
Provides: texlive-dviinfox = %{epoch}:%{source_date}-%{release}
Provides: tex-dviinfox = %{epoch}:%{source_date}-%{release}
Provides: texlive-dviinfox-bin = %{epoch}:%{source_date}-%{release}
License: MIT
Summary: Perl script to print DVI meta information
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea
Requires: perl-interpreter

%description -n %{shortname}-dviinfox
The package provides a perl script which prints information
about a DVI file. It also supports XeTeX XDV format.

%package -n %{shortname}-dviljk
Version: svn66186
Provides: texlive-dviljk = %{epoch}:%{source_date}-%{release}
Provides: tex-dviljk = %{epoch}:%{source_date}-%{release}
Provides: texlive-dviljk-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dviljk-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dviljk-bin < 7:20170520
License: GPL-1.0-or-later
Summary: DVI to Laserjet output
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dviljk
A dvi driver for the LaserJet printers, using kpathsea
recursive file searching.

%package -n %{shortname}-dviout-util
Version: svn66186
Provides: texlive-dviout-util = %{epoch}:%{source_date}-%{release}
Provides: tex-dviout-util = %{epoch}:%{source_date}-%{release}
Provides: texlive-dviout-util-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dviout-util-bin = %{epoch}:%{source_date}-%{release}
License: MIT
Summary: DVI output utilities
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dviout-util
This is a partial repackaging of elements of the DVIOUT package
by Toshio OSHIMA, Yoshiki OTOBE, and Kazunori ASAYAMA.
Here we don't include the main DVI previewer, but just want small utility
programs.

%package -n %{shortname}-dvipdfmx
Summary: An extended version of dvipdfm
Version: svn77942
Provides: texlive-dvipdfmx = %{epoch}:%{source_date}-%{release}
Provides: tex-dvipdfmx = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvipdfmx-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dvipdfmx-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvipdfmx-bin < 7:20170520
Provides: tex-dvipdfmx-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvipdfmx-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvipdfmx-doc < 7:20170520
Provides: dvipdfmx = %{epoch}:%{source_date}-%{release}
Provides: dvipdfm = %{epoch}:%{source_date}-%{release}
License: GPL-2.0-or-later
Requires: texlive-base
Requires: texlive-extractbb
Requires: texlive-glyphlist
Requires: texlive-kpathsea
Requires: texlive-texlive-scripts-extra
Requires: texlive-xetex

%description -n %{shortname}-dvipdfmx
Dvipdfmx (formerly dvipdfm-cjk) is a development of dvipdfm created to support
multi-byte character encodings and large character sets for East Asian
languages. Dvipdfmx, if "called" with the name dvipdfm, operates in a "dvipdfm
compatibility" mode, so that users of the both packages need only keep one
executable. A secondary design goal is to support as many "PDF" features as
does pdfTeX. The current version of the package is no longer maintained on CTAN
as a separate entity; development now takes place within the TeX Live
framework, and it is no longer available as a separate package. For download,
support, and other information, please see TeX Live. However, the information
on this page is maintained and should be current.

%package -n %{shortname}-dvipng
Summary: A fast DVI to PNG/GIF converter
Version: svn77830
Provides: texlive-dvipng = %{epoch}:%{source_date}-%{release}
Provides: tex-dvipng = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvipng-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dvipng-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvipng-bin < 7:20170520
Provides: tex-dvipng-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvipng-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvipng-doc < 7:20170520
Provides: dvipng = %{epoch}:%{source_date}-%{release}
License: LGPL-3.0-only
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dvipng
This program makes PNG and/or GIF graphics from DVI files as obtained from TeX
and its relatives. Its benefits include: Speed. It offers very fast rendering
of DVI as bitmap files, which makes it suitable for generating large amounts of
images on-the-fly, as needed in preview-latex, WeBWorK and others; It does not
read the postamble, so it can be started before TeX finishes. There is a
--follow switch that makes dvipng wait at end-of-file for further output,
unless it finds the POST marker that indicates the end of the DVI; Interactive
query of options. dvipng can read options interactively through stdin, and all
options are usable. It is even possible to change the input file through this
interface. Support for PK, VF, PostScript Type1, and TrueType fonts, colour
specials, and inclusion of PostScript, PNG, JPEG or GIF images.

%package -n %{shortname}-dvipos
Version: svn66186
Provides: texlive-dvipos = %{epoch}:%{source_date}-%{release}
Provides: tex-dvipos = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvipos-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dvipos-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvipos-bin < 7:20170520
License: LPPL-1.3c
Summary: support DVI pos: specials used by ConTeXt DVI output
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dvipos
support DVI pos: specials used by ConTeXt DVI output

%package -n %{shortname}-dvips
Summary: A DVI to PostScript driver
Version: svn77830
Provides: texlive-dvips = %{epoch}:%{source_date}-%{release}
Provides: tetex-dvips = %{epoch}:%{source_date}-%{release}
Provides: tex-dvips = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvips-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dvips-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvips-bin < 7:20170520
Provides: tex-dvips-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvips-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvips-doc < 7:20170520
License: GPL-1.0-or-later
# This is a special "tex()" Provides for the dvips binary.
# We do not do this for all binaries, just this one due to its
# broad need (and the fact that it has existed forever).
Provides: tex(dvips) = %{epoch}:%{source_date}-%{release}
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-latex-fonts

%description -n %{shortname}-dvips
This package has been withdrawn from CTAN, and bundled into the distributions'
package sets. Development now takes place within the TeX Live framework, and it
is no longer available as a separate package. For download, support, and other
information, please see TeX Live.

%package -n %{shortname}-dvisvgm
Summary: Convert DVI, EPS, and PDF files to Scalable Vector Graphics format (SVG)
Version: svn77830
Provides: texlive-dvisvgm = %{epoch}:%{source_date}-%{release}
Provides: tex-dvisvgm = %{epoch}:%{source_date}-%{release}
Provides: texlive-dvisvgm-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-dvisvgm-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-dvisvgm-bin < 7:20170520
License: GPL-3.0-or-later
# for mutool
Requires: mupdf
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-dvisvgm
Dvisvgm is a command line utility that converts TeX DVI as well as EPS and PDF
files to the XML-based Scalable Vector Graphics (SVG) format. It provides full
font support including virtual fonts, font maps, and sub-fonts. If necessary,
dvisvgm vectorizes Metafont's bitmap output in order to always create lossless
scalable output. The embedded SVG fonts can optionally be replaced with
graphics paths so that applications that do not support SVG fonts are enabled
to render the graphics properly. Besides many other features, dvisvgm also
supports color, emTeX, tpic, papersize, PDF mapfile and PostScript specials.
Users will need a working TeX installation including the kpathsea library. For
more detailed information, see the project page.

%package -n %{shortname}-easydtx
Version: svn72952
Provides: tex-easydtx = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
Summary: A simplified DTX format
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-easydtx
EasyDTX is a variant of the DTX format which eliminates the
need for all those pesky "macrocode" environments. Any line
introduced by a single comment counts as documentation, and
documentation lines may be indented. An .edtx file is converted
to a .dtx by a little Perl script called edtx2dtx. There is
also a rudimentary Emacs mode, implemented in
easydoctex-mode.el, which takes care of fontification,
indentation, and forward and inverse search.

%package -n %{shortname}-ebong
Summary: Utility for writing Bengali in Rapid Roman Format
Version: svn76924
Provides: texlive-ebong = %{epoch}:%{source_date}-%{release}
Provides: tex-ebong = %{epoch}:%{source_date}-%{release}
Provides: texlive-ebong-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-ebong-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ebong-bin < 7:20170520
Provides: tex-ebong-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ebong-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ebong-doc < 7:20170520
License: LicenseRef-Fedora-Public-Domain
# python
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-ebong
A tool (preprocessor) for writing your pRaa-ne-r ka-thaa in the Bengali
language. It allows one to write the text in Rapid Roman Bangla and convert it
to the bangtex format by a python program. All LaTeX markups are preserved in
the target file.

%package -n %{shortname}-eolang
Summary: Formulas and graphs for the EO programming language
Version: svn77164
Provides: tex-eolang = %{epoch}:%{source_date}-%{release}
License: MIT
# perl
BuildArch: noarch
Requires: texlive-adjustbox
Requires: texlive-amsfonts
Requires: texlive-amsmath
Requires: texlive-base
Requires: texlive-everyshi
Requires: texlive-fancyvrb
Requires: texlive-hyperref
Requires: texlive-iexec
Requires: texlive-kpathsea
Requires: texlive-pdftexcmds
Requires: texlive-pgf
Requires: texlive-pgfopts
Requires: texlive-stmaryrd
Requires: texlive-xstring

%description -n %{shortname}-eolang
This package helps you format expressions of [?] -calculus and draw SODG graphs
the EO programming language.

%package -n %{shortname}-eplain
Version: svn71409
Provides: texlive-eplain = %{epoch}:%{source_date}-%{release}
Provides: tex-eplain = %{epoch}:%{source_date}-%{release}
Provides: texlive-eplain-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-eplain-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-eplain-bin < 7:20170520
Provides: tex-eplain-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-eplain-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-eplain-doc < 7:20170520
License: GPL-2.0-or-later
Summary: Extended plain TeX macros
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-pdftex
Requires: texlive-babel
Requires: texlive-cm
Requires: texlive-hyphen-base
Requires: texlive-latex-fonts
Requires: texlive-l3backend
Requires: texlive-l3kernel
Requires: texlive-l3packages
Requires: texlive-tex-ini-files
Requires: texlive-unicode-data
Requires: texlive-dehyph
Requires: texlive-hyph-utf8
Requires: texlive-knuth-lib
Requires(post,postun): coreutils
# No actual binaries in here
BuildArch: noarch

%description -n %{shortname}-eplain
An extended version of the plain TeX format, adding support for
bibliographies, tables of contents, enumerated lists, verbatim
input of files, numbered equations, tables, two-column output,
footnotes, hyperlinks in PDF output and commutative diagrams.
Eplain can also load some of the more useful LaTeX packages,
notably graphics, graphicx (an extended of version of
graphics), color, autopict (a package instance of the LaTeX
picture code), psfrag, and url.

%package -n %{shortname}-epspdf
Version: svn74487
Provides: texlive-epspdf = %{epoch}:%{source_date}-%{release}
Provides: tex-epspdf = %{epoch}:%{source_date}-%{release}
Provides: texlive-epspdf-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-epspdf-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-epspdf-bin < 7:20170520
Provides: tex-epspdf-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-epspdf-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-epspdf-doc < 7:20170520
License: GPL-1.0-or-later
Summary: Converter for PostScript, EPS and PDF
Requires: texlive-base
Requires: texlive-kpathsea
# tcl and lua
BuildArch: noarch

%description -n %{shortname}-epspdf
Epspdftk.tcl is a GUI ps/eps/pdf converter. Epspdf.tlu, its
command-line backend, can be used by itself. Options include
grayscaling, cropping margins and single-page selection. Some
conversion options are made possible by converting in multiple
steps.

%package -n %{shortname}-epstopdf
Version: svn71782
Provides: texlive-epstopdf = %{epoch}:%{source_date}-%{release}
Provides: tex-epstopdf = %{epoch}:%{source_date}-%{release}
Provides: texlive-epstopdf-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-epstopdf-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-epstopdf-bin < 7:20170520
Provides: tex-epstopdf-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-epstopdf-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-epstopdf-doc < 7:20170520
License: BSD-3-Clause
Summary: Convert EPS to 'encapsulated' PDF using Ghostscript
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-epstopdf
Epstopdf is a Perl script that converts an EPS file to an
'encapsulated' PDF file (a single page file whose media box is
the same as the original EPS's bounding box). The resulting
file suitable for inclusion by PDFTeX as an image. The script
is adapted to run both on Windows and on Unix-alike systems.
The script makes use of Ghostscript for the actual conversion
to PDF. It assumes Ghostscript version 6.51 or later, and (by
default) suppresses its automatic rotation of pages where most
of the text is not horizontal. LaTeX users may make use of the
epstopdf package, which will run the epstopdf script "on the
fly", thus giving the illusion that PDFLaTeX is accepting EPS
graphic files.

%package -n %{shortname}-exceltex
Summary: Get data from Excel files into LaTeX
Version: svn76924
Provides: texlive-exceltex = %{epoch}:%{source_date}-%{release}
Provides: tex-exceltex = %{epoch}:%{source_date}-%{release}
Provides: texlive-exceltex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-exceltex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-exceltex-bin < 7:20170520
Provides: tex-exceltex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-exceltex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-exceltex-doc < 7:20170520
License: GPL-2.0-or-later
# perl
BuildArch: noarch
Requires: perl(Spreadsheet::ParseExcel)
Requires: tex(color.sty)
Requires: tex(ulem.sty)
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-exceltex
Exceltex is a LaTeX package combined with a helper program written in Perl. It
provides an easy to use yet powerful and flexible way to get data from
Spreadsheets into LaTeX. In contrast to other solutions, exceltex does not seek
to make the creation of tables in LaTeX easier, but to get data from
Spreadsheets into LaTeX as easily as possible. The Excel (TM) file format only
acts as an interface between the spreadsheet application and exceltex because
it is easily accessible (via the Spreadsheet::ParseExcel Perl module) and
because most spreadsheet applications are able to read and write Excel files.

%package -n %{shortname}-expltools
Summary: Development tools for expl3 programmers
Version: svn78336
Provides: tex-expltools = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c AND GPL-2.0-or-later
# lua
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-expltools
This bundle introduces explcheck, a static analysis tool for developers working
with expl3 code. Currently in its initial release, explcheck aims to help
developers identify potential issues and improve code quality. In the future,
this bundle may expand to include additional development tools for expl3.

%package -n %{shortname}-extractbb
Summary: A reimplementation of extractbb, written in Lua
Version: svn77855
Provides: tex-extractbb = %{epoch}:%{source_date}-%{release}
License: CC-BY-SA-4.0
# lua
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-extractbb
extractbb is a program that exports the dimensions of an image or PDF file to a
plain text format that is easily parsed by TeX. This tool is rarely run
directly by users, but is frequently used by packages running on XeTeX or
upTeX. This package specifically contains a Lua-based reimplementation
extractbb that behaves identically to the original C-based version distributed
with dvipdfmx.

%package -n %{shortname}-fig4latex
Version: svn26313
Provides: texlive-fig4latex = %{epoch}:%{source_date}-%{release}
Provides: tex-fig4latex = %{epoch}:%{source_date}-%{release}
Provides: texlive-fig4latex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-fig4latex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-fig4latex-bin < 7:20170520
Provides: tex-fig4latex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-fig4latex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-fig4latex-doc < 7:20170520
License: GPL-3.0-or-later
Summary: Management of figures for large LaTeX documents
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-fig4latex
Fig4LaTeX simplifies management of the figures in a large LaTeX
document. Fig4LaTeX is appropriate for projects that include
figures with graphics created by XFig -- in particular,
graphics which use the combined PS/LaTeX (or PDF/LaTeX) export
method. An example document (with its output) is provided.

%package -n %{shortname}-findhyph
Version: svn47444
Provides: texlive-findhyph = %{epoch}:%{source_date}-%{release}
Provides: tex-findhyph = %{epoch}:%{source_date}-%{release}
Provides: texlive-findhyph-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-findhyph-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-findhyph-bin < 7:20170520
Provides: tex-findhyph-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-findhyph-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-findhyph-doc < 7:20170520
License: GPL-1.0-or-later
Summary: Find hyphenated words in a document
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-findhyph
Findhyph is a Perl script that will analyse the log file from
running your document with \tracingparagraphs=1 set. The output
contains enough context to enable you to find the hyphenated
word that's being referenced.

%package -n %{shortname}-fontinst
Version: svn74240
Provides: texlive-fontinst = %{epoch}:%{source_date}-%{release}
Provides: tex-fontinst = %{epoch}:%{source_date}-%{release}
Provides: texlive-fontinst-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-fontinst-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-fontinst-bin < 7:20170520
Provides: tex-fontinst-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-fontinst-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-fontinst-doc < 7:20170520
License: LPPL-1.3c
Summary: Help with installing fonts for TeX and LaTeX
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(color.sty)
Requires: tex(amstext.sty)
# shell
BuildArch: noarch

%description -n %{shortname}-fontinst
TeX macros for converting Adobe Font Metric files to TeX metric
and virtual font format. Fontinst helps mainly with the number
crunching and shovelling parts of font installation. This means
in practice that it creates a number of files which give the
TeX metrics (and related information) for a font family that
(La)TeX needs to do any typesetting in these fonts. Fontinst
furthermore makes it easy to create fonts containing glyphs
from more than one base font, taking advantage of (e.g.)
"expert" font sets. Fontinst cannot examine files to see if
they contain any useful information, nor automatically search
for files or work with binary file formats; those tasks must
normally be done manually or with the help of some other tool,
such as the pltotf and vptovf programs.

%package -n %{shortname}-fontools
Summary: Tools to simplify using fonts (especially TT/OTF ones)
Version: svn78330
Provides: texlive-fontools = %{epoch}:%{source_date}-%{release}
Provides: tex-fontools = %{epoch}:%{source_date}-%{release}
Provides: texlive-fontools-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-fontools-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-fontools-bin < 7:20170520
Provides: tex-fontools-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-fontools-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-fontools-doc < 7:20170520
License: GPL-2.0-or-later
# perl
BuildArch: noarch
Requires: texlive-base
# For vptovf
Requires: texlive-fontware
Requires: texlive-kpathsea
# for otfinfo
Requires: texlive-lcdftypetools

%description -n %{shortname}-fontools
This package provides tools to simplify using OpenType fonts with LaTeX. By far
the most important program in this bundle is autoinst: autoinst - a wrapper
script around Eddie Kohler's LCDF TypeTools. Autoinst aims to automate the
installation of OpenType fonts in LaTeX by calling the LCDF TypeTools (with the
correct options) for all fonts you wish to install, and generating the
necessary .fd and .sty files. In addition, this bundle contains a few other,
less important utilities: afm2afm - re-encode .afm files, ot2kpx - extract
kerning pairs from OpenType fonts, splitttc - split an OpenType Collection file
(ttc or otc) into individual fonts.

%package -n %{shortname}-fontware
Summary: Tools for virtual font metrics
Version: svn77830
Provides: texlive-fontware = %{epoch}:%{source_date}-%{release}
Provides: tex-fontware = %{epoch}:%{source_date}-%{release}
Provides: texlive-fontware-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-fontware-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-fontware-bin < 7:20170520
License: Knuth-CTAN
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-fontware
Virtual font metrics are usually created in a textual form, the Virtual
Property List, but programs that use them need to use binary files (the Virtual
Font and the TeX Font Metric). The present two programs translate between the
two forms: - vptovf takes a VPL file and generates a VF file and a TFM file; -
vftovp takes a VF file and a TFM file and generates a VPL file. The programs
are to be found in every distribution of TeX.

%package -n %{shortname}-fragmaster
Version: svn26313
Provides: texlive-fragmaster = %{epoch}:%{source_date}-%{release}
Provides: tex-fragmaster = %{epoch}:%{source_date}-%{release}
Provides: texlive-fragmaster-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-fragmaster-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-fragmaster-bin < 7:20170520
Provides: tex-fragmaster-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-fragmaster-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-fragmaster-doc < 7:20170520
License: GPL-1.0-or-later
Summary: Using psfrag with PDFLaTeX
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-fragmaster
Fragmaster enables you to use psfrag with PDFLaTeX. It takes
EPS files and psfrag substitution definition files, and
produces PDF and EPS files with the substitutions included.

%package -n %{shortname}-getmap
Version: svn75447
Provides: texlive-getmap = %{epoch}:%{source_date}-%{release}
Provides: tex-getmap = %{epoch}:%{source_date}-%{release}
Provides: texlive-getmap-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-getmap-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-getmap-bin < 7:20170520
Provides: tex-getmap-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-getmap-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-getmap-doc < 7:20170520
License: LPPL-1.3c
Summary: Download OpenStreetMap maps for use in documents
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(xkeyval.sty)
Requires: tex(stringenc.sty)
Requires: tex(ifthen.sty)
# lua and shell
BuildArch: noarch

%description -n %{shortname}-getmap
The package provides a simple interface to OpenStreetMap, and
to Google Maps "map images". In the simplest case, it is
sufficient to specify the address you need (if you don't, the
package will use its own default). The package loads the map
image using an external lua script (invoked via \write 18:
LaTeX must be running with \write 18 enabled). The ("external")
lua script may be used from the command line; a bash version is
provided.

%package -n %{shortname}-git-latexdiff
Version: svn75878
Provides: texlive-git-latexdiff = %{epoch}:%{source_date}-%{release}
Summary: Call latexdiff on two Git revisions of a file
License: BSD-3-Clause
Requires: texlive-base texlive-kpathsea
Requires: git, texlive-latexdiff
# shell
BuildArch: noarch

%description -n %{shortname}-git-latexdiff
git-latexdiff is a tool to graphically visualize differences
between different versions of a LaTeX file. Technically, it is
a wrapper around git and latexdiff.

%package -n %{shortname}-glossaries
Summary: Create glossaries and lists of acronyms
Version: svn78288
Provides: texlive-glossaries = %{epoch}:%{source_date}-%{release}
Provides: tex-glossaries = %{epoch}:%{source_date}-%{release}
Provides: texlive-glossaries-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-glossaries-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-glossaries-bin < 7:20170520
Provides: tex-glossaries-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-glossaries-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-glossaries-doc < 7:20170520
License: LPPL-1.3c
# perl and lua
BuildArch: noarch
Requires: tex(accsupp.sty)
Requires: tex(amsgen.sty)
Requires: tex(array.sty)
Requires: tex(booktabs.sty)
Requires: tex(ifthen.sty)
Requires: tex(longtable.sty)
Requires: tex(multicol.sty)
Requires: tex(shellesc.sty)
Requires: tex(supertabular.sty)
Requires: tex(textcase.sty)
Requires: tex(translator.sty)
Requires: texlive-amsmath
Requires: texlive-base
Requires: texlive-datatool
Requires: texlive-etoolbox
Requires: texlive-kpathsea
Requires: texlive-mfirstuc
Requires: texlive-tracklang
Requires: texlive-xfor
Requires: texlive-xkeyval

%description -n %{shortname}-glossaries
The glossaries package supports acronyms and multiple glossaries, and has
provision for operation in several languages (using the facilities of either
babel or polyglossia). New entries are defined to have a name and description
(and optionally an associated symbol). Support for multiple languages is
offered, and plural forms of terms may be specified. An additional package,
glossaries-accsupp, can make use of the accsupp package mechanisms for
accessibility support for PDF files containing glossaries. The user may define
new glossary styles, and preambles and postambles can be specified. There is
provision for loading a database of terms, but only terms used in the text will
be added to the relevant glossary. The package uses an indexing program to
provide the actual glossary; either makeindex or xindy may serve this purpose,
and a Perl script is provided to serve as interface. This package requires the
mfirstuc package. The package supersedes the author's glossary package (which
is now obsolete).

%package -n %{shortname}-glyphlist
Version: svn54074
Provides: texlive-glyphlist = %{epoch}:%{source_date}-%{release}
Provides: tex-glyphlist = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
Summary: glyphlist package
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-glyphlist
glyphlist package.

%package -n %{shortname}-gregoriotex
Version: svn74348
Provides: texlive-gregoriotex = %{epoch}:%{source_date}-%{release}
Provides: tex-gregoriotex = %{epoch}:%{source_date}-%{release}
Provides: texlive-gregoriotex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-gregoriotex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-gregoriotex-bin < 7:20170520
Provides: tex-gregoriotex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-gregoriotex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-gregoriotex-doc < 7:20170520
License: GPL-3.0-only
Summary: Engraving Gregorian Chant scores
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(graphicx.sty)
Requires: tex(iftex.sty)
Requires: tex(kvoptions.sty)
Requires: tex(luacolor.sty)
Requires: tex(luamplib.sty)
Requires: tex(luaotfload.sty)
Requires: tex(luatexbase.sty)
Requires: tex(xcolor.sty)
Requires: tex(xstring.sty)

%description -n %{shortname}-gregoriotex
Gregorio is a software application for engraving Gregorian
Chant scores on a computer. Gregorio's main job is to convert a
gabc file (simple text representation of a score) into a
GregorioTeX file, which makes TeX able to create a PDF of your
score.

%package -n %{shortname}-gsftopk
Version: svn52851
Provides: texlive-gsftopk = %{epoch}:%{source_date}-%{release}
Provides: tex-gsftopk = %{epoch}:%{source_date}-%{release}
Provides: texlive-gsftopk-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-gsftopk-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-gsftopk-bin < 7:20170520
License: GPL-1.0-or-later
Summary: Convert "ghostscript fonts" to PK files
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-gsftopk
Designed for use with xdvi and dvips this utility converts
Adobe Type 1 fonts to PK bitmap format. It should not
ordinarily be much used nowadays, since both its target
applications are now capable of dealing with Type 1 fonts,
direct.

%package -n %{shortname}-hitex
Summary: A TeX extension writing HINT output for on-screen reading
Version: svn77830
Provides: texlive-hitex = %{epoch}:%{source_date}-%{release}
Provides: texlive-hitex-bin = %{epoch}:%{source_date}-%{release}
License: MIT
Requires: texlive-atbegshi
Requires: texlive-atveryend
Requires: texlive-babel
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-etex
Requires: texlive-everyshi
Requires: texlive-firstaid
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-l3backend
Requires: texlive-l3kernel
Requires: texlive-l3packages
Requires: texlive-latex
Requires: texlive-latex-fonts
Requires: texlive-plain
Requires: texlive-tex-ini-files
Requires: texlive-unicode-data

%description -n %{shortname}-hitex
An extension of TeX which generates HINT output. The HINT file format is an
alternative to the DVI and PDF formats which was designed specifically for
on-screen reading of documents. Especially on mobile devices, reading DVI or
PDF documents can be cumbersome. Mobile devices are available in a large
variety of sizes but typically are not large enough to display documents
formated for a4/letter-size paper. To compensate for the limitations of a small
screen, users are used to alternating between landscape (few long lines) and
portrait (more short lines) mode. The HINT format supports variable and varying
screen sizes, leveraging the ability of TeX to format a document for
nearly-arbitrary values of \hsize and \vsize.

%package -n %{shortname}-hyperxmp
Summary: Embed XMP metadata within a LaTeX document
Version: svn78281
Provides: texlive-hyperxmp = %{epoch}:%{source_date}-%{release}
Provides: texlive-hyperxmp-doc = %{epoch}:%{source_date}-%{release}
Provides: tex-hyperxmp-doc = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
Requires: tex(atenddvi.sty)
Requires: tex(etoolbox.sty)
Requires: tex(hyperref.sty)
Requires: tex(ifdraft.sty)
Requires: tex(ifluatex.sty)
Requires: tex(ifmtarg.sty)
Requires: tex(iftex.sty)
Requires: tex(ifthen.sty)
Requires: tex(intcalc.sty)
Requires: tex(kvoptions.sty)
Requires: tex(luacode.sty)
Requires: tex(pdfescape.sty)
Requires: tex(stringenc.sty)
Requires: tex(totpages.sty)
Requires: texlive-base
Requires: texlive-ifmtarg
Requires: texlive-kpathsea
Requires: texlive-oberdiek

%description -n %{shortname}-hyperxmp
XMP (eXtensible Metadata Platform) is a mechanism proposed by Adobe for
embedding document metadata within the document itself. The metadata is
designed to be easy to extract, even by programs that are oblivious to the
document's file format. Most of Adobe's applications store XMP metadata when
saving files. Now, with the hyperxmp package, it is trivial for LaTeX document
authors to store XMP metadata in their documents as well. The package
integrates seamlessly with hyperref and requires virtually no modifications to
documents that already exploit hyperref's mechanisms for specifying PDF
metadata. The current version of hyperxmp can embed the following metadata as
XMP: title, authors, primary author's title or position, metadata writer,
subject/summary, keywords, copyright, license URL, document base URL, document
identifier and instance identifier, language, source file name, PDF generating
tool, PDF version, and contact telephone number/postal address/email
address/URL. Hyperxmp currently embeds XMP only within PDF documents; it is
compatible with pdfLaTeX, XeLaTeX, LaTeX+dvipdfm, and LaTeX+dvips+ps2pdf.

%package -n %{shortname}-installfont
Version: svn31205
Provides: texlive-installfont = %{epoch}:%{source_date}-%{release}
Provides: tex-installfont = %{epoch}:%{source_date}-%{release}
Provides: texlive-installfont-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-installfont-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-installfont-bin < 7:20170520
Provides: tex-installfont-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-installfont-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-installfont-doc < 7:20170520
License: LPPL-1.3c
Summary: A bash script for installing a LaTeX font family
Requires: texlive-base
Requires: texlive-kpathsea
# shell
BuildArch: noarch

%description -n %{shortname}-installfont
With this script you can install a LaTeX font family
(PostScript Type 1, TrueType and OpenType formats are
supported). Font series from light to ultra bold, and (faked)
small caps and (faked) slanted shapes are supported, but not
expert fonts. The script will rename the fonts automatically
(optional) or will otherwise expect the *.afm files and the
font files (in PostScript Type1 format) named in the Karl Berry
scheme (e.g. 5bbr8a.pfb). After running the script, you should
have a working font installation in your local TeX tree.

%package -n %{shortname}-jadetex
Version: svn71409
Provides: texlive-jadetex = %{epoch}:%{source_date}-%{release}
Provides: tex-jadetex = %{epoch}:%{source_date}-%{release}
Provides: texlive-jadetex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-jadetex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-jadetex-bin < 7:20170520
Provides: tex-jadetex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-jadetex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-jadetex-doc < 7:20170520
Provides: jadetex = %{epoch}:%{source_date}-%{release}
License: MIT
Summary: Macros supporting Jade DSSSL output
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-latex
Requires: texlive-passivetex
Requires: texlive-pdftex
Requires: texlive-tex
Requires: texlive-amsfonts
Requires: texlive-atbegshi
Requires: texlive-atveryend
Requires: texlive-auxhook
Requires: texlive-babel
Requires: texlive-bigintcalc
Requires: texlive-bitset
Requires: texlive-cm
Requires: texlive-colortbl
Requires: texlive-cyrillic
Requires: texlive-dehyph
Requires: texlive-ec
Requires: texlive-etexcmds
Requires: texlive-fancyhdr
Requires: texlive-graphics
Requires: texlive-graphics-cfg
Requires: texlive-graphics-def
Requires: texlive-hycolor
Requires: texlive-hyperref
Requires: texlive-hyph-utf8
Requires: texlive-iftex
Requires: texlive-infwarerr
Requires: texlive-intcalc
Requires: texlive-kvdefinekeys
Requires: texlive-kvoptions
Requires: texlive-kvsetkeys
Requires: texlive-l3kernel
Requires: texlive-latex-fonts
Requires: texlive-latexconfig
Requires: texlive-letltxmacro
Requires: texlive-ltxcmds
Requires: texlive-marvosym
Requires: texlive-pdfescape
Requires: texlive-pdftexcmds
Requires: texlive-psnfss
Requires: texlive-rerunfilecheck
Requires: texlive-stmaryrd
Requires: texlive-symbol
Requires: texlive-tex-ini-files
Requires: texlive-tipa
Requires: texlive-tools
Requires: texlive-ulem
Requires: texlive-uniquecounter
Requires: texlive-unicode-data
Requires: texlive-url
Requires: texlive-wasysym
Requires: texlive-zapfding
Requires(post,postun): coreutils
# no binaries
BuildArch: noarch

%description -n %{shortname}-jadetex
Macro package on top of LaTeX to typeset TeX output of the Jade
DSSSL implementation.

%package -n %{shortname}-jfmutil
Version: svn60987
Provides: texlive-jfmutil = %{epoch}:%{source_date}-%{release}
Provides: tex-jfmutil = %{epoch}:%{source_date}-%{release}
Provides: texlive-jfmutil-bin = %{epoch}:%{source_date}-%{release}
License: MIT
Summary: Utility to process pTeX-extended TFM and VF
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-jfmutil
This program provides functionality to process data files (JFM
and VF) that form logical fonts used in (u)pTeX. The functions
currently available include: The mutual conversion between
Japanese virtual fonts (pairs of VF and JFM) and files in the
"ZVP format", which is an original text format representing
data in virtual fonts. This function can be seen as a
counterpart to the vftovp/vptovf programs. The mutual
conversion between VF files alone and files in the "ZVP0
format", which is a subset of the ZVP format.

%package -n %{shortname}-ketcindy
Version: svn58661
Provides: texlive-ketcindy = %{epoch}:%{source_date}-%{release}
Provides: tex-ketcindy = %{epoch}:%{source_date}-%{release}
Provides: tex-ketcindy-bin = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
Summary: Macros for graphic generation and Cinderella plugin
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-ketcindy
KETpic is a macro package designed for computer algebra systems
(CAS) to generate LaTeX source codes for high-quality
mathematical artwork. KETcindy is a plugin for Cinderella that
allows to generate graphics using KETpic. The generated code
can be included in any LaTeX document.

%package -n %{shortname}-kotex-utils
Version: svn38727
Provides: texlive-kotex-utils = %{epoch}:%{source_date}-%{release}
Provides: tex-kotex-utils = %{epoch}:%{source_date}-%{release}
Provides: texlive-kotex-utils-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-kotex-utils-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-kotex-utils-bin < 7:20170520
Provides: tex-kotex-utils-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-kotex-utils-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-kotex-utils-doc < 7:20170520
License: LPPL-1.3c
Summary: Utility scripts and support files for typesetting Korean
Requires: texlive-base
Requires: texlive-kotex-utf
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-kotex-utils
The bundle provides scripts and support files for index
generation in Korean language typesetting. The files belong to
the ko.TeX bundle.

%package -n %{shortname}-kpathsea
Summary: Path searching library for TeX-related files
Version: svn77861
Provides: texlive-kpathsea = %{epoch}:%{source_date}-%{release}
Provides: kpathsea = %{epoch}:%{source_date}-%{release}
Obsoletes: kpathsea < %{source_date}
Provides: tex-kpathsea = %{epoch}:%{source_date}-%{release}
Provides: texlive-kpathsea-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-kpathsea-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-kpathsea-bin < 7:20170520
Provides: tex-kpathsea-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-kpathsea-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-kpathsea-doc < 7:20170520
License: LGPL-2.1-or-later
# We absolutely need this to go in first, since the trigger needs it
Requires(post): texlive-texlive-scripts = %{epoch}:%{source_date}-%{release}
Requires: coreutils
Requires: grep
Requires: texlive-base

%description -n %{shortname}-kpathsea
Kpathsea is a library and utility programs which provide path searching
facilities for TeX file types, including the self-locating feature required for
movable installations, layered on top of a general search mechanism. It is not
distributed separately, but rather is released and maintained as part of the
TeX Live sources.

%package -n %{shortname}-l3build
Summary: A testing and building system for (La)TeX
Version: svn77170
Provides: texlive-l3build = %{epoch}:%{source_date}-%{release}
Provides: tex-l3build = %{epoch}:%{source_date}-%{release}
Provides: texlive-l3build-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-l3build-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-l3build-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-l3build-doc < 7:20180414
License: LPPL-1.3c
# lua
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-luatex

%description -n %{shortname}-l3build
The build system supports testing and building LaTeX3 code, on Linux, Mac OS X
and Windows systems. The package offers: A unit testing system for (La)TeX code
(whether kernel code or contributed packages); A system for typesetting package
documentation; and An automated process for creating CTAN releases. The package
is essentially independent of other material released by the LaTeX3 team, and
may be updated on a different schedule.

%package -n %{shortname}-l3sys-query
Summary: System queries for LaTeX using Lua
Version: svn77682
Provides: tex-l3sys-query = %{epoch}:%{source_date}-%{release}
License: MIT
# lua
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-luatex

%description -n %{shortname}-l3sys-query
The l3sys-query script provides a method for TeX runs to obtain system
information via shell escape to Lua. The facilities are more limited than the
similar Java script texosquery, but since it uses Lua, l3sys-query can be used
out of the box; with any installed TeX system. The script is written taking
account of TeX Live security requirements; it is therefore suitable for use
with restricted shell escape, the standard setting when installing a TeX
system. The supported queries are lsDirectory listing supporting a range of
options pwdObtaining details of the current working directory

%package -n %{shortname}-lacheck
Summary: LaTeX checker
Version: svn75712
Provides: texlive-lacheck = %{epoch}:%{source_date}-%{release}
Provides: tex-lacheck = %{epoch}:%{source_date}-%{release}
Provides: texlive-lacheck-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-lacheck-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-lacheck-bin < 7:20170520
License: GPL-1.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-lacheck
Lacheck is a tool for finding common mistakes in LaTeX documents. The
distribution includes sources, and executables for OS/2 and Win32 environments.
It is maintained as part of TeX Live.

%package -n %{shortname}-latex
Summary: A TeX macro package that defines LaTeX
Version: svn76924
Provides: texlive-latex = %{epoch}:%{source_date}-%{release}
Provides: tex-latex = %{epoch}:%{source_date}-%{release}
Provides: tetex-latex = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex-bin < 7:20170520
Provides: texlive-latex-bin-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latex-bin-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex-bin-bin < 7:20170520
Provides: tex-latex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex-doc < 7:20170520
Provides: texlive-texmf-latex = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texmf-latex < %{source_date}
License: LPPL-1.3c
# symlinks
BuildArch: noarch
Requires(post,postun): coreutils
Requires: tex(expl3.sty)
Requires: tex(hypdoc.sty)
Requires: tex(hyperref.sty)
Requires: tex(multicol.sty)
Requires: tex(url.sty)
Requires: texlive-base
# As a result of changes in textcomp, it requests TS1 fonts for some things
# most notably, \textbullet. Since people probably want a working itemize
# even on rather minimal installs, we add an explicit Requires on texlive-cm-super
# here. (bz1867927)
Requires: texlive-cm-super
Requires: texlive-kpathsea
Requires: texlive-latex-fonts
Requires: texlive-latexconfig
Requires: texlive-luatex
Requires: texlive-pdftex
# Another font dependency
Requires: texlive-psnfss

%description -n %{shortname}-latex
LaTeX is a widely-used macro package (format) for TeX, providing many basic
document formatting commands extended by a wide range of packages. It was
originally created by Leslie Lamport, whose last release was LaTeX 2.09. The
current LaTeX superseded that release in June 1994. The basic distribution is
catalogued separately, at latex-base. Apart from a large set of contributed
packages and third-party documentation (elsewhere on the archive), the
distribution includes: a number of required packages, which LaTeX authors may
assume will be present on any system running LaTeX; and a minimal set of
documentation detailing differences from the 'old' version of LaTeX in the
areas of user commands, font selection and control, class and package writing,
font encodings, configuration options and modification of LaTeX. For
downloading details, documentation links, etc., see the linked catalogue
entries above.

%package -n %{shortname}-latex-git-log
Version: svn71402
Provides: texlive-latex-git-log = %{epoch}:%{source_date}-%{release}
Provides: tex-latex-git-log = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex-git-log-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latex-git-log-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex-git-log-bin < 7:20170520
Provides: tex-latex-git-log-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex-git-log-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex-git-log-doc < 7:20170520
License: GPL-3.0-or-later
Summary: Typeset git log information
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-latex-git-log
The program is run within a git repository, and outputs the
entire version history, as a LaTeX table. That output will
typically be redirected to a file; the author recommends
typesetting in landscape orientation.

%package -n %{shortname}-latex-papersize
Version: svn53131
Provides: texlive-latex-papersize = %{epoch}:%{source_date}-%{release}
Provides: tex-latex-papersize = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex-papersize-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latex-papersize-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex-papersize-bin < 7:20170520
Provides: tex-latex-papersize-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex-papersize-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex-papersize-doc < 7:20170520
License: Apache-2.0
Summary: Calculate LaTeX settings for any font and paper size
Requires: texlive-base
Requires: texlive-kpathsea
# python
BuildArch: noarch

%description -n %{shortname}-latex-papersize
The package is a Python script, whose typical use is when
preparing printed material for users with low vision. The most
effective way of doing this is to print on (notional) small
paper, and then to magnify the result; the script calculates
the settings for various font and paper sizes. More details are
to be read in the script itself.

%package -n %{shortname}-latex2man
Summary: Translate LaTeX-based manual pages into Unix man format
Version: svn77377
Provides: texlive-latex2man = %{epoch}:%{source_date}-%{release}
Provides: tex-latex2man = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex2man-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latex2man-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex2man-bin < 7:20170520
Provides: tex-latex2man-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex2man-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex2man-doc < 7:20170520
License: LPPL-1.3c
# perl
BuildArch: noarch
Requires: tex(fancyhdr.sty)
Requires: tex(fancyheadings.sty)
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-latex2man
Latex2man is a tool to translate UNIX manual pages written with LaTeX into the
troff format understood by the UNIX man(1) command. Alternatively HTML,
Texinfo, or LaTeX code can be produced too. Output of parts of the text may be
suppressed using the conditional text feature (for this, LaTeX generation may
be used). There is a LaTeX package (latex2man.sty) for writing the man page and
a Perl script (latex2man) that does the actual translation.

%package -n %{shortname}-latex2nemeth
Summary: Convert LaTeX source to Braille with math in Nemeth
Version: svn76924
Provides: texlive-latex2nemeth = %{epoch}:%{source_date}-%{release}
Provides: tex-latex2nemeth = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex2nemeth-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latex2nemeth-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex2nemeth-bin < 7:20170520
Provides: tex-latex2nemeth-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-latex2nemeth-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latex2nemeth-doc < 7:20170520
License: GPL-3.0-only
# shell
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-latex2nemeth
After many failed attempts to transcribe real math notes and books to
Braille/Nemeth in order to deal with a real situation (blind student in Math
Dept.), we decided to develop a new program that follows a direct, from LaTeX
to Braille/Nemeth, approach. Our main target was the Greek language which is
only Braille level 1, but English at level 1 is supported as well. Simple
pictures in PSTricks are also supported in order to produce tactile graphics
with specialized equipment. Note that embossing will need LibreOffice and
odt2braille as this project does not deal with embossers' drivers. What's new
in version 1.1 In this version, the support of the user level commands of the
amsmath package was added, as described in its user guide, with the exception
of commutative diagrams (amscd package) as well as structures that are
irrelevant to visually impaired persons. Also, the Unicode mathematics symbols
of the unicode-math package that are represented by the Nemeth code are now
supported by latex2nemeth. We would like to acknowledge support by TUG's TeX
development fund for this project (development fund project 33).

%package -n %{shortname}-latexdiff
Summary: Determine and mark up significant differences between LaTeX files
Version: svn77278
Provides: texlive-latexdiff = %{epoch}:%{source_date}-%{release}
Provides: tex-latexdiff = %{epoch}:%{source_date}-%{release}
Provides: texlive-latexdiff-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latexdiff-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latexdiff-bin < 7:20170520
Provides: tex-latexdiff-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-latexdiff-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latexdiff-doc < 7:20170520
License: GPL-3.0-or-later
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-latexdiff
Latexdiff is a Perl script for visual mark up and revision of significant
differences between two LaTeX files. Various options are available for visual
markup using standard LaTeX packages such as color. Changes not directly
affecting visible text, for example in formatting commands, are still marked in
the LaTeX source. A rudimentary revision facility is provided by another Perl
script, latexrevise, which accepts or rejects all changes. Manual editing of
the difference file can be used to override this default behaviour and accept
or reject selected changes only.

%package -n %{shortname}-latexfileversion
Version: svn29349
Provides: texlive-latexfileversion = %{epoch}:%{source_date}-%{release}
Provides: tex-latexfileversion = %{epoch}:%{source_date}-%{release}
Provides: texlive-latexfileversion-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latexfileversion-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latexfileversion-bin < 7:20170520
Provides: tex-latexfileversion-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-latexfileversion-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latexfileversion-doc < 7:20170520
License: LPPL-1.3c
Summary: Prints the version and date of a LaTeX class or style file
Requires: texlive-base
Requires: texlive-kpathsea
# shell
BuildArch: noarch

%description -n %{shortname}-latexfileversion
This simple shell script prints the version and date of a LaTeX
class or style file. Syntax: latexfileversion <file> This
programme handles style files (extension .sty), class files
(extension .cls), and other TeX input files. The file extension
must be given.

%package -n %{shortname}-latexindent
Summary: Indent a LaTeX document, highlighting the programming structure
Version: svn76064
Provides: texlive-latexindent = %{epoch}:%{source_date}-%{release}
Provides: tex-latexindent = %{epoch}:%{source_date}-%{release}
Provides: texlive-latexindent-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latexindent-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latexindent-bin < 7:20170520
Provides: tex-latexindent-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-latexindent-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latexindent-doc < 7:20170520
License: GPL-3.0-or-later
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-latexindent
The Perl script processes a LaTeX file, indenting parts so as to highlight the
structure for the reader.

%package -n %{shortname}-latexpand
Version: svn66226
Provides: texlive-latexpand = %{epoch}:%{source_date}-%{release}
Provides: tex-latexpand = %{epoch}:%{source_date}-%{release}
Provides: texlive-latexpand-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-latexpand-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latexpand-bin < 7:20170520
Provides: tex-latexpand-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-latexpand-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-latexpand-doc < 7:20170520
License: BSD-3-Clause
Summary: Expand \input and \include in a LaTeX document
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-latexpand
Latexpand is a Perl script that simply replaces \input and
\include commands with the content of the file input/included.
The script does not deal with \includeonly commands.

%package -n %{shortname}-lcdftypetools
Version: svn70015
Provides: texlive-lcdtypetools = %{epoch}:%{source_date}-%{release}
Provides: tex-lcdftypetools = %{epoch}:%{source_date}-%{release}
# This is a mistake in the texlive package. Will be fixed in next major TL update.
Provides: lcdf-typetools = %{epoch}:%{source_date}-%{release}
Provides: texlive-lcdftypetools-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-lcdftypetools-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-lcdftypetools-bin < 7:20170520
License: GPL-1.0-or-later
Summary: A bundle of outline font manipulation tools
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-glyphlist

%description -n %{shortname}-lcdftypetools
This bundle of tools comprises: Cfftot1, which translates a
Compact Font Format (CFF) font, or a PostScript-flavored
OpenType font, into PostScript Type 1 format. It correctly
handles subroutines and hints; Mmafm and mmpfb, which create
instances of multiple-master fonts (mmafm and mmpfb were
previously distributed in their own package, mminstance);
Otfinfo, which reports information about OpenType fonts, such
as the features they support and the contents of their 'size'
optical size features; Otftotfm, which creates TeX font metrics
and encodings that correspond to a PostScript-flavored OpenType
font. It will interpret glyph positionings, substitutions, and
ligatures as far as it is able. You can say which OpenType
features should be activated; T1dotlessj, creates a Type 1 font
whose only character is a dotless j matching the input font's
design; T1lint, which checks a Type 1 font for correctness;
T1reencode, which replaces a font's internal encoding with one
you specify; and T1testpage, which creates a PostScript proof
for a Type 1 font.

%package -n %{shortname}-lib
Summary: Shared libraries for TeX-related files
Provides: texlive-kpathsea-lib = %{epoch}:%{source_date}-%{release}
# We have to straight up lie about this to ensure the upgrade.
Provides: texlive-kpathsea-lib(%{__isa}) = 6:2016
Obsoletes: texlive-kpathsea-lib < 2015
Provides: bundled(lua) = 5.2.4

%description -n %{shortname}-lib
TeX specific shared libraries.

%package -n %{shortname}-lib-devel
Summary: Development files for TeX specific shared libraries
Requires: %{shortname}-lib%{?_isa}
Provides: texlive-kpathsea-lib-devel = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-kpathsea-lib-devel < 2015

%description -n %{shortname}-lib-devel
Development files for TeX specific shared libraries.

%package -n %{shortname}-lilyglyphs
Version: svn56473
Provides: texlive-lilyglyphs = %{epoch}:%{source_date}-%{release}
Provides: tex-lilyglyphs = %{epoch}:%{source_date}-%{release}
Provides: texlive-lilyglyphs-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-lilyglyphs-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-lilyglyphs-bin < 7:20170520
Provides: tex-lilyglyphs-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-lilyglyphs-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-lilyglyphs-doc < 7:20170520
License: LPPL-1.3c
Summary: Access lilypond fragments and glyphs, in LaTeX
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(adjustbox.sty)
Requires: tex(booktabs.sty)
Requires: tex(fancyref.sty)
Requires: tex(fontspec.sty)
Requires: tex(hologo.sty)
Requires: tex(keyval.sty)
Requires: tex(listings.sty)
Requires: tex(longtable.sty)
Requires: tex(mdwlist.sty)
Requires: tex(microtype.sty)
Requires: tex(pgf.sty)
Requires: tex(selnolig.sty)
# python
BuildArch: noarch

%description -n %{shortname}-lilyglyphs
The package provides the means to include arbitrary elements of
Lilypond notation, including symbols from Lilypond's Emmentaler
font, in a LaTeX document. The package uses OpenType fonts, and
as a result must be compiled with LuaLaTeX or XeLaTeX.

%package -n %{shortname}-listbib
Version: svn29349
Provides: texlive-listbib = %{epoch}:%{source_date}-%{release}
Provides: tex-listbib = %{epoch}:%{source_date}-%{release}
Provides: texlive-listbib-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-listbib-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-listbib-bin < 7:20170520
Provides: tex-listbib-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-listbib-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-listbib-doc < 7:20170520
License: GPL-1.0-or-later
Summary: Lists contents of BibTeX files
Requires: texlive-base
Requires: texlive-kpathsea
# shell
BuildArch: noarch

%description -n %{shortname}-listbib
Generates listings of bibliographic data bases in BibTeX format
-- for example for archival purposes. Included is a listbib.bst
which is better suited for this purpose than the standard
styles.

%package -n %{shortname}-listings-ext
Version: svn29349
Provides: texlive-listings-ext = %{epoch}:%{source_date}-%{release}
Provides: tex-listings-ext = %{epoch}:%{source_date}-%{release}
Provides: texlive-listings-ext-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-listings-ext-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-listings-ext-bin < 7:20170520
Provides: tex-listings-ext-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-listings-ext-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-listings-ext-doc < 7:20170520
License: LPPL-1.3a
Summary: Automated input of source
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(listings.sty)
Requires: tex(xkeyval.sty)
# shell
BuildArch: noarch

%description -n %{shortname}-listings-ext
The package provides a means of marking a source, so that
samples of it may be included in a document (by means of the
listings package) in a stable fashion, regardless of any change
to the source. The markup in the source text defines tags for
blocks of source. These tags are processed by a shell script to
make a steering file that is used by the package when LaTeX is
being run.

%package -n %{shortname}-light-latex-make
Version: svn66473
Provides: texlive-light-latex-make = %{epoch}:%{source_date}-%{release}
Summary: llmk: A build tool for LaTeX documents
License: MIT
Requires: texlive-base texlive-kpathsea

%description -n %{shortname}-light-latex-make
This program is yet another build tool specific for LaTeX
documents. Its aim is to provide a simple way to specify a
workflow of processing LaTeX documents and encourage people to
always explicitly show the right workflow for each document.
The main features of the executable llmk are all about the
above purpose. First, you can describe the workflows either in
an external file llmk.toml or in a LaTeX document source in the
form of magic comments. Further, multiple magic comment formats
can be used. Second, it is fully cross-platform. The only
requirement of the program is the texlua command; llmk provides
a uniform way to describe the workflows available for nearly
all TeX environments. Third, it behaves exactly the same in any
environment. At this point, llmk intentionally does not provide
any method for user configuration. Therefore one can guarantee
that for a LaTeX document with an llmk setup, the process of
typesetting the document will be reproduced in any TeX
environment with the program.

%package -n %{shortname}-lollipop
Version: svn69742
Provides: texlive-lollipop = %{epoch}:%{source_date}-%{release}
Provides: tex-lollipop = %{epoch}:%{source_date}-%{release}
Provides: texlive-lollipop-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-lollipop-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-lollipop-bin < 7:20170520
Provides: tex-lollipop-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-lollipop-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-lollipop-doc < 7:20170520
License: GPL-3.0-or-later
Summary: TeX made easy
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-cm
Requires: texlive-hyphen-base
Requires: texlive-tex
Requires(post,postun): coreutils
# no actual binaries here
BuildArch: noarch

%description -n %{shortname}-lollipop
Lollipop is "TeX made easy" -- it is a macro package that
functions as a toolbox for writing TeX macros. Its main aim is
to make macro writing so easy that implementing a fully new
layout in TeX would become a matter of less than an hour for an
average document. The aim is that such a task could be
accomplished by someone with only a very basic training in TeX
programming. Thus, Lollipop aims to make structured text
formatting available in environments where typical users would
switch to WYSIWYG packages for the freedom that such a
mechanism offers. In addition, development of support for
Lollipop documents written in RTL languages (such as Persian)
is underway.

%package -n %{shortname}-ltxfileinfo
Version: svn38663
Provides: texlive-ltxfileinfo = %{epoch}:%{source_date}-%{release}
Provides: tex-ltxfileinfo = %{epoch}:%{source_date}-%{release}
Provides: texlive-ltxfileinfo-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-ltxfileinfo-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ltxfileinfo-bin < 7:20170520
Provides: tex-ltxfileinfo-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ltxfileinfo-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ltxfileinfo-doc < 7:20170520
License: GPL-1.0-or-later
Summary: Print version information for a LaTeX file
Requires: texlive-base
Requires: texlive-kpathsea
# shell
BuildArch: noarch

%description -n %{shortname}-ltxfileinfo
ltxfileinfo displays version information for LaTeX files. If no
path information is given, the file is searched using
kpsewhich. As an extra, for developers, the script will (use
the --star or --color options) check the valididity of the
\Provides... statements in the files. The script uses code from
Uwe Luck's readprov.sty.

%package -n %{shortname}-ltximg
Version: svn59335
Provides: texlive-ltximg = %{epoch}:%{source_date}-%{release}
Provides: tex-ltximg = %{epoch}:%{source_date}-%{release}
Provides: texlive-ltximg-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-ltximg-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ltximg-bin < 7:20170520
Provides: tex-ltximg-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ltximg-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ltximg-doc < 7:20170520
License: GPL-2.0-or-later
Summary: Split LaTeX files to sanitise a conversion process
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-ltximg
The package provides a Perl script that extracts all TikZ and
PStricks environments for separate processing to produce images
(in eps, pdf, png or jpg format) for use by a converter or the
preview bundle.

%package -n %{shortname}-luafindfont
Summary: Search fonts in the LuaTeX font database
Version: svn75679
Provides: texlive-luafindfont = %{epoch}:%{source_date}-%{release}
Provides: texlive-luafindfont-bin = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
# lua
BuildArch: noarch
Requires: lua >= 5.3
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-luafindfont
This Lua script searches for fonts in the font database.

%package -n %{shortname}-luaotfload
Version: svn74324
Provides: texlive-luaotfload = %{epoch}:%{source_date}-%{release}
Provides: tex-luaotfload = %{epoch}:%{source_date}-%{release}
Provides: texlive-luaotfload-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-luaotfload-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-luaotfload-bin < 7:20170520
Provides: tex-luaotfload-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-luaotfload-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-luaotfload-doc < 7:20170520
License: GPL-2.0-or-later
Summary: OpenType 'loader' for Plain TeX and LaTeX
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-lualibs
Requires: texlive-lua-alt-getopt
Requires: texlive-lua-uni-algos
Requires: tex(luatexbase.sty)
# lua
BuildArch: noarch

%description -n %{shortname}-luaotfload
The package adopts the TrueType/OpenType Font loader code
provided in ConTeXt, and adapts it to use in Plain TeX and
LaTeX. It works under LuaLaTeX only.

%package -n %{shortname}-luahbtex
Summary: LuaTeX with HarfBuzz library for glyph shaping
Version: svn77830
Provides: texlive-luahbtex = %{epoch}:%{source_date}-%{release}
Provides: tex-luahbtex = %{epoch}:%{source_date}-%{release}
Provides: texlive-luahbtex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-luahbtex-bin = %{epoch}:%{source_date}-%{release}
License: GPL-2.0-or-later
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-etex
Requires: texlive-hyph-utf8
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-luatex
Requires: texlive-plain
Requires: texlive-tex-ini-files
Requires: texlive-unicode-data

%description -n %{shortname}-luahbtex
LuaTeX with HarfBuzz library for glyph shaping

%package -n %{shortname}-luajittex
Summary: LuaTeX with just-in-time (jit) compiler, with and without HarfBuzz
Version: svn77830
Provides: texlive-luajittex = %{epoch}:%{source_date}-%{release}
Provides: tex-luajittex = %{epoch}:%{source_date}-%{release}
Provides: tex-luajittex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-luajittex-bin = %{epoch}:%{source_date}-%{release}
License: GPL-2.0-or-later
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-etex
Requires: texlive-hyph-utf8
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-luatex
Requires: texlive-plain
Requires: texlive-tex-ini-files
Requires: texlive-unicode-data

%description -n %{shortname}-luajittex
LuaTeX with just-in-time (jit) compiler, with and without HarfBuzz

%package -n %{shortname}-luatex
Summary: The LuaTeX engine
Version: svn78218
Provides: texlive-luatex = %{epoch}:%{source_date}-%{release}
Provides: tex-luatex = %{epoch}:%{source_date}-%{release}
Provides: texlive-luatex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-luatex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-luatex-bin < 7:20170520
Provides: tex-luatex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-luatex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-luatex-doc < 7:20170520
License: GPL-2.0-or-later
Requires(post,postun): coreutils
Requires: tex(luatex.def)
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-etex
Requires: texlive-hyph-utf8
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-plain
Requires: texlive-tex-ini-files
Requires: texlive-unicode-data

%description -n %{shortname}-luatex
LuaTeX is a greatly extended version of pdfTeX using Lua as an embedded
scripting language. The LuaTeX project's main objective is to provide an open
and configurable variant of TeX while at the same time offering substantive
backward compatibility. LuaTeX uses Unicode (as UTF-8) as its default input
encoding, and is able to use modern (OpenType and TrueType) fonts (for both
text and mathematics).

%package -n %{shortname}-lwarp
Summary: Converts LaTeX to HTML
Version: svn78111
Provides: texlive-lwarp = %{epoch}:%{source_date}-%{release}
Provides: tex-lwarp = %{epoch}:%{source_date}-%{release}
Provides: texlive-lwarp-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-lwarp-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-lwarp-bin < 7:20170520
Provides: tex-lwarp-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-lwarp-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-lwarp-doc < 7:20170520
License: LPPL-1.3c
# lua
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-lwarp
This package converts LaTeX to HTML by using LaTeX to process the user's
document and generate HTML tags. External utility programs are only used for
the final conversion of text and images. Math may be represented by SVG files
or MathJax. Hundreds of LaTeX packages are supported, and their load order is
automatically verified. Documents may be produced by LaTeX, LuaLaTeX, XeLaTeX,
and by several CJK engines, classes, and packages. A texlua script automates
compilation, index, glossary, and batch image processing, and also supports
latexmk. Configuration is semi-automatic at the first manual compile. Support
files are self-generated. Print and HTML versions of each document may coexist.
Assistance is provided for HTML import into EPUB conversion software and word
processors. Requirements include the commonly-available Poppler utilities, and
Perl. Detailed installation instructions are included for each of the major
operating systems and TeX distributions. A quick-start tutorial is provided.

%package -n %{shortname}-lyluatex
Version: svn66880
Provides: texlive-lyluatex = %{epoch}:%{source_date}-%{release}
Summary: Commands to include lilypond scores within a (Lua)LaTeX document
License: MIT
Requires: texlive-base texlive-kpathsea
# lua
BuildArch: noarch
Requires: tex(currfile.sty)
Requires: tex(environ.sty)
Requires: tex(graphicx.sty)
Requires: tex(luaotfload.sty)
Requires: tex(luaoptions.sty)
Requires: tex(luatexbase.sty)
Requires: tex(metalogo.sty)
Requires: tex(minibox.sty)
Requires: tex(pdfpages.sty)
Requires: tex(xkeyval.sty)

%description -n %{shortname}-lyluatex
This package provides macros for the inclusion of LilyPond
scores within LuaLaTeX. It calls LilyPond to compile scores,
then includes the produced files.

%package -n %{shortname}-make4ht
Summary: A build system for tex4ht
Version: svn78133
Provides: texlive-make4ht = %{epoch}:%{source_date}-%{release}
Provides: tex-make4ht = %{epoch}:%{source_date}-%{release}
Provides: texlive-make4ht-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-make4ht-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-make4ht-bin < 7:20170520
Provides: tex-make4ht-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-make4ht-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-make4ht-doc < 7:20170520
License: LPPL-1.3c
# lua
BuildArch: noarch
Requires: tex(tex4ht.sty)
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-tex4ht

%description -n %{shortname}-make4ht
make4ht is a simple build system for tex4ht, a TeX to XML converter. It
provides a command line tool that drives the conversion process. It also
provides a library which can be used to create customized conversion tools.

%package -n %{shortname}-makedtx
Summary: Perl script to help generate dtx and ins files
Version: svn77871
Provides: texlive-makedtx = %{epoch}:%{source_date}-%{release}
Provides: tex-makedtx = %{epoch}:%{source_date}-%{release}
Provides: texlive-makedtx-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-makedtx-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-makedtx-bin < 7:20170520
Provides: tex-makedtx-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-makedtx-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-makedtx-doc < 7:20170520
License: LPPL-1.3c
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-makedtx
The makedtx bundle is provided to help LaTeX2e developers to write the code and
documentation in separate files, and then combine them into a single .dtx file
for distribution. It automatically generates the character table, and also
writes the associated installation (.ins) script.

%package -n %{shortname}-makeindex
Summary: Makeindex development sources
Version: svn75712
Provides: texlive-makeindex = %{epoch}:%{source_date}-%{release}
Provides: tex-makeindex = %{epoch}:%{source_date}-%{release}
Provides: texlive-makeindex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-makeindex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-makeindex-bin < 7:20170520
Provides: tex-makeindex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-makeindex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-makeindex-doc < 7:20170520
License: MakeIndex
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-makeindex
The package contains the development sources of makeindex, which is now
maintained as part of TeX Live.

%package -n %{shortname}-markdown
Summary: Converting and rendering markdown documents inside TeX
Version: svn77254
Provides: tex-markdown = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
# lua
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-l3kernel
Requires: texlive-lt3luabridge
Requires: texlive-lua-tinyyaml

%description -n %{shortname}-markdown
The package provides facilities for the conversion of markdown and YAML markup
to plain TeX. These are provided both in form of a Lua module and in form of
plain TeX, LaTeX, and ConTeXt macro packages that enable the direct inclusion
of markdown and YAML documents inside TeX documents.

%package -n %{shortname}-match_parens
Summary: Find mismatches of parentheses, braces, (angle) brackets, in texts
Version: svn76442
Provides: texlive-match_parens = %{epoch}:%{source_date}-%{release}
Provides: tex-match_parens = %{epoch}:%{source_date}-%{release}
Provides: texlive-match_parens-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-match_parens-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-match_parens-bin < 7:20170520
Provides: tex-match_parens-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-match_parens-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-match_parens-doc < 7:20170520
License: GPL-1.0-or-later
# ruby
BuildArch: noarch
Requires: ruby
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-match_parens
Mismatches of parentheses, braces, (angle) brackets, especially in TeX sources
which may be rich in those, may be difficult to trace. This little Ruby script
helps you by writing your text to standard output, after adding a left margin
to your text, which will normally be almost empty, but will clearly show any
mismatches.

%package -n %{shortname}-mathspic
Version: svn31957
Provides: texlive-mathspic = %{epoch}:%{source_date}-%{release}
Provides: tex-mathspic = %{epoch}:%{source_date}-%{release}
Provides: texlive-mathspic-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mathspic-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mathspic-bin < 7:20170520
Provides: tex-mathspic-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-mathspic-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mathspic-doc < 7:20170520
License: LPPL-1.3c
Summary: A Perl filter program for use with PiCTeX
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(prepictex.tex)
Requires: tex(pictexwd.tex)
Requires: tex(postpictex.tex)
# perl
BuildArch: noarch

%description -n %{shortname}-mathspic
MathsPIC(Perl) is a development of the earlier MathsPIC(DOS)
program, now implemented as a Perl script, being much more
portable than the earlier program. MathsPIC parses a plain text
input file and generates a plain text output-file containing
commands for drawing a diagram. Version 1.0 produces output
containing PiCTeX and (La)TeX commands, which may then be
processed by plain TeX or LaTeX in the usual way. MathsPIC also
outputs a comprehensive log-file. MathsPIC facilitates creating
figures using PiCTeX by providing an environment for
manipulating named points and also allows the use of variables
and maths (advance, multiply, and divide)--in short--it takes
the pain out of PiCTeX.

%package -n %{shortname}-memoize
Version: svn73025
Provides: tex-memoize = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
Summary: Externalization of graphics and memoization of compilation results in general
Requires: texlive-base
Requires: texlive-kpathsea
# perl and python for some reason
BuildArch: noarch

%description -n %{shortname}-memoize
Memoize is a package for externalization of graphics and
memoization of compilation results in general, allowing the
author to reuse the results of compilation-intensive code.
Memoize (i) induces very little overhead, as all externalized
graphics is produced in a single compilation. It features (ii)
automatic recompilation upon the change of code or
user-adjustable context, and (iii) automatic externalization of
TikZ pictures and Forest trees, easily extensible to other
commands and environments. Furthermore, Memoize (iv) supports
cross-referencing, TikZ overlays and Beamer, (v) works with all
major engines and formats, and (vi) is adaptable to any
workflow.

%package -n %{shortname}-metafont
Summary: A system for specifying fonts
Version: svn77830
Provides: texlive-metafont = %{epoch}:%{source_date}-%{release}
Provides: tex-metafont = %{epoch}:%{source_date}-%{release}
Provides: texlive-metafont-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-metafont-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-metafont-bin < 7:20170520
License: Knuth-CTAN
Requires(post,postun): coreutils
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-modes

%description -n %{shortname}-metafont
The program takes a programmatic specification of a font, and produces a bitmap
font (whose properties are defined by a set of parameters of the target
device), and metrics for use by TeX. The bitmap output may be converted into a
format directly usable by a device driver, etc., by the tools provided in the
parallel mfware distribution. Third parties have developed tools to convert the
bitmap output to outline fonts. The distribution includes the source of Knuth's
Metafont book; this source is there to read, as an example of writing TeX -- it
should not be processed without Knuth's direct permission. The mailing list
tex-fonts@math.utah.edu is the best for general discussion of Metafont usage;
the tex-k@tug.org list is best for bug reports about building the software,
etc.

%package -n %{shortname}-metapost
Summary: A development of Metafont for creating graphics
Version: svn77830
Provides: texlive-metapost = %{epoch}:%{source_date}-%{release}
Provides: tex-metapost = %{epoch}:%{source_date}-%{release}
Provides: texlive-metapost-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-metapost-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-metapost-bin < 7:20170520
Provides: tex-metapost-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-metapost-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-metapost-doc < 7:20170520
License: LGPL-2.1-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-metapost
MetaPost uses a language based on that of Metafont to produce precise technical
illustrations. Its output is scalable PostScript or SVG, rather than the
bitmaps Metafont creates.

%package -n %{shortname}-mex
Version: svn58661
Provides: texlive-mex = %{epoch}:%{source_date}-%{release}
Provides: tex-mex = %{epoch}:%{source_date}-%{release}
Provides: texlive-mex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mex-bin < 7:20170520
Provides: tex-mex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-mex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mex-doc < 7:20170520
License: LicenseRef-Fedora-Public-Domain
Summary: Polish formats for TeX
Requires: texlive-base
Requires: texlive-enctex
Requires: texlive-hyph-utf8
Requires: texlive-hyphen-base
Requires: texlive-hyphen-polish
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-pdftex
Requires: texlive-pl
Requires: texlive-plain
Requires: texlive-tex
Requires: texlive-tex-ini-files
Requires: texlive-utf8mex
Requires(post,postun): coreutils
# just symlinks
BuildArch: noarch

%description -n %{shortname}-mex
MeX is an adaptation of Plain TeX (MeX) and LaTeX209 (LaMeX)
formats to the Polish language and to Polish printing customs.
It contains a complete set of Metafont sources of Polish fonts,
hyphenation rules for the Polish language and sources of
formats.

%package -n %{shortname}-mflua
Summary: Configuration and base files for MFLua
Version: svn77830
Provides: texlive-mflua = %{epoch}:%{source_date}-%{release}
Provides: tex-mflua = %{epoch}:%{source_date}-%{release}
Provides: texlive-mflua-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mflua-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mflua-bin < 7:20170520
License: GPL-1.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-luatex
Requires: texlive-metafont

%description -n %{shortname}-mflua
For information on this Lua-enabled Metafont, see, for example:
tug.org/TUGboat/tb32-2/tb101scarso.pdf.

%package -n %{shortname}-mfware
Summary: Supporting tools for Metafont: gftodvi, gftopk, gftype, mft
Version: svn77830
Provides: texlive-mfware = %{epoch}:%{source_date}-%{release}
Provides: tex-mfware = %{epoch}:%{source_date}-%{release}
Provides: texlive-mfware-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mfware-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mfware-bin < 7:20170520
License: LicenseRef-Fedora-Public-Domain
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-mfware
A collection of programs (as web source) for processing the output of Metafont.
They include: gftodvi (for making proof sheets of letters); gftopk (translate
gf bitmap files to pk bitmaps); gftype (human-readable dump of gf files); mft
(prettyprint Metafont source).

%package -n %{shortname}-mf2pt1
Version: svn71883
Provides: texlive-mf2pt1 = %{epoch}:%{source_date}-%{release}
Provides: tex-mf2pt1 = %{epoch}:%{source_date}-%{release}
Provides: texlive-mf2pt1-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mf2pt1-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mf2pt1-bin < 7:20170520
Provides: tex-mf2pt1-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-mf2pt1-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mf2pt1-doc < 7:20170520
License: LPPL-1.3c
Summary: Produce PostScript Type 1 fonts from Metafont source
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-mf2pt1
mf2pt1 facilitates producing PostScript Type 1 fonts from a
Metafont source file. It is not, as the name may imply, an
automatic converter of arbitrary Metafont fonts to Type 1
format. mf2pt1 imposes a number of restrictions on the Metafont
input. If these restrictions are met, mf2pt1 will produce valid
Type 1 output with more accurate control points than can be
reverse-engineered by TeXtrace, mftrace, and other programs
which convert bitmaps to outline fonts.

%package -n %{shortname}-minted
Summary: Highlighted source code for LaTeX
Version: svn78270
Provides: tex-minted = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c AND BSD-3-Clause
# python
BuildArch: noarch
Requires: texlive-base
Requires: texlive-catchfile
Requires: texlive-etoolbox
Requires: texlive-float
Requires: texlive-fvextra
Requires: texlive-kpathsea
Requires: texlive-latex2pydata
Requires: texlive-newfloat
Requires: texlive-pdftexcmds
Requires: texlive-pgf
Requires: texlive-pgfopts
Requires: texlive-tools
Requires: texlive-xcolor

%description -n %{shortname}-minted
The package that facilitates expressive syntax highlighting in LaTeX using the
powerful Pygments library. The package also provides options to customize the
highlighted source code output using fancyvrb.

%package -n %{shortname}-mkgrkindex
Version: svn26313
Provides: texlive-mkgrkindex = %{epoch}:%{source_date}-%{release}
Provides: tex-mkgrkindex = %{epoch}:%{source_date}-%{release}
Provides: texlive-mkgrkindex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mkgrkindex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mkgrkindex-bin < 7:20170520
Provides: tex-mkgrkindex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-mkgrkindex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mkgrkindex-doc < 7:20170520
License: LPPL-1.3c
Summary: Makeindex working with Greek
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-mkgrkindex
Makeindex is resolutely stuck with Latin-based alphabets, so
will not deal with Greek indexes, unaided. This package
provides a Perl script that will transmute the index of a Greek
document in such a way that makeindex will sort the entries
according to the rules of the Greek alphabet.

%package -n %{shortname}-mkjobtexmf
Version: svn29725
Provides: texlive-mkjobtexmf = %{epoch}:%{source_date}-%{release}
Provides: tex-mkjobtexmf = %{epoch}:%{source_date}-%{release}
Provides: texlive-mkjobtexmf-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mkjobtexmf-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mkjobtexmf-bin < 7:20170520
Provides: tex-mkjobtexmf-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-mkjobtexmf-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mkjobtexmf-doc < 7:20170520
License: GPL-2.0-only
Summary: Generate a texmf tree for a particular job
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-mkjobtexmf
The package provides a Perl script, which runs a program and
tries to find the names of file used. Two methods are
available, option -recorder of (Web2C) TeX and the program
strace. Then it generates a directory with a texmf tree. It
checks the found files and tries sort them in this texmf tree.
The script may be used for archiving purposes or to speed up
later TeX runs.

%package -n %{shortname}-mkpic
Summary: Perl interface to mfpic
Version: svn76483
Provides: texlive-mkpic = %{epoch}:%{source_date}-%{release}
Provides: tex-mkpic = %{epoch}:%{source_date}-%{release}
Provides: texlive-mkpic-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mkpic-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mkpic-bin < 7:20170520
Provides: tex-mkpic-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-mkpic-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mkpic-doc < 7:20170520
License: GPL-1.0-or-later
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-mkpic
mkpic provides an easy interface for making small pictures with mfpic. To this
end you create an input file consisting of commands, one per line, with space
separated parameters (or you modify the DATA section of the mkpic script, which
is used if you run it without an input file). For an extensive description see
the file mkpicdoc.pdf, which is part of the distribution.

%package -n %{shortname}-mltex
Version: svn71363
Provides: texlive-mltex = %{epoch}:%{source_date}-%{release}
Provides: tex-mltex = %{epoch}:%{source_date}-%{release}
Provides: texlive-mltex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mltex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mltex-bin < 7:20170520
Provides: tex-mltex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-mltex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mltex-doc < 7:20170520
License: Knuth-CTAN
Summary: The MLTeX system
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-latex
Requires: texlive-pdftex
Requires: texlive-cm
Requires: texlive-hyphen-base
Requires: texlive-babel
Requires: texlive-dehyph
Requires: texlive-hyph-utf8
Requires: texlive-l3kernel
Requires: texlive-latexconfig
Requires: texlive-latex-fonts
Requires: texlive-unicode-data
Requires: texlive-knuth-lib
Requires: texlive-plain
Requires(post,postun): coreutils
# symlinks
BuildArch: noarch

%description -n %{shortname}-mltex
MLTeX is a modification of TeX version >=3.0 that allows the
hyphenation of words with accented letters using ordinary
Computer Modern (CM) fonts. The system is distributed as a TeX
change file.

%package -n %{shortname}-mptopdf
Summary: Mpost to PDF, native MetaPost graphics inclusion
Version: svn78010
Provides: texlive-mptopdf = %{epoch}:%{source_date}-%{release}
Provides: tex-mptopdf = %{epoch}:%{source_date}-%{release}
Provides: texlive-mptopdf-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-mptopdf-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mptopdf-bin < 7:20170520
Provides: tex-mptopdf-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-mptopdf-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-mptopdf-doc < 7:20170520
License: GPL-1.0-or-later OR LPPL-1.3c
# perl
BuildArch: noarch
Requires(post,postun): coreutils
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-pdftex
Requires: texlive-plain

%description -n %{shortname}-mptopdf
The mptopdf script does standalone conversion from mpost to PDF, using the
supp-* and syst-* files. They also allow native MetaPost graphics inclusion in
LaTeX (via pdftex.def) and ConTeXt. They can be used independently of the rest
of ConTeXt, yet are maintained as part of it. So in TeX Live we pull them out
to this separate package for the benefit of LaTeX users who do not install the
rest of ConTeXt. This can be found on CTAN in macros/pdftex/graphics. The files
originally come from the ConTeXt distribution. TL uses the repackaging from
https://github.com/gucci-on-fleek/context-packaging.

%package -n %{shortname}-multibibliography
Summary: Multiple versions of a bibliography, with different sort orders
Version: svn77682
Provides: texlive-multibibliography = %{epoch}:%{source_date}-%{release}
Provides: tex-multibibliography = %{epoch}:%{source_date}-%{release}
Provides: texlive-multibibliography-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-multibibliography-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-multibibliography-bin < 7:20170520
Provides: tex-multibibliography-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-multibibliography-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-multibibliography-doc < 7:20170520
License: LPPL-1.3c
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-multibibliography
Conventional standards for bibliography styles impose a forced choice between
index and name/year citations, and corresponding references. The package avoids
this choice, by providing alphabetic, sequenced, and even chronological
orderings of references. Inline citations, that integrate these heterogeneous
styles, are also supported (and work with other bibliography packages).

%package -n %{shortname}-musixtex
Summary: Sophisticated music typesetting
Version: svn77682
Provides: texlive-musixtex = %{epoch}:%{source_date}-%{release}
Provides: tex-musixtex = %{epoch}:%{source_date}-%{release}
Provides: texlive-musixtex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-musixtex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-musixtex-bin < 7:20170520
Provides: tex-musixtex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-musixtex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-musixtex-doc < 7:20170520
License: GPL-2.0-or-later
# lua
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-musixtex
MusiXTeX provides a set of macros, based on the earlier MusicTeX, for
typesetting music with TeX. To produce optimal spacing, MusiXTeX is a
three-pass system: etex, musixflx, and etex again. (Musixflx is a lua script
that is provided in the bundle.) The three-pass process, optionally followed by
processing for printed output, is automated by the musixtex wrapper script. The
package uses its own specialised fonts, which must be available on the system
for musixtex to run. This version of MusiXTeX builds upon work by Andreas
Egler, whose own version is no longer being developed. The MusiXTeX macros are
universally acknowledged to be challenging to use directly: the pmx
preprocessor compiles a simpler input language to MusiXTeX macros..

%package -n %{shortname}-musixtnt
Version: svn69742
Provides: texlive-musixtnt = %{epoch}:%{source_date}-%{release}
Provides: tex-musixtnt = %{epoch}:%{source_date}-%{release}
Provides: texlive-musixtnt-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-musixtnt-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-musixtnt-bin < 7:20170520
Provides: tex-musixtnt-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-musixtnt-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-musixtnt-doc < 7:20170520
License: GPL-2.0-or-later
Summary: A MusiXTeX extension library that enables transformations of the effect of notes commands
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-musixtex

%description -n %{shortname}-musixtnt
The package includes an archive containing a MusiXTeX extension
library musixtnt, and documentation for a program:
msxlint. musixtnt.tex provides a macro \TransformNotes that
enables transformations of the effect of notes commands such
as \notes. In general, the effect of
\TransformNotes{input}{output} is that notes commands in the
source will expect their arguments to match the input pattern,
but the notes will be typeset according to the output pattern.
An example is extracting single-instrument parts from a multi-
instrument score. msxlint detects incorrectly formatted notes
lines in a MusiXTeX source file. This should be used before
using \TransformNotes.

%package -n %{shortname}-m-tx
Summary: A preprocessor for pmx
Version: svn78106
Provides: texlive-m-tx = %{epoch}:%{source_date}-%{release}
Provides: tex-m-tx = %{epoch}:%{source_date}-%{release}
Provides: texlive-m-tx-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-m-tx-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-m-tx-bin < 7:20170520
Provides: tex-m-tx-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-m-tx-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-m-tx-doc < 7:20170520
License: MIT
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-m-tx
M-Tx is a preprocessor to pmx, which is itself a preprocessor to musixtex, a
music typesetting system. The prime motivation to the development of M-Tx was
to provide lyrics for music to be typeset. In fact, pmx now provides a lyrics
interface, but M-Tx continues in use by those who prefer its language.

%package -n %{shortname}-oberdiek
Summary: A bundle of packages submitted by Heiko Oberdiek
Version: svn78315
Provides: texlive-oberdiek = %{epoch}:%{source_date}-%{release}
Provides: tex-oberdiek = %{epoch}:%{source_date}-%{release}
Provides: tex-oberdiek-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-oberdiek-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-oberdiek-doc < 7:20170520
License: LPPL-1.3c
BuildArch: noarch
# To complete the bundle
Requires: tex(amsmath.sty)
Requires: tex(array.sty)
Requires: tex(atveryend.sty)
Requires: tex(bigintcalc.sty)
Requires: tex(color.sty)
Requires: tex(etexcmds.sty)
Requires: tex(fontspec.sty)
Requires: tex(fp-basic.sty)
Requires: tex(fp-snap.sty)
Requires: tex(graphics.sty)
Requires: tex(hologo.sty)
Requires: tex(hypdoc.sty)
Requires: tex(hyperref.sty)
Requires: tex(index.sty)
Requires: tex(intcalc.sty)
Requires: tex(keyval.sty)
Requires: tex(kvsetkeys.sty)
Requires: tex(letltxmacro.sty)
Requires: tex(ltxcmds.sty)
Requires: tex(parallel.sty)
Requires: tex(parcolumns.sty)
Requires: tex(pdfcol.sty)
Requires: tex(pdfescape.sty)
Requires: tex(remreset.sty)
Requires: tex(unicode-math.sty)
Requires: tex(uniquecounter.sty)
Requires: tex(zref-base.sty)
Requires: texlive-auxhook
Requires: texlive-base
Requires: texlive-grfext
Requires: texlive-grffile
Requires: texlive-iftex
Requires: texlive-infwarerr
Requires: texlive-kpathsea
Requires: texlive-kvoptions
Requires: texlive-pdftexcmds

%description -n %{shortname}-oberdiek
The bundle comprises packages to provide: bmpsize: get bitmap size and
resolution data; centernot: a horizontally-centred \not symbol; chemarr:
extensible chemists' reaction arrows; classlist: record information about
document class(es) used; colonequals: poor man's mathematical relation symbols;
dvipscol: dvips colour stack management; engord: define counter-printing
operations producing English ordinals; eolgrab: collect arguments delimited by
end of line; flags: setting and clearing flags in bit fields and converting the
bit field into a decimal number; holtxdoc: extra documentation macros;
hypbmsec: bookmarks in sectioning commands; hypgotoe: experimental package for
links to embedded files; hyphsubst: substitute hyphenation patterns; ifdraft:
switch for option draft; iflang: provides expandable checks for the current
language; pdfcolparallel: fixes colour problems in package parallel;
pdfcolparcolumns: fixes colour problems in package parcolumns; pdfcrypt:
setting PDF encryption; protecteddef: define a command that protected against
expansion; resizegather: automatically resize overly large equations;
rotchiffre: performs simple rotation cyphers; scrindex: redefines environment
'theindex' of package 'index', if a class from KOMA-Script is loaded;
setouterhbox: set \hbox in outer horizontal mode; settobox: getting box sizes;
stackrel: extensions of the \stackrel command; stampinclude: selects the files
for \include by inspecting the timestamp of the .aux file(s); tabularht:
tabulars with height specification; tabularkv: key value interface for tabular
parameters; thepdfnumber: canonical numbers for use in PDF files and elsewhere;
twoopt: commands with two optional arguments; Each of the packages is
represented by two files, a .dtx (documented source) and a PDF file; the .ins
file necessary for installation is extracted by running the .dtx file with
Plain TeX.

%package -n %{shortname}-omegaware
Summary: A wide-character-set extension of TeX
Version: svn77830
Provides: texlive-omegaware = %{epoch}:%{source_date}-%{release}
Provides: tex-omegaware = %{epoch}:%{source_date}-%{release}
Provides: texlive-omegaware-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-omegaware-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-omegaware-bin < 7:20170520
Provides: tex-omegaware-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-omegaware-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-omegaware-doc < 7:20170520
License: GPL-1.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-omegaware
A development of TeX, which deals in multi-octet Unicode characters, to enable
native treatment of a wide range of languages without changing character-set.
Work on Omega has ceased (the TeX Live package contains only support files);
its compatible successor is aleph, which is itself also in major maintenance
mode only. Ongoing projects developing Omega (and Aleph) ideas include Omega-2
and LuaTeX.

%package -n %{shortname}-optex
Summary: LuaTeX format based on Plain TeX and OPmac
Version: svn78109
Provides: texlive-optex = %{epoch}:%{source_date}-%{release}
License: LicenseRef-Fedora-Public-Domain
Requires: texlive-amsfonts
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-ec
Requires: texlive-hyphen-base
Requires: texlive-kpathsea
Requires: texlive-librarian
Requires: texlive-lm
Requires: texlive-luaotfload
Requires: texlive-luatex
Requires: texlive-rsfs
Requires: texlive-unicode-data

%description -n %{shortname}-optex
OpTeX is a LuaTeX format based on Plain TeX macros with power from OPmac (fonts
selection system, colors, external graphics, references, hyperlinks, ...) with
unicode fonts.

%package -n %{shortname}-optexcount
Version: svn59817
Provides: texlive-optexcount = %{epoch}:%{source_date}-%{release}
Provides: texlive-optexcount-bin = %{epoch}:%{source_date}-%{release}
License: MIT
Summary: Python script for counting words in OpTeX documents
Requires: texlive-base, texlive-kpathsea
#python
BuildArch: noarch

%description -n %{shortname}-optexcount
OpTeXcount is a basic python utility that analyzes OpTeX source code. It is
inspired by already existing TeXcount for LaTeX. The functionality is really
lightweight and basic. It counts words and other elements of OpTeX document
and sorts them out into individual categories. Users can print the source code
with highlighted words using several colors,so they see what is considered as
word, header etc.

%package -n %{shortname}-pagelayout
Summary: Layout graphic rich documents
Version: svn71937
License: LPPL-1.3c
Requires: texlive-base texlive-kpathsea

%description -n %{shortname}-pagelayout
The pagelayout class enables you to layout pages declaratively
using simple macros for pages, covers, grids, templates, text,
and graphics to create graphic rich, perfectly typeset, and
print ready PDFs. The integration of Inkscape allows your to
create box shadows. The integration of ImageMagick allows you
to configure compression and sharpening for bitmap graphics to
export web, print or preview versions of your document.
Parallelized image optimization, caching, and a draft mode
enable fast PDF creation and a responsive workflow, even for
large documents with lots of photos and graphics. The
pagelayout class also integrates the Pgf/TikZ and tcolorbox
LaTeX packages.

%package -n %{shortname}-patgen
Summary: Generate hyphenation patterns
Version: svn77830
Provides: texlive-patgen = %{epoch}:%{source_date}-%{release}
Provides: tex-patgen = %{epoch}:%{source_date}-%{release}
Provides: texlive-patgen-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-patgen-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-patgen-bin < 7:20170520
License: LicenseRef-Fedora-Public-Domain
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-patgen
Patgen takes a list of hyphenated words and generates a set of patterns that
can be used by the TeX 82 hyphenation algorithm. Patgen was originally written
by Frank M. Liang as part of his Stanford Ph.D. work, and has always been
distributed alongside the other programs coming from the Stanford TeX project.
It was updated in 1991 by Peter Breitenlohner for the new 8-bit features of TeX
version 3. (These updates related to input/output and programming overhead; the
actual pattern generation algorithms were not changed.) Patgen is currently
maintained as part of TeX Live.

%package -n %{shortname}-pax
Version: svn63509
Provides: texlive-pax = %{epoch}:%{source_date}-%{release}
Provides: tex-pax = %{epoch}:%{source_date}-%{release}
Provides: texlive-pax-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pax-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pax-bin < 7:20170520
Provides: tex-pax-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pax-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pax-doc < 7:20170520
License: GPL-2.0-or-later
Summary: Extract and reinsert PDF annotations with pdfTeX
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(ifpdf.sty)
Requires: tex(graphicx.sty)
Requires: tex(ltxcmds.sty)
Requires: tex(kvsetkeys.sty)
Requires: tex(kvoptions.sty)
Requires: tex(auxhook.sty)
Requires: tex(etexcmds.sty)
# perl
BuildArch: noarch

%description -n %{shortname}-pax
If PDF files are included using pdfTeX, PDF annotations are
stripped. The pax project offers a solution without altering
pdfTeX. A Java program (pax.jar) parses the PDF file that will
later be included. The program then writes the data of the
annotations into a file that can be read by TeX. The LaTeX
package pax extends the graphics package to support the scheme:
if a PDF file is included, the package looks for the file with
the annotation data, reads them and puts the annotations in the
right place.

%package -n %{shortname}-pdfbook2
Summary: Create booklets from PDF files
Version: svn76924
Provides: texlive-pdfbook2 = %{epoch}:%{source_date}-%{release}
Provides: tex-pdfbook2 = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdfbook2-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pdfbook2-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdfbook2-bin < 7:20170520
Provides: tex-pdfbook2-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdfbook2-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdfbook2-doc < 7:20170520
License: GPL-3.0-or-later
# python
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-pdfcrop
Requires: texlive-pdfjam

%description -n %{shortname}-pdfbook2
This python program creates print-ready PDF files from some input PDF files for
booklet printing. The resulting files need to be printed in landscape/long edge
double sided printing. The default paper format depends on the locale and is
chosen by pdfjam. It can be chosen using the --paper option. Before the pdf is
composed, the input file is cropped to the relevant area in order to discard
unnecessary white spaces. In this process, all pages are cropped to the same
dimensions. Extra margins can be defined at the edges of the booklet and in the
middle where the binding occurs. The output is written to INPUT-book.pdf.
Existing files will be overwritten. All input files are processed separately.

%package -n %{shortname}-pdfcrop
Version: svn66862
Provides: texlive-pdfcrop = %{epoch}:%{source_date}-%{release}
Provides: tex-pdfcrop = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdfcrop-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pdfcrop-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdfcrop-bin < 7:20170520
Provides: tex-pdfcrop-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdfcrop-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdfcrop-doc < 7:20170520
License: LPPL-1.3c
Summary: Crop PDF graphics
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-pdftex
# perl
BuildArch: noarch

%description -n %{shortname}-pdfcrop
A Perl script that can either trim pages of any whitespace
border, or trim them of a fixed border.

%package -n %{shortname}-pdfjam
Version: svn75152
Provides: texlive-pdfjam = %{epoch}:%{source_date}-%{release}
Provides: tex-pdfjam = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdfjam-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pdfjam-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdfjam-bin < 7:20170520
Provides: tex-pdfjam-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdfjam-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdfjam-doc < 7:20170520
License: GPL-2.0-or-later
Summary: Shell scripts interfacing to pdfpages
Requires: texlive-base
Requires: texlive-collection-latex
Requires: texlive-kpathsea
Requires: texlive-latex
Requires: tex(pdfpages.sty)
# shell
BuildArch: noarch

%description -n %{shortname}-pdfjam
This is a collection of shell scripts which provide an
interface to the pdfpages LaTeX package. They do such jobs as
selecting pages, concatenating files, doing n-up formatting,
and so on.

%package -n %{shortname}-pdflatexpicscale
Version: svn72650
Provides: texlive-pdflatexpicscale = %{epoch}:%{source_date}-%{release}
Provides: tex-pdflatexpicscale = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdflatexpicscale-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pdflatexpicscale-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdflatexpicscale-bin < 7:20170520
Provides: tex-pdflatexpicscale-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdflatexpicscale-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdflatexpicscale-doc < 7:20170520
License: LPPL-1.3c
Summary: Support software for downscaling graphics to be included by pdfLaTeX
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-pdflatexpicscale
The package provides a script to scale pictures down to a
target resolution before creating a PDF document with pdfLaTeX.

%package -n %{shortname}-pdftex
Summary: A TeX extension for direct creation of PDF
Version: svn77868
Provides: texlive-pdftex = %{epoch}:%{source_date}-%{release}
Provides: tex-pdftex = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdftex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pdftex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdftex-bin < 7:20170520
Provides: tex-pdftex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdftex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdftex-doc < 7:20170520
License: GPL-2.0-or-later
Requires(post,postun): coreutils
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-dehyph
Requires: texlive-etex
Requires: texlive-graphics-def
Requires: texlive-hyph-utf8
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-plain
Requires: texlive-tex-ini-files

%description -n %{shortname}-pdftex
An extension of TeX which can directly generate PDF documents as well as DVI
output. All current free TeX distributions including TeX Live, MacTeX and
MiKTeX include pdfTeX (Plain TeX) and pdfLaTeX (LaTeX), among many other
formats based on the pdfTeX engine.

%package -n %{shortname}-pdftex-quiet
Version: svn49169
Provides: texlive-pdftex-quiet = %{epoch}:%{source_date}-%{release}
Provides: tex-pdftex-quiet = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdftex-quiet-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pdftex-quiet-bin = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-only
Summary: Bash utility to reduce the output of the pdftex command
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-pdftex
#bash
BuildArch: noarch

%description -n %{shortname}-pdftex-quiet
This is a tool in BASH serving to reduce the output of `pdftex` command and see
only relevant errors in red bold font to fight them ASAP.

%package -n %{shortname}-pdftosrc
Summary: Extract source file or stream from PDF file
Version: svn77830
Provides: texlive-pdftosrc = %{epoch}:%{source_date}-%{release}
Provides: tex-pdftosrc = %{epoch}:%{source_date}-%{release}
Provides: tex-pdftosrc-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdftosrc-bin = %{epoch}:%{source_date}-%{release}
License: GPL-2.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-pdftosrc
Extracts an embedded source file, or extracts and uncompresses a PDF stream
given by object number. Developed as part of the pdfTeX source tree.

%package -n %{shortname}-pdfxup
Version: svn71513
Provides: texlive-pdfxup = %{epoch}:%{source_date}-%{release}
Provides: tex-pdfxup = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdfxup-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pdfxup-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdfxup-bin < 7:20170520
Provides: tex-pdfxup-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pdfxup-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pdfxup-doc < 7:20170520
License: LPPL-1.3c
Summary: Create n-up PDF pages with minimal margins
Requires: texlive-base
Requires: texlive-kpathsea
# shell
BuildArch: noarch

%description -n %{shortname}-pdfxup
pdfxup is a unix/linux shell script that creates a PDF document
where each page is obtained by combining several pages of a PDF
file given as output.

%package -n %{shortname}-pedigree-perl
Version: svn64227
Provides: texlive-pedigree-perl = %{epoch}:%{source_date}-%{release}
Provides: tex-pedigree-perl = %{epoch}:%{source_date}-%{release}
Provides: texlive-pedigree-perl-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pedigree-perl-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pedigree-perl-bin < 7:20170520
Provides: tex-pedigree-perl-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pedigree-perl-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pedigree-perl-doc < 7:20170520
License: GPL-2.0-or-later
Summary: Generate TeX pedigree files from CSV files
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-pedigree-perl
This program generates TeX commands to typeset pedigrees --
either TeX fragments or full LaTeX files, to be processed by
the authors' pst-pdgr package. The program has support for
multilanguage pedigrees (at the present moment the English and
Russian languages are supported).

%package -n %{shortname}-perltex
Version: svn73044
Provides: texlive-perltex = %{epoch}:%{source_date}-%{release}
Provides: tex-perltex = %{epoch}:%{source_date}-%{release}
Provides: texlive-perltex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-perltex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-perltex-bin < 7:20170520
Provides: tex-perltex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-perltex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-perltex-doc < 7:20170520
License: LPPL-1.3c
Summary: Define LaTeX macros in terms of Perl code
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-perltex
PerlTeX is a combination Perl script (perltex.pl) and LaTeX2e
package (perltex.sty) that, together, give the user the ability
to define LaTeX macros in terms of Perl code. Once defined, a
Perl macro becomes indistinguishable from any other LaTeX
macro. PerlTeX thereby combines LaTeX's typesetting power with
Perl's programmability. PerlTeX will make use of persistent
named pipes, and thereby run more efficiently, on operating
systems that offer them (mostly Unix-like systems). Also
provided is a switch to generate a PerlTeX-free, document-
specific, noperltex.sty that is useful when distributing a
document to places where PerlTeX is not available.

%package -n %{shortname}-petri-nets
Version: svn39165
Provides: texlive-petri-nets = %{epoch}:%{source_date}-%{release}
Provides: tex-petri-nets = %{epoch}:%{source_date}-%{release}
Provides: texlive-petri-nets-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-petri-nets-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-petri-nets-bin < 7:20170520
Provides: tex-petri-nets-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-petri-nets-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-petri-nets-doc < 7:20170520
License: GPL-1.0-or-later
Summary: A set of TeX/LaTeX packages for drawing Petri nets
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-petri-nets
Petri-nets offers a set of TeX/LaTeX packages about Petri nets
and related models. Three packages are available: the first
allows the user to draw Petri-nets in PostScript documents; the
second defines macros related to PBC, M-nets and B(PN) models;
and a third that combines the other two.

%package -n %{shortname}-pfarrei
Version: svn68950
Provides: texlive-pfarrei = %{epoch}:%{source_date}-%{release}
Provides: tex-pfarrei = %{epoch}:%{source_date}-%{release}
Provides: texlive-pfarrei-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-pfarrei-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pfarrei-bin < 7:20170520
Provides: tex-pfarrei-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pfarrei-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pfarrei-doc < 7:20170520
License: LPPL-1.3c
Summary: LaTeX support of pastors' and priests' work
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(ifpdf.sty)
Requires: tex(pdfpages.sty)
Requires: tex(keyval.sty)
# lua
BuildArch: noarch

%description -n %{shortname}-pfarrei
In "Die TeXnische Komodie" (issue 1/2013) Christian Justen
described his use of LaTeX in his work as priest (similar
requirements may be encountered in the work of pastors and
other ministers of religion). One point was to arrange A5 pages
onto A4 landscape paper, either side-by-side or as a booklet.
Justen made two bash scripts for this job; the package provides
one texlua script for both requirements.

%package -n %{shortname}-pkfix
Version: svn26032
Provides: texlive-pkfix = %{epoch}:%{source_date}-%{release}
Provides: tex-pkfix = %{epoch}:%{source_date}-%{release}
Provides: tex-pkfix-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-pkfix-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pkfix-bin < 7:20170520
Provides: tex-pkfix-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pkfix-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pkfix-doc < 7:20170520
License: LPPL-1.3c
Summary: Replace pk fonts in PostScript with Type 1 fonts
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-pkfix
The perl script pkfix looks for DVIPSBitmapFont comments in
PostScript files, generated by 'not too old' dvips, and
replaces them by type 1 versions of the fonts, if possible.

%package -n %{shortname}-pkfix-helper
Version: svn56061
Provides: texlive-pkfix-helper = %{epoch}:%{source_date}-%{release}
Provides: tex-pkfix-helper = %{epoch}:%{source_date}-%{release}
Provides: tex-pkfix-helper-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-pkfix-helper-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pkfix-helper-bin < 7:20170520
Provides: tex-pkfix-helper-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pkfix-helper-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pkfix-helper-doc < 7:20170520
License: LPPL-1.3c
Summary: Make PostScript files accessible to pkfix
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-pkfix-helper
Pkfix is a useful utility for replacing resolution-dependent
bitmapped fonts in a dvips-produced PostScript file with the
corresponding resolution-independent vector fonts.
Unfortunately, pkfix needs to parse certain PostScript comments
that appear only in files produced by dvips versions later than
5.58 (ca. 1996); it fails to work on PostScript files produced
by older versions of dvips. Pkfix-helper is a program that
attempts to insert newer-dvips comments into an older-dvips
PostScript file, thereby making the file suitable for
processing by pkfix. pkfix-helper can sometimes process
documents fully autonomously but does require the user to
verify and, if needed, correct its decisions.

%package -n %{shortname}-pmx
Version: svn75301
Provides: texlive-pmx = %{epoch}:%{source_date}-%{release}
Provides: tex-pmx = %{epoch}:%{source_date}-%{release}
Provides: tex-pmx-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-pmx-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pmx-bin < 7:20170520
Provides: tex-pmx-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pmx-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pmx-doc < 7:20170520
License: GPL-2.0-or-later
Summary: Preprocessor for MusiXTeX
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-pmx
PMX provides a preprocessor for MusiXTeX. pmxab builds a TeX
input file based on a .pmx input file in a much simpler
language, making most of the layout decisions by itself. It has
most of MusiXTeX's functionality, but it also permits in-line
TeX to give access to virtually all of MusiXTeX. For
proof-listening, pmxab will make a MIDI file of your score.
scor2prt is an auxiliary program that makes parts from a score.

%package -n %{shortname}-pmxchords
Version: svn73868
Provides: texlive-pmxchords = %{epoch}:%{source_date}-%{release}
Provides: tex-pmxchords = %{epoch}:%{source_date}-%{release}
Provides: tex-pmxchords-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-pmxchords-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pmxchords-bin < 7:20170520
Provides: tex-pmxchords-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pmxchords-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pmxchords-doc < 7:20170520
License: GPL-2.0-or-later
Summary: Produce chord information to go with pmx output
Requires: texlive-base
Requires: texlive-kpathsea
# lua
BuildArch: noarch

%description -n %{shortname}-pmxchords
The bundle supplements pmx, providing the means of typesetting
chords above the notes of a score. The bundle contains: macros
for typing the chords; a Lua script to transpose chord macros
to the required key signature; and support scripts for common
requirements.

%package -n %{shortname}-ppmcheckpdf
Version: svn74165
Provides: tex-ppmcheckpdf = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
Summary: Convert PDF to PNG and compare PNG files after l3build
Requires: texlive-base
Requires: texlive-kpathsea
#lua
BuildArch: noarch

%description -n %{shortname}-ppmcheckpdf
The build system l3build normally writes the contents of some
boxes from .lvt files into corresponding .tlg files. Sometimes
a dependent package adds e.g. the command \kern0pt, so that
test files fail, even if the PDF files look the same as before
and are still correct. The ppmcheckpdf tool offers an
alternative option for regression testing: instead of printing
the contents of boxes in .lvt files, PDF files are converted to
PNG files and you can compare the PNG files after l3build has
finished its work.

%package -n %{shortname}-psutils
Version: svn61719
Provides: texlive-psutils = %{epoch}:%{source_date}-%{release}
Provides: tex-psutils = %{epoch}:%{source_date}-%{release}
Provides: tex-psutils-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-psutils-bin = %{epoch}:%{source_date}-%{release}
License: psutils
Summary: The TeXLive fork of the PS Utilities
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-psutils
Utilities for manipulating PostScript documents.
Page selection and rearrangement are supported, including arrangement into
signatures for booklet printing, and page merging for n-up printing.

This package contains a fork of the psutils binaries adjusted for TexLive.
All of the standard binaries have been namespaced with a "tl-" prefix.

%package -n %{shortname}-pst2pdf
Version: svn56172
Provides: texlive-pst2pdf = %{epoch}:%{source_date}-%{release}
Provides: tex-pst2pdf = %{epoch}:%{source_date}-%{release}
Provides: tex-pst2pdf-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-pst2pdf-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pst2pdf-bin < 7:20170520
Provides: tex-pst2pdf-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pst2pdf-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pst2pdf-doc < 7:20170520
License: GPL-2.0-or-later
Summary: A script to compile pstricks documents via pdftex
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-pst2pdf
The script extracts the preamble of the document and runs all
\begin{postscript}...\end{postscript}
\begin{pspicture}...\end{pspicture} and
\pspicture...\endpspicture separately through LaTeX with the
same preamble as the original document; thus it creates EPS,
PNG and PDF files of these snippets. In a final PDFLaTeX run
the script replaces the environments with \includegraphics to
include the processed snippets.

%package -n %{shortname}-pst-pdf
Summary: Make PDF versions of graphics by processing between runs
Version: svn77682
Provides: texlive-pst-pdf = %{epoch}:%{source_date}-%{release}
Provides: tex-pst-pdf = %{epoch}:%{source_date}-%{release}
Provides: tex-pst-pdf-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-pst-pdf-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pst-pdf-bin < 7:20170520
Provides: tex-pst-pdf-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pst-pdf-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pst-pdf-doc < 7:20170520
License: LPPL-1.3c
# shell
BuildArch: noarch
Requires: tex(environ.sty)
Requires: tex(graphicx.sty)
Requires: tex(luatex85.sty)
Requires: tex(preview.sty)
Requires: tex(pstricks.sty)
Requires: texlive-base
Requires: texlive-iftex
Requires: texlive-kpathsea

%description -n %{shortname}-pst-pdf
The package pst-pdf simplifies the use of graphics from PSTricks and other
PostScript code in PDF documents. As in building a bibliography with BibTeX,
additional external programmes are invoked. In this case they are used to
create a PDF file (\PDFcontainer) that will contain all the graphics material.
In the final document these contents will be inserted instead of the original
PostScript code. The package works with pstricks and requires a recent version
of the preview package.

%package -n %{shortname}-ps2eps
Summary: Produce Encapsulated PostScript from PostScript
Version: svn76924
Provides: texlive-ps2eps = %{epoch}:%{source_date}-%{release}
Provides: tex-ps2eps = %{epoch}:%{source_date}-%{release}
License: GPL-2.0-or-later
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-ps2eps
Produce Encapsulated PostScript Files (EPS/EPSF) from a one-page PostScript
document, or any PostScript document. A correct Bounding Box is calculated for
the EPS files and some PostScript command sequences that can produce erroneous
results on printers are filtered. The input is cropped to include just the
image contained in the PostScript file. The EPS files can then be included into
TeX documents. Other programs like ps2epsi (a script distributed with
ghostscript) don't always calculate the correct bounding box (because the
values are put on the PostScript stack which may get corrupted by bad
PostScript code) or they round it off, resulting in clipping the image.
Therefore ps2eps uses a resolution of 144 dpi to get the correct bounding box.
The bundle includes binaries for Linux, Solaris, Digital Unix or Windows
2000/9x/NT; for other platforms, the user needs perl, ghostscript and an ANSI-C
compiler. Included in the distribution is the bbox program, an application to
produce Bounding Box values for rawppm or rawpbm format files.

%package -n %{shortname}-ps2pk
Summary: Generate a PK font from an Adobe Type 1 font
Version: svn75712
Provides: texlive-ps2pk = %{epoch}:%{source_date}-%{release}
Provides: tex-ps2pk = %{epoch}:%{source_date}-%{release}
Provides: tex-ps2pk-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-ps2pk-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ps2pk-bin < 7:20170520
Provides: texlive-ps2pkm = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ps2pkm < 7:20170520
Provides: texlive-ps2pkm-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ps2pkm-bin < 7:20170520
License: MIT
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-ps2pk
Generates a PK file from an Adobe Type 1 font. PK fonts are (or used to be)
valuable in enabling previewers to view documents generated that use Type 1
fonts. The program makes use of code donated to the X consortium by IBM. It is
now maintained as part of TeX Live.

%package -n %{shortname}-ptex
Summary: A TeX system for publishing in Japanese
Version: svn77830
Provides: texlive-ptex = %{epoch}:%{source_date}-%{release}
Provides: tex-ptex = %{epoch}:%{source_date}-%{release}
Provides: tex-ptex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-ptex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ptex-bin < 7:20170520
Provides: tex-ptex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ptex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ptex-doc < 7:20170520
Provides: texlive-platex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-platex-bin < 7:20170520
License: BSD-3-Clause
Requires(post,postun): coreutils
Requires: tex(oldlfont.sty)
Requires: tex(shortvrb.sty)
Requires: texlive-adobemapping
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-etex
Requires: texlive-hyph-utf8
Requires: texlive-hyphen-base
Requires: texlive-ipaex
Requires: texlive-japanese-otf
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-latex
Requires: texlive-plain
Requires: texlive-ptex-base
Requires: texlive-ptex-fonts
Requires: texlive-tex
Requires: texlive-uptex

%description -n %{shortname}-ptex
pTeX adds features related to vertical writing, and deals with other problems
in typesetting Japanese. A manual (in both Japanese and English) is distributed
as package pTeX-manual.

%package -n %{shortname}-ptex-fontmaps
Version: svn65953
Provides: texlive-ptex-fontmaps = %{epoch}:%{source_date}-%{release}
Provides: tex-ptex-fontmaps = %{epoch}:%{source_date}-%{release}
Provides: tex-ptex-fontmaps = %{epoch}:%{source_date}-%{release}
Provides: texlive-ptex-fontmaps-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ptex-fontmaps-bin < 7:20170520
Provides: tex-ptex-fontmaps-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ptex-fontmaps-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ptex-fontmaps-doc < 7:20170520
Provides: tex-jfontmaps = %{epoch}:%{source_date}-%{release}
Provides: texlive-jfontmaps = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-jfontmaps <= 6:svn40613
Provides: tex-jfontmaps-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-jfontmaps-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-jfontmaps-bin <= 6:svn29848.0
Provides: tex-jfontmaps-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-jfontmaps-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-jfontmaps-doc <= 6:svn40613
License: GPL-3.0-only
Summary: Font maps and configuration tools for Japanese/Chinese/Korean fonts with (u)ptex
Requires: texlive-arphic-ttf
Requires: texlive-baekmuk
Requires: texlive-base
Requires: texlive-ipaex
Requires: texlive-kpathsea
# shell and perl
BuildArch: noarch

%description -n %{shortname}-ptex-fontmaps
This package provides font maps and setup tools for Japanese,
Korean, Traditional Chinese, and Simplified Chinese. It is the
successor of the jfontmaps package. The files in this package
contain font maps for dvipdfmx to make various
Japanese/Chinese/Korean fonts available for (u)ptex and related
programs and formats.

%package -n %{shortname}-ptex2pdf
Version: svn65953
Provides: texlive-ptex2pdf = %{epoch}:%{source_date}-%{release}
Provides: tex-ptex2pdf = %{epoch}:%{source_date}-%{release}
Provides: tex-ptex2pdf-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-ptex2pdf-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ptex2pdf-bin < 7:20170520
Provides: tex-ptex2pdf-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ptex2pdf-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ptex2pdf-doc < 7:20170520
License: GPL-2.0-or-later
Summary: Convert Japanese TeX documents to PDF
Requires: texlive-base
Requires: texlive-kpathsea
# lua
BuildArch: noarch

%description -n %{shortname}-ptex2pdf
The Lua script provides system-independent support of Japanese
typesetting engines in TeXworks. As TeXworks typesetting setup
does not allow for multistep processing, this script runs one
of the ptex-based programs (ptex, uptex, eptex, platex,
uplatex) followed by dvipdfmx.

%package -n %{shortname}-purifyeps
Version: svn29725
Provides: texlive-purifyeps = %{epoch}:%{source_date}-%{release}
Provides: tex-purifyeps = %{epoch}:%{source_date}-%{release}
Provides: tex-purifyeps-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-purifyeps-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-purifyeps-bin < 7:20170520
Provides: tex-purifyeps-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-purifyeps-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-purifyeps-doc < 7:20170520
License: LPPL-1.3c
Summary: Make EPS work with both LaTeX/dvips and pdfLaTeX
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-purifyeps
While pdfLaTeX has a number of nice features, its primary
shortcoming relative to standard LaTeX+dvips is that it is
unable to read ordinary Encapsulated PostScript (EPS) files,
the most common graphics format in the LaTeX world. Purifyeps
converts EPS files into a 'purified' form that can be read by
both LaTeX+dvips and pdfLaTeX. The trick is that the standard
LaTeX2e graphics packages can parse MetaPost-produced EPS
directly. Hence, purifyeps need only convert an arbitrary EPS
file into the same stylized format that MetaPost outputs.

%package -n %{shortname}-pygmentex
Version: svn64131
Provides: texlive-pygmentex = %{epoch}:%{source_date}-%{release}
Provides: tex-pygmentex = %{epoch}:%{source_date}-%{release}
Provides: tex-pygmentex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-pygmentex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pygmentex-bin < 7:20170520
Provides: tex-pygmentex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pygmentex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pythontex-doc < 7:20170520
License: LPPL-1.3c
Summary: Use Pygments to format code listings in documents
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(fancyvrb.sty)
Requires: tex(color.sty)
Requires: tex(ifthen.sty)
Requires: tex(caption.sty)
Requires: tex(pgfkeys.sty)
Requires: tex(efbox.sty)
Requires: tex(mdframed.sty)
Requires: tex(fvextra.sty)
Requires: tex(shellesc.sty)
# python
BuildArch: noarch

%description -n %{shortname}-pygmentex
PygmenTeX is a Python-based LaTeX package that can be used for
typesetting code listings in a LaTeX document using Pygments.
Pygments is a generic syntax highlighter for general use in all
kinds of software such as forum systems, wikis or other
applications that need to prettify source code.

%package -n %{shortname}-pythontex
Summary: Run Python from within a document, typesetting the results
Version: svn77873
Provides: texlive-pythontex = %{epoch}:%{source_date}-%{release}
Provides: tex-pythontex = %{epoch}:%{source_date}-%{release}
Provides: tex-pythontex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-pythontex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pythontex-bin < 7:20170520
Provides: tex-pythontex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-pythontex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-pythontex-doc < 7:20170520
License: LPPL-1.3c AND BSD-3-Clause
# python
BuildArch: noarch
Requires: tex(currfile.sty)
Requires: tex(etex.sty)
Requires: tex(etoolbox.sty)
Requires: tex(fancyvrb.sty)
Requires: tex(fvextra.sty)
Requires: tex(newfloat.sty)
Requires: tex(pgfopts.sty)
Requires: tex(upquote.sty)
Requires: tex(xcolor.sty)
Requires: tex(xstring.sty)
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-pythontex
The package allows you to enter Python code within a LaTeX document, execute
the code, and access its output in the original document. There is also support
for Bash, JavaScript, Julia, Octave, Perl, R, Raku (Perl 6), Ruby, Rust, and
SageMath. Code is only executed when it has been modified, or when it meets
user-specified criteria. Code may be divided into user-defined sessions, which
automatically run in parallel. Errors and warnings are synchronized with the
LaTeX document, so that they refer to the document's line numbers. External
dependencies can be tracked, so that code is re-executed when the data it
depends on is modified. PythonTeX also provides syntax highlighting for code in
LaTeX documents via the Pygments syntax highlighter. The package provides a
depythontex utility. This creates a copy of the document in which all Python
code has been replaced by its output. This is useful for journal submissions,
sharing documents, and conversion to other formats.

%package -n %{shortname}-rubik
Version: svn46791
Provides: texlive-rubik = %{epoch}:%{source_date}-%{release}
Provides: tex-rubik = %{epoch}:%{source_date}-%{release}
Provides: tex-rubik-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-rubik-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-rubik-bin < 7:20170520
Provides: tex-rubik-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-rubik-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-rubik-doc < 7:20170520
License: LPPL-1.3c
Summary: Document Rubik cube configurations and rotation sequences
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(fancyvrb.sty)
Requires: tex(forarray.sty)
Requires: tex(ifluatex.sty)
Requires: tex(ifthen.sty)
Requires: tex(shellesc.sty)
Requires: tex(tikz.sty)
# perl
BuildArch: noarch

%description -n %{shortname}-rubik
The bundle provides two packages: rubikcube provides commands
for typesetting Rubik cubes and their transformations; and
rubikrotation which can process a sequence of Rubik rotation
moves, with the help of a Perl package executed via \write18
(shell escape) commands.

%package -n %{shortname}-runtexfile
Summary: Automate the process of compiling (La)TeX documents with index, bibliography...
Version: svn76526
License: LPPL-1.3c
Requires: texlive-base
Requires: texlive-kpathsea
# lua
BuildArch: noarch

%description -n %{shortname}-runtexfile
This package provides a small script like latexmk to run a TeX or LaTeX
document controlled from within the document itself. The commands have to be
defined at the beginning of the document, e.g.: %! HV lualatex --shell-escape
%! HV biber %! HV lualatex --shell-escape %! HV xindex %! HV xindex --config
DIN2 -l DE -o test2.vwd %! HV xindex --config DIN2 -l DE -o test2.dbd %! HV
lualatex --shell-escape %! HV lualatex --shell-escape \documentclass[...]{...}
... The script itself does not parse the log file.

%package -n %{shortname}-runtexshebang
Version: svn68882
Provides: tex-runtexshebang = %{epoch}:%{source_date}-%{release}
License: MIT
Summary: A Lua script running LaTeX document files with TeX-style shebang
Requires: texlive-base
Requires: texlive-kpathsea
# lua
BuildArch: noarch

%description -n %{shortname}-runtexshebang
In short, a TeX-style shebang (%#!) is a special kind of TeX
comment that you include in your TeX/LaTeX document file to
tell the operating system's shell how to run the file for the
rest of the file: %#!lualatex foo.tex \documentclass{article}
\begin{document} Hello, {\LaTeX} World! Happy {\TeX}ing.
\end{document} If you are using a TeX-style shebang, it must
appear on the line that matched 20 lines or less in your LaTeX
document, and it has to start with a TeX comment symbol (%)
followed by a hash sign (#) and an exclamation mark (!),
colloquially known as the bang, hence the name shebang for
TeX/LaTeX.

%package -n %{shortname}-seetexk
Version: svn57972
Provides: texlive-seetexk = %{epoch}:%{source_date}-%{release}
Provides: tex-seetexk = %{epoch}:%{source_date}-%{release}
Provides: tex-seetexk-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-seetexk-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-seetexk-bin < 7:20170520
License: MIT
Summary: Utilities for manipulating DVI files
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-seetexk
The collection comprises: dvibook, which will rearrange the
pages of a DVI file into 'signatures' as used when printing a
book; dviconcat, for concatenating pages of DVI file(s);
dviselect, which will select pages from one DVI file to create
a new DVI file; dvitodvi, which will rearrange the pages of a
DVI file to create a new file; and libtex, a library for
manipulating the files, from the old SeeTeX project. The
utilities are provided as C source with Imakefiles, and an MS-
DOS version of dvibook is also provided.

%package -n %{shortname}-show-pdf-tags
Summary: Extract PDF tags from tagged PDF files
Version: svn77604
License: MIT
Requires: texlive-base
Requires: texlive-kpathsea
# lua
BuildArch: noarch

%description -n	%{shortname}-show-pdf-tags
This package provides a tool to make the structure of tagged PDF files visible.
It parses a PDF file and extracts most tagging related information to turn it
into either a visual tree structure or an XML document representing the tags.
The package is released together with a collection of schemas which can be used
to check that the resulting XML structure follows specified rules.


%package -n %{shortname}-spix
Version: svn65050
Provides: texlive-spix = %{epoch}:%{source_date}-%{release}
Summary: Yet another TeX compilation tool: simple, human readable, no option, no magic
License: GPL-3.0-or-later
Requires: texlive-base texlive-kpathsea

%description -n %{shortname}-spix
SpiX offers a way to store information about the compilation
process for a tex file inside the tex file itself. Just write
the commands as comments in the tex files, and SpiX will
extract and run those commands. Everything is stored in the tex
file (so that you are not missing some piece of information
that is located somewhere else), in a human-readable format (no
need to know SpiX to understand it).

%package -n %{shortname}-splitindex
Summary: Unlimited number of indexes
Version: svn77682
Provides: texlive-splitindex = %{epoch}:%{source_date}-%{release}
Provides: tex-splitindex = %{epoch}:%{source_date}-%{release}
Provides: tex-splitindex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-splitindex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-splitindex-bin < 7:20170520
Provides: tex-splitindex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-splitindex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-splitindex-doc < 7:20170520
License: LPPL-1.3c
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-splitindex
SplitIndex consists of a LaTeX package, splitidx, and a small program,
splitindex. The package may be used to produce one index or several indexes.
Without splitindex (for example, using the index package), the number of
indexes is limited by the number of TeX's output streams. But using the program
you may use even more than 16 indexes: splitidx outputs only a single file
\jobname.idx and the program splits that file into several raw index files and
calls your favorite index processor for each of the files.

%package -n %{shortname}-sqltex
Version: svn72396
Provides: tex-sqltex = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
Summary: An SQL Preprocessor for LaTeX
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-sqltex
SQLTeX is a preprocessor that enables the use of SQL statements
in LaTeX. The SQLTeX perl script reads an input file containing
the LaTeX source with SQL commands, and writes a LaTeX file in
which the SQL commands have been replaced by the values from
their execution. It is possible to select a field for
substitution in your LaTeX document, or to be used as input in
another SQL command. (When an SQL command returns multiple
fields and/or rows, the values can only be used within the
document.) The default is to use MySQL databases, but Pg,
Sybase, Oracle, Ingres, mSQL and PostgreSQL are also supported.

%package -n %{shortname}-srcredact
Version: svn38710
Provides: texlive-srcredact = %{epoch}:%{source_date}-%{release}
Provides: tex-srcredact = %{epoch}:%{source_date}-%{release}
Provides: tex-srcredact-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-srcredact-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-srcredact-bin < 7:20170520
Provides: tex-srcredact-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-srcredact-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-srcredact-doc < 7:20170520
License: GPL-2.0-or-later
Summary: A tool for redacting sources
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-srcredact
This package provides a tool to keep a master source,
consisting of different "chunks" intended for different
audiences. The tool allows to extract the versions intended for
different audiences and to incorporate the changes made in any
of these versions into the master document. This work was
commissioned by the Consumer Financial Protection Bureau,
United States Treasury.

%package -n %{shortname}-sty2dtx
Summary: Create a .dtx file from a .sty file
Version: svn76924
Provides: texlive-sty2dtx = %{epoch}:%{source_date}-%{release}
Provides: tex-sty2dtx = %{epoch}:%{source_date}-%{release}
Provides: tex-sty2dtx-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-sty2dtx-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-sty2dtx-bin < 7:20170520
Provides: tex-sty2dtx-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-sty2dtx-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-sty2dtx-doc < 7:20170520
License: GPL-3.0-or-later
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-sty2dtx
The package provides a Perl script that converts a .sty file (LaTeX package) to
.dtx format (documented LaTeX source), by surrounding macro definitions with
macro and macrocode environments. The macro name is automatically inserted as
an argument to the macro environment. Code lines outside macro definitions are
wrapped only in macrocode environments. Empty lines are removed. The script
should not be thought to be fool proof and 100% accurate but rather as a good
start to the business of making a .dtx file from an undocumented style file.
Full .dtx files are generated. A template based on the skeleton file from
dtxtut is used. User level macros are added automatically to the "Usage"
section of the .dtx file. A corresponding .ins file can be generated as well.

%package -n %{shortname}-svn-multi
Version: svn64967
Provides: texlive-svn-multi = %{epoch}:%{source_date}-%{release}
Provides: tex-svn-multi = %{epoch}:%{source_date}-%{release}
Provides: tex-svn-multi-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-svn-multi-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-svn-multi-bin < 7:20170520
Provides: tex-svn-multi-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-svn-multi-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-svn-multi-doc < 7:20170520
License: LPPL-1.3c
Summary: Subversion keywords in multi-file LaTeX documents
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(kvoptions.sty)
Requires: tex(filehook.sty)
Requires: tex(currfile.sty)
Requires: tex(graphics.sty)
Requires: tex(pgf.sty)
# perl
BuildArch: noarch

%description -n %{shortname}-svn-multi
This package lets you typeset keywords of the version control
system Subversion inside your LaTeX files anywhere you like.
Unlike the otherwise similar package svn the use of multiple
files for one LaTeX document is well supported. The package
uses the author's filehook and currfile packages. The package
interacts with an external Perl script, to retrieve information
necessary for the required output.

%package -n %{shortname}-synctex
Version: svn66203
Provides: texlive-synctex = %{epoch}:%{source_date}-%{release}
Provides: tex-synctex = %{epoch}:%{source_date}-%{release}
Provides: tex-synctex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-synctex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-synctex-bin < 7:20170520
License: LPPL-1.3c
Summary: engine-level feature synchronizing output and source
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-synctex
SyncTeX allows navigating between the TeX source and (usually
PDF) output, in both directions, given a SyncTeX-aware front
end. It is compiled into most engines and can be enabled with
the --synctex=1 option. It is developed as part of TeX Live.

%package -n %{shortname}-tex
Summary: A sophisticated typesetting engine
Version: svn77830
Provides: texlive-tex = %{epoch}:%{source_date}-%{release}
Provides: tex-tex = %{epoch}:%{source_date}-%{release}
Provides: tex-tex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-tex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tex-bin < 7:20170520
License: Knuth-CTAN
Requires(post,postun): coreutils
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-plain

%description -n %{shortname}-tex
TeX is a typesetting system that incorporates a macro processor. A TeX source
document specifies or incorporates a number of macro definitions that instruct
the TeX engine how to typeset the document. The TeX engine also uses font
metrics generated by Metafont, or by any of several other mechanisms that
incorporate fonts from other sources into an environment suitable for TeX. TeX
has been, and continues, a basis and an inspiration for several other programs,
including e-TeX and PDFTeX. The distribution includes the source of Knuth's TeX
book; this source is there to read, as an example of writing TeX -- it should
not be processed without Knuth's direct permission.

%package -n %{shortname}-tex4ebook
Summary: Converter from LaTeX to ebook formats
Version: svn78132
Provides: texlive-tex4ebook = %{epoch}:%{source_date}-%{release}
Provides: tex-tex4ebook = %{epoch}:%{source_date}-%{release}
Provides: tex-tex4ebook-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-tex4ebook-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tex4ebook-bin < 7:20170520
Provides: tex-tex4ebook-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-tex4ebook-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tex4ebook-doc < 7:20170520
License: LPPL-1.3c
# lua
BuildArch: noarch
Requires: tex(etoolbox.sty)
Requires: tex(graphicx.sty)
Requires: tex(kvoptions.sty)
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-make4ht
Requires: texlive-tex4ht

%description -n %{shortname}-tex4ebook
This is a bundle of Lua scripts and LaTeX packages for conversion of LaTeX
files to ebook formats such as epub, mobi and epub3. tex4ht is used as the
conversion engine.

%package -n %{shortname}-tex4ht
Summary: Convert (La)TeX to HTML/XML
Version: svn78343
Provides: texlive-tex4ht = %{epoch}:%{source_date}-%{release}
Provides: tex-tex4ht = %{epoch}:%{source_date}-%{release}
Provides: tex-tex4ht-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-tex4ht-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tex4ht-bin < 7:20170520
Provides: tex-tex4ht-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-tex4ht-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tex4ht-doc < 7:20170520
License: LPPL-1.3c
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-tex4ht
A converter from TeX and LaTeX to SGML-based formats such as (X)HTML, MathML,
OpenDocument, and Docbook, providing a configurable (La)TeX-based authoring
system for hypertext. TeX4ht does not independently parse (La)TeX source (so it
avoids the difficulties encountered by many other converters, arising from the
irregularity of (La)TeX syntax). Instead, TeX4ht uses (La)TeX itself (with
myriad macro modifications) to produce a helper DVI file that it can then
process. This technique allows TeX4ht to approach the robustness characteristic
of restricted-syntax systems such as gellmu. Full releases of TeX4ht are no
longer made, both because it is technically difficult to do so and because
their utility is questionable. Nevertheless, TeX4ht is actively maintained. So,
current source files are held on CTAN, and updated from the development
repository frequently. Creating the myriad derived files from them is
nontrivial, and generally done with the Makefile in development, from which the
TeX4ht package in TeX Live is updated.

%package -n %{shortname}-texaccents
Summary: Convert composite accented characters to Unicode
Version: svn64447
License: MIT
Requires: texlive-base texlive-kpathsea
Requires: snobol4
# snobol4
BuildArch: noarch

%description -n %{shortname}-texaccents
This small utility, written in SNOBOL, converts the composition
of special characters to Unicode, e. g. \"{a} - a, \k{a} - a,
...

%package -n %{shortname}-texblend
Summary: Compile segments of LaTeX documents
Version: svn68961
License: LPPL-1.3c
Provides: tex-texblend = %{epoch}:%{source_date}-%{release}
Requires: texlive-base texlive-kpathsea texlive-luatex
# lua
BuildArch: noarch

%description -n %{shortname}-texblend
This tool compiles individual files that are included as parts
of larger documents. It utilizes the preamble of the main
document but disregards all other included files. The main
purpose is to allow fast compilation of particular chapters or
sections, eliminating the need to recompile the entire
document. This facilitates an efficient way to check for
formatting or syntax errors in the particular part of the
document being worked on.

%package -n %{shortname}-texcount
Version: svn49013
Provides: texlive-texcount = %{epoch}:%{source_date}-%{release}
Provides: tex-texcount = %{epoch}:%{source_date}-%{release}
Provides: tex-texcount-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texcount-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texcount-bin < 7:20170520
Provides: tex-texcount-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texcount-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texcount-doc < 7:20170520
License: LPPL-1.3c
Summary: Count words in a LaTeX document
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-texcount
TeXcount is a Perl script that counts words in the text of
LaTeX files. It has rules for handling most of the common
macros, and can provide colour-coded output showing which parts
of the text have been counted. The package script is available
as a Web service via its home page.

%package -n %{shortname}-texdef
Version: svn74067
Provides: texlive-texdef = %{epoch}:%{source_date}-%{release}
Provides: tex-texdef = %{epoch}:%{source_date}-%{release}
Provides: tex-texdef-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texdef-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texdef-bin < 7:20170520
Provides: tex-texdef-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texdef-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texdef-doc < 7:20170520
License: GPL-3.0-or-later
Summary: Display the definitions of TeX commands
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-texdef
The (Perl) script displays the definition of (La)TeX command
sequences/macros. Various options allow the selection of the
used class and package files and other things which can have
influence on the definition (before/after the preamble, inside
an environment, ...). The script creates a temporary TeX file
which is then compiled using (La)TeX to find the '\meaning' of
the command sequence. The result is formatted and presented to
the user. Length or number command sequences (dimensions,
\char..., count registers, ...) are recognized and the
contained value is also shown (using \the). Special definitions
like protected macros are also recognized and the underlying
macros are shown as well. The script will show plain TeX
definitions by default. LaTeX and ConTeXt are supported,
including flavours (pdf(la)tex, lua(la)tex, xe(la)tex, ...).
The flavour can be selected using an command line option or
over the script name: latexdef will use LaTeX as default, etc.

%package -n %{shortname}-texdiff
Version: svn29752
Provides: texlive-texdiff = %{epoch}:%{source_date}-%{release}
Provides: tex-texdiff = %{epoch}:%{source_date}-%{release}
Provides: tex-texdiff-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texdiff-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texdiff-bin < 7:20170520
Provides: tex-texdiff-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texdiff-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texdiff-doc < 7:20170520
License: GPL-1.0-or-later
Summary: Compares two (La)TeX documents to create a merged version showing changes
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-texdiff
Texdiff compares two (La)TeX documents to create a merged version showing
changes, similar to that of 'Change Tracking' in some word processors.

%package -n %{shortname}-texdirflatten
Version: svn55064
Provides: texlive-texdirflatten = %{epoch}:%{source_date}-%{release}
Provides: tex-texdirflatten = %{epoch}:%{source_date}-%{release}
Provides: tex-texdirflatten-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texdirflatten-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texdirflatten-bin < 7:20170520
License: GPL-1.0-or-later
Summary: Collect files related to a LaTeX job in a single directory
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-texdirflatten
The Perl script parses a LaTeX file recursively, scanning all
child files, and collects details of any included and other
data files. These component files, are then all put into a
single directory (thus "flattening" the document's directory
tree).

%package -n %{shortname}-texdoc
Version: svn73876
Provides: texlive-texdoc = %{epoch}:%{source_date}-%{release}
Provides: tex-texdoc = %{epoch}:%{source_date}-%{release}
Provides: tex-texdoc-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texdoc-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texdoc-bin < 7:20170520
Provides: tex-texdoc-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texdoc-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texdoc-doc < 7:20170520
License: GPL-1.0-or-later
Summary: Documentation access for TeX distributions
Requires: texlive-base
Requires: texlive-kpathsea
# lua and perl
BuildArch: noarch

%description -n %{shortname}-texdoc
texdoc is a Lua script providing easy access to the
documentation in TeX Live: PDF, DVI, plain text files, and
more. Viewing and other configuration can be extensively
customized. It is distributed with TeX Live; MiKTeX provides a
program by the same name to do the same job, but its
implementation is unrelated.

%package -n %{shortname}-texdoctk
Version: svn62186
Provides: texlive-texdoctk = %{epoch}:%{source_date}-%{release}
Provides: tex-texdoctk = %{epoch}:%{source_date}-%{release}
Provides: tex-texdoctk-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-texdoctk-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texdoctk-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texdoctk-doc = %{epoch}:%{source_date}-%{release}
License: GPL-1.0-or-later
Summary: Easy access to package documentation
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-texdoctk
A Perl/Tk-based GUI for easy access to package documentation
for TeX on Unix platforms; the databases it uses are based on
the texmf/doc subtrees of teTeX, but database files for local
configurations with modified/extended directories can be
derived from them. Note that texdoctk is not a viewer itself,
but an interface for finding documentation files and opening
them with the appropriate viewer; so it relies on appropriate
programs to be installed on the system. However, the choice of
these programs can be configured by the sysadmin or user. Now
only distributed as part of TeX Live, which includes a Windows
executable.

%package -n %{shortname}-texfindpkg
Version: svn72937
Provides: tex-texfindpkg = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
Summary: Query or install TeX packages and their dependencies
Requires: texlive-base
Requires: texlive-kpathsea
# lua
BuildArch: noarch

%description -n %{shortname}-texfindpkg
This package makes it easy to query or install TeX packages and
their dependencies by file names, command names or environment
names. TeXFindPkg supports both TeX Live and MiKTeX
distributions. At present it focuses mainly on LaTeX packages,
but may be extended to ConTeXt packages if anyone would like to
contribute.

%package -n %{shortname}-texfot
Summary: Filter clutter from the output of a TeX run
Version: svn77286
Provides: texlive-texfot = %{epoch}:%{source_date}-%{release}
Provides: tex-texfot = %{epoch}:%{source_date}-%{release}
Provides: tex-texfot-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texfot-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texfot-bin < 7:20170520
Provides: tex-texfot-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texfot-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texfot-doc < 7:20170520
License: LicenseRef-Fedora-Public-Domain
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-texfot
The package provides a small Perl script to filter the online output from a TeX
run, attempting to show only those messages which probably deserve some change
in the source. The TeX invocation itself need not change.

%package -n %{shortname}-texliveonfly
Summary: On-the-fly download of missing TeX Live packages
Version: svn76924
Provides: texlive-texliveonfly = %{epoch}:%{source_date}-%{release}
Provides: tex-texliveonfly = %{epoch}:%{source_date}-%{release}
Provides: tex-texliveonfly-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texliveonfly-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texliveonfly-bin < 7:20170520
Provides: tex-texliveonfly-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texliveonfly-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texliveonfly-doc < 7:20170520
License: GPL-3.0-or-later
# python
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-texliveonfly
The package provides a script that performs 'on the fly' downloads of missing
packages, while a document is being compiled. (This feature is already
available in the MiKTeX distribution for Windows machines.) To use the script,
replace your (LaTeX) compilation command with texliveonfly.py file.tex (default
options are --engine=pdflatex and --arguments="-synctex=1
-interaction=nonstopmode", which may all be changed). The script is designed to
work on Linux distributions.

%package -n %{shortname}-texlive-en
Summary: TeX Live manual (English)
Version: svn78030
Provides: texlive-texlive-en = %{epoch}:%{source_date}-%{release}
Provides: tex-texlive-en = %{epoch}:%{source_date}-%{release}
Provides: tex-texlive-en-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texlive-en-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texlive-en-doc < 7:20170520
License: LPPL-1.3c
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-texlive-en
TeX Live manual (English)

%package -n %{shortname}-texlive-scripts
Summary: TeX Live infrastructure programs
Version: svn78361
Provides: texlive-texlive-scripts = %{epoch}:%{source_date}-%{release}
Provides: tex-texlive-scripts = %{epoch}:%{source_date}-%{release}
Provides: texlive-texlive-scripts-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texlive-scripts-bin < 7:20170520
Provides: texlive-tetex = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tetex < 7:20200327
License: LPPL-1.3c
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-gsftopk
Requires: texlive-kpathsea = %{epoch}:%{source_date}-%{release}
Requires: texlive-texlive.infra

%description -n %{shortname}-texlive-scripts
Includes install-tl, tl-portable, rungs, etc.; not needed for tlmgr to run but
still ours. Not included in tlcritical.

%package -n %{shortname}-texlive-scripts-extra
Summary: TeX Live scripts
Version: svn78162
Provides: texlive-texlive-scripts-extra = %{epoch}:%{source_date}-%{release}
Provides: tex-texlive-scripts-extra = %{epoch}:%{source_date}-%{release}
Provides: texlive-texlive-scripts-extra-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texconfig < 7:20200327
Obsoletes: texlive-pstools < 7:20200327
Obsoletes: texlive-pdftools < 7:20200327
License: GPL-1.0-or-later AND LPPL-1.3c AND LicenseRef-Fedora-Public-Domain
# perl and shell
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-texlive.infra

%description -n %{shortname}-texlive-scripts-extra
Miscellaneous scripts maintained as part of TeX Live, but not important for the
infrastructure. Thus, this is not part of scheme-infraonly or tlcritical, just
a normal package.

%package -n %{shortname}-texlive.infra
Summary: Basic TeX Live infrastructure
Version: svn78313
Provides: texlive-texlive.infra = %{epoch}:%{source_date}-%{release}
Provides: tex-texlive.infra = %{epoch}:%{source_date}-%{release}
Provides: tex-texlive.infra-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texlive.infra-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texlive.infra-bin < 7:20170520
Provides: tex-texlive.infra-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texlive.infra-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texlive.infra-doc < 7:20170520
License: LPPL-1.3c
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-texlive.infra
This package contains the files needed to get tlmgr running: perl modules, xz
binaries, plus (sometimes) tar, wget, lz4, and various other support files.
This package also represents the tlcritical recovery scripts. The standalone
installer is close, but not the same; it's defined in 00texlive.installer.

%package -n %{shortname}-texloganalyser
Version: svn54526
Provides: texlive-texloganalyser = %{epoch}:%{source_date}-%{release}
Provides: tex-texloganalyser = %{epoch}:%{source_date}-%{release}
Provides: tex-texloganalyser-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texloganalyser-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texloganalyser-bin < 7:20170520
Provides: tex-texloganalyser-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texloganalyser-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texloganalyser-doc < 7:20170520
License: BSD-3-Clause
Summary: Analyse TeX logs
Requires: texlive-base
Requires: texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-texloganalyser
The perl script allows the user to extract (and display)
elements of the log file.

%package -n %{shortname}-texlogfilter
Version: svn71525
Provides: texlive-texlogfilter = %{epoch}:%{source_date}-%{release}
Provides: texlive-texlogfilter-bin = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
Summary: Filter LaTeX engines output or log file
Requires: texlive-base, texlive-kpathsea
# perl
BuildArch: noarch

%description -n %{shortname}-texlogfilter
texlogfilter is a Perl script designed to filter LaTeX engines output or log
file (LaTeX, pdfLaTeX, LuaLaTeX or XeLaTeX). It reduces the LaTeX output or log
to keep only warnings and errors. The result is colorised. Options allow to
mask specific warnings, such as box or references/citations warnings. It's also
possible to add custom filter patterns.

%package -n %{shortname}-texlogsieve
Summary: Filter and summarize LaTeX log files
Version: svn77351
Provides: texlive-texlogsieve = %{epoch}:%{source_date}-%{release}
Provides: texlive-texlogsieve-bin = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
# lua
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-texlogsieve
texlogsieve reads a LaTeX log file (or the standard input if no file is
specified), filters out less relevant messages, and displays a summary report.
It is a texlua script, similar in spirit to tools such as texfot,
texloganalyser, rubber-info, textlog_extract, texlogparser, texlogfilter, pulp,
and others. Highlights: Two reports: the most important messages from the log
file followed by a summary of repeated messages, undefined references etc.; The
program goes to great lengths to correctly handle TeX line wrapping and does a
much better job at that than existing tools; Multiline messages are treated as
a single entity; Several options to control which messages should be filtered
out; No messages are accidentally removed; The summary report is currently
simple, but useful.

%package -n %{shortname}-texosquery
Summary: Cross-platform Java application to query OS information
Version: svn77682
Provides: texlive-texosquery = %{epoch}:%{source_date}-%{release}
Provides: tex-texosquery = %{epoch}:%{source_date}-%{release}
Provides: tex-texosquery-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texosquery-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texosquery-bin < 7:20170520
Provides: tex-texosquery-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texosquery-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texosquery-doc < 7:20170520
License: LPPL-1.3c
# shell
BuildArch: noarch
Requires: java-headless
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-texosquery
This package provides a cross-platform Java application to query OS information
designed for use in TeX's shell escape mechanism. The application can query the
following: locale and codeset current working directory user home directory
temporary directory OS name, arch and version Current date and time in PDF
format (for TeX formats that don't provide \pdfcreationdate) Date-time stamp of
a file in PDF format (for TeX formats that don't provide \pdffilemoddate) Size
of a file in bytes (for TeX formats that don't provide \pdffilesize) Contents
of a directory (captured as a list) Directory contents filtered by regular
expression (captured as a list) URI of a file Canonical path of a file All
paths use a forward slash as directory divider so results can be used, for
example, in commands like \includegraphics. There are files provided for easy
access in TeX documents: texosquery.tex: generic TeX code texosquery.sty: LaTeX
package This provides commands to run texosquery using TeX's shell escape
mechanism and capture the result in a control sequence. The category code of
most of TeX's default special characters (and some other potentially
problematic characters) is temporarily changed to 12 while reading the result.

%package -n %{shortname}-texplate
Version: svn71963
Provides: texlive-texplate = %{epoch}:%{source_date}-%{release}
Provides: tex-texplate = %{epoch}:%{source_date}-%{release}
Provides: tex-texplate-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texplate-bin = %{epoch}:%{source_date}-%{release}
License: BSD-3-Clause
Summary: A tool for creating document structures based on templates
Requires: texlive-base
Requires: texlive-kpathsea
# So much java
BuildArch: noarch

%description -n %{shortname}-texplate
TeXplate is a tool for creating document structures based on
templates. The application name is a word play on TeX and
template, so the purpose seems quite obvious: we want to
provide an easy and straightforward framework for reducing the
typical code boilerplate when writing TeX documents. Also note
that one can easily extrapolate the use beyond articles and
theses: the application is powerful enough to generate any
text-based structure, given that a corresponding template
exists.

%package -n %{shortname}-texsis
Version: svn69742
Provides: texlive-texsis = %{epoch}:%{source_date}-%{release}
Provides: tex-texsis = %{epoch}:%{source_date}-%{release}
Provides: tex-texsis-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texsis-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texsis-bin < 7:20170520
Provides: tex-texsis-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-texsis-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texsis-doc < 7:20170520
License: LPPL-1.3c
Summary: Plain TeX macros for Physicists
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-pdftex
Requires: texlive-tex
Requires: texlive-cm
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-plain
Requires(post,postun): coreutils
# symlinks only
BuildArch: noarch

%description -n %{shortname}-texsis
TeXsis is a TeX macro package which provides useful features
for typesetting research papers and related documents. For
example, it includes support specifically for: Automatic
numbering of equations, figures, tables and references;
Simplified control of type sizes, line spacing, footnotes,
running headlines and footlines, and tables of contents,
figures and tables; Specialized document formats for research
papers, preprints and ``e-prints,'' conference proceedings,
theses, books, referee reports, letters, and memoranda;
Simplified means of constructing an index for a book or thesis;
Easy to use double column formatting; Specialized environments
for lists, theorems and proofs, centered or non-justified text,
and listing computer code; Specialized macros for easily
constructing ruled tables. TeXsis was originally developed for
physicists, but others may also find it useful. It is
completely compatible with Plain TeX.

%package -n %{shortname}-texware
Summary: Basic utility programs for use with TeX
Version: svn77830
Provides: texlive-texware = %{epoch}:%{source_date}-%{release}
Provides: tex-texware = %{epoch}:%{source_date}-%{release}
Provides: tex-texware-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-texware-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-texware-bin < 7:20170520
License: LicenseRef-Fedora-Public-Domain
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-texware
Basic utility programs from the original TeX project at Stanford, comprising:
dvitype, which converts a TeX output (DVI) file to a plain text file (see also
the DVI structure topic); pooltype, which converts a TeX-suite program's "pool"
(string) file into human-readable form; and tftopl and pltotf, which convert
between binary TeX font metric (TFM) files and human readable property list
(PL) files.

%package -n %{shortname}-thumbpdf
Version: svn62518
Provides: texlive-thumbpdf = %{epoch}:%{source_date}-%{release}
Provides: tex-thumbpdf = %{epoch}:%{source_date}-%{release}
Provides: tex-thumbpdf-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-thumbpdf-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-thumbpdf-bin < 7:20170520
Provides: tex-thumbpdf-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-thumbpdf-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-thumbpdf-doc < 7:20170520
License: LPPL-1.3c
Summary: Thumbnails for pdfTeX and dvips/ps2pdf
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(ifluatex.sty)
Requires: ghostscript
# perl
BuildArch: noarch

%description -n %{shortname}-thumbpdf
A Perl script that provides support for thumbnails in pdfTeX
and dvips/ps2pdf. The script uses ghostscript to generate the
thumbnails which get represented in a TeX readable file that is
read by the package thumbpdf.sty to automatically include the
thumbnails. This arrangement works with both plain TeX and
LaTeX.

%package -n %{shortname}-tie
Summary: Allow multiple web change files
Version: svn77830
Provides: texlive-tie = %{epoch}:%{source_date}-%{release}
Provides: tex-tie = %{epoch}:%{source_date}-%{release}
Provides: tex-tie-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-tie-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tie-bin < 7:20170520
License: Latex2e
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-tie
Tie was originally developed to allow web programmers to apply more than one
change file to their source. The program may also be used to create a new
version of a .web file that incorporates existing changes.

%package -n %{shortname}-tikztosvg
Version: svn60289
Provides: texlive-tikztosvg = %{epoch}:%{source_date}-%{release}
Summary: A utility for rendering TikZ diagrams to SVG
License: GPL-3.0-only
Requires: texlive-base texlive-kpathsea

%description -n %{shortname}-tikztosvg
This package provides a shell script that calls XeTeX and
pdf2svg to convert TikZ environments to SVG files.

%package -n %{shortname}-tpic2pdftex
Summary: Use tpic commands in pdfTeX
Version: svn75712
Provides: texlive-tpic2pdftex = %{epoch}:%{source_date}-%{release}
Provides: tex-tpic2pdftex = %{epoch}:%{source_date}-%{release}
Provides: tex-tpic2pdftex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-tpic2pdftex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tpic2pdftex-bin < 7:20170520
Provides: tex-tpic2pdftex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-tpic2pdftex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-tpic2pdftex-doc < 7:20170520
License: GPL-2.0-or-later
# awk
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-tpic2pdftex
This AWK script converts pic language, embedded inline (delimited by .PS and
.PE markers), to \pdfliteral commands. It is now maintained as part of TeX
Live.

%package -n %{shortname}-ttfutils
Summary: Convert TrueType to TFM and PK fonts
Version: svn77830
Provides: texlive-ttfutils = %{epoch}:%{source_date}-%{release}
Provides: tex-ttfutils = %{epoch}:%{source_date}-%{release}
Provides: tex-ttfutils-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-ttfutils-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ttfutils-bin < 7:20170520
Provides: tex-ttfutils-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ttfutils-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ttfutils-doc < 7:20170520
License: LPPL-1.3c
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-ttfutils
Utilities: ttf2afm ttf2pk ttf2tfm ttfdump. FreeType is the underlying library.

%package -n %{shortname}-typeoutfileinfo
Version: svn67526
Provides: texlive-typeoutfileinfo = %{epoch}:%{source_date}-%{release}
Provides: tex-typeoutfileinfo = %{epoch}:%{source_date}-%{release}
Provides: tex-typeoutfileinfo-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-typeoutfileinfo-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-typeoutfileinfo-bin < 7:20170520
Provides: tex-typeoutfileinfo-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-typeoutfileinfo-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-typeoutfileinfo-doc < 7:20170520
License: LPPL-1.3c
Summary: Display class/package/file information
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(readprov.sty)
# shell
BuildArch: noarch

%description -n %{shortname}-typeoutfileinfo
The package provides a minimalist shell script, for Unix
systems, that displays the information content in a
\ProvidesFile, \ProvidesPackage or \ProvidesClass command in a
LaTeX source file. The package requires that the readprov
package is available.

%package -n %{shortname}-typog
Summary: Typographic fine-tuning and micro-typographic enhancements
Version: svn76661
Provides: tex-typog = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-typog
This package provides macros for micro-typographic enhancements. It covers a
variety of topics: Precise hyphenation control Disable/break ligatures Manual
italic correction Extra kerning for slash and hyphen Raising selected
characters (e.g. hyphen, en-dash, and em-dash) Aligning of the last line of a
paragraph Filling of the last line of a paragraph Word spacing control
Microtype front-end Slightly sloppy paragraphs Vertically partially-tied
paragraphs Breakable displayed equations Setspace front-end Smooth ragged-right
paragraphs Moreover, typog provides an environment to flag interesting parts of
the information deluge typically accumulating in a LaTeX log-file and an
associated tool, typog-grep, that selectively retrieves these parts.

%package -n %{shortname}-ulqda
Version: svn26313
Provides: texlive-ulqda = %{epoch}:%{source_date}-%{release}
Provides: tex-ulqda = %{epoch}:%{source_date}-%{release}
Provides: tex-ulqda-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-ulqda-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ulqda-bin < 7:20170520
Provides: tex-ulqda-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-ulqda-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-ulqda-doc < 7:20170520
License: LPPL-1.3c
Summary: Support of Qualitative Data Analysis
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(multicol.sty)
Requires: tex(tikz.sty)
Requires: tex(dot2texi.sty)
Requires: tex(soul.sty)
# perl
BuildArch: noarch

%description -n %{shortname}-ulqda
The package is for use in Qualitative Data Analysis research.
It supports the integration of Qualitative Data Analysis (QDA)
research tasks, specifically for Grounded Theory, into the
LaTeX work flow. It assists in the analysis of textual data
such as interview transcripts and field notes by providing the
LaTeX user with macros which are used to markup textual
information -- for example, in-depth interviews.

%package -n %{shortname}-upmendex
Summary: Multilingual index processor
Version: svn74401
License: BSD-3-Clause
Requires: texlive-base texlive-kpathsea
Provides: tex-upmendex = %{epoch}:%{source_date}-%{release}
Provides: tex-upmendex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-upmendex-bin = %{epoch}:%{source_date}-%{release}

%description -n %{shortname}-upmendex
The package is a multilingual index processor with the
following features: Mostly compatible with makeindex and upper
compatible with mendex. Supports UTF-8 and works with upLaTeX,
XeLaTeX and LuaLaTeX. Supports Latin (including non-English),
Greek, Cyrillic, Korean Hangul and Chinese Han (Hanzi
ideographs) scripts, as well as Japanese Kana. Supports
Devanagari, Thai, Arabic and Hebrew scripts (experimental).
Supports four kinds of sort orders (Pinyin, Radical-Stroke,
Stroke and Zhuyin) for Chinese Han scripts (Hanzi ideographs).
Applies International Components for Unicode (ICU) for sorting
process.

%package -n %{shortname}-uptex
Summary: Unicode version of pTeX
Version: svn77830
Provides: texlive-uplatex = %{epoch}:%{source_date}-%{release}
Provides: tex-uptex = %{epoch}:%{source_date}-%{release}
Provides: tex-uptex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-uptex-doc = %{epoch}:%{source_date}-%{release}
Provides: tex-uplatex = %{epoch}:%{source_date}-%{release}
Provides: tex-uplatex-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-uplatex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-uptex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-uptex-bin < 7:20170520
Provides: texlive-uplatex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-uplatex-bin < 7:20170520
Provides: texlive-uplatex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-uplatex-doc < 7:20170520
Provides: texlive-uptex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-uptex-doc < 7:20170520
License: BSD-3-Clause
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-convbkmk
Requires: texlive-etex
Requires: texlive-hyph-utf8
Requires: texlive-hyphen-base
Requires: texlive-ipaex
Requires: texlive-japanese-otf
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-plain
Requires: texlive-ptex-base
Requires: texlive-uptex-base
Requires: texlive-uptex-fonts

%description -n %{shortname}-uptex
upTeX is an extension of pTeX, using UTF-8 input and producing UTF-8 output. It
was originally designed to improve support for Japanese, but is also useful for
documents in Chinese and Korean. It can process Chinese simplified, Chinese
traditional, Japanese, and Korean simultaneously, and can also process original
LaTeX with \inputenc{utf8} and Babel (Latin/Cyrillic/Greek etc.) by switching
its \kcatcode tables.

%package -n %{shortname}-urlbst
Summary: Web support for BibTeX
Version: svn76790
Provides: texlive-urlbst = %{epoch}:%{source_date}-%{release}
Provides: tex-urlbst = %{epoch}:%{source_date}-%{release}
Provides: tex-urlbst-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-urlbst-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-urlbst-bin < 7:20170520
Provides: tex-urlbst-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-urlbst-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-urlbst-doc < 7:20170520
License: GPL-2.0-only AND LPPL-1.3c
# perl
BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-urlbst
Supports a new BibTeX 'webpage' entry type and 'url', 'lastchecked', and
'eprint' and 'DOI' fields. The Perl script urlbst can be used to add this
support to an arbitrary .bst file which has a reasonably conventional
structure. The result is meant to be robust rather than pretty.

%package -n %{shortname}-velthuis
Version: svn66186
Provides: texlive-velthuis = %{epoch}:%{source_date}-%{release}
Provides: tex-velthuis = %{epoch}:%{source_date}-%{release}
Provides: tex-velthuis-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-velthuis-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-velthuis-bin < 7:20170520
Provides: tex-velthuis-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-velthuis-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-velthuis-doc < 7:20170520
Provides: texlive-devnag = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-devnag < 7:20170520
Provides: texlive-devnag-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-devnag-bin < 7:20170520
License: GPL-1.0-or-later
Summary: Typeset Devanagari
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-xetex-devanagari
Requires: tex(hindicaptions.sty)
Requires: tex(cite.sty)
Requires: tex(ifxetex.sty)

%description -n %{shortname}-velthuis
Frans Velthuis' preprocessor for Devanagari text, and fonts and
macros to use when typesetting the processed text. The macros
provide features that support Sanskrit, Hindi, Marathi, Nepali,
and other languages typically printed in the Devanagari script.
The package provides fonts, in both Metafont and Type 1
formats. Users of modern TeX distributions may care to try the
XeTeX based package, which is far preferable for users who can
type Unicode text.

%package -n %{shortname}-vlna
Version: svn73908
Provides: texlive-vlna = %{epoch}:%{source_date}-%{release}
Provides: tex-vlna = %{epoch}:%{source_date}-%{release}
Provides: tex-vlna-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-vlna-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-vlna-bin < 7:20170520
Provides: tex-vlna-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-vlna-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-vlna-doc < 7:20170520
License: LPPL-1.3c
Summary: Adds ~ after non-syllabic preposition, for Czech/Slovak
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-vlna
Preprocessor for TeX source implementing the Czech/Slovak
typographical rule forbidding a non-syllabic preposition alone
at the end of a line.

%package -n %{shortname}-vpe
Version: svn26039
Provides: texlive-vpe = %{epoch}:%{source_date}-%{release}
Provides: tex-vpe = %{epoch}:%{source_date}-%{release}
Provides: tex-vpe-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-vpe-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-vpe-bin < 7:20170520
Provides: tex-vpe-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-vpe-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-vpe-doc < 7:20170520
License: LPPL-1.3c
Summary: Source specials for PDF output
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(keyval.sty)
Requires: tex(color.sty)
Requires: tex(pifont.sty)
# perl
BuildArch: noarch

%description -n %{shortname}-vpe
VPE is a system to make the equivalent of "source special"
marks in a PDF file. Clicking on a mark will activate an
editor, pointing at the source line that produced the text that
was marked. The system comprises a perl file (vpe.pl) and a
LaTeX package (vpe.sty); it will work with PDF files generated
via LaTeX/dvips, pdfTeX (version 0.14 or better), and
LaTeX/VTeX. Using the LaTeX/dvips or pdfLaTeX routes, the
(pdf)TeX processor should be run with shell escapes enabled.

%package -n %{shortname}-web
Summary: The original literate programming system
Version: svn77830
Provides: texlive-web = %{epoch}:%{source_date}-%{release}
Provides: tex-web = %{epoch}:%{source_date}-%{release}
Provides: tex-web-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-web-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-web-bin < 7:20170520
License: Knuth-CTAN
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-web
The system processes 'web' files in two ways: firstly to rearrange them to
produce compilable code (using the program tangle), and secondly to produce a
TeX source (using the program weave) that may be typeset for comfortable
reading.

%package -n %{shortname}-webquiz
Version: svn58808
Provides: texlive-webquiz = %{epoch}:%{source_date}-%{release}
Provides: tex-webquiz = %{epoch}:%{source_date}-%{release}
Provides: tex-webquiz-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-webquiz-bin = %{epoch}:%{source_date}-%{release}
License: GPL-3.0-or-later
Summary: A LaTeX package for writing online quizzes
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-tex4ht
Requires: texlive-make4ht
Requires: tex(tikz.sty)
Requires: tex(pstricks.sty)
Requires: texlive-dvisvgm
Requires: ghostscript
Requires: python3
# python3
BuildArch: noarch

%description -n %{shortname}-webquiz
WebQuiz makes it possible to use LaTeX to write interactive online quizzes.
The quizzes are first written in LaTeX and then converted into HTML using
WebQuiz, which is written in python. The conversion from LaTeX to HTML is
done behind the scenes using TeX4ht. The idea is that you should be able to
produce nice online quizzes using WebQuiz and basic knowledge of LaTeX.

%package -n %{shortname}-wordcount
Version: svn46165
Provides: texlive-wordcount = %{epoch}:%{source_date}-%{release}
Provides: tex-wordcount = %{epoch}:%{source_date}-%{release}
Provides: texlive-wordcount-bin = %{epoch}:%{source_date}-%{release}
Provides: tex-wordcount-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-wordcount-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-wordcount-doc < 7:20180414
License: LPPL-1.3c
Summary: Estimate the number of words in a LaTeX document
Requires: texlive-base
Requires: texlive-kpathsea
# shell
BuildArch: noarch

%description -n %{shortname}-wordcount
The package provides a relatively easy way of estimating the
number of words in a LaTeX document that does not require
dvitty or other DVI converters. It does however require
something like Unix grep -c that can search a file for a
particular string and report the number of matching lines. An
accompanying shell script wordcount.sh contains more
information in its comments.

%package -n %{shortname}-xdvi
Version: svn62387
Provides: texlive-xdvi = %{epoch}:%{source_date}-%{release}
License: MIT
Summary: A DVI previewer for the X Window System
Provides: tex-xdvi = %{epoch}:%{source_date}-%{release}
Provides: tex-xdvi-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-xdvi-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-xdvi-bin < 7:20170520
Provides: xdvi = %{epoch}:%{source_date}-%{release}
Provides: xdvik = %{epoch}:%{source_date}-%{release}
Requires: texlive-kpathsea
Requires: texlive-base

%description -n %{shortname}-xdvi
The canonical previewer for use on Unix and other X-windows
based systems.

%package -n %{shortname}-xdvipsk
Version: svn77931
License: GPL-2.0-or-later
Summary: Convert a TeX DVI file to PostScript (dvips extexsion)
Provides: tex-xdvipsk = %{epoch}:%{source_date}-%{release}
Provides: tex-xdvipsk-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-xdvipsk-bin = %{epoch}:%{source_date}-%{release}
Provides: xdvipsk = %{epoch}:%{source_date}-%{release}
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-xdvipsk
XDvipsk is an extended Dvips, which is a DVI-to-PostScript translator.

%package -n %{shortname}-xetex
Summary: An extended variant of TeX for use with Unicode sources
Version: svn77830
Provides: texlive-xetex = %{epoch}:%{source_date}-%{release}
Provides: tex-xetex = %{epoch}:%{source_date}-%{release}
Provides: tex-xetex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-xetex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-xetex-bin < 7:20170520
Provides: tex-xetex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-xetex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-xetex-doc < 7:20170520
License: MIT
Requires(post,postun): coreutils
Requires: teckit
Requires: tex(xetex.def)
Requires: texlive-atbegshi
Requires: texlive-atveryend
Requires: texlive-babel
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-dvipdfmx
Requires: texlive-etex
Requires: texlive-everyshi
Requires: texlive-firstaid
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-l3backend
Requires: texlive-l3kernel
Requires: texlive-l3packages
Requires: texlive-latex
Requires: texlive-latex-fonts
Requires: texlive-lm
Requires: texlive-plain
Requires: texlive-tex-ini-files
Requires: texlive-unicode-data
Requires: texlive-xetexconfig

%description -n %{shortname}-xetex
XeTeX is a TeX typesetting engine using Unicode and supporting modern font
technologies such as OpenType, TrueType or Apple Advanced Typography (AAT),
including OpenType mathematics fonts. XeTeX supports many extensions that
reflect its origins in linguistic research; it also supports micro-typography
(as available in pdfTeX). XeTeX was developed by the SIL (the first version was
specifically developed for those studying linguistics, and using Macintosh
computers). XeTeX's immediate output is an extended variant of DVI format,
which is ordinarily processed by a tightly bound processor (called xdvipdfmx),
that produces PDF. XeTeX is released as part of TeX Live; documentation has
arisen separately. Source code is available from ctan:/systems/texlive/Source/.

%package -n %{shortname}-xindex
Summary: Unicode-compatible index generation
Version: svn77844
Provides: texlive-xindex = %{epoch}:%{source_date}-%{release}
Provides: tex-xindex = %{epoch}:%{source_date}-%{release}
Provides: tex-xindex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-xindex-bin = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c AND MIT
# lua
BuildArch: noarch
Requires: lua >= 5.3
Requires: tex(imakeidx.sty)
Requires: tex(makeidx.sty)
Requires: tex(xkeyval.sty)
Requires: texlive-base
Requires: texlive-kpathsea
Requires: texlive-luatex

%description -n %{shortname}-xindex
This package provides a Unicode-compatible index program for LaTeX.

%package -n %{shortname}-xindy
Version: svn65958
Provides: texlive-xindy = %{epoch}:%{source_date}-%{release}
Provides: tex-xindy = %{epoch}:%{source_date}-%{release}
%if %{without bootstrap}
Provides: tex-xindy-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-xindy-bin = %{epoch}:%{source_date}-%{release}
%endif
Provides: tex-xindy-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-xindy-bin <= 6:svn41316
Provides: tex-xindy-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-xindy-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-xindy-doc <= 6:svn41316
License: GPL-2.0-or-later
Summary: A general-purpose index processor
# There are some arch specific binaries in here.
# BuildArch: noarch
Requires: texlive-base
Requires: texlive-kpathsea
Requires: clisp

%description -n %{shortname}-xindy
Xindy was deceloped after an impasse had been encountered in
the attempt to complete internationalisation of makeindex.
Xindy can be used to process indexes for documents marked up
using (La)TeX, Nroff family and SGML-based languages. Xindy is
highly configurable, both in markup terms and in terms of the
collating order of the text being processed.

%package -n %{shortname}-xml2pmx
Version: svn57972
Provides: texlive-xml2pmx = %{epoch}:%{source_date}-%{release}
Summary: Convert MusicXML to PMX and MusiXTeX
License: GPL-3.0-or-later
Requires: texlive-base texlive-kpathsea

%description -n %{shortname}-xml2pmx
This program translates MusicXML files to input suitable for
PMX and MusiXTeX processing. This package supports Windows,
MacOS and Linux systems.

%package -n %{shortname}-xmltex
Summary: Support for parsing XML documents
Version: svn76924
Provides: texlive-xmltex = %{epoch}:%{source_date}-%{release}
Provides: tex-xmltex = %{epoch}:%{source_date}-%{release}
Provides: tex-xmltex-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-xmltex-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-xmltex-bin < 7:20170520
Provides: tex-xmltex-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-xmltex-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-xmltex-doc < 7:20170520
Provides: xmltex = %{epoch}:%{source_date}-%{release}
License: LPPL-1.3c
# symlinks
BuildArch: noarch
Requires: tex-kpathsea
Requires: texlive-babel
Requires: texlive-base
Requires: texlive-cm
Requires: texlive-dehyph
Requires: texlive-firstaid
Requires: texlive-hyph-utf8
Requires: texlive-hyphen-base
Requires: texlive-knuth-lib
Requires: texlive-kpathsea
Requires: texlive-kpathsea-bin
Requires: texlive-l3backend
Requires: texlive-l3kernel
Requires: texlive-l3packages
Requires: texlive-latex
Requires: texlive-latex-fonts
Requires: texlive-latexconfig
Requires: texlive-pdftex
Requires: texlive-tex
Requires: texlive-tex-ini-files
Requires: texlive-unicode-data
Requires: texlive-xmltexconfig

%description -n %{shortname}-xmltex
The package provides an implementation of a parser for documents matching the
XML 1.0 and XML Namespace Recommendations. In addition to parsing commands are
provided to attach TeX typesetting instructions to the various markup elements
as they are encountered. Sample files for typesetting a subset of TEI, MathML,
are included. Element and Attribute names, as well as character data, may use
any characters allowed in XML, using UTF-8 or a suitable 8-bit encoding.

%package -n %{shortname}-xpdfopen
Version: svn65952
Provides: texlive-xpdfopen = %{epoch}:%{source_date}-%{release}
Provides: tex-xpdfopen = %{epoch}:%{source_date}-%{release}
Provides: tex-xpdfopen-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-xpdfopen-bin = %{epoch}:%{source_date}-%{release}
License: LicenseRef-Fedora-Public-Domain
Summary: Commands to control PDF readers, under X11
Requires: texlive-base
Requires: texlive-kpathsea

%description -n %{shortname}-xpdfopen
The command-line programs pdfopen and pdfclose allow you to
control the X Window System version of Adobe's Acrobat Reader
from the command line or from within a (shell) script. The
programs work with Acrobat Reader 5, 7, 8 and 9 for Linux, xpdf
and evince. This version derives from one written by Fabrice
Popineau for Microsoft operating systems.

%package -n %{shortname}-yplan
Version: svn34398
Provides: texlive-yplan = %{epoch}:%{source_date}-%{release}
Provides: tex-yplan = %{epoch}:%{source_date}-%{release}
Provides: tex-yplan-bin = %{epoch}:%{source_date}-%{release}
Provides: texlive-yplan-bin = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-yplan-bin < 7:20170520
Provides: tex-yplan-doc = %{epoch}:%{source_date}-%{release}
Provides: texlive-yplan-doc = %{epoch}:%{source_date}-%{release}
Obsoletes: texlive-yplan-doc < 7:20170520
License: LPPL-1.3c
Summary: Daily planner type calendar
Requires: texlive-base
Requires: texlive-kpathsea
Requires: tex(ifthen.sty)
# perl
BuildArch: noarch

%description -n %{shortname}-yplan
Prints two six-monthly vertical-type daily planner (i.e.,
months along the top, days downwards), with each 6-month period
fitting onto a single A4 (or US letter) sheet. The package
offers support for English, French, German, Spanish and
Portuguese. The previous scheme of annual updates has now been
abandoned, in favour of a Perl script yplan that generates a
year's planner automatically. (The last manually-generated
LaTeX file remains on the archive.)

%prep
%setup -q -c -T
# xz -dc %%{SOURCE0} | tar x
tar xf %{SOURCE0}
[ -e %{source_name} ] && mv %{source_name} source
%patch -P1 -p0
%patch -P2 -p1 -b .format
%patch -P5 -p0
%if %{with poppler}
%if 0%{?fedora} || 0%{?rhel} >= 8
%patch -P7 -p1 -b .newpoppler
%endif
%endif
%patch -P8 -p1 -b .texinfo-fix
%patch -P17 -p1 -b .annocheck
%if %{with poppler}
%if 0%{?fedora} || 0%{?rhel} >= 8
%patch -P18 -p1 -b .poppler-0.73
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
%patch -P23 -p1 -b .poppler-0.84
%endif
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%patch -P29 -p1 -b .poppler090
%endif
%endif
%patch -P30 -p1 -b .out_of_memory
%if %{with poppler}
%patch -P31 -p1 -b .poppler-xpdf-fix
%if 0%{?fedora} >= 36 || 0%{?rhel} > 9
%patch -P34 -p1 -b .poppler22
%patch -P35 -p1 -b .poppler-crash-fix
%endif
%if 0%{?fedora} >= 37 || 0%{?rhel} > 9
%patch -P36 -p1 -b .poppler-22.08.0
%endif
%endif

%if 0%{?fedora} >= 38 || 0%{?rhel} > 9
%patch -P37 -p1 -b .libpaper2
%endif

# Setup copies of the licenses
for l in `unxz -c %{SOURCE3} | tar t`; do
ln -s %{_texdir}/licenses/$l $l
done

%patch -P44 -p1 -b .pdf-header-order-fix
# %%patch -P51 -p1 -b .ftbfs-gcc16

# Disable broken tests
# updmap-cmdline-test.pl is not useful and it will fail because it finds the system perl bits instead of the local copy
sed -i 's|TESTS = tests/updmap-cmdline-test.pl||g' source/texk/texlive/Makefile.in
sed -i 's|TESTS = tests/updmap-cmdline-test.pl||g' source/texk/texlive/Makefile.am
# bibtex8 fails on x86_64 and i686, but not really. I think this test might also be using the older system bits
sed -i 's|bibtex8_tests = tests/bibtex8.test|bibtex8_tests =|g' source/texk/bibtex-x/Makefile.in
sed -i 's|bibtex8_tests = tests/bibtex8.test|bibtex8_tests =|g' source/texk/bibtex-x/Makefile.am

# Value here is "17" not "16" because we have a source0 at index 1.
# Source16 at index 17 is our first "normal" noarch source file.
# Also, this macro has to be here, not at the top, or it will not evaluate properly. :P
%global mysources %{lua: for index,value in ipairs(sources) do if index >= 17 then print(value.." ") end end}

# Drop source/libs/xpdf dir, we use system ver (if at all)
rm -rf source/libs/xpdf

# Create an RPM dependency generator for use in other texlive-* packages.
cat > texlive.attr << 'EOF'
%%__texlive_path          %{gsub %__texlive_path \ \\}
%%__texlive_exclude_path  %__texlive_exclude_path
%%__texlive_provides()    tex(%%{basename:%%{1}}) = %{tl_version}
EOF

%build

%if %{without bootstrap}
cat /usr/share/texlive/kpathsea.log || :
# DEBUG
# Okay. Lets look at things.
# 1. /usr/share/texlive/texmf-dist/web2c/fmtutil.cnf should exist and be valid.
ls -l /usr/share/texlive/texmf-dist/web2c/fmtutil.cnf || :
# cat /usr/share/texlive/texmf-dist/web2c/fmtutil.cnf

# Check for ls-R files
ls -l /usr/share/texlive/texmf-config/ls-R || :
ls -l /usr/share/texlive/texmf-dist/ls-R || :
ls -l /usr/share/texlive/texmf-local/ls-R || :
ls -l /usr/share/texlive/texmf-var/ls-R || :

# 2. kpsewhich -all fmtutil.cnf
# We should see /usr/share/texlive/texmf-dist/web2c/fmtutil.cnf
kpsewhich -version || :

kpsewhich --debug -1 -all fmtutil.cnf || :

# 3. fmtutil-sys --all
# This should recreate all format files, may not be able to do that here (non-root)
fmtutil-sys --all || :

# 4. mktexfmt latex should succeed
mktexfmt latex || :

# Make texlive generate latex.fmt, so that multiple threads do not race to
# make it during the xindy build.
cat > dummy.tex << EOF
\documentclass{article}
\begin{document}
This is a document.
\end{document}
EOF
latex dummy.tex
rm -f dummy.*
%endif

# https://gcc.gnu.org/bugzilla/show_bug.cgi?id=118112
export CFLAGS="$RPM_OPT_FLAGS -std=gnu17 -fno-strict-aliasing -Werror=format-security"

# -std=gnu++17 until icu is properly C++20 compatible
%if 0%{?fedora} >= 36 || 0%{?rhel} > 9
export CXXFLAGS="$RPM_OPT_FLAGS -std=gnu++17 -fno-strict-aliasing -Werror=format-security"
%else
export CXXFLAGS="$RPM_OPT_FLAGS -std=c++11 -fno-strict-aliasing -Werror=format-security"
%endif

cd source
PREF=`pwd`/inst
mkdir -p work
%global _configure ../configure
cd work
%if %{without poppler}
export GLIB_LIBS=`pkg-config --libs glib-2.0`
export PAPER_LIBS="-lpaper"
export FONTCONFIG_LIBS=`pkg-config --libs fontconfig`
export XPDF_INCLUDES="-I/usr/include/xpdf -I/usr/include/xpdf/fofi -I/usr/include/xpdf/goo -I/usr/include/xpdf/splash"
export XPDF_LIBS="-lxpdfcore -lfofi -lgoo -lsplash $GLIB_LIBS $PAPER_LIBS $FONTCONFIG_LIBS"
%endif
%configure \
--prefix=$PREF --datadir=$PREF --libdir=$PREF/lib --includedir=$PREF/include --datarootdir=$PREF/share --mandir=$PREF/share/man \
--infodir=$PREF/share/info --exec_prefix=$PREF --bindir=$PREF/bin --with-system-zlib --with-system-libpng \
--with-system-gd --with-system-t1lib --with-system-teckit --with-system-freetype2 --with-system-zziplib \
--with-system-cairo --with-system-icu --with-system-harfbuzz --with-system-graphite2 --with-system-libgs --with-system-pixman \
--with-system-libpaper --with-system-potrace --with-pic --with-xdvi-x-toolkit=xaw --with-system-mpfr --with-system-gmp \
--enable-shared --enable-compiler-warnings=max --without-cxx-runtime-hack \
--disable-native-texlive-build --disable-t1utils --enable-psutils --disable-biber --disable-ptexenc --disable-largefile \
%if %{with poppler}
--with-system-poppler --with-system-xpdf \
%else
--with-system-xpdf \
%endif
%ifarch %{power64} s390 s390x riscv64
--disable-luajittex --disable-mfluajit --disable-luajithbtex --disable-mfluajit-nowin \
%endif
%if %{without bootstrap}
--enable-xindy \
%else
--disable-xindy \
%endif
--disable-xindy-docs --disable-xindy-rules \
--disable-rpath

# disable rpath
for i in `find . -name libtool`; do
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' $i
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' $i
done

%make_build world STRIPPROG=/bin/true STRIP=/bin/true ||:

%install
# make directories
mkdir -p %{buildroot}%{_texdir}/texmf-config/web2c
mkdir -p %{buildroot}%{_texmf_var}

# make symlinks
pushd %{buildroot}%{_texdir}/texmf-config/web2c
ln -s ../../texmf-dist/web2c/updmap.cfg updmap.cfg
popd

# make compatibility symlink
pushd %{buildroot}%{_datadir}
mkdir -p texlive/texmf-local/texmf-compat
ln -s texlive/texmf-local/texmf-compat texmf
popd

# make opentype fontdir symlinks
# NOTE: fontawesome, stix, oldstandard are a conflict, so we just add Requires for the 
# corresponding system font packages for them.
# NOTE: We might have to handle this differently if there are lots of conflicts later.
# DO NOT MAKE A SYMLINK FOR public/ebgaramond
# The EB Garamond upstream font decided to map some historical flags (i.e., flags 
# obsolete for centuries) to the Unicode flag emoji code points.
# Since most other fonts do not include the relevant code points, Fontconfig decides to 
# pick up the EB Garamond flags through the fallback font mechanism for almost all 
# fonts on the system, including DejaVu Sans, Liberation Sans, etc.
mkdir -p %{buildroot}%{_datadir}/fonts
pushd %{buildroot}%{_datadir}/fonts
for i in public/lilyglyphs ; do
  j=`echo $i | cut -d / -f 2`
  ln -s %{_texmf_main}/fonts/opentype/$i $j
done
popd

# install binaries
mkdir -p %{buildroot}%{_bindir}
rm -f source/inst/bin/man
cp -a source/inst/bin/* %{buildroot}%{_bindir}

# install libs
mkdir -p %{buildroot}%{_libdir}
cp -d source/inst/lib/*.so* %{buildroot}%{_libdir}
cp -a source/inst/lib/pkgconfig %{buildroot}%{_libdir}

# install includes
mkdir -p %{buildroot}%{_includedir}
cp -r source/inst/include/* %{buildroot}%{_includedir}

# install shared files
mkdir -p %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_texdir}
pushd source/inst/share
cp -a info %{buildroot}%{_datadir}/
cp -a man %{buildroot}%{_datadir}/
cp -a texmf-dist %{buildroot}%{_texdir}/
popd

# relocate binaries to %%{_bindir} and fix relative symlinks
pushd %{buildroot}%{_bindir}
for i in `find . -type l`; do
if [ "`readlink $i | grep '..' | wc -l`" == "1" ]; then
l=`readlink $i | sed s,.*texmf,/usr/share/texlive/texmf,`
rm -f $i
ln -s $l $i
fi
done
popd

# install noarch bits
pushd %{buildroot}%{_texdir}
echo %{mysources}
for noarchsrc in %{mysources}; do
  xz -dc $noarchsrc | tar x
done
popd
# Do the weird noarch bits
pushd  %{buildroot}%{_texmf_main}
xz -dc %{SOURCE5} | tar x
xz -dc %{SOURCE6} | tar x
xz -dc %{SOURCE7} | tar x
xz -dc %{SOURCE8} | tar x
xz -dc %{SOURCE9} | tar x
xz -dc %{SOURCE10} | tar x
xz -dc %{SOURCE11} | tar x
xz -dc %{SOURCE12} | tar x
xz -dc %{SOURCE13} | tar x
xz -dc %{SOURCE14} | tar x
xz -dc %{SOURCE15} | tar x
popd

# We want the texmf.cnf we patched, not the vanilla one from the kpathsea.tar.xz
cp -a source/texk/kpathsea/texmf.cnf %{buildroot}%{_texmf_main}/web2c/texmf.cnf

# Apply fixes
# We do it here because this is the first time we have the complete tree.
# bz1384067
sed -i 's|\\sc |\\scshape |g' %{buildroot}%{_texmf_main}/bibtex/bst/base/acm.bst
sed -i 's|\\sc |\\scshape |g' %{buildroot}%{_texmf_main}/bibtex/bst/base/siam.bst

# Patches to component tarballs
pushd %{buildroot}%{_texmf_main}

# neuter tlmgr a bit
patch -p1 < %{_sourcedir}/texlive-20190410-tlmgr-ignore-warning.patch

# Fix texmfcnf.lua
patch -p1 < %{_sourcedir}/texlive-2026-fedora-texmfcnf.lua.patch

# Fix interpreter on perl scripts
patch -p1 < %{_sourcedir}/texlive-base-20230311-fix-scripts.patch

popd

# config files in /etc symlinked
mkdir -p %{buildroot}%{_sysconfdir}/texlive/web2c
mkdir -p %{buildroot}%{_sysconfdir}/texlive/dvips/config
mkdir -p %{buildroot}%{_sysconfdir}/texlive/tex/generic/config

for i in mktex.cnf texmfcnf.lua texmf.cnf updmap.cfg; do
        mv %{buildroot}%{_texmf_main}/web2c/$i %{buildroot}%{_sysconfdir}/texlive/web2c/
        ln -s %{_sysconfdir}/texlive/web2c/$i %{buildroot}%{_texmf_main}/web2c/$i
done

# configure texmf-local - make it visible to kpathsea
sed -i -e 's|^TEXMFLOCAL.*|TEXMFLOCAL = $TEXMFROOT/texmf-local//|' %{buildroot}%{_sysconfdir}/texlive/web2c/texmf.cnf

mv %{buildroot}%{_texmf_main}/dvips/config/config.ps %{buildroot}%{_sysconfdir}/texlive/dvips/config/
ln -s %{_sysconfdir}/texlive/dvips/config/config.ps %{buildroot}%{_texmf_main}/dvips/config/config.ps

# Move the stock fmtutil.cnf under /etc and make sure everything is commented out
mv %{buildroot}%{usr_fmtutil_cnf} %{buildroot}%{etc_fmtutil_cnf}
sed -i '/^[a-z].*$/s/^/\#\!\ /' %{buildroot}%{_sysconfdir}/texlive/web2c/fmtutil.cnf

# Split the stock texmf.cnf file:
# * Look for lines like "# from foo:" and use those as the names of the files
#   we generate.
# * Take the text starting at "# from foo:" and ending just before the next
#   line containing just '#' (or EOF).
# * remove '#!'
# * Add a single line containing '#' to the beginning
# * Stuff that into a file named "foo" in %%_texdir/fmtutil.cnf.d
#
# This is a bit fragile as the precise format of the stock fmtutil.cnf file
# could change.
# The leading '#' and the "# from foo:" line are added to the output only to
# match the existing format of the file, just in case some tool cares.
mkdir %{buildroot}%{_texdir}/fmtutil.cnf.d
for i in $(grep '^# from .*:$' %{buildroot}%{etc_fmtutil_cnf}|sed 's/^# from //; s/:$//'); do
    echo "#" > %{buildroot}%{fmtutil_cnf_d}/$i
    sed -n "s/^#! //; /^# from $i:\$/,/^#\$/{/^#\$/!p}" %{buildroot}%{etc_fmtutil_cnf} >> %{buildroot}%{fmtutil_cnf_d}/$i
done

# Install the fmtutil.cnf generation script
install -D -p -m 755 -t %{buildroot}%{_sbindir} %{SOURCE4}

# Create fileattr for generating tex(...) Provides.
mkdir -p %{buildroot}%{_fileattrsdir}
cp -a texlive.attr %{buildroot}%{_fileattrsdir}/texlive.attr

# create macro file for building texlive
mkdir -p %{buildroot}%{_rpmmacrodir}
cp -a %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.texlive

# install texlive.tlpdb
cp %{SOURCE2} %{buildroot}%{_texdir}
# make a symlink so texdoc is happy
pushd %{buildroot}%{_texdir}/tlpkg
ln -s ../texlive.tlpdb .
popd

# install licenses
mkdir -p %{buildroot}%{_texdir}/licenses
pushd %{buildroot}%{_texdir}/licenses
xz -dc %{SOURCE3} | tar x
popd

# nuke useless tlmgr packaging stuff and doc droppings
rm -f %{buildroot}/%{_texdir}/install-tl
rm -rf %{buildroot}%{_texdir}/tlpkg/gpg/
rm -rf %{buildroot}%{_texdir}/tlpkg/tltcl/
rm -rf %{buildroot}%{_texdir}/tlpkg/tlpobj/
rm -rf %{buildroot}%{_texmf_main}/tlpkg/tlpobj/
# texconfig needs tlmgr.pl
# We're only including what it needs, no more.
# rm -f %{buildroot}%{_texmf_main}/doc/man/man1/tlmgr.1
# rm -f %{buildroot}%{_texmf_main}/scripts/texlive/tlmgr.pl
# rm -f %{buildroot}%{_bindir}/tlmgr
# rm -f %{buildroot}%{_texdir}/tlpkg/installer/config.guess
rm -f %{buildroot}%{_texmf_main}/scripts/texlive/tlmgr.pl.orig
rm -f %{buildroot}%{_texmf_main}/scripts/texlive/tl-errmess.vbs
rm -f %{buildroot}%{_texmf_main}/scripts/texlive/tlmgrgui.pl
rm -f %{buildroot}%{_texmf_main}/scripts/texlive/uninstall-win32.pl
rm -f %{buildroot}%{_texmf_main}/scripts/texlive/uninstall-windows.pl
rm -f %{buildroot}%{_texmf_main}/scripts/texlive/uninstq.vbs
rm -f %{buildroot}%{_texmf_main}/scripts/tlcockpit/tlcockpit.sh
rm -f %{buildroot}%{_texmf_main}/scripts/tlshell/tlshell.tcl
rm -f %{buildroot}%{_texdir}/tlpkg/installer/COPYING.MinGW-runtime.txt
rm -f %{buildroot}%{_texdir}/tlpkg/installer/ctan-mirrors.pl
rm -rf %{buildroot}%{_texdir}/tlpkg/installer/curl
rm -f %{buildroot}%{_texdir}/tlpkg/installer/install-menu-extl.pl
rm -f %{buildroot}%{_texdir}/tlpkg/installer/install-menu-perltk.pl
rm -f %{buildroot}%{_texdir}/tlpkg/installer/install-menu-text.pl
rm -f %{buildroot}%{_texdir}/tlpkg/installer/install-menu-wizard.pl
rm -f %{buildroot}%{_texdir}/tlpkg/installer/install-tl-gui.tcl
rm -f %{buildroot}%{_texdir}/tlpkg/installer/texlive.png
rm -f %{buildroot}%{_bindir}/tlcockpit
rm -f %{buildroot}%{_bindir}/tlshell
rm -rf %{buildroot}%{_datadir}/info/dir
rm -rf %{buildroot}%{_texdir}/readme-txt.dir/README.*
rm -rf %{buildroot}%{_texmf_main}/doc/man/man*/*.pdf
rm -rf %{buildroot}%{_texmf_main}/doc/man/man*/*.pdf
rm -rf %{buildroot}%{_texmf_main}/doc/man/Makefile
rm -rf %{buildroot}%{_texmf_main}/doc/man/man*/Makefile
rm -rf %{buildroot}%{_texmf_main}/doc/info/dir
# nuke unwanted ptexenc devel files
rm -rf %{buildroot}%{_includedir}/ptexenc
# nuke context windows files
rm -f %{buildroot}/%{_texmf_main}/scripts/context/stubs/mswin/*
rm -f %{buildroot}/%{_texmf_main}/scripts/context/stubs/win64/*
rm -f %{buildroot}/%{_texmf_main}/scripts/context/stubs/source/*

# Make this perl module show up in @INC
mkdir -p %{buildroot}%{_datadir}/perl5
ln -s %{_texdir}/tlpkg/TeXLive %{buildroot}%{_datadir}/perl5/TeXLive

# not sure why this is here
rm -rf %{buildroot}%{_texmf_main}/source/fonts/zhmetrics/ttfonts.map

pushd %{buildroot}%{_texdir}
# ALWAYS NUKE THIS IF IT IS HERE.
rm -rf texmf-var
# AND NOW WE MAKE THE SYMLINK.
ln -s %{_texmf_var} texmf-var
popd

# sync built/distro binaries
pushd %{buildroot}%{_bindir}
[ ! -e mfplain ] && ln -s mpost mfplain
[ ! -e texlua ] && ln -s luatex texlua
[ ! -e texluac ] && ln -s luatex texluac

# remove latexmk
# This lives in the "latexmk" package in Fedora.
rm -f latexmk
rm -rf %{buildroot}%{_texmf_main}/scripts/latexmk
rm -f %{buildroot}%{_datadir}/texlive/texmf-dist/doc/man/man1/latexmk.*

# remove ltx2unitxt
# this lives in the "perl-LaTeX-ToUnicode" package
rm -f ltx2unitxt
rm -rf %{buildroot}%{_texmf_main}/scripts/bibtexperllibs/ltx2unitxt

# Fix symlinks for helper scripts
rm -f bibexport.sh
ln -s /usr/share/texlive/texmf-dist/scripts/bibexport/bibexport.sh bibexport.sh
rm -rf mktexmf
ln -s /usr/share/texlive/texmf-dist/scripts/texlive/mktexmf mktexmf
rm -rf mkjobtexmf
ln -s /usr/share/texlive/texmf-dist/scripts/mkjobtexmf/mkjobtexmf.pl mkjobtexmf
rm -rf digestif
ln -s /usr/share/texlive/texmf-dist/scripts/digestif/digestif.texlua digestif
rm -rf texexec
ln -s /usr/share/texlive/texmf-dist/scripts/context/stubs/unix/texexec texexec
rm -rf texmfstart
ln -s /usr/share/texlive/texmf-dist/scripts/context/stubs/unix/texmfstart texmfstart


# make a mtxrun stub
rm -f mtxrun
cat > mtxrun << EOF
#!/bin/sh
env LUATEXDIR=/usr/share/texlive/texmf-dist/scripts/context/lua luatex --luaonly mtxrun.lua "\$@"
EOF
chmod 0755 mtxrun

# fix context
rm -f context
cat > context << EOF
#!/bin/sh
export TEXMF=/usr/share/texlive/texmf-dist;
export TEXMFCNF=/usr/share/texlive/texmf-dist/web2c;
export TEXMFCACHE=\$(realpath \$HOME/.cache/texlive);
%{_bindir}/mtxrun --script context "\$@"
EOF
chmod 0755 context

# fix texaccents
# TODO: Detect snobol4 version rather than hardcoding it here.
rm -f texaccents
cat > texaccents << EOF
#!/bin/sh
env SNOPATH=/usr/lib64/snobol4/2.3.1/lib:/usr/share/texlive/texmf-dist/scripts/texaccents /usr/bin/snobol4 /usr/share/texlive/texmf-dist/scripts/texaccents/texaccents.sno "\$@"
EOF
chmod 0755 texaccents
popd

# more texaccents fixes
mv %{buildroot}%{_texmf_main}/source/support/texaccents/* %{buildroot}%{_texmf_main}/scripts/texaccents
sed -i 's|host.inc|host.sno|g' %{buildroot}%{_texmf_main}/scripts/texaccents/texaccents.sno
sed -i 's|repl.inc|repl.sno|g' %{buildroot}%{_texmf_main}/scripts/texaccents/grepl.inc

# Move docs
mkdir -p %{buildroot}%{_datadir}/
mkdir -p %{buildroot}%{_infodir}/
cp -R %{buildroot}%{_texmf_main}/doc/man %{buildroot}%{_datadir}/
find %{buildroot}%{_texmf_main}/doc/man -type f | xargs rm -f
mv %{buildroot}%{_texmf_main}/doc/info/* %{buildroot}%{_infodir}/

# Remove cjk-gs-integrate files
# Yes, we probably should remove the source, but there is a possibility that we will
# re-add this subpackage at some point.
rm -rf %{buildroot}%{_bindir}/cjk-gs-integrate
rm -rf %{buildroot}%{_texmf_main}/scripts/cjk-gs-integrate
rm -rf %{buildroot}%{_texmf_main}/doc/fonts/cjk-gs-integrate
rm -rf %{buildroot}%{_texmf_main}/fonts/misc/cjk-gs-integrate

# Fix pkgconfig files
for file in $(find %{buildroot}%{_libdir}/pkgconfig/ -type f -name '*.pc')
do sed -i 's|%{_builddir}/%{name}-%{source_date}/source/inst|/usr|g' $file
   sed -i 's|/usr/lib|%{_libdir}|g' $file
done

# Python fixup
# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
pushd %{buildroot}
find -type f -exec sed -i '1s|^#!/usr/bin/python$|#!%{__python3}|' {} +
find -type f -exec sed -i '1s|^#!/usr/bin/env python$|#!%{__python3}|' {} +
sed -i '1s|^#!/usr/bin/python |#!%{__python3} |' ./%{_texmf_main}/scripts/de-macro/de-macro

# Get rid of the python2 variant bits from pythontex (we need them to generate the py3 bits, but not in the package)
rm -rf ./%{_texmf_main}/scripts/pythontex/pythontex2.py
rm -rf ./%{_texmf_main}/scripts/pythontex/depythontex2.py
popd

# One dir to own
mkdir -p %{buildroot}%{_texmf_main}/tex/generic/context/third

# TeXLive has a fork of psutils
# we namespace those binaries to avoid conflicts with the upstream psutils
pushd %{buildroot}%{_bindir}
for i in epsffit extractres includeres psbook psjoin psnup psresize psselect pstops
do mv $i tl-$i
done
popd
# we also rename the manpages
pushd %{buildroot}%{_mandir}/man1/
for i in epsffit extractres includeres psbook psjoin psnup psresize psselect pstops psutils
do mv $i.1 tl-$i.1
done
popd
# and move the config file
mkdir -p %{buildroot}%{_sysconfdir}/texlive/psutils
mv %{buildroot}%{_texmf_main}/psutils/paper.cfg %{buildroot}%{_sysconfdir}/texlive/psutils/paper.cfg
ln -s %{_sysconfdir}/texlive/psutils/paper.cfg %{buildroot}%{_texmf_main}/psutils/paper.cfg

# Some (most) of the binaries are ending up with RPATH despite our best efforts.
for i in afm2pl afm2tfm aleph bibtex bibtex8 bibtexu chkdvifont chktex ctie ctangle ctwill ctwill-refsort ctwill-twinx cweave detex disdvi dt2dv dv2dt dvi2tty dvibook dviconcat dvicopy dvilj dvilj2p dvilj4 dvilj4l dvipng \
         dvipos dvips dviselect dvispc dvisvgm dvitodvi dvitype eptex euptex gftodvi gftopk gftype gregorio gsftopk hbf2gf hitex kpsewhich luahbtex luatex mag makeindex makejvf mendex mf mflua mft mf-nowin mpost otftotfm msxlint \
         odvicopy odvitype omfonts otangle otp2ocp outocp patgen pbibtex pdftex pdftosrc pktogf pdvitype pfb2pfa pk2bm pktype pltotf pmpost pooltype ppltotf ps2pk ptekf ptex ptftopl synctex t4ht tangle tex tex4ht texprof tftopl tie tl-epsffit tl-psbook tl-psnup tl-psresize tl-psselect tl-pstops \
         ttf2afm ttf2pk ttf2tfm ttfdump twill upbibtex updvitype upmendex upmpost uppltotf uptex uptftopl vftovp vptovf weave wofm2opl wopl2ofm wovf2ovp wovp2ovf xdvi-xaw xdvipdfmx xdvipsk xetex; do
chrpath --delete %{buildroot}%{_bindir}/$i
done

%ifnarch %{power64} s390 s390x riscv64
chrpath --delete %{buildroot}%{_bindir}/luajithbtex
chrpath --delete %{buildroot}%{_bindir}/luajittex
chrpath --delete %{buildroot}%{_bindir}/mfluajit
%endif

# And remove the rpath from this library.
chrpath --delete %{buildroot}%{_libdir}/libptexenc.so.*

# This map file provided by texlive-scripts is not useful and confuses lots of things when it ends up in pdftex.map
# Renaming it should prevent it from being included
mv %{buildroot}%{_texmf_main}/fonts/map/dvips/tetex/dvipdfm35.map %{buildroot}%{_texmf_main}/fonts/map/dvips/tetex/dvipdfm35.oldmap

# SCRIPTLETS

%pretrans -p <lua>
path = "/usr/share/texmf"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end

%pre
rm -rf %{_texdir}/texmf-var
rm -rf %{_texmf_var}/*
:

%posttrans
if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
[ -x /sbin/restorecon ] && /sbin/restorecon -R %{_texmf_var}/
fi
:

%transfiletriggerin -n %{shortname}-context -- %{_texdir}
export TEXMFLOCAL=/usr/share/texlive/texmf-local
%{_bindir}/mtxrun --generate &> /dev/null || :

%transfiletriggerin -n %{shortname}-kpathsea -- %{_texdir}
# Commented lines are DEBUG mode
# touch /usr/share/texlive/kpathsea.log
# /usr/share/texlive/texmf-dist/scripts/texlive/mktexlsr --version 2>&1 | tee -a /usr/share/texlive/kpathsea.log || :
# /usr/share/texlive/texmf-dist/scripts/texlive/mktexlsr --verbose 2>&1 | tee -a /usr/share/texlive/kpathsea.log || :
# /usr/bin/sh -x %{_bindir}/texhash 2>&1 | tee -a /usr/share/texlive/kpathsea.log || :
/usr/share/texlive/texmf-dist/scripts/texlive/mktexlsr 2> /dev/null || :
export TEXMF=/usr/share/texlive/texmf-dist
export TEXMFCNF=/usr/share/texlive/texmf-dist/web2c
export TEXMFCACHE=/var/lib/texmf
# %{_bindir}/fmtutil-sys --all 2>&1 | tee -a /usr/share/texlive/kpathsea.log || :
%{_bindir}/fmtutil-sys --all &> /dev/null || :

%transfiletriggerpostun -n %{shortname}-kpathsea -- %{_texdir}
/usr/share/texlive/texmf-dist/scripts/texlive/mktexlsr 2> /dev/null || :

%transfiletriggerin -n %{shortname}-kpathsea -- %{_texdir}/texmf-dist/fonts/map/dvips/
# MixedMap list, from directory with _EVERY_ tex subpackage unpacked: for i in `grep -r "addMixedMap" tlpkg/ |cut -d ":" -f 2- | sort -n | uniq | cut -d " " -f 3`; do printf "$i|"; done
# Map list, from directory with _EVERY_ tex subpackage unpacked: for i in `grep -r "addMap" tlpkg/ |cut -d ":" -f 2- | sort -n | uniq | cut -d " " -f 3`; do printf "$i|"; done
# NO OTHER MAPS SHOULD BE ADDED. That road leads to madness.
list=`grep "\.map" | sort -n | uniq`
while read -r line; do
        [ -z "$line" ] && continue
        shortfile=`basename "$line"`
        if `echo $shortfile | grep -Eq 'allrunes.map|arabtex.map|arss.map|artm.map|bbold.map|cbgreek-full.map|ccpl.map|cmextra.map|cmll.map|cm.map|cm-super-t1.map|cm-super-t2a.map|cm-super-t2b.map|cm-super-t2c.map|cm-super-ts1.map|cm-super-x2.map|cmtext-bsr-interpolated.map|cmupint.map|cyrillic.map|esint.map|ethiop.map|eurosym.map|hfbright.map|iby.map|latxfont.map|lxfonts.map|manfnt.map|mflogo.map|mongolian.map|musix.map|pigpen.map|plother.map|pltext.map|rsfs.map|semaf.map|stmaryrd.map|symbols.map|tipa.map|trajan.map|vnrother.map|vnrtext.map|wasy.map|xypic.map|yhmath.map'`; then
                %{_bindir}/updmap-sys --nomkmap --enable MixedMap=$shortfile >/dev/null 2>&1 || :
        else
                if `echo $shortfile | grep -Eq 'accanthis.map|Acorn.map|aesupp.map|Alegreya.map|AlgolRevived.map|almendra.map|AnnSton.map|AnonymousPro.map|antt.map|ap.map|arabi.map|archaicprw.map|arev.map|arevvn.map|arimo.map|ArrowsADF.map|ArtNouvc.map|ArtNouv.map|ascii.map|ascmac.map|aspectratio.map|atkinson.map|augie.map|auncial.map|aurical.map|Baskervaldx.map|BaskervilleF.map|belleek.map|bera.map|beuron.map|bguq.map|bitter.map|bkaiu.map|boondox.map|bsmiu.map|BulletsADF.map|burmese.map|cabin.map|caladea.map|calligra.map|cantarell.map|carlito.map|Carrickc.map|CascadiaCodThree.map|ccicons.map|charter.map|chartervn.map|chemarrow.map|cherokee.map|Chivo.map|cinzel.map|cjhebrew.map|Clara.map|ClearSans.map|clm.map|cmathbb.map|cmbrightvn.map|cmcyr.map|cmexb.map|cmin.map|cm-lgc.map|cmsrb.map|Cochineal.map|Coelacanth.map|comfortaa.map|ComicNeueAngular.map|ComicNeue.map|concretevn.map|CormorantGaramond.map|countriesofeurope.map|CourierOneZeroPitch.map|crimson.map|CrimsonPro.map|cs-charter.map|csfonts.map|cuprum.map|cyklop.map|dad.map|dante.map|dejavu-type1.map|dgj.map|dictsym.map|dmj.map|Domitian.map|droidsans.map|droidsansmono.map|droidserif.map|DSSerif.map|dstroke.map|dutchcal.map|EBGaramond.map|EBGaramond-Maths.map|Eichenla.map|EileenBl.map|Eileen.map|Elzevier.map|epigrafica.map|epiolmec.map|erewhon.map|esrelation.map|ESSTIX.map|esvect.map|ETbb.map|fbb.map|fdsymbol.map|fetamont.map|fge.map|fira.map|foekfont.map|fonetika.map|fontawesome5.map|fontawesome.map|forum.map|fourier.map|fourier-utopia-expert.map|fpls.map|frcursive.map|GaramondLibre.map|garuda-c90.map|gbsnu.map|gentium-type1.map|gfsartemisia.map|gfsbaskerville.map|gfsbodoni.map|gfscomplutum.map|gfsdidot.map|gfsneohellenic.map|gfsporson.map|gfssolomos.map|gillius.map|gkaiu.map|go.map|GotIn.map|GoudyIn.map|gptimes.map|grotesqvn.map|Gudea.map|hacm.map|Heuristica.map|HindMadurai.map|ibarra.map|icelandic.map|imfellEnglish.map|InriaSans.map|InriaSerif.map|Inter.map|ipaex-type1.map|iwona.map|josefin.map|Junicode.map|kerkis.map|Kinigcap.map|knitfont.map|Konanur.map|kpfonts.map|Kramer.map|kurier.map|l7x-urwvn.map|lato.map|libertinegc.map|libertine.map|libertinus.map|libertinust1math.map|LibreBaskerville.map|LibreBodoni.map|LibreCaslon.map|LibreFranklin.map|linearA.map|LinguisticsPro.map|lm.map|LobsterTwo.map|Magra.map|marcellus.map|marvosym.map|mathabx.map|mc2j.map|mcj.map|mdbch.map|mdgreek.map|mdici.map|mdpgd.map|mdpus.map|mdput.map|mdsymbol.map|mdugm.map|merriweather.map|miama.map|mintspirit.map|mlm.map|MnSymbol.map|Montserrat.map|MorrisIn.map|mr2j.map|mrj.map|mxedruli.map|nanumfonts.map|nectec.map|newpx.map|newtx.map|newtxsf.map|newtxtt.map|nf.map|niceframe.map|nimbus15.map|norasi-c90.map|noto.map|NotoMath.map|Nouveaud.map|oasy.map|ocrb.map|oinuit.map|OldStandard.map|omega.map|opensans.map|OrnementsADF.map|overlock.map|paratype-type1.map|pazo.map|pbsi.map|phaistos.map|PlayfairDisplay.map|plex.map|plimsoll.map|PoiretOne.map|prodint.map|pxfonts.map|pxtx.map|qag.map|qbk.map|qcr.map|qcs.map|qhv.map|qpl.map|qtm.map|quattrocento.map|qzc.map|Raleway.map|recycle.map|roboto.map|rojud.map|Romantik.map|Rosario.map|Rothdn.map|RoyalIn.map|rsfso.map|Sanremo.map|sansmathaccent.map|sansmathfonts.map|scanpages.map|ScholaX.map|sipa.map|SkakNew.map|skt.map|SourceCodePro.map|SourceSansPro.map|SourceSerifPro.map|spectral.map|sqrcaps.map|Starburst.map|starfont.map|STEPGreekTest.map|STEP.map|SticksTooText.map|stix2.map|stix.map|superiors.map|svrsymbols.map|syriac.map|tabvar.map|tempora.map|tfrupee.map|TheanoDidot.map|TheanoModern.map|TheanoOldStyle.map|tinos.map|tlwg.map|txfonts.map|txttvn.map|TXUprCal.map|Typocaps.map|uag.map|uaq.map|ubk.map|ucr.map|ugq.map|uhv.map|umj.map|unc.map|universalis.map|upl.map|urwvn.map|usy.map|utm.map|utopia.map|uzc.map|uzd.map|vntopia.map|XCharter.map|ybd.map|ybv.map|yes.map|yfrak.map|yly.map|yrd.map|yv1.map|yv2.map|yv3.map|yvo.map|yvt.map|Zallman.map|Zeroswald.map|zi4.map'`; then
                        %{_bindir}/updmap-sys --nomkmap --enable Map=$shortfile >/dev/null 2>&1 || :
                fi
        fi
done <<< "$list"
# With the demise of updmap-map, we need to make system maps here.
# %{_bindir}/updmap-sys --quiet --nomkmap >/dev/null || :
yes | %{_bindir}/updmap-sys --quiet --syncwithtrees >/dev/null 2>&1 || :
%{_bindir}/updmap-sys --quiet --force 2>&1 || :

%transfiletriggerpostun -n %{shortname}-kpathsea -- %{_texdir}/texmf-dist/fonts/map/dvips/
# I am not sure we need to do this, but it is not harmful.
# TODO: see if we can safely remove everything above the updmap-sys calls
list=`grep "\.map" | sort -n | uniq`
while read -r line; do
        [ -z "$line" ] && continue
        shortfile=`basename "$line"`
        if `echo $shortfile | grep -Eq 'allrunes.map|arabtex.map|arss.map|artm.map|bbold.map|cbgreek-full.map|ccpl.map|cmextra.map|cmll.map|cm.map|cm-super-t1.map|cm-super-t2a.map|cm-super-t2b.map|cm-super-t2c.map|cm-super-ts1.map|cm-super-x2.map|cmtext-bsr-interpolated.map|cmupint.map|cyrillic.map|esint.map|ethiop.map|eurosym.map|hfbright.map|iby.map|latxfont.map|lxfonts.map|manfnt.map|mflogo.map|mongolian.map|musix.map|pigpen.map|plother.map|pltext.map|rsfs.map|semaf.map|stmaryrd.map|symbols.map|tipa.map|trajan.map|vnrother.map|vnrtext.map|wasy.map|xypic.map|yhmath.map'`; then
                %{_bindir}/updmap-sys --nomkmap --disable MixedMap=$shortfile >/dev/null 2>&1 || :
        else
                if `echo $shortfile | grep -Eq 'accanthis.map|Acorn.map|aesupp.map|Alegreya.map|AlgolRevived.map|almendra.map|AnnSton.map|AnonymousPro.map|antt.map|ap.map|arabi.map|archaicprw.map|arev.map|arevvn.map|arimo.map|ArrowsADF.map|ArtNouvc.map|ArtNouv.map|ascii.map|ascmac.map|aspectratio.map|atkinson.map|augie.map|auncial.map|aurical.map|Baskervaldx.map|BaskervilleF.map|belleek.map|bera.map|beuron.map|bguq.map|bitter.map|bkaiu.map|boondox.map|bsmiu.map|BulletsADF.map|burmese.map|cabin.map|caladea.map|calligra.map|cantarell.map|carlito.map|Carrickc.map|CascadiaCodThree.map|ccicons.map|charter.map|chartervn.map|chemarrow.map|cherokee.map|Chivo.map|cinzel.map|cjhebrew.map|Clara.map|ClearSans.map|clm.map|cmathbb.map|cmbrightvn.map|cmcyr.map|cmexb.map|cmin.map|cm-lgc.map|cmsrb.map|Cochineal.map|Coelacanth.map|comfortaa.map|ComicNeueAngular.map|ComicNeue.map|concretevn.map|CormorantGaramond.map|countriesofeurope.map|CourierOneZeroPitch.map|crimson.map|CrimsonPro.map|cs-charter.map|csfonts.map|cuprum.map|cyklop.map|dad.map|dante.map|dejavu-type1.map|dgj.map|dictsym.map|dmj.map|Domitian.map|droidsans.map|droidsansmono.map|droidserif.map|DSSerif.map|dstroke.map|dutchcal.map|EBGaramond.map|EBGaramond-Maths.map|Eichenla.map|EileenBl.map|Eileen.map|Elzevier.map|epigrafica.map|epiolmec.map|erewhon.map|esrelation.map|ESSTIX.map|esvect.map|ETbb.map|fbb.map|fdsymbol.map|fetamont.map|fge.map|fira.map|foekfont.map|fonetika.map|fontawesome5.map|fontawesome.map|forum.map|fourier.map|fourier-utopia-expert.map|fpls.map|frcursive.map|GaramondLibre.map|garuda-c90.map|gbsnu.map|gentium-type1.map|gfsartemisia.map|gfsbaskerville.map|gfsbodoni.map|gfscomplutum.map|gfsdidot.map|gfsneohellenic.map|gfsporson.map|gfssolomos.map|gillius.map|gkaiu.map|go.map|GotIn.map|GoudyIn.map|gptimes.map|grotesqvn.map|Gudea.map|hacm.map|Heuristica.map|HindMadurai.map|ibarra.map|icelandic.map|imfellEnglish.map|InriaSans.map|InriaSerif.map|Inter.map|ipaex-type1.map|iwona.map|josefin.map|Junicode.map|kerkis.map|Kinigcap.map|knitfont.map|Konanur.map|kpfonts.map|Kramer.map|kurier.map|l7x-urwvn.map|lato.map|libertinegc.map|libertine.map|libertinus.map|libertinust1math.map|LibreBaskerville.map|LibreBodoni.map|LibreCaslon.map|LibreFranklin.map|linearA.map|LinguisticsPro.map|lm.map|LobsterTwo.map|Magra.map|marcellus.map|marvosym.map|mathabx.map|mc2j.map|mcj.map|mdbch.map|mdgreek.map|mdici.map|mdpgd.map|mdpus.map|mdput.map|mdsymbol.map|mdugm.map|merriweather.map|miama.map|mintspirit.map|mlm.map|MnSymbol.map|Montserrat.map|MorrisIn.map|mr2j.map|mrj.map|mxedruli.map|nanumfonts.map|nectec.map|newpx.map|newtx.map|newtxsf.map|newtxtt.map|nf.map|niceframe.map|nimbus15.map|norasi-c90.map|noto.map|NotoMath.map|Nouveaud.map|oasy.map|ocrb.map|oinuit.map|OldStandard.map|omega.map|opensans.map|OrnementsADF.map|overlock.map|paratype-type1.map|pazo.map|pbsi.map|phaistos.map|PlayfairDisplay.map|plex.map|plimsoll.map|PoiretOne.map|prodint.map|pxfonts.map|pxtx.map|qag.map|qbk.map|qcr.map|qcs.map|qhv.map|qpl.map|qtm.map|quattrocento.map|qzc.map|Raleway.map|recycle.map|roboto.map|rojud.map|Romantik.map|Rosario.map|Rothdn.map|RoyalIn.map|rsfso.map|Sanremo.map|sansmathaccent.map|sansmathfonts.map|scanpages.map|ScholaX.map|sipa.map|SkakNew.map|skt.map|SourceCodePro.map|SourceSansPro.map|SourceSerifPro.map|spectral.map|sqrcaps.map|Starburst.map|starfont.map|STEPGreekTest.map|STEP.map|SticksTooText.map|stix2.map|stix.map|superiors.map|svrsymbols.map|syriac.map|tabvar.map|tempora.map|tfrupee.map|TheanoDidot.map|TheanoModern.map|TheanoOldStyle.map|tinos.map|tlwg.map|txfonts.map|txttvn.map|TXUprCal.map|Typocaps.map|uag.map|uaq.map|ubk.map|ucr.map|ugq.map|uhv.map|umj.map|unc.map|universalis.map|upl.map|urwvn.map|usy.map|utm.map|utopia.map|uzc.map|uzd.map|vntopia.map|XCharter.map|ybd.map|ybv.map|yes.map|yfrak.map|yly.map|yrd.map|yv1.map|yv2.map|yv3.map|yvo.map|yvt.map|Zallman.map|Zeroswald.map|zi4.map'`; then
                        %{_bindir}/updmap-sys --nomkmap --disable Map=$shortfile >/dev/null 2>&1 || :
                fi
        fi
done <<< "$list"
# With the demise of updmap-map, we need to make system maps here.
# %{_bindir}/updmap-sys --quiet --nomkmap >/dev/null || :
yes | %{_bindir}/updmap-sys --quiet --syncwithtrees >/dev/null 2>&1 || :
%{_bindir}/updmap-sys --quiet --force 2>&1 || :

%transfiletriggerin -n %{shortname}-kpathsea -P 2000000 -- %{_texdir}/fmtutil.cnf.d/
%{_sbindir}/generate-fmtutilcnf %{_texdir}

%transfiletriggerpostun -n %{shortname}-kpathsea -P 2000000 -- %{_texdir}/fmtutil.cnf.d/
%{_sbindir}/generate-fmtutilcnf %{_texdir}

%files
%{_texdir}/licenses/
%{_texdir}/texlive.tlpdb
%{_texdir}/tlpkg/texlive.tlpdb
%{_fileattrsdir}/texlive.attr
%{_rpmmacrodir}/macros.texlive
# Mostly we own directories.
%dir %{_sysconfdir}/%{shortname}
%dir %{_sysconfdir}/%{shortname}/dvips
%dir %{_sysconfdir}/%{shortname}/dvips/config
%dir %{_sysconfdir}/%{shortname}/tex
%dir %{_sysconfdir}/%{shortname}/tex/generic
%dir %{_sysconfdir}/%{shortname}/tex/generic/config
%dir %{_sysconfdir}/%{shortname}/web2c
%dir %{_texdir}
%dir %{_texmf_main}
%dir %{_texmf_main}/bibtex/
%dir %{_texmf_main}/bibtex/csf
%dir %{_texmf_main}/bibtex/csf/base
%dir %{_texmf_main}/doc
%dir %{_texmf_main}/doc/info
%dir %{_texmf_main}/doc/man
%dir %{_texmf_main}/doc/man/man1
%dir %{_texmf_main}/doc/man/man5
%dir %{_texmf_main}/dvips
%dir %{_texmf_main}/dvips/config
%dir %{_texmf_main}/fonts
%dir %{_texmf_main}/fonts/cmap
%dir %{_texmf_main}/fonts/enc
%dir %{_texmf_main}/fonts/enc/dvips
%dir %{_texmf_main}/fonts/map
%dir %{_texmf_main}/fonts/map/dvips
%dir %{_texmf_main}/fonts/map/glyphlist
%dir %{_texmf_main}/fonts/sfd
%dir %{_texmf_main}/scripts
%dir %{_texmf_main}/scripts/texlive
%dir %{_texmf_main}/source
%dir %{_texmf_main}/source/fonts
%dir %{_texmf_main}/source/fonts/zhmetrics
%dir %{_texmf_main}/tex
%dir %{_texmf_main}/tex/generic
%dir %{_texmf_main}/tex/generic/bibtex
%dir %{_texmf_main}/tex/generic/config
%dir %{_texmf_main}/tex/latex
%dir %{_texmf_main}/tex/lualatex
%dir %{_texmf_main}/tex/luatex
%dir %{_texmf_main}/tex/xelatex
%dir %{_texmf_main}/web2c
%dir %{_texmf_var}
%doc %{_texdir}/doc.html
%{_texdir}/texmf-var
%{_texdir}/texmf-local/
%{_datadir}/texmf
%ghost %{_datadir}/texmf.rpmmoved

%files -n %{shortname}-a2ping
%license gpl.txt
%{_bindir}/a2ping
%{_texmf_main}/scripts/a2ping/
%{_mandir}/man1/a2ping.1*
%doc %{_texmf_main}/doc/support/a2ping/

%files -n %{shortname}-accfonts
%license gpl.txt
%{_bindir}/mkt1font
%{_bindir}/vpl2ovp
%{_bindir}/vpl2vpl
%{_texmf_main}/scripts/accfonts/
%{_texmf_main}/tex/latex/accfonts/
%doc %{_texmf_main}/doc/fonts/accfonts/

%files -n %{shortname}-adhocfilelist
%license lppl1.txt
%{_bindir}/adhocfilelist
%{_texmf_main}/scripts/adhocfilelist/
%{_texmf_main}/tex/support/adhocfilelist/
%doc %{_texmf_main}/doc/support/adhocfilelist/

%files -n %{shortname}-afm2pl
%license lppl1.txt
%{_bindir}/afm2pl
%{_mandir}/man1/afm2pl.1*
%{_texmf_main}/fonts/enc/dvips/afm2pl/
%{_texmf_main}/fonts/lig/afm2pl/
%{_texmf_main}/tex/fontinst/afm2pl/

%files -n %{shortname}-albatross
%license bsd.txt
%{_bindir}/albatross
%{_mandir}/man1/albatross.*
%doc %{_texmf_main}/doc/support/albatross
%{_texmf_main}/scripts/albatross

%files -n %{shortname}-aleph
%license lgpl.txt
%doc %{_texmf_main}/doc/aleph/
%{_bindir}/aleph
# symlink to aleph, not created in 2021
# %%{_bindir}/lamed
%{_mandir}/man1/aleph.1*
# %%{_mandir}/man1/lamed.1*
%{fmtutil_cnf_d}/aleph

%files -n %{shortname}-amstex
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/amstex/base/
%{_bindir}/amstex
%{_mandir}/man1/amstex.1*
%{_texmf_main}/tex/amstex/
%{fmtutil_cnf_d}/amstex

%files -n %{shortname}-aomart
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/aomart
%{_bindir}/aom-fullref
%{_mandir}/man1/aom-fullref.1*
%{_texmf_main}/bibtex/bst/aomart/
%{_texmf_main}/scripts/aomart/
%{_texmf_main}/tex/latex/aomart/

%files -n %{shortname}-arara
%license bsd.txt
%doc %{_texmf_main}/doc/support/arara/
%{_bindir}/arara
%{_mandir}/man1/arara.*
%{_texmf_main}/scripts/arara/

%files -n %{shortname}-attachfile2
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/attachfile2/
%{_bindir}/pdfatfi
%{_mandir}/man1/pdfatfi.1*
%{_texmf_main}/scripts/attachfile2/
%{_texmf_main}/tex/latex/attachfile2/

%files -n %{shortname}-authorindex
%license lppl1.txt
%{_bindir}/authorindex
%{_texmf_main}/scripts/authorindex/
%{_texmf_main}/tex/latex/authorindex/
%doc %{_texmf_main}/doc/latex/authorindex/

%files -n %{shortname}-autosp
%license gpl2.txt
%doc %{_texmf_main}/doc/generic/autosp/
%{_bindir}/autosp
%{_bindir}/tex2aspc
%{_mandir}/man1/autosp.1*
%{_mandir}/man1/tex2aspc.1*

%files -n %{shortname}-axodraw2
%license gpl3.txt
%doc %{_texmf_main}/doc/latex/axodraw2/
%{_bindir}/axohelp
%{_mandir}/man1/axohelp.1*
%{_texmf_main}/tex/latex/axodraw2/

%files -n %{shortname}-bib2gls
%license gpl3.txt
%doc %{_texmf_main}/doc/support/bib2gls/
%{_bindir}/bib2gls
%{_bindir}/convertgls2bib
%{_bindir}/datatool2bib
%{_mandir}/man1/bib2gls.1*
%{_mandir}/man1/convertgls2bib.1*
%{_mandir}/man1/datatool2bib.1*
%{_texmf_main}/scripts/bib2gls/

%files -n %{shortname}-bibcop
%license mit.txt
%doc %{_texmf_main}/doc/bibtex/bibcop
%{_bindir}/bibcop
%{_mandir}/man1/bibcop.1*
%{_texmf_main}/scripts/bibcop
%{_texmf_main}/tex/latex/bibcop

%files -n %{shortname}-bibexport
%license lppl1.3.txt
%{_bindir}/bibexport
%{_bindir}/bibexport.sh
%{_texmf_main}/bibtex/bst/bibexport/
%{_texmf_main}/scripts/bibexport/
%doc %{_texmf_main}/doc/bibtex/bibexport/

%files -n %{shortname}-bibtex
%license knuth.txt
%doc %{_texmf_main}/doc/bibtex/base/README
%doc %{_texmf_main}/doc/bibtex/base/btxbst.doc
%doc %{_texmf_main}/doc/bibtex/base/btxdoc.bib
%doc %{_texmf_main}/doc/bibtex/base/btxdoc.pdf
%doc %{_texmf_main}/doc/bibtex/base/btxdoc.tex
%doc %{_texmf_main}/doc/bibtex/base/btxhak.pdf
%doc %{_texmf_main}/doc/bibtex/base/btxhak.tex
%{_bindir}/bibtex
%{_mandir}/man1/bibtex.1*
%{_texmf_main}/bibtex/bib/
%{_texmf_main}/bibtex/bst/
%{_texmf_main}/tex/generic/bibtex/apalike.sty
%{_texmf_main}/tex/generic/bibtex/apalike.tex

%files -n %{shortname}-bibtexperllibs
%license gpl.txt
%license artistic2.txt
%license pd.txt
%{_mandir}/man1/ltx2unitxt.1*

%files -n %{shortname}-bibtexu
%license lppl1.txt
%{_bindir}/bibtexu
%doc %{_texmf_main}/doc/bibtexu/
%{_mandir}/man1/bibtexu.1*

%files -n %{shortname}-bibtex8
%license gpl2.txt
%doc %{_texmf_main}/doc/bibtex8/
%{_bindir}/bibtex8
%{_mandir}/man1/bibtex8.1*
%{_texmf_main}/bibtex/csf/base/88591lat.csf
%{_texmf_main}/bibtex/csf/base/88591sca.csf
%{_texmf_main}/bibtex/csf/base/README.TEXLIVE
%{_texmf_main}/bibtex/csf/base/ascii.csf
%{_texmf_main}/bibtex/csf/base/cp437lat.csf
%{_texmf_main}/bibtex/csf/base/cp850lat.csf
%{_texmf_main}/bibtex/csf/base/cp850sca.csf
%{_texmf_main}/bibtex/csf/base/cp866rus.csf
%{_texmf_main}/bibtex/csf/base/csfile.txt
%{_texmf_main}/bibtex/csf/polish-csf/88592pl.csf
%{_texmf_main}/bibtex/csf/polish-csf/cp1250pl.csf
%{_texmf_main}/bibtex/csf/polish-csf/cp852pl.csf
%{_texmf_main}/bibtex/csf/polish-csf/iso8859-7.csf

%files -n %{shortname}-bookshelf
%license lppl1.3.txt
%{_bindir}/bookshelf-listallfonts
%{_bindir}/bookshelf-mkfontsel
%{_mandir}/man1/bookshelf-listallfonts.1*
%{_mandir}/man1/bookshelf-mkfontsel.1*
%{_texmf_main}/bibtex/bst/bookshelf/
%{_texmf_main}/scripts/bookshelf/
%{_texmf_main}/tex/latex/bookshelf/
%doc %{_texmf_main}/doc/latex/bookshelf/

%files -n %{shortname}-bundledoc
%license lppl1.txt
%{_bindir}/arlatex
%{_bindir}/bundledoc
%{_mandir}/man1/arlatex.1*
%{_mandir}/man1/bundledoc.1*
%{_texmf_main}/scripts/bundledoc/
%{_texmf_main}/tex/latex/bundledoc/
%doc %{_texmf_main}/doc/support/bundledoc/

%files -n %{shortname}-cachepic
%license lppl1.3.txt
%{_bindir}/cachepic
%{_texmf_main}/scripts/cachepic/
%{_texmf_main}/tex/latex/cachepic/
%doc %{_texmf_main}/doc/latex/cachepic/

%files -n %{shortname}-checkcites
%license lppl1.3.txt
%{_bindir}/checkcites
%{_texmf_main}/scripts/checkcites/
%doc %{_texmf_main}/doc/support/checkcites/

%files -n %{shortname}-checklistings
%license lppl1.2.txt
%{_bindir}/checklistings
%{_texmf_main}/scripts/checklistings/
%{_texmf_main}/tex/latex/checklistings/
%doc %{_texmf_main}/doc/latex/checklistings/

%files -n %{shortname}-chklref
%license gpl3.txt
%{_bindir}/chklref
%{_mandir}/man1/chklref.1*
%{_texmf_main}/scripts/chklref/
%{_texmf_main}/tex/latex/chklref/
%doc %{_texmf_main}/doc/support/chklref/

%files -n %{shortname}-chktex
%license gpl2.txt
%doc %{_texmf_main}/doc/chktex/
%{_bindir}/chktex
%{_bindir}/chkweb
%{_bindir}/deweb
%{_mandir}/man1/chktex.1*
%{_mandir}/man1/chkweb.1*
%{_mandir}/man1/deweb.1*
%{_texmf_main}/chktex/
%{_texmf_main}/scripts/chktex/

%files -n %{shortname}-citation-style-language
%license mit.txt
%license cc-zero-1.txt
%license other-free.txt
%doc %{_texmf_main}/doc/latex/citation-style-language/
%{_bindir}/citeproc-lua
%{_mandir}/man1/citeproc-lua.1*
%{_texmf_main}/scripts/citation-style-language/
%{_texmf_main}/tex/latex/citation-style-language/

%if 0
%files -n %{shortname}-cjk-gs-integrate
%license gpl3.txt
%{_bindir}/cjk-gs-integrate
%{_texmf_main}/scripts/cjk-gs-integrate/
%{_texmf_main}/fonts/misc/cjk-gs-integrate/
%doc %{_texmf_main}/doc/fonts/cjk-gs-integrate/
%endif

%files -n %{shortname}-cjkutils
%license lppl1.txt
%{_bindir}/bg5+latex
%{_bindir}/bg5+pdflatex
%{_bindir}/bg5conv
%{_bindir}/bg5latex
%{_bindir}/bg5pdflatex
%{_bindir}/cef5conv
%{_bindir}/cef5latex
%{_bindir}/cef5pdflatex
%{_bindir}/cefconv
%{_bindir}/ceflatex
%{_bindir}/cefpdflatex
%{_bindir}/cefsconv
%{_bindir}/cefslatex
%{_bindir}/cefspdflatex
%{_bindir}/extconv
%{_bindir}/gbklatex
%{_bindir}/gbkpdflatex
%{_bindir}/hbf2gf
%{_bindir}/sjisconv
%{_bindir}/sjislatex
%{_bindir}/sjispdflatex
%{_mandir}/man1/bg5conv.1*
%{_mandir}/man1/cef5conv.1*
%{_mandir}/man1/cefconv.1*
%{_mandir}/man1/cefsconv.1*
%{_mandir}/man1/extconv.1*
%{_mandir}/man1/hbf2gf.1*
%{_mandir}/man1/sjisconv.1*
%{_texmf_main}/hbf2gf/

%files -n %{shortname}-clojure-pamphlet
%license gpl3.txt
%doc %{_texmf_main}/doc/support/clojure-pamphlet/
%{_bindir}/pamphletangler
%{_mandir}/man1/pamphletangler.1*
%{_texmf_main}/scripts/clojure-pamphlet/
%{_texmf_main}/tex/latex/clojure-pamphlet/

%files -n %{shortname}-cluttex
%license gpl3.txt
%{_bindir}/cllualatex
%{_bindir}/cluttex
%{_bindir}/clxelatex
%{_texmf_main}/scripts/cluttex/
%{_mandir}/man1/cllualatex.1*
%{_mandir}/man1/cluttex.1*
%{_mandir}/man1/clxelatex.1*
%doc %{_texmf_main}/doc/support/cluttex/

%files -n %{shortname}-context
%license other-free.txt
%dir %{_texmf_main}/metapost/context/
%dir %{_texmf_main}/metapost/context/base/
%exclude %{_texmf_main}/scripts/context/perl/mptopdf.pl
%exclude %{_texmf_main}/scripts/context/ruby
%exclude %{_texmf_main}/scripts/context/stubs
%exclude %{_texmf_main}/tex/context/base/mkii
%exclude %{_texmf_main}/tex/context/bib/mkii
%exclude %{_texmf_main}/tex/context/fonts/mkii
%exclude %{_texmf_main}/tex/context/modules/common
%exclude %{_texmf_main}/tex/context/modules/mkii
%exclude %{_texmf_main}/tex/context/patterns/mkii
%exclude %{_texmf_main}/tex/context/user/mkii
%{_bindir}/context
# %%{_bindir}/contextjit
# %%{_bindir}/luatools
%{_bindir}/mtxrun
# %%{_bindir}/mtxrunjit
# %%{_bindir}/texexec
# %%{_bindir}/texmfstart
%{_mandir}/man1/context.1*
# %%{_mandir}/man1/luatools.1*
%{_mandir}/man1/mtxrun-babel.1*
%{_mandir}/man1/mtxrun-base.1*
%{_mandir}/man1/mtxrun-bibtex.1*
%{_mandir}/man1/mtxrun-cache.1*
%{_mandir}/man1/mtxrun-chars.1*
%{_mandir}/man1/mtxrun-check.1*
%{_mandir}/man1/mtxrun-colors.1*
%{_mandir}/man1/mtxrun-context.1*
%{_mandir}/man1/mtxrun-convert.1*
%{_mandir}/man1/mtxrun-ctan.1*
%{_mandir}/man1/mtxrun-dvi.1*
%{_mandir}/man1/mtxrun-epub.1*
%{_mandir}/man1/mtxrun-evohome.1*
%{_mandir}/man1/mtxrun-fcd.1*
%{_mandir}/man1/mtxrun-fixpdf.1*
%{_mandir}/man1/mtxrun-flac.1*
%{_mandir}/man1/mtxrun-fonts.1*
%{_mandir}/man1/mtxrun-grep.1*
%{_mandir}/man1/mtxrun-interface.1*
%{_mandir}/man1/mtxrun-kpse.1*
%{_mandir}/man1/mtxrun-metapost.1*
%{_mandir}/man1/mtxrun-modules.1*
%{_mandir}/man1/mtxrun-package.1*
%{_mandir}/man1/mtxrun-patterns.1*
%{_mandir}/man1/mtxrun-pdf.1*
%{_mandir}/man1/mtxrun-plain.1*
%{_mandir}/man1/mtxrun-profile.1*
%{_mandir}/man1/mtxrun-rsync.1*
%{_mandir}/man1/mtxrun-scite.1*
%{_mandir}/man1/mtxrun-server.1*
%{_mandir}/man1/mtxrun-spell.1*
%{_mandir}/man1/mtxrun-synctex.1*
%{_mandir}/man1/mtxrun-texworks.1*
%{_mandir}/man1/mtxrun-tools.1*
%{_mandir}/man1/mtxrun-unicode.1*
%{_mandir}/man1/mtxrun-unzip.1*
%{_mandir}/man1/mtxrun-update.1*
%{_mandir}/man1/mtxrun-vscode.1*
%{_mandir}/man1/mtxrun-watch.1*
%{_mandir}/man1/mtxrun-youless.1*
%{_mandir}/man1/mtxrun.1*
# %%{_mandir}/man1/texexec.1*
# %%{_mandir}/man1/texmfstart.1*
# %%{_texmf_main}/context/
# %%{_texmf_main}/fonts/fea/context/
# %%{_texmf_main}/fonts/map/luatex/context/
%{_texmf_main}/fonts/opentype/public/context/
%{_texmf_main}/fonts/truetype/public/context/
%{_texmf_main}/metapost/context/base/common/
%{_texmf_main}/metapost/context/base/mpiv/
%{_texmf_main}/metapost/context/base/mpxl/
%{_texmf_main}/metapost/context/fonts/
%{_texmf_main}/scripts/context/
%{_texmf_main}/tex/context/
%{_texmf_main}/tex/luatex/context/

%files -n %{shortname}-context-doc
%doc %{_texmf_main}/doc/context/
%doc %{_texmf_main}/doc/fonts/context/
%doc %{_texmf_main}/doc/luametatex/
%exclude %{_texmf_main}/doc/context/scripts/mkii

%files -n %{shortname}-context-legacy
%dir %{_texmf_main}/bibtex/bst/context/
%doc %{_texmf_main}/doc/context/scripts/mkii
# these four are in mptopdf
%exclude %{_texmf_main}/tex/context/base/mkii/supp-mis.mkii
%exclude %{_texmf_main}/tex/context/base/mkii/supp-mpe.mkii
%exclude %{_texmf_main}/tex/context/base/mkii/supp-pdf.mkii
%exclude %{_texmf_main}/tex/context/base/mkii/syst-tex.mkii
%exclude %{_texmf_main}/tex/generic/context/mptopdf
%{_bindir}/texexec
%{_bindir}/texmfstart
%{_mandir}/man1/texexec.1*
%{_mandir}/man1/texmfstart.1*
%{_texmf_main}/bibtex/bst/context/mkii/cont-ab.bst
%{_texmf_main}/bibtex/bst/context/mkii/cont-au.bst
%{_texmf_main}/bibtex/bst/context/mkii/cont-no.bst
%{_texmf_main}/bibtex/bst/context/mkii/cont-ti.bst
%{_texmf_main}/fonts/afm/public/context/
%{_texmf_main}/fonts/cid/
%{_texmf_main}/fonts/enc/dvips/context/
%{_texmf_main}/fonts/map/dvips/context/
%{_texmf_main}/fonts/map/pdftex/context/
%{_texmf_main}/fonts/misc/xetex/fontmapping/context/
%{_texmf_main}/fonts/tfm/public/context/
%{_texmf_main}/fonts/type1/public/context/
%{_texmf_main}/metapost/context/base/mpii/
%{_texmf_main}/scripts/context/ruby/
%{_texmf_main}/scripts/context/stubs/
%{_texmf_main}/tex/context/base/mkii
%{_texmf_main}/tex/context/bib/mkii/
%{_texmf_main}/tex/context/fonts/mkii/
%{_texmf_main}/tex/context/modules/common/
%{_texmf_main}/tex/context/modules/mkii/
%{_texmf_main}/tex/context/patterns/mkii/
%{_texmf_main}/tex/context/user/mkii/
%{_texmf_main}/tex/generic/context/
%{fmtutil_cnf_d}/context-legacy

%files -n %{shortname}-convbkmk
%{_bindir}/convbkmk
%{_texmf_main}/scripts/convbkmk/
%doc %{_texmf_main}/doc/support/convbkmk/

%files -n %{shortname}-crossrefware
%license gpl.txt
%{_bindir}/bbl2bib
%{_bindir}/bibdoiadd
%{_bindir}/bibmradd
%{_bindir}/biburl2doi
%{_bindir}/bibzbladd
%{_bindir}/ltx2crossrefxml
%{_mandir}/man1/bbl2bib.1*
%{_mandir}/man1/bibdoiadd.1*
%{_mandir}/man1/bibmradd.1*
%{_mandir}/man1/biburl2doi.1*
%{_mandir}/man1/bibzbladd.1*
%{_mandir}/man1/ltx2crossrefxml.1*
%{_texmf_main}/scripts/crossrefware/
%{_texmf_main}/tex/latex/crossrefware/
%doc %{_texmf_main}/doc/support/crossrefware/

%files -n %{shortname}-cslatex
%license gpl.txt
# %%{_bindir}/cslatex
# %%{_bindir}/pdfcslatex
%{_texmf_main}/tex/cslatex/
%{fmtutil_cnf_d}/cslatex

%files -n %{shortname}-csplain
%license other-free.txt
%{_bindir}/csplain
%{_bindir}/pdfcsplain
%{_texmf_main}/tex/csplain/
%{fmtutil_cnf_d}/csplain

%files -n %{shortname}-ctan-o-mat
%license bsd.txt
%{_bindir}/ctan-o-mat
%{_mandir}/man1/ctan-o-mat.1*
%{_texmf_main}/scripts/ctan-o-mat/
%doc %{_texmf_main}/doc/support/ctan-o-mat/

%files -n %{shortname}-ctanbib
%license lppl1.3.txt
%{_bindir}/ctanbib
%{_mandir}/man1/ctanbib.1*
%{_texmf_main}/scripts/ctanbib/
%doc %{_texmf_main}/doc/support/ctanbib/

%files -n %{shortname}-ctanify
%license lppl1.3.txt
%{_bindir}/ctanify
%{_mandir}/man1/ctanify.1*
%{_texmf_main}/scripts/ctanify/
%doc %{_texmf_main}/doc/latex/ctanify/

%files -n %{shortname}-ctanupload
%license gpl3.txt
%{_bindir}/ctanupload
%{_texmf_main}/scripts/ctanupload/
%doc %{_texmf_main}/doc/support/ctanupload/

%files -n %{shortname}-ctie
%license gpl2.txt
%{_bindir}/ctie
%{_mandir}/man1/ctie.1*

%files -n %{shortname}-cweb
%license knuth.txt
%{_bindir}/ctangle
%{_bindir}/ctwill
%{_bindir}/ctwill-proofsort
%{_bindir}/ctwill-refsort
%{_bindir}/ctwill-twinx
%{_bindir}/cweave
%{_bindir}/twill
%{_bindir}/twill-refsort
%{_mandir}/man1/ctangle.1*
%{_mandir}/man1/ctwill-proofsort.1*
%{_mandir}/man1/ctwill-refsort.1*
%{_mandir}/man1/ctwill-twinx.1*
%{_mandir}/man1/ctwill.1*
%{_mandir}/man1/cweave.1*
%{_mandir}/man1/cweb.1*
%{_mandir}/man1/twill-refsort.1*
%{_mandir}/man1/twill.1*
%{_texmf_main}/tex/plain/cweb/

%files -n %{shortname}-cyrillic
%license lppl1.3.txt
%{_bindir}/rubibtex
%{_bindir}/rumakeindex
%{_mandir}/man1/rubibtex.1*
%{_mandir}/man1/rumakeindex.1*
%{_texmf_main}/tex/latex/cyrillic/
%{_texmf_main}/scripts/texlive-extra/rubibtex.sh
%{_texmf_main}/scripts/texlive-extra/rumakeindex.sh
%doc %{_texmf_main}/doc/latex/cyrillic/

%files -n %{shortname}-de-macro
%{_bindir}/de-macro
%{_texmf_main}/scripts/de-macro/
%doc %{_texmf_main}/doc/support/de-macro/

%files -n %{shortname}-detex
%{_bindir}/detex
%{_mandir}/man1/detex.1*

%files -n %{shortname}-diadia
%license lppl1.txt
%{_bindir}/diadia
%{_texmf_main}/scripts/diadia/
%{_texmf_main}/tex/latex/diadia/
%doc %{_texmf_main}/doc/latex/diadia/

%files -n %{shortname}-digestif
%license gpl3.txt lppl1.3.txt fdl.txt
%{_bindir}/digestif
%{_texmf_main}/scripts/digestif
%doc %{_texmf_main}/doc/support/digestif

%files -n %{shortname}-dosepsbin
%{_bindir}/dosepsbin
%{_mandir}/man1/dosepsbin.1*
%{_texmf_main}/scripts/dosepsbin/
%doc %{_texmf_main}/doc/support/dosepsbin/

%files -n %{shortname}-dtl
%license pd.txt
%{_bindir}/dt2dv
%{_bindir}/dv2dt
%{_mandir}/man1/dt2dv.1*
%{_mandir}/man1/dv2dt.1*

%files -n %{shortname}-dtxgen
%license gpl2.txt
%doc %{_texmf_main}/doc/support/dtxgen/
%{_bindir}/dtxgen
%{_texmf_main}/scripts/dtxgen/

%files -n %{shortname}-dvi2tty
%license gpl.txt
%{_bindir}/disdvi
%{_bindir}/dvi2tty
%{_mandir}/man1/disdvi.1*
%{_mandir}/man1/dvi2tty.1*

%files -n %{shortname}-dviasm
%license gpl3.txt
%{_bindir}/dviasm
%{_mandir}/man1/dviasm.1*
%{_texmf_main}/scripts/dviasm/
%doc %{_texmf_main}/doc/latex/dviasm/

%files -n %{shortname}-dvicopy
%license gpl2.txt
%{_bindir}/dvicopy
%{_mandir}/man1/dvicopy.1*

%files -n %{shortname}-dvidvi
%license other-free.txt
%{_bindir}/dvidvi
%{_mandir}/man1/dvidvi.1*

%files -n %{shortname}-dviinfox
%{_bindir}/dviinfox
%{_texmf_main}/scripts/dviinfox/
%doc %{_texmf_main}/doc/latex/dviinfox/

%files -n %{shortname}-dviljk
%license gpl.txt
%{_bindir}/dvihp
%{_bindir}/dvilj
%{_bindir}/dvilj2p
%{_bindir}/dvilj4
%{_bindir}/dvilj4l
%{_bindir}/dvilj6
%{_mandir}/man1/dvihp.1*
%{_mandir}/man1/dvilj.1*
%{_mandir}/man1/dvilj2p.1*
%{_mandir}/man1/dvilj4.1*
%{_mandir}/man1/dvilj4l.1*
%{_mandir}/man1/dvilj6.1*

%files -n %{shortname}-dviout-util
%{_bindir}/chkdvifont
%{_bindir}/dvispc
%{_mandir}/man1/chkdvifont.1*
%{_mandir}/man1/dvispc.1*

%files -n %{shortname}-dvipdfmx
%license gpl2.txt
%doc %{_texmf_main}/doc/dvipdfm/
%doc %{_texmf_main}/doc/dvipdfmx/
%exclude %{_texmf_main}/fonts/map/dvipdfmx/ptex-fontmaps/
%{_bindir}/dvipdfm
%{_bindir}/dvipdfmx
%{_bindir}/dvipdft
%{_bindir}/ebb
%{_mandir}/man1/dvipdfm.1*
%{_mandir}/man1/dvipdfmx.1*
%{_mandir}/man1/dvipdft.1*
%{_mandir}/man1/ebb.1*
%{_mandir}/man1/xdvipdfmx.1*
%{_texdir}/tlpkg/tlpostcode/dvipdfmx.pl
%{_texmf_main}/dvipdfmx/
%{_texmf_main}/fonts/cmap/
%{_texmf_main}/fonts/map/dvipdfmx/

%files -n %{shortname}-dvipng
%license lgpl.txt
%doc %{_texmf_main}/doc/dvipng/
%{_bindir}/dvigif
%{_bindir}/dvipng
%{_infodir}/dvipng.info*
%{_mandir}/man1/dvigif.1*
%{_mandir}/man1/dvipng.1*

%files -n %{shortname}-dvipos
%license lppl1.txt
%{_bindir}/dvipos
%{_mandir}/man1/dvipos.1*

%files -n %{shortname}-dvips
%license other-free.txt
%config(noreplace) %{_sysconfdir}/texlive/dvips/config/config.ps
%dir %{_texmf_main}/fonts/map/dvips/
%doc %{_texmf_main}/doc/dvips/
%{_bindir}/afm2tfm
%{_bindir}/dvips
%{_infodir}/dvips.info*
%{_mandir}/man1/afm2tfm.1*
%{_mandir}/man1/dvips.1*
%{_texmf_main}/dvips/base/
%{_texmf_main}/dvips/config/
%{_texmf_main}/fonts/enc/dvips/base/
%{_texmf_main}/tex/generic/dvips/

%files -n %{shortname}-dvisvgm
%license gpl3.txt
%{_bindir}/dvisvgm
%{_mandir}/man1/dvisvgm.1*

%files -n %{shortname}-easydtx
%license gpl3.txt
%{_bindir}/edtx2dtx
%{_mandir}/man1/edtx2dtx.1*
%{_texmf_main}/scripts/easydtx/
%doc %{_texmf_main}/doc/support/easydtx/

%files -n %{shortname}-ebong
%license pd.txt
%doc %{_texmf_main}/doc/latex/ebong/
%{_bindir}/ebong
%{_texmf_main}/scripts/ebong/

%files -n %{shortname}-eolang
%license mit.txt
%doc %{_texmf_main}/doc/latex/eolang/
%{_bindir}/eolang
%{_mandir}/man1/eolang.1*
%{_texmf_main}/scripts/eolang/
%{_texmf_main}/tex/latex/eolang/

%files -n %{shortname}-eplain
%license gpl2.txt
%{_bindir}/eplain
%{_mandir}/man1/eplain.1*
%{_infodir}/eplain.info*
%{_texmf_main}/tex/eplain/
%{fmtutil_cnf_d}/eplain
%doc %{_texmf_main}/doc/eplain/

%files -n %{shortname}-epspdf
%license gpl.txt
%{_bindir}/epspdf
%{_bindir}/epspdftk
%{_infodir}/epspdf.info*
%{_texmf_main}/scripts/epspdf/
%doc %{_texmf_main}/doc/support/epspdf/

%files -n %{shortname}-epstopdf
%{_bindir}/epstopdf
%{_bindir}/repstopdf
%{_mandir}/man1/epstopdf.1*
%{_mandir}/man1/repstopdf.1*
%{_texmf_main}/scripts/epstopdf/
%doc %{_texmf_main}/doc/support/epstopdf/

%files -n %{shortname}-exceltex
%license gpl2.txt
%doc %{_texmf_main}/doc/latex/exceltex/
%{_bindir}/exceltex
%{_texmf_main}/scripts/exceltex/
%{_texmf_main}/tex/latex/exceltex/

%files -n %{shortname}-expltools
%license lppl1.3c.txt
%license gpl2.txt
%doc %{_texmf_main}/doc/support/expltools/
%{_bindir}/explcheck
%{_texmf_main}/scripts/expltools/

%files -n %{shortname}-extractbb
%license other-free.txt
%license cc-by-sa-4.txt
%doc %{_texmf_main}/doc/support/extractbb/
%{_bindir}/extractbb
%{_mandir}/man1/extractbb.1*
%{_texmf_main}/scripts/extractbb/

%files -n %{shortname}-fig4latex
%license gpl3.txt
%{_bindir}/fig4latex
%{_texmf_main}/scripts/fig4latex/
%doc %{_texmf_main}/doc/support/fig4latex/

%files -n %{shortname}-findhyph
%license gpl.txt
%{_bindir}/findhyph
%{_mandir}/man1/findhyph.1*
%{_texmf_main}/scripts/findhyph/
%doc %{_texmf_main}/doc/support/findhyph/

%files -n %{shortname}-fontinst
%license lppl1.txt
%{_bindir}/fontinst
%{_mandir}/man1/fontinst.1*
%{_texmf_main}/scripts/texlive-extra/fontinst.sh
%{_texmf_main}/tex/fontinst/
%{_texmf_main}/tex/latex/fontinst/
%doc %{_texmf_main}/doc/fonts/fontinst/

%files -n %{shortname}-fontools
%license gpl2.txt
%doc %{_texmf_main}/doc/support/fontools/
%{_bindir}/afm2afm
%{_bindir}/autoinst
%{_bindir}/ot2kpx
%{_mandir}/man1/afm2afm.1*
%{_mandir}/man1/autoinst.1*
%{_mandir}/man1/ot2kpx.1*
%{_texmf_main}/fonts/enc/dvips/fontools/
%{_texmf_main}/scripts/fontools/

%files -n %{shortname}-fontware
%license knuth.txt
%{_bindir}/pltotf
%{_bindir}/tftopl
%{_bindir}/vftovp
%{_bindir}/vptovf
%{_mandir}/man1/pltotf.1*
%{_mandir}/man1/tftopl.1*
%{_mandir}/man1/vftovp.1*
%{_mandir}/man1/vptovf.1*

%files -n %{shortname}-fragmaster
%license gpl.txt
%{_bindir}/fragmaster
%{_texmf_main}/scripts/fragmaster/
%doc %{_texmf_main}/doc/support/fragmaster/

%files -n %{shortname}-getmap
%license lppl1.txt
%{_bindir}/getmapdl
%{_texmf_main}/scripts/getmap/
%{_texmf_main}/tex/latex/getmap/
%doc %{_texmf_main}/doc/latex/getmap/

%files -n %{shortname}-git-latexdiff
%{_bindir}/git-latexdiff
%{_mandir}/man1/git-latexdiff.*
%doc %{_texmf_main}/doc/support/git-latexdiff
%{_texmf_main}/scripts/git-latexdiff

%files -n %{shortname}-glossaries
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/glossaries/
%{_bindir}/makeglossaries
%{_bindir}/makeglossaries-lite
%{_mandir}/man1/makeglossaries-lite.1*
%{_mandir}/man1/makeglossaries.1*
%{_texmf_main}/scripts/glossaries/
%{_texmf_main}/tex/latex/glossaries/

%files -n %{shortname}-glyphlist
%{_texmf_main}/fonts/map/glyphlist/

%files -n %{shortname}-gregoriotex
%license gpl3.txt
%{_bindir}/gregorio
%{_texmf_main}/scripts/gregoriotex/
%{_texmf_main}/tex/lualatex/gregoriotex/
%{_texmf_main}/tex/luatex/gregoriotex/
%{_texmf_main}/fonts/source/gregoriotex/
%{_texmf_main}/fonts/truetype/public/gregoriotex/
%doc %{_texmf_main}/doc/luatex/gregoriotex/

%files -n %{shortname}-gsftopk
%license gpl.txt
%{_bindir}/gsftopk
%{_mandir}/man1/gsftopk.1*
%{_texmf_main}/dvips/gsftopk/

%files -n %{shortname}-hitex
%doc %{_texmf_main}/doc/hitex/
%{_bindir}/hilatex
%{_bindir}/hishrink
%{_bindir}/histretch
%{_bindir}/hitex
%{_bindir}/texprof
%{_bindir}/texprofile
%{_mandir}/man1/hishrink.1*
%{_mandir}/man1/histretch.1*
%{_mandir}/man1/hitex.1*
%{_mandir}/man1/texprof.1*
%{_mandir}/man1/texprofile.1*
%{_texdir}/fmtutil.cnf.d/hitex
%{_texmf_main}/makeindex/hitex/
%{_texmf_main}/tex/hitex/

%files -n %{shortname}-hyperxmp
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/hyperxmp
%{_bindir}/hyperxmp-add-bytecount
%{_mandir}/man1/hyperxmp*
%{_texmf_main}/scripts/hyperxmp/
%{_texmf_main}/tex/latex/hyperxmp

%files -n %{shortname}-installfont
%license lppl1.txt
%{_bindir}/installfont-tl
%{_texmf_main}/scripts/installfont/
%doc %{_texmf_main}/doc/support/installfont/

%files -n %{shortname}-jadetex
%{_bindir}/jadetex
%{_bindir}/pdfjadetex
%{_mandir}/man1/jadetex.1*
%{_mandir}/man1/pdfjadetex.1*
%{_texmf_main}/tex/jadetex/
%{fmtutil_cnf_d}/jadetex
%doc %{_texmf_main}/doc/otherformats/jadetex/

%files -n %{shortname}-jfmutil
%{_bindir}/jfmutil
%{_texmf_main}/scripts/jfmutil/
%doc %{_texmf_main}/doc/fonts/jfmutil/

%files -n %{shortname}-ketcindy
%license gpl3.txt
%{_bindir}/ketcindy
%{_texmf_main}/scripts/ketcindy/
%{_texmf_main}/tex/latex/ketcindy/
%doc %{_texmf_main}/doc/support/ketcindy/

%files -n %{shortname}-kotex-utils
%license lppl1.txt
%{_bindir}/jamo-normalize
%{_bindir}/komkindex
%{_bindir}/ttf2kotexfont
%{_texmf_main}/makeindex/kotex-utils/
%{_texmf_main}/scripts/kotex-utils/
%doc %{_texmf_main}/doc/latex/kotex-utils/

%files -n %{shortname}-kpathsea
%license lgpl2.1.txt
%config(noreplace) %{_sysconfdir}/texlive/web2c/fmtutil.cnf
%config(noreplace) %{_sysconfdir}/texlive/web2c/mktex.cnf
%config(noreplace) %{_sysconfdir}/texlive/web2c/texmf.cnf
%dir %{fmtutil_cnf_d}
%doc %{_texmf_main}/doc/kpathsea/
%doc %{_texmf_main}/doc/web2c/
%ghost %{_texmf_main}/web2c/fmtutil.cnf
%{_bindir}/kpseaccess
%{_bindir}/kpsereadlink
%{_bindir}/kpsestat
%{_bindir}/kpsewhich
%{_bindir}/mkocp
%{_bindir}/mkofm
%{_bindir}/mktexfmt
%{_bindir}/texhash
%{_infodir}/kpathsea.info*
%{_infodir}/web2c.info*
%{_mandir}/man1/kpseaccess.1*
%{_mandir}/man1/kpsereadlink.1*
%{_mandir}/man1/kpsestat.1*
%{_mandir}/man1/kpsewhich.1*
%{_mandir}/man1/mkocp.1*
%{_mandir}/man1/mkofm.1*
%{_mandir}/man1/mktexfmt.1*
%{_mandir}/man1/texhash.1*
%{_mandir}/man5/fmtutil.cnf.5*
%{_sbindir}/generate-fmtutilcnf
%{_texmf_main}/web2c/amiga-pl.tcx
%{_texmf_main}/web2c/cp1250cs.tcx
%{_texmf_main}/web2c/cp1250pl.tcx
%{_texmf_main}/web2c/cp1250t1.tcx
%{_texmf_main}/web2c/cp227.tcx
%{_texmf_main}/web2c/cp852-cs.tcx
%{_texmf_main}/web2c/cp852-pl.tcx
%{_texmf_main}/web2c/cp8bit.tcx
%{_texmf_main}/web2c/empty.tcx
%{_texmf_main}/web2c/il1-t1.tcx
%{_texmf_main}/web2c/il2-cs.tcx
%{_texmf_main}/web2c/il2-pl.tcx
%{_texmf_main}/web2c/il2-t1.tcx
%{_texmf_main}/web2c/kam-cs.tcx
%{_texmf_main}/web2c/kam-t1.tcx
%{_texmf_main}/web2c/macce-pl.tcx
%{_texmf_main}/web2c/macce-t1.tcx
%{_texmf_main}/web2c/maz-pl.tcx
%{_texmf_main}/web2c/mktex.cnf
%{_texmf_main}/web2c/mktex.opt
%{_texmf_main}/web2c/mktexdir
%{_texmf_main}/web2c/mktexdir.opt
%{_texmf_main}/web2c/mktexnam
%{_texmf_main}/web2c/mktexnam.opt
%{_texmf_main}/web2c/mktexupd
%{_texmf_main}/web2c/natural.tcx
%{_texmf_main}/web2c/tcvn-t5.tcx
%{_texmf_main}/web2c/texmf.cnf
%{_texmf_main}/web2c/viscii-t5.tcx

%files -n %{shortname}-l3build
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/l3build/
%{_bindir}/l3build
%{_mandir}/man1/l3build.1*
%{_texmf_main}/scripts/l3build/
%{_texmf_main}/tex/latex/l3build/

%files -n %{shortname}-l3sys-query
%license mit.txt
%doc %{_texmf_main}/doc/support/l3sys-query/
%{_bindir}/l3sys-query
%{_mandir}/man1/l3sys-query.1*
%{_texmf_main}/scripts/l3sys-query/

%files -n %{shortname}-lacheck
%license gpl2.txt
%{_bindir}/lacheck
%{_mandir}/man1/lacheck.1*

%files -n %{shortname}-latex
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/base/
%{_bindir}/dvilualatex
%{_bindir}/latex
%{_bindir}/pdflatex
%{_mandir}/man1/latex.1*
%{_mandir}/man1/pdflatex.1*
%{_texmf_main}/makeindex/latex/
%{_texmf_main}/tex/latex/base/
%{fmtutil_cnf_d}/latex-bin

%files -n %{shortname}-latex-git-log
%license gpl3.txt
%{_bindir}/latex-git-log
%{_mandir}/man1/latex-git-log.1*
%{_texmf_main}/scripts/latex-git-log/
%doc %{_texmf_main}/doc/support/latex-git-log/

%files -n %{shortname}-latex-papersize
%license apache2.txt
%{_bindir}/latex-papersize
%{_texmf_main}/scripts/latex-papersize
%doc %{_texmf_main}/doc/support/latex-papersize/

%files -n %{shortname}-latex2man
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/support/latex2man/
%{_bindir}/latex2man
%{_infodir}/latex2man.info*
%{_mandir}/man1/latex2man.1*
%{_texmf_main}/scripts/latex2man/
%{_texmf_main}/tex/latex/latex2man/

%files -n %{shortname}-latex2nemeth
%license gpl3.txt
%doc %{_texmf_main}/doc/support/latex2nemeth
%{_bindir}/latex2nemeth
%{_texmf_main}/scripts/latex2nemeth/

%files -n %{shortname}-latexdiff
%license gpl3.txt
%doc %{_texmf_main}/doc/support/latexdiff/
%{_bindir}/latexdiff
%{_bindir}/latexdiff-vc
%{_bindir}/latexrevise
%{_mandir}/man1/latexdiff-vc.1*
%{_mandir}/man1/latexdiff.1*
%{_mandir}/man1/latexrevise.1*
%{_texmf_main}/scripts/latexdiff/

%files -n %{shortname}-latexfileversion
%license lppl1.txt
%{_bindir}/latexfileversion
%{_texmf_main}/scripts/latexfileversion/
%doc %{_texmf_main}/doc/support/latexfileversion/

%files -n %{shortname}-latexpand
%license bsd.txt
%{_bindir}/latexpand
%{_texmf_main}/scripts/latexpand/
%doc %{_texmf_main}/doc/support/latexpand/

%files -n %{shortname}-latexindent
%license gpl3.txt
%doc %{_texmf_main}/doc/support/latexindent/
%{_bindir}/latexindent
%{_texmf_main}/scripts/latexindent/

%files -n %{shortname}-lcdftypetools
%license gpl.txt
%{_bindir}/cfftot1
%{_bindir}/mmafm
%{_bindir}/mmpfb
%{_bindir}/otfinfo
%{_bindir}/otftotfm
%{_bindir}/t1dotlessj
%{_bindir}/t1lint
%{_bindir}/t1rawafm
%{_bindir}/t1reencode
%{_bindir}/t1testpage
%{_bindir}/ttftotype42
%{_mandir}/man1/cfftot1.1*
%{_mandir}/man1/mmafm.1*
%{_mandir}/man1/mmpfb.1*
%{_mandir}/man1/otfinfo.1*
%{_mandir}/man1/otftotfm.1*
%{_mandir}/man1/t1dotlessj.1*
%{_mandir}/man1/t1lint.1*
%{_mandir}/man1/t1rawafm.1*
%{_mandir}/man1/t1reencode.1*
%{_mandir}/man1/t1testpage.1*
%{_mandir}/man1/ttftotype42.1*

%files -n %{shortname}-lib
%{_libdir}/*.so.*
%dir %{_texdir}/texmf-config
%dir %{_texdir}/texmf-config/web2c
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %{_texdir}/texmf-config/ls-R
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %{_texmf_main}/ls-R
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %{_texdir}/texmf-local/ls-R

%files -n %{shortname}-lib-devel
%dir %{_includedir}/kpathsea
%{_includedir}/kpathsea/*
%{_includedir}/synctex/
%{_includedir}/texlua53/
%ifnarch %{power64} s390 s390x riscv64
%{_includedir}/texluajit/
%endif
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{shortname}-light-latex-make
%{_bindir}/llmk
%{_mandir}/man1/llmk*
%doc %{_texmf_main}/doc/support/light-latex-make
%{_texmf_main}/scripts/light-latex-make

%files -n %{shortname}-lilyglyphs
%license lppl1.3.txt
%{_bindir}/lily-glyph-commands
%{_bindir}/lily-image-commands
%{_bindir}/lily-rebuild-pdfs
%{_datadir}/fonts/lilyglyphs
%{_texmf_main}/fonts/opentype/public/lilyglyphs/
%{_texmf_main}/scripts/lilyglyphs/
%{_texmf_main}/tex/latex/lilyglyphs/
%doc %{_texmf_main}/doc/latex/lilyglyphs/

%files -n %{shortname}-listbib
%license gpl.txt
%{_bindir}/listbib
%{_texmf_main}/bibtex/bst/listbib/
%{_texmf_main}/scripts/listbib/
%{_texmf_main}/tex/latex/listbib/
%doc %{_texmf_main}/doc/latex/listbib/

%files -n %{shortname}-listings-ext
%license lppl1.2.txt
%{_bindir}/listings-ext.sh
%{_texmf_main}/scripts/listings-ext/
%{_texmf_main}/tex/latex/listings-ext/
%doc %{_texmf_main}/doc/latex/listings-ext/

%files -n %{shortname}-lollipop
%license gpl3.txt
%{_bindir}/lollipop
%{_texmf_main}/tex/lollipop/
%{fmtutil_cnf_d}/lollipop
%doc %{_texmf_main}/doc/otherformats/lollipop/

%files -n %{shortname}-ltxfileinfo
%license gpl.txt
%{_bindir}/ltxfileinfo
%{_texmf_main}/scripts/ltxfileinfo/
%doc %{_texmf_main}/doc/support/ltxfileinfo/

%files -n %{shortname}-ltximg
%license gpl2.txt
%{_bindir}/ltximg
%{_mandir}/man1/ltximg.1*
%{_texmf_main}/scripts/ltximg/
%doc %{_texmf_main}/doc/support/ltximg/

%files -n %{shortname}-luafindfont
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/support/luafindfont/
%{_bindir}/luafindfont
%{_mandir}/man1/luafindfont.1*
%{_texmf_main}/scripts/luafindfont/

%files -n %{shortname}-luaotfload
%license gpl2.txt
%{_bindir}/luaotfload-tool
%{_mandir}/man1/luaotfload-tool.1*
%{_mandir}/man5/luaotfload.conf.5*
%{_texmf_main}/scripts/luaotfload/
%{_texmf_main}/tex/luatex/luaotfload/
%doc %{_texmf_main}/doc/luatex/luaotfload/

%files -n %{shortname}-luahbtex
%{_bindir}/luahbtex
%{_bindir}/lualatex
%{_bindir}/lualatex-dev
%{_mandir}/man1/luahbtex.1*
%{_mandir}/man1/lualatex-dev.1*
%{fmtutil_cnf_d}/luahbtex

%files -n %{shortname}-luajittex
%{_mandir}/man1/luajithbtex.1*
%{_mandir}/man1/luajittex.1*
%{fmtutil_cnf_d}/luajittex
%ifnarch %{power64} s390 s390x riscv64
%{_bindir}/luajittex
%{_bindir}/luajithbtex
%{_bindir}/texluajit
%{_bindir}/texluajitc
%endif

%files -n %{shortname}-luatex
%license gpl2.txt
%doc %{_texmf_main}/doc/luatex/base/
%{_bindir}/dvilualatex-dev
%{_bindir}/dviluatex
%{_bindir}/luacsplain
%{_bindir}/luatex
%{_bindir}/texlua
%{_bindir}/texluac
%{_mandir}/man1/dvilualatex-dev.1*
%{_mandir}/man1/dviluatex.1*
%{_mandir}/man1/luatex.1*
%{_mandir}/man1/texlua.1*
%{_mandir}/man1/texluac.1*
%{_sysconfdir}/texlive/web2c/texmfcnf.lua
%{_texmf_main}/tex/generic/config/luatex-unicode-letters.tex
# %%{_texmf_main}/tex/generic/config/luatexiniconfig.tex
%{_texmf_main}/web2c/texmfcnf.lua
%{fmtutil_cnf_d}/luatex

%files -n %{shortname}-lwarp
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/lwarp
%{_bindir}/lwarpmk
%{_texmf_main}/scripts/lwarp/
%{_texmf_main}/tex/latex/lwarp

%files -n %{shortname}-lyluatex
%{_texmf_main}/scripts/lyluatex/
%{_texmf_main}/tex/luatex/lyluatex/
%doc %{_texmf_main}/doc/support/lyluatex/

%files -n %{shortname}-make4ht
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/support/make4ht/
%{_bindir}/make4ht
%{_texmf_main}/scripts/make4ht/

%files -n %{shortname}-makedtx
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/support/makedtx/
%{_bindir}/makedtx
%{_texmf_main}/scripts/makedtx/
%{_texmf_main}/tex/latex/makedtx/

%files -n %{shortname}-makeindex
%license other-free.txt
%doc %{_texmf_main}/doc/support/makeindex/
%exclude %{_texmf_main}/makeindex/latex/
%{_bindir}/makeindex
%{_bindir}/mkindex
%{_mandir}/man1/makeindex.1*
%{_mandir}/man1/mkindex.1*
%{_texmf_main}/makeindex/
%{_texmf_main}/tex/plain/makeindex/

%files -n %{shortname}-markdown
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/context/third/markdown/
%doc %{_texmf_main}/doc/generic/markdown/
%doc %{_texmf_main}/doc/latex/markdown/
%doc %{_texmf_main}/doc/optex/markdown/
%{_bindir}/markdown2tex
%{_mandir}/man1/markdown2tex.1*
%{_texmf_main}/scripts/markdown/
%{_texmf_main}/tex/context/third/markdown/
%{_texmf_main}/tex/generic/markdown/
%{_texmf_main}/tex/latex/markdown/
%{_texmf_main}/tex/luatex/markdown/

%files -n %{shortname}-match_parens
%license gpl2.txt
%doc %{_texmf_main}/doc/support/match_parens/
%{_bindir}/match_parens
%{_mandir}/man1/match_parens.1*
%{_texmf_main}/scripts/match_parens/

%files -n %{shortname}-mathspic
%license lppl1.txt
%{_bindir}/mathspic
%{_mandir}/man1/mathspic.1*
%{_texmf_main}/scripts/mathspic/
%{_texmf_main}/tex/latex/mathspic/
%doc %{_texmf_main}/doc/latex/mathspic/

%files -n %{shortname}-memoize
%license lppl1.3.txt
%{_bindir}/memoize-clean.pl
%{_bindir}/memoize-clean.py
%{_bindir}/memoize-extract.pl
%{_bindir}/memoize-extract.py
%{_mandir}/man1/memoize-clean.1*
%{_mandir}/man1/memoize-clean.pl.1*
%{_mandir}/man1/memoize-clean.py.1*
%{_mandir}/man1/memoize-extract.1*
%{_mandir}/man1/memoize-extract.pl.1*
%{_mandir}/man1/memoize-extract.py.1*
%{_texmf_main}/scripts/memoize/
%{_texmf_main}/tex/generic/memoize/
%{_texmf_main}/tex/latex/memoize/
%{_texmf_main}/tex/plain/memoize/
%doc %{_texmf_main}/doc/generic/memoize/

%files -n %{shortname}-metafont
%license knuth.txt
%{_bindir}/inimf
%{_bindir}/mf
%{_bindir}/mf-nowin
%{_mandir}/man1/inimf.1.*
%{_mandir}/man1/mf-nowin.1*
%{_mandir}/man1/mf.1*
%{_texmf_main}/metafont/
%{fmtutil_cnf_d}/metafont

%files -n %{shortname}-metapost
%license lgpl2.1.txt
%doc %{_texmf_main}/doc/metapost/
%exclude %{_texmf_main}/metapost/context/
%{_bindir}/dvitomp
%{_bindir}/mfplain
%{_bindir}/mpost
%{_bindir}/r-mpost
%{_mandir}/man1/dvitomp.1*
%{_mandir}/man1/mpost.1*
%{_texmf_main}/fonts/afm/metapost/
%{_texmf_main}/fonts/enc/dvips/metapost/
%{_texmf_main}/fonts/map/dvips/metapost/
%{_texmf_main}/fonts/tfm/metapost/
%{_texmf_main}/fonts/type1/metapost/
%{_texmf_main}/metapost/
%{_texmf_main}/tex/generic/metapost/

%files -n %{shortname}-mex
%license pd.txt
%{_bindir}/mex
%{_bindir}/pdfmex
%{_bindir}/utf8mex
%{_texmf_main}/tex/mex/
%{fmtutil_cnf_d}/mex
%doc %{_texmf_main}/doc/mex/

%files -n %{shortname}-mflua
%{_bindir}/mflua
%{_bindir}/mflua-nowin
%{_texmf_main}/metafont/mflua/
%{_texmf_main}/scripts/mflua/
%{fmtutil_cnf_d}/mflua
%ifnarch %{power64} s390 s390x riscv64
%{_bindir}/mfluajit
%{_bindir}/mfluajit-nowin
%endif

%files -n %{shortname}-mfware
%license pd.txt
%{_bindir}/gftodvi
%{_bindir}/gftopk
%{_bindir}/gftype
%{_bindir}/mft
%{_bindir}/pktogf
%{_bindir}/pktype
%{_mandir}/man1/gftodvi.1*
%{_mandir}/man1/gftopk.1*
%{_mandir}/man1/gftype.1*
%{_mandir}/man1/mft.1*
%{_mandir}/man1/pktogf.1*
%{_mandir}/man1/pktype.1*
%{_texmf_main}/mft/

%files -n %{shortname}-mf2pt1
%license lppl1.txt
%{_bindir}/mf2pt1
%{_infodir}/mf2pt1.info*
%{_texmf_main}/metapost/mf2pt1/
%{_texmf_main}/scripts/mf2pt1/
%doc %{_texmf_main}/doc/support/mf2pt1/

%files -n %{shortname}-minted
%license lppl1.3c.txt
%license bsd.txt
%doc %{_texmf_main}/doc/latex/minted/
%{_bindir}/latexminted
%{_mandir}/man1/latexminted.1*
%{_texmf_main}/scripts/minted/
%{_texmf_main}/tex/latex/minted/

%files -n %{shortname}-mkgrkindex
%{_bindir}/mkgrkindex
%{_texmf_main}/makeindex/mkgrkindex/
%{_texmf_main}/scripts/mkgrkindex/
%doc %{_texmf_main}/doc/support/mkgrkindex/

%files -n %{shortname}-mkjobtexmf
%{_bindir}/mkjobtexmf
%{_mandir}/man1/mkjobtexmf.1*
%{_texmf_main}/scripts/mkjobtexmf/
%doc %{_texmf_main}/doc/generic/mkjobtexmf/

%files -n %{shortname}-mkpic
%license gpl2.txt
%doc %{_texmf_main}/doc/support/mkpic/
%{_bindir}/mkpic
%{_texmf_main}/scripts/mkpic/

%files -n %{shortname}-mltex
%license knuth.txt
%{_bindir}/mllatex
%{_bindir}/mltex
%{_texmf_main}/tex/latex/mltex/
%{_texmf_main}/tex/mltex/
%{fmtutil_cnf_d}/mltex
%doc %{_texmf_main}/doc/latex/mltex/

%files -n %{shortname}-mptopdf
%license gpl2.txt
%doc %{_texmf_main}/doc/context/scripts/mkii/mptopdf.man
%{_bindir}/mptopdf
%{_mandir}/man1/mptopdf.1*
%{_texmf_main}/scripts/context/perl/mptopdf.pl
%{_texmf_main}/tex/context/base/mkii/supp-mis.mkii
%{_texmf_main}/tex/context/base/mkii/supp-mpe.mkii
%{_texmf_main}/tex/context/base/mkii/supp-pdf.mkii
%{_texmf_main}/tex/context/base/mkii/syst-tex.mkii
%{_texmf_main}/tex/generic/context/mptopdf/
%{fmtutil_cnf_d}/mptopdf

%files -n %{shortname}-multibibliography
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/multibibliography/
%{_bindir}/multibibliography
%{_texmf_main}/bibtex/bst/multibibliography/
%{_texmf_main}/scripts/multibibliography/
%{_texmf_main}/tex/latex/multibibliography/

%files -n %{shortname}-musixtex
%license gpl2.txt
%doc %{_texmf_main}/doc/generic/musixtex/
%{_bindir}/musixflx
%{_bindir}/musixtex
%{_mandir}/man1/musixflx.1*
%{_mandir}/man1/musixtex.1*
%{_texmf_main}/dvips/musixtex/
%{_texmf_main}/scripts/musixtex/
%{_texmf_main}/tex/generic/musixtex/
%{_texmf_main}/tex/latex/musixtex/

%files -n %{shortname}-musixtnt
%license gpl2.txt
%{_bindir}/msxlint
%{_mandir}/man1/msxlint.1*
%{_texmf_main}/tex/generic/musixtnt/
%doc %{_texmf_main}/doc/generic/musixtnt/

%files -n %{shortname}-m-tx
%license mit.txt
%doc %{_texmf_main}/doc/generic/m-tx/
%{_bindir}/prepmx
%{_mandir}/man1/prepmx.1*
%{_texmf_main}/tex/generic/m-tx/
%{_texmf_main}/tex/latex/m-tx/

%files -n %{shortname}-oberdiek
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/oberdiek/
%{_texmf_main}/bibtex/bib/oberdiek/
%{_texmf_main}/tex/generic/oberdiek/
%{_texmf_main}/tex/latex/oberdiek/

%files -n %{shortname}-omegaware
%license gpl2.txt
%{_bindir}/odvicopy
%{_bindir}/odvitype
%{_bindir}/ofm2opl
%{_bindir}/omfonts
%{_bindir}/opl2ofm
%{_bindir}/otangle
%{_bindir}/otp2ocp
%{_bindir}/outocp
%{_bindir}/ovf2ovp
%{_bindir}/ovp2ovf
%{_bindir}/wofm2opl
%{_bindir}/wopl2ofm
%{_bindir}/wovf2ovp
%{_mandir}/man1/odvicopy.1*
%{_mandir}/man1/odvitype.1*
%{_mandir}/man1/ofm2opl.1*
%{_mandir}/man1/opl2ofm.1*
%{_mandir}/man1/otangle.1*
%{_mandir}/man1/otp2ocp.1*
%{_mandir}/man1/outocp.1*
%{_mandir}/man1/ovf2ovp.1*
%{_mandir}/man1/ovp2ovf.1*

%files -n %{shortname}-optex
%license pd.txt
%doc %{_texmf_main}/doc/optex/
%{_bindir}/optex
%{_mandir}/man1/optex.1*
%{_texmf_main}/tex/optex/
%{fmtutil_cnf_d}/optex

%files -n %{shortname}-optexcount
%{_bindir}/optexcount
%{_texmf_main}/scripts/optexcount/
%doc %{_texmf_main}/doc/support/optexcount/

%files -n %{shortname}-pagelayout
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/pagelayout
%{_bindir}/pagelayoutapi
%{_bindir}/textestvis
%{_mandir}/man1/pagelayoutapi.1*
%{_mandir}/man1/textestvis.1*
%{_texmf_main}/scripts/pagelayout
%{_texmf_main}/tex/latex/pagelayout

%files -n %{shortname}-patgen
%license pd.txt
%{_bindir}/patgen
%{_mandir}/man1/patgen.1*

%files -n %{shortname}-pax
%{_bindir}/pdfannotextractor
%{_texmf_main}/scripts/pax/
%{_texmf_main}/tex/latex/pax/
%doc %{_texmf_main}/doc/latex/pax/

%files -n %{shortname}-pdfbook2
%license gpl3.txt
%doc %{_texmf_main}/doc/support/pdfbook2/
%{_bindir}/pdfbook2
%{_mandir}/man1/pdfbook2.1*
%{_texmf_main}/scripts/pdfbook2/

%files -n %{shortname}-pdfcrop
%license lppl1.txt
%{_bindir}/pdfcrop
%{_bindir}/rpdfcrop
%{_texmf_main}/scripts/pdfcrop/
%doc %{_texmf_main}/doc/support/pdfcrop/

%files -n %{shortname}-pdfjam
%license gpl2.txt
%{_bindir}/pdfjam
%{_mandir}/man1/pdfjam.1*
%{_texmf_main}/scripts/pdfjam/
%doc %{_texmf_main}/doc/support/pdfjam/

%files -n %{shortname}-pdflatexpicscale
%license lppl.txt
%{_bindir}/pdflatexpicscale
%{_texmf_main}/scripts/pdflatexpicscale
%doc %{_texmf_main}/doc/support/pdflatexpicscale

%files -n %{shortname}-pdftex
%license gpl2.txt
%doc %{_texmf_main}/doc/pdftex/
%{_bindir}/etex
%{_bindir}/latex-dev
%{_bindir}/pdfetex
%{_bindir}/pdflatex-dev
%{_bindir}/pdftex
%{_bindir}/simpdftex
%{_mandir}/man1/latex-dev.1*
%{_mandir}/man1/pdfetex.1*
%{_mandir}/man1/pdflatex-dev.1*
%{_mandir}/man1/pdftex.1*
%{_texmf_main}/fonts/map/dvips/dummy-space/dummy-space.map
%{_texmf_main}/fonts/tfm/public/pdftex/
%{_texmf_main}/fonts/type1/public/pdftex/
%{_texmf_main}/scripts/simpdftex/
%{_texmf_main}/tex/generic/config/pdftex-dvi.tex
%{_texmf_main}/tex/generic/pdftex/
%{fmtutil_cnf_d}/latex-bin-dev
%{fmtutil_cnf_d}/pdftex

%files -n %{shortname}-pdftex-quiet
%license gpl3.txt
%{_bindir}/pdftex-quiet
%{_texmf_main}/scripts/pdftex-quiet/
%doc %{_texmf_main}/doc/support/pdftex-quiet/

%files -n %{shortname}-pdftosrc
%{_bindir}/pdftosrc
%{_mandir}/man1/pdftosrc.1*

%files -n %{shortname}-pdfxup
%license lppl1.3.txt
%{_bindir}/pdfxup
%{_mandir}/man1/pdfxup.1*
%{_texmf_main}/tex/latex/pdfxup/
%{_texmf_main}/scripts/pdfxup/
%doc %{_texmf_main}/doc/support/pdfxup/

%files -n %{shortname}-pedigree-perl
%license gpl2.txt
%{_bindir}/pedigree
%{_mandir}/man1/pedigree.1*
%{_texmf_main}/scripts/pedigree-perl/
%doc %{_texmf_main}/doc/support/pedigree-perl/

%files -n %{shortname}-perltex
%license lppl1.txt
%{_bindir}/perltex
%{_mandir}/man1/perltex.1*
%{_texmf_main}/scripts/perltex/
%{_texmf_main}/tex/latex/perltex/
%doc %{_texmf_main}/doc/latex/perltex/

%files -n %{shortname}-petri-nets
%license gpl.txt
%{_bindir}/pn2pdf
%{_texmf_main}/scripts/petri-nets/
%{_texmf_main}/tex/generic/petri-nets/
%doc %{_texmf_main}/doc/generic/petri-nets/

%files -n %{shortname}-pfarrei
%license lppl1.3.txt
%{_bindir}/a5toa4
%{_bindir}/pfarrei
%{_texmf_main}/scripts/pfarrei/
%{_texmf_main}/tex/latex/pfarrei/
%doc %{_texmf_main}/doc/latex/pfarrei/

%files -n %{shortname}-pkfix
%license lppl1.3.txt
%{_bindir}/pkfix
%{_texmf_main}/scripts/pkfix/
%doc %{_texmf_main}/doc/support/pkfix/

%files -n %{shortname}-pkfix-helper
%license lppl1.txt
%{_bindir}/pkfix-helper
%{_mandir}/man1/pkfix-helper.1*
%{_texmf_main}/scripts/pkfix-helper/
%doc %{_texmf_main}/doc/support/pkfix-helper/

%files -n %{shortname}-pmx
%license gpl2.txt
%{_bindir}/pmxab
%{_bindir}/scor2prt
%{_mandir}/man1/pmxab.1*
%{_mandir}/man1/scor2prt.1*
%{_texmf_main}/tex/generic/pmx/
%doc %{_texmf_main}/doc/generic/pmx/

%files -n %{shortname}-pmxchords
%license gpl2.txt
%{_bindir}/pmxchords
%{_mandir}/man1/pmxchords.1*
%{_texmf_main}/scripts/pmxchords/
%{_texmf_main}/tex/generic/pmxchords/
%doc %{_texmf_main}/doc/support/pmxchords/

%files -n %{shortname}-ppmcheckpdf
%license lppl1.3.txt
%{_bindir}/ppmcheckpdf
%{_mandir}/man1/ppmcheckpdf.1*
%{_texmf_main}/scripts/ppmcheckpdf/
%doc %{_texmf_main}/doc/support/ppmcheckpdf/

%files -n %{shortname}-pst2pdf
%license gpl2.txt
%{_bindir}/pst2pdf
%{_texmf_main}/scripts/pst2pdf/
%doc %{_texmf_main}/doc/support/pst2pdf/

%files -n %{shortname}-pst-pdf
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/pst-pdf/
%{_bindir}/ps4pdf
%{_texmf_main}/scripts/pst-pdf/
%{_texmf_main}/tex/latex/pst-pdf/

%files -n %{shortname}-psutils
%{_bindir}/tl-epsffit
%{_bindir}/tl-extractres
%{_bindir}/tl-includeres
%{_bindir}/tl-psbook
%{_bindir}/tl-psjoin
%{_bindir}/tl-psnup
%{_bindir}/tl-psresize
%{_bindir}/tl-psselect
%{_bindir}/tl-pstops
%{_mandir}/man1/tl-epsffit.1*
%{_mandir}/man1/tl-extractres.1*
%{_mandir}/man1/tl-includeres.1*
%{_mandir}/man1/tl-psbook.1*
%{_mandir}/man1/tl-psjoin.1*
%{_mandir}/man1/tl-psnup.1*
%{_mandir}/man1/tl-psresize.1*
%{_mandir}/man1/tl-psselect.1*
%{_mandir}/man1/tl-pstops.1*
%{_mandir}/man1/tl-psutils.1*
%{_texmf_main}/dvips/getafm/
%{_texmf_main}/psutils/
%dir %{_sysconfdir}/texlive/psutils
%config(noreplace) %{_sysconfdir}/texlive/psutils/paper.cfg
%{_texmf_main}/scripts/psutils

%files -n %{shortname}-ps2eps
%license gpl2.txt
%{_bindir}/bbox
%{_bindir}/ps2eps
%{_mandir}/man1/bbox.1*
%{_mandir}/man1/ps2eps.1*
%{_texmf_main}/scripts/ps2eps/

%files -n %{shortname}-ps2pk
%license other-free.txt
%{_bindir}/mag
%{_bindir}/pfb2pfa
%{_bindir}/pk2bm
%{_bindir}/ps2pk
%{_mandir}/man1/mag.1*
%{_mandir}/man1/pfb2pfa.1*
%{_mandir}/man1/pk2bm.1*
%{_mandir}/man1/ps2pk.1*

%files -n %{shortname}-ptex
%license bsd.txt
%{_bindir}/eptex
%{_bindir}/makejvf
%{_bindir}/mendex
%{_bindir}/pbibtex
%{_bindir}/pdvitomp
%{_bindir}/pdvitype
%{_bindir}/platex
%{_bindir}/platex-dev
%{_bindir}/pmpost
%{_bindir}/ppltotf
%{_bindir}/ptekf
%{_bindir}/ptex
%{_bindir}/ptftopl
%{_bindir}/r-pmpost
%{_mandir}/man1/eptex.1*
%{_mandir}/man1/makejvf.1*
%{_mandir}/man1/mendex.1*
%{_mandir}/man1/pbibtex.1*
%{_mandir}/man1/platex-dev.1*
%{_mandir}/man1/ppltotf.1*
%{_mandir}/man1/ptekf.1*
%{_mandir}/man1/ptex.1*
%{_mandir}/man1/ptftopl.1*
%{fmtutil_cnf_d}/platex
%{fmtutil_cnf_d}/ptex

%files -n %{shortname}-ptex-fontmaps
%license gpl3.txt
%license pd.txt
%{_bindir}/kanji-config-updmap
%{_bindir}/kanji-config-updmap-sys
%{_bindir}/kanji-config-updmap-user
%{_bindir}/kanji-fontmap-creator
%{_texmf_main}/fonts/cmap/ptex-fontmaps
%{_texmf_main}/fonts/map/dvipdfmx/ptex-fontmaps
%{_texmf_main}/fonts/misc/ptex-fontmaps/
%{_texmf_main}/scripts/ptex-fontmaps
%{_texdir}/tlpkg/tlpostcode/ptex-fontmaps-tlpost.pl
%doc %{_texmf_main}/doc/fonts/ptex-fontmaps

%files -n %{shortname}-ptex2pdf
%license gpl2.txt
%{_bindir}/ptex2pdf
%{_texmf_main}/scripts/ptex2pdf/
%{_texdir}/tlpkg/tlpostcode/ptex2pdf-tlpost.pl
%doc %{_texmf_main}/doc/latex/ptex2pdf/

%files -n %{shortname}-purifyeps
%license lppl1.txt
%{_bindir}/purifyeps
%{_mandir}/man1/purifyeps.1*
%{_texmf_main}/scripts/purifyeps/
%doc %{_texmf_main}/doc/support/purifyeps/

%files -n %{shortname}-pygmentex
%license lppl1.3.txt
%{_bindir}/pygmentex
%{_texmf_main}/scripts/pygmentex/
%{_texmf_main}/tex/latex/pygmentex/
%doc %{_texmf_main}/doc/latex/pygmentex/

%files -n %{shortname}-pythontex
%license lppl1.3c.txt
%license bsd.txt
%doc %{_texmf_main}/doc/latex/pythontex/
%{_bindir}/depythontex
%{_bindir}/pythontex
%{_texmf_main}/scripts/pythontex/
%{_texmf_main}/tex/latex/pythontex/

%files -n %{shortname}-rubik
%license lppl1.3.txt
%{_bindir}/rubikrotation
%{_mandir}/man1/rubikrotation.1*
%{_texmf_main}/scripts/rubik/
%{_texmf_main}/tex/latex/rubik/
%doc %{_texmf_main}/doc/latex/rubik/

%files -n %{shortname}-runtexfile
%license lppl1.3c.txt
%{_bindir}/runtexfile
%{_texmf_main}/scripts/runtexfile/
%{_mandir}/man1/runtexfile.1*
%doc %{_texmf_main}/doc/support/runtexfile/

%files -n %{shortname}-runtexshebang
%license mit.txt
%{_bindir}/runtexshebang
%{_texmf_main}/scripts/runtexshebang/
%doc %{_texmf_main}/doc/support/runtexshebang/

%files -n %{shortname}-seetexk
%{_bindir}/dvibook
%{_bindir}/dviconcat
%{_bindir}/dviselect
%{_bindir}/dvitodvi
%{_mandir}/man1/dvibook.1*
%{_mandir}/man1/dviconcat.1*
%{_mandir}/man1/dviselect.1*
%{_mandir}/man1/dvitodvi.1*

%files -n %{shortname}-show-pdf-tags
%license mit.txt
%{_bindir}/show-pdf-tags
%{_texmf_main}/scripts/show-pdf-tags/
%{_texmf_main}/tex/latex/show-pdf-tags/
%{_mandir}/man1/show-pdf-tags.1*
%doc %{_texmf_main}/doc/support/show-pdf-tags/

%files -n %{shortname}-spix
%license gpl3.txt
%{_bindir}/spix
%{_mandir}/man1/spix*
%doc %{_texmf_main}/doc/support/spix
%{_texmf_main}/scripts/spix

%files -n %{shortname}-splitindex
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/splitindex/
%{_bindir}/splitindex
%{_mandir}/man1/splitindex.1*
%{_texmf_main}/scripts/splitindex/
%{_texmf_main}/tex/generic/splitindex/
%{_texmf_main}/tex/latex/splitindex/

%files -n %{shortname}-sqltex
%license lppl1.3.txt
%{_bindir}/sqltex
%{_texmf_main}/scripts/sqltex/
%doc %{_texmf_main}/doc/support/sqltex/

%files -n %{shortname}-srcredact
%license gpl2.txt
%{_bindir}/srcredact
%{_mandir}/man1/srcredact.1*
%{_texmf_main}/scripts/srcredact/
%doc %{_texmf_main}/doc/support/srcredact/

%files -n %{shortname}-sty2dtx
%license gpl3.txt
%doc %{_texmf_main}/doc/support/sty2dtx/
%{_bindir}/sty2dtx
%{_mandir}/man1/sty2dtx.1*
%{_texmf_main}/scripts/sty2dtx/

%files -n %{shortname}-svn-multi
%license lppl1.txt
%{_bindir}/svn-multi
%{_texmf_main}/scripts/svn-multi/
%{_texmf_main}/tex/latex/svn-multi/
%doc %{_texmf_main}/doc/latex/svn-multi/
%doc %{_texmf_main}/doc/support/svn-multi/

%files -n %{shortname}-synctex
%license lppl1.txt
%{_bindir}/synctex
%{_mandir}/man1/synctex.1*
%{_mandir}/man5/synctex.5*

%files -n %{shortname}-tex
%license knuth.txt
%{_bindir}/initex
%{_bindir}/tex
%{_mandir}/man1/initex.1*
%{_mandir}/man1/tex.1*
%{fmtutil_cnf_d}/tex

%files -n %{shortname}-tex4ebook
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/support/tex4ebook/
%{_bindir}/tex4ebook
%{_texmf_main}/scripts/tex4ebook/
%{_texmf_main}/tex/latex/tex4ebook/

%files -n %{shortname}-tex4ht
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/generic/tex4ht/
%{_bindir}/ht
# %%{_bindir}/htcontext
%{_bindir}/htlatex
%{_bindir}/htmex
%{_bindir}/httex
%{_bindir}/httexi
%{_bindir}/htxelatex
%{_bindir}/htxetex
%{_bindir}/mk4ht
%{_bindir}/t4ht
%{_bindir}/tex4ht
%{_bindir}/xhlatex
%{_texmf_main}/scripts/tex4ht/
%{_texmf_main}/tex/generic/tex4ht/
%{_texmf_main}/tex4ht/

%files -n %{shortname}-texaccents
%license mit.txt
%{_bindir}/texaccents
%{_mandir}/man1/texaccents.1*
%doc %{_texmf_main}/doc/support/texaccents
%{_texmf_main}/scripts/texaccents

%files -n %{shortname}-texblend
%license lppl1.3.txt
%{_bindir}/texblend
%{_texmf_main}/scripts/texblend/
%doc %{_texmf_main}/doc/support/texblend/

%files -n %{shortname}-texcount
%license lppl1.txt
%{_bindir}/texcount
%{_texmf_main}/scripts/texcount/
%doc %{_texmf_main}/doc/support/texcount/

%files -n %{shortname}-texdef
%license gpl3.txt
%{_bindir}/latexdef
%{_bindir}/texdef
%{_texmf_main}/scripts/texdef/
%doc %{_texmf_main}/doc/support/texdef/

%files -n %{shortname}-texdiff
%license gpl.txt
%{_bindir}/texdiff
%{_texmf_main}/scripts/texdiff
%{_mandir}/man1/texdiff.1*
%doc %{_texmf_main}/doc/support/texdiff/

%files -n %{shortname}-texdirflatten
%{_bindir}/texdirflatten
%{_mandir}/man1/texdirflatten.1*
%{_texmf_main}/scripts/texdirflatten/
%doc %{_texmf_main}/doc/support/texdirflatten/

%files -n %{shortname}-texdoc
%license gpl.txt
%{_bindir}/texdoc
%{_mandir}/man1/texdoc.1*
%{_texmf_main}/scripts/texdoc/
%{_texmf_main}/texdoc/
%doc %{_texmf_main}/doc/support/texdoc/

%files -n %{shortname}-texdoctk
%license gpl.txt
%{_bindir}/texdoctk
%{_mandir}/man1/texdoctk.1*
%{_texmf_main}/scripts/texdoctk/
%{_texmf_main}/texdoctk/

%files -n %{shortname}-texfot
%license pd.txt
%doc %{_texmf_main}/doc/support/texfot/
%{_bindir}/texfot
%{_mandir}/man1/texfot.1*
%{_texmf_main}/scripts/texfot/

%files -n %{shortname}-texfindpkg
%license gpl3.txt
%{_bindir}/texfindpkg
%{_mandir}/man1/texfindpkg.1*
%{_texmf_main}/scripts/texfindpkg/
%{_texmf_main}/tex/latex/texfindpkg/
%doc %{_texmf_main}/doc/support/texfindpkg/

%files -n %{shortname}-texliveonfly
%license gpl3.txt
%doc %{_texmf_main}/doc/support/texliveonfly/
%{_bindir}/texliveonfly
%{_texmf_main}/scripts/texliveonfly/

%files -n %{shortname}-texlive-en
%doc %{_texmf_main}/doc/texlive/texlive-en/
%doc %{_texmf_main}/doc/texlive/tlbuild/tlbuild.html
%doc %{_texmf_main}/doc/texlive/tlbuild/tlbuild.pdf
%{_infodir}/tlbuild.info*

%files -n %{shortname}-texlive-scripts
%config(noreplace) %{_sysconfdir}/texlive/web2c/updmap.cfg
%{_bindir}/fmtutil
%{_bindir}/fmtutil-sys
%{_bindir}/fmtutil-user
%{_bindir}/mktexlsr
%{_bindir}/mktexmf
%{_bindir}/mktexpk
%{_bindir}/mktextfm
%{_bindir}/rungs
%{_bindir}/updmap
%{_bindir}/updmap-sys
%{_bindir}/updmap-user
%{_mandir}/man1/fmtutil-sys.1*
%{_mandir}/man1/fmtutil-user.1*
%{_mandir}/man1/fmtutil.1*
%{_mandir}/man1/install-tl.1*
%{_mandir}/man1/mktexlsr.1*
%{_mandir}/man1/mktexmf.1*
%{_mandir}/man1/mktexpk.1*
%{_mandir}/man1/mktextfm.1*
%{_mandir}/man1/updmap-sys.1*
%{_mandir}/man1/updmap-user.1*
%{_mandir}/man1/updmap.1*
%{_mandir}/man5/updmap.cfg.5*
%{_texdir}/texmf-config/web2c/updmap.cfg
%{_texmf_main}/dvips/tetex/
%{_texmf_main}/fonts/enc/dvips/tetex/
%{_texmf_main}/fonts/map/dvips/tetex/
%{_texmf_main}/scripts/texlive/fmtutil-sys.sh
%{_texmf_main}/scripts/texlive/fmtutil-user.sh
%{_texmf_main}/scripts/texlive/fmtutil.pl
%{_texmf_main}/scripts/texlive/mktexlsr*
%{_texmf_main}/scripts/texlive/mktexmf
%{_texmf_main}/scripts/texlive/mktexpk
%{_texmf_main}/scripts/texlive/mktextfm
%{_texmf_main}/scripts/texlive/rungs.lua
# %%{_texmf_main}/scripts/texlive/rungs.tlu
%{_texmf_main}/scripts/texlive/updmap-sys.sh
%{_texmf_main}/scripts/texlive/updmap-user.sh
%{_texmf_main}/scripts/texlive/updmap.pl
%{_texmf_main}/web2c/updmap.cfg

%files -n %{shortname}-texlive-scripts-extra
%{_bindir}/allcm
%{_bindir}/allec
%{_bindir}/allneeded
%{_bindir}/dvi2fax
%{_bindir}/dvired
%{_bindir}/e2pall
%{_bindir}/kpsepath
%{_bindir}/kpsetool
%{_bindir}/kpsewhere
%{_bindir}/kpsexpand
%{_bindir}/ps2frag
%{_bindir}/pslatex
%{_bindir}/texconfig
%{_bindir}/texconfig-dialog
%{_bindir}/texconfig-sys
%{_bindir}/texlinks
%{_mandir}/man1/allcm.1*
%{_mandir}/man1/allec.1*
%{_mandir}/man1/allneeded.1*
%{_mandir}/man1/dvi2fax.1*
%{_mandir}/man1/dvired.1*
%{_mandir}/man1/e2pall.1*
%{_mandir}/man1/kpsepath.1*
%{_mandir}/man1/kpsetool.1*
%{_mandir}/man1/kpsewhere.1*
%{_mandir}/man1/kpsexpand.1*
%{_mandir}/man1/ps2frag.1*
%{_mandir}/man1/pslatex.1*
%{_mandir}/man1/texconfig-sys.1*
%{_mandir}/man1/texconfig.1*
%{_mandir}/man1/texlinks.1*
%{_texmf_main}/scripts/texlive-extra/
%{_texmf_main}/texconfig/

%files -n %{shortname}-texlive.infra
%doc %{_texdir}/tlpkg/README
%doc %{_texmf_main}/scripts/texlive/NEWS
%{_bindir}/tlmgr
%{_datadir}/perl5/TeXLive
%{_mandir}/man1/tlmgr.1*
%{_texdir}/LICENSE.CTAN
%{_texdir}/LICENSE.TL
%{_texdir}/README
%{_texdir}/README.usergroups
%{_texdir}/index.html
%{_texdir}/readme-html.dir/readme.cs.html
%{_texdir}/readme-html.dir/readme.de.html
%{_texdir}/readme-html.dir/readme.en.html
%{_texdir}/readme-html.dir/readme.es.html
%{_texdir}/readme-html.dir/readme.fr.html
%{_texdir}/readme-html.dir/readme.it.html
%{_texdir}/readme-html.dir/readme.ja.html
%{_texdir}/readme-html.dir/readme.pl.html
%{_texdir}/readme-html.dir/readme.pt-br.html
%{_texdir}/readme-html.dir/readme.ru.html
%{_texdir}/readme-html.dir/readme.sk.html
%{_texdir}/readme-html.dir/readme.sr.html
%{_texdir}/readme-html.dir/readme.vi.html
%{_texdir}/readme-html.dir/readme.zh-cn.html
%{_texdir}/release-texlive.txt
%{_texdir}/tlpkg/TeXLive/
%{_texdir}/tlpkg/installer/config.guess
%{_texmf_main}/scripts/texlive/tl-errmess.ps1
%{_texmf_main}/scripts/texlive/tlmgr.pl
%{_texmf_main}/scripts/texlive/uninstq.ps1
%{_texmf_main}/web2c/fmtutil-hdr.cnf
%{_texmf_main}/web2c/updmap-hdr.cfg

%files -n %{shortname}-texloganalyser
%{_bindir}/texloganalyser
%{_texmf_main}/scripts/texloganalyser/
%doc %{_texmf_main}/doc/support/texloganalyser/

%files -n %{shortname}-texlogfilter
%{_bindir}/texlogfilter
%{_mandir}/man1/texlogfilter.1*
%{_texmf_main}/scripts/texlogfilter/
%doc %{_texmf_main}/doc/support/texlogfilter/

%files -n %{shortname}-texlogsieve
%license gpl3.txt
%doc %{_texmf_main}/doc/support/texlogsieve/
%{_bindir}/texlogsieve
%{_mandir}/man1/texlogsieve.1*
%{_texmf_main}/scripts/texlogsieve/

%files -n %{shortname}-texosquery
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/support/texosquery
%{_bindir}/texosquery*
%{_texmf_main}/scripts/texosquery/
%{_texmf_main}/tex/latex/texosquery

%files -n %{shortname}-texplate
%license bsd.txt
%{_bindir}/texplate
%{_texmf_main}/scripts/texplate
%doc %{_texmf_main}/doc/support/texplate

%files -n %{shortname}-texsis
%license lppl1.txt
%{_bindir}/texsis
%{_mandir}/man1/texsis.1*
%{_texmf_main}/bibtex/bst/texsis/
%{_texmf_main}/tex/texsis/
%{fmtutil_cnf_d}/texsis
%doc %{_texmf_main}/doc/otherformats/texsis/

%files -n %{shortname}-texware
%license pd.txt
%{_bindir}/dvitype
%{_bindir}/pooltype
%{_mandir}/man1/dvitype.1*
%{_mandir}/man1/pooltype.1*

%files -n %{shortname}-thumbpdf
%license lppl1.txt
%{_bindir}/thumbpdf
%{_mandir}/man1/thumbpdf.1*
%{_texmf_main}/scripts/thumbpdf/
%{_texmf_main}/tex/generic/thumbpdf/
%doc %{_texmf_main}/doc/generic/thumbpdf/

%files -n %{shortname}-tie
%license other-free.txt
%{_bindir}/tie
%{_mandir}/man1/tie.1*

%files -n %{shortname}-tikztosvg
%license gpl3.txt
%{_bindir}/tikztosvg
%{_mandir}/man1/tikztosvg*
%doc %{_texmf_main}/doc/support/tikztosvg
%{_texmf_main}/scripts/tikztosvg

%files -n %{shortname}-tpic2pdftex
%license gpl2.txt
%doc %{_texmf_main}/doc/support/tpic2pdftex/
%{_bindir}/tpic2pdftex
%{_mandir}/man1/tpic2pdftex.1*

%files -n %{shortname}-ttfutils
%doc %{_texmf_main}/doc/support/ttf2pk/
%{_bindir}/ttf2afm
%{_bindir}/ttf2pk
%{_bindir}/ttf2tfm
%{_bindir}/ttfdump
%{_mandir}/man1/ttf2afm.1*
%{_mandir}/man1/ttf2pk.1*
%{_mandir}/man1/ttf2tfm.1*
%{_mandir}/man1/ttfdump.1*
%{_texmf_main}/fonts/enc/ttf2pk/
%{_texmf_main}/fonts/sfd/ttf2pk/
%{_texmf_main}/ttf2pk/

%files -n %{shortname}-typeoutfileinfo
%license lppl1.3.txt
%{_bindir}/typeoutfileinfo
%{_texmf_main}/scripts/typeoutfileinfo/
%doc %{_texmf_main}/doc/support/typeoutfileinfo/

%files -n %{shortname}-typog
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/latex/typog/
%{_bindir}/typog-grep
%{_mandir}/man1/typog-grep.1*
%{_texmf_main}/scripts/typog/
%{_texmf_main}/tex/latex/typog/

%files -n %{shortname}-ulqda
%license lppl1.txt
%{_bindir}/ulqda
%{_texmf_main}/scripts/ulqda/
%{_texmf_main}/tex/latex/ulqda/
%doc %{_texmf_main}/doc/latex/ulqda/

%files -n %{shortname}-upmendex
%license bsd.txt
%{_bindir}/upmendex
%{_mandir}/man1/upmendex.1*
%doc %{_texmf_main}/doc/support/upmendex/

%files -n %{shortname}-uptex
%license other-free.txt
%doc %{_texmf_main}/doc/uplatex/
%{_bindir}/euptex
%{_bindir}/r-upmpost
%{_bindir}/upbibtex
%{_bindir}/updvitomp
%{_bindir}/updvitype
%{_bindir}/uplatex
%{_bindir}/uplatex-dev
%{_bindir}/upmpost
%{_bindir}/uppltotf
%{_bindir}/uptex
%{_bindir}/uptftopl
%{_bindir}/wovp2ovf
%{_mandir}/man1/euptex.1*
%{_mandir}/man1/upbibtex.1*
%{_mandir}/man1/uplatex-dev.1*
%{_mandir}/man1/uplatex.1*
%{_mandir}/man1/uppltotf.1*
%{_mandir}/man1/uptex.1*
%{_mandir}/man1/uptftopl.1*
%{fmtutil_cnf_d}/uplatex
%{fmtutil_cnf_d}/uptex

%files -n %{shortname}-urlbst
%license gpl2.txt
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/bibtex/urlbst/
%{_bindir}/urlbst
%{_texmf_main}/bibtex/bst/urlbst/
%{_texmf_main}/scripts/urlbst/

%files -n %{shortname}-velthuis
%license gpl.txt
%{_bindir}/devnag
%{_mandir}/man1/devnag.1*
%{_texmf_main}/fonts/afm/public/velthuis/
%{_texmf_main}/fonts/map/dvips/velthuis/
%{_texmf_main}/fonts/source/public/velthuis/
%{_texmf_main}/fonts/tfm/public/velthuis/
%{_texmf_main}/fonts/type1/public/velthuis/
%{_texmf_main}/tex/generic/velthuis/
%{_texmf_main}/tex/latex/velthuis/
%{_texmf_main}/tex/plain/velthuis/
%{_texmf_main}/tex/xelatex/velthuis/
%doc %{_texmf_main}/doc/generic/velthuis/

%files -n %{shortname}-vlna
%license lppl1.txt
%{_bindir}/vlna
%{_mandir}/man1/vlna.1*
%doc %{_texmf_main}/doc/support/vlna/

%files -n %{shortname}-vpe
%license lppl1.txt
%{_bindir}/vpe
%{_texmf_main}/scripts/vpe/
%{_texmf_main}/tex/latex/vpe/
%doc %{_texmf_main}/doc/latex/vpe/

%files -n %{shortname}-web
%license knuth.txt
%{_bindir}/tangle
%{_bindir}/weave
%{_mandir}/man1/tangle.1*
%{_mandir}/man1/weave.1*

%files -n %{shortname}-webquiz
%license gpl.txt
%{_bindir}/webquiz
%{_mandir}/man1/webquiz.1*
%{_texmf_main}/scripts/webquiz/
%{_texmf_main}/tex/latex/webquiz/
%doc %{_texmf_main}/doc/latex/webquiz/

%files -n %{shortname}-wordcount
%license lppl1.txt
%{_bindir}/wordcount
%{_texmf_main}/scripts/wordcount/
%{_texmf_main}/tex/latex/wordcount/
%doc %{_texmf_main}/doc/latex/wordcount/

%files -n %{shortname}-xdvi
%{_bindir}/xdvi
%{_bindir}/xdvi-xaw
%{_mandir}/man1/xdvi.1*
%{_texmf_main}/dvips/xdvi/
%{_texmf_main}/xdvi/

%files -n %{shortname}-xdvipsk
%license gpl2.txt
%{_bindir}/xdvipsk
%{_mandir}/man1/xdvipsk.1*
%{_texmf_main}/dvips/xdvipsk/

%files -n %{shortname}-xetex
%doc %{_texmf_main}/doc/xetex/
%{_bindir}/xdvipdfmx
%{_bindir}/xelatex
%{_bindir}/xelatex-dev
%{_bindir}/xelatex-unsafe
%{_bindir}/xetex
%{_bindir}/xetex-unsafe
%{_mandir}/man1/xelatex-dev.1*
%{_mandir}/man1/xelatex-unsafe.1*
%{_mandir}/man1/xelatex.1*
%{_mandir}/man1/xetex-unsafe.1*
%{_mandir}/man1/xetex.1*
%{_texdir}/tlpkg/tlpostcode/xetex.pl
%{_texmf_main}/fonts/misc/xetex/
%{_texmf_main}/scripts/texlive-extra/
%{fmtutil_cnf_d}/xelatex-dev
%{fmtutil_cnf_d}/xetex

%files -n %{shortname}-xindex
%license lppl1.3c.txt
%license mit.txt
%doc %{_texmf_main}/doc/lualatex/xindex/
%{_bindir}/xindex
%{_texmf_main}/scripts/xindex/
%{_texmf_main}/tex/latex/xindex/
%{_texmf_main}/tex/lualatex/

%files -n %{shortname}-xindy
%license gpl.txt
%if %{without bootstrap}
%{_bindir}/tex2xindy
%{_bindir}/texindy
%{_bindir}/xindy
%{_bindir}/xindy.mem
%endif
%{_mandir}/man1/xindy.1*
%{_mandir}/man1/texindy.1*
%{_mandir}/man1/tex2xindy.1*
%{_texmf_main}/scripts/xindy/
%{_texmf_main}/xindy/
%doc %{_texmf_main}/doc/xindy/

%files -n %{shortname}-xml2pmx
%license gpl3.txt
%{_bindir}/xml2pmx
%{_mandir}/man1/xml2pmx*

%files -n %{shortname}-xmltex
%license lppl1.3c.txt
%doc %{_texmf_main}/doc/otherformats/xmltex/
%{_bindir}/pdfxmltex
%{_bindir}/xmltex
%{_texmf_main}/tex/xmltex/
%{fmtutil_cnf_d}/xmltex

%files -n %{shortname}-xpdfopen
%{_bindir}/pdfclose
%{_bindir}/pdfopen
%{_mandir}/man1/pdfclose.1*
%{_mandir}/man1/pdfopen.1*

%files -n %{shortname}-yplan
%license lppl1.txt
%{_bindir}/yplan
%{_texmf_main}/scripts/yplan/
%{_texmf_main}/tex/latex/yplan/
%doc %{_texmf_main}/doc/latex/yplan/

%changelog
* Fri May 01 2026 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 12:20260301-111
- Fix erroneous autogenerated Provides for paths matching extensions without dots

* Wed Apr 29 2026 Tom Callaway <spot@fedoraproject.org> - 12:20260301-110
- move %{_bindir}/lualatex to the luahbtex package (bz2460478)

* Wed Apr  1 2026 Tom Callaway <spot@fedoraproject.org> - 12:20260301-109
- fix typo causing "tfm" font files to not be detected for autogenerated provides

* Thu Mar 26 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 12:20260301-108
- Remove duplicate texmfstart

* Wed Mar 25 2026 Tom Callaway <spot@fedoraproject.org> - 12:20260301-107
- add explicit Provides: tex(dvips) back (bz2451395)

* Tue Mar 24 2026 Tom Callaway <spot@fedoraproject.org> - 12:20260301-106
- Add local RPM dependency generator to produce tex(...) Provides
  Full credit to Elliott Sales de Andrade <quantum.analyst@gmail.com>

* Tue Mar 17 2026 Tom Callaway <spot@fedoraproject.org> - 12:20260301-105
- aliascnt.sty has left oberdiek for its own package (in texlive-collection-latexextra)

* Sat Mar 14 2026 Tom Callaway <spot@fedoraproject.org> - 12:20260301-104
- Move runtexfile and show-pdf-tags from collection-binextra to here
- Add xdvipsk package (new)
- Update aleph to svn77830
- Update amstex to svn77830
- Update aomart to svn76110
- Update arara to svn75653
- Update attachfile2 to svn77682
- Update autosp to svn77851
- Update axodraw2 to svn77682
- Update bib2gls to svn76845
- Update bibtex to svn77830
- Update bibtexperllibs to svn76255
- Update bibtex8 to svn75712
- Update chktex to svn78219
- Update citation-style-language to svn77682
- Update clojure-pamphlet to svn77682
- Update context to svn78010
- Update context-legacy to svn78010
- Update csplain to svn76924
- Update ctie to svn77830
- Update cweb to svn77830
- Update dtxgen to svn75946
- Update dvicopy to svn77830
- Update dvidvi to svn75712
- Update dvipdfmx to svn77942
- Update dvipng to svn77830
- Update dvips to svn77830
- Update dvisvgm to svn77830
- Update ebong to svn76924
- Update eolang to svn77164
- Update exceltex to svn76924
- Update expltools to svn78336
- Update extractbb to svn77855
- Update fontools to svn78330
- Update fontware to svn77830
- Update glossaries to svn78288
- Update hitex to svn77830
- Update hyperxmp to svn78281
- Update kpathsea to svn77861
- Update l3build to svn77170
- Update l3sys-query to svn77682
- Update lacheck to svn75712
- Update latex to svn76924
- Update latex2man to svn77377
- Update latex2nemeth to svn76924
- Update latexdiff to svn77278
- Update latexindent to svn76064
- Update luafindfont to svn75679
- Update luahbtex to svn77830
- Update luajittex to svn77830
- Update luatex to svn78218
- Update lwarp to svn78111
- Update make4ht to svn78133
- Update makedtx to svn77871
- Update makeindex to svn75712
- Update markdown to svn77254
- Update match_parens to svn76442
- Update metafont to svn77830
- Update metapost to svn77830
- Update mflua to svn77830
- Update mfware to svn77830
- Update minted to svn78270
- Update mkpic to svn76483
- Update mptopdf to svn78010
- Update multibibliography to svn77682
- Update musixtex to svn77682
- Update m-tx to svn78106
- Update oberdiek to svn78315
- Update omegaware to svn77830
- Update optex to svn78109
- Update patgen to svn77830
- Update pdfbook2 to svn76924
- Update pdftex to svn77868
- Update pdftosrc to svn77830
- Update pst-pdf to svn77682
- Update ps2eps to svn76924
- Update ps2pk to svn75712
- Update ptex to svn77830
- Update pythontex to svn77873
- Update splitindex to svn77682
- Update sty2dtx to svn76924
- Update tex to svn77830
- Update tex4ebook to svn78132
- Update tex4ht to svn78343
- Update texfot to svn77286
- Update texliveonfly to svn76924
- Update texlive-en to svn78030
- Update texlive-scripts to svn78361
- Update texlive-scripts-extra to svn78162
- Update texlive.infra to svn78313
- Update texlogsieve to svn77351
- Update texosquery to svn77682
- Update texware to svn77830
- Update tie to svn77830
- Update tpic2pdftex to svn75712
- Update ttfutils to svn77830
- Update typog to svn76661
- Update uptex to svn77830
- Update urlbst to svn76790
- Update web to svn77830
- Update xetex to svn77830
- Update xindex to svn77844
- Update xmltex to svn76924

* Fri Mar 13 2026 Tom Callaway <spot@fedoraproject.org> - 12:20260301-103
- update to 20260301 (wheeee!)

* Thu Feb 19 2026 Tom Callaway <spot@fedoraproject.org> - 12:20250308-102
- fix provides for texlive-uplatex (bz2437564)

* Tue Feb 10 2026 Tom Callaway <spot@fedoraproject.org> - 12:20250308-101
- update git-latexdiff to svn75878 (bz2435847)
- fix texlive-git-latexdiff to be noarch package (it is just shell)

* Fri Jan 23 2026 Than Ngo <than@redhat.com> - 12:20250308-100
- Fix rhbz#2431538, FTBFS with gcc-16

* Thu Jan 22 2026 Tom Callaway <spot@fedoraproject.org> - 12:20250308-99
- time to land this big bird in rawhide. hold on to your butts.
- oh and we're also forcing -std=gnu++17. Thanks icu.

- Historical notes from my TL2025 out-of-band changes are below
- * Tue Oct 21 2025 Tom Callaway <spot@fedoraproject.org>
  - strip the scripts out of bibtexperllibs to avoid conflicts
- * Fri Oct 17 2025 Tom Callaway <spot@fedoraproject.org>
  - fix typos in explicit perl module dependencies
- * Tue Oct  7 2025 Tom Callaway <spot@fedoraproject.org>
  - update crossrefware to r76407 to fix typo which was causing invalid perl(IO::file) (should be IO::File) dependency
  - add Provides for texlive-xelatex-dev (we don't actually package this)
- * Mon Sep 22 2025 Tom Callaway <spot@fedoraproject.org>
  - add more obsoletes, make the ms one more accurate
- * Fri Sep 19 2025 Tom Callaway <spot@fedoraproject.org>
  - obsolete texlive-ms/ms-doc
- * Thu Sep 18 2025 Tom Callaway <spot@fedoraproject.org>
  - bootstrap off
- * Thu Sep 18 2025 Tom Callaway <spot@fedoraproject.org>
  - remove all Requires on old "tex-" names, we don't use those anymore
    and it was causing old packages to be pulled in
  - bootstrap still on
- * Tue Sep 16 2025 Tom Callaway <spot@fedoraproject.org>
  - fix dep issue
- * Wed Jun 11 2025 Tom Callaway <spot@fedoraproject.org>
  - TeXLive 2025

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 11:20230311-95
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Nov 26 2025 Björn Esser <besser82@fedoraproject.org> - 11:20230311-94
- Rebuild(xpdf)

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 11:20230311-93
- Rebuilt for icu 77.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11:20230311-92
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 19 2025 Than Ngo <than@redhat.com> - 11:20230311-91
- Fix rhbz#2379729 - texlive-pythontex is not compatible with python3.13

* Fri Jul 18 2025 Than Ngo <than@redhat.com> - 11:20230311-90
- Fix rhbz#2354991 - bundling option for perl-5.40.x

* Thu Jan 23 2025 Than Ngo <than@redhat.com> - 11:20230311-89
- Fix rhbz#2341430, FTBFS with gcc15

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11:20230311-88
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 11:20230311-87
- Rebuild for ICU 76

* Thu Aug 01 2024 Than Ngo <than@redhat.com> - 20230311-86
- fix license tag

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11:20230311-85
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 10 2024 Than Ngo <than@redhat.com> - 20230311-84
- fix bz#2271830, fix eln marco

* Fri Mar 15 2024 Than Ngo <than@redhat.com> - 20230311-83
- fix bz#2269661, FTBFS due to libXaw 1.0.16

* Thu Feb 29 2024 Tom Callaway <spot@fedoraproject.org> - 11:20230311-82
- rebuild for new xpdf

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 11:20230311-81
- Rebuild for ICU 74

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11:20230311-80
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Michael J Gruber <mjg@fedoraproject.org> - 11:20230311-79
- fix FTBFS with GCC 14 on i686
- add missed ignore entries from "Update to TL2022"

* Fri Jan 19 2024 Than Ngo <than@redhat.com> - 11:20230311-78
- fixed bz#2259157 - texlive-base FTBFS

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11:20230311-77
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 11:20230311-76
- Rebuilt for ICU 73.2

* Mon Jun  5 2023 Tom Callaway <spot@fedoraproject.org> - 11:20230311-75
- move texmfcnf.lua to /etc/texlive/web2c with a symlink back to its original home in /usr/share/texlive/texmf-dist/web2c
- properly handle mkii files that should only be in texlive-mptopdf

* Tue May 30 2023 Tom Callaway <spot@fedoraproject.org> - 11:20230311-74
- fix double packaging of mptopdf files in context

* Thu May 25 2023 Tom Callaway <spot@fedoraproject.org> - 11:20230311-73
- update to svn66984 source tree to fix CVE-2023-32700
- fix mtxrun stub
- patch texmfcnf.lua
- fix mptopdf.pl and thumbpdf.pl to have proper interpreter lines

* Fri Apr 14 2023 Tom Callaway <spot@fedoraproject.org> - 11:20230311-72
- fix Requires for texlive-fontools (bz 2185284)

* Mon Mar 27 2023 Tom Callaway <spot@fedoraproject.org> - 11:20230311-71
- fix texaccents so that:
  1. it has all the includes it needs
  2. it is noarch
  3. it has a proper launcher script
  NOTE1: texaccents will no longer pickup a Requires on /usr/bin/snobol4
         but it still needs it. It's pending review for inclusion in Fedora.
  NOTE2: With snobol4, texaccents itself runs but does not function usefully
         at the moment

* Mon Mar 20 2023 Tom Callaway <spot@fedoraproject.org> - 11:20230311-70
- TeXLive 2023
- bring digestif over here

* Mon Mar  6 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-69
- fix texlive-pdfcrop to have an explicit Requires: texlive-pdftex (bz2175666)

* Tue Jan 31 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-68
- fix header order for xpdf dependent bits to ensure off_t is set properly on i686

* Tue Jan 31 2023 Florian Weimer <fweimer@redhat.com> - 10:20220321-67
- Various C99 compatibility fixes

* Mon Jan 30 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-66
- conditionalize use of poppler (and disable it by default)
- fix issue where vasprintf() could be undefined in a build

* Tue Jan 24 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-65
- artificial bump to 65, I accidentally had ketcindy in both texlive and texlive-base.
  removed it from texlive, rebuilt at release=65, building here at 65 so we have it

* Tue Jan 24 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-61
- rebuild for ghostscript 10.0.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10:20220321-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-58
- hack in dvisvgm 3.0.1

* Sun Jan  8 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-57
- rebuild against libpaper v2

* Sat Jan  7 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-56
- add dependency on texlive-lua-uni-algos on texlive-luaotfload (bz2158837)

* Mon Jan  2 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-55
- minor dep cleanups

* Sun Jan  1 2023 Tom Callaway <spot@fedoraproject.org> - 10:20220321-54
- 10:20220321
- epoch bump so we can use accurate versions for the component packages here
- reminder: release does not reset here due to koji limitations
- fix context-doc package to be noarch
  in theory, this might break some upgrades, but... i bet the number of people
  who have texlive-context-doc (all 90M of it) installed is very very low

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 9:20210325-53
- Rebuild for ICU 72

* Wed Aug 24 2022 Tom Callaway <spot@fedoraproject.org> - 9:202110325-52
- fixup texlive-base-20210325-poppler-22.08.0.patch (bz2121167)

* Mon Aug 08 2022 Marek Kasik <mkasik@redhat.com> - 9:20210325-51
- Bootstrap off

* Mon Aug 08 2022 Marek Kasik <mkasik@redhat.com> - 9:20210325-50
- Rebuild for poppler 22.08.0 - bootstrap on

* Wed Aug 03 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 9:20210325-49
- Rebuild for ICU 71.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9:20210325-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Tom Callaway <spot@fedoraproject.org> - 9:20210325-47
- replace group handling code in pdftoepdf.cc with code that is simpler (and does not crash)

* Sat Jan 15 2022 Tom Callaway <spot@fedoraproject.org> - 9:20210325-46
- bootstrap off (conditionalize poppler changes)

* Thu Jan 13 2022 Tom Callaway <spot@fedoraproject.org> - 9:20210325-45
- rebuild for new poppler, bootstrap on

* Tue Jan 11 2022 Tom Callaway <spot@fedoraproject.org> - 9:20210325-44
- update arara to address log4j CVEs

* Wed Dec 15 2021 Tom Callaway <spot@fedoraproject.org> - 9:20210325-43
- rework the font map trigger logic

* Wed Sep 08 2021 Than Ngo <than@redhat.com> - 9:20210325-42
- Re-enable LTO

* Mon Aug 16 2021 Stephen Gallagher <sgallagh@redhat.com> - 9:20210325-41
- Rebuild for libpoppler soname bump

* Mon Aug  2 2021 Tom Callaway <spot@fedoraproject.org> - 9:20210325-40
- bootstrap off

* Mon Aug  2 2021 Tom Callaway <spot@fedoraproject.org> - 9:20210325-39
- rebuild for poppler

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9:20210325-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Tom Callaway <spot@fedoraproject.org> - 9:20210325-37
- fix fonts/map/dvips ownership
- rename dvipdfm35.map to dvipdfm35.oldmap to prevent it from being included in pdftex.map
- fix lyluatex versioning

* Mon Jun 21 2021 Tom Callaway <spot@fedoraproject.org> - 9:20210325-36
- remove deprecated .setpdfwrite ghostscript call

* Fri May 28 2021 Tom Callaway <spot@fedoraproject.org> - 9:20210325-35
- force system font maps to be sync'd with trees and regenerated in the triggers

* Fri May 28 2021 Tom Callaway <spot@fedoraproject.org> - 9:20210325-34
- add texlive-gsftopk as a dependency on texlive-texlive-scripts for mktexpk
- add texlive-psnfss as a dependency on texlive-latex
- drop Rquires: tex(psfonts.map), died with updmap-map
- conditionalize removing rpath from binaries which aren't always built

* Thu May 27 2021 Tom Callaway <spot@fedoraproject.org> - 9:20210325-33
- scrape rpath off everything

* Thu May 27 2021 Tom Callaway <spot@fedoraproject.org> - 9:20210325-32
- 20210325

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 7:20200327-31
- Rebuild for ICU 69

* Thu Apr  1 2021 Tom Callaway <spot@fedoraproject.org> - 7:20200327-30
- update source urls (except tug urls) to https

* Thu Mar 18 2021 Tom Callaway <spot@fedoraproject.org> - 7:20200327-29
- force builtin copy of pygmentex to 0.10 (supports python3)

* Tue Feb 2  2021 Tom Callaway <spot@fedoraproject.org> - 7:20200327-28
- set TEXMFLOCAL during the context scriptlet to minimize the scope of where it looks during mtxrun --generate

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9:20200327-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 26 2021 Tomas Popela <tpopela@redhat.com> - 9:20200327-26
- Don't build texlive-xindy on ELN because of its requirements (clisp)

* Fri Jan 15 2021 Tom Callaway <spot@fedoraproject.org> - 9:20200327-25
- debootstrap

* Fri Jan 15 2021 Tom Callaway <spot@fedoraproject.org> - 9:20200327-24
- fix context shell binary to handle /home dirs that are symlinks (bz1913245)

* Wed Dec 30 2020 Tom Callaway <spot@fedoraproject.org> - 9:20200327-23
- update pygmentex (supports python3)
- update dviasm (supports python3)

* Mon Nov 16 2020 Tom Callaway <spot@fedoraproject.org> - 9:20200327-22
- make proper texlive-optex subpackage by moving it here
- bump epoch to 9 so this texlive-optex package replaces the one that used to live in texlive

* Thu Nov 12 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-21
- obsolete texlive-texconfig, texlive-pdftools, texlive-pstools (in texlive-texlive-scripts-extra)

* Tue Nov 10 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-20
- fix issues with file ownership duplication
- fix issue with obsoleting texlive-tetex
- turn LTO back off, as it was assuming code needed libcrypto for some unknown reason

* Thu Oct 29 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-19
- fix dependencies of texlive-ptex and texlive-uptex

* Sun Oct 11 2020 Jeff Law <law@redhat.com> - 7:20200327-18
- Re-enable LTO

* Wed Sep 23 2020 Than Ngo <than@redhat.com> - 7:20200327-17
- Fix pdflatex run out of memory

* Mon Sep 21 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-16
- move "mtxrun --generate" call from -kpathsea transfiletriggerin to -context
- drop Requires(post): texlive-context from -kpathsea
- add an explicit versioning on the dependency of texlive-texlive-scripts in -kpathsea (and vice versa)

* Thu Aug 13 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-15
- make texlive-latex have an explicit Requires on texlive-cm-super (bz1867927)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7:20200327-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Tom Stellard <tstellar@redhat.com> - 7:20200327-13
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 21 2020 Marek Kasik <mkasik@redhat.com> - 7:20200327-12
- rebuild for poppler 0.90.0
- bodhi needs latest build

* Tue Jul 14 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-11
- disable bootstrap

* Tue Jul 14 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-10.1
- unbootstrapped build (TEMPORARY, when -11 comes out of the side tag, it will replace this)

* Tue Jul 14 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-10
- bootstrap again again

* Tue Jul 14 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-9
- bootstrap again

* Tue Jul 14 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-8
- rebuild for poppler 0.90.0
- bootstrap on

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 7:20200327-7
- Disable LTO

* Wed May 27 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-6
- split off context-doc (bz1839593)
- add Rquires: tex(psfonts.map) to gsftopk (bz1840379)
- update component sources to match main tree tarball (not doing this before was an epic fail on my part)

* Wed May 20 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-5
- rebuild with bootstrap off and triggers with debugging off

* Sun May 17 2020 Orion Poplawski <orion@nwra.com> - 7:20200327-4
- Add bootstrap flag to disable circular dep on latex due to xindy
- Fix --disable-xindy-rules configure parameter

* Sat May 16 2020 Orion Poplawski <orion@nwra.com> - 7:20200327-3
- Make texlive-kpathsea require texlive-texlive-scripts (bz#1836464)
- Update fedora/rhel conditionals
- Add (temporary) BR on texlive-texlive-scripts to fix latex dummy.tex

* Wed May 13 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-2
- fix symlink issues

* Mon Apr 20 2020 Tom Callaway <spot@fedoraproject.org> - 7:20200327-1
- update to 20200327

* Wed Feb 05 2020 Than Ngo <than@redhat.com> - 7:20190410-12
- fix bz#1798119 - buffer overflow in TexOpen() function, CVE-2019-19601

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7:20190410-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Tom Callaway <spot@fedoraproject.org> - 7:20190410-10
- fix gcc10 issues

* Fri Jan 17 2020 Marek Kasik <mkasik@redhat.com> - 7:20190410-9
- Bring back xindy and the circular dependency on texlive-latex

* Fri Jan 17 2020 Marek Kasik <mkasik@redhat.com> - 7:20190410-8
- Rebuild for poppler-0.84.0
- Don't include C++ headers in C sources
- Temporarily break circular dependency on texlive-latex (will be reverted)

* Fri Jan 10 2020 Tom Callaway <spot@fedoraproject.org> - 7:20190410-7
- fix python3 issue with pdfbook2 (thanks to "Mildred", bz1733794)
- fix python3 issue with latex-papersize (thanks to Silas S. Brown, bz1783964)

* Fri Nov 15 2019 Tom Callaway <spot@fedoraproject.org> - 7:20190410-6
- package up the TL fork of psutils to help tlmgr find all the configs it expects

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 7:20190410-5
- Rebuild for ICU 65

* Fri Oct 18 2019 Tom Callaway <spot@fedoraproject.org> - 7:20190410-4
- fix dir ownership

* Wed Oct  9 2019 Jerry James <loganjerry@gmail.com> - 7:20190410-3
- Rebuild for mpfr 4

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7:20190410-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 23 2019 Tom Callaway <spot@fedoraproject.org> - 7:20190410-1
- update to 20190410
- update all component tarballs to latest available
- new subpackages: cluttex, ctanbib, dviout-util, pdftex-quiet, webquiz, xindex
- add a slightly neutered tlmgr back into texlive.infra because texconfig paper needs it
  IF YOU ARE READING THIS PLEASE DO NOT USE tlmgr install/update. IF YOU IGNORE ME
  PLEASE DO NOT FILE BUGS. PLEASE DO NOT REQUEST THE tlmgrgui BITS.

* Wed May 15 2019 Jerry James <loganjerry@gmail.com> - 7:20180414-36
- Fix xindy build by eliminating race to create latex.fmt
- Build xindy on all supported arches

* Tue Mar 19 2019 Tom Callaway <spot@fedoraproject.org> - 7:20180414-35
- do not throw no file error in synctex

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7:20180414-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Marek Kasik <mkasik@redhat.com> - 7:20180414-33
- Rebuild for poppler-0.73.0

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 7:20180414-32
- Rebuild for ICU 63

* Wed Jan 16 2019 Than Ngo <than@redhat.com> - 7:20180414-31
- fixed annocheck distro flag failure detected by rpmdiff

* Wed Dec 12 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-30
- add explicit Requires: texlive-xetex to texlive-dvipdfmx (bz1657755)

* Fri Dec  7 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-29
- use python3 properly in pdfbook2

* Mon Nov 26 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-28
- do not try to ls /usr/share/texlive/fmtutil.cnf.d, it can be empty, 
  and that makes for noisy errors in scripts (bz1650935)
  Thanks to Villy Kruse.
- fix pkgconfig cleanup sed to use %%{source_date} instead of %%{version}
  which is overridden with subpackage specific data at that point. (bz1426622)

* Mon Nov 12 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-27
- make texlive-kpathsea Requires: texlive-tetex so scriptlets don't fail noisily

* Thu Nov  8 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-26
- make a symlink so texdoc can find texlive.tlpdb

* Thu Nov  1 2018 Adam Williamson <awilliam@redhat.com> - 7:20180414-25
- Add missing dep from -tetex to -texconfig (bz1555931)

* Thu Oct  4 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-24
- disable test that fails on 32 bit arches in rawhide

* Mon Oct  1 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-23
- apply upstream fix for CVE-2018-17407

* Wed Sep 19 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-22
- fix lyluatex provides

* Tue Sep 18 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-21
- add lyluatex

* Fri Aug 24 2018 Marek Kasik <mkasik@redhat.com> - 7:20180414-20
- Install synctex_version.h to be able to build evince

* Tue Aug 14 2018 Marek Kasik <mkasik@redhat.com> - 7:20180414-19
- Rebuild for poppler-0.67.0
- Disable xindy temporarily (there is a cyclic dependency which
- prevents me from building texlive-base with new poppler)

* Mon Aug  6 2018 Marek Kasik <mkasik@redhat.com> - 7:20180414-18
- Fix paths in pkgconfig files
- Resolves: #1426622

* Wed Jul 11 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-17
- update latex2man to resolve perl issues
- use different ctan mirror, old one was out of date
- update pretty much everything since we're updating latex2man and we know the old mirror was outdated
- l3build and axodraw2 are now packaged properly in the tarball
- texdoctk is now its own package (reflecting upstream split)

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 7:20180414-16
- Rebuild for ICU 62

* Sat Jul  7 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-15
- revert trigger changes from -14

* Mon Jul  2 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-14
- fix triggers to force enable of new maps and run syncwithtrees before doing map operations
- add old "tex-foo-doc" provides for every package with doc provides (bz1593860, 1593863)

* Tue Jun 26 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-13
- apply tibbs's fix (PR#4) for fmtutil cnf handling without tons of ugly scriptlets
- explicitly run updmap-sys in the kpathsea triggers, bug reports imply this is needed

* Tue Jun 19 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-12
- add Requires: tex(fvextra.sty) to pythontex (bz1590621)

* Mon Jun 11 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-11
- add tex-jfontmaps(bin/doc) provides

* Fri Jun  8 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-10
- add tex-uplatex(bin/doc) provides

* Thu Jun  7 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-9
- add pretrans to handle /usr/share/texmf

* Mon Jun  4 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-8
- add Provides: tetex-dvips
- add symlink to /usr/share/texmf for legacy packages

* Fri Jun  1 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-7
- add Provides: xmltex

* Tue May 29 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-6
- add BR: texlive-metafont, texlive-cm-super, texlive-ec for xindy
- disable xindy for arm

* Tue May 29 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-5
- fix xindy and jfontmaps obsoletes
- fix typo preventing xindy subpackage

* Tue May 29 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-4
- add Provides: jadetex and Provides: tex-uptex-doc

* Mon May 21 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-3
- add posttrans to force latex scriptlets to work right

* Mon May 14 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-2
- fix arara-doc obsoletes (bz1576693)

* Tue May  1 2018 Tom Callaway <spot@fedoraproject.org> - 7:20180414-1
- update to 20180414
- fix synctex.pc (bz1426622)
- new subpackages: axodraw2, bib2gls, ctan-o-mat, dviinfox, jfmutil, l3build, wordcount

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 7:20170520-28
- Rebuild for ICU 61.1

* Fri Mar 30 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-27
- actually use the texmf.cnf we patch (not the vanilla one from the kpathsea.tar.xz)

* Tue Mar 27 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-26
- add lcdf-typetools provide to fix broken collection-fontutils (fixing that in texlive later) (bz1560379)
- add LatexIndent* to filtered Requires to prevent dep issues there (bz1560381)

* Sun Mar 25 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-25
- fix aleph obsoletes (bz1560355)

* Fri Mar 23 2018 Kevin Fenzi <kevin@scrye.com> - 7:20170520-24
- Rebuild for poppler soname bump.

* Thu Mar 15 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-23
- add Requires: tex(pdfpages.sty) to texlive-pdfjam (bz1164237)

* Sun Mar 11 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-22
- fix a2ping to work with gs 9.22

* Sat Mar 10 2018 Kevin Fenzi <kevin@scrye.com> - 7:20170520-21
- Make kpathsea scriptlets not fail in the installer env.

* Fri Mar  9 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-20
- disable cjk-gs-integrate 

* Fri Mar  9 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-19
- configure TEXMFLOCAL to point to /usr/share/texlive/texmf-local/ (bz1553462)

* Wed Mar  7 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-18
- switch to shebang mangling that does not change exec perms
  most/all of the mangling is correct, but we do not want to risk breaking
  ancient texlive scripts that are suddently -x
- add versions for arara bundled provides
- use spaces instead of tabs

* Mon Mar  5 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-17
- add Provides: tetex-latex to the latex subpackage
- fix obviously incorrect license tag on -base package
- use %%_rpmmacrodir instead of our local %%macrosdir
- add BuildRequires: gcc gcc-c++

* Mon Feb 26 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-16
- include uplatex docs in uptex
- conditionalize xindy because clisp doesn't have ppc64/aarch64 packages

* Sat Feb 24 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-15
- turn on xindy
- disable shebang mangling
- disable tests that fail on 32bit arches with gcc8

* Fri Feb 23 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-14
- pass LDFLAGS
- update lcdf-typetools to git current to fix test failures
- turn on xindy

* Thu Feb 22 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-13
- rebuild again for new poppler in rawhide/f28

* Sun Feb  4 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-12
- fix pathing so that texinfo files are found

* Thu Jan 18 2018 Tom Callaway <spot@fedoraproject.org> - 7:20170520-11
- add missing deps for texlive-pdfbook2
- fix ghostscript BR

* Wed Nov 29 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-10
- kpathsea trigger uses mtxrun, which is in the context subpackage ...
  ... but the kpathsea subpackage did not have a Requires on it.
  It does now. How long was this broken?!?
- force texdir/texmf-var to be a symlink to /var/lib/texmf

* Tue Nov 14 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-9
- var handling & perl cleanups & extra scriptlets

* Fri Nov 10 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-8
- add additional provides for texlive-dvipng, texlive-dvipdfmx, and texlive-xdvi

* Fri Nov 10 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-7
- add epoch to Obsolete versioning

* Thu Nov  9 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-6
- try removing a version from the kpathsea-bin/kpathsea-doc Obsoletes
  to see if that will work with DNF. I miss yum.

* Thu Nov  9 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-5
- lie about what texlive-kpathsea-lib(__isa) version we provide
  because rpm needs this to get over the dependency hurdle

* Thu Nov  9 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-4
- add explicit provide for texlive-kpathsea-lib(__isa) to facilitate update

* Thu Nov  9 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-3
- use more accurate provides

* Sun Oct 29 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-2
- use new files from upstream that work with current poppler in rawhide

* Tue Sep 12 2017 Tom Callaway <spot@fedoraproject.org> - 7:20170520-1
- new package
