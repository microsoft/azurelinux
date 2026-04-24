# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Mail-Sender
Version:        0.903
# I really wish CPAN maintainers would stop fscking around with versions.
# we went from 0.900003 to 0.901
Epoch:          1
Release: 28%{?dist}
Summary:        Module for sending mails with attachments through an SMTP server

# There is also a clause which says that it may not be used for SPAM.
# However, since spamming is illegal in the US, this isn't really a use restriction.
# Instead, its a friendly reminder of the law, so we won't list it here.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Mail-Sender
Source0:        https://cpan.metacpan.org/authors/id/C/CA/CAPOEIRAB/Mail-Sender-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(MIME::QuotedPrint)
BuildRequires:  perl(Socket)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Tie::Handle)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(Try::Tiny) >= 0.24
BuildRequires:  perl(warnings)

%description
%{summary}.


%prep
%setup -q -n Mail-Sender-%{version}
%{__perl} -pi -e 's/\r\n/\n/' README


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} < /dev/null


%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -delete
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# Remove the Win32 module in order to avoid requiring perl(Win32API::Registry)
find $RPM_BUILD_ROOT -type f -name Win32.pm -delete


%check
make test


%files
# License: perl + spam exception.
# See the main POD page for the copyright information.
# For the Artistic and GPL license text(s), see the perl package.
%doc Changes README
%{perl_vendorlib}/Mail/
%{_mandir}/man3/*.3pm*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 31 2023 Michal Josef Špaček <mspacek@redhat.com> - 1:0.903-21
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.903-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.903-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.903-12
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.903-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.903-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.903-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.903-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 18 2016 Tom Callaway <spot@fedoraproject.org> - 1:0.903-1
- update to 0.903

* Wed Aug 31 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.902-1
- 0.902 bump

* Tue Jul  5 2016 Tom Callaway <spot@fedoraproject.org> - 1:0.901-1
- update to 0.901 (bump epoch for upgrade path)

* Wed Jun 15 2016 Tom Callaway <spot@fedoraproject.org> - 0.900003-1
- update to 0.900003

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.23-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 26 2015 Petr Šabata <contyk@redhat.com> - 0.8.23-4
- Prevent FTBFS by correcting the build time dependency list

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.23-2
- Perl 5.22 rebuild

* Tue Oct 21 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.8.23-1
- Upstream update.
- Spec cleanup.

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.21-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.8.21-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Tom Callaway <spot@fedoraproject.org> - 0.8.21-1
- update to 0.8.21

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.8.16-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.8.16-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8.16-6
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8.16-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.8.16-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.16-2
- missing BR on Test::More

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.16-1
- update to 0.8.16

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.13-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.13-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.13-2
- Update to 0.8.13.

* Wed Mar 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.13-1
- Update to 0.8.13.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.10-3
- Rebuild for FC5 (perl 5.8.8).

* Mon Sep 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.10-2
- License clarification.

* Sat Sep 10 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.10-1
- First build.
