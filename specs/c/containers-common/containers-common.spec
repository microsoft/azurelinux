## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global project containers
%global repo container-libs

%if %{defined copr_username}
%define copr_build 1
%endif

# See https://github.com/containers/netavark/blob/main/rpm/netavark.spec
# for netavark epoch
%if %{defined copr_build}
%define netavark_epoch 102
%else
%define netavark_epoch 2
%endif

Name: containers-common
%if %{defined copr_build}
Epoch: 102
%else
Epoch: 5
%endif
# DO NOT TOUCH the Version string!
# The TRUE source of this specfile is:
# https://github.com/containers/container-libs/blob/main/common/rpm/containers-common.spec
# If that's what you're reading, Version must be 0, and will be updated by Packit for
# copr and koji builds.
# If you're reading this on dist-git, the version is automatically filled in by Packit.
Version: 0.67.0
Release: %autorelease
License: Apache-2.0
BuildArch: noarch
# for BuildRequires: go-md2man
ExclusiveArch: %{golang_arches} noarch
Summary: Common configuration and documentation for containers
BuildRequires: git-core
BuildRequires: go-md2man
Provides: skopeo-containers = %{epoch}:%{version}-%{release}
Requires: (container-selinux >= 2:2.162.1 if selinux-policy)
%if 0%{?fedora}
Recommends: fuse-overlayfs
Requires: (fuse-overlayfs if fedora-release-identity-server)
%else
Suggests: fuse-overlayfs
%endif
URL: https://github.com/%{project}/%{repo}
Source0: %{url}/archive/refs/tags/common/v%{version}.tar.gz
Source1: https://raw.githubusercontent.com/containers/shortnames/refs/heads/main/shortnames.conf
# Fetch RPM-GPG-KEY-redhat-release from the authoritative source instead of storing
# a copy in repo or dist-git. Depending on distribution-gpg-keys rpm is also
# not an option because that package doesn't exist on CentOS Stream.
Source2: https://access.redhat.com/security/data/fd431d51.txt

%description
This package contains common configuration files and documentation for container
tools ecosystem, such as Podman, Buildah and Skopeo.

It is required because the most of configuration files and docs come from projects
which are vendored into Podman, Buildah, Skopeo, etc. but they are not packaged
separately.

%package extra
Summary: Extra dependencies for Podman and Buildah
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: container-network-stack
Requires: oci-runtime
Requires: passt
%if %{defined fedora}
Conflicts: podman < 5:5.0.0~rc4-1
Recommends: composefs
Recommends: crun
Requires: (crun if fedora-release-identity-server)
Requires: netavark >= %{netavark_epoch}:1.10.3-1
Suggests: slirp4netns
Recommends: qemu-user-static
Requires: (qemu-user-static-aarch64 if fedora-release-identity-server)
Requires: (qemu-user-static-arm if fedora-release-identity-server)
Requires: (qemu-user-static-x86 if fedora-release-identity-server)
%endif

%description extra
This subpackage will handle dependencies common to Podman and Buildah which are
not required by Skopeo.

%prep
%autosetup -Sgit -n %{repo}-common-v%{version}

# Fine-grain distro- and release-specific tuning of config files,
# e.g., seccomp, composefs, registries on different RHEL/Fedora versions
bash common/rpm/update-config-files.sh

