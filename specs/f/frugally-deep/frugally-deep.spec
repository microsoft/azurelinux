# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# For testing
# Depends on downloading and being in a git repo
%bcond_with test

# Header only package
%global debug_package %{nil}

Summary:        Header-only library for using Keras (TensorFlow) models in C++
Name:           frugally-deep
License:        MIT
# Main license is MIT
# BSD-2-Clause is only for cmake/HunterGate.cmake and that is not distributed
Version:        0.15.30
Release: 10%{?dist}

URL:            https://github.com/Dobiasd/frugally-deep
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  fplus-devel
%if 0%{?suse_version}
BuildRequires:  nlohmann_json-devel
%else
BuildRequires:  json-devel
%endif
BuildRequires:  gcc-c++

%description
Would you like to build/train a model using Keras/Python? And would
you like to run the prediction (forward pass) on your model in C++
without linking your application against TensorFlow? Then
frugally-deep is exactly for you.

frugally-deep

* is a small header-only library written in modern and pure C++.
* is very easy to integrate and use.
* depends only on FunctionalPlus, Eigen and json - also header-only
  libraries.
* supports inference (model.predict) not only for sequential models
  but also for computational graphs with a more complex topology,
  created with the functional API.
* re-implements a (small) subset of TensorFlow, i.e., the operations
  needed to support prediction.
* results in a much smaller binary size than linking against TensorFlow.
* works out-of-the-box also when compiled into a 32-bit executable.
  (Of course, 64 bit is fine too.)
* avoids temporarily allocating (potentially large chunks of)
  additional RAM during convolutions (by not materializing the im2col
  input matrix).
* utterly ignores even the most powerful GPU in your system and uses
  only one CPU core per prediction. ;-)
* but is quite fast on one CPU core, and you can run multiple
  predictions in parallel, thus utilizing as many CPUs as you like
  to improve the overall prediction throughput of your
  application/pipeline.

%package devel

Summary:        Header-only library for using Keras (TensorFlow) models in C++
Provides:       %{name}-static = %{version}-%{release}

%description devel
Would you like to build/train a model using Keras/Python? And would
you like to run the prediction (forward pass) on your model in C++
without linking your application against TensorFlow? Then
frugally-deep is exactly for you.

frugally-deep

* is a small header-only library written in modern and pure C++.
* is very easy to integrate and use.
* depends only on FunctionalPlus, Eigen and json - also header-only
  libraries.
* supports inference (model.predict) not only for sequential models
  but also for computational graphs with a more complex topology,
  created with the functional API.
* re-implements a (small) subset of TensorFlow, i.e., the operations
  needed to support prediction.
* results in a much smaller binary size than linking against TensorFlow.
* works out-of-the-box also when compiled into a 32-bit executable.
  (Of course, 64 bit is fine too.)
* avoids temporarily allocating (potentially large chunks of)
  additional RAM during convolutions (by not materializing the im2col
  input matrix).
* utterly ignores even the most powerful GPU in your system and uses
  only one CPU core per prediction. ;-)
* but is quite fast on one CPU core, and you can run multiple
  predictions in parallel, thus utilizing as many CPUs as you like
  to improve the overall prediction throughput of your
  application/pipeline.

%prep
%autosetup -p1 -n %{name}-%{version}

# cmake changed
sed -i -e 's@cmake_minimum_required(VERSION 3.2)@cmake_minimum_required(VERSION 3.5)@' CMakeLists.txt

%build
%cmake 
%cmake_build

%if %{with test}
%check
%ctest
%endif

%install
%cmake_install

%files devel
%dir %_includedir/fdeep
%dir %_libdir/cmake/%{name}
%license LICENSE
%doc README.md
%_includedir/fdeep/*
%_libdir/cmake/%{name}/*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.30-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Feb 28 2025 Tom Rix <Tom.Rix@amd.com> - 0.15.30-8
- cmake changed

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 2 2024 Tom Rix <Tom.Rix@amd.com> - 0.15.30-6
- Build on TW
- Fix dir ownership

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Tom Rix <trix@redhat.com> - 0.15.30-2
- Reduce license to MIT
- Remove unneeded cmake arg

* Mon Jan 15 2024 Tom Rix <trix@redhat.com> - 0.15.30-1
- Update to 0.15.30

* Fri Dec 15 2023 Tom Rix <trix@redhat.com> - 0.15.26-1
- Initial package
