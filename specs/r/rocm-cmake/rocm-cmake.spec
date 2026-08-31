# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# there is no debug package - this is just cmake modules
%global debug_package %{nil}

%global rocm_release 6.4
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

Name:     rocm-cmake
Version:  %{rocm_version}
Release:  2%{?dist}
Summary:  CMake modules for common build and development tasks for ROCm
License:  MIT
URL:      https://github.com/ROCm/rocm-cmake
Source:   %{url}/archive/rocm-%{version}.tar.gz#/rocm-cmake-rocm-%{version}.tar.gz

BuildArch: noarch
BuildRequires: cmake
Requires: cmake

%description
rocm-cmake is a collection of CMake modules for common build and development
tasks within the ROCm project. It is therefore a build dependency for many of
the libraries that comprise the ROCm platform.

rocm-cmake is not required for building libraries or programs that use ROCm; it
is required for building some of the libraries that are a part of ROCm.


%prep
%autosetup -n rocm-cmake-rocm-%{version}


%build
%cmake
%cmake_build


%install
%cmake_install

if [ -f %{buildroot}%{_prefix}/share/doc/rocm-cmake/LICENSE ]; then
    rm %{buildroot}%{_prefix}/share/doc/rocm-cmake/LICENSE
fi

%files
%dir %{_datadir}/rocm
%dir %{_datadir}/rocmcmakebuildtools

%doc CHANGELOG.md
%license LICENSE
%{_datadir}/rocm/*
%{_datadir}/rocmcmakebuildtools/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Apr 16 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.0-1
- Update to 6.4.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 8 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sat Nov 9 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed



