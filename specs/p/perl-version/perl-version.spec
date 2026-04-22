# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_version_enables_optional_test
%else
%bcond_with perl_version_enables_optional_test
%endif

Name:           perl-version
Epoch:          9
Version:        0.99.33
%global module_version 0.9933
Release: 522%{?dist}
Summary:        Perl extension for Version Objects
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/version
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/version-%{module_version}.tar.gz
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
# ExtUtils::CBuilder not helpful
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Temp) >= 0.13
BuildRequires:  perl(strict)
# Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(if)
BuildRequires:  perl(locale)
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(warnings)
BuildRequires:  perl(warnings::register)
BuildRequires:  perl(XSLoader)
# Tests only
BuildRequires:  perl(base)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(I18N::Langinfo)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More) >= 0.45
# Optional tests
%if %{with perl_version_enables_optional_test} && ! %{defined perl_bootstrap}
BuildRequires:  perl(Test::Taint)
%endif
Requires:       perl(B)
Requires:       perl(Carp)
Requires:       perl(locale)
Requires:       perl(UNIVERSAL)
Requires:       perl(warnings)
Requires:       perl(XSLoader)

%{?perl_default_filter}
# version::vxs is private module (see bug #633775)
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(version::vxs\\)
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
Version objects were added to Perl in 5.10. This module implements version
objects for older version of Perl and provides the version object API for
all versions of Perl. All previous releases before 0.74 are deprecated and
should not be used due to incompatible API changes. Version 0.77 introduces
the new 'parse' and 'declare' methods to standardize usage. You are
strongly urged to set 0.77 as a minimum in your code.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(I18N::Langinfo)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n version-%{module_version}

