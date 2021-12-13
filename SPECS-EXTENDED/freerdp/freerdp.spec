Vendor:         Microsoft Corporation
Distribution:   Mariner
# Can be rebuilt with FFmpeg/H264 support enabled by passing "--with=ffmpeg",
# "--with=x264" or "--with=openh264" to mock/rpmbuild; or by globally setting
# these variables:

#global _with_ffmpeg 1
#global _with_x264 1
#global _with_openh264 1

# Momentarily disable GSS support
# https://github.com/FreeRDP/FreeRDP/issues/4348
#global _with_gss 1

# Disable server support in RHEL
# https://bugzilla.redhat.com/show_bug.cgi?id=1639165
%{!?rhel:%global _with_server 1}

# Disable support for missing codecs in RHEL
%{!?rhel:%global _with_soxr 1}

%global _with_lame 1


Name:           freerdp
Version:        2.2.0
Release:        3%{?dist}
Summary:        Free implementation of the Remote Desktop Protocol (RDP)
License:        ASL 2.0
URL:            http://www.freerdp.com/

Source0:        https://github.com/FreeRDP/FreeRDP/archive/%{version}/FreeRDP-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake >= 2.8
BuildRequires:  cups-devel
BuildRequires:  gsm-devel
%{?_with_lame:BuildRequires:  lame-devel}
BuildRequires:  libicu-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libXrandr-devel
%{?_with_server:BuildRequires:  libXtst-devel}
BuildRequires:  libXv-devel
%{?_with_openh264:BuildRequires:  openh264-devel}
%{?_with_x264:BuildRequires:  x264-devel}
%{?_with_server:BuildRequires:  pam-devel}
BuildRequires:  xmlto
BuildRequires:  zlib-devel
BuildRequires:  multilib-rpm-config

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-fft-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
%{?_with_gss:BuildRequires:  pkgconfig(krb5) >= 1.13}
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(openssl)
%{?_with_soxr:BuildRequires:  pkgconfig(soxr)}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)

%{?_with_ffmpeg:
BuildRequires:  pkgconfig(libavcodec) >= 57.48.101
BuildRequires:  pkgconfig(libavutil)
}

Provides:       xfreerdp = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       libwinpr%{?_isa} = %{version}-%{release}

%description
The xfreerdp & wlfreerdp Remote Desktop Protocol (RDP) clients from the FreeRDP
project.

xfreerdp & wlfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%package        libs
Summary:        Core libraries implementing the RDP protocol
Requires:       libwinpr%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-plugins < 1:1.1.0
Provides:       %{name}-plugins = %{version}-%{release}
%description    libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 2.8

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}-libs.

%{?_with_server:
%package        server
Summary:        Server support for %{name}
Requires:       libwinpr%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    server
The %{name}-server package contains servers which can export a desktop via
the RDP protocol.
}

%package -n     libwinpr
Summary:        Windows Portable Runtime
Provides:       %{name}-libwinpr = %{version}-%{release}
Obsoletes:      %{name}-libwinpr < 1:1.2.0

%description -n libwinpr
WinPR provides API compatibility for applications targeting non-Windows
environments. When on Windows, the original native API is being used instead of
the equivalent WinPR implementation, without having to modify the code using it.

%package -n     libwinpr-devel
Summary:        Windows Portable Runtime development files
Requires:       libwinpr%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 2.8

%description -n libwinpr-devel
The %{name}-libwinpr-devel package contains libraries and header files for
developing applications that use %{name}-libwinpr.

%prep
%autosetup -p1 -n FreeRDP-%{version}

# Rpmlint fixes
find . -name "*.h" -exec chmod 664 {} \;
find . -name "*.c" -exec chmod 664 {} \;

