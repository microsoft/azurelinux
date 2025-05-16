Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Getopt-Long
Version:        2.58
Release:        3%{?dist}
Summary:        Extended processing of command line options
License:        GPL-2.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Getopt-Long
Source0:        https://cpan.metacpan.org/authors/id/J/JV/JV/Getopt-Long-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(lib)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(Test::More)
Requires:       perl(Text::ParseWords)
# Recommended:
Requires:       perl(Pod::Usage) >= 1.14
# Dependencies on these Perl 4 files are generated as perl(foo.pl):
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides:       perl(newgetopt.pl) = %{version}

%description
The Getopt::Long module implements an extended getopt function called
GetOptions(). It parses the command line from @ARGV, recognizing and removing
specified options and their possible values.  It adheres to the POSIX syntax
for command line options, with GNU extensions. In general, this means that
options have long names instead of single letters, and are introduced with
a double dash "--". Support for bundling of command line options, as was the
case with the more traditional single-letter approach, is provided but not
enabled by default.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(newgetopt.pl)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Getopt-Long-%{version}

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
%doc Changes examples README.md
%dir %{perl_vendorlib}/Getopt
%{perl_vendorlib}/Getopt/Long*
%{perl_vendorlib}/newgetopt.pl*
%{_mandir}/man3/Getopt::Long*

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue May 13 2025 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 2.58-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.58-1
- 2.58 bump (rhbz#2291318)

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.57-510
- Increase release to favour standalone package

* Tue May 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.57-4
- Add directory %%{perl_vendorlib}/Getopt to %%files (rhbz#2282000)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.57-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.57-1
- 2.57 bump (rhbz#2249036)

* Thu Nov 09 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.55-1
- 2.55 bump (rhbz#2248884)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.54-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.54-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.54-1
- 2.54 bump

* Wed Nov 16 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.53-1
- 2.53 bump
- Package tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.52-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.52-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.52-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.52-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.52-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 Petr Pisar <ppisar@redhat.com> - 1:2.52-1
- 2.52 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.51-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.51-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Petr Pisar <ppisar@redhat.com> - 1:2.51-1
- 2.51 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.50-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.50-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.50-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.50-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.50-416
- Increase release to favour standalone package

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.50-2
- Perl 5.26 rebuild

* Mon May 29 2017 Petr Pisar <ppisar@redhat.com> - 2.50-1
- 2.50 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 2.49.1-1
- 2.49.1 bump

* Wed Jun 15 2016 Petr Pisar <ppisar@redhat.com> - 2.49-1
- 2.49 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.48-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Petr Pisar <ppisar@redhat.com> - 2.48-1
- 2.48 bump

* Wed Jun 17 2015 Petr Pisar <ppisar@redhat.com> - 2.47-1
- 2.47 bump

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.46-2
- Perl 5.22 rebuild

* Tue Jun 02 2015 Petr Pisar <ppisar@redhat.com> - 2.46-1
- 2.46 bump

* Tue Feb 24 2015 Petr Pisar <ppisar@redhat.com> - 2.45-1
- 2.45 bump

* Thu Feb 19 2015 Petr Pisar <ppisar@redhat.com> - 2.44-1
- 2.44 bump

* Fri Jan 30 2015 Petr Pisar <ppisar@redhat.com> - 2.43-1
- 2.43 bump

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.42-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.42-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 02 2013 Petr Pisar <ppisar@redhat.com> - 2.42-1
- 2.42 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.41-2
- Link minimal build-root packages against libperl.so explicitly

* Wed Jul 10 2013 Petr Pisar <ppisar@redhat.com> - 2.41-1
- 2.41 bump

* Thu Jun 20 2013 Petr Pisar <ppisar@redhat.com> - 2.40-1
- 2.40 bump

* Fri Apr 05 2013 Petr Pisar <ppisar@redhat.com> 2.39-1
- Specfile autogenerated by cpanspec 1.78.
