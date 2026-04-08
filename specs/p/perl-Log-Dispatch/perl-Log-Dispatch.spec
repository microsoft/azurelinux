# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Supported rpmbuild options:
#
# --with email_tests ... also check sending e-mails.
#     Default: --without (Exclude e-mail tests)
%bcond_with     release_tests
# --without httpd ... do not build ApacheLog logging output for httpd.
#     Default: --with (Build ApacheLog)
%if 0%{?rhel} >= 9
%bcond_with     httpd
%else
%bcond_without     httpd
%endif
# --with release_tests ... also check "RELEASE_TESTS".
#     Default: --without (Exclude tests)
%bcond_with     release_tests

Name:           perl-Log-Dispatch
Version:        2.71
Release:        7%{?dist}
Summary:        Dispatches messages to one or more outputs
License:        Artistic-2.0
URL:            https://metacpan.org/release/Log-Dispatch
Source0:        https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Log-Dispatch-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
# Apache2::Log not used at tests
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::GlobalDestruction)
BuildRequires:  perl(Dist::CheckConflicts) >= 0.02
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
#BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Run3)
BuildRequires:  perl(JSON::PP) >= 2.27300
BuildRequires:  perl(lib)
BuildRequires:  perl(Mail::Send)
BuildRequires:  perl(Mail::Sender)
BuildRequires:  perl(Mail::Sendmail)
BuildRequires:  perl(MIME::Lite)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Params::ValidationCompiler)
BuildRequires:  perl(parent)
BuildRequires:  perl(PerlIO)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Specio) >= 0.32
BuildRequires:  perl(Specio::Declare)
BuildRequires:  perl(Specio::Exporter)
BuildRequires:  perl(Specio::Library::Builtins)
BuildRequires:  perl(Specio::Library::Numeric)
BuildRequires:  perl(Specio::Library::String)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sys::Syslog) >= 0.28
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)

# Optional
BuildRequires:  perl(CPAN::Meta) >= 2.120900

# testsuite
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)

# If LOG_DISPATCH_TEST_EMAIL is passed to tests, a sendmail will be needed,
# bug #1083418
BuildRequires:  %{_sbindir}/sendmail

%if %{with release_tests} 
# for improved tests
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildRequires:  perl(Test::EOL)
BuildRequires:  perl(Test::NoTabs)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Spelling)
BuildRequires:  perl(Test::CPAN::Changes)
BuildRequires:  perl(Test::Mojibake)
BuildRequires:  perl(Test::Portability::Files)
BuildRequires:  perl(Test::Version)
BuildRequires:  perl(Test::Code::TidyAll) > 0.24

# Required by t/release-pod-no404s.t
# Likely a bug underneath of Test::Pod::No404s
BuildRequires:  perl(LWP::Protocol::https)
%endif

# Ouch - Introduced by upstream in 2.40
Conflicts:      perl(Log::Dispatch::File::Stamped) >= 0.10


%description
Log::Dispatch is a suite of OO modules for logging messages to
multiple outputs, each of which can have a minimum and maximum log
level.  It is designed to be easily subclassed, both for creating a
new dispatcher object and particularly for creating new outputs.
An Apache output is available in perl-Log-Dispatch-ApacheLog package.

%if %{with httpd}
%package ApacheLog
Summary:        Log::Dispatch output for logging to Apache::Log objects
Requires:       %{name} = %{?epoch:%{epocho}:}%{version}-%{release}
Requires:       perl(Apache2::Log)
Conflicts:      perl-Log-Dispatch < 2.70-2

%description ApacheLog
This Perl module enables you to pass messages to Apache's log object,
represented by the Apache::Log class.
%endif


%prep
%setup -q -n Log-Dispatch-%{version}

%build
%{__perl} Makefile.PL installdirs=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{__make} test %{?with_release_tests:RELEASE_TESTING=1} \
    %{?with_email_tests:LOG_DISPATCH_TEST_EMAIL="root@localhost.localdomain"}

