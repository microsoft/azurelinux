# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without RRD

Name:           perl-Log-Log4perl
Version:        1.57
Release:        8%{?dist}
Summary:        Log4j implementation for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Log-Log4perl
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETJ/Log-Log4perl-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Find)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBI)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path) >= 2.07
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(if)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(IPC::Semaphore)
BuildRequires:  perl(IPC::SysV)
BuildRequires:  perl(Log::Dispatch::File)
BuildRequires:  perl(Log::Dispatch::FileRotate) >= 1.10
BuildRequires:  perl(Log::Dispatch::Screen)
BuildRequires:  perl(Log::Dispatch::Syslog)
BuildRequires:  perl(POSIX)
%if %{with RRD}
BuildRequires:  perl(RRDs)
%endif
BuildRequires:  perl(Safe)
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sys::Hostname)
# Term::ANSIColor is not needed for runing tests
# Time::HiRes is not needed for runing the tests
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XML::DOM) >= 1.29
# Tests
BuildRequires:  perl(Benchmark)
BuildRequires:  perl(fields)
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Log::Dispatch)
BuildRequires:  perl(Test::More) >= 0.45
BuildRequires:  perl(utf8)
# Optional tests
%if ! (0%{?rhel} >= 7)
BuildRequires:  perl(DBD::CSV) >= 0.33
BuildRequires:  perl(DBI) >= 1.607
BuildRequires:  perl(Log::Dispatch)
BuildRequires:  perl(SQL::Statement) >= 1.20
BuildRequires:  perl(Sys::Syslog)
%endif
Requires:       perl(Encode)
Requires:       perl(Net::LDAP)
Requires:       perl(Safe)
Requires:       perl(Sys::Hostname)
Requires:       perl(Time::HiRes)

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Log4perlInternalTest\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(L4pResurrectable\\)

%description
Log::Log4perl lets you remote-control and fine-tune the logging
behavior of your system from the outside. It implements the widely
popular (Java-based) Log4j logging package in pure Perl.

To log into RRD database, install perl-Log-Log4perl-Appender-RRDs package.
To log into a database via DBI, install perl-Log-Log4perl-Appender-DBI package.

To read log4j XML configuration files, install
perl-Log-Log4perl-Config-DOMConfigurator package.

%package Appender-DBI
Summary:        Log to a database
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name} < 1.46-2

%description Appender-DBI
Log::Log4perl::Appender::DBI appender facilitates writing data to a database
using DBI interface via Log4perl.

%if %{with RRD}
%package Appender-RRDs
Summary:        Log to a RRDtool archive
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name} < 1.46-2

%description Appender-RRDs
Log::Log4perl::Appender::RRDs appender facilitates writing data to
RRDtool round-robin archives via Log4perl.
%endif

%package Config-DOMConfigurator
Summary:        Read log4j XML configuration files
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name} < 1.46-2

%description Config-DOMConfigurator
Log::Log4perl::Config::DOMConfigurator adds support for log4j XML
configuration files to Log::Log4perl Perl logging system.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Filter::Util::Call)
# Optional tests
%if ! (0%{?rhel} >= 7)
Requires:       perl(DBD::CSV) >= 0.33
Requires:       perl(DBI) >= 1.607
Requires:       perl(Log::Dispatch)
Requires:       perl(SQL::Statement) >= 1.20
Requires:       perl(Sys::Syslog)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Log-Log4perl-%{version}
find lib -name '*.pm' -exec chmod -c a-x {} +
perl -MConfig -pi -e 's|^#!/usr/local/bin/perl|$Config{startperl}|' \
    eg/newsyslog-test eg/benchmarks/simple

