Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-String-CRC32
Version:        1.8
Release:        3%{?dist}
Summary:        Perl interface for cyclic redundancy check generation
License:        Public Domain
URL:            https://metacpan.org/release/String-CRC32
Source0:        https://cpan.metacpan.org/modules/by-module/String/String-CRC32-%{version}.tar.gz#/perl-String-CRC32-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Test Suite
# (no additional dependencies)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Avoid perl object provides
%{?perl_default_filter}

%description
This packages provides a perl module to generate checksums from strings and
from files.

The checksums are the same as those calculated by ZMODEM, PKZIP, PICCHECK and
many others.

There's another perl module called String::CRC, which supports calculation of
CRC values of various widths (i.e. not just 32 bits), but the generated sums
differ from those of the programs mentioned above.

%prep
%setup -q -n String-CRC32-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc README.md
%{perl_vendorarch}/String/
%{perl_vendorarch}/auto/String/
%{_mandir}/man3/String::CRC32.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov  1 2019 Paul Howarth <paul@city-fan.org> - 1.8-1
- Update to 1.8
  - Perldoc tweaks (GH#3)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.7-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Petr Pisar <ppisar@redhat.com> - 1.7-2
- Perl 5.28 rebuild

* Tue Jul  3 2018 Paul Howarth <paul@city-fan.org> - 1.7-1
- Update to 1.7
  - Perldoc tweaks (GH#2)

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.6-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Paul Howarth <paul@city-fan.org> - 1.6-1
- Update to 1.6
  - New maintainer: LEEJO
  - Add Changes file
  - Add link to github repo
  - Add strict and warnings
  - Add LICENSE to POD + LICENSE file
  - Add META.* files through make dist
  - Add .travis.yml for CI
- This release by LEEJO → update source URL
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.5-11
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.5-9
- Perl 5.24 rebuild

* Tue Apr 19 2016 Paul Howarth <paul@city-fan.org> - 1.5-8
- Classify buildreqs by usage
- Simplify find commands using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.5-5
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.5-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan  1 2014 Paul Howarth <paul@city-fan.org> - 1.5-1
- Update to 1.5 (document use of binmode)
- Drop %%defattr, redundant since rpm 4.4
- No need to remove empty directories from the buildroot
- Use %%{_fixperms} macro rather than our own chmod incantation

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.4-19
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Petr Pisar <ppisar@redhat.com> - 1.4-17
- Correct dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.4-15
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4-13
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4-11
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4-10
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.4-9
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-6
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4-5
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4-4
- rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 1.4-3
- fix typo in %%summary and tidy up %%description
- remove redundant dependency on perl >= 1:5.6.1
- fix argument order for find with -depth
- drop "|| :" from %%check (only required for ancient rpmbuild versions)
- add buildreq perl(ExtUtils::MakeMaker)

* Wed Aug 02 2006 Warren Togami <wtogami@redhat.com> 1.4-2
- bump

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 1.4-1.FC6
- upgrade to upstream version 1.4

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3-3.FC5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3-3.FC5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0:1.03-3.FC5
- rebuild for new perl-5.8.8

* Thu Jan 19 2006 Jason Vas Dias <jvdias@redhat.com> - 0:1.03-2.FC5
- bug 176175 addendum: license should be 'Public Domain'

* Fri Jan 13 2006 Jason Vas Dias <jvdias@redhat.com> - 0.1.03-1.4.FC5
- fix bug 177700: differentiate version from FE4, FE dev versions

* Fri Dec 16 2005 Jason Vas Dias <jvdias@redhat.com> - 0:1.03-1
- Initial build.
- Required by lftp-3.3.x+
- Imported to fix bug 176175
