%global toolchain clang

# Opt out of https://fedoraproject.org/wiki/Changes/fno-omit-frame-pointer
# https://bugzilla.redhat.com/show_bug.cgi?id=2158587
%undefine _include_frame_pointers

%global maj_ver 18
%global libcxx_version %{maj_ver}.1.2
%global libcxx_srcdir libcxx-%{libcxx_version}
%global libcxxabi_srcdir libcxxabi-%{libcxx_version}
%global libunwind_srcdir libunwind-%{libcxx_version}

Name:		libcxx
Version:	%{libcxx_version}
Release:	1%{?dist}
Summary:	C++ standard library targeting C++11
License:	Apache-2.0 WITH LLVM-exception OR MIT OR NCSA
URL:		http://libcxx.llvm.org/
Source0:    https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-%{version}.tar.gz

BuildRequires:  clang
BuildRequires:  llvm-devel 
#BuildRequires:  llvm-cmake-utils 
BuildRequires:  cmake
BuildRequires:  ninja-build

Requires: libcxxabi%{?_isa} = %{version}-%{release}

%description
libc++ is a new implementation of the C++ standard library, targeting C++11.

%package devel
Summary:	Headers and libraries for libcxx devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libcxxabi-devel

%description devel
%{summary}.

%package static
Summary:	Static libraries for libcxx

%description static
%{summary}.

%package -n libcxxabi
Summary:	Low level support for a standard C++ library

%description -n libcxxabi
libcxxabi provides low level support for a standard C++ library.

%package -n libcxxabi-devel
Summary:	Headers and libraries for libcxxabi devel
Requires:	libcxxabi%{?_isa} = %{version}-%{release}

%description -n libcxxabi-devel
%{summary}.

%package -n libcxxabi-static
Summary:	Static libraries for libcxxabi

%description -n libcxxabi-static
%{summary}.

%package -n llvm-libunwind
Summary:    LLVM libunwind

%description -n llvm-libunwind

LLVM libunwind is an implementation of the interface defined by the HP libunwind
project. It was contributed Apple as a way to enable clang++ to port to
platforms that do not have a system unwinder. It is intended to be a small and
fast implementation of the ABI, leaving off some features of HP's libunwind
that never materialized (e.g. remote unwinding).

%package -n llvm-libunwind-devel
Summary:    LLVM libunwind development files
Provides:   libunwind(major) = %{maj_ver}
Requires:   llvm-libunwind%{?_isa} = %{version}-%{release}

%description -n llvm-libunwind-devel
Unversioned shared library for LLVM libunwind

%package -n llvm-libunwind-static
Summary: Static library for LLVM libunwind

%description -n llvm-libunwind-static
%{summary}.

%package -n llvm-libunwind-doc
Summary:    libunwind documentation
# jquery.js and langage_data.js are used in the HTML doc and under BSD License
License:    BSD AND (Apache-2.0 WITH LLVM-exception OR NCSA OR MIT)

%description -n llvm-libunwind-doc
Documentation for LLVM libunwind

%prep
%autosetup -p1 -n llvm-project-llvmorg-%{version}

%build
mkdir -p build
cd build
cmake \
    -G Ninja \
    -S ../runtimes \
    -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_MODULE_PATH="%{_libdir}/cmake/llvm;%{_datadir}/llvm/cmake/Modules" \
	-DCMAKE_POSITION_INDEPENDENT_CODE=ON \
	-DLIBCXX_STATICALLY_LINK_ABI_IN_STATIC_LIBRARY=ON \
	-DLIBCXX_INCLUDE_BENCHMARKS=OFF \
	-DLIBCXX_ENABLE_ABI_LINKER_SCRIPT=ON \
	-DLIBUNWIND_INSTALL_INCLUDE_DIR=%{_includedir}/llvm-libunwind \
    -DCXX_SUPPORTS_NOSTDLIBXX_FLAG=OFF

#	-DLIBCXX_LIBDIR_SUFFIX:STRING=64 \
#	-DLIBCXXABI_LIBDIR_SUFFIX:STRING=64 \
#	-DLIBUNWIND_LIBDIR_SUFFIX:STRING=64 \

