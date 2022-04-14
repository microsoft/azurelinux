%global glib2_version 2.45.8
%global libsoup_version 2.51.92
%global json_glib_version 1.1.2
%global gdk_pixbuf_version 2.31.5

Summary:   Library for AppStream metadata
Name:      libappstream-glib
Version:   0.7.17
Release:   2%{?dist}
License:   LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:       http://people.freedesktop.org/~hughsient/appstream-glib/
Source0:   http://people.freedesktop.org/~hughsient/appstream-glib/releases/appstream-glib-%{version}.tar.xz

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: docbook-utils
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel
BuildRequires: gperf
BuildRequires: libarchive-devel
BuildRequires: libsoup-devel >= %{libsoup_version}
BuildRequires: gdk-pixbuf2-devel >= %{gdk_pixbuf_version}
BuildRequires: gettext
BuildRequires: libuuid-devel
BuildRequires: libstemmer-devel
BuildRequires: json-glib-devel >= %{json_glib_version}
BuildRequires: meson
BuildRequires: rpm-devel
BuildRequires: git-core

# for the builder component
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: pango-devel

# for the manpages
BuildRequires: libxslt
BuildRequires: docbook-style-xsl

# Make sure we pull in the minimum required versions
Requires: gdk-pixbuf2%{?_isa} >= %{gdk_pixbuf_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: json-glib%{?_isa} >= %{json_glib_version}
Requires: libsoup%{?_isa} >= %{libsoup_version}

# no longer required
Obsoletes: appdata-tools < 0.1.9
Provides: appdata-tools

# Removed in F30
Obsoletes: libappstream-glib-builder-devel < 0.7.15

# this is not a library version
%define as_plugin_version               5

%description
This library provides GObjects and helper methods to make it easy to read and
write AppStream metadata. It also provides a simple DOM implementation that
makes it easy to edit nodes and convert to and from the standardized XML
representation.

%package devel
Summary: GLib Libraries and headers for appstream-glib
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
GLib headers and libraries for appstream-glib.

%package builder
Summary: Library and command line tools for building AppStream metadata
Requires: %{name}%{?_isa} = %{version}-%{release}
Recommends: pngquant

%description builder
This library and command line tool is used for building AppStream metadata
from a directory of packages.

%prep
%autosetup -p1 -Sgit -n appstream-glib-%{version}

%build
%meson \
    -Dgtk-doc=true \
    -Dstemmer=true \
    -Ddep11=false \
    -Dfonts=false
%meson_build

%install
%meson_install

%find_lang appstream-glib

%ldconfig_scriptlets
%ldconfig_scriptlets builder

%files -f appstream-glib.lang
%license COPYING
%doc README.md AUTHORS NEWS
%{_libdir}/libappstream-glib.so.8*
%{_libdir}/girepository-1.0/*.typelib
%{_bindir}/appstream-util
%{_bindir}/appstream-compose
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/appstream-util
%{_mandir}/man1/appstream-util.1.gz
%{_mandir}/man1/appstream-compose.1.gz

%files devel
%{_libdir}/libappstream-glib.so
%{_libdir}/pkgconfig/appstream-glib.pc
%dir %{_includedir}/libappstream-glib
%{_includedir}/libappstream-glib/*.h
%{_datadir}/gtk-doc/html/appstream-glib
%{_datadir}/gir-1.0/AppStreamGlib-1.0.gir
%{_datadir}/aclocal/*.m4
%{_datadir}/installed-tests/appstream-glib/*.test
%{_datadir}/gettext/its/appdata.its
%{_datadir}/gettext/its/appdata.loc

%files builder
%license COPYING
%{_bindir}/appstream-builder
%{_datadir}/bash-completion/completions/appstream-builder
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_appdata.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_desktop.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_gettext.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_hardcoded.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_icon.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_shell_extension.so
%{_mandir}/man1/appstream-builder.1.gz

%changelog
* Thu Feb 25 2021 Henry Li <lihl@microsoft.com> 0.7.17-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove gtk dependency
- Add -Dfonts=false to disable fonts modules which depend on gtk 
- Remove libasb_plugin_font.so from builder subpackage

* Thu Feb 20 2020 Richard Hughes <richard@hughsie.com> 0.7.17-1
- New upstream release
- Add "icon-theme" as recognised component type
- Fix CI by moving 'future' back a bit
- Make default content rating values match OARS semantics
- Properly initialize unique_id_mutex

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Kalev Lember <klember@redhat.com> - 0.7.16-2
- Backport a patch to fix parsing Qt translations in subdirectories

* Mon Sep 30 2019 Richard Hughes <richard@hughsie.com> 0.7.16-1
- Update to 0.7.15
- Add UPL short name to SPDX conversion
- Allow parsing desktop files using as_app_parse_data()
- Do not preserve restrictive permissions when installing AppStream files
- Modernize the validation requirements
- Remove relative path from icon names
- Support loading YAML from as_store_from_bytes()
- Update list of allowed metadata licences
- Update the SPDX license list to v3.5

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 22:13:19 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.15-3
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:02 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.15-2
- Rebuild for RPM 4.15

* Thu Feb 28 2019 Kalev Lember <klember@redhat.com> - 0.7.15-1
- Update to 0.7.15
- Remove and obsolete the -builder-devel subpackage

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 28 2018 Kalev Lember <klember@redhat.com> 0.7.14-4
- Backport an upstream patch to fix common gnome-software crash

* Tue Dec 18 2018 Kalev Lember <klember@redhat.com> 0.7.14-3
- Backport AsStore locking patches from upstream

* Wed Oct 24 2018 Kalev Lember <klember@redhat.com> 0.7.14-2
- Add new as_utils_vercmp_full() API for gnome-software

* Tue Oct 16 2018 Richard Hughes <richard@hughsie.com> 0.7.14-1
- New upstream release
- Add new API for gnome-software
- Set the AppStream ID from the X-Flatpak desktop key

* Fri Sep 28 2018 Richard Hughes <richard@hughsie.com> 0.7.13-1
- New upstream release
- Do not restrict the maximum number of releases allowed
- Throw an error when a launchable desktop-id is invalid

* Mon Aug 13 2018 Richard Hughes <richard@hughsie.com> 0.7.12-1
- New upstream release
- Support localised text in agreement sections

* Thu Aug 09 2018 Richard Hughes <richard@hughsie.com> 0.7.11-1
- New upstream release
- Add AS_APP_QUIRK_DEVELOPER_VERIFIED
- Escape quotes in attributes
- Provide async variants of store load functions

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard Hughes <richard@hughsie.com> 0.7.10-1
- New upstream release
- Do not parse firmware files anymore
- Do not require a release transaction when validating in relaxed mode
- Extract release descriptions and agreement sections for translation

* Mon Jun 04 2018 Richard Hughes <richard@hughsie.com> 0.7.9-1
- New upstream release
- Convert local icons found in metainfo files
- Follow the Debian tilde usage when ordering versions
- Use the launchable to find the desktop filename

* Fri Apr 20 2018 Richard Hughes <richard@hughsie.com> 0.7.8-1
- New upstream release
- Add as_version_string() for fwupd
- Add support for component agreements
- Correctly compare version numbers like '1.2.3' and '1.2.3a'
- Don't include the path component in the name when parsing the package filename
- If the launchable is specified don't guess it when composing
- Never add more than one component to the AppStream store when composing

* Tue Apr 17 2018 Kalev Lember <klember@redhat.com> 0.7.7-3
- Veto apps that have empty OnlyShowIn= (#1568492)

* Thu Mar 15 2018 Kalev Lember <klember@redhat.com> 0.7.7-2
- Backport a patch to add as_utils_unique_id_match()

* Tue Mar 13 2018 Richard Hughes <richard@hughsie.com> 0.7.7-1
- New upstream release
- Add custom metadata key for shell extension uuid
- Always resize AppStream icons to fit the destination size
- Correctly validate files using OR in the metadata_license
- Do not fail to validate if the timestamps are out of order
- Don't abort the build if pngquant fails
- Update the SPDX license list to v3.0

* Fri Feb 09 2018 Richard Hughes <richard@hughsie.com> 0.7.6-1
- New upstream release
- Add support for release types

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.5-4
- Switch to %%ldconfig_scriptlets

* Tue Jan 30 2018 Richard Hughes <richard@hughsie.com> 0.7.5-3
- Backport a fix from master to fix XML generation.

* Wed Jan 24 2018 Richard Hughes <richard@hughsie.com> 0.7.5-2
- Backport two crash fixes from master.

* Mon Jan 22 2018 Richard Hughes <richard@hughsie.com> 0.7.5-1
- New upstream release
- Add more GObject Introspection annotations for Python
- Do not try to extract duplicate files in the icon theme packages
- Don't expect an enum when really passing a bitfield
- Fix a crash when calling as_release_add_location() directly
- Fix appstream-compose when using new-style desktop IDs
- Fix compile with GCab v1.0
- Fix the arithmetic when fitting an image in 16:9
- Generate icons and samples for emoji fonts
- Never change the default screenshot when processing AppData
- Support OARS v1.1 additions
- Use pngquant to make the application icons take up less space

* Thu Nov 09 2017 Kalev Lember <klember@redhat.com> 0.7.4-1
- Update to 0.7.4

* Mon Oct 23 2017 Richard Hughes <richard@hughsie.com> 0.7.3-1
- New upstream release
- Add new API required by fwupd
- Do not assign "flatpak" as an app's origin when no origin was found
- Fix the inode mode to be sane on extracted files
- Prefer /usr/share/metainfo as default path for metainfo files
- Write XML for newer AppStream specification versions

* Mon Aug 21 2017 Richard Hughes <richard@hughsie.com> 0.7.2-1
- New upstream release
- Allow remote icon types for desktop AppData files
- Do not check the suffix of <id> tags
- Prefer /usr/share/metainfo as default path for metainfo files

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.1-4
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.1-3
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.1-2
- Rebuilt for RPM soname bump

* Thu Aug 03 2017 Richard Hughes <richard@hughsie.com> 0.7.1-1
- New upstream release
- Add <id> kinds for application provides
- Fail to validate if AppData screenshots are duplicated
- Install appdata-xml.m4
- Skip loading desktop data from Snap directory
- Update the SPDX license list to 2.6
- Validate the <id> format according to the spec

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Richard Hughes <richard@hughsie.com> 0.7.0-1
- New upstream release
- Add the limits in the validation output messages
- Do not enforce that the project is a valid environment_id
- Don't cast gsize to guint32 when getting file length
- Remove the cache-id functionality
- Show a warning if adding keywords after the cache creation
- Switch to the meson build system

* Mon May 08 2017 Richard Hughes <richard@hughsie.com> 0.6.13-1
- New upstream release
- Add a 'check-component' command to appstream-util
- Add new API for gnome-software and fwupd
- Add support for icon scaling and <launchable>
- Allow using the app origin as a search keyword
- Casefold all stemmed entries
- Support non-numeric version numbers correctly

* Wed Apr 12 2017 Richard Hughes <richard@hughsie.com> 0.6.12-1
- New upstream release
- Validate kudos in AppData and AppStream files
- Copy hash table keys to avoid a common crash on Ubuntu
- Fix the predicate comparison when using globs in metainfo files

* Mon Mar 20 2017 Richard Hughes <richard@hughsie.com> 0.6.11-1
- New upstream release
- Add initial support for Mozilla .xpi translations
- Fix a problem with appstream-compose with older AppData files
- Make content_rating required for any component with a 'Game' category
- Parse small version numbers correctly
- Show a warning if a desktop file is not found when required

* Mon Mar 06 2017 Richard Hughes <richard@hughsie.com> 0.6.10-1
- New upstream release
- Fix small unintentional ABI break
- Ignore <p></p> in AppStream markup

* Mon Feb 27 2017 Richard Hughes <richard@hughsie.com> 0.6.9-1
- New upstream release
- Do not set the AsApp state using the AsRelease state
- Fail to validate if any release is in the future or in the wrong order

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Kalev Lember <klember@redhat.com> 0.6.8-2
- Backport a patch for overly strict appstream-util validate-relax

* Thu Feb 02 2017 Kalev Lember <klember@redhat.com> 0.6.8-1
- New upstream release

* Fri Jan 27 2017 Kalev Lember <klember@redhat.com> 0.6.7-3
- Backport two use-after-free fixes from upstream

* Mon Jan 16 2017 Kalev Lember <klember@redhat.com> 0.6.7-2
- Fix epiphany showing up twice in gnome-software

* Thu Jan 12 2017 Richard Hughes <richard@hughsie.com> 0.6.7-1
- New upstream release
- Add AsRequire as a way to store runtime requirements
- Add support for "+" at the end of SPDX license identifiers
- Allow loading application XPM icons
- Fix a crash when using as_release_get_location_default()
- Fix dep extraction when multiple versions are available
- Only fail to validate <icon> in AppData desktop components
- Scan /usr/share/metainfo as well when building appstream-data
- Update the SPDX licence list to v2.5

* Thu Dec 15 2016 Richard Hughes <richard@hughsie.com> 0.6.6-1
- New upstream release
- Add Geary to the app id fallbacks
- Deduplicate the AsNode attribute key and value using a hash table
- Detect invalid files in the libyaml read handler
- Do not absorb core addons into the main application
- Do not add <kudos>, <languages>, <provides> or <releases> for addons
- Do not save the attributes if the node or parent node is ignored
- Set a better icon for codecs

* Mon Nov 07 2016 Richard Hughes <richard@hughsie.com> 0.6.5-1
- New upstream release
- Add app-removed, app-added and app-changed signals to AsStore
- Add a 'watch' command to appstream-util
- Allow only loading native languages when parsing AppStream
- Allow the client to control what search fields are indexed
- Always copy the state when replacing AppData with AppStream
- Do not sent a REMOVED signal when deleting a transient temp file
- Ensure the component scope is set when loading yaml files
- Handle files being moved into monitored AppStream directories
- Load the search token blacklist into a hash table
- Monitor missing AppStream directories
- Only transliterate when the locale requires it
- Process file changes when an attribute changes

* Wed Oct 12 2016 Richard Hughes <richard@hughsie.com> 0.6.4-1
- New upstream release
- Add more API used by gnome-software master branch
- Add support for AppImage bundles
- Don't show a critical warning on invalid yaml file
- Fix a small memory leak when parsing yaml files
- Fix building metadata on repos with mixed architecture content
- Fix setting the origin for Flatpak user repos
- Fix the CSM rating age calculation
- Never inhierit Name and Comment when using appstream-compose

* Tue Sep 06 2016 Richard Hughes <richard@hughsie.com> 0.6.3-1
- New upstream release
- Add a component kind of 'driver'
- Add an easy way to add a language to an existing file
- Add an easy way to add a modalias to an existing file
- Support components with merge=replace rules

* Mon Aug 29 2016 Richard Hughes <richard@hughsie.com> 0.6.2-1
- New upstream release
- Add API for gnome-software
- Do not merge all LangPack entries
- Do not require an icon from LOCALIZATION kind
- Do not use the prefix check when parsing YAML
- Ignore system datadirs that are actually per-user
- Invalidate the unique-id if any of the parts are changed
- Make upgrade check for SPDX license string
- Pay attention to errors from libyaml

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> 0.6.1-2
- Fix gcc shift warnings on 32 bit platforms

* Fri Aug 12 2016 Richard Hughes <richard@hughsie.com> 0.6.1-1
- New upstream release
- Add new API for latest AppStream specification level
- Add some more validation checks for keywords
- Add support for AppStream merge components
- Add support for Google .PAK files
- Allow multiple components with the same ID in the AsStore
- Convert all current component-type names
- Do not save the 'X-' prefixed keys to the AppStream metadata
- Ensure predictable output order of XML attributes
- Port away from intltool
- Remove specific support for flatpak
- Restrict addons to the same scope and bundle kind

* Wed Aug 10 2016 Richard Hughes <richard@hughsie.com> 0.5.18-1
- New upstream release
- Add Sugar as a valid desktop environment
- Add the translate URL kind
- Do not split up the main AudioVideo category
- Don't redundantly monitor files
- No validation failure for lots of releases

* Wed Jul 13 2016 Richard Hughes <richard@hughsie.com> 0.5.17-1
- New upstream release
- Add external (X-*) keys of an app's desktop file as metadata AsApp
- Correct disabling of timestamps for gzip
- Do not add multiple categories for apps with AudioVideo
- Do not emit a warning when flatpak user directory doesn't exist
- Fall back to the country code in as_app_get_language()
- Use libstemmer for keyword stemming

* Fri Jul 01 2016 Kalev Lember <klember@redhat.com> 0.5.16-2
- Set minimum required versions for dependencies

* Mon Jun 13 2016 Richard Hughes <richard@hughsie.com> 0.5.16-1
- New upstream release
- Add elementary to list of project groups
- Allow setting the id prefix and origin using a symlink name
- Correctly detect new AppStream apps in new directories
- Do not rename a category ID in AsApp
- Load metainfo files if present
- Never allow NULL to be added to AsApp string array

* Mon May 23 2016 Richard Hughes <richard@hughsie.com> 0.5.15-1
- New upstream release
- Add all applications for all architectures when loading Flatpak apps
- Add new API for gnome-software
- Ignore files with invalid suffixes when building installed stores
- Omit timestamp from gzip compressed files
- Rename the xdg-app support to the new name: Flatpak
- Sort archive contents by name for repeatable results

* Wed Apr 20 2016 Richard Hughes <richard@hughsie.com> 0.5.14-1
- New upstream release
- Add new API for gnome-software 3.21
- Add search-pkgname to appstream-cmd
- Fall back to searching in as_store_get_app_by_pkgname()
- Ignore desktop files with X-AppStream-Ignore
- Search /usr/share/metainfo for local files

* Fri Apr 01 2016 Richard Hughes <richard@hughsie.com> 0.5.13-1
- New upstream release
- Enforce the requirement of AppData for 'Categories=DesktopSettings'
- Also filter YAML apps before adding to the store
- Always veto anything with X-Unity-Settings-Panel
- Do not hardcode x86_64 when searching for xdg-app metadata
- Support more DEP11 YAML markup

* Tue Mar 29 2016 Richard Hughes <richard@hughsie.com> 0.5.12-1
- New upstream release
- Add a merge-appstream command to appstream-util
- Add new API required for GNOME Software
- Add support for content ratings
- Split up AudioVideo into two categories

* Mon Mar 14 2016 Richard Hughes <rhughes@redhat.com> - 0.5.11-2
- Rebuild to fix NVRs

* Tue Mar 08 2016 Richard Hughes <richard@hughsie.com> 0.5.11-1
- New upstream release
- Add new API for gnome-software
- Fix token splitting for searching

* Fri Feb 26 2016 Richard Hughes <richard@hughsie.com> 0.5.10-1
- New upstream release
- Add an application prefix to the ID for certain install scopes
- Add a 'split-appstream' command to appstream-util
- Add support for getting the SDK and runtime from the bundle
- Improve the application search tokenizing and filtering
- Load AppStream stores in a predictable order

* Fri Feb 12 2016 Richard Hughes <richard@hughsie.com> 0.5.9-1
- New upstream release
- Accept FSFAP as a valid metadata license
- Fix a validation error for metainfo files with descriptions
- Pick up newly added appinfo dirs for xdg-app remotes
- Update the SPDX license list

* Tue Feb 02 2016 Richard Hughes <richard@hughsie.com> 0.5.8-1
- New upstream release
- Add a modify command to appstream-util
- Add support for per-user and system-wide xdg-app installed stores
- Reject an invalid project group when parsing
- Support multi-line copyright statements
- Support the QT translation system
- Support <translation> tags in AppData files

* Fri Jan 15 2016 Richard Hughes <richard@hughsie.com> 0.5.6-1
- New upstream release
- Accept various 'or later' metadata content licenses
- Check the project_group when validating
- Cull the application blacklist now we depend on AppData files
- Fix things up for xdg-app use
- Install gettext ITS rules

* Wed Dec 16 2015 Richard Hughes <richard@hughsie.com> 0.5.5-1
- New upstream release
- Add as_utils_license_to_spdx()
- Add the package name as another application search token
- Fix a crash when tokenizing a NULL string
- Log when we auto-add kudos or keywords
- Support live updates

* Wed Nov 18 2015 Richard Hughes <richard@hughsie.com> 0.5.4-1
- New upstream release
- Add as_utils_version_from_uint16()
- Generate GUID values according to RFC4122

* Thu Nov 05 2015 Richard Hughes <richard@hughsie.com> 0.5.3-1
- New upstream release
- Return the correct error when the desktop file has no group
- Strip Win32 and Linux paths when decompressing firmware

* Tue Oct 27 2015 Richard Hughes <richard@hughsie.com> 0.5.2-1
- New upstream release
- Accept a '0x' hexidecimal prefix when parsing a version
- Add multi-guid cabinet firmware support
- Add support for AppStream <size> metadata
- Fix crash in validator when processing '<li></li>'
- Remove the long-obsolete appdata-validate tool
- Require AppData files to be present in the AppStream metadata
- Use g_set_object() to fix potential crash when adding pixbufs

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> 0.5.1-2
- Backport a patch to fix icons in gnome-software for apps without AppData
- Use license macro for COPYING

* Tue Sep 15 2015 Richard Hughes <richard@hughsie.com> 0.5.1-1
- New upstream release
- Add a few applications that have changed desktop ID
- Add support for release urgency
- Do not blacklist the 'desktop' token
- Don't show mangled version numbers as negatives
- Ignore empty AppStream XML files
- Support SPDX IDs with the LicenseRef prefix

* Sat Sep 05 2015 Kalev Lember <klember@redhat.com> - 0.5.0-2
- Rebuilt for librpm soname bump

* Wed Aug 12 2015 Richard Hughes <richard@hughsie.com> 0.5.0-1
- New upstream release
- Add support for the flashed firmware provide kind
- Make the DriverVer in the .inf file optional
- Show a better error message when there's not enough text

* Wed Jul 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.4.1-2
- Rebuilt for rpm 4.12.90

* Mon Jul 20 2015 Richard Hughes <richard@hughsie.com> 0.4.1-1
- New upstream release
- Add am 'incorporate' command to appstream-util
- Add a 'mirror-local-firmware' and 'compare' commands to appstream-util
- Add extra flags for use when building metadata
- Be less strict when loading incorrect AppData files
- Do not duplicate <location> tags within a release
- Do not expect the INF ClassGuid to be the ESRT GUID
- Don't crash when parsing a <release> with no description
- Update the SPDX licence list to v2.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Richard Hughes <richard@hughsie.com> 0.4.0-1
- New upstream release
- Add a mirror-screenshots command to appstream-util
- Check for duplicate screenshots when adding fonts
- Detect recolorable symbolic icons
- Fix a crash for an invalid AppData file
- Remove all networking support when building metadata
- Remove overzealous blacklisting entry

* Wed Apr 29 2015 Kalev Lember <kalevlember@gmail.com> 0.3.6-2
- Fix exo-web-browser blacklist entry (#1216218)

* Mon Mar 30 2015 Richard Hughes <richard@hughsie.com> 0.3.6-1
- New upstream release
- Add a 'replace-screenshots' command to appstream-util
- Always upscale screenshots if they are too small
- Assume the INF DriverVer is UTC
- Remove the gtk3 dep from libappstream-glib
- Use the correct image URL for HiDPI screenshots

* Wed Mar 11 2015 Richard Hughes <richard@hughsie.com> 0.3.5-1
- New upstream release
- Add new API required for firmware support
- Add new API required for OSTree and xdg-app support

* Sat Jan 17 2015 Richard Hughes <richard@hughsie.com> 0.3.4-1
- New upstream release
- Add more applications to the blacklist
- Add show-search-tokens subcommand to appstream-util
- Add some new API for gnome-software to use
- Add the matrix-html subcommand to appstream-util
- Add the VCS information to the AppStream metadata
- Assume <image>foo</image> is a source image kind for AppData files
- Assume that stock icons are available in HiDPI sizes
- Blacklist the 40 most common search tokens
- Check if the search entries are valid before searching
- Check screenshots are a reasonable size
- Fall back to the dumb tokenizer for keywords with special chars
- Set an error if an XML file contains font markup
- Show the offending text when validation fails

* Mon Nov 24 2014 Richard Hughes <richard@hughsie.com> 0.3.3-1
- New upstream release
- Allow filtering addons in the status html pages
- Detect missing parents in the old metadata
- Do not fail to load all the desktop files if one is bad
- Improve appdata-xml.m4 deprecation notice

* Tue Nov 04 2014 Richard Hughes <richard@hughsie.com> 0.3.2-1
- New upstream release
- Add a simple 'search' command to appstream-util
- Add some more valid metadata licenses
- Do not generate metadata with an icon prefix
- Obsolete the appdata-tools package
- Show the kudo stats on the status page

* Tue Oct 21 2014 Richard Hughes <richard@hughsie.com> 0.3.1-1
- New upstream release
- Add an --enable-hidpi argument to appstream-builder
- Add AS_ICON_KIND_EMBEDDED and AS_ICON_KIND_LOCAL
- Add more applications to the blacklist
- Allow application with NoDisplay=true and an AppData file
- Allow AppStream files to be upgraded using appstream-util
- Install AppStream files with correct permissions
- Monitor the XML and icons path for changes
- Relax validation requirements for font metainfo files

* Mon Sep 01 2014 Richard Hughes <richard@hughsie.com> 0.3.0-1
- New upstream release
- Add a new kudo for high contrast icons
- A keyword search match is better than the project name
- Allow desktop->addon demotion with an AppData file
- Allow translated keywords
- Conform to the actual SPDX 2.0 license expression syntax
- Ignore AppData screenshots with xml:lang attributes
- Metadata licenses like 'CC0 and CC-BY-3.0' are content licenses
- Update the SPDX license list to v1.20

* Mon Aug 18 2014 Richard Hughes <richard@hughsie.com> 0.2.5-1
- New upstream release
- Add check-root to appstream-util
- Add some validation rules for metainfo files
- Allow desktop->addon demotion with an AppData file
- Allow different source roots to define addons
- Do not require sentence case when validating with relaxed settings
- Fix up legacy license IDs when tokenizing
- Metadata licenses like 'CC0 and CC-BY-3.0' are valid content licenses
- Never add duplicate <extends> tags

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Richard Hughes <richard@hughsie.com> 0.2.4-1
- New upstream release
- Add an installed tests to validate appdata
- Add support for <source_pkgname> which will be in AppStream 0.8
- Add the <dbus> provide for applications automatically
- Do not load applications with NoDisplay=true when loading local
- Do not pad the compressed AppStream metadata with NUL bytes
- Do not treat app-install metadata as installed
- Markup errors should not be fatal when assembling a store

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.3-2
- Rebuilt for gobject-introspection 1.41.4

* Thu Jul 17 2014 Richard Hughes <richard@hughsie.com> 0.2.3-1
- New upstream release
- Add oxygen-icon-theme when an application depends on kde-runtime
- Add some simple filtering in the status.html page
- Be more careful with untrusted XML data
- Do not allow duplicates to be added when using as_app_add_kudo_kind()
- Do not fail to build packages with invalid KDE service files
- Record if distro metadata and screenshots are being used
- Show any package duplicates when generating metadata
- Show the builder progress in a ncurses-style panel

* Fri Jul 11 2014 Richard Hughes <richard@hughsie.com> 0.2.2-1
- New upstream release
- Add two new builder plugins to add kudos on KDE applications
- Assume local files are untrusted when parsing
- Do not allow NoDisplay=true applications to ever be in the metadata
- Never scale up small screenshots
- Never upscale icons, either pad or downscale with sharpening
- Sharpen resized screenshots after resizing with a cubic interpolation
- Write metadata of the failed applications

* Tue Jun 24 2014 Richard Hughes <richard@hughsie.com> 0.2.1-1
- New upstream release
- Add an 'appstream-util upgrade' command to convert version < 0.6 metadata
- Add packages recursively when using appstream-builder --packages-dir
- Allow empty URL sections
- Fix the xmldir in the APPSTREAM_XML_RULES m4 helper

* Thu Jun 19 2014 Richard Hughes <richard@hughsie.com> 0.2.0-1
- New upstream release
- Accept slightly truncated SPDX IDs
- Allow any SPDX license when validating in relaxed mode
- Allow as_node_get_attribute_as_int() to parse negative numbers
- Allow dumping .desktop, .appdata.xml and .metainfo.xml files in appstream-util
- Do not add addons that are packaged in the parent package
- Do not require a content license to be included into the metadata
- This is the first release that merges the createrepo_as project.
- Validate the <developer_name> tag values

* Thu Jun 12 2014 Richard Hughes <richard@hughsie.com> 0.1.7-1
- New upstream release
- Add <extends> from the draft AppStream 0.7 specification
- Add support for the 'dbus' AsProvideKind
- Add support for validating metainfo.xml files
- Allow 'appstream-util validate' to validate multiple files
- Do not log a critical warning in as_store_to_xml()
- Fix a crash when we try to validate <p></p>
- Support the non-standard X-Ubuntu-Software-Center-Name

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Richard Hughes <richard@hughsie.com> 0.1.6-1
- New upstream release
- Add some more API for createrepo_as and gnome-software
- Also support validating .appdata.xml.in files
- Correctly parse the localized descriptions from AppData files
- Fix validation of old-style AppData files without screenshot sizes
- Only autodetect the AsAppSourceKind when unknown
- Only require <project_licence> when being strict
- Only show the thumbnail when creating the HTML status page
- Retain comments in .desktop and .appdata.xml files when required

* Mon May 12 2014 Richard Hughes <richard@hughsie.com> 0.1.5-1
- New upstream release
- Add some more API for createrepo_as and gnome-software
- Be less strict with the case of the XML header
- Check the licenses against the SPDX list when validating
- Support AppData version 0.6 files too

* Fri Apr 25 2014 Richard Hughes <richard@hughsie.com> 0.1.4-1
- New upstream release
- Add some more API for createrepo_as and gnome-software
- Add tool appstream-util

* Thu Apr 10 2014 Richard Hughes <richard@hughsie.com> 0.1.3-1
- New upstream release
- Add new API required by gnome-software
- Ignore settings panels when parsing desktop files
- Load AppStream files assuming literal text strings

* Wed Mar 26 2014 Richard Hughes <richard@hughsie.com> 0.1.2-1
- New upstream release
- Add more API for gnome-software to use
- Reduce the number of small attr key allocations
- Use gperf to generate a perfect hash for the tag names
- Use the full ID for the AsStore hash

* Fri Mar 21 2014 Richard Hughes <richard@hughsie.com> 0.1.1-1
- New upstream release
- Add an 'api-version' property to AsStore
- Add the new AsUrlKind's and <architectures> from API 0.6
- Support old-style markup-less <description> tags
- Support the 'origin' attribute on the root node
- Do not crash when using getting an unset description
- Do not depend on functions introduced in Glib 2.39.1
- Fix parsing incompletely translated AppData files

* Tue Mar 18 2014 Richard Hughes <richard@hughsie.com> 0.1.0-1
- First upstream release
