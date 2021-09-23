#
# spec file for package patterns-ceph-containers
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           patterns-ceph-containers
Version:        1.0
Release:        bp153.1.5
Summary:        Patterns for the Ceph containers
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Metapackages
Url:            http://en.opensuse.org/Patterns
Source0:        %{name}-rpmlintrc
ExclusiveArch:  x86_64 aarch64 ppc64le s390x

%description
This is an internal package that is used to create the patterns as part
of the installation source setup. Installation of this package does
not make sense.

%package ceph_base
Summary:        Ceph base
Group:          Metapackages
Provides:       pattern() = ceph_base
Provides:       pattern-icon()
Provides:       pattern-category() = Containers
Provides:       pattern-order() = 3000
Provides:       pattern-visible()
Requires:       ceph
Requires:       ceph-base
Requires:       ceph-common
Requires:       ceph-fuse
Requires:       cephadm
Requires:       ceph-grafana-dashboards
Requires:       ceph-mds
Requires:       ceph-mgr
Requires:       ceph-mgr-rook
Requires:       ceph-mgr-cephadm
Requires:       ceph-mgr-dashboard
Requires:       ceph-mgr-diskprediction-local
Requires:       ceph-mon
Requires:       ceph-osd
Requires:       ceph-prometheus-alerts
Requires:       ceph-radosgw
Requires:       ceph-iscsi
Requires:       rbd-mirror
Requires:       rbd-nbd
Requires:       ca-certificates
Requires:       e2fsprogs
Requires:       kmod
Requires:       lvm2
Requires:       gptfdisk

%description ceph_base
This provides the base for the Ceph, Rook, Ceph CSI driver packages and containers.

%prep
# empty on purpose

%build
# empty on purpose

%install
mkdir -p %buildroot/usr/share/doc/packages/patterns-ceph-containers/
echo 'This file marks the pattern ceph-base to be installed.' >%buildroot/usr/share/doc/packages/patterns-ceph-containers/ceph_base.txt

%files ceph_base
%defattr(-,root,root)
%dir %{_docdir}/patterns-ceph-containers
%{_docdir}/patterns-ceph-containers/ceph_base.txt

%changelog
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