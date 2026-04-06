# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global has_luajit 1

%ifarch ppc64le s390x riscv64
%global has_luajit 0
%endif

# Look, you probably don't want this. scim is so 2012. ibus is the new hotness.
# Enabling this means you'll almost certainly need to pass ECORE_IMF_MODULE=xim
# to get anything to work. (*cough*terminology*cough*)
%global with_scim 0

# Enable avif support (this broke before)
%bcond avif 1

Name:		efl
Version:	1.28.1
Release:	2%{?dist}
Summary:	Collection of Enlightenment libraries
# Automatically converted from old format: BSD and LGPLv2+ and GPLv2 and zlib - review is highly recommended.
License:	LicenseRef-Callaway-BSD AND LicenseRef-Callaway-LGPLv2+ AND GPL-2.0-only AND Zlib
URL:		http://enlightenment.org/
Source0:	http://download.enlightenment.org/rel/libs/efl/efl-%{version}.tar.xz
# This is hacky, but it gets us building in rawhide again.
# Upstream efl probably needs to rework how they use check in their C tests
Patch1:		efl-1.25.0-check-fix.patch

# Fix headerless .po files that modern gettext doesn't like
Patch2:		efl-1.27.0-gettextfix.patch

# Build ecore_sdl versioned so. So efl no longer requires efl-devel
Patch3:		efl-1.27.0-sdl-version-build.patch

# Handle incompatible pointer types in the bigendian cases
Patch4:		efl-1.27.0-bigendian-gcc-fix.patch

%ifnarch s390x
BuildRequires:	libunwind-devel
%endif
BuildRequires:  gcc-c++
BuildRequires:	bullet-devel libpng-devel libjpeg-devel gstreamer1-devel zlib-devel
BuildRequires:	gstreamer1-plugins-base-devel libtiff-devel openssl-devel
BuildRequires:	curl-devel dbus-devel glibc-devel fontconfig-devel freetype-devel
BuildRequires:	fribidi-devel pulseaudio-libs-devel libsndfile-devel libX11-devel
BuildRequires:	libXau-devel libXcomposite-devel libXdamage-devel libXdmcp-devel
BuildRequires:	libXext-devel libXfixes-devel libXinerama-devel libXrandr-devel
BuildRequires:	libXrender-devel libXScrnSaver-devel libXtst-devel libXcursor-devel
BuildRequires:	libXi-devel mesa-libGL-devel mesa-libEGL-devel
BuildRequires:	libblkid-devel libmount-devel systemd-devel harfbuzz-devel
BuildRequires:	libwebp-devel tslib-devel SDL2-devel SDL-devel c-ares-devel
BuildRequires:	libxkbcommon-devel uuid-devel libxkbcommon-x11-devel avahi-devel
BuildRequires:	rlottie-devel libjxl-devel
BuildRequires:	pkgconfig(poppler-cpp) >= 0.12
BuildRequires:	pkgconfig(libspectre) pkgconfig(libraw)
BuildRequires:	pkgconfig(librsvg-2.0) >= 2.14.0
BuildRequires:	pkgconfig(cairo) >= 1.0.0
%if %{with avif}
BuildRequires:	pkgconfig(libavif)
%endif
%if %{with_scim}
BuildRequires:	scim-devel
%endif
BuildRequires:	ibus-devel
BuildRequires:	doxygen systemd giflib-devel openjpeg2-devel libdrm-devel
BuildRequires:	wayland-devel >= 1.11.0
BuildRequires:	wayland-protocols-devel >= 1.7
BuildRequires:	meson >= 0.50
BuildRequires:	ninja-build gettext-devel mesa-libGLES-devel
BuildRequires:	mesa-libgbm-devel libinput-devel
%if 0%{?has_luajit}
BuildRequires:	luajit-devel
%else
BuildRequires:	compat-lua-devel
%endif
# For AutoReq cmake-filesystem
BuildRequires:	cmake
# These are convenience provides to aid in migration
Provides:	e_dbus%{?_isa} = %{version}-%{release}
Provides:	e_dbus = %{version}-%{release}
Obsoletes:	e_dbus <= 1.7.10
Provides:	ecore = %{version}-%{release}
Provides:	ecore%{?_isa} = %{version}-%{release}
Obsoletes:	ecore <= 1.7.10
Provides:	edje = %{version}-%{release}
Provides:	edje%{?_isa} = %{version}-%{release}
Obsoletes:	edje <= 1.7.10
Provides:	eet = %{version}-%{release}
Provides:	eet%{?_isa} = %{version}-%{release}
Obsoletes:	eet <= 1.7.10
Provides:	eeze = %{version}-%{release}
Provides:	eeze%{?_isa} = %{version}-%{release}
Obsoletes:	eeze <= 1.7.10
Provides:	efreet = %{version}-%{release}
Provides:	efreet%{?_isa} = %{version}-%{release}
Obsoletes:	efreet <= 1.7.10
Provides:	eina%{?_isa} = %{version}-%{release}
Provides:	eio = %{version}-%{release}
Provides:	eio%{?_isa} = %{version}-%{release}
Obsoletes:	eio <= 1.7.10
Provides:	eldbus%{?_isa} = %{version}-%{release}
Provides:	elementary = %{version}-%{release}
Provides:	elementary%{?_isa} = %{version}-%{release}
Obsoletes:	elementary <= 1.17.1
# Provides:	elocation%%{?_isa} = %%{version}-%%{release}
Provides:	elua%{?_isa} = %{version}-%{release}
Provides:	embryo = %{version}-%{release}
Provides:	embryo%{?_isa} = %{version}-%{release}
Obsoletes:	embryo <= 1.7.10
Provides:	emotion = %{version}-%{release}
Provides:	emotion%{?_isa} = %{version}-%{release}
Obsoletes:	emotion <= 1.7.10
Provides:	eo%{?_isa} = %{version}-%{release}
Provides:	eolian%{?_isa} = %{version}-%{release}
Provides:	ephysics%{?_isa} = %{version}-%{release}
Provides:	ethumb = %{version}-%{release}
Provides:	ethumb%{?_isa} = %{version}-%{release}
Obsoletes:	ethumb <= 1.7.10
Provides:	evas = %{version}-%{release}
Provides:	evas%{?_isa} = %{version}-%{release}
Obsoletes:	evas <= 1.7.10
Provides:	evas-generic-loaders = %{version}-%{release}
Provides:	evas-generic-loaders%{?_isa} = %{version}-%{release}
Obsoletes:	evas-generic-loaders <= 1.17.0
Provides:	libeina = %{version}-%{release}
Provides:	libeina%{?_isa} = %{version}-%{release}
Obsoletes:	libeina <= 1.7.10

