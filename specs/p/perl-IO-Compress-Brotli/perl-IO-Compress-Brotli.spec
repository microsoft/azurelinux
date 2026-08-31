# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global cpan_version 0.019
Name:           perl-IO-Compress-Brotli
Version:        %{cpan_version}000
Release:        4%{?dist}
Summary:        Perl bindings for Brotli compression
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/IO-Compress-Brotli/
Source0:        https://cpan.metacpan.org/authors/id/M/MG/MGV/IO-Compress-Brotli-%{cpan_version}.tar.gz
Patch0:         IO-Compress-Brotli-0.019-Use-pkgconfig-instead-of-bundled-libbrotli.patch

# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libbrotlienc)
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(ExtUtils::PkgConfig)
# Run-time
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Slurper)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Tests
BuildRequires:  perl(Test::More)
# Used in the installed script `bro-perl` - added by perl-generators
# BuildRequires:  perl(Getopt::Long)
# BuildRequires:  perl(Time::HiRes)

%description
IO::Compress::Brotli is a module that compresses Brotli buffers and
streams. Despite its name, it is not a subclass of IO::Compress::Base
and does not implement its interface. This will be rectified in a
future release.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl(Test::Harness)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n IO-Compress-Brotli-%{cpan_version}
%patch -P0 -p1

# Remove bundled source
for F in `find brotli -type f | grep -v testdata`; do 
    rm -rf $F
    perl -i -ne 'print $_ unless m{^\Q'"$F"'\E}' MANIFEST
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_libexecdir}/%{name}/brotli/tests
cp -a brotli/tests/testdata %{buildroot}%{_libexecdir}/%{name}/brotli/tests/
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
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/IO*
%{_mandir}/man3/*
%{_bindir}/bro-perl

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.019000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.019000-3
- Perl 5.42 rebuild

* Mon May 12 2025 Michal Josef Špaček <mspacek@redhat.com> - 0.019000-2
- Fix version of rpm package

* Fri May 09 2025 Michal Josef Špaček <mspacek@redhat.com> - 0.019-1
- 0.019 bump

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.004001-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.004001-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.004001-13
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.004001-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.004001-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.004001-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.004001-9
- Perl 5.38 rebuild

* Tue Feb 14 2023 Petr Salaba <psalaba@redhat.com> - 0.004001-8
- Add tests subpackage

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.004001-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 16 2022 Petr Salaba <psalaba@redhat.com> - 0.004001-6
- Update package summary

* Thu Aug 04 2022 Petr Salaba <psalaba@redhat.com> - 0.004001-5
- Update license in spec

* Wed Aug 03 2022 Petr Salaba <psalaba@redhat.com> - 0.004001-4
- Update summary, fix up spec file

* Tue Aug 02 2022 Petr Salaba <psalaba@redhat.com> - 0.004001-3
- Add exception for no-manual-page-for-binary

* Mon Aug 01 2022 Petr Salaba <psalaba@redhat.com> - 0.004001-2
- Cleaned up spec, switched to ExtUtils::PkgConfig

* Wed Jul 27 2022 Petr Salaba <psalaba@redhat.com> 0.004001-1
- Specfile autogenerated by cpanspec 1.78.
- Patched to use system libbrotli instead of bundled lib
