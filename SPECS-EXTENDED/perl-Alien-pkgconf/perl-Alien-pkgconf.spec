Name:           perl-Alien-pkgconf
Version:        0.20
Release:        4%{?dist}
Summary:        Discover pkgconf and libpkgconf
# Other files:  GPL-1.0-or-later OR Artistic-1.0-Perl
## Not used
# patch/pkgconf-solaris-1.3.9.diff: GPL-3.0-or-later WITH Autoconf-exception-macro
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
SourceLicense:  (%{license}) AND GPL-3.0-or-later WITH Autoconf-exception-macro
URL:            https://metacpan.org/release/Alien-pkgconf
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Alien-pkgconf-%{version}.tar.gz
# Accept pkgconf-1.9, we have patched perl-PkgConfig-LibPkgConf, bug #2172713
Patch0:         Alien-pkgconf-0.19-Accept-pkgconf-1.9.patch
# This is a full-arch package because it stores data about arch-specific
# libpkgconf.so library and it stores them into an arch-specific directory.
# But it does not install any ELF, therefore disable debuginfo generation.
%global debug_package %{nil}
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.98
# FFI::CheckLib is optional but provides additional data to bake into a binary
# package
BuildRequires:  perl(FFI::CheckLib)
# script/system.pl is executed at build time
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(JSON::PP) >= 2.27400
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  pkgconf
# Upstream precludes pkgconfig(libpkgconf) >= 1.9.0 because
# PkgConfig-LibPkgConf-0.11 does not support it.
# But we have added the support in downstream.
# <https://github.com/PerlAlien/PkgConfig-LibPkgConf/issues/15>.
BuildRequires:  pkgconfig(libpkgconf) >= 1.5.2
# Run-time:
BuildRequires:  perl(File::ShareDir) >= 1.102
# Tests:
# An XS code is built by Test::Alien::xs_ok() in t/xs.t
BuildRequires:  perl-devel
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test2::V0) >= 0.000065
BuildRequires:  perl(Test::Alien) >= 0.08
# This RPM package ensures libpkgconf.so is installed on the system
Requires:       libpkgconf-devel(%{__isa}) = %(type -p pkgconf >/dev/null && pkgconf --exists libpkgconf && pkgconf --modversion libpkgconf || echo 0)
Requires:       perl(File::ShareDir) >= 1.102
Requires:       perl(JSON::PP) >= 2.27400

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((File::ShareDir|JSON::PP|Test::Alien|Test2::V0)\\)$

