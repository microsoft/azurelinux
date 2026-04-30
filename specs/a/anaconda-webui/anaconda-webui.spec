# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           anaconda-webui
Version:        53.1^20251022g00cddf56
Release: 2%{?dist}
Summary:        Anaconda installer Web interface
License:        LGPL-2.1-or-later AND MIT
URL:            https://github.com/rhinstaller/%{name}

#Source0:        https://github.com/rhinstaller/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
# Manual instructions (until patch builds work https://pagure.io/packaging-committee/issue/1496 )
# git clone https://github.com/AdamWill/anaconda-webui.git
# cd anaconda-webui
# git checkout 00cddf567f50a98f019f783161a6b20b9eedb190
# make dist
# this tarball contains
# https://github.com/AdamWill/anaconda-webui/commit/00cddf567f50a98f019f783161a6b20b9eedb190
# a dumb emergency fix for https://bugzilla.redhat.com/show_bug.cgi?id=2405872
Source0:        anaconda-webui-53.1.1.g00cddf56.tar.xz
BuildArch:      noarch
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  gettext
# Needed for the unitdir macro
BuildRequires: systemd-rpm-macros

%global anacondacorever 0

%if 0%{?fedora} > 41
%global anacondacorever 42.5
%endif

%global cockpitver 275

%define _unitdir /usr/lib/systemd/system

Requires: cockpit-storaged
Requires: cockpit-bridge >= %{cockpitver}
Requires: cockpit-ws >= %{cockpitver}
Requires: anaconda-core  >= %{anacondacorever}
# Firefox dependency needs to be specified there as cockpit web-view does not have a hard dependency on Firefox as
# it can often fall back to a diferent browser. This does not work in the limited installer
# environment, so we need to make sure Firefox is available. Exclude on RHEL, only Flatpak version will be there.
%if ! 0%{?rhel}
Requires: (firefox if fedora-release-workstation)
%endif
%if 0%{?fedora}
%endif
BuildRequires: desktop-file-utils

Provides: bundled(npm(@patternfly/patternfly)) = 6.3.1
Provides: bundled(npm(@patternfly/react-core)) = 6.3.1
Provides: bundled(npm(@patternfly/react-icons)) = 6.3.1
Provides: bundled(npm(@patternfly/react-log-viewer)) = 6.3.0
Provides: bundled(npm(@patternfly/react-styles)) = 6.3.1
Provides: bundled(npm(@patternfly/react-table)) = 6.3.1
Provides: bundled(npm(@patternfly/react-tokens)) = 6.3.1
Provides: bundled(npm(attr-accept)) = 2.2.5
Provides: bundled(npm(dequal)) = 2.0.3
Provides: bundled(npm(file-selector)) = 2.1.2
Provides: bundled(npm(focus-trap)) = 7.6.4
Provides: bundled(npm(js-tokens)) = 4.0.0
Provides: bundled(npm(lodash)) = 4.17.21
Provides: bundled(npm(loose-envify)) = 1.4.0
Provides: bundled(npm(luxon)) = 3.7.2
Provides: bundled(npm(memoize-one)) = 5.2.1
Provides: bundled(npm(object-assign)) = 4.1.1
Provides: bundled(npm(prop-types)) = 15.8.1
Provides: bundled(npm(react-dom)) = 18.3.1
Provides: bundled(npm(react-dropzone)) = 14.3.8
Provides: bundled(npm(react-is)) = 16.13.1
Provides: bundled(npm(react)) = 18.3.1
Provides: bundled(npm(scheduler)) = 0.23.2
Provides: bundled(npm(tabbable)) = 6.2.0
Provides: bundled(npm(throttle-debounce)) = 5.0.2
Provides: bundled(npm(tslib)) = 2.8.1

Requires: system-logos
%description
Anaconda installer Web interface

%prep
%setup -q -n %{name}

%build
# Nothing to build

%install
%make_install PREFIX=/usr

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/extlinks.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/anaconda-gnome-control-center.desktop

