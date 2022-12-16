%global security_hardening nofortify
%global debug_package %{nil}
%global set_build_flags %{nil}
%define __os_install_post %{nil}
%global _unpackaged_files_terminate_build 0

# Globals which should be in a macro file.
# These should be set programatically in the future.
%global _host_arch      x86_64
%global _target_arch    aarch64

%global _tuple          %{_target_arch}-%{_vendor}-linux-gnu
%global _cross_name     %{_target_arch}-%{_vendor}-linux-gnu

# Folders which should be in our macro file
%global _opt                /opt/
%global _crossdir           /opt/cross/

# Generally we include '/usr' in most paths.
# Can we also use '/usr' for our paths? This will bring us in line with the
# %%configure macro which sets these.
%global _bindir            /bin
%global _sbindir           /sbin
%global _libdir            /lib
%global _lib64dir          /lib64
%global _libexecdir        /libexec
%global _datadir           /share
%global _docdir            /share/doc
%global _includedir        /include
%global _infodir           /share/info
%global _mandir            /share/man
%global _oldincludedir     /include

# If we want our cross compile aware packges to also support native, we
# need logic to switch modes something like this:
%if "%{_target_arch}" != "%{_host_arch}"
%global _cross_prefix       %{_crossdir}%{_tuple}/
%global _cross_sysroot      %{_crossdir}%{_tuple}/sysroot/
%global _cross_includedir   /usr/%{_host}/%{_tuple}/include/
%global _cross_infodir      %{_crossdir}%{_tuple}/share/info
%global _cross_bindir       %{_tuple}/bin
%global _cross_libdir       %{_tuple}/lib
%global _tuple_name         %{_tuple}-

%global __strip %{_cross_prefix}%{_bindir}/%{_tuple_name}strip
%global __objdump %{_cross_prefix}%{_bindir}/%{_tuple_name}objdump
%else
%global _cross_prefix       %{nil}
%global _cross_sysroot      %{nil}
%global _cross_includedir   %{_includedir}
%global _cross_infodir      %{_infodir}
%global _cross_bindir       %{_bindir}
%global _cross_libdir       %{_libdir}
%global _tuple_name         %{nil}
%endif

Summary:        Contains the GNU compiler collection
Name:           %{_cross_name}-gcc-bootstrap3
Version:        11.2.0
Release:        2%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://gcc.gnu.org/
Source0:        https://ftp.gnu.org/gnu/gcc/%{name}-%{version}/gcc-%{version}.tar.xz
Source1:        https://ftp.gnu.org/gnu/mpfr/mpfr-4.1.0.tar.xz
Source2:        http://ftp.gnu.org/gnu/gmp/gmp-6.2.1.tar.xz
Source3:        https://ftp.gnu.org/gnu/mpc/mpc-1.2.1.tar.gz

BuildRequires:  %{_cross_name}-binutils
BuildRequires:  %{_cross_name}-kernel-headers
BuildRequires:  %{_cross_name}-glibc-bootstrap2
AutoReqProv:    no
ExclusiveArch:  x86_64
Conflicts:      %{_cross_name}-cross-gcc
Conflicts:      %{_cross_name}-gcc-bootstrap
Conflicts:      %{_cross_name}-gcc-bootstrap2
#%%if %%{with_check}
#BuildRequires:  autogen
#BuildRequires:  dejagnu
#%%endif

#Merge all of the packages for the bootstrap packages
# (Only gfortran, c++ sub packages are built for bootstrap 1)

%description
The GCC package contains the GNU compiler collection,
which includes the C and C++ compilers.

# %%package -n     gfortran
# Summary:        GNU Fortran compiler.
# Group:          Development/Tools
# Requires:       %%{_cross_name}-gcc = %%{version}-%%{release}
# Provides:       %%{_cross_name}-gcc-gfortran = %%{version}-%%{release}

# %%description -n gfortran
# The gfortran package contains GNU Fortran compiler.

# %%package -n     libgcc
# Summary:        GNU C Library
# Group:          System Environment/Libraries

