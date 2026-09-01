# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-HTML-Template
Version:        2.97
Release:        27%{?dist}
Summary:        Perl module to use HTML Templates
# Automatically converted from old format: GPL+ or Artistic - review is highly recommended.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/HTML-Template
Source0:        https://cpan.metacpan.org/modules/by-module/HTML/HTML-Template-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module
BuildRequires:  perl(Carp)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(integer)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Optional Functionality
BuildRequires:  perl(GTop)
BuildRequires:  perl(IPC::SharedCache)
BuildRequires:  perl(Storable)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(CGI)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
# Dependencies
Suggests:       perl(GTop)
Suggests:       perl(IPC::SharedCache)
Suggests:       perl(Storable)

%description
This module attempts make using HTML templates simple and natural.  It
extends standard HTML with a few new HTML-esque tags - <TMPL_VAR>,
<TMPL_LOOP>, <TMPL_INCLUDE>, <TMPL_IF> and <TMPL_ELSE>.  The file
written with HTML and these new tags is called a template.  It is
usually saved separate from your script - possibly even created by
someone else!  Using this module you fill in the values for the
variables, loops and branches declared in the template.  This allows
you to separate design - the HTML - from the data, which you generate
in the Perl script.


%prep
%setup -q -n HTML-Template-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}


%check
TEST_SHARED_MEMORY=1 make test


%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/HTML/
%{_mandir}/man3/HTML::Template.3*
%{_mandir}/man3/HTML::Template::FAQ.3*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 06 2024 Miroslav Suchý <msuchy@redhat.com> - 2.97-25
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.97-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.97-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.97-12
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 17 2019 Paul Howarth <paul@city-fan.org> - 2.97-10
- Spec tidy-up
  - Use author-independent source URL
  - Classify buildreqs by usage
  - Add Suggests: for modules providing optional functionality
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Simplify find command using -delete
  - Don't need to remove empty directories from the buildroot
  - Fix permissions verbosely
  - Make %%files list more explicit
  - Use %%license

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.97-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.97-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.97-2
- Perl 5.26 rebuild

* Fri May 19 2017 Tom Callaway <spot@fedoraproject.org> - 2.97-1
- update to 2.97

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.95-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.95-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.95-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.95-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.95-4
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.95-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 23 2013 Tom Callaway <spot@fedoraproject.org> - 2.95-1
- update to 2.95

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 2.94-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.94-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Tom Callaway <spot@fedoraproject.org> - 2.94-1
- update to 2.94

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 2.91-2
- Perl 5.16 rebuild
- Specify all dependencies

* Mon Apr  2 2012 Tom Callaway <spot@fedoraproject.org> - 2.91-1
- update to 2.91

* Mon Jan 16 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.10-5
- Add BR: perl(Digest::MD5) (Fix gcc-4.7 FTBFS).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 30 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.10-3
- Set module version to fake 2.91 to work around versioning issue (#734253).
- Fix source URL, drop no longer needed README linefeed conversion.

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 2.10-2
- Perl mass rebuild

* Thu Jul 14 2011 Tom Callaway <spot@fedoraproject.org>  - 2.10-1
- update to 2.10

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.9-11
- Perl mass rebuild

* Sun Apr 24 2011 Tom Callaway <spot@fedoraproject.org> - 2.9-10
- actually apply man page fixes patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.9-8
- 661697 rebuild for fixing problems with vendorach/lib
- add missing BR CGI
- add man page fixes from Debian

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.9-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.9-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9-2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9-1.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Jan 30 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.9-1
- Update to 2.9.

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.8-3
- Rebuild for FC6.

* Sat Feb 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.8-2
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.8-1
- Update to 2.8.

* Sat Aug 13 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.7-4
- README file: corrected the end-of-line encoding (#165874).
- Bring up to date with Fedora Extras template.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.7-3
- rebuilt

* Mon Oct 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.7-0.fdr.2
- Typo correction (rpmlint warning).
- Build requirements: removed perl(CGI).

* Fri Jun 25 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:2.7-0.fdr.1
- First build after 2nd time of losing the specfile somewhere :(
