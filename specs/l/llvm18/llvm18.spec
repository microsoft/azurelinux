# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with snapshot_build

%if %{with snapshot_build}
# Unlock LLVM Snapshot LUA functions
%{llvm_sb}
%endif

# We are building with clang for faster/lower memory LTO builds.
# See https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_macros
%global toolchain clang

# Opt out of https://fedoraproject.org/wiki/Changes/fno-omit-frame-pointer
# https://bugzilla.redhat.com/show_bug.cgi?id=2158587
%undefine _include_frame_pointers

# Components enabled if supported by target architecture:
%define gold_arches %{ix86} x86_64 aarch64 %{power64} s390x
%ifarch %{gold_arches}
  %bcond_without gold
%else
  %bcond_with gold
%endif

%bcond_without compat_build
%bcond_without check

%ifarch %ix86 riscv64
# Disable LTO on x86 in order to reduce memory consumption
%bcond_with lto_build
%elif %{with snapshot_build}
# Disable LTO to speed up builds
%bcond_with lto_build
%else
%bcond_without lto_build
%endif

%global maj_ver 18
%global min_ver 1
%global patch_ver 8
#global rc_ver 4

%if %{with snapshot_build}
%undefine rc_ver
%global maj_ver %{llvm_snapshot_version_major}
%global min_ver %{llvm_snapshot_version_minor}
%global patch_ver %{llvm_snapshot_version_patch}
%endif

%global llvm_srcdir llvm-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:rc%{rc_ver}}.src
%global cmake_srcdir cmake-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:rc%{rc_ver}}.src
%global third_party_srcdir third-party-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:rc%{rc_ver}}.src

%if %{with compat_build}
%global pkg_name llvm%{maj_ver}
%global exec_suffix -%{maj_ver}
%global install_prefix %{_libdir}/%{name}
%global install_bindir %{install_prefix}/bin
%global install_includedir %{install_prefix}/include
%global install_libdir %{install_prefix}/lib

%global pkg_includedir %{_includedir}/%{name}
%global pkg_datadir %{install_prefix}/share
%else
%global pkg_name llvm
%global install_prefix /usr
%global install_bindir %{_bindir}
%global install_libdir %{_libdir}
%global install_includedir %{_includedir}
%global pkg_datadir %{_datadir}
%global exec_suffix %{nil}
%endif

%if 0%{?rhel}
%global targets_to_build "X86;AMDGPU;PowerPC;NVPTX;SystemZ;AArch64;ARM;Mips;BPF;WebAssembly"
%global experimental_targets_to_build ""
%else
%global targets_to_build "all"
%global experimental_targets_to_build "AVR"
%endif

%global build_install_prefix %{buildroot}%{install_prefix}

# Lower memory usage of dwz on s390x
%global _dwz_low_mem_die_limit_s390x 1
%global _dwz_max_die_limit_s390x 1000000

%global llvm_triple %{_target_platform}

# https://fedoraproject.org/wiki/Changes/PythonSafePath#Opting_out
# Don't add -P to Python shebangs
# The executable Python scripts in /usr/share/opt-viewer/ import each other
%undefine _py3_shebang_P

Name:		%{pkg_name}
Version:	%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:~rc%{rc_ver}}%{?llvm_snapshot_version_suffix:~%{llvm_snapshot_version_suffix}}
Release: 8%{?dist}
Summary:	The Low Level Virtual Machine

License:	Apache-2.0 WITH LLVM-exception OR NCSA
URL:		http://llvm.org
%if %{with snapshot_build}
Source0:	%{llvm_snapshot_source_prefix}llvm-%{llvm_snapshot_yyyymmdd}.src.tar.xz
Source2:	%{llvm_snapshot_source_prefix}cmake-%{llvm_snapshot_yyyymmdd}.src.tar.xz
Source4:	%{llvm_snapshot_source_prefix}third-party-%{llvm_snapshot_yyyymmdd}.src.tar.xz
%{llvm_snapshot_extra_source_tags}
%else
Source0:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:-rc%{rc_ver}}/%{llvm_srcdir}.tar.xz
Source1:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:-rc%{rc_ver}}/%{llvm_srcdir}.tar.xz.sig
Source2:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:-rc%{rc_ver}}/%{cmake_srcdir}.tar.xz
Source3:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:-rc%{rc_ver}}/%{cmake_srcdir}.tar.xz.sig
Source4:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:-rc%{rc_ver}}/%{third_party_srcdir}.tar.xz
Source5:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:-rc%{rc_ver}}/%{third_party_srcdir}.tar.xz.sig
Source6:	release-keys.asc
%endif

Patch0: cstdint.patch

# RHEL-specific patch to avoid unwanted python3-myst-parser dep
Patch101:	0101-Deactivate-markdown-doc.patch

# https://github.com/llvm/llvm-project/pull/96959
Patch201: 	0001-llvm_gtest-Only-install-once.patch

BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	ninja-build
BuildRequires:	zlib-devel
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	python3-psutil
BuildRequires:	python3-sphinx
%if %{undefined rhel}
BuildRequires:	python3-myst-parser
%endif
BuildRequires:	multilib-rpm-config
%if %{with gold}
BuildRequires:	binutils-devel
%endif
%ifarch %{valgrind_arches}
# Enable extra functionality when run the LLVM JIT under valgrind.
BuildRequires:	valgrind-devel
%endif
# LLVM's LineEditor library will use libedit if it is available.
BuildRequires:	libedit-devel
# We need python3-devel for %%py3_shebang_fix
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools

# For origin certification
BuildRequires:	gnupg2


Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

Provides:	llvm(major) = %{maj_ver}

%description
LLVM is a compiler infrastructure designed for compile-time, link-time,
runtime, and idle-time optimization of programs from arbitrary programming
languages. The compiler infrastructure includes mirror sets of programming
tools as well as libraries with equivalent functionality.

%package devel
Summary:	Libraries and header files for LLVM
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
# The installed LLVM cmake files will add -ledit to the linker flags for any
# app that requires the libLLVMLineEditor, so we need to make sure
# libedit-devel is available.
Requires:	libedit-devel
# The installed cmake files reference binaries from llvm-test, llvm-static, and
# llvm-gtest.  We tried in the past to split the cmake exports for these binaries
# out into separate files, so that llvm-devel would not need to Require these packages,
# but this caused bugs (rhbz#1773678) and forced us to carry two non-upstream
# patches.
Requires:	%{name}-static%{?_isa} = %{version}-%{release}
Requires:	%{name}-test%{?_isa} = %{version}-%{release}
Requires:	%{name}-googletest%{?_isa} = %{version}-%{release}


