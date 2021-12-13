Name: 		perl-Text-Glob
Version: 	0.11
Release: 	11%{?dist}
Summary: 	Perl module to match globbing patterns against text
License: 	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: 		https://metacpan.org/release/Text-Glob
Source0: 	https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Text-Glob-%{version}.tar.gz#/perl-Text-Glob-%{version}.tar.gz

BuildArch: noarch
BuildRequires:  perl-generators
BuildRequires:  %{__perl}
BuildRequires:  %{__make}

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Text::Glob implements glob(3) style matching that can be used to match
against text, rather than fetching names from a file-system.  If you
want to do full file globbing use the File::Glob module instead.

%prep
%setup -q -n Text-Glob-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%{__make} %{?_smp_mflags}

%install
%{__make} pure_install DESTDIR=$RPM_BUILD_ROOT
chmod -R u+w $RPM_BUILD_ROOT/*

%check
%{__make} test

%files
%doc Changes
%{perl_vendorlib}/Text
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-8
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-2
- Perl 5.26 rebuild

* Mon Mar 13 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.11-1
- Upstream update.
- Spec files cosmetics.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 22 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.10-1
- Upstream update.

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-16
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.09-14
- Modernize spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-12
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-11
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.09-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-6
- Update BRs and remove %%defattr.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.09-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.09-2
- Perl mass rebuild

* Wed Mar 02 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.09-1
- Upstream update.
- Spec cleanup.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-9
- Mass rebuild with perl-5.12.0

* Thu Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.08-8
- add readme

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.08-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-4
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-3
- rebuild for new perl

* Sat Aug 18 2007 Ralf Corsépius <rc040203@freenet.de> - 0.08-2
- Update license tag.

* Tue May 08 2007 Ralf Corsépius <rc040203@freenet.de> - 0.08-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.07-2
- Mass rebuild.

* Thu Jul 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.07-1
- Upstream update.

* Tue Feb 28 2006 Ralf Corsépius <rc040203@freenet.de> - 0.06-4
- Rebuild for perl-5.8.8.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.06-3
- Spec cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.06-2
- FE resubmission.

* Fri Jul 01 2005 Ralf Corsepius <ralf@links2linux.de> - 0.06-1
- FE submission.
