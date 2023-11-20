%global with_lua 1
%global plugins_version 4.0

Summary:        Network traffic analyzer
Name:           wireshark
Version:        4.0.8
Release:        1%{?dist}
License:        BSD-1-Clause AND BSD-2-Clause AND BSD-3-Clause AND MIT AND GPL-2.0-or-later AND LGPL-2.0-or-later AND Zlib AND ISC AND (BSD-3-Clause OR GPL-2.0-only) AND (GPL-2.0-or-later AND Zlib)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.wireshark.org/
Source0:        https://wireshark.org/download/src/%{name}-%{version}.tar.xz
Source1:        90-wireshark-usbmon.rules
Patch2:         wireshark-0002-Customize-permission-denied-error.patch
Patch3:         wireshark-0003-fix-string-overrun-in-plugins-profinet.patch
Patch4:         wireshark-0004-Restore-Fedora-specific-groups.patch
Patch5:         wireshark-0005-Fix-paths-in-a-wireshark.desktop-file.patch
Patch6:         wireshark-0006-Move-tmp-to-var-tmp.patch
Patch7:         wireshark-0007-cmakelists.patch
Patch8:         wireshark-0008-glib2-g_strdup-build.patch
Patch9:         wireshark-0009-fix-asn2wrs-cmake.patch
Patch10:        wireshark-0010-ripemd-fips-core-dump.patch
Patch11:        wireshark-0011-manage-interfaces-crash.patch
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  c-ares-devel
BuildRequires:  cmake
BuildRequires:  elfutils-devel
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  glib2-devel
BuildRequires:  gnutls-devel
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libnghttp2-devel
BuildRequires:  libnl3-devel
BuildRequires:  libpcap-devel >= 0.9
BuildRequires:  libselinux-devel
BuildRequires:  libsmi-devel
BuildRequires:  libssh-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  pcre2-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  systemd-devel
BuildRequires:  xdg-utils
BuildRequires:  zlib-devel
BuildRequires:  perl(English)
BuildRequires:  perl(Pod::Html)
BuildRequires:  perl(Pod::Man)
BuildRequires:  perl(open)
#install tshark together with wireshark GUI
Requires:       %{name}-cli = %{version}-%{release}
Requires:       c-ares
Requires:       glib2
Requires:       systemd-libs
Requires:       zlib

%description
Wireshark allows you to examine protocol data stored in files or as it is
captured from wired or wireless (WiFi or Bluetooth) networks, USB devices,
and many other sources.  It supports dozens of protocol capture file formats
and understands more than a thousand protocols.

It has many powerful features including a rich display filter language
and the ability to reassemble multiple protocol packets in order to, for
example, view a complete TCP stream, save the contents of a file which was
transferred over HTTP or CIFS, or play back an RTP audio stream.

%package        cli
Summary:        Network traffic analyzer
Requires(post): systemd-udev
Requires(pre):  shadow-utils

%description    cli
This package contains command-line utilities, plugins, and documentation for
Wireshark.

%package        devel
Summary:        Development headers and libraries for wireshark
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel
Requires:       glibc-devel

%description devel
The wireshark-devel package contains the header files, developer
documentation, and libraries required for development of wireshark scripts
and plugins.

%prep
%autosetup -S git

%build
%cmake -G "Unix Makefiles" \
  -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
  -DDISABLE_WERROR=ON \
  -DENABLE_LUA=ON \
  -DENABLE_LIBXML2=ON \
  -DENABLE_NETLINK=ON \
  -DENABLE_NGHTTP2=ON \
  -DENABLE_PLUGINS=ON \
  -DENABLE_SMI=ON \
  -DBUILD_androiddump=OFF \
  -DBUILD_dcerpcidl2wrs=OFF \
  -DBUILD_mmdbresolve=OFF \
  -DBUILD_randpktdump=OFF \
  -DBUILD_sdjournal=ON \
  -DBUILD_wireshark=OFF \
  .

%cmake_build

%install
%cmake_install


