Name:           perl-XML-Twig
Version:        3.52
Release:        13%{?dist}
Summary:        Perl module for processing huge XML documents in tree mode
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/XML-Twig
Source0:        https://cpan.metacpan.org/authors/id/M/MI/MIROD/XML-Twig-%{version}.tar.gz#/perl-XML-Twig-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  expat >= 2.0.1
BuildRequires:  findutils
BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
# Keep HTML::Entities::Numbered optional
# Keep HTML::Tidy optional
BuildRequires:  perl(HTML::TreeBuilder) >= 4.00
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::Wrap)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XML::Parser) >= 2.23
# Prefer XML::XPathEngine over XML::XPath
BuildRequires:  perl(XML::XPathEngine)
# Tests:
BuildRequires:  perl(Cwd)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(IO::String)
BuildRequires:  perl(LWP)
BuildRequires:  perl(HTML::Entities)
%if !( 0%{?rhel} >= 7 )
BuildRequires:  perl(Test::CPAN::Meta::JSON)
%endif
BuildRequires:  perl(Text::Iconv)
BuildRequires:  perl(Tie::IxHash)
BuildRequires:  perl(Unicode::Map8)
BuildRequires:  perl(Unicode::String)
BuildRequires:  perl(utf8)
BuildRequires:  perl(XML::Filter::BufferText)
BuildRequires:  perl(XML::Handler::YAWriter)
BuildRequires:  perl(XML::SAX::Writer) >= 0.39
BuildRequires:  perl(XML::Simple)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Encode)
Requires:       perl(HTML::TreeBuilder) >= 4.00
Requires:       perl(IO::Scalar)
Requires:       perl(Scalar::Util)
Requires:       perl(Text::Wrap)
Requires:       perl(XML::Parser) >= 2.23

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\(XML::XPathEngine::NodeSet\\)
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(xml_split::state\\)
# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(XML::Parser\\)$

%description
This module provides a way to process XML documents. It is build on
top of XML::Parser.  XML::Twig offers a tree interface to the
document, while allowing you to output the parts of it that have been
completely processed.  It allows minimal resource (CPU and memory)
usage by building the tree only for the parts of the documents that
need actual processing, through the use of the twig_roots and
twig_print_outside_roots options.

%prep
%setup -q -n XML-Twig-%{version}
iconv -f iso88591 -t utf8 < Changes > Changes.utf8 && \
    mv -f Changes.utf8 Changes

%build
perl Makefile.PL -y INSTALLDIRS=perl NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README 
%{perl_privlib}/*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.52-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.52-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.52-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.52-10
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.52-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.52-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.52-7
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.52-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 14 2017 Petr Pisar <ppisar@redhat.com> - 3.52-5
- Modernize spec file

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.52-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.52-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 24 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.52-1
- 3.52 bump

* Wed Nov 23 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.50-1
- 3.50 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.49-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.49-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.49-2
- Perl 5.22 rebuild

* Mon Apr 13 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.49-1
- 3.49 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.48-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.48-1
- 3.48 bump

* Wed Mar 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.46-1
- 3.46 bump

* Tue Mar 04 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.45-1
- 3.45 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 3.44-2
- Perl 5.18 rebuild

* Tue May 14 2013 Petr Šabata <contyk@redhat.com> - 3.44-1
- 3.44 enhancement update

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Petr Pisar <ppisar@redhat.com> - 3.42-2
- Do not build-require Test::CPAN::Meta::JSON on RHEL >= 7
- Keep Tidy optional

* Mon Nov 12 2012 Petr Pisar <ppisar@redhat.com> - 3.42-1
- 3.42 bump

* Tue Aug 14 2012 Petr Šabata <contyk@redhat.com> - 3.41-1
- 3.41 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 3.40-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 3.40-2
- Perl 5.16 rebuild

* Fri May 11 2012 Petr Šabata <contyk@redhat.com> - 3.40-1
- 3.40 bump
- Dropping defattr and perl command macros

* Thu Apr 19 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.39-4
- make module Kwalitee conditional

* Tue Apr 10 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.39-3
- remove cyclic dependency added by mistake  810563 
  XML::Twig::Elt, XML::Twig::XPath

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Petr Sabata <contyk@redhat.com> - 3.39-1
- 3.39 bump

* Sun Jul 24 2011 Iain Arnell <iarnell@gmail.com> 3.38-4
- update filtering for rpm 4.9

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 3.38-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 3.38-2
- Perl mass rebuild

* Wed Mar 23 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.38-1
- update to 3.38
- BR organize according to cpanspec list

* Mon Feb 14 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.37-3
- 677179 filter internal xml_split::state from requires and call filter properly
- add new BR, which is now in Fedora

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.37-1
- update, fix BR, R

* Tue Sep 21 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.35-1
- update

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.34-2
- Mass rebuild with perl-5.12.0

* Tue Jan 19 2010 Chris Weyl <cweyl@alumni.drew.edu> 3.34-1
- update prov/dep filtering to current guidelines
- auto-update to 3.34 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- altered br on perl(XML::Parser) (0 => 2.23)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.33-2
- rebuild against perl 5.10.1

* Mon Oct 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 3.33-1
- new development release which should fix various bug reports e.g. 529220

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Mar  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.32-1
- update to 3.32

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.29-6
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.29-5
- rebuild for new perl

* Sun Jul 08 2007 Robin Norwood <rnorwood@redhat.com> - 3.29-4
- Resolves: rhbz#247247
- Remove bogus Provides: perl(XML::XPathEngine::NodeSet), and move
  Requires filter into spec file.

* Thu Jun 28 2007 Robin Norwood <rnorwood@redhat.com> - 3.29-3
- Add several buildrequires for tests and optional features

* Sat Feb 17 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.29-2
- Minor cleanups.

* Tue Feb 13 2007 Robin Norwood <rnorwood@redhat.com> - 3.29-1
- New version: 3.29

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 3.26-1
- Upgrade to 3.26

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 3.25-1
- Upgrade to 3.25

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 3.22-1.1
- Update to 3.23
- rebuild for new perl-5.8.8

* Mon Dec 19 2005 Jason Vas Dias<jvdias@redhat.com> - 3.22-1
- Update to 3.22

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sun Apr 17 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.17-1
- Update to 3.17.
- Specfile cleanup. (#155168)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 3.13-6
- rebuild

* Mon May  3 2004 Chip Turner <cturner@redhat.com> 3.13-5
- bugzilla 122079, add dep filter to remove bad dependency

* Fri Apr 23 2004 Chip Turner <cturner@redhat.com> 3.13-4
- remove Packager tag

* Fri Apr 23 2004 Chip Turner <cturner@redhat.com> 3.13-2
- bump

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 3.13-1
- update to 3.13

* Tue Dec 10 2002 Chip Turner <cturner@redhat.com>
- update to latest version from CPAN

* Mon Aug 26 2002 Chip Turner <cturner@redhat.com>
- rebuild for build failure

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed May 29 2002 cturner@redhat.com
- Specfile autogenerated