%files
%doc Changes
%license LICENSE
%{perl_vendorlib}/Log/
%exclude %{perl_vendorlib}/Log/Dispatch/ApacheLog.pm
%{_mandir}/man3/*.3pm*
%exclude %{_mandir}/man3/Log::Dispatch::ApacheLog.3pm*

%if %{with httpd}
%files ApacheLog
%{perl_vendorlib}/Log/Dispatch/ApacheLog.pm
%{_mandir}/man3/Log::Dispatch::ApacheLog.3pm*
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 12 2023 Tom Callaway <spot@fedoraproject.org> - 2.71-1
- update to 2.71

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.70-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.70-9
- Modernize spec.
- Convert license to SPDX.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.70-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.70-7
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.70-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.70-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.70-4
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Petr Pisar <ppisar@redhat.com> - 2.70-2
- Correct perl(Apache2::Log) dependency (bug #1914939)
- Move Log::Dispatch::ApacheLog to perl-Log-Dispatch-ApacheLog subpackage
  (bug #1914939)
- Disable perl-Log-Dispatch-ApacheLog on RHEL ≥ 9 (bug #1914939)
- Modernize a spec file
- Do not send e-mails when running tests (bug #1414996)

* Fri Jul 31 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.70-1
- Update to 2.70.
- Remove outdated comments.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.69-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.69-4
- Perl 5.32 rebuild

* Thu Mar 19 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.69-3
- Specify all dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 29 2019 Tom Callaway <spot@fedoraproject.org> - 2.69-1
- update to 2.69

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.68-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.68-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 27 2018 Tom Callaway <spot@fedoraproject.org> - 2.68-1
- update to 2.68

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.67-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.67-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 25 2017 Tom Callaway <spot@fedoraproject.org> - 2.67-1
- update to 2.67

* Tue Aug 29 2017 Tom Callaway <spot@fedoraproject.org> - 2.66-1
- update to 2.66

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Tom Callaway <spot@fedoraproject.org> - 2.65-1
- update to 2.65

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.63-2
- Perl 5.26 rebuild

* Mon Feb 20 2017 Tom Callaway <spot@fedoraproject.org> - 2.63-1
- update to 2.63

* Tue Feb 14 2017 Paul Howarth <paul@city-fan.org> - 2.62-1
- update to 2.62
- re-enable tests - Devel::Confess added by mistake in 2.60

* Mon Feb 13 2017 Tom Callaway <spot@fedoraproject.org> - 2.60-1
- update to 2.60
- disabling tests until Devel::Confess shows up

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 15 2016 Tom Callaway <spot@fedoraproject.org> - 2.58-1
- update to 2.58

* Thu Aug 18 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.57-1
- Update to 2.57.
- Add BR: perl(Module::Runtime).
- Add BR: perl(Test::Needs), remove perl(Test::Requires).

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.56-2
- Perl 5.24 rebuild

* Mon May  9 2016 Tom Callaway <spot@fedoraproject.org> - 2.56-1
- update to 2.56

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.54-3
- Modernize spec.

* Sat Jan 23 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.54-2
- Add BR: perl(Exporter).

* Tue Jan 19 2016 Tom Callaway <spot@fedoraproject.org> - 2.54-1
- Update to 2.54.

* Sat Jan 16 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.53-2
- Add BR: perl(POSIX).

* Fri Jan 15 2016 Tom Callaway <spot@fedoraproject.org> - 2.53-1
- Update to 2.53.

* Thu Jan 14 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.52-1
- Update to 2.52.
- Add BR: perl(JSON::PP).
- Remove BR: perl(Test::Pod::No404s).

* Mon Sep 21 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.51-1
- Update to 2.51.
- Add BR: perl(CPAN::Meta).

* Mon Aug 24 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.50-1
- Update to 2.50 (Upstream fix to RHBZ#1258940).
- Add BR: perl(Encode).

* Mon Aug 24 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.49-1
- Upstream update.

* Sat Aug 08 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.48-1
- Upstream update.
- Update deps.

* Sat Aug 08 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.46-1
- Upstream update.
- BR: perl(Params::Validate) >= 1.03.

* Sat Aug 08 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.45-1
- Upstream update.
- Introduce %%license.
- Drop Log-Dispatch-2.42.diff.
- Update deps.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.44-2
- Perl 5.22 rebuild

* Tue Oct 21 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.44-1
- Upstream update.

* Mon Oct 13 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.43-1
- Upstream update.

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.42-2
- Perl 5.20 rebuild

* Mon Aug 18 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.42-1
- Upstream update.
- Reflect dep changes.
- Add Log-Dispatch-2.42.diff.
- Remove Log-Dispatch-2.38.diff

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 Petr Pisar <ppisar@redhat.com> - 2.41-2
- Build-require a sendmail program for tests (bug #1083418)

* Fri Aug 16 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.41-1
- Upstream update.
- Spec cleanup.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 2.40-2
- Perl 5.18 rebuild

* Fri Jul 12 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.40-1
- Upstream update.
- Add Conflicts: perl(Log::Dispatch::File::Stamped) >= 0.10.
- Add %%bcond_with release_tests (Default to without, because RELEASE_TESTING
  is currently broken).

* Wed Apr 17 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.38-1
- Upstream update.

* Mon Feb 04 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.35-1
- Upstream update.

* Wed Dec 12 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.34-3
- Add %%bcond_with network (Test::Pod::No404 based tests fail in koji).

* Wed Dec 12 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.34-2
- Fix broken condition to BR: perl(Test::Pod::No404s).
- Conditionally BR: perl(LWP::Protocol::https).

* Tue Dec 11 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.34-1
- Upstream update.
- Update BR:s.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 2.29-2
- Perl 5.16 rebuild

* Mon Feb 06 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.29-1
- Upstream update.
- Remove --with mailtests build option (unnecessary).
- Remove Log-Dispatch-2.11-enable-mail-tests.patch (rotten, obsolete).
- Rework spec.
- Enable release tests.
- Make hunspell checks working.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.27-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.27-1
- update to 2.27

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.22-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.22-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.22-2
- BR: perl(Test::Kwalitee).

* Wed Nov 26 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.22-1
- Upstream update.

* Fri Mar 14 2008 Ralf Corsépius <rc040203@freenet.de> - 2.21-1
- Upstream update.
- BR: perl(Apache2::Log) instead of mod_perl.
- Add BR: Test::Pod::Coverage, activate IS_MAINTAINER checks.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-1
- bump to 2.20

* Sat Jun  9 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.18-1
- Update to 2.18.

* Wed Dec 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.16-1
- Update to 2.16.
- Removed perl(IO::String) from the BR list (no longer needed).

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-2
- New build requirement: perl(IO::String).

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-1
- Update to 2.15.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-2
- Log-Dispatch-2.11-mod_perl2.patch no longer needed.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-1
- Update to 2.14.

* Tue Sep 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.13-1
- Update to 2.13.

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.12-1
- Update to 2.12.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Sep 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-3
- Exclude mod_perl from the requirements list
  (overkill for most applications using Log::Dispatch).

* Mon Sep 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-2
- Better mod_perl handling.

* Fri Sep 09 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-1
- First build.
