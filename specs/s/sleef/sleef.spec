## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond dft 1
%bcond quad 1
# Fedora packages should not ship static libraries unless absolutely required.
# Some software may really rely on the inline headers and accompanying static
# support library for exceptional performance requirements, but we will leave
# this feature disabled until someone asks for it.
%bcond static 0

# Adds a BuildRequires on tlfloat and enables more tests
%bcond tlfloat 1

Name:           sleef
Version:        3.9.0
%global tag %{version}
%global so_version 3
Release:        %autorelease
Summary:        Vectorized math library

# The entire source is BSL-1.0, except the following gencoef tool sources,
# which are CC-BY-4.0:
#   src/gencoef/dp.h
#   src/gencoef/gencoef.c
#   src/gencoef/ld.h
#   src/gencoef/qp.h
#   src/gencoef/simplexfr.c
#   src/gencoef/sp.h
# Since CC-BY-4.0 is allowed for content but not for code, these are removed
# before uploading the source to the lookaside cache.
License:        BSL-1.0
URL:            https://sleef.org
# This is a filtered version of:
#   https://github.com/shibatch/sleef/archive/%%{tag}/sleef-%%{tag}.tar.gz
# See the comment above License for why this is necessary. The archive is
# produced by using the script in Source1:
#   ./get_source.sh ${VERSION}
Source0:        sleef-%{tag}-filtered.tar.zst
Source1:        get_source.sh

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

# On aarch64, since 3.9.0, we cannot link at least bin/tester3svenofma when LTO
# is enabled, due to confusion about SVE.
#
#   /builddir/build/BUILD/sleef-3.9.0-build/sleef-3.9.0/src/common/testerutil.c:
#   In function ‘memrand.constprop’:
#   /builddir/build/BUILD/sleef-3.9.0-build/sleef-3.9.0/src/common/testerutil.c:101:6:
#   error: this operation requires the SVE ISA extension
#     101 | void memrand(void *p, int size) {
#         |      ^
#   /builddir/build/BUILD/sleef-3.9.0-build/sleef-3.9.0/src/common/testerutil.c:101:6:
#   note: you can enable SVE using the command-line option ‘-march’, or by
#   using the ‘target’ attribute or pragma
#   /builddir/build/BUILD/sleef-3.9.0-build/sleef-3.9.0/src/common/testerutil.c:101:
#   confused by earlier errors, bailing out
#
# This might be an upstream bug, but it is hard to understand. Upstream
# provides their own LTO option, SLEEF_ENABLE_LTO, but for does not support it
# in combination with shared libraries.
#
# - We could still build the library with LTO and not test it
#   (-DSLEEF_BUILD_TESTS:BOOL=FALSE) on aarch64.
# - It’s not clear how we could disable LTO *only for the tests*.
# - We choose to disable LTO entirely on aarch64, because we really want to run
#   the tests. We hope that the performance impact is not significant. It
#   currently does not seem necessary to disable LTO on other architectures.
%ifarch %{arm64}
%global _lto_cflags %{nil}
%endif

BuildRequires:  cmake >= 3.4.3
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
# For tests only:
BuildRequires:  pkgconfig(mpfr)
BuildRequires:  pkgconfig(gmp)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(libcrypto)
%if %{with dft}
BuildRequires:  pkgconfig(fftw3)
%endif
%if %{with tlfloat}
BuildRequires:  pkgconfig(tlfloat)
%endif

# See https://sleef.org/additional.xhtml#gnuabi. The gnuabi version of the
# library only applies to these architectures.
%global gnuabi_arches %{ix86} %{x86_64} %{arm64}
# See https://github.com/shibatch/sleef/pull/283.
%if %{with static}
%global inline_enabled 1
%endif

%description
SLEEF stands for SIMD Library for Evaluating Elementary Functions. It
implements vectorized versions of all C99 real floating point math functions.
It can utilize SIMD instructions that are available on modern processors. SLEEF
is designed to efficiently perform computation with SIMD instructions by
reducing the use of conditional branches and scatter/gather memory access.

The library contains implementations of all C99 real FP math functions in
double precision and single precision. Different accuracy of the results can be
chosen for a subset of the elementary functions; for this subset there are
versions with up to 1 ULP error (which is the maximum error, not the average)
and even faster versions with a few ULPs of error. For non-finite inputs and
outputs, the functions return correct results as specified in the C99 standard.


%package devel
Summary:        Development files for sleef
Requires:       sleef%{?_isa} = %{version}-%{release}

%description devel
The sleef-devel package contains libraries and header files for
developing applications that use sleef.


%if 0%{?inline_enabled}
%package static
Summary:        Inline headers and static library for sleef
Requires:       sleef-devel%{?_isa} = %{version}-%{release}

%description static
The sleef-static package contains libraries and header files for
developing applications that use sleef.
%endif


%package doc
Summary:        Documentation for sleef
BuildArch:      noarch

%description doc
The sleef-doc package contains detailed API documentation for developing
applications that use sleef.