%build
%cmake %{?_cmake_skip_rpath} \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
    -DWITH_ALSA=ON \
    -DWITH_CUPS=ON \
    -DWITH_CHANNELS=ON -DBUILTIN_CHANNELS=OFF \
    -DWITH_CLIENT=ON \
    -DWITH_DIRECTFB=OFF \
    -DWITH_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_GSM=ON \
    -DWITH_GSSAPI=%{?_with_gss:ON}%{?!_with_gss:OFF} \
    -DWITH_GSTREAMER_1_0=ON -DWITH_GSTREAMER_0_10=OFF \
    -DGSTREAMER_1_0_INCLUDE_DIRS=%{_includedir}/gstreamer-1.0 \
    -DWITH_ICU=ON \
    -DWITH_IPP=OFF \
    -DWITH_JPEG=ON \
    -DWITH_LAME=%{?_with_lame:ON}%{?!_with_lame:OFF} \
    -DWITH_MANPAGES=ON \
    -DWITH_OPENH264=%{?_with_openh264:ON}%{?!_with_openh264:OFF} \
    -DWITH_OPENSSL=ON \
    -DWITH_PCSC=ON \
    -DWITH_PULSE=ON \
    -DWITH_SERVER=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SERVER_INTERFACE=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SHADOW_X11=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SHADOW_MAC=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SOXR=%{?_with_soxr:ON}%{?!_with_soxr:OFF} \
    -DWITH_WAYLAND=ON \
    -DWITH_X11=ON \
    -DWITH_X264=%{?_with_x264:ON}%{?!_with_x264:OFF} \
    -DWITH_XCURSOR=ON \
    -DWITH_XEXT=ON \
    -DWITH_XKBFILE=ON \
    -DWITH_XI=ON \
    -DWITH_XINERAMA=ON \
    -DWITH_XRENDER=ON \
    -DWITH_XTEST=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_XV=ON \
    -DWITH_ZLIB=ON \
%ifarch x86_64
    -DWITH_SSE2=ON \
    -DWITH_VAAPI=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
%else
    -DWITH_SSE2=OFF \
%endif
%ifarch armv7hl
    -DARM_FP_ABI=hard \
    -DWITH_NEON=OFF \
%endif
%ifarch armv7hnl
    -DARM_FP_ABI=hard \
    -DWITH_NEON=ON \
%endif
%ifarch armv5tel armv6l armv7l
    -DARM_FP_ABI=soft \
    -DWITH_NEON=OFF \
%endif
    .

%make_build

pushd winpr/tools/makecert-cli
%make_build
popd

%install
%make_install
%make_install COMPONENT=tools

find %{buildroot} -name "*.a" -delete

%multilib_fix_c_header --file %{_includedir}/freerdp2/freerdp/build-config.h

%files
%{_bindir}/winpr-hash
%{_bindir}/winpr-makecert
%{_bindir}/wlfreerdp
%{_bindir}/xfreerdp
%{_mandir}/man1/winpr-hash.1*
%{_mandir}/man1/winpr-makecert.1*
%{_mandir}/man1/wlfreerdp.1*
%{_mandir}/man1/xfreerdp.1*

%files libs
%license LICENSE
%doc README.md ChangeLog
%{_libdir}/freerdp2/
%{_libdir}/libfreerdp-client2.so.*
%{?_with_server:
%{_libdir}/libfreerdp-server2.so.*
%{_libdir}/libfreerdp-shadow2.so.*
%{_libdir}/libfreerdp-shadow-subsystem2.so.*
}
%{_libdir}/libfreerdp2.so.*
%{_libdir}/libuwac0.so.*
%{_mandir}/man7/wlog.*

%files devel
%{_includedir}/freerdp2
%{_includedir}/uwac0
%{_libdir}/cmake/FreeRDP2
%{_libdir}/cmake/FreeRDP-Client2
%{?_with_server:
%{_libdir}/cmake/FreeRDP-Server2
%{_libdir}/cmake/FreeRDP-Shadow2
}
%{_libdir}/cmake/uwac0
%{_libdir}/libfreerdp-client2.so
%{?_with_server:
%{_libdir}/libfreerdp-server2.so
%{_libdir}/libfreerdp-shadow2.so
%{_libdir}/libfreerdp-shadow-subsystem2.so
}
%{_libdir}/libfreerdp2.so
%{_libdir}/libuwac0.so
%{_libdir}/pkgconfig/freerdp2.pc
%{_libdir}/pkgconfig/freerdp-client2.pc
%{?_with_server:
%{_libdir}/pkgconfig/freerdp-server2.pc
%{_libdir}/pkgconfig/freerdp-shadow2.pc
}
%{_libdir}/pkgconfig/uwac0.pc

%{?_with_server:
%files server
%{_bindir}/freerdp-proxy
%{_bindir}/freerdp-shadow-cli
%{_mandir}/man1/freerdp-shadow-cli.1*
}

%files -n libwinpr
%license LICENSE
%doc README.md ChangeLog
%{_libdir}/libwinpr2.so.*
%{_libdir}/libwinpr-tools2.so.*

%files -n libwinpr-devel
%{_libdir}/cmake/WinPR2
%{_includedir}/winpr2
%{_libdir}/libwinpr2.so
%{_libdir}/libwinpr-tools2.so
%{_libdir}/pkgconfig/winpr2.pc
%{_libdir}/pkgconfig/winpr-tools2.pc

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.2.0-3
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:2.2.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jul 23 2020 Simone Caronni <negativo17@gmail.com> - 2:2.2.0-1
- Update to 2.2.0.

