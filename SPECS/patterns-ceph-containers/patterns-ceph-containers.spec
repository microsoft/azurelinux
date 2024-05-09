Summary:        Patterns for the Ceph containers
Name:           patterns-ceph-containers
Version:        1.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Metapackages
URL:            https://en.opensuse.org/Patterns

%description
This is an internal package that is used to create the patterns as part
of the installation source setup. Installation of this package does
not make sense.

%package ceph_base
Summary:        Ceph base
Group:          Metapackages
Provides:       pattern() = ceph_base
Provides:       pattern-category() = Containers
Provides:       pattern-order() = 3000
Provides:       pattern-visible()
Requires:       ca-certificates
Requires:       ceph
Requires:       ceph-base
Requires:       ceph-common
Requires:       ceph-fuse
Requires:       ceph-grafana-dashboards
Requires:       ceph-mds
Requires:       ceph-mgr
Requires:       ceph-mgr-cephadm
Requires:       ceph-mgr-dashboard
# Following two package currently not supported in Azure Linux; keeping dependency for future reference.
#Requires:      ceph-mgr-rook
#Requires:      ceph-mgr-diskprediction-local
Requires:       ceph-mon
Requires:       ceph-osd
Requires:       ceph-prometheus-alerts
Requires:       ceph-radosgw
Requires:       cephadm
Requires:       e2fsprogs
Requires:       gptfdisk
Requires:       kmod
Requires:       lvm2
#Package currently not supported in mariner, keeping dependency for future reference.
#Requires: ceph-iscsi
Requires:       rbd-mirror
Requires:       rbd-nbd

%description ceph_base
This provides the base for the Ceph, Rook, Ceph CSI driver packages and containers.

%prep
# empty on purpose

%build
# empty on purpose

%files ceph_base

%changelog
* Tue Apr 23 2024 Andrew Phelps <anphel@microsoft.com> - 1.0-2
- Remove requirement on `ceph-mgr-rook`
- Remove non-applicable ExclusiveArch tags

* Mon Oct 04 2021 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.0-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License Verified
- Removed unused source file

* Mon Feb  1 2021 Nathan Cutler <ncutler@suse.com>
- Drop all nfs-ganesha packages from ceph-base:
  + nfs-ganesha
  + nfs-ganesha-ceph
  + nfs-ganesha-rgw
  + nfs-ganesha-rados-grace
  + nfs-ganesha-rados-urls

* Tue Jan 28 2020 Denis Kondratenko <denis.kondratenko@suse.com>
- Added nfs-ganesha-rados-urls to ceph_base

* Fri Dec 13 2019 Kristoffer Gronlund <kgronlund@suse.com>
- ceph-daemon was renamed to cephadm
- ceph-mgr-ssh was renamed to ceph-mgr-cephadm

* Thu Nov 28 2019 Kristoffer Gronlund <kgronlund@suse.com>
- Add missing dependencies to pattern

* Mon Jul 22 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Rename pattern according to the recomendations (replacing "-" with "_")

* Mon Jul 22 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Add missing packages (mgr) to the pattern

* Wed Jul 17 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Initial version