%description
EFL is a collection of libraries for handling many common tasks a
developer may have such as data structures, communication, rendering,
widgets and more.

%package devel
Summary:	Development files for EFL
Requires:	efl%{?_isa} = %{version}-%{release}
Requires:	pkgconfig, libX11-devel
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Provides:	e_dbus-devel%{?_isa} = %{version}-%{release}
Provides:	e_dbus-devel = %{version}-%{release}
Obsoletes:	e_dbus-devel <= 1.7.10
Provides:	ecore-devel = %{version}-%{release}
Provides:	ecore-devel%{?_isa} = %{version}-%{release}
Obsoletes:	ecore-devel <= 1.7.10
Provides:	edje-devel = %{version}-%{release}
Provides:	edje-devel%{?_isa} = %{version}-%{release}
Obsoletes:	edje-devel <= 1.7.10
Provides:	eet-devel = %{version}-%{release}
Provides:	eet-devel%{?_isa} = %{version}-%{release}
Obsoletes:	eet-devel <= 1.7.10
Provides:	eeze-devel = %{version}-%{release}
Provides:	eeze-devel%{?_isa} = %{version}-%{release}
Obsoletes:	eeze-devel <= 1.7.10
Provides:	efreet-devel = %{version}-%{release}
Provides:	efreet-devel%{?_isa} = %{version}-%{release}
Obsoletes:	efreet-devel <= 1.7.10
Provides:	eina-devel%{?_isa} = %{version}-%{release}
Provides:	eio-devel = %{version}-%{release}
Provides:	eio-devel%{?_isa} = %{version}-%{release}
Obsoletes:	eio-devel <= 1.7.10
Provides:	eldbus-devel%{?_isa} = %{version}-%{release}
Provides:	elementary-devel = %{version}-%{release}
Provides:	elementary-devel%{?_isa} = %{version}-%{release}
Obsoletes:	elementary-devel <= 1.17.1
# Provides:	elocation-devel%%{?_isa} = %%{version}-%%{release}
Provides:	embryo-devel = %{version}-%{release}
Provides:	embryo-devel%{?_isa} = %{version}-%{release}
Obsoletes:	embryo-devel <= 1.7.10
Provides:	emotion-devel = %{version}-%{release}
Provides:	emotion-devel%{?_isa} = %{version}-%{release}
Obsoletes:	emotion-devel <= 1.7.10
Provides:	eo-devel%{?_isa} = %{version}-%{release}
Provides:	eolian-devel%{?_isa} = %{version}-%{release}
Provides:	ephysics-devel%{?_isa} = %{version}-%{release}
Provides:	ethumb-devel = %{version}-%{release}
Provides:	ethumb-devel%{?_isa} = %{version}-%{release}
Obsoletes:	ethumb-devel <= 1.7.10
Provides:	evas-devel = %{version}-%{release}
Provides:	evas-devel%{?_isa} = %{version}-%{release}
Obsoletes:	evas-devel <= 1.7.10
Provides:	libeina-devel = %{version}-%{release}
Provides:	libeina-devel%{?_isa} = %{version}-%{release}
Obsoletes:	libeina-devel <= 1.7.10

