# Enable optional MLDBM support
%if 0%{?rhel}
%bcond_with perl_IO_All_enables_mldbm
%else
%bcond_without perl_IO_All_enables_mldbm
%endif
# Run optional test
%bcond_without perl_IO_All_enables_optional_test
# Run extra test
%if 0%{?rhel}
%bcond_with perl_IO_All_enables_extra_test
%else
%bcond_without perl_IO_All_enables_extra_test
%endif

Name:           perl-IO-All
Version:        0.87
Release:        11%{?dist}
Summary:        IO::All Perl module
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/IO-All
Source0:        https://cpan.metacpan.org/authors/id/F/FR/FREW/IO-All-%{version}.tar.gz#/perl-IO-All-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Glob)
BuildRequires:  perl(File::MimeInfo)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::ReadBackwards)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Socket)
%if %{with perl_IO_All_enables_mldbm}
BuildRequires:  perl(MLDBM)
%endif
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Tie::File)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(diagnostics)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
%if %{with perl_IO_All_enables_optional_test}
# Optional Tests
BuildRequires:  perl(PerlIO::encoding)
%endif
%if %{with perl_IO_All_enables_extra_test}
# Extra Tests
BuildRequires:  perl(Test::Pod) >= 1.41
%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Copy)
Requires:       perl(File::MimeInfo)
Requires:       perl(File::Path)
Requires:       perl(File::ReadBackwards)
Requires:       perl(IO::Handle)
%if %{with perl_IO_All_enables_mldbm}
Recommends:     perl(MLDBM)
%endif
Requires:       perl(Tie::File)
Requires:       perl(warnings)

%description
The IO::All object is a proxy for IO::File, IO::Dir, IO::Socket,
IO::String, Tie::File, File::Spec, File::Path and File::ReadBackwards; as
well as all the DBM and MLDBM modules. You can use most of the methods
found in these classes and in IO::Handle (which they inherit from). IO::All
adds dozens of other helpful idiomatic methods including file stat and
manipulation functions.

%prep
%setup -q -n IO-All-%{version}
find -type f -perm /0100 -name '*.pm' -exec chmod -c a-x {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
%if %{with perl_IO_All_enables_extra_test}
RELEASE_TESTING=1
%else
unset RELEASE_TESTING
%endif
make %{?_smp_mflags} test

%files
%license LICENSE
%doc Changes CONTRIBUTING README example/
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::All.3*
%{_mandir}/man3/IO::All::DBM.3*
%{_mandir}/man3/IO::All::Dir.3*
%{_mandir}/man3/IO::All::File.3*
%{_mandir}/man3/IO::All::Filesys.3*
%{_mandir}/man3/IO::All::Link.3*
%{_mandir}/man3/IO::All::MLDBM.3*
%{_mandir}/man3/IO::All::Pipe.3*
%{_mandir}/man3/IO::All::STDIO.3*
%{_mandir}/man3/IO::All::Socket.3*
%{_mandir}/man3/IO::All::String.3*
%{_mandir}/man3/IO::All::Temp.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.87-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.87-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.87-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.87-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.87-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Petr Pisar <ppisar@redhat.com> - 0.87-6
- Recommend MLDBM

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.87-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.87-4
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.87-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Paul Howarth <paul@city-fan.org> - 0.87-1
- Update to 0.87
  - Fix io($dir)->all when files have unicode in names (GH#95)
  - Stop trampling $!
  - Add cmp overload to fix some windows problems (GH#74)
- This release by FREW → update source URL
- Simplify find command using -delete

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-2
- Perl 5.22 rebuild

* Sun Jan  4 2015 Paul Howarth <paul@city-fan.org> - 0.86-1
- Update to 0.86 (revamp docs)
- This release by INGY → update source URL

* Wed Dec 17 2014 Petr Šabata <contyk@redhat.com> - 0.85-1
- Update to 0.85
- A Windows test fix only

* Mon Dec 15 2014 Paul Howarth <paul@city-fan.org> - 0.84-1
- Update to 0.84
  - Allow passing an argument to ->relative
  - Pass separator along when tie'ing (GH#52)
  - Add ->copy method
  - Prefix private methods with underscores

* Fri Nov 14 2014 Petr Pisar <ppisar@redhat.com> - 0.82-1
- 0.82 bump
  - Use bsd_glob for ::Dir->glob

* Thu Nov  6 2014 Paul Howarth <paul@city-fan.org> - 0.81-1
- Update to 0.81
  - Make the Role Call list link to their doc sections
  - Fixed a doc formatting bug

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.79-2
- Perl 5.20 rebuild

* Fri Sep  5 2014 Paul Howarth <paul@city-fan.org> - 0.79-1
- Update to 0.79
  - Add t/000-compile-modules.t
  - Eliminate File::Basename from test/
  - Eliminate spurious trailing whitespace
  - Meta 0.0.2
  - Remove 'use 5.x.x' from code
  - Fix strict/warnings
  - Change testdir to t
  - Replace tabs with spaces
  - Add new overloads from PR/49
  - Doc enhancement (PR/51)

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.68-2
- Perl 5.20 rebuild

* Thu Aug 14 2014 Paul Howarth <paul@city-fan.org> - 0.68-1
- Update to 0.68
  - Fix Copyright years
  - Documentation fixes
- Use %%license

* Thu Jul 17 2014 Paul Howarth <paul@city-fan.org> - 0.66-1
- Update to 0.66
  - Move doc to Swim
  - Fix Meta and add Contributing file
- Include new upstream documentation

* Mon Jun 16 2014 Paul Howarth <paul@city-fan.org> - 0.65-1
- Update to 0.65
  - New badge syntax
  - Changed the ABSTRACT
  - Support recommended modules again

* Tue Jun 10 2014 Paul Howarth <paul@city-fan.org> - 0.63-1
- Update to 0.63
  - Convert release to Zilla::Dist
  - Convert documentation to Kwim
  - Add coveralls badge
- This release by INGY -> update source URL

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May  7 2014 Paul Howarth <paul@city-fan.org> - 0.61-1
- Update to 0.61
  - Fix head() returning prematurely
    (https://github.com/ingydotnet/io-all-pm/issues/44)

* Sat Mar 22 2014 Paul Howarth <paul@city-fan.org> - 0.60-1
- Update to 0.60
  - Fix IO Layer situation

* Fri Mar  7 2014 Paul Howarth <paul@city-fan.org> - 0.59-1
- Update to 0.59
  - Fix possible infinite loop in t/accept.t (GH#42)
  - Fix yet another utf8 validation issue (GH#38)
  - Fix warnings running t/tie.t on Windows (GH#37)

* Mon Mar  3 2014 Paul Howarth <paul@city-fan.org> - 0.58-1
- Update to 0.58
  - Fix canonpath on MSWin32
  - Fix marking files as both binary and utf8 (closes GH#36)

* Fri Feb 14 2014 Paul Howarth <paul@city-fan.org> - 0.57-1
- Update to 0.57
  - Make '' not become / when using io->dir('')
  - Add a fix for io->file("foobar")->assert
  - Make io->file('') not break on Windows systems
  - Fix dangling file handles in tests
  - Make mkdir die if it fails (CPAN RT#61697)
  - Fix possible path test issues, especially in Win32
  - Fix ->binary under -utf8 import mode (CPAN RT#81224)
  - Validate UTF-8 in ->utf8 (CPAN RT#74642)
  - Consistently use :encoding($encoding) (CPAN RT#68512)
  - Pass perms to mkpath in assert_dirpath (CPAN RT#53687)
  - Fix minor POD niggle (CPAN RT#83798)
  - Remove broken test for ->mimetype (CPAN RT#91743)
  - Skip t/encoding.t for perls built without PerlIO::encoding (CPAN RT#26230)
  - Abandon RT in favor of GitHub Issues
  - Remove mentions of unimplemented strict (GH#15)
  - Allow testing on non-SDBM DBM's
  - Change minimum perl version to 5.8.1, and thus remove dep for IO::String
  - Return realpath for canonpath when possible (GH#34)
  - Correctly check exists for ::File, ::Dir, and ::Link
  - Fix test failures on MacOS (CPAN RT#61627/GH#29, CPAN RT#82633/GH#32)
  - Some documentation clean-up around the SYNOPSIS
  - Fix printing to a tie'd object (GH#26)
  - Fix tests if $^X ne 'perl' (GH#35)
- This release by FREW -> update source URL
- Package upstream's README.md file
- Run the Pod test too

* Sat Oct 19 2013 Paul Howarth <paul@city-fan.org> - 0.50-1
- Update to 0.50
  - Fix various tests on Windows (CPAN RT#89609)
  - Fix wrong return precedence (CPAN RT#87200)
- This release by INGY -> update source URL

* Tue Oct  8 2013 Paul Howarth <paul@city-fan.org> - 0.48-1
- Update to 0.48
  - Add ->os method to ::Filesys
  - Switch from Module::Install to Dist::Zilla

* Sun Oct  6 2013 Paul Howarth <paul@city-fan.org> - 0.47-1
- Update to 0.47
  - Add ->glob method to ::Dir
  - Add list based constructors to ::Dir and ::File
  - Add ->mimetype method to ::FileSys
  - Add ->ext method to ::FileSys
  - All tests should be parallelizable
- This release by FREW -> update source URL
- Specify all dependencies
- Make %%files list more explicit
- Don't use macros for commands
- Drop redundant %%{?perl_default_filter}

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.46-3
- Perl 5.18 rebuild
- Correct find usage

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 07 2012 Iain Arnell <iarnell@gmail.com> 0.46-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.41-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.41-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.41-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Dec 14 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.41-1
- Update to 0.41 (Fix FTBFS: BZ 660953).
- Remove requires-filter.
- Remove R:/BR: perl(Spiffy).

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.39-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.39-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Steven Pritchard <steve@kspei.com> 0.39-1
- Update to 0.39.
- Fix permissions on *.pm.

* Sat Feb 02 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.38-3
- rebuild for new perl

* Mon Dec 31 2007 Ralf Corsépius <rc040203@freenet.de> 0.38-2
- Adjust License-tag.
- BR: perl(Test::More) (BZ 419631).

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 0.38-1
- Update to 0.38.
- BR ExtUtils::MakeMaker.
- BR MLDBM for better test coverage.

* Tue Oct 17 2006 Steven Pritchard <steve@kspei.com> 0.36-1
- Update to 0.36.
- Use fixperms macro instead of our own chmod incantation.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.35-4
- Fix find option order.

* Fri Jul 07 2006 Steven Pritchard <steve@kspei.com> 0.35-3
- BR IO::String so the tests actually pass.

* Fri Jul 07 2006 Steven Pritchard <steve@kspei.com> 0.35-2
- Re-enable "make test".
- BR File::ReadBackwards for better test coverage.

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 0.35-1
- Update to 0.35.

* Fri Mar 10 2006 Steven Pritchard <steve@kspei.com> 0.33-3
- Change dep filter.
- Various cleanups to match current cpanspec.

* Mon Feb 27 2006 Steven Pritchard <steve@kspei.com> 0.33-2
- Filter Requires: perl(mixin).
- Turn off "make test" for now.
- Drop explict BR: perl.

* Wed Dec 28 2005 Steven Pritchard <steve@kspei.com> 0.33-1
- Specfile autogenerated.
