# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-CGI-Fast
Version:        2.17
Release: 7%{?dist}
Summary:        CGI Interface for Fast CGI
# lib/CGI/Fast.pm probably qotes piece of Artistic license before declaring
# "as Perl itself" <https://github.com/leejo/cgi-fast/issues/13>
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/CGI-Fast
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEEJO/CGI-Fast-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(CGI) >= 4.00
BuildRequires:  perl(CGI::Carp)
BuildRequires:  perl(deprecate)
BuildRequires:  perl(FCGI) >= 0.67
BuildRequires:  perl(if)
BuildRequires:  perl(strict)
# Tests:
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(warnings)
Requires:       perl(deprecate)
Requires:       perl(CGI) >= 4.00
Requires:       perl(FCGI) >= 0.67
# perl-CGI-Fast was split from perl-CGI
Conflicts:      perl-CGI < 4.00

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((CGI|FCGI)\\)$

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%description
CGI::Fast is a subclass of the CGI object created by CGI.pm. It is
specialized to work well FCGI module, which greatly speeds up CGI scripts
by turning them into persistently running server processes. Scripts that
perform time-consuming initialization processes, such as loading large
modules or opening persistent database connections, will see large
performance improvements.

%prep
%setup -q -n CGI-Fast-%{version}

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

# Remove release test
rm t/006_changes.t
perl -i -ne 'print $_ unless m{^t/006_changes\.t}' MANIFEST

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
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes README
%{perl_vendorlib}/CGI*
%{_mandir}/man3/CGI::Fast*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 14 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.17-1
- 2.17 bump (rhbz#2249456)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-3
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 01 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-1
- 2.16 bump
- Package tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.15-8
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.15-5
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.15-2
- Perl 5.30 rebuild

* Mon Apr 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.15-1
- 2.15 bump

* Tue Mar 26 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.14-1
- 2.14 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.13-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 20 2017 Petr Pisar <ppisar@redhat.com> - 2.13-1
- 2.13 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.12-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.12-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 23 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.12-1
- 2.12 bump

* Mon Nov 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-1
- 2.11 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 23 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-1
- 2.10 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-2
- Perl 5.22 rebuild

* Thu Mar 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-1
- 2.09 bump

* Mon Feb 23 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.07-1
- 2.07 bump

* Wed Jan 14 2015 Petr Pisar <ppisar@redhat.com> - 2.05-2
- Specify run-time dependency versions

* Mon Dec 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.05-1
- 2.05 bump

* Wed Dec 10 2014 Petr Pisar <ppisar@redhat.com> - 2.04-2
- Do not load Test::Deep where not needed
- Make Test::Deep tests optional as it's not in the core in contrast to the
  CGI-Fast

* Mon Oct 13 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-1
- 2.04 bump

* Wed Sep 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.03-1
- 2.03 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-2
- Perl 5.20 rebuild

* Mon Jun 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-1
- 2.02 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.01-1
- 2.01 bump

* Mon May 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-1
- Specfile autogenerated by cpanspec 1.78.
