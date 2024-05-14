Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global libchewing_python_dir %{python3_sitelib}

%global im_name_zh_TW 新酷音輸入法
%global name_zh_TW %{im_name_zh_TW}函式庫

Name:           libchewing
Version:        0.5.1
Release:        18%{?dist}
Summary:        Intelligent phonetic input method library for Traditional Chinese
Summary(zh_TW): %{name_zh_TW}

License:        LGPLv2+
URL:            https://chewing.csie.net/
Source0:        https://github.com/chewing/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# https://github.com/chewing/libchewing/pull/310
Patch0:         0001-chewing.py-supports-platforms-with-64bit-pointer.patch

BuildRequires:  autoconf automake libtool pkgconfig texinfo 
BuildRequires:  sqlite-devel
BuildRequires:  python3-devel
Requires: sqlite
# since f31
Obsoletes:      python2-libchewing < 0.5.1-13

%description
libchewing is an intelligent phonetic input method library for Chinese.

It provides the core algorithm and logic that can be used by various
input methods. The Chewing input method is a smart bopomofo phonetics
input method that is useful for inputting Mandarin Chinese.

%description -l zh_TW
%{name_zh_TW}提供實做了核心選字演算法，以便輸入法程式調用。

%{im_name_zh_TW}是一種智慧型注音/拼音猜字輸入法，透過智慧型的字庫分析、習慣記錄學習與預測分析，
使拼字輸入的人為選字機率降至最低，進而提升中文輸入、打字的效率。

%package -n %{name}-devel
Summary:        Development files for libchewing
Summary(zh_TW): %{name_zh_TW}開發者套件
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n %{name}-devel
Headers and other files needed to develop applications using the %{name}
library.

%description -l zh_TW  -n %{name}-devel
%{name_zh_TW}開發者套件提供了開發%{im_name_zh_TW}相關程式所需的檔案，
像是標頭檔(header files)，以及函式庫。


%package -n python3-%{name}
Summary:        Python binding for libchewing
BuildArch:      noarch
Summary(zh_TW): %{name_zh_TW} python 綁定
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{name}
Python binding of libchewing.

%description -l zh_TW -n python3-%{name}
%{name_zh_TW} python 綁定

%prep
%setup -q
%patch 0 -p1

%build
CFLAGS="%{optflags} -g -DLIBINSTDIR='%{_libdir}'"
autoreconf -ivf
%configure --disable-static
make V=1 RPM_CFLAGS="%{optflags}" %{_smp_mflags}

%install
make DESTDIR=%{buildroot} install INSTALL="install -p"
rm %{buildroot}%{_libdir}/libchewing.la

mkdir -p %{buildroot}%{libchewing_python_dir}
cp -p contrib/python/chewing.py %{buildroot}%{libchewing_python_dir}

rm -f %{buildroot}/%{_infodir}/dir

