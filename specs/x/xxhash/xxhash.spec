# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		xxhash
Version:	0.8.3
Release: 4%{?dist}
Summary:	Extremely fast hash algorithm

#		The source for the library (xxhash.c and xxhash.h) is BSD-2-Clause
#		The source for the command line tool (xxhsum.c) is GPL-2.0-or-later
License:	BSD-2-Clause AND GPL-2.0-or-later
URL:		https://www.xxhash.com/
Source0:	https://github.com/Cyan4973/xxHash/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	doxygen

%description
xxHash is an Extremely fast Hash algorithm, running at RAM speed
limits. It successfully completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash
functions. Code is highly portable, and hashes are identical on all
platforms (little / big endian).

%package libs
Summary:	Extremely fast hash algorithm - library
License:	BSD-2-Clause

%description libs
xxHash is an Extremely fast Hash algorithm, running at RAM speed
limits. It successfully completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash
functions. Code is highly portable, and hashes are identical on all
platforms (little / big endian).

%package devel
Summary:	Extremely fast hash algorithm - development files
License:	BSD-2-Clause
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
# By setting XXH_INLINE_ALL, xxhash may be used as a header-only library.
# Dependent packages that use xxhash this way must BR this virtual Provide:
Provides:	%{name}-static = %{version}-%{release}

%description devel
Development files for the xxhash library

%package doc
Summary:	Extremely fast hash algorithm - documentation files
License:	BSD-2-Clause
BuildArch:	noarch

%description doc
Documentation files for the xxhash library

%prep
%setup -q -n xxHash-%{version}

%build
# Enable runtime detection of sse2/avx2/avx512 on intel architectures
%ifarch %{ix86} x86_64
%global dispatch 1
# Some distribution variants build with -march=x86-64-v3.
# See xxh_x86dispatch.c.
%global moreflags_dispatch -DXXH_X86DISPATCH_ALLOW_AVX
%else
%global dispatch 0
%global moreflags_dispatch %{nil}
%endif

%make_build \
    MOREFLAGS="%{__global_cflags} %{?__global_ldflags} %{moreflags_dispatch}" \
    DISPATCH=%{dispatch} \
    LIBXXH_DISPATCH=%{dispatch}
doxygen

%install
%make_install \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir} \
    DISPATCH=%{dispatch} \
    LIBXXH_DISPATCH=%{dispatch}
rm %{buildroot}/%{_libdir}/libxxhash.a

%check
make check
make test-xxhsum-c

%files
%{_bindir}/xxh*sum
%{_mandir}/man1/xxh*sum.1*
%license cli/COPYING
%doc cli/README.md

%files libs
%{_libdir}/libxxhash.so.*
%license LICENSE
%doc README.md

%files devel
%{_includedir}/xxhash.h
%{_includedir}/xxh3.h
%if %{?dispatch}
%{_includedir}/xxh_x86dispatch.h
%endif
%{_libdir}/libxxhash.so
%{_libdir}/pkgconfig/libxxhash.pc

%files doc
%doc doxygen/html

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.8.3-1
- Update to version 0.8.3

* Wed Sep 25 2024 Andreas Rogge <andreas.rogge@bareos.com> - 0.8.2-4
- add xxh_x86dispatch.h to devel package when dispatching is enabled (rhbz#2314193)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.8.2-1
- Update to version 0.8.2
- Drop patch xxhash-epel7-ppc64le.patch
- Use SPDX license identifiers

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Florian Weimer <fweimer@redhat.com> - 0.8.1-5
- Enable building with -march=x86-64-v3 (#2215831)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.8.1-1
- Update to version 0.8.1
- Drop patch xxhash-pkgconfig-version.patch (accepted upstream)
- Fix compilation on RHEL 7 ppc64le (gcc 4.8)
- The x86 dispatch code now enables sse2 and avx2 separately, it can now use
  sse2 on EPEL 7 without trying to use avx2 which is not supported by gcc 4.8
- Add documentation package - doxygen mark-up was added

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.0-3
- Add virtual Provide for xxhash-static in xxhash-devel

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.8.0-1
- Update to version 0.8.0
- Drop patches xxhash-compiler-warning-32-bit.patch (accepted upstream)
  and xxhash-pkgconfig.patch (issue fixed upstream)
- Fix empty version in .pc file

* Fri Jul 24 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.7.4-2
- Fix libdir in pkg-config file

* Sat Jun 27 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.7.4-1
- Update to version 0.7.4
- Enable runtime detection of sse2/avx2/avx512 on intel architectures
- Fix compiler warning for 32 bit architectures

* Fri Mar 06 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.7.3-1
- Update to version 0.7.3
- Drop patch xxhash-gcc10-altivec.patch (accepted upstream)

* Fri Feb 07 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.7.2-3
- Fix ppc64le build with gcc 10

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 09 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.7.2-1
- Update to version 0.7.2

* Sat Aug 17 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.7.1-1
- Update to version 0.7.1

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.7.0-1
- Update to version 0.7.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 19 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.6.5-1
- Update to version 0.6.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.6.4-1
- Update to version 0.6.4
- Drop previously backported patches

* Thu Oct 19 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.6.3-2
- Correct License tag (command line tool is GPLv2+)
- Adjust Source tag to get a more descriptive tarfile name

* Wed Oct 18 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 0.6.3-1
- Initial packaging
