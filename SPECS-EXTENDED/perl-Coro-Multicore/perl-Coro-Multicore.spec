# Filter under-specified dependecies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((AnyEvent|Coro)\\)$

Summary:        Make Coro threads on multiple cores with specially supported modules
Name:           perl-Coro-Multicore
Version:        1.07
Release:        3%{?dist}
# COPYING:          GPL+ or Artistic
# perlmulticore.h:  Public Domain or CC0
License:        (GPL+ OR Artistic) AND (Public Domain OR CC0)
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Coro-Multicore
Source0:        https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/Coro-Multicore-%{version}.tar.gz
# Declare POD encoding, submitted to upstream,
# <https://lists.schmorp.de/pipermail/anyevent/2015q4/000780.html>
Patch0:         Coro-Multicore-0.02-Declare-POD-encoding.patch
# Fix build failure on Perl 5.26.1 with enabled treads, CPAN RT#124131,
# 1.05 provided a fix, but forgot to return a value from thread_proc().
# Keep the patch until upstream resolves it.
Patch1:         Coro-Multicore-1.04-Fix-passing-context.patch

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl-podlators
# Run-time:
BuildRequires:  perl(AnyEvent) >= 7
BuildRequires:  perl(Canary::Stability)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Coro) >= 6.44
BuildRequires:  perl(Coro::MakeMaker)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(XSLoader)

%if 0%{?with_check}
BuildRequires:  perl(Coro::AnyEvent)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(AnyEvent) >= 7
Requires:       perl(Carp)
Requires:       perl(Coro) >= 6.44

%description
While Coro threads (unlike ithreads) provide real threads similar to
pthreads, python threads and so on, they do not run in parallel to each
other even on machines with multiple CPUs or multiple CPU cores.

This module lifts this restriction under two very specific but useful
conditions: firstly, the coro thread executes in XS code and does not
touch any perl data structures, and secondly, the XS code is specially
prepared to allow this.

# We package perlmulticore.h because it is bundled by perl-Compress-LZF-3.8.
# We deliver it from Coro-Multicore because perlmulticore.h's documentation
# points to Coro-Multicore CVS tree.
%package -n perlmulticore-devel
Summary:        Perl Multicore specification and implementation
License:        Public Domain OR CC0
# Packaging guidelines require header-only packages:
# to be architecture-specific, to deliver headers in -devel package, to
# provide -static symbol for reverse build-requires.
Provides:       perlmulticore-static = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n perlmulticore-devel
This header file implements a simple mechanism for XS modules to allow
re-use of the perl interpreter for other threads while doing some lengthy
operation, such as cryptography, SQL queries, disk I/O and so on.

%package tests
Summary:        Tests for %{name}
License:        (GPL+ OR Artistic) AND (Public Domain OR CC0)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Coro) >= 6.44
BuildArch:      noarch

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Coro-Multicore-%{version}
%patch 0 -p1
%patch 1 -p1

%build
export CORO_MULTICORE_CHECK=0 PERL_CANARY_STABILITY_NOPROMPT=1
perl Makefile.PL INSTALLDIRS=vendor \
    NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}" </dev/null
%make_build

# perlmulticore-devel:
pod2man perlmulticore.h >perlmulticore.h.3

%install
%make_install
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

# perlmulticore-devel:
install -d %{buildroot}/%{_includedir}
install -m 0644 perlmulticore.h %{buildroot}/%{_includedir}
install -d %{buildroot}/%{_mandir}/man3
install -m 0644 perlmulticore.h.3 %{buildroot}/%{_mandir}/man3

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
%{perl_vendorarch}/Coro*
%{_mandir}/man3/Coro::Multicore.3*

%files -n perlmulticore-devel
# COPYING file is about Perl module. Header files have a different license.
%license %{_includedir}/perlmulticore.h
%{_includedir}/perlmulticore.h
%{_mandir}/man3/perlmulticore.h.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Jan 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.07-3
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Wed Aug 04 2021 Petr Pisar <ppisar@redhat.com> - 1.07-2
- Do not package Coro::Multicore tests in case coro feature is disabled

* Tue Aug 03 2021 Petr Pisar <ppisar@redhat.com> - 1.07-1
- 1.07 bump
- Package the tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-3
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-1
- 1.06 bump

* Tue Dec 10 2019 Petr Pisar <ppisar@redhat.com> - 1.05-1
- 1.05 bump

* Tue Dec 03 2019 Petr Pisar <ppisar@redhat.com> - 1.04-1
- 1.04 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-2
- Perl 5.30 rebuild

* Thu Mar 07 2019 Petr Pisar <ppisar@redhat.com> - 1.03-1
- 1.03 bump

* Wed Mar 06 2019 Petr Pisar <ppisar@redhat.com> - 1.02-1
- 1.02 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 15 2018 Petr Pisar <ppisar@redhat.com> - 1.01-1
- 1.01 bump

* Mon Aug 13 2018 Petr Pisar <ppisar@redhat.com> - 1.0-1
- 1.0 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.03-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Petr Pisar <ppisar@redhat.com> - 0.03-1
- 0.03 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.02-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 24 2016 Petr Pisar <ppisar@redhat.com> - 0.02-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Petr Pisar <ppisar@redhat.com> 0.02-1
- Specfile autogenerated by cpanspec 1.78.
