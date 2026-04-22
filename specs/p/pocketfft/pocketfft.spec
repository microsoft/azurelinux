# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 076cb3d2536b7c5d0629093ad886e10ac05f3623
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20230214

Summary:        C++ header for FFT
Name:           pocketfft
License:        BSD-3-Clause
Version:        1.0^git%{date0}.%{shortcommit0}
Release: 8%{?dist}

# Only a header
BuildArch:      noarch

URL:            https://github.com/mreineck/%{name}
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  gcc-c++

%description
PocketFFT for C++
=================

This is a heavily modified implementation of FFTPack [1,2], with the following
advantages:

- Strictly C++11 compliant
- More accurate twiddle factor computation
- Worst case complexity for transform sizes with large prime factors is
  `N*log(N)`, because Bluestein's algorithm [3] is used for these cases.
- Supports multidimensional arrays and selection of the axes to be transformed.
- Supports `float`, `double`, and `long double` types.
- Supports fully complex and half-complex (i.e. complex-to-real and
  real-to-complex) FFTs. For half-complex transforms, several conventions for
  representing the complex-valued side are supported (reduced-size complex
  array, FFTPACK-style half-complex format and Hartley transform).
- Supports discrete cosine and sine transforms (Types I-IV)
- Makes use of CPU vector instructions when performing 2D and higher-dimensional
  transforms, if they are available.
- Has a small internal cache for transform plans, which speeds up repeated
  transforms of the same length (most significant for 1D transforms).
- Has optional multi-threading support for multidimensional transforms

%package devel

Summary:        C++ header for FFT
Provides:       %{name}-static = %{version}-%{release}

%description devel
PocketFFT for C++
=================

This is a heavily modified implementation of FFTPack [1,2], with the following
advantages:

- Strictly C++11 compliant
- More accurate twiddle factor computation
- Worst case complexity for transform sizes with large prime factors is
  `N*log(N)`, because Bluestein's algorithm [3] is used for these cases.
- Supports multidimensional arrays and selection of the axes to be transformed.
- Supports `float`, `double`, and `long double` types.
- Supports fully complex and half-complex (i.e. complex-to-real and
  real-to-complex) FFTs. For half-complex transforms, several conventions for
  representing the complex-valued side are supported (reduced-size complex
  array, FFTPACK-style half-complex format and Hartley transform).
- Supports discrete cosine and sine transforms (Types I-IV)
- Makes use of CPU vector instructions when performing 2D and higher-dimensional
  transforms, if they are available.
- Has a small internal cache for transform plans, which speeds up repeated
  transforms of the same length (most significant for 1D transforms).
- Has optional multi-threading support for multidimensional transforms

%prep
%autosetup -n %{name}-%{commit0}

%check
g++ pocketfft_demo.cc -o test
./test

%install
mkdir -p %{buildroot}%{_includedir}
install -p -m 644 pocketfft_hdronly.h %{buildroot}%{_includedir}

%files devel
%doc README.md
%license LICENSE.md
%{_includedir}/pocketfft_hdronly.h

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20230214.076cb3d-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20230214.076cb3d-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20230214.076cb3d-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20230214.076cb3d-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20230214.076cb3d-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 24 2023 Tom Rix <trix@redhat.com> - 1.0^git20230214.076cb3d-2
- Address review comments

* Sat Sep 23 2023 Tom Rix <trix@redhat.com> - 1.0^git20230214.076cb3d-1
- Initial package