%description devel
Development files for EFL.

%prep
%autosetup -n %{name}-%{version} -p1

%build
export CFLAGS="%optflags -std=gnu17"
export CXXFLAGS="%optflags -std=gnu++17"
%{meson} \
 -Dxinput22=true \
 -Dsystemd=true \
%if %{with avif}
 -Devas-loaders-disabler=json,heif \
%else
 -Devas-loaders-disabler=json,heif,avif \
%endif
 -Dharfbuzz=true \
 -Dsdl=true \
 -Dbuffer=true \
 -Davahi=true \
%if %{with_scim}
 -Decore-imf-loaders-disabler= \
%else
 -Decore-imf-loaders-disabler=scim \
 -Dglib=true \
%endif
 -Dfb=true \
 -Dwl=true \
 -Ddrm=true \
 -Dinstall-eo-files=true \
%if 0%{?has_luajit}
 -Dbindings=lua,cxx \
 -Dlua-interpreter=luajit \
 -Delua=true \
%else
 -Dbindings=cxx \
 -Dlua-interpreter=lua \
%endif
 -Dphysics=true
%{meson_build}

%install
%{meson_install}

# There is probably a better place to fix this, but I couldn't untangle it.
sed -i 's|ecore_sdl|ecore-sdl|g' %{buildroot}%{_libdir}/pkgconfig/elementary.pc
sed -i 's|ecore_sdl|ecore-sdl|g' %{buildroot}%{_libdir}/pkgconfig/elementary-cxx.pc

# yay pathing
%if 0%{?__isa_bits} == 64
mv %{buildroot}%{_datadir}/gdb/auto-load/usr/lib %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}
%endif

# fix perms
chmod -x src/bin/edje/edje_cc_out.c

find %{buildroot} -name '*.la' -delete

%find_lang %{name}

%post
%systemd_user_post ethumb.service

%postun
%systemd_user_postun ethumb.service

%preun
%systemd_user_preun ethumb.service

%files -f %{name}.lang
%license COPYING licenses/COPYING.BSD licenses/COPYING.GPL licenses/COPYING.LGPL licenses/COPYING.SMALL
%doc AUTHORS COMPLIANCE README.md
%{_libdir}/libefl.so.1*
%{_libdir}/libefl_canvas_wl.so.1*
%{_bindir}/efl_debug
%{_bindir}/efl_debugd
%{_datadir}/icons/Enlightenment-X/
# ecore
%{_bindir}/ecore_evas_convert
%{_libdir}/ecore/
%{_libdir}/ecore_buffer/
%{_libdir}/ecore_con/
%{_libdir}/ecore_evas/
%{_libdir}/ecore_imf/
%{_libdir}/ecore_wl2/
%{_libdir}/libecore*.so.*
%{_datadir}/ecore/
%{_datadir}/ecore_con/
%{_datadir}/ecore_imf/
%{_datadir}/ecore_x/
%{_libdir}/libector.so.*
# edje
%{_bindir}/edje*
%{_datadir}/mime/packages/edje.xml
%{_libdir}/edje/
%{_libdir}/libedje.so.1*
# eet
%{_bindir}/diffeet
%{_bindir}/eet
%{_bindir}/eetpack
%{_bindir}/vieet
%{_libdir}/libeet.so.*
# eeze
%attr(0755,root,root) %caps(cap_audit_write,cap_chown,cap_setuid,cap_sys_admin=pe) %{_bindir}/eeze_scanner
%{_bindir}/eeze_scanner_monitor
%{_bindir}/eeze_disk_ls
%{_bindir}/eeze_mount
%{_bindir}/eeze_umount
%{_libdir}/eeze/
%{_libdir}/libeeze.so.1*
# efreet
%{_bindir}/efreetd
# we don't depend on dbus, but we want clean dir ownership here.
%dir %{_datadir}/dbus-1/
%dir %{_datadir}/dbus-1/services/
%{_libdir}/efreet/
%{_libdir}/libefreet.so.1*
%{_libdir}/libefreet_mime.so.1*
%{_libdir}/libefreet_trash.so.1*
# eina
%{_bindir}/eina_btlog
%{_bindir}/eina_modinfo
%{_libdir}/libeina.so.*
# eio
%{_libdir}/libeio.so.1*
# eldbus
%{_bindir}/eldbus-codegen
%{_libdir}/libeldbus.so.1*
# elementary
%{_bindir}/elementary_codegen
%{_bindir}/elementary_config
%{_bindir}/elementary_perf
%{_bindir}/elementary_quicklaunch
%{_bindir}/elementary_run
%{_bindir}/elementary_test
%{_bindir}/elm_prefs_cc
%{_libdir}/libelementary.so.1*
%{_libdir}/elementary/
%{_datadir}/applications/elementary*.desktop
%{_datadir}/elementary/
%{_datadir}/icons/hicolor/*/apps/elementary.png
# elocation
# %%{_libdir}/libelocation.so.1*
# elput
%{_libdir}/libelput.so.1*
# elua
%if 0%{?has_luajit}
%{_bindir}/elua
%{_datadir}/elua/
%{_libdir}/libelua.so.1*
%else
%exclude %{_datadir}/elua/
%endif
# embryo
%{_bindir}/embryo_cc
%{_libdir}/libembryo.so.1*
%{_libdir}/libemile.so.*
# emotion
%{_bindir}/emotion_test*
%{_libdir}/emotion/
%{_libdir}/libemotion.so.1*
# eo
%{_bindir}/eo_debug
%{_libdir}/libeo.so.1*
%{_libdir}/libeo_dbg.so.1*
%{_datadir}/gdb/auto-load/%{_libdir}/libeo.so.1*
# eolian
%{_bindir}/eolian_cxx
%{_bindir}/eolian_gen
%{_libdir}/libeolian.so.1*
# ephysics
%{_libdir}/libephysics.so.1*
# ethumb
%{_bindir}/ethumb
%{_bindir}/ethumbd
%{_bindir}/ethumbd_client
%{_userunitdir}/ethumb.service
%{_libdir}/ethumb/
%{_libdir}/ethumb_client/
%{_libdir}/libethumb.so.1*
%{_libdir}/libethumb_client.so.1*
%{_datadir}/dbus-1/services/org.enlightenment.Ethumb.service
%{_datadir}/ethumb
%{_datadir}/ethumb_client
# evas
# %%{_bindir}/evas_*
%{_libdir}/evas/
%{_libdir}/libevas.so.*
%{_datadir}/evas/
%{_datadir}/mime/packages/evas.xml
# exactness
%{_bindir}/exactness*
%{_libdir}/libexactness*.so.*
%{_datadir}/exactness/

%files devel
%{_includedir}/efl-1/
%{_includedir}/efl-cxx-1/
%{_includedir}/efl-canvas-wl-1/
%{_bindir}/efl_canvas_wl_test*
%{_libdir}/cmake/Efl/
%{_libdir}/libefl.so
%{_libdir}/libefl_canvas_wl.so
%{_libdir}/pkgconfig/efl-core.pc
%{_libdir}/pkgconfig/efl-cxx.pc
%{_libdir}/pkgconfig/efl-net.pc
%{_libdir}/pkgconfig/efl-ui.pc
%{_libdir}/pkgconfig/efl-canvas-wl.pc
%{_libdir}/pkgconfig/efl.pc
# ecore-devel
%{_includedir}/ecore-1/
%{_includedir}/ecore-audio-1/
%{_includedir}/ecore-avahi-1/
%{_includedir}/ecore-buffer-1/
%{_includedir}/ecore-con-1/
%{_includedir}/ecore-cxx-1/
%{_includedir}/ecore-drm2-1/
%{_includedir}/ecore-evas-1/
%{_includedir}/ecore-fb-1/
%{_includedir}/ecore-file-1/
%{_includedir}/ecore-imf-1/
%{_includedir}/ecore-imf-evas-1/
%{_includedir}/ecore-input-1/
%{_includedir}/ecore-input-evas-1/
%{_includedir}/ecore-ipc-1/
%{_includedir}/ecore-sdl-1/
%{_includedir}/ecore-wl2-1/
%{_includedir}/ecore-x-1/
%{_libdir}/cmake/Ecore*/
%{_libdir}/libecore*.so
%{_libdir}/pkgconfig/ecore*.pc
%{_libdir}/libector.so
%{_libdir}/pkgconfig/ector.pc
# edje-devel
%{_libdir}/libedje.so
%{_libdir}/pkgconfig/edje*.pc
%{_datadir}/edje
%{_includedir}/edje-*
%{_libdir}/cmake/Edje/
# eet-devel
%{_includedir}/eet-1/
%{_includedir}/eet-cxx-1/
%{_libdir}/cmake/Eet/
%{_libdir}/cmake/EetCxx/
%{_libdir}/pkgconfig/eet*.pc
%{_libdir}/libeet.so
# eeze-devel
%{_includedir}/eeze-1/
%{_libdir}/cmake/Eeze/
%{_libdir}/libeeze.so
%{_datadir}/eeze/
%{_libdir}/pkgconfig/eeze.pc
# efreet-devel
%{_includedir}/efreet-1/
%{_libdir}/cmake/Efreet/
%{_libdir}/libefreet.so
%{_libdir}/libefreet_mime.so
%{_libdir}/libefreet_trash.so
%{_datadir}/efreet/
%{_libdir}/pkgconfig/efreet.pc
%{_libdir}/pkgconfig/efreet-mime.pc
%{_libdir}/pkgconfig/efreet-trash.pc
# eina-devel
%{_includedir}/eina-1/
%{_includedir}/eina-cxx-1/
%{_libdir}/cmake/Eina*/
%{_libdir}/pkgconfig/eina*.pc
%{_libdir}/libeina.so
# eio-devel
%{_includedir}/eio-1/
%{_includedir}/eio-cxx-1/
%{_libdir}/libeio.so
%{_libdir}/pkgconfig/eio.pc
%{_libdir}/pkgconfig/eio-cxx.pc
%{_libdir}/cmake/Eio/
# eldbus-devel
%{_includedir}/eldbus-1/
%{_includedir}/eldbus-cxx-1/
%{_libdir}/cmake/Eldbus/
%{_libdir}/libeldbus.so
%{_libdir}/pkgconfig/eldbus.pc
%{_libdir}/pkgconfig/eldbus-cxx.pc
# elementary-devel
%{_includedir}/elementary-1/
%{_includedir}/elementary-cxx-1/
%{_libdir}/cmake/Elementary/
%{_libdir}/libelementary.so
%{_libdir}/pkgconfig/elementary.pc
%{_libdir}/pkgconfig/elementary-cxx.pc
# elocation-devel
# %%{_includedir}/elocation-1/
# %%{_libdir}/libelocation.so
# %%{_libdir}/pkgconfig/elocation.pc
# elput-devel
%{_includedir}/elput-1/
%{_libdir}/libelput.so
%{_libdir}/pkgconfig/elput.pc
# elua-devel
%if 0%{?has_luajit}
%{_includedir}/elua-1/
%{_libdir}/libelua.so
%{_libdir}/pkgconfig/elua.pc
%{_libdir}/cmake/Elua/
%else
%exclude %{_libdir}/cmake/Elua/
%endif
# embryo-devel
%{_includedir}/embryo-1/
%{_libdir}/libembryo.so
%{_libdir}/pkgconfig/embryo.pc
%{_datadir}/embryo/
%{_includedir}/emile-1/
%{_libdir}/cmake/Emile/
%{_libdir}/libemile.so
%{_libdir}/pkgconfig/emile.pc
# emotion-devel
%{_includedir}/emotion-1/
%{_libdir}/cmake/Emotion/
%{_libdir}/libemotion.so
%{_libdir}/pkgconfig/emotion.pc
%{_datadir}/emotion/
# eo-devel
%{_includedir}/eo-1/
%{_includedir}/eo-cxx-1/
%{_libdir}/cmake/Eo/
%{_libdir}/cmake/EoCxx/
%{_libdir}/libeo.so
%{_libdir}/libeo_dbg.so
%{_libdir}/pkgconfig/eo.pc
%{_libdir}/pkgconfig/eo-cxx.pc
%{_datadir}/eo/
# eolian-devel
%{_includedir}/eolian-1/
%{_includedir}/eolian-cxx-1/
%{_libdir}/cmake/Eolian/
%{_libdir}/cmake/EolianCxx/
%{_libdir}/pkgconfig/eolian.pc
%{_libdir}/pkgconfig/eolian-cxx.pc
%{_libdir}/libeolian.so
%{_datadir}/eolian/
# ephysics-devel
%{_includedir}/ephysics-1/
%{_libdir}/libephysics.so
%{_libdir}/pkgconfig/ephysics.pc
# ethumb-devel
%{_includedir}/ethumb-1/
%{_includedir}/ethumb-client-1/
%{_libdir}/cmake/Ethumb/
%{_libdir}/cmake/EthumbClient/
%{_libdir}/libethumb.so
%{_libdir}/libethumb_client.so
%{_libdir}/pkgconfig/ethumb.pc
%{_libdir}/pkgconfig/ethumb-client.pc
%{_libdir}/pkgconfig/ethumb_client.pc
# evas-devel
%{_includedir}/evas-1/
%{_includedir}/evas-cxx-1/
%{_libdir}/libevas.so
%{_libdir}/cmake/Evas/
%{_libdir}/cmake/EvasCxx/
%{_libdir}/pkgconfig/evas*.pc
# exactness
%{_libdir}/libexactness*.so

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Mar 29 2025 Tom Callaway <spot@fedoraproject.org> - 1.28.1-1
- update to 1.28.1

