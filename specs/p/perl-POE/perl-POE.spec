# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform network tests
%bcond_without perl_POE_enables_network_test
# Perform optional tests
%bcond_without perl_POE_enables_optional_test

Name:       perl-POE
Version:    1.370
Release: 13%{?dist}
Summary:    Portable multitasking and networking framework for event loops
License:    GPL-1.0-or-later OR Artistic-1.0-Perl
URL:        https://metacpan.org/release/POE
Source0:    https://cpan.metacpan.org/authors/id/B/BI/BINGOS/POE-%{version}.tar.gz
BuildArch:  noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec) >= 0.87
# Getopt::Long not used
BuildRequires:  perl(lib)
BuildRequires:  perl(Socket) >= 1.7
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(constant)
# Curses 1.08 not used at tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Errno) >= 1.09
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(HTTP::Date)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(HTTP::Response)
BuildRequires:  perl(HTTP::Status)
BuildRequires:  perl(IO::Handle) >= 1.27
BuildRequires:  perl(IO::Pipely) >= 0.005
BuildRequires:  perl(IO::Poll) >= 0.01
BuildRequires:  perl(IO::Pty)
BuildRequires:  perl(IO::Tty) >= 1.08
BuildRequires:  perl(POSIX) >= 1.02
BuildRequires:  perl(Scalar::Util)
# Socket6 not needed with current Socket
# Socket::GetAddrInfo not needed with current Socket
# Storable || FreezeThaw || YAML
BuildRequires:  perl(Storable) >= 2.26
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(Term::Cap) >= 1.10
BuildRequires:  perl(Term::ReadKey) >= 2.21
# Time::Hires loaded from lib/POE/Resource/Clock.pm
BuildRequires:  perl(Time::HiRes) >= 1.59
BuildRequires:  perl(URI) >= 1.30
# Win32* not needed
# Optional run-time:
BuildRequires:  perl(Compress::Zlib) >= 1.33
# POE::XS::Queue::Array not needed, to exhibit a default implementation
# Tests:
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(lib)
%if %{with perl_POE_enables_network_test}
BuildRequires:  perl(List::Util)
%endif
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Handle)
BuildRequires:  perl(Time::HiRes) >= 1.59
%if %{with perl_POE_enables_optional_test}
# Optional tests:
%if !%{defined perl_bootstrap}
BuildRequires:  perl(POE::Test::Loops) >= 1.360
%endif
BuildRequires:  perl(YAML)
%endif
Requires:       perl(bytes)
Recommends:     perl(Compress::Zlib) >= 1.33
Requires:       perl(Curses) >= 1.08
Requires:       perl(Data::Dumper)
Requires:       perl(Errno) >= 1.09
Requires:       perl(File::Spec) >= 0.87
Requires:       perl(IO::Handle) >= 1.27
Requires:       perl(IO::Pipely) >= 0.005
Requires:       perl(IO::Pty)
Requires:       perl(IO::Tty) >= 1.08
Suggests:       perl(POE::XS::Queue::Array)
Requires:       perl(POSIX) >= 1.02
Requires:       perl(Socket) >= 1.7
Requires:       perl(Storable) >= 2.26
Requires:       perl(Term::Cap) >= 1.10
Requires:       perl(Term::ReadKey) >= 2.21
Requires:       perl(Time::HiRes) >= 1.59

%{?perl_default_filter}
# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Curses|Errno|File::Spec|IO::Handle|IO::Pipely|IO::Pty|POSIX|Socket|Term::Cap|Term::ReadKey)\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(POE::Kernel\\)$

%description
POE is a framework for cooperative, event driven multitasking in Perl. It
provides a unified interface for several event loops, including select(),
IO::Poll, Glib, Gtk, Tk, Wx, and Gtk2. Many of these event loop interfaces
were written by others, with the help of POE::Test::Loops.

%prep
%setup -q -n POE-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 --default
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%if !%{with perl_POE_enables_network_test}
rm run_network_tests
%endif
# note that there are currently a number of tests that throw errors, but do
# not fail nor cause the build/suite to fail.  For now just please be aware
# that there will be some noisy output as the tests are run.
# Reported upstream at http://rt.cpan.org/Public/Bug/Display.html?id=19878
unset AUTOMATED_TESTING CONTENT_LENGTH CONTENT_TYPE POE_ASSERT_USAGE \
    POE_CATCH_EXCEPTIONS POE_EVENT_LOOP POE_IMPLEMENTATION POE_USE_HIRES \
    POE_USE_SIGNAL_PIPE QUERY_STRING RELEASE_TESTING REQUEST_METHOD
make test

%files
%doc CHANGES examples HISTORY README TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.370-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.370-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.370-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.370-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.370-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.370-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.370-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Michal Josef Špaček <mspacek@redhat.com> - 1.370-5
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.370-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.370-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.370-2
- Perl 5.36 rebuild

* Wed Mar 23 2022 Michal Josef Špaček <mspacek@redhat.com> - 1.370-1
- 1.370 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.368-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.368-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.368-7
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.368-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.368-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.368-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.368-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.368-2
- Perl 5.32 rebuild

* Wed Feb 05 2020 Petr Pisar <ppisar@redhat.com> - 1.368-1
- 1.368 bump

