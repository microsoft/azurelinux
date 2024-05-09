Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%define		perl_vendorarch	%(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

Summary:	Modular text mode IRC client with Perl scripting
Name:		irssi
Version:	1.2.2
Release:	6%{?dist}

License:	GPLv2+
URL:		https://irssi.org/
Source0:	https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
Source1:	irssi-config.h
BuildRequires:	ncurses-devel openssl-devel zlib-devel
BuildRequires:	pkgconfig glib2-devel perl-devel perl-generators perl(ExtUtils::Embed)
BuildRequires:	autoconf automake libtool utf8proc-devel libotr-devel
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# rhbz#1773190
Obsoletes:	irc-otr
# https://github.com/irssi/irssi/pull/1183
Patch0:		irssi-1.2.2-ctrl-space-fix.patch

%package devel
Summary:	Development package for irssi
Requires:	%{name} = %{version}-%{release}

%description
Irssi is a modular IRC client with Perl scripting. Only text-mode
frontend is currently supported. The GTK/GNOME frontend is no longer
being maintained.

%description devel
This package contains headers needed to develop irssi plugins.

Irssi is a modular IRC client with Perl scripting. Only text-mode
frontend is currently supported. The GTK/GNOME frontend is no longer
being maintained.


%prep
%setup -q
%patch 0 -p1 -b .ctrl-space-fix


%build
autoreconf -i
%configure --with-textui		\
	--with-proxy			\
	--with-bot			\
	--with-perl=yes			\
	--with-perl-lib=vendor		\
	--enable-true-color		\
	--with-otr=yes

make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
mv irssi-config.h irssi-config-$(getconf LONG_BIT).h
cp -p %{SOURCE1} irssi-config.h


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PERL_INSTALL_ROOT=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
install -p irssi-config-$(getconf LONG_BIT).h $RPM_BUILD_ROOT%{_includedir}/%{name}/irssi-config-$(getconf LONG_BIT).h

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/modules/lib*.*a
rm -Rf $RPM_BUILD_ROOT/%{_docdir}/%{name}
find $RPM_BUILD_ROOT%{perl_vendorarch} -type f -a -name '*.bs' -a -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{perl_vendorarch} -type f -a -name .packlist -exec rm {} ';'
chmod -R u+w $RPM_BUILD_ROOT%{perl_vendorarch}




%files
%doc docs/*.txt docs/*.html AUTHORS COPYING NEWS README.md TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/botti
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/%{name}.1*
%{perl_vendorarch}/Irssi*
%{perl_vendorarch}/auto/Irssi


%files devel
%{_includedir}/irssi/


%changelog
* Thu Jul  8 2021 Muhammad Falak R Wani <mwani@microsoft.com> - 1.2.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Fix Patch directive `Patch -> Patch0`

* Wed Jul  8 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.2-5
- Fixed ctrl+space problem
  Resolves: rhbz#1854822

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.2-4
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.2-2
- Obsoleted irc-otr
  Resolves: rhbz#1773190

* Fri Aug 30 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.2-1
- New version
  Resolves: rhbz#1640348
  Resolves: CVE-2019-15717

* Mon Jul 29 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.1-1
- New version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.2-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 1.1.2-1
- New version
  Resolves: CVE-2019-5882
- Dropped coverity-scan-fix patch (upstreamed)

* Thu Dec  6 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1.1.1-6
- Renamed patch fixing issue found by coverity scan

* Tue Dec  4 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1.1.1-5
- Updated patch fixing issues found by coverity scan

* Tue Dec  4 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1.1.1-4
- Fixed some issues found by coverity scan

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.1-2
- Perl 5.28 rebuild

* Fri Feb 16 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1.1.1-1
- New version
  Resolves: rhbz#1534795

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.6-2
- Rebuilt for switch to libxcrypt

* Mon Jan  8 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.6-1
- New version
  Resolves: rhbz#1531973

* Mon Oct 23 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.5-1
- New version
  Resolves: rhbz#1505182

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.4-1
- New version
  Resolves: rhbz#1468785
  Resolves: CVE-2017-10965
  Resolves: CVE-2017-10966
- Dropped allow-negative-values-in-settings patch (not needed)

* Tue Jun 27 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.3-1
- New version
  Resolves: rhbz#1459539
  Resolves: CVE-2017-9468
  Resolves: CVE-2017-9469

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.2-2
- Perl 5.26 rebuild

* Mon Mar 13 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.2-1
- New version
  Resolves: rhbz#1431388

* Mon Feb  6 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.1-1
- New version
  Resolves: rhbz#1419372

* Thu Jan 19 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.0-1
- New version
  Resolves: rhbz#1410770

* Thu Jan 19 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.21-1
- New version
  Resolves: CVE-2017-5193
  Resolves: CVE-2017-5194
  Resolves: CVE-2017-5195
  Resolves: CVE-2017-5196
  Resolves: CVE-2017-5356
- Dropped CVE-2016-7553 patch (upstreamed)

* Mon Sep 26 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.20-2
- Fixed buf.pl not to disclosure information through the filesystem
  Resolves: CVE-2016-7553

* Thu Sep 22 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.20-1
- New version
  Resolves: rhbz#1378261
  Resolves: CVE-2016-7044
  Resolves: CVE-2016-7045

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.19-2
- Perl 5.24 rebuild

* Tue Mar 29 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.19-1
- New version
  Resolves: rhbz#1316054
- New download URL, switched to XZ compressed sources

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.17-3
- Perl 5.22 rebuild

* Thu Apr 09 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.8.17-2
- Enable 24bit colour support

* Mon Oct 13 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.17-1
- New version
  Resolves: rhbz#1152060
- Dropped no-static-unload and man-fix patches (both upstreamed)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.16-3
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.16-1
- New version
  Resolves: rhbz#1107342
- Dropped format-security patch (not needed)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-0.4.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.16-0.3.rc1
- Fixed change log

* Wed Dec  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.16-0.2.rc1
- Fixed compilation with -Werror=format-security
  Resolves: rhbz#1037139

* Mon Sep 16 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.16-0.1.rc1
- New version
- Dropped init-resize-crash-fix (upstreamed)
- Fixed bogus date in changelog (best effort)
- Disabled unloading static modules (by no-static-unload patch)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.8.15-14
- Perl 5.18 rebuild

* Mon Mar 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-13
- Added support for aarch64
  Resolves: rhbz#925598

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug  3 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-11
- Removed usage parameter from the man page (popt leftover)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 0.8.15-9
- Perl 5.16 rebuild

* Fri Feb 24 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-8
- Fixed crash that can occur if term is resized during irssi init
  (init-resize-crash-fix patch)
  Resolves: rhbz#796457

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.8.15-6
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.8.15-5
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8.15-3
- Mass rebuild with perl-5.12.0

* Mon May 31 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-2
- Rebuilt with -fno-strict-aliasing

* Tue Apr 13 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-1
- Update to new version: irssi-0.8.15

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.8.14-4
- rebuild against perl 5.10.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.8.14-3
- rebuilt with new openssl

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.8.14-2
- Use bzipped upstream tarball.

* Mon Aug  3 2009 Marek Mahut <mmahut@fedoraproject.org> - 0.8.14-1
- Upstream release 0.8.14

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.8.13-2
- Resolve CVE-2009-1959

* Fri May  1 2009 Marek Mahut <mmahut@fedoraproject.org> - 0.8.13-1
- Upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.8.12-12
- rebuild with new openssl

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.12-11
- Don't include any C header files in main package.

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.12-10
- BR: perl(ExtUtils::Embed)

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.12-9
- Rebuild for new perl

* Sat Mar  1 2008 Marek Mahut <mmahut@fedoraproject.org> - 0.8.12-8
- Fix for multiarch conflict (BZ#341591)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.12-5
- Autorebuild for GCC 4.3

* Sun Nov 11 2007 Marek Mahut <mmahut fedoraproject.org> - 0.8.12-3
- Enabling perl build-in support as per request in BZ#375121

* Mon Oct 08 2007 Marek Mahut <mmahut fedoraproject.org> - 0.8.12-1
- New release
- Fixes bug from BZ#239511, dropping patch

* Sun Aug 19 2007 Marek Mahut <mmahut fedoraproject.org> - 0.8.11-5
- Fixing properly irssi-support-meta-cursor-xterm.patch

* Thu Aug 16 2007 Marek Mahut <mmahut redhat.com> - 0.8.11-4
- Added irssi-support-meta-cursor-xterm.patch (BZ#239511)

* Thu Aug 16 2007 Marek Mahut <mmahut redhat.com> - 0.8.11-2
- Updating license tag
- Rebuild for 0.8.11

* Wed May  2 2007 Dams <anvil[AT]livna.org> - 0.8.11-1
- Updated to 0.8.11
- Dropped patch0

* Sat Apr 21 2007 Dams <anvil[AT]livna.org> - 0.8.10-7.a
- Release bump

* Sun Sep 17 2006 Dams <anvil[AT]livna.org> - 0.8.10-6.a
- Bumped release 

* Sun Sep 17 2006 Dams <anvil[AT]livna.org> - 0.8.10-5.a
- Updated to 0.8.10a
- Fixed tarball name..
- Updated Patch0 still from Saleem

* Wed Mar 15 2006 Dams <anvil[AT]livna.org> - 0.8.10-4
- Added patch from Saleem Abdulrasool to fix invalid pointer.

* Sat Jan 28 2006 Dams <anvil[AT]livna.org> - 0.8.10-3
- Fixed changelog -_-

* Sat Jan 28 2006 Dams <anvil[AT]livna.org> - 0.8.10-2
- Disabled gc support

* Sun Dec 11 2005 Dams <anvil[AT]livna.org> - 0.8.10-1
- Updated to final 0.8.10

* Wed Dec  7 2005 Dams <anvil[AT]livna.org> - 0.8.10-0.2.rc8
- Updated to rc8

* Tue Nov 15 2005 Dams <anvil[AT]livna.org> - 0.8.10-0.1.rc7
- Dropped patch 2 (seems applied upstream) and 3 (no longer needed)
- Removed conditionnal build against glib1 parts

* Sun Nov 13 2005 Luke Macken <lmacken@redhat.com> 0.8.9-8
- Rebuild against new openssl

* Mon Apr 11 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.8.9-7
- Two patches to fix build for GCC4 and new Perl with config.h.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Dec 24 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.8.9-5
- Reduce Perl dir ownership and add MODULE_COMPAT dependency.

* Fri Apr  2 2004 Dams <anvil[AT]livna.org> 0:0.8.9-0.fdr.4
- Rebuilt to use new perl to prevent random segmentation fault at load
  time

* Fri Feb  6 2004 Dams <anvil[AT]livna.org> 0:0.8.9-0.fdr.3
- Patch from Michael Schwendt to fix convert-replace-trigger script
  (bug #1120 comment #3)

* Sat Dec 20 2003 Dams <anvil[AT]livna.org> 0:0.8.9-0.fdr.2
- Fixed changelog typo
- Added trigger.pl as replace.pl wont be maintained anymore
- Updated replace.pl to 0.1.4 version
- Added replace.pl URL in Source tag
- Removed .packlist files
- Added as doc a script to convert pref from replace.pl to trigger.pl

* Thu Dec 11 2003 Dams <anvil[AT]livna.org> 0:0.8.9-0.fdr.1
- Updated to 0.8.9

* Mon Nov 24 2003 Dams <anvil[AT]livna.org> 0:0.8.8-0.fdr.1
- Updated to 0.8.8
- Enabled gc

* Sun Sep 14 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.13
- Rebuild

* Sun Sep 14 2003 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.8.6-0.fdr.12
- apply openssl patch only if openssl-devel supports pkgconfig

* Thu Sep 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.11
- Installing replace.pl in good directory

* Thu Sep 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.10
- Rebuild

* Thu Sep 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.9
- Using vendor perl directories

* Thu Sep 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.8
- Added missing unowned directories
- Added an additionnal useful perl script (replace.pl)

* Tue Aug  5 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.7
- Added zlib-devel buildrequires

* Sat Jul 12 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.6
- Applied Patches from Ville Skyttä (bug #277 comment #11 and
  comment #12)

* Mon Jun 23 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.5
- Modified BuildRequires for ssl

* Wed Jun 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.4
- Added another dir entry

* Sun Jun  8 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.3
- Added some dir entry in file section

* Tue May 20 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.2
- Exclude modules ".a" files
- Include more files as doc

* Sat May 10 2003 Dams <anvil[AT]livna.org>
- Initial build.
