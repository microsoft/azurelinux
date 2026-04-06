# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           xeve
Version:        0.5.1
Release:        5%{?dist}
Summary:        Reference MPEG-5 Part 1 (EVC) encoder

License:        BSD-3-Clause
URL:            https://github.com/mpeg5/xeve
# Generated sources using Source1 script
Source0:        %{name}-free-%{version}.tar.gz
# Script to generate tarball with unencumbered sources
Source1:        %{name}_gen_free_tarball.sh
# Fix build on non-x86
Patch0:         %{name}-fix-build-on-non-x86.patch
# Link correctly to libm
Patch1:         %{name}-link-libm.patch

BuildRequires:  cmake >= 3.12
BuildRequires:  gcc
%ifarch aarch64
BuildRequires:  sse2neon-static
%endif

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
The eXtra-fast Essential Video Encoder (XEVE) is an
opensource and fast MPEG-5 EVC encoder.

MPEG-5 Essential Video Coding (EVC) is a video compression
standard of ISO/IEC Moving Picture Experts Group (MPEG).
The main goal of the EVC is to provide a significantly
improved compression capability over existing video coding
standards with timely publication of terms.

EVC defines two profiles, including "Baseline Profile" and "Main Profile".

The "Baseline profile" contains only technologies that are older than
20 years or otherwise freely available for use in the standard.
In addition, the "Main profile" adds a small number of additional tools,
each of which can be either cleanly disabled or switched to the
corresponding baseline tool on an individual basis.

This package only includes the "Baseline profile".


%package        libs
Summary:        Library files for %{name}

%description    libs
The %{name}-libs package contains libraries for applications to use
%{name}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1
%ifarch aarch64
rm src_base/neon/sse2neon.h
%endif

# Required for the CMake scripts to work
echo "v%{version}" > version.txt


%build
%cmake -DSET_PROF=BASE
%cmake_build


%install
%cmake_install

# We're not shipping static libraries shipped under private library subdir
rm -rfv %{buildroot}%{_libdir}/%{name}*


%files
%license COPYING
%doc README.md doc
%{_bindir}/%{name}*

%files libs
%license COPYING
%{_libdir}/lib%{name}*.so.0{,.*}

%files devel
%{_libdir}/lib%{name}*.so
%{_includedir}/%{name}*/
%{_libdir}/pkgconfig/%{name}*.pc


%changelog
* Sun Aug 24 2025 Neal Gompa <ngompa@fedoraproject.org> - 0.5.1-5
- Add patch to link libm properly
- Drop pc file definition patch

* Sun Aug 24 2025 Neal Gompa <ngompa@fedoraproject.org> - 0.5.1-4
- Add patch to fix pc file definition

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 13 2025 Dominik Mierzejewski <dominik@greysector.net> - 0.5.1-2
- fix build on non-x86
- unbundle sse2neon

* Sun Sep 29 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.5.1-1
- Updated to 0.5.1

* Wed Oct 18 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.4.3-1
- Initial package
