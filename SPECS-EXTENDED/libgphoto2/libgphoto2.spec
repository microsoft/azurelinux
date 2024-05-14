Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%bcond_with gp2ddb

%global udevdir %(pkg-config --variable=udevdir udev)
%global port_version 0.12.0

Name:           libgphoto2
Version:        2.5.27
Release:        2%{?dist}
Summary:        Library for accessing digital cameras
# GPLV2+ for the main lib (due to exif.c) and most plugins, some plugins GPLv2
License:        GPLv2+ and GPLv2
URL:            https://www.gphoto.org/

Source0:        https://downloads.sourceforge.net/gphoto/%{name}-%{version}.tar.bz2
Patch1:         gphoto2-pkgcfg.patch
Patch2:         gphoto2-device-return.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  systemd-devel
%if %{with gp2ddb}
BuildRequires:  flex
BuildRequires:  bison
%endif
BuildRequires:  libtool-ltdl-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libcurl-devel
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  gd-devel
BuildRequires:  pkgconfig(libexif)
# -----------------------------------
# libgphoto2_port
# -----------------------------------
BuildRequires:  lockdev-devel
BuildRequires:  pkgconfig(libusb-1.0)
Requires:       lockdev
# -----------------------------------

# Temporarily required for patch3
BuildRequires: autoconf automake libtool gettext-devel

%description
libgphoto2 is a library that can be used by applications to access
various digital cameras. libgphoto2 itself is not a GUI application,
opposed to gphoto. There are GUI frontends for the gphoto2 library,
however, such as gtkam for example.

%package devel
Summary:        Headers and links to compile against the libgphoto2 library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      gphoto2-devel < 2.4.0-11
Provides:       gphoto2-devel = %{version}-%{release}

%description devel
libgphoto2 is a library that can be used by applications to access
various digital cameras. libgphoto2 itself is not a GUI application,
opposed to gphoto. There are GUI frontends for the gphoto2 library,
however, such as gtkam for example.

This package contains files needed to compile applications that
use libgphoto2.

%prep
%autosetup -p1
for f in AUTHORS ChangeLog COPYING libgphoto2_port/AUTHORS libgphoto2_port/COPYING.LIB `find -name 'README.*'`; do
    iconv -f ISO-8859-1 -t UTF-8 $f > $f.conv && mv -f $f.conv $f
done

%build
# Temporarily required for patch3
autoreconf -if

%configure \
    udevscriptdir='%{udevdir}'   \
    --with-drivers=all           \
    --with-doc-dir=%{_pkgdocdir} \
%if %{with gp2ddb}
    --enable-gp2ddb              \
%endif
    --disable-static             \
    --disable-rpath              \
    %{nil}

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool libgphoto2_port/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool libgphoto2_port/libtool


%make_build

%install
%make_install INSTALL="install -p" mandir=%{_mandir}

pushd packaging/linux-hotplug/
  export LIBDIR=%{buildroot}%{_libdir}
  export CAMLIBS=%{buildroot}%{_libdir}/%{name}/%{version}
  export LD_LIBRARY_PATH=%{buildroot}%{_libdir}

  # Output udev rules for device identification; this is used by GVfs gphoto2
  # backend and others.
  mkdir -p %{buildroot}%{_udevrulesdir}
  %{buildroot}%{_libdir}/%{name}/print-camera-list udev-rules version 201 > %{buildroot}%{_udevrulesdir}/40-libgphoto2.rules

  # Add support for hwdb (#1658259) 
  mkdir -p %{buildroot}%{_udevhwdbdir}
  %{buildroot}%{_libdir}/%{name}/print-camera-list hwdb version 201 > %{buildroot}%{_udevhwdbdir}/20-gphoto2.hwdb
popd

# remove circular symlink in /usr/include/gphoto2 (#460807)
rm -f %{buildroot}%{_includedir}/gphoto2/gphoto2

# remove unneeded print-camera-list from libdir (#745081)
rm -f %{buildroot}%{_libdir}/libgphoto2/print-camera-list

find %{buildroot} -type f -name "*.la" -print -delete

%find_lang %{name}-6
%find_lang %{name}_port-12
cat libgphoto2*.lang >> %{name}.lang

