# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Enable curses on PTY
%bcond_without perl_POE_Test_Loops_enables_curses

Name:           perl-POE-Test-Loops
Summary:        Reusable tests for POE::Loop authors
Version:        1.360
Release: 33%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Source0:        https://cpan.metacpan.org/authors/id/R/RC/RCAPUTO/POE-Test-Loops-%{version}.tar.gz 
URL:            https://metacpan.org/release/POE-Test-Loops
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
# File::Temp not used at tests
# Getopt::Long not used at tests
# IO::File not used at tests
# IO::Handle not used at tests
# IO::Pipely not used at tests
# IO::Socket not used at tests
# IO::Socket::INET not used at tests
BuildRequires:  perl(lib)
# POE not used at tests
# POE::Component::Client::TCP not used at tests
# POE::Component::Server::TCP not used at tests
# POE::Driver::SysRW not used at tests
# POE::Filter::Block not used at tests
# POE::Filter::Line not used at tests
# POE::Filter::Map not used at tests
# POE::Filter::Stream not used
# POE::NFA not used at tests
# POE::Pipe::OneWay not used at tests
# POE::Pipe::TwoWay not used at tests
# POE::Session not used at tests
# POE::Wheel::Curses not used at all
# POE::Wheel::FollowTail no used at tests
# POE::Wheel::ListenAccept not used at tests
# POE::Wheel::ReadWrite not used at tests
# POE::Wheel::Run not used at tests
# POE::Wheel::SocketFactory not used at tests
# POSIX not used at tests
# Socket not used at tests
# Symbol not used at tests
BuildRequires:  perl(Test::More) >= 1.001002
# Time::HiRes not used at tests
BuildRequires:  perl(vars)
%if %{with perl_POE_Test_Loops_enables_curses}
# Optional run-time:
# Curses not used at tests
# IO::Pty not used at tests
%endif
# Socket6 not used at all
# Optional tests:
BuildRequires:  perl(Scalar::Util)
Requires:       perl(Carp)
Requires:       perl(POE::Component::Client::TCP)
Requires:       perl(POE::Component::Server::TCP)
Requires:       perl(POE::Driver::SysRW)
Requires:       perl(POE::Filter::Block)
Requires:       perl(POE::Filter::Line)
Requires:       perl(POE::Filter::Map)
Requires:       perl(POE::Pipe::TwoWay)
Requires:       perl(POE::Wheel::FollowTail)
Requires:       perl(POE::Wheel::ListenAccept)
Requires:       perl(POE::Wheel::SocketFactory)
Requires:       perl(Test::More) >= 1.001002
%if %{with perl_POE_Test_Loops_enables_curses}
Suggests:       perl(Curses)
Suggests:       perl(IO::Pty)
%endif

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(Test::More\\)$

# Hide private modules
%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(POE::MySession\\)
%global __provides_exclude %__provides_exclude|perl\\(POE::Kernel\\)
%global __provides_exclude %__provides_exclude|perl\\(PoeTestWorker\\)
%global __provides_exclude %__provides_exclude|perl\\([DIFMOSU].*\\)
%global __provides_exclude %__provides_exclude|perl\\(Switch\\)

%description
POE::Test::Loops contains one function, generate(), which will generate all
the loop tests for one or more POE::Loop subclasses.  The poe-gen-tests manual
page also documents the POE::Test::Loops system in more detail.

%prep
%setup -q -n POE-Test-Loops-%{version}
find . -type f -exec chmod -c -x {} +

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*
%{_bindir}/poe-gen-tests
%{_mandir}/man1/poe-gen-tests.1.gz

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 09 2022 Michal Josef Špaček <mspacek@redhat.com> - 1.360-25
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.360-23
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.360-20
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.360-17
- Perl 5.32 rebuild

* Tue May 05 2020 Petr Pisar <ppisar@redhat.com> - 1.360-16
- Modernize a spec file

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.360-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.360-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.360-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.360-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.360-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.360-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.360-2
- Perl 5.22 rebuild

* Tue Nov 04 2014 Petr Šabata <contyk@redhat.com> - 1.360-1
- 1.360 bump

* Wed Oct 08 2014 Petr Šabata <contyk@redhat.com> - 1.359-1
- 1.359 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.358-2
- Perl 5.20 rebuild

* Fri Jul 18 2014 Petr Šabata <contyk@redhat.com> - 1.358-1
- 1.358 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.354-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 24 2013 Petr Šabata <contyk@redhat.com> - 1.354-1
- 1.354 bump (just meta changes)

* Fri Sep 20 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.353-1
- 1.353 bump

* Wed Aug 21 2013 Petr Šabata <contyk@redhat.com> - 1.352-1
- 1.352 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.351-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.351-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.351-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.351-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.351-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 1.351-1
- 1.351 bump
- Remove commands macros
- Explicitly add all the POE dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.350-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Petr Šabata <contyk@redhat.com> - 1.350-1
- 1.350 bump

* Fri Aug  5 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.312-2
- filter also Switch from provides, just to be sure

* Wed Jul 27 2011 Petr Sabata <contyk@redhat.com> - 1.312-1
- 1.312 bump (needed by current POE)
- Drop Buildroot and defattr support
- Fix dependencies a bit
- Add RPM 4.9 style filters
- Filter POE::Kernel and PoeTestWorker from Provides

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.035-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.035-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.035-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jun  7 2010 Petr Pisar <ppisar@redhat.com> - 1.035-1
- 1.035 bump
- Orthography fix in description

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.033-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.033-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (1.033)

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.022-1
- update filtering
- auto-update to 1.022 (by cpan-spec-update 0.01)

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.021-1
- auto-update to 1.021 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.005-1
- update for submission

* Fri Apr 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.005-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