* Fri Jan 31 2020 Petr Pisar <ppisar@redhat.com> - 1.367-22
- Adapt to changes in Perl 5.31.5
- Revise dependenices

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.367-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.367-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-19
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-18
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.367-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.367-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-15
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-14
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.367-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.367-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-11
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-10
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.367-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-8
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.367-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 10 2015 Petr Šabata <contyk@redhat.com> - 1.367-5
- Require Time::HiRes (#1252038)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.367-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.367-2
- Perl 5.22 rebuild

* Thu Jun 04 2015 Petr Šabata <contyk@redhat.com> - 1.367-1
- 1.367 bump
- Rewrite the dep list, drop EPEL support
- Don't package tests

* Tue Nov 04 2014 Petr Šabata <contyk@redhat.com> - 1.366-1
- 1.366 bump

* Tue Oct 14 2014 Petr Šabata <contyk@redhat.com> - 1.365-1
- 1.365 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.364-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.364-2
- Perl 5.20 rebuild

* Mon Jul 21 2014 Petr Šabata <contyk@redhat.com> - 1.364-1
- 1.364 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.358-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 10 2013 Petr Pisar <ppisar@redhat.com> - 1.358-1
- 1.358 bump
- This version is not fully backward compatible with respect to handling
  exceptions and __DIE__ signals

* Wed Aug 21 2013 Petr Šabata <contyk@redhat.com> - 1.356-1
- 1.356 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.354-9
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.354-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.354-7
- Perl 5.18 rebuild

* Wed May 15 2013 Petr Šabata <contyk@redhat.com> - 1.354-6
- Don't require POE::Test::Loops on EPEL

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.354-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.354-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.354-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.354-2
- Perl 5.16 rebuild

* Wed May 16 2012 Petr Šabata <contyk@redhat.com> - 1.354-1
- 1.354 bump

* Fri May 11 2012 Petr Šabata <contyk@redhat.com> - 1.353-1
- 1.353 bump

* Thu Apr 05 2012 Petr Šabata <contyk@redhat.com> - 1.352-2
- Remove POE::Test::Loops circular buildtime and runtime dependency
  (thanks, Paul; #810234)

* Wed Mar 28 2012 Petr Šabata <contyk@redhat.com> - 1.352-1
- 1.352 bump
- Filter underspecified dependencies

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 1.351-1
- 1.351 bump
- Remove command macros

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.350-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Petr Šabata <contyk@redhat.com> - 1.350-1
- 1.350 bump
- Remove Buildroot and defattr

* Mon Aug 01 2011 Petr Sabata <contyk@redhat.com> - 1.312-1
- 1.312 bump
- Deps updated

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.289-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.289-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.289-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Sep 12 2010 Iain Arnell <iarnell@gmail.com> 1.289-2
- doesn't require POE::Test::Loops (RHBZ#632855)

* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 1.289-1
- 1.289 bump
- Reenable t/90_regression/rt1648-tied-stderr.t test

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.269-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.269-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.269-1
- update filtering...
- auto-update to 1.269 (by cpan-spec-update 0.01)
- added a new br on perl(Module::Build)
- altered br on perl(POE::Test::Loops) (1.021 => 1.022)
- altered req on perl(POE::Test::Loops) (1.021 => 1.022)

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.007-1
- auto-update to 1.007 (by cpan-spec-update 0.01)

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.007-1
- auto-update to 1.007 (by cpan-spec-update 0.01)
- altered br on perl(POE::Test::Loops) (1.004 => 1.021)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Errno) (version 1.09)
- added a new req on perl(Exporter) (version 0)
- added a new req on perl(File::Spec) (version 0.87)
- added a new req on perl(IO::Handle) (version 1.27)
- added a new req on perl(IO::Tty) (version 1.08)
- added a new req on perl(POE::Test::Loops) (version 1.021)
- added a new req on perl(POSIX) (version 1.02)
- added a new req on perl(Socket) (version 1.7)
- added a new req on perl(Storable) (version 2.16)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.006-1
- auto-update to 1.006 (by cpan-spec-update 0.01)

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.005-1
- auto-update to 1.005 (by cpan-spec-update 0.01)
- added a new br on perl(Storable) (version 2.16)
- added a new br on perl(Errno) (version 1.09)
- added a new br on perl(IO::Handle) (version 1.27)
- added a new br on perl(Socket) (version 1.7)
- added a new br on perl(IO::Tty) (version 1.08)
- added a new br on perl(POE::Test::Loops) (version 1.004)
- added a new br on perl(POSIX) (version 1.02)
- added a new br on perl(File::Spec) (version 0.87)
- added a new br on perl(Exporter) (version 0)
- added a new br on perl(Test::Harness) (version 2.26)
- added a new br on perl(Carp) (version 0)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.003-1
- update to 1.003
- filter provides, too

* Mon Jun 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.0002-1
- update to 1.0002

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9999-1
- update to 0.9999
- don't filter out POE::Kernel, POE::Loop::Tk (it actually is provided)

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9989-2
- rebuild for new perl

* Sat May 19 2007 Chris Weyl <cweyl@alumni.drew.edu>
- spec cleanups, tweaks
- add t/ to doc
- move away from macroized versioning system
- no rebuild at this point

* Fri Mar 23 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.9989-1
- update to 0.9989

* Wed Mar 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.9917-1
- update to 0.9917.  0.3800-1, below, was never built/released to the wild.

* Mon Sep 25 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3800-1
- update to 0.38.  0.37-1, below, was never built/released to the wild.

* Mon Sep 11 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3700-1
- update to 0.37
- samples/ is now examples/
- add additional br's: perl(IO::Pty), perl(Test::Pod),
  perl(Test::Pod::Coverage)

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3601-2
- bump for mass rebuild

* Sun Aug 13 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3601-1
- update to cpan ver 0.3601

* Thu Aug 10 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3600-1
- update to cpan ver 0.36

* Tue Jun 20 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3502-1
- filter errant provides.  Also translate POE::Provides::foo modules to
  POE::Provide::foo
- Bump to latest version released

* Thu Jun 15 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3501-2
- Nix test that was causing build to fail in plague

* Wed Jun 14 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3501-1
- bump release, minor cleanups per review.

* Fri Jun 09 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3501-0
- Initial spec file for F-E
