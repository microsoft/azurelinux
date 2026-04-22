# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel} == 8
%bcond_without graphics_magick
%else
%bcond_with graphics_magick
%endif

Name:           perl-Image-Size
Version:        3.300
Release: 34%{?dist}
Summary:        Determine the size of images in several common formats in Perl
# Automatically converted from old format: LGPLv2 or Artistic 2.0 - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2 OR Artistic-2.0
URL:            https://metacpan.org/release/Image-Size
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJRAY/Image-Size-%{version}.tar.gz
# WEBP: use proper endian-agnostic extractor 
# https://github.com/rjray/image-size/commit/37609b9079cc2449589fa436baa2e08a3e2b427d
Patch0:         perl-Image-Size-3.300-endian-fix.patch
BuildArch:      noarch
BuildRequires: make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(bytes)
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
%if %{with graphics_magick}
BuildRequires:  perl(Graphics::Magick)
%else
BuildRequires:  perl(Image::Magick)
%endif
BuildRequires:  perl(IO::File)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
Requires:       perl(Compress::Zlib)
Requires:       perl(Cwd)
Requires:       perl(File::Spec)
%if %{with graphics_magick}
Recommends:     perl(Graphics::Magick)
%else
Recommends:     perl(Image::Magick)
%endif
Requires:       perl(Symbol)

%description
Image::Size is a library based on the image-sizing code in the wwwimagesize
script, a tool that analyzes HTML files and adds HEIGHT and WIDTH tags to
IMG directives. Image::Size has generalized that code to return a raw (X, Y)
pair, and included wrappers to pre-format that output into either HTML or
a set of attribute pairs suitable for the CGI.pm library by Lincoln Stein.
Currently, Image::Size can size images in XPM, XBM, GIF, JPEG, PNG, MNG, TIFF,
the PPM family of formats (PPM/PGM/PBM) and if Image::Magick is installed,
the formats supported by it.

%prep
%setup -q -n Image-Size-%{version}
%patch -P0 -p1 -b .endianfix

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc ChangeLog README
%{_bindir}/imgsize
%{perl_vendorlib}/Image/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 3.300-31
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.300-24
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.300-21
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.300-18
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.300-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.300-12
- Perl 5.28 rebuild

* Thu May  3 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.300-11
- Added support for building with Graphics::Magick

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.300-8
- Perl 5.26 rebuild

* Thu Jun  1 2017 Tom Callaway <spot@fedoraproject.org> - 3.300-7
- use proper endian-agnostic extractor (bz1457935)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.300-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.300-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.300-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.300-2
- Perl 5.22 rebuild

* Fri Mar 20 2015 Tom Callaway <spot@fedoraproject.org> - 3.300-1
- update to 3.300

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.232-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.232-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.232-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 3.232-2
- Perl 5.18 rebuild

* Thu Jun 27 2013 Petr Šabata <contyk@redhat.com> - 3.232-1
- 3.232 bump
- Modernize the spec somewhat
- Drop the extra Build.PL; upstream's shipping Makefile.PL,
  there's no reason for our own solution
- Fix a bogus date in changelog

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 3.2-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.2-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.2-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.2-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.2-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-1
- update to 3.2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-3
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-1
- bump to 3.1
- license change (now LGPLv2 or Artistic 2.0)

* Sat Sep 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.01-1
- Update to 3.01.
- Makefile.PL -> Build.PL.

* Sat Jun 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.0-1
- Update to 3.0.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.992-5
- Rebuild for FC5 (perl 5.8.8).

* Fri Dec 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.992-4
- Dist tag.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.992-3
- rebuilt

* Thu Jun  3 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.992-0.fdr.2
- Bring up to date with current fedora.us perl spec template.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.992-0.fdr.1
- First build.
