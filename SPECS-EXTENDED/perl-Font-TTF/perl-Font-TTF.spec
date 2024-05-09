Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:          perl-Font-TTF
Version:       1.06
Release:       13%{?dist}
Summary:       Perl library for modifying TTF font files
# other files:  Artistic 2.0
## not in binary packages
# t/testfont.*: OFL
License:       Artistic 2.0
URL:           https://metacpan.org/release/Font-TTF
Source0:       https://cpan.org/authors/id/B/BH/BHALLISSY/Font-TTF-%{version}.tar.gz
BuildArch:     noarch
# Build
BuildRequires: make
BuildRequires: perl-generators
BuildRequires: perl-interpreter
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires: perl(Getopt::Std)
BuildRequires: perl(strict)
# Runtime
BuildRequires: perl(bytes)
BuildRequires: perl(Compress::Zlib)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec)
BuildRequires: perl(IO::File)
BuildRequires: perl(IO::String)
BuildRequires: perl(Symbol)
BuildRequires: perl(utf8)
BuildRequires: perl(vars)
# XML::Parser::Expat not used at tests
# Tests only
BuildRequires: perl(File::Compare)
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Simple)
Requires: perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description
Perl module for TrueType font hacking. Supports reading, processing and writing
of the following tables: GDEF, GPOS, GSUB, LTSH, OS/2, PCLT, bsln, cmap, cvt,
fdsc, feat, fpgm, glyf, hdmx, head, hhea, hmtx, kern, loca, maxp, mort, name,
post, prep, prop, vhea, vmtx and the reading and writing of all other table
types.

In short, you can do almost anything with a standard TrueType font with this
module.

%package XMLparse
Summary:       XML Font parser
Requires:      perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Conflicts:     perl-Font-TTF < 1.06-6

%description XMLparse
This Perl module contains the support routines for parsing XML and generating
the TrueType font structures as a result.

The module has been separated from the rest of the perl-Font-TTF package in
order to reduce the dependency that this would bring, of the whole package on
XML::Parser. This way, people without the XML::Parser can still use the rest
of the package.


%prep
%setup -q -n Font-TTF-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc README.TXT CONTRIBUTORS Changes TODO
%dir %{perl_vendorlib}/Font
%dir %{perl_vendorlib}/Font/TTF
%{perl_vendorlib}/ttfmod.pl
%{perl_vendorlib}/Font/TTF.pm
%{perl_vendorlib}/Font/TTF/*
%exclude %{perl_vendorlib}/Font/TTF/XMLparse.pm
%{_mandir}/man3/*.3*
%exclude %{_mandir}/man3/Font::TTF::XMLparse.3pm.*
# We really don't want to use this perl package in a Win32 env
# or poke in the windows registry to resolve fonts
# (upstream makefile needs to get smarter)
%exclude %{perl_vendorlib}/Font/TTF/Win32.pm
%exclude %{_mandir}/man3/Font::TTF::Win32.3pm.*

%files XMLparse
%license LICENSE
%doc CONTRIBUTORS Changes
%dir %{perl_vendorlib}/Font
%dir %{perl_vendorlib}/Font/TTF
%{perl_vendorlib}/Font/TTF/XMLparse.pm
%{_mandir}/man3/Font::TTF::XMLparse.3pm.*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.06-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-7
- Perl 5.28 rebuild

* Wed May 02 2018 Petr Pisar <ppisar@redhat.com> - 1.06-6
- Move Font::TTF::XMLparse into perl-Font-TTF-XMLparse subpackage

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 29 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-1
- 1.06 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-2
- Perl 5.22 rebuild

* Mon Feb 02 2015 Petr Šabata <contyk@redhat.com> - 1.05-1
- 1.05 enhancement and bugfix bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Petr Šabata <contyk@redhat.com> - 1.04-1
- 1.04 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.02-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Petr Šabata <contyk@redhat.com> - 1.02-2
- Add missing dependencies

* Fri Aug 31 2012 Petr Šabata <contyk@redhat.com> - 1.02-1
- 1.02 bump (a lettercase fix)

* Thu Aug 30 2012 Petr Šabata <contyk@redhat.com> - 1.01-1
- 1.01 bump (Makefile/META changes only)

* Wed Aug 29 2012 Petr Šabata <contyk@redhat.com> - 1.00-1
- 1.00 bump
- Modernize the spec file

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.48-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.48-2
- Perl mass rebuild

* Wed Mar 09 2011 Parag Nemade <panemade AT fedoraproject DOT org> - 0.48-1
- new upstream release 0.48

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.45-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.45-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.45-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.45-3
— global-ization

* Thu Sep 4 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.45-2
⚖ ⇒ Artistic 2.0

* Fri Jul 11 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.45-1
⌖ Fedora 10 alpha general package cleanup
⚖ Upstream needs to relicense fast to avoid culling

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 0.43-3
Rebuild for new perl

* Sat Feb 09 2008  Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.43-2

* Fri May 18 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.41-1

* Tue Mar 20 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.40.0-3
- small packaging fixes

* Sat Sep 02 2006  Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.40.0-2
- FE6 Rebuild

* Mon Jul 31 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.40.0-1

* Sat Feb 18 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.38.1-1
- new version with COPYING file as requested from upstream
  many thanks to Martin Hosken for quick action!

* Mon Feb 13 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.37-4
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Feb 5 2006 Nicolas Mailhot <nicolas.mailhot (at) laposte.net>
- 0.37-3
- spec cleanups #2

* Sun Feb 5 2006 Nicolas Mailhot <nicolas.mailhot (at) laposte.net>
- 0.37-2
- spec cleanups

* Sat Feb 4 2006 Nicolas Mailhot <nicolas.mailhot (at) laposte.net>
- 0.37-1
- Initial release