# %%description -n libgcc
# The libgcc package contains GCC shared libraries for gcc.

# %%package -n     libgcc-atomic
# Summary:        GNU C Library for atomic counter updates
# Group:          System Environment/Libraries
# Requires:       %%{_cross_name}-libgcc = %%{version}-%%{release}
# Provides:       %%{_cross_name}-libatomic = %%{version}-%%{release}

# %%description -n libgcc-atomic
# The libgcc package contains GCC shared libraries for atomic counter updates.

# %%package -n     libgcc-devel
# Summary:        GNU C Library
# Group:          Development/Libraries
# Requires:       %%{_cross_name}-libgcc = %%{version}-%%{release}

# %%description -n libgcc-devel
# The libgcc package contains GCC shared libraries for gcc .
# This package contains development headers and static library for libgcc.

# %%package        c++
# Summary:        C++ support for GCC
# Group:          System Environment/Libraries
# Requires:       %%{_cross_name}-gcc = %%{version}-%%{release}
# Requires:       %%{_cross_name}-libstdc++-devel = %%{version}-%%{release}
# Provides:       %%{_cross_name}-gcc-g++ = %%{version}-%%{release}
# Provides:       %%{_cross_name}-g++ = %%{version}-%%{release}

# %%description    c++
# This package adds C++ support to the GNU Compiler Collection.
# It includes support for most of the current C++ specification,
# including templates and exception handling.

# %%package -n     libstdc++
# Summary:        GNU C Library
# Group:          System Environment/Libraries
# Requires:       %%{_cross_name}-libgcc = %%{version}-%%{release}

# %%description -n libstdc++
# This package contains the GCC Standard C++ Library v3, an ongoing project to implement the ISO/IEC 14882:1998 Standard C++ library.

# %%package -n     libstdc++-devel
# Summary:        GNU C Library
# Group:          Development/Libraries
# Requires:       %%{_cross_name}-libstdc++ = %%{version}-%%{release}
# Provides:       %%{_cross_name}-libstdc++-static = %%{version}-%%{release}

# %%description -n libstdc++-devel
# This is the GNU implementation of the standard C++ libraries.
# This package includes the headers files and libraries needed for C++ development.

# %%package -n     libgomp
# Summary:        GNU C Library
# Group:          System Environment/Libraries

# %%description -n libgomp
# An implementation of OpenMP for the C, C++, and Fortran 95 compilers in the GNU Compiler Collection.

# %%package -n     libgomp-devel
# Summary:        Development headers and static library for libgomp
# Group:          Development/Libraries
# Requires:       %%{_cross_name}-libgomp = %%{version}-%%{release}

# %%description -n libgomp-devel
# An implementation of OpenMP for the C, C++, and Fortran 95 compilers in the GNU Compiler Collection.
# This package contains development headers and static library for libgomp

%prep
%setup -q -n gcc-%{version}
# disable no-pie for gcc binaries
sed -i '/^NO_PIE_CFLAGS = /s/@NO_PIE_CFLAGS@//' gcc/Makefile.in

install -vdm 755 %{_builddir}/%{name}-build
cd %{_builddir}
tar -xf %{SOURCE1}
ln -s mpfr-4.1.0 gcc-%{version}/mpfr
tar -xf %{SOURCE2}
ln -s gmp-6.2.1 gcc-%{version}/gmp
tar -xf %{SOURCE3}
ln -s mpc-1.2.1 gcc-%{version}/mpc

cp mpfr-4.1.0/COPYING gcc-%{version}/COPYING-mpfr
cp gmp-6.2.1/COPYING gcc-%{version}/COPYING-gmp
cp mpc-1.2.1/COPYING.LESSER gcc-%{version}/COPYING.LESSER-mpc

%build
# What flags do we want here? Clearing with '%%global set_build_flags %%{nil}' at start of file.
# #CFLAGS="`echo " %%{build_cflags} " | sed 's/-Werror=format-security/-Wno-error=format-security/'`"
# #CXXFLAGS="`echo " %%{build_cxxflags} " | sed 's/-Werror=format-security/-Wno-error=format-security/'`"