%description
This Perl module provides you with the information that you need to invoke
pkgconf or link against libpkgconf. It isn't intended to be used directly,
but rather to provide the necessary package by a CPAN module that needs
libpkgconf, such as PkgConfig::LibPkgConf.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
# An XS code is built by Test::Alien::xs_ok() in t/xs.t
Requires:       perl-devel
Requires:       perl-Test-Harness
Requires:       perl(Test2::V0) >= 0.000065
Requires:       perl(Test::Alien) >= 0.08

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n Alien-pkgconf-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
unset ALIEN_FORCE ALIEN_INSTALL_TYPE
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
# ExtUtils::CBuilder::have_compiler() writes into CWD
# <https://github.com/Perl/perl5/issues/15697>.
set -e
DIR=$(mktemp -d)
cp -a %{_libexecdir}/%{name}/* "$DIR"
pushd "$DIR"
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes README
%dir %{perl_vendorarch}/auto/Alien
%{perl_vendorarch}/auto/Alien/pkgconf
%dir %{perl_vendorarch}/auto/share
%dir %{perl_vendorarch}/auto/share/dist
%{perl_vendorarch}/auto/share/dist/Alien-pkgconf
%dir %{perl_vendorarch}/Alien
%{perl_vendorarch}/Alien/pkgconf.pm
%{_mandir}/man3/Alien::pkgconf.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Aug 07 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.20-4
- Rebuild for pkgconf 2.3.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 16 2024 Petr Pisar <ppisar@redhat.com> - 0.20-2
- Rebuild against pkgconf 2.1.1 (bug #2280677)

* Mon Mar 11 2024 Petr Pisar <ppisar@redhat.com> - 0.20-1
- 0.20 bump

* Mon Mar 11 2024 Petr Pisar <ppisar@redhat.com> - 0.19-10
- Make the build reproducible

* Thu Feb 15 2024 Petr Pisar <ppisar@redhat.com> - 0.19-9
- Fix a priority in the source license value

* Thu Feb 15 2024 Petr Pisar <ppisar@redhat.com> - 0.19-8
- Rebuild against pkgconf 2.1.0 (bug #2264268)
- Define a distinct license for the source package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Petr Pisar <ppisar@redhat.com> - 0.19-4
- Rebuild against pkgconf 1.9.5 (bug #2221456)

* Thu Feb 23 2023 Petr Pisar <ppisar@redhat.com> - 0.19-3
- Rebuild against pkgconf 1.9.4 (bug #2172713)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 25 2022 Petr Pisar <ppisar@redhat.com> - 0.19-1
- 0.19 bump

* Tue Aug 16 2022 Petr Pisar <ppisar@redhat.com> - 0.18-1
- 0.18 bump
- Package the tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-12
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jul 26 2021 Petr Pisar <ppisar@redhat.com> - 0.17-10
- Rebuild against pkgconf 1.8.0 (bug #1985899)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Petr Pisar <ppisar@redhat.com> - 0.17-8
- Rebuild against pkgconf 1.7.4 (bug #1976453)

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-7
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 04 2020 Petr Pisar <ppisar@redhat.com> - 0.17-5
- Rebuild against pkgconf 1.7.3 (bug #1864519)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.17-3
- Perl 5.32 rebuild

* Tue May 26 2020 Petr Pisar <ppisar@redhat.com> - 0.17-2
- Rebuild against pkgconf 1.7.0 (bug #1840033)

* Tue May 19 2020 Petr Pisar <ppisar@redhat.com> - 0.17-1
- 0.17 bump

* Mon Feb 24 2020 Petr Pisar <ppisar@redhat.com> - 0.16-1
- 0.16 bump

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Petr Pisar <ppisar@redhat.com> - 0.15-8
- Rebuild against pkgconf 1.6.3

* Fri Jul 12 2019 Petr Pisar <ppisar@redhat.com> - 0.15-7
- Rebuild against pkgconf 1.6.2

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-6
- Perl 5.30 rebuild

* Wed Mar 27 2019 Petr Pisar <ppisar@redhat.com> - 0.15-5
- Rebuild against pkgconf 1.6.1

* Mon Feb 11 2019 Petr Pisar <ppisar@redhat.com> - 0.15-4
- Rebuild against pkgconf 1.6.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Petr Pisar <ppisar@redhat.com> - 0.15-2
- Rebuild against pkgconf 1.5.4

* Tue Sep 04 2018 Petr Pisar <ppisar@redhat.com> - 0.15-1
- 0.15 bump

* Mon Jul 23 2018 Petr Pisar <ppisar@redhat.com> - 0.14-1
- 0.14 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-2
- Perl 5.28 rebuild

* Fri Jun 29 2018 Petr Pisar <ppisar@redhat.com> - 0.12-1
- 0.12 bump

* Fri Jun 29 2018 Petr Pisar <ppisar@redhat.com> - 0.11-8
- Rebuild against pkgconf 1.5.1

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-7
- Perl 5.28 rebuild

* Sat Mar 31 2018 Neal Gompa <ngompa13@gmail.com> - 0.11-6
- Actually rebuild against pkgconf 1.4.2

* Sat Mar 31 2018 Neal Gompa <ngompa13@gmail.com> - 0.11-5
- Rebuild for pkgconf 1.4.2

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Petr Pisar <ppisar@redhat.com> - 0.11-3
- Rebuild against pkgconf-1.4.1

* Fri Jan 05 2018 Neal Gompa <ngompa13@gmail.com> - 0.11-2
- Rebuild for pkgconf 1.4.0

* Tue Jan 02 2018 Petr Pisar <ppisar@redhat.com> - 0.11-1
- 0.11 bump

* Tue Dec 19 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.10-15
- Rebuild for pkgconf 1.3.90

* Mon Dec 11 2017 Petr Pisar <ppisar@redhat.com> - 0.10-14
- Rebuild against pkgconf-1.3.12

* Wed Nov 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.10-13
- Rebuild against pkgconf-1.3.10

* Mon Oct 02 2017 Petr Pisar <ppisar@redhat.com> - 0.10-12.1
- Really rebuild against pkgconf-1.3.9

* Fri Sep 22 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.10-12
- Rebuild against pkgconf-1.3.9

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Petr Pisar <ppisar@redhat.com> - 0.10-9
- Rebuild against pkgconf-1.3.8

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-8
- Perl 5.26 rebuild

* Tue May 30 2017 Petr Pisar <ppisar@redhat.com> - 0.10-7
- Rebuild against pkgconf-1.3.7

* Fri May 12 2017 Petr Pisar <ppisar@redhat.com> - 0.10-6
- Rebuild against libpkgconf-1.3.6

* Wed Apr 05 2017 Petr Pisar <ppisar@redhat.com> - 0.10-5
- Rebuild against libpkgconf-1.3.5

* Mon Apr 03 2017 Petr Pisar <ppisar@redhat.com> - 0.10-4
- Rebuild against libpkgconf-1.3.4

* Tue Mar 28 2017 Petr Pisar <ppisar@redhat.com> - 0.10-3
- Rebuild against libpkgconf-1.3.3

* Mon Mar 27 2017 Petr Pisar <ppisar@redhat.com> - 0.10-2
- Rebuild against libpkgconf-1.3.2

* Thu Mar 09 2017 Petr Pisar <ppisar@redhat.com> 0.10-1
- Specfile autogenerated by cpanspec 1.78.
