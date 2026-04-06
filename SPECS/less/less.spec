# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A text file browser similar to more, but better
Name: less
Version: 691
Release: 2%{?dist}
License: GPL-3.0-only and BSD-2-Clause
Source0: https://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
%global lesspipe_version 2.22
Source1: https://github.com/wofr06/lesspipe/archive/refs/tags/v%{lesspipe_version}.tar.gz#/lesspipe-%{lesspipe_version}.tar.gz
Source2: less.sh
Source3: less.csh
Patch4: less-394-time.patch
Patch5: less-475-fsync.patch
Patch6: less-436-manpage-add-old-bot-option.patch
Patch8: less-458-lessecho-usage.patch
Patch9: less-458-less-filters-man.patch
Patch10: less-458-lesskey-usage.patch
Patch11: less-458-old-bot-in-help.patch
Patch13: less-436-help.patch
URL: https://www.greenwoodsoftware.com/less/
BuildRequires: ncurses-devel
BuildRequires: autoconf automake libtool
BuildRequires: make
# for lesspipe make test
BuildRequires: perl-Archive-Tar
# for less-color's Perl dependencies
BuildRequires: perl-generators
# for lesspipe
Recommends: (less-color = %{version}-%{release} if perl-interpreter)
Recommends: unzip
Recommends: html2text
Recommends: 7zip

%description
The less utility is a text file browser that resembles more, but has
more capabilities.  Less allows you to move backwards in the file as
well as forwards.  Since less doesn't have to read the entire input file
before it starts, less starts up more quickly than text editors (for
example, vi).

You should install less because it is a basic utility for viewing text
files, and you'll use it frequently.

%package color
Summary: Colorizers for less
Requires: %{name} = %{version}-%{release}
Conflicts: less < 685-5

%description color
Syntax highlighting modes for the less pager.


%prep
%setup -q -a 1
%patch -P 4 -p1 -b .time
%patch -P 5 -p2 -b .fsync
%patch -P 6 -p1 -b .manpage-add-old-bot-option
%patch -P 8 -p1 -b .lessecho-usage
%patch -P 9 -p1 -b .less-filters-man
%patch -P 10 -p1 -b .lesskey-usage
%patch -P 11 -p1 -b .old-bot
%patch -P 13 -p1 -b .help

# get consistent result localy and on builders
sed -i -e 's|"#!/usr/bin/env $selected_shell"|"#!$shellcmd"|' -e '/ZSH_/d' lesspipe-%{lesspipe_version}/configure

%build
rm -f ./configure
autoreconf -fiv
%configure
%make_build CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"

pushd lesspipe-%{lesspipe_version}
./configure --prefix=%{_prefix} --shell=%{_bindir}/sh --bash-completion-dir=%{_datadir}/bash-completion/completions/
# do not run make, it does nothing atm, but it reruns configure with wrong argumens
popd

%install
%make_install
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/profile.d
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/profile.d

pushd lesspipe-%{lesspipe_version}
%make_install
rm -rf $RPM_BUILD_ROOT/usr/share/bash-completion/
popd

%check
pushd lesspipe-%{lesspipe_version}
# we dont have all required components to pass full test, but it is still
# useful to run for debug purposes
make test ||:
popd

