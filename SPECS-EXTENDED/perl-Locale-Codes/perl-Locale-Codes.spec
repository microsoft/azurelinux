Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Locale-Codes
Version:        3.81
Release:        1%{?dist}
Summary:        Distribution of modules to handle locale codes
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Locale-Codes
Source0:        https://cpan.metacpan.org/authors/id/S/SB/SBECK/Locale-Codes-%{version}.tar.gz#/perl-Locale-Codes-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
# deprecate not used on perl < 5.27.7
BuildRequires:  perl(Exporter)
BuildRequires:  perl(if)
BuildRequires:  perl(utf8)
# Tests:
# Release tests are deleted
BuildRequires:  perl(deprecate)
BuildRequires:  perl(Test::Inter) >= 1.09
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# deprecate not used on perl < 5.27.7

# Filter dependencies on private modules, they are not provided. Generator:
# for F in $(find lib -type f); do perl -e '$/ = undef; $_ = <>; if (/^package #\R([\w:]*);/m) { print qq{|^perl\\\\($1\\\\)} }' "$F"; done
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Locale::Codes::Country_Retired\\)|^perl\\(Locale::Codes::LangFam_Retired\\)|^perl\\(Locale::Codes::Script_Retired\\)|^perl\\(Locale::Codes::LangExt_Codes\\)|^perl\\(Locale::Codes::LangFam_Codes\\)|^perl\\(Locale::Codes::Script_Codes\\)|^perl\\(Locale::Codes::Language_Codes\\)|^perl\\(Locale::Codes::LangExt_Retired\\)|^perl\\(Locale::Codes::Currency_Codes\\)|^perl\\(Locale::Codes::LangVar_Retired\\)|^perl\\(Locale::Codes::Language_Retired\\)|^perl\\(Locale::Codes::Country_Codes\\)|^perl\\(Locale::Codes::LangVar_Codes\\)|^perl\\(Locale::Codes::Currency_Retired\\)
# Filter dependencies on test subscripts
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(do_tests\\.pl\\)

