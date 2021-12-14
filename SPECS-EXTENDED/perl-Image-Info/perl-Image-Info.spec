Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Image-Info
Version:        1.42
Release:        3%{?dist}
Summary:        Image meta information extraction module for Perl
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Image-Info
Source0:        https://cpan.metacpan.org/authors/id/S/SR/SREZIC/Image-Info-%{version}.tar.gz#/perl-Image-Info-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Image::Xbm)
BuildRequires:  perl(Image::Xpm)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
BuildRequires:  perl(vars)
BuildRequires:  perl(XML::LibXML::Reader)
BuildRequires:  perl(XML::Simple)
Requires:       rgb
Requires:       perl(Compress::Zlib)
Requires:       perl(IO::Scalar)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This Perl extension allows you to extract meta information from
various types of image files.

%prep
%setup -q -n Image-Info-%{version}
chmod -c 644 exifdump imgdump

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc CHANGES CREDITS README TODO exifdump imgdump
%{perl_vendorlib}/Bundle/
%{perl_vendorlib}/Image/
%{_mandir}/man3/*.3pm*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.42-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-1
- 1.42 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.41-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.41-7
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.41-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.41-4
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Tom Callaway <spot@fedoraproject.org> - 1.41-1
- update to 1.41

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.40-2
- Perl 5.26 rebuild

* Tue Apr 11 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.40-1
- 1.40 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 10 2016 Tom Callaway <spot@fedoraproject.org> - 1.39-1
- update to 1.39

* Wed Oct  5 2016 Tom Callaway <spot@fedoraproject.org> - 1.38-6
- apply upstream fix for XXE SVG security issue (bz1379556)

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-2
- Perl 5.22 rebuild

* Tue Apr 21 2015 Tom Callaway <spot@fedoraproject.org> - 1.38-1
- update to 1.38

* Fri Mar 20 2015 Tom Callaway <spot@fedoraproject.org> - 1.37-1
- update to 1.37

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.33-3
- Perl 5.18 rebuild

* Wed Jan 30 2013 Paul Howarth <paul@city-fan.org> - 1.33-2
- Don't BR: perl(Image::TIFF); it's provided by this package

* Wed Nov 14 2012 Petr Šabata <contyk@redhat.com> - 1.33-1
- 1.33 bump
- Get rid of the old cruft
- Fix dependencies
- Update the source URL

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1.28-13
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.28-11
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.28-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.28-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.28-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.28-6
- rebuild against perl 5.10.1

* Mon Nov 09 2009 Adam Jackson <ajax@redhat.com> 1.28-5
- Requires: rgb, not Requires: /usr/share/X11/rgb.txt

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.28-1
- update to 1.28

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.27-3
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.27-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.27-1
- bump to 1.27

* Wed May 30 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.25-1
- Update to 1.25.

* Mon Feb 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-1
- Update to 1.24.

* Sat Sep 30 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.23-1
- Update to 1.23.

* Sun Jul 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.22-1
- Update to 1.22.

* Mon May  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.21-2
- Bumping release due to CVS problem.

* Mon May  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.21-1
- Update to 1.21.

* Mon Mar 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-1
- Update to 1.20.

* Wed Mar  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.19-1
- Update to 1.19 (broken: cpan tickets: #18020 and #18147).
- Module::Install 0.58 is broken (Image-Info-1.19-inc-Module-Install.pm.patch).
- BR: perl(Image::Xbm), perl(Image::Xpm), perl(XML::Simple).

* Fri Mar  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.18-1
- Update to 1.18 (broken: cpan ticket #6558).
- Dropped patches Image-Info-1.16-X[BP]M.pm.patch (accepted upstream).
- Dropped patch Image-Info-1.16-string.t.patch (test has been rewritten).

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.17-2
- BR: perl(Test::Pod), perl(Test::Pod::Coverage).

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.17-1
- Update to 1.17.
- New upstream maintainer.

* Wed Nov 23 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.16-6
- Add dependency on rgb.txt, adjust its location for FC5.
- Specfile cleanups.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.16-4
- rebuilt

* Thu Jul  1 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.16-0.fdr.3
- Reverted Image::Xbm and Image::Xpm patches.
- Patched Image::Info::XBM.pm and Image::Info::XPM.pm instead.

* Tue Jun  8 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.16-0.fdr.2
- Patched Image::Xbm and Image::Xpm to avoid test failures in this module.

* Thu Jun  3 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.16-0.fdr.1
- Update to version 1.16.
- Bring up to date with current fedora.us perl spec template.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.15-0.fdr.1
- First build.