#export glibcxx_cv_c99_math_cxx98=yes glibcxx_cv_c99_math_cxx11=yes
#SED=sed \

TEMP_SYSROOT="%{_builddir}/temp_sysroot/"
cp -r "%{_cross_sysroot}" "$TEMP_SYSROOT"
# This should reference our %%{_includedir} probably? Why the missmatch between /include and /usr/include?
mkdir -p "$TEMP_SYSROOT/usr"
ln -s "../include" "$TEMP_SYSROOT/usr/include"

# Ideally we would like to model this after the %%configure macro in the future.
cd %{_builddir}/%{name}-build
../gcc-%{version}/configure \
            --cache-file=/dev/null \
            --prefix=%{_cross_prefix} \
            --target=%{_tuple} \
            --disable-multilib \
            --enable-shared \
            --enable-threads=posix \
            --enable-__cxa_atexit \
            --enable-clocale=gnu \
            --enable-languages=c,c++,fortran \
            --disable-bootstrap \
            --enable-linker-build-id \
            --enable-plugin \
            --enable-default-pie \
            --with-sysroot=%{_cross_sysroot} \
            --with-build-sysroot="$TEMP_SYSROOT"

make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-build
make %{?_smp_mflags} DESTDIR=%{buildroot} install

find %{buildroot} -name '*.la' -delete
rm -rf %{buildroot}%{_cross_prefix}%{_infodir}
cd ../gcc-%{version}
%find_lang %{name} --all-name

# Turning off so we don't get ldconfig errors for crossarch packages
# Add the /opt/cross libs to the ldcache
# mkdir -p %%{buildroot}%%{_sysconfdir}/ld.so.conf.d/
# echo %%{buildroot}%%{_sysconfdir}/ld.so.conf.d/%%{name}.conf
# cat > %%{buildroot}%%{_sysconfdir}/ld.so.conf.d/%%{name}.conf <<EOF
# %%{_cross_prefix}%%{_tuple}%%{_lib64dir}
# EOF
# cat %%{buildroot}%%{_sysconfdir}/ld.so.conf.d/%%{name}.conf

