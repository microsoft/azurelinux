Name: ck
Version: 0.7.2
Release: 1%{?dist}
Summary: Library for high performance concurrent programming

License: BSD-2-clause AND Apache-2.0 AND BSD-3-clause
# concurrencykit.org has been done for many months now, so use github instead
URL: https://github.com/concurrencykit/ck
Source: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# disable ck_hclh_test from ck_spinlock temporary solution
# github issue: https://github.com/concurrencykit/ck/issues/153
Patch3: ck_disable_ck_hclh_test.patch
# measure unit test times
Patch4: ck-unit-time.patch
# specify SEQUENCE_CORES different for one test
Patch5: ck-unit-sequence.patch

BuildRequires: gcc
BuildRequires: make
BuildRequires: sed

%description
Concurrency Kit provides a plethora of concurrency primitives, safe memory
reclamation mechanisms and lock-less and lock-free data structures designed to
aid in the design and implementation of high performance concurrent systems. It
is designed to minimize dependencies on operating system-specific interfaces
and most of the interface relies only on a strict subset of the standard
library and more popular compiler extensions.

%package devel
Summary: Header files and libraries for CK development
Requires: %{name} = %{version}-%{release}

%description devel
Concurrency Kit provides a plethora of concurrency primitives, safe memory
reclamation mechanisms and lock-less and lock-free data structures designed to
aid in the design and implementation of high performance concurrent systems. It
is designed to minimize dependencies on operating system-specific interfaces
and most of the interface relies only on a strict subset of the standard
library and more popular compiler extensions.

This package provides the libraries, include files, and other
resources needed for developing Concurrency Kit applications.

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags}"
./configure 		\
	--libdir=%{_libdir} 			\
	--includedir=%{_includedir}/%{name}	\
	--mandir=%{_mandir}			\
	--prefix=%{_prefix}

%make_build

%install
%make_install

# fix weird mode of the shared library
chmod 0755 %{buildroot}%{_libdir}/libck.so.*

# remove static library
rm %{buildroot}%{_libdir}/libck.a

%check
MAX_CORES=4
# 8+ CORES take quite long, limit them to 4
CORES=$(grep '^CORES=' build/regressions.build | cut -d= -f2)
# ck_sequence tests wants all cores on the system to be quick
SEQUENCE_CORES="$CORES"
TIMEOUT=$((30*60))
TIMEOUT_KILL=$((TIMEOUT+100))
[ "${CORES}" -gt "${MAX_CORES}" ] && CORES="${MAX_CORES}"
%ifarch %{power64}
    # It hangs often on this test for some reason
    sed -e '/^OBJECTS=/ s, barrier_mcs,,' -i regressions/ck_barrier/validate/Makefile
%endif
%ifarch %{arm32} %{arm64}
    # Some tests take quite long on ARMs. Skip them
    sed -e '/^\s*brlock\s/ d' -e '/^\s*cohort\s/ d' -e '/^\s*rwlock\s/ d' \
        -i regressions/Makefile
%endif
# Protect builders against hard lock
time timeout -k $TIMEOUT_KILL $TIMEOUT \
    make check CORES=${CORES} SEQUENCE_CORES=${SEQUENCE_CORES}

%files
%license LICENSE
%{_libdir}/libck.so.*

%files devel
%{_libdir}/libck.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/*.3.gz

%changelog
* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Petr Menšík <pemensik@redhat.com> - 0.7.1-2
- Use SPDX licenses

* Wed Jul 12 2023 Paul Wouters <paul.wouters@aiven.io - 0.7.1-1
- Updated to 0.7.1 (partially for testing resolving of rhbz#2113147)
- Remove upstreamed patches
- Updated URL: and Source: to github, as concurrencykit.org has been dead for a while

* Fri Feb 17 2023 Petr Menšík <pemensik@redhat.com> - 0.7.0-10
- Set time limit to unit test run
- Limit unit test to less cores to make them faster
- Skip some tests on ppc64le and aarch64 platforms to avoid failures

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 17 2020 Filip Januš <fjanus@redhat.com> - 0.7.0-3
- Build fails due to ck_hclh test
- github issue: https://github.com/concurrencykit/ck/issues/153
- resolves:https://bugzilla.redhat.com/show_bug.cgi?id=1799226
- add patch - disables ck_hclh test

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 22 2019 Honza Horak <hhorak@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Wed Aug 21 2019 Honza Horak <hhorak@redhat.com> - 0.6.0-11
- Add upstream patch ck_barrier_combining: switch to seq_cst semantics to make
  ppc64le

* Wed Aug 21 2019 Honza Horak <hhorak@redhat.com> - 0.6.0-10
- Remove static gettid definition

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Honza Horak <hhorak@redhat.com> - 0.6.0-7
- Explicitly include gcc

* Tue Jul 17 2018 Honza Horak <hhorak@redhat.com> - 0.6.0-6
- Fix building on s390x and ignore tests also for ppc64le and ix86 and x86_64

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 Xavier Bachelot <xavier@bachelot.org> - 0.6.0-1
- Update to 0.6.0.
- Run test suite.

* Sat Feb 11 2017 Honza Horak <hhorak@redhat.com> - 0.5.2-2
- Fix issues found during Package Review
  Summary provides better idea what this library is for
  Using macros for make build and install
  Fix permissions of the shared library

* Sat Feb 04 2017 Honza Horak <hhorak@redhat.com> - 0.5.2-1
- Initial packaging

