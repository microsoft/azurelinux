# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build

%bcond_without gui

Summary:       Hardware lister
Name:          lshw
Version:       B.02.20
Release: 11%{?dist}
License:       GPL-2.0-only
URL:           https://github.com/lyonel/lshw
Source0:       https://github.com/lyonel/lshw/archive/refs/tags/%{version}.tar.gz
Source1:       https://salsa.debian.org/openstack-team/third-party/lshw/raw/debian/stein/debian/patches/lshw-gtk.1
Patch:         lshw-B.02.20-209f83.patch
Patch:         lshw-B.02.18-scandir.patch
Patch:         lshw-B.02.20-cmake.patch
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gettext
%if %{with gui}
BuildRequires: gtk3-devel >= 3.24
BuildRequires: libappstream-glib
%endif
BuildRequires: ninja-build
BuildRequires: python3-devel
BuildRequires: sqlite-devel
Requires:      hwdata
%description
lshw is a small tool to provide detailed informaton on the hardware
configuration of the machine. It can report exact memory
configuration, firmware version, mainboard configuration, CPU version
and speed, cache configuration, bus speed, etc. on DMI-capable x86
systems and on some PowerPC machines (PowerMac G4 is known to work).

Information can be output in plain text, XML or HTML.

%if %{with gui}
%package       gui
Summary:       Graphical hardware lister
Requires:      polkit
Requires:      %{name} = %{version}-%{release}
%description   gui
Graphical frontend for the hardware lister (lshw) tool. If desired,
hardware information can be saved to file in plain, XML or HTML
format.
%endif

%prep
%autosetup -p1

%build
%if %{with gui}
%global gui_config -DGUI=ON
%else
%global gui_config -DGUI=OFF
%endif

%cmake -DNOLOGO=ON -DHWDATA=OFF -DPOLICYKIT=ON -DSQLITE=ON -DBUILD_SHARED_LIBS=OFF %{gui_config} -GNinja
%cmake_build

