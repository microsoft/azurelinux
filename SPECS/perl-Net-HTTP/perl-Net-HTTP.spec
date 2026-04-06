# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Add support for IPv6
%{bcond_without perl_Net_HTTP_enables_ipv6}
# Do not run network tests accessing Internet
%{bcond_with perl_Net_HTTP_enables_network_test}
# Add support for TLS/SSL
%{bcond_without perl_Net_HTTP_enables_ssl}

Name:           perl-Net-HTTP
Version:        6.24
Release:        1%{?dist}
Summary:        Low-level HTTP connection (client)
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Net-HTTP
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/Net-HTTP-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6.2
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Raw::Zlib)
# Prefer IO::Socket::IP over IO::Socket::INET
%if %{with perl_Net_HTTP_enables_ipv6}
BuildRequires:  perl(IO::Socket::IP)
%else
BuildRequires:  perl(IO::Socket)
%endif
%if %{with perl_Net_HTTP_enables_ssl}
# IO::Socket::SSL or Net::SSL
BuildRequires:  perl(IO::Socket::SSL) >= 2.012
%endif
BuildRequires:  perl(IO::Uncompress::Gunzip)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(URI)
BuildRequires:  perl(warnings)
# Tests only:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::More)
Requires:       perl(Compress::Raw::Zlib)
Requires:       perl(IO::Uncompress::Gunzip)
# Prefer IO::Socket::IP over IO::Socket::INET
%if %{with perl_Net_HTTP_enables_ipv6}
Requires:       perl(IO::Socket::IP)
%else
Requires:       perl(IO::Socket)
%endif
Requires:       perl(Symbol)
%if %{with perl_Net_HTTP_enables_ssl}
Requires:       perl(IO::Socket::SSL) >= 2.012
%endif
Conflicts:      perl-libwww-perl < 6

%description
The Net::HTTP class is a low-level HTTP client. An instance of the
Net::HTTP class represents a connection to an HTTP server. The HTTP
protocol is described in RFC 2616. The Net::HTTP class supports HTTP/1.0
and HTTP/1.1.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{with perl_Net_HTTP_enables_network_test}
%if %{with perl_Net_HTTP_enables_ssl}
Requires:  perl(IO::Socket::SSL) >= 2.012
%endif
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Net-HTTP-%{version}
%if %{without perl_Net_HTTP_enables_network_test}
rm t/live*.t
perl -i -ne 'print $_ unless m{^t/live.*\.t}' MANIFEST
%endif
# Help generators to recognize a Perl code
for F in t/*.t; do
    perl -i -MConfig -pe 'print qq{$Config{startperl}\n} if $. == 1 && !s{\A#!.*\bperl}{$Config{startperl}}' "$F"
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
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
set -e
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes CONTRIBUTORS README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Sep 01 2025 Michal Josef Špaček <mspacek@redhat.com> - 6.24-1
- 0.24 bump

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 21 2023 Michal Josef Špaček <mspacek@redhat.com> - 6.23-1
- 6.23 bump
- Fix comments in spec file (IO::Socket::INET6 is deprecated)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.22-4
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 6.22-2
- Perl 5.36 rebuild

* Mon Jan 24 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.22-1
- 6.22 bump
- Unify macros in spec file

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 6.21-2
- Perl 5.34 rebuild

* Fri Mar 19 2021 Petr Pisar <ppisar@redhat.com> - 6.21-1
- 6.21 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Petr Pisar <ppisar@redhat.com> - 6.20-1
- 6.20 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.19-5
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.19-2
- Perl 5.30 rebuild

* Fri May 17 2019 Petr Pisar <ppisar@redhat.com> - 6.19-1
- 6.19 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.18-2
- Perl 5.28 rebuild

* Thu May 10 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.18-1
- 6.18 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 04 2017 Petr Pisar <ppisar@redhat.com> - 6.17-1
- 6.17 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.16-2
- Perl 5.26 rebuild

* Tue May 30 2017 Petr Pisar <ppisar@redhat.com> - 6.16-1
- 6.16 bump

* Mon May 15 2017 Petr Pisar <ppisar@redhat.com> - 6.15-1
- 6.15 bump

* Tue Apr 25 2017 Petr Pisar <ppisar@redhat.com> - 6.14-1
- 6.14 bump

* Mon Feb 20 2017 Petr Pisar <ppisar@redhat.com> - 6.13-1
- 6.13 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 06 2017 Petr Pisar <ppisar@redhat.com> - 6.12-1
- 6.12 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.09-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.09-2
- Perl 5.22 rebuild

* Thu May 21 2015 Petr Pisar <ppisar@redhat.com> - 6.09-1
- 6.09 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.07-2
- Perl 5.20 rebuild

* Tue Jul 29 2014 Petr Pisar <ppisar@redhat.com> - 6.07-1
- 6.07 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 6.06-3
- Specify all dependencies

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 6.06-2
- Perl 5.18 rebuild

* Mon Mar 11 2013 Petr Pisar <ppisar@redhat.com> - 6.06-1
- 6.06 bump

* Fri Mar 08 2013 Petr Pisar <ppisar@redhat.com> - 6.05-3
- Handle IO::Socket::SSL as non-blocking (bug #768394)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Petr Pisar <ppisar@redhat.com> - 6.05-1
- 6.05 bump

* Fri Nov 09 2012 Petr Pisar <ppisar@redhat.com> - 6.04-1
- 6.04 bump

* Mon Aug 13 2012 Petr Pisar <ppisar@redhat.com> - 6.03-4
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 6.03-2
- Perl 5.16 rebuild

* Mon Feb 20 2012 Petr Pisar <ppisar@redhat.com> - 6.03-1
- 6.03 bump: Restore blocking override for Net::SSL (RT #72790)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Petr Pisar <ppisar@redhat.com> - 6.02-1
- 6.02 bump
- Fixes HTTPS time-out in LWP::UserAgent/IO::Socket::SSL (bug #750793)

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 6.01-2
- Perl mass rebuild

* Mon Apr 18 2011 Petr Pisar <ppisar@redhat.com> - 6.01-1
- 6.01 bump

* Thu Mar 17 2011 Petr Pisar <ppisar@redhat.com> 6.00-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff
- Conflicts with perl-libwww-perl-5* and older
