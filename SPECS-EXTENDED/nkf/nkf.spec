Name:		nkf
Version:	2.1.4
Release:	18%{?dist}
License:	BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://nkf.osdn.jp/
Source0:	https://iij.dl.osdn.jp/nkf/64158/%{name}-%{version}.tar.gz
## snippet from the source code
Source3:	nkf.copyright
Source4:	nkf.1j
Patch0:		%{name}-fix-man.patch
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	gcc

Summary:	A Kanji code conversion filter

%description
Nkf is a Kanji code converter for terminals, hosts, and networks. Nkf
converts input Kanji code to 7-bit JIS, MS-kanji (shifted-JIS) or
EUC.

%package -n perl-NKF
Summary:	Perl extension for Network Kanji Filter
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-NKF
This is a Perl Extension version of nkf (Network Kanji Filter).
It converts the last argument and return converted result.
Conversion details are specified by flags before the last argument.

%prep
%autosetup -p1
cp -p %{SOURCE4} .

%build
make CFLAGS="$RPM_OPT_FLAGS" nkf
cp -p %{SOURCE3} .
pushd NKF.mod
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL PREFIX=%{_prefix} INSTALLDIRS=vendor
make %{?_smp_mflags}
popd

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/{man1,ja/man1}

./nkf -e nkf.1j > nkf.1jeuc
iconv -f euc-jp -t utf-8 nkf.1jeuc > nkf.1utf8
touch -r nkf.1j nkf.1utf8
install -m 755 -p nkf $RPM_BUILD_ROOT%{_bindir}
install -m 644 -p nkf.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 -p nkf.1utf8 $RPM_BUILD_ROOT%{_mandir}/ja/man1/nkf.1
pushd NKF.mod
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="/usr/bin/install -p"
rm -f	$RPM_BUILD_ROOT%{perl_vendorarch}/perllocal.pod		\
	$RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod		\
	$RPM_BUILD_ROOT%{perl_vendorarch}/auto/NKF/NKF.bs	\
	$RPM_BUILD_ROOT%{perl_vendorarch}/auto/NKF/.packlist
popd
chmod 0755 $RPM_BUILD_ROOT%{perl_vendorarch}/auto/NKF/NKF.so


%check
make test

%files
%doc nkf.doc
%license nkf.copyright
%{_bindir}/nkf
%{_mandir}/man1/nkf.1*
%{_mandir}/ja/man1/nkf.1*

