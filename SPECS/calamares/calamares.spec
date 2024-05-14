# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global py_byte_compile 1
Summary:        Installer from a live CD/DVD/USB to disk
# do not use QtWebEngine because it no longer works with QtWebEngine >= 5.11
# (it now refuses to run as root unless "export QTWEBENGINE_DISABLE_SANDBOX=1")
# https://github.com/calamares/calamares/issues/1051
Name:           calamares
Version:        3.3.1
Release:        5%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://calamares.io/
# Source0..19 - source tarballs
Source0:        https://github.com/calamares/calamares/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source1..4 is an artifact from https://dev.azure.com/mariner-org/mariner/_git/calamares-installer-module
Source1:        calamares-users-3.0.3.tar.gz
Source2:        calamares-finished-3.0.2.tar.gz
Source3:        calamares-welcome-3.0.2.tar.gz
Source4:        calamares-partition-3.0.3.tar.gz
Source5:        calamares-license-3.0.2.tar.gz
# Source20..39 - configuration files
Source20:       license.conf
Source21:       settings.conf
Source22:       show.qml
Source23:       branding.desc
Source25:       stylesheet.qss
# Source40..100 - Assets
Source40:       azl-logo.png
# Run:
# lupdate-qt5 show.qml -ts calamares-auto_fr.ts
# then translate the template in linguist-qt5.
Source41:       calamares-auto_fr.ts
# Run:
# lupdate-qt5 show.qml -ts calamares-auto_de.ts
# then translate the template in linguist-qt5.
Source42:       calamares-auto_de.ts
# Run:
# lupdate-qt5 show.qml -ts calamares-auto_it.ts
# then translate the template in linguist-qt5.
Source43:       calamares-auto_it.ts
Source52:       azl-welcome.png
Source53:       azl-eula
# adjust some default settings (default shipped .conf files)
Patch0:         Azure-Linux-Calamares-Conf-Patch-3.3.1.patch
#Patch3:         round-to-full-disk-size.patch
# Due to a race condition, Calamares would crash intermittently when switching
# partitioning method or encryption password. Patch4 fixes that bug.
Patch4:         serialize-read-access.patch
# Progress bar would expect a non-false return from a pooled thread, assuming
# such result means a critical error. However, depending on timing
# the process might return false since it already exited. Patch5 fixes that bug.
#Patch5:         install-progress-bar-fix.patch

# Compilation tools
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc
# Other build-time tools
BuildRequires:  gettext
# KF 6
BuildRequires:  kf-kconfig-devel
BuildRequires:  kf-kcoreaddons-devel
BuildRequires:  kf-ki18n-devel
BuildRequires:  kf-kwidgetsaddons-devel
# Macros
BuildRequires:  kf-rpm-macros
# KPMCORE
BuildRequires:  kpmcore-devel >= 3.3
BuildRequires:  libatasmart-devel
# Other libraries
BuildRequires:  libgcrypt-devel
BuildRequires:  libpwquality-devel
BuildRequires:  parted
BuildRequires:  pkg-config
# Python 3
BuildRequires:  python3-devel >= 3.3
# Qt 6
BuildRequires:  qt-linguist >= 6.6.1
BuildRequires:  qttools-devel >= 6.6.1
BuildRequires:  qtbase-devel >= 6.6.1
BuildRequires:  qtdeclarative-devel >= 6.6.1
BuildRequires:  qtsvg-devel >= 6.6.1
BuildRequires:  polkit-qt6-1-devel
BuildRequires:  util-linux-devel
BuildRequires:  yaml-cpp-devel >= 0.5.1
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       coreutils
Requires:       efibootmgr
# Partition manipulation
Requires:       util-linux
# LVM / encrypted disk setup
Requires:       cryptsetup
Requires:       lvm2

# Fonts
Requires:       freefont
Requires:       grub2
Requires:       systemd
ExclusiveArch:  x86_64

%description
Calamares is a distribution-independent installer framework, designed to install
from a live CD/DVD/USB environment to a hard disk. It includes a graphical
installation program based on Qt 6. This package includes the Calamares
framework and the required configuration files to produce a working replacement
for Anaconda's liveinst.

%package        libs
Summary:        Calamares runtime libraries
Requires:       %{name} = %{version}-%{release}

%description    libs
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       cmake

%description    devel
The %{name}-devel package contains libraries and header files for
developing custom modules for Calamares.

%prep
# Setup main calamares source
%setup -q

rm -rf src/modules/{users,finished,welcome,partition,license}
# Replace modules with custom sources
%setup -q -T -a 1 -D
%setup -q -T -a 2 -D
%setup -q -T -a 3 -D
%setup -q -T -a 4 -D
%setup -q -T -a 5 -D
for module in users finished welcome partition license; do
    mv "$module-%{version}" src/modules/"$module"
done


# Apply custom license config
mv %{SOURCE20} src/modules/license/license.conf

%patch -P 0 -p1
#%patch3 -p1
%patch -P 4 -p1
#%patch5 -p1

%build
%cmake_kf \
  -DBUILD_TESTING:BOOL=OFF \
  -DWITH_PYTHONQT:BOOL=OFF \
  -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo" \
  -DINSTALL_POLKIT:BOOL=OFF \
  -DWITH_QT6=ON \
  -DWITH_QML=OFF

%cmake_build

%install
%cmake_install
# create the branding directory
mkdir -p %{buildroot}%{_datadir}/calamares/branding/AzureLinux/lang
lrelease-qt6 %{SOURCE41} -qm %{buildroot}%{_datadir}/calamares/branding/AzureLinux/lang/calamares-auto_fr.qm
lrelease-qt6 %{SOURCE42} -qm %{buildroot}%{_datadir}/calamares/branding/AzureLinux/lang/calamares-auto_de.qm
lrelease-qt6 %{SOURCE43} -qm %{buildroot}%{_datadir}/calamares/branding/AzureLinux/lang/calamares-auto_it.qm

install -p -m 644 %{SOURCE40} %{buildroot}%{_datadir}/calamares/branding/AzureLinux/azl-logo.png
install -p -m 644 %{SOURCE22} %{buildroot}%{_datadir}/calamares/branding/AzureLinux/show.qml
install -p -m 644 %{SOURCE23} %{buildroot}%{_datadir}/calamares/branding/AzureLinux/branding.desc
install -p -m 644 %{SOURCE25} %{buildroot}%{_datadir}/calamares/branding/AzureLinux/stylesheet.qss
install -p -m 644 %{SOURCE52} %{buildroot}%{_datadir}/calamares/branding/AzureLinux/azl-welcome.png

mkdir -p %{buildroot}%{_sysconfdir}/calamares

cp -r %{buildroot}%{_datadir}/calamares/branding/ %{buildroot}%{_sysconfdir}/calamares/
cp -r %{buildroot}%{_datadir}/calamares/modules/ %{buildroot}%{_sysconfdir}/calamares/

install -p -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/calamares/settings.conf

# EULA
install -p -m 644 %{SOURCE53} %{buildroot}%{_sysconfdir}/calamares/azl-eula

%find_lang calamares-python

%post

%files -f calamares-python.lang
%doc AUTHORS
%{_bindir}/calamares
%{_datadir}/applications/calamares.desktop
%{_datadir}/calamares/branding/AzureLinux/azl-logo.png
%{_datadir}/calamares/branding/AzureLinux/azl-welcome.png
%{_datadir}/calamares/branding/AzureLinux/branding.desc
%{_datadir}/calamares/branding/AzureLinux/lang/
%{_datadir}/calamares/branding/AzureLinux/show.qml
%{_datadir}/calamares/branding/AzureLinux/stylesheet.qss
%{_datadir}/calamares/branding/default/
%{_datadir}/calamares/modules/
%{_datadir}/calamares/qml/
%{_datadir}/calamares/settings.conf
%{_datadir}/icons/hicolor/scalable/apps/calamares.svg
%{_mandir}/man8/calamares.8*
%{_sysconfdir}/calamares/
%{_sysconfdir}/calamares/azl-eula
%{_sysconfdir}/calamares/settings.conf
%dir %{_datadir}/calamares/
%dir %{_datadir}/calamares/branding/
%dir %{_datadir}/calamares/branding/AzureLinux/

