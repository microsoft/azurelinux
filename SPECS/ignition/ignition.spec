%bcond_with check

%global ignedgecommit a2587490b2a9a215ad12cf15866025efbe027552
%global ignedgeshortcommit %(c=%{ignedgecommit}; echo ${c:0:7})

%global goarch %{_arch}
%ifarch x86_64
%global goarch amd64
%endif
%ifarch aarch64
%global goarch arm64
%endif

%define with_cross  0

%define with_validate  0

%define with_grub  0

# https://github.com/coreos/ignition
%global goipath         github.com/coreos/ignition
%global gomodulesmode   GO111MODULE=on
Version:                2.22.0

%global golicenses      LICENSE
%global godocs          README.md docs/
%global dracutlibdir %{_prefix}/lib/dracut

Name:           ignition
Release:        1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:        First boot installer and configuration tool

# Upstream license specification: Apache-2.0
License:        Apache-2.0
URL:            %{gourl}
Source0:        https://github.com/coreos/ignition/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-sed-s-coreos-flatcar.patch
Patch1:         0002-config-add-ignition-translation.patch
Patch2:         0003-mod-add-flatcar-ignition-0.36.2.patch
Patch3:         0004-sum-go-mod-tidy.patch
Patch4:         0005-vendor-go-mod-vendor.patch
Patch5:         0006-config-v3_6-convert-ignition-2.x-to-3.x.patch
Patch6:         0007-internal-prv-cmdline-backport-flatcar-patch.patch
Patch7:         0008-provider-qemu-apply-fw_cfg-patch.patch
Patch8:         0009-config-3_6-test-add-ignition-2.x-test-cases.patch
Patch9:         0010-internal-disk-fs-ignore-fs-format-mismatches-for-the.patch
Patch10:        0011-VMware-Fix-guestinfo.-.config.data-and-.config.url-v.patch
Patch11:        0012-config-version-handle-configuration-version-1.patch
Patch12:        0013-config-util-add-cloud-init-detection-to-initial-pars.patch
Patch13:        0014-Revert-drop-OEM-URI-support.patch
Patch14:        0015-internal-resource-url-support-btrfs-as-OEM-partition.patch
Patch15:        0016-translation-support-OEM-and-oem.patch
Patch16:        0017-revert-internal-oem-drop-noop-OEMs.patch
Patch17:        0018-docs-Add-re-added-platforms-to-docs-to-pass-tests.patch
Patch18:        0019-usr-share-oem-oem.patch
Patch19:        0020-internal-exec-stages-mount-Mount-oem.patch

BuildRequires: libblkid-devel
BuildRequires: systemd-rpm-macros
BuildRequires: go-rpm-macros
BuildRequires: golang

ExcludeArch: %{ix86}

# Requires for 'disks' stage
%if 0%{?fedora}
Recommends: btrfs-progs
%endif
Requires: dosfstools
Requires: gdisk
Requires: dracut

%description
Ignition is a utility used to manipulate systems during the initramfs.
This includes partitioning disks, formatting partitions, writing files
(regular files, systemd units, etc.), and configuring users. On first
boot, Ignition reads its configuration from a source of truth (remote
URL, network metadata service, hypervisor bridge, etc.) and applies
the configuration.

%if 0%{?with_validate}
############## validate subpackage ##############

%package validate

Summary:  Validation tool for Ignition configs
License:  Apache-2.0

%description validate
Ignition is a utility used to manipulate systems during the initramfs.
This includes partitioning disks, formatting partitions, writing files
(regular files, systemd units, etc.), and configuring users. On first
boot, Ignition reads its configuration from a source of truth (remote
URL, network metadata service, hypervisor bridge, etc.) and applies
the configuration.

This package contains a tool for validating Ignition configurations.

############## validate-redistributable subpackage ##############
%endif

%if 0%{?with_grub}
############## grub subpackage ##############

%package grub
Summary:  Enablement glue for bootupd's grub2 config
License:  Apache-2.0