Requires(post):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

Provides:	llvm-devel(major) = %{maj_ver}

%description devel
This package contains library and header files needed to develop new native
programs that use the LLVM infrastructure.

%package doc
Summary:	Documentation for LLVM
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for the LLVM compiler infrastructure.

%package libs
Summary:	LLVM shared libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
Shared libraries for the LLVM compiler infrastructure.

%package static
Summary:	LLVM static libraries
Conflicts:	%{name}-devel < 8

Provides:	llvm-static(major) = %{maj_ver}

%description static
Static libraries for the LLVM compiler infrastructure.

%package cmake-utils
Summary: CMake utilities shared across LLVM subprojects

%description cmake-utils
CMake utilities shared across LLVM subprojects.
This is for internal use by LLVM packages only.

%package test
Summary:	LLVM regression tests
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

Provides:	llvm-test(major) = %{maj_ver}

%description test
LLVM regression tests.

%package googletest
Summary: LLVM's modified googletest sources

%description googletest
LLVM's modified googletest sources.

%prep
%{gpgverify} --keyring='%{SOURCE6}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%{gpgverify} --keyring='%{SOURCE6}' --signature='%{SOURCE3}' --data='%{SOURCE2}'
%{gpgverify} --keyring='%{SOURCE6}' --signature='%{SOURCE5}' --data='%{SOURCE4}'
%setup -T -q -b 2 -n %{cmake_srcdir}
# TODO: It would be more elegant to set -DLLVM_COMMON_CMAKE_UTILS=%{_builddir}/%{cmake_srcdir},
# but this is not a CACHED variable, so we can't actually set it externally :(
cd ..
mv %{cmake_srcdir} cmake
%setup -T -q -b 4 -n %{third_party_srcdir}
%autopatch -m 201 -M 300 -p2
cd ..
mv %{third_party_srcdir} third-party

%setup -T -q -b 0 -n %{llvm_srcdir}
%autopatch -M%{?!rhel:100}%{?rhel:200} -p2

