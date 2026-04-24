# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global cpan_version 0.2311
Name:           perl-File-Temp
Epoch:          1
# Normalized version, compete with perl.spec
Version:        0.231.100
Release: 521%{?dist}
Summary:        Return name and handle of a temporary file safely
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/File-Temp
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/File-Temp-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
# Keep Carp::Heavy optional
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(Fcntl) >= 1.03
BuildRequires:  perl(File::Path) >= 2.06
BuildRequires:  perl(File::Spec) >= 0.8
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Seekable)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent) >= 0.221
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
# Symbol not needed
# VMS::Stdio not needed
# Tests:
BuildRequires:  perl(FileHandle)
# Symbol not needed
BuildRequires:  perl(Test::More)
Requires:       perl(POSIX)

# Filter unused dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Symbol|VMS::Stdio\\)

%description
File::Temp can be used to create and open temporary files in a safe way.
There is both a function interface and an object-oriented interface. The
File::Temp constructor or the tempfile() function can be used to return the
name and the open file handle of a temporary file. The tempdir() function
can be used to create a temporary directory.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n File-Temp-%{cpan_version}
chmod -x misc/benchmark.pl
perl -MConfig -p -i -e 's|\A#!/usr/local/bin/perl\b|$Config{startperl}|' \
    misc/benchmark.pl

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
#!/bin/bash
set -e
# Some tests write into temporary files/directories.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
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
# Omit CONTRIBUTING (first half is not relevant to a binary package, second
# half is already presented in POD)
%doc Changes misc README
%{perl_vendorlib}/File*
%{_mandir}/man3/File::Temp*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.231.100-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.231.100-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 16 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.231.100-501
- Package tests

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.231.100-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.231.100-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.231.100-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.231.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 05 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.231.100-1
- 0.2311 bump

* Tue Sep 29 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.231.000-1
- 0.2310 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.230.900-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.230.900-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.230.900-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.230.900-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.230.900-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.230.900-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Petr Pisar <ppisar@redhat.com> - 1:0.230.900-1
- 0.2309 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.230.800-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Petr Pisar <ppisar@redhat.com> - 1:0.230.800-1
- 0.2308 bump

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.230.600-2
- Perl 5.28 rebuild

* Mon Jun 25 2018 Petr Pisar <ppisar@redhat.com> - 0.230.600-1
- 0.2306 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.230.400-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 15 2017 Petr Pisar <ppisar@redhat.com> - 0.230.400-395
- Remove duplicate dependencies

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.230.400-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.230.400-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.230.400-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Petr Pisar <ppisar@redhat.com> - 0.230.400-1
- Normalize package version to dotted decimal format

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.23.04-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.04-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.04-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.23.04-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.23.04-311
- Perl 5.22 rebuild

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.23.04-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.23.04-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 14 2013 Petr Pisar <ppisar@redhat.com> - 0.23.04-1
- 0.2304 bump

* Thu Oct 10 2013 Petr Pisar <ppisar@redhat.com> - 0.23.03-1
- 0.2303 bump

* Tue Oct 01 2013 Petr Pisar <ppisar@redhat.com> - 0.23.02-1
- 0.2302 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 29 2013 Petr Pisar <ppisar@redhat.com> - 0.23.01-3
- Specify all dependencies

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 0.23.01-2
- Link minimal build-root packages against libperl.so explicitly

* Mon Apr 15 2013 Petr Pisar <ppisar@redhat.com> - 0.23.01-1
- 0.2301 bump

* Fri Mar 22 2013 Petr Pisar <ppisar@redhat.com> 0.23-1
- Specfile autogenerated by cpanspec 1.78.
