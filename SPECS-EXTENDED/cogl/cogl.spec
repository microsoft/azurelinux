%global with_tests 1
Summary:        A library for using 3D graphics hardware to draw pretty pictures
Name:           cogl
Version:        1.22.8
Release:        7%{?dist}
License:        LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.clutter-project.org/
Source0:        https://download.gnome.org/sources/cogl/1.22/%{name}-%{version}.tar.xz
# Vaguely related to https://bugzilla.gnome.org/show_bug.cgi?id=772419
# but on the 1.22 branch, and the static inline in the header is gross
# ajax promises he'll clean this up.
Patch0:         0001-egl-Use-eglGetPlatformDisplay-not-eglGetDisplay.patch
# "GL_ARB_shader_texture_lod" is used to do lod biased texturing. It
# make achieve faster blurring of images instead of using large blur radius.
Patch1:         0002-add-GL_ARB_shader_texture_lod-support.patch
# "copy_sub_image" is used to implement feature similar with kwin blur
# effect by being abel to copy partial of framebuffer contents as texture
# and do post blurring.
Patch2:         0003-texture-support-copy_sub_image.patch
BuildRequires:  chrpath
BuildRequires:  make
BuildRequires:  mesa-libEGL-devel
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(xkbcommon)

%description
Cogl is a small open source library for using 3D graphics hardware to draw
pretty pictures. The API departs from the flat state machine style of
OpenGL and is designed to make it easy to write orthogonal components that
can render without stepping on each others toes.

As well aiming for a nice API, we think having a single library as opposed
to an API specification like OpenGL has a few advantages too; like being
able to paper over the inconsistencies/bugs of different OpenGL
implementations in a centralized place, not to mention the myriad of OpenGL
extensions. It also means we are in a better position to provide utility
APIs that help software developers since they only need to be implemented
once and there is no risk of inconsistency between implementations.

Having other backends, besides OpenGL, such as drm, Gallium or D3D are
options we are interested in for the future.

%package devel
Summary:        %{name} development environment
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for building and developing apps with %{name}.

%package       doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description   doc
This package contains documentation for %{name}.

%if 0%{?with_tests}
%package       tests
Summary:        Tests for %{name}
Requires:       %{name} = %{version}-%{release}

%description   tests
This package contains the installable tests for %{cogl}.
%endif

%prep
%autosetup -p1

%build
CFLAGS="%{optflags} -fPIC"
%configure \
  --enable-cairo=yes \
  --enable-cogl-pango=yes \
  --enable-gdk-pixbuf=yes \
  --enable-glx=yes \
  --disable-gtk-doc \
  --enable-introspection=yes \
  --enable-kms-egl-platform \
  --enable-wayland-egl-platform \
  --enable-wayland-egl-server \
  --enable-xlib-egl-platform \
  %{?with_tests:--enable-installed-tests}

%make_build

%install
%make_install

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete -print

# This gets installed by mistake
rm %{buildroot}%{_datadir}/cogl/examples-data/crate.jpg

# Remove lib64 rpaths
chrpath --delete %{buildroot}/%{_libdir}/libcogl-path.so
chrpath --delete %{buildroot}/%{_libdir}/libcogl-pango.so

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc NEWS README
%{_libdir}/libcogl*.so.20*
%{_libdir}/girepository-1.0/Cogl*.typelib

%files devel
%{_includedir}/cogl
%{_libdir}/libcogl*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Cogl*.gir

%if 0%{?with_tests}
%files tests
%{_datadir}/installed-tests/%{name}
%{_libexecdir}/installed-tests/%{name}
%endif

%changelog
* Thu Jan 05 2023 Sumedh Sharma <sumsharma@microsoft.com> - 1.22.8-7
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Disable doc building, remove BR on gtk-doc
- License verified

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Kalev Lember <klember@redhat.com> - 1.22.8-1
- Update to 1.22.8

* Mon Mar 09 2020 Kalev Lember <klember@redhat.com> - 1.22.6-1
- Update to 1.22.6