* Fri Feb 14 2025 Tom Callaway <spot@fedoraproject.org> - 1.28.0-2
- rebuild for poppler

* Sun Feb 02 2025 Robert-André Mauchin <zebob.m@gmail.com> - 1.28.0-1
- Update to 1.28.0
- Fix FTBFS by forcing std17
- Close: rhbz#2337186
- Fix: rhbz#2340116
- Rebuild for jpegxl (libjxl) 0.11.1

* Sun Feb 02 2025 Sérgio Basto <sergio@serjux.com> - 1.27.0-15
- Rebuild for jpegxl (libjxl) 0.11.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Nov 30 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.27.0-13
- Cleanup arch/spec, EOL releases

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 1.27.0-12
- convert license to SPDX

* Thu Aug 22 2024 Marek Kasik <mkasik@redhat.com> - 1.27.0-11
- Rebuild for poppler 24.08.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 13 2024 Sérgio Basto <sergio@serjux.com> - 1.27.0-9
- Rebuild for jpegxl (libjxl) 0.10.2

* Thu Feb 29 2024 David Abdurachmanov <davidlt@rivosinc.com> - 1.27.0-8
- Disable LuaJIT on riscv64 (not ported)

* Wed Feb 14 2024 Sérgio Basto <sergio@serjux.com> - 1.27.0-7
- Rebuild for jpegxl (libjxl) 0.9.2 with soname bump

