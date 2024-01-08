Name:           perl-local-lib
Version:        2.000029
Release:        1%{?dist}
Summary:        Create and use a local lib/ for perl modules
License:        GPL+ OR Artistic
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://metacpan.org/release/local-lib
Source:         https://cpan.metacpan.org/authors/id/H/HA/HAARG/local-lib-%{version}.tar.gz
Source10:       perl-homedir.sh
Source11:       perl-homedir.csh
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(CPAN)
BuildRequires:  perl(CPAN::HandleConfig)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 7.00
# BuildRequires:  perl(File::HomeDir)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Carp::Heavy)
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Glob)
# Tests only
%if %{with_check}
BuildRequires:  perl(base)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
%endif
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Carp::Heavy)
Requires:       perl(File::Basename)
Requires:       perl(File::Glob)
Requires:       perl(File::Spec)

%description
This module provides a quick, convenient way of bootstrapping a user-
local Perl module library located within the user's home directory. It
also constructs and prints out for the user the list of environment
variables using the syntax appropriate for the user's current shell (as
specified by the 'SHELL' environment variable), suitable for directly
adding to one's shell configuration file.

More generally, local::lib allows for the bootstrapping and usage of a
directory containing Perl modules outside of Perl's '@INC'. This makes
it easier to ship an application with an app-specific copy of a Perl module,
or collection of modules. Useful in cases like when an upstream maintainer
hasn't applied a patch to a module of theirs that you need for your
application.

%package -n perl-homedir
License:    GPL+ or Artistic
Summary:    Per-user Perl local::lib setup
Requires:   %{name} = %{version}-%{release}
Requires:   sed

%description -n perl-homedir
perl-homedir configures the system to automatically create a ~/perl5
directory in each user's $HOME on user login.  This allows each user to
install CPAN packages via the CPAN to their $HOME, with no additional
configuration or privileges, and without installing them system-wide.

If you want your users to be able to install and use their own Perl modules,
install this package.

%prep
%setup -q -n local-lib-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/profile.d/
install -pm0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/profile.d/

%check
make test

%files
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files -n perl-homedir
%{_sysconfdir}/profile.d/*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.000029-1
- Auto-upgrade to 2.000029 - Azure Linux 3.0 - package upgrades

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.000024-10
- Adding 'BuildRequires: perl-generators'.

* Fri Jul 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.000024-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License verified

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.000024-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.000024-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.000024-6
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.000024-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.000024-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.000024-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.000024-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 12 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.000024-1
- 2.000024 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.000023-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.000023-1
- 2.000023 bump

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.000019-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.000019-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.000019-2
- Perl 5.24 rebuild

* Fri Apr 22 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.000019-1
- 2.000019 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.000018-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.000018-1
- 2.000018 bump

* Tue Oct 06 2015 Petr Šabata <contyk@redhat.com> - 2.000017-1
- 2.000017 bump
- Drop the hard CPAN dependency from perl-homedir

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000015-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.000015-3
- Perl 5.22 rebuild

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 2.000015-2
- Do not hard-code /usr/bin

* Wed Dec 17 2014 Petr Šabata <contyk@redhat.com> - 2.000015-1
- 2.000015 bump

* Tue Nov 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.000014-1
- 2.000014 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.008010-8
- Perl 5.20 rebuild

* Mon Jul 28 2014 Petr Pisar <ppisar@redhat.com> - 1.008010-7
- sed(1) is packaged as /bin/sed

* Fri Jul 25 2014 Petr Pisar <ppisar@redhat.com> - 1.008010-6
- Parse perl-homedir configuration bash syntax by csh profile script
  (bug #1122993)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008010-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 21 2013 Petr Pisar <ppisar@redhat.com> - 1.008010-4
- Fix setting undefined variable in CSH (bug #1033018)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 1.008010-2
- Perl 5.18 rebuild

* Fri Jun 07 2013 Iain Arnell <iarnell@gmail.com> 1.008010-1
- update to latest upstream version

* Fri Apr 19 2013 Iain Arnell <iarnell@gmail.com> 1.008009-2
- rebase append-semicolon patch

* Fri Mar 08 2013 Iain Arnell <iarnell@gmail.com> 1.008009-1
- update to latest upstream version

* Tue Feb 19 2013 Iain Arnell <iarnell@gmail.com> 1.008007-1
- update to latest upstream version

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 1.008006-1
- udpate to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008004-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Petr Šabata <contyk@redhat.com> - 1.008004-11
- Add missing buildtime dependencies
- Drop useless deps
- Drop command macros
- Modernize the spec

* Mon Aug 20 2012 Petr Pisar <ppisar@redhat.com> - 1.008004-10
- Fix CSH support (bug #849609)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008004-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 1.008004-8
- Perl 5.16 rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.008004-7
- Trim Module::Build depencency version to 2 digits because upstream has
  regressed the version

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 1.008004-6
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 1.008004-5
- Round Module::Build version to 2 digits

* Fri Feb 10 2012 Iain Arnell <iarnell@gmail.com> 1.008004-4
- avoid creating ~/perl5/ for all users (rhbz#789146)
- drop defattr in files lists

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.008004-2
- Perl mass rebuild

* Wed Mar 16 2011 Iain Arnell <iarnell@gmail.com> 1.008004-1
- update to latest upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Iain Arnell <iarnell@gmail.com> 1.008001-2
- update requires perl(Module::Build) >= 0.3600

* Sun Jan 23 2011 Iain Arnell <iarnell@gmail.com> 1.008001-1
- update to latest upstream version
- drop R/BR perl(ExtUtils::CBuilder) and perl(ExtUtils::ParseXS)

* Fri Dec 17 2010 Iain Arnell <iarnell@gmail.com> 1.007000-1
- update to latest upstream version
- fix typo in description

* Sun Nov 21 2010 Iain Arnell <iarnell@gmail.com> 1.006007-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- BR perl(Capture::Tiny)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.004009-3
- Mass rebuild with perl-5.12.0

* Tue Jan 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.004009-2
- add perl-homedir subpackage

* Tue Jan 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.004009-1
- add perl_default_filter
- auto-update to 1.004009 (by cpan-spec-update 0.01)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.004007-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004007-1
- auto-update to 1.004007 (by cpan-spec-update 0.01)

* Sat Aug 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004006-1
- auto-update to 1.004006 (by cpan-spec-update 0.01)

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004005-1
- auto-update to 1.004005 (by cpan-spec-update 0.01)

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004004-1
- auto-update to 1.004004 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::Install) (version 1.43)
- added a new req on perl(CPAN) (version 1.80)
- added a new req on perl(ExtUtils::CBuilder) (version 0)
- added a new req on perl(ExtUtils::Install) (version 1.43)
- added a new req on perl(ExtUtils::MakeMaker) (version 6.31)
- added a new req on perl(ExtUtils::ParseXS) (version 0)
- added a new req on perl(Module::Build) (version 0.28)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.004001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004001-1
- auto-update to 1.004001 (by cpan-spec-update 0.01)

* Tue May 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004000-1
- auto-update to 1.004000 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (6.31 => 6.42)

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.003002-1
- submission

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.003002-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
