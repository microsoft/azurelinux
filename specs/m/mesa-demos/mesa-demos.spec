# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global demodir %{_libdir}/mesa

Summary: Mesa demos
Name: mesa-demos
Version: 9.0.0
Release: 11%{?dist}
# SPDX
License: MIT
URL: http://www.mesa3d.org
Source: https://archive.mesa3d.org/demos/%{name}-%{version}.tar.xz
# Patch pointblast/spriteblast/dinoshade out for legal reasons
# (not in public domain)
Patch0: mesa-demos-8.5.0-legal.patch
# Install glsl demos data
Patch1: mesa-demos-system-data.patch
BuildRequires: meson
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: pkgconfig
BuildRequires: freeglut-devel
BuildRequires: glslang
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: libGLU-devel
BuildRequires: libXext-devel
BuildRequires: libdecor-devel
BuildRequires: libxcb-devel
BuildRequires: libxkbcommon-devel
BuildRequires: libxkbcommon-x11-devel
BuildRequires: vulkan-loader-devel
BuildRequires: wayland-devel
BuildRequires: wayland-protocols-devel
BuildRequires: freetype-devel

%description
This package provides some demo applications for testing Mesa.

%package -n glx-utils
Summary: GLX utilities
Provides: glxinfo glxinfo%{?__isa_bits}
# mesa-demos' glx-utils used to provide xdriinfo for a long time, but that has
# always been an additional external source, so it was split into its own
# package.
# Recommend it here so that it still gets pulled at first for anyone expecting
# it to be there, but it doesn't need to be a hard requirement anymore.
Recommends: xdriinfo

%description -n glx-utils
The glx-utils package provides the glxinfo and glxgears utilities.

%package -n egl-utils
Summary: EGL utilities
Provides: eglinfo es2_info

%description -n egl-utils
The egl-utils package provides the eglinfo, eglgears, es2_info and es2gears utilities.

%prep
%setup -q -n %{name}-%{version}
%patch -P0 -p1 -b .legal
%patch -P1 -p1 -b .systemdata

# These two files are distributable, but non-free (lack of permission to modify).
rm -rf src/demos/pointblast.c
rm -rf src/demos/spriteblast.c

%build
%meson \
    --bindir=%{demodir} \
    -Dwith-system-data-files=true \
    -Dx11=enabled \
    -Dwayland=enabled \
    -Degl=enabled \
    -Dgles2=enabled \
    -Dvulkan=enabled \
    -Dlibdrm=enabled \
    -Dosmesa=disabled

%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/src/xdemos/glxgears %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/src/xdemos/glxinfo %{buildroot}%{_bindir}
%if 0%{?__isa_bits} != 0
install -m 0755 %{_vpath_builddir}/src/xdemos/glxinfo %{buildroot}%{_bindir}/glxinfo%{?__isa_bits}
%endif

install -m 0755 %{_vpath_builddir}/src/egl/opengl/eglinfo %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/src/egl/opengl/eglgears_x11 %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/src/egl/opengl/eglgears_wayland %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/src/egl/opengles2/es2_info %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/src/egl/opengles2/es2gears_x11 %{buildroot}%{_bindir}
install -m 0755 %{_vpath_builddir}/src/egl/opengles2/es2gears_wayland %{buildroot}%{_bindir}

%check

%files
%{demodir}
%{_datadir}/%{name}/

%files -n glx-utils
%{_bindir}/glxinfo*
%{_bindir}/glxgears

%files -n egl-utils
%{_bindir}/eglinfo
%{_bindir}/eglgears_x11
%{_bindir}/eglgears_wayland
%{_bindir}/es2_info
%{_bindir}/es2gears_x11
%{_bindir}/es2gears_wayland

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 01 2024 José Relvas <jrelvas@proton.me> - 9.0.0-7
- Add eglgears and es2gears (eglgears_x11,eglgears_wayland,es2gears_x11,es2gears_wayland)
  to egl-utils subpackage

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 03 2023 Erico Nunes <ernunes@redhat.com> - 9.0.0-4
- Split xdriinfo into its own package
- Remove xdriinfo additional source build and autotools dependencies