# %%post   -p /sbin/ldconfig
# %%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%license COPYING-mpfr
%license COPYING-gmp
%license COPYING.LESSER-mpc
%exclude /opt/cross/aarch64-mariner-linux-gnu/share/man/man1/aarch64-mariner-linux-gnu-lto-dump.1
#%%{_sysconfdir}/ld.so.conf.d/%%{name}.conf
#%%{_lib}/cpp
# Executables
#%%exclude %%{_cross_prefix}%%{_bindir}/*gfortran
#%%exclude %%{_cross_prefix}%%{_bindir}/*c++
#%%exclude %%{_cross_prefix}%%{_bindir}/*g++
%{_cross_prefix}%{_bindir}/*
# Libraries
%{_cross_prefix}%{_tuple}%{_lib64dir}/*
#%%exclude %%{_cross_prefix}%%{_libexecdir}/gcc/%%{_tuple}/%%{version}/f951
#%%exclude %%{_cross_prefix}%%{_libexecdir}/gcc/%%{_tuple}/%%{version}/cc1plus
%{_cross_prefix}%{_libdir}/gcc/*
# Library executables
%{_cross_prefix}%{_libexecdir}/gcc/*
# Man pages
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}gcov.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}gcov-dump.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}gcov-tool.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}gcc.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}g++.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}cpp.1
%{_cross_prefix}%{_mandir}/man7/*
#%%{_cross_prefix}%%{_datadir}/gdb/*

#%%exclude %%{_cross_prefix}%%{_lib64dir}/libgcc*
#%%exclude %%{_cross_prefix}%%{_lib64dir}/libstdc++*
#%%exclude %%{_cross_prefix}%%{_lib64dir}/libsupc++*
#%%exclude %%{_cross_prefix}%%{_lib64dir}/libgomp*

# %%files -n gfortran
# %%defattr(-,root,root)
#%%{_cross_prefix}%%{_bindir}/*gfortran
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}gfortran.1
#%%{_cross_prefix}%%{_libexecdir}/gcc/%%{_tuple}/%%{version}/f951

# %%files -n libgcc
# %%defattr(-,root,root)
# %%{_cross_prefix}%%{_tuple}%%{_lib64dir}/libgcc_s.so.*

# %%files -n libgcc-atomic
# %%defattr(-,root,root)
# %%{_cross_prefix}%%{_lib64dir}/libatomic.so*

# %%files -n libgcc-devel
# %%defattr(-,root,root)
# %%{_cross_prefix}%%{_tuple}%%{_lib64dir}/libgcc_s.so
 %{_cross_prefix}%{_lib64dir}/libcc1.*

# %%files c++
# %%defattr(-,root,root)
#%%{_cross_prefix}%%{_bindir}/*c++
#%%{_cross_prefix}%%{_bindir}/*g++
#%%{_cross_prefix}%%{_libexecdir}/gcc/%%{_tuple}/%%{version}/cc1plus

# %%files -n libstdc++
# %%defattr(-,root,root)
# %%{_cross_prefix}%%{_lib64dir}/libstdc++.so.*
# # Switched these from _datarootdir to _datadir
 %dir %{_cross_prefix}%{_datadir}/gcc-%{version}/python/libstdcxx
 %{_cross_prefix}%{_datadir}/gcc-%{version}/python/libstdcxx/*

# %%files -n libstdc++-devel
# %%defattr(-,root,root)
# %%{_cross_prefix}%%{_lib64dir}/libstdc++.so
# %%{_cross_prefix}%%{_lib64dir}/libstdc++.la
# %%{_cross_prefix}%%{_lib64dir}/libstdc++.a
# %%{_cross_prefix}%%{_lib64dir}/libstdc++fs.a
# %%{_cross_prefix}%%{_lib64dir}/libsupc++.a
# %%{_cross_prefix}%%{_lib64dir}/libsupc++.la

 %{_cross_prefix}/%{_tuple}/%{_includedir}/c++/*

# %%files -n libgomp
# %%defattr(-,root,root)
# %%{_cross_prefix}%%{_lib64dir}/libgomp*.so.*

# %%files -n libgomp-devel
# %%defattr(-,root,root)
# %%{_cross_prefix}%%{_lib64dir}/libgomp.a
# %%{_cross_prefix}%%{_lib64dir}/libgomp.la
# %%{_cross_prefix}%%{_lib64dir}/libgomp.so
# %%{_cross_prefix}%%{_lib64dir}/libgomp.spec

%changelog
* Thu Dec 15 2022 Dallas Delaney <dadelan@microsoft.com> - 11.2.0-2
- Update to 11.2.0-2

* Fri Feb 12 2021 Daniel McIlvaney <damcilva@microsoft.com> - 9.1.0-11
- Fork normal gcc package into cross compile aware boot strap package

* Fri Jan 08 2021 Ruying Chen <v-ruyche@microsoft.com> - 9.1.0-10
- Provide libquadmath and libquadmath-devel.

* Tue Nov 03 2020 Joe Schmitt <joschmit@microsoft.com> - 9.1.0-9
- Provide gcc-plugin-devel.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 9.1.0-8
- Split gcc-c++ subpackage.
- Provide cpp, gcc-gfortran, libatomic, and listdc++-static.

* Thu Sep 10 2020 Thomas Crain <thcrain@microsoft.com> - 9.1.0-7
- Ignore CVE-2019-15847, as it applies to an unsupported ISA

* Mon Jul 06 2020 Henry Beberman <henry.beberman@microsoft.com> - 9.1.0-6
- Comment out with_check BuildRequires to break circular dependency in build graph.

* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> - 9.1.0-5
- Disable -Werror=format-security to build with hardened cflags

* Sat May 09 00:21:12 PST 2020 Nick Samson <nisamson@microsoft.com> - 9.1.0-4
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
