#
# spec file for package cni
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


%define         cni_etc_dir  %{_sysconfdir}/cni
%define         cni_bin_dir  %{_libexecdir}/cni
%define         cni_doc_dir  %{_docdir}/cni
# Remove stripping of Go binaries.
%define __arch_install_post export NO_BRP_STRIP_DEBUG=true
Summary:        Container Network Interface - networking for Linux containers
Name:           cni
Version:        1.0.1
Release:        15%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Management
URL:            https://github.com/containernetworking/cni
#Source0:       https://github.com/containernetworking/cni/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        99-loopback.conf
Source2:        build.sh
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/containernetworking/cni/archive/refs/tags/v1.0.1.tar.gz -o %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source3:        %{name}-%{version}-vendor.tar.gz
BuildRequires:  golang
BuildRequires:  systemd-rpm-macros
BuildRequires:  xz
Requires:       systemd
Requires(post): %fillup_prereq
Recommends:     cni-plugins

%description
The CNI (Container Network Interface) project consists of a
specification and libraries for writing plugins to configure
network interfaces in Linux containers, along with a number of
supported plugins. CNI concerns itself only with network
connectivity of containers and removing allocated resources when
the container is deleted. Because of this focus, CNI has a wide
range of support and the specification is simple to implement.

%prep
%setup -q
cp %{SOURCE2} build.sh

%build
# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE3} --no-same-owner

# go1.16+ default is GO111MODULE=on set to auto temporarily
# until using upstream release with go.mod
export GO111MODULE=auto
sh ./build.sh

%install

# install the plugins
install -m 755 -d "%{buildroot}%{cni_bin_dir}"
cp bin/noop "%{buildroot}%{cni_bin_dir}/"
cp bin/sleep "%{buildroot}%{cni_bin_dir}/"

# undo a copy: cnitool must go to sbin/
install -m 755 -d "%{buildroot}%{_sbindir}"
cp bin/cnitool  "%{buildroot}%{_sbindir}/"

# config
install -m 755 -d "%{buildroot}%{cni_etc_dir}"
install -m 755 -d "%{buildroot}%{cni_etc_dir}/net.d"
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{cni_etc_dir}/net.d/99-loopback.conf.sample

# documentation
install -m 755 -d "%{buildroot}%{cni_doc_dir}"

%post
%{fillup_only -n %{name}}

