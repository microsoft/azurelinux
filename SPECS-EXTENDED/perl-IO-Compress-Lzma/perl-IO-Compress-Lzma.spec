# Perform optional tests
%if 0%{?rhel} >= 9
%bcond_with perl_IO_Compress_Lzma_enables_optional_test
%else
%bcond_without perl_IO_Compress_Lzma_enables_optional_test
%endif

Name:		perl-IO-Compress-Lzma
Version:	2.213
Release:	1%{?dist}
Summary:	Read and write lzma compressed data
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/IO-Compress-Lzma
Source0:        https://cpan.metacpan.org/modules/by-module/IO/IO-Compress-Lzma-%{version}.tar.gz
Source1:        LICENSE.PTR
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Config)
BuildRequires:	perl(ExtUtils::MakeMaker) >= 5.16
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(lib)
# Module Runtime
BuildRequires:	perl(bytes)
BuildRequires:	perl(Compress::Raw::Lzma) >= %{version}
BuildRequires:	perl(constant)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(IO::Compress::Base) >= %{version}
BuildRequires:	perl(IO::Compress::Base::Common) >= %{version}
BuildRequires:	perl(IO::Uncompress::Base) >= %{version}
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Carp)
BuildRequires:	perl(Compress::Raw::Zlib) >= 2
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::Compress::Zip)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IO::Uncompress::AnyUncompress)
BuildRequires:	perl(IO::Uncompress::Unzip)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Test::More)
BuildRequires:	xz, xz-lzma-compat
%if %{with perl_IO_Compress_Lzma_enables_optional_test}
# Optional Tests
BuildRequires:	lzip
BuildRequires:	perl(Encode)
BuildRequires:	perl(IO::String)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::CPAN::Meta::JSON)
BuildRequires:	perl(Test::NoWarnings)
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	/usr/bin/7z
%endif
# Dependencies
# (none)

%description
This distribution provides a Perl interface to allow reading and writing of
compressed data created with the lzma library.

%prep
%setup -q -n IO-Compress-Lzma-%{version}

# Remove bundled test modules
rm -rv t/Test/
perl -i -ne 'print $_ unless m{^t/Test/}' MANIFEST