# `ignition-grub` is a rename `ignition-ignition-grub` so let's obsolete `ignition-ignition-grub`
Obsoletes: ignition-ignition-grub < 2.13.0-4

%description grub
This package contains the grub2 config which is compatable with bootupd.
%endif

%prep
%forgeautosetup -p1

%build
export LDFLAGS="-X github.com/coreos/ignition/v2/internal/version.Raw=%{version} -X github.com/coreos/ignition/v2/internal/distro.selinuxRelabel=false "
%if 0%{?rhel} && 0%{?rhel} <= 8
# Disable writing ssh keys fragments on RHEL/CentOS <= 8
LDFLAGS+=' -X github.com/coreos/ignition/v2/internal/distro.writeAuthorizedKeysFragment=false '
%endif
%if 0%{?rhel}
# Need uncompressed debug symbols for debuginfo extraction
LDFLAGS+=' -compressdwarf=false '
%endif
export GOFLAGS="-mod=vendor"

echo "Building ignition..."
GOEXPERIMENT=strictfipsruntime %gobuild -ldflags "${LDFLAGS:-} -o ./ignition internal/main.go

%if 0%{?with_validate}
echo "Building ignition-validate..."
%gobuild -ldflags "${LDFLAGS:-} -o ./ignition-validate validate/main.go

%global gocrossbuild go build -ldflags "${LDFLAGS:-} -B 0x$(cat /dev/urandom | tr -d -c '0-9a-f' | head -c16)" -a -v -x
%endif

%if 0%{?with_cross}
echo "Building statically-linked Linux ignition-validate..."
GOEXPERIMENT= CGO_ENABLED=0 GOARCH=%{goarch} GOOS=linux %gocrossbuild -o ./ignition-validate-%{_target_cpu}-unknown-linux-gnu-static validate/main.go
GOEXPERIMENT= CGO_ENABLED=0 GOARCH=s390x GOOS=linux %gocrossbuild -o ./ignition-validate-s390x-unknown-linux-gnu-static validate/main.go
GOEXPERIMENT= CGO_ENABLED=0 GOARCH=ppc64le GOOS=linux %gocrossbuild -o ./ignition-validate-ppc64le-unknown-linux-gnu-static validate/main.go

echo "Building macOS ignition-validate..."
GOEXPERIMENT= GOARCH=%{goarch} GOOS=darwin %gocrossbuild -o ./ignition-validate-%{_target_cpu}-apple-darwin validate/main.go

%ifarch x86_64
echo "Building Windows ignition-validate..."
GOEXPERIMENT= GOARCH=amd64 GOOS=windows %gocrossbuild -o ./ignition-validate-%{_target_cpu}-pc-windows-gnu.exe validate/main.go
%endif
%endif

%install
install -m 0755 -d %{buildroot}/%{_libexecdir}

%if 0%{?with_grub}
# grub
install -d -p %{buildroot}%{_prefix}/lib/bootupd/grub2-static/configs.d
install -p -m 0644 grub2/05_ignition.cfg  %{buildroot}%{_prefix}/lib/bootupd/grub2-static/configs.d/
%endif

# ignition
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 ./ignition %{buildroot}%{_bindir}
%if 0%{?with_validate}
install -p -m 0755 ./ignition-validate %{buildroot}%{_bindir}
%endif


ln -rsf %{buildroot}%{_bindir}/ignition %{buildroot}%{_libexecdir}/ignition-rmcfg

%if 0%{?with_cross}
install -d -p %{buildroot}%{_datadir}/ignition
install -p -m 0644 ./ignition-validate-* %{buildroot}%{_datadir}/ignition
%endif

%if %{with check}
%check
sed -i '34d' ./test
sed -i '/Checking gofmt/,+5d' ./test
VERSION=%{version} GOARCH=%{goarch} ./test
%endif

%files
%license %{golicenses}
%doc %{godocs}
%{_libexecdir}/ignition-rmcfg
%{_bindir}/ignition