%check
exit 0
# We have some integration tests, but those require running a VM, so that would
# be an overkill for RPM check script.

%files
%dir %{_datadir}/cockpit/anaconda-webui
%doc README.rst
%license LICENSE dist/index.js.LEGAL.txt
%{_datadir}/cockpit/anaconda-webui/qr-code-feedback.svg
%{_datadir}/cockpit/anaconda-webui/index.js.LEGAL.txt
%{_datadir}/cockpit/anaconda-webui/index.html
%{_datadir}/cockpit/anaconda-webui/index.js.gz
%{_datadir}/cockpit/anaconda-webui/index.js.map
%{_datadir}/cockpit/anaconda-webui/index.css.gz
%{_datadir}/cockpit/anaconda-webui/index.css.map
%{_datadir}/cockpit/anaconda-webui/manifest.json
%{_datadir}/cockpit/anaconda-webui/po.*.js.gz
%{_datadir}/cockpit/anaconda-webui/VERSION.txt
%{_libexecdir}/anaconda/cockpit-coproc-wrapper.sh
%dir %{_datadir}/anaconda/firefox-theme
%dir %{_datadir}/anaconda/firefox-theme/default
%dir %{_datadir}/anaconda/firefox-theme/default/chrome
%{_datadir}/anaconda/firefox-theme/default/user.js
%{_datadir}/anaconda/firefox-theme/default/chrome/userChrome.css
%dir %{_datadir}/anaconda/firefox-theme/live
%dir %{_datadir}/anaconda/firefox-theme/live/chrome
%{_datadir}/anaconda/firefox-theme/live/user.js
%{_datadir}/anaconda/firefox-theme/live/chrome/userChrome.css
%dir %{_datadir}/anaconda/firefox-theme/extlink
%{_datadir}/anaconda/firefox-theme/extlink/user.js
%{_libexecdir}/anaconda/webui-desktop
%{_libexecdir}/anaconda/browser-ext
%{_datadir}/applications/extlinks.desktop
%{_datadir}/applications/anaconda-gnome-control-center.desktop
%{_unitdir}/webui-cockpit-ws.service


