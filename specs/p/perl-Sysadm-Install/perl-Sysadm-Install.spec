# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:	Typical installation tasks for system administrators
Name:		perl-Sysadm-Install
Version:	0.48
Release: 27%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Sysadm-Install
Source0:	https://cpan.metacpan.org/authors/id/M/MS/MSCHILLI/Sysadm-Install-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Archive::Tar)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Encode)
BuildRequires:	perl(Expect)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp) >= 0.16
BuildRequires:	perl(File::Which) >= 1.09
BuildRequires:	perl(HTTP::Request)
BuildRequires:	perl(HTTP::Status)
BuildRequires:	perl(Log::Log4perl) >= 1.00
BuildRequires:	perl(Log::Log4perl::Util)
BuildRequires:	perl(LWP::UserAgent)
BuildRequires:	perl(strict)
BuildRequires:	perl(Term::ReadKey)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Carp)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(utf8)
# Dependencies
Requires:	perl(Archive::Tar)
Requires:	perl(Encode)
Requires:	perl(Expect)
Requires:	perl(HTTP::Request)
Requires:	perl(HTTP::Status)
Requires:	perl(LWP::UserAgent)

%description
"Sysadm::Install" executes shell-like commands performing typical
installation tasks: Copying files, extracting tarballs, calling "make".
It has a "fail once and die" policy, meticulously checking the result of
every operation and calling "die()" immediately if anything fails,
with optional logging of everything.

"Sysadm::Install" also supports a *dry_run* mode, in which it logs
everything, but suppresses any write actions.

%prep
%setup -q -n Sysadm-Install-%{version}

# Fix perl interpreter in eg/mkperl
perl -pi -e 's|/usr/local/bin/perl|/usr/bin/perl|;' eg/mkperl

# Note: not turning off exec bits in examples because they don't
# introduce any unwanted dependencies

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%check
make test TEST_VERBOSE=1

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%files
%doc Changes README eg/
# one-liner is an overly-generic name to include in %%{_bindir} and is included
# as %%doc if needed
%exclude %{_bindir}/one-liner
%{perl_vendorlib}/Sysadm/
%{_mandir}/man3/Sysadm::Install.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-12
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-9
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 16 2016 Paul Howarth <paul@city-fan.org> - 0.48-1
- Update to 0.48
  - Typo fix (CPAN RT#114826)
  - Reopening stderr now after password_read prompt to tty closed it

* Tue May 31 2016 Paul Howarth <paul@city-fan.org> - 0.47-1
- Update to 0.47
  - password_read() now writes the prompt to STDERR (instead of STDOUT), and
    optionally to /dev/tty if specified; this allows for redirecting STDOUT
    (and even STDERR) to a file without losing the password prompt
- BR: perl-generators where available
- Simplify find command using -delete

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 24 2015 Paul Howarth <paul@city-fan.org> - 0.46-1
- Update to 0.46
  - ask() and pick() now support getting the user's response on the tty,
    instead of stdin, so they can be used from within a pipe

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-2
- Perl 5.22 rebuild

* Tue May 26 2015 Paul Howarth <paul@city-fan.org> - 0.45-1
- Update to 0.45
  - Fixed manifest and tests for the Windows platform
- Classify buildreqs by usage

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.44-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Paul Howarth <paul@city-fan.org> - 0.44-1
- Update to 0.44
  - Replaced bin_find() implementation by File::Which
  - tap() with raise_error option set now dies with stderr output, because
    $! isn't set on failed close()

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Aug 01 2013 Petr Pisar <ppisar@redhat.com> - 0.43-2
- Perl 5.18 rebuild

* Tue Mar 19 2013 Paul Howarth <paul@city-fan.org> 0.43-1
- Update to 0.43
  - Using binmode() now for slurp/blurt for compatibility with Win32 systems

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Paul Howarth <paul@city-fan.org> 0.42-1
- Update to 0.42
  - No longer silently remove directories that are in the way before untar()
  - Better error diagnosis on failing untar() tests

* Tue Dec 18 2012 Paul Howarth <paul@city-fan.org> 0.41-1
- Update to 0.41
  - Added home_dir() function returning user's home directory
  - tap() now supports stdout_limit and stderr_limit options to limit log
    verbosity

* Sun Sep 16 2012 Paul Howarth <paul@city-fan.org> 0.40-1
- Update to 0.40
  - Fix Cwd problem on Win32/Mac

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> 0.39-2
- Perl 5.16 rebuild

* Thu May 17 2012 Paul Howarth <paul@city-fan.org> 0.39-1
- Update to 0.39
  - Fixed bin_find to omit directories
  - Added cdback() with reset option

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 31 2011 Paul Howarth <paul@city-fan.org> 0.38-1
- Update to 0.38
  - Fixed Win32 test in 012tap.t

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> 0.37-2
- Perl mass rebuild

* Sun Jun 26 2011 Paul Howarth <paul@city-fan.org> 0.37-1
- Update to 0.37
  - Fix for tap's raise_error option and added test case (CPAN RT#68095)
- Drop redundant defattr()

* Mon May  2 2011 Paul Howarth <paul@city-fan.org> 0.36-1
- Update to 0.36
  - Added owner_cp() to copy uid and gid of a file or directory
  - Added raise_error option for tap()
  - snip() now returns original string (with unprintables replaced) if the data
    length is shorter than $maxlen
- Clean up for modern perl and rpmbuild
- Nobody else likes macros for commands

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> 0.35-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> 0.35-2
- Mass rebuild with perl-5.12.0

* Thu Apr 15 2010 Paul Howarth <paul@city-fan.org> 0.35-1
- Update to 0.35
  - Fix blurt_atomic on Win32 (CPAN RT#54885)
  - Fixed local caller_depth increments
  - Fixed printable() bug masking '-'

* Mon Feb 22 2010 Paul Howarth <paul@city-fan.org> 0.34-1
- Update to 0.34 (documentation update and fixes for Windows)
- BR/R perl(Config), perl(Encode), perl(HTTP::Request), perl(HTTP::Status)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 0.33-2
- Rebuild against perl 5.10.1

* Mon Sep 14 2009 Paul Howarth <paul@city-fan.org> 0.33-1
- Update to 0.33
  - No longer require perl(Encode)
  - Use perl(LWP::UserAgent) rather than perl(LWP::Simple)

* Tue Sep  1 2009 Paul Howarth <paul@city-fan.org> 0.32-1
- Update to 0.32 (make UTF-8 handling configurable, not automatic)

* Fri Aug 28 2009 Paul Howarth <paul@city-fan.org> 0.31-1
- Update to 0.31 (improved UTF-8 support)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul  3 2009 Paul Howarth <paul@city-fan.org> 0.29-1
- Update to 0.29
  - Add proper error handling to print and pipe statements
  - Fix up some "if $dir" cases to protect against a value of "0" in $dir
  - Fix up logcroak calls to use the current logger

* Tue May 12 2009 Paul Howarth <paul@city-fan.org> 0.28-1
- Update to 0.28 (fixed download() with a better check for getstore())

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct  9 2008 Paul Howarth <paul@city-fan.org> 0.27-2
- Incorporate comments from package review (#466223)
  - don't include one-liner in %%{_bindir}
  - tighten up %%description

* Thu Oct  9 2008 Paul Howarth <paul@city-fan.org> 0.27-1
- Initial RPM version
