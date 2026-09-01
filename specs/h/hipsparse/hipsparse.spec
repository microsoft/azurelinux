# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Copyright Fedora Project Authors.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
%bcond_with gitcommit
%if %{with gitcommit}
%global commit0 2584e35062ad9c2edb68d93c464cf157bc57e3b0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20250926
%endif

%global upstreamname hipsparse
%global rocm_release 7.1
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

%bcond_with compat
%if %{with compat}
%global pkg_libdir lib
%global pkg_prefix %{_prefix}/lib64/rocm/rocm-%{rocm_release}
%global pkg_suffix -%{rocm_release}
%global pkg_module rocm%{pkg_suffix}
%else
%global pkg_libdir %{_lib}
%global pkg_prefix %{_prefix}
%global pkg_suffix %{nil}
%global pkg_module default
%endif
%if 0%{?suse_version}
%global hipsparse_name libhipsparse4%{pkg_suffix}
%else
%global hipsparse_name hipsparse%{pkg_suffix}
%endif

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-mtls-dialect=gnu2//')

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RelWithDebInfo
%endif

# export an llvm compilation database
# Useful for input for other llvm tools
%bcond_with export
%if %{with export}
%global build_compile_db ON
%else
%global build_compile_db OFF
%endif

# downloads tests, use mock --enable-network
%bcond_with test
%if %{with test}
%global build_test ON
%global __brp_check_rpaths %{nil}
%else
%global build_test OFF
%endif

%bcond_without check

# gfortran and clang rpm macros do not mix
%global build_fflags %{nil}

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

Name:           %{hipsparse_name}
%if %{with gitcommit}
Version:        git%{date0}.%{shortcommit0}
Release:        2%{?dist}
%else
Version:        %{rocm_version}
Release:        5%{?dist}
%endif
Summary:        ROCm SPARSE marshalling library
License:        MIT
URL:            https://github.com/ROCm/rocm-libraries

%if %{with gitcommit}
Source0:        %{url}/archive/%{commit0}/rocm-libraries-%{shortcommit0}.tar.gz
%else
Source0:        %{url}/releases/download/rocm-%{version}/%{upstreamname}.tar.gz#/%{upstreamname}-%{version}.tar.gz
%endif

Patch1:         0001-hipsparse-change-test-download-dir.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
%if 0%{?suse_version}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif
BuildRequires:  rocm-cmake%{pkg_suffix}
BuildRequires:  rocm-comgr%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  rocm-hip%{pkg_suffix}-devel
BuildRequires:  rocm-runtime%{pkg_suffix}-devel
BuildRequires:  rocm-rpm-macros%{pkg_suffix}
BuildRequires:  rocprim%{pkg_suffix}-static
BuildRequires:  rocsparse%{pkg_suffix}-devel

%if %{with test}
%if 0%{?suse_version}
BuildRequires:  gtest
%else
BuildRequires:  gtest-devel
%endif
BuildRequires:  rocblas%{pkg_suffix}-devel
%endif

%if %{with check}
%if %{with export}
BuildRequires:  cppcheck
BuildRequires:  cppcheck-htmlreport
BuildRequires:  rocm-clang-analyzer%{pkg_suffix}
BuildRequires:  rocm-clang-tools-extra%{pkg_suffix}
%endif
%endif

Provides:       hipsparse%{pkg_suffix} = %{version}-%{release}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
hipSPARSE is a SPARSE marshalling library with multiple
supported backends. It sits between your application and
a 'worker' SPARSE library, where it marshals inputs to
the backend library and marshals results to your
application. hipSPARSE exports an interface that doesn't
require the client to change, regardless of the chosen
backend. Currently, hipSPARSE supports rocSPARSE and
cuSPARSE backends.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       hipsparse%{pkg_suffix}-devel = %{version}-%{release}

%description devel
%{summary}

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%prep
%if %{with gitcommit}
%setup -q -n rocm-libraries-%{commit0}
cd projects/hiprand
%patch -P1 -p1
%else
%autosetup -p1 -n %{upstreamname}
%endif

# A better default for the matrices dir
sed -i -e 's@hipsparse_exepath() + "../matrices/"@"%{pkg_prefix}/share/hipsparse/matrices/"@' clients/include/utility.hpp

%build
%if %{with gitcommit}
cd projects/hipsparse
%endif

