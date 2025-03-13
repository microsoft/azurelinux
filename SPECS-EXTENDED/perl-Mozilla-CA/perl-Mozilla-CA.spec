Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Mozilla-CA
# You do not need to back-port a new version for updating a list of the
# certificates. They are taken from ca-certificates package instead
# per bug #738383.
Version:        20240730
Release:        2%{?dist}
Summary:        Mozilla's CA certificate bundle in PEM format
# README:                       MPL-2.0
## Unbundled
# mk-ca-bundle.pl:              MIT
# lib/Mozilla/CA/cacert.pem:    MPL-2.0
License:        MPL-2.0
URL:            https://metacpan.org/release/Mozilla-CA
Source0:        https://cpan.metacpan.org/authors/id/L/LW/LWP/Mozilla-CA-%{version}.tar.gz#/perl-Mozilla-CA-%{version}.tar.gz
# Use a CA bundle from ca-certificates package, bug #738383
Patch0:         Mozilla-CA-20240730-Redirect-to-ca-certificates-bundle.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  ca-certificates
BuildRequires:  perl(strict)
BuildRequires:  perl(File::Spec)
# Tests:
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       ca-certificates

%description
Mozilla::CA provides a path to ca-certificates copy of Mozilla's bundle of
certificate authority certificates in a form that can be consumed by modules
and libraries based on OpenSSL.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Mozilla-CA-%{version}
%patch -P0 -p1
# Remove a bundled CA bundle for sure
rm lib/Mozilla/CA/cacert.pem
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
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Dec 16 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 20240730-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Aug 01 2024 Michal Josef Špaček <mspacek@redhat.com> - 20240730-1
- 20240730 bump

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240313-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 15 2024 Michal Josef Špaček <mspacek@redhat.com> - 20240313-1
- 20240313 bump

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231213-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231213-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 14 2023 Michal Josef Špaček <mspacek@redhat.com> - 20231213-1
- 20231213 bump

* Fri Aug 25 2023 Michal Josef Špaček <mspacek@redhat.com> - 20230821-1
- 20230821 bump

* Tue Aug 15 2023 Michal Josef Špaček <mspacek@redhat.com> - 20230807-1
- 20230807 bump

* Thu Aug 03 2023 Michal Josef Špaček <mspacek@redhat.com> - 20230801-1
- 20230801 bump
- Fix %patch macro usage

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221114-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221114-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 15 2022 Michal Josef Špaček <mspacek@redhat.com> - 20221114-1
- 20221114 bump

* Mon Nov 07 2022 Michal Josef Špaček <mspacek@redhat.com> - 20211001-5
- Package tests
- Unify variable to macro
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 20211001-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 02 2021 Jitka Plesnikova <jplesnik@redhat.com> - 20211001-1
- 20211001 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200520-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 20200520-5
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200520-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200520-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 20200520-2
- Perl 5.32 rebuild

* Wed May 20 2020 Petr Pisar <ppisar@redhat.com> - 20200520-1
- 20200520 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20180117-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180117-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 20180117-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180117-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180117-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 20180117-2
- Perl 5.28 rebuild

* Fri Mar 02 2018 Petr Pisar <ppisar@redhat.com> - 20180117-1
- 20180117 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20160104-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160104-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 20160104-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160104-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 20160104-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20160104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Petr Pisar <ppisar@redhat.com> - 20160104-1
- 20160104 bump

* Wed Aug 26 2015 Petr Pisar <ppisar@redhat.com> - 20150826-1
- 20150826 bump
- License changed from (MPLv1.1 or LGPLv2+ or GPLv2+) to (MPLv2.0)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20141217-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 20141217-2
- Perl 5.22 rebuild

* Fri Jan 02 2015 Petr Pisar <ppisar@redhat.com> - 20141217-1
- 20141217 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 20130114-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130114-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Petr Pisar <ppisar@redhat.com> - 20130114-5
- Specify all dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130114-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 20130114-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130114-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Petr Pisar <ppisar@redhat.com> - 20130114-1
- 20130114 bump

* Thu Aug 23 2012 Petr Pisar <ppisar@redhat.com> - 20120823-1
- 20120823 bump

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 20120822-1
- 20120822 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120309-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 20120309-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Petr Pisar <ppisar@redhat.com> - 20120309-1
- 20120309 bump

* Wed Jan 18 2012 Petr Pisar <ppisar@redhat.com> - 20120118-1
- 20120118 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20111025-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Petr Pisar <ppisar@redhat.com> - 20111025-1
- 20111025 bump
- Remove defattr from spec code

* Fri Sep 16 2011 Petr Pisar <ppisar@redhat.com> - 20110914-2
- Redirect to ca-certificates bundle (bug #738383)

* Thu Sep 15 2011 Petr Pisar <ppisar@redhat.com> - 20110914-1
- 20110914 bump

* Mon Sep 05 2011 Petr Pisar <ppisar@redhat.com> - 20110904-1
- 20110904 bump

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 20110409-2
- Perl mass rebuild

* Mon Apr 11 2011 Petr Pisar <ppisar@redhat.com> - 20110409-1
- 20110409 bump

* Mon Mar 28 2011 Petr Pisar <ppisar@redhat.com> 20110301-1
- Specfile autogenerated by cpanspec 1.78.
- Correct License tag
- Remove BuildRoot stuff