%description
Locale-Codes is a distribution containing a set of modules. The modules
each deal with different types of codes which identify parts of the locale
including languages, countries, currency, etc.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}-%{version}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Locale-Codes-%{version}
chmod -x examples/*
chmod +x t/*.pl
# Delete release tests
rm t/_*
perl -i -lne 'print $_ unless m{\At/_}' MANIFEST
# Delete unused files
rm t/runtests t/runtests.bat
perl -i -lne 'print $_ unless m{\At/runtests}' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
#!/usr/bin/sh
cd %{_libexecdir}/%{name} && exec prove -j $(getconf _NPROCESSORS_ONLN)
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
unset RELEASE_TESTING
make test

%files
%license LICENSE
%doc Changes examples README README.first
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue Dec 24 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 3.81-1
- Update to 3.81
- License verified.

* Fri Apr 22 2022 Muhammad Falak <mwani@microsoft.com> - 3.66-4
- Add an explicit BR on `perl(deprecate)` to enable ptest
- License verified

* Mon Nov 01 2021 Muhammad Falak <mwani@microsoft.com> - 3.66-3
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.66-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Dec 01 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.66-1
- 3.66 bump

* Wed Sep 02 2020 Petr Pisar <ppisar@redhat.com> - 3.65-1
- 3.65 bump

* Wed Jun 03 2020 Petr Pisar <ppisar@redhat.com> - 3.64-1
- 3.64 bump

* Wed Mar 04 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.63-1
- 3.63 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Petr Pisar <ppisar@redhat.com> - 3.62-1
- 3.62 bump
- Package tests

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Petr Pisar <ppisar@redhat.com> - 3.61-1
- 3.61 bump

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.60-2
- Perl 5.30 rebuild

* Fri Mar 01 2019 Petr Pisar <ppisar@redhat.com> - 3.60-1
- 3.60 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Petr Pisar <ppisar@redhat.com> - 3.59-1
- 3.59 bump

* Tue Sep 04 2018 Petr Pisar <ppisar@redhat.com> - 3.58-1
- 3.58 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.57-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.57-2
- Perl 5.28 rebuild

* Mon Jun 04 2018 Petr Pisar <ppisar@redhat.com> - 3.57-1
- 3.57 bump

* Fri Mar 02 2018 Petr Pisar <ppisar@redhat.com> - 3.56-1
- 3.56 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 20 2017 Petr Pisar <ppisar@redhat.com> - 3.55-1
- 3.55 bump

* Mon Sep 04 2017 Petr Pisar <ppisar@redhat.com> - 3.54-1
- 3.54 bump

* Wed Jul 26 2017 Petr Pisar <ppisar@redhat.com> - 3.53-1
- 3.53 bump

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.52-2
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Petr Pisar <ppisar@redhat.com> - 3.52-1
- 3.52 bump

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.51-2
- Perl 5.26 rebuild

* Mon Apr 10 2017 Petr Pisar <ppisar@redhat.com> - 3.51-1
- 3.51 bump

* Thu Mar 02 2017 Petr Pisar <ppisar@redhat.com> - 3.50-1
- 3.50 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Petr Pisar <ppisar@redhat.com> - 3.42-1
- 3.42 bump

* Mon Nov 21 2016 Petr Pisar <ppisar@redhat.com> - 3.41-1
- 3.41 bump

* Mon Sep 05 2016 Petr Pisar <ppisar@redhat.com> - 3.40-1
- 3.40 bump

* Wed Jun 01 2016 Petr Pisar <ppisar@redhat.com> - 3.39-1
- 3.39 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.38-2
- Perl 5.24 rebuild

* Thu Mar 03 2016 Petr Pisar <ppisar@redhat.com> - 3.38-1
- 3.38 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Petr Pisar <ppisar@redhat.com> - 3.37-1
- 3.37 bump

* Wed Sep 02 2015 Petr Pisar <ppisar@redhat.com> - 3.36-1
- 3.36 bump (Locale::Codes::_delete_code_alias() removed)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.35-2
- Perl 5.22 rebuild

* Tue Jun 02 2015 Petr Pisar <ppisar@redhat.com> - 3.35-1
- 3.35 bump

* Tue Mar 03 2015 Petr Pisar <ppisar@redhat.com> - 3.34-1
- 3.34 bump

* Fri Dec 05 2014 Petr Pisar <ppisar@redhat.com> - 3.33-1
- 3.33 bump

* Wed Sep 10 2014 Petr Pisar <ppisar@redhat.com> - 3.32-1
- 3.32 bump

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.31-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 3.31-1
- 3.31 bump

* Wed Mar 05 2014 Petr Pisar <ppisar@redhat.com> - 3.30-1
- 3.30 bump

* Thu Jan 30 2014 Petr Pisar <ppisar@redhat.com> - 3.29-1
- 3.29 bump

* Wed Dec 04 2013 Petr Pisar <ppisar@redhat.com> - 3.28-2
- Filter private module Locale::Codes::LangFam_Retired from dependencies

* Tue Dec 03 2013 Petr Pisar <ppisar@redhat.com> - 3.28-1
- 3.28 bump

* Thu Sep 12 2013 Petr Pisar <ppisar@redhat.com> - 3.27-2
- Filter dependencies on private modules

* Tue Sep 10 2013 Petr Pisar <ppisar@redhat.com> - 3.27-1
- 3.27 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.26-2
- Perl 5.18 rebuild

* Fri Jun 07 2013 Petr Pisar <ppisar@redhat.com> - 3.26-1
- 3.26 bump

* Fri Mar 01 2013 Petr Pisar <ppisar@redhat.com> - 3.25-1
- 3.25 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Petr Pisar <ppisar@redhat.com> - 3.24-1
- 3.24 bump

* Tue Nov 20 2012 Petr Šabata <contyk@redhat.com> - 3.23-2
- Add missing deps
- Drop command macros
- Modernize spec

* Tue Sep 04 2012 Petr Pisar <ppisar@redhat.com> - 3.23-1
- 3.23 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3.22-2
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Pisar <ppisar@redhat.com> - 3.22-1
- 3.22 bump

* Mon Jun 04 2012 Petr Pisar <ppisar@redhat.com> - 3.21-2
- The POD tests do not run by default anymore
- Switch build script from Module::Build to EU::MM

* Fri Mar 02 2012 Petr Pisar <ppisar@redhat.com> - 3.21-1
- 3.21 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Petr Pisar <ppisar@redhat.com> - 3.20-1
- 3.20 bump

* Thu Sep 01 2011 Petr Pisar <ppisar@redhat.com> - 3.18-1
- 3.18 bump

* Thu Jun 30 2011 Petr Pisar <ppisar@redhat.com> 3.17-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr
