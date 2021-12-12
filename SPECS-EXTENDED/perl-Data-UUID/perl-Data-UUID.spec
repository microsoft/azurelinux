Name:		perl-Data-UUID
Version:	1.224
Release:	5%{?dist}
Summary:	Globally/Universally Unique Identifiers (GUIDs/UUIDs)
# Upstream says BSD but LICENSE file looks more like MIT
# https://lists.fedoraproject.org/pipermail/legal/2013-August/002226.html
License:	BSD and MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Data-UUID
Source0:	https://cpan.metacpan.org/modules/by-module/Data/Data-UUID-%{version}.tar.gz#/perl-Data-UUID-%{version}.tar.gz
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Config)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(Pod::Usage)
BuildRequires:	perl(warnings)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
# Test Suite
BuildRequires:	perl(Test::More)
BuildRequires:	perl(threads)
%if ! 0%{?_module_build}
# Optional Tests
BuildRequires:	perl(Test::Pod) >= 1.14
BuildRequires:	perl(Test::Pod::Coverage) >= 1.06
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Avoid provides for private shared objects
%{?perl_default_filter}

%description
This module provides a framework for generating v3 UUIDs (Universally Unique
Identifiers, also known as GUIDs (Globally Unique Identifiers). A UUID is 128
bits long, and is guaranteed to be different from all other UUIDs/GUIDs
generated until 3400 CE.

UUIDs were originally used in the Network Computing System (NCS) and later in
the Open Software Foundation's (OSF) Distributed Computing Environment.
Currently many different technologies rely on UUIDs to provide unique identity
for various software components. Microsoft COM/DCOM for instance, uses GUIDs
very extensively to uniquely identify classes, applications and components
across network-connected systems.

The algorithm for UUID generation, used by this extension, is described in the
Internet Draft "UUIDs and GUIDs" by Paul J. Leach and Rich Salz (see RFC 4122).
It provides a reasonably efficient and reliable framework for generating UUIDs
and supports fairly high allocation rates - 10 million per second per machine -
and therefore is suitable for identifying both extremely short-lived and very
persistent objects on a given system as well as across the network.

This module provides several methods to create a UUID. In all methods,
<namespace> is a UUID and <name> is a free form string.

%prep
%setup -q -n Data-UUID-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test AUTHOR_TESTING=1
perl smp-test/collision.t

%files
%license LICENSE
%doc Changes README
%{perl_vendorarch}/auto/Data/
%{perl_vendorarch}/Data/
%{_mandir}/man3/Data::UUID.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.224-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.224-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.224-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.224-2
- Perl 5.30 rebuild

* Sun Mar  3 2019 Paul Howarth <paul@city-fan.org> - 1.224-1
- Update to 1.224
  - Properly quote C strings passed in DEFINE
  - Fix memory leak by decreasing reference count
  - Use File::Spec to get tmpdir instead of hardcoding

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.221-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.221-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.221-11
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.221-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.221-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.221-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.221-7
- Perl 5.26 rebuild

* Fri Apr 21 2017 Petr Hracek <phracek@redhat.com> - 1.221-6
- Don't include perl(Test::Pod) during modular build

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.221-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.221-4
- Perl 5.24 rebuild

* Thu Apr 21 2016 Paul Howarth <paul@city-fan.org> - 1.221-3
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.221-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 11 2015 Paul Howarth <paul@city-fan.org> - 1.221-1
- Update to 1.221
  - Documentation improvements

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.220-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.220-2
- Perl 5.22 rebuild

* Thu Dec 18 2014 Paul Howarth <paul@city-fan.org> - 1.220-1
- Update to 1.220
  - Improve chances it'll work on Android
- Classify buildreqs by usage
- Use %%license

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.219-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.219-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.219-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 23 2013 Paul Howarth <paul@city-fan.org> - 1.219-3
- Change license to "BSD and MIT"
  https://lists.fedoraproject.org/pipermail/legal/2013-August/002226.html
- Drop EL-5 compatibility (#998143)

* Sat Aug 17 2013 Paul Howarth <paul@city-fan.org> - 1.219-2
- Sanitize for Fedora submission

* Thu Aug 15 2013 Paul Howarth <paul@city-fan.org> - 1.219-1
- Initial RPM version
