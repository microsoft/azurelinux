# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 faa23f21fc677af5792825dc30cb1ccef4bf33a6
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%if 0%{?rhel} >= 10
%global compositor mutter
%global x11_tests 0
%elif 0%{?rhel}
%global x11_tests 1
%else
%global compositor weston
%global x11_tests 1
%endif

Name:           libglvnd
Version:        1.7.0
Release:        8%{?dist}
# Provide an upgrade path from the negativo17.org pkgs which have Epoch 1
Epoch:          1
Summary:        The GL Vendor-Neutral Dispatch library

License:        MIT-feh AND MIT-Modern-Variant AND BSD-1-Clause AND BSD-3-Clause AND GPL-3.0-or-later WITH Autoconf-exception-macro
URL:            https://gitlab.freedesktop.org/glvnd/libglvnd
Source0:        %{url}/-/archive/v%{version}/%{name}-%{version}.tar.gz
Patch1:         0001-glx-Add-another-fallback-library-name.patch

BuildRequires: make
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  python3-rpm-macros
BuildRequires:  python3-libxml2
BuildRequires:  pkgconfig(glproto)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
%if 0%{?x11_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif
%if 0%{?compositor:1}
BuildRequires:  mesa-dri-drivers
BuildRequires:  %{compositor}
BuildRequires:  xwayland-run
%endif

%{?_without_mesa_glvnd_default:
%global __provides_exclude_from %{_libdir}/%{name}
%global __requires_exclude_from %{_libdir}/%{name}
}

%description
libglvnd is an implementation of the vendor-neutral dispatch layer for
arbitrating OpenGL API calls between multiple vendors on a per-screen basis.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-opengl%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-gles%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-glx%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-egl%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-core-devel%{?_isa} = %{epoch}:%{version}-%{release}
# Required by any glx.h users.
Requires:       libX11-devel%{?_isa}
# We might split into more sub-packages
Obsoletes:      mesa-libGLES-devel < 19.3.0~rc1
Provides:       mesa-libGLES-devel = %{epoch}:%{version}-%{release}
Provides:       mesa-libGLES-devel%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:      mesa-khr-devel < 19.3.0~rc1
Provides:       mesa-khr-devel = %{epoch}:%{version}-%{release}
Provides:       mesa-khr-devel%{?_isa} = %{epoch}:%{version}-%{release}
Provides:       libGLES-devel = %{epoch}:%{version}-%{release}
Provides:       libGLES-devel%{?_isa} = %{epoch}:%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        core-devel
Summary:        Core development files for %{name}

%description core-devel
The %{name}-core-devel package is a bootstrap trick for Mesa, which wants
to build against the %{name} headers but does not link against any of
its libraries (and, initially, has file conflicts with them). If you are
not Mesa you almost certainly want %{name}-devel instead.


%package        opengl
Summary:        OpenGL support for libglvnd
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description    opengl
libOpenGL is the common dispatch interface for the workstation OpenGL API.


%package        gles
Summary:        GLES support for libglvnd
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%{!?_without_mesa_glvnd_default:
%{!?flatpak_runtime:
# mesa is the default EGL implementation provider
Requires:       mesa-libEGL%{?_isa} >= 13.0.4-1
}
Obsoletes:      mesa-libGLES < 19.3.0~rc1
Provides:       mesa-libGLES
Provides:       mesa-libGLES%{?_isa}
Provides:       libGLES
Provides:       libGLES%{?_isa}
}

%description    gles
libGLESv[12] are the common dispatch interface for the GLES API.


%package        egl
Summary:        EGL support for libglvnd
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%{!?_without_mesa_glvnd_default:
%{!?flatpak_runtime:
# mesa is the default EGL implementation provider
Requires:       mesa-libEGL%{?_isa} >= 13.0.4-1
}
Provides:       libEGL
Provides:       libEGL%{?_isa}
}

%description    egl
libEGL are the common dispatch interface for the EGL API.


%package        glx
Summary:        GLX support for libglvnd
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%{!?_without_mesa_glvnd_default:
%{!?flatpak_runtime:
# mesa is the default GL implementation provider
Requires:       mesa-libGL%{?_isa} >= 13.0.4-1
}
Provides:       libGL
Provides:       libGL%{?_isa}
}

%description    glx
libGL and libGLX are the common dispatch interface for the GLX API.


%prep
%autosetup -p1 -n %{name}-v%{version}-%{?commit0}
autoreconf -vif

%build
export PYTHON=%{__python3}
#Prefer asm and tls for x86* and ppc64*
#armhfp and aarch64 fallback to asm and tsd
#Others arches fallback to pure-c and tls.
%configure \
  --disable-static \
  --enable-asm \
  --enable-tls

%make_build V=1


%install
%make_install INSTALL="install -p"
find %{buildroot} -name '*.la' -delete

%{?_without_mesa_glvnd_default:
# Avoid conflict with mesa-libGL
mkdir -p %{buildroot}%{_libdir}/%{name}/
for l in libEGL libGL libGLESv1_CM libGLESv2 libGLX; do
  mv %{buildroot}%{_libdir}/${l}.so* \
    %{buildroot}%{_libdir}/%{name}/
done
}

# Create directory layout
mkdir -p %{buildroot}%{_sysconfdir}/glvnd/egl_vendor.d/
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d/
mkdir -p %{buildroot}%{_sysconfdir}/egl/egl_external_platform.d/
mkdir -p %{buildroot}%{_datadir}/egl/egl_external_platform.d/


%check
%if 0%{?x11_tests}
export DO_X11_TESTS=1
xvfb-run -s '-screen 0 640x480x24' -d make check V=1 || \
%ifarch s390x ppc64
    :
%else
    (cat `find . -name test-suite.log` ; exit 1)
%endif
%endif
%if 0%{?compositor:1}
export DO_X11_TESTS=1
xwfb-run -c %{compositor} -- make check V=1 || \
%ifarch s390x ppc64
    :
%else
    (cat `find . -name test-suite.log` ; exit 1)
%endif
%endif


%ldconfig_scriptlets
%files
%doc README.md
%dir %{_sysconfdir}/glvnd/
%dir %{_datadir}/glvnd/
%{_libdir}/libGLdispatch.so.0*

%ldconfig_scriptlets opengl
%files opengl
%{_libdir}/libOpenGL.so.0*

%ldconfig_scriptlets gles
%files gles
%if 0%{?_without_mesa_glvnd_default}
%{_libdir}/%{name}/libGLES*.so.*
%else
%{_libdir}/libGLES*.so.*
%endif

%ldconfig_scriptlets glx
%files glx
%if 0%{?_without_mesa_glvnd_default}
%{_libdir}/%{name}/libGL.so.*
%{_libdir}/%{name}/libGLX.so.*
%else
%{_libdir}/libGL.so.*
%{_libdir}/libGLX.so.*
%endif

%ldconfig_scriptlets egl
%files egl
%dir %{_sysconfdir}/glvnd/egl_vendor.d/
%dir %{_datadir}/glvnd/egl_vendor.d/
%dir %{_sysconfdir}/egl/
%dir %{_sysconfdir}/egl/egl_external_platform.d/
%dir %{_datadir}/egl/
%dir %{_datadir}/egl/egl_external_platform.d/
%if 0%{?_without_mesa_glvnd_default}
%{_libdir}/%{name}/libEGL*.so.*
%else
%{_libdir}/libEGL*.so.*
%endif

%files core-devel
%dir %{_includedir}/glvnd/
%{_includedir}/glvnd/*.h
%{_libdir}/pkgconfig/libglvnd.pc

%files devel
%dir %{_includedir}/EGL/
%dir %{_includedir}/GL/
%dir %{_includedir}/GLES/
%dir %{_includedir}/GLES2/
%dir %{_includedir}/GLES3/
%dir %{_includedir}/KHR/
%{_includedir}/EGL/*.h
%{_includedir}/GL/*.h
%{_includedir}/GLES/*.h
%{_includedir}/GLES2/*.h
%{_includedir}/GLES3/*.h
%{_includedir}/KHR/*.h
%{_libdir}/lib*.so
%if 0%{?_without_mesa_glvnd_default}
%{_libdir}/%{name}/lib*.so
%endif
%{_libdir}/pkgconfig/gl*.pc
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/pkgconfig/opengl.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 05 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.7.0-6
- Test on wayland/Xwayland

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 15 2023 Dave Airlie <airlied@redhat.com> - 1:1.7.0-2
- SPDX license update

* Thu Sep 14 2023 Nicolas Chauvet <kwizart@gmail.com> - 1:1.7.0-1
- Update to 1.7.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 22 2022 Nicolas Chauvet <kwizart@gmail.com> - 1:1.6.0-1
- Update to 1.6.0

* Tue Aug 23 2022 Nicolas Chauvet <kwizart@gmail.com> - 1:1.5.0-1
- Update to 1.5.0

* Fri Aug 12 2022 Nicolas Chauvet <kwizart@gmail.com> - 1:1.4.0-4
- Backport patch for BTI enabled aarch64 hw - rhbz#2111900

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Nicolas Chauvet <kwizart@gmail.com> - 1:1.4.0-1
- Update to 1.4.0

* Sun Oct 24 2021 Leigh Scott <leigh123linux@gmail.com> - 1:1.3.4-2
- Rebuilt

* Wed Aug 25 2021 Nicolas Chauvet <kwizart@gmail.com> - 1:1.3.4-1
- Update to 1.3.4

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 01 2021 Nicolas Chauvet <kwizart@gmail.com> - 1:1.3.3-1
- Update to 1.3.3

* Mon Apr 19 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 1:1.3.2-4
- Add upstream patch to fix egl call failures with nvidia libs installed

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Nicolas Chauvet <kwizart@gmail.com> - 1:1.3.2-1
- Update to 1.3.2

* Fri May 08 2020 Nicolas Chauvet <kwizart@gmail.com> - 1:1.3.1-2
- Forward few patches from rhel

* Mon Feb 24 2020 Nicolas Chauvet <kwizart@gmail.com> - 1:1.3.1-1
- Update to 1.3.1

* Wed Feb 19 2020 Kalev Lember <klember@redhat.com> - 1:1.3.0-1
- Update to 1.3.0

* Wed Feb 19 2020 Kalev Lember <klember@redhat.com> - 1:1.2.0-10
- Bump mesa-libGLES obsoletes version as well

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 1:1.2.0-8
- Bump mesa-libGLES-devel and mesa-khr-devel obsoletes versions

* Sat Oct 26 2019 Nicolas Chauvet <kwizart@gmail.com> - 1:1.2.0-7
- Move from core to main

* Fri Oct 25 2019 Peter Robinson <pbrobinson@gmail.com> - 1:1.2.0-6
- Add %%{?_isa} too, just for fun!

* Fri Oct 25 2019 Peter Robinson <pbrobinson@gmail.com> - 1:1.2.0-5
- provides shouldn't have been versioned

* Fri Oct 25 2019 Peter Robinson <pbrobinson@gmail.com> - 1:1.2.0-4
- Also provide old libGLES-devel

* Fri Oct 25 2019 Peter Robinson <pbrobinson@gmail.com> - 1:1.2.0-4
- Obsolete/Provide the bits moved from mesa so builds don't break

* Fri Oct 25 2019 Pete Walter <pwalter@fedoraproject.org> - 1:1.2.0-2
- Sync headers with mesa

* Thu Oct 24 2019 Leigh Scott <leigh123linux@gmail.com> - 1:1.2.0-1
- libglvnd 1.2.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 14 2019 Adam Jackson <ajax@redhat.com> - 1.1.1-4
- libglvnd 1.1.1

* Thu Feb 14 2019 Nicolas Chauvet <kwizart@gmail.com> - 1:1.1.0-4.gitf92208b
- Update snapshot

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.1.0-2
- Add upstream python3 PR

* Thu Aug 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.1.0-1
- Update to 1.1.0 release

* Tue Jul 24 2018 Dave Airlie <airlied@redhat.com> - 1.0.1-0.9.git5baa1e5
- rename fallback from fedora to system

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.1-0.8.git5baa1e5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Adam Jackson <ajax@redhat.com> - 1.0.1-0.7.git5baa1e5
- Add another fallback GLX library name

* Thu Apr 26 2018 Adam Jackson <ajax@redhat.com> - 1.0.1-0.6.git5baa1e5
- Enable %%check for all but ppc64 and s390x, which has known but low-impact
  failures
- Simplify %%release

* Wed Apr 18 2018 Adam Jackson <ajax@redhat.com> - 1.0.1-0.5.20180327git5baa1e5
- Go back to Requires: mesa-*, the fallout is too great (#1568881 etc)

* Fri Apr 13 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.0.1-0.4.20180327git5baa1e5
- Update snapshot to 20180327

* Thu Mar 15 2018 Adam Jackson <ajax@redhat.com> - 1.0.1-0.3.20180226gitb029c24
- Use Recommends: mesa-* not Requires.
- (Trivially) switch the build to python3

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1:1.0.1-0.2.20180226gitb029c24
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.0.1-0.1.20180226gitb029c24
- Update snapshot to 20180226
- Update scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:1.0.0-1
- Update to 1.0.0 release

* Wed Aug 23 2017 Nicolas Chauvet <kwizart@gmail.com> - 1:0.2.999-24.20170818git8d4d03f
- Update snapshot to 20170818

* Mon Aug 14 2017 Ville Skyttä <ville.skytta@iki.fi> - 1:0.2.999-23.20170620gitd850cdd
- Own %%{_sysconfdir}/egl and %%{_datadir}/egl dirs

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.999-22.20170620gitd850cdd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.999-21.20170620gitd850cdd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1:0.2.999-20.20170620gitd850cdd
- Rebuild due to bug in RPM (RHBZ #1468476)

* Thu Jul 06 2017 Nicolas Chauvet <kwizart@gmail.com> - 1:0.2.999-19.20170620gitd850cdd
- Update snapshot to 20170620

* Tue Jun 13 2017 Nicolas Chauvet <kwizart@gmail.com> - 1:0.2.999-18.20170607git80d9a87
- Update snapshot to 20170607
- Default to asm and tls when available
- Use the fixed tsd for armhfp and aarch64
  fixed in https://github.com/NVIDIA/libglvnd/issues/116

* Tue Apr 04 2017 Björn Esser <besser82@fedoraproject.org> - 1:0.2.999-17.20170308git8e6e102
- Add conditional to disable testsuite, when needed

* Tue Apr 04 2017 Björn Esser <besser82@fedoraproject.org> - 1:0.2.999-16.20170308git8e6e102
- Rebuilt with testsuite again

* Tue Apr 04 2017 Björn Esser <besser82@fedoraproject.org> - 1:0.2.999-15.20170308git8e6e102
- Rebuilt without testssuite

* Tue Apr 04 2017 Björn Esser <besser82@fedoraproject.org> - 1:0.2.999-14.20170308git8e6e102
- Fix conditionals for _without_mesa_glvnd_default
- Fix other RHEL-conditionals, too

* Tue Apr 04 2017 Simone Caronni <negativo17@gmail.com> - 1:0.2.999-13.20170308git8e6e102
- Update RPM filters for private libraries (includes GLX, fixes RHEL 6).

* Mon Apr 03 2017 Simone Caronni <negativo17@gmail.com> - 1:0.2.999-12.20170308git8e6e102
- Update to latest snapshot, remove upstreamed patches.
- Update release to packaging guidelines format.
- Make sure that for Fedora 24 and RHEL the libraries are always private.

* Thu Feb 23 2017 Nicolas Chauvet <kwizart@gmail.com> - 1:0.2.999-11.gitdc16f8c
- asm enabled only for x86 - rhbz#1419944

* Mon Feb  6 2017 Hans de Goede <hdegoede@redhat.com> - 1:0.2.999-10.gitdc16f8c
- Drop 0007-GLX-Add-GLX_SGIX_fbconfig-functions.patch the bug this works
  around actually is in mesa

* Thu Feb  2 2017 Hans de Goede <hdegoede@redhat.com> - 1:0.2.999-9.gitdc16f8c
- Add eglexternalplatform spec. config dirs to -egl subpackage (rhbz#1415143)

* Thu Feb  2 2017 Hans de Goede <hdegoede@redhat.com> - 1:0.2.999-8.gitdc16f8c
- Fix GLX_SGIX_fbconfig extension, this fixes games such as "The Binding of
  Isaac: Rebirth" and "Crypt of the NecroDancer" from Steam not working

* Wed Jan 11 2017 Hans de Goede <hdegoede@redhat.com> - 1:0.2.999-7.gitdc16f8c
- Epoch:1 to provide upgrade path from negativo17.org rpms
- New snapshot
- Add patches to fix building on ARM (from Rob Clark)
- Add BuildRequires: python
- Add ldconfig scriptlets for library sub-packages

* Wed Jan 11 2017 Adam Jackson <ajax@redhat.com>
- Don't hide libraries in a subdir (rhbz#1413579)
- Split up libraries to appropriate subpackages
- Make the req/prov filter catch more cases
- Restore libGLESv1 for ABI compliance

* Wed Oct 26 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.2.999-6.git28867bb
- Update snapshot
- Fix EGL crash for KDE/Plasma (rfbz#4303)

* Tue Oct 25 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.2.999-5.git295e5e5
- Fix EGL crash (rfbz#4303)

* Fri Oct 14 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.2.999-4.git295e5e5
- Update snapshot

* Wed Oct 12 2016 Adam Jackson <ajax@redhat.com> - 0.2.999-3.git14f6283
- Restore hardened build
- Remove ExclusiveArch
- Remove some pointless Provides/Obsoletes
- BuildRequires pkgconfig(xext) not pkgconfig(xv)
- Update description to be a bit more confident
- Dump make check errors into the build log

* Wed Oct 05 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.2.999-2.git14f6283
- Add the correct License: MIT

* Thu Sep 15 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.2.999-1.git14f6283
- Update to 2.999 version
- Add EGL

* Fri Sep 02 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.1-2.gitf7fbc4b
- Update license
- Fix Obsoletes/Provides to avoid self obsolete

* Tue Aug 30 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.1-1.gitf7fbc4b
- Update to 1.1.gitf7fbc4b

* Tue Jun 14 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-4.git093f048
- Update to 20160610 git commit

* Fri May 20 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-3.gita82982d
- Update to current snapshot

* Fri May 13 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-2.git509de0d
- Update to current snapshot
- Remove unused dt-auxiliary
- Add support for graphical make test
- Undefine hardened build for xorg

* Wed May 04 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-1.git8277115
- Update to lastest snapshot

* Thu Feb 18 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-9.git4d977ea
- Remove patch to enable by default

* Wed Feb 17 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-8git20160217
- Update to git20160217
- Introduce --with mesa-libglvnd-default build conditional
- Avoid error on make check - testglxqueryversion.sh stil fails in mock
- Filter on provided libGL until glvnd support is in upstream mesa
- Use upstream tarball and use autoreconf

* Fri Jan 15 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-7git20160115
- Bump for 20160115
- Enable make check
- Description improvements
- Enable libglvnd by default
- Enable devel sub-package

* Wed Jan 06 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-6git20160106
- Update to 20160106 snapshot
- Remove 10-x11glvnd

* Sat Nov 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-5git20151121
- Update to 20151121 snapshot
- Avoid conflicts with mesa-libGL{,ES}
- Disable libGLESv1_CM

* Tue Nov 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-4git20151110
- Update to today snapshot
- Fix license

* Tue Sep 01 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-3git20150901
- Update to snapshot 20150901

* Fri Aug 07 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-2
- Update to today snapshoot

* Fri Feb  6 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-1
- Initial spec file
