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
%global upstreamname HIPIFY

%global rocm_release 7.1
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

%bcond_with compat
%if %{with compat}
%global pkg_libdir lib
%global pkg_prefix %{_prefix}/lib64/rocm/rocm-%{rocm_release}/
%global pkg_suffix -%{rocm_release}
%global pkg_module rocm%{pkg_suffix}
%else
%global pkg_libdir %{_lib}
%global pkg_prefix %{_prefix}
%global pkg_suffix %{nil}
%global pkg_module default
%endif

# This is a clang tool so best to build with clang
%global toolchain clang

Name:           hipify%{pkg_suffix}
Version:        %{rocm_version}
Release:        3%{?dist}
Summary:        Convert CUDA to HIP

Url:            https://github.com/ROCm
License:        MIT
Source0:        %{url}/%{upstreamname}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz
Patch0:         0001-prepare-hipify-cmake-for-fedora.patch

BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  perl
# System clang may be too old, use rocm-llvm
BuildRequires:  rocm-llvm%{pkg_suffix}-static
BuildRequires:  rocm-clang%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  zlib-devel

Requires:       perl

# ROCm is really only on x86_64
ExclusiveArch:  x86_64

%description
HIPIFY is a set of tools to translate CUDA source code into portable
HIP C++ automatically.

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

%build
%cmake \
    -DCMAKE_CXX_COMPILER=%rocmllvm_bindir/clang++ \
    -DCMAKE_C_COMPILER=%rocmllvm_bindir/clang \
    -DCMAKE_INSTALL_LIBDIR=%{pkg_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{pkg_prefix} \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/..

%cmake_build

%check
echo "void f(int *a, const cudaDeviceProp *b) { cudaChooseDevice(a,b); }" > b.cu
echo "void f(int *a, const hipDeviceProp_t *b) { hipChooseDevice(a,b); }" > e.hip
./bin/hipify-perl b.cu -o t.hip
diff e.hip t.hip

%install
%cmake_install
rm -rf %{buildroot}%{pkg_prefix}/hip
# Fix executable perm:
chmod a+x %{buildroot}%{pkg_prefix}/bin/*
# Fix script shebang (Fedora doesn't allow using "env"):
sed -i 's|\(/usr/bin/\)env perl|\1perl|' %{buildroot}%{pkg_prefix}/bin//hipify-perl

# Fix
# /usr/bin/hipify-clang: error while loading shared libraries: libclang-cpp.so.19.0git
chrpath %{buildroot}%{pkg_prefix}/bin/hipify-clang -r %rocmllvm_libdir

# No devel package
rm -rf %{buildroot}%{pkg_prefix}/include

%files
%doc README.md
%license LICENSE.txt
%{pkg_prefix}/bin/hipify-clang
%{pkg_prefix}/bin/hipify-perl
%{pkg_prefix}/libexec/hipify/

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 22 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-2
- Add --with compat

* Fri Oct 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Fri Sep 19 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-1
- Update to 7.0.1

* Thu Aug 28 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-5
- Add Fedora copyright

* Mon Aug 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-4
- Simplify file removal

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-2
- Fix hipify-clang rpath

* Thu May 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.1-1
- Update to 6.4.1

* Fri Apr 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Fri Apr 4 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-4
- Use rocm clang

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 17 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- Build with system clang

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3
