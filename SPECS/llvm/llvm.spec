Summary:        A collection of modular and reusable compiler and toolchain technologies.
Name:           llvm
Version:        17.0.6
Release:        2%{?dist}
License:        NCSA
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://llvm.org/
Source0:        https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  libffi-devel
BuildRequires:  libxml2-devel
BuildRequires:  ninja-build
BuildRequires:  python3-devel
Requires:       libxml2
Provides:       %{name} = %{version}
Provides:       %{name} = %{version}-%{release}

%description
The LLVM Project is a collection of modular and reusable compiler and toolchain technologies. Despite its name, LLVM has little to do with traditional virtual machines, though it does provide helpful libraries that can be used to build them. The name "LLVM" itself is not an acronym; it is the full name of the project.

%package devel
Summary:        Development headers for llvm
Requires:       %{name} = %{version}-%{release}

%description devel
The llvm-devel package contains libraries, header files and documentation
for developing applications that use llvm.

%prep
%setup -q -n llvm-project-llvmorg-%{version}

%build
# Disable symbol generation
export CFLAGS="`echo " %{build_cflags} " | sed 's/ -g//'`"
export CXXFLAGS="`echo " %{build_cxxflags} " | sed 's/ -g//'`"

mkdir -p build
cd build
cmake -G Ninja                              \
      -DCMAKE_INSTALL_PREFIX=%{_prefix}     \
      -DLLVM_ENABLE_FFI=ON                  \
      -DLLVM_ENABLE_RTTI=ON                 \
      -DCMAKE_BUILD_TYPE=Release            \
      -DLLVM_PARALLEL_LINK_JOBS=1           \
      -DLLVM_PARALLEL_COMPILE_JOBS=%{?_smp_ncpus_max:%_smp_build_ncpus} \
      -DLLVM_BUILD_LLVM_DYLIB=ON            \
      -DLLVM_LINK_LLVM_DYLIB=ON             \
      -DLLVM_INCLUDE_TESTS=ON               \
      -DLLVM_BUILD_TESTS=ON                 \
      -DLLVM_TARGETS_TO_BUILD="host"        \
      -DLLVM_INCLUDE_GO_TESTS=No            \
      -DLLVM_ENABLE_RTTI=ON                 \
      -Wno-dev ../llvm

%ninja_build LLVM
%ninja_build

%install
%ninja_install -C build

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
# disable security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
cd build

# remove tests that do not pass because of 'root' user usage in chroot while testing
#    - e.g.: verifying access denied against a file for current user
rm -f ../llvm/test/tools/llvm-ar/error-opening-permission.test
rm -f ../llvm/test/tools/llvm-ranlib/error-opening-permission.test
rm -f ../llvm/test/tools/llvm-dwarfdump/X86/output.s
rm -f ../llvm/test/tools/llvm-ifs/fail-file-write.test

ninja check-all

%files
%defattr(-,root,root)
%license LICENSE.TXT
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%dir %{_datadir}/opt-viewer
%{_datadir}/opt-viewer/opt-diff.py
%{_datadir}/opt-viewer/opt-stats.py
%{_datadir}/opt-viewer/opt-viewer.py
%{_datadir}/opt-viewer/optpmap.py
%{_datadir}/opt-viewer/optrecord.py
%{_datadir}/opt-viewer/style.css

%files devel
%{_libdir}/*.a
%{_libdir}/cmake/*
%{_includedir}/*

%changelog
* Wed Jan 31 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 17.0.6-2
- Address %check issues

* Fri Jan 12 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 17.0.6-1
- Upgrade to 17.0.6

* Thu Jun 29 2023 Andrew Phelps <anphel@microsoft.com> - 16.0.0-3
- Modify parallel compile jobs limit to _smp_ncpus_max if set, or _smp_build_ncpus

* Thu Jun 01 2023 Andrew Phelps <anphel@microsoft.com> - 16.0.0-2
- Limit to 2 parallel compile jobs to avoid running out of memory in build

* Wed Apr 05 2023 Andrew Phelps <anphel@microsoft.com> - 16.0.0-1
- Add spec for llvm16

* Tue Dec 06 2022 Adam Schwab <adschwab@microsoft.com> - 12.0.1-5
- Workaround for llvm issue #49955 with patch

* Wed Feb 09 2022 Chris Co <chrco@microsoft.com> - 12.0.1-4
- Allow tools to link to libLLVM shared library

* Mon Jan 31 2022 Thomas Crain <thcrain@microsoft.com> - 12.0.1-3
- Use python3 during build

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 12.0.1-2
- Removing the explicit %%clean stage.

* Fri Sep 17 2021 Chris Co <chrco@microsoft.com> - 12.0.1-1
- Update to 12.0.1

* Tue Apr 27 2021 Thomas Crain <thcrain@microsoft.com> - 8.0.1-5
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 8.0.1-4: Enable tests in build and run test with ninja.

* Thu Apr 15 2021 Henry Li <lihl@microsoft.com> - 8.0.1-4
- Add -DLLVM_ENABLE_RTTI=ON to cmake build option

* Fri Jun 12 2020 Henry Beberman <henry.beberman@microsoft.com> - 8.0.1-3
- Switch to ninja-build to use LLVM_PARALLEL_LINK_JOBS=1 to reduce
- fatal OOM errors during linking phase.
- Temporarily disable generation of debug symbols.

* Sat May 09 00:21:29 PST 2020 Nick Samson <nisamson@microsoft.com> - 8.0.1-2
- Added %%license line automatically

* Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> - 8.0.1-1
- Update to 8.0.1. URL Fixed. Source0 URL Fixed. License verified.

* Fri Sep 27 2019 Andrew Phelps <anphel@microsoft.com> - 6.0.1-5
- Enable BPF target which is required for BCC spec

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 6.0.1-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jun 26 2019 Keerthana K <keerthanak@vmware.com> - 6.0.1-3
- Enable target BPF

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> - 6.0.1-2
- Added BuildRequires python2

* Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 6.0.1-1
- Update to version 6.0.1 to get it to build with gcc 7.3

* Thu Aug 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.0.0-3
- Make check fix

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.0.0-2
- BuildRequires libffi-devel

* Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.0.0-1
- Version update

* Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com> - 3.9.1-1
- Initial build.