%files
%doc README.md AUTHORS COPYING NEWS TODO
%{_datadir}/%{name}/
%{_libdir}/*.so.*
%{_infodir}/%{name}.info.*

%files devel
%dir %{_includedir}/chewing
%{_includedir}/chewing/*
%{_libdir}/pkgconfig/chewing.pc
%{_libdir}/*.so

%files -n python3-%{name}
%{libchewing_python_dir}/chewing.py
%{libchewing_python_dir}/__pycache__/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.1-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-16
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-15
- Rebuilt for Python 3.8

* Thu Aug  8 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 0.5.1-14
- Remove obsolete requirements for %%post/%%preun scriptlets

* Thu Aug  8 2019 Robin Lee <cheeselee@fedoraproject.org> - 0.5.1-13
- Remove python2 binding and create python3 one (RHBZ#1738025)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.5.1-11
- Remove hardcoded gzip suffix from GNU info pages

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.1-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.1-6
- Python 2 binary subpackage is renamed to python2-libchewing
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu May 19 2016 Ding-Yi Chen <dchen@redhat.com> - 0.5.1-1
- Upstream update to 0.5.1

* Sat May 07 2016 Ding-Yi Chen <dchen@redhat.com> - 0.5.0-1
- Upstream update to 0.5.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Ding-Yi Chen <dchen at redhat dot com> - 0.4.0-3
- Upstream update to 0.4.0
  Details: https://github.com/chewing/libchewing/releases/tag/v0.4.0
- Fixed Bug 1087272 - libchewing-0.4.0 is available
- Update the URL for Sources.

-* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-3
-- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Ding-Yi Chen <dchen at redhat dot com> - 0.3.5-2
- CFLAGS: added -fstack-protector-strong

* Mon Oct 14 2013 Ding-Yi Chen <dchen at redhat dot com> - 0.3.5-1
- Upstream update to 0.3.5

* Mon Jul 29 2013 Parag Nemade <pnemade at redhat dot com> - 0.3.4-4
- spec file cleanup to follow packaging guidelines

* Wed Feb 27 2013 Ding-Yi Chen <dchen at redhat dot com> - 0.3.4-3
- Fixed [Bug 913214] libchewing complains "no info dir entry" while installing
  Add direntry in libchewing.texi so it can be listed under 
  Category "Localization"

* Thu Feb 07 2013 Ding-Yi Chen <dchen at redhat dot com> - 0.3.4-2
- Fix RPM build.

* Fri Jan 11 2013 Ding-Yi Chen <dchen at redhat dot com> - 0.3.4-1
- Upstream update to 0.3.4
- Download is changed to Google Code.
- /usr/share/chewing is removed, data files now located in
  /usr/lib(64)/libchewing
- Info for libchewing is included.

* Thu Nov 22 2012 Ding-Yi Chen <dchen at redhat dot com> - 0.3.3-5
- RPM Macro: define is replaced by global.

* Tue Nov 20 2012 Ding-Yi Chen <dchen at redhat dot com> - 0.3.3-4
- BuildRequires for libchewing-python changed
  from python-devel to python2-devel
- RPM_BUILD_ROOT changed to buildroot

* Thu Jul 19 2012 Ding-Yi Chen <dchen at redhat dot com> - 0.3.3-3
- Fixed Bug 477690 - libchewing multilib conflict

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 07 2011 Ding-Yi Chen <dchen at redhat dot com> - 0.3.3-1
- Upstream update to 0.3.3
  + Fix memory access violation.
  + Improved Python binding.
  + Merged with libchewing-data project. (r455)
  + Improved random key stroke tester.
  + Fix the handling of phonetic symbols in Hsu's keyboard.
  + Fix unexpected candidate disorder when doing symbol choice.
  + Revised phrase choice from rearward logic.
  + Fix cross compilation.
  + Improved shell script to merge changes form libchewing-data.


* Thu Sep 02 2010 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-28
- Resolves: #625980
  Add padding to wch_t to ensure it's word aligned.

* Thu Mar 04 2010 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-27
- Fix Dvorak Hsu 4th tone key (ibus google issue 755 comment 12,
  chewing google issue 10)
- Resolves: #555192

* Mon Feb 15 2010 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-24
- Fix Hsu and Dvorak Hsu input (ibus google issue 755,
  chewing google issue 10)
- Resolves: #555192

* Mon Feb 15 2010 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-23
- Fix Hsu and Dvorak Hsu input (ibus google issue 755,
  chewing google issue 10)
- Resolves: #555192

* Wed Feb 10 2010 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-22
- Fix Hsu and Dvorak Hsu input (ibus google issue 755)
- Resolves: #555192

* Tue Feb 02 2010 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-21
- Revised phrase choice from rear logic.
  Thus update phraseChoiceRearward.patch as phraseChoiceRearward.2.patch
- Resolves: #555192

* Thu Jan 21 2010 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-20
- Resolves: #555192
- Fix for package wrangler.

* Tue Jan 19 2010 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-18
- Resolves: #555192
- Fix for package wrangler.

* Tue Jan 05 2010 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-17
- Add zh_TW summary and description
- Split out python binding into a subpackage.
- Fix for package wrangler.

* Wed Sep 30 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-16
- Fix chewing Google issue 352:
  zuin_count in chewing_zuin_String( ChewingContext *ctx, int *zuin_count )
  does not count correctly.

* Mon Aug 03 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-15
- Fix [Bug 512108:issue 11] ibus-chewing crash the application
  by move cursor_orig to chewingio.c global.

* Thu Jul 30 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-14
- Fix [Bug 512108] ibus-chewing crash the application

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-12
- Rebuild to correct tags.

* Fri Jun 26 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-11
- Revise phraseChoiceRearward.patch so the cursor won't move to left
  when repeatly press down key.

* Wed May 20 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-10
- Need autoreconf and BuildRequires: pkgconfig to make changes in
  Makefile.am effective, thus actually fix [Bug 477960] libchewing multilib conflict.

* Mon May 18 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-9
- Possible Fix of Bug 501220 - RFE: edit last preedit character from end of line
  Chewing upstream does not handle if phrase choice rearward is enabled.

* Wed Apr 22 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-8
- Fix [Bug 496968] - libchewing-debuginfo does not contain sources.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-6
- Fix [Bug 486409] - Wrong python binding installed path
  Add BuildRequires:  python2-devel

* Wed Feb 18 2009 Adam Jackson <ajax@redhat.com> 0.3.2-5
- Rerun autotools so changes to Makefile.am actually take effect.

* Fri Jan 23 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-4
- touch python-<ver>/site-packages/libchewing/__init__.py,
  So python thinks libchewing is a library.

* Wed Jan 14 2009 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-3
- Add python binding by copy python/chewing.py to
  <python_dir>/site_packages/libchewing

* Tue Dec 23 2008 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-2
- [Bug 477690] libchewing multilib conflict
  Move /usr/share/chewing/fonetree.dat to corresponding libdir.

* Wed Dec 03 2008 Ding-Yi Chen <dchen at redhat dot com> - 0.3.2-0
- Upstream update to 0.3.2.

* Wed Oct 08 2008 Ding-Yi Chen <dchen at redhat dot com> - 0.3.1-0
- Upstream update.

* Wed Sep 17 2008 Ding-Yi Chen <dchen at redhat dot com> - 0.3.0.901-0
- Upstream update.

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3.0-12
- fix license tag

* Tue Apr 22 2008 Caius Chance <cchance@redhat.com> - 0.3.0-11.fc10
- Resolves: rhbz195416 (Initial input mode between Chinese and English.)

* Wed Feb 13 2008 Caius Chance <cchance@redhat.com> - 0.3.0-10.fc9
- Rebuild for F9.

* Tue Jan 08 2008 Caius Chance <cchance@redhat.com> - 0.3.0-9.devel
- Resolves: rhbz#200694 (Moving "Han-Yin" <-> Zhu-Yin" option to AUX UI.)

* Fri Jun 01 2007 Caius Chance <cchance@redhat.com> - 0.3.0-8.devel
- Fixed bz#237916: [chewing] Candidate list (symbol) page change inaccracy.

* Fri Apr 20 2007 Caius Chance <cchance@redhat.com> - 0.3.0-7.fc7
- Fixed bz#237233: Up arrow on candidate list doesn't work.

* Fri Mar 09 2007 Caius Chance <cchance@redhat.com> - 0.3.0-6.devel
- Fixed bz231568: [chewing] Look up table is showing candidates of previous
  look-up.

* Tue Nov 21 2006 Caius Chance <cchance@redhat.com> - 0.3.0-5.fc7
- Fixed bz#216581: Ported the following bugfix:
- (bz#216337: Page Up / Page Down key doesn't when Chewing is activated.)
- (bz#209575: preedit buffer is not cleared when framework calls for
  instance reset.)

* Fri Sep 15 2006 Caius Chance <cchance@redhat.com> - 0.3.0-4.fc6
- Fixed bz#206232 - Shift_L + space doesn't work correctly

* Mon Sep 04 2006 Caius Chance <cchance@redhat.com> - 0.3.0-3.fc6
- Fixed bz#199353 - scim-chewing hangs for commit > 6 characters

* Wed Jul 19 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-2
- fix release

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-1.2.1.1
- rebuild

* Mon May 22 2006 Darshan Santani <dsantani@redhat.com>
- New source tarball added.
- Rebuild.

* Thu May 18 2006 Jens Petersen <petersen@redhat.com>
- configure with --disable-static
- exclude INSTALL from docs

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.2.7-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.2.7-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Aug 16 2005 Jens Petersen <petersen@redhat.com> - 0.2.7-1
- Initial build for Fedora Core
- cleanup spec file according to Fedora standard

* Fri Dec 31 2004 rabit <rabit@ipserv.org> 0.2.5-fc3
- update for 0.2.5. and fedora core 3

* Fri Oct 8 2004 rabit <rabit@ipserv.org> 0.2.4-fc2
- update for 0.2.4.

* Thu Oct 7 2004 rabit <rabit@ipserv.org> 0.2.3-fc2
- Initial build.