%files
%doc README NEWS INSTALL
%license LICENSE COPYING
/etc/profile.d/*
%{_bindir}/less
%{_bindir}/lesscomplete
%{_bindir}/lessecho
%{_bindir}/lesskey
%{_bindir}/lesspipe.sh
%{_mandir}/man1/*

%files color
%{_bindir}/archive_color
%{_bindir}/code2color
%{_bindir}/vimcolor

%changelog
* Tue Jan 27 2026 Michal Hlavinka <mhlavink@redhat.com> - 691-2
- update lesspipe.sh to 2.22

* Tue Jan 27 2026 Michal Hlavinka <mhlavink@redhat.com> - 691-1
- updated to 691 (#2431354)

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 685-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Nov 24 2025 Michal Hlavinka <mhlavink@redhat.com> - 685-6
- reintroduce use more feature rich lesspipe filter, but separate
  perl dependent colorizer into subpackage, credits Yaakov Selkowitz 

* Fri Nov 14 2025 Adam Williamson <awilliam@redhat.com> - 685-5
- Revert new lesspipe filter due to hard perl dependency

* Wed Nov 12 2025 Michal Hlavinka <mhlavink@redhat.com> - 685-4
- use more feature rich lesspipe filter (#2308285)

* Wed Oct 22 2025 Michal Hlavinka <mhlavink@redhat.com> - 685-1
- updated to 685 (#2404089)

* Tue Sep 02 2025 Michal Hlavinka <mhlavink@redhat.com> - 679-4
- add man page for lesspipe.sh (rhbz#2376159)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 679-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 23 2025 Michal Hlavinka <mhlavink@redhat.com> - 679-1
- updated to 679

* Thu May 22 2025 Michal Hlavinka <mhlavink@redhat.com> - 678-1
- updated to 678 (#2367012)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 668-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 18 2024 Michal Hlavinka <mhlavink@redhat.com> - 668-1
- updated to 668 (#2319532)

* Mon Aug 12 2024 Michal Hlavinka <mhlavink@redhat.com> - 661-2
- fix post-v590 regression causing reading only part of pipe when stdin is null (upstream#558)

* Fri Jul 26 2024 Michal Hlavinka <mhlavink@redhat.com> - 661-1
- updated to 661(2294840)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 643-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 06 2024 Matej Mužila <mmuzila@redhat.com> - 643-4
- migrated to SPDX license

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 643-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 643-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 05 2023 Matej Mužila <mmuzila@redhat.com> - 643-1
- Update to new upstream release
- Resolves: #2231663

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 633-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 05 2023 Matej Mužila <mmuzila@redhat.com> - 633-1
- Update to new upstream release
- Resolves: CVE-2022-46663

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 608-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 24 2022 Matej Mužila <mmuzila@redhat.com> - 608-1
- Update to new upstream release

* Mon Jul 25 2022 Daan De Meyer <daan.j.demeyer@gmail.com> - 590-5
- Backport patch from upstream to fix memory leak

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 590-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 590-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Oct 02 2021 FeRD (Frank Dana) <ferdnyc@gmail.com> - 590-2
- Backport patch from upstream to fix hyperlinked text bug

* Tue Aug 10 2021 Matej Mužila <mmuzila@redhat.com> - 590-1
- Update to new upstream release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 581.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 6 2021 Filip Januš <fjanus@redhat.com> - 581.2-1
- Rebase to 581.2-1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 575-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Stephen Gallagher <sgallagh@redhat.com> - 575-1
- Update to latest version (#1919119)

* Mon Nov 30 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 568-1
- Update to latest version (#1818534)

* Thu Aug 20 2020 Andrew Schorr <ajschorr@fedoraproject.org> - 551-5
- Add zstd and brotli support to lesspipe.sh

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 551-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 551-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 551-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Matej Mužila <mmuzila@redhat.com> - 551-1
- Update to new upstream release
- Resolves: #1719419

* Tue Jun 04 2019 Matej Mužila <mmuzila@redhat.com> - 550-1
- Update to new upstream release
- Resolves: #1674080

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 530-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Pavel Raiskup <praiskup@redhat.com> - 530-3
- add lzip compression support into lesspipe.sh (rhbz#1664383)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 530-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Feb 17 2018 Pavel Raiskup <praiskup@redhat.com> - 530-1
- new release, per upstream release notes:
  http://greenwoodsoftware.com/less/news.530.html

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 487-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 487-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 487-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Pavel Raiskup <praiskup@redhat.com> - 487-3
- read correctly text files named accidentally '*.rpm' (rhbz#1449790)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 487-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 28 2016 Jozef Mlich <imlich@fit.vutbr.cz> - 487-1
- Resolves: rhbz#1389577
  Update to new upstream release

* Tue Oct 11 2016 Ville Skyttä <ville.skytta@iki.fi> - 481-6
- Prefer gpg2 over gpg for *.gpg (rhbz#1383284)

* Mon Apr 25 2016 Pavel Raiskup <praiskup@redhat.com> - 481-5
- again use the correct '||' syntax in LESSOPEN variable (rhbz#1254837)

* Wed Apr 20 2016 Pavel Raiskup <praiskup@redhat.com> - 481-4
- don't strictly require man-db or groff-base (rhbz#1278857)

* Tue Mar 29 2016 Pavel Raiskup <praiskup@redhat.com> - 481-3
- avoid one ubiquitous stat() call in less.sh and less.csh if possible
  (rhbz#1321591)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 481-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 2 2015 Viktor Jancik <vjancik@redhat.com> - 481-1
- Update to version 481, fixes #1231493

* Wed Sep 2 2015 Viktor Jancik <vjancik@redhat.com> - 479-3
- Added missing double quotes in profile.d scripts
- Corrected license information

* Mon Aug 24 2015 Viktor Jancik <vjancik@redhat.com> - 479-2
- Updated spec file to comply with current Fedora Packaging Guidelines
  Added missing documentation files
- Fixed less profile.d scripts
- Fixed preprocessing of man pages with special characters (#1241543)

* Tue Jul 07 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 479-1
- Update to 479 (#1240456)

* Wed Jun 24 2015 Jozef Mlich <jmlich@redhat.com> - 478-1
- update to 478
  http://greenwoodsoftware.com/less/news.478.html

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 471-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015 Jozef Mlich <jmlich@redhat.com> - 471-4
- update of previous patch

* Mon Jun 01 2015 Jozef Mlich <jmlich@redhat.com> - 471-3
- out of bounds read access in is_utf8_well_formed()
  Resolves: #1201310
  CVE-2014-9488

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 471-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Dec 17 2014 Jozef Mlich <jmlich@redhat.com> - 471-1
- Update to 471

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 458-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 458-12
- fix license handling

* Mon Jun 23 2014 Jozef Mlich <jmlich@redhat.com> - 458-11
- rollback of previous problem. See explanation of upstream.
  http://greenwoodsoftware.com/less/faq.html#profileout
- fixing exit status values (the $? should be used as soon
  as possible)

* Thu Jun 19 2014 Jozef Mlich <jmlich@redhat.com> - 458-10
- (lesspipe) better handling of exit status
  fixing regression of #186931 - turns over the lesspipe exit behavior

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 458-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Jozef Mlich <jmlich@redhat.com> - 458-8
- (lesspipe) the groff was used just in case of gzipped man pages
- (lesspipe) the exit $? should be used directly after command; 
  otherwise may return unexpected value.
- (lesspipe) not preprocessed output was returning 1

* Mon Mar 31 2014 Jozef Mlich <jmlich@redhat.com> - 458-7
- FIXES outdated ubin_table in charset.c; 
  Kudos to Akira TAGOH
  Resolves: #1074489

* Mon Feb 10 2014 Jozef Mlich <jmlich@redhat.com> - 458-6
- The data in less-458-old-bot-in-help.patch was not
  preprocessed by mkhelp (i.e. not applied)

* Mon Dec 02 2013 Jozef Mlich <jmlich@redhat.com> - 458-5
- Resolves #1036326 fixing command line parsing in lesskey
- changed day of week in order to avoid bogus date in changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 458-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Fridolin Pokorny <fpokorny@redhat.com> - 458-3
- Expanded lessecho usage (#948597)
- Added lessfilter info to man (#948597)
- Expanded lesskey usage (#948597)
- Added --old-bot to help (#948597)

* Thu Apr 11 2013 Fridolin Pokorny <fpokorny@redhat.com> - 458-2
- Added gpg support to lesspipe.sh (#885122)
- Added ~/.lessfilter support (#885122)

* Thu Apr 11 2013 Fridolin Pokorny <fpokorny@redhat.com> - 458-1
- Update to 458

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 451-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Martin Briza <mbriza@redhat.com> - 451-2
- Changed unnecessary groff dependency to groff-base (#868376)

* Tue Sep 11 2012 Martin Briza <mbriza@redhat.com> - 451-1
- Rebase to 451 (#835802)
- Removed the empty-lessopen-pipe patch as the issue is now fixed upstream.

* Mon May 14 2012 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-7
- Fix less.sh not to override user-defined LESSOPEN variable (#802757)
- Use POSIX regcomp instead of PCRE - revert 406-11, commit 4b961c7 (#643233)
- Merge Foption changes by Colin Guthrie to Foption.v2.patch (#805735)

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 444-6
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 444-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-4
- Avoid some unnecessary stat calls and commands in lesspipe.sh,
  patch by Ville Skyttä (#741440)
- Use `groff' instead of `man -s' for rendering manpages to prevent
  options incompatibility between man and man-db packages (#718498)
- Add groff to Requires

* Tue Aug 23 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-3
- Substitute %%makeinstall macro with make DESTDIR* install (#732557)

* Fri Aug 12 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-2
- Fix debuginfo source files permissions
- Remove strip after %%makeinstall to fix debuginfo package

* Thu Jul 14 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-1
- Rebase to 444 (#713406)

* Wed Apr 20 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 443-1
- Rebase to 443
- Foption patch made applicable against 443
- Manpage extra line patch removed; fixed upstream (#697451)

* Wed Apr 13 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-13
- Don't convert files with UTF-16/UTF-32 string in filename (#638312)

* Tue Feb 15 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-12
- Enable LESSOPEN exit statuses as default also in less.sh (#666084, #676057)

* Tue Feb 15 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-11
- Clean lesspipe.sh script
- Split case for compressed and plain troff files
- Add support for *.xz and *.lzma man pages (#676057)
- Add support for reading UTF-16 and UTF-32 files (#638312)
- Don't require correct exit status from LESSOPEN scripts until
  it gets accepted by upstream (preserve backward compatibility) (#666084, #676057)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 436-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 03 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-9
- Fix regression in lesspipe.sh script (*.gz files etc.) (#615303 comment #9)

* Wed Dec 22 2010 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-8
- The new "--old-bot" option is not documented in the man page (#510724)
- Fix descriptions of some options in online help
  (#578289, patch by Jeff Bastian <jbastian@redhat.com> [IT603793])

* Tue Dec 21 2010 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-7
- Fix for valid empty LESSOPEN pipe output (#579251, #615303)

* Wed Jan 20 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 436-6
- RFE: lesspipe.sh could use a support for *.xz file

* Mon Jan 4 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 436-5
- patched wrong manpage. Resolves: #537746.

* Sat Dec 12 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 436-4
- #546613 - RFE: add *.jar *.nbm to lesspipe.sh

* Wed Dec 9 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 436-3
- Resolves: #537746 - Two different descriptions about the default value of LESSBINFMT

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 436-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Zdenek Prikryl <zprikryl@redhat.com> - 436-1
- Foption patch is more optimal now
- Update to 436

* Tue Apr 14 2009 Zdenek Prikryl <zprikryl@redhat.com> - 429-1
- Update to 429

* Tue Mar 31 2009 Zdenek Prikryl <zprikryl@redhat.com> - 424-4
- Added GraphicsMagick support (#492695)

* Tue Mar 17 2009 Zdenek Prikryl <zprikryl@redhat.com> - 424-3
- Added lzma support
- Added test if fsync produces EIVAL on tty

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 424-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jun 25 2008 Zdenek Prikryl <zprikryl@redhat.com> - 424-1
- Update to 424

* Wed Jun 11 2008 Zdenek Prikryl <zprikryl@redhat.com> - 423-1
- Update to 423

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 418-3
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Zdenek Prikryl <zprikryl@redhat.com> - 418-2
- Fixed -F option
- Resolves: #427551

* Fri Jan 04 2008 Zdenek Prikryl <zprikryl@redhat.com> - 418-1
- Update to 418

* Fri Nov 23 2007 Zdenek Prikryl <zprikryl@redhat.com> - 416-1
- Update to 416
- Fixed SIGABORT caused by UTF-8 related bug
- Resolves #395591

* Wed Nov 21 2007 Zdenek Prikryl <zprikryl@redhat.com> - 415-1
- Update to 415

* Tue Nov 13 2007 Ivana Varekova <varekova@redhat.com> - 409-2
- remove which usage (#312591)

* Mon Oct 22 2007 Ivana Varekova <varekova@redhat.com> - 409-1
- upgrade to 409
- remove useless/obsolete patches
- add autoconf buildrequires

* Mon Oct  1 2007 Ivana Varekova <varekova@redhat.com> - 406-12
- change license tag
- fix 312591 - add which dependency

* Thu Aug  9 2007 Ivana Varekova <varekova@redhat.com> - 406-11
- configure a regular expression library

* Tue Jun 26 2007 Ivana Varekova <varekova@redhat.com> - 406-10
- update to 406

* Mon Jun  4 2007 Ivana Varekova <varekova@redhat.com> - 394-10
- Resolves: #242077
  remove "-" option from lesspipe.sh script

* Tue Feb 20 2007 Ivana Varekova <varekova@redhat.com> - 394-9
- change /etc/profile.d script's permissions

* Mon Feb 19 2007 Ivana Varekova <varekova@redhat.com> - 394-8
- change LICENSE permissions

* Wed Feb  7 2007 Ivana Varekova <varekova@redhat.com> - 394-7
- incorporate the package review

* Wed Nov 22 2006 Ivana Varekova <varekova@redhat.com> - 394-6
- fix permissions of debuginfo source code

* Wed Oct 25 2006 Ivana Varekova <varekova@redhat.com> - 394-5
- fix command ">" (#120916)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 394-4.1
- rebuild

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> - 394-4
- fix problem with unassigned variable DECOMPRESSOR (#190619)

* Wed Feb 15 2006 Ivana Varekova <varekova@redhat.com> - 394-3
- add patch for search problem (search did not find string which
  occurs in a line after '\0')

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 394-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 394-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 16 2006 Jindrich Novy <jnovy@redhat.com> 394-2
- apply better fix for #120916 from Avi Kivity (#177819)
  to avoid flickering when '>' is pressed multiple times

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Jindrich Novy <jnovy@redhat.com> 394-1
- update to less-394

* Mon Nov  7 2005 Jindrich Novy <jnovy@redhat.com> 393-1
- update to less-393
- groom Foption patch a bit
- remove obsolete ncursesw and utf8detect patches

* Fri Oct 21 2005 Jindrich Novy <jnovy@redhat.com> 392-2
- fix the -F option (#79650), thanks to Petr Raszyk

* Wed Oct 19 2005 Jindrich Novy <jnovy@redhat.com> 392-1
- update to less-392 - fixes #122847 and enhances UTF8 support

* Fri Sep  2 2005 Jindrich Novy <jnovy@redhat.com> 382-8
- fix displaying of bogus newline for growing files (#120916)

* Fri Mar  4 2005 Jindrich Novy <jnovy@redhat.com> 382-7
- rebuilt with gcc4

* Wed Feb 16 2005 Jindrich Novy <jnovy@redhat.com> 382-6
- add patch for proper detection of UTF-8 locale,
  patch from Peter Rockai

* Tue Nov 16 2004 Karsten Hopp <karsten@redhat.de> 382-5 
- minor fix in lesspipe.sh (#73215)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar 29 2004 Karsten Hopp <karsten@redhat.de> 382-3
- remove old stuff from /etc/profile.d/less.*, fixes #109011

* Tue Mar 02 2004 Karsten Hopp <karsten@redhat.de> 382-1.1 
- build for FC1

* Sat Feb 14 2004 Karsten Hopp <karsten@redhat.de> 382-1
- new upstream version

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 15 2004 Karsten Hopp <karsten@redhat.de> 381-2 
- drop iso247 patch, doesn't work

* Wed Jun 11 2003 Karsten Hopp <karsten@redhat.de> 381-1
- new version with rewritten iso247 patch

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix korean #79977
- add new less.sh from #89780, s/ko/korean/ and write .csh script
- add patch from #91661: /japanses/japanese-euc/

* Tue Feb  4 2003 Tim Waugh <twaugh@redhat.com> 378-7
- Part of multibyte patch was missing; fixed.

* Mon Feb  3 2003 Tim Waugh <twaugh@redhat.com> 378-6
- Fix underlining multibyte characters (bug #83377).

* Thu Jan 30 2003 Karsten Hopp <karsten@redhat.de> 378-5
- removed older, unused patches
- add patch from Yukihiro Nakai to fix display of japanese text
  (#79977)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 18 2002 Karsten Hopp <karsten@redhat.de>č
- removed default 'cat' from lesspipe.sh as it breaks 'v' and 'F' keys 
  (#79921)

* Fri Dec  6 2002 Nalin Dahyabhai <nalin@redhat.com> 378-2
- add a default case to lesspipe so that it shows other kinds of files

* Mon Nov 04 2002 Karsten Hopp <karsten@redhat.de>
- less-378
- added some debian patches
- show image info instead of binary garbage when viewing images

* Fri Oct 05 2001 Karsten Hopp <karsten@redhat.de>
- fix line numbering (less -N filename), caused by
  a broken i18n patch

* Tue Sep 04 2001 Karsten Hopp <karsten@redhat.de>
- recompile with large file support (#52945)

* Tue Jul 24 2001 Karsten Hopp <karsten@redhat.de>
- fix #49506 (BuildRequires)

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- fixup eline patch to initialize result correctly

* Mon Jun 25 2001 Karsten Hopp <karsten@redhat.de>
- update URLs
- Copyright -> License
- fix #43348 (crashes when searching for /<)
- fix #39849 (
  _ ignores LESSCHARDEF in displaying characters,
  _ prefaces sequences of one or "high" characters with a capital "A")

* Mon Feb  5 2001 Yukihiro Nakai <ynakai@redhat.com>
- Update less.sh, less.csh to set JLESSCHARSET=japanese
  when LANG=ja??

* Mon Feb  5 2001 Matt Wilson <msw@redhat.com>
- changed the less-358+iso247-20001210.diff patch to use strcasecmp when
  comparing locale names

* Thu Feb 01 2001 Karsten Hopp <karsten@redhat.de>
- fixed character translations (bugzilla #24463)

* Wed Jan 31 2001 Karsten Hopp <karsten@redhat.de>
- fixed lesspipe (bugzilla #17456 #25324)

* Tue Dec 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with new ncurses

* Mon Dec 11 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese patch with ia64 support.

* Mon Nov 27 2000 Karsten Hopp <karsten@redhat.de>
- rebuild with new ncurses
- fix Bug #21288

* Mon Nov 13 2000 Karsten Hopp <karsten@redhat.de>
- fixed handling of manpages of type *.1x.gz
- added support for cpio packages

* Thu Sep 14 2000 Than Ngo <than@redhat.com>
- added new lesspipe.sh (Bug #17456)

* Wed Aug 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- support files with spaces in their names (Bug #16777)

* Tue Aug  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Support gzipped man pages in lesspipe.sh (Bug #15610)

* Thu Aug  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Tweak init script (Bug #14622)

* Thu Jul 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Oops, actually apply the patch for 9443. ;)

* Wed Jul 26 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up messed output if a user outputs anything in ~/.bashrc or the
  likes (Bug #9443)
- handle RPM_OPT_FLAGS

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 358

* Mon Jun 26 2000 Matt Wilson <msw@redhat.com>
- defattr root

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Fri Apr 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 354

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to v352

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Tue Jan 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to v346
- Update download URL
- use the configure marcro
- strip binary
- fix up lesspipe stuff (Bug #8750 and a couple of non-reported bugs)
  (Karsten, did I mention I'll kill you when you return from SAP? ;) )

* Fri Jan 7 2000 Karsten Hopp <karsten@redhat.de>
- added lesspipe.sh to show listings of package
  contents instead of binary output.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- less finally gets maintenance, upgraded to 340

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Tue Mar 16 1999 Preston Brown <pbrown@redhat.com>
- removed ifarch axp stuff for /bin/more, more now works on alpha properly.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Thu May 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 332 and built for Manhattan
- added buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