# https://fedoraproject.org/wiki/Packaging_tricks#With_.25doc
mkdir __doc
mv %{buildroot}%{_pkgdocdir}/* __doc
rm -rf %{buildroot}%{_pkgdocdir}
rm -rf %{buildroot}%{_datadir}/libgphoto2_port/*/vcamera/

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README.md NEWS
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}_port.so.*
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/%{version}/
%dir %{_libdir}/%{name}_port/
%dir %{_libdir}/%{name}_port/%{port_version}/
%{_libdir}/%{name}/%{version}/*.so
%{_libdir}/%{name}_port/%{port_version}/*.so
%{_udevrulesdir}/40-libgphoto2.rules
%{_udevhwdbdir}/20-gphoto2.hwdb
%{udevdir}/check-ptp-camera
%{_datadir}/libgphoto2/

%files devel
%doc __doc/*
%{_bindir}/gphoto2-config
%{_bindir}/gphoto2-port-config
%{_includedir}/gphoto2/
%{_libdir}/%{name}.so
%{_libdir}/%{name}_port.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}_port.pc
%{_mandir}/man3/%{name}.3*
%{_mandir}/man3/%{name}_port.3*

%changelog
* Fri Mar 26 2021 Henry Li <lihl@microsoft.com> - 2.5.27-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- systemd-devel contains the .pc file to provide pkgconfig variables

* Wed Mar 10 2021 Josef Ridky <jridky@redhat.com> - 2.5.27-1
- New upstream release 2.5.27 (#1931187)

* Wed Jan 27 2021 Josef Ridky <jridky@redhat.com> - 2.5.26-1
- New upstream release 2.5.26 (#1887201)
- Add support for hwdb output (#1658259)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 07 2020 Josef Ridky <jridky@redhat.com> - 2.5.25-1
- New upstream release 2.5.25 (#1839543)

* Thu Aug  6 2020 Daniel P. Berrangé <berrange@redhat.com> - 2.5.24-4
- Fix configure check for symbol versioning with GCC 10 (rhbz #1862745)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 13 2020 Daniel P. Berrangé <berrange@redhat.com> - 2.5.24-2
- Add libcurl for Lumix WIFI support

* Wed May 13 2020 Daniel P. Berrangé <berrange@redhat.com> - 2.5.24-1
- Update to 2.5.24 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 21 2019 Josef Řídký <jridky@redhat.com> - 2.5.23-1
- New upstream release 2.5.23

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Bastien Nocera <bnocera@redhat.com> - 2.5.21-2
- Fix camera mounts not showing up in GNOME

* Tue Dec 11 2018 Bastien Nocera <bnocera@redhat.com> - 2.5.21-1
- Update to 2.5.21

* Tue Nov 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.20-1
- Update to 2.5.20

* Sun Sep 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.19-1
- Update to 2.5.19

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.18-1
- Update to 2.5.18

* Fri Apr 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.17-1
- Update to 2.5.17

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.16-2
- Switch to %%ldconfig_scriptlets

* Wed Nov 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.16-1
- Update to 2.5.16

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.14-1
- Update to 2.5.14

* Sat Apr 29 2017 Jon Disnard <parasense@fedoraproject.org> - 2.5.23-1
- Update to 2.5.13

* Sun Feb 12 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.12-1
- Update to 2.5.12

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 21 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.5.11-1
- Update to 2.5.11

* Sun Jul 10 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.5.10-1
- Update to 2.5.10 for new device support
- Use %%license
- minor cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 28 2015 Jon Disnard <parasense@fedoraproject.org> 2.5.8-1
- Update to 2.5.8 for new device support
- Drop USB result patch that went upstream (formerly patch#5)
- Drop IXANY patch that went upstream (formerly patch#3)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 2.5.7-3
- rebuild against libvpx 1.4.0

* Thu Mar 12 2015 Tim Waugh <twaugh@redhat.com> 2.5.7-2
- Apply upstream patch to correctly report errors when performing
  USB control transfers (bug #1201048).

* Tue Jan 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.5.7-1
- Update to 2.5.7 for new device support

* Sun Sep 07 2014 Jindrich Novy <novyjindrich@gmail.com> 2.5.5.1-1
- update to 2.5.5.1 - regression fix release of 2.5.5

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Tim Waugh <twaugh@redhat.com> - 2.5.3-7
- Moved runtime-required files to main package (bug #1086411).

* Wed Feb 12 2014 Jon Disnard <jdisnard@gmail.com> - 2.5.3-6
- Bump to latest upstream version.

* Wed Aug 28 2013 Tim Waugh <twaugh@redhat.com> - 2.5.2-5
- Fixed documentation issue due to unversioned doc dirs (bug #1001263).

* Fri Aug 16 2013 Tim Waugh <twaugh@redhat.com> - 2.5.2-4
- Build against libusbx instead of libusb (bug #997880).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 2.5.2-2
- rebuild for new GD 2.1.0

* Mon May  6 2013 Hans de Goede <hdegoede@redhat.com> - 2.5.2-1
- New upstream release bugfix 2.5.2
- Drop bugfix patches (merged upstream)

* Sat May  4 2013 Hans de Goede <hdegoede@redhat.com> - 2.5.1.1-4
- Fix crash when dealing with PTP devices without a memory card (rhbz#915688)

* Thu May  2 2013 Hans de Goede <hdegoede@redhat.com> - 2.5.1.1-3
- Fix PTP devices not working in USB-3 ports (rhbz#819918)
- Cleanup spec-file

* Tue Apr 23 2013 Tim Waugh <twaugh@redhat.com> 2.5.1.1-2
- Use _udevrulesdir macro.

* Tue Feb 19 2013 Jindrich Novy <jnovy@redhat.com> 2.5.1.1-1
- update to 2.5.1.1

* Sun Feb 17 2013 Jindrich Novy <jnovy@redhat.com> 2.5.0-8
- fix camera detection - thanks to Panu Matilainen (#912040)

* Wed Jan 30 2013 Jindrich Novy <jnovy@redhat.com> 2.5.0-7
- move /lib files to /usr/lib
- fix changelog

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.5.0-6
- rebuild due to "jpeg8-ABI" feature drop

* Sun Jan 13 2013 Jindrich Novy <jnovy@redhat.com> 2.5.0-5
- remove deprecated HAL file (#894527)

* Sat Dec 01 2012 Jindrich Novy <jnovy@redhat.com> 2.5.0-4
- compile with -fno-strict-aliasing (because of ptp.c)

* Wed Sep 19 2012 Hans de Goede <hdegoede@redhat.com> 2.5.0-3
- Fix the usbscsi port driver not working, this fixes many miniature
  (keychain) photo frames no longer being accessible

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Jindrich Novy <jnovy@redhat.com> 2.5.0-1
- update to 2.5.0

* Mon Apr 16 2012 Jindrich Novy <jnovy@redhat.com> 2.4.14-1
- update to 2.4.14

* Wed Mar 21 2012 Jindrich Novy <jnovy@redhat.com> 2.4.13-1
- update to 2.4.13

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Jindrich Novy <jnovy@redhat.com> 2.4.11-2
- remove unneeded print-camera-list from libdir (#745081)

* Mon Apr 18 2011 Jindrich Novy <jnovy@redhat.com> 2.4.11-1
- update to 2.4.11

* Wed Feb 09 2011 Jindrich Novy <jnovy@redhat.com> 2.4.10.1-1
- update to 2.4.10.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Caolán McNamara <caolanm@redhat.com> 2.4.10-4
- rebuild for dependencies

* Wed Oct 20 2010 Jindrich Novy <jnovy@redhat.com> 2.4.10-3
- move udev helper scripts to /lib/udev (#644552)

* Mon Sep 06 2010 Jindrich Novy <jnovy@redhat.com> 2.4.10-2
- BR: gd-devel because of ax203 and st2205 camlibs (#630570)

* Tue Aug 17 2010 Jindrich Novy <jnovy@redhat.com> 2.4.10-1
- update to 2.4.10

* Mon Jul 12 2010 Dan Horák <dan[at]danny.cz> 2.4.9-2
- remove the need to call autoreconf

* Mon Apr 12 2010 Jindrich Novy <jnovy@redhat.com> 2.4.9-1
- update to 2.4.9

* Mon Jan 25 2010 Jindrich Novy <jnovy@redhat.com> 2.4.8-1
- update to 2.4.8

* Fri Dec 18 2009 Jindrich Novy <jnovy@redhat.com> 2.4.7-3
- remove circular symlink in /usr/include/gphoto2 (#460807)

* Fri Oct 23 2009 Jindrich Novy <jnovy@redhat.com> 2.4.7-2
- return the dual-mode device to kernel once we don't use it (#530545)

* Tue Aug 18 2009 Jindrich Novy <jnovy@redhat.com> 2.4.7-1
- update to 2.4.7
- drop udev patch, applied upstream
- update storage patch

* Sun Aug 09 2009 David Zeuthen <davidz@redhat.com> 2.4.6-3
- Add patch from https://sourceforge.net/tracker/?func=detail&aid=2801117&group_id=8874&atid=308874
  and generate generic udev rules for device identification (ID_GPHOTO2* properties)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Jindrich Novy <jnovy@redhat.com> 2.4.6-1
- update to 2.4.6
- new IDs for Kodak V803, M1063, Canon PowerShot A650IS, SD990 (aka IXUS 980IS),
  SD880IS, A480, Canon EOS 50D, Fuji FinePix S1000fd
- many Canon related fixes

* Wed Apr 08 2009 Jindrich Novy <jnovy@redhat.com> 2.4.5-1
- update to 2.4.5
- remove .canontimeout patch, applied upstream

* Wed Apr 01 2009 Jindrich Novy <jnovy@redhat.com> 2.4.4-4
- increase timeouts for Canon cameras (#476355), thanks to
  Andrzej Nowak and Russell Harrison

* Thu Mar 05 2009 Caolán McNamara <caolanm@redhat.com> - 2.4.4-3
- tweak BR to get to build

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Jindrich Novy <jnovy@redhat.com> 2.4.4-1
- update to 2.4.4
- many fixes and improvements to Nikon and Canon cameras
- translation updates

* Thu Nov 13 2008 Rex Dieter <rdieter@fedoraproject.org> 2.4.3-2
- respin (libtool)

* Mon Oct 20 2008 Jindrich Novy <jnovy@redhat.com> 2.4.3-1
- update to libgphoto2-2.4.3

* Tue Sep 23 2008 Jindrich Novy <jnovy@redhat.com> 2.4.2-2
- convert all shipped docs to UTF-8

* Fri Aug 01 2008 Jindrich Novy <jnovy@redhat.com> 2.4.2-1
- update to 2.4.2
- contains many fixes in the Canon camera communication interface
- drop build patch, no more needed

* Mon Jul 07 2008 Jindrich Novy <jnovy@redhat.com> 2.4.1-6
- increase maximal number of entries in the camera list (#454245)

* Fri Jun 20 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.1-5
- fix pkgcfg patch to match actual .pc file names (fixes kdegraphics build)

* Thu Jun 12 2008 Jindrich Novy <jnovy@redhat.com> 2.4.1-3
- libgphoto2-devel requires libusb-devel and libexif-devel for
  pkgconfig

* Wed Jun 04 2008 Jindrich Novy <jnovy@redhat.com> 2.4.1-2
- fix obsoletes
- workaround problem with coreutils-6.12 and RHEL5-xen kernels
  what prevents libgphoto2 koji build

* Mon Jun 02 2008 Jindrich Novy <jnovy@redhat.com> 2.4.1-1
- update to 2.4.1 (#443515, #436138)

* Thu May 29 2008 Stepan Kasal <skasal@redhat.com> 2.4.0-3
- drop gphoto2-norpath.patch
- use quoted here-document in %%prep
- fix some typos in m4 sources
- run autoreconf to get autotools right

* Mon Apr 21 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-2
- apply patch to fix build with libusb

* Fri Apr 18 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-1
- backport patch from upstream to avoid segfault when
  data phase is skipped for certain devices (#435413)
- initial build

* Mon Apr 14 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-0.2
- review fixes, thanks to Hans de Goede: (#437285)
  - remove unused macro
  - don't exclude s390/s390x
  - preserve timestamps
  - fix license

* Thu Mar 13 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-0.1
- initial libgphoto2 packaging
