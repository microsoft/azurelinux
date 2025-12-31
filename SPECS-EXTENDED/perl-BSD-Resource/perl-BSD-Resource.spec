# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_BSD_Resource_enables_optional_test
%else
%bcond_with perl_BSD_Resource_enables_optional_test
%endif

Name:           perl-BSD-Resource
Version:        1.291.100
%global module_version 1.2911
Release:        13%{?dist}
Summary:        BSD process resource limit and priority functions
# No matter what the pm and xs headers say, this is stated in the POD and,
# according to upstream changelog for 1.2905, is correct.
# No matter what POD says, ppport.h comes from perl with perl's license.
License:        (LGPLv2 or Artistic 2.0) and (GPL+ or Artistic)
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/BSD-Resource
Source0:        https://cpan.metacpan.org/authors/id/J/JH/JHI/BSD-Resource-%{module_version}.tar.gz#/perl-BSD-Resource-%{module_version}.tar.gz
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(vars)
# Run-time:
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
%if %{with perl_BSD_Resource_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%{?perl_default_filter}

%description
A module providing an interface for testing and setting process limits
and priorities.

%prep
%setup -q -n BSD-Resource-%{module_version} 

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -a -size 0 -delete
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc README
%{perl_vendorarch}/BSD/
%{perl_vendorarch}/auto/BSD/
%{_mandir}/man3/*
%exclude %{_mandir}/man3/BSD::Resource.3pm.gz

%changelog
* Tue Dec 30 2025 Aninda Pradhan <v-anindap@microsoft.com> - 1.291.100-13
- Fixed license warning by excluding changelog from doc and BSD::Resource.3pm.gz from man directory
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.291.100-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.291.100-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.291.100-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.291.100-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.291.100-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.291.100-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.291.100-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.291.100-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.291.100-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.291.100-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.291.100-2
- Perl 5.26 rebuild

* Mon Apr 10 2017 Jan Pazdziora <jpazdziora@redhat.com> - 1.291.100-1
- 1440744 - Rebase to upstream version 1.2911.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.291.000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.291.000-2
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jan Pazdziora <jpazdziora@redhat.com> - 1.291.000-1
- 1336059 - Rebase to upstream version 1.2910.

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.290.900-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.290.900-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 25 2015 Petr Šabata <contyk@redhat.com> - 1.290.900-1
- 1.2909 bump

* Thu Oct 22 2015 Petr Pisar <ppisar@redhat.com> - 1.290.800-1
- 1.2908 bump
- Correct the license tag to ((LGPLv2 or Artistic 2.0) and (GPL+ or Artistic)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.290.700-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.290.700-2
- Perl 5.22 rebuild

* Thu Dec 04 2014 Petr Pisar <ppisar@redhat.com> - 1.290.700-1
- Normalize version

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.29.07-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.29.07-2
- Perl 5.18 rebuild

* Mon Jul 15 2013 Petr Šabata <contyk@redhat.com> - 1.29.07-1
- 1.2907 bump, tests and pod enhancements
- Fix a bogus date in changelog

* Mon Jul 01 2013 Petr Šabata <contyk@redhat.com> - 1.29.05-1
- 1.2905 bump
- Correct the licence tag
- Various typo and perl5.18 fixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.04-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 19 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.29.04-13
- Add perl_default_filter to filter Resource.so from provides. 

* Thu Aug  2 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.29.04-12
- Update BR, Provides
- Clean up for modern rpmbuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.29.04-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 10 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.29.04-8
- add filter for unneeded provides

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.29.04-6
- Perl mass rebuild & add provide

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29.04-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 1.29.04-1
- 1.2904 bump (bug #600626)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29.03-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.29.03-3
- rebuild against perl 5.10.1

* Thu Oct 29 2009 Stepan Kasal <skasal@redhat.com> - 1.29.03-2
- bump release

* Mon Jul 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.29.03-1
- update, remove unneeded patch

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.28-7
- Fix Patch0:/%%patch mismatch.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.28-6
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.28-5
- Autorebuild for GCC 4.3

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.28-4
- rebuild for new perl

* Thu Aug 23 2007 Robin Norwood <rnorwood@redhat.com> 1.28-3
- Fix license tag.
- Add %%doc section

* Sat Jun 30 2007 Steven Pritchard <steve@kspei.com> 1.28-2
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Remove check macro cruft.
- Remove redundant BR perl.
- BR ExtUtils::MakeMaker, Test::More, Test::Pod, and Test::Pod::Coverage.
- Patch t/setrlimit.t to fix bogus test failure.
- Set OPTIMIZE when running Makefile.PL, not make.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.28-1.fc6.1
- rebuild

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 1.28-1
- upgrade to upstream version 1.28

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.24-3.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.24-3.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.24-3.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Apr  2 2005 Warren Togami <wtogami@redhat.com> - 1.24-3
- skip make test #153178

* Sat Apr  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-2
- spec cleanup
- License corrected

* Thu Mar 31 2005 Warren Togami <wtogami@redhat.com> 1.24-1
- 1.24

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.23-1
- update to 1.23

* Thu Jun 05 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Jun  4 2002 Chip Turner <cturner@redhat.com>
- properly claim directories owned by package so they are removed when package is removed

* Wed Jan 30 2002 cturner@redhat.com
- Specfile autogenerated