%if 0%{?with_validate}
%files validate
%doc README.md
%license %{golicenses}
%{_bindir}/ignition-validate
%if 0%{?with_cross}
%dir %{_datadir}/ignition
%{_datadir}/ignition/ignition-validate-*
%endif
%endif

%if 0%{?with_grub}
%files grub
%doc README.md
%license %{golicenses}
%{_prefix}/lib/bootupd/grub2-static/configs.d/05_ignition.cfg
%endif

%changelog
* Fri Jan 16 2026 Sumit Jena <v-sumitjena@microsoft.com> - 2.22.1-2
- Initial Azure Linux import from Fedora 43 (license: MIT)
- License verified

* Fri Dec 12 2025 Steven Presti <spresti@redhat.com> - 2.25.0-1
- New Release

* Tue Oct 14 2025 Steven Presti <spresti@redhat.com> - 2.24.0-1
- New Release

* Fri Oct 10 2025 Alejandro Sáez <asm@redhat.com> - 2.23.0-3
- rebuild

* Wed Oct 01 2025 Steven Presti <spresti@redhat.com> - 2.23.0-2
- Build Ignition with GOEXPERIMENT=strictfipsruntime
- Ignition-validate non-FIPS

* Wed Sep 10 2025 Steven Presti <spresti@redhat.com> - 2.23.0-1
- New Release

* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 2.22.0-5
- Rebuild for golang-1.25.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Tiago Bueno <tiago.bueno@gmail.com> - 2.22.0-3
- Fix rpminspect debug symbols failure

* Tue Jul 15 2025 Tiago Bueno <tiago.bueno@gmail.com> - 2.22.0-2
- Backport fix for OracleCloud do not wrap errors from FetchToBuffer

* Tue Jul 8 2025 Yasmin Valim <ydesouza@redhat.com> - 2.22.0-1
- New Release

* Wed Mar 19 2025 Steven Presti <spresti@redhat.com> - 2.21.0-2
- Rename ignition.cfg -> 05_ignition.cfg to mirror upstream
  additionally backport rename.
- Rename ignition-ignition-grub subpackage to ignition-grub
- Update grub2 config to use the correct dir for bootupd static grub configs
  https://github.com/coreos/ignition/pull/2037#issuecomment-2736300056

* Fri Mar 14 2025 Steven Presti <spresti@redhat.com> - 2.21.0-1
- New Release

* Mon Jan 27 2025 David Jachimowicz <djachimo@redhat.com> - 2.20.0-5
- Update ignition-edge commit to include https://github.com/fedora-iot/ignition-edge/pull/3

* Wed Jan 22 2025 FeRD (Frank Dana) <ferdnyc@gmail.com> - 2.20.0-4
- Apply upstream patch for Go 1.24 compatibility

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 05 2024 Miguel Martín <mmartinv@redhat.com> - 2.20.0-2
- Update ignition-edge commit to include
    - https://github.com/fedora-iot/ignition-edge/pull/2

* Wed Oct 23 2024 Steven Presti <spresti@redhat.com> - 2.20.0-1
- New Release

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 05 2024 Steven Presti <spresti@redhat.com> - 2.19.0-1
- New release

* Mon Mar 4 2024 Yasmin de Souza <ydesouza@redhat.com> - 2.18.0-1
- New release
- Discontinue support for i686

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 2.17.0-6
- Rebuild for golang 1.22.0

* Fri Feb 09 2024 Timothée Ravier <tim@siosm.fr> - 2.17.0-5
- Backport fix for unexpected Azure IMDS status codes

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Steven Presti <spresti@redhat.com> - 2.17.0-2
- Add ignition-grub subpackage

* Wed Nov 22 2023 Steven Presti <spresti@redhat.com> - 2.17.0-1
- New release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Benjamin Gilbert <bgilbert@redhat.com> - 2.16.2-1
- New release

* Mon Jul 10 2023 Benjamin Gilbert <bgilbert@redhat.com> - 2.16.1-1
- New release

* Thu Jun 1 2023 Steven Presti <spresti@redhat.com> - 2.15.0-4
- Switch License tags to SPDX

* Thu Feb 23 2023 Benjamin Gilbert <bgilbert@redhat.com> - 2.15.0-3
- Remove ignition-edge files from base package

* Wed Feb 22 2023 Paul Whalen <pwhalen@fedoraproject.org> - 2.15.0-2
- Enable ignition-edge in Fedora

* Tue Feb 21 2023 Benjamin Gilbert <bgilbert@redhat.com> - 2.15.0-1
- New release
- Drop Conflicts/Obsoletes for ancient Ignition releases

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 9 2022 Christian Glombek <cglombek@redhat.com> - 2.14.0-5
- Enable writing ssh keys fragments on RHEL/CentOS >= 9

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 27 2022 Benjamin Gilbert <bgilbert@redhat.com> - 2.14.0-3
- Add macOS aarch64 binary to -redistributable

* Sat Jun 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 2.14.0-2
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Mon May 16 2022 Steven Presti <spresti@redhat.com> - 2.14.0-1
- New release
- Add ignition-apply symlink
- Add ignition-rmcfg symlink and ignition-delete-config.service

* Thu Mar 17 2022 Sohan Kunkerkar <skunkerk@redhat.com> - 2.13.0-5
- Avoid kernel lockdown on VMware when running with secure boot

* Fri Jan 28 2022 Benjamin Gilbert <bgilbert@redhat.com> - 2.13.0-4
- Rename -validate-nonlinux subpackage to -validate-redistributable
- Add static Linux binaries to -redistributable
- Fix macro invocation in comment

* Thu Jan 20 2022 Benjamin Gilbert <bgilbert@redhat.com> - 2.13.0-3
- Fix LUKS volume reuse
- Avoid double patch application on non-Fedora

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 30 2021 Sohan Kunkerkar <skunkerk@redhat.com> - 2.13.0-1
- New release

* Wed Oct 13 2021 Sohan Kunkerkar <skunkerk@redhat.com> - 2.12.0-3
- Move Ignition report to /etc

* Thu Aug 26 2021 Sohan Kunkerkar <skunkerk@redhat.com> - 2.12.0-2
- Disable file fragment writing logic for SSH authorized_keys on RHEL/CentOS
- Disable compressdwarf flag to avoid build failures on RHEL/CentOS
- Disable cross-building of Ignition-validate on RHEL/CentOS
- Conditionalize Fedora-specific configuration

* Fri Aug 6 2021 Sohan Kunkerkar <skunkerk@redhat.com> - 2.12.0-1
- New release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul  8 2021 Benjamin Gilbert <bgilbert@redhat.com> - 2.11.0-2
- Move ignition-firstboot-complete and ignition-setup-user services out of
  package into distro glue

* Fri Jun 25 2021 Benjamin Gilbert <bgilbert@redhat.com> - 2.11.0-1
- New release

* Wed May 26 2021 Jonathan Lebon <jonathan@jlebon.com> - 2.10.1-3
- Backport patch for multipath on firstboot
  https://github.com/coreos/ignition/pull/1208
  https://github.com/coreos/fedora-coreos-config/pull/1011

* Wed May 26 2021 Jonathan Lebon <jonathan@jlebon.com> - 2.10.1-2
- Redo packaging using go2rpm

* Thu Apr 29 2021 Stephen Lowrie <slowrie@redhat.com> - 2.10.1-1
- New release

* Fri Feb 05 2021 Benjamin Gilbert <bgilbert@redhat.com> - 2.9.0-4
- Drop Git commit hash from Release
- Correctly enable IMDS patch
- Switch to %%autosetup
- Set ExclusiveArch from %%go_arches
- Drop mention of networkd in package description

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-3.git1d56dc8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Sohan Kunkerkar <skunkerk@redhat.com> - 2.9.0-2.git1d56dc8
- Fix AWS probing by using the IMDS token URL to ensure that networking is up

* Fri Jan 08 2021 Sohan Kunkerkar <skunkerk@redhat.com> - 2.9.0-1.git1d56dc8
- New release

* Thu Dec 03 2020 Sohan Kunkerkar <skunkerk@redhat.com> - 2.8.1-1.gitc733d23
- New release

* Wed Nov 25 2020 Sohan Kunkerkar <skunkerk@redhat.com> - 2.8.0-1.gitdb4d30d
- New release

* Wed Oct 14 2020 Stephen Lowrie <slowrie@redhat.com> - 2.7.0-1.git5be43fd
- New release

* Wed Aug 12 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.6.0-2.git947598e
- Fix sector size detection on s390x

* Fri Aug 07 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.6.0-1.git947598e
- New release

* Fri Aug 07 2020 Jonathan Lebon <jonathan@jlebon.com> - 2.5.0-3.git0d6f3e5
- Backport conditional networking fix for OpenStack and CloudStack
  https://github.com/coreos/ignition/pull/1057

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2.git0d6f3e5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.5.0-1.git0d6f3e5
- New release
- Ship support code from Ignition tarball instead of ignition-dracut

* Thu Jul 16 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.4.1-1.git5260a5b
- New release
- Bump ignition-dracut to fix warning in udev rule

* Wed Jul 15 2020 Jonathan Lebon <jonathan@jlebon.com> - 2.4.0-2.gitd18bf90
- Backport root homedir relabeling fix
  https://github.com/coreos/ignition/pull/1029 for
  https://github.com/coreos/fedora-coreos-config/pull/426#issuecomment-658867731.

* Mon Jul 13 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.4.0-1.gitd18bf90
- New release
- Bump ignition-dracut

* Mon Jun 15 2020 Timothée Ravier <travier@redhat.com> - 2.3.0-3.gitee616d5
- Update to latest ignition-dracut to fix coreos-gpt-setup unit
  https://github.com/coreos/ignition-dracut/pull/191

* Mon Jun 01 2020 Jonathan Lebon <jonathan@jlebon.com> - 2.3.0-2.gitee616d5
- Update to latest ignition-dracut to fix error handling
  https://github.com/coreos/ignition-dracut/pull/188

* Tue May 05 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.3.0-1.gitee616d5
- New release
- Bump ignition-dracut

* Sun Apr 26 2020 Dusty Mabe <dusty@dustymabe.com> - 2.2.1-5.git2d3ff58
- Update to latest ignition-dracut for network fixes
  https://github.com/coreos/ignition-dracut/pull/174

* Thu Apr 16 2020 Colin Walters <walters@verbum.org> - 2.2.1-4.git2d3ff58
- Update to latest ignition-dracut for virtio dump

* Mon Mar 30 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.2.1-3.git2d3ff58
- Bump ignition-dracut to fix umount stage network access

* Sat Mar 28 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.2.1-2.git2d3ff58
- Fix userdata/metadata fetch on Packet

* Tue Mar 24 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.2.1-1.git2d3ff58
- New release
- Bump ignition-dracut for initramfs network teardown

* Sat Feb 01 2020 Benjamin Gilbert <bgilbert@redhat.com> - 2.1.1-6.git40c0b57
- Switch -validate-nonlinux to noarch; move files to /usr/share/ignition
- Improve -validate-nonlinux descriptive text

* Fri Jan 31 2020 Jonathan Lebon <jonathan@jlebon.com> - 2.1.1-5.git40c0b57
- Bump ignition-dracut for ignition-diskful-subsequent target
  https://github.com/coreos/ignition-dracut/pull/151
- Kill grub dropin
  https://github.com/coreos/ignition-dracut/pull/91

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4.git40c0b57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Dusty Mabe <dusty@dustymabe.com> - 2.1.1-3.git40c0b57
- Backport upstream patch to workaround problem booting on live systems
    - https://github.com/coreos/fedora-coreos-tracker/issues/339
    - https://github.com/coreos/ignition/pull/907

* Tue Dec 17 2019 Andrew Jeddeloh <ajeddelo@redhat.com> - 2.1.1-2.git40c0b57
- Add ignition-validate-nonlinux subpackage. This should not be installed. It
  is only used for building binaries to sign by Fedora release engineering and
  include on the Ignition project's Github releases page.

* Fri Dec 13 2019 Andrew Jeddeloh <ajeddelo@redhat.com> - 2.1.1-1.git40c0b57
- New release 2.1.1

* Mon Dec 09 2019 Jonathan Lebon <jonathan@jlebon.com> - 2.0.1-9.gita8f91fa
- Use the master branch of ignition-dracut, not spec2x

* Fri Dec 06 2019 Jonathan Lebon <jonathan@jlebon.com> - 2.0.1-8.gita8f91fa
- Bump Ignition for that sweet SELinux labeling:
  https://github.com/coreos/ignition/pull/846

* Thu Dec 05 2019 Jonathan Lebon <jonathan@jlebon.com> - 2.0.1-7.git641ec6a
- Don't require btrfs-progs, just recommend it
  https://github.com/coreos/fedora-coreos-tracker/issues/323

* Wed Dec 04 2019 Allen Bai <abai@redhat.com> - 2.0.1-6.git641ec6a
- Update dracut to latest spec2x
    * firstboot-complete: tell zipl to run

* Thu Oct 31 2019 Colin Walters <walters@verbum.org> - 2.0.1-5.git641ec6a
- Update dracut

* Wed Sep 25 2019 Colin Walters <walters@verbum.org> - 2.0.1-4.git641ec6a
- Bump to latest in prep for rootfs redeploy work

* Sat Sep 21 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.1-3.gite75cf24
- Fix up arch dependencies for new golang specs

* Fri Aug 16 2019 Colin Walters <walters@verbum.org> - 2.0.1-2.gite75cf24
- Update dracut for gpt fixes

* Thu Jul 25 2019 Andrew Jeddeloh <ajeddelo@redhat.com> - 2.0.1-1.gite75cf24
- New release 2.0.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2.git0c1da80
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 2019 Andrew Jeddeloh <ajeddelo@redhat.com> - 2.0.0-1.git0c1da80
- New release 2.0.0

* Fri May 03 2019 Jonathan Lebon <jonathan@jlebon.com> - 2.0.0-beta.3.git910e6c6
- Adapt distro.selinuxRelabel flag path for v2/ move

* Fri May 03 2019 Jonathan Lebon <jonathan@jlebon.com> - 2.0.0-beta.2.git910e6c6
- Bump ignition-dracut dropping CoreOS integration files

* Mon Apr 29 2019 Andrew Jeddeloh <ajeddelo@redhat.com> - 2.0.0-beta.1.git910e6c6
- New release 2.0.0-beta

* Mon Apr 08 2019 Jonathan Lebon <jonathan@jlebon.com> - 2.0.0-alpha.3.git906cf04
- ignition-dracut: update to latest
    * dracut/30ignition: link to RHBZ in ignition-complete
    * dracut/30ignition: add OnFailure= for ExecStop= services
    * dracut/30ignition: order ExecStop= units before initrd-switch-root.target
    * dracut/30ignition: re-order directives in remount-sysroot
    * dracut/30ignition: add missing Before= for mount unit
    * dracut/30ignition: order ignition-complete.target before initrd.target
    * module_setup: include cdrom rules for openstack

* Wed Mar 27 2019 Benjamin Gilbert <bgilbert@backtick.net> - 2.0.0-alpha.2.git906cf04
- Backport fix for SELinux relabeling of systemd units
- Drop obsolete override of chroot path

* Wed Mar 27 2019 Jonathan Lebon <jonathan@jlebon.com> - 2.0.0-alpha.1.git906cf04
- New release 2.0.0-alpha
- ignition-dracut: Go back to master branch

* Fri Mar 22 2019 Dusty Mabe <dusty@dustymabe.com> - 0.31.0-7.gitf59a653
- ignition-dracut: Pull in latest from spec2x branch
    * grub: support overriding network kcmdline args
- ignition: pull in subuid/subgid files patch from spec2x branch
    * stages/files: Also relabel subuid/subgid files

* Wed Mar 20 2019 Michael Nguyen <mnguyen@redhat.com> - 0.31.0-6.gitf59a653
- Backport patch for supporting guestinfo.ignition.config.data

* Mon Mar 18 2019 Dusty Mabe <dusty@dustymabe.com> - 0.31.0-5.gitf59a653
- Use the spec2x branch of ignition-dracut upstream
- * Since ignition-dracut master has moved to supporting ignition
    spec 3.x we are applying 2.x related fixes to the spec2x
    branch in the ignition-dracut repo.
  * Summary of backports: https://github.com/coreos/ignition-dracut/pull/58

* Mon Mar 18 2019 Benjamin Gilbert <bgilbert@backtick.net> - 0.31.0-4.gitf59a653
- Move dracut modules into main ignition package
- Move ignition binary out of the PATH
- Move ignition-validate into a subpackage
- Include ignition-dracut license file
- Drop developer docs from base package

* Mon Mar 18 2019 Colin Walters <walters@verbum.org> - 0.31.0-3.gitf59a653
- Backport patch for networking

* Mon Mar 04 2019 Dusty Mabe <dusty@dustymabe.com> - 0.31.0-2.gitf59a653
- ignition-dracut: backport patch for finding ignition.firstboot file on UEFI systems
  https://github.com/coreos/ignition-dracut/pull/52

* Wed Feb 20 2019 Andrew Jeddeloh <andrew.jeddeloh@redhat.com> - 0.31.0-1.gitf59a653
- New release 0.31.0