%files libs
%{_libdir}/calamares/
%{_libdir}/libcalamares.so.*
%{_libdir}/libcalamaresui.so.*

%files devel
%{_includedir}/libcalamares/
%{_libdir}/cmake/Calamares/
%{_libdir}/libcalamares.so
%{_libdir}/libcalamaresui.so

%changelog
* Wed Mar 20 2024 Sam Meluch <sammeluch@microsfot.com> - 3.3.1-5
- update calamares modules for runtime errors

* Tue Mar 12 2024 Sam Meluch <sammeluch@microsoft.com> - 3.3.1-4
- update license.conf file path to use azl-eula

* Fri Mar 08 2024 Sam Meluch <sammeluch@microsoft.com> - 3.3.1-3
- Fix python macros for calamares

* Thu Mar 07 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.3.1-2
- Updated reference to distro in patch file from "Mariner" to "Azure Linux"

* Tue Jan 16 2024 Sam Meluch <sammeluch@microsoft.com> - 3.3.1-1
- Upgrade to version 3.3.1 for Azure Linux 3.0
- Update patches to accomodate version 3.3.1

* Fri Jan 27 2023 Mateusz Malisz <mamalisz@microsoft.com> - 3.2.11-40
- Fix application crash when discoverin partitions due to a race condition with serialize-read-access.patch
- Fix application crash when the Mariner installer process thread have already exited during progress bar installation view
- Update Requires with some runtime dependencies for LVM and encryption support.

* Mon Jul 25 2022 Minghe Ren <mingheren@microsoft.com> - 3.2.11-39
- Modify users.conf to imporve security

* Mon Apr 04 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 3.2.11-38
- Fix partioning bug
- License verified

* Mon Jan 25 2021 Nicolas Ontiveros <niontive@microsoft.com> - 3.2.11-37
- Add "dmroot" flag to encrypted partition
- Hide verity root read only skus

* Fri Sep 04 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.2.11-36
- Add dictionary check for root encryption passphrase.

* Wed Sep 2 2020 Jon Slobodzian <joslobo@microsoft.com> 3.2.11-35
- Replaced temporary placeholder logo and images

* Wed Jul 29 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-34
- Update component tarballs to 1.1.0 version.

* Wed Jul 01 2020 Andrew Phelps <anphel@microsoft.com> 3.2.11-33
- Wait for installation to complete.

* Wed Jun 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.2.11-32
- Enable root encryption.

* Wed Jun 03 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-31
- Allow all portable filename characters in the username.

* Wed May 27 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-30
- Enable pressing navigation buttons with Enter(Return) key.

* Tue May 19 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-29
- Update user view adding regular user creation.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.2.11-28
- Added %%license line automatically

* Thu May 07 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-27
- Remove unnecessary system checks from startup.

* Wed May 06 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-26
- UI responsiveness improvements to the installation view.

* Wed May 06 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-25
- UI improvements to the partition and system configuration view.

* Tue May 05 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-24
- Replace white background in installation slideshow with a gray one to match the background.

* Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 3.2.11-23
- Replace BuildArch with ExclusiveArch

* Wed Apr 29 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-22
- Remove font package
- Add freefont dependency
- Update partition module (UI changes)
- Update welcome module (UI changes)
- Update user module (UI changes)

* Wed Apr 29 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-21
- Add stylesheet to branding that makes dialogs easier to see.