%install
%cmake_install
%if %{with gui}
install -m0644 -D %{SOURCE1} %{buildroot}%{_mandir}/man1/lshw-gui.1
%if "%{_sbindir}" != "%{_bindir}"
ln -s gtk-lshw %{buildroot}%{_sbindir}/lshw-gui
%endif
%endif
# translations seems borken, remove for now
#find_lang %{name}
rm -rf %{buildroot}%{_datadir}/locale/*/

%check
%if %{with gui}
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml
%endif

# check json output is valid
%{_vpath_builddir}/src/lshw -json \
    -disable usb -disable pcmcia -disable isapnp \
    -disable ide -disable scsi -disable dmi -disable memory \
    -disable cpuinfo 2>/dev/null | %{__python3} -m json.tool

#files -f %{name}.lang
%files
%license COPYING
%doc README.md
%{_mandir}/man1/lshw.1*
%{_sbindir}/lshw

%if %{with gui}
%files gui
%license COPYING
%{_bindir}/lshw-gui
%{_sbindir}/gtk-lshw
%if "%{_sbindir}" != "%{_bindir}"
%{_sbindir}/lshw-gui
%endif
%{_mandir}/man1/lshw-gui.1*
%dir %{_datadir}/lshw
%{_datadir}/lshw/artwork
%dir %{_datadir}/lshw/ui
%{_datadir}/lshw/ui/gtk-lshw.ui
%{_datadir}/pixmaps/gtk-lshw.svg
%{_datadir}/applications/gtk-lshw.desktop
%{_datadir}/appdata/gtk-lshw.appdata.xml
%{_datadir}/polkit-1/actions/org.ezix.lshw.gui.policy
%endif

%changelog
* Mon Jan 12 2026 Terje Rosten <terjeros@gmail.com> - B.02.20-10
- Improve cmake patch to get all required flags added
- Increase required cmake version
- Update to latest commit 209f83

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - B.02.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Feb 27 2025 Terje Rosten <terjeros@gmail.com> - B.02.20-8
- Work with newer cmake

* Thu Feb 27 2025 Terje Rosten <terjeros@gmail.com> - B.02.20-7
- Redo sbin merge logic (Yaakov Selkowitz <yselkowi@redhat.com>)

* Mon Feb 24 2025 Terje Rosten <terjeros@gmail.com> - B.02.20-6
- Unbreak sbin merge

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - B.02.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - B.02.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - B.02.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - B.02.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 06 2024 Terje Rosten <terje.rosten@ntnu.no> - B.02.20-1
- B.02.20
- Remove all upstream patches

* Tue Aug 08 2023 Terje Rosten <terje.rosten@ntnu.no> - B.02.19.2-13
- Use SPDX licence

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - B.02.19.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 05 2023 Terje Rosten <terje.rosten@ntnu.no> - B.02.19.2-11
- Use modern macros

* Tue Apr 04 2023 Yaakov Selkowitz <yselkowi@redhat.com> - B.02.19.2-10
- Update to upstream commit 76afbaaf40e

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - B.02.19.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - B.02.19.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 19 2022 Stewart Smith <trawets@amazon.com> - B.02.19.2-7
- Make GUI an optional bcond
- Disable remote DNS lookup on 'lshw -version'

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - B.02.19.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - B.02.19.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - B.02.19.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - B.02.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Apr 24 2020 Terje Rosten <terje.rosten@ntnu.no> - B.02.19.2-2
- Add patch from openSUSE to fix rhbz#1822455

* Tue Mar 24 2020 Terje Rosten <terje.rosten@ntnu.no> - B.02.19.2-1
- B.02.19.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 28 2019 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-21
- Update to commit 6cc0581
- Rebase cmake patch on top 6cc0581
- Add NVME patch from PR#45

* Sat May 25 2019 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-20
- Add lshw-gui man page (from Debian, thanks!)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - B.02.18-17
- Rebuilt for Python 3.7

* Mon Apr 02 2018 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-16
- Update to commit 20cda77
- Convert to cmake build system

* Thu Feb 08 2018 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-15
- Fix JSON issue (rhbz#1543320)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-13
- Fix date
- Need gettext

* Fri Jan 26 2018 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-12
- Update to commit d05baa7

* Mon Aug 28 2017 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-11
- Prefer lshw-gui in lshw-gui context

* Sun Aug 13 2017 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-10
- Add AppData bz#1476498

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 24 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-5
- Modify lshw gui wrapper to fix bz#1368404

* Thu Aug 11 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-4
- Add patches to fix sysconf/long_bit issue and crash (bz#1342792)

* Wed May 18 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-3
- Add patch to fix crash (bz#1332486)

* Mon Apr 25 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-2
- Date fix

* Mon Apr 25 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-1
- B.02.18

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - B.02.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - B.02.17-5
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 30 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.17-2
- Add patch to fix segfault in scan fat code

* Thu Sep 26 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.17-1
- B.02.17

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 09 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-8
- Rename macro

* Sun Jun 09 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-7
- Fix desktop file (bz #953684)
- Remove broken translations (bz #905896)
- Add vendor macro
 
* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - B.02.16-6
- Drop desktop vendor tag.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-3
- Switch from consolehelper to PolicyKit (bz #502730)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-2
- Rebuilt for c++ ABI breakage

* Sun Jan 29 2012 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-1
- B.02.16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Terje Rosten <terje.rosten@ntnu.no> - B.02.15-3
- Own all dirs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 21 2010 Terje Rosten <terje.rosten@ntnu.no> - B.02.15-1
- B.02.15
- Remove patches now upstream
- Build with sqlite support

* Sun Sep 05 2010 Terje Rosten <terje.rosten@ntnu.no> - B.02.14-5
- Add patch to fix build with gcc-4.5

* Sun Sep 05 2010 Terje Rosten <terje.rosten@ntnu.no> - B.02.14-4
- Add patch to fix ext4 issue

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 06 2009 Adam Jackson <ajax@redhat.com> - B.02.14-2
- Requires: hwdata
- Drop redundant copies of pci.ids and friends, since we'll pick up the
  copies in hwdata at runtime

* Sun Mar  1 2009 Terje Rosten <terjeros@phys.ntnu.no> - B.02.14-1
- B.02.14
- Drop gcc43 patch now upstream

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.13-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.13-3
- rebuild

* Wed Aug 13 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.13-2
- proper patch macro

* Wed Aug 13 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.13-1
- B.02.13
- remove patches now upstream
- add new gcc43 patch

* Tue Apr 15 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-5
- rebuild

* Tue Apr 15 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-4
- add patch to fix bz #442501

* Mon Feb 11 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-3
- add patch to build with gcc-4.3

* Sat Feb 09 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-2
- rebuild

* Mon Nov  5 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-1
- B.02.12.01
- Replace trademark icons

* Tue Aug 14 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11.01-3
- Move desktop and pam config to files
- Simplify build

* Tue Aug 07 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11.01-2
- Remove trademarks

* Mon Aug 06 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11.01-1
- B.02.11.01

* Sun Aug 05 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11-3
- Move artwork to gui subpackage
- Implement consolehelper support

* Sat Aug 04 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11-2
- License is GPLv2 (only)
- Fix ui %%description

* Wed Aug 01 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11-1
- Follow upstream version scheme

* Wed Jul 25 2007 Terje Rosten <terjeros@phys.ntnu.no> - 2.11-1
- 2.11

* Wed Jun 27 2007 Terje Rosten <terjeros@phys.ntnu.no> - 2.10-2
- minor fixes
- add patch to avoid stripping
- add desktop file
- strip changelog
- move from sbin to bin
- new url

* Wed Feb 14 2007 Dag Wieers <dag@wieers.com> - 2.10-1 - 4876+/dag
- Updated to release B.02.10.

* Tue Dec 21 2004 Dag Wieers <dag@wieers.com> - 2.0-1
- Initial package. (using DAR)

