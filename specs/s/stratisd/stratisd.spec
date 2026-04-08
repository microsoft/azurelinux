## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without check

%global udevdir %(pkg-config --variable=udevdir udev)
%global dracutdir %(pkg-config --variable=dracutdir dracut)

Name:           stratisd
Version:        3.8.6
Release:        %autorelease
Summary:        Daemon that manages block devices to create filesystems

License:        (MIT OR Apache-2.0) AND Unicode-DFS-2016 AND Apache-2.0 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND MIT AND MPL-2.0 AND (Unlicense OR MIT)
URL:            https://github.com/stratis-storage/stratisd
Source0:        %{url}/archive/stratisd-v%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/stratisd-v%{version}/%{name}-%{version}-vendor.tar.gz

# * Allow procfs 0.18: https://github.com/stratis-storage/stratisd/pull/3951
Patch:          stratisd-fix-metadata.diff

ExclusiveArch:  %{rust_arches}
%if 0%{?rhel}
ExcludeArch:    i686
%endif

%if 0%{?rhel}
BuildRequires:  rust-toolset
%else
BuildRequires:  rust-packaging
%endif
BuildRequires:  rust-srpm-macros
BuildRequires:  systemd-devel
BuildRequires:  dbus-devel
BuildRequires:  libblkid-devel
BuildRequires:  cryptsetup-devel
BuildRequires:  clang
BuildRequires:  glibc-static
BuildRequires:  device-mapper-devel
BuildRequires:  %{_bindir}/a2x

# Required to calculate install directories
BuildRequires:  systemd
BuildRequires:  dracut

Requires:       xfsprogs
Requires:       device-mapper-persistent-data
Requires:       systemd-libs
Requires:       dbus-libs
Requires:       cryptsetup-libs
Requires:       libblkid

# stratisd does not require clevis; it can be used in restricted environments
# where clevis is not available.
# If using encryption via clevis, stratisd requires the instance of clevis
# that it uses to have been built in an environment with cryptsetup >= 2.6.0.
Recommends:     clevis-luks >= 18

%description
%{summary}.

%package dracut
Summary: Dracut modules for use with stratisd

ExclusiveArch:  %{rust_arches}
%if 0%{?rhel}
ExcludeArch:    i686
%endif

Requires:     stratisd
Requires:     dracut >= 051
Requires:     systemd

%description dracut
%{summary}.

%package tools
Summary: Tools that support Stratis operation

ExclusiveArch:  %{rust_arches}
%if 0%{?rhel}
ExcludeArch:    i686
%endif

Requires:     stratisd

%description tools
%{summary}.

%prep
%autosetup -n stratisd-stratisd-v%{version} -p1 %{?rhel:-a1}

%if 0%{?rhel}
%cargo_prep -v vendor
%else
%cargo_prep
%generate_buildrequires
%cargo_generate_buildrequires -f engine,dbus_enabled,min,systemd_compat,extras,udev_scripts
%endif

%build
%{cargo_license -f engine,dbus_enabled,min,systemd_compat,extras,udev_scripts} > LICENSE.dependencies
%{__cargo} build %{?__cargo_common_opts} --release --bin=stratisd
%{__cargo} build %{?__cargo_common_opts} --release --bin=stratis-min --bin=stratisd-min --bin=stratis-utils --no-default-features --features engine,min,systemd_compat
%{__cargo} rustc %{?__cargo_common_opts} --release --bin=stratis-str-cmp --no-default-features --features udev_scripts -- -Ctarget-feature=+crt-static
%{__cargo} rustc %{?__cargo_common_opts} --release --bin=stratis-base32-decode --no-default-features --features udev_scripts -- -Ctarget-feature=+crt-static
%{__cargo} build %{?__cargo_common_opts} --release --bin=stratisd-tools --no-default-features --features engine,extras
a2x -f manpage docs/stratisd.txt
a2x -f manpage docs/stratis-dumpmetadata.txt
%{cargo_vendor_manifest}

%install
%make_install DRACUTDIR=%{dracutdir} PROFILEDIR=release

%if %{with check}
%check
%cargo_test -- --no-run
%endif

%post
%systemd_post stratisd.service

%preun
%systemd_preun stratisd.service

%postun
%systemd_postun_with_restart stratisd.service

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_libexecdir}/stratisd
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/system.d
%{_datadir}/dbus-1/system.d/stratisd.conf
%{_mandir}/man8/stratisd.8*
%{_unitdir}/stratisd.service
%{_udevrulesdir}/61-stratisd.rules
%{udevdir}/stratis-str-cmp
%{udevdir}/stratis-base32-decode
%{_bindir}/stratis-predict-usage
%{_unitdir}/stratisd-min-postinitrd.service
%{_unitdir}/stratis-fstab-setup@.service
%{_unitdir}/stratis-fstab-setup-with-network@.service
%{_bindir}/stratis-min
%{_libexecdir}/stratisd-min
%{_bindir}/stratis-decode-dm
%{_systemd_util_dir}/stratis-fstab-setup


%files dracut
%license LICENSE
%{dracutdir}/modules.d/50stratis-clevis/module-setup.sh
%{dracutdir}/modules.d/50stratis-clevis/stratis-clevis-rootfs-setup
%{dracutdir}/modules.d/50stratis/61-stratisd.rules
%{dracutdir}/modules.d/50stratis/module-setup.sh
%{dracutdir}/modules.d/50stratis/stratis-rootfs-setup
%{dracutdir}/modules.d/50stratis/stratisd-min.service
%{_systemd_util_dir}/system-generators/stratis-clevis-setup-generator
%{_systemd_util_dir}/system-generators/stratis-setup-generator

%files tools
%license LICENSE
%{_bindir}/stratisd-tools
%{_bindir}/stratis-dumpmetadata
%{_mandir}/man8/stratis-dumpmetadata.8*

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 3.8.6-3
- Latest state for stratisd

* Mon Jan 05 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 3.8.6-2
- Allow procfs 0.18

* Tue Nov 18 2025 mulhern <amulhern@redhat.com> - 3.8.6-1
- Update to version 3.8.6

* Tue Sep 16 2025 Chung Chung <cchung@redhat.com> - 3.8.5-1
- Update to version 3.8.5

* Fri Aug 29 2025 Chung Chung <cchung@redhat.com> - 3.8.4-1
- Update to version 3.8.4

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 27 2025 mulhern <amulhern@redhat.com> - 3.8.2-2
- Require testing version 3.8.1

* Fri Jun 27 2025 mulhern <amulhern@redhat.com> - 3.8.2-1
- Update to version 3.8.2

* Thu Mar 13 2025 Chung Chung <cchung@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 18 2024 Bryan Gurney <bgurney@redhat.com> - 3.7.3-1
- Update to 3.7.3

* Tue Oct 15 2024 Bryan Gurney <bgurney@redhat.com> - 3.7.2-1
- Update to 3.7.2

* Tue Oct 08 2024 Bryan Gurney <bgurney@redhat.com> - 3.7.1-1
- Update to 3.7.1

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Bryan Gurney <bgurney@redhat.com> - 3.6.8-1
- Update to 3.6.8

* Sun May 12 2024 mulhern <amulhern@redhat.com> - 3.6.7-2
- Add a generic gating.yaml file

* Thu Apr 04 2024 Bryan Gurney <bgurney@redhat.com> - 3.6.7-1
- Update to 3.6.7

* Tue Mar 26 2024 Bryan Gurney <bgurney@redhat.com> - 3.6.6-1
- Update to 3.6.6

* Thu Feb 15 2024 Bryan Gurney <bgurney@redhat.com> - 3.6.5-2
- Rebuild after mass branch

* Tue Feb 13 2024 Bryan Gurney <bgurney@redhat.com> - 3.6.5-1
- Update to 3.6.5

* Thu Jan 25 2024 Bryan Gurney <bgurney@redhat.com> - 3.6.4-1
- Update to 3.6.4

* Thu Nov 30 2023 Bryan Gurney <bgurney@redhat.com> - 3.6.3-1
- Update to 3.6.3

* Thu Nov 16 2023 Bryan Gurney <bgurney@redhat.com> - 3.6.2-1
- Update to 3.6.2

* Tue Oct 31 2023 Bryan Gurney <bgurney@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Wed Oct 25 2023 Bryan Gurney <bgurney@redhat.com> - 3.6.0-2
- Use testing tag v3.6.0

* Tue Oct 24 2023 Bryan Gurney <bgurney@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Aug 30 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.9-2
- Use testing tag v3.5.3
- Remove vendor-serde_derive.patch file

* Wed Aug 30 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.9-1
- Update to 3.5.9
- Remove patch macro for serde_derive patch

* Mon Jul 31 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.8-4
- Use patch macro for serde_derive patch

* Fri Jul 28 2023 mulhern <amulhern@redhat.com> - 3.5.8-3
- Patch vendored tarfile to remove executable

* Thu Jul 27 2023 mulhern <amulhern@redhat.com> - 3.5.8-2
- Add additional dependency for TMT tests

* Thu Jul 27 2023 mulhern <amulhern@redhat.com> - 3.5.8-1
- Update to 3.5.8

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.7-2
- Use tmt tests

* Wed Jun 07 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.7-1
- Update to 3.5.7

* Wed May 31 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.5-2
- Rebuild for new libcryptsetup-rs version

* Wed May 17 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Wed Apr 26 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.4-3
- Fix up ExclusiveArch directives

* Mon Apr 24 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.4-2
- Update spec file

* Fri Apr 21 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.4-1
- Update to 3.5.4

* Mon Apr 17 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.3-1
- Update to 3.5.3

* Fri Mar 17 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.2-2
- Add BuildRequires for device-mapper-devel

* Fri Mar 17 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.2-1
- Update to 3.5.2

* Tue Feb 28 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.1-3
- Allow annocheck on rpminspect.yaml for non-static binaries

* Mon Feb 20 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.1-2
- Add debuginfo ignore to rpminspect.yaml

* Tue Feb 07 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.1-1
- Update to 3.5.1

* Fri Feb 03 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.0-4
- Remove debuginfo ignore from rpminspect.yaml

* Thu Feb 02 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.0-3
- Remove elf ignore from rpminspect.yaml

* Wed Feb 01 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.0-2
- Update rpminspect.yaml

* Tue Jan 24 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.0-1
- Update to 3.5.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Bryan Gurney <bgurney@redhat.com> - 3.4.4-2
- Remove Fedora ELN conditionals from spec file
- Use ExclusiveArch only if RHEL

* Tue Jan 03 2023 Bryan Gurney <bgurney@redhat.com> - 3.4.4-1
- Update to 3.4.4

* Thu Dec 15 2022 Bryan Gurney <bgurney@redhat.com> - 3.4.3-1
- Update to 3.4.3

* Tue Dec 06 2022 Bryan Gurney <bgurney@redhat.com> - 3.4.2-1
- Update to 3.4.2

* Tue Nov 29 2022 Bryan Gurney <bgurney@redhat.com> - 3.4.1-1
- Update to 3.4.1

* Tue Oct 18 2022 Bryan Gurney <bgurney@redhat.com> - 3.3.0-1
- Update to 3.3.0

* Sun Aug 28 2022 mulhern <amulhern@redhat.com> - 3.2.3-1
- Update to 3.2.3

* Wed Aug 24 2022 Bryan Gurney <bgurney@redhat.com> - 3.2.2-1
- Update to 3.2.2

* Fri Jul 29 2022 mulhern <amulhern@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Wed Jul 27 2022 mulhern <amulhern@redhat.com> - 3.1.2-2
- Run all gating tests that require no devices

* Wed Jul 27 2022 mulhern <amulhern@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Bryan Gurney <bgurney@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Fri Jul 01 2022 Bryan Gurney <bgurney@redhat.com> - 3.1.0-5
- Refine gating tests to minimal set

* Wed Jun 22 2022 Bryan Gurney <bgurney@redhat.com> - 3.1.0-4
- Add gating test

* Mon Jun 06 2022 Bryan Gurney <bgurney@redhat.com> - 3.1.0-3
- Remove buildhost_subdomain section from rpminspect.yaml

* Fri Jun 03 2022 Bryan Gurney <bgurney@redhat.com> - 3.1.0-2
- Synchronize spec with upstream unified spec file
- Remove .rust2rpm.conf file

* Wed May 25 2022 mulhern <amulhern@redhat.com> - 3.1.0-1
- Update to 3.1.0

* Mon Mar 28 2022 mulhern <amulhern@redhat.com> - 3.0.4-11
- Fix ${rust_arches}; use long form tar options

* Sat Mar 26 2022 mulhern <amulhern@redhat.com> - 3.0.4-10
- Fix cryptsetup-Requires; add blkid-Requires

* Fri Mar 25 2022 mulhern <amulhern@redhat.com> - 3.0.4-9
- Make specfile fully and minimally unified

* Thu Mar 24 2022 mulhern <amulhern@redhat.com> - 3.0.4-8
- Tidy up BuildRequires

* Thu Mar 24 2022 mulhern <amulhern@redhat.com> - 3.0.4-7
- Remove __cargo_skip_build

* Thu Mar 24 2022 mulhern <amulhern@redhat.com> - 3.0.4-6
- Only build the tests, do not try to run them

* Thu Mar 24 2022 mulhern <amulhern@redhat.com> - 3.0.4-5
- Do not set unused global

* Tue Mar 15 2022 mulhern <amulhern@redhat.com> - 3.0.4-4
- Install two scripts

* Mon Mar 14 2022 mulhern <amulhern@redhat.com> - 3.0.4-3
- Fix the previous revision

* Mon Mar 14 2022 mulhern <amulhern@redhat.com> - 3.0.4-2
- Use upstream crate for Rust source

* Sat Feb 12 2022 mulhern <amulhern@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Mon Feb 7 2022 mulhern <amulhern@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 mulhern <amulhern@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Sun Nov 28 2021 mulhern <amulhern@redhat.com> - 2.4.4-1
- Update to 2.4.4

* Tue Oct 19 2021 mulhern <amulhern@redhat.com> - 2.4.2-3
- Rebuilt to include dbus-tree 0.9.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 1 2021 mulhern <amulhern@redhat.com> - 2.4.2-1
- Update to 2.4.2

* Tue May 18 2021 John Baublitz <jbaublitz@redhat.com> - 2.4.1-1
- Update to new release and split dracut modules out into subpackage

* Thu May 13 2021 John Baublitz <jbaublitz@redhat.com> - 2.4.0-4
- Ensure that binaries are installed with proper features enabled

* Wed May 12 2021 John Baublitz <jbaublitz@redhat.com> - 2.4.0-3
- Fix installed file paths

* Tue Apr 27 2021 mulhern <amulhern@redhat.com> - 2.4.0-2
- Fixes to previous release

* Tue Apr 27 2021 mulhern <amulhern@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Wed Mar 17 2021 mulhern <amulhern@redhat.com> - 2.3.0-10
- Use external URL for vendored sources

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.3.0-9
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.3.0-7
- Fix build on ELN

* Fri Jan 15 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.3.0-6
- Make package compatible without violating guidelines

* Fri Jan 15 2021 mulhern <amulhern@redhat.com> - 2.3.0-5
- Add both sources at the same time

* Fri Jan 15 2021 mulhern <amulhern@redhat.com> - 2.3.0-4
- Restore RHEL/Fedora compatible spec file, adding some additional changes

* Fri Jan 15 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.3.0-3
- Partially revert previous commit

* Thu Jan 14 2021 mulhern <amulhern@redhat.com> - 2.3.0-2
- Make RHEL/Fedora compatible spec file

* Tue Jan 12 2021 mulhern <amulhern@redhat.com> - 2.3.0-1
- Update to 2.3.0

* Mon Dec 28 13:34:26 CET 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.2.1-3
- Rebuild

* Sun Dec 27 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.2.1-2
- Rebuild

* Mon Nov 9 2020 mulhern <amulhern@redhat.com> - 2.2.1-1
- Update to 2.2.1

* Mon Oct 19 2020 mulhern <amulhern@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 John Baublitz <jbaublitz@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Wed Feb 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.0.1-2
- Fixup license

* Wed Feb 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Fri Sep 06 20:52:06 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Josh Stone <jistone@redhat.com> - 1.0.4-2
- Bump nix to 0.14

* Tue May 07 08:16:24 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Mar 06 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Wed Dec 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Fri Nov 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Thu Sep 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0

* Wed Sep 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-4
- Add missing systemd scriptlets

* Wed Sep 19 2018 Tony Asleson <tasleson@redhat.com> - 0.9.0-3
- Add systemd unit file
- Remove systemd activation file

* Tue Sep 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-2
- Rebuild to workaround pungi bug

* Sat Sep 01 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Fri Aug 3 2018 Andy Grover <agrover@redhat.com> - 0.5.5-2
- Disable a failing but noncritical test

* Fri Aug 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.5-1
- Update to 0.5.5

* Thu Jul 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.4-3
- Upgrade dependencies

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.4-1
- Update to 0.5.4

* Fri Jun 22 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.3-2
- Add -init version of daemon
- Own dbus-1 directory

* Mon Jun 4 2018 Andy Grover <agrover@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Fri May 4 2018 Andy Grover <agrover@redhat.com> - 0.5.2-2
- Add 0002-Prefix-commands-with-entire-path.patch

* Tue May 1 2018 Andy Grover <agrover@redhat.com> - 0.5.2-1
- Update to 0.5.2

* Tue Apr 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1

* Tue Mar 13 2018 Andy Grover <agrover@redhat.com> - 0.5.0-2
- Add stratisd manpage

* Thu Mar 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Thu Feb 15 2018 Andy Grover <agrover@redhat.com> - 0.1.5-2
- Require packages that contain binaries that we exec: xfsprogs and
  device-mapper-persistent-data

* Sun Feb 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.5-1
- Update to 0.1.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.4-3
- Rebuild for rust-packaging v5

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.4-2
- Move binary under %%{_libexecdir}
- Add dbus service (so it is activatable)
- Fix rand's version bump

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.4-1
- Initial package

## END: Generated by rpmautospec
