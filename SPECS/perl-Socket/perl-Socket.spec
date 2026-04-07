# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Socket
Epoch:          4
Version:        2.040
Release:        2%{?dist}
Summary:        Networking constants and support functions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Socket
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Socket-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::Constant) >= 0.23
# ExtUtils::Constant::ProxySubs not used
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.6.1
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Scalar::Util is needed only if getaddrinfo(3) does not exist. Not our case.
BuildRequires:  perl(warnings::register)
BuildRequires:  perl(XSLoader)
# Tests only:
BuildRequires:  perl(Errno)
BuildRequires:  perl(Test::More)
Requires:       perl(:VERSION) >= 5.6.1

%{?perl_default_filter}

%description
This Perl module provides a variety of constants, structure manipulators and
other functions related to socket-based networking. The values and functions
provided are useful when used in conjunction with Perl core functions such as
socket(), setsockopt() and bind(). It also provides several other support
functions, mostly for dealing with conversions of network addresses between
human-readable and native binary forms, and for hostname resolver operations.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Socket-%{version}

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
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
%license Artistic Copying LICENSE
%doc Changes
%{perl_vendorarch}/auto/Socket*
%{perl_vendorarch}/Socket*
%{_mandir}/man3/Socket*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.040-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.040-1
- 2.040 bump (rhbz#2382324)

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.039-2
- Perl 5.42 rebuild

* Mon Jun 30 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.039-1
- 2.039 bump (rhbz#2375527)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.038-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.038-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.038-510
- Increase release to favour standalone package

* Tue Apr 16 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.038-1
- 2.038 bump (rhbz#2275188)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.037-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.037-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.037-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.037-2
- Perl 5.38 rebuild

* Tue Jun 06 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.037-1
- 2.037 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.036-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 22 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.036-1
- 2.036 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.035-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.035-1
- 2.035 bump

* Tue Jun 28 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.034-1
- 2.034 bump

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.033-488
- Increase release to favour standalone package

* Mon May 02 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.033-1
- 2.033 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.032-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.032-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.032-1
- 2.032 bump
- Package tests

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.031-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.031-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.031-1
- 2.031 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.030-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Petr Pisar <ppisar@redhat.com> - 4:2.030-1
- 2.030 bump

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.029-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.029-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.029-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.029-3
- Perl 5.30 rebuild

* Mon Apr 15 2019 Petr Pisar <ppisar@redhat.com> - 4:2.029-2
- Make Socket::inet_aton() thread safe (bug #1693293)

* Fri Feb 22 2019 Petr Pisar <ppisar@redhat.com> - 4:2.029-1
- 2.029 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.027-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.027-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.027-416
- Increase release to favour standalone package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.027-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Petr Pisar <ppisar@redhat.com> - 4:2.027-1
- 2.027 bump

* Fri Jan 12 2018 Petr Pisar <ppisar@redhat.com> - 4:2.026-1
- 2.026 bump

* Fri Jan 12 2018 Petr Pisar <ppisar@redhat.com> - 4:2.025-2
- Fix compiler warnings (CPAN RT#124044)

* Wed Jan 10 2018 Petr Pisar <ppisar@redhat.com> - 4:2.025-1
- 2.025 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.024-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.024-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.024-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.024-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.024-1
- 2.024 bump

* Thu Aug 04 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.023-1
- 2.023 bump

* Tue Aug 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.022-1
- 2.022 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.021-3
- Increase epoch to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.021-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 19 2015 Petr Pisar <ppisar@redhat.com> - 3:2.021-1
- 2.021 bump

* Thu Jun 25 2015 Petr Pisar <ppisar@redhat.com> - 3:2.020-1
- 2.020 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:2.019-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:2.019-2
- Perl 5.22 rebuild
- Increase Epoch to favour standalone package

* Thu Apr 30 2015 Petr Pisar <ppisar@redhat.com> - 2:2.019-1
- 2.019 bump

* Fri Feb 13 2015 Petr Pisar <ppisar@redhat.com> - 2:2.018-1
- 2.018 bump

* Wed Feb 11 2015 Petr Pisar <ppisar@redhat.com> - 2:2.017-1
- 2.017 bump

* Thu Oct 09 2014 Petr Pisar <ppisar@redhat.com> - 2:2.016-1
- 2.016 bump

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:2.015-3
- Increase Epoch to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.015-2
- Perl 5.20 rebuild

* Mon Aug 18 2014 Petr Pisar <ppisar@redhat.com> - 1:2.015-1
- 0.15 bump

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 1:2.014-1
- 2.014 bump

* Tue Oct 29 2013 Petr Pisar <ppisar@redhat.com> - 1:2.013-1
- 2.013 bump

* Tue Sep 10 2013 Petr Pisar <ppisar@redhat.com> - 1:2.012-1
- 2.012 bump

* Tue Aug 06 2013 Petr Pisar <ppisar@redhat.com> - 1:2.011-1
- 2.011 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.010-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.010-3
- Link minimal build-root packages against libperl.so explicitly

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.010-2
- Perl 5.18 rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.010-1
- Increase epoch to compete with perl.spec

* Tue Jun 25 2013 Petr Pisar <ppisar@redhat.com> - 2.010-1
- 2.010 bump

* Fri May 24 2013 Petr Pisar <ppisar@redhat.com> - 2.009-3
- Specify all dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Petr Pisar <ppisar@redhat.com> - 2.009-1
- 2.009 bump

* Thu Jan 03 2013 Petr Pisar <ppisar@redhat.com> - 2.008-1
- 2.008 bump

* Mon Dec 17 2012 Petr Pisar <ppisar@redhat.com> - 2.007-1
- 2.007 bump

* Thu Nov 08 2012 Petr Pisar <ppisar@redhat.com> - 2.006-2
- Update description

* Mon Aug 20 2012 Petr Pisar <ppisar@redhat.com> - 2.006-1
- 2.006 bump

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 2.005-1
- 2.005 bump

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 2.004-1
- 2.004 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2.002-2
- Perl 5.16 rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.002-1
- 2.002 bump

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.001-2
- Perl 5.16 rebuild

* Wed Mar 28 2012 Petr Pisar <ppisar@redhat.com> - 2.001-1
- 2.001 bump (bug-fixing release)

* Tue Mar 27 2012 Petr Pisar <ppisar@redhat.com> - 2.000-3
- Fix invalid write while unpacking AF_UNIX sockaddr (bug #806543)

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 2.000-2
- Increase release number due to F17 build

* Wed Mar 14 2012 Petr Pisar <ppisar@redhat.com> - 2.000-1
- 2.000 bump
- Fix a buffer overflow (RT#75623)

* Wed Feb 22 2012 Petr Pisar <ppisar@redhat.com> - 1.99-1
- 1.99 bump

* Thu Feb 16 2012 Petr Pisar <ppisar@redhat.com> - 1.98-1
- 1.98 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Petr Pisar <ppisar@redhat.com> - 1.97-1
- 1.97 bump
- License texts added

* Mon Dec 12 2011 Petr Pisar <ppisar@redhat.com> - 1.96-1
- 1.96 bump

* Fri Dec 02 2011 Petr Pisar <ppisar@redhat.com> - 1.95-1
- 1.95 bump

* Wed Nov 23 2011 Petr Pisar <ppisar@redhat.com> 1.94.07-1
- 1.94_07 packaged.
