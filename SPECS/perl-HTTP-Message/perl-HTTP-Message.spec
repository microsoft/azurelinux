# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-HTTP-Message
Version:        7.01
Release:        1%{?dist}
Summary:        HTTP style message
# CONTRIBUTING.md:  CC0-1.0
# other files:      GPL-1.0-or-later OR Artistic-1.0-Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND CC0-1.0
URL:            https://metacpan.org/release/HTTP-Message
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Message-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(parent)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Clone)
BuildRequires:  perl(Compress::Raw::Zlib)
BuildRequires:  perl(Encode) >= 3.01
BuildRequires:  perl(Encode::Locale) >= 1
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(HTTP::Date) >= 6
BuildRequires:  perl(IO::Compress::Brotli)
BuildRequires:  perl(IO::Compress::Bzip2) >= 2.021
BuildRequires:  perl(IO::Compress::Deflate)
BuildRequires:  perl(IO::Compress::Gzip)
BuildRequires:  perl(IO::HTML)
BuildRequires:  perl(IO::Uncompress::Inflate)
BuildRequires:  perl(IO::Uncompress::RawInflate)
BuildRequires:  perl(LWP::MediaTypes) >= 6
BuildRequires:  perl(MIME::Base64) >= 2.1
BuildRequires:  perl(MIME::QuotedPrint)
BuildRequires:  perl(URI) >= 1.10
# Tests only:
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(PerlIO::encoding)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Needs)
# Time::Local only used on MacOS
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(URI::URL)
Recommends:     perl(IO::Compress::Brotli)
Requires:       perl(Clone) => 0.46
Requires:       perl(Compress::Raw::Zlib) >= 2.062
Requires:       perl(Encode) >= 3.01
Requires:       perl(Encode::Locale) >= 1
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(IO::Compress::Bzip2) >= 2.021
Requires:       perl(IO::Compress::Deflate)
Requires:       perl(IO::Compress::Gzip)
Requires:       perl(IO::HTML)
Requires:       perl(IO::Uncompress::Inflate)
Requires:       perl(IO::Uncompress::RawInflate)
Requires:       perl(LWP::MediaTypes) >= 6
Requires:       perl(MIME::Base64) >= 2.1
Requires:       perl(MIME::QuotedPrint)
Requires:       perl(URI) >= 1.10
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Clone|Exporter|HTTP::Date|URI)\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(HTTP::Headers\\)$
# Remove private modules and unused dependencies
%global __requires_exclude %{__requires_exclude}|^perl\\((Secret|Time::Local)\\)
%global __provides_exclude %{__provides_exclude}|^perl\\(Secret\\)$

%description
The HTTP-Message distribution contains classes useful for representing the
messages passed in HTTP style communication.  These are classes representing
requests, responses and the headers contained within them.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(URI::URL)
Requires:       perl(IO::Compress::Brotli)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n HTTP-Message-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
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
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING.md README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Nov 07 2025 Michal Josef Špaček <mspacek@redhat.com> - 7.01-1
- 7.01 bump

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Michal Josef Špaček <mspacek@redhat.com> - 7.00-1
- 7.00 bump
- Requires IO::Compress::Brotli for tests.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 28 2024 Michal Josef Špaček <mspacek@redhat.com> - 6.46-1
- 6.46 bump

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Michal Josef Špaček <mspacek@redhat.com> - 6.45-1
- 6.45 bump

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 27 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.44-1
- 6.44 bump

* Tue Oct 25 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.43-2
- Update license to SPDX

* Mon Oct 24 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.43-1
- 6.43 bump

* Fri Oct 21 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.42-1
- 6.42 bump

* Tue Oct 18 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.40-1
- 6.40 bump

* Wed Aug 17 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.37-1
- 6.37 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 6.36-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.36-1
- 6.36 bump

* Tue Jan 04 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.35-1
- 6.35 bump

