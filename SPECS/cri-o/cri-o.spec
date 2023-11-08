#
# spec file for package cri-o
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
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


%define debug_package %{nil}
%define project github.com/cri-o/cri-o
#Compat macro for new _fillupdir macro introduced in Nov 2017
%if ! %{defined _fillupdir}
  %define _fillupdir %{_var}/adm/fillup-templates
%endif
Summary:        OCI-based implementation of Kubernetes Container Runtime Interface
# Define macros for further referenced sources
Name:           cri-o
Version:        1.21.2
Release:        18%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/cri-o/cri-o
#Source0:       https://github.com/%{name}/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/cri-o/cri-o/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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
Source2:        crio.service
Source3:        sysconfig.crio
Source4:        crio.conf
Source5:        cri-o-rpmlintrc
Source6:        kubelet.env
BuildRequires:  btrfs-progs-devel
BuildRequires:  device-mapper-devel
BuildRequires:  fdupes
BuildRequires:  glib2-devel
BuildRequires:  glibc-devel
BuildRequires:  golang
BuildRequires:  golang-packaging
BuildRequires:  gpgme-devel
BuildRequires:  libapparmor-devel
BuildRequires:  libassuan-devel
BuildRequires:  libseccomp-devel
BuildRequires:  sed
BuildRequires:  systemd-rpm-macros
Requires:       cni
Requires:       cni-plugins
Requires:       conmon
Requires:       conntrack-tools
Requires:       iproute
Requires:       iptables
Requires:       libcontainers-common >= 0.0.1
Requires:       moby-runc
Suggests:       katacontainers
# Provide generic cri-runtime dependency (needed by kubernetes)
Provides:       cri-runtime = %{version}-%{release}
ExcludeArch:    i586

%description
CRI-O provides an integration path between OCI conformant runtimes
and the kubelet. Specifically, it implements the Kubelet Container Runtime
Interface (CRI) using OCI conformant runtimes. The scope of CRI-O is tied to
the scope of the CRI.

%package kubeadm-criconfig
Summary:        CRI-O container runtime configuration for kubeadm
# Temporarily comment out this line as kubernetes is not supported
# CBL-Mariner yet. Will fix this once kubernetes gets supported
#Requires:       kubernetes-kubeadm-provider
Requires(post): %fillup_prereq
Supplements:    cri-o
Conflicts:      docker-kubic-kubeadm-criconfig
Provides:       kubernetes-kubeadm-criconfig

%description kubeadm-criconfig
This package provides the CRI-O container runtime configuration for kubeadm

%prep
%setup -q

%build
tar -xf %{SOURCE1} --no-same-owner

