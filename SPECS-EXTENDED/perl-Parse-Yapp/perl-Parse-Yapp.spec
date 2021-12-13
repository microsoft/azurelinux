%global cpan_version 1.21

Name:           perl-Parse-Yapp
# Keep 2-digit version for history
Version:        %{cpan_version}
Release:        8%{?dist}
Summary:        Perl extension for generating and using LALR parsers
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Parse-Yapp
Source0:        https://cpan.metacpan.org/authors/id/W/WB/WBRASWELL/Parse-Yapp-%{cpan_version}.tar.gz#/perl-Parse-Yapp-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Parse::Yapp (Yet Another Perl Parser compiler) is a collection of modules that
let you generate and use yacc like thread safe (reentrant) parsers with perl
object oriented interface.  The script yapp is a front-end to the Parse::Yapp
module and let you easily create a Perl OO parser from an input grammar file.

%prep
%setup -q -n Parse-Yapp-%{cpan_version}
chmod 644 README lib/Parse/{*.pm,Yapp/*.pm}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{_bindir}/yapp
%{perl_vendorlib}/Parse/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.21-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 09 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-1
- 1.21 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-1
- 1.2 bump

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-62
- Perl 5.26 rebuild

* Mon May 22 2017 Petr Pisar <ppisar@redhat.com> - 1.05-61
- Restore compatibility with Perl 5.26.0 (CPAN RT#106685, CPAN RT#114776)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-59
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-56
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-55
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.05-52
- Specify all dependencies

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.05-51
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 15 2012 Petr Pisar <ppisar@redhat.com> - 1.05-49
- Specify all dependencies
- Modernize spec file
- Fix Parse::Yapp POD

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.05-47
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-45
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-43
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-42
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-41
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-38
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-37
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-36.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 29 2006 Patrice Dumas <dumas@centre-cired.fr> - 1.05-36
- rebuild for FC6

* Fri Feb 17 2006 Patrice Dumas <dumas@centre-cired.fr> - 1.05-35
- rebuild for fc5

* Wed Nov 16 2005 Warren Togami <wtogami@redhat.com> - 1.05-34
- import into Extras

* Wed Apr 20 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-33
- #155467
- Bring up to date with current Fedora.Extras perl spec template.

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1.05-32
- rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Jun  4 2002 Chip Turner <cturner@redhat.com>
- properly claim directories owned by package so they are removed when package is removed

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated. 
