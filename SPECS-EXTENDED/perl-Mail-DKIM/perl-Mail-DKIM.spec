Summary:        Sign and verify Internet mail with DKIM/DomainKey signatures
Name:           perl-Mail-DKIM
Version:        0.58
Release:        4%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://dkimproxy.sourceforge.net/
Source0:        https://cpan.metacpan.org/authors/id/M/MB/MBRADSHAW/Mail-DKIM-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Carp)
BuildRequires:  perl(Crypt::OpenSSL::RSA) >= 0.24
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Mail::Address)
BuildRequires:  perl(Mail::AuthenticationResults)
BuildRequires:  perl(Net::DNS)
BuildRequires:  perl(Net::DNS::Resolver::Mock)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::RequiresInternet)
BuildRequires:  perl(Test::Simple)
BuildRequires:  perl(YAML::XS)
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{_bindir}/perl -V:version`"; echo $version))
BuildArch:      noarch

%description
This module implements the various components of the DKIM and DomainKeys
message-signing and verifying standards for Internet mail. It currently
tries to implement RFC4871 (for DKIM) and RFC4870 (DomainKeys).

It is required if you wish to enable DKIM checking in SpamAssassin via the
Mail::SpamAssassin::Plugin::DKIM plugin.

%prep
%autosetup -n Mail-DKIM-%{version}
# Make the example scripts non-executable
chmod -x scripts/*.pl
# Use the real path in the shebang
perl -pi -e 's|^#!%{_bindir}/env perl|#!%{_bindir}/perl|' scripts/arcverify.pl
# Remove dos-type line endings
perl -pi -e 's/\r//' doc/qp1.txt

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} %{buildroot}/*

%check
%make_build test

%files
%license README.md
%doc ChangeLog Changes doc HACKING.DKIM TODO scripts/*.pl
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Tue Mar 07 2023 Muhammad Falak <mwani@microsoft.com> - 0.58-4
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.58-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Nov 17 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 0.58-1
- Update to 0.58

* Sun Oct 13 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 0.57-1
- Update to 0.57
- Replace calls to %/usr/bin/perl with /usr/bin/perl

* Sun Aug 25 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 0.56-1
- Update to 0.56
- Replace calls to "make pure_install" with %%{make_install}
- Replace calls to "make" with %%{make_build}
- Pass NO_PERLLOCAL=1 to Makefile.PL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.55-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.55-2
- Perl 5.30 rebuild

* Wed Apr 17 2019 Xavier Bachelot <xavier@bachelot.org> - 0.55-1
- Update to 0.55.
- Don't drop network dependent tests, build checks for internet access.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 21 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 0.54-1
- Update to 0.54
- Fix shebang path in scripts/arcverify.pl
- Fix line endings in doc/qp1.txt

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.53-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.53-2
- Perl 5.28 rebuild

* Mon Jun 18 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.53-1
- 0.53 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-1
- 0.52 bump

* Wed Jan 10 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-1
- 0.50 bump

* Thu Oct 19 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.44-1
- 0.44 bump

* Thu Oct 12 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-1
- 0.43 bump

* Fri Aug 11 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-1
- 0.42 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-1
- 0.41 bump

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-11
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.40-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-9
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.40-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-6
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.40-2
- Perl 5.18 rebuild

* Tue May 21 2013 Nick Bebout <nb@fedoraproject.org> - 0.40-1
- Update to 0.40

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Petr Šabata <contyk@redhat.com> - 0.39-7
- Add missing build dependencies
- Drop command macros

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.39-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.39-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 5 2010 Nick Bebout <nb@fedoraproject.org> - 0.39-1
- Update to 0.39 to fix bug # 659003

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.37-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.37-2
- rebuild against perl 5.10.1

* Wed Sep 9 2009 Warren Togami <wtogami@redhat.com> - 0.37-1
- 0.37

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Kyle VanderBeek <kylev@kylev.com> - 0.33-2
- Revise network-driven testing exclusions.

* Wed Jun 10 2009 Kyle VanderBeek <kylev@kylev.com> - 0.33-1
- Update to 0.33

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 23 2008 Kyle VanderBeek <kylev@kylev.com> - 0.32-3
- Disable some tests that require network access and fail inside koji

* Wed Jun 18 2008 Kyle VanderBeek <kylev@kylev.com> - 0.32-2
- Make example scripts non-executable to avoid dep detection bloat.

* Tue Jun 17 2008 Kyle VanderBeek <kylev@kylev.com> - 0.32-1
- Initial version.