# We can't use symlinks here because go-list gets confused by symlinks, so we
# have to copy the source to $HOME/go and then use that as the GOPATH.
export GOPATH=$HOME/go
mkdir -pv $HOME/go/src/%{project}
rm -rf $HOME/go/src/%{project}/*
cp -avr * $HOME/go/src/%{project}
cd $HOME/go/src/%{project}

# Build crio
GO_BUILD="go build -mod vendor" make

%install
cd $HOME/go/src/%{project}

# Binaries
install -D -m 0755 bin/crio    %{buildroot}/%{_bindir}/crio
install -D -m 0755 bin/crio-status    %{buildroot}/%{_bindir}/crio-status
install -D -m 0755 bin/pinns    %{buildroot}/%{_bindir}/pinns
install -d %{buildroot}/%{_libexecdir}/crio/bin
# Completions
install -D -m 0644 completions/bash/crio %{buildroot}/%{_datadir}/bash-completion/completions/crio
install -D -m 0644 completions/zsh/_crio %{buildroot}%{_sysconfdir}/zsh_completion.d/_crio
install -D -m 0644 completions/fish/crio.fish %{buildroot}/%{_datadir}/fish/completions/crio.fish
install -D -m 0644 completions/bash/crio-status %{buildroot}/%{_datadir}/bash-completion/completions/crio-status
install -D -m 0644 completions/zsh/_crio-status %{buildroot}%{_sysconfdir}/zsh_completion.d/_crio-status
install -D -m 0644 completions/fish/crio-status.fish %{buildroot}/%{_datadir}/fish/completions/crio-status.fish
# Manpages
install -d %{buildroot}/%{_mandir}/man5
install -d %{buildroot}/%{_mandir}/man8
install -m 0644 docs/crio.conf.5 %{buildroot}/%{_mandir}/man5
install -m 0644 docs/crio.8      %{buildroot}/%{_mandir}/man8
# Configs
sed -e 's-@LIBEXECDIR@-%{_libexecdir}-g' -i %{SOURCE4}
install -D -m 0644 %{SOURCE4}       %{buildroot}/%{_sysconfdir}/crio/crio.conf.d/00-default.conf
install -D -m 0644 crio-umount.conf %{buildroot}/%{_datadir}/oci-umount/oci-umount.d/cri-umount.conf
install -D -m 0644 %{SOURCE3}       %{buildroot}%{_fillupdir}/sysconfig.crio
# Systemd
install -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/crio.service
# place kubelet.env in fillupdir
install -D -m 0644 %{SOURCE6} %{buildroot}%{_fillupdir}/sysconfig.kubelet
# Symlinks to rc files
install -d -m 0755 %{buildroot}%{_sbindir}
ln -sf service %{buildroot}%{_sbindir}/rccrio

%fdupes %{buildroot}/%{_prefix}

%post
%systemd_post crio.service
# This is the additional directory where cri-o is going to look up for CNI
# plugins installed by DaemonSets running on Kubernetes (i.e. Cilium).
mkdir -p /opt/cni/bin

%post kubeadm-criconfig
%fillup_only -n kubelet

%preun
%systemd_preun crio.service

%postun
%systemd_postun_with_restart crio.service

%files
# Binaries
%{_bindir}/crio
%{_bindir}/crio-status
%{_bindir}/pinns
%dir %{_libexecdir}/crio
%dir %{_libexecdir}/crio/bin
# Completions
%{_datadir}/bash-completion/completions/crio
%{_datadir}/bash-completion/completions/crio-status
%{_sysconfdir}/zsh_completion.d
%{_sysconfdir}/zsh_completion.d/_crio
%{_sysconfdir}/zsh_completion.d/_crio-status
%{_datadir}/fish
%{_datadir}/fish/completions
%{_datadir}/fish/completions/crio.fish
%{_datadir}/fish/completions/crio-status.fish
# Manpages
%{_mandir}/man5/crio.conf.5*
%{_mandir}/man8/crio.8*
# License
%license LICENSE
# Configs
%dir %{_sysconfdir}/crio
%dir %{_sysconfdir}/crio/crio.conf.d
%config %{_sysconfdir}/crio/crio.conf.d/00-default.conf
%dir %{_datadir}/oci-umount
%dir %{_datadir}/oci-umount/oci-umount.d
%{_datadir}/oci-umount/oci-umount.d/cri-umount.conf
%{_fillupdir}/sysconfig.crio
# Systemd
%{_unitdir}/crio.service
%{_sbindir}/rccrio

%files kubeadm-criconfig
%defattr(-,root,root)
%{_fillupdir}/sysconfig.kubelet

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21.2-18
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.21.2-17
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21.2-16
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21.2-15
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21.2-14
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21.2-13
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21.2-12
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21.2-11
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21.2-10
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21.2-9
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.21.2-8
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.21.2-7
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.21.2-6
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.21.2-5
- Bump release to rebuild with golang 1.18.3

* Mon Apr 25 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.21.2-4
- Replace openSUSE systemd macros with upstream systemd macros

* Wed Sep 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.21.2-3
- Added missing BR on "systemd-rpm-macros".

* Thu Aug 19 2021 Henry Li <lihl@microsoft.com> - 1.21.2-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag)
- License Verified
- Use prebuilt go vendor source
- Use mariner packages as build/runtime requirements
- Remove macros that are not supported in CBL-Mariner
- Remove patterns-base-apparmor from Requires
- Add %define debug_package %{nil}

* Fri Jul 23 2021 alexandre.vicenzi@suse.com
- Update to version 1.21.2:
  * oci: be more precise about channels and routines
  * oci: wait for runtime to write pidfile before starting timer
  * oci: refactor fsnotify usage
  * vendor: add notify package
  * version: bump to v1.21.2
  * server: use cnimgr to wait for cni plugin ready before creating a pod
  * server: use cnimgr for runtime status
  * config: add cnimgr
  * Introduce cnimgr
  * server: prevent segfault by not using a potentially nil sandbox
  * network: pass pod UID to ocicni when performing network operations
  * vendor: bump ocicni to 4ea5fb8752cfe
  * Bump c/storage to v1.32.3
  * oci: kill runtime process on exec if exec pid isn't written yet
  * oci: don't pre-create pid file
  * dbus: update retryondisconnect to handle eagain too
  * simplify checking for dbus error
  * utils: close dbus conn channel
  * dbusmgr: protect against races in NewDbusConnManager
  * cgmgr: reuse dbus connection
  * cgmgr: create systemd manager constructor
  * try again on EAGAIN from dbus
  * test: fix cgroupfs workload tests
  * Disable short name mode
  * workloads: don't set conmon cpuset if systemd doesn't support AllowedCPUs
  * test: add test for conmon in workloads
  * workloads: setup on conmon cgroup
  * Bump runc to get public RangeToBits function
  * server: export InfraName and drop references to leaky
  * storage: succeed in DeleteContainer if container is unknown
  * bump to v1.21.1
  * Fix CI
  * oci: drop internal ExecSync structs
  * oci: do not use conmon for exec sync
  * bump c/storage to 1.31.1
  * bump runc to 1.0.0-rc94
  * Fix unit tests
  * Add support to drop ALL and add back few capabilities
  * server: call CNI del in separate routine in restore
  * server: reduce log verbosity on restore
  * reduce listen socket permissions to 0660
  * test: adapt crio wipe tests to handle new behavior
  * ignore storage.ErrNotAContainer
  * move internal wipe to only wipe images
  * server: properly remove sandbox network on failed restore
  * runtimeVM: Use internal context to ensure goroutines are stopped
  * Fix go.sum
  * sandbox remove: unmount shm before removing infra container
  * use more ContainerServer.StopContainer
  * sandbox: fix race with cleanup
  * server: don't unconditionally fail on sandbox cleanup
  * server: group namespace cleanup with network stop
  * resourcestore: run cleanup in parallel
  * test: add test for delayed cleanup of network on restart
  * InternalWipe: retry on failures
  * server: get hooks after we've check if a sandbox is already stopped
  * server: move newPodNetwork to a more logical place
  * Add resource cleaner retry functionality
  * test: add test for internal_wipe
  * server: add support for internal_wipe
  * crio wipe: add support for internal_wipe
  * config: add InternalWipe
  * server: breakup stop/remove all functions with internal helpers
  * storage: remove RemovePodSandbox function
  * server: reuse container removal code for infra
  * Cleanup pod network on sandbox removal
  * test: add test for absent_mount_sources_to_reject
  * server: add support for absent_mount_sources_to_reject
  * config: add absent_mount_sources_to_reject option
  * server: use background context for network stop
  * resource store: prevent segfault on cleanup step
  * Pin gocapability to v0.0.0-20180916011248-d98352740cb2
  * config: fix type of privileged_without_host_devices
  * Fix podman name in README
  * Fix RuntimeDefault seccomp behavior if disabled
  * Add After=crio.service dependency to containers and conmon
  * Use extra context for runtime VM
  * workloads: move to more concrete type
  * workloads: update how overrides are specified
  * main: still rely on logrus (rather than using the internal log)
  * container server: fix silly typo
  * nsmgr: remove duplicate IsNSOrErr call
  * nsmgr: fix some leaks with GetNamespace
  * bump to containers/image 5.11.1
  * Bug 1942608: do not list the image with error locating manifest
  * runtimeVM: Calculate the WorkingSetBytes stats
  * runtimeVM: Use containerd/cgroups for metrics
  * runtimeVM: Move metricsToCtrStats() around
  * runtimeVM: Vendor typeurl instead of maintain our own copy

* Thu Apr 15 2021 alexandre.vicenzi@suse.com
- Update to version 1.21.0:
  * bump to v1.21.0
  * config: drop registries field as it is no longer supported
  * Revert "test: drop unneeded sed statement"
  * WIP: add debug print
  * test: drop unneeded sed statement
  * config: fix template insecure_registries field
  * config: drop commented config lines
  * build(deps): bump google.golang.org/grpc from 1.36.1 to 1.37.0
  * Bump OpenShift CI cri-tools version and fix build path
  * build(deps): bump github.com/containers/image/v5 from 5.10.5 to 5.11.0
  * Bump cri-tools to v1.21.0
  * Update Kubernetes to v1.21.0
  * Add container out of memory metrics
  * [CLI] "crio config" only prints the fields that are differet than the default.
  * Set short name mode to permissive
  * docs-validation: update to handle workloads
  * Fix unnecessary conversion lint report
  * add tests for workloads
  * integrate with server
  * config: update workloads structure
  * Clarify release cadence and version skew
  * Add correct start time to initial log output
  * Add support for workload settings
  * refactor handling of allowed_annotations
  * Do not push main binary into cachix cache
  * resourcestore: introduce ResourceCleaner
  * Use internal logging when context available
  * build(deps): bump github.com/coreos/go-systemd/v22 from 22.3.0 to 22.3.1
  * server: remove dead code
  * sandbox: use defined CRI type for NamespaceOption
  * config: remove dead code
  * oci: remove dead code
  * lib: remove dead code
  * build(deps): bump github.com/containers/podman/v3
  * build(deps): bump k8s.io/client-go from 0.20.1 to 0.20.5
  * update pause image to 3.5 for non-root
  * build(deps): bump github.com/soheilhy/cmux from 0.1.4 to 0.1.5
  * build(deps): bump google.golang.org/grpc from 1.34.0 to 1.36.1
  * build(deps): bump github.com/containers/buildah from 1.19.8 to 1.20.0
  * build(deps): bump github.com/prometheus/client_golang
  * build(deps): bump github.com/godbus/dbus/v5 from 5.0.3 to 5.0.4
  * build(deps): bump k8s.io/cri-api from 0.20.1 to 0.20.5
  * build(deps): bump github.com/containers/podman/v3
  * build(deps): bump k8s.io/kubernetes from 1.13.0 to 1.20.5
  * crio-wipe: only clear storage if CleanShutdownFile is supported
  * Add static bundle node e2e tests to GitHub actions
  * Reload the main config file when reloading configs
  * crio wipe: only completely wipe storage after a reboot
  * Bump static binary dependency versions
  * Add dependabot config file
  * runtimeVM: Fix shimv2 binary name construction
  * config,runtimeVM: Improve runtime_path validation
  * oci_test: Add basic coverage to "RuntimeType()"
  * oci_test: Add basic coverage to "privileged_without_host_devices"
  * oci_test: Leave invalidRuntime on its own line
  * tweak scope dependencies
  * Do not return `<none>` placeholders for images any more
  * Fix invalid libcontainer GetExecUser call
  * Update dependencies
  * config: Don't fail if the non default runtime doesn't pass validation
  * Remove check for CI env variable for release-notes and dependencies
  * cgmgr: add CreateSandboxCgroup method
  * inspect: send container PID for dropped infra sandbox
  * oci: specify sbox id when creating spoofed container
  * Run GitHub actions on release branches
  * Update bats to v1.3.0 (#4661)
  * use happy-eyeballs for port-forwarding
  * fix mock issues
  * fix lint issues
  * install: drop support matrix and update instructions
  * do not store context in runtime vm
  * Fix lint GitHub action
  * pkg/container: take process args
  * Use and publish version marker for CRI-O
  * Add GitHub API pages support to `get` script
  * add libbtrfs-dev to unit tests
  * Revert "server: use IsAlive() more"
  * Fix GitHub actions cache key
  * Bug 1881694: Add pull source as info level log
  * test: use latest conmon
  * runtime_vm: Create the global fifo inside the runtime root path
  * stats: fix log spam
  * Support CRI seccomp security profiles
  * oci: add unit tests for stop timeouts
  * oci: don't update stop timeout if it's earlier than old one
  * oci: update timeout even if we're ignoring kill
  * oci: don't wait too long on a long stop
  * oci: check process is still around with kill
  * Add integration test for started/finished container time
  * fix: Don't set `image-endpoint` in crictl config
  * feat: Add CLI option to set registries.conf.d path
  * Add allowed io.containers.trace-syscall annotation to static bundle
  * Make `get` script independent from `make`
  * test: correct the env variable for dropping the infra container
  * Add metric to grab latency of individual cri calls
  * Fix `get` script commit SHA retrieval
  * Add arm64 static build to GitHub actions
  * Fix GitHub actions workflow syntax
  * Updates yq commnands for yq v4
  * gh-actions:  also run on release branches
  * pkg/sandbox: add InitInfraContainer endpoint
  * test: reconfigure how runtimes are passed in
  * test: add runtime() function
  * sandbox/container: drop context
  * test: drop workaround for crun
  * pkg/sandbox: cleanup unused funcs/files
  * fix doc log_level adding trace option
  * Fix oci container update config
  * Update e2e-aws logic for 4.8
  * nsmgr: take Initalize method
  * Switch to go 1.16 for GitHub actions and remove scripts/build-test-image
  * config: remove and create the correct dir
  * Update nix pin with `make nixpkgs`
  * server: mount cgroup with rslave
  * crio wipe: ensure a clean shutdown
  * Move integration tests to GitHub actions
  * Run release-notes GitHub action after dependencies
  * Bumps github.com/containers/ocicrypt from 1.0.3 to 1.1.0.
  * config/node: refactor checking for CollectMode
  * Fix GitHub actions checkout permissions
  * change binary version to 1.21.0-dev
  * Set conmon scope KillSignal to SIGPIPE
  * Move repo modification jobs to GitHub actions
  * bump protobuf to 1.3.2
  * Log container stop timeout
  * ResourceStore: add close method
  * Allow seccomp hook tracing for separate containers
  * ResourceStore: extend tests to test WatcherForResource
  * ResourceStore: update tests to all run
  * ResourceStore: update docs for WatcherForResource
  * ResourceStore: don't segfault
  * server: support setting raw unified cgroupv2 settings
  * vendor: update runtime-specs
  * cgroup: implement fix for swap memcg on cgroup v2
  * server: leave swap mem limit unset if not supported
  * test: skip ServiceAccountIssuerDiscovery test
  * hostport manager clean up host ports
  * allows stream timeout to be set from config
  * config: pre-create pinns directories
  * Bump containers image to v5.10.1
  * Move unit tests to GitHub actions
  * Move go1.14 and 386 builds to GitHub actions
  * set kubelet node IP
  * Fix validate-completions GitHub action
  * Add integration test for pprof over unix socket
  * Add a flag for enabling profile over unix socket
  * Lookup echo command for unit tests
  * Move static build to GitHub actions
  * pinns: Fixup 'pwarn' output to match 'pwarnf' output
  * pinns: Don't put errno in the exit message for argument checks
  * nsmgr: use host option
  * nsmgr: Use config struct for NewPodNamespaces
  * pinns: support pinning host ns
  * Remove implicit GitHub action `name` fields
  * Move docs and completions validation to GitHub actions
  * Bump golangci-lint to v1.35.2
  * Make config tests work rootless
  * Make rootless namespace unit test execution work
  * config: fix template to show infra_ctr_cpus option
  * Do not log file path on ioutil.ReadFile
  * fixes version_test.go
  * Close the stdin/tty on server start to avoid shortname prompts
  * docs: fix http link
  * docs: update kubeadm tutorial
  * Fix `make lint`
  * Return runtime API version based on protocol
  * Update compatibility matrix to mention v1.20
  * add method comment
  * restore irqbalance config only on system restart
  * add blurb in doc and more informative name for unit tests
  * add is-enabled check for irqbalance service
  * fix unit tests
  * add unit tests
  * fix bash/zsh completions
  * fix the docs validation
  * handle irqbalance service
  * runtime_vm: set finished time when containers stop
  * nsmgr: fix/add calls to GetNamespace
  * managed namespaces: move to dedicated package
  * Provide integration test for infra-ctr-cpuset feature
  * Set CPUs for the infra containers during the creation
  * Add shell completion for infra-containers-cpu flag
  * Add new infra-containers-cpus to the CLI and config file
  * refine `registries` deprecation message
  * Circle CI: install test/registries.conf
  * crio.8.md: runroot defaults to /run/containers/storage
  * support short-name aliases
  * pull: do check for blocked registries
  * config: deprecate registries
  * Rollback gocapability vendor bump
  * vendor: bump containers/storage to v1.24.4
  * Update nix pin with `make nixpkgs`
  * contrib/test/int: add Kata Containers runtime support
  * contrib/test/int: enforce linking in parallel build process
  * contrib/test/int: build parallel from sources in CentOS
  * contrib/test/int: allow to skip user namespace testing
  * contrib/test/int: allow to configure test timeout
  * Capitalize Kubernetes
  * modify the error url of podctl
  * Add Digital Science to adopters
  * crio.service: Request to be run before kubelet.service
  * pinns: make binary not always static
  * server: use IsAlive() more
  * Support CRI v1 and v1alpha2 at the same time
  * drop support for ManageNSLifecycle
  * test/timeout.bats: increase timeout to fix flakes
  * release-notes: fix flags
  * test/timeout.bats: fix comments
  * int/resourcestore: fix comment about Put
  * test/image.bats: simplify some loops
  * test/helpers.bats: simplify cleanup_*
  * contrib/test/int: rm node-e2e test
  * contrib/test/int: fix iptables rule
  * critest: add unix:// prefix
  * critest.yml: don't skip test on RHEL
  * test: add timeout.bats
  * bump network creation timeout to 5 minutes
  * resourcecache: add watcher idiom
  * server: use ResourceCache instead of dropping progress
  * Add unit tests for ResourceCache
  * Introduce ResourceCache
  * moves shmsize to a handler allowed annotation
  * image pull: close progress chan
  * test/ctr.bats: fix a "ctr execsync" flake
  * Fix the functions' name in completions
  * make: drop link to crio.service
  * test: rm "run ctr with image with Config.Volumes"
  * test: add no-pull-on-run=true
  * test/devices.bats: fix "additional device permissions" case
  * test/devices.bats: rm unneeded run
  * test/devices.bats: skip earlier
  * Bandwidht CNI plugin reserved an upper limit on burst,in which banned include boundary. See: https://github.com/containernetworking/plugins/blob/v0.8.7/plugins/meta/bandwidth/main.go#L113
- Drop config-fix-tz.patch as upstream dependency was patched

* Fri Apr  9 2021 alexandre.vicenzi@suse.com
- Update to version 1.20.2:
  * bump to latest c/storage 1.24 branch
  * Remove check for CI env variable for release-notes and dependencies
  * fix lint
  * test: pin cri-tools to 1.20
  * bump to v1.20.2
  * Run GitHub actions on release branches
  * Pin gocapability to v0.0.0-20180916011248-d98352740cb2
  * [PATCH 9/9] add method comment
  * [PATCH 8/9] restore irqbalance config only on system restart
- Add vendor.tar.gz to avoid dependency downloads
- Add config-fix-tz.patch to fix crio validation error while building

* Fri Jan  8 2021 rbrown@suse.com
- Update to version 1.19.1:
  * bump to v1.19.1
  * don't do unnecesary iptables restore
  * switch CRI-O to use its own hostport manager
  * dual-stack host port manager
  * fix upstream hostport manager
  * Add README to hostport folder
  * fork hosport kubernetes code
  * [1.19] vendor: bump containers/storage to v1.20.5
  * runtime_vm: Ensure closeIOChan is not nil inside CloseStdin's function
  * runtime: parse oom file for VM type runtimes
  * runtime_vm: Ignore ttrpc.ErrClosed when removing a container
  * runtime_vm: StopContainers() should not fail when the VM is shutdown
  * runtime_vm: Don't let wait() return ttrpc.ErrClosed
  * runtime_vm: Fix updateContainerStatus() logic
  * runtime_vm: set Pid and InitPid for VM runtimes
  * internal/config/node: add checkFsMayDetachMounts
  * Fix bogus CI test failures
  * test/config: fix shellcheck warning
  * test/config: fix "config dir should fail with invalid option"
  * server: cleanup container in runtime after failed creation

* Tue Sep 15 2020 Sascha Grunert <sgrunert@suse.com>
- API Change
  - CRI-O now manages namespace lifecycles by default
- Feature
  - Add --version-file-persist, a place to put the version file in
    persistent storage. Now, crio wipe wipes containers if
  - -version-file is not present
  - Add big_files_temporary_dir to allow customization of where
    large temporary files are put
  - Add build support for setting SOURCE_DATE_EPOCH
  - Added `--metrics-socket`/`metrics_socket` configuration option
    to allow exposing the metrics endpoint on a local socket path
  - Added `crio_image_layer_reuse` metric which counts layer reuses
    during image pull
  - Added `privileged` field to container status `info`
  - Added behavior to allow filtering by a partial Pod Sandbox ID
  - Added configuration validation to ensure a `conmon_cgroup ==
    "pod"` if `cgroup_manager == "cgroupfs"`
  - Added latest `crun` version to static binary bundle
  - Added metrics-exporter and [documentation]
  - Added new metrics `crio_image_pulls_failures` and
    `crio_image_pulls_successes`. For more information please refer
    to the [CRI-O metrics guide]
  - Container HostPort with SCTP protocol is supported.
  - Containers running `init` or `systemd` are now given a new
    selinux label `container_init_t`, giving it selinux privileges
    more appropriate for the workload
  - If users want the container_kvm_t label when using a runtime
    that supports kvm separation, they will need to either set the
    runtime_type to "vm" or have "kata" in the runtime name. E.g
    [crio.runtime.runtimes.my-kata-runtime]
    runtime_path = ""
    runtime_type = "oci"
    runtime_root = "/run/kata"
    or
    [crio.runtime.runtimes.my-kata-runtime]
    runtime_path = ""
    runtime_type = "vm"
    runtime_root = "/run/kata"
  - Re-add the behavior that string slices can be passed to the CLI
    comma separated, for example `--default-capabilities
    CHOWN,KILL`
  - Removed `socat` runtime dependency which was needed for pod
    port forwarding
  - Return pod image, pid and spec in sandbox_status CRI verbose
    mode
- Design
  - Hooks_dir entries are now created if they don't exist
- Documentation
  - Added `crun` container runtime to `crio.conf`
  - Added dependency report to generated release notes
  - The changelog is now rendered by a custom go template and
    contains the table of contents
- Bug or Regression
  - Adding additional runtime handler doesn't require the user to
    copy existing default runtime handler configuration. The
    existing default runtime handler configuration will be
    preserved while adding the new runtime handler.
  - ExecSync requests will ask conmon to not double fork, causing
    systemd to have fewer conmons re-parented to it. conmon v2.0.19
    or greater is required for this feature.
  - Fix handling of the --cni-plugin-dir and other multivalue
    command line flags
  - Fix path to bash via `/usr/bin/env` in crio-shutdown.service
  - Fix the container cgroup in case cgroupfs cgroup manager is
    used
  - Fix working set calculation
  - Fixed `crio version` binary mode parsing on musl toolchains
  - Fixed a bug where crictl only showed pod level stats, not
    container level stats.
  - Fixed a bug where exec sync requests (manually or automatically
    triggered via readiness/liveness probes) overwrite the runtime
    `info.runtimeSpec.process.args` of the container status
  - Fixed bug where Pod creation would fail if Uid was not
    specified in Metadata of sandbox config passed in a run pod
    sandbox request
  - Fixed bug where pod names would sometimes leak on creation,
    causing the kubelet to fail to recreate
  - Fixed crio restart behavior to make sure that Pod creation
    timestamps are restored and the order in the list of pods stays
    stable across restarts
  - Fixed wrong linkmode output
  - Reflects resource updates under the container spec.
- Other
  - Added info logs for image pulls and image status
  - Cleanup default info logging
  - Cleanup go module and vendor files.
  - Pod creation now fails if conmon cannot be moved to the cgroup
    specified in `conmon_cgroup`. Our default value for
    `conmon_cgroup` is `system.slice`, which is invalid for
    cgroupfs. As such, if you use cgroupfs, you should change
    `conmon_cgroup` to `pod`
  - Removed `crio-wipe.service` and `crio-shutdown.service` systemd
    units from the static bundle since they are not required
- Uncategorized
  - Add `--drop-infra-ctr` option to ask CRI-O to drop the infra
    container when a pod level pid namespace isn't requested. This
    feature is considered experimental
  - Adds a new optional field, runtime_type, to the "--runtimes"
    option.
  - Cleanup and update nix derivation for static builds
  - Fix a bug where a sudden reboot causes incomplete image writes.
    This could cause image storage to be corrupted, resulting in an
    error `layer not known`.
  - Fix bug where empty config fields having to do with storage
    cause `/info` requests to return incorrect information
  - Fixes panic when /sys/fs/cgroup can't be stat'ed
  - If the default_runtime is changed from the default
    configuration, the corresponding existing default entry in the
    runtime map in the configuration will be ignored.
  - Remove support for `--runtime` flag
  - Updated `crictl.yaml` configuration inside the repository to
    reflect cri-tools v1.19.0 changes
- Dependency-Change
  - Compile with go 1.15

* Sun Aug  2 2020 Callum Farmer <callumjfarmer13@gmail.com>
- Fixes for %%_libexecdir changing to /usr/libexec (bsc#1174075)

* Tue Jul 28 2020 Fabian Vogt <fvogt@suse.com>
- Suggest katacontainers instead of recommending it. It's not
  enabled by default, so it's just bloat

* Mon Jul 20 2020 Sascha Grunert <sgrunert@suse.com>
- Update to version 1.18.3:
  - Fix a bug where a sudden reboot causes incomplete image writes.
    This could cause image storage to be corrupted, resulting in an
    error layer not known.
  - Fixed bug where pod names would sometimes leak on creation,
    causing the kubelet to fail to recreate
  - If conmon is v2.0.19 or greater, ExecSync requests will not
    double fork, causing systemd to have fewer conmons re-parented
    to it

* Thu Jun 18 2020 dmueller@suse.com
- Update to version 1.18.2:
  * Bump version to v1.18.2
  * criocli: Avoid parsing the config twice
  * StringSliceTrySplit: return a copy of the underlying slice
  * Restore version output from crio --version
  * Add info logs for image pull and status CRI calls
  * managed_ns: deflake tests
  * bump containers image to 5.4.4  (fixes gh#containers/image/issues/898)

* Mon May 18 2020 sgrunert@suse.com
- Update to version 1.18.1:
  - Feature
  - Add -–version-file-persist, a place to put the version file
    in persistent storage. Now, crio wipe wipes containers if
  - –version-file is not present (presumably it is on temporary
    storage), and wipes images if both -–version-file and
  - –version-file-persist are out of date (presumably there has
    been an upgrade of cri-o’s minor version
  - Containers running init or systemd are now given a new
    selinux label container_init_t, giving it selinux privileges
    more appropriate for the workload
  - Other (Bug, Cleanup or Flake)
  - Fix linkmode retrieval on crio version for static binaries
  - Fix a bug where CRI-O could not start a container if
    CONFIG_CGROUP_HUGETLB was not set in the kernel
  - Re-add the behavior that string slices can be passed to the
    CLI comma separated, for example --default-capabilities
    CHOWN,KILL
  - Removed crio-wipe.service and crio-shutdown.service systemd
    units from the static bundle since they are not required
  - Fix some crio version oddities

* Wed Apr 29 2020 Sascha Grunert <sgrunert@suse.com>
- Remove the `go >= 1.13` build requirement

* Mon Apr 27 2020 Ralf Haferkamp <rhafer@suse.com>
- Restore calls to %%service_* macros that were accidently removed
  with the last change

* Thu Apr 23 2020 Sascha Grunert <sgrunert@suse.com>
- Remove crio-wipe.service and crio-shutdown.service
- Update to version 1.18.0:
  - Deprecation
  - Drop support for golang < v1.13
  - API Change
  - Removed version from default AppArmor profile name in config
  - CRI-O now runs containers without NET_RAW and SYS_CHROOT
    capabilities by default. This can result in permission denied
    errors when the container tries to do something that would
    require either of these capabilities. For instance, using
    `ping` requires NET_RAW, unless the container is given the
    sysctl `net.ipv4.ip_forward`. Further, if you have a
    container that runs buildah or configures RPMs, they may fail
    without SYS_CHROOT. Ultimately, the dropped capabilities are
    worth it, as the majority of containers don't need them. The
    fewer capabilities CRI-O gives out by default, the more
    secure it is by default.
  - When pinning namespaces, CRI-O now pins to
    /var/run/$NS_NAMEns/$RAND_ID instead of
    /var/run/crio/ns/$RAND_ID/$NS_NAME for better compatibility
    with third party networking plugins
  - Feature
  - Add `crio config -m/--migrate` option which supports
    migrating a v1.17.0 configuration file to the latest version.
  - Add available image labels to image status info
  - Add cgroup namespace unsharing to pinns
  - Add live configuration reload to AppArmor profile option
  - Add live configuration reload to seccomp profile option
  - Add log context to container stats to improve logging
  - Added `--cni-default-network`/`cni_default_network` option to
    specify the CNI network to select. The default value is
    `crio`, but this option can be explicitly set to `""` to
    pickup the first network found in
    `--cni-config-dir`/`network_dir`.
  - Added `conmon`, `runc` and `cni-plugins` to the static
    release bundle
  - Added `linkmode` (dynamic or static) output to `crio version`
    subcommand
  - Added gRPC method names to log entries to increase
    trace-ablity
  - Added live reload to `decryption_keys_path`
  - Added pinns binary to static bundle
  - Improve `crio --version` / `version` output to show more
    details
  - Provide the possibility to set the default config path via
    `make DEFAULTS_PATH=<PATH>`
  - Take local images into account when pulling images prefixed
    with `localhost/`
  - Added support for drop-in registries.conf configuration
    files. Please refer to the registries.conf.d documentation
    (https://github.com/containers/image/blob/master/docs/containers-registries.conf.d.5.md)
    for further details.
  - If a specified or the default hooks directory is not
    available, then we warn the user but do not fail any more.
  - Documentation
  - Update documentation that the lowest possible value for the
    ctr_stop_timeout is 30seconds. We also move the validation of
    this fact into the config validation part of the library.
  - Added man page for crio.conf.d(5)
  - Other (Bug, Cleanup or Flake)
  - Empty sandbox labels are now serialized into proper JSON (`null`)
  - Fixed CRI-O to fail to start when `runc` is no configured
    runtime and the `runc` binary is not in `$PATH`
  - Fixed SIGHUP reload for drop-in configuration files
  - Provide the latest release bundle via a Google Cloud Storage
    Bucket at:
    https://console.cloud.google.com/storage/browser/k8s-conform-cri-o/artifacts
  - Removed annoying logs coming directly from lower level
    runtimes like runc
  - Removed the musl libc build target from the static binary
    bundle in favor of the existing glibc variant
  - Removed warning about non-absolute container log paths when
    creating a container
  - CRI-O's version can be overriden at buildtime with
    `VERSION=my.version.number make bin/crio`
  - ContainerStatus no longer waits for a container operation
    (such as start or stop) to finish.
  - Fix bug resulting in false reports of OOM
  - Fixed SIGHUP reload behavior for unqualified search
    registries
  - Return grpc code NotFound when we can't find a container or
    pod
  - Systemd unit file: drop crio-wipe.service as a requirement

* Thu Apr 16 2020 Richard Brown <rbrown@suse.com>
- criconfig: Require kubernetes-kubeadm-provider to be compatable with multi-version kubernetes packaging

* Thu Apr 16 2020 Michal Jura <mjura@suse.com>
- Update apparmor_profile with current cri-o version, bsc#1161056

* Fri Apr 10 2020 Michal Jura <mjura@suse.com>
- Update to version 1.17.3:
  * Bump version to 1.17.3
  * Update c/image to v5.3.1
  * sandbox: Make sure the label annotation is proper JSON
  * container_server: Wrap a few more errors in LoadSandbox
  * restore tests: verify some namespace lifecycle cases work
  * fail on failed pinns
  * pinns: pin to /var/run/*ns instead of /var/run/crio/ns/*
  * Add the -d flag when installing runc for circle ci
  * Add the mounts that are required by systemd
  * bump to 1.17.2

* Fri Mar 27 2020 Richard Brown <rbrown@suse.com>
- Use new pause:3.2 image

* Mon Mar 16 2020 Sascha Grunert <sgrunert@suse.com>
- Update to v1.17.1:
  * Drop conmonmon
  * Update docs and completions for crio wipe --force
  * wipe: Add a force flag for skipping version check
  * Restore sandbox selinux labels directly from config.json
  * klog: don't write to /tmp
  * Pass down the integer value of the stop signal
  * exec: Close pipe fds to prevent hangs
  * Unwrap errors from label.Relabel() before checking for ENOTSUP
  * oci: Handle timeouts correctly for probes

* Mon Feb 10 2020 Sascha Grunert <sgrunert@suse.com>
- Put default configuration in /etc/crio/crio.conf.d/00-default.conf
  in replacement for /etc/crio/crio.conf

* Mon Feb 10 2020 Sascha Grunert <sgrunert@suse.com>
- Uncomment default apparmor profile to always fallback to the
  default one

* Mon Feb 10 2020 Sascha Grunert <sgrunert@suse.com>
- Remove prevent-local-loopback-teardown-rh1754154.patch which is
  now included in upstream
- Update to v1.17.0:
  * Major Changes
  - Allow CRI-O to manage IPC and UTS namespaces, in addition to
    Network
  - Add support for drop-in configuration files
  - Added image pull and network setup metrics
  - Image decryption support
  - Remove unneeded host_ip configuration value
  * Minor Changes
  - Setup container environment variables before user
  - Move default version file location to a tmpfs
  - Failures to stop the network will now cause a stop sandbox
    request to fail
  - Persist container exit codes across reboot
  - Add conmonmon: a conmon monitoring loop to protect against
    conmon being OOM'd
  - Add namespaces{-_}dir CLI and config option
  - Add disk usage for ListContainerStats
  - Introduce new runtime field to restrict devices in privileged
    mode

* Sat Jan 18 2020 Sascha Grunert <sgrunert@suse.com>
- Fix invalid apparmor profile (bsc#1161179)

* Thu Jan 16 2020 Sascha Grunert <sgrunert@suse.com>
- Include system proxy settings in service if present (bsc#1155323)

* Thu Jan 16 2020 Sascha Grunert <sgrunert@suse.com>
- Removed the usage of `name_` variables to reduce the error
  proneness
- Fixed systemd unit install locations for crio-wipe.service and
  crio-shutdown.service (bsc#1161056)

* Fri Jan 10 2020 Richard Brown <rbrown@suse.com>
- Add prevent-local-loopback-teardown-rh1754154.patch to stop local loopback interfaces being torndown before cluster is bootstrapped

* Tue Dec 17 2019 jmassaguerpla@suse.com
- Make cgroup-driver for kubelet be cgroupfs for SLE to be consistent
  with the cri-o configuration

* Wed Nov 27 2019 Sascha Grunert <sgrunert@suse.com>
- Update to v1.16.1:
  * Add manifest list support
  * Default to system.slice for conmon cgroup
  * Don't set PodIPs on host network pods

* Tue Nov 26 2019 Dirk Mueller <dmueller@suse.com>
- switch to libcontainers-common requires, as the other two are
  provided by it already (avant-garde#1056)

* Tue Nov 19 2019 David Cassany <dcassany@suse.com>
- Revert cgroup_manager from systemd to cgroupsfs for SLE15
  k8s default is cgroupfs and in can be modified at runtime by the
  `--kubelet-cgroups` flag. However this flag is deprecated and
  avoinding it is currently preferred over introducing it. In order
  to switch to systemd as the cgroups manager in SLE15 further analysis is
  required to find a suitable configuration strategy.

* Fri Nov 15 2019 Sascha Grunert <sgrunert@suse.com>
- Use single service macro invocation
- Add shell completions directories to files

* Thu Nov 14 2019 Sascha Grunert <sgrunert@suse.com>
- Add crio and crio-status shell completions
- Add crio-wipe and crio-shutdown services
- Update kubelet verbosity to `-v=2`
- Update conmon cgroup to `system.slice`
- Update crio.conf to match latest version
- Update to v1.16.0:
  * Major Changes
  * Add support for manifest lists
  * Dual stack IPv6 support
  * HUP reload of SystemRegistries
  * file_locking is no longer a supported option in the
    configuration file
  * Hooks are no longer found implicitally.
  * conmon now lives in a separate repository and must be
    downloaded separately.
  * Minor
  * All OCI mounts are mounted as rw when a pod is privileged
  * CRI-O can now run on a cgroupv2 system (only with the runtime
    crun)
  * Add environment variables to CLI flags
  * Add crio-status client to conveniently query status of crio
    or a container
  * Conmon is now found in $PATH if a path isn't specified or is
    empty
  * Add metrics to configuration file
  * Bandwidth burst can only be 4GB
  * If another container manager shares CRI-O's storage (like
    podman), CRI-O no longer attempts to restore them
  * Increase validation for log_dir and runtime_type in
    configuration
  * Allow usage of short container ID in ContainerStats
  * Make image volumes writeable by the container user
  * Various man page fixes
  * The crio-wipe script is now included in the crio binary (as
    crio wipe), and only removes CRI-O containers and images.
  * Set some previously public packages as internal (client, lib,
    oci, pkg, tools, version)
  * infra container now spawned as not privileged

* Mon Nov 11 2019 Richard Brown <rbrown@suse.com>
- Switch to `systemd` cgroup driver in kubelet config also

* Thu Oct 24 2019 Sascha Grunert <sgrunert@suse.com>
- Switch to `systemd` cgroup manager in replacement for `cgroupfs`

* Thu Oct 17 2019 Richard Brown <rbrown@suse.com>
- Remove obsolete Groups tag (fate#326485)

* Mon Oct  7 2019 Sascha Grunert <sgrunert@suse.com>
- Fix default apparmor profile to match the latest version

* Tue Sep 10 2019 Sascha Grunert <sgrunert@suse.com>
- Update to v1.15.2:
  * Use HTTP2MatchHeaderFieldSendSettings for incoming gRPC connections
  * Fix 32 bit builds
  * crio-wipe: Fix int compare in lib.bash

* Thu Sep  5 2019 Marco Vedovati <mvedovati@suse.com>
- Add katacontainers as a recommended package, and include it as an
  additional OCI runtime in the configuration.
- Document the format of the [crio.runtime.runtimes] table entries,
  and remove clutter from the current runc entry.

* Thu Sep  5 2019 David Cassany <dcassany@suse.com>
- Updating to v1.15.1 included de fix for CVE-2019-10214 (bsc#1144065)

* Thu Sep  5 2019 Sascha Grunert <sgrunert@suse.com>
- Update to v1.15.1:
  * Bump container storage to v1.12.6
  * Allow building with go1.10
  * Allow default IP route to not be present
  * Update libpod to the latest version
  * Require crio-wipe for crio service file
  * Disable crio-wipe in systemd by default
  * Change default apparmor profile to actually contain the version

* Thu Aug 29 2019 Sascha Grunert <sgrunert@suse.com>
- Update crio.conf to:
  * set manage_network_ns_lifecycle per default to true

* Tue Aug  6 2019 Sascha Grunert <sgrunert@suse.com>
- Update crio.conf to:
  * use `127.0.0.1` as streaming address
  * use any ephemeral port for streaming server

* Thu Jul 25 2019 Richard Brown <rbrown@suse.com>
- Update crio.conf to use correct pause_command

* Thu Jul 18 2019 Richard Brown <rbrown@suse.com>
- Update crio.conf to use better versioned pause container

* Wed Jul 17 2019 Richard Brown <rbrown@suse.com>
- Update crio.conf to use official kubic pause container

* Wed Jul  3 2019 Sascha Grunert <sgrunert@suse.com>
- Update CRI-O to v1.15.0:
  * update readme for currently supported branches
  * Update deps for k8s 1.15.0
  * Remove invalid unit test
  * Remove unnecessary indirect dependency gopopulate
  * go.mod: drop github.com/containerd/cgroups
  * cgroups: use libpod/pkg/cgroups
  * go.mod: update libpod and godbus/dbus
  * Move the creation of sourceCtx in Server.PullImage out of the loop
  * Remove the imageAuthFile parameter to RuntimeServer.CreateContainer
  * Set SystemContext.AuthFilePath in global Server.systemContext
  * Set SystemContext.DockerRegistryUserAgent in global Server.systemContext
  * Base copy.Options.{Source,Destination}Ctx both on the input systemContext
  * Expect a non-nil copy.Options in ImageServer.PullImage
  * Use a types.SystemContext instead of copy.Options in PrepareImage
  * Use an explicit DockerInsecureSkipTLSVerify = types.OptionalBoolTrue
  * Split imageService.remoteImageReference from prepareReference
  * Simplify the handling of PullImageRequest.auth
  * Build copy.Options.SourceCtx from Server.systemContext
  * Add a buildImageResult helper to avoid duplicating the code
  * Call buildImageCacheItem in ImageStatus
  * Don't redundantly look up an already available store.Image
  * Don't use path.join for docker references
  * Remove redundant manifest parsing to get config digest
  * Remove redundant calls to types.ImageSource.Size
  * When looking up a local image by transport:name reference, use the tag/digest as well
  * Use reference.Named.String() instead of open-coding it
  * Use reference.ParseNormalizedNamed for parsing storage.Image.Names
  * Don't modify the caller-provided SystemContext in server.New
  * Remove `seccomp.json` and fallback to internal defaults
  * Fix mockGetRef, and deal with all of the fallout
  * Return mockSequence from mockListImage and mockLoop, use global inOrder everywhere
  * Remove ImageServer.RemoveImage
  * Rename mockToCreate to mockCreateContainerOrPodSandboxImageExists
  * Add mockStorageImageSourceGetSize and mockNewImage
  * Don't split the first gomock expecation into a BeforeEach
  * Add mockGetStoreImage and mockResolveImage
  * Add a shared mockParseStoreReference
  * Add mockStorageReferenceStringWithinTransport and use it instead of open-coded sequences
  * Add an inOrder helper
  * Create a separate MockController for every test
  * Remove duplicate Dockerfile's
  * Discover runtimePath from $PATH environment
  * Use GlobalAuthFile, incl. for the pause image if PauseImageAuthFile is not set
  * Don't discard copy.Options.SourceCtx when credentials are provided
  * Don't set non-default copy.Options in imageService.PullImage if it is nil
  * Remove the *copy.Options parameter to RuntimeService.Create{PodSandbox,Container}
  * Add global_auth_file option to crio.image config
  * Remove the types.SystemContext parameter where no longer necessary
  * Don't read registries.conf for the defaults of --registry and --insecure-registry
  * Add state of infracontainer to disk when stopped
  * Use repository logo instead of rawgit
  * Exclude 'vendor' for git-validation checks
  * Bump up minMemoryLimit to 12Mb
  * enable inline exec and attach test
  * Mark file_locking deprecated
  * Disable file locking by default
  * Add release bundle target
  * Update dependency containerd/cgroups
  * crio-wipe: fix readme nits
  * conmon: force unlink attach socket
  * Add junit test files to .gitignore
  * Use *config.Config within OCI runtime
  * Move lib.Config to a dedicated package
  * Refactor sandbox and container name reservation
  * Update dependencies
  * Remove travis in favor of CircleCI
  * Vendor Kubernetes v1.15.0
  * Fix e2e_features_* selinux denials
  * add vrothberg to OWNERS file
  * Add documentation about the HTTP API
  * Default to runc is default_runtime is not set
  * Set default run root if not specified
  * Fix redundant if in lib/rename.go
  * Add codecov upload step to CircleCI config
  * Add flake attempts to critest integration testing
  * Add CircleCI badge
  * Add live reload feature to pause configuration
  * Update dependencies
  * Rebase containers/image to 2.0.0, buildah to 1.8.4, libpod to 1.4.1
  * Fix Vagrantfile vendor inconsistency
  * version: if git commit is empty, silently ignore
  * Use the official nix package for building static binaries
  * Add status related server unit tests
  * Create network directory if it doesn't exist
  * Small stderr fixes in crio-wipe
  * Add crio-wipe
  * Add version file functionality
  * Enable ppc64le Travis CI
  * Fix mentioned distributions in README.md
  * crictl.md: Fix a typo
  * Vendor Kubernetes 1.15.0-rc.1
  * Update golangci-lint to v1.17.1
  * README.md: Fix a typo
  * Fix missing images names on list
  * Update dependencies
  * Update setup.md
  * Refactor sandbox cgroup annotation
  * Fix gomega matcher syntax
  * Fix mentioned distributions within the setup tutorial
  * Go mod tidy
  * Add bandwidth limiting support
  * Switch to 'stable status' badge
  * Cleanup README.md
  * Vendor Kubernetes v1.15.0-beta.1
  * Close temporary image in PullImage
  * Add live reload integration tests and /config endpoint
  * Fix errcheck lint for network namespace creation
  * remove PluginDir from config if it existed
  * Change plugin_dir to plugin_dirs
  * Update dependencies
  * Bump github.com/containernetworking/plugins from 0.7.5 to 0.8.0
  * Enable errcheck lint and fixup error paths
  * Add critest to integration test suite
  * Update Dockerfile CNI plugins to v0.8.0
  * Update contrib systemd unit files to match project name
  * Fix runtime panic when having concurrent writes to runtime impl map
  * Fix build issues on 32-bit architectures
  * tests: added log max test to ctr.bats and command.bats
  * Update device cgroup permissions for configured devices.
  * Revert old fix
  * test: set container runtime to remote for e2e and fixup crio.conf
  * server: do not add default /sys if bind mounted
  * skip runtimes handler test until we can get a better solution
  * Fix possible runtime panic on store shutdown
  * Update Makefile to be usable without git
  * Ensure the test suite configures config directories.
  * Update depedencies
  * Add predefined build tags to .golangci.yml
  * Add container server unit tests
  * README.md: fix a typo
  * conmon: support OOM monitor under cgroup v2
  * Fix logging to journal
  * refresh apt before installation
  * Bump github.com/containers/libpod from 1.2.0 to 1.3.1
  * docs/crio.conf.5: Add "have" to "higher precedence" typo
  * Update scripts to find correct bash path
  * Fix links in tutorials/setup.md
  * Improve CI speed
  * Remove redundant source remove
  * setup: fix broken link
  * readme: Remove timeout from kube documentation
  * Remove terminal watch after success
  * Vendor Kubernetes v1.15.0-beta.0
  * Cleanup SystemContext usage
  * Bump github.com/golang/mock from 1.3.0 to 1.3.1
  * Bump github.com/containers/storage from 1.12.6 to 1.12.7
  * Bump github.com/docker/go-units from 0.3.3 to 0.4.0
  * Remove debug output from integration tests
  * sandbox_run: Log a warning if we can't find a slice
  * test: Add test for conmon cgroups
  * readme: Remove roadmap
  * Add config validation for conmon cgroup
  * Add CLI flag for --conmon-cgroup
  * Add config to run conmon under a custom cgroup slice
  * Add gocritic paramTypeCombine linter and fixes
  * Add awesome CRI-O list
  * Add config live reload feature
  * Update unit test target to not run `mockgen`
  * Add gocritic builtinShadow linter and fixes
  * Fix sandbox tests
  * conmon: detect cgroup2 and skip OOM handling
  * conmon: properly set conmon logs
  * Update test suites
  * Add gocritic importShadow linter and fixes
  * Add server sandbox unit tests
  * Add gocritic wrapperFunc linter and fixes
  * Add gocritic unnamedResult linter and fix issues
  * Add gocritic sloppyReassign linter and fixes
  * Add gocritic appendCombine linter and fixes
  * Add gocritic appendAssign linter and fixes
  * Add fossa badge
  * Add nakedret linter and related fixes
  * Bump github.com/go-zoo/bone from 0.0.0 to 1.3.0
  * Improve error handling for crio main.go
  * Bump github.com/containernetworking/cni from 0.7.0-rc2 to 0.7.0
  * Bump github.com/kr/pty from 1.1.1 to 1.1.4
  * Bump github.com/opencontainers/runc from 1.0.0-rc7 to 1.0.0-rc8
  * Bump github.com/opencontainers/selinux from 1.2.1 to 1.2.2
  * Bump google.golang.org/grpc from 1.20.0 to 1.20.1
  * Bump github.com/Microsoft/go-winio from 0.4.11 to 0.4.12
  * Bump golang.org/x/text from 0.3.1 to 0.3.2
  * Bump github.com/golang/mock from 1.2.0 to 1.3.0
  * Bump github.com/containers/storage from 1.12.4 to 1.12.6
  * Bump github.com/opencontainers/runtime-spec from 1.0.0 to 1.0.1
  * Add useragent unit tests
  * Add username and homedir to generated password
  * conmon: fix cross-compilation
  * Fix kubernetes import paths for cri-api
  * fixes make fmt/spacing issue
  * fixes assumption that socklen_t is always an unsigned long
  * Fix logic of server.restore()
  * Update CNI plugin test dependency to v0.7.5
  * Update runc test dependency to v1.0.0-rc8
  * Add server image unit tests
  * Vendor Kubernetes v1.15.0-alpha.2
  * Remove references to kubernetes/pause image
  * Migrate server config test to ginkgo
  * Add CircleCI support
  * Fix hack/openpgp_tag.sh on older distributions
  * Add server test suite and initial cases
  * Update `LogDir` to be configurable
  * Add documentation about static builds
  * Vendor containers/storage v1.12.4
  * Add server config interface
  * Add unit test inject files
  * Add additional build tags to setup guide
  * Remove ostree dependency from tutorial
  * Update PluginDir to be created if not existing
  * Add static crio binary build for x86_64 (glibc/musl)
  * Add openpgp_tag.sh as fallback if no gpgme available
  * Remove go build -i flag
  * Update test to use empty CNI hooks dir per default
  * Fix testunit-bin makefile target
  * Remove gofmt Makefile target
  * Remove ostree dependency
  * Vendor updated opencontainers/runtime-tools & runtime-spec
  * Fix coverity scan problem
  * run make vendor
  * Add min memory limit check to sandbox_run_linux.go
  * Add nil check for image status size
  * Add infra container check for pod sandbox
  * Revert back some changes from master
  * Use format strings instead of `Value` attribute
  * Remove default str in `Usage` when `Value` is used
  * Add default text to flags
  * Remove unnecessary golints
  * Update bats tests to run in parallel
  * Began documentation update.
  * conmon, exec: specify runtime root
  * test: use crictl inspect instead of RUNTIME state
  * Fix travis badge URL
  * fix broken link to policy.json(5) in readme
  * tests: added negative metrics testing to command.bats
  * tests: added metrics test to ctr.bats
  * Fix Makefile targets for sudo
  * Fix travis build
  * Switch to go modules
  * conmon: use sd_journal_sendv
  * Add stylecheck, unused and gosimple linters
  * Add config interface nil check
  * Update cri-tools versions
  * Allow containers/storage to manage SELinux labels
  * Move ContainerAttachSocketDir/containerExitsDir to lib
  * Use libpod registrar instead of pkg/registrar
  * travis: Switch to go 1.12.x
  * test: Switch to go 1.12.2
  * Add RuntimeHandler.RuntimeRoot
  * utils: add license headers for pulled files
  * userns: drop intermediate mount namespace
  * Refactor: use idtools.ParseIDMap instead of bundling own version
  * Fix parallel make build failure
  * rootless: propagate XDG_RUNTIME_DIR
  * oci: fix segfault when cgroup cannot be configured
  * Update error handling paths for sandbox add and removal
  * Add go-md2man to repo
  * netns can be nil which can cause a segfault
  * test: Fix oom test
  * test: ami fixups
  * conmon: do not leak fd when creating oom file
  * Fixup for moving to github.com/cri-o/cri-o
  * update github.com/containers/* dependencies
  * Do not crash when netns is not set up
  * readme: Update support matrix for 1.14
  * test: Increase number of inotify user watches
  * Remove timeout flag from kubernetes.yml
  * Log oom_handling_score failure to debug
  * tests: allow to switch manage_network_ns_lifecycle
  * Update linter to use hugeParam
  * config: export manage_network_ns_lifecycle
  * Fix possible out of bounds access during log parsing
- Update crio.conf to match the latest version
- Remove registry-mirror.patch since it is now included in upstream
- Remove unnecessary dependencies git-core and go-go-md2man
- Remove custom build and use native build target `make`
- Remove unit-test execution during package build since it
  requires (local) networking
- Remove seccomp.json since it is now included in the binary
- Fix apparmor dependencies

* Fri May 24 2019 Sascha Grunert <sgrunert@suse.com>
- Add apparmor-parser as dependency (bsc#1136403)

* Thu May 16 2019 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Add _constraints to avoid OOM

* Thu May  9 2019 Sascha Grunert <sgrunert@suse.com>
- Update cri-o to v1.14.1
  * Add min memory limit check to sandbox_run_linux.go
  * Fix crash when network namespace is not setup
  * Log oom_handling_score failure to debug
  * Fix possible out of bounds access during log parsing
  * Fix sandbox segfault with manage_network_ns_lifecycle
- Add registry-mirror.patch
- Update repository paths from `kubernetes-sigs` to `cri-o`
- Remove unnecessary ostree dependency

* Thu Apr 18 2019 Michal Rostecki <mrostecki@opensuse.org>
- Use /opt/cni/bin as the additional directory where cri-o is going
  to look up for CNI plugins installed by DaemonSets running on
  Kubernetes (i.e. Cilium).

* Fri Apr 12 2019 Sascha Grunert <sgrunert@suse.com>
- Update the configuration to fallback to the storage driver
  specified in libcontainers-common (`/etc/containers/storage.conf`)
- Update go version to >= 1.12 to be in sync with upstream

* Mon Apr  1 2019 Flavio Castelli <fcastelli@suse.com>
- Introduce new runtime dependency conntrack-tools: the conntrack
  package is required to avoid failures in network connection cleanup.

* Fri Mar 29 2019 Flavio Castelli <fcastelli@suse.com>
- Update cri-o to v1.14.0
  * Fix possible out of bounds access during log parsing
- Update default configuration file: crio.network.plugin_dir is now
  a list instead of being a string

* Thu Mar 28 2019 Daniel Orf <dorf@suse.com>
- Update go requirements to >= go1.11.3 to fix
  * bsc#1118897 CVE-2018-16873
    go#29230 cmd/go: remote command execution during "go get -u"
  * bsc#1118898 CVE-2018-16874

* Mon Mar 18 2019 Sascha Grunert <sgrunert@suse.com>
- Update cri-o to v1.13.3
  * Always set gid if returned from container user files
  * server: delete the container if it cannot be restored
  * Bump github.com/containers/storage to v1.11
  * Add support for host ip configuration
  * Pause credentials 1.13
  * Allow device mounting to work in privileged mode
  * Fix detach non tty

* Tue Feb 26 2019 Richard Brown <rbrown@suse.com>
- Update cri-o to v1.13.1
  * container: fix potential segfault on setup failure
  * container_create: fix race with sandbox being stopped
  * oci: read conmon process status
  * oci: Extend container stop timeout

* Fri Dec 14 2018 Sascha Grunert <sgrunert@suse.com>
- Update cri-o deprecated configuration and documentation to match
  upstream

* Fri Dec  7 2018 Richard Brown <rbrown@suse.com>
- Update cri-o to v1.13.0:
  * Support kubernetes 1.13

* Mon Nov 19 2018 Valentin Rothberg <vrothberg@suse.com>
- Update cri-o to v1.12.1:
  * Remove nodev from mounts
  * vendor: update storage for a panic fix
  * container_create: fix dev mounts and remove nodev from /dev mounts
  * Use CurrentContainerStatus in list CRI calls
  * oci: Add CurrentContainerStatus API
  * conmon: fsync the log file

* Wed Nov  7 2018 Valentin Rothberg <vrothberg@suse.com>
- Set NOFILE and NPROC limit to 1048576 to align with Docker/containerd
  and the upstream unit file.
  Fix bsc#1112980

* Fri Oct 19 2018 Valentin Rothberg <vrothberg@suse.com>
- Update cri-o to v1.12.0:
  * docs: tweak crio and crio.conf man pages
  * config: provide a default runtime and deprecate the runtime option
  * cri: Implement runtime handler support
  * *: implement default ulimits for containers
  * Fix manpage to correctly state default storage driver
  * crio.conf(5): update manpage to the latest state
  * Remove sysctl parsing code from cri-o
  * Add default_systcls option to crio.conf
  * Image Volumes should be bind mounted as private
  * Create LICENSE
  * conmon: fix segfault when --log-level is not specified
  * Add log-level option to conmon and crio.conf
  * Remove "--log-level debug" from service file
  * conmon: close extra files before exit
  * Block use of /proc/acpi from inside containers
  * conmon: do not use an empty env when running the exit command

* Mon Oct  8 2018 Jeff Kowalczyk <jkowalczyk@suse.com>
- Add go-1.11-compat-backport.patch for go1.11 compatibility.
  * Tested with golang(API) == 1.10 and golang(API) == 1.11, OK
  * Upstream git master commit
    https://github.com/kubernetes-sigs/cri-o/commit/0bd30872028b5ed2d0eb7febb39f034b5f2da72a
    contains 1 hunk adding missing argument in format string of
    calls to:
    [#] github.com/kubernetes-incubator/cri-o/lib
    lib/container_server.go:309: Debugf call needs 1 arg but has 2 args
    lib/container_server.go:317: Debugf call needs 1 arg but has 2 args
    ...
    FAIL   github.com/kubernetes-incubator/cri-o/lib [build failed]
    Calls in question:
    logrus.Debugf("loaded new pod sandbox %%s", sandboxID, err)
    logrus.Debugf("loaded new pod container %%s", containerID, err)
    require another argument to the string format (": %%v" per upstream):
    logrus.Debugf("loaded new pod sandbox %%s: %%v", sandboxID, err)
    logrus.Debugf("loaded new pod container %%s: %%v", containerID, err)
    Patch contents not available in upstream cri-o released versions:
    cri-o-1.11.3
    cri-o-1.11.4
    cri-o-1.11.5
    cri-o-1.11.6
    Filed upstream issue requesting patch contents in released version:
    https://github.com/kubernetes-sigs/cri-o/issues/1827

* Tue Aug 21 2018 rbrown@suse.com
- cri-o-kubeadm-criconfig: correct conflicts with docker-kubic

* Tue Aug 21 2018 rbrown@suse.com
- cri-o-kubeadm-criconfig: Remove /etc/kubernetes/runtime.conf,
  replace with /etc/sysconfig/kublet

* Mon Aug 20 2018 vrothberg@suse.com
- Update crio.conf to be as close to the default one as possible:
  * Extend crio.conf with all previously missing options; crio.conf(5) isn't
    mentioning all of them which soon will be fixed.
  * Uncomment options to use /etc/containers/{registries,storage}.conf where
    appropriate.
- Remove Fix-AppArmor-build.patch as the build issue is fixed with v1.11.2.
- Update cri-o to v1.11.2:
  * Fix AppArmor build
  * Image Volumes should be bind mounted as private
  * container_create: Set a minimum memory limit
  * Add log-level option to conmon and crio.conf
  * server/container_create: error out if capability is unknown

* Fri Aug 17 2018 vrothberg@suse.com
- Add "docker.io" to the registries list in the crio.conf to enable
  pulling of unqualified images by default.

* Thu Aug 16 2018 rbrown@suse.com
- ExcludeArch i586 (does not build, nor makes sense for that arch)

* Tue Aug 14 2018 rbrown@suse.com
- Make crio default, docker as alternative runtime (boo#1104821)
- Configure kubernetes CRI runtime with $runtime-kubeadm-criconfig
  packages

* Tue Aug 14 2018 rbrown@suse.com
- Use btrfs storage driver to be consistant with other supported
  runtimes

* Thu Aug  2 2018 vrothberg@suse.com
- Do not provide `/etc/crictl.yaml` anymore.  Although being shipped by
  upstream this package belongs into the `cri-tools` package.
  bsc#1104598
- add Fix-AppArmor-build.patch to temporarily fix apparmor builds
- Update cri-o to v1.11.1:
  * server: Don't make additional copy of config.json
  * cri-tools: Use release-1.11 branch

* Tue Jul 10 2018 David Cassany <dcassany@suse.com>
- Update to v1.10.6 included:
  * bsc#1100838 fix race between container create and cadvisor asking for info

* Tue Jul 10 2018 vrothberg@suse.com
- Update cri-o to v1.10.6:
  * mask /proc/{acpi,keys}

* Mon Jul  2 2018 vrothberg@suse.com
- Update cri-o to v1.10.5:
  * Reduce amount of logs being printed by default
  * Update to latest ocicni

* Wed Jun 27 2018 vrothberg@suse.com
- Update cri-o to v1.10.4:
  * network: Fix manage NetworkNS lifecycle
  * sandbox_run: fix selinux relabel sharing
  * container_create: more selinux relabel fixes
  * container_create: correctly relabel mounts when asked

* Mon Jun 18 2018 vrothberg@suse.com
- Update cri-o to v1.10.3:
  * container_portforward: add support for short pod IDs
  * container_create: no privileged container if not privileged sandbox
  * container_create: always mount sysfs as rw for privileged containers
  * container_create: set rw for privileged containers
  * conmon: on a flush error discard the iov buffer

* Fri Jun 15 2018 vrothberg@suse.com
- Update cri-o to v1.10.2:
  * various improvements to conmon
  * oci: avoid race on container stop
  * image: Let size be calculated dynamically
  * Add support for short IDs for exec and attach
  * Make network namespace lifecycle management optional
  * container_exec: Fix terminal setting for exec
  * oci: Force kill the container process only if nothing else worked
  * Add extra info to verbose requests to PodSandboxStatus
  * Make conmon and crio share the same constants
  * conmon: catch SIGTERM, SIGINT and SIQUIT
  * Invalidate cache by building fresh one and replacing previous all at once
  * Enable per pod PID namespace setting
  * Make the /opt/cni mount rw
  * conmon: add new option --version
  * oci: Copy-edits for waitContainerStop chControl comment
  * system container: add /var/tmp as RW
  * container_status: expose LogPath as requested by the CRI
  * container_create: only bind mount /etc/hosts if not provided by k8s
  * kubernetes: Simplify and freshen the required-files table
  * Report an warning when no stages are defined for a hook

* Mon Jun 11 2018 vrothberg@suse.com
- Use actual tag for v1.9.13.  Upstream missed to set a tag and the
  last revision mistakenly set it to v1.9.14-dev instead of v1.9.13.

* Thu Jun  7 2018 vrothberg@suse.com
- Update cri-o to v1.9.13:
  * runtime_status: report correct network status
  * container_status: expose LogPath as requested by the CRI
    bsc#1095154

* Tue Jun  5 2018 dcassany@suse.com
- Refactor %%license usage to a simpler form

* Mon Jun  4 2018 dcassany@suse.com
- Make use of %%license macro

* Fri May  4 2018 ndas@suse.de
- use correct path for runc

* Thu Apr 12 2018 fcastelli@suse.com
- Put cri-o deamon under the podruntime slice. This the recommended
  deployment to allow fine resource control on Kubernetes.
  bsc#1086185

* Wed Apr 11 2018 vrothberg@suse.com
- Update cri-o to v1.9.11:
  * oci: avoid race on container stop
  * server/sandbox_stop: Pass context through StopAllPodSandboxes
  * conmon: Add container ID to syslog
  * Add logging support for base condition in debug
  * Simplify filter block
  * Specifying a filter with no filtering expressions is now idempotent
  * Add methods for listing and fetching container stats
  * Implement the stats for the image_fs_info command
  * Return error for container exec

* Thu Mar 15 2018 vrothberg@suse.com
- Require cni and cni-plugins to enable container networking.
  feature#crio

* Thu Mar 15 2018 vrothberg@suse.com
- Update cri-o to v1.9.10:
  * conmon: Avoid strlen in logging path
  * conmon: Remove info logs
  * container_exec: Fix terminal setting for exec

* Mon Mar 12 2018 vrothberg@suse.com
- Update cri-o to v1.9.9:
  * sandbox_stop: Call CNI stop before stopping pod infra container

* Thu Mar  8 2018 vrothberg@suse.com
- Remove the crio-shutdown.service.  It does not have any effect when
  shutting down crio and also isn't shipped on Fedora.
  - crio-shutdown.service

* Mon Mar  5 2018 vrothberg@suse.com
- crio.conf: update default socket to /var/run/crio/crio.sock as suggested
  by upstream.

* Mon Mar  5 2018 vrothberg@suse.com
- Update cri-o to v1.9.8:
  * system_containers: Update mounts
  * execsync: Set terminal to true when we pass -t to conmon
  * Make network namespace pinning optional
  * Add context to net ns symlink removal errors
  * Make the /opt/cni mount rw
  * sandbox_stop: close/remove the netns _after_ stopping the containers
  * sandbox net: set netns closed after actaully closing it

* Mon Mar  5 2018 vrothberg@suse.com
- Configuration files should generally be tagged as %%config(noreplace) in order
  to keep the modified config files and to avoid losing data when the package
  is being updated.

* Sat Mar  3 2018 vrothberg@suse.com
- Remove empty filter rule from cri-o-rpmlintrc, which was mistakenly
  masking a few warnings, some of which have been fixed, others need
  to be filtered.  conmon and pause are not compiled with -fpie anymore
  to align with what upstream does; linking fails when done properly.

* Fri Mar  2 2018 fcastelli@suse.com
- Update minimum version of the Go compiler required

* Fri Mar  2 2018 fcastelli@suse.com
- Add missing runtime dependencies: socat, iptables, iproute

* Wed Feb 28 2018 vrothberg@suse.com
- Change the installation path of conmon and pause from
  /usr/lib/crio to /usr/lib/crio/bin in order to align with upstream
  requirements.
- Update crio.conf to the reflect the new path of conmon and set the correct
  path of CNI plugins (i.e., /usr/lib/cni).

* Tue Feb 20 2018 vrothberg@suse.com
- Update cri-o to v1.9.6:
  * vendor: update c/image to handle text/plain from registries
    Fixes cases where text/plain s1 schemes are mistakenly converted
    to MIME.

* Sun Feb 18 2018 jengelh@inai.de
- Let description say what the package really does.

* Fri Feb 16 2018 vrothberg@suse.com
- Update cri-o to v1.9.5:
  * system container: add /var/tmp as RW
  * container_create: correctly set user
  * imageService: cache information about images
  * image: Add lock around image cache access

* Fri Feb 16 2018 vrothberg@suse.com
- Cleanup version-update related changelogs to only keep log entries of
  changes that are visible and important to the user, and the project.

* Mon Feb 12 2018 vrothberg@suse.com
- Add requirements to libcontainers-{common,image,storage}.
- Run spec-cleaner on cri-o.spec.

* Mon Feb 12 2018 vrothberg@suse.com
- Update cri-o to v1.9.3:
  * Be more diligent about cleaning up failed-to-create containers
  * Use crictl instead of crioctl in image integration tests
  * Handle truncated IDs in imageService.ResolveNames()
  * Switch to ImageServer.UntagImage in RemoveImage handler
  * Return image references from the storage package
  * storage: API fixups

* Fri Feb  9 2018 vrothberg@suse.com
- Use golang-packaging macro for binary stripping.
- Use -buildmode=pie for compilation.
- The update to 1.9.0+ removes the crioctl binary.  The crictl binary from
  cri-tools should be used instead.
- Update cri-o to v1.9.2:
  * sandbox: fix sandbox logPath when crio restarts
  * Adapt to recent containers/image API updates
  * container_create: only bind mount /etc/hosts if not provided by k8s
  * container_attach: Ensure ctl file is closed
  * lib,oci: drop stateLock when possible
  * container_exec: fix terminal true process json
  * container_create: fix apparmor from container config
  * container_create: correctly set image and kube envs
  * oci: do not append conmon env to container process
  * container_exec: use process file with runc exec
  * drop crioctl source code
  * conmon: Add support for partial/newline log tags
  * image_pull: fix image resolver
  * Add /proc/scsi to masked paths
  * replace crioctl with crictl
  * replace crioctl in e2e with crictl
  * Move crio default sock to /var/run/crio/crio.sock
  * container_create: set the seccomp profile in the container object

* Mon Feb  5 2018 vrothberg@suse.com
- Fix libostree-devel %%if condition for TW, Leap 15+ and SLES 15+.

* Thu Feb  1 2018 vrothberg@suse.com
- Use `%%fdupes %%buildroot/%%_prefix` since `fdupes %%buildroot` is not allowedv
  because you cannot make hardlinks between certain partitions.

* Wed Jan 31 2018 vrothberg@suse.com
- Source the cri-o-rpmlintrc the spec file.

* Tue Jan 30 2018 vrothberg@suse.com
- Add cri-o package: CRI-O is meant to provide an integration path between OCI
  conformant runtimes and the kubelet. Specifically, it implements the Kubelet
  Container Runtime Interface (CRI) using OCI conformant runtimes. The scope of
  CRI-O is tied to the scope of the CRI.