* Wed Jan 31 2024 František Zatloukal <fzatlouk@redhat.com> - 1.27.0-6
- Rebuilt for libavif 1.0.3

* Tue Jan 30 2024 Tom Callaway <spot@fedoraproject.org> - 1.27.0-5
- fix incompatible pointer types in bigendian cases causing FTBFS
- fix pointer issue with aarch64 specific code

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Ding-Yi Chen <dchen@redhat.com> - 1.27.0-2
-  Build ecore_sdl versioned so. So efl no longer requires efl-devel

* Tue Jan 02 2024 Ding-Yi Chen <dchen@redhat.com> - 1.27.0-1
- Fixes Bug 2255716 - efl-1.27.0 is available
- Add BuildRequires: libjxl-devel
- Documents:
  + Remove NEWS, because upstream no-longer have it
  + Rename README to README.md

* Tue Aug  1 2023 Tom Callaway <spot@fedoraproject.org> - 1.26.3-8
- fix headerless .po files that modern gettext does not like (bz2225767)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.3-5
- LibRaw rebuild

* Thu Dec 01 2022 Kalev Lember <klember@redhat.com> - 1.26.3-4
- Rebuild for new libavif

* Sun Oct 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.26.3-3
- Rebuild for new libavif

* Sun Oct 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.26.3-2
- Rebuild for new libavif

* Sat Sep 24 2022 Tom Callaway <spot@fedoraproject.org> - 1.26.3-1
- update to 1.26.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 22 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.26.1-4
- Rebuilt for new libavif

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 1.26.1-3
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan  3 2022 Tom Callaway <spot@fedoraproject.org> - 1.26.1-1
- update to 1.26.1

* Wed Dec 29 2021 Tom Callaway <spot@fedoraproject.org> - 1.26.0-1
- update to 1.26.0

* Wed Dec 01 2021 Andreas Schneider <asn@redhat.com> - 1.25.1-10
- Don't build with luajit support on ppc64le and s390x
- Remove unknown systemdunitdir option

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.25.1-8
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb 12 2021 Tom Callaway <spot@fedoraproject.org> - 1.25.1-6
- rebuild against new bullet

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec  4 2020 Tom Callaway <spot@fedoraproject.org> - 1.25.1-4
- merge libavif logic to one spec

* Mon Nov 30 2020 Andreas Schneider <asn@redhat.com> - 1.25.1-3.1
- Disable avif support

* Tue Oct 27 2020 Mamoru TASAKA <mtasaka@fedoraprojet.org> - 1.25.1-3
- Disable libavif support for now (bug 1891658)

* Fri Oct 23 10:33:37 CEST 2020 Nils Philippsen <nils@tiptoe.de> - 1.25.1-2
- rebuild for new libavif

* Mon Oct 12 2020 Tom Callaway <spot@fedoraproject.org> - 1.25.1-1
- update to 1.25.1

* Wed Sep 30 2020 Adam Jackson <ajax@redhat.com> - 1.25.0-2
- Drop unused BuildRequires: libXp-devel

* Tue Sep 22 2020 Tom Callaway <spot@fedoraproject.org> - 1.25.0-1
- update to 1.25.0

* Wed Aug  5 2020 Tom Callaway <spot@fedoraproject.org> - 1.24.3-4
- fix build against check in rawhide

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Ding-Yi Chen <dchen@redhat.com> - 1.24.3-1
- update to 1.24.3
- Remove meson flag -Dopengl=full
- Remove Patch1 efl-1.17.1-old-nomodifier-in-drm_mode_fb_cmd2.patch
- Remove Patch2 efl-1.23.1-luajitfix.patch
  as luaL_reg is no longer required

* Tue May 26 2020 Tom Callaway <spot@fedoraproject.org> - 1.24.2-1
- update to 1.24.2

* Mon May 11 2020 Tom Callaway <spot@fedoraproject.org> - 1.24.1-1
- update to 1.24.1

* Mon May 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.23.3-6
- Rebuild for new LibRaw

* Tue May 05 2020 Sereinity <sereinity@sereinity.fr> - 1.23.3-5
- rebuilt