* Mon Apr 27 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-20
- User view improvements.
- License view improvements.
- Add placeholder license text.

* Thu Apr 23 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-19
- Update manual partitioning:
  - Remove LVM support from manual partitioning view.
  - Force GPT on new partition table.
  - Always use default bootloader path.
  - Ignore existing partition layout.

* Tue Apr 21 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-18
- Remove hide-installation-progress-bar patch
- Add use-single-job-for-progress-bar-value patch

* Thu Apr 16 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-17
- Replace partitioning module with a custom one.

* Mon Apr 13 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-16
- Integrate libpwquality and enable password quality checks to users module.

* Fri Apr 03 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.2.11-15
- Adding BuildRequires for the sake of enabling the "partition" module.

* Fri Apr 03 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-14
- Update welcome module sources.

* Fri Apr 03 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-13
- Add hide-installation-progress-bar patch
- Make mariner-logo equal in width and height to prevent stretching and its SHA.
- Update finish module SHA.

* Thu Apr 02 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-12
- Add SKU selection
- Refactor spec

* Thu Apr 02 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-11
- Add Mariner branding

* Thu Apr 02 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-10
- Add custom finished module and add its SHA.
- Increase users module version to 1.0.1 and update its SHA.

* Thu Apr 02 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-9
- Update settings.conf to show license and update its SHA.
- Add license.conf to overwrite default conf and add its SHA.
- Remove settings.conf patches from calamares-3.2.11-default-settings.patch

* Thu Apr 02 2020 Joe Schmitt <joschmit@microsoft.com> 3.2.11-8
- Update settings.conf and its SHA.

* Wed Apr 01 2020 Mateusz Malisz <mamalisz@microsoft.com> 3.2.11-7
- Update settings.conf and its SHA.

* Wed Apr 01 2020 Joe Schmitt <joschmit@microsoft.com> - 3.2.11-6
- Extract custom users module into modules directory

* Wed Apr 01 2020 Chris Co <chrco@microsoft.com> - 3.2.11-5
- Change ExclusiveArch to BuildArch and set to x86_64

* Tue Mar 31 2020 Joe Schmitt <joschmit@microsoft.com> - 3.2.11-4
- Fix missing python3 global
- Add custom users module
- Remove unused requires and buildrequires
- Remove snaphash macro
- Update Vendor and Distribution tags

* Mon Mar 30 2020 Mateusz Malisz <mamalisz@microsoft.com> - 3.2.11-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.11-1
- Update to 3.2.11 (fixes CVE-2019-13178)
- Rebase default-settings and kdesu patches
- default-settings patch: improve default branding (but auto is still better)
- Drop upstreamed shim-grub-cfg patch

* Sun May 12 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.8-3
- bootloader: shim-grub-cfg patch: fix destination path for grub.cfg
- default-settings patch: fix warnings due to missing or unimplemented settings

* Sun May 12 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.8-2
- bootloader: fix sb-shim mode to write grub.cfg into the EFI System Partition

* Fri May 10 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.8-1
- Update to 3.2.8
- Rebase default-settings patch, disable GeoIP that is now enabled by default
- Drop upstreamed boost-python3, unpackfs-dev,
  dont-unmount-dev-mapper-live-base, and mount-selinux patches

* Wed May 08 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-10
- mount: copy the SELinux context of the host directory to the mountpoint

* Wed May 08 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-9
- Revert the change from "-8", this cannot be done with shellprocess

* Wed May 08 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-8
- default-settings patch: enable the shellprocess module to create the mount
  point directories on the / partition with the correct SELinux contexts

* Mon May 06 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-7
- default-settings patch: update the log path in umount.conf

