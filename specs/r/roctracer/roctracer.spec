# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upstreamname roctracer
%global rocm_release 6.4
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain clang
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')

# Needs ROCm HW and is only suitable for local testing
# GPU_TARGETS in the cmake config are only for testing
%bcond_with test
%if %{with test}
# rpm flags interfere with building the tests
%global build_cflags %{nil}
%endif

%bcond_with doc

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
%define _source_payload	w7T0.xzdio
%define _binary_payload	w7T0.xzdio

Name:           roctracer
Version:        %{rocm_version}
Release:        4%{?dist}
Summary:        ROCm Tracer Callback/Activity Library for Performance tracing AMD GPUs

Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT
Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros

%if 0%{?suse_version}
BuildRequires:  libatomic1
%if %{suse_version} < 1699
BuildRequires:  python3-cppheaderparser
%else
BuildRequires:  python313-cppheaderparser
%endif
%else
BuildRequires:  libatomic
# https://github.com/ROCm/roctracer/issues/113
BuildRequires:  python3-cppheaderparser
%endif

%if %{with doc}
BuildRequires:  doxygen
BuildRequires:  texlive-adjustbox
BuildRequires:  texlive-dvips
BuildRequires:  texlive-ec
BuildRequires:  texlive-hanging
BuildRequires:  texlive-latex
BuildRequires:  texlive-makeindex
BuildRequires:  texlive-metafont
BuildRequires:  texlive-multirow
BuildRequires:  texlive-newunicodechar
BuildRequires:  texlive-stackengine
BuildRequires:  texlive-texlive-scripts
BuildRequires:  texlive-tocloft
BuildRequires:  texlive-ulem
BuildRequires:  texlive-url
BuildRequires:  texlive-wasy
BuildRequires:  texlive-wasysym
%endif

# ROCm is only x86_64 for now
ExclusiveArch:  x86_64

%description
ROC-tracer

* ROC-tracer library: Runtimes Generic Callback/Activity APIs

  The goal of the implementation is to provide a generic independent
  from specific runtime profiler to trace API and asynchronous activity.

  The API provides functionality for registering the runtimes API
  callbacks and asynchronous activity records pool support.

* ROC-TX library: Code Annotation Events API

  Includes API for:

  * roctxMark
  * roctxRangePush
  * roctxRangePop

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary:        The %{name} development package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The headers of libraries for %{name}.

%if %{with doc}
%package doc
Summary:        Docs for %{name}

%description doc
%{summary}
%endif

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

# No knob in cmake to turn off testing
%if %{without test}
sed -i -e 's@add_subdirectory(test)@#add_subdirectory(test)@' CMakeLists.txt

%else

# Adjust test running script lib dir
sed -i -e 's@../lib/@../lib64/@' test/run.sh

%endif

%build
%cmake \
    -DCMAKE_CXX_COMPILER=%rocmllvm_bindir/clang++ \
    -DCMAKE_C_COMPILER=%rocmllvm_bindir/clang \
    -DCMAKE_MODULE_PATH=%{_libdir}/cmake/hip \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
    -DROCM_SYMLINK_LIBS=OFF \
    -DGPU_TARGETS=%{rocm_gpu_list_test} \
    -DHIP_PLATFORM=amd \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=RelDebInfo

%cmake_build

%if %{with doc}
%cmake_build -t doc
%endif

%install
%cmake_install

# Only install the pdf
rm -rf rm %{buildroot}%{_datadir}/html

%files
%dir %{_libdir}/%{name}
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}64.so.*
%{_libdir}/libroctx64.so.*
%{_libdir}/%{name}/libfile_plugin.so
%{_libdir}/%{name}/libhip_stats.so
%{_libdir}/%{name}/libroctracer_tool.so
%exclude %{_docdir}/%{name}*/LICENSE

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}64.so
%{_libdir}/libroctx64.so

%if %{with doc}
%files doc
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/%{name}.pdf
%endif

%if %{with test}
%files test
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%endif

%changelog
* Thu Aug 7 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-4
- Fix building test subpackage - 6.4.0-3

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Remove suse check of ldconfig

* Fri Apr 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Mon Feb 24 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-7
- Specialize python-cppheaderparser for tw

* Thu Feb 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-6
- Fix SLE 15.6

* Wed Feb 5 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-5
- Fix TW build

* Mon Jan 20 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-4
- multithread compress

* Sat Jan 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-3
- fix gpu list

* Wed Jan 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- build requires gcc-c++

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3
