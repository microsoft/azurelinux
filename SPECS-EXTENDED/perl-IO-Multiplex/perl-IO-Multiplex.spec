Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:	Manage IO on many file handles
Name:		perl-IO-Multiplex
Version:	1.16
Release:	16%{?dist}
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/IO-Multiplex
Source0:	https://cpan.metacpan.org/authors/id/B/BB/BBB/IO-Multiplex-%{version}.tar.gz#/perl-IO-Multiplex-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	perl-interpreter
BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(FileHandle)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(Socket)
BuildRequires:	perl(strict)
BuildRequires:	perl(Tie::Handle)
BuildRequires:	perl(Time::HiRes)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(IO::Socket)
BuildRequires:	perl(Test)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Time::HiRes)

%description
IO::Multiplex is designed to take the effort out of managing multiple file
handles. It is essentially a really fancy front end to the select system call.
In addition to maintaining the select loop, it buffers all input and output
to/from the file handles. It can also accept incoming connections on one or
more listen sockets.

%prep
%setup -q -n IO-Multiplex-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README TODO
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::Multiplex.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-2
- Perl 5.22 rebuild

* Fri Apr 10 2015 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to 1.16
  - Fix descriptor memory leak: Make $mux->close actually untie *$fh

* Wed Apr  1 2015 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to 1.15
  - Move untie patch to the right place

* Tue Mar 31 2015 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to 1.14
  - Fix 110_ntest to avoid reading from muxed handle
  - Apply patch to prevent untie warnings (CPAN RT#67846)
- This release by BBB → update source URL
- Classify buildreqs by usage
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-10
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.13-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.13-4
- Perl 5.16 rebuild

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.13-2
- Add buildreqs for core modules, which may be dual-lived

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.13-2
- Perl mass rebuild

* Fri Apr 15 2011 Paul Howarth <paul@city-fan.org> - 1.13-1
- Update to 1.13
  - Fix handling of outbuf that contains '0' (CPAN RT#67458)
- Nobody else likes macros for commands

* Thu Feb 24 2011 Paul Howarth <paul@city-fan.org> - 1.12-1
- Update to 1.12
  - Fixes for Windows (CPAN RT#66096)

* Mon Feb 21 2011 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Avoid warning while adding pipe (CPAN RT#16259, CPAN RT#60068)
  - Add EWOULDBLOCK and non-blocking mode for windows (CPAN RT#23982)
  - Fix typo in documentation (CPAN RT#21085)
  - Avoid shutdown after close (CPAN RT#5885, CPAN RT#5715)
  - Use length of outbuf, not exists to see if it is empty
  - Turn "use warnings" on
- This release by MARKOV -> update source URL
- Use %%{_fixperms} rather than our own chmod incantation
- Tidy up %%summary and %%description

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.10-8
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.10-7
- Mass rebuild with perl 5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.10-6
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Paul Howarth <paul@city-fan.org> - 1.10-4
- Fix argument order for find with -depth
- Include TODO
- Cosmetic changes

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.10-1
- Update to 1.10, upstream found and relicensing has happened!

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.09-1
- Rebuild for new perl
- 1.09

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-5.1
- Add BR: perl(ExtUtils::MakeMaker)

* Fri Sep 15 2006 Leif O M Bergman <lmb@biosci.ki.se> - 1.08-5
- Add dist tag

* Tue Dec 13 2005 Leif O M Bergman <lmb@biosci.ki.se> - 1.08-4
- Changes for fedora xtras compliance

* Mon Dec 12 2005 Leif O M Bergman <lmb@biosci.ki.se> - 1.08-3
- Cosmetic changes for fedora xtras

* Sun Feb 20 2005 Dag Wieers <dag@wieers.com> - 1.08-2
- Cosmetic changes

* Thu Mar 18 2004 Dag Wieers <dag@wieers.com> - 1.08-1
- Updated to release 1.08

* Mon Jul 14 2003 Dag Wieers <dag@wieers.com> - 1.04-0
- Initial package (using DAR)
