# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-HTTP-Cookies
Version:        6.11
Release: 7%{?dist}
Summary:        HTTP cookie jars
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/HTTP-Cookies
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Cookies-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(HTTP::Date) >= 6
BuildRequires:  perl(HTTP::Headers::Util) >= 6
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(locale)
# Win32 not supported
# Tests:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(HTTP::Response)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(URI)
Requires:       perl(Carp)
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(HTTP::Headers::Util) >= 6
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies.
# One function of provided HTTP::Cookies::Microsoft works on Win32 only, other
# function do not need it. We keep the module, but remove the dependency.
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\((HTTP::Date|HTTP::Headers::Util|Win32)\\)$

%description
This class is for objects that represent a "cookie jar" -- that is, a
database of all the HTTP cookies that a given LWP::UserAgent object
knows about.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n HTTP-Cookies-%{version}
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
rm -f %{buildroot}%{_libexecdir}/%{name}/t/00*
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Test t/cookies.t write into CWD
DIR=$(mktemp -d)
cp -a %{_libexecdir}/%{name}/* "$DIR"
pushd "$DIR"
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -r "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTORS README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 08 2023 Michal Josef Špaček <mspacek@redhat.com> - 6.11-1
- 6.11 bump

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.10-9
- Package tests
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 6.10-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 6.10-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 05 2021 Petr Pisar <ppisar@redhat.com> - 6.10-1
- 6.10 bump

* Fri Nov 20 2020 Petr Pisar <ppisar@redhat.com> - 6.09-1
- 6.09 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.08-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Petr Pisar <ppisar@redhat.com> - 6.08-1
- 6.08 bump

* Mon Nov 18 2019 Petr Pisar <ppisar@redhat.com> - 6.07-1
- 6.07 bump

* Wed Nov 13 2019 Petr Pisar <ppisar@redhat.com> - 6.06-2
- Do not build-require vars module removed in 6.05

* Wed Nov 13 2019 Petr Pisar <ppisar@redhat.com> - 6.06-1
- 6.06 bump

* Thu Oct 24 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.05-1
- 6.05 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 11 2017 Petr Pisar <ppisar@redhat.com> - 6.04-1
- 6.04 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Petr Pisar <ppisar@redhat.com> - 6.03-4
- Remove old RPM dependency filters

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 6.03-3
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.03-2
- Perl 5.26 rebuild

* Tue Apr 04 2017 Petr Pisar <ppisar@redhat.com> - 6.03-1
- 6.03 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.01-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.01-13
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.01-10
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.01-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 6.01-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Petr Šabata <contyk@redhat.com> - 6.01-4
- Modernize the spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 6.01-2
- Perl 5.16 rebuild

* Thu Feb 16 2012 Petr Pisar <ppisar@redhat.com> - 6.01-1
- 6.01 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.00-3
- add new filter

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.00-2
- Perl mass rebuild

* Wed Mar 16 2011 Petr Pisar <ppisar@redhat.com> 6.00-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff
- Conflicts with perl-libwww-perl-5* and older