%build
mkdir -p man5
for i in common/docs/*.5.md image/docs/*.5.md storage/docs/*.5.md; do
   go-md2man -in $i -out man5/$(basename $i .md)
done

%install
# install config and policy files for registries
install -dp %{buildroot}%{_sysconfdir}/containers/{certs.d,oci/hooks.d,networks,systemd}
install -dp %{buildroot}%{_sharedstatedir}/containers/sigstore
install -dp %{buildroot}%{_datadir}/containers/systemd
install -dp %{buildroot}%{_prefix}/lib/containers/storage
install -dp -m 700 %{buildroot}%{_prefix}/lib/containers/storage/overlay-images
touch %{buildroot}%{_prefix}/lib/containers/storage/overlay-images/images.lock
install -dp -m 700 %{buildroot}%{_prefix}/lib/containers/storage/overlay-layers
touch %{buildroot}%{_prefix}/lib/containers/storage/overlay-layers/layers.lock

install -Dp -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/000-shortnames.conf
install -Dp -m0644 image/default.yaml %{buildroot}%{_sysconfdir}/containers/registries.d/default.yaml
install -Dp -m0644 image/default-policy.json %{buildroot}%{_sysconfdir}/containers/policy.json
install -Dp -m0644 image/registries.conf %{buildroot}%{_sysconfdir}/containers/registries.conf
install -Dp -m0644 storage/storage.conf %{buildroot}%{_datadir}/containers/storage.conf

# RPM-GPG-KEY-redhat-release already exists on rhel envs, install only on
# fedora and centos
%if %{defined fedora} || %{defined centos}
install -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
%endif

install -Dp -m0644 common/contrib/redhat/registry.access.redhat.com.yaml -t %{buildroot}%{_sysconfdir}/containers/registries.d
install -Dp -m0644 common/contrib/redhat/registry.redhat.io.yaml -t %{buildroot}%{_sysconfdir}/containers/registries.d

# install manpages
for i in man5/*.5; do
    install -Dp -m0644 $i -t %{buildroot}%{_mandir}/man5
done
ln -s containerignore.5 %{buildroot}%{_mandir}/man5/.containerignore.5

# install config files for mounts, containers and seccomp
install -m0644 common/pkg/subscriptions/mounts.conf %{buildroot}%{_datadir}/containers/mounts.conf
install -m0644 common/pkg/seccomp/seccomp.json %{buildroot}%{_datadir}/containers/seccomp.json
install -m0644 common/pkg/config/containers.conf %{buildroot}%{_datadir}/containers/containers.conf

# install secrets patch directory
install -d -p -m 755 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s ../../../..%{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s ../../../..%{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
ln -s ../../../..%{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/redhat.repo

# Placeholder check to silence rpmlint warnings
%check

%files
%dir %{_sysconfdir}/containers
%dir %{_sysconfdir}/containers/certs.d
%dir %{_sysconfdir}/containers/networks
%dir %{_sysconfdir}/containers/oci
%dir %{_sysconfdir}/containers/oci/hooks.d
%dir %{_sysconfdir}/containers/registries.conf.d
%dir %{_sysconfdir}/containers/registries.d
%dir %{_sysconfdir}/containers/systemd
%dir %{_prefix}/lib/containers
%dir %{_prefix}/lib/containers/storage
%dir %{_prefix}/lib/containers/storage/overlay-images
%dir %{_prefix}/lib/containers/storage/overlay-layers
%{_prefix}/lib/containers/storage/overlay-images/images.lock
%{_prefix}/lib/containers/storage/overlay-layers/layers.lock

%config(noreplace) %{_sysconfdir}/containers/policy.json
%config(noreplace) %{_sysconfdir}/containers/registries.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf.d/000-shortnames.conf
%if 0%{?fedora} || 0%{?centos}
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
%endif
%config(noreplace) %{_sysconfdir}/containers/registries.d/default.yaml
%config(noreplace) %{_sysconfdir}/containers/registries.d/registry.redhat.io.yaml
%config(noreplace) %{_sysconfdir}/containers/registries.d/registry.access.redhat.com.yaml
%ghost %{_sysconfdir}/containers/storage.conf
%ghost %{_sysconfdir}/containers/containers.conf
%dir %{_sharedstatedir}/containers/sigstore
%{_mandir}/man5/Containerfile.5.gz
%{_mandir}/man5/containerignore.5.gz
%{_mandir}/man5/.containerignore.5.gz
%{_mandir}/man5/containers*.5.gz
%dir %{_datadir}/containers
%dir %{_datadir}/containers/systemd
%{_datadir}/containers/storage.conf
%{_datadir}/containers/containers.conf
%{_datadir}/containers/mounts.conf
%{_datadir}/containers/seccomp.json
%dir %{_datadir}/rhel
%dir %{_datadir}/rhel/secrets
%{_datadir}/rhel/secrets/*

%files extra

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 5:0.67.0-2
- test: add initial lock files

* Wed Feb 11 2026 Packit <hello@packit.dev> - 5:0.67.0-1
- Update to 0.67.0 upstream release

* Wed Sep 03 2025 Packit <hello@packit.dev> - 5:0.64.2-1
- Update to 0.64.2 upstream release

* Thu Aug 14 2025 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.64.1-2
- update shortnames.conf with QUBIP/pq-container info

* Tue Aug 05 2025 Packit <hello@packit.dev> - 5:0.64.1-1
- Update to 0.64.1 upstream release

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5:0.64.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Packit <hello@packit.dev> - 5:0.64.0-1
- Update to 0.64.0 upstream release

* Wed Jun 04 2025 Packit <hello@packit.dev> - 5:0.63.1-1
- Update to 0.63.1 upstream release

* Thu Apr 17 2025 Packit <hello@packit.dev> - 5:0.63.0-1
- Update to 0.63.0 upstream release

* Thu Mar 27 2025 Packit <hello@packit.dev> - 5:0.62.3-1
- Update to 0.62.3 upstream release

* Wed Mar 12 2025 Packit <hello@packit.dev> - 5:0.62.2-1
- Update to 0.62.2 upstream release

* Mon Mar 03 2025 Packit <hello@packit.dev> - 5:0.62.1-1
- Update to 0.62.1 upstream release

* Thu Feb 06 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:0.62.0-2
- remove patch merged upstream

* Fri Jan 31 2025 Packit <hello@packit.dev> - 5:0.62.0-1
- Update to 0.62.0 upstream release

* Thu Jan 16 2025 Packit <hello@packit.dev> - 5:0.61.1-1
- Update to 0.61.1 upstream release

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5:0.61.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 08 2024 Packit <hello@packit.dev> - 5:0.61.0-1
- Update to 0.61.0 upstream release

* Thu Oct 17 2024 Debarshi Ray <rishi@fedoraproject.org> - 5:0.60.4-5
- Revert "Move fuse-overlayfs to suggests" for all Fedoras

* Wed Oct 16 2024 Debarshi Ray <rishi@fedoraproject.org> - 5:0.60.4-4
- Revert "Move fuse-overlayfs to suggests" for Fedora 40 and older

* Tue Oct 15 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:0.60.4-3
- disable zstd chunked on fedora

* Tue Oct 08 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:0.60.4-2
- packit sidetag stuff

* Tue Oct 01 2024 Packit <hello@packit.dev> - 5:0.60.4-1
- Update to 0.60.4 upstream release

* Tue Sep 24 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:0.60.3-2
- add packit sidetag stuff

* Mon Sep 23 2024 Packit <hello@packit.dev> - 5:0.60.3-1
- Update to 0.60.3 upstream release

* Fri Sep 20 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:0.60.2-2
- delete stale patch - fixed upstream

* Tue Aug 20 2024 Packit <hello@packit.dev> - 5:0.60.2-1
- Update to 0.60.2 upstream release

* Mon Aug 12 2024 Packit <hello@packit.dev> - 5:0.60.1-1
- Update to 0.60.1 upstream release

* Fri Jul 26 2024 Packit <hello@packit.dev> - 5:0.60.0-1
- Update to 0.60.0 upstream release

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5:0.59.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Packit <hello@packit.dev> - 5:0.59.2-1
- Update to 0.59.2 upstream release

* Tue Jun 04 2024 Packit <hello@packit.dev> - 5:0.59.1-1
- Update to 0.59.1 upstream release

* Thu May 30 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.59.0-2
- ensure files are copied to builddir before patching

* Thu May 23 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.59.0-1
- bump to v0.59.0

* Fri Apr 19 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.58.0-18
- Add composefs but leave it disabled

* Fri Apr 19 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.58.0-17
- Revert "Add a hard requirement on composefs for now" and "Turn on
  composefs and convert_images=true"

* Thu Apr 18 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-16
- local build

* Thu Apr 18 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-15
- Convert image is currently broken

* Thu Apr 18 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-14
- local build

* Thu Apr 18 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-13
- Merge branch 'rawhide' of ssh://pkgs.fedoraproject.org/rpms/containers-
  common into rawhide

* Thu Apr 18 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-12
- local build

* Thu Apr 18 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-11
- Add recommends for composefs, which is used by default

* Wed Apr 17 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-10
- local build

* Wed Apr 17 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-9
- Turn on composefs and convert_images=true

* Tue Apr 02 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-8
- local build

* Tue Apr 02 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-7
- Add support for additionalstore /usr/lib/containers/storage

* Tue Apr 02 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-6
- local build

* Tue Mar 26 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.58.0-5
- Conflict with podman older than 5.0 rc4 as we now have pasta default

* Wed Mar 20 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.58.0-4
- container-selinux should be a hard Requires

* Wed Mar 20 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-3
- local build

* Wed Mar 20 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-2
- Change default to zstd:chunked

* Wed Mar 13 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.58.0-1
- bump to v0.58.0

* Wed Mar 13 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.3-7
- make passt and netavark hard dependencies

* Fri Mar 01 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.3-6
- local build

* Fri Mar 01 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.3-5
- local build

* Fri Mar 01 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.3-4
- Update for podman 5.0

* Wed Feb 07 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.3-3
- remove cni-plugins dependency

* Thu Feb 01 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.3-2
- bump netavark dep

* Thu Feb 01 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.3-1
- bump to v0.57.3

* Tue Jan 30 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 5:0.57.1-8
- Build only on golang arches

* Mon Jan 29 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.1-7
- local build

* Mon Jan 29 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.1-6
- local build

* Sun Jan 28 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.1-5
- local build

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5:0.57.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5:0.57.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.1-2
- containers.conf changes are common so far for all fedoras

* Fri Jan 05 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.1-1
- Use c/common upstream version for rpm with Epoch bump

* Sun Dec 10 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-101
- local build

* Thu Nov 09 2023 Brent Baude <bbaude@redhat.com> - 4:1-100
- Reverting zstd change to containers.conf

* Sun Nov 05 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-99
- Revert update.sh back to f39 version.

* Sun Nov 05 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-98
- local build

* Tue Oct 24 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-97
- local build

* Thu Sep 21 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-96
- local build

* Fri Aug 11 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-95
- local build

* Sat Jul 22 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-94
- local build

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-93
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 09 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-92
- local build

* Sun Jul 02 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-91
- local build

* Wed Apr 12 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-90
- extra subpackage depends netavark v1.6.0 or higher

* Mon Apr 10 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-89
- local build

* Mon Apr 10 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-88
- local build

* Tue Feb 21 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-87
- Resolves: #2170856 - add passt dependency

* Tue Feb 14 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 4:1-86
- Switch License to SPDX

* Wed Feb 01 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-85
- Suggests: qemu-user-static superseded by Recommends

* Tue Jan 31 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-84
- adjust qemu-user-static dependencies in containers-common-extra

* Thu Jan 26 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-83
- local build

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-82
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Alexander Larsson <alexl@redhat.com> - 4:1-81
- Add /etc/containers/systemd and /usr/share/containers/systemd dirs

* Thu Dec 15 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-80
- Change container-selinux to a recommends

* Wed Nov 02 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-79
- install RPM-GPG-KEY-redhat-release only on fedora and centos environments

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-78
- add cni-plugins and qemu-user-static deps to containers-common-extra

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-77
- both buildah and podman require iptables and nftables

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-76
- add containers-common-extra subpackage

* Wed Oct 05 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-75
- local build

* Tue Oct 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-74
- remove debbuild macros to comply with fedora guidelines

* Fri Sep 23 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-73
- deb envs probably need an explicit provides, whatevs

* Fri Sep 23 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-72
- obsolete and provide golang-github-containers-[common|image] =
  %%{epoch}:%%{version}-%%{release}

* Fri Sep 23 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-71
- obsolete golang-github-containers-common in debian and ubuntu

* Tue Sep 13 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-70
- local build

* Sun Sep 04 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-69
- local build

* Tue Aug 16 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-68
- Fix debbuild maintainer field issue

* Tue Aug 16 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-67
- debbuild package conflicts with golang-github-containers-common

* Wed Aug 10 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-66
- local build

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-64
- Update man pages and config files

* Wed Jul 13 2022 Jonathan Wakely <jwakely@fedoraproject.org> - 4:1-63
- Fix missing markup in Containerfile.5 man page

* Mon Jun 13 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-62
- Revert "skip RPM-GPG-KEY-redhat-release installation on non-centos RHEL"

* Mon Jun 13 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-61
- skip RPM-GPG-KEY-redhat-release installation on non-centos RHEL

* Tue May 31 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-60
- local build

* Fri May 27 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-59
- build deb packages using debbuild

* Thu May 12 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-58
- local build

* Tue Apr 26 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-57
- local build

* Thu Apr 14 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-56
- Update man pages and config files

* Wed Mar 23 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-55
- local build

* Tue Mar 15 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-54
- comment out log_driver for rhel8 on copr

* Mon Feb 14 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-53
- fix build - don't delete what doesn't exist

* Mon Feb 14 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-52
- temporarily remove dockerfile manpages

* Tue Feb 08 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-51
- update config files

* Thu Feb 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-50
- Revert "handle md2man dep for c9s"

* Thu Feb 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-49
- handle md2man dep for c9s

* Wed Feb 02 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-48
- Check for docker manpage existence in %%post

* Tue Feb 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-47
- resolve docker manpage conflicts

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-46
- no error if man5 exists

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-45
- install containerfile and dockerfile manpages

* Wed Jan 26 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-44
- Update man pages and config files

* Mon Jan 24 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-43
- Depend on container-network-stack and switch to autospec

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-41
- Update to grab latest man pages and configuration files

* Mon Nov 29 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-40
- Update to grab latest man pages and configuration files

* Mon Nov 08 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-39
- Update to grab latest man pages and configuration files

* Thu Oct 21 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-38
- Update to grab latest man pages and configuration files

* Thu Oct 07 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-37
- Update to grab latest man pages and configuration files

* Tue Oct 05 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-36
- Add .containerignore.5 link

* Fri Oct 01 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-35
- Update to grab latest man pages and configuration files

* Sun Sep 26 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-34
- Update to grab latest man pages and configuration files

* Mon Sep 20 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-33
- Update to grab latest man pages and configuration files

* Tue Sep 14 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-32
- Update to grab latest man pages and configuration files

* Wed Sep 08 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-31
- Update to grab latest man pages and configuration files

* Wed Aug 25 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-30
- Add memfd_secret to seccomp.json

* Thu Aug 12 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-29
- Update to grab latest man pages and configuration files

* Mon Jul 26 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-28
- Add support for signed RHEL images, enabled by default

* Mon Jul 26 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-27
- Add support for signed RHEL images, enabled by default

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-24
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Tue Jun 29 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-23
- containers-common-4:1-21
- fetch latest upstream configs

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-22
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-21
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-20
- Merge branch 'rawhide' of ssh://pkgs.fedoraproject.org/rpms/containers-
  common into rawhide

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-19
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Tue May 11 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-18
- Update containers.conf to latest, and change default log-driver to
  journald.

* Thu Apr 15 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-17
- containers-common-4:1-17
- add common dependencies like oci-runtime and container-selinux
- will pull in crun by default, runc users should install runc separately
  first or explicitly require runc

* Mon Apr 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-16
- containers-common-4:1-16
- use latest configs from upstream

* Fri Apr 09 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-15
- containers-common-4:1-15
- pull latest files from upstream

* Fri Mar 19 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-14
- correctly bump release tag this time

* Fri Mar 19 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-13
- containers-common-4:1-14
- also provide skopeo-containers
- bump release tag for smooth upgrade from f34
- use latest upstream files

* Thu Feb 18 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-12
- containers-common-4:1-10
- install shortnames.conf as 000-shrotnames.conf

* Mon Feb 15 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-11
- Remove registry.centos.org and add quay.io from registries.conf

* Mon Feb 15 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-10
- Update content

* Mon Feb 01 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-9
- remove unused policy.json

* Mon Feb 01 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-8
- containers-common-4:1-7
- use the correct policy.json file

* Thu Jan 28 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-7
- containers-common-4:1-6
- short-name-mode="enforcing" in registries.conf

* Thu Jan 28 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-6
- containers-common-4:1-5
- number sources in order

* Thu Jan 28 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-5
- containers-common-4:1-4
- Resolves: #1916922 - do not depend on subscription-manager
- reorder sources in alphabetical order

* Tue Jan 26 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-4
- remove unused macros

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-2
- correct typo

* Wed Jan 20 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-1
- containers-common-4:1-2
- bump version to random number
- no connection of package to github.com/containers/common
- add conf files to dist-git repo
- bring back update.sh

* Wed Jan 13 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:0.33.0-4
- containers-common-4:0.33.0-3
- copy source files into builddir and change them there before installation

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:0.33.0-3
- containers-common-4:0.33.0-2
- move update.sh code to spec file itself

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:0.33.0-2
- containers-common-4:0.33.0-1
- update registries.conf and other files
- source urls in update.sh

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:0.33.0-1
- bump epoch to 4

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:1-3
- containers-common-3:1-2
- update registries.conf and other files

* Mon Dec 14 2020 Jindrich Novy <jnovy@redhat.com> - 3:1-2
- containers-common-1-1.fc34
- initial build

* Tue May 18 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-1
- containers-common-4:1-19
- use container-selinux 2.162.1 and use latest configs

* Thu Apr 18 2024 Adam Williamson <awilliam@redhat.com> - 5:0.58.0-11
- Add a hard requirement on composefs for now

* Wed Apr 17 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-10
- local build

* Wed Apr 17 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-9
- Turn on composefs and convert_images=true

* Tue Apr 02 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-8
- local build

* Tue Apr 02 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-7
- Add support for additionalstore /usr/lib/containers/storage

* Tue Apr 02 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-6
- local build

* Tue Mar 26 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.58.0-5
- Conflict with podman older than 5.0 rc4 as we now have pasta default

* Wed Mar 20 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.58.0-4
- container-selinux should be a hard Requires

* Wed Mar 20 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-3
- local build

* Wed Mar 20 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.58.0-2
- Change default to zstd:chunked

* Wed Mar 13 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.58.0-1
- bump to v0.58.0

* Wed Mar 13 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.3-7
- make passt and netavark hard dependencies

* Fri Mar 01 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.3-6
- local build

* Fri Mar 01 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.3-5
- local build

* Fri Mar 01 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.3-4
- Update for podman 5.0

* Wed Feb 07 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.3-3
- remove cni-plugins dependency

* Thu Feb 01 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.3-2
- bump netavark dep

* Thu Feb 01 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.3-1
- bump to v0.57.3

* Tue Jan 30 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 5:0.57.1-8
- Build only on golang arches

* Mon Jan 29 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.1-7
- local build

* Mon Jan 29 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.1-6
- local build

* Sun Jan 28 2024 Daniel J Walsh <dwalsh@redhat.com> - 5:0.57.1-5
- local build

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5:0.57.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5:0.57.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.1-2
- containers.conf changes are common so far for all fedoras

* Fri Jan 05 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.57.1-1
- Use c/common upstream version for rpm with Epoch bump

* Sun Dec 10 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-101
- local build

* Thu Nov 09 2023 Brent Baude <bbaude@redhat.com> - 4:1-100
- Reverting zstd change to containers.conf

* Sun Nov 05 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-99
- Revert update.sh back to f39 version.

* Sun Nov 05 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-98
- local build

* Tue Oct 24 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-97
- local build

* Thu Sep 21 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-96
- local build

* Fri Aug 11 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-95
- local build

* Sat Jul 22 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-94
- local build

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-93
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 09 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-92
- local build

* Sun Jul 02 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-91
- local build

* Wed Apr 12 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-90
- extra subpackage depends netavark v1.6.0 or higher

* Mon Apr 10 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-89
- local build

* Mon Apr 10 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-88
- local build

* Tue Feb 21 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-87
- Resolves: #2170856 - add passt dependency

* Tue Feb 14 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 4:1-86
- Switch License to SPDX

* Wed Feb 01 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-85
- Suggests: qemu-user-static superseded by Recommends

* Tue Jan 31 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-84
- adjust qemu-user-static dependencies in containers-common-extra

* Thu Jan 26 2023 Daniel J Walsh <dwalsh@redhat.com> - 4:1-83
- local build

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-82
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Alexander Larsson <alexl@redhat.com> - 4:1-81
- Add /etc/containers/systemd and /usr/share/containers/systemd dirs

* Thu Dec 15 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-80
- Change container-selinux to a recommends

* Wed Nov 02 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-79
- install RPM-GPG-KEY-redhat-release only on fedora and centos environments

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-78
- add cni-plugins and qemu-user-static deps to containers-common-extra

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-77
- both buildah and podman require iptables and nftables

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-76
- add containers-common-extra subpackage

* Wed Oct 05 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-75
- local build

* Tue Oct 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-74
- remove debbuild macros to comply with fedora guidelines

* Fri Sep 23 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-73
- deb envs probably need an explicit provides, whatevs

* Fri Sep 23 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-72
- obsolete and provide golang-github-containers-[common|image] =
  %%{epoch}:%%{version}-%%{release}

* Fri Sep 23 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-71
- obsolete golang-github-containers-common in debian and ubuntu

* Tue Sep 13 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-70
- local build

* Sun Sep 04 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-69
- local build

* Tue Aug 16 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-68
- Fix debbuild maintainer field issue

* Tue Aug 16 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-67
- debbuild package conflicts with golang-github-containers-common

* Wed Aug 10 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-66
- local build

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-64
- Update man pages and config files

* Wed Jul 13 2022 Jonathan Wakely <jwakely@fedoraproject.org> - 4:1-63
- Fix missing markup in Containerfile.5 man page

* Mon Jun 13 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-62
- Revert "skip RPM-GPG-KEY-redhat-release installation on non-centos RHEL"

* Mon Jun 13 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-61
- skip RPM-GPG-KEY-redhat-release installation on non-centos RHEL

* Tue May 31 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-60
- local build

* Fri May 27 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-59
- build deb packages using debbuild

* Thu May 12 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-58
- local build

* Tue Apr 26 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-57
- local build

* Thu Apr 14 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-56
- Update man pages and config files

* Wed Mar 23 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-55
- local build

* Tue Mar 15 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-54
- comment out log_driver for rhel8 on copr

* Mon Feb 14 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-53
- fix build - don't delete what doesn't exist

* Mon Feb 14 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-52
- temporarily remove dockerfile manpages

* Tue Feb 08 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-51
- update config files

* Thu Feb 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-50
- Revert "handle md2man dep for c9s"

* Thu Feb 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-49
- handle md2man dep for c9s

* Wed Feb 02 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-48
- Check for docker manpage existence in %%post

* Tue Feb 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-47
- resolve docker manpage conflicts

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-46
- no error if man5 exists

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-45
- install containerfile and dockerfile manpages

* Wed Jan 26 2022 Daniel J Walsh <dwalsh@redhat.com> - 4:1-44
- Update man pages and config files

* Mon Jan 24 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-43
- Depend on container-network-stack and switch to autospec

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-41
- Update to grab latest man pages and configuration files

* Mon Nov 29 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-40
- Update to grab latest man pages and configuration files

* Mon Nov 08 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-39
- Update to grab latest man pages and configuration files

* Thu Oct 21 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-38
- Update to grab latest man pages and configuration files

* Thu Oct 07 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-37
- Update to grab latest man pages and configuration files

* Tue Oct 05 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-36
- Add .containerignore.5 link

* Fri Oct 01 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-35
- Update to grab latest man pages and configuration files

* Sun Sep 26 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-34
- Update to grab latest man pages and configuration files

* Mon Sep 20 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-33
- Update to grab latest man pages and configuration files

* Tue Sep 14 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-32
- Update to grab latest man pages and configuration files

* Wed Sep 08 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-31
- Update to grab latest man pages and configuration files

* Wed Aug 25 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-30
- Add memfd_secret to seccomp.json

* Thu Aug 12 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-29
- Update to grab latest man pages and configuration files

* Mon Jul 26 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-28
- Add support for signed RHEL images, enabled by default

* Mon Jul 26 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-27
- Add support for signed RHEL images, enabled by default

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-24
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Tue Jun 29 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-23
- containers-common-4:1-21
- fetch latest upstream configs

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-22
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-21
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> - 4:1-20
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
