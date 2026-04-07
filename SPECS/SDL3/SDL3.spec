# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# For the generated library symbol suffix
%if 0%{?__isa_bits} == 32
%global libsymbolsuffix %{nil}
%else
%global libsymbolsuffix ()(%{__isa_bits}bit)
%endif

# For declaring rich dependency on libdecor
%global libdecor_majver 0

%if 0%{?rhel}
# Disable static library on RHEL
%bcond_with static
# RHEL is Wayland-only, XWayland does not support XScrnSaver
%bcond_with xscrnsaver
%else
%bcond_without static
%bcond_without xscrnsaver
%endif


Name:           SDL3
Version:        3.4.0
Release:        3%{?dist}
Summary:        Cross-platform multimedia library
License:        Zlib AND MIT AND Apache-2.0 AND (Apache-2.0 OR MIT)
URL:            http://www.libsdl.org/
Source0:        http://www.libsdl.org/release/%{name}-%{version}.tar.gz
Source1:        SDL3_revision.h

# Patches from upstream

# Patches proposed upstream

BuildRequires:  git-core
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
# Technically, there are a few C++ files in SDL3, but none are used for the Linux build
# BuildRequires:  gcc-c++
BuildRequires:  alsa-lib-devel
BuildRequires:  fribidi-devel
BuildRequires:  libthai-devel
BuildRequires:  liburing-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  libXext-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
%if %{with xscrnsaver}
BuildRequires:  libXScrnSaver-devel
%endif
BuildRequires:  libXinerama-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXfixes-devel
BuildRequires:  systemd-devel
# For building man pages
BuildRequires:  perl-interpreter
BuildRequires:  pkgconfig(libusb-1.0)
# PulseAudio
BuildRequires:  pkgconfig(libpulse-simple)
# Jack
BuildRequires:  pkgconfig(jack)
# PipeWire
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pipewire-jack-audio-connection-kit-devel
# D-Bus
BuildRequires:  pkgconfig(dbus-1)
# IBus
BuildRequires:  pkgconfig(ibus-1.0)
# Wayland
BuildRequires:  pkgconfig(libdecor-%{libdecor_majver})
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)
# Vulkan
BuildRequires:  vulkan-devel
# KMS
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libdrm-devel
BuildRequires:	libXtst-devel

# Ensure libdecor is pulled in when libwayland-client is (rhbz#1992804)
Requires:       (libdecor-%{libdecor_majver}.so.%{libdecor_majver}%{libsymbolsuffix} if libwayland-client)

# Long ago forked hidraw customized for SDL
Provides:       bundled(hidraw)

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:        Files needed to develop Simple DirectMedia Layer applications
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Add deps required to compile SDL apps
## For SDL_opengl.h
Requires:       pkgconfig(gl)
Requires:       pkgconfig(glu)
## For SDL_syswm.h
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xproto)
%if ! %{with static}
# Remove any leftover -static subpackages
Obsoletes:      %{name}-static < %{version}-%{release}
%endif

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%if %{with static}
%package static
Summary:        Static libraries for SDL3
# Needed to keep CMake happy
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libraries for SDL3.
%endif

%package test
Summary:        Testing libraries for SDL3
# Needed to keep CMake happy
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description test
Testing libraries for SDL3.


%prep
%autosetup -S git_am
sed -e 's/\r//g' -i README.md WhatsNew.txt BUGS.txt LICENSE.txt CREDITS.md


%build
# Deal with new CMake policy around whitespace in LDFLAGS...
export LDFLAGS="%{shrink:%{build_ldflags}}"

%cmake \
    -DSDL_INSTALL_DOCS=ON \
    -DSDL_DEPS_SHARED=ON \
    -DSDL_SSE3=OFF \
    -DSDL_RPATH=OFF \
    -DSDL_VENDOR_INFO="%{?dist_vendor} %{version}-%{release}" \
    %{?with_static:-DSDL_STATIC=ON} \
    %{?with_static:-DCMAKE_POSITION_INDEPENDENT_CODE=ON} \
    %{!?with_xscrnsaver:-DSDL_X11_XSCRNSAVER=OFF} \
%ifarch ppc64le
    -DSDL_ALTIVEC=OFF \
%endif

%cmake_build


%install
%cmake_install

# Rename SDL_revision.h to SDL_revision-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_revision.h wrapper
# TODO: Figure out how in the hell the SDL_REVISION changes between architectures on the same SRPM.
mv %{buildroot}%{_includedir}/SDL3/SDL_revision.h %{buildroot}%{_includedir}/SDL3/SDL_revision-%{_arch}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/SDL3/SDL_revision.h


%files
%license LICENSE.txt
%doc BUGS.txt CREDITS.md README.md
%{_libdir}/libSDL3.so.0{,.*}

%files devel
%doc README.md WhatsNew.txt
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl3.pc
%dir %{_libdir}/cmake/SDL3
%{_libdir}/cmake/SDL3/SDL3Config*.cmake
%{_libdir}/cmake/SDL3/SDL3headersTargets*.cmake
%{_libdir}/cmake/SDL3/SDL3sharedTargets*.cmake
%{_includedir}/SDL3
%{_mandir}/man3/SDL*.3*

%if %{with static}
%files static
%license LICENSE.txt
%{_libdir}/libSDL3.a
%{_libdir}/cmake/SDL3/SDL3staticTargets*.cmake
%endif

%files test
%license LICENSE.txt
%{_libdir}/libSDL3_test.a
%{_libdir}/cmake/SDL3/SDL3testTargets*.cmake


%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Jan  5 2026 Tom Callaway <spot@fedoraproject.org> - 3.4.0-1
- update to 3.4.0

* Sun Dec 21 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 3.3.6-2
- Disable libXScrnSaver on RHEL

* Fri Dec 19 2025 Tom Callaway <spot@fedoraproject.org> - 3.3.6-1
- update to 3.3.6

* Mon Nov 24 2025 Tom Callaway <spot@fedoraproject.org> - 3.3.2-2
- drop BR: gcc-c++
- add BR: libXtst-devel
- thanks to "anotheruser" (bz2416555)

* Sun Oct 26 2025 Ding-Yi Chen  <dchen@fedoraproject.org> - 3.3.2-1
- update to 3.3.2

* Fri Oct  3 2025 Tom Callaway <spot@fedoraproject.org> - 3.2.24-1
- update to tree-too-tinty-floor ... err... 3.2.24

* Tue Aug  5 2025 Tom Callaway <spot@fedoraproject.org> - 3.2.20-1
- update to 3.2.20

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 04 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.16-1
- Update to 3.2.16

* Fri May 09 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.12-1
- Update to 3.2.12

* Fri Apr 11 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.10-1
- Update to 3.2.10

* Sun Mar 16 2025 Simone Caronni <negativo17@gmail.com> - 3.2.8-1
- Update to 3.2.8.
- Drop merged patch.

* Mon Feb 10 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.4-2
- Add fix for building against PipeWIre 1.3.x

* Sat Feb 08 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.4-1
- Update to 3.2.4

* Mon Feb 03 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2

* Wed Jan 22 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0 (SDL3 GA)

* Thu Jan 16 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.1.10-1
- Update to 3.1.10

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.1.8-2
- Disable static library subpackage on RHEL

* Thu Jan 09 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.1.8-1
- Update to 3.1.8
- Enable man pages

* Mon Dec 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 3.1.6-1
- Update to 3.1.6
- Split testing library into subpackage

* Fri Oct 04 2024 Neal Gompa <ngompa@fedoraproject.org> - 3.1.3-1
- Initial package