* Tue Nov 09 2021 Michal Josef Špaček <mspacek@redhat.com> - 6.34-1
- 6.34 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Michal Josef Špaček <mspacek@redhat.com> - 6.33-1
- 6.33 bump

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 6.32-2
- Perl 5.34 rebuild

* Wed May 19 2021 Michal Josef Špaček <mspacek@redhat.com> - 6.32-1
- 6.32 bump

* Wed May 12 2021 Michal Josef Špaček <mspacek@redhat.com> - 6.31-1
- 6.31 bump
- Simplify running of tests

* Tue May 11 2021 Michal Josef Špaček <mspacek@redhat.com> - 6.30-1
- 6.30 bump

* Mon Mar 08 2021 Petr Pisar <ppisar@redhat.com> - 6.29-1
- 6.29 bump

* Mon Feb 22 2021 Petr Pisar <ppisar@redhat.com> - 6.28-1
- 6.28 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 05 2021 Petr Pisar <ppisar@redhat.com> - 6.27-1
- 6.27 bump

* Thu Sep 10 2020 Petr Pisar <ppisar@redhat.com> - 6.26-1
- 6.26 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.25-3
- Perl 5.32 re-rebuild

* Mon Jun 29 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.25-2
- Perl 5.32 re-rebuild

* Mon Jun 29 2020 Petr Pisar <ppisar@redhat.com> - 6.25-1
- 6.25 bump

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.24-2
- Perl 5.32 rebuild

* Mon May 11 2020 Petr Pisar <ppisar@redhat.com> - 6.24-1
- 6.24 bump

* Tue Feb 25 2020 Petr Pisar <ppisar@redhat.com> - 6.22-1
- 6.22 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.18-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.18-2
- Perl 5.28 rebuild

* Wed Jun 06 2018 Petr Pisar <ppisar@redhat.com> - 6.18-1
- 6.18 bump

* Thu Mar 29 2018 Petr Pisar <ppisar@redhat.com> - 6.16-1
- 6.16 bump

* Wed Mar 14 2018 Petr Pisar <ppisar@redhat.com> - 6.15-1
- 6.15 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 21 2017 Petr Pisar <ppisar@redhat.com> - 6.14-1
- 6.14 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.13-1
- 6.13 bump

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.11-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.11-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 10 2015 Petr Pisar <ppisar@redhat.com> - 6.11-1
- 6.11 bump

* Mon Jul 20 2015 Petr Pisar <ppisar@redhat.com> - 6.10-1
- 6.10 bump

* Fri Jul 10 2015 Petr Pisar <ppisar@redhat.com> - 6.08-1
- 6.08 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.06-10
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.06-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 6.06-6
- Perl 5.18 rebuild

* Tue Jul 23 2013 Petr Šabata <contyk@redhat.com> - 6.06-5
- Add missing dependencies

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 6.06-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Petr Šabata <contyk@redhat.com> - 6.06-2
- BuildRequire perl(Carp)
- Modernize the spec and drop command macros

* Mon Oct 22 2012 Petr Pisar <ppisar@redhat.com> - 6.06-1
- 6.06 bump

* Tue Oct 02 2012 Petr Pisar <ppisar@redhat.com> - 6.04-1
- 6.04 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 6.03-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 6.03-3
- Perl 5.16 rebuild

* Fri Apr 06 2012 Petr Pisar <ppisar@redhat.com> - 6.03-2
- Break build-time cycle while boostrapping perl (bug #810223)

* Mon Feb 20 2012 Petr Pisar <ppisar@redhat.com> - 6.03-1
- 6.03 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.02-3
- add new filter

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.02-2
- Perl mass rebuild

* Wed Mar 23 2011 Petr Pisar <ppisar@redhat.com> - 6.02-1
- 6.02 bump

* Thu Mar 17 2011 Petr Pisar <ppisar@redhat.com> 6.01-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff
- Conflicts with perl-libwww-perl 5* and older