* Fri Feb 15 2019 Dusty Mabe <dusty@dustymabe.com> - 0.30.0-4.git308d7a0
- Bump to ignition-dracut 2c69925
- * support platform configs and user configs in /boot
    ^ https://github.com/coreos/ignition-dracut/pull/43
  * Add ability to parse config.ign file on boot
    ^ https://github.com/coreos/ignition-dracut/pull/42

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-3.git308d7a0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Dusty Mabe <dusty@dustymabe.com> - 0.30.0-2.git308d7a0
- Bump to ignition-dracut fa7131b
- * 7579b92 journal: add clarifying comment for context
  * a6551f1 Remount /sysroot rw (#38)
  * ignition-firstboot-complete.service: Remount /boot rw

* Sat Dec 15 2018 Benjamin Gilbert <bgilbert@redhat.com> - 0.30.0-1.git308d7a0
- New release 0.30.0

* Fri Dec 14 2018 Michael Nguyen <mnguyen@redhat.com> - 0.29.1-3.gitb1ab0b2
- define gopath for RHEL7

* Tue Dec 11 2018 Dusty Mabe <dusty@dustymabe.com> - 0.29.1-2.gitb1ab0b2
- require golang >= 1.10 and specify architecture list for RHEL7

* Tue Dec 11 2018 Andrew Jeddeloh <andrew.jeddeloh@redhat.com> - 0.29.1-1.gitb1ab0b2
- New release 0.29.1

* Wed Nov 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.28.0-12.gitf707912
- Rebuild for protobuf 3.6 in rawhide (f30)

* Tue Nov 20 2018 Jonathan Lebon <jonathan@jlebon.com> - 0.28.0-11.git7b83454
- Bump to ignition-dracut 7b83454

* Thu Oct 25 2018 Dusty Mabe <dusty@dustymabe.com> - 0.28.0-10.gitf707912
- Bump to ignition-dracut decf63f
- * 03d8438 30ignition: only instmods if module available

* Thu Oct 25 2018 Dusty Mabe <dusty@dustymabe.com> - 0.28.0-9.gitf707912
- Bump to ignition-dracut 7ee64ca
- * 3ec0b39 remove ignition-remount-sysroot.service files
  * 66335f2 ignition: run files stage at original CL ordering
  * 0301a03 ignition-disks.service: drop Requires=network.target
  * a0bc135 ignition-ask-var-mount.service: use RemainAfterExit=yes
  * ecf5779 module-setup.sh: explicitly install qemu_fw_cfg

* Mon Oct 15 2018 Dusty Mabe <dusty@dustymabe.com> - 0.28.0-8.gitf707912
- Bump to ignition-dracut 4bdfb34
- * 6d0763a module-setup: Make mkfs.btrfs optional

* Wed Oct 10 2018 Jonathan Lebon <jonathan@jlebon.com> - 0.28.0-7.gitf707912
- Backport patch for handling sysctl files correctly
  https://github.com/coreos/coreos-assembler/pull/128
  https://github.com/openshift/machine-config-operator/pull/123

* Wed Sep 26 2018 Dusty Mabe <dusty@dustymabe.com> - 0.28.0-6.gitf707912
- Bump to ignition-dracut c09ce6f
- * ce9f648 30ignition: add support for ignition-disks

* Mon Sep 24 2018 Dusty Mabe <dusty@dustymabe.com> - 0.28.0-5.gitf707912
- Remove requires for btrfs on !fedora
- Bump to ignition-dracut 8c85eb3
- * 26f2396 journal: Don't log to console AND kmsg

* Mon Sep 17 2018 Jonathan Lebon <jonathan@jlebon.com> - 0.28.0-4.gitf707912
- Backport patch for relabeling /var/home on FCOS
  https://github.com/coreos/fedora-coreos-config/issues/2

* Thu Sep 06 2018 Luca Bruno <lucab@fedoraproject.org> - 0.28.0-3.gitf707912
- Add requires for disks stage

* Thu Aug 30 2018 Dusty Mabe <dusty@dustymabe.com> - 0.28.0-2.gitf707912
- Bump to ignition-dracut d056287
- * 3f41219 dracut/ignition: remove CL-legacy udev references
- * 92ef9dd coreos-firstboot-complete: RemainAfterExit=yes

* Thu Aug 30 2018 Andrew Jeddeloh <andrewjeddeloh@redhat.com> - 0.28.0-1.gitf707912
- New release 0.28.0

* Fri Aug 17 2018 Dusty Mabe <dusty@dustymabe.com> - 0.27.0-3.gitcc7ebe0
- Bump to ignition-dracut 56aa514

* Wed Aug 15 2018 Jonathan Lebon <jonathan@jlebon.com> - 0.27.0-2.gitcc7ebe0
- Backport patch for /root relabeling
  https://github.com/coreos/ignition/pull/613

* Fri Aug 10 2018 Jonathan Lebon <jonathan@jlebon.com> - 0.27.0-1.gitcc7ebe0
- New release 0.27.0

* Sat Jul 21 2018 Dusty Mabe <dusty@dustymabe.com> - 0.26.0-0.6.git7610725
- Bump to ignition-dracut d664657

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-0.5.git7610725
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Dusty Mabe <dusty@dustymabe.com> - 0.26.0-0.4.git7610725
- Fix building on el7 (install -D not working)

* Fri Jun 29 2018 Dusty Mabe <dusty@dustymabe.com> - 0.26.0-0.3.git7610725
- Bump to ignition-dracut 17a201b

* Tue Jun 26 2018 Dusty Mabe <dusty@dustymabe.com> - 0.26.0-0.2.git7610725
- Rename dustymabe/bootengine upstrem to dustymabe/ignition-dracut

* Thu Jun 21 2018 Dusty Mabe <dusty@dustymabe.com> - 0.26.0-0.1.git7610725
- First package for Fedora

