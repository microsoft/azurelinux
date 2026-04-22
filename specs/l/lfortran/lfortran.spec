# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Version:        0.56.0
Name:           lfortran
Release: 3%{?dist}
Summary:        A modern Fortran compiler

# Main code is BSD-3-Clause
# src/libasr/codegen/KaleidoscopeJIT.h is available under the Apache 2.0
# License with LLVM exception
License:        BSD-3-Clause AND Apache-2.0 WITH LLVM-exception
URL:            https://lfortran.org/
Source0:        https://github.com/lfortran/lfortran/releases/download/v%{version}/lfortran-%{version}.tar.gz
# Add support for LLVM 21
Patch:          https://github.com/lfortran/lfortran/pull/8611.patch

# https://github.com/lfortran/lfortran/issues/2981
ExclusiveArch: x86_64

%global with_jupyter 1

BuildRequires: binutils-devel
BuildRequires: bison
BuildRequires: cmake
BuildRequires: fmt-devel
BuildRequires: gcc-c++
BuildRequires: json-devel
BuildRequires: libffi-devel
BuildRequires: libunwind-devel
BuildRequires: libuuid-devel
BuildRequires: llvm-devel
BuildRequires: python3-devel
BuildRequires: rapidjson-devel
BuildRequires: re2c
BuildRequires: zlib-ng-compat-devel
BuildRequires: zlib-ng-compat-static
%if %{with_jupyter}
# Needed for Jupyter kernel
BuildRequires: cppzmq-devel
BuildRequires: json-devel
BuildRequires: openssl-devel
BuildRequires: xeus-devel
BuildRequires: xeus-zmq-devel
BuildRequires: xtl-devel
%endif
# For backend=cpp
BuildRequires: kokkos-devel
# Not explicitly linked, hence listed here
Requires: kokkos-devel

Requires: %{name}-shared%{?_isa} = %{version}-%{release}

%global lfortran_desc \
LFortran is a modern open-source (BSD licensed) interactive Fortran \
compiler built on top of LLVM. It can execute user's code interactively \
to allow exploratory work (much like Python, MATLAB or Julia) as well as \
compile to binaries with the goal to run user's code on modern \
architectures such as multi-core CPUs and GPUs.

%description
%{lfortran_desc}

%package devel
Summary:  Development headers and libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{lfortran_desc}

This package contains development headers and libraries for %{name}.

%package static
Summary:   Static runtime library for %{name}

%description static
%{lfortran_desc}

This package contains static runtime library for %{name}.

%package shared
Summary:   Shared runtime library for %{name}

%description shared
%{lfortran_desc}

This package contains shared runtime library for %{name}.

%if %{with_jupyter}
%package jupyter
Summary:   Jupyter kernel for %{name}
Requires:  %{name}%{?_isa} = %{version}-%{release}
Requires:  jupyterlab
Requires:  python-jupyter-filesystem

%description jupyter
%{lfortran_desc}

This package contains the jupyter kernel for %{name}.
%endif


%prep
%autosetup -p1

%build
# WITH_ZSD is just used to fix static linking of llvm
# not needed on Fedora
# WASM=OFF due to lfortran/lfortran#3899
# WITH_STACKTRACE=OFF due to lfortran/lfortran#5072
%cmake \
       -DWITH_LLVM=ON \
       -DWITH_ZSTD=OFF \
       -DWITH_RUNTIME_LIBRARY=ON \
       -DWITH_FMT=ON \
       -DWITH_JSON=ON \
       -DWITH_KOKKOS=ON \
       -DWITH_STACKTRACE=OFF \
       -DWITH_TARGET_WASM=OFF \
       -DWITH_UNWIND=ON \
       -DWITH_WHEREAMI=ON \
       -DWITH_XEUS=%{with_jupyter} \
       -DWITH_ZLIB=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
# liblfortran_runtime.so is in this package as
# lfortran calls it directly.
%doc README.md
%license LICENSE
%{_bindir}/lfortran
%{_mandir}/man1/lfortran.1.*
%{_libdir}/liblfortran_runtime.so

