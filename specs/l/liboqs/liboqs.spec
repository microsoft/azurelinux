# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global oqs_version 0.12.0
Name:       liboqs
Version:    %{oqs_version}
Release: 6%{?dist}
Summary:    liboqs is an open source C library for quantum-safe cryptographic algorithms.

#liboqs uses MIT license by itself but includes several files licensed under different terms.
#src/common/crypto/sha3/xkcp_low/.../KeccakP-1600-AVX2.s : BSD-like CRYPTOGAMS license
#src/common/rand/rand_nist.c: See file
#see https://github.com/open-quantum-safe/liboqs/blob/main/README.md#license for more details
License:    MIT AND Apache-2.0 AND BSD-3-Clause AND (BSD-3-Clause OR GPL-1.0-or-later) AND CC0-1.0 AND Unlicense
URL:        https://github.com/open-quantum-safe/liboqs.git
Source:     https://github.com/open-quantum-safe/liboqs/archive/refs/tags/liboqs-%{oqs_version}.tar.gz
Patch1:	    liboqs-0.12.0-acvp_patch.patch
Patch2:	    liboqs-0.10.0-std-stricter.patch
# https://github.com/open-quantum-safe/liboqs/pull/2043
Patch3:	    liboqs-0.12.0-openssl-memfuncs.patch

BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: openssl-devel
BuildRequires: python3-pytest
%if %{undefined rhel}
BuildRequires: python3-pytest-xdist
%endif
BuildRequires: unzip
BuildRequires: xsltproc
#BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: python3-yaml
%ifarch %{valgrind_arches}
BuildRequires: valgrind
%endif

%description
liboqs provides:
 - a collection of open source implementations of quantum-safe key encapsulation mechanism (KEM) and digital signature algorithms; the full list can be found below
 - a common API for these algorithms
 - a test harness and benchmarking routines
liboqs is part of the Open Quantum Safe (OQS) project led by Douglas Stebila and Michele Mosca, which aims to develop and integrate into applications quantum-safe cryptography to facilitate deployment and testing in real world contexts. In particular, OQS provides prototype integrations of liboqs into TLS and SSH, through OpenSSL and OpenSSH.

%package devel
Summary:          Development libraries for liboqs
Requires:         liboqs%{?_isa} = %{version}-%{release}

%description devel
Header and Library files for doing development with liboqs.

%prep
%setup -T -b 0 -q -n liboqs-%{oqs_version}
%autopatch -p1
#hobble
rm -rf src/kem/bike
rm -rf src/kem/bike/additional_r4
rm -rf src/kem/classic_mceliece
rm -rf src/kem/frodokem
rm -rf src/kem/hqc
rm -rf src/kem/ntruprime
# code_conventions is for upstream CI, requires astyle
# pytest-xdist is not available in RHEL due to dependencies
sed -e '/COMMAND.*pytest/s|$| --ignore tests/test_code_conventions.py|' \
%if %{defined rhel}
    -e 's/--numprocesses=auto//' \
%endif
    -i tests/CMakeLists.txt

%build
%cmake -GNinja -DBUILD_SHARED_LIBS=ON -DOQS_USE_AES_OPENSSL=ON -DOQS_USE_AES_INSTRUCTIONS=OFF -DOQS_DIST_BUILD=ON -DOQS_ALGS_ENABLED=NIST_2024 -DOQS_USE_SHA3_OPENSSL=ON -DOQS_DLOPEN_OPENSSL=ON -DCMAKE_BUILD_TYPE=Debug -LAH ..
%cmake_build
#ninja gen_docs

%check
cd "%{_vpath_builddir}"
ninja run_tests

%install
%cmake_install
for i in liboqsTargets.cmake liboqsTargets-debug.cmake
do
  cp $RPM_BUILD_ROOT/%{_libdir}/cmake/liboqs/$i /tmp/$i
  sed -e "s;$RPM_BUILD_ROOT;;g" /tmp/$i   > $RPM_BUILD_ROOT/%{_libdir}/cmake/liboqs/$i
  rm /tmp/$i
done

%files
%license LICENSE.txt
%{_libdir}/liboqs.so.%{oqs_version}
%{_libdir}/liboqs.so.7

%files devel
%{_libdir}/liboqs.so
%dir %{_includedir}/oqs
%{_includedir}/oqs/*
%dir %{_libdir}/cmake/liboqs
%{_libdir}/cmake/liboqs/liboqsTargets.cmake
%{_libdir}/cmake/liboqs/liboqsTargets-debug.cmake
%{_libdir}/cmake/liboqs/liboqsConfig.cmake
%{_libdir}/cmake/liboqs/liboqsConfigVersion.cmake
%{_libdir}/pkgconfig/liboqs.pc
#%dir %%{_datadir}/doc/oqs
#%doc %%{_datadir}/doc/oqs/html/*
#%doc %%{_datadir}/doc/oqs/xml/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 05 2025 David Abdurachmanov <davidlt@rivosinc.com> - 0.12.0-4
- Properly check valgrind arches

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Daiki Ueno <dueno@redhat.com> - 0.12.0-2
- Avoid unresolved symbols when compiled with OQS_DLOPEN_OPENSSL

* Fri Jan 03 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 0.12.0-1
- Rebasing to liboqs-0.12.0
  Removing support of Kyber from build. Falcon is also disabled until being
  standardized.

* Tue Oct 01 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 0.11.0-2
- rebuilt and cleanup

* Mon Sep 30 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 0.11.0-1
- Update to 0.11.0 version

* Fri Aug 02 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.10.1-3
- Add PQ container test

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 0.10.1-1
- Update to 0.10.1 version (CVE-2024-36405)

* Mon May 06 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 0.10.0-3
- Support IANA pre-standard Kyber groups for compatibility's sake

* Wed Apr 24 2024 Daiki Ueno <dueno@redhat.com> - 0.10.0-2
- Load OpenSSL libcrypto.so on demand through dlopen

* Wed Mar 27 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 0.10.0-1
- Update to 0.10.0 version

* Thu Feb 01 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 0.9.2-1
- Update to 0.9.2 version

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 30 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.9.0-2
- Skip code style tests

* Fri Oct 27 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 0.9.0-1
- Switch to 0.9.0 version
  Resolves: rhbz#2241615

* Wed Oct 04 2023 Stephen Gallagher <sgallagh@redhat.com> - 0.8.0-4
- Bump release to rebuild for ELN issue
- https://github.com/fedora-eln/eln/issues/125

* Wed Jul 26 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 0.8.0-3
- The exception we get covers avx2 implementation, no need to remove it

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Feb 13 2023 Dmitry Belyavskiy - 0.8.0-1
- Initial build of liboqs for Fedora

