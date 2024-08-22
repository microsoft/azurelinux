# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_indirect_enables_extra_test
%else
%bcond_with perl_indirect_enables_extra_test
%endif

Name:           perl-indirect
Version:        0.39
Release:        6%{?dist}
Summary:        Lexically warn about using the indirect object syntax
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/indirect
Source0:        https://cpan.metacpan.org/authors/id/V/VP/VPIT/indirect-%{version}.tar.gz#/perl-indirect-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Test Suite
BuildRequires:  perl(B)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
# Optional Tests
%if 0%{!?perl_bootstrap:1} && %{with perl_indirect_enables_extra_test}
BuildRequires:  perl(Devel::CallParser)
BuildRequires:  perl(Devel::Declare) >= 0.006007
%endif
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Socket)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(XSLoader)

# Avoid provides for perl shared objects
%{?perl_default_filter}

%description
When enabled (or disabled as some may prefer to say, since you actually
turn it on by calling no indirect), this pragma warns about indirect object
syntax constructs that may have slipped into your code.

%prep
%setup -q -n indirect-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README samples/
%{perl_vendorarch}/auto/indirect/
%{perl_vendorarch}/indirect.pm
%{_mandir}/man3/indirect.3*

%changelog
* Thu Aug 22 2024 Neha Agarwal <nehaagrwal@microsoft.com> - 0.39-6
- Promote package to Core repository.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.39-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov  6 2019 Paul Howarth <paul@city-fan.org> - 0.39-3
- Avoid need for bootstrapping EPEL builds

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul  8 2019 Paul Howarth <paul@city-fan.org> - 0.39-1
- Update to 0.39
  - Fix failures on perl ≥ 5.28.0 with -DDEBUGGING (CPAN RT#127118); the
    module has been amended to accommodate with a change of behaviour of a core
    macro
  - Updated contact information

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-8
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-7
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov  6 2017 Paul Howarth <paul@city-fan.org> - 0.38-1
- Update to 0.38
  - Fix compatibility with CV-in-stash optimization (CPAN RT#123374)
- Drop legacy Group: tag

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Paul Howarth <paul@city-fan.org> - 0.37-1
- Update to 0.37
  - A large chunk of boilerplate XS code, which is also used in other XS
    modules, has been factored out of the main .xs file to a collection of .h
    files in the xsh subdirectory
  - Fixed intermittent segfaults with heredocs (CPAN RT#115392)

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-5
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-4
- Perl 5.24 rebuild

* Thu Apr 21 2016 Paul Howarth <paul@city-fan.org> - 0.36-3
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jul 18 2015 Paul Howarth <paul@city-fan.org> - 0.36-1
- Update to 0.36
  - Fix CPAN RT#104312: no indirect 'fatal' will no longer hide compilation
    errors occurring before indirect constructs

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-2
- Perl 5.22 rebuild

* Wed Apr  8 2015 Paul Howarth <paul@city-fan.org> - 0.35-1
- Update to 0.35
  - The module could end being disabled in one thread if it was first loaded in
    another thread and that thread was immediately terminated; this is now
    fixed and should address test failures of t/09-load-threads.t and
    t/42-threads-global.t

* Fri Apr  3 2015 Paul Howarth <paul@city-fan.org> - 0.34-1
- Update to 0.34
  - The new environment variable to enable thread tests on older perls is
    PERL_FORCE_TEST_THREADS; note that this variable should only be turned on
    by authors
  - Add link in documentation to historical tchrist post (CPAN RT#100068)
  - Fix segfaults when the module is loaded by several threads (or Windows
    emulated processes) ran in parallel
  - Update the Windows ActivePerl + gcc 3.4 workaround for ExtUtils::MakeMaker
    version 7.04
  - Be really compatible with the optional OP_PARENT feature
  - Test: $ENV{$Config{ldlibpthname}} is now preserved on all platforms, which
    will address failures of t/41-threads-teardown.t and t/50-external.t with
    unusual compilers (like icc) that link all their compiled objects to their
    own libraries

* Wed Nov 12 2014 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Fix false positives with Devel::Declare (CPAN RT#83806)
  - Fix false positive using ? : syntax (CPAN RT#83839)
  - Fix incorrect RT link in metadata (CPAN RT#84649)
  - no indirect in eval could trigger for direct calls on __PACKAGE__
    (CPAN RT#88428)
  - Author tests are no longer bundled with this distribution
  - Add support for the PERL_OP_PARENT optional feature introduced in
    perl 5.21.2
  - Fix tests that use run_perl(), which fail on Android (CPAN RT#92806)
  - indirect constructs will no longer segfault while inside the empty
    package on perl 5.8.x; this fix may also prevent some segfaults during
    global destruction
  - Stop breaking eval in an END block in Win32 pseudo-forks (CPAN RT#99083)
  - Fix segfaults during global destruction of a thread or a pseudo-fork
- Classify buildreqs by usage
- Make %%files list more explicit
- Package samples directory as documentation

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-9
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-8
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb  4 2014 Paul Howarth <paul@city-fan.org> - 0.29-5
- Build for epel7 bootstrap done

* Fri Jan 31 2014 Paul Howarth <paul@city-fan.org> - 0.29-4
- Don't pull in Devel::CallParser when bootstrapping
- Bootstrap epel7 build

* Wed Aug 07 2013 Petr Pisar <ppisar@redhat.com> - 0.29-3
- Perl 5.18 rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Iain Arnell <iarnell@gmail.com> 0.29-1
- update to latest upstream version

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 0.27-1
- update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.26-3
- Perl 5.16 rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 06 2011 Iain Arnell <iarnell@gmail.com> 0.26-1
- update to latest upstream version

* Sun Aug 28 2011 Iain Arnell <iarnell@gmail.com> 0.25-1
- update to latest upstream version

* Wed Aug 24 2011 Iain Arnell <iarnell@gmail.com> 0.24-2
- remove unnecessary explicit BR on perl

* Thu Aug 11 2011 Iain Arnell <iarnell@gmail.com> 0.24-1
- Specfile autogenerated by cpanspec 1.78.