* Fri Jan 31 2020 Tom Callaway <spot@fedoraproject.org> - 1.23.3-4
- fix FTBFS

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Marek Kasik <mkasik@redhat.com> - 1.23.3-2
- Rebuild for poppler-0.84.0

* Mon Dec  2 2019 Tom Callaway <spot@fedoraproject.org> - 1.23.3-1
- update to 1.23.3

* Tue Nov  5 2019 Tom Callaway <spot@fedoraproject.org> - 1.23.2-1
- update to 1.23.2

* Wed Oct 16 2019 Tom Callaway <spot@fedoraproject.org> - 1.23.1-1
- update to 1.23.1

* Wed Sep  4 2019 Tom Callaway <spot@fedoraproject.org> - 1.22.4-1
- update to 1.22.4

* Fri Aug 23 2019 Tom Callaway <spot@fedoraproject.org> - 1.22.3-1
- update to 1.22.3

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 2 2019 Tom Callaway <spot@fedoraproject.org> - 1.22.2-1
- update to 1.22.2

* Thu Feb 28 2019 Pete Walter <pwalter@fedoraproject.org> - 1.21.1-5
- Update wayland deps

* Fri Feb 15 2019 Tom Callaway <spot@fedoraproject.org> - 1.21.1-4
- use khrplatform.h defines everywhere, because ptrdiff_t is not signed long int on 32bit arches

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Dan Horák <dan[at]danny.cz> - 1.21.1-2
- enable NEON on arm/aarch64, EFL uses runtime CPU detection

* Fri Sep 21 2018 Tom Callaway <spot@fedoraproject.org> - 1.21.1-1
- update to 1.21.1

* Sat Aug 18 2018 Tom Callaway <spot@fedoraproject.org> - 1.21.0-1
- Update to 1.21.0

* Thu Jul 19 2018 Adam Williamson <awilliam@redhat.com> - 1.20.7-4
- Rebuild for new libraw

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 23 2018 Marek Kasik <mkasik@redhat.com> - 1.20.7-2
- Rebuild for poppler-0.63.0

* Mon Mar  5 2018 Tom Callaway <spot@fedoraproject.org> - 1.20.7-1
- update to 1.20.7

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 1.20.5-7
- Rebuild (giflib)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Sandro Mani <manisandro@gmail.com> - 1.20.5-5
- Switch to openjpeg2

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.20.5-4
- Remove obsolete scriptlets

* Thu Jan 04 2018 Troy Dawson <tdawson@redhat.com> - 1.20.5-3
- Update conditional

* Mon Dec 18 2017 Rich Mattes <richmattes@gmail.com> - 1.20.5-2
- Rebuild for bullet-2.87

* Sun Oct 29 2017 Tom Callaway <spot@fedoraproject.org> - 1.20.5-1
- update to 1.20.5

* Sat Oct 21 2017 Benoît Marcelin <sereinity@sereinity.fr> - 1.20.4-1
- update to 1.20.4
- remove (merged upstream) patch about builds on big endians

* Fri Sep  1 2017 Tom Callaway <spot@fedoraproject.org> - 1.20.3-1
- update to 1.20.3

* Wed Aug 30 2017 Dan Horák <dan[at]danny.cz> - 1.20.2-2
- fix build on big endians

* Fri Aug 11 2017 Tom Callaway <spot@fedoraproject.org> - 1.20.2-1
- update to 1.20.2
- BR: libunwind-devel
- ExcludeArch: s390x

* Mon Aug 07 2017 Tom Callaway <spot@fedoraproject.org> - 1.20.1-1
- update to 1.20.1

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 1.19.1-4
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 Tom Callaway <spot@fedoraproject.org> - 1.19.1-1
- update to 1.19.1

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon May 15 2017 Tom Callaway <spot@fedoraproject.org> - 1.19.0-3
- disable luajit for aarch64

* Mon May 15 2017 Tom Callaway <spot@fedoraproject.org> - 1.19.0-2
- rebuild for new tslib, luajit

* Tue Apr 18 2017 Sereinity <sereinit@fedoraproject.org> - 1.19.0-1
- update to 1.19.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 1.18.4-3
- Rebuild (libwebp)

* Tue Dec 27 2016 Jon Ciesla <limburgher@gmail.com> - 1.18.4-2
- Rebuild for new LibRaw.

* Fri Dec  9 2016 Tom Callaway <spot@fedoraproject.org> - 1.18.4-1
- update to 1.18.4

* Thu Dec  1 2016 Tom Callaway <spot@fedoraproject.org> - 1.18.3-2
- fix systemd handling

* Mon Nov 28 2016 Tom Callaway <spot@fedoraproject.org> - 1.18.3-1
- update to 1.18.3

* Wed Oct 19 2016 Tom Callaway <spot@fedoraproject.org> - 1.18.2-1
- update to 1.18.2