%ifarch %{gnuabi_arches}
%package gnuabi
Summary:        GNUABI version of sleef

%global gnuabi_enabled 1

%description gnuabi
The GNUABI version of the library (libsleefgnuabi.so) is built for x86 and
aarch64 architectures. This library provides an API compatible with libmvec in
glibc, and the API conforms to the x86 vector ABI, AArch64 vector ABI and Power
Vector ABI.


%package gnuabi-devel
Summary:        Development files for GNUABI version of sleef
Requires:       sleef-gnuabi%{?_isa} = %{version}-%{release}

%description gnuabi-devel
The sleef-gnuabi-devel package contains libraries for developing applications
that use the GNUABI version of sleef. Note that this package does not contain
any header files.
%endif


%if %{with dft}
%package dft
Summary:        Discrete Fourier Transform (DFT) library
Requires:       sleef%{?_isa} = %{version}-%{release}

%description dft
SLEEF includes subroutines for discrete Fourier transform(DFT). These
subroutines are fully vectorized, heavily unrolled, and parallelized in such a
way that modern SIMD instructions and multiple cores can be utilized for
efficient computation. It has an API similar to that of FFTW for easy
migration. The subroutines can utilize long vectors up to 2048 bits.


%package dft-devel
Summary:        Development files for sleef-dft
Requires:       sleef-dft%{?_isa} = %{version}-%{release}

%description dft-devel
The sleef-dft-devel package contains libraries and header files for
developing applications that use sleef-dft.
%endif


%if %{with quad}
%package quad
Summary:        Vectorized quad-precision math library

%description quad
An experimental quad-precision library


%package quad-devel
Summary:        Development files for sleef-quad
Requires:       sleef-quad%{?_isa} = %{version}-%{release}

%description quad-devel
The sleef-quad-devel package contains libraries and header files for
developing applications that use sleef-quad.
%endif


%prep
%autosetup -n sleef-%{tag} -p1
# Remove an unwanted hidden file from the docs
find docs/ -type f -name .nojekyll -print -delete


%conf
# -GNinja: This used to be required for parallel builds; it is still faster.
#
# -DENFORCE_TESTER3: The build should fail if we cannot build all tests.
# -DENFORCE_TESTER4: Likewise, except that tester4 requires tlfloat.
#
# -DBUILD_INLINE_HEADERS: Do not build the “inline” headers. This would provide
#   an arch-specific collection of sleefinline_*.h headers in _includedir, as
#   well as a static support library, libsleefinline.a, in _libdir. Both the
#   static library and the headers (which are basically a header-only library,
#   and would thus also be treated as a static library in the Fedora
#   guidelines) should be omitted unless something in Fedora absolutely
#   requires them.
#
# -DSLEEFDFT_ENABLE_STREAM: The author writes, “The recommended value for
#   SLEEFDFT_ENABLE_STREAM depends on the architecture, and it is only
#   recommended to be turned on on x86_64.”
#   https://github.com/shibatch/sleef/discussions/654#discussioncomment-12860550
%cmake \
    -GNinja \
    -DSLEEF_BUILD_DFT:BOOL=%{?with_dft:TRUE}%{?!with_dft:FALSE} \
    -DSLEEF_ENFORCE_DFT:BOOL=%{?with_dft:TRUE}%{?!with_dft:FALSE} \
%ifarch %{x86_64}
    -DSLEEFDFT_ENABLE_STREAM:BOOL=TRUE \
%else
    -DSLEEFDFT_ENABLE_STREAM:BOOL=FALSE \
%endif
    -DSLEEF_BUILD_GNUABI_LIBS:BOOL=%{?gnuabi_enabled:TRUE}%{?!gnuabi_enabled:FALSE} \
    -DSLEEF_BUILD_INLINE_HEADERS:BOOL=%{?inline_enabled:TRUE}%{?!inline_enabled:FALSE} \
    -DSLEEF_BUILD_QUAD:BOOL=%{?with_quad:TRUE}%{?!with_quad:FALSE} \
    -DSLEEF_BUILD_SHARED_LIBS:BOOL=TRUE \
    -DSLEEF_ENFORCE_TESTER3:BOOL=TRUE \
    -DSLEEF_ENFORCE_TESTER4:BOOL=%{?with_tlfloat:TRUE}%{?!with_tlfloat:FALSE} \
    -DSLEEF_ENABLE_TLFLOAT:BOOL=%{?with_tlfloat:TRUE}%{?!with_tlfloat:FALSE}


%build
%cmake_build


%install
%cmake_install


%check
# Logging CPU features is helpful for debugging, especially in COPR builds
# where the builder hardware information is not necessarily logged separately.
echo '==== Build host CPU features ===='
cat /proc/cpuinfo

skips='^($.'

%ifarch %{arm64}
# Some tests are specifically for SVE code. We can only run these tests on
# builder hardware that has the SVE extensions, which are not part of the
# aarch64 baseline.
if ! grep -E '[Ff](lags|eatures).*\bsve\b' /proc/cpuinfo >/dev/null
then
  skips="${skips}|gnuabi_compatibility_SVE(_masked)?|qiutsve"
