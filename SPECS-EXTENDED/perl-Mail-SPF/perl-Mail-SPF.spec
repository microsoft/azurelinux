Name:           perl-Mail-SPF
Version:        3.20240923
Release:        1%{?dist}
Summary:        Object-oriented implementation of Sender Policy Framework
License:        BSD-3-Clause
URL:            https://metacpan.org/release/Mail-SPF
Source0:        https://cpan.metacpan.org/modules/by-module/Mail/Mail-SPF-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Error)
BuildRequires:  perl(Net::DNS) >= 0.62
BuildRequires:  perl(Net::DNS::Resolver)
BuildRequires:  perl(NetAddr::IP) >= 4
BuildRequires:  perl(overload)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(URI::Escape) >= 1.13
BuildRequires:  perl(utf8)
# Tests only
BuildRequires:  perl(blib)
BuildRequires:  perl(Net::DNS::Resolver::Programmable) >= 0.003
BuildRequires:  perl(Net::DNS::RR)
BuildRequires:  perl(Test::More)
Requires:       perl(Net::DNS) >= 0.62
Requires:       perl(URI) >= 1.13

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description
Mail::SPF is an object-oriented implementation of Sender Policy Framework
(SPF). See http://www.openspf.org for more information about SPF.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Mail-SPF-%{version}
chmod -x bin/*

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
# The spfquery and spfd will use alternatives
%{__mv} -f %{buildroot}%{_bindir}/spfquery %{buildroot}%{_bindir}/spfquery.%{name}
%{__mv} -f %{buildroot}%{_bindir}/spfd %{buildroot}%{_bindir}/spfd.%{name}
%{__mv} -f %{buildroot}%{_mandir}/man1/spfquery.1 %{buildroot}%{_mandir}/man1/spfquery-%{name}.1
touch %{buildroot}%{_bindir}/spfquery %{buildroot}%{_bindir}/spfd %{buildroot}%{_mandir}/man1/spfquery.1.gz

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/t/90-author*
for F in `ls %{buildroot}%{_libexecdir}/%{name}/t/*`; do
    perl -i -ne 'print $_ unless m{^use blib}' $F
done
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
make test

%post
%{_sbindir}/update-alternatives --install %{_bindir}/spfquery spf %{_bindir}/spfquery.%{name} 10 \
       --slave %{_bindir}/spfd spf-daemon %{_bindir}/spfd.%{name} \
       --slave %{_mandir}/man1/spfquery.1.gz spfquery-man-page %{_mandir}/man1/spfquery-%{name}.1.gz

%postun
if [ $1 -eq 0 ] ; then
       %{_sbindir}/update-alternatives --remove spf %{_bindir}/spfquery.%{name}
fi

%files
%license LICENSE
%doc Changes README TODO bin/
%{perl_vendorlib}/Mail/SPF*
%{_mandir}/man1/spf*
%{_mandir}/man3/Mail::SPF*
%ghost %{_bindir}/spfquery
%ghost %{_bindir}/spfd
%ghost %{_mandir}/man1/spfquery.1.gz
%{_bindir}/spfquery.%{name}
%{_bindir}/spfd.%{name}

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Sep 23 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.20240923-1
- 3.20240923 bump (rhbz#2314156)

* Wed Aug 28 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.20240827-1
- 3.20240827 bump (rhbz#2308077)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.20240617-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.20240617-1
- 3.20240617 bump (rhbz#2292629)

* Tue Feb 06 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.20240206-1
- 3.20240206 bump (rhbz#2262902)

* Mon Feb 05 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.20240205-1
- 3.20240205 bump (rhbz#2262786)
- Package tests

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 07 2023 Michal Josef Špaček <mspacek@redhat.com> - 2.9.0-31
- Fix %patch macro
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.9.0-28
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.9.0-25
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.9.0-22
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.9.0-19
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.9.0-16
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.9.0-13
- Perl 5.26 rebuild

* Sun Feb 12 2017 Jan Pazdziora <jpazdziora@redhat.com> - 2.9.0-12
- 1399246 - ship /usr/bin/spfquery and /usr/bin/spfd as alternatives.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.9.0-10
- Perl 5.24 rebuild

* Mon Feb 29 2016 Petr Šabata <contyk@redhat.com> - 2.9.0-9
- Package cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.9.0-6
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.9.0-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 2.9.0-2
- Perl 5.18 rebuild

* Mon Jul 22 2013 Paul Howarth <paul@city-fan.org> - 2.9.0-1
- Update to 2.9.0
  - Default to querying only TXT type RRs
    (query_rr_types = Mail::SPF::Server->query_rr_type_txt); experience has
    shown that querying SPF type RRs is impractical

* Fri Jun 28 2013 Paul Howarth <paul@city-fan.org> - 2.8.0-3
- Fix broken POD (CPAN RT#86060)
- Work around test suite failures with Net::DNS ≥ 0.68 (CPAN RT#78214)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Petr Šabata <contyk@redhat.com> - 2.8.0-1
- 2.8.0 bump
- Fix dependencies
- Drop command macros

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.007-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2.007-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.007-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 5 2010 Nick Bebout <nb@fedoraproject.org> - 2.007-1
- Update to 2.007

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.006-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.006-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Steven Pritchard <steve@kspei.com> 2.006-1
- Update to 2.006.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.005-2
- Rebuild for new perl

* Mon Jul 09 2007 Steven Pritchard <steve@kspei.com> 2.005-1
- Specfile autogenerated by cpanspec 1.71.
- Add the "v" before version numbers to handle broken upstream packaging.
- Remove redundant perl build dependency.
- Drop bogus version number from Net::DNS::Resolver::Programmable dependency.
- Drop redundant explicit dependencies.
- BR Test::More and Test::Pod.
- Include the spfd and spfquery scripts as %%doc
