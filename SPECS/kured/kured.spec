#
# spec file for package kured
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
# nodebuginfo


# Remove stripping of Go binaries.
%define __arch_install_post export NO_BRP_STRIP_DEBUG=true
# Project upstream commit.
%define commit 2b36eab
%global debug_package %{nil}
Summary:        Kubernetes daemonset to perform safe automatic node reboots
Name:           kured
Version:        1.9.1
Release:        14%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Management
URL:            https://github.com/weaveworks/kured
#Source0:       https://github.com/weaveworks/kured/archive/refs/tags/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/weaveworks/kured/archive/refs/tags/%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         kured-imagePullPolicy.patch
BuildRequires:  fdupes
BuildRequires:  go-go-md2man
BuildRequires:  golang
ExcludeArch:    s390

%description
Kured (KUbernetes REboot Daemon) is a Kubernetes daemonset that
performs safe automatic node reboots when the need to do so is
indicated by the package management system of the underlying OS.

- Watches for the presence of a reboot sentinel e.g. %{_localstatedir}/run/reboot-required

- Utilises a lock in the API server to ensure only one node reboots at a time

- Optionally defers reboots in the presence of active Prometheus alerts

- Cordons & drains worker nodes before reboot, uncordoning them after

%package k8s-yaml
Summary:        Kubernetes yaml file to run kured container
Group:          System/Management
BuildArch:      noarch

%description k8s-yaml
This package contains the yaml file requried to download and run the
kured container in a kubernetes cluster.

%prep
%setup -q
%patch0 -p1

%build
# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE1} --no-same-owner

