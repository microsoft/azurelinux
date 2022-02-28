Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:    Library to make writing a VNC server easy
Name:       libvncserver
Version:    0.9.13
Release:    3%{?dist}

# NOTE: --with-filetransfer => GPLv2
License:    GPLv2+
URL:        http://libvnc.github.io/
Source0:    https://github.com/LibVNC/libvncserver/archive/LibVNCServer-%{version}.tar.gz

## TLS security type enablement patches
# https://github.com/LibVNC/libvncserver/pull/234
Patch10: 0001-libvncserver-Add-API-to-add-custom-I-O-entry-points.patch
Patch11: 0002-libvncserver-Add-channel-security-handlers.patch

## downstream patches
Patch102: libvncserver-LibVNCServer-0.9.13-system-crypto-policy.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
#BuildRequires:  pkgconfig(lzo2)
#BuildRequires:  ffmpeg-devel
BuildRequires:  gettext-devel
BuildRequires:  libgcrypt-devel


BuildRequires:  lzo-devel
BuildRequires:  lzo-minilzo
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
# Additional deps for --with-x11vnc, see https://bugzilla.redhat.com/show_bug.cgi?id=864947
BuildRequires:  pkgconfig(avahi-client)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xtst)

# For %%check
BuildRequires:  xorg-x11-xauth
BuildRequires:  zlib-devel

%description
LibVNCServer makes writing a VNC server (or more correctly, a program exporting
a frame-buffer via the Remote Frame Buffer protocol) easy.

It hides the programmer from the tedious task of managing clients and
compression schemata.

%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
# libvncserver-config deps
Requires:   coreutils

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-LibVNCServer-%{version}

## FIXME: needs rebasing
%patch10 -p1 -b .tls-1
%patch11 -p1 -b .tls-2

%patch102 -p1 -b .crypto_policy

# Nuke bundled minilzo
rm -fv common/lzodefs.h common/lzoconf.h commmon/minilzo.h common/minilzo.c


# Fix encoding
for file in ChangeLog ; do
    mv ${file} ${file}.OLD && \
    iconv -f ISO_8859-1 -t UTF8 ${file}.OLD > ${file} && \
    touch --reference ${file}.OLD $file
done


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake3 ..
popd
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS* README* TODO*
%{_libdir}/libvncclient.so.1
%{_libdir}/libvncclient.so.%{version}
%{_libdir}/libvncserver.so.1
%{_libdir}/libvncserver.so.%{version}

%files devel
#{_bindir}/libvncserver-config
%{_includedir}/rfb/
%{_libdir}/libvncclient.so
%{_libdir}/libvncserver.so
%{_libdir}/pkgconfig/libvncclient.pc
%{_libdir}/pkgconfig/libvncserver.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.13-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jul 02 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.9.13-2
- tls patches rebased

* Thu Jul 02 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.9.13-1
- 0.9.13
- FIXME/TODO: tls patches need rebasing, work-in-progress

* Tue Feb 11 2020 Sérgio Basto <sergio@serjux.com> - 0.9.12-1
- Update to 0.9.12

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Jonas Ådahl <jadahl@redhat.com> - 0.9.11-7
- Add API to enable implementing TLS security type

* Mon Feb 26 2018 Petr Pisar <ppisar@redhat.com> - 0.9.11-6
- Fix CVE-2018-7225 (bug #1546860)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.9.11-2.1
- revert soname bump for < f26

* Tue May 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.9.11-2
- libvncclient sets +SRP in priority string (#1449605)
- libvncserver blocks gtk-vnc clients >= 0.7.0 (#1451321)

* Tue Feb 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.9.11-1
- 0.9.11 (#1421948)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 18 2016 Than Ngo <than@redhat.com> - 0.9.10-5
- fix conflict with max() macro with gcc6, which causes build failure in KDE/Qt
  like krfb

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Simone Caronni <negativo17@gmail.com> - 0.9.10-3
- Update crypto policies patch.

* Sat Dec 12 2015 Simone Caronni <negativo17@gmail.com> - 0.9.10-2
- Add patch for using system crypto policies (#1179318).

* Fri Dec 11 2015 Simone Caronni <negativo17@gmail.com> - 0.9.10-1
- Update to official 0.9.10 release, update configure parameters and remove
  upstreamed patches.
- Trim changelog.
- Clean up SPEC file.
- Add license macro.
- Remove very old obsolete/provides on pacakge with camel case (LibVNCServer).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-0.7.20140718git9453be42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Sep 25 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.10-0.6.20140718git9453be42
- Security fixes (#1145878) ...
- CVE-2014-6051 (#1144287)
- CVE-2014-6052 (#1144288)
- CVE-2014-6053 (#1144289)
- CVE-2014-6054 (#1144291)
- CVE-2014-6055 (#1144293)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-0.5.20140718git9453be42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug 03 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.10-0.4.20140718git9453be42
- 20140718git9453be42 snapshot

* Sun Aug 03 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.10-0.3.20140405git646f844f
- include krfb patches (upstream pull request #16)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-0.2.20140405git646f844f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.10-0.1.20140405git646f844f
- Update to the latest git commit 646f844 (#1092245)

* Mon Mar 31 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.9-11
- x11vnc crash when client connect (#972618)
  pull in some upstream commits that may help

* Sat Dec 21 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.9.9-10
- include additional dependencies for x11vnc (#864947)
- %%build: --disable-silent-rules
- cleanup spec, drop support for old rpm (el5)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.9-8
- Automagic dependencies, explitictly build --with-gcrypt --with-png (#852660)

* Thu Feb 14 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.9-7
- pkgconfig love (#854111)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.9.9-5
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.9.9-4
- rebuild against new libjpeg

* Thu Jul 26 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.9-3
- libvncserver fails to build in mock with selinux enabled (#843603)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 07 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.9-1
- 0.9.9
