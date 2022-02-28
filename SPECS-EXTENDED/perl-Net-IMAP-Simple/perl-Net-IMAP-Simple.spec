Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          perl-Net-IMAP-Simple
Version:       1.2212
Release:       6%{?dist}
Summary:       Simple IMAP account handling
License:       GPL+ or Artistic
URL:           https://metacpan.org/release/Net-IMAP-Simple
Source0:       https://cpan.metacpan.org/authors/id/J/JE/JETTERO/Net-IMAP-Simple-%{version}.tar.gz#/perl-Net-IMAP-Simple-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: coreutils
BuildRequires: findutils
BuildRequires: make
BuildRequires: perl-interpreter
BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::Command)
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
# Many of the tests do nothing because they need a real IMAP server defined by
# NIS_TEST_HOST environment variable. Because TCP port cannot be redefined,
# it's not possible to run a fake server as a non-root. Therefore many
# dependencies are not exercised by the tests.
BuildRequires: perl(base)
BuildRequires: perl(Carp)
BuildRequires: perl(IO::File)
BuildRequires: perl(IO::Select)
BuildRequires: perl(IO::Socket)
# IO::Socket::SSL not used at tests
BuildRequires: perl(IPC::Open3)
# Net::SSLeay not used at tests
BuildRequires: perl(overload)
BuildRequires: perl(Parse::RecDescent)
BuildRequires: perl(strict)
BuildRequires: perl(Symbol)
BuildRequires: perl(Tie::Handle)
BuildRequires: perl(warnings)
# Optional run-time:
# IO::Socket::INET6 not used at tests
# Tests:
BuildRequires: perl(Fcntl)
BuildRequires: perl(File::Spec)
BuildRequires: perl(IO::Socket::INET)
BuildRequires: perl(Test)
BuildRequires: perl(Test::More)
BuildRequires: perl(Time::HiRes)
# Optional tests:
# Test::Perl::Critic not used
# Test::Pod 1.00 not used
# Test::Pod::Coverage 1.00 not used
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:      perl(IO::Socket::SSL)
Requires:      perl(Net::SSLeay)

%description
Perl extension for simple IMAP account handling, mostly compatible
with Net::POP3.

%prep
%setup -q -n Net-IMAP-Simple-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 </dev/null
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT

%check
make %{?_smp_mflags} test I_PROMISE_TO_TEST_SINGLE_THREADED=1

%files
%doc README Changes TODO
%dir %{perl_vendorlib}/Net/
%dir %{perl_vendorlib}/Net/IMAP/
%{perl_vendorlib}/Net/IMAP/Simple.pm
%{perl_vendorlib}/Net/IMAP/Simple.pod
%{perl_vendorlib}/Net/IMAP/Simple/PipeSocket.pm
%{perl_vendorlib}/Net/IMAP/SimpleX.pm
%{perl_vendorlib}/Net/IMAP/SimpleX.pod
%{_mandir}/man3/Net::IMAP::Simple.3*
%{_mandir}/man3/Net::IMAP::Simple::PipeSocket.3*
%{_mandir}/man3/Net::IMAP::SimpleX.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2212-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2212-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2212-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.2212-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2212-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.2212-1
- 1.2212 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2211-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.2211-2
- Perl 5.28 rebuild

* Fri May 25 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.2211-1
- 1.2211 bump

* Mon May 14 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.2210-1
- 1.2210 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2209-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 10 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.2209-1
- 1.2209 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2207-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.2207-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2207-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 06 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.2207-1
- 1.2207 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.2206-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 24 2015 Petr Pisar <ppisar@redhat.com> - 1.2206-1
- 1.2206 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1916-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.1916-15
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.1916-14
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1916-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1916-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.1916-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1916-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1916-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.1916-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1916-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1916-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1916-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.1916-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Jun 27 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.1916-3
- Fix Source0 URL (#607876)
- New release after review (#607876)

* Sat Jun 19 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.1916-1
- First package
