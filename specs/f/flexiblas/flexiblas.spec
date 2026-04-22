# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond system_lapack 0
%bcond atlas %[%{undefined rhel} && %{undefined flatpak} && "%{_arch}" != "riscv64" ]
%bcond blis %[%{undefined rhel} && %{undefined flatpak}]
%bcond openblas 1

# https://bugzilla.redhat.com/show_bug.cgi?id=2058840
%undefine _ld_as_needed

%if %{with openblas}
%global default_backend openblas-openmp
%else
%global default_backend netlib
%endif
%global default_backend64 %{default_backend}64

%global major_version 3
%global minor_version 5
%global patch_version 0

Name:           flexiblas
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release: 2%{?dist}
Summary:        A BLAS/LAPACK wrapper library with runtime exchangeable backends

# LGPL-3.0-or-later
# libcscutils/ is LGPL-2.0-or-later
# contributed/ and test/ are BSD-3-Clause-Open-MPI
License:        LGPL-3.0-or-later AND LGPL-2.0-or-later AND BSD-3-Clause-Open-MPI
URL:            https://www.mpi-magdeburg.mpg.de/projects/%{name}
Source:         https://github.com/mpimd-csc/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake, python
BuildRequires:  gcc, gcc-fortran
BuildRequires:  multilib-rpm-config
%if %{with system_lapack}
BuildRequires:  blas-static, lapack-static
%endif
%if %{with atlas}
BuildRequires:  atlas-devel
%endif
%if %{with blis}
BuildRequires:  blis-devel
%endif
%if %{with openblas}
BuildRequires:  openblas-devel
%endif
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}

%global _description %{expand:
FlexiBLAS is a wrapper library that enables the exchange of the BLAS and
LAPACK implementation used by a program without recompiling or relinking it.
}

%description %_description

%package        netlib
Summary:        FlexiBLAS wrapper library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-%{default_backend}%{?_isa} = %{version}-%{release}

%description    netlib %_description
This package contains the wrapper library with 32-bit integer support.

%package        hook-profile
Summary:        FlexiBLAS profile hook plugin
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}

%description    hook-profile %_description
This package contains a plugin that enables profiling support.

%package        devel
Summary:        Development headers and libraries for FlexiBLAS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}
%if 0%{?__isa_bits} == 64
Requires:       %{name}-netlib64%{?_isa} = %{version}-%{release}
%endif

%description    devel %_description
This package contains the development headers and libraries.

%if %{with atlas}
%package        atlas
Supplements:    (atlas and %{name})
Summary:        FlexiBLAS wrappers for ATLAS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}

%description    atlas %_description
This package contains FlexiBLAS wrappers for the ATLAS project.
%endif

%if %{with blis}
%package        blis-serial
Supplements:    (blis-serial and %{name})
Summary:        FlexiBLAS wrappers for BLIS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}

%description    blis-serial %_description
This package contains FlexiBLAS wrappers for the sequential library compiled
with a 32-integer interface.

%package        blis-openmp
Supplements:    (blis-openmp and %{name})
Summary:        FlexiBLAS wrappers for BLIS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}

%description    blis-openmp %_description
This package contains FlexiBLAS wrappers for the library compiled with
OpenMP support with a 32-integer interface.

%package        blis-threads
Supplements:    (blis-threads and %{name})
Summary:        FlexiBLAS wrappers for BLIS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}

%description    blis-threads %_description
This package contains FlexiBLAS wrappers for the library compiled with
threading support with a 32-integer interface.
%endif

%if %{with openblas}
%package        openblas-serial
Supplements:    (openblas-serial and %{name})
Summary:        FlexiBLAS wrappers for OpenBLAS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}

%description    openblas-serial %_description
This package contains FlexiBLAS wrappers for the sequential library compiled
with a 32-integer interface.

%package        openblas-openmp
Supplements:    (openblas-openmp and %{name})
Summary:        FlexiBLAS wrappers for OpenBLAS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}

%description    openblas-openmp %_description
This package contains FlexiBLAS wrappers for the library compiled with
OpenMP support with a 32-integer interface.

