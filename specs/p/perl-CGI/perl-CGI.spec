# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-CGI
Summary:        Handle Common Gateway Interface requests and responses
Version:        4.71
Release: 2%{?dist}
License:        Artistic-2.0
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEEJO/CGI-%{version}.tar.gz
URL:            https://metacpan.org/release/CGI
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-requires:
BuildRequires:  perl(Carp)
# Config not needed on Linux
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Temp) >= 0.17
BuildRequires:  perl(HTML::Entities) >= 3.69
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
# Text::ParseWords not used at tests
BuildRequires:  perl(URI) >= 1.76
BuildRequires:  perl(warnings)
# Apache modules are optional
# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(lib)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::Warn) >= 0.3
BuildRequires:  perl(utf8)
Requires:       perl(File::Spec) >= 0.82
Requires:       perl(File::Temp) >= 0.17
Requires:       perl(HTML::Entities) >= 3.69
Requires:       perl(Text::ParseWords)
Requires:       perl(URI) >= 1.76

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((File::Spec)\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((File::Temp)\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((URI)\\)$
# Remove false dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Fh)\\)
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(MultipartBuffer\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Fh\\)

# Filter modules bundled for tests
%global __requires_exclude %{__requires_exclude}|^perl\\(Apache)\s*$
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
CGI.pm is a stable, complete and mature solution for processing and preparing
HTTP requests and responses. Major features including processing form
submissions, file uploads, reading and writing cookies, query string
generation and manipulation, and processing and preparing HTTP headers. Some
HTML generation utilities are included as well.

CGI.pm performs very well in in a vanilla CGI.pm environment and also comes 
with built-in support for mod_perl and mod_perl2 as well as FastCGI.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}-%{version}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n CGI-%{version}
iconv -f iso8859-1 -t utf-8 < Changes > Changes.1
mv Changes.1 Changes
chmod -c -x examples/*

# Help file to recognise the Perl scripts
for F in `find t -name *.t`; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
rm %{buildroot}/%{_libexecdir}/%{name}/t/compiles_pod.t
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes README.md examples/
%{perl_vendorlib}/CGI*
%{perl_vendorlib}/Fh*
%{_mandir}/man3/CGI*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Thu Oct 09 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4.71-1
- 4.71 bump (rhbz#2402510)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4.70-1
- 4.70 bump (rhbz#2382299)

* Mon Jun 23 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4.69-1
- 4.69 bump (rhbz#2374269)

* Mon Apr 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4.68-1
- 4.68 bump (rhbz#2356535)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4.67-1
- 4.67 bump (rhbz#2336423)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.66-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4.66-1
- 4.66 bump (rhbz#2293061)

* Wed Jun 05 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4.65-1
- 4.65 bump (rhbz#2290414)

* Mon Mar 18 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4.64-1
- 4.64 bump (rhbz#2270079)

* Thu Mar 07 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4.63-1
- 4.63 bump (rhbz#2268208)

* Mon Mar 04 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4.62-1
- 4.62 bump (rhbz#2267294)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4.61-1
- 4.61 bump (rhbz#2257292)

* Fri Nov 10 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4.60-2
- Remove unused dependency perl(Test::CPAN::Changes)

* Wed Nov 01 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4.60-1
- 4.60 bump (rhbz#2247441)

* Tue Oct 03 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4.59-1
- 4.59 bump (rhbz#2241705)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 04 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4.57-1
- 4.57 bump

* Fri Mar 03 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4.56-1
- 4.56 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4.55-1
- 4.55 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4.54-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4.54-2
- Perl 5.36 rebuild

* Mon Feb 07 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4.54-1
- 4.54 bump

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.53-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.53-1
- 4.53 bump

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.52-4
- Perl 5.34 re-rebuild of bootstrapped packages

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.52-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.52-2
- Perl 5.34 rebuild

* Tue May 04 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.52-1
- 4.52 bump

* Mon Mar 01 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.51-3
- Package tests

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 06 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.51-1
- 4.51 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.50-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.50-2
- Perl 5.32 rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.50-1
- 4.50 bump

* Mon Jun 08 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.49-1
- 4.49 bump

* Tue Jun 02 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.48-1
- 4.48 bump

* Mon May 04 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.47-1
- 4.47 bump

* Tue Feb 04 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.46-1
- 4.46 bump

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.45-1
- 4.45 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.44-1
- 4.44 bump

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.43-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.43-2
- Perl 5.30 rebuild

* Thu May 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.43-1
- 4.43 bump

* Wed Mar 27 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.42-1
- 4.42 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 20 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.40-1
- 4.40 bump

* Tue Aug 14 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.39-1
- 4.39 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.38-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.38-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.38-1
- 4.38 bump

* Wed Nov 01 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.37-1
- 4.37 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.36-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.36-2
- Perl 5.26 rebuild

* Fri Apr 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.36-1
- 4.36 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 14 2016 Petr Pisar <ppisar@redhat.com> - 4.35-1
- 4.35 bump

* Mon Sep 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.33-1
- 4.33 bump

* Wed Jul 20 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.32-1
- 4.32 bump

* Wed Jun 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.31-1
- 4.31 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.28-6
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.28-5
- Perl 5.24 rebuild

* Wed Apr 20 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.28-4
- Don't BR Test::CPAN::Changes when bootstrapping

* Thu Mar 17 2016 Petr Pisar <ppisar@redhat.com> - 4.28-3
- Drop Test::Deep patch

* Tue Mar 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.28-2
- Update patch which makes Test::Deep optional

* Mon Mar 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.28-1
- 4.28 bump

* Wed Mar 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.27-1
- 4.27 bump

* Mon Feb 08 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.26-1
- 4.26 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 22 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.25-1
- 4.25 bump

* Mon Dec 21 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.24-1
- 4.24 bump

* Mon Oct 19 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.22-1
- 4.22 bump

* Tue Jun 23 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.21-1
- 4.21 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.20-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.20-2
- Perl 5.22 rebuild

* Mon Jun 01 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.20-1
- 4.20 bump

* Mon Apr 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.15-1
- 4.15 bump
- Package examples directory as documentation

* Wed Apr 01 2015 Petr Pisar <ppisar@redhat.com> - 4.14-1
- 4.14 bump

* Fri Feb 13 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.13-1
- 4.13 bump
- Make Test::NoWarnings tests optional

* Wed Dec 10 2014 Petr Pisar <ppisar@redhat.com> - 4.04-2
- Make Test::Deep tests optional as it's not in the core in contrast to the CGI

* Fri Sep 19 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.04-1
- 4.04 bump

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.03-2
- Perl 5.20 rebuild

* Mon Jul 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.03-1
- 4.03 bump

* Thu Jun 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.02-1
- 4.02 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.01-1
- 4.01 bump

* Mon May 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.00-1
- 4.00 bump
  - CGI::Fast split out into its own distribution

* Wed Feb 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.65-1
- 3.65 bump

* Tue Nov 26 2013 Petr Pisar <ppisar@redhat.com> - 3.64-1
- 3.64 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.63-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 3.63-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.63-4
- Perl 5.18 rebuild

* Mon Jun 24 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3.63-3
- Specify all dependencies
- Update License - CGI.pm is distributed under GPL and Artistic 2.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Petr Pisar <ppisar@redhat.com> - 3.63-1
- 3.63 bump

* Wed Nov 14 2012 Petr Pisar <ppisar@redhat.com> - 3.62-1
- 3.62 bump

* Tue Nov 06 2012 Petr Šabata <contyk@redhat.com> - 3.61-1
- 3.61 bump, no code changes

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 3.60-1
- 3.60 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.51-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3.51-7
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 3.51-6
- Clean spec file
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.51-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 3.51-4
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.51-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.51-1
- update to fix CVE-2010-2761

* Mon Nov 29 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.50-2
- remove -test sub-package, which would be needed also in perl-core

* Mon Nov 29 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.50-1
- initial dual-life package