* Mon May 06 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-6
- Fix branding logos to use the correct form factor for each variant
- partition: do not unmount /dev/mapper/live-* (live-base needed in unpackfs)

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-5
- Drop the grub2-efi*-modules dependencies, not needed with sb-shim support
- Add Requires: efibootmgr instead, used by the sb-shim support
- default-settings patch: disable the new libpwquality check by default

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-4
- unpackfs: do not use -o loop if the source is a device (fails on F29+)

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-3
- Add BuildRequires: parted-devel (used in welcome to check storage requirement)

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-2
- Fix finding Boost::Python3 on F30+
- Only BuildRequire libatasmart-devel and libblkid-devel on F29-

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-1
- Update to 3.2.7 and update BuildRequires and Requires
- Add plasmalnf subpackage for the new plasmalnf module requiring plasma-desktop
- Switch webview from QtWebEngine to QtWebKit to work around upstream issue 1051
- Rebase default-settings patch and update some settings:
  - enable INSTALL_CONFIG by default (we patch it in place, so install it)
  - disable plymouthcfg by default (now only needed to change the default theme)
  - bootloader.conf: enable sb-shim (UEFI "Secure Boot" support)
  - plasmalnf.conf (note: module disabled by default): fix default liveuser
  - plasmalnf.conf (note: module disabled by default): default: show all themes
  - tracking.conf (note: module disabled by default): default tracking to none
  - users.conf: default to honoring the default shell from /etc/default/useradd
  - welcome.conf: use https for internetCheckUrl (catches more captive portals)
- Rebase kdesu patch

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Jonathan Wakely <jwakely@redhat.com> - 3.1.8-12
- Rebuilt for Boost 1.69

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 3.1.8-11
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1.8-9
- Rebuilt for Python 3.7

* Wed Feb 14 2018 Richard Shaw <hobbes1069@gmail.com> - 3.1.8-8
- Rebuild for yaml-cpp 0.6.0.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 3.1.8-6
- Rebuilt for Boost 1.66

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 3.1.8-5
- Rebuilt for switch to libxcrypt

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.1.8-4
- Remove obsolete scriptlets

* Tue Dec 26 2017 Mattia Verga <mattia.verga@email.it> - 3.1.8-3
- Rebuild for libkpmcore soname bump in rawhide

* Sun Dec 03 2017 Mattia Verga <mattia.verga@email.it> - 3.1.8-2
- Rebuild for libkpmcore soname bump in F27 and F26 branches

* Tue Nov 14 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.8-1
- Update to 3.1.8 (bugfix release)
- Rebase default-settings patch
- Update fallback PRODUCTURL and SUPPORTURL

* Wed Oct 25 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.7-1
- Update to 3.1.7

