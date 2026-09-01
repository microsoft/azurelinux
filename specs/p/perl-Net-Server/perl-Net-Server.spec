# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Net-Server
Version:        2.014
Release:        9%{?dist}
Summary:        Extensible, general Perl server engine
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Net-Server
Source0:        https://cpan.metacpan.org/modules/by-module/Net/Net-Server-%{version}.tar.gz
# Only initialize existing Net::SSLeay methods (RT#154333)
Patch0:         https://github.com/rhandom/perl-net-server/pull/Net-Server-2.014-Fix-using-OpenSSL-ENGINE-API-routines.patch

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
# BuildRequires:  perl(CGI)
# BuildRequires:  perl(CGI::Compile)
# BuildRequires:  perl(CGI::PSGI)
# BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Temp)
# BuildRequires:  perl(HTTP::Parser::XS)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Multiplex) >= 1.05
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket)
# BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(IO::Socket::IP)
BuildRequires:  perl(IO::Socket::SSL) >= 1.31
BuildRequires:  perl(IO::Socket::UNIX)
# BuildRequires:  perl(IPC::Open3)
# BuildRequires:  perl(IPC::Semaphore)
# BuildRequires:  perl(IPC::SysV)
# BuildRequires:  perl(Log::Log4perl)
# BuildRequires:  perl(Net::CIDR)
BuildRequires:  perl(Net::SSLeay)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(re)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Socket6)
# BuildRequires:  perl(Symbol)
# BuildRequires:  perl(Sys::Syslog)
BuildRequires:  perl(Time::HiRes)
# BuildRequires:  perl(Unix::Syslog)
BuildRequires:  perl(vars)
# Tests
BuildRequires:  perl(constant)
BuildRequires:  perl(English)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(threads)
BuildRequires:  perl(Test::More)
 
# IO::Multiplex support is optional, but not including it causes build problems in some packages...
Requires:       perl(IO::Multiplex) >= 1.05
#  RHBZ#1395714: Optional dependency, including it so that the build matches runtime
Requires:       perl(IO::Socket::IP)

# Remove private test modules
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(NetServerTest\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(NetServerTest\\)$

%description
An extensible, class oriented module written in perl and intended to
be the back end layer of internet protocol servers.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n Net-Server-%{version}

# Do not want to pull in any packaging deps here.
chmod -c 644 examples/*

# Help generators to recognize Perl scripts
for F in $(find t/ -name '*.t'); do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
# XXX Not possible to run in parallel
cd %{_libexecdir}/%{name} && exec prove -I . -r
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes README examples
%{perl_vendorlib}/*
%{_mandir}/man3/*
%{_bindir}/net-server
%{_mandir}/man1/net-server.1*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.014-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.014-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 04 2024 Michal Josef Špaček <mspacek@redhat.com> - 2.014-7
- Fix running of tests in perl-Net-Server-tests subpackage
- Rename patch file to better name

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.014-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.014-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 17 2023 Michal Josef Špaček <mspacek@redhat.com> - 2.014-2
- Package tests
- Update license to SPDX format

* Fri Mar 17 2023 Michal Josef Špaček <mspacek@redhat.com> - 2.014-1
- 2.014 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.010-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.010-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.010-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.010-1
- 2.010 bump

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.009-13
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.009-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 01 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.009-11
- Disable optional run-requires for build

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.009-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.009-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.009-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.009-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.009-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.009-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.009-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 10 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.009-1
- 2.009 bump
- Modernize spec file

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.008-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.008-9
- Perl 5.26 rebuild

* Wed May 24 2017 Petr Pisar <ppisar@redhat.com> - 2.008-8
- Restore compatibility with Perl 5.26.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.008-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 17 2016 "D. Johnson" <fenris02@fedoraproject.org> - 2.008-6
- Bug 1395714 - perl-Net-Server should depend on perl-IO-Socket-INET6

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.008-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.008-2
- Perl 5.22 rebuild

* Wed May 27 2015 Kevin Fenzi <kevin@scrye.com> 2.008-1
- Update to 2.008. Fixes bug #1225064

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.007-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2.007-2
- Perl 5.18 rebuild

* Wed Jul 24 2013 Paul Howarth <paul@city-fan.org> - 2.007-1
- Update to 2.007
- BR: perl(Test::More) and perl(Time::HiRes)
- Add various other buildreqs for additional test coverage
- Don't use macros for commands
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.006-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Kevin Fenzi <kevin@scrye.com> 2.006-1
- Update to 2.006 upstream release
- Redo spec with current guidelines. 

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.97-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.97-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.97-10
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.97-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.97-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 <nicolas.mailhot at laposte.net>
- 0.97-5
⌖ Fedora 10 alpha general package cleanup

* Mon Jun 02 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.97-3
⋰ remove old %%check Dag leftover rpmbuild does not like anymore

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 0.97-2
Rebuild for new perl

* Sun Aug 12 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
⍟ 0.97-1

* Fri May 18 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
⍟ 0.96-2
- more build checks
⍟ 0.96-1
- trim changelog

* Tue Mar 20 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.95-1 

* Sat Sep 02 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.94-2
- FE6 Rebuild

* Sun Jul 30 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.94-1

* Sun Apr 23 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.93-1

* Mon Feb 13 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.90-2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Jan 8 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.90-1
- Updated to 0.90
- add IO::Multiplex dep
