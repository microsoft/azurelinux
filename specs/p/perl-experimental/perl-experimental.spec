# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-experimental
Version:        0.036
Release:        2%{?dist}
Summary:        Experimental features made easy
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/experimental
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/experimental-%{version}.tar.gz
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
BuildRequires:  perl(Carp)
# feature is highly recommended on perl >= 5.10
BuildRequires:  perl(feature)
BuildRequires:  perl(version)
# Tests:
BuildRequires:  perl(Test::More) >= 0.89
# feature is highly recommended on perl >= 5.10
Requires:       perl(feature)

%description
This pragma provides an easy and convenient way to enable or disable
experimental features.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n experimental-%{version}

# Help file to recognise the Perl scripts
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
%license LICENSE
%doc Changes README
%{perl_vendorlib}/experimental*
%{perl_vendorlib}/stable*
%{_mandir}/man3/experimental*
%{_mandir}/man3/stable*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.036-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.036-1
- 0.036 bump (rhbz#2382306)

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.035-519
- Increase release to favour standalone package

* Mon May 05 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.035-1
- 0.035 bump (rhbz#2363256)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.034-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.034-1
- 0.034 bump (rhbz#2336813)

* Thu Jan 02 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.033-1
- 0.033 bump (rhbz#2333919)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.032-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.032-510
- Increase release to favour standalone package

* Fri Apr 26 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.032-1
- 0.032 bump (rhbz#2277236)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.031-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.031-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.031-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.031-499
- Increase release to favour standalone package

* Wed Feb 01 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.031-1
- 0.031 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.030-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.030-1
- 0.030 bump

* Wed Oct 26 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.029-1
- 0.029 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.028-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.028-488
- Increase release to favour standalone package

* Tue Apr 26 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.028-1
- 0.028 bump

* Wed Feb 09 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.027-1
- 0.027 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.025-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.025-1
- 0.025 bump

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-478
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.024-477
- Increase release to favour standalone package

* Mon May 03 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.024-1
- 0.024 bump
- Package test

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.022-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.022-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-2
- Perl 5.32 rebuild

* Tue May 05 2020 Petr Pisar <ppisar@redhat.com> - 0.022-1
- 0.022 bump

* Mon Feb 24 2020 Petr Pisar <ppisar@redhat.com> - 0.021-1
- 0.021 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.020-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.020-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.020-438
- Increase release to favour standalone package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.020-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.020-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.020-2
- Perl 5.28 rebuild

* Thu May 10 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.020-1
- 0.020 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Petr Pisar <ppisar@redhat.com> - 0.019-1
- 0.019 bump

* Fri Dec 01 2017 Petr Pisar <ppisar@redhat.com> - 0.018-1
- 0.018 bump

* Wed Nov 15 2017 Petr Pisar <ppisar@redhat.com> - 0.017-1
- 0.017 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-366
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 12 2015 Petr Pisar <ppisar@redhat.com> - 0.016-1
- 0.016 bump

* Mon Oct 05 2015 Petr Pisar <ppisar@redhat.com> - 0.015-1
- 0.015 bump

* Mon Sep 14 2015 Petr Pisar <ppisar@redhat.com> - 0.014-1
- 0.014 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-3
- Perl 5.22 rebuild

* Thu Dec 11 2014 Petr Pisar <ppisar@redhat.com> - 0.013-2
- Use ExtUtils::MakeMaker for building

* Mon Oct 27 2014 Petr Pisar <ppisar@redhat.com> - 0.013-1
- 0.013 bump

* Mon Oct 13 2014 Petr Pisar <ppisar@redhat.com> - 0.012-1
- 0.012 bump

* Mon Sep 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-1
- 0.011 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-2
- Perl 5.20 rebuild

* Fri Aug 22 2014 Petr Pisar <ppisar@redhat.com> - 0.010-1
- 0.010 bump

* Mon Aug 18 2014 Petr Pisar <ppisar@redhat.com> - 0.009-1
- 0.009 bump

* Mon Jul 07 2014 Petr Pisar <ppisar@redhat.com> - 0.008-1
- 0.008 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Petr Pisar <ppisar@redhat.com> - 0.007-1
- 0.007 bump

* Mon Jan 20 2014 Petr Pisar <ppisar@redhat.com> - 0.006-1
- 0.006 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.005-2
- Perl 5.18 rebuild

* Mon Jun 10 2013 Petr Pisar <ppisar@redhat.com> - 0.005-1
- 0.005 bump

* Fri Jun 07 2013 Petr Pisar <ppisar@redhat.com> - 0.004-1
- 0.004 bump

* Wed May 29 2013 Petr Pisar <ppisar@redhat.com> 0.003-1
- Specfile autogenerated by cpanspec 1.78.