* Sun Oct 22 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.6-2
- Update grub2-efi* package names for 32-bit UEFI support (F27+) (#1505151)

* Sat Oct 14 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.6-1
- Update to 3.1.6

* Sun Oct 01 2017 Mattia Verga <mattia.verga@email.it> - 3.1.5-2
- Rebuild for libkpmcore soname bump

* Wed Sep 27 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.5-1
- Update to 3.1.5
- Rebase default-settings and kdesu patches
- Drop "-DWITH_CRASHREPORTER:BOOL=OFF", upstream removed the crash reporter
- Install calamares-python.mo, delete unused calamares-dummypythonqt.mo

* Mon Aug 14 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.1-1
- Update to 3.1.1
- Rebase default-settings patch
- Update auto branding to add welcomeStyleCalamares and sidebarTextHighlight
- Update minimum cmake and kpmcore versions
- Add manpage to the file list
- Disable crash reporter for now (as was the default in previous releases)

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 3.1.0-6
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 3.1.0-3
- Rebuilt for Boost 1.64

* Sun Jun 04 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.1.0-2
- Rebuild for libkpmcore soname bump

* Sun Mar 05 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.0-1
- Update to 3.1.0
- Rebase default-settings patch
- default-settings: comment out unneeded and problematic "sudoersGroup: wheel"
- default-settings: change the new internetCheckUrl to the Fedora hotspot.txt

* Thu Feb 09 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.0-2
- Rebuild for libboost_python3 soname bump

* Sat Jan 21 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.0-1
- Update to 3.0 (stable release, now out of beta)

* Thu Jan 19 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.0-0.1.beta2
- Update to 3.0-beta2 (upstream renamed 2.5 to 3.0)

* Thu Jan 19 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.5-0.2.beta1
- Update to 2.5-beta1
- Rebase default-settings patch

* Sun Jan 15 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.5-0.1.alpha1
- Update to 2.5-alpha1
- Rebase default-settings and kdesu patches

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.4.80-0.4.20161119git34516e9477b2f
- Rebuild for Python 3.6

* Sat Nov 19 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.80-0.3.20161119git34516e9477b2f
- New snapshot from git master (34516e9477b2fd5e9b3e5823350d1efc2099573f)

* Sun Nov 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.80-0.2.20161113gitd6e0e09bc1472
- Drop PowerPC arches from ExclusiveArch as we don't support them as live arches

* Sun Nov 13 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.80-0.1.20161113gitd6e0e09bc1472
- New snapshot from git master (d6e0e09bc1472009e2bdabd4186979dbf4c2303e)
- Drop upstreamed patches (UEFI fixes, Internet connection check)
- Rebase default-settings and kdesu patches
- BuildRequire kpmcore-devel >= 2.9.90

* Sun Nov 06 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.4-4
- Fix UEFI firmware workaround for 32-bit UEFI (CAL-403, patch by TeHMoroS)
- Disable the Requires: grub2-efi grub2-efi-modules on 32-bit x86 again

* Sat Nov 05 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.4-3
- Fix the check for available Internet connection on startup

* Sat Nov 05 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.4-2
- Fix UEFI installation failure in the bootloader module (bad vfat_correct_case)

* Fri Nov 04 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.4-1
- Update to 2.4.4 (bugfix release, should in particular fix UEFI on Fedora)
- Rebase default-settings patch for packages module changes
- Drop Requires: gdisk (sgdisk), no longer needed
- Enable Requires: grub2-efi also on 32-bit, should work too
- Requires: grub2-efi-modules for UEFI grub2-install until we get shim support

* Fri Oct 28 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.3-1
- Update to 2.4.3 (LUKS FDE support backported upstream, bugfixes)
- Drop grubcfg-quoting, dracut-luks-fde backports, now in upstream 2.4.x (2.4.3)

* Thu Oct 20 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.2-3
- grubcfg module: Fix mismatched quoting and escaping
- Update dracut-luks-fde backport with the grubcfg fixes for hostonly="no" mode

* Tue Oct 18 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.2-2
- Add (backport from master) support for LUKS full disk encryption (with dracut)
- Adjust default-settings patch accordingly

* Fri Oct 14 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.2-1
- Update to 2.4.2 (bugfix release)
- Drop upstreamed users-no-chfn and locale-utf8 patches
- Drop no-luks-fde patch, set enableLuksAutomatedPartitioning: false instead
- Don't write /etc/default/keyboard (set writeEtcDefaultKeyboard: false)

* Sun Oct 02 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.1-3
- BuildRequire Qt >= 5.6, required by the locale and netinstall modules
- Use kdesu instead of pkexec (works around #1171779)
- Hide the LUKS full disk encryption checkbox which does not work on Fedora yet

* Sun Sep 25 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.1-2
- locale module: Fix locale filtering for UTF-8 on Fedora

* Mon Sep 19 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.1-1
- Update to 2.4.1
- Drop support for separate partitionmanager tarball, kpmcore is now an external
  dependency (BuildRequires)
- Update KF5 build requirements
- Update minimum Boost requirement, decreased from 1.55.0 to 1.54.0
- Explicitly BuildRequire gcc-c++ >= 4.9.0
- Drop support for yum (i.e., for Fedora < 22)
- Rebase default-settings patch
- default-settings: Use America/New_York as the default time zone (matches both
                    Anaconda and upstream Calamares, remixes can override it)
- Drop desktop-file patch, use the upstream .desktop file and (now fixed) icon
- Update file list and scriptlets for the icon, add Requires: hicolor-icon-theme
- Use QtWebEngine for the optional webview module by default
- users module: Drop dependency on chfn, which is no longer installed by default
- Add an -interactiveterminal subpackage, new module depending on konsole5-part

* Tue Aug 23 2016 Richard Shaw <hobbes1069@gmail.com> - 1.1.4.2-5
- Rebuild for updated yaml-cpp

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Jonathan Wakely <jwakely@redhat.com> - 1.1.4.2-3
- Rebuilt for Boost 1.60

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Oct 31 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.4.2-1
- Update to 1.1.4.2
- Update URL tag and the calamares.io link in show.qml to use https

* Sat Sep 26 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.3-1
- Update to 1.1.3
- Add additional changes to calamares-default-settings.patch
- BuildRequires: qt5-qtwebkit-devel >= 5.3 for the webview module
- Add webview subpackage for the webview module (not used by default, extra dep)

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.1.2-2
- Rebuilt for Boost 1.59

* Mon Aug 17 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.2-1
- Update to 1.1.2 (#1246955)
- Add Requires: gdisk (for sgdisk), dmidecode, upower, NetworkManager
- Add slideshow translations (fr, de, it)
- Drop obsolete calamares-1.0.1-fix-version.patch
- Rebase calamares-default-settings.patch

* Wed Aug 05 2015 Jonathan Wakely <jwakely@redhat.com> 1.0.1-6.20150502gita70306e54f505
- Rebuilt for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5.20150502gita70306e54f505
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 03 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.1-4.20150502gita70306e54f505
- New snapshot, fixes bugs, improves EFI support, UI and translations
- Drop fix-reboot patch, fixed upstream
- Update default-settings patch
- Update automatic branding generation scriptlet

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 05 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.1-2
- Fix the version number reported in the About dialog (1.0.1, not 1.0.0)
- Apply upstream fix to make "Restart now" in "Finished" page actually reboot
- Make the link in the default show.qml clickable

* Mon Feb 02 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.1-1
- Update to the official release 1.0.1 (adds slideshow support, "Finished" page)
- Install a show.qml with a default, Calamares-branded slideshow
- BuildRequires:  qt5-qtdeclarative-devel >= 5.3 (needed for the new slideshow)

* Mon Jan 19 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-8.20150119git5c6a302112cee
- New snapshot, fixes swap fstab entries and yum/dnf package removal

* Sun Jan 11 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-7.20150105gitfe44633e0ca52
- Rebuild for new extra-cmake-modules (to verify that it still builds)

* Sat Jan 10 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-6.20150105gitfe44633e0ca52
- New snapshot, improves the partitioning interface and updates translations
- Point URL to https://calamares.io/
- default-settings patch: Enable the packages module, make it remove calamares
- desktop-file patch: Remove the NoDisplay=true line, unneeded with the above
- Requires: dnf or yum depending on the Fedora version, for the packages module

* Sun Dec 07 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-5.20141206giteb748cca8ebfc
- Bump Release to distinguish official F21 update from Copr build

* Sun Dec 07 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-4.20141206giteb748cca8ebfc
- New snapshot, fixes detection and setup of display managers
- default-settings patch: Don't delist non-sddm DMs from displaymanager.conf
- Drop the Requires: sddm, no longer needed (now works with any DM or even none)

* Sat Dec 06 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-3.20141206git75adfa03fcba0
- New snapshot, fixes some bugs, adds partial/incomplete grub-efi support
- Add ExclusiveArch matching the livearches from anaconda.spec (#1171380)
- Requires: grub-efi on x86_64
- Rebase default-settings patch, set efiBootloaderId in grub.cfg

* Sat Nov 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-2.20141128giteee54241d1f58
- New snapshot, sets the machine-id, fixes mounting/unmounting bugs
- Rebase default-settings patch

* Thu Nov 27 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-1.20141127git8591dcf731cbf
- New snapshot, adds locale selector, fixes installation with SELinux enabled
- Use the version number from CMakeLists.txt, now at 0.17.0
- Use post-release snapshot numbering, milestone 0.17 was already reached

* Mon Nov 24 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.17.20141123gitc17898a6501fd
- New snapshot, adds "About" dialog and improves partitioning error reporting

* Thu Nov 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.16.20141119git01c3244396f35
- Automatically generate the branding to use by default (new "auto" branding)
- Remove README.branding, no longer needed

* Thu Nov 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.15.20141119git01c3244396f35
- New snapshot, creates /etc/default/grub if missing (calamares#128)
- README.branding: Mention new bootloaderEntryName setting
- Remove no longer needed workaround that wrote /etc/default/grub in %%post

* Tue Nov 18 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.14.20141117gitdf47842fc7a03
- New snapshot, makes Python modules get branding information from branding.desc
- README.branding: Update with the resulting simplified instructions

* Sat Nov 15 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.13.20141115git6b2ccfb442def
- New snapshot, adds retranslation support to more modules, fixes writing
  /etc/hosts, writes /etc/locale.conf (always LANG=en_US.UTF-8 for now)
- Drop grub2-tools (calamares#123) patch, names made configurable upstream
- Update default-settings patch to set the grub2 names and handle new modules
- Drop workaround recreating calamares/libcalamares.so symlink, fixed upstream
- Move desktop-file-validate call to %%check

* Tue Nov 11 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.12.20141111gitfaa77d7f5e656
- New snapshot, writes keyboard configuration files to the installed system
  (calamares#31), adds a language selector and dynamic retranslation support

* Fri Nov 07 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.11.20141107gitfd5d1935290d9
- New snapshot, fixes the calamares#132 fix again, fixes enabling translations

* Thu Nov 06 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.10.20141106git1df44eddba572
- New snapshot, fixes the calamares#132 fix, calamares#124 (colors in build.log)
- Drop pkexec policy rename from desktop-file patch, fixed upstream

* Wed Nov 05 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.9.20141104gitb9af5b7d544a7
- New snapshot, creates sddm.conf if missing (calamares#132), adds translations
- Use and customize the new upstream .desktop file
- Point URL to the new https://calamares.github.io/ page

* Tue Oct 28 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.8.20141028git10ca85338db00
- New snapshot, fixes FTBFS in Rawhide (Qt 5.4.0 beta) (calamares#125)

* Tue Oct 28 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.7.20141027git6a9c9cbaae0a9
- Add a README.branding documenting how to rebrand Calamares

* Mon Oct 27 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.6.20141027git6a9c9cbaae0a9
- New snapshot, device-source patch (calamares#127) upstreamed

* Thu Oct 23 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.5.20141020git89fe455163c62
- Disable startup notification, does not work properly with pkexec

* Wed Oct 22 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.4.20141020git89fe455163c62
- Add a .desktop file that live kickstarts can use to show a menu entry or icon

* Mon Oct 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.3.20141020git89fe455163c62
- New snapshot, fixes escape sequences in g++ diagnostics in the build.log
- Allow using devices as sources for unpackfs, fixes failure to install
- Write /etc/default/grub in %%post if missing, fixes another install failure
- Fix the path to grub.cfg, fixes another install failure
- Own /etc/calamares/branding/

* Mon Oct 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.2.20141017git8a623cc1181e9
- Pass -DWITH_PARTITIONMANAGER:BOOL="ON"
- Pass -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"
- Remove unnecessary Requires: kf5-filesystem

* Mon Oct 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.1.20141017git8a623cc1181e9
- Initial package
