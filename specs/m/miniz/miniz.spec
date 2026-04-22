# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       miniz
Version:    3.1.0
Release: 2%{?dist}
Summary:    Compression library implementing the zlib and Deflate
# examples/example1.c:  Unlicense (refers to "unlicense" statement at the end
#                       of tinfl.c from miniz-1.15)
# examples/example2.c:  Unlicense
# examples/example3.c:  Unlicense
# examples/example4.c:  Unlicense
# examples/example5.c:  Unlicense ("Public domain. See unlicense statement")
# examples/example6.c:  Unlicense
# LICENSE:  MIT text
# miniz.c:  MIT
# miniz.h:  Unlicense (See "unlicense" statement at the end of this file.)
# readme.md:    MIT
License:    MIT AND Unlicense
URL:        https://github.com/richgel999/%{name}
Source0:    %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# Adjust examples for building against a system miniz library,
# not suitable for upstream that prefers a copy-lib approach.
Patch0:     miniz-2.2.0-Examples-to-include-system-miniz.h.patch
BuildRequires:  cmake
BuildRequires:  coreutils
# diffutils for cmp
BuildRequires:  diffutils
%if "%{toolchain}" == "gcc"
BuildRequires:  gcc
BuildRequires:  gcc-g++
%else
%if "%{toolchain}" == "clang"
BuildRequires:  clang
%else
%{error:Unknown toolchain.}
%endif
%endif
BuildRequires:  dos2unix

%description
Miniz is a lossless, high performance data compression library in a single
source file that implements the zlib (RFC 1950) and Deflate (RFC 1951)
compressed data format specification standards. It supports the most commonly
used functions exported by the zlib library, but is a completely independent
implementation so zlib's licensing requirements do not apply. It also
contains simple to use functions for writing PNG format image files and
reading/writing/appending ZIP format archives. Miniz's compression speed has
been tuned to be comparable to zlib's, and it also has a specialized real-time
compressor function designed to compare well against fastlz/minilzo.

%package devel
Summary:    Development files for the %{name} library
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   cmake-filesystem
Requires:   pkg-config%{?_isa}

%description devel
Header files for developing applications that use the %{name} library.


%prep
%setup -q -n %{name}-%{version}
%patch -P0 -p1

# Normalize end-of-lines
dos2unix -k ChangeLog.md LICENSE

%build
%cmake
%cmake_build

%install
%cmake_install

%check
pushd bin
for EXAMPLE in *; do
    case "$EXAMPLE" in
        example3)
            LD_LIBRARY_PATH=../%{__cmake_builddir} "./${EXAMPLE}" c ../readme.md readme.md.z
            LD_LIBRARY_PATH=../%{__cmake_builddir} "./${EXAMPLE}" d readme.md.z readme.md
            cmp ../readme.md readme.md
            ;;
        example4)
            LD_LIBRARY_PATH=../%{__cmake_builddir} "./${EXAMPLE}" readme.md.z readme.md
            cmp ../readme.md readme.md
            ;;
        example5)
            LD_LIBRARY_PATH=../%{__cmake_builddir} "./${EXAMPLE}" c ../readme.md readme.md.z
            LD_LIBRARY_PATH=../%{__cmake_builddir} "./${EXAMPLE}" d readme.md.z readme.md
            cmp ../readme.md readme.md
            ;;
        *)
            LD_LIBRARY_PATH=../%{__cmake_builddir} "./${EXAMPLE}"
            ;;
    esac
done

%files
%license LICENSE
%doc ChangeLog.md readme.md
%{_libdir}/lib%{name}.so.{3,%{version}}

%files devel
%doc examples/*.c
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Mon Sep 22 2025 Paul Howarth <paul@city-fan.org> - 3.1.0-1
- Update to 3.1.0 (rhbz#2397198)
- C++ compiler needed for tests

* Tue Jul 29 2025 Dominik Mierzejewski <dominik@greysector.net> - 3.0.2-9
- switch to tar.gz source to avoid manual build
- build using CMake (use upstream SONAME)
- ship pkg-config and CMake files (resolves rhbz#2378931)
- fix build with CMake 4.0
- use dos2unix instead of sed

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Petr Pisar <ppisar@redhat.com> - 3.0.2-1
- 3.0.2 bump

* Mon Nov 07 2022 Petr Pisar <ppisar@redhat.com> - 3.0.1-1
- 3.0.1 bump

* Tue Nov 01 2022 Petr Pisar <ppisar@redhat.com> - 3.0.0-1
- 3.0.0 bump (an API and ABI change)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jan 24 2022 Petr Pisar <ppisar@redhat.com> - 2.2.0-4
- Fix an unitialized memory in tinfl_decompress_mem_to_callback() (GH#197)
- Fix an unaligned memory access
- Fix setting MZ_ZIP_GENERAL_PURPOSE_BIT_FLAG_UTF8
- Fix an undefined behaviour in tinfl_decompress() (GH#216)
- Fix mz_zip_reader_extract_to_heap() to read correct sizes (GH#220)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 01 2021 Petr Pisar <ppisar@redhat.com> - 2.2.0-2
- Use standard toolchain macros (FPC#1066)

* Wed Aug 11 2021 Petr Pisar <ppisar@redhat.com> - 2.2.0-1
- 2.2.0 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Tom Stellard <tstellar@redhat.com> - 2.1.0-6
- Use toolchain macro instead of hard-coding gcc

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 23 2019 Petr Pisar <ppisar@redhat.com> - 2.1.0-2
- Remove a dependency on gcc from miniz-devel
- Normalize end-of-lines in a change log

* Wed May 22 2019 Petr Pisar <ppisar@redhat.com> - 2.1.0-1
- 2.1.0 bump
- Upstream moved to <https://github.com/richgel999/miniz>
- License changed from "Unlicense" to "MIT and Unlicense"
- ABI changed, API preserved

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-12.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Petr Pisar <ppisar@redhat.com> - 1.15-11.r4
- Fix link order

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-10.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 23 2018 Petr Pisar <ppisar@redhat.com> - 1.15-9.r4
- Modernize a spec file

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-8.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-7.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-6.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-5.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 08 2016 Petr Pisar <ppisar@redhat.com> - 1.15-4.r4
- Correct dependency on libc headers

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-3.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 14 2014 Petr Pisar <ppisar@redhat.com> - 1.15-1.r4
- 1.15r4 version packaged


