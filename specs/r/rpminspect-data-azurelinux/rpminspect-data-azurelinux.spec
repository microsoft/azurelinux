# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: rpminspect-data-azurelinux
Version:        1.16
Release: 5%{?dist}
Epoch:          1
Summary:        Build deviation compliance tool data files
Group:          Development/Tools
License:        CC-BY-SA-4.0
URL:            https://github.com/rpminspect/rpminspect-data-fedora
Source0: %{url}/releases/download/v%{version}/rpminspect-data-fedora-%{version}.tar.gz
Source1: %{url}/releases/download/v%{version}/rpminspect-data-fedora-%{version}.tar.gz.asc
Source2:        gpgkey-62977BB9C841B965.gpg

BuildArch:      noarch

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  gnupg2

Requires:       rpminspect >= 2.0

# Used by inspections enabled in the configuration file
Requires:       xhtml1-dtds
Requires:       dash
Requires:       ksh
Requires:       zsh
Requires:       tcsh
Requires:       bash
Requires:       libabigail
Requires:       /usr/bin/annocheck


Requires: rpminspect-data-generic >= 2.1
Requires: clamav-data
Patch0: 0001-add-fileinfo.patch
Patch1: 0002-add-capabilities.patch
Patch2: 0003-install-azurelinux-yaml.patch
Patch3: 0004-azurelinux-deltas.patch
%description
Fedora Linux specific configuration file for rpminspect and data files
used by the inspections provided by librpminspect.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n rpminspect-data-fedora-%{version} -p1 -N
%autopatch -q -p1 -M2

# Derive azurelinux.yaml from Fedora's own fedora.yaml instead of patching
# in a frozen copy, so upstream policy fixes are inherited automatically
# whenever this pin is bumped; only the Azure Linux deltas (Patch3) are
# maintained separately.
cp -p fedora.yaml azurelinux.yaml
%patch -P3 -p1


%build
%meson
%meson_build


%install
%meson_install


%files
%license CC-BY-SA-4.0.txt
%doc AUTHORS.md README
%{_datadir}/rpminspect
%{_bindir}/rpminspect-fedora


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 David Cantrell <dcantrell@redhat.com> - 1.16-1
- Upgrade to rpminspect-data-fedora-1.16

* Tue Jan 21 2025 David Cantrell <dcantrell@redhat.com> - 1:1.15-1
- Upgrade to rpminspect-data-fedora-1.15

* Tue Jan 21 2025 David Cantrell <dcantrell@redhat.com> - 1:1.14-1
- Upgrade to rpminspect-data-fedora-1.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 10 2024 David Cantrell <dcantrell@redhat.com> - 1.13-1
- Upgrade to rpminspect-data-fedora-1.13

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 22 2023 David Cantrell <dcantrell@redhat.com> - 1.12-2
- Convert License tag to SPDX expression

* Wed Sep 20 2023 David Cantrell <dcantrell@redhat.com> - 1.12-1
- Upgrade to rpminspect-data-fedora-1.12

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 14 2023 David Cantrell <dcantrell@redhat.com> - 1.10-1
- Upgrade to rpminspect-data-fedora-1.10

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 David Cantrell <dcantrell@redhat.com> - 1.9-1
- Upgrade to rpminspect-data-fedora-1.9

* Mon Feb 21 2022 David Cantrell <dcantrell@redhat.com> - 1.8-1
- Upgrade to rpminspect-data-fedora-1.8

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 David Cantrell <dcantrell@redhat.com> - 1.7-1
- Upgrade to rpminspect-data-fedora-1.7

* Fri Nov 12 2021 David Cantrell <dcantrell@redhat.com> - 1.6-1
- Upgrade to rpminspect-data-fedora-1.6

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 30 2021 David Cantrell <dcantrell@redhat.com> - 1.5-1
- Add a 'rawhide' profile to disable a lot of inspections
- Add missing ID value to the npsl license entry
- /usr/lib/dracut and /usr/lib/udev are valid paths
- Update fedora.yaml with all current configuration file changes
- Explain size_threshold can be 'info'

* Wed Feb 24 2021 David Cantrell <dcantrell@redhat.com> - 1.4-1
- Increment the development tree version to 1.4.
- Document the release process and add another helper target to the
  Makefile
- 'make koji' skips branches that lack Koji build targets
- Set VENDORBLD to the vendor build too in submit-koji-builds.sh
- Add NPSL
- Update fedora.yaml for the new 'badfuncs' inspection.
- The badfuncs inspection is in rpminspect >= 1.3, update spec file
- Add MIT-0 license
- Add runpath section to fedora.yaml

* Wed Feb 24 2021 David Cantrell <dcantrell@redhat.com> - 1.4-1
- Increment the development tree version to 1.4.
- Document the release process and add another helper target to the
  Makefile
