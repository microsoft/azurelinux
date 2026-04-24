# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upstreamname HIPIFY

%global rocm_release 6.4
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

# This is a clang tool so best to build with clang
%global toolchain clang

Name:           hipify
Version:        %{rocm_version}
Release: 4%{?dist}
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
BuildRequires:  rocm-llvm-static
BuildRequires:  rocm-clang-devel
BuildRequires:  rocm-compilersupport-macros
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
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/..

%cmake_build

%check
echo "void f(int *a, const cudaDeviceProp *b) { cudaChooseDevice(a,b); }" > b.cu
echo "void f(int *a, const hipDeviceProp_t *b) { hipChooseDevice(a,b); }" > e.hip
./bin/hipify-perl b.cu -o t.hip
diff e.hip t.hip

%install
%cmake_install
rm -rf %{buildroot}/usr/hip
# Fix executable perm:
chmod a+x %{buildroot}%{_bindir}/*
# Fix script shebang (Fedora doesn't allow using "env"):
sed -i 's|\(/usr/bin/\)env perl|\1perl|' %{buildroot}%{_bindir}//hipify-perl

# Fix
# /usr/bin/hipify-clang: error while loading shared libraries: libclang-cpp.so.19.0git
chrpath %{buildroot}%{_bindir}/hipify-clang -r %rocmllvm_libdir

if [ -d %{buildroot}%{_includedir} ]; then
    rm -rf %{buildroot}%{_includedir}
fi

%files
%doc README.md
%license LICENSE.txt
%{_bindir}/hipconvertinplace-perl.sh
%{_bindir}/hipconvertinplace.sh
%{_bindir}/hipexamine-perl.sh
%{_bindir}/hipexamine.sh
%{_bindir}/hipify-clang
%{_bindir}/hipify-perl
%{_libexecdir}/%{name}

%changelog
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