* Sat Mar 07 2020 Leigh Scott <leigh123linux@gmail.com> - 1.22.4-4
- Fix building against libglvnd-provided EGL headers

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.22.4-1
- Update to 1.22.4

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 1.22.2-13
- Backport MR#8 to fix builds of cogl-using packages in F31+

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.22.2-9
- Switch to %%ldconfig_scriptlets

* Wed Nov 22 2017 Troy Dawson <tdawson@redhat.com> - 1.22.2-8
- Fix spec file conditionals

* Thu Sep 28 2017 mosquito <sensor.wen@gmail.com> - 1.22.2-7
- Add GL_ARB_shader_texture_lod and copy_sub_image support (#1421055)
- Add pkgconfig(egl) BReq for rawhide
- Move BReqs to pkgconfig

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Owen Taylor <otaylor@redhat.com> - 1.22.2-4
- Add Requires: %%{name} = %%{version}-%%{release} to the tests subpackage

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 11 2016 Adam Jackson <ajax@redhat.com> - 1.22.2-2
- Prefer eglGetPlatformDisplay to eglGetDisplay

* Fri Aug 26 2016 Kalev Lember <klember@redhat.com> - 1.22.2-1
- Update to 1.22.2
- Don't set group tags

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 21 2015 Ray Strode <rstrode@redhat.com> 1.22.0-2
- Fix black login screen
  Resolves: #1272737

* Wed Sep 16 2015 Kalev Lember <klember@redhat.com> - 1.22.0-1
- Update to 1.22.0

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> - 1.21.2-2
- Re-enable parallel make

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> - 1.21.2-1
- Update to 1.21.2
- Use make_install macro
- Mark COPYING as %%license
- Drop large ChangeLog file

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Ray Strode <rstrode@redhat.com> 1.20.0-3
- Update to upstreamed version of mgag200 fix

* Wed Mar 11 2015 Ray Strode <rstrode@redhat.com> 1.20.0-2
- Try to fix wayland on mgag200

* Mon Feb 23 2015 Kalev Lember <kalevlember@gmail.com> - 1.20.0-1
- Update to 1.20.0

* Tue Jan 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.18.2-10
- Enable tests subpackage (rhbz 1163429)

* Sun Nov 16 2014 Kalev Lember <kalevlember@gmail.com> - 1.18.2-9
- Obsolete compat-cogl116 from rhughes-f20-gnome-3-12 copr

* Thu Nov 13 2014 Kalev Lember <kalevlember@gmail.com> - 1.18.2-8
- Disable cogl-gst as long as we don't have clutter-gst3 (#1158676)

* Sat Nov 01 2014 Richard Hughes <rhughes@redhat.com> - 1.18.2-7
- Fix compile on RHEL, harder

* Mon Oct 27 2014 Richard Hughes <rhughes@redhat.com> - 1.18.2-6
- Fix compile on RHEL

* Fri Aug 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.18.2-5
- Remove lib64 rpaths (#1132876)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.18.2-3
- Rebuilt for gobject-introspection 1.41.4

* Fri Jul 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.18.2-2
- Run make check but don't fail build on it

* Fri Jul 04 2014 Kalev Lember <kalevlember@gmail.com> - 1.18.2-1
- Update to 1.18.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Kalev Lember <kalevlember@gmail.com> - 1.18.0-3
- Backport an upstream fix for a totem crash

* Thu May 08 2014 Adam Jackson <ajax@redhat.com>
- Add optional installed-tests subpackage

* Mon Apr 28 2014 Richard Hughes <rhughes@redhat.com> - 1.18.0-2
- Build with --enable-cogl-gst

* Fri Mar 21 2014 Kalev Lember <kalevlember@gmail.com> - 1.18.0-1
- Update to 1.18.0

* Fri Mar 21 2014 Kalev Lember <kalevlember@gmail.com> - 1.17.5-1.gitbb10532
- Update to 1.17.5 git snapshot

* Fri Feb 21 2014 Kalev Lember <kalevlember@gmail.com> - 1.17.4-2
- Drop compat-libcogl19

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 1.17.4-1
- Update to 1.17.4, which includes soname bump
- Build a temporary compat-libcogl19 subpackage to ease the rebuilds

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 1.17.2-1
- Update to 1.17.2

* Tue Jan 21 2014 Richard Hughes <rhughes@redhat.com> - 1.16.2-1
- Update to 1.16.2

* Wed Sep 25 2013 Dan Horák <dan[at]danny.cz> - 1.16.0-2
- fix build on big endians (#1011893)

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 1.16.0-1
- Update to 1.16.0

* Thu Sep 12 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.10-3
- More configure options for enabling the gnome-shell Wayland compositor
- Enable parallel build

* Tue Sep 10 2013 Matthias Clasen <mclasen@redhat.com> - 1.15.10-2
- Add configure options that are needed to enable the gnome-shell
  Wayland compositor

* Mon Sep 02 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.10-1
- Update to 1.15.10

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.8-1
- Update to 1.15.8

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.4-1
- Update to 1.15.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Kalev Lember <kalevlember@gmail.com> 1.14.0-3
- Rebuilt

* Wed May 22 2013 Adam Jackson <ajax@redhat.com> 1.14.0-2
- cogl-1.14.0-21-ge26464f.patch: Sync with 1.14 branch for a crash fix.

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> 1.14.0-1
- Update to 1.14.0

* Wed Mar 13 2013 Matthias Clasen <mclasen@redhat.com> 1.13.4-2
- Enable wayland backend

* Thu Feb 21 2013 Bastien Nocera <bnocera@redhat.com> 1.13.4-1
- Update to 1.13.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 24 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.13.2-1
- Update to 1.13.2

* Mon Jan  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.12.2-1
- Update to 1.12.2

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 1.12.0-1
- Update to 1.12.0

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.11.6-1
- Update to 1.11.6
- Drop upstreamed cogl-1.11.4-mesa-strings.patch

* Mon Sep 17 2012 Adam Jackson <ajax@redhat.com> 1.11.4-2
- cogl-1.11.4-mesa-strings.patch: Update match strings for Mesa.

* Mon Sep  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.11.4-1
- Update to 1.11.4

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 1.11.2-1
- Update to 1.11.2

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.4-1
- Update to 1.10.4
- Dropped no-framebuffer-blit patch which is included in the release

* Thu Apr 19 2012 Adel Gadllah <adel.gadllah@gmail.com> - 1.10.2-1
- Update to 1.10.2

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.0-1
- Update to 1.10.0

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.8-1
- Update to 1.9.8

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.6-1
- Update to 1.9.6

* Tue Jan 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.4-1
- Update to 1.9.4
- https://ftp.gnome.org/pub/GNOME/sources/cogl/1.9/cogl-1.9.4.news

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> 1.9.2-1
- Update to 1.9.2

* Thu Nov 03 2011 Adam Jackson <ajax@redhat.com> 1.8.2-4
- cogl-1.8.2-lp-no-framebuffer-blit.patch: Disable the subbuffer blit code
  when running on llvmpipe until it's unbroken.

* Tue Nov 01 2011 Adam Jackson <ajax@redhat.com> 1.8.2-3
- cogl-1.8.2-no-drm-hax.patch: Don't try insane direct DRM vblank wait.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-2
- Rebuilt for glibc bug#747377

* Mon Oct 17 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.2-1
- 1.8.2 stable release
- https://ftp.gnome.org/pub/GNOME/sources/cogl/1.8/cogl-1.8.2.news
- Enable gdk-pixbuf2 support - Fixes RHBZ # 738092

* Mon Sep 19 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.0-1
- 1.8.0 stable release
- https://ftp.gnome.org/pub/GNOME/sources/cogl/1.8/cogl-1.8.0.news

* Mon Sep  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.6-1
- Update to 1.7.6

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.4-1
- Update to 1.7.4

* Mon Jul  4 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Thu Jun 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.0-3
- Update spec for review feedback

* Thu Jun 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.0-2
- Update spec for review feedback

* Wed Jun 15 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.0-1
- Initial Package