%ninja_build cxx
%ninja_build

%install
cd build
%ninja_install

# We can't install the unversionned path on default location because that would conflict with
# https://src.fedoraproject.org/rpms/libunwind
#
# The versionned path has a different soname (libunwind.so.1 compared to
# libunwind.so.8) so they can live together in %%{_libdir}
#
# ABI wise, even though llvm-libunwind's library is named libunwind, it doesn't
# have the exact same ABI as gcc's libunwind (it actually provides a subset).
rm %{buildroot}%{_libdir}/libunwind.so
mkdir -p %{buildroot}/%{_libdir}/llvm-unwind/

pushd %{buildroot}/%{_libdir}/llvm-unwind
ln -s ../libunwind.so.1.0 libunwind.so
popd

#rm %{buildroot}%{_pkgdocdir}/html/.buildinfo

%ldconfig_scriptlets

%files
%license libcxx/LICENSE.TXT
%doc libcxx/CREDITS.TXT libcxx/TODO.TXT
%{_libdir}/libc++.so.*

%files devel
%{_includedir}/c++/
%exclude %{_includedir}/c++/v1/cxxabi.h
%exclude %{_includedir}/c++/v1/__cxxabi_config.h
%{_libdir}/libc++.so

%files static
%license libcxx/LICENSE.TXT
%{_libdir}/libc++.a
%{_libdir}/libc++experimental.a

%files -n libcxxabi
%license libcxxabi/LICENSE.TXT
%doc libcxxabi/CREDITS.TXT
%{_libdir}/libc++abi.so.*

%files -n libcxxabi-devel
%{_includedir}/c++/v1/cxxabi.h
%{_includedir}/c++/v1/__cxxabi_config.h
%{_libdir}/libc++abi.so

%files -n libcxxabi-static
%{_libdir}/libc++abi.a

%files -n llvm-libunwind
%license libunwind/LICENSE.TXT
%{_libdir}/libunwind.so.1
%{_libdir}/libunwind.so.1.0

%files -n llvm-libunwind-devel
%{_includedir}/llvm-libunwind/__libunwind_config.h
%{_includedir}/llvm-libunwind/libunwind.h
%{_includedir}/llvm-libunwind/libunwind.modulemap
%{_includedir}/llvm-libunwind/mach-o/compact_unwind_encoding.h
%{_includedir}/llvm-libunwind/mach-o/compact_unwind_encoding.modulemap
%{_includedir}/llvm-libunwind/unwind.h
%{_includedir}/llvm-libunwind/unwind_arm_ehabi.h
%{_includedir}/llvm-libunwind/unwind_itanium.h
%dir %{_libdir}/llvm-unwind
%{_libdir}/llvm-unwind/libunwind.so

%files -n llvm-libunwind-static
%{_libdir}/libunwind.a

%files -n llvm-libunwind-doc
%license libunwind/LICENSE.TXT
#%%doc %{_pkgdocdir}/html

%changelog
* Tue May 21 2024 Tom Stellard <tstellar@redhat.com> - 18.1.6-1
- 18.1.6 Release

* Fri May 03 2024 Tom Stellard <tstellar@redhat.com> - 18.1.4-1
- 18.1.4 Release

* Wed Apr 17 2024 Tom Stellard <tstellar@redhat.com> - 18.1.3-1
- 18.1.3 Release

* Fri Mar 22 2024 Tom Stellard <tstellar@redhat.com> - 18.1.2-1
- 18.1.2 Release

* Wed Mar 13 2024 Tom Stellard <tstellar@redhat.com> - 18.1.1-1
- 18.1.1 Release

* Mon Mar 04 2024 Nikita Popov <npopov@redhat.com> - 18.1.0~rc4-2
- Disable LIBCXXABI_USE_LLVM_UNWINDER (rhbz#2267690)

* Thu Feb 29 2024 Tom Stellard <tstellar@redhat.com> - 18.1.0~rc4-1
- 18.1.0-rc4 Release

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 17.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
