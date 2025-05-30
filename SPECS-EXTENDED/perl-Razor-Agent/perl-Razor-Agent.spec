Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Filter the Perl extension module
%{?perl_default_filter}

%global pkgname Razor2-Client-Agent

Summary:        Collaborative, content-based spam filtering network agent
Name:           perl-Razor-Agent
Version:        2.86
Release:        13%{?dist}
License:        Artistic-2.0
URL:            https://metacpan.org/release/%{pkgname}
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/%{pkgname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         https://github.com/toddr/Razor2-Client-Agent/commit/033b00e94741550ef3ef087d9903742ac881a7ba.patch#/perl-Razor-Agent-2.86-parallel-make.patch
Patch1:         https://github.com/toddr/Razor2-Client-Agent/commit/1a8dc0ea64c6bbe187babdb1079bc0cf05926e59.patch#/perl-Razor-Agent-2.86-digest-sha.patch
Requires:       perl(Digest::SHA)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Config)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(vars)
Provides:       perl-%{pkgname} = %{version}-%{release}
Provides:       perl-%{pkgname}%{?_isa} = %{version}-%{release}

%description
Vipul's Razor is a distributed, collaborative, spam detection and
filtering network. Razor establishes a distributed and constantly
updating catalogue of spam in propagation. This catalogue is used
by clients to filter out known spam. On receiving a spam, a Razor
Reporting Agent (run by an end-user or a troll box) calculates
and submits a 20-character unique identification of the spam (a
SHA Digest) to its closest Razor Catalogue Server. The Catalogue
Server echos this signature to other trusted servers after storing
it in its database. Prior to manual processing or transport-level
reception, Razor Filtering Agents (end-users and MTAs) check their
incoming mail against a Catalogue Server and filter out or deny
transport in case of a signature match. Catalogued spam, once
identified and reported by a Reporting Agent, can be blocked out
by the rest of the Filtering Agents on the network.

%prep
%setup -q -n %{pkgname}-%{version}
%patch -P0 -p1
%patch -P1 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
%make_build

%install
%make_install
%if 0%{?rhel} && 0%{?rhel} <= 7
find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
%endif
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%license LICENSE
%doc BUGS Changes CREDITS FAQ README.md SERVICE_POLICY
%{_bindir}/razor-admin
%{_bindir}/razor-check
%{_bindir}/razor-client
%{_bindir}/razor-report
%{_bindir}/razor-revoke
%{perl_vendorarch}/Razor2/
%{perl_vendorarch}/auto/Razor2/
%{_mandir}/man1/razor-admin.1*
%{_mandir}/man1/razor-check.1*
%{_mandir}/man1/razor-report.1*
%{_mandir}/man1/razor-revoke.1*
%{_mandir}/man3/Razor2::Errorhandler.3pm*
%{_mandir}/man3/Razor2::Preproc::deHTMLxs.3pm*
%{_mandir}/man3/Razor2::Syslog.3pm*
%{_mandir}/man5/razor-agent.conf.5*
%{_mandir}/man5/razor-agents.5*
%{_mandir}/man5/razor-whitelist.5*

%changelog
* Fri Dec 20 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 2.86-13
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.86-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.86-11
- Perl 5.40 rebuild

