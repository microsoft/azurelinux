Summary:        Concise Binary Object Representation (CBOR)
Name:           perl-CBOR-XS
Version:        1.86
Release:        2%{?dist}
# COPYING:      GPLv3+
## Replaced by system header-only package
# ecb.h:        BSD or GPLv2+
License:        GPLv3+ AND (BSD OR GPLv2+)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/CBOR-XS
Source0:        https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/CBOR-XS-%{version}.tar.gz
# Use system libecb
Patch0:         CBOR-XS-1.6-Include-ecb.h-from-system.patch
# Silent compiler warnings
Patch1:         CBOR-XS-1.84-Cast-char-and-U8-where-needed.patch

BuildRequires:  coreutils
BuildRequires:  findutils
# gcc for standard header files
BuildRequires:  gcc
BuildRequires:  libecb-static
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Canary::Stability)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Math::BigFloat)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  perl(Time::Piece)
BuildRequires:  perl(Types::Serialiser)
BuildRequires:  perl(URI)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(common::sense)

%if %{with_check}
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Math::BigInt::FastCalc)
%endif

# Run-time:
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Math::BigFloat)
Requires:       perl(Math::BigInt)
Requires:       perl(Math::BigRat)
Requires:       perl(Time::Piece)
Requires:       perl(URI)

%description
This module converts Perl data structures to the Concise Binary Object
Representation (CBOR) and vice versa. CBOR is a fast binary serialization
format that aims to use an (almost) superset of the JSON data model, i.e.
when you can represent something useful in JSON, you should be able to
represent it in CBOR.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Math::BigInt::FastCalc)
BuildArch:      noarch

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n CBOR-XS-%{version}
# Remove bundled libecb
rm ecb.h
perl -i -ne 'print $_ unless m{^ecb\.h}' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}" </dev/null
%make_build

%install
%make_install
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
%license COPYING
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/CBOR*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Jan 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.86-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Fri Nov 05 2021 Petr Pisar <ppisar@redhat.com> - 1.86-1
- 1.86 bump (bug #2020382)

* Mon Oct 25 2021 Petr Pisar <ppisar@redhat.com> - 1.85-1
- 1.85 bump

* Thu Oct 21 2021 Petr Pisar <ppisar@redhat.com> - 1.84-1
- 1.84 bump
- Package the tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.83-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.83-3
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 08 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.83-1
- 1.83 bump

* Tue Dec 01 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.82-1
- 1.82 bump

* Mon Nov 30 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.80-1
- 1.8 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.71-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.71-6
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.71-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.71-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.71-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Petr Pisar <ppisar@redhat.com> - 1.71-1
- 0.71 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.7-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Petr Pisar <ppisar@redhat.com> - 1.7-1
- 1.7 bump

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.6-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 08 2016 Petr Pisar <ppisar@redhat.com> - 1.6-1
- 1.6 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.5-2
- Perl 5.24 rebuild

* Wed Apr 27 2016 Petr Pisar <ppisar@redhat.com> - 1.5-1
- 1.5 bump

* Mon Feb 29 2016 Petr Pisar <ppisar@redhat.com> - 1.4.1-1
- 1.41 bump

* Tue Feb 09 2016 Petr Pisar <ppisar@redhat.com> - 1.4-1
- 1.4 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 29 2015 Petr Pisar <ppisar@redhat.com> 1.3-1
- Specfile autogenerated by cpanspec 1.78.