# Remove spurious exec permissions
chmod -c -x examples/*

# Fix shellbangs in examples
perl -pi -e 's|^#!/usr/local/bin/perl\b|#!/usr/bin/perl|' \
	examples/lzcat examples/lzstream examples/xzcat examples/xzstream

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

cp %{SOURCE1} .

%check
make test COMPRESS_ZLIB_RUN_MOST=1

%files
%license LICENSE.PTR
%doc Changes README examples/*
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::Compress::Lzip.3*
%{_mandir}/man3/IO::Compress::Lzma.3*
%{_mandir}/man3/IO::Compress::Xz.3*
%{_mandir}/man3/IO::Uncompress::UnLzip.3*
%{_mandir}/man3/IO::Uncompress::UnLzma.3*
%{_mandir}/man3/IO::Uncompress::UnXz.3*

%changelog
* Thu Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 2.213-1
- Update to version 2.213
- License verified

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.101-5
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.101-3
- Perl 5.34 rebuild

* Fri Mar 19 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.101-2
- Disable optional tests on ELN

* Sat Feb 20 2021 Paul Howarth <paul@city-fan.org> - 2.101-1
- Update to 2.101 (no changes)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan  7 2021 Paul Howarth <paul@city-fan.org> - 2.100-1
- Update to 2.100
  - Trim whitespace
  - Avoid indirect calls
  - Fix typo

* Sat Aug  1 2020 Paul Howarth <paul@city-fan.org> - 2.096-1
- Update to 2.096
  - Add test for Zip with XZ compression

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.095-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Paul Howarth <paul@city-fan.org> - 2.095-1
- Update to 2.095 (no changes)

* Tue Jul 14 2020 Paul Howarth <paul@city-fan.org> - 2.094-1
- Update to 2.094 (no changes)

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.093-4
- Perl 5.32 rebuild

* Fri Feb 14 2020 Petr Pisar <ppisar@redhat.com> - 2.093-3
- Unbundle test dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.093-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec  8 2019 Paul Howarth <paul@city-fan.org> - 2.093-1
- Update to 2.093
  - Fixed minor typo in the pod (GH#3)

* Thu Dec  5 2019 Paul Howarth <paul@city-fan.org> - 2.092-1
- Update to 2.092
  - t/oooprereq.t: Fix list of dumped packages
  - t/oooprereq.t: Dump version data

* Sun Nov 24 2019 Paul Howarth <paul@city-fan.org> - 2.091-1
- Update to 2.091 (no changes)

* Sun Nov 10 2019 Paul Howarth <paul@city-fan.org> - 2.090-1
- Update to 2.090
  - Fix typo: change lzstrem to xzstream

* Sun Nov  3 2019 Paul Howarth <paul@city-fan.org> - 2.089-1
- Update to 2.089 (no changes)

* Sun Nov  3 2019 Paul Howarth <paul@city-fan.org> - 2.088-1
- Update to 2.088
  - Add support details to documentation
  - Beef up reset for zip use-case
  - Remove unnecessary commented code
  - Documentation updates

* Mon Aug 12 2019 Paul Howarth <paul@city-fan.org> - 2.087-1
- Update to 2.087 (no changes)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.086-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.086-2
- Perl 5.30 rebuild

* Mon Apr  1 2019 Paul Howarth <paul@city-fan.org> - 2.086-1
- Update to 2.086
  - Moved source to github: https://github.com/pmqs/IO-Compress-Lzma
  - Add META_MERGE to Makefile.PL
  - Added meta-json.t and meta-yaml.t

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.084-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan  7 2019 Paul Howarth <paul@city-fan.org> - 2.084-1
- Update to 2.084
  - Added support for lzip with IO::Compress::Lzip and
    IO::Uncompress::UnLzip

* Wed Jan  2 2019 Paul Howarth <paul@city-fan.org> - 2.083-1
- Update to 2.083 (no changes)
- Drop legacy Group: tag

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.081-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.081-2
- Perl 5.28 rebuild

* Mon Apr  9 2018 Paul Howarth <paul@city-fan.org> - 2.081-1
- Update to 2.081
  - Previous release used $^W instead of use warnings - fixed

* Wed Apr  4 2018 Paul Howarth <paul@city-fan.org> - 2.080-1
- Update to 2.080 (no changes)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.074-2
- Perl 5.26 rebuild

* Mon Feb 20 2017 Paul Howarth <paul@city-fan.org> - 2.074-1
- Update to 2.074
  - ISA fixes for c3 (CPAN RT#120239)

* Mon Feb 13 2017 Paul Howarth <paul@city-fan.org> - 2.072-1
- Update to 2.072
  - Fix for Makefile.PL depending on . in @INC (CPAN RT#120084)
- Run additional tests by specifying COMPRESS_ZLIB_RUN_MOST

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.070-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Paul Howarth <paul@city-fan.org> - 2.070-1
- Update to 2.070 (no changes)
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.069-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.069-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Sep 27 2015 Paul Howarth <paul@city-fan.org> - 2.069-1
- Update to 2.069 (no changes)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.068-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-2
- Perl 5.22 rebuild

* Wed Dec 24 2014 Paul Howarth <paul@city-fan.org> - 2.068-1
- Update to 2.068 (no changes)

* Tue Dec  9 2014 Paul Howarth <paul@city-fan.org> - 2.067-1
- Update to 2.067 (no changes)
- Classify buildreqs by usage

* Mon Sep 22 2014 Paul Howarth <paul@city-fan.org> - 2.066-1
- Update to 2.066 (no changes)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.064-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.064-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb  2 2014 Paul Howarth <paul@city-fan.org> - 2.064-1
- Update to 2.064 (no changes)

* Sun Nov  3 2013 Paul Howarth <paul@city-fan.org> - 2.063-1
- Update to 2.063 (no changes)

* Mon Aug 12 2013 Paul Howarth <paul@city-fan.org> - 2.062-1
- Update to 2.062
  - Typo fixes (CPAN RT#86578)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.061-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 2.061-2
- Perl 5.18 rebuild

* Mon May 27 2013 Paul Howarth <paul@city-fan.org> - 2.061-1
- Update to 2.061
  - Fix IO::Uncompress::UnXz v2.060 memLimit option bug (CPAN RT#84966)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.060-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Paul Howarth <paul@city-fan.org> - 2.060-1
- Update to 2.060 (no changes)

* Sun Dec 16 2012 Paul Howarth <paul@city-fan.org> - 2.059-1
- Update to 2.059 (no changes)

* Tue Nov 13 2012 Paul Howarth <paul@city-fan.org> - 2.058-1
- Update to 2.058 (general performance improvements)

* Mon Aug  6 2012 Paul Howarth <paul@city-fan.org> - 2.055-1
- Update to 2.055 (no changes)
- BR: perl(Carp), perl(constant), perl(File::Spec), perl(IO::Handle) and
  perl(lib)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.052-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 2.052-2
- Perl 5.16 rebuild

* Sun Apr 29 2012 Paul Howarth <paul@city-fan.org> - 2.052-1
- Update to 2.052 (no changes)
- Don't need to remove empty directories from buildroot
- Package examples
- Drop %%defattr, redundant since rpm 4.4

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 2.049-1
- Update to 2.049 (no changes)

* Sun Jan 29 2012 Paul Howarth <paul@city-fan.org> - 2.048-1
- Update to 2.048
  - Set minimum Perl version to 5.6

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.045-2
- Fedora 17 mass rebuild

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Moved FAQ.pod to IO::Compress

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.044-1
- Update to 2.044
  - Moved FAQ.pod under the lib directory so it can get installed

* Mon Nov 21 2011 Paul Howarth <paul@city-fan.org> - 2.043-1
- Update to 2.043 (no changes)

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 2.042-1
- Update to 2.042 (no changes)
- Resync versioned dependencies on IO::Compress::Base and Compress::Raw::Lzma

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.041-1
- Update to 2.041
  - Remove debugging line in t/001lzma.t that writes to /tmp (CPAN RT#72023)
- Update version requirements for IO::Compress and Compress::Raw::Lzma

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - Fixed uncompression issue in IO::Uncompress::UnLzma (CPAN RT#71114)

* Fri Jun 24 2011 Paul Howarth <paul@city-fan.org> - 2.038-2
- Perl mass rebuild

* Fri Jun 24 2011 Paul Howarth <paul@city-fan.org> - 2.038-1
- Update to 2.038
  - Fixed missing SKIP label in t/050interop-zip-lzma.t
- Hard-code version requirements for IO::Compress and Compress::Raw::Lzma
  until the next synchronized release happens

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037
  - Handle "Cannot Allocate Memory" issue with Extreme test in
    t/105oneshot-zip-lzma-only.t

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-1
- Update to 2.036
  - IO::Compress::Adapter:
    - Added interface to allow creation of LZMA stream for use in a zip file
  - IO::Uncompress::Adapter:
    - Added interface to allow reading of LZMA stream in a zip file
- BR: /usr/bin/7z for additional test coverage

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (fix test failure on Windows - CPAN RT#67931)

* Tue May  3 2011 Paul Howarth <paul@city-fan.org> - 2.034-1
- Update to 2.034 (updates to test harness)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (made 001xz.t more forgiving when the tests run out of memory)

* Fri Jan  7 2011 Paul Howarth <paul@city-fan.org> - 2.032-1
- Update to 2.032 (no changes)

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.030-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon Jul 26 2010 Paul Howarth <paul@city-fan.org> - 2.030-1
- Update to 2.030 (no changes)

* Tue May 11 2010 Paul Howarth <paul@city-fan.org> - 2.027-2
- Drop redundant buildroot tag

* Thu Apr 29 2010 Paul Howarth <paul@city-fan.org> - 2.027-1
- Initial RPM version
