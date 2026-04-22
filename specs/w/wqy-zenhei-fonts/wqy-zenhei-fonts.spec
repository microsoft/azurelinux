# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT

%global fontname wqy-zenhei

Version: 0.9.46
Release: 35%{?dist}
URL:     http://wenq.org/enindex.cgi

%global foundry           WQY
%global fontlicense       GPL-2.0-only WITH Font-exception-2.0
%global fontlicenses      COPYING
%global fontdocs          AUTHORS ChangeLog README

%global fontfamily        ZenHei
%global fontsummary       WenQuanYi Zen Hei CJK Font
%global fonts             *.ttc
%global fontconfs         %{SOURCE10}
%global fontdescription   %{expand:
WenQuanYi Zen Hei is a Hei-Ti style (sans-serif type) Chinese \
outline font. It is designed for general purpose text formatting \
and on-screen display of Chinese characters and symbols from \
many other languages. The embolden strokes of the font glyphs \
produces enhanced screen contrast, making it easier to read \
recognize. The embedded bitmap glyphs further enhance on-screen \
performance, which can be enabled with the provided configuration \
files. WenQuanYi Zen Hei provides a rather complete coverage to \
Chinese Hanzi glyphs, including both simplified and traditional \
forms. The total glyph number in this font is over 35,000, including \
over 21,000 Chinese Hanzi. This font has full coverage to GBK(CP936) \
charset, CJK Unified Ideographs, as well as the code-points \
needed for zh_cn, zh_sg, zh_tw, zh_hk, zh_mo, ja (Japanese) \
and ko (Korean) locales for fontconfig. Starting from version \
0.8, this font package has contained two font families, i.e. \
the proportionally-spaced Zen Hei, and a mono-spaced face \
named "WenQuanYi Zen Hei Mono".
}

Source0:  http://downloads.sourceforge.net/wqy/%{fontname}-%{version}-May.tar.bz2
Source10: 66-%{fontpkgname}.conf

%fontpkg

%prep
%setup -q -n %{fontname}
%linuxtext -e GB18030 AUTHORS
%linuxtext -e ISO-8859-1 README

%build
%fontbuild

%install
%fontinstall

%check
%fontcheck

%fontfiles

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 13 2023 Peng Wu <pwu@redhat.com> - 0.9.46-29
- Update to follow New Fonts Packaging Guidelines
- Migrate to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May  4 2015 Peng Wu <pwu@redhat.com> - 0.9.46-13
- Lower font priority, as Adobe Source Han Sans are default Chinese fonts

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Peng Wu <pwu@redhat.com> - 0.9.46-9
- Fixes spec file again

* Thu Nov 15 2012  Peng Wu <pwu@redhat.com> - 0.9.46-8
- Improves spec file

* Tue Nov 13 2012  Peng Wu <pwu@redhat.com> - 0.9.46-7
- Fixes spec file

* Wed Aug 22 2012  Peng Wu <pwu@redhat.com> - 0.9.46-6
- Fixes Download URL

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012  Peng Wu <pwu@redhat.com> - 0.9.46-4
- Fixes fontconf

* Fri Jan 06 2012  Peng Wu <pwu@redhat.com> - 0.9.46-3
- Change the default Simplified Chinese font to "WenQuanYi Zen Hei Sharp"

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011  Peng Wu <pwu@redhat.com> - 0.9.46-1
- Update to snapshot build (Fighting-states) for GB18030 test.

* Thu May 27 2010  Peng Wu <pwu@redhat.com> - 0.9.45-5
- Obsoletes -common sub-package.

* Wed May 26 2010  Peng Wu <pwu@redhat.com> - 0.9.45-4
- Clean up rpm spec file and remove unused patches.

* Wed May 26 2010  Peng Wu <pwu@redhat.com> - 0.9.45-3
- Improves Simplified Chinese and Traditional Chinese fonts.
  Resolves [rhbz#595223] Improves SC/TC fonts - Make wqy-zenhei as the default font for Simplified Chinese.

* Mon Apr 19 2010  Peng Wu <pwu@redhat.com> - 0.9.45-2
- get rid of binding="same", fixes [rhbz#578051] New: lang-specific overrides rule doesn't work as expected.

* Mon Mar 15 2010  Peng Wu <pwu@redhat.com> - 0.9.45-1
- Update to the upstream version 0.9.45 (#573330)

* Mon Mar 01 2010 Peng Wu <pwu@redhat.com> - 0.8.38-5
- make this package adopt the Packaging:FontsPolicy (#568587)

* Mon Dec 21 2009 Jens Petersen <petersen@redhat.com> - 0.8.38-4
- add a fedora fontconfig file for zh (#476459)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

*Mon Mar 30 2009 Qianqian Fang <fangqq@gmail.com> 0.8.38-2
- rebuild to pickup font autodeps (# 491974)

*Sat Mar 07 2009 Qianqian Fang <fangqq@gmail.com> 0.8.38-1
- update to the final version of upstream v0.8 release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.34-3.20081027cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

*Wed Feb 11 2009 Qianqian Fang <fangqq@gmail.com> 0.8.34-2.20081027cvs
- remove fontconfig preference section (# 476459)

*Tue Feb 10 2009 Qianqian Fang <fangqq@gmail.com> 0.8.34-1.20081027cvs
- use fontpackages macros (# 478891)

*Mon Oct 27 2008 Qianqian Fang <fangqq@gmail.com> 0.8.34-0.cvs20081027
- upstream new version prelease

*Wed Jun 25 2008 Qianqian Fang <fangqq@gmail.com> 0.6.26-0
- new upstream release

*Sat Apr 5 2008 Qianqian Fang <fangqq@gmail.com> 0.5.23-0
- new upstream release

*Fri Feb 15 2008 Qianqian Fang <fangqq@gmail.com> 0.4.23-1
- new upstream release

*Fri Nov 2 2007 Qianqian Fang <fangqq@gmail.com> 0.2.16-0.2.20071031cvs
- spec file clean up

*Thu Nov 1 2007 Qianqian Fang <fangqq@gmail.com> 0.2.16-0.1.20071031cvs
- initial packaging for Fedora (# 361121)

