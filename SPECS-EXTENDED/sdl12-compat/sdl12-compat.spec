Name:           sdl12-compat
Version:        1.2.68
Release:        4%{?dist}
Summary:        SDL 1.2 runtime compatibility library using SDL 2.0
# mp3 decoder code is MIT-0/PD
# SDL_opengl.h is zlib and MIT
License:        zlib and (Public Domain or MIT-0) and MIT
URL:            https://github.com/libsdl-org/sdl12-compat
Source0:        %{url}/archive/release-%{version}/%{name}-%{version}.tar.gz
# Multilib aware-header stub
Source1:        SDL_config.h

# Backports from upstream (0001~0500)

# Proposed patches (0501~1000)

# Fedora specific patches (1001+)
Patch1001:      sdl12-compat-sdlconfig-multilib.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  make
BuildRequires:  SDL2-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
# This replaces SDL
Obsoletes:      SDL < 1.2.15-49
Conflicts:      SDL < 1.2.50
Provides:       SDL = %{version}
Provides:       SDL%{?_isa} = %{version}
# This dlopens SDL2 (?!), so manually depend on it
Requires:       SDL2%{?_isa} >= 2.0.18

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio device.

This code is a compatibility layer; it provides a binary-compatible API for
programs written against SDL 1.2, but it uses SDL 2.0 behind the scenes.

If you are writing new code, please target SDL 2.0 directly and do not use
this layer.

%package devel
Summary:        Files to develop SDL 1.2 applications using SDL 2.0
Requires:       %{name}%{?_isa} = %{version}-%{release}
# This replaces SDL-devel
Obsoletes:      SDL-devel < 1.2.15-49
Conflicts:      SDL-devel < 1.2.50
Provides:       SDL-devel = %{version}
Provides:       SDL-devel%{?_isa} = %{version}
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
programs written against SDL 1.2, but it uses SDL 2.0 behind the scenes.

If you are writing new code, please target SDL 2.0 directly and do not use
this layer.


%package static
Summary:        Static library to develop SDL 1.2 applications using SDL 2.0
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
# This replaces SDL-static
Obsoletes:      SDL-static < 1.2.15-49
Conflicts:      SDL-static < 1.2.50
Provides:       SDL-static = %{version}
Provides:       SDL-static%{?_isa} = %{version}

%description static
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio device.

This code is a compatibility layer; it provides a static link library for
programs written against SDL 1.2, but it uses SDL 2.0 behind the scenes.
Note that applications that use this library will need to declare SDL2 as
a dependency manually, as the library is dlopen()'d to preserve APIs between
SDL-1.2 and SDL-2.0.

If you are writing new code, please target SDL 2.0 directly and do not use
this layer.


%prep
%autosetup -n %{name}-release-%{version} -S git_am


%build
%cmake -DSTATICDEVEL=ON
%cmake_build


%install
%cmake_install

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}/%{_includedir}/SDL/SDL_config.h %{buildroot}/%{_includedir}/SDL/SDL_config-%{_arch}.h
install -m644 %{SOURCE1} %{buildroot}/%{_includedir}/SDL/SDL_config.h

# Delete leftover static files
#rm -rf %{buildroot}%{_libdir}/*.a


%files
%license LICENSE.txt
%doc README.md BUGS.md COMPATIBILITY.md
%{_libdir}/libSDL-1.2.so.*

%files devel
%{_bindir}/sdl-config
%{_datadir}/aclocal/sdl.m4
%{_includedir}/SDL/
%{_libdir}/libSDL-1.2.so
%{_libdir}/libSDL.so
%{_libdir}/pkgconfig/sdl12_compat.pc

%files static
%{_libdir}/libSDL.a
%{_libdir}/libSDLmain.a


%changelog
* Mon Mar 17 2025 Jyoti kanase <v-jykanase@microsoft.com> - 1.2.68-4
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 26 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.2.68-1
- Update to 1.2.68

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 10 2023 Petr Pisar <ppisar@redhat.com> - 1.2.60-3
- Fix a hang in SDL_FreeYUVOverlay() (RH#2173510)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Oct 30 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.2.60-1
- Update to 1.2.60

* Fri Sep 16 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.2.56-1
- Update to 1.2.56 (RH#2127545)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 03 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.2.52-1
- Update to 1.2.52 (RH#2060590)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1~git.20211125.4e4527a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 11 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.0.1~git.20211125.4e4527a-3
- Conflict with all old SDL subpackages properly

* Wed Dec 01 2021 Neal Gompa <ngompa@centosproject.org> - 0.0.1~git.20211125.4e4527a-2
- Obsolete the SDL package properly

* Sat Nov 27 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.0.1~git.20211125.4e4527a-1
- Update to new snapshot release

* Sun Nov 07 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.0.1~git.20211107.a10d6b6-1
- Update to new snapshot release

* Sun Sep 26 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.0.1~git.20210926.c6cfc8f-1
- Update to new snapshot release
- Ensure SDL2 dependency is arched

* Sun Sep 12 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.0.1~git.20210909.a98590a-1
- Update to new snapshot release

* Thu Aug 26 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.0.1~git.20210825.b5f7170-1
- Update to new snapshot release

* Sun Aug 22 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.0.1~git.20210814.a3bfcb2-1
- Update to new snapshot release

* Sun Jul 25 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.0.1~git.20210719.aa9919b-1
- Update to new snapshot release

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1~git.20210709.51254e5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210709.51254e5-1
- Update to new snapshot release

* Tue Jun 29 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210628.cf47f88-1
- Update to new snapshot release

* Mon Jun 28 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210624.08b5def-1
- Update to new snapshot release

* Sun Jun 20 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210619.4ad7ba6-2
- Update devel dependencies based on upstream feedback

* Sun Jun 20 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210619.4ad7ba6-1
- Update to new snapshot release

* Sun Jun 20 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210618.f44f295-2
- Add devel dependencies expected by SDL packages to devel subpackage

* Fri Jun 18 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210618.f44f295-1
- Update to new snapshot release

* Sun Jun 13 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210612.44f299f-1
- Update to new snapshot release
- Update license tag information

* Sat Jun 12 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210612.c0504eb-1
- Update to new snapshot release

* Thu Jun 10 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210610.21830e8-1
- Update to new snapshot release
- Add static link library for non-RHEL

* Wed Jun 09 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210609.efe9791-1
- Update to new snapshot release
- Refresh patch for multilib support

* Thu Jun 03 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210602.cc5826a-3
- Fix for multilib support

* Thu Jun 03 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210602.cc5826a-2
- Add missing SDL2 dependency and fix Obsoletes

* Wed Jun 02 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210602.cc5826a-1
- Update to new snapshot release

* Sat May 29 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210528.646ecd7-0.1
- Update to new snapshot release

* Fri May 28 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210527.a915ff1-0.1
- Update to new snapshot release

* Wed May 26 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210526.848ad42-0.1
- Update to new snapshot release

* Mon May 24 2021 Neal Gompa <ngompa13@gmail.com> - 0.0.1~git.20210524.cf71450-0.1
- Update to new snapshot release

* Sat May 15 2021 Neal Gompa <ngompa13@gmail.com> - 0~git.20210515.9f2d88a-1
- Initial package