# Build the binary.
export VERSION=%{version}
export COMMIT=%{commit}
go build \
   -mod vendor -v -buildmode=pie \
   -ldflags "-s -w -X main.gitCommit=$COMMIT -X main.version=$VERSION" \
   -o %{name} cmd/kured/*go

%install
# Install the binary.
install -D -m 0755 %{name} "%{buildroot}/%{_bindir}/%{name}"

# Build the man page from markdown documentation.
go-md2man -in README.md -out %{name}.1

# Install the man page.
install -D -m 0644 %{name}.1 "%{buildroot}/%{_mandir}/man1/%{name}.1"
rm %{name}.1

# Install provided yaml file to download and run the kured container
mkdir -p %{buildroot}%{_datadir}/k8s-yaml/kured
cat kured-rbac.yaml kured-ds.yaml > %{buildroot}%{_datadir}/k8s-yaml/kured/kured.yaml
chmod 644  %{buildroot}%{_datadir}/k8s-yaml/kured/kured.yaml
sed -i -e 's|image: .*|image: registry.opensuse.org/kubic/kured:%{version}|g' %{buildroot}%{_datadir}/k8s-yaml/kured/kured.yaml

%fdupes %{buildroot}

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_mandir}/man1/kured.1.*

%files k8s-yaml
%dir %{_datarootdir}/k8s-yaml
%dir %{_datarootdir}/k8s-yaml/kured
%{_datarootdir}/k8s-yaml/kured/kured.yaml

%changelog
* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.9.1-14
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.9.1-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.1-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.1-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.9.1-2
- Bump release to rebuild with golang 1.18.3

* Wed Feb 09 2022 Henry Li <lihl@microsoft.com> - 1.9.1-1
- Upgrade to version 1.9.1
- Remove systemctl-path.patch
- Update kured-imagePullPolicy.patch

* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.1-2
- Switching to using a single digit for the 'Release' tag.

* Fri Jun 18 2021 Henry Li <lihl@microsoft.com> 1.6.1-1.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License Verified
- Use golang as build dependency
- Remove {?ext_man}, which is not supported in CBL-Mariner
- Add %global debug_package %{nil} to resolve empty file error
- Use self-built go vendor source
- Add -v to the go build step

* Tue Feb  2 2021 kukuk@suse.com
- Update to version 1.6.1:
  - add additional parameters to override the drain/reboot slack messages
  - rename message template parameters so they are not related to slack
  - Improve coordinated reboot output
  - Add more logs into gates
  - Added support for time wrap in timewindow.Contains

* Tue Nov 24 2020 kukuk@suse.com
- Update to version 1.5.1:
  * rename annotation-ttl to lock-ttl in all places, follow-up to #213
  * Drain: allow pods grace period to terminate
  * Prepare 1.5.1 release
  * Add lint job
  * Make lint happier in pkg folder
  * Make lint happier
  * Remove prom-active-alerts
  * update docs following #210
  * run 'go mod tidy'
  * Replaced --annotationTTL with --lockTTL and made it work correctly
  * Refactor drain/uncordon
  * Remove kubectl exception in container scanning
  * Bump prometheus
  * Use kubectl as library instead of calling from cli
  * fix: Follow DKL-DI-0004 guideline
  * feat: Add security scanning into CI
  * add missing quote - thanks Karan Arora for reporting
  * Bump helm chart version
  * Remove quote for parameter alert-filter-regexp
  * Release helper

* Mon Sep 21 2020 kukuk@suse.com
- Update to version 1.5.0:
  * Prepare 1.5.0 release
  * Bump helm/kind-action from v1.0.0-rc.1 to v1.0.0
  * Bump helm/chart-testing-action from v1.0.0-rc.2 to v1.0.0
  * Add dependabot
  * Prepare for k8s release 1.19 (Aug 25)

* Fri Aug 14 2020 kukuk@suse.com
- Update to version 1.4.5:
  * document how releases are town wrt Helm bits
  * bump versions for 1.4.5 release
  * Use nindent, not indent
  * chart: update readme
  * Bump chart version
  * Add missing 'end'
  * Chart: Support extraEnvVars
  * update install instructions to use latest
  * update chart version
  * Prep for 1.4.4 release
  * bump and fix
  * split matchLabels template
  * restructured and improved service

* Tue Jun 30 2020 dmueller@suse.com
- Update to version 1.4.3:
  * bump and fix
  * split matchLabels template
  * restructured and improved service
  * bumped kured to upcoming 1.4.3 fixed servicemonitor indent fixed quotes for arguments
  * update things for 1.4.2 release
  * Use GITHUB_TOKEN for releasing chart
  * make markdownlint happier
  * update version
  * prepare chart-release for 1.4.1
  * Revert #139
- use obs-service for regenerating vendor.tar.gz

* Tue Jun 30 2020 Thorsten Kukuk <kukuk@suse.com>
- Update to version 1.4.2
  - Adding --annotation-ttl for automatic unlock
- Refresh vendor.tar.xz

* Mon May 18 2020 Thorsten Kukuk <kukuk@suse.com>
- kured-imagePullPolicy.patch: always update the image

* Sun May 17 2020 Thorsten Kukuk <kukuk@suse.com>
- systemctl-path.patch: last systemd update removed symlinks
  from /bin ...

* Mon May 11 2020 Thorsten Kukuk <kukuk@suse.com>
- Update to version 1.4.0
  - Updated kubectl, client-go, etc to k8s 1.17 (#127, #135)
  - Update to go 1.13 (#130)
  - print node id when commanding reboot (#134)

* Wed Apr 22 2020 Dominique Leuenberger <dimstar@opensuse.org>
- Fix build-dependency: we require golang(API) 1.12, not the exact
  go package version 1.12.

* Mon Mar  2 2020 Thorsten Kukuk <kukuk@suse.com>
- Update to version 1.3.0
  - Update k8s client tools to 1.15.x
  - Ad Slack channel name configuration
  - Add reboot window
- Obsoletes k8s-1.14.diff
- Remove kured-telemetrics.patch, chances that upstream accepts
  any third party code are nearly zero.
- Update vendor.tar.xz

* Mon Jun 24 2019 kukuk@suse.de
- k8s-1.14.diff: kubernetes 1.14.1 support from git

* Wed Jun  5 2019 kukuk@suse.de
- Fix path to image in manifest

* Wed May 22 2019 kukuk@suse.de
- Update to version 1.2.0
  - support newer kubernetes versions
- Adjust kured-telemetrics.patch
- Update vendor.tar.gz with recent versions

* Sat Apr  6 2019 kukuk@suse.de
- Enable building on s390x

* Thu Mar 28 2019 Jan Engelhardt <jengelh@inai.de>
- Combine %%setup calls.

* Thu Mar 28 2019 kukuk@suse.de
- kured-telemetrics.patch: add hooks for telemetrics data
- Renamed kured-yaml to kured-k8s-yaml to follow new policy

* Thu Feb 28 2019 kukuk@suse.de
- Change path in yaml file to point to official container image

* Fri Jan 18 2019 kukuk@suse.de
- Create a correct yaml file to download and run the kured container
  image in a kubernetes cluster
- Create new subpackage containing only the yaml file, so that
  people using the container don't need to install the not needed
  full package.

* Thu Nov 15 2018 Jeff Kowalczyk <jkowalczyk@suse.com>
- Update to kured 1.1.0
- Upstream bumped dependency on go1.10 via dependency k8s.io/client-go 0.9.0
  https://github.com/kubernetes/client-go
- Provide dependencies in separate vendor.tar.gz
- Improvements
  * RBAC support
  * Use the systemctl in the host mount namespace to effect reboots, reducing
    image size and eliminating the potential for incompatibility
  * Notify Slack on drain in addition to reboot
  * Pass through log output from invoked kubectl commands
  * Tolerate NoSchedule taint on node-role.kubernetes.io/master
  * Fixed reversal of daemonset name/namespace arguments and comments in the
    manifest
- Kubernetes Version Compatibility
  * The daemon image contains a 1.12.x k8s.io/client-go and kubectl binary for
    the purposes of maintaining the lock and draining worker nodes. Kubernetes
    aims to provide forwards & backwards compatibility of one minor version
    between client and server, so this should work on 1.11.x and 1.13.x.
  * Tested in minikube on 1.11.4, 1.12.1 & 1.13.0-alpha.2
  * Tested in production on 1.11.2 & 1.12.2

* Thu Sep 13 2018 jkowalczyk@suse.com
- Remove hardcoded GOARCH=amd64 and GOOS=linux
- Revise go build arg -ldflags and add -buildmode=pie
- Together these fix rpmlint warnings:
  * position-independent-executable-suggested
  * statically-linked-binary
- Upstream kured project code imports package as 'context'. Bump BuildRequires
  to go1.7 wherein import path for package context graduates from
  'golang.org/x/net/context' to the standard library as 'context'.
  https://golang.org/doc/go1.7#context
- Bump release number

* Wed Sep 12 2018 jkowalczyk@suse.com
- Initial packaging of upstream master branch @ 5731b98 (tagged 1.0.0 + 24)
- Include 24 commits since release 1.0.0 updating kubernetes version support
- Dependency sources vendored via dep ensure per upstream build instructions
- Man page converted from README.md, some HTML formatting artifacts present
- rpmlint warning: position-independent-executable-suggested
  * go1.11 currently in review status supports option -buildmode=pie
- rpmlint warning: statically-linked-binary
  * Go binaries are generally statically linked