* Wed Sep 21 2016 Tom Callaway <spot@fedoraproject.org> - 1.18.1-1
- update to 1.18.1

* Mon Sep 19 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.18.0-5
- aarch64 now has LuaJIT

* Wed Aug 31 2016 Tom Callaway <spot@fedoraproject.org> - 1.18.0-4
- explicitly disable cocoa. we are not osx. sloppy configure gets it wrong.
- fix typo in elementary pc files

* Wed Aug 31 2016 Tom Callaway <spot@fedoraproject.org> - 1.18.0-3
- properly provide/obsolete evas-generic-loaders

* Wed Aug 31 2016 Tom Callaway <spot@fedoraproject.org> - 1.18.0-2
- properly provide/obsolete elementary-devel

* Mon Aug 29 2016 Tom Callaway <spot@fedoraproject.org> - 1.18.0-1
- update to 1.18.0

* Mon Aug 29 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.17.2-2
- Rebuild for LuaJIT 2.1.0

* Fri Jul 15 2016 Ding-Yi Chen <dchen@redhat.com> - 1.17.2-1
- update to 1.17.2

* Mon Jun 13 2016 Tom Callaway <spot@fedoraproject.org> - 1.17.1-2
- apply old target changes to rawhide

* Mon Jun 13 2016 Tom Callaway <spot@fedoraproject.org> - 1.17.1-1.1
- fix old targets (rhel7, f22)

* Mon Jun 13 2016 Tom Callaway <spot@fedoraproject.org> - 1.17.1-1
- update to 1.17.1

* Mon May 23 2016 Ding-Yi Chen <dchen@redhat.com> - 1.17.0-5
- Rebuild for latest libinput

* Mon Mar 14 2016 Ding-Yi Chen <dchen@redhat.com> - 1.17.0-4
- Disable wayland for Fedora 22 and EPEL, as they do not have
  dependencies

* Mon Mar 14 2016 Ding-Yi Chen <dchen@redhat.com> - 1.17.0-3
- Re-enable wayland

* Tue Feb 09 2016 Rich Mattes <richmattes@gmail.com> - 1.17.0-2
- Rebuild for bullet 2.83

* Wed Feb 3 2016 Ding-Yi Chen <dchen@redhat.com> - 1.17.0-1
- Upstream update to 1.17.0
- Removed: /usr/include/ector-1

* Tue Jan 19 2016 Ding-Yi Chen <dchen@redhat.com> - 1.16.1-2
- Fix rpmlint error

* Tue Jan 05 2016 Ding-Yi Chen <dchen@redhat.com> - 1.16.1-1
- update to 1.16.1

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.16.0-3
- Rebuilt for libwebp soname bump

* Mon Nov 23 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.16.0-2
- Follow upstream decision and disable NEON on AArch64 as well.

* Tue Nov 10 2015 Tom Callaway <spot@fedoraproject.org> - 1.16.0-1
- update to 1.16.0

* Mon Sep 14 2015 Tom Callaway <spot@fedoraproject.org> - 1.15.1-2
- fix compilation against current lua (thanks to Rafael Fonseca)

* Fri Aug 28 2015 Tom Callaway <spot@fedoraproject.org> - 1.15.1-1
- update to 1.15.1

* Mon Aug 10 2015 Tom Callaway <spot@fedoraproject.org> - 1.15.0-1
- update to 1.15.0

* Tue Jul  7 2015 Tom Callaway <spot@fedoraproject.org> - 1.14.2-1
- disable scim by default
- update to 1.14.2

* Sun Jul  5 2015 Conrad Meyer <cemeyer@uw.edu> - 1.14.1-3
- Install eo_gdb autoload script with correct path

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun  3 2015 Tom Callaway <spot@fedoraproject.org> - 1.14.1-1
- update to 1.14.1

* Thu May 28 2015 Tom Callaway <spot@fedoraproject.org> - 1.14.0-1
- update to 1.14.0
- disable wayland support (bz 1214597)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.13.2-3
- Rebuilt for GCC 5 C++11 ABI change

* Wed Apr  8 2015 Dan Horák <dan[at]danny.cz> - 1.13.2-2
- use luajit only where available

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.2-1
- update to 1.13.2

* Tue Mar 31 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-7
- add dbus dir ownership

* Mon Mar 30 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-6
- fix provides/obsoletes to replace old split out packages with efl
- add scriptlets for mimeinfo handling
- mark COPYING as a license file

* Wed Mar 18 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-5
- own cmake dirs, not just cmake files

* Mon Mar 16 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-4
- drop incorrect patch, do not enable gl-drm

* Thu Mar  5 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-3
- add e_dbus Provides/Obsoletes

* Fri Feb 27 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-1
- drop subpackages
- update to 1.13.1

* Mon Dec 15 2014 Tom Callaway <spot@fedoraproject.org> - 1.12.2-1
- initial package