- 'make koji' skips branches that lack Koji build targets
- Set VENDORBLD to the vendor build too in submit-koji-builds.sh
- Add NPSL
- Update fedora.yaml for the new 'badfuncs' inspection.
- The badfuncs inspection is in rpminspect >= 1.3, update spec file
- Add MIT-0 license
- Add runpath section to fedora.yaml

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
* Fri Jan 08 2021 David Cantrell <dcantrell@redhat.com> - 1.3-1
- Small change to the way Koji builds are submitted
- Ignore build/ in .gitignore
- Update fedora.yaml from generic.yaml, disable 'patches' inspection
- Eliminate duplicate entries in licenses/fedora.json
- Simplify test() definition in meson.build

* Mon Oct 26 2020 David Cantrell <dcantrell@redhat.com> - 1.2-1
- More fixes for submit-koji-builds.sh
- Increment development work version to 1.2
- Rename '%%files' to 'files'; add 'config' and 'doc' to inspections
- Remove the politics/ subdirectory and the files in it.
- Add 'politics' and 'virus' to the fedora.yaml config file.
- s/DT_NEEDED/dsodeps/g in fedora.yaml
- Require optional packages used by enabled inspections.
- Add excluded_paths block to the pathmigration block
- Adjust the pathmigration block to have 'migrated_paths'
- Update rpminspect-data-fedora.spec.in
- Updates to the 'make koji' process

* Mon Oct 12 2020 David Cantrell <dcantrell@redhat.com> - 1.1-2
- Add explicit Requires for packages needed for inspections (#1887426)

* Fri Sep 11 2020 David Cantrell <dcantrell@redhat.com> - 1.1-1
- Restructure rpminspect-data-fedora so it can coexist with other pkgs
- Update the README
- Add 'types: off' to the list of commented out inspections
- Rename ipv6_blacklist to forbidden_ipv6_blacklist
- Rename stat-whitelist to fileinfo, adjust header comments
- Rename abi-checking-whitelist/ to abi/
- Rename political-whitelist/ to politics/
- Rename version-whitelist/ to rebaseable/
- Change default licensing to CC-BY-SA-4.0
- A few missed files for the license change
- Rollback project version change
- Add abidiff section to fedora.yaml
- Update abidiff and kmidiff blocks in fedora.yaml
- Add kabi_dir and kabi_filename to fedora.yaml, but commented out.
- Add Firmware and Distributable licenses.
- Set minimum JVM bytecode version for Fedora 34 (#9)
- Update the inspections section in fedora.yaml
- Utility script and Copr Makefile updates

* Mon Jun 29 2020 David Cantrell <dcantrell@redhat.com> - 1.0-1
- Use this project's user.name and user.email for Koji builds.
- Add .gitignore
- Convert configuration files to YAML format, bump version to 1.0.
- Update the 'ignore' section in rpminspect.yaml
- Add /usr/bin/vmware-user-suid-wrapper to setxid whitelist
- Split 'make release' in to 'make new-release' and 'make release'

* Mon May 18 2020 David Cantrell <dcantrell@redhat.com> - 0.10-1
- Add F32 to stat-whitelist, fix version names
- Add F33 with Java 11 default bytecode version
- Add [lto] section to rpminspect.conf with lto_symbol_name_prefixes

* Tue Apr 21 2020 David Cantrell <dcantrell@redhat.com> - 0.9-1
- Add the new favor_release setting to rpminspect.conf
- Add commented out [inspections] block in rpminspect.conf
- Simplify the string concatenation in meson.build
- Make compatible with meson 0.47.0
- Sync up rpminspect.conf with the default one.
- Add 'pathmigration' settings to rpminspect.conf
- Add size_threshold=20 to the [settings] section
- Ignore *.xml.in template files.
- Synchronize with official Fedora license list.
- Update the AUTHORS file
- Remove GitHub Release entry stuff from utils/release.sh

* Tue Apr 21 2020 David Cantrell <dcantrell@redhat.com> - 0.9-1
- Add the new favor_release setting to rpminspect.conf
- Add commented out [inspections] block in rpminspect.conf
- Simplify the string concatenation in meson.build
- Make compatible with meson 0.47.0
- Sync up rpminspect.conf with the default one.
- Add 'pathmigration' settings to rpminspect.conf
- Add size_threshold=20 to the [settings] section
- Ignore *.xml.in template files.
- Synchronize with official Fedora license list.
- Update the AUTHORS file
- Remove GitHub Release entry stuff from utils/release.sh

* Fri Feb 14 2020 David Cantrell <dcantrel@redhat.com> - 0.8-1
- Use MESON_BUILD_DIR in the Makefile 'all' target.
- Add runtime profiles and update rpminspect.conf
- specname primary setting; 'basename' -> 'filename'
- Add vendor_data_dir to rpminspect.conf, change licensedb.
- Rename [tests] section in rpminspect.conf to [settings]
- Remove desktop_icon_paths since rpminspect doesn't use it anymore.
- Add fedora_abbrev to Universal Permissive License v1.0 entry
- Change UPL to approved: yes
- Merge pull request #3 from jiekang/patch-1
- Skip the emptyrpm inspection in the 'scl' profile.

* Tue Dec 17 2019 David Cantrell <dcantrel@redhat.com> - 0.7-1
- Add commented out [products] section to rpminspect.conf
- Update product regexps so they being with '.'
- Add [annocheck] section to rpminspect.conf
- Update build files and helper scripts
- Include generated changelog file.