%files
%defattr(-,root,root)
%doc CONTRIBUTING.md README.md DCO
%license LICENSE
%dir %{cni_etc_dir}
%dir %{cni_etc_dir}/net.d
%config %{cni_etc_dir}/net.d/*
%dir %{cni_bin_dir}
%dir %{cni_doc_dir}
%{cni_bin_dir}/*
%{cni_etc_dir}/net.d/*
%{_sbindir}/cnitool

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-15
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.0.1-14
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.0.1-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.0.1-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.0.1-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.0.1-2
- Bump release to rebuild with golang 1.18.3

* Wed Feb 09 2022 Henry Li <lihl@microsoft.com> - 1.0.1-1
- Upgrade to version 1.0.1
- Add vendor source, which is required to build
- Modify build.sh to build using vendor source

* Tue Aug 17 2021 Henry Li <lihl@microsoft.com> - 0.8.1-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License Verified
- Remove shadow from BR
- Use systemd and fillup from runtime requirements
- Manually define fillup-related macros
- Remove buildroot definition

* Mon May 31 2021 John Paul Adrian Glaubitz <adrian.glaubitz@suse.com>
- Update to version 0.8.1:
  * This is a security release that fixes a single bug:
  - Tighten up plugin-finding logic (#811).

* Sat Apr 24 2021 Dirk Müller <dmueller@suse.com>
- use buildmode=pie (cnitool is installed into sbindir)

* Tue Mar 16 2021 Jeff Kowalczyk <jkowalczyk@suse.com>
- Set GO111MODULE=auto to build with go1.16+
  * Default changed to GO111MODULE=on in go1.16
  * Set temporarily until using upstream release with go.mod
  * Drop BuildRequires: golang-packaging not currently using macros
  * Add BuildRequires: golang(API) >= 1.13 recommended dependency expression

* Thu Oct  1 2020 John Paul Adrian Glaubitz <adrian.glaubitz@suse.com>
- Update to version 0.8.0:
  * Specification and Conventions changes
    + docs: add ips and mac to well-known capabilities
    + add interface name validation
    + Add GUID to well known Capabilities
    + Add DeviceID attribute to RuntimeConfig
    + Typo fixes for infiniband GUID
    + Fix linting issues in docs, add headers to json example, update errors into table
  * Documentation changes
    + Update cnitool docs
    + Remove extra ',' chars which makes conflist examples invalid.
  * libcni changes
    + Remove Result.String method
    + libcni: add config caching [v2]
    + clean up : fix staticcheck warnings
    + libcni: add InitCNIConfigWithCacheDir() and deprecate RuntimeConfig.CacheDir
    + skel: clean up errors in skel and add some well-known error codes
    + libcni: find plugin in exec
    + validate containerID and networkName
    + skel: remove needless functions and types
    + libcni: also cache IfName
    + libcni: fix cache file 'result' key name
    + Bump Go version to 1.13
    + When CNI version isn't supplied in config, use default.
    + intercept netplugin std error
    + invoke: capture and return stderr if plugin exits unexpectedly
    + Retry exec commands on text file busy

* Mon Jan 13 2020 Sascha Grunert <sgrunert@suse.com>
- Set correct CNI version for 99-loopback.conf

* Tue Jul 16 2019 John Paul Adrian Glaubitz <adrian.glaubitz@suse.com>
- Update to version 0.7.1 (bsc#1160460):
  * Library changes:
    + invoke : ensure custom envs of CNIArgs are prepended to process envs
    + add GetNetworkListCachedResult to CNI interface
    + delegate : allow delegation funcs override CNI_COMMAND env automatically in heritance
  * Documentation & Convention changes:
    + Update cnitool documentation for spec v0.4.0
    + Add cni-route-override to CNI plugin list
  * Build and test changes:
    + Release: 4%{?dist}

* Fri May 17 2019 John Paul Adrian Glaubitz <adrian.glaubitz@suse.com>
- Update to version 0.7.0:
  * Spec changes:
    + Use more RFC2119 style language in specification (must, should...)
    + add notes about ADD/DEL ordering
    + Make the container ID required and unique.
    + remove the version parameter from ADD and DEL commands.
    + Network interface name matters
    + be explicit about optional and required structure members
    + add CHECK method
    + Add a well-known error for "try again"
    + SPEC.md: clarify meaning of 'routes'
  * Library changes:
    + pkg/types: Makes IPAM concrete type
    + libcni: return error if Type is empty
    + skel: VERSION shouldn't block on stdin
    + non-pointer instances of types.Route now correctly marshal to JSON
    + libcni: add ValidateNetwork and ValidateNetworkList functions
    + pkg/skel: return error if JSON config has no network name
    + skel: add support for plugin version string
    + libcni: make exec handling an interface for better downstream testing
    + libcni: api now takes a Context to allow operations to be timed out or cancelled
    + types/version: add helper to parse PrevResult
    + skel: only print about message, not errors
    + skel,invoke,libcni: implementation of CHECK method
    + cnitool: Honor interface name supplied via CNI_IFNAME environment variable.
    + cnitool: validate correct number of args
    + Don't copy gw from IP4.Gateway to Route.GW When converting from 0.2.0
    + add PrintTo method to Result interface
    + Return a better error when the plugin returns none
- Install sleep binary into CNI plugin directory
- Restore build.sh script which was removed upstream

* Tue Jun  5 2018 dcassany@suse.com
- Refactor %%license usage to a simpler form

* Mon Jun  4 2018 dcassany@suse.com
- Make use of %%license macro

* Wed Apr  4 2018 jmassaguerpla@suse.com
- Remove creating subvolumes. This should be in another package (kubernetes-kubelet)

* Mon Jan 29 2018 kmacinnes@suse.com
- Use full/absolute path for mksubvolume
- Change snapper Requires to a Requires(post)

* Thu Jan 18 2018 kmacinnes@suse.com
- Add snapper as a requirement, to provide mksubvolume

* Mon Jan 15 2018 alvaro.saurin@suse.com
- Make /var/lib/cni writable

* Tue Dec 19 2017 alvaro.saurin@suse.com
- Remove the dependency with the cni-plugins
- Recommend the cni-plugins

* Mon Aug 28 2017 opensuse-packaging@opensuse.org
- Update to version 0.6.0:
  * Conventions: add convention around chaining interfaces
  * pkg/types: safer typecasting for TextUnmarshaler when loading args
  * pkg/types: modify LoadArgs to return a named error when an unmarshalable condition is detected
  * Update note about next Community Sync, 2017-06-21
  * types: fix marshalling of omitted "interfaces" key in IPConfig JSON
  * Update and document release process
  * scripts/release.sh: Add in s390x architecture
  * cnitool: add support for CNI_ARGS
  * README plugins list: add Linen CNI plugin

* Mon Apr 10 2017 opensuse-packaging@opensuse.org
- Update to version 0.5.2:
  * Rename build script to avoid conflict with bazel
  * Enable s390x build
  * Update community sync detail
  * Added entry for CNI-Genie
  * travis: shift forward to Go 1.8 and 1.7
  * spec/plugins: fix 'ip'->'ips' in the spec, bump to 0.3.1
  * libcni: Improved error messages.
  * libcni: Fixed tests that were checking error strings.
  * Documentation: Added documentation for `cnitool`.

* Thu Mar 23 2017 opensuse-packaging@opensuse.org
- Update to version 0.5.1:
  * readme.md: Add link to community sync
  * pkg/ip: do not leak types from vendored netlink package
  * pkg/ip: SetupVeth returns net.Interface
  * pkg/ip: improve docstring for SetupVeth
  * Added Romana to list of CNI providers...
  * plugins/meta/flannel: If net config is missing do not return err on DEL
  * plugins/*: Don't error if the device doesn't exist

* Wed Mar 22 2017 alvaro.saurin@suse.com
- Update to version 0.5.0:
  * Documentation: Add conventions doc
  * noop: allow specifying debug file in config JSON
  * Spec/Conventions: Update to include plugin config
  * spec: add network configuration list specification
  * api,libcni: add network config list-based plugin chaining
  * Update CONVENTIONS.md
  * skel: adds PluginMainWithError which returns a *types.Error
  * testutils: pass netConf in for version operations; pass raw result out for tests
  * types: make Result an interface and move existing Result to separate package
  * macvlan/ipvlan: use common RenameLink method
  * plugins/flannel: organize test JSON alphabetically
  * pkg/ipam: add testcases
  * spec/plugins: return interface details and multiple IP addresses to runtime
  * spec, libcni, pkg/invoke: Use OS-agnostic separator when parsing CNI_PATH
  * pkg/utils/sysctl/sysctl_linux.go: fix build tag.
  * pkg/utils/sysctl/sysctl_linux.go: fix typo.
  * invoke: Enable plugin file names with extensions
  * CONVENTIONS.md: Update details on port-mappings
  * Update with feedback
  * More markups
  * spec: Remove `routes` from Network Configuration
  * docs: consolidate host-local documentation
  * pkg/ns: refactored so that builds succeed on non-linux platforms
  * Fix grammar
  * plugins/main/ptp: set the Sandbox property on the response
  * README: List multus as 3rd party plugin
  * Replace Michael Bridgen with Bryan Boreham
  * pkg/ns, pkg/types: refactored non linux build fix code to
  * pkg/ip: refactored so that builds succeed on non-linux platforms
  * vendor: Update vishvanana/netlink dependency
  * libcni: up-convert a Config to a ConfigList when no other configs are found.
  * docs: CNI versioning for 0.3.0 upgrade
  * docs: Edits to v0.3.0 upgrade guidance
  * docs: minor improvements to 0.3.0 upgrade guidance
  * docs: add small upgrade instructions
  * docs: minor improvements to spec-upgrades
  * docs: fill-out and correct version conversion table
  * docs: table formatting is hard
  * pkg/testutils: return errors after restoring stdout
  * pkg/types: misc current types testcase cleanups
  * Minor rewording about default config version
  * spec,libcni: add support for injecting runtimeConfig into plugin stdin data
  * Check n.IPAM before use it in LoadIPAMConfig function
  * do not error if last_reserved_ip is missing for host local ipam
  * add test for ensuring initial subnet creation does not contain an error
  * fix unrelated failing tests

* Wed Mar  1 2017 opensuse-packaging@opensuse.org
- Update to version 0.4.0:
  * plugins/noop: return a helpful message for test authors
  * host-local: trim whitespace from container IDs and disk file contents
  * travis: roll forward the versions of Go that we test
  * MAINTAINERS: hi CaseyC!
  * ipam/host-local: Move allocator and config to backend
  * ipam/host-local: add ResolvConf argument for DNS configuration
  * spec: notice of version

* Thu Feb 23 2017 alvaro.saurin@suse.com
- Initial version
