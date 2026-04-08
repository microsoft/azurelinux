# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sdl3_minver 3.4.0

# Features disabled for RHEL
%if 0%{?rhel}
%bcond_with static
%else
%bcond_without static
%endif

Name:           sdl2-compat
Version:        2.32.64
Release:        1%{?dist}
SourceLicense:  Zlib and Apache-2.0 and MIT and BSD-3-Clause
Summary:        SDL 2.0 runtime compatibility library using SDL 3.0
License:        Zlib
URL:            https://github.com/libsdl-org/sdl2-compat
Source0:        %{url}/archive/release-%{version}/%{name}-%{version}.tar.gz
# Multilib aware-header stub
Source1:        SDL2_config.h
Source2:        SDL2_revision.h

# Backports from upstream (0001~0500)

# Proposed patches (0501~1000)

# Fedora specific patches (1001+)
Patch1001:      sdl2-compat-sdlconfig-multilib.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  make
BuildRequires:  SDL3-devel >= %{sdl3_minver}
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
# This replaces SDL2
Obsoletes:      SDL2 < 2.30.11-2
Conflicts:      SDL2 < 2.32.50~
Provides:       SDL2 = %{version}
Provides:       SDL2%{?_isa} = %{version}
# This dlopens SDL3 (?!), so manually depend on it
Requires:       SDL3%{?_isa} >= %{sdl3_minver}

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio device.

This code is a compatibility layer; it provides a binary-compatible API for
programs written against SDL 2.0, but it uses SDL 3.0 behind the scenes.

If you are writing new code, please target SDL 3.0 directly and do not use
this layer.

%package devel
Summary:        Files to develop SDL 2.0 applications using SDL 3.0
# License of SDL-2.0 headers
License:        Zlib and Apache-2.0 and MIT and BSD-3-Clause
Requires:       %{name}%{?_isa} = %{version}-%{release}
# This replaces SDL2-devel
Obsoletes:      SDL2-devel < 2.30.11-2
Conflicts:      SDL2-devel < 2.32.50~
Provides:       SDL2-devel = %{version}
Provides:       SDL2-devel%{?_isa} = %{version}
%if ! %{with static}
# We don't provide the static library, but we want to replace SDL2-static anyway
Obsoletes:      SDL2-static < 2.30.11-2
Conflicts:      SDL2-static < 2.30.50~
%endif
# Add deps required to compile SDL apps
## For SDL_opengl.h
Requires:       pkgconfig(gl)
Requires:       pkgconfig(glu)
## For SDL_syswm.h
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xproto)

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio device.

This code is a compatibility layer; it provides a source-compatible API for
programs written against SDL 2.0, but it uses SDL 3.0 behind the scenes.

If you are writing new code, please target SDL 3.0 directly and do not use
this layer.


%if %{with static}
%package static
Summary:        Static library to develop SDL 2.0 applications using SDL 3.0
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
# This replaces SDL2-static
Obsoletes:      SDL2-static < 2.30.11-2
Conflicts:      SDL2-static < 2.32.50~
Provides:       SDL2-static = %{version}
Provides:       SDL2-static%{?_isa} = %{version}

%description static
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio device.

This code is a compatibility layer; it provides a static link library for
programs written against SDL 2.0, but it uses SDL 3.0 behind the scenes.
Note that applications that use this library will need to declare SDL2 as
a dependency manually, as the library is dlopen()'d to preserve APIs between
SDL-2.0 and SDL-3.0.

If you are writing new code, please target SDL 3.0 directly and do not use
this layer.
%endif

%prep
%autosetup -n %{name}-release-%{version} -S git_am


%build
%cmake %{?with_static:-DSDL2COMPAT_STATIC=ON}
%cmake_build


%install
%cmake_install

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}%{_includedir}/SDL2/SDL_config.h %{buildroot}%{_includedir}/SDL2/SDL_config-%{_arch}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/SDL2/SDL_config.h

# Rename SDL_revision.h to SDL_revision-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_revision.h wrapper
# TODO: Figure out how in the hell the SDL_REVISION changes between architectures on the same SRPM.
mv %{buildroot}%{_includedir}/SDL2/SDL_revision.h %{buildroot}%{_includedir}/SDL2/SDL_revision-%{_arch}.h
install -p -m 644 %{SOURCE2} %{buildroot}%{_includedir}/SDL2/SDL_revision.h


%check
%ctest


%files
%license LICENSE.txt
%doc README.md BUGS.md COMPATIBILITY.md
%{_libdir}/libSDL2-2.0.so.*

%files devel
%{_bindir}/sdl2-config
%{_datadir}/aclocal/sdl2.m4
%{_includedir}/SDL2/
%dir %{_libdir}/cmake/SDL2
%{_libdir}/cmake/SDL2/sdl2-config*.cmake
%{_libdir}/cmake/SDL2/SDL2Config*.cmake
%{_libdir}/cmake/SDL2/SDL2Targets*.cmake
%{_libdir}/cmake/SDL2/SDL2mainTargets*.cmake
%{_libdir}/libSDL2-2.0.so
%{_libdir}/libSDL2.so
%{_libdir}/pkgconfig/sdl2-compat.pc
%{_libdir}/libSDL2main.a
%{_libdir}/libSDL2_test.a
%{_libdir}/cmake/SDL2/SDL2_testTargets*.cmake


%if %{with static}
%files static
%{_libdir}/libSDL2.a
%{_libdir}/cmake/SDL2/SDL2-staticTargets*.cmake
%endif


%changelog
* Sun Feb 08 2026 Neal Gompa <ngompa@fedoraproject.org> - 2.32.64-1
- Update to 2.32.64

* Mon Feb 02 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 2.32.62-1
- Update to 2.32.62

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.56-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat May 10 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.32.56-1
- Update to 2.32.56

* Fri Apr 11 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.32.54-1
- Update to 2.32.54

* Sun Mar 16 2025 Simone Caronni <negativo17@gmail.com> - 2.32.52-1
- Update to 2.32.52.
- Drop patches.

* Mon Feb 10 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.32.50-2
- Backport fixes from upstream
  + Correctly handle SDL environment variables
  + Fix to avoid over optimizing away internal strlen

* Mon Feb 10 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.32.50-1
- Update to 2.32.50

* Mon Feb 03 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.30.52-1
- Update to 2.30.52

* Thu Jan 30 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.30.51-1
- Update to 2.30.51

* Wed Jan 22 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.30.50-1
- Update to 2.30.50 GA

* Sun Jan 19 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.30.50~git20250119.1126.208cea9-1
- Bump to new git snapshot

* Fri Jan 17 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.30.50~git20250116.10a9ed3-1
- Bump to new git snapshot

* Wed Jan 15 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.30.50~git20250107.c368587-3
- Backport fix adding some defines to fix mupen64plus FTBFS

* Mon Jan 13 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.30.50~git20250107.c368587-2
- Fix versioned Obsoletes

* Sun Jan 12 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.30.50~git20250107.c368587-1
- Bump to new git snapshot

* Mon Dec 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 2.30.50~git20241130.89e3c65-1
- Bump to a new snapshot

* Fri Oct 04 2024 Neal Gompa <ngompa@fedoraproject.org> - 2.30.50~git20241004.2115.e6b9f31-1
- Initial package