#install devel files (inspired by debian/wireshark-dev.header-files)
install -d -m 0755  %{buildroot}%{_includedir}/wireshark
IDIR="%{buildroot}%{_includedir}/wireshark"
mkdir -p "${IDIR}/epan"
mkdir -p "${IDIR}/epan/crypt"
mkdir -p "${IDIR}/epan/ftypes"
mkdir -p "${IDIR}/epan/dfilter"
mkdir -p "${IDIR}/epan/dissectors"
mkdir -p "${IDIR}/epan/wmem"
mkdir -p "${IDIR}/wiretap"
mkdir -p "${IDIR}/wsutil"
mkdir -p %{buildroot}%{_udevrulesdir}
install -m 644 config.h epan/register.h "${IDIR}/"
install -m 644 cfile.h file.h "${IDIR}/"
install -m 644 epan/*.h "${IDIR}/epan/"
install -m 644 epan/crypt/*.h "${IDIR}/epan/crypt"
install -m 644 epan/ftypes/*.h "${IDIR}/epan/ftypes"
install -m 644 epan/dfilter/*.h "${IDIR}/epan/dfilter"
install -m 644 epan/dissectors/*.h "${IDIR}/epan/dissectors"
install -m 644 wiretap/*.h "${IDIR}/wiretap"
install -m 644 wsutil/*.h "${IDIR}/wsutil"
install -m 644 %{SOURCE1} %{buildroot}%{_udevrulesdir}


touch %{buildroot}%{_bindir}/%{name}

# Remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete -print

%pre cli
getent group wireshark >/dev/null || groupadd -r wireshark
getent group usbmon >/dev/null || groupadd -r usbmon

%post cli
%{?ldconfig}
# skip triggering if udevd isn't even accessible, e.g. containers or
# rpm-ostree-based systems
if [ -S /run/udev/control ]; then
  %{_bindir}/udevadm trigger --subsystem-match=usbmon
fi

%ldconfig_postun cli

%files
%{_bindir}/wireshark
#%{_mandir}/man1/wireshark.*

%files cli
%license COPYING
%doc AUTHORS INSTALL NEWS README*
%{_bindir}/capinfos
%{_bindir}/captype
%{_bindir}/editcap
%{_bindir}/mergecap
%{_bindir}/randpkt
%{_bindir}/reordercap
%{_bindir}/sharkd
%{_bindir}/text2pcap
%{_bindir}/tshark
%attr(0750, root, wireshark) %caps(cap_net_raw,cap_net_admin=ep) %{_bindir}/dumpcap
%{_bindir}/rawshark
%{_udevrulesdir}/90-wireshark-usbmon.rules
%{_libdir}/lib*.so.*
%dir %{_libdir}/wireshark
%dir %{_libdir}/wireshark/extcap
%dir %{_libdir}/wireshark/plugins
%{_libdir}/wireshark/extcap/ciscodump
%{_libdir}/wireshark/extcap/udpdump
%{_libdir}/wireshark/extcap/wifidump
%{_libdir}/wireshark/extcap/sshdump
%{_libdir}/wireshark/extcap/sdjournal
%{_libdir}/wireshark/extcap/dpauxmon
%dir %{_libdir}/wireshark/cmake
%{_libdir}/wireshark/cmake/*.cmake
#the version wireshark uses to store plugins is only x.y, not .z
%dir %{_libdir}/wireshark/plugins/%{plugins_version}
%dir %{_libdir}/wireshark/plugins/%{plugins_version}/epan
%dir %{_libdir}/wireshark/plugins/%{plugins_version}/wiretap
%dir %{_libdir}/wireshark/plugins/%{plugins_version}/codecs
%{_libdir}/wireshark/plugins/%{plugins_version}/epan/*.so
%{_libdir}/wireshark/plugins/%{plugins_version}/wiretap/*.so
%{_libdir}/wireshark/plugins/%{plugins_version}/codecs/*.so
#%{_mandir}/man1/editcap.*
#%{_mandir}/man1/tshark.*
#%{_mandir}/man1/mergecap.*
#%{_mandir}/man1/text2pcap.*
#%{_mandir}/man1/capinfos.*
#%{_mandir}/man1/dumpcap.*
#%{_mandir}/man4/wireshark-filter.*
#%{_mandir}/man1/rawshark.*
#%{_mandir}/man1/dftest.*
#%{_mandir}/man1/randpkt.*
#%{_mandir}/man1/reordercap.*
#%{_mandir}/man1/sshdump.*
#%{_mandir}/man1/udpdump.*
#%{_mandir}/man1/androiddump.*
#%{_mandir}/man1/captype.*
#%{_mandir}/man1/ciscodump.*
#%{_mandir}/man1/randpktdump.*
#%{_mandir}/man1/dpauxmon.*
#%{_mandir}/man1/sdjournal.*
#%{_mandir}/man4/extcap.*
%dir %{_datadir}/wireshark
%{_datadir}/wireshark/*
#%{_docdir}/wireshark/*.html

%files devel
%doc doc/README.* ChangeLog
%{_includedir}/wireshark
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Sep 07 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 4.0.8-1
- Upgrade version to address 27 CVEs
- Address CVE-2021-22207, CVE-2021-22222, CVE-2021-22235, CVE-2021-39920, CVE-2021-39921,
  CVE-2021-39922, CVE-2021-39923, CVE-2021-39924, CVE-2021-39925, CVE-2021-39926,
  CVE-2021-39928, CVE-2021-39929, CVE-2021-4181, CVE-2021-4182, CVE-2021-4184,
  CVE-2021-4185, CVE-2021-4186, CVE-2021-4190, CVE-2022-0581, CVE-2022-0582,
  CVE-2022-0583, CVE-2022-0585, CVE-2022-0586, CVE-2022-3190, CVE-2022-4344,
  CVE-2023-0667, CVE-2023-2906
- Swith to SPDX identifiers
- Fix source URL
- Lint spec

* Thu Oct 13 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.4.16-1
- Upgrade to 3.4.16

* Fri Jun 10 2022 Jon Slobodzian <joslobo@microsoft.com> - 3.4.14-1
- Update to resolves CVEs
- Disabled Android Dump.
- Removed unused/disabled features.
- Fixed Formatting.

* Wed Feb 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.4.4-5
- License verified.

* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.4.4-4
- Adding missing BRs on Perl modules.

* Thu Oct 28 2021 Muhammad Falak <mwani@microsft.com> - 3.4.4-3
- Remove epoch

* Mon Aug 23 2021 Muhammad Falak <mwani@microsoft.com> - 1:3.4.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Introduce macro `with_gui` to toggle building with/without gui support.

* Tue Mar 16 2021 Michal Ruprich <mruprich@redhat.com> - 1:3.4.4-1
- New version 3.4.4
- Fix for CVE-2021-22191

* Tue Feb 16 2021 Michal Ruprich <mruprich@redhat.com> - 1:3.4.3-1
- New version 3.4.3
- Fix for CVE-2021-22173, CVE-2021-22174

* Fri Jan 29 2021 Michal Ruprich <mruprich@redhat.com> - 1:3.4.2-1
- New version 3.4.2
- Fix for CVE-2020-26418, CVE-2020-26419, CVE-2020-26420, CVE-2020-26421

* Thu Dec 03 2020 Michal Ruprich <mruprich@redhat.com> - 1:3.4.0-1
- New version 3.4.0
- Fix for CVE-2020-26575, CVE-2020-28030

* Fri Oct 09 2020 Michal Ruprich <mruprich@redhat.com> - 1:3.2.7-1
- New version 3.2.7
- Fix for CVE-2020-25862, CVE-2020-25863, CVE-2020-25866

* Wed Aug 19 2020 Michal Ruprich <mruprich@redhat.com> - 1:3.2.6-1
- New version 3.2.6
- Fix for CVE-2020-17498

* Thu Jul 30 2020 Michal Ruprich <mruprich@redhat.com> - 1:3.2.5-2
- Adding ownership for dirs created by wireshark (rhbz#1860650)

* Thu Jul 02 2020 Michal Ruprich <mruprich@redhat.com> - 1:3.2.5-1
- New version 3.2.5

* Fri May 22 2020 Michal Ruprich <mruprich@redhat.com> - 1:3.2.4-1
- New version 3.2.4
- Enabling build with androiddump (rhbz#1834367)

* Mon Apr 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:3.2.3-1
- 3.2.3

* Fri Apr 03 2020 Michal Ruprich <mruprich@redhat.com> - 1:3.2.2-1
- New version 3.2.2

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 19 2019 Michal Ruprich <mruprich@redhat.com> - 1:3.2.0-1
- New version 3.2.0

* Wed Oct 30 2019 Michal Ruprich <mruprich@redhat.com> - 1:3.0.5-1
- New version 3.0.5

* Tue Aug 20 2019 Michal Ruprich <mruprich@redhat.com> - 1:3.0.3-1
- New version 3.0.3
- Fixes CVE-2019-13619

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 09 2019 Michal Ruprich <mruprich@redhat.com> - 1:3.0.1-1
- New version 3.0.1
- Fixes CVE-2019-10894, CVE-2019-10895, CVE-2019-10896, CVE-2019-10897, CVE-2019-10898, CVE-2019-10899, CVE-2019-10900, CVE-2019-10901, CVE-2019-10902, CVE-2019-10903

* Mon Mar 11 2019 Michal Ruprich <mruprich@redhat.com> - 1:3.0.0-1
- New version 3.0.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Michal Ruprich <mruprich@redhat.com> - 1:2.6.6-1
- New version 2.6.6 
- Contains fixes for CVE-2019-5716, CVE-2019-5717, CVE-2019-5718, CVE-2019-5719
- Add explicit curdir on CMake invokation

* Wed Jan 02 2019 Michal Ruprich <mruprich@redhat.com> - 1:2.6.5-2
- Adding libnghttp2-devel as BuildRequires - needed for HTTP2 support(rhbz#1512722)

* Mon Dec 10 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.6.5-1
- New version 2.6.5
- Contains fixes for CVE-2018-19622, CVE-2018-19623,  CVE-2018-19624, CVE-2018-19625, CVE-2018-19626, CVE-2018-19627, CVE-2018-19628

* Mon Nov 12 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.6.4-1
- New version 2.6.4
- Contains fixes for CVE-2018-16056, CVE-2018-16057, CVE-2018-16058

* Mon Jul 23 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.6.2-1
- New version 2.6.2
- Contains fixes for CVE-2018-14339, CVE-2018-14340, CVE-2018-14341, CVE-2018-14342, CVE-2018-14343, CVE-2018-14344, CVE-2018-14367, CVE-2018-14368, CVE-2018-14369, CVE-2018-14370

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.6.1-2
- Fixing build error with newer qt5 version

* Thu May 24 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.6.1-1
- New version 2.6.1

* Tue May 15 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.6.0-2
- Added Obsoletes for wireshark-qt and wireshark-gtk

* Wed May 02 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.6.0-1
- New version 2.6.0
- Fix for CVE-2018-9256, CVE-2018-9257, CVE-2018-9258, CVE-2018-9259, CVE-2018-9260, CVE-2018-9261, CVE-2018-9262, CVE-2018-9263, CVE-2018-9264, CVE-2018-9265, CVE-2018-9266, CVE-2018-9267, CVE-2018-9268, CVE-2018-9269, CVE-2018-9270, CVE-2018-9271, CVE-2018-9272, CVE-2018-9273, CVE-2018-9274
- Switch from autotools to cmake
- Removed python2-devel(#1560284) and libssh2-devel from dependencies
- Removed python scripts

* Thu Mar 15 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.4.5-2
- Removing dependency on wireshark from wireshark-cli (rhbz#1554818)
- Removing deprecated Group tags

* Fri Mar 09 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.4.5-1
- New upstream version 2.4.5
- Contains fixes for CVE-2018-7419, CVE-2018-7418, CVE-2018-7417, CVE-2018-7420, CVE-2018-7320, CVE-2018-7336, CVE-2018-7337, CVE-2018-7334, CVE-2018-7335, CVE-2018-6836, CVE-2018-5335,  CVE-2018-5334,  CVE-2017-6014, CVE-2017-9616, CVE-2017-9617, CVE-2017-9766
- Removed GTK+ based GUI (rhbz#1486203)
- Corrected LDFLAGS in spec (rhbz#1548665)
- Alternatives are no longer needed (rhbz#1533701)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:2.4.4-2
- Escape macros in %%changelog

* Fri Jan 19 2018 Michal Ruprich <mruprich@redhat.com> - 1:2.4.4-1
- New upstream version 2.4.4
- Contains fix for CVE-2017-17935 

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:2.4.3-2
- Remove obsolete scriptlets

* Wed Dec 20 2017 Michal Ruprich <mruprich@redhat.com> - 1:2.4.3-1
- New upstream version 2.4.3
- Contains fixe for CVE-2017-17085, CVE-2017-17084, CVE-2017-17083

* Thu Oct 12 2017 Michal Ruprich <mruprich@redhat.com> - 1:2.4.2-1
- New upstream version 2.4.2
- Contains fixes for CVE-2017-15189, CVE-2017-15190, CVE-2017-15191, CVE-2017-15192, CVE-2017-15193, CVE-2017-13764, CVE-2017-13765, CVE-2017-13766, CVE-2017-13767

* Tue Aug 08 2017 Martin Sehnoutka <msehnout@redhat.com> - 1:2.4.0-6
- Use epoch in Requires (rhbz#1478501)

* Thu Aug 03 2017 Martin Sehnoutka <msehnout@redhat.com> - 1:2.4.0-5
- Add libssh as a build dependency (rhbz#1419131)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.4.0-2
- Move init.lua file into the main subpackage (rhbz#1463270)

* Thu Jul 20 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.4.0-2
- New upstream version 2.4.0

* Thu Jun 29 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.4.0rc2-1
- New upstream version

* Mon Jun 12 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.2.7-1
- New upstream release 2.2.7

* Thu May 25 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.2.6-5
- Add triggerin script to remove old alternatives
- Remove appdata.xml as it is provided by upstream now

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon Apr 24 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.2.6-2
- Build with lua support (resolves: #1259623)

* Fri Apr 21 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.2.6-1
- New upstream release 2.2.6

* Fri Apr 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.2.5-2
- Stop patching pkg-config

* Tue Mar 07 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.2.5-1
- New upstream version 2.2.5

* Mon Mar 06 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.2.4-3
- Fix python_sitearch macro
- Fix path in desktop file

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Martin Sehnoutka <msehnout@redhat.com> - 2.2.4-2
- New upstream release 2.2.4

* Thu Dec 08 2016 Martin Sehnoutka <msehnout@redhat.com> - 2.2.2-4
- Change update-alternatives name from wireshark to wireshark-gui; Resolve:
  #1400654

* Thu Dec 01 2016 Martin Sehnoutka <msehnout@redhat.com> - 2.2.2-3
- Move all executables into /usr/bin/ directory

* Fri Nov 18 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.2.2-2
- Build QT GUI with qt5 (rhbz #1347752)

* Fri Nov 18 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.2.2-1
- Version 2.2.2
- See https://www.wireshark.org/docs/relnotes/wireshark-2.2.2.html
- Use %%license, spec cleanups
- Put udev rules in right location (rhbz #1365581)

* Wed Nov  2 2016 Peter Lemenkov <lemenkov@gmail.com> - 2.1.1-3
- No longer uses adns ( https://github.com/wireshark/wireshark/commit/7a1d3f6 )
- Remove --with-ipv6 switch ( https://github.com/wireshark/wireshark/commit/fad1565 )
- Change GTK option switch ( https://github.com/wireshark/wireshark/commit/d77029d )

* Tue Sep 13 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.1-2
- Add Requires(post) for systemd-udev to avoid rpm scriptlet failures

* Sun Jul 24 2016 Peter Hatina <phatina@gmail.com> - 2.1.1-1
- Ver. 2.1.1
- See https://www.wireshark.org/docs/relnotes/wireshark-2.1.1.html

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 13 2016 Peter Hatina <phatina@gmail.com> - 2.1.0-3
- Fix typo, install ws_diag_control
- Related: rhbz#1347869

* Mon Jun 20 2016 Peter Hatina <phatina@gmail.com> - 2.1.0-2
- Install ws_diag_control.h into standard include directory
- Resolves: rhbz#1347869

* Tue Jun 14 2016 Peter Hatina <phatina@gmail.com> - 2.1.0-1
- Ver. 2.1.0
- See https://www.wireshark.org/docs/relnotes/wireshark-2.1.0.html

* Thu Apr 28 2016 Peter Hatina <phatina@redhat.com> - 2.0.3-1
- Ver. 2.0.3

* Tue Mar 01 2016 Peter Hatina <phatina@redhat.com> - 2.0.2-1
- Ver. 2.0.2

* Tue Feb 23 2016 Peter Hatina <phatina@redhat.com> - 2.0.1-3
- Fix missing Requires in wireshark.pc

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Peter Hatina <phatina@redhat.com> - 2.0.1-1
- Ver. 2.0.1
- Introduced wireshark metapackage for wireshark-cli and wireshark-gtk
- wireshark-qt and wireshark-gtk contain the GUI applications
- See https://www.wireshark.org/docs/relnotes/wireshark-2.0.1.html

* Fri Jan  8 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.12.9-1
- Ver. 1.12.9
- See https://www.wireshark.org/docs/relnotes/wireshark-1.12.9.html

* Tue Nov  3 2015 Peter Lemenkov <lemenkov@gmail.com> - 1.12.8-2
- Fixed Wireshark detection in external projects using wireshark.m4 script.
  See https://bugzilla.redhat.com/1274831 for further details.

* Thu Oct 15 2015 Peter Hatina <phatina@redhat.com> - 1.12.8-1
- Ver. 1.12.8
- Dropped patch no. 10 (applied upstream)

* Fri Aug 21 2015 Peter Lemenkov <lemenkov@gmail.com> - 1.12.7-2
- Enable libnl3 (see rhbz#1207386, rhbz#1247566)
- Remove airpcap switch (doesn't have any effect on Linux)
- Backport patch no. 11
- Fixed building with F24+

* Tue Aug 18 2015 Peter Lemenkov <lemenkov@gmail.com> - 1.12.7-1
- Ver. 1.12.7
- Dropped patch no. 11 (applied upstream)

* Tue Jun 30 2015 Peter Hatina <phatina@redhat.com> - 1.12.6-4
- Move plugins to %%{_libdir}/wireshark/plugins to avoid
  transaction conflicts

* Fri Jun 26 2015 Peter Hatina <phatina@redhat.com> - 1.12.6-3
- Disable overlay scrolling in main window
- Resolves: rhbz#1235830

* Fri Jun 26 2015 Peter Hatina <phatina@redhat.com> - 1.12.6-2
- Add symlink plugins/current -> plugins/%%{version}

* Thu Jun 18 2015 Peter Hatina <phatina@redhat.com> - 1.12.6-1
- Ver. 1.12.6

* Wed May 13 2015 Peter Hatina <phatina@redhat.com> - 1.12.5-1
- Ver. 1.12.5

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1.12.4-2
- Add an AppData file for the software center

* Thu Mar  5 2015 Peter Hatina <phatina@redhat.com> - 1.12.4-1
- Ver. 1.12.4

* Mon Feb  2 2015 Peter Hatina <phatina@redhat.com> - 1.12.3-3
- temporary: disable lua

* Mon Feb  2 2015 Peter Hatina <phatina@redhat.com> - 1.12.3-2
- rebuild with gtk3
- fix gdk crash

* Thu Jan  8 2015 Peter Hatina <phatina@redhat.com> - 1.12.3-1
- Ver. 1.12.3

* Mon Dec 22 2014 Peter Hatina <phatina@redhat.com> - 1.12.2-2
- fix CLI parsing by getopt_long

* Mon Nov 17 2014 Peter Hatina <phatina@redhat.com> - 1.12.2-1
- Ver. 1.12.2

* Mon Sep 22 2014 Peter Hatina <phatina@redhat.com> - 1.12.1-1
- Ver. 1.12.1

* Tue Sep 09 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.12.0-5
- Install epan/wmem/*.h files. See rhbz #1129419

* Wed Sep  3 2014 Peter Hatina <phatina@redhat.com> - 1.12.0-4
- fix fields print format

* Mon Aug 18 2014 Rex Dieter <rdieter@fedoraproject.org> 1.12.0-3
- update mime scriptlets

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.12.0-1
- Ver. 1.12.0
- Dropped a lot of outdated patches.
- Added /usr/sbin/captype application.
- Added temporary workaround for wireshark.pc.in missing in the official
  tarball.
- Removed outdated --with-dumpcap-group="wireshark" cli switch. It doesn't work
  during rpmbuild, and we still set group explicitly in the 'files' section.
- Removed --enable-setcap-install. Likewise.
- Some ANSI C header files were moved to epan/

* Fri Aug  1 2014 Peter Hatina <phatina@redhat.com> - 1.10.9-1
- Ver. 1.10.9

* Fri Jun 13 2014 Peter Hatina <phatina@redhat.com> - 1.10.8-1
- Ver. 1.10.8

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Peter Hatina <phatina@redhat.com> - 1.0.7-2
- add AMQP 1.0 support

* Wed Apr 23 2014 Peter Hatina <phatina@redhat.com> - 1.10.7-1
- Ver. 1.10.7

* Fri Mar 21 2014 Peter Hatina <phatina@redhat.com> - 1.10.6-2
- Reload udev rule for usbmon subsystem only

* Sat Mar 08 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.10.6-1
- Ver. 1.10.6

* Fri Mar  7 2014 Peter Hatina <phatina@redhat.com> - 1.10.5-4
- Fix Capture Dialog layout on low resolution displays
- Resolves: #1071313

* Sun Feb  9 2014 Ville Skyttä <ville.skytta@iki.fi>
- Fix --with-gtk* build option usage.

* Wed Jan 29 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.10.5-3
- Fixed paths in the desktop-file (see rhbz #1059188)

* Mon Jan 13 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.10.5-2
- Updated RTPproxy dissector (again)
- Fix rare issue with the Sniffer traces (patch no. 23)

* Mon Dec 23 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.5-1
- Ver. 1.10.5
- Don't apply upstreamed patches no. 18, 19, 20.

* Thu Dec 19 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.4-2
- Fix endianness in the Bitcoin protocol dissector (patch no. 19)
- Last-minute fix for wrongly backported change (patch no. 20)
- Fix FTBFS in Rawhide (see patch no. 21 - recent Glib doesn't provide g_memmove macro anymore)

* Wed Dec 18 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.4-1
- Ver. 1.10.4
- Don't apply upsteamed patches no. 13, 14, 15, 16, 17
- Fix variable overflow (patch no. 18)
- Updated RTPproxy dissector (backported three more patches from trunk)

* Tue Dec 10 2013 Peter Hatina <phatina@redhat.com> - 1.10-3-9
- remove python support

* Tue Dec 10 2013 Peter Hatina <phatina@redhat.com> - 1.10-3-8
- fix read permissions of /dev/usbmon* for non-root users

* Mon Dec 09 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-7
- Fix error in the backported RTPproxy patches

* Fri Dec 06 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-6
- Updated RTPproxy dissector (again), squashed patch no. 15 (applied upstream).
- Use proper soname in the python scripts
- Don't apply no longer needed fix for pod2man.
- Fix for main window. See patch no. 15
- Fix for SCTP dissection. See patch no. 16
- Fix for rare issue in Base Station Subsystem GPRS Protocol dissection. See
  patch no. 17
- Fix building w/o Lua

* Wed Nov 27 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-5
- Updated RTPproxy dissector (again)
- Allow packets more than 64k (for USB capture). See patch no. 13
- Don't die during loading of some SIP capture files. See patch no. 14
- Backport support for RTPproxy dissector timeouts detection. See patch no. 15

* Wed Nov 13 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-4
- Updated RTPproxy dissector

* Thu Nov 07 2013 Peter Hatina <phatina@redhat.com> - 1.10.3-3
- fix subpackage requires

* Wed Nov 06 2013 Peter Hatina <phatina@redhat.com> - 1.10.3-2
- harden dumpcap capabilities

* Sat Nov 02 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-1
- Ver. 1.10.3
- Dropped upsteamed patch no. 13

* Tue Oct 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-8
- Added support for rtpproxy conversations (req/resp matching)

* Tue Sep 24 2013 Peter Hatina <phatina@redhat.com> - 1.10.2-7
- fix build error caused by symbols clash

* Tue Sep 17 2013 Peter Hatina <phatina@redhat.com> - 1.10.2-6
- move default temporary directory to /var/tmp

* Fri Sep 13 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-5
- Convert automake/pkgconfig files into patches (better upstream integration)
- Restored category in the *.desktop file
- Install another one necessary header file - frame_data_sequence.h

* Thu Sep 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-4
- Enhance desktop integration (*.desktop and MIME-related files)

* Thu Sep 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-3
- Fix building on Fedora 18 (no perl-podlators)

* Thu Sep 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-2
- Add an OpenFlow dissector

* Wed Sep 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10-2-1
- Ver. 1.10.2
- Actually remove the console helper

* Mon Sep 09 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.1-1
- Ver. 1.10.1
- Backported rtpproxy dissector module

* Wed Sep 04 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-11
- fix missing ws_symbol_export.h

* Wed Sep 04 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-10
- fix tap iostat overflow

* Wed Sep 04 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-9
- fix sctp bytes graph crash

* Wed Sep 04 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-8
- fix string overrun in plugins/profinet

* Tue Sep 03 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-7
- fix BuildRequires - libgcrypt-devel

* Tue Sep 03 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-6
- fix build parameter -fstack-protector-all

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Peter Hatina <phatina@redhat.com> 1.10.0-4
- fix pod2man build error

* Mon Jun 24 2013 Peter Hatina <phatina@redhat.com> 1.10.0-3
- fix bogus date

* Mon Jun 17 2013 Peter Hatina <phatina@redhat.com> 1.10.0-2
- fix flow graph crash

* Mon Jun 17 2013 Peter Hatina <phatina@redhat.com> 1.10.0-1
- upgrade to 1.10.0
- see https://www.wireshark.org/docs/relnotes/wireshark-1.10.0.html

* Mon Apr 08 2013 Peter Hatina <phatina@redhat.com> 1.8.6-5
- fix documentation build error

* Wed Mar 27 2013 Peter Hatina <phatina@redhat.com> 1.8.6-4
- fix capture crash (#894753)

* Tue Mar 19 2013 Peter Hatina <phatina@redhat.com> 1.8.6-3
- fix dns resolving crash (#908211)

* Mon Mar 18 2013 Peter Hatina <phatina@redhat.com> 1.8.6-2
- return to gtk2, stable branch 1.8 is not gtk3 ready

* Tue Mar 12 2013 Peter Hatina <phatina@redhat.com> 1.8.6-1
- upgrade to 1.8.6
- see https://www.wireshark.org/docs/relnotes/wireshark-1.8.6.html

* Sun Feb 10 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.8.5-3
- Remove vendor tag from desktop file as per https://fedorahosted.org/fesco/ticket/1077

* Tue Feb 05 2013 Peter Hatina <phatina@redhat.com> - 1.8.5-2
- fix gtk3 layout issues
- NOTE: there may be some windows with broken layouts left

* Thu Jan 31 2013 Peter Hatina <phatina@redhat.com> - 1.8.5-1
- upgrade to 1.8.5
- see https://www.wireshark.org/docs/relnotes/wireshark-1.8.5.html

* Mon Dec 03 2012 Peter Hatina <phatina@redhat.com> - 1.8.4-1
- upgrade to 1.8.4
- see https://www.wireshark.org/docs/relnotes/wireshark-1.8.4.html

* Tue Oct 16 2012 Peter Hatina <phatina@redhat.com> - 1.8.3-2
- backport dissector table fix
- TODO: remove this after new release

* Thu Oct 11 2012 Peter Hatina <phatina@redhat.com> - 1.8.3-1
- upgrade to 1.8.3
- see https://www.wireshark.org/docs/relnotes/wireshark-1.8.3.html

* Tue Sep  4 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.2-3
- added back compatibility with RHEL6
- GeoIP build dependency made also conditional on with_GeoIP variable

* Wed Aug 29 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.2-2
- fixed "libwireshark.so.1: cannot open shared object file" error
  message on startup

* Thu Aug 16 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.2-1
- upgrade to 1.8.2
- see https://www.wireshark.org/docs/relnotes/wireshark-1.8.2.html

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 24 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.1-1
- upgrade to 1.8.1
- see https://www.wireshark.org/docs/relnotes/wireshark-1.8.1.html

* Mon Jun 25 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.0
- upgrade to 1.8.0
- see https://www.wireshark.org/docs/relnotes/wireshark-1.8.0.html

* Wed May 23 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.8-1
- upgrade to 1.6.8
- see https://www.wireshark.org/docs/relnotes/wireshark-1.6.8.html

* Mon May 21 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.7-2
- Removed dependency on GeoIP on RHEL.

* Tue Apr 10 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.7-1
- upgrade to 1.6.7
- see https://www.wireshark.org/docs/relnotes/wireshark-1.6.7.html

* Wed Mar 28 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.6-1
- upgrade to 1.6.6
- see https://www.wireshark.org/docs/relnotes/wireshark-1.6.6.html

* Fri Mar  9 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.5-2
- fixed wireshark crashing when using combo box in import dialog (#773290)
- added AES support into netlogon dissector

* Wed Jan 11 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.5-1
- upgrade to 1.6.5
- see https://www.wireshark.org/docs/relnotes/wireshark-1.6.5.html

* Fri Dec  2 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.4-1
- upgrade to 1.6.4
- see https://www.wireshark.org/docs/relnotes/wireshark-1.6.4.html
- build with c-ares and libpcap (#759305)
- fixed display of error message boxes on startup in gnome3 (#752559)

* Mon Nov 14 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.3-2
- added dependency on shadow-utils (#753293)
- removed usermode support

* Wed Nov  2 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.3-1
- upgrade to 1.6.3
- see https://www.wireshark.org/docs/relnotes/wireshark-1.6.3.html

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for glibc bug#747377

* Fri Oct 21 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.2-4
- updated autoconf macros and pkgconfig file in wireshark-devel to reflect
  current config.h (#746655)

* Mon Oct 17 2011 Steve Dickson <steved@redhat.com> - 1.6.2-3
- Fixed a regression introduce by upstream patch r38306
    which caused v4.1 traffic not to be displayed.
- Added v4 error status to packet detail window.

* Tue Sep 13 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.2-2
- fixed spelling of the security message (#737270)

* Fri Sep  9 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.2-1
- upgrade to 1.6.2
- see https://www.wireshark.org/docs/relnotes/wireshark-1.6.2.html

* Thu Jul 21 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.1-1
- upgrade to 1.6.1
- see https://www.wireshark.org/docs/relnotes/wireshark-1.6.1.html

* Thu Jun 16 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.0-4
- fixed previous incomplete fix

* Thu Jun 16 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.0-3
- fixed Fedora-specific message when user is not part of 'wireshark' group
  - now it does not contain '<' and '>' characters (#713545)

* Thu Jun  9 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.0-2
- added wspy_dissectors directory to the package
  - other packages can add Python plugins there
  - as side effect, removed following message:
    [Errno 2] No such file or directory: '/usr/lib64/wireshark/python/1.6.0/wspy_dissectors'
- enabled zlib support

* Wed Jun  8 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.0-1
- upgrade to 1.6.0
- see https://www.wireshark.org/docs/relnotes/wireshark-1.6.0.html

* Thu Jun  2 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.7-1
- upgrade to 1.4.7
- see https://www.wireshark.org/docs/relnotes/wireshark-1.4.7.html

* Thu May 19 2011 Steve Dickson <steved@redhat.com> - 1.4.6-3
- Improved the NFS4.1 patcket dissectors 

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 1.4.6-2
- Update icon cache scriptlet

* Tue Apr 19 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.6-1
- upgrade to 1.4.6
- see https://www.wireshark.org/docs/relnotes/wireshark-1.4.6.html

* Mon Apr 18 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.5-1
- upgrade to 1.4.5
- see https://www.wireshark.org/docs/relnotes/wireshark-1.4.5.html

* Sun Apr 03 2011 Cosimo Cecchi <cosimoc@redhat.com> - 1.4.4-2
- Use hi-res icons

* Thu Mar  3 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.4-1
- upgrade to 1.4.4
- see https://www.wireshark.org/docs/relnotes/wireshark-1.4.4.html

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.3-2
- create the 'wireshark' group as system, not user
- add few additional header files to -devel subpackage (#671997)

* Thu Jan 13 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.3-1
- upgrade to 1.4.3
- see https://www.wireshark.org/docs/relnotes/wireshark-1.4.3.html

* Wed Jan  5 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.2-5
- fixed buffer overflow in ENTTEC dissector (#666897)

* Wed Dec 15 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.2-4
- added epan/dissectors/*.h to -devel subpackage (#662969)

* Mon Dec  6 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.2-3
- fixed generation of man pages again (#635878)

* Fri Nov 26 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.2-2
- rework the Wireshark security (#657490). Remove the console helper and
  allow only members of new 'wireshark' group to capture the packets.

* Mon Nov 22 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.2-1
- upgrade to 1.4.2
- see https://www.wireshark.org/docs/relnotes/wireshark-1.4.2.html

* Mon Nov  1 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.1-2
- temporarily disable zlib until
  https://bugs.wireshark.org/bugzilla/show_bug.cgi?id=4955 is resolved (#643461)

* Fri Oct 22 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.1-1
- upgrade to 1.4.1
- see https://www.wireshark.org/docs/relnotes/wireshark-1.4.1.html
- Own the %%{_libdir}/wireshark dir (#644508)
- associate *.pcap files with wireshark (#641163)

* Wed Sep 29 2010 jkeating - 1.4.0-2
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.0-2
- fixed generation of man pages (#635878)

* Tue Aug 31 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.0-1
- upgrade to 1.4.0
- see https://www.wireshark.org/docs/relnotes/wireshark-1.4.0.html

* Fri Jul 30 2010 Jan Safranek <jsafrane@redhat.com> - 1.2.10-1
- upgrade to 1.2.10
- see https://www.wireshark.org/docs/relnotes/wireshark-1.2.10.html

* Fri Jul 30 2010 Jan Safranek <jsafrane@redhat.com> - 1.2.9-4
- Rebuilt again for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 22 2010 Jan Safranek <jsafrane@redhat.com> - 1.2.9-3
- removing useless LDFLAGS (#603224)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 11 2010 Radek Vokal <rvokal@redhat.com> - 1.2.9-1
- upgrade to 1.2.9
- see https://www.wireshark.org/docs/relnotes/wireshark-1.2.9.html

* Mon May 17 2010 Radek Vokal <rvokal@redhat.com> - 1.2.8-4
- removing traling bracket from python_sitearch (#592391)

* Fri May  7 2010 Radek Vokal <rvokal@redhat.com> - 1.2.8-3
- fix patched applied without fuzz=0

* Thu May  6 2010 Radek Vokal <rvokal@redhat.com> - 1.2.8-2
- use sitearch instead of sitelib to avoid pyo and pyc conflicts

* Thu May  6 2010 Radek Vokal <rvokal@redhat.com> - 1.2.8-1
- upgrade to 1.2.8
- see https://www.wireshark.org/docs/relnotes/wireshark-1.2.8.html

* Tue Apr  6 2010 Radek Vokal <rvokal@redhat.com> - 1.2.7-2
- rebuild with GeoIP support (needs to be turned on in IP protocol preferences)

* Fri Apr  2 2010 Radek Vokal <rvokal@redhat.com> - 1.2.7-1
- upgrade to 1.2.7
- see https://www.wireshark.org/docs/relnotes/wireshark-1.2.7.html

* Wed Mar 24 2010 Radek Vokal <rvokal@redhat.com> - 1.2.6-3
- bring back -pie

* Tue Mar 16 2010 Jeff Layton <jlayton@redhat.com> - 1.2.6-2
- add patch to allow decode of NFSv4.0 callback channel
- add patch to allow decode of more SMB FIND_FILE infolevels

* Fri Jan 29 2010 Radek Vokal <rvokal@redhat.com> - 1.2.6-1
- upgrade to 1.2.6
- see https://www.wireshark.org/docs/relnotes/wireshark-1.2.6.html

* Wed Jan 20 2010 Radek Vokal <rvokal@redhat.com> - 1.2.5-5
- minor spec file tweaks for better svn checkout support (#553500)

* Tue Jan 05 2010 Radek Vokál <rvokal@redhat.com> - 1.2.5-4
- init.lua is present always and not only when lua support is enabled

* Tue Jan 05 2010 Radek Vokál <rvokal@redhat.com> - 1.2.5-3
- fix file list, init.lua is only in -devel subpackage (#552406)

* Fri Dec 18 2009 Patrick Monnerat <pm@datasphere.ch> 1.2.5-2
- Autoconf macro for plugin development.

* Fri Dec 18 2009 Radek Vokal <rvokal@redhat.com> - 1.2.5-1
- upgrade to 1.2.5
- fixes security vulnaribilities, see https://www.wireshark.org/security/wnpa-sec-2009-09.html

* Thu Dec 17 2009 Radek Vokal <rvokal@redhat.com> - 1.2.4-3
- split -devel package (#547899, #203642, #218451)
- removing root warning dialog (#543709)

* Mon Dec 14 2009 Radek Vokal <rvokal@redhat.com> - 1.2.4-2
- enable lua support - https://wiki.wireshark.org/Lua
- attempt to fix filter crash on 64bits

* Wed Nov 18 2009 Radek Vokal <rvokal@redhat.com> - 1.2.4-1
- upgrade to 1.2.4
- https://www.wireshark.org/docs/relnotes/wireshark-1.2.4.html

* Fri Oct 30 2009 Radek Vokal <rvokal@redhat.com> - 1.2.3-1
- upgrade to 1.2.3
- https://www.wireshark.org/docs/relnotes/wireshark-1.2.3.html

* Mon Sep 21 2009 Radek Vokal <rvokal@redhat.com> - 1.2.2-1
- upgrade to 1.2.2
- https://www.wireshark.org/docs/relnotes/wireshark-1.2.2.html

* Mon Sep 14 2009 Bill Nottingham <notting@redhat.com> - 1.2.1-5
- do not use portaudio in RHEL

* Fri Aug 28 2009 Radek Vokal <rvokal@redhat.com> - 1.2.1-4
- yet anohter rebuilt

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-3
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Radek Vokal <rvokal@redhat.com> - 1.2.1
- upgrade to 1.2.1
- https://www.wireshark.org/docs/relnotes/wireshark-1.2.1.html

* Tue Jun 16 2009 Radek Vokal <rvokal@redhat.com> - 1.2.0
- upgrade to 1.2.0
- https://www.wireshark.org/docs/relnotes/wireshark-1.2.0.html

* Fri May 22 2009 Radek Vokal <rvokal@redhat.com> - 1.1.4-0.pre1
- update to latest development build

* Thu Mar 26 2009 Radek Vokal <rvokal@redhat.com> - 1.1.3-1
- upgrade to 1.1.3

* Thu Mar 26 2009 Radek Vokal <rvokal@redhat.com> - 1.1.2-4.pre1
- fix libsmi support

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Radek Vokal <rvokal@redhat.com> - 1.1.2-2.pre1
- add netdump support

* Sun Feb 15 2009 Steve Dickson <steved@redhat.com> - 1.1.2-1.pre1
- NFSv4.1: Add support for backchannel decoding

* Mon Jan 19 2009 Radek Vokal <rvokal@redhat.com> - 1.1.2-0.pre1
- upgrade to latest development release
- added support for portaudio (#480195)

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.1.1-0.pre1.2
- rebuild with new openssl

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1.1-0.pre1.1
- Rebuild for Python 2.6

* Thu Nov 13 2008 Radek Vokál <rvokal@redhat.com> 1.1.1-0.pre1
- upgrade to 1.1.1 development branch

* Wed Sep 10 2008 Radek Vokál <rvokal@redhat.com> 1.0.3-1
- upgrade to 1.0.3
- Security-related bugs in the NCP dissector, zlib compression code, and Tektronix .rf5 file parser have been fixed.
- WPA group key decryption is now supported.
- A bug that could cause packets to be wrongly dissected as "Redback Lawful Intercept" has been fixed.

* Mon Aug 25 2008 Radek Vokál <rvokal@redhat.com> 1.0.2-3
- fix requires for wireshark-gnome

* Thu Jul 17 2008 Steve Dickson <steved@redhat.com> 1.0.2-2
- Added patches to support NFSv4.1

* Fri Jul 11 2008 Radek Vokál <rvokal@redhat.com> 1.0.2-1
- upgrade to 1.0.2

* Tue Jul  8 2008 Radek Vokál <rvokal@redhat.com> 1.0.1-1
- upgrade to 1.0.1

* Sun Jun 29 2008 Dennis Gilmore <dennis@ausil.us> 1.0.0-3
- add sparc arches to -fPIE
- rebuild for new gnutls

* Tue Apr  1 2008 Radek Vokál <rvokal@redhat.com> 1.0.0-2
- fix BuildRequires - python, yacc, bison

* Tue Apr  1 2008 Radek Vokál <rvokal@redhat.com> 1.0.0-1
- April Fools' day upgrade to 1.0.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.99.7-3
- Autorebuild for GCC 4.3

* Wed Dec 19 2007 Radek Vokál <rvokal@redhat.com> 0.99.7-2
- fix crash in unprivileged mode (#317681)

* Tue Dec 18 2007 Radek Vokál <rvokal@redhat.com> 0.99.7-1
- upgrade to 0.99.7

* Fri Dec  7 2007 Radek Vokál <rvokal@redhat.com> 0.99.7-0.pre2.1
- rebuilt for openssl

* Mon Nov 26 2007 Radek Vokal <rvokal@redhat.com> 0.99.7-0.pre2
- switch to libsmi from net-snmp
- disable ADNS due to its lack of Ipv6 support
- 0.99.7 prerelease 2

* Tue Nov 20 2007 Radek Vokal <rvokal@redhat.com> 0.99.7-0.pre1
- upgrade to 0.99.7 pre-release

* Wed Sep 19 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-3
- fixed URL

* Thu Aug 23 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-2
- rebuilt

* Mon Jul  9 2007 Radek Vokal <rvokal@redhat.com> 0.99.6-1
- upgrade to 0.99.6 final

* Fri Jun 15 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-0.pre2
- another pre-release
- turn on ADNS support

* Wed May 23 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-0.pre1
- update to pre1 of 0.99.6 release

* Mon Feb  5 2007 Radek Vokál <rvokal@redhat.com> 0.99.5-1
- multiple security issues fixed (#227140)
- CVE-2007-0459 - The TCP dissector could hang or crash while reassembling HTTP packets
- CVE-2007-0459 - The HTTP dissector could crash.
- CVE-2007-0457 - On some systems, the IEEE 802.11 dissector could crash.
- CVE-2007-0456 - On some systems, the LLT dissector could crash.

* Mon Jan 15 2007 Radek Vokal <rvokal@redhat.com> 0.99.5-0.pre2
- another 0.99.5 prerelease, fix build bug and pie flags

* Tue Dec 12 2006 Radek Vokal <rvokal@redhat.com> 0.99.5-0.pre1
- update to 0.99.5 prerelease

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.99.4-5
- rebuild for python 2.5

* Tue Nov 28 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-4
- rebuilt for new libpcap and net-snmp

* Thu Nov 23 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-3
- add htmlview to Buildrequires to be picked up by configure scripts (#216918)

* Tue Nov  7 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-2.fc7
- Requires: net-snmp for the list of MIB modules

* Wed Nov  1 2006 Radek Vokál <rvokal@redhat.com> 0.99.4-1
- upgrade to 0.99.4 final

* Tue Oct 31 2006 Radek Vokál <rvokal@redhat.com> 0.99.4-0.pre2
- upgrade to 0.99.4pre2

* Tue Oct 10 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-0.pre1
- upgrade to 0.99.4-0.pre1

* Fri Aug 25 2006 Radek Vokál <rvokal@redhat.com> 0.99.3-1
- upgrade to 0.99.3
- Wireshark 0.99.3 fixes the following vulnerabilities:
- the SCSI dissector could crash. Versions affected: CVE-2006-4330
- the IPsec ESP preference parser was susceptible to off-by-one errors. CVE-2006-4331
- a malformed packet could make the Q.2931 dissector use up available memory. CVE-2006-4333

* Tue Jul 18 2006 Radek Vokál <rvokal@redhat.com> 0.99.2-1
- upgrade to 0.99.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.99.2-0.pre1.1
- rebuild

* Tue Jul 11 2006 Radek Vokál <rvokal@redhat.com> 0.99.2-0.pre1
- upgrade to 0.99.2pre1, fixes (#198242)

* Tue Jun 13 2006 Radek Vokal <rvokal@redhat.com> 0.99.1-0.pre1
- spec file changes

* Fri Jun  9 2006 Radek Vokal <rvokal@redhat.com> 0.99.1pre1-1
- initial build for Fedora Core