# Help file to recognise the Perl scripts
for F in t/*.t t/survey_locales; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done
perl -MConfig -i -pe 's/\A#!.*perl/$Config{startperl}/' t/*.pm

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" UNINST=0 NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc CHANGES README
%doc %{perl_vendorarch}/version.pod
%dir %{perl_vendorarch}/version/
%doc %{perl_vendorarch}/version/Internals.pod
%{perl_vendorarch}/auto/version/
%{perl_vendorarch}/version.pm
%{perl_vendorarch}/version/vpp.pm
%{perl_vendorarch}/version/vxs.pm
%{perl_vendorarch}/version/regex.pm
%{_mandir}/man3/version.3pm*
%{_mandir}/man3/version::Internals.3pm*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9:0.99.33-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 9:0.99.33-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 9:0.99.33-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9:0.99.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Jitka Plesnikova <jplesnik@redhat.com> - 9:0.99.33-1
- 0.9233 bump (rhbz#2308052)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9:0.99.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 9:0.99.32-3
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 9:0.99.32-2
- Increase epoch to favour standalone package

* Mon Apr 29 2024 Jitka Plesnikova <jplesnik@redhat.com> - 8:0.99.32-1
- 0.9932 bump (rhbz#2277524)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8:0.99.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8:0.99.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 8:0.9930-1
- 0.9930 bump (rhbz#2238421)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8:0.99.29-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 8:0.99.29-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 8:0.99.29-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8:0.99.29-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8:0.99.29-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 8:0.99.29-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 8:0.99.29-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8:0.99.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8:0.99.29-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 8:0.99.29-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 8:0.99.29-2
- Increase epoch to favour standalone package

* Mon Apr 19 2021 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.29-1
- 0.9929 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7:0.99.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.28-1
- 0.9928 bump

* Fri Aug 21 2020 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.27-458
- 0.9927 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7:0.99.24-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.24-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.24-456
- Increase release to favour standalone package

* Thu Feb 06 2020 Tom Stellard <tstellar@redhat.com> - 7:0.99.24-443
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMake

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7:0.99.24-442
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Petr Pisar <ppisar@redhat.com> - 7:0.99.24-441
- Do not clobber memory when switching a locale (Perl GH#17054)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7:0.99.24-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.24-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.24-438
- Increase release to favour standalone package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7:0.99.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7:0.99.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.24-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.24-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7:0.99.24-2
- Perl 5.28 rebuild

* Fri Apr 20 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6:0.99.24-1
- 0.9924 bump

* Mon Apr 16 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6:0.99.23-1
- 0.9923 bump

* Thu Apr 12 2018 Petr Pisar <ppisar@redhat.com> - 6:0.99.21-1
- 0.9921 bump

* Mon Apr 09 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6:0.99.20-1
- 0.9920 bump

* Fri Mar 09 2018 Petr Pisar <ppisar@redhat.com> - 6:0.99.18-7
- Remove useless build-time dependency on ExtUtils::CBuilder
- Fix documentation about numify() and stringify() trailing zeros
  (CPAN RT#64635, CPAN RT#122858)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6:0.99.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6:0.99.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6:0.99.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6:0.99.18-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6:0.99.18-2
- Perl 5.26 rebuild

* Fri Apr 21 2017 Jitka Plesnikova <jplesnik@redhat.com> - 5:0.99.18-1
- 0.9918 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5:0.99.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 5:0.99.17-1
- 0.9917 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 5:0.99.16-365
- Increase release to favour standalone package

* Mon Mar 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 5:0.99.16-1
- 0.9916 bump

* Sun Mar 06 2016 Petr Šabata <contyk@redhat.com> - 5:0.99.15-1
- 0.9915 bump, documentation updated

* Thu Feb 25 2016 Petr Šabata <contyk@redhat.com> - 5:0.99.14-1
- 0.9914 bump

* Wed Feb 17 2016 Petr Šabata <contyk@redhat.com> - 5:0.99.13-1
- 0.9913 bump
- Backwards-incompatible changes in normal/numify/stringify

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5:0.99.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul  6 2015 Paul Howarth <paul@city-fan.org> - 5:0.99.12-4
- Use UNINST=0 to avoid trying to mess with existing installation during
  rebuild (#1239335)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5:0.99.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:0.99.12-2
- Perl 5.22 rebuild
- Increase Epoch to favour standalone package

* Tue Feb 03 2015 Petr Pisar <ppisar@redhat.com> - 4:0.99.12-1
- 0.9912 bump

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4:0.99.09-3
- Increase Epoch to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3:0.99.09-2
- Perl 5.20 rebuild

* Wed Aug 20 2014 Petr Šabata <contyk@redhat.com> - 3:0.99.09-1
- 0.9909 bump

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.99.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.99.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Petr Šabata <contyk@redhat.com> - 3:0.99.08-1
- 0.9908 bump

* Mon Jan 27 2014 Petr Pisar <ppisar@redhat.com> - 3:0.99.07-2
- Specify all dependencies

* Wed Jan 15 2014 Petr Šabata <contyk@redhat.com> - 3:0.99.07-1
- 0.9907 bugfix bump

* Tue Jan 07 2014 Petr Šabata <contyk@redhat.com> - 3:0.99.06-1
- 0.9906 bump

* Tue Sep 10 2013 Petr Šabata <contyk@redhat.com> - 3:0.99.04-2
- Release bump to (hopefully) fix the build

* Tue Sep 10 2013 Petr Šabata <contyk@redhat.com> - 3:0.99.04-1
- 0.9904 bump

* Mon Aug 26 2013 Petr Šabata <contyk@redhat.com> - 3:0.99.03-1
- 0.9903 bump
- Prefer %%global over %%define

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.99.02-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 3:0.99.02-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3:0.99.02-3
- Perl 5.18 rebuild

* Tue Jul 02 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3:0.99.02-2
- Specify all dependencies

* Thu Mar  7 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3:0.99.02-1
- 0.9902 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.99.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Jitka Plesnikova <jplesnik@redhat.com> - 3:0.99.01-1
- 0.9901 bump

* Tue Aug 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 3:0.99-241
- Add test BR perl(Test::Harness)
- Remove %%defattr

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 3:0.99-240
- Increase release to replace perl sub-package (bug #848961)

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 3:0.99-1
- 0.99 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.88-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3:0.88-9
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 3:0.88-8
- Fix dependencies

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.88-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3:0.88-6
- change path on vendor, so our debuginfo are not conflicting with
  perl core debuginfos

* Sun Jul 24 2011 Iain Arnell <iarnell@gmail.com> 3:0.88-5
- update filtering for rpm 4.9

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3:0.88-4
- Perl mass rebuild

* Fri Apr 08 2011 Petr Pisar <ppisar@redhat.com> - 3:0.88-3
- Unexport private version::vxs module (bug #633775)
- Remove BuildRoot stuff

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> 3:0.88-1
- Update to 0.88
- Revert to Makefile.PL flow as upstream dropped Build.PL to avoid circular
  dependencies
- Install into perl directories rather than vendor directories
- Mark Pod files as %%doc

* Tue Mar 09 2010 Marcela Mašláňová <mmaslano@redhat.com> 3:0.82-1
- Specfile autogenerated by cpanspec 1.78.