fi
%endif
%ifarch %{power64}
# Some tests are specifically for VSX3 code. We can only run these tests on
# builder hardware that has the VSX3 extensions (POWER 9 or later), which are
# not part of the ppc64le baseline (POWER 8).
if grep -E -i '\bPOWER8\b' /proc/cpuinfo >/dev/null
then
  skips="${skips}|.*vsx3(nofma)?"
fi
%endif

skips="${skips})$"

%ctest --exclude-regex "${skips}" --extra-verbose


%files
%license LICENSE.txt
%{_libdir}/libsleef.so.%{so_version}{,.*}


%files devel
%{_includedir}/sleef.h
%{_libdir}/libsleef.so
%{_libdir}/pkgconfig/sleef.pc
%{_libdir}/cmake/sleef/


%if 0%{?inline_enabled}
%files static
%{_includedir}/sleefinline_*.h
%{_libdir}/libsleefinline.a
%endif


%files doc
%license LICENSE.txt
%doc CHANGELOG.md
%doc README.adoc
%doc docs/


%ifarch %{gnuabi_arches}
%files gnuabi
%license LICENSE.txt
%{_libdir}/libsleefgnuabi.so.%{so_version}{,.*}


%files gnuabi-devel
%{_libdir}/libsleefgnuabi.so
%endif


%if %{with dft}
%files dft
%{_libdir}/libsleefdft.so.%{so_version}{,.*}


%files dft-devel
%{_includedir}/sleefdft.h
%{_libdir}/libsleefdft.so
%endif


%if %{with quad}
%files quad
%license LICENSE.txt
%{_libdir}/libsleefquad.so.%{so_version}{,.*}


%files quad-devel
%{_includedir}/sleefquad.h
%{_libdir}/libsleefquad.so
%endif


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 3.9.0-5
- test: add initial lock files

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun May 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.9.0-3
- Remove an unwanted hidden file from the docs

* Sun May 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.9.0-2
- Update .rpmlintrc file for current rpmlint

* Sat Apr 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.9.0-1
- Update to 3.9.0 (close RHBZ#2355181)

* Wed Mar 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.8.0-2
- Use %%{x86_64}/%%{arm64} instead of x86_64/aarch64, for generality

* Tue Jan 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.8.0-1
- Update to 3.8.0 (close RHBZ#2342573)

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.7.0-5
- Work around removal of some PowerPC intrinsics in GCC 15

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.7.0-2
- Invoke %%cmake in %%conf rather than in %%build

* Tue Sep 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.7.0-1
- Update to 3.7.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.6.1-1
- Update to 3.6.1 (close RHBZ#2264430)
- Build and package the quad-precision and DFT libraries

* Fri Apr 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-36
- Use zstd instead of xz for filtered source archive compression

* Fri Apr 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-35
- Improve reproducibility of the filtered source archive

* Mon Mar 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-33
- Stop skipping tests; optimization bug fixed in GCC

* Mon Mar 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-32
- Revert "Work around a GCC optimization bug"

* Mon Mar 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-31
- Work around a GCC optimization bug

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-29
- Fix compiling tests with MPFR 4.2.0 and later

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-27
- Use new (rpm 4.17.1+) bcond style

* Mon Jan 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-26
- Filter gencoef CC-BY-4.0 sources before uploading

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-24
- Drop conditionals for retired 32-bit ARM

* Thu Dec 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-23
- Leaf package: remove i686 support

* Thu Dec 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-22
- Trivially simplify a files list

* Thu Dec 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-21
- Indicate dirs. in files list with trailing slashes

* Tue Nov 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-20
- Also skip iutzvector2 and iutzvector2nofma on s390x

* Tue Nov 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-19
- Update License to SPDX
- Remove CC-BY-4.0-licensed gencoef tool sources in %%%%prep

* Tue Nov 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-18
- Slightly nicer %%%%files listings

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-15
- Restore ppc64le support (fix RHBZ#2040887)

* Fri Jan 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-14
- Link upstream issue for skipped tests on GCC 12

* Fri Jan 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-13
- Add enough workarounds to build with GCC 12

* Fri Jan 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-12
- Stop logging builder CPU features

* Fri Jan 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-11
- Stop skipping some tests on s390x

* Tue Sep 28 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-10
- Use stricter file globs

* Tue Sep 28 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-9
- Reduce macro indirection in the spec file

* Tue Sep 28 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-8
- Use pkgconfig(…) style dependencies where applicable

* Tue Sep 28 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-7
- Do not compute the so-version automatically

* Tue Sep 28 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-6
- Drop EPEL workarounds from Fedora spec

* Mon May 17 2021 Dave Love <loveshack@fedoraproject.org> - 3.5.1-4
- Support epel7

* Wed Mar 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-3
- Improve source URL

* Thu Dec 24 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-2
- Drop explicit pkgconfig dependency; providing a .pc file implies it

* Fri Dec 18 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 3.5.1-1
- Initial spec file

## END: Generated by rpmautospec