%cmake \
    -DCMAKE_C_COMPILER=%rocmllvm_bindir/amdclang \
    -DCMAKE_CXX_COMPILER=%rocmllvm_bindir/amdclang++ \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=%{build_compile_db} \
    -DCMAKE_INSTALL_LIBDIR=%{pkg_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{pkg_prefix} \
    -DCMAKE_LINKER=%rocmllvm_bindir/ld.lld \
    -DCMAKE_AR=%rocmllvm_bindir/llvm-ar \
    -DCMAKE_RANLIB=%rocmllvm_bindir/llvm-ranlib \
    -DCMAKE_BUILD_TYPE=%build_type \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DCMAKE_SKIP_RPATH=ON \
    -DROCM_SYMLINK_LIBS=OFF \
    -DHIP_PLATFORM=amd \
    -DGPU_TARGETS=%{rocm_gpu_list_default} \
    -DBUILD_CLIENTS_BENCHMARKS=%{build_test} \
    -DBUILD_CLIENTS_SAMPLES=OFF \
    -DBUILD_CLIENTS_TESTS=%{build_test} \
    -DBUILD_CLIENTS_TESTS_OPENMP=OFF \
    -DCMAKE_MATRICES_DIR=%{_builddir}/hipsparse-test-matrices/ \
    -DBUILD_FORTRAN_CLIENTS=OFF

%cmake_build

%if %{with check}
%check
%if %{with export}
json=`find . -name 'compile_commands.json'`
json=`realpath $json`
json_dir=`dirname $json`
if [ -f ${json} ]; then
    jobs=`nproc`
    export PATH=%{rocmllvm_bindir}:$PATH
    output=/tmp/%{name}-tidy/
    mkdir -p ${output}
    # Use echo to consume tidy's error code
    %{rocmllvm_bindir}/run-clang-tidy -p ${json_dir} &> ${output}/tidy.log || echo "ran clang-tidy"
    
    output=/tmp/%{name}-cppcheck/
    mkdir -p ${output}
    cppcheck --project=${json} -j ${jobs} --std=c++17 --safety --output-file=${output}/cppcheck.txt
    cppcheck --project=${json} -j ${jobs} --std=c++17 --safety --xml --output-file=${output}/cppcheck.xml
    cppcheck-htmlreport --file=${output}/cppcheck.xml --report-dir=${output}
fi
%endif
%endif

%install
%if %{with gitcommit}
cd projects/hipsparse
%endif

%cmake_install

rm -f %{buildroot}%{pkg_prefix}/share/doc/hipsparse/LICENSE.md

%if %{with test}
mkdir -p %{buildroot}/%{pkg_prefix}/share/hipsparse/matrices
install -pm 644 %{_builddir}/%{name}-test-matrices/* %{buildroot}/%{pkg_prefix}/share/hipsparse/matrices
%endif

%files
%if %{with gitcommit}
%doc projects/hipsparse/README.md
%license projects/hipsparse/LICENSE.md
%else
%doc README.md
%license LICENSE.md
%endif

%{pkg_prefix}/%{pkg_libdir}/libhipsparse.so.4{,.*}

%files devel
%{pkg_prefix}/include/hipsparse/
%{pkg_prefix}/%{pkg_libdir}/libhipsparse.so
%{pkg_prefix}/%{pkg_libdir}/cmake/hipsparse/

%if %{with test}
%files test
%{pkg_prefix}/bin/hipsparse*
%{pkg_prefix}/share/hipsparse/
%endif

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Jan 12 2026 Tom Rix <Tom.Rix@amd.com> - 7.1.1-4
- Add static analysis check

* Wed Jan 7 2026 Tom Rix <Tom.Rix@amd.com> - 7.1.1-3
- Fix test matrices location
- Remove --with check

* Tue Dec 23 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-2
- Add --with compat
- Add copyright

* Thu Nov 27 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-1
- Update to 7.1.1

* Thu Nov 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-2
- Remove dir tags

* Fri Oct 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Sat Sep 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.0-1
- Update to 7.0.1

* Mon Aug 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Simplify file removal

* Wed Jul 30 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-2
- Remove -mtls-dialect cflag

* Thu Jul 24 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 19 2025 Tim Flink <tflink@fedoraproject.org> - 6.4.0-4
- rework test subpackage to include test data in a predictable location

* Mon Jun 16 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Remove suse check of ldconfig

* Wed May 14 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Cleanup module build

* Sat Apr 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Thu Feb 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-5
- Remove multi build
- Fix SLE 15.6

* Tue Jan 21 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-4
- multithread compress

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- build requires gcc-c++

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sun Nov 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed

