%bcond qt %[%{undefined rhel} || 0%{?rhel} < 10]

# Currently broken without DVB due to a bunch of random bits
# being built/installed even though they're DVB specific
%define with_dvb 1

Name:           v4l-utils
Version:        1.28.1
Release:        1%{?dist}
Summary:        Utilities for video4linux and DVB devices
# libdvbv5, dvbv5 utils, ir-keytable are GPL-2.0-only
# e.g. utils/cec-follower/cec-follower.cpp is (GPL-2.0-only OR BSD-3-Clause) 
# utils/qvidcap/capture.cpp, paint.cpp are LicenseRef-Fedora-Public-Domain
# utils/v4l2-sysfs-path/v4l2-sysfs-path.c is HPND-sell-variant
License:        GPL-2.0-or-later AND GPL-2.0-only AND (GPL-2.0-only OR BSD-3-Clause) AND LicenseRef-Fedora-Public-Domain AND HPND-sell-variant
URL:            http://www.linuxtv.org/downloads/v4l-utils/

Source0:        http://linuxtv.org/downloads/v4l-utils/v4l-utils-%{version}.tar.xz
# TODO: submit upstream
Patch0:         sbin-location.diff

BuildRequires:  alsa-lib-devel
BuildRequires:  doxygen
BuildRequires:  gettext
BuildRequires:  json-c-devel
BuildRequires:  kernel-headers
BuildRequires:  libjpeg-devel
BuildRequires:  meson >= 0.56
%if %{with qt}
BuildRequires:  desktop-file-utils
%if 0%{?fedora} < 41 || 0%{?rhel}
BuildRequires:  qt5-qtbase-devel
%else
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qt5compat-devel
%endif
%endif
BuildRequires:  systemd-devel
# For /usr/share/pkgconfig/udev.pc
BuildRequires:  systemd
# BPF decoder dependencies
BuildRequires:  clang
BuildRequires:  elfutils-libelf-devel
BuildRequires:  libbpf-devel

# For /lib/udev/rules.d ownership
Requires:       systemd-udev
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description
v4l-utils is a collection of various video4linux (V4L) and DVB utilities. The
main v4l-utils package contains cx18-ctl, ir-keytable, ivtv-ctl, v4l2-ctl and
v4l2-sysfs-path.


%package -n     libv4l
Summary:        Collection of video4linux support libraries 
# Some of the decompression helpers are GPL-2.0-or-later, the rest is LGPL-2.1-or-later
# lib/libv4lconvert/jidctflt.c and jpeg_memsrcdest.c are IJG-short
# lib/libv4lconvert/helper-funcs.h and libv4lsyscall-priv.h are BSD-2-Clause
License:        LGPL-2.1-or-later AND GPL-2.0-or-later AND IJG-short AND BSD-2-Clause
URL:            http://hansdegoede.livejournal.com/3636.html

%description -n libv4l
libv4l is a collection of libraries which adds a thin abstraction layer on
top of video4linux2 devices. The purpose of this (thin) layer is to make it
easy for application writers to support a wide variety of devices without
having to write separate code for different devices in the same class. libv4l
consists of 3 different libraries: libv4lconvert, libv4l1 and libv4l2.

libv4lconvert offers functions to convert from any (known) pixel-format
to V4l2_PIX_FMT_BGR24 or V4l2_PIX_FMT_YUV420.

libv4l1 offers the (deprecated) v4l1 API on top of v4l2 devices, independent
of the drivers for those devices supporting v4l1 compatibility (which many
v4l2 drivers do not).

libv4l2 offers the v4l2 API on top of v4l2 devices, while adding for the
application transparent libv4lconvert conversion where necessary.


%package -n     libv4l-devel
Summary:        Development files for libv4l
License:        LGPL-2.1-or-later AND GPL-2.0-or-later AND IJG-short AND BSD-2-Clause
URL:            http://hansdegoede.livejournal.com/3636.html
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description -n libv4l-devel
The libv4l-devel package contains libraries and header files for
developing applications that use libv4l.


%package        devel-tools
Summary:        Utilities for v4l2 / DVB driver development and debugging
License:        GPL-2.0-or-later AND GPL-2.0-only
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description    devel-tools
Utilities for v4l2 driver authors: v4l2-compliance and
v4l2-dbg.


%if %{with qt}
%package -n     qv4l2
Summary:        QT v4l2 test control and streaming test application
# utils/qv4l2/qv4l2.svg is CC-BY-SA-3.0
License:        GPL-2.0-or-later AND CC-BY-SA-3.0
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description -n qv4l2
QT v4l2 test control and streaming test application.
%endif


%if %{with dvb}
%package -n     libdvbv5
Summary:        Libraries to control, scan and zap on Digital TV channels
# /lib/include/libdvbv5/dvb-frontend.h is LGPL-2.1-or-later WITH Linux-syscall-note
License:        LGPL-2.1-or-later AND LGPL-2.1-or-later WITH Linux-syscall-note

%description -n libdvbv5
Libraries to control, scan and zap on Digital TV channels


%package -n libdvbv5-gconv
Summary:        Gconv files with the charsets For Digital TV.
License:        LGPL-2.1-or-later

%description -n libdvbv5-gconv
Some digital TV standards define their own charsets. Add library
support for them: EN 300 468 and ARIB STD-B24


%package -n     libdvbv5-devel
Summary:        Development files for libdvbv5
License:        LGPL-2.1-or-later AND LGPL-2.1-or-later WITH Linux-syscall-note
Requires:       libdvbv5%{?_isa} = %{version}-%{release}

%description -n libdvbv5-devel
The libdvbv5-devel package contains libraries and header
files for developing applications that use libdvbv5.


%package        -n dvb-tools
Summary:        Utilities for DVB driver
License:        GPL-2.0-or-later AND GPL-2.0-only
Requires:       libdvbv5%{?_isa} = %{version}-%{release}
Requires:       libv4l%{?_isa} = %{version}-%{release}
Requires:       v4l-utils%{?_isa} = %{version}-%{release}

%description    -n dvb-tools
Utilities and tools for DVB receivers.
%endif


%prep
%autosetup -p1

%build
%meson -Dbpf=auto -Ddoxygen-man=true -Ddoxygen-html=false \
  %{!?with_dvb:-Dlibdvbv5=disabled} \
  %{!?with_qt:-Dqv4l2=disabled -Dqvidcap=disabled}

%meson_build

%install
%meson_install

find $RPM_BUILD_ROOT -name '*.la' -delete
# Driver removed from upstream
rm -f $RPM_BUILD_ROOT%{_bindir}/decode_tm6000
rm -f $RPM_BUILD_ROOT%{_libdir}/{v4l1compat.so,v4l2convert.so}
mkdir $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.d
mv $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.d/libdvbv5.conf

%if %{with qt}
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qv4l2.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qvidcap.desktop
%endif

%find_lang %{name}
%find_lang libdvbv5


%ldconfig_scriptlets -n libv4l

%ldconfig_scriptlets -n libdvbv5