%package        openblas-threads
Supplements:    (openblas-threads and %{name})
Summary:        FlexiBLAS wrappers for OpenBLAS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib%{?_isa} = %{version}-%{release}

%description    openblas-threads %_description
This package contains FlexiBLAS wrappers for the library compiled with
threading support with a 32-integer interface.
%endif

%if 0%{?__isa_bits} == 64
%package        netlib64
Summary:        FlexiBLAS wrapper library (64-bit)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-%{default_backend64}%{?_isa} = %{version}-%{release}

%description    netlib64 %_description
This package contains the wrapper library with 64-bit integer support.

%package        hook-profile64
Summary:        FlexiBLAS profile hook plugin (64-bit)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib64%{?_isa} = %{version}-%{release}

%description    hook-profile64 %_description
This package contains a plugin that enables profiling support.

%if %{with blis}
%package        blis-serial64
Supplements:    (blis-serial64 and %{name})
Summary:        FlexiBLAS wrappers for BLIS (64-bit)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib64%{?_isa} = %{version}-%{release}

%description    blis-serial64 %_description
This package contains FlexiBLAS wrappers for the sequential library compiled
with a 64-integer interface.

%package        blis-openmp64
Supplements:    (blis-openmp64 and %{name})
Summary:        FlexiBLAS wrappers for BLIS (64-bit)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib64%{?_isa} = %{version}-%{release}

%description    blis-openmp64 %_description
This package contains FlexiBLAS wrappers for the library compiled with
OpenMP support with a 64-integer interface.

%package        blis-threads64
Supplements:    (blis-threads64 and %{name})
Summary:        FlexiBLAS wrappers for BLIS (64-bit)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib64%{?_isa} = %{version}-%{release}

%description    blis-threads64 %_description
This package contains FlexiBLAS wrappers for the library compiled with
threading support with a 64-integer interface.
%endif

%if %{with openblas}
%package        openblas-serial64
Supplements:    (openblas-serial64 and %{name})
Summary:        FlexiBLAS wrappers for OpenBLAS (64-bit)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib64%{?_isa} = %{version}-%{release}

%description    openblas-serial64 %_description
This package contains FlexiBLAS wrappers for the sequential library compiled
with a 64-integer interface.

%package        openblas-openmp64
Supplements:    (openblas-openmp64 and %{name})
Summary:        FlexiBLAS wrappers for OpenBLAS (64-bit)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib64%{?_isa} = %{version}-%{release}

%description    openblas-openmp64 %_description
This package contains FlexiBLAS wrappers for the library compiled with
OpenMP support with a 64-integer interface.

%package        openblas-threads64
Supplements:    (openblas-threads64 and %{name})
Summary:        FlexiBLAS wrappers for OpenBLAS (64-bit)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-netlib64%{?_isa} = %{version}-%{release}

%description    openblas-threads64 %_description
This package contains FlexiBLAS wrappers for the library compiled with
threading support with a 64-integer interface.
%endif
%endif

%prep
%autosetup -p1

%build
%if %{with system_lapack}
rm -rf contributed/{cblas,lapack-*,netlib-blas,win32ports}
%endif
%global _vpath_builddir build
%cmake \
%if %{with system_lapack}
    -DSYS_BLAS_LIBRARY=$(pkg-config --variable=libdir blas)/libblas.a \
    -DSYS_LAPACK_LIBRARY=$(pkg-config --variable=libdir lapack)/liblapack.a \
%endif
    -DINTEGER8=OFF \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
    -DTESTS=ON
%cmake_build
%if 0%{?__isa_bits} == 64
%global _vpath_builddir build64
%cmake \
%if %{with system_lapack}
    -DSYS_BLAS_LIBRARY=$(pkg-config --variable=libdir blas)/libblas64.a \
    -DSYS_LAPACK_LIBRARY=$(pkg-config --variable=libdir lapack)/liblapack64.a \
%endif
    -DINTEGER8=ON \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
    -DTESTS=ON
%cmake_build
%endif

