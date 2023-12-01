%global security_hardening nofortify
%define _use_internal_dependency_generator 0
Summary:        Contains the GNU compiler collection
Name:           gcc
Version:        13.2.0
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://gcc.gnu.org/
Source0:        https://ftp.gnu.org/gnu/gcc/%{name}-%{version}/%{name}-%{version}.tar.xz
#Patch0:         CVE-2023-4039.patch
Requires:       gcc-c++ = %{version}-%{release}
Requires:       gmp
Requires:       libgcc-atomic = %{version}-%{release}
Requires:       libgcc-devel = %{version}-%{release}
Requires:       libgomp-devel = %{version}-%{release}
Requires:       libmpc
Requires:       libstdc++-devel = %{version}-%{release}
Provides:       cpp = %{version}-%{release}
Provides:       gcc-plugin-devel = %{version}-%{release}
Provides:       libasan = %{version}-%{release}
Provides:       libasan%{?_isa} = %{version}-%{release}
Provides:       libasan-static = %{version}-%{release}
Provides:       libasan-static%{?_isa} = %{version}-%{release}
Provides:       liblsan = %{version}-%{release}
Provides:       liblsan%{?_isa} = %{version}-%{release}
Provides:       liblsan-static = %{version}-%{release}
Provides:       liblsan-static%{?_isa} = %{version}-%{release}
Provides:       libtsan = %{version}-%{release}
Provides:       libtsan%{?_isa} = %{version}-%{release}
Provides:       libtsan-static = %{version}-%{release}
Provides:       libtsan-static%{?_isa} = %{version}-%{release}
Provides:       libubsan = %{version}-%{release}
Provides:       libubsan%{?_isa} = %{version}-%{release}
Provides:       libubsan-static = %{version}-%{release}
Provides:       libubsan-static%{?_isa} = %{version}-%{release}
Provides:       libquadmath = %{version}-%{release}
Provides:       libquadmath-devel = %{version}-%{release}
Provides:       libquadmath-devel%{?_isa} = %{version}-%{release}
#%if %{with_check}
#BuildRequires:  autogen
#BuildRequires:  dejagnu
#%endif

%description
The GCC package contains the GNU compiler collection,
which includes the C and C++ compilers.

%package -n     gfortran
Summary:        GNU Fortran compiler.
Group:          Development/Tools
Requires:       gcc = %{version}-%{release}
Provides:       gcc-gfortran = %{version}-%{release}

%description -n gfortran
The gfortran package contains GNU Fortran compiler.

%package -n     libgcc
Summary:        GNU C Library
Group:          System Environment/Libraries

%description -n libgcc
The libgcc package contains GCC shared libraries for gcc.

%package -n     libgcc-atomic
Summary:        GNU C Library for atomic counter updates
Group:          System Environment/Libraries
Requires:       libgcc = %{version}-%{release}
Provides:       libatomic = %{version}-%{release}

%description -n libgcc-atomic
The libgcc package contains GCC shared libraries for atomic counter updates.

%package -n     libgcc-devel
Summary:        GNU C Library
Group:          Development/Libraries
Requires:       libgcc = %{version}-%{release}

%description -n libgcc-devel
The libgcc package contains GCC shared libraries for gcc .
This package contains development headers and static library for libgcc.

%package        c++
Summary:        C++ support for GCC
Group:          System Environment/Libraries
Requires:       gcc = %{version}-%{release}
Requires:       libstdc++-devel = %{version}-%{release}
Provides:       gcc-g++ = %{version}-%{release}
Provides:       g++ = %{version}-%{release}

%description    c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n     libbacktrace-static
Summary:        Static library for GCC's libbacktrace.
Group:          System Environment/Libraries

%description -n libbacktrace-static
This package contains GCC's static libbacktrace library and its header.

%package -n     libstdc++
Summary:        GNU C Library
Group:          System Environment/Libraries
Requires:       libgcc = %{version}-%{release}

%description -n libstdc++
This package contains the GCC Standard C++ Library v3, an ongoing project to implement the ISO/IEC 14882:1998 Standard C++ library.

%package -n     libstdc++-devel
Summary:        GNU C Library
Group:          Development/Libraries
Requires:       libstdc++ = %{version}-%{release}
Provides:       libstdc++-static = %{version}-%{release}

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.
This package includes the headers files and libraries needed for C++ development.

%package -n     libgomp
Summary:        GNU C Library
Group:          System Environment/Libraries

%description -n libgomp
An implementation of OpenMP for the C, C++, and Fortran 95 compilers in the GNU Compiler Collection.

%package -n     libgomp-devel
Summary:        Development headers and static library for libgomp
Group:          Development/Libraries
Requires:       libgomp = %{version}-%{release}

%description -n libgomp-devel
An implementation of OpenMP for the C, C++, and Fortran 95 compilers in the GNU Compiler Collection.
This package contains development headers and static library for libgomp

%prep
%autosetup -p1

%build

CFLAGS="`echo " %{build_cflags} " | sed 's/-Werror=format-security/-Wno-error=format-security/'`"
CXXFLAGS="`echo " %{build_cxxflags} " | sed 's/-Werror=format-security/-Wno-error=format-security/'`"
FCFLAGS="`echo " %{build_fflags} " | sed 's/-Werror=format-security/-Wno-error=format-security/'`"
export CFLAGS="$CFLAGS -Wno-error=missing-include-dirs"
export CXXFLAGS="$CXXFLAGS -Wno-error=missing-include-dirs"
export FCFLAGS="$FCFLAGS -Wno-error=missing-include-dirs"

LD=ld \
%configure \
    --enable-shared \
    --enable-threads=posix \
    --enable-__cxa_atexit \
    --enable-clocale=gnu \
    --enable-languages=c,c++,fortran \
    --disable-multilib \
    --disable-bootstrap \
    --enable-linker-build-id \
    --enable-plugin \
    --enable-default-pie \
    --enable-default-ssp \
    --disable-fixincludes \
    --disable-libsanitizer \
    --with-system-zlib
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_libdir}
ln -sv %{_bindir}/cpp %{buildroot}/%{_libdir}
ln -sv gcc %{buildroot}%{_bindir}/cc
install -vdm 755 %{buildroot}%{_datarootdir}/gdb/auto-load%{_libdir}
mv -v %{buildroot}%{_lib64dir}/*gdb.py %{buildroot}%{_datarootdir}/gdb/auto-load%{_libdir}
chmod 755 %{buildroot}/%{_lib64dir}/libgcc_s.so.1

# Install libbacktrace-static components
mv host-%{_host}/libbacktrace/.libs/libbacktrace.a %{buildroot}%{_lib64dir}
mv libbacktrace/backtrace.h %{buildroot}%{_includedir}

rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

%check
ulimit -s 32768
# disable PCH tests is ASLR is on (due to bug in pch)
test `cat /proc/sys/kernel/randomize_va_space` -ne 0 && rm gcc/testsuite/gcc.dg/pch/pch.exp
# disable security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
# run only gcc tests
tests_ok=true
make %{?_smp_mflags} check-gcc || tests_ok=false
# Only 1 FAIL is OK
[ `grep ^FAIL testsuite/gcc/gcc.sum | wc -l` -ne 1 -o `grep ^XPASS testsuite/gcc/gcc.sum | wc -l` -ne 0 ] && tests_ok=false
[ `grep "^FAIL: gcc.dg/cpp/trad/include.c (test for excess errors)" testsuite/gcc/gcc.sum | wc -l` -ne 1 ] && tests_ok=false
$tests_ok

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_libdir}/cpp
# Executables
%exclude %{_bindir}/*gfortran
%exclude %{_bindir}/*c++
%exclude %{_bindir}/*g++
%{_bindir}/*
# Libraries
%{_lib64dir}/*
%exclude %{_libexecdir}/gcc/%{_arch}-%{_host_vendor}-linux-gnu/%{version}/f951
%exclude %{_libexecdir}/gcc/%{_arch}-%{_host_vendor}-linux-gnu/%{version}/cc1plus
%{_libdir}/gcc/*
# Library executables
%{_libexecdir}/gcc/*
# Man pages
%{_mandir}/man1/gcov.1.gz
%{_mandir}/man1/gcov-dump.1.gz
%{_mandir}/man1/gcov-tool.1.gz
%{_mandir}/man1/gcc.1.gz
%{_mandir}/man1/g++.1.gz
%{_mandir}/man1/cpp.1.gz
%{_mandir}/man1/lto-dump.1.gz
%{_mandir}/man7/*.gz
%{_datadir}/gdb/*

%exclude %{_lib64dir}/libbacktrace*
%exclude %{_lib64dir}/libgcc*
%exclude %{_lib64dir}/libgomp*
%exclude %{_lib64dir}/libstdc++*
%exclude %{_lib64dir}/libsupc++*

%files -n gfortran
%defattr(-,root,root)
%{_bindir}/*gfortran
%{_mandir}/man1/gfortran.1.gz
%{_libexecdir}/gcc/%{_arch}-%{_host_vendor}-linux-gnu/%{version}/f951

%files -n libbacktrace-static
%defattr(-,root,root)
%{_includedir}/backtrace.h
%{_lib64dir}/libbacktrace.a

%files -n libgcc
%defattr(-,root,root)
%{_lib64dir}/libgcc_s.so.*

%files -n libgcc-atomic
%defattr(-,root,root)
%{_lib64dir}/libatomic.so*

%files -n libgcc-devel
%defattr(-,root,root)
%{_lib64dir}/libgcc_s.so
%{_libdir}/libcc1.*

%files c++
%defattr(-,root,root)
%{_bindir}/*c++
%{_bindir}/*g++
%{_libexecdir}/gcc/%{_arch}-%{_host_vendor}-linux-gnu/%{version}/cc1plus

%files -n libstdc++
%defattr(-,root,root)
%{_lib64dir}/libstdc++.so.*
%dir %{_datarootdir}/gcc-%{version}/python/libstdcxx
%{_datarootdir}/gcc-%{version}/python/libstdcxx/*

%files -n libstdc++-devel
%defattr(-,root,root)
%{_lib64dir}/libstdc++.so
%{_lib64dir}/libstdc++.la
%{_lib64dir}/libstdc++.a
%{_lib64dir}/libstdc++fs.a
%{_lib64dir}/libsupc++.a
%{_lib64dir}/libsupc++.la

%{_includedir}/c++/*

%files -n libgomp
%defattr(-,root,root)
%{_lib64dir}/libgomp*.so.*

%files -n libgomp-devel
%defattr(-,root,root)
%{_lib64dir}/libgomp.a
%{_lib64dir}/libgomp.la
%{_lib64dir}/libgomp.so
%{_lib64dir}/libgomp.spec

%changelog
* Thu Nov 02 2023 Andrew Phelps <anphel@microsoft.com> - 13.2.0-1
- Upgrade to version 13.2.0
- Remove gfortran

* Tue Sep 26 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 11.2.0-7
- Removing 'exit' calls from the '%%check' section.

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 11.2.0-6
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Sep 13 2023 Andrew Phelps <anphel@microsoft.com> - 11.2.0-5
- Add CVE-2023-4039.patch

* Fri Dec 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 11.2.0-4
- Removing libbacktrace.a from the default package.

* Thu Dec 08 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 11.2.0-3
- Adding static components for "libbacktrace".

* Tue Jan 25 2022 Olivia Crain <oliviacrain@microsoft.com> - 11.2.0-2
- Add provides for libasan, liblsan, libtsan, and libubsan (and their static counterparts) to the main package
- Remove CVE-2019-15847 nopatch file (not relevant to our version of GCC)

* Mon Oct 18 2021 Andrew Phelps <anphel@microsoft.com> - 11.2.0-1
- Update to version 11.2.0

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 9.1.0-11
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Fri Jan 08 2021 Ruying Chen <v-ruyche@microsoft.com> - 9.1.0-10
- Provide libquadmath and libquadmath-devel.

* Tue Nov 03 2020 Joe Schmitt <joschmit@microsoft.com> - 9.1.0-9
- Provide gcc-plugin-devel.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 9.1.0-8
- Split gcc-c++ subpackage.
- Provide cpp, gcc-gfortran, libatomic, and listdc++-static.

* Thu Sep 10 2020 Olivia Crain <oliviacrain@microsoft.com> - 9.1.0-7
- Ignore CVE-2019-15847, as it applies to an unsupported ISA

* Mon Jul 06 2020 Henry Beberman <henry.beberman@microsoft.com> - 9.1.0-6
- Comment out with_check BuildRequires to break circular dependency in build graph.

* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> - 9.1.0-5
- Disable -Werror=format-security to build with hardened cflags

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 9.1.0-4
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 9.1.0-3
- Renaming mpc to libmpc

* Thu Apr 09 2020 Emre Girgin <mrgirgin@microsoft.com> - 9.1.0-2
- Add the "--enable-default-pie" flag in order to enforce ASLR-enabled binaries.

* Tue Mar 17 2020 Andrew Phelps <anphel@microsoft.com> - 9.1.0-1
- Update to version 9.1.0. License verified. Add libstdc++fs.a

* Tue Jan 21 2020 Andrew Phelps <anphel@microsoft.com> - 7.3.0-6
- Fixing build issues for multiple architectures

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 7.3.0-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Nov 02 2018 Alexey Makhalov <amakhalov@vmware.com> - 7.3.0-4
- Use nofortify security_hardening instead of sed hacking
- Use %configure

* Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> - 7.3.0-3
- Fix compilation issue for glibc-2.28

* Thu Aug 30 2018 Keerthana K <keerthanak@vmware.com> - 7.3.0-2
- Packaging .a files (libstdc++-static files).

* Wed Aug 01 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 7.3.0-1
- Update to version 7.3.0 to get retpoline support.

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.3.0-7
- Aarch64 support

* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.3.0-6
- Added smp_mflags for parallel build

* Mon Sep 25 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.3.0-5
- Enable elfdeps for libgcc_s to generate libgcc_s.so.1(*)(64bit) provides

* Mon Aug 28 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.3.0-4
- Fix makecheck

* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.3.0-3
- Fix compilation issue for glibc-2.26

* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.3.0-2
- Improve make check

* Thu Mar 9 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.3.0-1
- Update version to 6.3

* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.3.0-6
- Enabled fortran.

* Wed Feb 22 2017 Alexey Makhalov <amakhalov@vmware.com> - 5.3.0-5
- Added new plugin entry point: PLUGIN_TYPE_CAST (.patch)

* Thu Sep  8 2016 Alexey Makhalov <amakhalov@vmware.com> - 5.3.0-4
- Enable plugins and linker build id.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 5.3.0-3
- GA - Bump release of all rpms

* Tue May 17 2016 Anish Swaminathan <anishs@vmware.com> - 5.3.0-2
- Change package dependencies

* Mon Mar 28 2016 Alexey Makhalov <amakhalov@vmware.com> - 5.3.0-1
- Update version to 5.3

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> - 4.8.2-6
- Handled locale files with macro find_lang

* Mon Nov 02 2015 Vinay Kulkarni <kulkarniv@vmware.com> - 4.8.2-5
- Put libatomic.so into its own package.

* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> - 4.8.2-4
- Updated group.

* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> - 4.8.2-3
- Update according to UsrMove.

* Fri May 15 2015 Divya Thaluru <dthaluru@vmware.com> - 4.8.2-2
- Packaging .la files

* Tue Apr 01 2014 baho-utot <baho-utot@columbus.rr.com> - 4.8.2-1
- Initial build. First version