%py3_shebang_fix \
	test/BugPoint/compile-custom.ll.py \
	tools/opt-viewer/*.py \
	utils/update_cc_test_checks.py

%build

%if %{without lto_build}
%global _lto_cflags %nil
%endif

%ifarch s390 s390x %ix86 riscv64
# Decrease debuginfo verbosity to reduce memory consumption during final library linking
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

# Copy CFLAGS into ASMFLAGS, so -fcf-protection is used when compiling assembly files.
export ASMFLAGS="%{build_cflags}"

# force off shared libs as cmake macros turns it on.
# TODO: Disable LLVM_UNREACHABLE_OPTIMIZE.
%cmake	-G Ninja \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DLLVM_PARALLEL_LINK_JOBS=1 \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_SKIP_RPATH:BOOL=ON \
%ifarch s390 %ix86 riscv64
	-DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -DNDEBUG" \
%endif
%if %{without compat_build}
%if 0%{?__isa_bits} == 64
	-DLLVM_LIBDIR_SUFFIX=64 \
%else
	-DLLVM_LIBDIR_SUFFIX= \
%endif
%endif
	\
	-DLLVM_TARGETS_TO_BUILD=%{targets_to_build} \
	-DLLVM_ENABLE_LIBCXX:BOOL=OFF \
	-DLLVM_ENABLE_ZLIB:BOOL=ON \
	-DLLVM_ENABLE_FFI:BOOL=ON \
	-DLLVM_ENABLE_RTTI:BOOL=ON \
	-DLLVM_USE_PERF:BOOL=ON \
%if %{with gold}
	-DLLVM_BINUTILS_INCDIR=%{_includedir} \
%endif
	-DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD=%{experimental_targets_to_build} \
	\
	-DLLVM_BUILD_RUNTIME:BOOL=ON \
	\
	-DLLVM_INCLUDE_TOOLS:BOOL=ON \
	-DLLVM_BUILD_TOOLS:BOOL=ON \
	\
	-DLLVM_INCLUDE_TESTS:BOOL=ON \
	-DLLVM_BUILD_TESTS:BOOL=ON \
	-DLLVM_INSTALL_GTEST:BOOL=ON \
	-DLLVM_LIT_ARGS=-v \
	\
	-DLLVM_INCLUDE_EXAMPLES:BOOL=ON \
	-DLLVM_BUILD_EXAMPLES:BOOL=OFF \
	\
	-DLLVM_INCLUDE_UTILS:BOOL=ON \
	-DLLVM_INSTALL_UTILS:BOOL=ON \
	-DLLVM_UTILS_INSTALL_DIR:PATH=bin \
	-DLLVM_TOOLS_INSTALL_DIR:PATH=bin \
	\
	-DLLVM_INCLUDE_DOCS:BOOL=ON \
	-DLLVM_BUILD_DOCS:BOOL=ON \
	-DLLVM_ENABLE_SPHINX:BOOL=ON \
	-DLLVM_ENABLE_DOXYGEN:BOOL=OFF \
	\
%if %{with snapshot_build}
	-DLLVM_VERSION_SUFFIX="%{llvm_snapshot_version_suffix}" \
%else
	-DLLVM_VERSION_SUFFIX='' \
%endif
	-DLLVM_UNREACHABLE_OPTIMIZE:BOOL=ON \
	-DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
	-DLLVM_BUILD_EXTERNAL_COMPILER_RT:BOOL=ON \
	-DLLVM_INSTALL_TOOLCHAIN_ONLY:BOOL=OFF \
	-DLLVM_DEFAULT_TARGET_TRIPLE=%{llvm_triple} \
	-DSPHINX_WARNINGS_AS_ERRORS=OFF \
	-DCMAKE_INSTALL_PREFIX=%{install_prefix} \
	-DLLVM_INSTALL_SPHINX_HTML_DIR=%{_pkgdocdir}/html \
	-DSPHINX_EXECUTABLE=/usr/bin/sphinx-build-3 \
	-DLLVM_INCLUDE_BENCHMARKS=OFF \
%if %{with lto_build}
	-DLLVM_UNITTEST_LINK_FLAGS="-Wl,-plugin-opt=O0" \
%endif
%ifarch x86_64
	-DCMAKE_SHARED_LINKER_FLAGS="$LDFLAGS -Wl,-z,cet-report=error"
%endif

# Build libLLVM.so first.  This ensures that when libLLVM.so is linking, there
# are no other compile jobs running.  This will help reduce OOM errors on the
# builders without having to artificially limit the number of concurrent jobs.
%cmake_build --target LLVM
%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}/%{_bindir}

# Install binaries needed for lit tests
%global test_binaries llvm-isel-fuzzer llvm-opt-fuzzer

for f in %{test_binaries}
do
    install -m 0755 %{_vpath_builddir}/bin/$f %{buildroot}%{install_bindir}
done

# Remove testing of update utility tools
rm -rf test/tools/UpdateTestChecks

# Install libraries needed for unittests
%if %{without compat_build}
%global build_libdir %{_vpath_builddir}/%{_lib}
%else
%global build_libdir %{_vpath_builddir}/lib
%endif

install %{build_libdir}/libLLVMTestingSupport.a %{buildroot}%{install_libdir}
install %{build_libdir}/libLLVMTestingAnnotations.a %{buildroot}%{install_libdir}

# Fix multi-lib
%multilib_fix_c_header --file %{install_includedir}/llvm/Config/llvm-config.h

%if %{without compat_build}

# Fix some man pages
ln -s llvm-config.1 %{buildroot}%{_mandir}/man1/llvm-config%{exec_suffix}-%{__isa_bits}.1

%if %{with gold}
# Add symlink to lto plugin in the binutils plugin directory.
%{__mkdir_p} %{buildroot}%{_libdir}/bfd-plugins/
ln -s -t %{buildroot}%{_libdir}/bfd-plugins/ ../LLVMgold.so
%endif

%else

# Add version suffix to binaries
for f in %{buildroot}/%{install_bindir}/*; do
  filename=`basename $f`
  ln -s ../../%{install_bindir}/$filename %{buildroot}/%{_bindir}/$filename%{exec_suffix}
done

# Create ld.so.conf.d entry
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat >> %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf << EOF
%{install_libdir}
EOF

# Add version suffix to man pages and move them to mandir.
mkdir -p %{buildroot}/%{_mandir}/man1
for f in %{build_install_prefix}/share/man/man1/*; do
  filename=`basename $f | cut -f 1 -d '.'`
  mv $f %{buildroot}%{_mandir}/man1/$filename%{exec_suffix}.1
done

%endif

# llvm-config special casing. llvm-config is managed by update-alternatives.
# the original file must remain available for compatibility with the CMake
# infrastructure. Without compat, cmake points to the symlink, with compat it
# points to the original file.

%if %{without compat_build}

mv %{buildroot}/%{install_bindir}/llvm-config %{buildroot}/%{install_bindir}/llvm-config%{exec_suffix}-%{__isa_bits}
# We still maintain a versionned symlink for consistency across llvm versions.
# This is specific to the non-compat build and matches the exec prefix for
# compat builds. An isa-agnostic versionned symlink is also maintained in the (un)install
# steps.
(cd %{buildroot}/%{install_bindir} ; ln -s llvm-config%{exec_suffix}-%{__isa_bits} llvm-config-%{maj_ver}-%{__isa_bits} )
# ghost presence
touch %{buildroot}%{_bindir}/llvm-config-%{maj_ver}

%else

rm %{buildroot}%{_bindir}/llvm-config%{exec_suffix}
(cd %{buildroot}/%{install_bindir} ; ln -s llvm-config llvm-config%{exec_suffix}-%{__isa_bits} )

%endif

# ghost presence
touch %{buildroot}%{_bindir}/llvm-config%{exec_suffix}

mkdir -p %{buildroot}%{pkg_datadir}/llvm/cmake
cp -Rv ../cmake/* %{buildroot}%{pkg_datadir}/llvm/cmake

%check
(cd test
 # non reproducible errors
 rm tools/dsymutil/X86/swift-interface.test
 # https://bugzilla.redhat.com/show_bug.cgi?id=2385159
 rm tools/opt-viewer/{basic,filter,suppress,unicode-function-name}.test
%ifarch ppc64le
 rm tools/dsymutil/X86/DWARFLinkerParallel/odr-{fwd-declaration2,predictable-output2,string}.test
%endif
)

%if %{with check}
# FIXME: use %%cmake_build instead of %%__ninja
LD_LIBRARY_PATH=%{buildroot}/%{install_libdir}  %{__ninja} check-all -C %{_vpath_builddir}
%endif

%if %{with compat_build}
# Packages that install files in /etc/ld.so.conf have to manually run
# ldconfig.
# See https://bugzilla.redhat.com/show_bug.cgi?id=2001328 and
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_linker_configuration_files
%post -p /sbin/ldconfig libs
%postun -p /sbin/ldconfig libs
%endif

%post devel
/usr/sbin/update-alternatives --install %{_bindir}/llvm-config%{exec_suffix} llvm-config%{exec_suffix} %{install_bindir}/llvm-config%{exec_suffix}-%{__isa_bits} %{__isa_bits}
%if %{without compat_build}
/usr/sbin/update-alternatives --install %{_bindir}/llvm-config-%{maj_ver} llvm-config-%{maj_ver} %{install_bindir}/llvm-config%{exec_suffix}-%{__isa_bits} %{__isa_bits}

# During the upgrade from LLVM 16 (F38) to LLVM 17 (F39), we found out the
# main llvm-devel package was leaving entries in the alternatives system.
# Try to remove them now.
for v in 14 15 16; do
  if [[ -e %{_bindir}/llvm-config-$v
		&& "x$(%{_bindir}/llvm-config-$v --version | awk -F . '{ print $1 }')" != "x$v" ]]; then
    /usr/sbin/update-alternatives --remove llvm-config-$v %{install_bindir}/llvm-config%{exec_suffix}-%{__isa_bits}
  fi
done
%endif


%postun devel
if [ $1 -eq 0 ]; then
  /usr/sbin/update-alternatives --remove llvm-config%{exec_suffix} %{install_bindir}/llvm-config%{exec_suffix}-%{__isa_bits}
fi
%if %{without compat_build}
# When upgrading between minor versions (i.e. from x.y.1 to x.y.2), we must
# not remove the alternative.
# However, during a major version upgrade (i.e. from 16.x.y to 17.z.w), the
# alternative must be removed in order to give priority to a newly installed
# compat package.
if [[ $1 -eq 0
	  || "x$(%{_bindir}/llvm-config-%{maj_ver} --version | awk -F . '{ print $1 }')" != "x%{maj_ver}" ]]; then
  /usr/sbin/update-alternatives --remove llvm-config-%{maj_ver} %{install_bindir}/llvm-config%{exec_suffix}-%{__isa_bits}
fi
%endif

%files
%license LICENSE.TXT
%exclude %{_mandir}/man1/llvm-config*
%{_mandir}/man1/*
%{install_bindir}/*
%if %{with compat_build}
# This is for all the binaries with the version suffix.
%{_bindir}/*%{exec_suffix}
%endif

%exclude %{_bindir}/llvm-config%{exec_suffix}
%exclude %{install_bindir}/llvm-config%{exec_suffix}-%{__isa_bits}

%exclude %{_bindir}/llvm-config-%{maj_ver}
%exclude %{install_bindir}/llvm-config-%{maj_ver}-%{__isa_bits}
%exclude %{install_bindir}/not
%exclude %{install_bindir}/count
%exclude %{install_bindir}/yaml-bench
%exclude %{install_bindir}/lli-child-target
%exclude %{install_bindir}/llvm-isel-fuzzer
%exclude %{install_bindir}/llvm-opt-fuzzer
%{pkg_datadir}/opt-viewer

%files libs
%license LICENSE.TXT
%{install_libdir}/libLLVM-%{maj_ver}%{?llvm_snapshot_version_suffix:%{llvm_snapshot_version_suffix}}.so
%if %{with gold}
%{install_libdir}/LLVMgold.so
%if %{without compat_build}
%{_libdir}/bfd-plugins/LLVMgold.so
%endif
%endif
%{install_libdir}/libLLVM-%{maj_ver}.so
%{install_libdir}/libLLVM.so.%{maj_ver}.%{min_ver}
%{install_libdir}/libLTO.so*
%{install_libdir}/libRemarks.so*
%if %{with compat_build}
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%endif

%files devel
%license LICENSE.TXT

%ghost %{_bindir}/llvm-config%{exec_suffix}
%{install_bindir}/llvm-config%{exec_suffix}-%{__isa_bits}
%{_mandir}/man1/llvm-config*

%{install_includedir}/llvm
%{install_includedir}/llvm-c
%{install_libdir}/libLLVM.so
%{install_libdir}/cmake/llvm
%{install_bindir}/llvm-config-%{maj_ver}-%{__isa_bits}
%ghost %{_bindir}/llvm-config-%{maj_ver}

%files doc
%license LICENSE.TXT
%doc %{_pkgdocdir}/html

%files static
%license LICENSE.TXT
%{install_libdir}/*.a
%exclude %{install_libdir}/libLLVMTestingSupport.a
%exclude %{install_libdir}/libLLVMTestingAnnotations.a
%exclude %{install_libdir}/libllvm_gtest.a
%exclude %{install_libdir}/libllvm_gtest_main.a

%files cmake-utils
%license LICENSE.TXT
%{pkg_datadir}/llvm/cmake

%files test
%license LICENSE.TXT
%{install_bindir}/not
%{install_bindir}/count
%{install_bindir}/yaml-bench
%{install_bindir}/lli-child-target
%{install_bindir}/llvm-isel-fuzzer
%{install_bindir}/llvm-opt-fuzzer

%files googletest
%license LICENSE.TXT
%{install_libdir}/libLLVMTestingSupport.a
%{install_libdir}/libLLVMTestingAnnotations.a
%{install_libdir}/libllvm_gtest.a
%{install_libdir}/libllvm_gtest_main.a
%{install_includedir}/llvm-gtest
%{install_includedir}/llvm-gmock


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 18.1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Timm Bäder <tbaeder@redhat.com> - 18.1.8-6
- Fix missing cstdint include that broke the build.
- See https://bugzilla.redhat.com/show_bug.cgi?id=2338982

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 18.1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 04 2024 Timm Bäder <tbaeder@redhat.com> - 18.1.8-4
- Update to 18.1.8

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 18.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Timm Bäder <tbaeder@redhat.com> - 18.1.7-3
- Fix gating configuration to work for compat packages

* Thu Jun 27 2024 Tom Stellard <tstellar@redhat.com> - 18.1.7-2
- Fix double install of gtest libraries in the compat package

* Fri Jun 07 2024 Tom Stellard <tstellar@redhat.com> - 18.1.7-1
- 18.1.7 Release

* Tue May 28 2024 Nikita Popov <npopov@redhat.com> - 18.1.6-2
- Fix use after free on ppc64le (rhbz#2283525)

* Sat May 18 2024 Tom Stellard <tstellar@redhat.com> - 18.1.6-1
- 18.1.6 Release

* Tue May 14 2024 Tom Stellard <tstellar@redhat.com> - 18.1.3-2
- Backport fix for rhbz#2275090

%{?llvm_snapshot_changelog_entry}
* Thu Apr 25 2024 Tom Stellard <tstellar@redhat.com> - 18.1.4-1
- 18.1.4 Release

* Fri Apr 12 2024 Tom Stellard <tstellar@redhat.com> - 18.1.3-1
- 18.1.3 Release

* Thu Mar 21 2024 Zhengyu He <hezhy472013@gmail.com> - 18.1.2-2
- Add support for riscv64

* Thu Mar 21 2024 Tom Stellard <tstellar@redhat.com> - 18.1.2-1
- 18.1.2 Release

* Mon Mar 11 2024 Tom Stellard <tstellar@redhat.com> - 18.1.1-1
- 18.1.1 Release

* Tue Feb 27 2024 Tom Stellard <tstellar@redhat.com> - 18.1.0~rc4-1
- 18.1.0-rc4 Release

* Tue Feb 20 2024 Tom Stellard <tstellar@redhat.com> - 18.1.0~rc3-1
- 18.1.0-rc3 Release

* Thu Feb 01 2024 Nikita Popov <npopov@redhat.com> - 17.0.6-6
- Fix crash with -fzero-call-used-regs (rhbz#2262260)

* Mon Jan 29 2024 Nikita Popov <npopov@redhat.com> - 17.0.6-5
- Only use cet-report=error on x86_64

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 17.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 17.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 30 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.6-2
- Fix rhbz #2248872

* Tue Nov 28 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.6-1
- Update to LLVM 17.0.6

* Tue Nov 14 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.5-1
- Update to LLVM 17.0.5

* Tue Oct 31 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.4-1
- Update to LLVM 17.0.4

* Tue Oct 17 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.3-1
- Update to LLVM 17.0.3

* Tue Oct 03 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.2-1
- Update to LLVM 17.0.2

* Fri Sep 22 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.1~rc4-1
- Update to LLVM 17.0.1

* Tue Sep 05 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc4-1
- Update to LLVM 17.0.0 RC4

* Thu Aug 24 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc3-1
- Update to LLVM 17.0.0 RC3

* Thu Aug 24 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc2-2
- Temporarily disable a failing test on ppc64le

* Thu Aug 17 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc2-1
- Update to LLVM 17.0.0 RC2

* Wed Aug 16 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc1-4
- Disable LTO on i686

* Mon Aug 14 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc1-3
- Re-add patch removed by mistake

* Tue Aug 01 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc1-2
- Enable LLVM_UNREACHABLE_OPTIMIZE temporarily

* Mon Jul 31 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc1-1
- Update to LLVM 17.0.0 RC1

* Mon Jul 31 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.6-6
- Fix rhbz #2224885

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.6-4
- Use LLVM_UNITTEST_LINK_FLAGS to reduce link times for unit tests

* Mon Jul 03 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.6-3
- Improve error messages for unsupported relocs on s390x (rhbz#2216906)
- Disable LLVM_UNREACHABLE_OPTIMIZE

* Wed Jun 14 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.6-1
- Update to LLVM 16.0.6

* Fri Jun 09 2023 Nikita Popov <npopov@redhat.com> - 16.0.5-2
- Split off llvm-cmake-utils package

* Mon Jun 05 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.5-1
- Update to LLVM 16.0.5

* Fri May 19 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 16.0.4-2
- Avoid recommonmark dependency in RHEL builds

* Thu May 18 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.4-1
- Update to LLVM 16.0.4

* Tue May 09 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.3-1
- Update to LLVM 16.0.3

* Tue Apr 25 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.2-1
- Update to LLVM 16.0.2

* Tue Apr 11 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.1-1
- Update to LLVM 16.0.1

* Thu Mar 23 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0-2
- Distribute libllvm_gtest.a and libllvm_gtest_main.a with llvm-googletest
- Stop distributing /usr/share/llvm/src/utils

* Mon Mar 20 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0-1
- Update to LLVM 16.0.0

* Thu Mar 16 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0~rc4-2
- Fix the ppc64le triple

* Tue Mar 14 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0~rc4-1
- Update to LLVM 16.0.0 RC4

* Fri Mar 10 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0~rc3-2
- Fix llvm-exegesis failures on s390x

* Wed Feb 22 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0~rc3-1
- Update to LLVM 16.0.0 RC3

* Wed Feb 01 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0~rc1-1
- Update to LLVM 16.0.0 RC1

* Thu Jan 19 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 15.0.7-3
- Update license to SPDX identifiers.
- Include the Apache license adopted in 2019.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Nikita Popov <npopov@redhat.com> - 15.0.7-1
- Update to LLVM 15.0.7

* Mon Jan 09 2023 Tom Stellard <tstellar@redhat.com> - 15.0.6-3
- Omit frame pointers when building

* Mon Dec 19 2022 Nikita Popov <npopov@redhat.com> - 15.0.6-2
- Remove workaround for rbhz#2048440

* Mon Dec 05 2022 Nikita Popov <npopov@redhat.com> - 15.0.6-1
- Update to LLVM 15.0.6

* Fri Nov 11 2022 Nikita Popov <npopov@redhat.com> - 15.0.4-2
- Copy CFLAGS to ASMFLAGs to enable CET in asm files

* Wed Nov 02 2022 Nikita Popov <npopov@redhat.com> - 15.0.4-1
- Update to LLVM 15.0.4

* Tue Sep 27 2022 Nikita Popov <npopov@redhat.com> - 15.0.0-2
- Export GetHostTriple.cmake

* Tue Sep 06 2022 Nikita Popov <npopov@redhat.com> - 15.0.0-1
- Update to LLVM 15.0.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Timm Bäder <tbaeder@redhat.com> - 14.0.5-2
- Release bump for new redhat-rpm-config

* Mon Jun 13 2022 Timm Bäder <tbaeder@redhat.com> - 14.0.5-1
- 14.0.5 Release

* Wed May 18 2022 Tom Stellard <tstellar@redhat.com> - 14.0.3-1
- 14.0.3 Release

* Fri Apr 29 2022 Timm Bäder <tbaeder@redhat.com> - 14.0.0-2
- Remove llvm-cmake-devel package

* Wed Mar 23 2022 Timm Bäder <tbaeder@redhat.com> - 14.0.0-1
- Update to LLVM 14.0.0

* Wed Feb 02 2022 Nikita Popov <npopov@redhat.com> - 13.0.1-1
- Update to LLVM 13.0.1 final

* Tue Jan 25 2022 Nikita Popov <npopov@redhat.com> - 13.0.1~rc3-1
- Update to LLVM 13.0.1rc3

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.1~rc2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Nikita Popov <npopov@redhat.com> - 13.0.1~rc2-1
- Update to LLVM 13.0.1rc2

* Mon Jan 10 2022 Nikita Popov <npopov@redhat.com> - 13.0.1~rc1-1
- Upstream 13.0.1 rc1 release

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 13.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Thu Nov 11 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0-7
- Enable lto on s390x and arm

* Mon Oct 25 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0-6
- Build with Thin LTO

* Mon Oct 18 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0-5
- Build with clang

* Fri Oct 08 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0-4
- Fix default triple on arm

* Wed Oct 06 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0-3
- Set default triple

* Mon Oct 04 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0-2
- Drop abi_revision from soname

* Thu Sep 30 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0-1
- 13.0.0 Release

* Thu Sep 30 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0~rc4-2
- Restore config.guess for host triple detection

* Fri Sep 24 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0~rc4-1
- 13.0.0-rc4 Release

* Fri Sep 17 2021 Tom Stellard <tstellar@redhta.com> - 13.0.0~rc3-1
- 13.0.0-rc3 Release

* Mon Sep 13 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0~rc1-3
- Pass LLVM_DEFAULT_TARGET_TRIPLE to cmake

* Mon Sep 13 2021 Konrad Kleine <kkleine@redhat.com> - 13.0.0~rc1-2
- Add --without=check option

* Wed Aug 04 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0~rc1-1
- 13.0.0-rc1 Release

* Thu Jul 22 2021 sguelton@redhat.com - 12.0.1-3
- Maintain versionned link to llvm-config

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Tom Stellard <tstellar@redhat.com> - 12.0.1-1
- 12.0.1 Release

* Wed Jun 30 2021 Tom Stellard <tstellar@redhat.com> - llvm-12.0.1~rc3-1
- 12.0.1-rc3 Release

* Fri May 28 2021 Tom Stellard <tstellar@redhat.com> - 12.0.1~rc1-2
- Stop installing lit tests

* Wed May 26 2021 Tom Stellard <tstellar@redhat.com> - llvm-12.0.1~rc1-1
- 12.0.1-rc1 Release

* Mon May 17 2021 sguelton@redhat.com - 12.0.0-7
- Fix handling of llvm-config

* Mon May 03 2021 kkleine@redhat.com - 12.0.0-6
- More verbose builds thanks to python3-psutil

* Sat May 01 2021 sguelton@redhat.com - 12.0.0-5
- Fix llvm-config install

* Tue Apr 27 2021 sguelton@redhat.com - 12.0.0-4
- Provide default empty value for exec_suffix when not in compat mode

* Tue Apr 27 2021 sguelton@redhat.com - 12.0.0-3
- Fix llvm-config install

* Tue Apr 20 2021 sguelton@redhat.com - 12.0.0-2
- Backport compat package fix

* Thu Apr 15 2021 Tom Stellard <tstellar@redhat.com> - 12.0.0-1
- 12.0.0 Release

* Thu Apr 08 2021 sguelton@redhat.com - 12.0.0-0.11.rc5
- New upstream release candidate

* Tue Apr 06 2021 sguelton@redhat.com - 12.0.0-0.10.rc4
- Patch test case for compatibility with llvm-test latout

* Fri Apr 02 2021 sguelton@redhat.com - 12.0.0-0.9.rc4
- New upstream release candidate

* Wed Mar 31 2021 Jonathan Wakely <jwakely@redhat.com> - 12.0.0-0.8.rc3
- Rebuilt for removed libstdc++ symbols (#1937698)

* Thu Mar 11 2021 sguelton@redhat.com - 12.0.0-0.7.rc3
- LLVM 12.0.0 rc3

* Wed Mar 10 2021 Kalev Lember <klember@redhat.com> - 12.0.0-0.6.rc2
- Add llvm-static(major) provides to the -static subpackage

* Tue Mar 09 2021 sguelton@redhat.com - 12.0.0-0.5.rc2
- rebuilt

* Tue Mar 02 2021 sguelton@redhat.com - 12.0.0-0.4.rc2
- Change CI working dir

* Wed Feb 24 2021 sguelton@redhat.com - 12.0.0-0.3.rc2
- 12.0.0-rc2 release

* Tue Feb 16 2021 Dave Airlie <airlied@redhat.com> - 12.0.0-0.2.rc1
- Enable LLVM_USE_PERF to allow perf integration

* Tue Feb 2 2021 Serge Guelton - 12.0.0-0.1.rc1
- 12.0.0-rc1 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.0-0.3.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Serge Guelton - 11.1.0-0.2.rc2
- 11.1.0-rc2 release

* Thu Jan 14 2021 Serge Guelton - 11.1.0-0.1.rc1
- 11.1.0-rc1 release

* Tue Jan 05 2021 Serge Guelton - 11.0.1-3.rc2
- Waive extra test case

* Sun Dec 20 2020 sguelton@redhat.com - 11.0.1-2.rc2
- 11.0.1-rc2 release

* Tue Dec 01 2020 sguelton@redhat.com - 11.0.1-1.rc1
- 11.0.1-rc1 release

* Sat Oct 31 2020 Jeff Law <law@redhat.com> - 11.0.0-2
- Fix missing #include for gcc-11

* Wed Oct 14 2020 Josh Stone <jistone@redhat.com> - 11.0.0-1
- Fix coreos-installer test crash on s390x (rhbz#1883457)

* Mon Oct 12 2020 sguelton@redhat.com - 11.0.0-0.11
- llvm 11.0.0 - final release

* Thu Oct 08 2020 sguelton@redhat.com - 11.0.0-0.10.rc6
- 11.0.0-rc6

* Fri Oct 02 2020 sguelton@redhat.com - 11.0.0-0.9.rc5
- 11.0.0-rc5 Release

* Sun Sep 27 2020 sguelton@redhat.com - 11.0.0-0.8.rc3
- Fix NVR

* Thu Sep 24 2020 sguelton@redhat.com - 11.0.0-0.2.rc3
- Obsolete patch for rhbz#1862012

* Thu Sep 24 2020 sguelton@redhat.com - 11.0.0-0.1.rc3
- 11.0.0-rc3 Release

* Wed Sep 02 2020 sguelton@redhat.com - 11.0.0-0.7.rc2
- Apply upstream patch for rhbz#1862012

* Tue Sep 01 2020 sguelton@redhat.com - 11.0.0-0.6.rc2
- Fix source location

* Fri Aug 21 2020 Tom Stellard <tstellar@redhat.com> - 11.0.0-0.5.rc2
- 11.0.0-rc2 Release

* Wed Aug 19 2020 Tom Stellard <tstellar@redhat.com> - 11.0.0-0.4.rc1
- Fix regression-tests CI tests

* Tue Aug 18 2020 Tom Stellard <tstellar@redhat.com> - 11.0.0-0.3.rc1
- Fix rust crash on ppc64le compiling firefox
- rhbz#1862012

* Tue Aug 11 2020 Tom Stellard <tstellar@redhat.com> - 11.0.0-0.2.rc1
- Install update_cc_test_checks.py script

* Thu Aug 06 2020 Tom Stellard <tstellar@redhat.com> - 11.0.0-0.1-rc1
- LLVM 11.0.0-rc1 Release
- Make llvm-devel require llvm-static and llvm-test

* Tue Aug 04 2020 Tom Stellard <tstellar@redhat.com> - 10.0.0-10
- Backport upstream patch to fix build with -flto.
- Disable LTO on s390x to work-around unit test failures.

* Sat Aug 01 2020 sguelton@redhat.com - 10.0.0-9
- Fix update-alternative uninstall script

* Sat Aug 01 2020 sguelton@redhat.com - 10.0.0-8
- Fix gpg verification and update macro usage.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Thu Jun 11 2020 sguelton@redhat.com - 10.0.0-5
- Make llvm-test.tar.gz creation reproducible.

* Tue Jun 02 2020 sguelton@redhat.com - 10.0.0-4
- Instruct cmake not to generate RPATH

* Thu Apr 30 2020 Tom Stellard <tstellar@redhat.com> - 10.0.0-3
- Install LLVMgold.so symlink in bfd-plugins directory

* Tue Apr 07 2020 sguelton@redhat.com - 10.0.0-2
- Do not package UpdateTestChecks tests in llvm-tests
- Apply upstream patch bab5908df to pass gating tests

* Wed Mar 25 2020 sguelton@redhat.com - 10.0.0-1
- 10.0.0 final

* Mon Mar 23 2020 sguelton@redhat.com - 10.0.0-0.6.rc6
- 10.0.0 rc6

* Thu Mar 19 2020 sguelton@redhat.com - 10.0.0-0.5.rc5
- 10.0.0 rc5

* Sat Mar 14 2020 sguelton@redhat.com - 10.0.0-0.4.rc4
- 10.0.0 rc4

* Thu Mar 05 2020 sguelton@redhat.com - 10.0.0-0.3.rc3
- 10.0.0 rc3

* Fri Feb 28 2020 sguelton@redhat.com - 10.0.0-0.2.rc2
- Remove *_finite support, see rhbz#1803203

* Fri Feb 14 2020 sguelton@redhat.com - 10.0.0-0.1.rc2
- 10.0.0 rc2

* Fri Jan 31 2020 sguelton@redhat.com - 10.0.0-0.1.rc1
- 10.0.0 rc1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Tom Stellard <tstellar@redhat.com> - 9.0.1-4
- Rebuild after previous build failed to strip binaries

* Fri Jan 17 2020 Tom Stellard <tstellar@redhat.com> - 9.0.1-3
- Add explicit Requires from sub-packages to llvm-libs

* Fri Jan 10 2020 Tom Stellard <tstellar@redhat.com> - 9.0.1-2
- Fix crash with kernel bpf self-tests

* Thu Dec 19 2019 tstellar@redhat.com - 9.0.1-1
- 9.0.1 Release

* Mon Nov 25 2019 sguelton@redhat.com - 9.0.0-4
- Activate AVR on all architectures

* Mon Sep 30 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-3
- Build libLLVM.so first to avoid OOM errors

* Fri Sep 27 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-2
- Remove unneeded BuildRequires: libstdc++-static

* Thu Sep 19 2019 sguelton@redhat.com - 9.0.0-1
- 9.0.0 Release

* Wed Sep 18 2019 sguelton@redhat.com - 9.0.0-0.5.rc3
- Support avr target, see rhbz#1718492

* Tue Sep 10 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-0.4.rc3
- Split out test executables into their own export file

* Fri Sep 06 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-0.3.rc3
- Fix patch for splitting out static library exports

* Fri Aug 30 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-0.2.rc3
- 9.0.0-rc3 Release

* Thu Aug 01 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-0.1.rc2
- 9.0.0-rc2 Release

* Tue Jul 30 2019 Tom Stellard <tstellar@redhat.com> - 8.0.0-9
- Sync with llvm8.0 spec file

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Tom Stellard <tstellar@redhat.com> - 8.0.0-8
- Add provides for the major version of sub-packages

* Fri May 17 2019 sguelton@redhat.com - 8.0.0-7
- Fix conflicts between llvm-static = 8 and llvm-dev < 8 around LLVMStaticExports.cmake

* Wed Apr 24 2019 Tom Stellard <tstellar@redhat.com> - 8.0.0-6
- Make sure we aren't passing -g on s390x

* Sat Mar 30 2019 Tom Stellard <tstellar@redhat.com> - 8.0.0-5
- Enable build rpath while keeping install rpath disabled

* Wed Mar 27 2019 Tom Stellard <tstellar@redhat.com> - 8.0.0-4
- Backport r351577 from trunk to fix ninja check failures

* Tue Mar 26 2019 Tom Stellard <tstellar@redhat.com> - 8.0.0-3
- Fix ninja check

* Fri Mar 22 2019 Tom Stellard <tstellar@redhat.com> - 8.0.0-2
- llvm-test fixes

* Wed Mar 20 2019 sguelton@redhat.com - 8.0.0-1
- 8.0.0 final

* Fri Mar 15 2019 sguelton@redhat.com - 8.0.0-0.6.rc4
- Activate all backends (rhbz#1689031)

* Tue Mar 12 2019 sguelton@redhat.com - 8.0.0-0.5.rc4
- 8.0.0 Release candidate 4

* Mon Mar 4 2019 sguelton@redhat.com - 8.0.0-0.4.rc3
- Move some binaries to -test package, cleanup specfile

* Mon Mar 4 2019 sguelton@redhat.com - 8.0.0-0.3.rc3
- 8.0.0 Release candidate 3

* Fri Feb 22 2019 sguelton@redhat.com - 8.0.0-0.2.rc2
- 8.0.0 Release candidate 2

* Sat Feb 9 2019 sguelton@redhat.com - 8.0.0-0.1.rc1
- 8.0.0 Release candidate 1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Josh Stone <jistone@redhat.com> - 7.0.1-2
- Fix discriminators in metadata, rhbz#1668033

* Mon Dec 17 2018 sguelton@redhat.com - 7.0.1-1
- 7.0.1 release

* Tue Dec 04 2018 sguelton@redhat.com - 7.0.0-5
- Ensure rpmlint passes on specfile

* Sat Nov 17 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-4
- Install testing libraries for unittests

* Sat Oct 27 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-3
- Fix running unittests as not-root user

* Thu Sep 27 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-2
- Fixes for llvm-test package:
- Add some missing Requires
- Add --threads option to run-lit-tests script
- Set PATH so lit can find tools like count, not, etc.
- Don't hardcode tools directory to /usr/lib64/llvm
- Fix typo in yaml-bench define
- Only print information about failing tests

* Fri Sep 21 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-1
- 7.0.0 Release

* Thu Sep 13 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.15.rc3
- Disable rpath on install LLVM and related sub-projects

* Wed Sep 12 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.14.rc3
- Remove rpath from executables and libraries

* Tue Sep 11 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.13.rc3
- Re-enable arm and aarch64 targets on x86_64

* Mon Sep 10 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.12.rc3
- 7.0.0-rc3 Release

* Fri Sep 07 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.11.rc2
- Use python3 shebang for opt-viewewr scripts

* Thu Aug 30 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.10.rc2
- Drop all uses of python2 from lit tests

* Thu Aug 30 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.9.rc2
- Build the gold plugin on all supported architectures

* Wed Aug 29 2018 Kevin Fenzi <kevin@scrye.com> - 7.0.0-0.8.rc2
- Re-enable debuginfo to avoid 25x size increase.

* Tue Aug 28 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.7.rc2
- 7.0.0-rc2 Release

* Tue Aug 28 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.6.rc1
- Guard valgrind usage with valgrind_arches macro

* Thu Aug 23 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.5.rc1
- Package lit tests and googletest sources.

* Mon Aug 20 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.4.rc1
- Re-enable AMDGPU target on ARM rhbz#1618922

* Mon Aug 13 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.3.rc1
- Drop references to TestPlugin.so from cmake files

* Fri Aug 10 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.2.rc1
- Fixes for lit tests

* Fri Aug 10 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.1.rc1
- 7.0.0-rc1 Release
- Reduce number of enabled targets on all arches.
- Drop s390 detection patch, LLVM does not support s390 codegen.

* Mon Aug 06 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-6
- Backport some fixes needed by mesa and rust

* Thu Jul 26 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-5
- Move libLLVM-6.0.so to llvm6.0-libs.

* Mon Jul 23 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-4
- Rebuild because debuginfo stripping failed with the previous build

* Fri Jul 13 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-3
- Sync specfile with llvm6.0 package

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-1
- 6.0.1 Release

* Thu Jun 07 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-0.4.rc2
- 6.0.1-rc2

* Wed Jun 06 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-0.3.rc1
- Re-enable all targets to avoid breaking the ABI.

* Mon Jun 04 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-0.2.rc1
- Reduce the number of enabled targets based on the architecture

* Thu May 10 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-0.1.rc1
- 6.0.1 rc1

* Tue Mar 27 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-11
- Re-enable arm tests that used to hang

* Thu Mar 22 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-10
- Fix testcase in backported patch

* Tue Mar 20 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-9
- Prevent external projects from linking against both static and shared
  libraries.  rhbz#1558657

* Mon Mar 19 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-8
- Backport r327651 from trunk rhbz#1554349

* Fri Mar 16 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-7
- Filter out cxxflags and cflags from llvm-config that aren't supported by clang
- rhbz#1556980

* Wed Mar 14 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-6
- Enable symbol versioning in libLLVM.so

* Wed Mar 14 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-5
- Stop statically linking libstdc++.  This is no longer required by Steam
  client, but the steam installer still needs a work-around which should
  be handled in the steam package.
* Wed Mar 14 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-4
- s/make check/ninja check/

* Fri Mar 09 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-3
- Backport fix for compile time regression on rust rhbz#1552915

* Thu Mar 08 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-2
- Build with Ninja: This reduces RPM build time on a 6-core x86_64 builder
  from 82 min to 52 min.

* Thu Mar 08 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-1
- 6.0.0 Release

* Thu Mar 08 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.5.rc2
- Reduce debuginfo size on i686 to avoid OOM errors during linking

* Fri Feb 09 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.4.rc2
- 6.0.1 rc2

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6.0.0-0.3.rc1
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.1.rc1
- 6.0.1 rc1

* Tue Dec 19 2017 Tom Stellard <tstellar@redhat.com> - 5.0.1-1
- 5.0.1 Release

* Mon Nov 20 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-5
- Backport debuginfo fix for rust

* Fri Nov 03 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-4
- Reduce debuginfo size for ARM

* Tue Oct 10 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-2
- Reduce memory usage on ARM by disabling debuginfo and some non-ARM targets.

* Mon Sep 25 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-1
- 5.0.0 Release

* Mon Sep 18 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-6
- Add Requires: libedit-devel for llvm-devel

* Fri Sep 08 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-5
- Enable libedit backend for LineEditor API

* Fri Aug 25 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-4
- Enable extra functionality when run the LLVM JIT under valgrind.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-1
- 4.0.1 Release

* Thu Jun 15 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-6
- Install llvm utils

* Thu Jun 08 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-5
- Fix docs-llvm-man target

* Mon May 01 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-4
- Make cmake files no longer depend on static libs (rhbz 1388200)

* Tue Apr 18 2017 Josh Stone <jistone@redhat.com> - 4.0.0-3
- Fix computeKnownBits for ARMISD::CMOV (rust-lang/llvm#67)

* Mon Apr 03 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-2
- Simplify spec with rpm macros.

* Thu Mar 23 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-1
- LLVM 4.0.0 Final Release

* Wed Mar 22 2017 tstellar@redhat.com - 3.9.1-6
- Fix %%postun sep for -devel package.

* Mon Mar 13 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-5
- Disable failing tests on ARM.

* Sun Mar 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 3.9.1-4
- Fix missing mask on relocation for aarch64 (rhbz 1429050)

* Wed Mar 01 2017 Dave Airlie <airlied@redhat.com> - 3.9.1-3
- revert upstream radeonsi breaking change.

* Thu Feb 23 2017 Josh Stone <jistone@redhat.com> - 3.9.1-2
- disable sphinx warnings-as-errors

* Fri Feb 10 2017 Orion Poplawski <orion@cora.nwra.com> - 3.9.1-1
- llvm 3.9.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Josh Stone <jistone@redhat.com> - 3.9.0-7
- Apply backports from rust-lang/llvm#55, #57

* Tue Nov 01 2016 Dave Airlie <airlied@gmail.com - 3.9.0-6
- rebuild for new arches

* Wed Oct 26 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-5
- apply the patch from -4

* Wed Oct 26 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-4
- add fix for lldb out-of-tree build

* Mon Oct 17 2016 Josh Stone <jistone@redhat.com> - 3.9.0-3
- Apply backports from rust-lang/llvm#47, #48, #53, #54

* Sat Oct 15 2016 Josh Stone <jistone@redhat.com> - 3.9.0-2
- Apply an InstCombine backport via rust-lang/llvm#51

* Wed Sep 07 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-1
- llvm 3.9.0
- upstream moved where cmake files are packaged.
- upstream dropped CppBackend

* Wed Jul 13 2016 Adam Jackson <ajax@redhat.com> - 3.8.1-1
- llvm 3.8.1
- Add mips target
- Fix some shared library mispackaging

* Tue Jun 07 2016 Jan Vcelak <jvcelak@fedoraproject.org> - 3.8.0-2
- fix color support detection on terminal

* Thu Mar 10 2016 Dave Airlie <airlied@redhat.com> 3.8.0-1
- llvm 3.8.0 release

* Wed Mar 09 2016 Dan Horák <dan[at][danny.cz> 3.8.0-0.3
- install back memory consumption workaround for s390

* Thu Mar 03 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.2
- llvm 3.8.0 rc3 release

* Fri Feb 19 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.1
- llvm 3.8.0 rc2 release

* Tue Feb 16 2016 Dan Horák <dan[at][danny.cz> 3.7.1-7
- recognize s390 as SystemZ when configuring build

* Sat Feb 13 2016 Dave Airlie <airlied@redhat.com> 3.7.1-6
- export C++ API for mesa.

* Sat Feb 13 2016 Dave Airlie <airlied@redhat.com> 3.7.1-5
- reintroduce llvm-static, clang needs it currently.

* Fri Feb 12 2016 Dave Airlie <airlied@redhat.com> 3.7.1-4
- jump back to single llvm library, the split libs aren't working very well.

* Fri Feb 05 2016 Dave Airlie <airlied@redhat.com> 3.7.1-3
- add missing obsoletes (#1303497)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.1-1
- new upstream release
- enable gold linker

* Wed Nov 04 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- fix Requires for subpackages on the main package

* Tue Oct 06 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- initial version using cmake build system