%install
%global _vpath_builddir build
%cmake_install
echo "default = %{default_backend}" > %{buildroot}%{_sysconfdir}/%{name}rc
%if 0%{?__isa_bits} == 64
%global _vpath_builddir build64
%cmake_install
echo "default = %{default_backend64}" > %{buildroot}%{_sysconfdir}/%{name}64rc
%endif

# Replace arch-dependent header file with arch-independent stub
%multilib_fix_c_header --file %{_includedir}/%{name}/%{name}_config.h

# remove dummy hook
rm -f %{buildroot}%{_libdir}/%{name}*/lib%{name}_hook_dummy.so

# set Fedora-friendly names
rename -- serial -serial %{buildroot}%{_libdir}/%{name}*/* || true
rename -- openmp -openmp %{buildroot}%{_libdir}/%{name}*/* || true
rename -- pthread -threads %{buildroot}%{_libdir}/%{name}*/* || true
rename -- Serial -serial %{buildroot}%{_sysconfdir}/%{name}*.d/* || true
rename -- OpenMP -openmp %{buildroot}%{_sysconfdir}/%{name}*.d/* || true
rename -- PThread -threads %{buildroot}%{_sysconfdir}/%{name}*.d/* || true
find %{buildroot}%{_sysconfdir}/%{name}*.d/* -type f \
    -exec sed -i 's Serial -serial gI' {} \;\
    -exec sed -i 's OpenMP -openmp gI' {} \;\
    -exec sed -i 's PThread -threads gI' {} \;\
    -exec sed -i 's .* \L& g' {} \;\
    -exec sh -c 'mv $0 $(dirname $0)/$(basename $0 | tr [A-Z] [a-z])' {} \;

%check
%global _smp_mflags -j1
# limit the number of threads
# MAX_CORES=10; CORES=$(nproc)
# export OMP_NUM_THREADS=$((CORES > MAX_CORES ? MAX_CORES : CORES))
export CTEST_OUTPUT_ON_FAILURE=1
export FLEXIBLAS_TEST=%{buildroot}%{_libdir}/%{name}/lib%{name}_%{default_backend}.so
%global _vpath_builddir build
%ctest
%if 0%{?__isa_bits} == 64
export FLEXIBLAS64_TEST=%{buildroot}%{_libdir}/%{name}64/lib%{name}_%{default_backend64}.so
%global _vpath_builddir build64
%ctest
%endif

%files
%license COPYING COPYING.NETLIB
%doc ISSUES.md README.md CHANGELOG

%files netlib
%config(noreplace) %{_sysconfdir}/%{name}rc
%dir %{_sysconfdir}/%{name}rc.d
%{_sysconfdir}/%{name}rc.d/netlib.conf
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.%{major_version}
%{_libdir}/lib%{name}.so.%{major_version}.%{minor_version}
%{_libdir}/lib%{name}_api.so.%{major_version}
%{_libdir}/lib%{name}_api.so.%{major_version}.%{minor_version}
%{_libdir}/lib%{name}_mgmt.so.%{major_version}
%{_libdir}/lib%{name}_mgmt.so.%{major_version}.%{minor_version}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lib%{name}_fallback_lapack.so
%{_libdir}/%{name}/lib%{name}_netlib.so
%{_mandir}/man1/%{name}.1*

%files hook-profile
%{_libdir}/%{name}/lib%{name}_hook_profile.so

%files devel
%{_bindir}/%{name}-config
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_api.so
%{_libdir}/lib%{name}_mgmt.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}_api.pc
%if 0%{?__isa_bits} == 64
%{_bindir}/%{name}64-config
%{_includedir}/%{name}64
%{_libdir}/lib%{name}64.so
%{_libdir}/lib%{name}64_api.so
%{_libdir}/lib%{name}64_mgmt.so
%{_libdir}/pkgconfig/%{name}64.pc
%{_libdir}/pkgconfig/%{name}64_api.pc
%endif
%{_mandir}/man3/%{name}_*
%{_mandir}/man7/%{name}-api.7*

%if %{with atlas}
%files atlas
%{_sysconfdir}/%{name}rc.d/*atlas.conf
%{_libdir}/%{name}/lib%{name}_*atlas.so
%endif

%if %{with blis}
%files blis-serial
%{_sysconfdir}/%{name}rc.d/blis-serial.conf
%{_libdir}/%{name}/lib%{name}_blis-serial.so

%files blis-openmp
%{_sysconfdir}/%{name}rc.d/blis-openmp.conf
%{_libdir}/%{name}/lib%{name}_blis-openmp.so

%files blis-threads
%{_sysconfdir}/%{name}rc.d/blis-threads.conf
%{_libdir}/%{name}/lib%{name}_blis-threads.so
%endif

%if %{with openblas}
%files openblas-serial
%{_sysconfdir}/%{name}rc.d/openblas-serial.conf
%{_libdir}/%{name}/lib%{name}_openblas-serial.so

%files openblas-openmp
%{_sysconfdir}/%{name}rc.d/openblas-openmp.conf
%{_libdir}/%{name}/lib%{name}_openblas-openmp.so

%files openblas-threads
%{_sysconfdir}/%{name}rc.d/openblas-threads.conf
%{_libdir}/%{name}/lib%{name}_openblas-threads.so
%endif

%if 0%{?__isa_bits} == 64
%files netlib64
%config(noreplace) %{_sysconfdir}/%{name}64rc
%dir %{_sysconfdir}/%{name}64rc.d
%{_sysconfdir}/%{name}64rc.d/netlib.conf
%{_bindir}/%{name}64
%{_libdir}/lib%{name}64.so.%{major_version}
%{_libdir}/lib%{name}64.so.%{major_version}.%{minor_version}
%{_libdir}/lib%{name}64_api.so.%{major_version}
%{_libdir}/lib%{name}64_api.so.%{major_version}.%{minor_version}
%{_libdir}/lib%{name}64_mgmt.so.%{major_version}
%{_libdir}/lib%{name}64_mgmt.so.%{major_version}.%{minor_version}
%dir %{_libdir}/%{name}64
%{_libdir}/%{name}64/lib%{name}_fallback_lapack.so
%{_libdir}/%{name}64/lib%{name}_netlib.so
%{_mandir}/man1/%{name}64.1*

%files hook-profile64
%{_libdir}/%{name}64/lib%{name}_hook_profile.so

%if %{with blis}
%files blis-serial64
%{_sysconfdir}/%{name}64rc.d/blis-serial64.conf
%{_libdir}/%{name}64/lib%{name}_blis-serial64.so

%files blis-openmp64
%{_sysconfdir}/%{name}64rc.d/blis-openmp64.conf
%{_libdir}/%{name}64/lib%{name}_blis-openmp64.so

%files blis-threads64
%{_sysconfdir}/%{name}64rc.d/blis-threads64.conf
%{_libdir}/%{name}64/lib%{name}_blis-threads64.so
%endif

%if %{with openblas}
%files openblas-serial64
%{_sysconfdir}/%{name}64rc.d/openblas-serial64.conf
%{_libdir}/%{name}64/lib%{name}_openblas-serial64.so

%files openblas-openmp64
%{_sysconfdir}/%{name}64rc.d/openblas-openmp64.conf
%{_libdir}/%{name}64/lib%{name}_openblas-openmp64.so

%files openblas-threads64
%{_sysconfdir}/%{name}64rc.d/openblas-threads64.conf
%{_libdir}/%{name}64/lib%{name}_openblas-threads64.so
%endif
%endif

%changelog
* Sat Oct 25 2025 Iñaki Úcar <iucar@fedoraproject.org> - 3.5.0-1
- Update to 3.5.0

* Thu Aug 28 2025 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.5-5
- Rebuild for lapack 3.12.0-10

* Wed Jul 30 2025 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.5-4
- Rebuild for blis 2.0 (rhbz#2384773)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.5-2
- Opt out https://fedoraproject.org/wiki/Changes/CMake_ninja_default

* Fri Jan 31 2025 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.5-1
- Update to 3.4.5
- Remove thread limit for testing

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.4-6
- Restore atlas support, was saved

* Wed Jan 08 2025 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.4-5
- Limit the number of threads for testing

* Sun Dec 22 2024 Orion Poplawski <orion@nwra.com> - 3.4.4-4
- Drop atlas support in Fedora 42+

* Wed Aug 07 2024 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.4-3
- Bump LAPACK API to 3.12.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 24 2024 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.4-1
- Update to 3.4.4

* Wed Feb 28 2024 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.2-1
- Update to 3.4.2 (rhbz#2264712)

* Fri Feb 09 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 3.4.1-4
- Disable ATLAS and BLIS in RHEL builds

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.1-1
- Update to 3.4.1

* Tue Jan 09 2024 Iñaki Úcar <iucar@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0
- License changes to LGPL-3.0-or-later

* Tue Jul 25 2023 Iñaki Úcar <iucar@fedoraproject.org> - 3.3.1-5
- Add Supplements to help pull wrappers if libraries are installed directly

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 19 2023 Iñaki Úcar <iucar@fedoraproject.org> - 3.3.1-3
- Require netlib from base package
- Adapt license tag to SPDX
- Add rpminspect.yaml file to skip tests with false positives

* Tue Apr 04 2023 Iñaki Úcar <iucar@fedoraproject.org> - 3.3.1-2
- Fix multilib config header conflict

* Mon Apr 03 2023 Iñaki Úcar <iucar@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Iñaki Úcar <iucar@fedoraproject.org> - 3.3.0-1
- Update to 3.3.0

* Fri Dec 23 2022 Iñaki Úcar <iucar@fedoraproject.org> - 3.2.1-3
- Specify LAPACK API compatibility level

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Iñaki Úcar <iucar@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1

* Mon Jun 27 2022 Iñaki Úcar <iucar@fedoraproject.org> - 3.2.0-4
- Add depency on netlib subpackage to all backends (RHBZ#2101369)

* Tue May 24 2022 Iñaki Úcar <iucar@fedoraproject.org> - 3.2.0-3
- Add explicit requires to devel package to content rpmdeps test

* Tue May 17 2022 Iñaki Úcar <iucar@fedoraproject.org> - 3.2.0-2
- Undefine _ld_as_needed to fix underlinking issue (BZ 2058840)

* Tue May 17 2022 Iñaki Úcar <iucar@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0

* Fri Feb 25 2022 Iñaki Úcar <iucar@fedoraproject.org> - 3.1.3-1
- Update to 3.1.3

* Mon Jan 17 2022 Iñaki Úcar <iucar@fedoraproject.org> - 3.1.2-1
- Update to 3.1.2, adding support for LAPACK up to 3.10.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Nikola Forró <nforro@redhat.com> - 3.0.4-5
- Get rid of RPATH

* Fri Apr 23 2021 Iñaki Úcar <iucar@fedoraproject.org> 3.0.4-4
- Rebuilt for LAPACK 3.9.1 with LAPACK_API_VERSION=3.9.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Iñaki Úcar <iucar@fedoraproject.org> 3.0.4-2
- https://fedoraproject.org/wiki/Changes/Remove_make_from_BuildRoot

* Thu Oct 22 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.0.4-1
- Update to 3.0.4, fixes #1889069

* Wed Oct 21 2020 Kalev Lember <klember@redhat.com> - 3.0.3-2
- Use pkg-config for getting blas and lapack directories

* Fri Aug 28 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.0.3-1
- Update to 3.0.3, fixes ScaLAPACK issues

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2

* Tue Jul 21 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1, license updated

* Fri Jul 03 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.0.0-5
- Change default backend to openblas-openmp

* Wed Jul 01 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.0.0-4
- Fix a bug setting the default backend

* Wed Jul 01 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.0.0-3
- Move man3 pages to devel subpackage
- Remove dummy hook (only useful for FlexiBLAS development)
- Move profile hook to a separate package (not needed for standard usage)
- Enable Blis64 on s390x again, #1852549 fixed in rawhide

* Tue Jun 30 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.0.0-2
- Own provided directories
- More robust file renaming
- Rename wrapper(64) subpackages to netlib(64)
- Conditionalize all external libraries, as well as the default
- Disable Blis64 on s390x, which is currently unavailable

* Mon Jun 29 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.0.0-1
- Initial packaging for Fedora