%files -f %{name}.lang
%doc README.md
%dir %{_sysconfdir}/rc_keymaps
%config(noreplace) %{_sysconfdir}/rc_maps.cfg
%{_udevrulesdir}/70-infrared.rules
%{_udevrulesdir}/../rc_keymaps/*
%{_bindir}/cec-ctl
%{_bindir}/cec-follower
%{_bindir}/ir-ctl
%{_bindir}/ir-keytable
%{_bindir}/media-ctl
%{_bindir}/rds-ctl
%{_bindir}/v4l2-ctl
%{_bindir}/v4l2-sysfs-path
%{_bindir}/v4l2-tracer
%{_mandir}/man1/cec-ctl*.1*
%{_mandir}/man1/cec-follower*.1*
%{_mandir}/man1/ir*.1*
%{_mandir}/man1/v4l*.1*
%{_mandir}/man5/rc_keymap*.5*
%exclude %{_mandir}/man1/v4l2-compliance.1*

%files devel-tools
%doc README.md
%{_bindir}/cec-compliance
%{_bindir}/v4l2-compliance
%{_mandir}/man1/cec-compliance.1*
%{_mandir}/man1/v4l2-compliance.1*
%{_sbindir}/v4l2-dbg

%files -n libv4l
%license COPYING.libv4l COPYING
%doc README.libv4l
%dir %{_libdir}/libv4l
%{_libdir}/libv4l/v4l*
%{_libdir}/libv4l/plugins
%{_libdir}/libv4l*.so.*

%files -n libv4l-devel
%doc README.lib-multi-threading ChangeLog TODO
%{_includedir}/libv4l*.h
%{_libdir}/libv4l*.so
%{_libdir}/libv4l/ov*
%{_libdir}/pkgconfig/libv4l*.pc

%if %{with qt}
%files -n qv4l2
%doc README.md
%{_bindir}/qv4l2
%{_bindir}/qvidcap
%{_datadir}/applications/qv4l2.desktop
%{_datadir}/applications/qvidcap.desktop
%{_datadir}/icons/hicolor/*/apps/qv4l2.*
%{_datadir}/icons/hicolor/*/apps/qvidcap.*
%{_mandir}/man1/qv4l2.1*
%{_mandir}/man1/qvidcap.1*
%endif

%if %{with dvb}
%files -n libdvbv5 -f libdvbv5.lang
%license COPYING.libdvbv5 COPYING
%doc lib/libdvbv5/README
%{_libdir}/libdvbv5*.so.*

%files -n libdvbv5-gconv
%{_libdir}/gconv/*.so
%{_libdir}/gconv/gconv-modules.d/libdvbv5.conf

%files -n libdvbv5-devel
%{_includedir}/libdvbv5/*.h
%{_libdir}/libdvbv5*.so
%{_libdir}/pkgconfig/libdvbv5*.pc
%{_mandir}/man3/*.3*

%files -n dvb-tools
%{_bindir}/cx18-ctl
%{_bindir}/dvb*
%{_bindir}/ivtv-ctl
%{_mandir}/man1/dvb*.1*
%endif


%changelog
* Thu Jul 25 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.28.1-1
- Update to 1.28.1
- Build f41+ with QT6

* Mon Jul 22 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.28.0-1
- Update to 1.28.0
- spec file cleanups, fixes, minor reorg

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.26.1-5
- Rebuilt for the bin-sbin merge

* Wed Apr 24 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.26.1-4
- Fix location of gconv conflicts

* Tue Apr 23 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.26.1-3
- Split dvb tools to it's own sub package

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.26.1-1
- Update to 1.26.1

* Mon Dec 04 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.26.0-1
- Update to 1.26.0

* Wed Aug 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.25.0-4
- Disable qv4l2 in RHEL 10 builds

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 20 2023 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> 1.25.0-1
- Updated to latest development branch

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Oct 23 2022 Hans de Goede <hdegoede@redhat.com> - 1.22.1-4
- Fix libv4lconvert issues when stride > width (with some formats)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 08 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.22.1-1
- Update to 1.22.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 Jeff Law <law@redhat.com> - 1.20.0-2
- Force C++14 as this code is not C++17 ready

* Wed Aug 12 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.20.0-1
- Update to 1.20.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 25 2020 Than Ngo <than@redhat.com> - 1.18.0-4
- Fixed FTBFS

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 22 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> 1.18.0-1
- Updated to latest stable release

* Mon Sep 02 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> 1.16.7-1
- Updated to new fix release with NIT parsing fix

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May  1 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.16.5-3
- The actual fix for libdvbv5 (rhbz 1695023)

* Tue Apr 16 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.16.5-2
- Upstream fix for libdvbv5 (rhbz 1695023)

* Sun Mar 31 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.16.5-1
- New upstream release 1.16.5

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 17 2018 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> 1.6.3-1
- Updated to new fix release, with should solve BPF protocol packaging issues

* Thu Nov 22 2018 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> 1.6.2-2
- Add dependencies needed to build BPF code

* Mon Nov 19 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.16.2-1
- New upstream release 1.16.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 29 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.14.2-2
- Add sys/sysmacros.h include fix patch

* Sun Apr 29 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.14.2-1
- New upstream release 1.14.2

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.12.5-6
- Remove obsolete scriptlets

* Thu Nov 02 2017 Hans de Goede <hdegoede@redhat.com> - 1.12.5-5
- Fix libv4lconvert failing on some hardware (rhbz#1508706)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri May 12 2017 Hans de Goede <hdegoede@redhat.com> - 1.12.5-1
- New upstream bugfix release 1.12.5

* Mon May  8 2017 Hans de Goede <hdegoede@redhat.com> - 1.12.4-1
- New upstream release 1.12.4

* Sun Mar 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.12.3-1
- New upstream release 1.12.3

* Sun Feb 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.12.2-1
- New upstream release 1.12.2
- Add new CEC utils

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Hans de Goede <hdegoede@redhat.com> - 1.10.1-1
- New upstream release 1.10.1
- Fix FTBFS (rhbz#1402087)

* Tue Mar  1 2016 Hans de Goede <hdegoede@redhat.com> - 1.10.0-2
- Update upside down table to apply to PEGATRON laptops (rhbz#1311545)

* Wed Feb 24 2016 Hans de Goede <hdegoede@redhat.com> - 1.10.0-1
- Upgrade to new upstream release 1.10.0
- Use qt5 instead of qt4 for qv4l2

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 12 2015 Gregor Jasny <gjasny@googlemail.com> - 1.8.1-1
- Upgrade to version 1.8.1

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.6.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Nov 22 2014 Mauro Carvalho Chehab <mchehab@osg.samsung.com> - 1.6.2-1
- Update to version 1.6.2 with contains several bugfixes

* Thu Nov 20 2014 Hans de Goede <hdegoede@redhat.com> - 1.6.0-2
- Fix crash when decoding 1920x1080 jpeg to YUV420

* Sun Oct 05 2014 Mauro Carvalho Chehab - 1.6.0-1
- Upgrade to version 1.6.0

* Mon Sep 08 2014 Mauro Carvalho Chehab - 1.4.0-1
- Upgrade to version 1.4.0

* Fri Aug 22 2014 Mauro Carvalho Chehab - 1.2.1-3
- Add ALSA support on qv4l2 and fix a couple issues at spec file

* Thu Aug 21 2014 Mauro Carvalho Chehab - 1.2.1-2
- Update to version 1.2.1 and add package for libdvbv5

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug  3 2013 Hans de Goede <hdegoede@redhat.com> - 1.0.0-1
- New upstream release 1.0.0 final
- Drop libdvb5 (made private upstream for now)

* Fri Jun 14 2013 Hans de Goede <hdegoede@redhat.com> - 0.9.5-2
- Add a few libv4l2rds patches from upstream, which bring libv4l2rds to its
  final API / ABI, so that apps build against it won't need a rebuild in the
  future

* Sun Jun  9 2013 Hans de Goede <hdegoede@redhat.com> - 0.9.5-1
- New upstream release 0.9.5 (rhbz#970412)
- Modernize specfile a bit

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 0.8.8-5
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.8.8-4
- rebuild against new libjpeg

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Hans de Goede <hdegoede@redhat.com> - 0.8.8-2
- Cherry-pick 2 patches from upstream git fixing an exotic crash (rhbz#838279)

* Tue May 22 2012 Hans de Goede <hdegoede@redhat.com> - 0.8.8-1
- New upstream release 0.8.8
- Add patches from upstream git to improve Pixart JPEG decoding
- Add patch from upstream git to fix building with latest kernels (rhbz#823863)

* Mon Apr  9 2012 Hans de Goede <hdegoede@redhat.com> - 0.8.7-1
- New upstream release 0.8.7
- Fixes rhbz#807656

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 17 2011 Hans de Goede <hdegoede@redhat.com> 0.8.5-1
- New upstream release 0.8.5
- Fixes rhbz#711492

* Wed Jun  1 2011 Hans de Goede <hdegoede@redhat.com> 0.8.4-1
- New upstream release 0.8.4

* Sat Mar 12 2011 Hans de Goede <hdegoede@redhat.com> 0.8.3-2
- Add a .desktop file for qv4l2
- Add fully versioned Requires on libv4l to other (sub)packages

* Thu Feb 10 2011 Hans de Goede <hdegoede@redhat.com> 0.8.3-1
- New upstream release 0.8.3

* Wed Jan 26 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-3
- Add missing BuildRequires: kernel-headers

* Mon Jan 24 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-2
- Change tarbal to official upstream 0.8.2 release
- This fixes multiple Makefile issues pointed out in the review (#671883)
- Add ir-keytable config files
- Explicitly specify CXXFLAGS so that qv4l2 gets build with rpm_opt_flags too

* Sat Jan 22 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-1
- Initial Fedora package