# The changelog is automatically generated and merged
%changelog
* Wed Oct 22 2025 Adam Williamson <awilliam@redhat.com> - 53.1^20251022g00cddf56-1
- emergency fix for console keyboard layout setting (rhbz#2405872)

* Tue Oct 21 2025 Toshio Kuratomi <toshio@fedoraproject.org> - 53.1-1
- components/localization: Only offer ASCII-capable keyboard layouts (rhbz#2402430)
- localization: dissallow layouts which do not support ASCII input in gnome
- storage: normalize locale decimals for PatternFly slider input (rhbz#2403028)
- review: storage: don't use action-description from blivet in conditions as it's translated
- storage: stop using inputValue from slider as it cannot parse localized floats
- storage: encryption: show warning when the compositor layout differs from target system default
- localization: set virtual console keymap explicity when choosing keyboards

* Thu Oct 09 2025 Packit <hello@packit.dev> - 53-1
- keyboard: in Gnome spawn Gnome keyboard settings in storage configurationscreen
- storage: installation-method: the screen id is
  'anaconda-screen-method' (Fixes notification for missing space for /boot)

* Thu Sep 25 2025 Packit <hello@packit.dev> - 52-1
- mount point mapping: keep menu within wizard scroll context (rhbz#2397098)

* Tue Sep 23 2025 Packit <hello@packit.dev> - 51-1
- storage: detect locked LUKS on selected disks including whole-disk LUKS (rhbz#2396646)
- Consume branding for Fedora from cockpit/static/branding.css
- webui-desktop: fix env variables scope for firefox to fix displayed icon

* Wed Sep 10 2025 Packit <hello@packit.dev> - 50-1
- fix(timezone): correctly parse timezones with multiple slashes
- fix(timezone): when reading timezone from backend read value from dbus object
- datetime:: dissallow proceeding custom NTP modal with empty values
- storage: Add mountpoints size check to storage review screen
- storage: Make size check on review screen a blocking error

* Wed Sep 10 2025 Adam Williamson <awilliam@redhat.com> - 48-3
- Actually apply patches from 48-2

* Fri Sep 05 2025 Katerina Koukiou <kkoukiou@redhat.com> - 48-2
- Fix: users: disallow proceeding from users page when neither root or user is configured (rhbz#2379957, rhbz#2392205, rhbz#2392203)
- Fix: prevent installations with not enough space on partitions used for system (rhbz#2351824)

* Mon Aug 25 2025 Packit <hello@packit.dev> - 48-1
- Infra and test improvements

* Tue Aug 05 2025 Packit <hello@packit.dev> - 46-1
- components: review: show selected timezone in the review screen

* Tue Jul 29 2025 Packit <hello@packit.dev> - 45-1
- components. datetime: introduce a Date and Time screen
- components: users: autogenerate username from full name
- components: users: support skipping account creation in the users screen (rhbz#2379957)
- components: users: improve text around user being in wheel group
- components: users: add hint for not using the root account

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Packit <hello@packit.dev> - 44-1
- logging: write error logs also to journal
- error: when frontend crash prompt users to also attach anaconda-webui log file
- components: storage: unify partition reset logic on page load (rhbz#2361201)

* Wed Jul 09 2025 Packit <hello@packit.dev> - 43-1
- components: port to new modal from Patternfly library
- Only require Firefox on Fedora Workstation
- Other test code and source code improvements

* Mon Jul 07 2025 Packit <hello@packit.dev> - 42-1
- components/localization: adjust menu height for smaller screens
- components/users: improve UX by focusing root password input on checkbox toggle
- Replace firefox-ext with browser-ext to handle Spins which do not have firefox as default
- Simplify webui-desktop script by removing unnecessary URL path parsing
- webui-desktop: modularize the script by isolating user creation and firefox logic
- webui-desktop: Add support for custom web engine

* Tue Jun 24 2025 Packit <hello@packit.dev> - 41-1
- components: error: redesign error reporting

* Thu Jun 19 2025 Packit <hello@packit.dev> - 40-1
- storage: mount-point-assignment: display partitions on RAID disks in mount point assignment
- storage: fix unselecting the only available disk
- storage: handle better scenarios when disk selection is not valid
- storage: home reuse: allow for Fedora along Windows on a single disk

* Tue May 27 2025 Packit <hello@packit.dev> - 39-1
- components: storage: DiskEncryption: removed unused properties

* Thu May 22 2025 Packit <hello@packit.dev> - 38-1
- Fix gnome detection logic: use process inspection to detect GNOME instead of XDG_CURRENT_DESKTOP

* Wed May 21 2025 Packit <hello@packit.dev> - 37.1-1
- show bootloader devices on review screen
- components: storage: fix disabled radio buttons
- storage: avoid rendering wizard pages while Cockpit Storage is active
- components: keyboard: run Gnome keyboard settings only on Gnome variant
- components: disk encryption: show selected keyboard also for non-gnome
- components: localization: show all keyboards for selection
- build: Introduce node_modules/ as submodule
- Support home reuse also on MBR partitioned disks

* Mon May 12 2025 Packit <hello@packit.dev> - 36-1
- build: bring back cockpit-storaged requirement

* Thu May 08 2025 Packit <hello@packit.dev> - 35-1
- Port patternfly version to 6
- fix: can't click outside of header dropdown to close it

* Tue Apr 15 2025 Packit <hello@packit.dev> - 34-1
- Migrate isFinal to new ProductData API
- storage: reclaim dialog: rely on official property for sticky header
- build: pin down cockpit-storaged version because of Patternfly 6 changes

* Tue Apr 08 2025 Packit <hello@packit.dev> - 33-1
- storage: mount point mapping: fix wrapping of the custom mount points rows
- cockpit-storage-integration: remove unused property from preparePartitioning method call
- cockpit-storage-integration: report failures when preparing partitioning
- cockpit-storage-integration: prevent race condition with selected disks
- cockpit-storage-integration: ensure checkStep is defined before checking its properties
- storage-actions: set IS_FETCHING to false after dispatching new devices
- cockpit-storage-integration: remove unused property `scenarioAvailability`
- storage: fix selected disk handling when replacing an MD RAID device (rhbz#2354798)
- Override globally modals min-width to stretch according to the contents (rhbz#2357172)
- storage: disable home reuse for existing non-linux systems

* Wed Apr 02 2025 Packit <hello@packit.dev> - 32-1
- cockpit-storage-integration: Fix disk selection after MD array deletion (rhbz#2354798)
- cockpit-storage-integration: move storage check steps to custom hook with step handling (rhbz#2354798)
- cockpit-storage-integration: reuse code when one of the storage preparation steps fail (rhbz#2354798)
- cockpit-storage-integration: seperate luks unlock wait logic from luks unlock itself (rhbz#2354798)
- cockpit-storage-integration: the waitForUnlockedDevices method is not destructive (rhbz#2354798)
- Do not offer home reuse if there is no GPT disk (rhbz#2353002)

* Fri Mar 28 2025 Packit <hello@packit.dev> - 31-1
- cockpit-storage-integration: Prevent crash when deleting an encrypted device
- language: fix markup to specify lang attribute (rhbz#2355246)
- mount-point-assignment: support disks as target devices (rhbz#2354044)
- storage: cockpit-storage: prevent bootloader partitions on MDRAID devices (rhbz#2352953)

* Wed Mar 26 2025 Packit <hello@packit.dev> - 30-1
- storage: fix parsing of usable devices for manual partitioning
- Ensure that translations are not requested at file load time (rhbz#2351026)
- storage: support disks with filesystem directly on them for installation (rhbz#2352385)

* Mon Mar 24 2025 Packit <hello@packit.dev> - 29-1
- storage: cockpit-storage-integration: ensure selected disks are
  re-configured after removing devices (rhbz#2351830)
- Ensure that translations are not requested at file load time
  (rhbz#2351026)

* Thu Mar 20 2025 Packit <hello@packit.dev> - 28-1
- po: Update from Fedora Weblate (rhbz#2351026)
- Fix translations that were prepared as string concatenation (rhbz#2351026)
- Adjust build target for translations: html2po was converted to python (rhbz#2351026)
- Adjust build target for translations: manifest2po was converted to python (rhbz#2351026)
- cockpit-storage-integration: reset partitioning always before disk rescan (rhbz#rhbz#2352573)
- cockpit-storage-integration: show 'use configured storage' scenario only if partitioning was applied (rhbz#2352573)
- tests: update pixel tests for new keyboard feature translations
- storage: when the bootloader partition is on different disks than rootfs choose bootloader device (rhbz#rhbz#2352573)

* Fri Mar 14 2025 Packit <hello@packit.dev> - 27-1
- storage: adjust scenario display order and default scenario selection

* Thu Mar 06 2025 Packit <hello@packit.dev> - 26-1
- storage: cockpit-storage: select newly created mdarrays if the user created them
- cockpit-storage: detect invalid mdarray configuration
- localization: spawn gnome settings for changing keyboards in workstation
- Do not display in the menus the extlinks Firefox app
- firefox-theme: swap option for disabling external link warning
- Do not show warning pop up for close on external link clicks
- storage: when checking available scenarios through cockpit-storage don't consider reclaim space
- cockpit-storage: when the user created a RAID device without content assume 'Use entire disk' scenario

* Tue Feb 18 2025 Packit <hello@packit.dev> - 25-1
- Add support for setting keyboard

* Fri Feb 14 2025 Packit <hello@packit.dev> - 24-1
- cockpit-storage-integration: fix using top level btrfs volume for root mount point (rhbz#2336489)
- infra: add logic for reporting test results to fedora wiki
- Other test and infra improvements

* Wed Jan 22 2025 Packit <hello@packit.dev> - 22-1
- Ensure that URL path is always set when loading the app (rhbz#2336488)
- Parse hidden_webui_pages option from anaconda.conf

* Mon Jan 20 2025 Packit <hello@packit.dev> - 21-1
- Parse new 'hidden_webui_screen' configuration file options

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 09 2024 Packit <hello@packit.dev> - 20-1
- firefox theme: fix Firefox parsing of user.js
- firefox theme: change CSS that hides UI when there's only 1 tab (rhbz#2330377)
- storage: home reuse: add check for unexpected existing mount points

* Mon Dec 02 2024 Packit <hello@packit.dev> - 19-1
- Disable removal of extended partition for efi OS
- Retheme to better match FedoraJarema (1):
- firefox: disable builtin Password Manager / Password Generation
- storage: when detecting usable partitions check all ancestors for the selected disks
- storage: restrict access to the storage editor to the scenario selection step
- storage: move disk unlocking to the installation method screen
- storage: refresh existing systems after unlocking devices
- review: show 'encrypted' instead of 'encrypt' for reused mount points

* Fri Nov 08 2024 Packit <hello@packit.dev> - 18-1
- reclaim: Make the list scroll instead of the modal body
- reclaim: Adjust layout and alignment
- ux: remove 'Make sure to have backed your data' warning
- storage: show device type not format type for non partitions
- ux: switch font weight to 'bold' for the storage actions in review
- storage: Hide mount point mapping scenario when no mountable partitions are available
- Open external links in firefox without the custom profile
- Move disk encryption under generic storage configuration step
- review: show device type if it's formatted as btrfs
- storage: cockpit: fix UI flickering when exiting cockpit storage
- Do not permit clicking 'Modify storage' button when installation has been started

* Fri Oct 25 2024 Packit <hello@packit.dev> - 17-1
- Run browser as liveuser instead of root
- Introduce new guided partitioning scenario 'Home reuse'
- Update strings based on latest mockups
- storage: mount-point-mapping page: group devices in selector by disk
- storage: disk selection: do not show sync-alt Icon when the spinner is on
- storage: emphasize the hint text in the reclaim modal
- review: storage section: show first column device and last column mount point
- Change the wording from 'Modify storage' to 'Launch storage editor'
- Move the cockpit-ws spawning to a service file
- Do not run firefox when remote installation is requested
- And few more enhancements with lower impact

* Mon Sep 23 2024 Packit <hello@packit.dev> - 16-1
- storage: mount point assignment: show partition labels in device selection
- components: common: remove AddressContext provider as it's not used
- Reimplement error handling using error boundaries (Resolves: rhbz#2308279)
- storage: re-design the disk selection component
- storage: move 'Modify storage' to the header kebab

* Wed Sep 11 2024 Packit <hello@packit.dev> - 15-1
- storage: use `console.warn` not `console.warning` to fix crash

* Mon Sep 09 2024 Adam Williamson <awilliam@redhat.com> - 14-3
- Backport #435 to really fix crash when device path doesn't exist

* Thu Sep 05 2024 Adam Williamson <awilliam@redhat.com> - 14-2
- Rebuild to get a combined update with anaconda

* Wed Sep 4 2024 Packit <hello@packit.dev> - 14-1
- Move webui-desktop in libexec to our subdirectory
- storage: fix crash when device path is not existing

* Mon Aug 19 2024 Packit <hello@packit.dev> - 13-1
- storage: Update text for cockpit storage confirmation modal
- storage: increase the radio button spacing in the scenario selection group
- storage: reclaim: don't schedule actions for partitions whose parents are removed
- review: switch from confirmation modal to checkbox
- storage: increase spacing between password fields
- users: fix spelling of 'privilege'
- storage: make reclaim dialog table compact
- storage: don't wrap disk name away from the icon
- storage: use name not device-id in the Name column in reclaim dialog
- Allow having duplicate device names
- storage: wait for iframe to load before adding event listeners
- storage: reclaim dialog: show format type not device type

* Tue Aug 6 2024 Packit <hello@packit.dev> - 12-1
- storage: display names not IDs in the storage screens

* Sat Aug 3 2024 Packit <hello@packit.dev> - 11-1
- Re-add alert confirmation before Cockpit Storage
- storage: implement shrink partition action in reclaim dialog
- review: show previous and new size of resized devices
- review: remove the seperate 'Disk encryption' section
- review: hide account section for Workstation media
- storage: give hint on how to resize bitlocker encrypted windows partitions
- review: show resized partitions that belong to an OS
- storage: show icon for encrypted LUKS devices in Reclaim dialog

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Packit <hello@packit.dev> - 10-1
- review: show hostname and configuration option in server variant
- Adopt modal based design for the cockpit-storage iframe
- apis: Read storage-scenario-id from sessionStorage where it's stored
- storage: helpers: fix the calculation of device children
- storage: cockpit-integration: do not overwrite request object structure - only extend it  (Resolves: rhbz#226441)
- review: organize groups and seperate with gutter
- storage: create MANUAL partitioning after unlocking the devices
- Show the storage layout in the review page for all scenarios
- Do not filter steps manually as the isHidden property is handled internally
- actions: use modern async / await when reading device data
- storage: set InitializationMode when creating the partitioning
- storage: disable form before applying the partitioning
- Disable also navigation items when the form is disabled
- Introduce some logic for knowing if devices are currently being fetched
- Disable 'Return to installation' in cockpit storage dialog when fetching device data
- storage: reset the partitioning only if there is one applied
- storage: reset partitioning before loading the scenario selection
- storage: use getNewPartitioning reusable method also for manual
- storage: do not update the scenario selection while cockpit storage mode is open
- Disable the form by default on page enter and let each page enable it after initialization
- storage: reset the partitioning before enabling the form in the disk encryption screen
- Explicitely disable all scenarios when there are not selected disks
- Remove unused isHidden property from FormHelperText
- storage: get the partitioning information only for the last created partitioning
- storage: Introduce 'Reclaim space' dialog
- review: show delete actions only for partitions
- review: get the information about deleted devices from the original device tree
- test: fix test case for installation against a disk with an existing Linux OS
- review: show existing systems affected by deleted partitions
- review: extend note about deleted systems to show affected systems
- review: use helper functions for parsing the device tree data
- storage: fix available space in reclaim dialog when parent device is deleted

* Thu Apr 4 2024 Packit <hello@packit.dev> - 9-1
- Translation updates
- A large series code cleanups

* Wed Feb 21 2024 Packit <hello@packit.dev> - 8-1
- Change hardcoded installation phases to new API
- Add bootloader partition early check based on mount point constraints

* Mon Feb 19 2024 Packit <hello@packit.dev> - 7-1
- storage: fix password visibility toggle when clicking on 'eye' button (#2250790)
- storage: enhance integration between Anaconda Web UI and Cockpit storage (#2263971)
- storage: inform user when oops happens in cockpit-storage (#2264041)
- storage: do not force reformatting /
- storage: add storage layout review text in the cockpit-storage exit dialog

* Fri Feb 16 2024 Packit <hello@packit.dev> - 6-1
- Tests stabilization

* Wed Feb 7 2024 Packit <hello@packit.dev> - 5.2-1
- Packaging fixes and introduced installability test upstream

* Tue Jan 30 2024 Packit <hello@packit.dev> - 4-1
- storage: add support for recommended mount points

* Tue Jan 23 2024 Packit <hello@packit.dev> - 3-1
- Accounts: allow to set root password
- Add feedback section in the installation screen

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 5 2023 Packit <hello@packit.dev> - 2-1
- Improved field validation and other improvements in the user creation step

* Wed Nov 24 2021 Katerina Koukiou <kkoukiou@redhat.com> - 1-1
- First public preview of Anaconda Web UI after repository move