* Tue Jun 30 2020 Simone Caronni <negativo17@gmail.com> - 2:2.1.2-1
- Update to 2.1.2.

* Thu May 21 2020 Ondrej Holy <oholy@redhat.com> - 2:2.1.1-1
- Update to 2.1.1.

* Fri May 15 2020 Ondrej Holy <oholy@redhat.com> - 2:2.1.0-1
- Update to 2.1.0 (#1833540).

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 2:2.0.0-57.20200207git245fc60
- Rebuild for ICU 67

* Fri Feb 07 2020 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-56.20200207git245fc60
- Update to latest snapshot.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-55.20190820git6015229
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 2:2.0.0-54.20190820git6015229
- Rebuild for ICU 65

* Tue Aug 20 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-53.20190820git6015229
- Update to latest snapshot.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-52.20190918git5e672d4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-51.20190918git5e672d4
- Update to latest snapshot.

* Sat May 18 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-50.20190517gitb907324
- Update to latest snapshot.

* Wed Mar 06 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-49.20190304git435872b
- Fix for GFX color depth (Windows 10).

* Thu Feb 28 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-48.20190228gitce386c8
- Update to latest snapshot post rc4.
- CVE-2018-1000852 (#1661642).

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-47.rc4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 29 2018 Ondrej Holy <oholy@redhat.com> - 2:2.0.0-47.rc4
- Update to 2.0.0-rc4

* Mon Oct 15 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-46.20181008git00af869
- Enable Xtest option (#1559606).

* Mon Oct 15 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-45.20181008git00af869
- Update to last snapshot post 2.0.0-rc3.

* Mon Aug 20 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-44.rc3
- Update SPEC file.

* Sat Aug 04 2018 Mike DePaulo <mikedep333@fedoraproject.org> - 2:2.0.0-43.20180801.rc3
- Update to 2.0.0-rc3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-42.20180405gita9ecd6a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-41.20180405gita9ecd6a
- Update to latest snapshot.

* Wed Mar 21 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-40.20180320gitde83f4d
- Add PAM support (fixes freerdp-shadow-cli). Thanks Paolo Zeppegno.
- Update to latest snapshot.

* Thu Mar 15 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-39.20180314gitf8baeb7
- Update to latest snapshot.
- Fixes connection to RDP servers with the latest Microsoft patches:
  https://github.com/FreeRDP/FreeRDP/issues/4449

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-38.20180115git8f52c7e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Karsten Hopp <karsten@redhat.com> - 2.0.0-37git}
- use versioned build requirement on pkgconfig(openssl) to prevent using
  compat-openssl10-devel instead of openssl-devel

* Tue Jan 16 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-36.20180115git8f52c7e
- Update to latest snapshot.
- Make GSS support optional and disable it for now (#1534094 and FreeRDP #4348,
  #1435, #4363).

* Wed Dec 20 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-35.20171220gitbfe8359
- Update to latest snapshot post 2.0.0rc1.

* Mon Sep 11 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-34.20170831git3b83526
- Update to latest snapshot.
- Trim changelog.

* Mon Aug 07 2017 Björn Esser <besser82@fedoraproject.org> - 2:2.0.0-33.20170724gitf8c9f43
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-32.20170724gitf8c9f43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-31.20170724gitf8c9f43
- Update to latest snapshot, Talos security fixes.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-30.20170710gitf580bea
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-29.20170710gitf580bea
- Update to latest snapshot.

* Mon Jun 26 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-28.20170623git9904c32
- Update to latest snapshot.

* Mon May 15 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-27.20170512gitb1df835
- Update to latest snapshot.

* Thu Apr 20 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-26.20170419gitbfcf8e7
- Update to latest 2.0 snapshot.

* Thu Apr 13 2017 Orion Poplawski <orion@cora.nwra.com> - 2:2.0.0-25.20170317git8c68761
- Install tools via make install

* Wed Mar 22 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-24.20170317git8c68761
- Update to latest snapshot.

* Mon Mar 06 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-23.20170302git210de68
- Remove shared libxfreerdp-client shared library.

* Thu Mar 02 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-22.20170302git210de68
- Move libxfreerdp-client shared object into devel subpackage.

* Thu Mar 02 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-21.20170302git210de68
- Update to latest snapshot.
- Update build requirements, tune build options.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-20.20161228git90877f5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-19.20161228git90877f5
- Update to latest snapshot.
