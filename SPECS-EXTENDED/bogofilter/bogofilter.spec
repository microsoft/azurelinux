Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Fast anti-spam filtering by Bayesian statistical analysis
Name: bogofilter
Version: 1.2.5
Release: 3%{?dist}
License: GPLv2
URL: https://bogofilter.sourceforge.net/
Source0: https://downloads.sourceforge.net/bogofilter/bogofilter-%{version}.tar.xz
BuildRequires: gcc
BuildRequires: flex libdb-devel gsl-devel
BuildRequires: /usr/bin/iconv
BuildRequires: perl-generators

%description
Bogofilter is a Bayesian spam filter.  In its normal mode of
operation, it takes an email message or other text on standard input,
does a statistical check against lists of "good" and "bad" words, and
returns a status code indicating whether or not the message is spam.
Bogofilter is designed with fast algorithms (including Berkeley DB system),
coded directly in C, and tuned for speed, so it can be used for production
by sites that process a lot of mail.

%package bogoupgrade
Summary: Upgrades bogofilter database to current version
Requires: %{name} = %{version}-%{release}

%description bogoupgrade
bogoupgrade is a command to upgrade bogofilter’s databases from an old
format to the current format. Since the format of the database changes
once in a while, the utility is designed to make the upgrade easy.

bogoupgrade is in an extra package to remove the perl dependency on the
main bogofilter package.

%prep
%setup -q
iconv -f iso-8859-1 -t utf-8 \
 doc/bogofilter-faq-fr.html > doc/bogofilter-faq-fr.html.utf8
%{__mv} -f doc/bogofilter-faq-fr.html.utf8 \
 doc/bogofilter-faq-fr.html

%build
%configure --disable-rpath
%{__make} %{?_smp_mflags}

%install
%{__make} DESTDIR=%{buildroot} install

%{__mv} -f %{buildroot}%{_sysconfdir}/bogofilter.cf.example \
 %{buildroot}%{_sysconfdir}/bogofilter.cf

%{__install} -d -m0755 rpm-doc/xml/ rpm-doc/html/
%{__install} -m644 doc/*.xml rpm-doc/xml/
%{__install} -m644 doc/*.html rpm-doc/html/

%{__chmod} -x contrib/*

%check
%{__make} %{?_smp_mflags} check

%files bogoupgrade
%{_bindir}/bogoupgrade
%{_mandir}/man1/bogoupgrade*

%files
%doc AUTHORS COPYING NEWS README* RELEASE.NOTES* TODO bogofilter.cf.example
%doc doc/bogofilter-SA* doc/bogofilter-tuning.HOWTO* doc/integrating* doc/programmer/
%doc rpm-doc/html/ rpm-doc/xml/ contrib
%{_mandir}/man1/bogo*.1*
%{_mandir}/man1/bf_*.1*
%config(noreplace) %{_sysconfdir}/bogofilter.cf
%{_bindir}/bogo*
%{_bindir}/bf_*
%exclude %{_bindir}/bogoupgrade
%exclude %{_mandir}/man1/bogoupgrade*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.5-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Adrian Reber <adrian@lisas.de> - 1.2.5-1
- Updated to 1.2.5
- No longer necessary to re-package sources: All problematic files have
  been re-licensed
- All 19 patches are part of the 1.2.5 release and have been removed

* Tue Aug 20 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.2.4-18
- Rebuilt for GSL 2.6.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 13 2019 Adrian Reber <adrian@lisas.de> - 1.2.4-16
- Applied 11 patches from Georg Sauthoff (#1676460)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 16 2017 Marek Kasik <mkasik@redhat.com> - 1.2.4-12
- Enable unit tests
- Resolves: #1502678

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Adrian Reber <adrian@lisas.de> - 1.2.4-9
- Rebuild for gsl 2.4 (#1474397)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 22 2016 Adrian Reber <adrian@lisas.de> - 1.2.4-7
- Added multiple upstream patches to fix various memory bugs
- Fixes "[abrt] bogofilter: yyrealloc(): bogofilter killed by SIGABRT" (#1246282)
- Fixes "why libdb4" (#1367329) by switching BR to libdb-devel (from db4-devel)

* Mon Feb 22 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.4-6
- Rebuild for gsl 2.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Adrian Reber <adrian@lisas.de> - 1.2.4-1
- updated to 1.2.4 (fixes #1084359)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.2.3-4
- Perl 5.18 rebuild

* Fri Feb 22 2013 Adrian Reber <adrian@lisas.de> - 1.2.3-2
- removed three files with an unfree license from Source (fixes #912694)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Adrian Reber <adrian@lisas.de> - 1.2.3-1
- updated to 1.2.3 (fixes #883358, CVE-2012-5468)

* Thu Jul 26 2012 Adrian Reber <adrian@lisas.de> - 1.2.2-5
- add new libdb4 include path to configure options

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 16 2010 Adrian Reber <adrian@lisas.de> - 1.2.2-1
- updated to 1.2.2 (fixes #611511, CVE-2010-2494)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Adrian Reber <adrian@lisas.de> - 1.2.0-1
- updated to 1.2.0

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.7-2
- rebuild against db4-4.7
- use make DESTDIR install
- disable rpaths

* Sat May 31 2008 Adrian Reber <adrian@lisas.de> - 1.1.7-1
- updated to 1.1.7
- moved bogoupgrade to its own package to remove the perl
  dependency on bogofilter (bz #442843)

* Thu Feb 14 2008 Adrian Reber <adrian@lisas.de> - 1.1.6-2
- rebuilt for gcc43

* Thu Dec 13 2007 Adrian Reber <adrian@lisas.de> - 1.1.6-1
- updated to 1.1.6
- made rpmlint happy
- upstream confirmed that bogofilter is GPLv2

* Thu Aug 23 2007 Adrian Reber <adrian@lisas.de> - 1.1.5-2
- rebuilt
- added patch to build with new glibc

* Wed Mar 07 2007 Adrian Reber <adrian@lisas.de> - 1.1.5-1
- updated to 1.1.5

* Tue Sep 05 2006 Adrian Reber <adrian@lisas.de> - 1.0.3-1
- updated to 1.0.3

* Wed Apr 19 2006 Adrian Reber <adrian@lisas.de> - 1.0.2-1
- updated to 1.0.2

* Mon Jan 02 2006 Dries Verachtert <dries@ulyssis.org> - 1.0.1-1 - 3875/dries
- Updated to release 1.0.1.

* Fri Dec 02 2005 Dag Wieers <dag@wieers.com> - 1.0.0-1
- Updated to release 1.0.0.

* Tue Nov 22 2005 Dries Verachtert <dries@ulyssis.org> - 0.96.6-1
- Updated to release 0.96.6.

* Mon Aug 02 2004 Dag Wieers <dag@wieers.com> - 0.92.4-1
- Updated to release 0.92.4.

* Sat Apr 10 2004 Dag Wieers <dag@wieers.com> - 0.17.5-1
- Updated to release 0.17.5.

* Mon Jan 26 2004 Dag Wieers <dag@wieers.com> - 0.16.4-0
- Initial package. (using DAR)