* Sat Apr 20 2024 Miroslav Suchý <msuchy@redhat.com> - 2.86-10
- convert license to SPDX

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.86-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.86-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.86-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.86-6
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.86-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.86-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.86-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Robert Scheck <robert@fedoraproject.org> 2.86-1
- Upgrade to 2.86 (#1584474, #2030889)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-41
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 2.85-38
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-37
- Perl 5.32 rebuild

* Tue Mar 17 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-36
- Specify all build dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-33
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-30
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-26
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Robert Scheck <robert@fedoraproject.org> 2.85-24
- Added patch to unbreak parallel make (#1379566)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-23
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Robert Scheck <robert@fedoraproject.org> 2.85-21
- Correct installation place of man pages (#1297257)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-19
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-18
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 2.85-14
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2.85-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.85-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.85-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.85-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.85-5
- rebuild against perl 5.10.1

* Sun Nov 01 2009 Warren Togami <wtogami@redhat.com> - 2.85-4
- Use Digest::SHA instead of Digest::SHA1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 2.85-2
- Rebuilt against gcc 4.4 and rpm 4.6

* Wed Jul 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.85-1
- update to 2.85, relicensed to Artistic 2.0

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.84-4
- Rebuild for new perl

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 2.84-3
- Rebuilt against gcc 4.3

* Wed Aug 29 2007 Robert Scheck <robert@fedoraproject.org> 2.84-2
- Rebuilt (missing BuildID)

* Sat Aug 11 2007 Robert Scheck <robert@fedoraproject.org> 2.84-1
- Upgrade to 2.84 (#250869)
- Added build requirement to perl(ExtUtils::MakeMaker)

* Sat Sep 16 2006 Warren Togami <wtogami@redhat.com> - 2.82-1
- 2.82

* Thu Mar 16 2006 Warren Togami <wtogami@redhat.com> - 2.77-3
- rebuild for FC5

* Fri Nov 11 2005 Warren Togami <wtogami@redhat.com> - 2.77-2
- 2.77

* Fri Aug 05 2005 Warren Togami <wtogami@redhat.com> - 2.75-1
- 2.75

* Thu Jun 16 2005 Warren Togami <wtogami@redhat.com> - 2.71-1
- 2.71 and buildroot patch (#160629 mschwendt)

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.67-2
- Fix SMP build flags.

* Sun Feb 06 2005 Warren Togami <wtogami@redhat.com> 0:2.67-0.FC3
- 2.67

* Mon Mar 29 2004 Warren Togami <wtogami@redhat.com> 0:2.40-0.fdr.2
- #1428 man error patch0

* Sat Mar 27 2004 Warren Togami <wtogami@redhat.com> 0:2.40-0.fdr.1
- Update to 2.40
  no longer needs taintsafe patch
  no longer uses Digest-Nilsimsa
- Explicit Requires perl(Net::DNS) so razor-admin -register does not fail

* Sat Mar 13 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:2.36-0.fdr.7
- Don't create patch backup files as they would be included.
- Own fewer directories because Fedora Core perl package has been fixed.

* Sun Nov 30 2003 Warren Togami <warren@togami.com> - 0:2.36-0.fdr.6
- Add Nicolas ls bug workaround to fix FC1 build #377

* Sat Nov 29 2003 Warren Togami <warren@togami.com> - 0:2.36-0.fdr.5
- Add taint safe patch from spamassassin.org
- Add check macro workaround for rpm < 4.1.1

* Fri Sep 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.36-0.fdr.4
- Specfile cleanup, using vendor dirs, PERL_INSTALL_ROOT and INSTALLARCHLIB.

* Sun Aug 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.36-0.fdr.3
- Rewrite specfile, using fedora-rpm-helper.
- Use perl(XXX) -style dependencies.
- Drop seemingly spurious MailTools dependency.
- Update %%doc list.
- Run make test in %%check.
- Drop MDK specfile since we don't have much common with it any more.

* Sun Jun 15 2003 Warren Togami <warren@togami.com> - 2.34-0.fdr.2
- Apply anvil's fixes

* Sat Jun 14 2003 Warren Togami <warren@togami.com> - 2.34-0.fdr.1
- Minimal Fedora conversion attempt

* Wed Jun  4 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.34-2mdk
- Fix man install for Mdk 8.0

* Mon Jun  2 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.34-1mdk
- Release 2.34

* Mon May 12 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.22-2mdk
- isteamization (Mdk Linux 8.0) (Nicolas Chipaux)

* Sat Mar 29 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.22-1mdk
- Release 2.22

* Wed Oct 30 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.20-2mdk
- ISTEAM powered = add support for Mdk 8.0

* Tue Oct 29 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.20-1mdk
- Release 2.20

* Fri Sep 13 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.14-1mdk
- Release 2.14

* Fri Jul 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.12-1mdk
- From Ben Reser <ben@reser.org> :
 - Release 2.12

* Thu Jul 11 2002 Pixel <pixel@mandrakesoft.com> 2.08-5mdk
- drop the explicit depency on perl 5.6.1

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 2.08-4mdk
- handle man5 pages by hand
- rebuild for perl 5.8.0

* Thu Jun 27 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.08-3mdk
- Fix BuildRequires

* Tue Jun 18 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.08-2mdk
- Add missing depencency on perl-URI and perl-MIME-Base64

* Tue Jun 18 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.08-1mdk
- Release 2.0.8
- Remove patch0 (no longer needed)

* Tue Apr  9 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.20-1mdk
- First Mdk package

* Sun Jan 27 2002 Scott Pakin <pakin@uiuc.edu>
- Initial version