* Thu Sep 07 2023 José Expósito <jexposit@redhat.com>
- SPDX migration: license is already SPDX compatible

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 9.0.0-2
- Install all necessary shader files (#1373299)

* Mon Mar 27 2023 Erico Nunes <ernunes@redhat.com> - 9.0.0-1
- Update to 9.0.0
- Enable vulkan demos

* Fri Feb 03 2023 Erico Nunes <ernunes@redhat.com> - 8.5.0-1
- Update to 8.5.0
- Change build system to meson

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-15.20210504git0f9e7d9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-14.20210504git0f9e7d9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-13.20210504git0f9e7d9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-12.20210504git0f9e7d9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 04 2021 Adam Jackson <ajax@redhat.com> - 8.4.0-11.20210504git0f9e7d995a14f15
- Sync with upstream to drop the glew dependency

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-9.20181118git1830dcb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Tom Stellard <tstellar@redhat.com> - 8.4.0-8.20181118git1830dcb
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-7.20181118git1830dcb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-6.20181118git1830dcb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 04 2019 Gwyn Ciesla <gwync@protonmail.com> - 8.4.0-5.20181118git1830dcb
- Rebuilt for new freeglut.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-4.20181118git1830dcb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-3.20181118git1830dcb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Lyude Paul <lyude@redhat.com> - 8.4.0-2.20181118git1830dcb
- Start using proper git version strings for rawhide
- Enabling building of wayland and freetype demos

* Sun Nov 18 2018 Lyude Paul <lyude@redhat.com> - 8.4.0-1
- New git snapshot

* Thu Aug 23 2018 Nicolas Chauvet <kwizart@gmail.com> - 8.3.0-12
- Rebuilt for glew 2.1.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 27 2017 Adam Jackson <ajax@redhat.com> - 8.3.0-9
- New git snapshot

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 13 2017 Hans de Goede <hdegoede@redhat.com> - 8.3.0-6
- Fix xdriinfo not working with libglvnd (rhbz#1429894)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Orion Poplawski <orion@cora.nwra.com> - 8.3.0-4
- Rebuild for glew 2.0.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Adam Jackson <ajax@redhat.com> - 8.3.0-2
- Rebuild for glew 1.13

* Fri Dec 18 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.3.0-1
- 8.3.0

* Thu Dec 03 2015 Adam Jackson <ajax@redhat.com> 8.2.0-5
- New git snap
- Add EGL/GLES buildreqs and egl-utils subpackage

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 8.2.0-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.2.0-1
- 8.2.0 upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 17 2013 Dave Airlie <airlied@redhat.com> - 8.1.0-5
- rebuilt for glew 1.10

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Adam Jackson <ajax@redhat.com> 8.1.0-3
- Build with --as-needed so glxinfo doesn't needlessly drag in GLEW

* Wed Feb 27 2013 Adam Jackson <ajax@redhat.com> 8.1.0-2
- Copy glxinfo to glxinfo%%{__isa_bits}, to allow people to check that their
  compatibility drivers are working.

* Sun Feb 24 2013 Dave Airlie <airlied@redhat.com> 8.1.0-1
- package upstream demos release 8.1.0 (mainly for new glxinfo)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.1-2.20121218git6eef979
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Tom Callaway <spot@fedoraproject.org> - 8.0.1-1.20121218git6eef979
- update to 8.0.1 (git checkout from 20121218)
- update xdriinfo to 1.0.4
- remove non-free files (bz892925)

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 7.10-9.20101028
- Rebuild for glew 1.9.0

* Fri Jul 27 2012 Kalev Lember <kalevlember@gmail.com> - 7.10-8.20101028
- Rebuilt for GLEW soname bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-7.20101028
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-6.20101028
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 ajax@redhat.com - 7.10-5.20101028
- Rebuild for new glew soname

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-4.20101028
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 01 2010 Adam Jackson <ajax@redhat.com> 7.10-3.20101028
- Install rgba images too (#640688)

* Sat Oct 30 2010 Dave Airlie <airlied@redhat.com> 7.10-2.20101028
- fix install of gears/info (#647947)

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 7.10-1.20101028
- Today's git snapshot
- Arbitrary EVR bump to be newer than when the mesa source package dropped
  the demos subpackage.

* Tue Jun 15 2010 Jerome Glisse <jglisse@redhat.com> 7.7
- Initial build.