# Help generators to recognize Perl scripts
for F in t/*.t t/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a eg t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
# Shared memory tests guarded with L4P_ALL_TESTS fail in mock.
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/Log/Log4perl/Appender/RRDs.pm
%exclude %{perl_vendorlib}/Log/Log4perl/Appender/DBI.pm
%exclude %{perl_vendorlib}/Log/Log4perl/Config/DOMConfigurator.pm
%exclude %{perl_vendorlib}/Log/Log4perl/JavaMap/JDBCAppender.pm
%{_mandir}/man1/*
%{_mandir}/man3/*
%exclude %{_mandir}/man3/Log::Log4perl::Appender::RRDs.*
%exclude %{_mandir}/man3/Log::Log4perl::Appender::DBI.*
%exclude %{_mandir}/man3/Log::Log4perl::Config::DOMConfigurator.*
%exclude %{_mandir}/man3/Log::Log4perl::JavaMap::JDBCAppender.*
%{_bindir}/*

%files Appender-DBI
%{perl_vendorlib}/Log/Log4perl/Appender/DBI.pm
%{perl_vendorlib}/Log/Log4perl/JavaMap/JDBCAppender.pm
%{_mandir}/man3/Log::Log4perl::Appender::DBI.*
%{_mandir}/man3/Log::Log4perl::JavaMap::JDBCAppender.*

%if %{with RRD}
%files Appender-RRDs
%{perl_vendorlib}/Log/Log4perl/Appender/RRDs.pm
%{_mandir}/man3/Log::Log4perl::Appender::RRDs.*
%endif

%files Config-DOMConfigurator
%{perl_vendorlib}/Log/Log4perl/Config/DOMConfigurator.pm
%{_mandir}/man3/Log::Log4perl::Config::DOMConfigurator.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 24 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.57-1
- 1.57 bump

* Mon Sep 05 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.56-1
- 1.56 bump
- Package tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 06 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.55-1
- 1.55 bump

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.54-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.54-2
- Perl 5.34 rebuild

* Mon Feb 08 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.54-1
- 1.54 bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 18 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.53-1
- 1.53 bump

* Wed Sep 16 2020 Petr Pisar <ppisar@redhat.com> - 1.52-2
- Build-require Time::HiRes because of a bug in Time::HiRes detection

* Mon Sep 07 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-1
- 1.52 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Petr Pisar <ppisar@redhat.com> - 1.50-1
- 1.50 bump

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.49-12
- Perl 5.32 rebuild

* Thu Mar 19 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.49-11
- Specify all dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.49-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.49-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.49-2
- Perl 5.26 rebuild

* Tue Feb 21 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.49-1
- 1.49 bump

* Wed Nov 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.48-1
- 1.48 bump

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.47-2
- Perl 5.24 rebuild

* Fri Mar 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.47-1
- 1.47 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-3
- Perl 5.22 rebuild

* Fri Apr 03 2015 Petr Pisar <ppisar@redhat.com> - 1.46-2
- Modernize spec file
- Move RRDs back-end into perl-Log-Log4perl-Appender-RRDs sub-package
- Move DBI back-end into perl-Log-Log4perl-Appender-DBI sub-package
- Move XML configuration file parser into
  perl-Log-Log4perl-Config-DOMConfigurator sub-package

* Mon Nov 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-1
- 1.46 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-1
- 1.44 bump

* Tue Mar 18 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.43-1
- 1.43 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Aug 01 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-1
- 1.42 bump

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.41-2
- Perl 5.18 rebuild
- Do not perform shared-memory tests

* Tue Apr 23 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.41-1
- 1.41 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.40-1
- 1.40 bump

* Tue Oct 30 2012 Petr Šabata <contyk@redhat.com> - 1.39-1
- 1.39 bump

* Wed Sep 26 2012 Petr Pisar <ppisar@redhat.com> - 1.38-2
- Disable optional tests on RHEL >= 7

* Wed Sep 26 2012 Petr Pisar <ppisar@redhat.com> - 1.38-1
- 1.38 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 1.37-2
- Perl 5.16 rebuild

* Fri Jun 08 2012 Petr Šabata <contyk@redhat.com> - 1.37-1
- 1.37 bump
- Drop command macros

* Wed Feb 22 2012 Petr Pisar <ppisar@redhat.com> - 1.36-1
- 1.36 bump

* Fri Jan 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.35-1
- bump to 1.35

* Mon Nov 07 2011 Petr Sabata <contyk@redhat.com> - 1.34-1
- 1.34 bump
- Removing the BuildRoot tag

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.33-3
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.33-2
- Perl mass rebuild

* Wed Jun  1 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.33-1
- 1.33 bump
- clean spec from defattr, clean section & rm -rf

* Mon Feb 28 2011 Petr Sabata <psabata@redhat.com> - 1.32-1
- 1.32 bump, bugfix release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.30-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Sep 08 2010 Petr Pisar <ppisar@redhat.com> - 1.30-1
- 1.30 bump
- l4p-tmpl executable added
- Add BuildRequires for tests
- Spelling in package description corrected

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.24-2
- rebuild against perl 5.10.1

* Thu Aug 06 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-1
- Fix mass rebuild breakdown: Upgrade to upstream 1.24.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.20-1
- Upstream update.
- Reactivate testsuite.
- Remove examples (eg, ldap) from %%doc.
- Don't chmod -x eg/*.
- Remove BR: perl(IPC::Shareable).

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-2
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-1.1
- disable tests

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-1
- bump to 1.13

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-1.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Jun 29 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.

* Thu Apr  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.10-1
- Update to 1.10.

* Sun Feb 11 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-1
- Update to 1.09.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-1
- Update to 1.08.

* Sat Oct 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- Update to 1.07.

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Sun Jun 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Tue Apr 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-2
- Log::Dispatch::FileRotate is no longer excluded due to licensing
  problems (the package now includes copyright information).

* Mon Mar  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.

* Mon Feb 27 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-3
- Rebuild for FC5 (perl 5.8.8).

* Thu Feb  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-2
- Added a couple of comments as suggested by Paul Howarth (#176137).

* Tue Feb  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.
- Disabled the Log::Dispatch::FileRotate requirement (see #171640).

* Mon Dec 19 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-1
- Update to 1.02.

* Sat Oct 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- Update to 1.01.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.00-1
- First build.