%files -n perl-NKF
%doc nkf.doc
%license nkf.copyright
%{perl_vendorarch}/NKF.pm
%{perl_vendorarch}/auto/*
%{_mandir}/man3/NKF.3pm.gz

%changelog
* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 2.1.4-18
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.1.4-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.1.4-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.1.4-11
- Perl 5.28 rebuild

* Mon Feb 19 2018 Akira TAGOH <tagoh@redhat.com> - 1:2.1.4-10
- Add BR: gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Akira TAGOH <tagoh@redhat.com> - 1:2.1.4-8
- Fix manpage (#1539528)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.1.4-5
- Perl 5.26 rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.1.4-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 16 2015 Akira TAGOH <tagoh@redhat.com> - 1:2.1.4-1
- New upstream release. (#129029)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.1.3-6
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.1.3-5
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 Akira TAGOH <tagoh@redhat.com> - 1:2.1.3-2
- Fix the broken nkf man page. (#1039359)

* Tue Nov 26 2013 Akira TAGOH <tagoh@redhat.com> - 1:2.1.3-1
- New upstream release. (#1034089)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:2.1.2-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Akira TAGOH <tagoh@redhat.com> - 1:2.1.2-6
- Add %%check.

* Thu Nov 22 2012 Akira TAGOH <tagoh@redhat.com> - 1:2.1.2-5
- the spec file cleanup.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:2.1.2-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep  9 2011 Akira TAGOH <tagoh@redhat.com> - 1:2.1.2-1
- New upstream release. (#737004)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1:2.1.1-4
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1:2.1.1-3
- Perl mass rebuild

* Tue Jun 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:2.1.1-2
- Perl mass rebuild

* Wed Mar 16 2011 Akira TAGOH <tagoh@redhat.com> - 1:2.1.1-1
- New upstream release.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.8b-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:2.0.8b-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:2.0.8b-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.8b-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.8b-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 Akira TAGOH <tagoh@redhat.com> - 1:2.0.8b-4
- Fix a source URL.

* Tue Jul  1 2008 Akira TAGOH <tagoh@redhat.com> - 1:2.0.8b-3
- Add perl(:MODULE_COMPAT_...) deps. (#453413)

* Tue Feb 12 2008 Akira TAGOH <tagoh@redhat.com> - 1:2.0.8b-2
- Rebuild for gcc-4.3.

* Fri Sep 21 2007 Akira TAGOH <tagoh@redhat.com> - 1:2.0.8b-1
- New upstream release.
- clean up the spec file.

* Thu Aug 23 2007 Akira TAGOH <tagoh@redhat.com> - 2.07-3
- Rebuild

* Fri Aug 10 2007 Akira TAGOH <tagoh@redhat.com> - 2.07-2
- Update License tag.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.07-1.1
- rebuild

* Thu Jul  6 2006 Akira TAGOH <tagoh@redhat.com> - 2.07-1
- New upstream release.
- use dist tag.
- clean up the spec file.

* Thu Mar 30 2006 Akira TAGOH <tagoh@redhat.com> - 2.06-1
- New upstream release.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.05-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.05-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Jul  7 2005 Akira TAGOH <tagoh@redhat.com> - 2.05-1
- New upstream release.

* Thu Mar 17 2005 Akira TAGOH <tagoh@redhat.com> - 2.04-5
- rebuilt

* Thu Feb 10 2005 Akira TAGOH <tagoh@redhat.com> - 2.04-4
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 07 2004 Akira TAGOH <tagoh@redhat.com> 2.04-1
- New upstream release.

* Tue Sep 30 2003 Akira TAGOH <tagoh@redhat.com> 2.03-1
- New upstream release.
- converted Japanese nkf.1 to UTF-8. (#105762)
- nkf-1.92-glibc2290.diff: removed.

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com> 2.02-4
- Fix unpackaged files

* Fri Jun 27 2003 Akira TAGOH <tagoh@redhat.com> 2.02-3
- had perl-NKF as separated package.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 09 2003 Akira TAGOH <tagoh@redhat.com> 2.02-1
- New upstream release.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 10 2003 Akira TAGOH <tagoh@redhat.com> 2.01-1
- New upstream release.
  it contains UTF-8 support.

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebbuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Akira TAGOH <tagoh@redhat.com> 1.92-10
- fix the stripped binary.
- s/Copyright/License/

* Mon Jun 03 2002 Yukihiro Nakai <ynakai@redhat.com>
- Add output bug patch for glibc-2.2.90 (#65864)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Sep  4 2001 SATO Satoru <ssato@redhat.com> - 1.92-6
- attached nkf.1jeuc(euc-jp) instead of nkf.1j(iso-2022-jp) (#53127)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Feb 28 2001 SATO Satoru <ssato@redhat.com>
- nkf.copyright attached
- use system-defined macros (%%*dir)

* Tue Aug 29 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- adopt FHS

* Mon Aug  7 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- japanese manpages moved ja_JP.eucJP -> ja
- modified to be able to build by normal user.

* Tue Aug 01 2000 Yukihiro Nakai <ynakai@redhat.com>
- Update to 1.92
- rebuild for 7.0J

* Sat Mar 25 2000 Matt Wilson <msw@redhat.com>
- rebuilt for 6.2j
- support compressed man pages

* Wed Mar 22 2000 Chris Ding <cding@redhat.com>
- ja_JP.ujis -> ja_JP.eucJP

* Thu Oct  7 1999 Matt Wilson <msw@redhat.com>
- rebuilt against 6.1

* Sun May 30 1999 FURUSAWA,Kazuhisa <kazu@linux.or.jp>
- 1st Release for i386 (glibc2.1).
- Original Packager: Kazuhiko Mori(COW) <cow@he.mirai.ne.jp>

* Sun Jan 10 1999 Kazuhiko Mori(COW) <cow@he.mirai.ne.jp>
- just rebuilt for glibc TL. (release not changed.)