%files devel
%dir %{_includedir}/lfortran
%dir %{_includedir}/lfortran/impure
%{_includedir}/lfortran/impure/lfortran_intrinsics.h
%dir %{_datadir}/lfortran
%{_datadir}/lfortran/*.py
%{_libdir}/lfortran_*.mod
%{_libdir}/omp_lib.mod

%files static
%{_libdir}/liblfortran_runtime_static.a

%files shared
%{_libdir}/liblfortran_runtime.so.*

%if %{with_jupyter}
%files jupyter
%dir %{_datadir}/jupyter/kernels/fortran
%{_datadir}/jupyter/kernels/fortran/kernel.json
%{_datadir}/jupyter/kernels/fortran/logo-svg.svg
%endif

%changelog
* Mon Sep 22 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.56.0-2
- Add support for LLVM 21
- Rebuild for xeus SONAME bump

* Mon Aug 18 2025 Packit <hello@packit.dev> - 0.56.0-1
- Update to version 0.56.0
- Resolves: rhbz#2389120

* Sat Aug 09 2025 Packit <hello@packit.dev> - 0.55.0-1
- Update to version 0.55.0
- Resolves: rhbz#2387438

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.54.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Christoph Junghans <junghans@votca.org> - 0.54.0-1
- Version bump to v0.54.0

* Wed Jun 11 2025 Packit <hello@packit.dev> - 0.53.0-1
- Update to version 0.53.0
- Resolves: rhbz#2372344

* Mon May 05 2025 Packit <hello@packit.dev> - 0.52.0-1
- Update to version 0.52.0
- Resolves: rhbz#2364257

* Tue Apr 08 2025 Benson Muite <fed500@fedoraproject.org> - 0.51.0-1
- Version bump to v0.51.0 (bug #2358171)

* Mon Mar 31 2025 Christoph Junghans <junghans@votca.org> - 0.50.0-1
- Version bump to v0.50.0 (bug #2355916)

* Sun Mar 16 2025 Benson Muite <fed500@fedoraproject.org> - 0.49.0-2
- Remove unneeded patch

* Sun Mar 16 2025 Benson Muite <fed500@fedoraproject.org> - 0.49.0-1
- Version bump to v0.49.0 (bug #2352738)

* Mon Mar 10 2025 Christoph Junghans <junghans@votca.org> - 0.48.0-2
- Fix build with llvm-20

* Mon Mar 10 2025 Christoph Junghans <junghans@votca.org> - 0.48.0-1
- Version bump to v0.48.0 (bug #2351164)

* Fri Mar 07 2025 Christoph Junghans <junghans@votca.org> - 0.47.0-1
- Version bump v0.47.0 (bug #2350550)

* Sat Mar 01 2025 Christoph Junghans <junghans@votca.org> - 0.46.0-1
- Version bump to v0.46.0 (bug #2349117)

* Sun Jan 26 2025 Christoph Junghans <junghans@votca.org> - 0.45.0-1
- Version bump to v0.45.0 (bug #2342111)

* Sun Jan 19 2025 Christoph Junghans <junghans@votca.org> - 0.44.0-1
- Version bump to v0.44.0 (bug #2338372)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 16 2024 Christoph Junghans <junghans@votca.org> - 0.42.0-3
- Build with llvm-19

* Sat Dec 14 2024 Christoph Junghans <junghans@votca.org> - 0.42.0-2
- Build with llvm18

* Tue Dec 10 2024 Benson Muite <benson_muite@emailplus.org> - 0.42.0-1
- Version bump v0.42.0 (bug #2326295)

* Mon Oct 14 2024 Christoph Junghans <junghans@votca.org> - 0.41.0-1
- Version bump v0.41.0 (bug #2304184)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jul 14 2024 Benson Muite <benson_muite@emailplus.org> - 0.38.0-1
- Version bump to v0.38.0 (bug #2296537)

* Wed Jul 03 2024 Christoph Junghans <junghans@votca.org> - 0.37.0-1
- Version bump to v0.37.0 (bug #2295521)

* Mon Jun 24 2024 Christoph Junghans <junghans@votca.org> - 0.36.1-1
- Version bump to v0.36.1 (bug #2293599)

* Thu May 30 2024 Benson Muite <benson_muite@emailplus.org> - 0.36.0-1
- Version bump to v0.36.0 (bug #2283918)

* Thu Apr 18 2024 Christoph Junghans <junghans@votca.org> - 0.35.0-1
- Version bump to v0.35.0 (bug #2271254)

* Wed Jan 31 2024 Christoph Junghans <junghans@votca.org> - 0.33.1-2
- Move liblfortran_runtime.so to the right package

* Wed Jan 31 2024 Christoph Junghans <junghans@votca.org> - 0.33.1-1
- Version bump to v0.33.1

* Wed Jan 31 2024 Christoph Junghans <junghans@votca.org> - 0.33.0-1
- Version bump to v0.33.0 (bug #2261190)

* Mon Jan 29 2024 Benson Muite <benson_muite@emailplus.org> - 0.32.0-1
- Version bump to v0.32.0 (bug #2260659)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Christoph Junghans <junghans@votca.org> - 0.31.0-1
- Version bump to v0.31.0 (bug #2259671)

* Fri Jan 19 2024 Christoph Junghans <junghans@votca.org> - 0.30.0-9
- Drop jupyter package on F38

* Fri Jan 19 2024 Christoph Junghans <junghans@votca.org> - 0.30.0-8
- Add kokkos dependency

* Fri Jan 19 2024 Benson Muite <benson_muite@emailplus.org> - 0.30.0-7
- Use conditional includes for llvm and zlib

* Fri Jan 19 2024 Benson Muite <benson_muite@emailplus.org> - 0.30.0-6
- Use llvm instead of llvm16 on f38

* Fri Jan 19 2024 Benson Muite <benson_muite@emailplus.org> - 0.30.0-5
- Use zlib for f39 and f38

* Tue Jan 16 2024 Benson Muite <benson_muite@emailplus.org> - 0.30.0-4
- Use zlib-ng
- Ensure all directories are owned

* Mon Jan 15 2024 Christoph Junghans <junghans@votca.org> - 0.30.0-3
- Enable WASM backend

* Wed Jan 10 2024 Christoph Junghans <junghans@votca.org> - 0.30.0-2
- More subpackages

* Thu Jan 04 2024 Christoph Junghans <junghans@votca.org> - 0.30.0-1
- Version bump v0.30.0

* Sat Oct 07 2023 Benson Muite <benson_muite@emailplus.org> - 0.21.5-1
- Initial packaging
