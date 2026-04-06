## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
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
* Mon Apr 06 2026 azldev <> - 5:0.67.0-2
- Latest state for containers-common

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
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
