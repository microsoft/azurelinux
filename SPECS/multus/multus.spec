#
# spec file for package multus
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Summary:        CNI plugin providing multiple interfaces in containers
Name:           multus
Version:        4.0.2
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Management
URL:            https://github.com/intel/multus-cni
Source0:        https://github.com/k8snetworkplumbingwg/multus-cni/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define commit efdc0a5c7d1ea4bb236d638403420448b48782b3
BuildRequires:  golang
BuildRequires:  golang-packaging

%description
Multus is a CNI plugin which provides multiple network interfaces in
containers. It allows to use many CNI plugins at the same time and supports all
plugins which implement the CNI specification.

%package k8s-yaml
Summary:        Kubernetes yaml file to run Multus containers
Group:          System/Management

%description k8s-yaml
Multus is a CNI plugin which provides multiple network interfaces in
containers. It allows to use many CNI plugins at the same time and supports all
plugins which implement the CNI specification.

This package contains the yaml file requried to download and run Multus
containers in a Kubernetes cluster.

%prep
%autosetup -p1 -n %{name}-cni-%{version}

%build
VERSION=%{version} COMMIT=%{commit} ./hack/build-go.sh

%install
install -D -m0755 bin/multus %{buildroot}%{_bindir}/multus
install -D -m0755 images/entrypoint.sh %{buildroot}%{_bindir}/multus-entrypoint
install -D -m0644 images/multus-daemonset-crio.yml %{buildroot}%{_datadir}/k8s-yaml/multus/multus.yaml

%files
%license LICENSE
%doc README.md
%{_bindir}/multus
%{_bindir}/multus-entrypoint

%files k8s-yaml
%dir %{_datarootdir}/k8s-yaml
%dir %{_datarootdir}/k8s-yaml/multus
%{_datarootdir}/k8s-yaml/multus/multus.yaml

%changelog
* Thu Sep 28 2023 Aditya Dubey <adityadubey@microsoft.com> - 4.0.2-1
- Upgrade to v4.0.2

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8-13
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 3.8-12
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8-11
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8-10
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8-9
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8-8
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8-7
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8-6
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8-5
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.8-4
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.8-3
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.8-2
- Bump release to rebuild with go 1.18.8

* Wed Sep 07 2022 Yash Panchal <yashpanchal@microsoft.com> - 3.8-1
- License verified
- Initial changes to build for Mariner
- Initial CBL-Mariner import from openSUSE TumbleWeed (license: same as "License" tag)

* Fri Jan 08 2021 Richard Brown rbrown@suse.com
- Update to version 3.6:
  * Remove obsolete 0001-build-Allow-to-define-VERSION-and-COMMIT-without-git.patch
  * Remove obsolete multus-override-build-date.patch
  * Update vendors
  * Fix error handling on cmdDel
  * Allow to override build date with SOURCE_DATE_EPOCH
  * Add infinibandGUID runtime config to delegate netconf
  * Struct updates
  * build: Enable -mod build flag to be toggled via environment variable
  * Add support for log rotation
  * README typo for roll-YOUR-own
  * Fix network status name/namespace to compliant with multi-net-spec
  * Adds code of conduct
  * Change the error handling for kubernetes client
  * Add deviceid in clusterNetwork
  * Simplify examples directory
  * Introduce gopkg.in for go module
  * Move pre-1.16 Kubernetes assets to a deprecated folder (to later remove)
  * Simplify error message in case of delegating CNI error
  * Adds development docs note regarding issue policy
  * Sets the Kubernetes API calls timeout to 60 seconds
  * Allows namespaceIsolation to allow pods in any namespace refer to the default namespace
  * Skip docker push action if REPOSITORY_PASS is not set
  * Add error message in case of unexpected situation
  * Check Pod parameter against nil before calling Eventf
  * Updates Dockerfile to golang 1.13 (specifying version)
  * Fix pre 1.16 api version for CRDs

* Wed Jul 8 2020 Bernhard Wiedemann <bwiedemann@suse.com>
- Add multus-override-build-date.patch to override build date (boo#1047218)

* Fri Oct 25 2019 Michał Rostecki <mrostecki@opensuse.org>
- Update to version 3.3:
  * This release updates for parameters necessary to properly
    create a CNI configuration under Kubernetes 1.16, among other
    recent stability fixes.
- Add multus-k8s-yaml package which provides the Kubernetes yaml
  file to run Multus containers.
- Add patch which fixes the build from tarball:
  * 0001-build-Allow-to-define-VERSION-and-COMMIT-without-git.patch

* Tue Nov 27 2018 Michał Rostecki <mrostecki@suse.de>
- Initial version 3.1
  * Update test.sh with coveralls job inclusion
  * coveralls code coverage during Travis CI run, adds CI badges
  * Fix glide.yaml
  * fixing the cmddel fix code
  * handling the multiple cmd del call from kubelet
  * Add debug log for newly added functions.
  * Convert bytes to string in Debugf()
  * Add logging message for debug/error
  * Enable hairpin in the multus config
  * adding error checking in network status creation as well
