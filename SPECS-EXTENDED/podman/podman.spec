## START: Set by rpmautospec
## (rpmautospec version 0.7.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global with_debug 1

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

# RHEL's default %%gobuild macro doesn't account for the BUILDTAGS variable, so we
# set it separately here and do not depend on RHEL's go-[s]rpm-macros package
# until that's fixed.
# c9s bz: https://bugzilla.redhat.com/show_bug.cgi?id=2227328
%if %{defined rhel} && 0%{?rhel} < 10
%define gobuild(o:) go build -buildmode pie -compiler gc -tags="rpm_crashtraceback libtrust_openssl ${BUILDTAGS:-}" -ldflags "-linkmode=external -compressdwarf=false ${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v -x %{?**};
%endif

%global gomodulesmode GO111MODULE=on

%if %{defined rhel}
# _user_tmpfiles.d currently undefined on rhel
%global _user_tmpfilesdir %{_datadir}/user-tmpfiles.d
%endif

%if %{defined fedora}
%define build_with_btrfs 1
%endif

%if %{defined copr_username}
%define copr_build 1
%endif

%global container_base_path github.com/containers
%global container_base_url https://%{container_base_path}

# For LDFLAGS
%global ld_project %{container_base_path}/%{name}/v5
%global ld_libpod %{ld_project}/libpod

# %%{name}
%global git0 %{container_base_url}/%{name}

Name: podman
%if %{defined copr_build}
Epoch: 102
%else
Epoch: 5
%endif
# DO NOT TOUCH the Version string!
# The TRUE source of this specfile is:
# https://github.com/containers/podman/blob/main/rpm/podman.spec
# If that's what you're reading, Version must be 0, and will be updated by Packit for
# copr and koji builds.
# If you're reading this on dist-git, the version is automatically filled in by Packit.
Version: 5.3.1
# The `AND` needs to be uppercase in the License for SPDX compatibility
License: Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0
Release: %autorelease
%if %{defined golang_arches_future}
ExclusiveArch: %{golang_arches_future}
%else
ExclusiveArch: aarch64 ppc64le s390x x86_64
%endif
Summary: Manage Pods, Containers and Container Images
URL: https://%{name}.io/
# All SourceN files fetched from upstream
Source0: %{git0}/archive/v%{version_no_tilde}.tar.gz
Provides: %{name}-manpages = %{epoch}:%{version}-%{release}
BuildRequires: %{_bindir}/envsubst
%if %{defined build_with_btrfs}
BuildRequires: btrfs-progs-devel
%endif
BuildRequires: gcc
BuildRequires: glib2-devel
BuildRequires: glibc-devel
BuildRequires: glibc-static
BuildRequires: golang
BuildRequires: git-core
%if %{undefined rhel} || 0%{?rhel} >= 10
BuildRequires: go-rpm-macros
%endif
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: libgpg-error-devel
BuildRequires: libseccomp-devel
BuildRequires: libselinux-devel
BuildRequires: shadow-utils-subid-devel
BuildRequires: pkgconfig
BuildRequires: make
BuildRequires: man-db
BuildRequires: ostree-devel
BuildRequires: systemd
BuildRequires: systemd-devel
Requires: catatonit
Requires: conmon >= 2:2.1.7-2
%if %{defined fedora} && 0%{?fedora} >= 40
# TODO: Remove the f40 conditional after a few releases to keep conditionals to
# a minimum
# Ref: https://bugzilla.redhat.com/show_bug.cgi?id=2269148
Requires: containers-common-extra >= 5:0.58.0-1
%else
Requires: containers-common-extra
%endif
Obsoletes: %{name}-quadlet <= 5:4.4.0-1
Provides: %{name}-quadlet = %{epoch}:%{version}-%{release}

%description
%{name} (Pod Manager) is a fully featured container engine that is a simple
daemonless tool.  %{name} provides a Docker-CLI comparable command line that
eases the transition from other container engines and allows the management of
pods, containers and images.  Simply put: alias docker=%{name}.
Most %{name} commands can be run as a regular user, without requiring
additional privileges.

%{name} uses Buildah(1) internally to create container images.
Both tools share image (not container) storage, hence each can use or
manipulate images (but not containers) created by the other.


%package docker
Summary: Emulate Docker CLI using %{name}
BuildArch: noarch
Requires: %{name} = %{epoch}:%{version}-%{release}
Conflicts: docker
Conflicts: docker-latest
Conflicts: docker-ce
Conflicts: docker-ee
Conflicts: moby-engine

%description docker
This package installs a script named docker that emulates the Docker CLI by
executes %{name} commands, it also creates links between all Docker CLI man
pages and %{name}.

%package tests
Summary: Tests for %{name}

Requires: %{name} = %{epoch}:%{version}-%{release}
%if %{defined fedora}
Requires: bats
%endif
Requires: jq
Requires: skopeo
Requires: nmap-ncat
Requires: httpd-tools
Requires: openssl
Requires: socat
Requires: buildah
Requires: gnupg

%description tests
%{summary}

This package contains system tests for %{name}

%package remote
Summary: (Experimental) Remote client for managing %{name} containers

%description remote
Remote client for managing %{name} containers.

This experimental remote client is under heavy development. Please do not
run %{name}-remote in production.

%{name}-remote uses the version 2 API to connect to a %{name} client to
manage pods, containers and container images. %{name}-remote supports ssh
connections as well.

%package -n %{name}sh
Summary: Confined login and user shell using %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}
Provides: %{name}-shell = %{epoch}:%{version}-%{release}
Provides: %{name}-%{name}sh = %{epoch}:%{version}-%{release}

%description -n %{name}sh
%{name}sh provides a confined login and user shell with access to volumes and
capabilities specified in user quadlets.

It is a symlink to %{_bindir}/%{name} and execs into the `%{name}sh` container
when `%{_bindir}/%{name}sh` is set as a login shell or set as os.Args[0].

%package machine
Summary: Metapackage for setting up %{name} machine
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: gvisor-tap-vsock
Requires: qemu
Requires: virtiofsd

%description machine
This subpackage installs the dependencies for %{name} machine, for more see:
https://docs.podman.io/en/latest/markdown/podman-machine.1.html

%prep
%autosetup -Sgit -n %{name}-%{version_no_tilde}
sed -i 's;@@PODMAN@@\;$(BINDIR);@@PODMAN@@\;%{_bindir};' Makefile

# cgroups-v1 is supported on rhel9
%if 0%{?rhel} == 9
sed -i '/DELETE ON RHEL9/,/DELETE ON RHEL9/d' libpod/runtime.go
%endif

# These changes are only meant for copr builds
%if %{defined copr_build}
# podman --version should show short sha
sed -i "s/^const RawVersion = .*/const RawVersion = \"##VERSION##-##SHORT_SHA##\"/" version/rawversion/version.go
# use ParseTolerant to allow short sha in version
sed -i "s/^var Version.*/var Version, err = semver.ParseTolerant(rawversion.RawVersion)/" version/version.go
%endif

%build
%set_build_flags
export CGO_CFLAGS=$CFLAGS

# These extra flags present in $CFLAGS have been skipped for now as they break the build
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-flto=auto//g')
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-Wp,D_GLIBCXX_ASSERTIONS//g')
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//g')

%ifarch x86_64
export CGO_CFLAGS+=" -m64 -mtune=generic -fcf-protection=full"
%endif

export GOPROXY=direct

LDFLAGS="-X %{ld_libpod}/define.buildInfo=${SOURCE_DATE_EPOCH:-$(date +%s)} \
         -X %{ld_libpod}/config._installPrefix=%{_prefix} \
         -X %{ld_libpod}/config._etcDir=%{_sysconfdir} \
         -X %{ld_project}/pkg/systemd/quadlet._binDir=%{_bindir}"

# build rootlessport first
%gobuild -o bin/rootlessport ./cmd/rootlessport

export BASEBUILDTAGS="seccomp exclude_graphdriver_devicemapper $(hack/systemd_tag.sh) $(hack/libsubid_tag.sh)"

# build %%{name}
export BUILDTAGS="$BASEBUILDTAGS $(hack/btrfs_installed_tag.sh) $(hack/btrfs_tag.sh) $(hack/libdm_tag.sh)"
%gobuild -o bin/%{name} ./cmd/%{name}

# build %%{name}-remote
export BUILDTAGS="$BASEBUILDTAGS exclude_graphdriver_btrfs btrfs_noversion remote"
%gobuild -o bin/%{name}-remote ./cmd/%{name}

# build quadlet
export BUILDTAGS="$BASEBUILDTAGS $(hack/btrfs_installed_tag.sh) $(hack/btrfs_tag.sh)"
%gobuild -o bin/quadlet ./cmd/quadlet

# build %%{name}-testing
export BUILDTAGS="$BASEBUILDTAGS $(hack/btrfs_installed_tag.sh) $(hack/btrfs_tag.sh)"
%gobuild -o bin/podman-testing ./cmd/podman-testing

# reset LDFLAGS for plugins binaries
LDFLAGS=''

%{__make} docs docker-docs

%install
install -dp %{buildroot}%{_unitdir}
PODMAN_VERSION=%{version} %{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} ETCDIR=%{_sysconfdir} \
       install.bin \
       install.man \
       install.systemd \
       install.completions \
       install.docker \
       install.docker-docs \
       install.remote \
       install.testing

# See above for the iptables.conf declaration
%if %{defined fedora} && 0%{?fedora} < 41
%{__make} DESTDIR=%{buildroot} MODULESLOADDIR=%{_modulesloaddir} install.modules-load
%endif

sed -i 's;%{buildroot};;g' %{buildroot}%{_bindir}/docker

# do not include docker and podman-remote man pages in main package
for file in `find %{buildroot}%{_mandir}/man[157] -type f | sed "s,%{buildroot},," | grep -v -e %{name}sh.1 -e remote -e docker`; do
    echo "$file*" >> %{name}.file-list
done

rm -f %{buildroot}%{_mandir}/man5/docker*.5

install -d -p %{buildroot}%{_datadir}/%{name}/test/system
cp -pav test/system %{buildroot}%{_datadir}/%{name}/test/

# symlink virtiofsd in %%{name} libexecdir for machine subpackage
ln -s ../virtiofsd %{buildroot}%{_libexecdir}/%{name}

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files -f %{name}.file-list
%license LICENSE vendor/modules.txt
%doc README.md CONTRIBUTING.md install.md transfer.md
%{_bindir}/%{name}
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/rootlessport
%{_libexecdir}/%{name}/quadlet
%{_datadir}/bash-completion/completions/%{name}
# By "owning" the site-functions dir, we don't need to Require zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_unitdir}/%{name}*
%{_userunitdir}/%{name}*
%{_tmpfilesdir}/%{name}.conf
%{_systemdgeneratordir}/%{name}-system-generator
%{_systemdusergeneratordir}/%{name}-user-generator
# iptables modules are only needed with iptables-legacy,
# as of f41 netavark will default to nftables so do not load unessary modules
# https://fedoraproject.org/wiki/Changes/NetavarkNftablesDefault
%if %{defined fedora} && 0%{?fedora} < 41
%{_modulesloaddir}/%{name}-iptables.conf
%endif

%files docker
%{_bindir}/docker
%{_mandir}/man1/docker*.1*
%{_sysconfdir}/profile.d/%{name}-docker.*
%{_tmpfilesdir}/%{name}-docker.conf
%{_user_tmpfilesdir}/%{name}-docker.conf

%files remote
%license LICENSE
%{_bindir}/%{name}-remote
%{_mandir}/man1/%{name}-remote*.*
%{_datadir}/bash-completion/completions/%{name}-remote
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}-remote.fish
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}-remote

%files tests
%{_bindir}/%{name}-testing
%{_datadir}/%{name}/test

%files -n %{name}sh
%{_bindir}/%{name}sh
%{_mandir}/man1/%{name}sh.1*

%files machine
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/virtiofsd

%changelog
## START: Generated by rpmautospec
* Thu Nov 21 2024 Packit <hello@packit.dev> - 5:5.3.1-1
- Update to 5.3.1 upstream release

* Wed Nov 13 2024 Packit <hello@packit.dev> - 5:5.3.0-1
- Update to 5.3.0 upstream release

* Wed Nov 06 2024 Packit <hello@packit.dev> - 5:5.3.0~rc3-1
- Update to 5.3.0-rc3 upstream release

* Thu Oct 31 2024 Packit <hello@packit.dev> - 5:5.3.0~rc2-1
- Update to 5.3.0-rc2 upstream release

* Tue Oct 22 2024 Packit <hello@packit.dev> - 5:5.3.0~rc1-1
- Update to 5.3.0-rc1 upstream release

* Fri Oct 18 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:5.2.5-1
- bump to v5.2.5

* Tue Oct 15 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:5.2.4-2
- c/common pr 2194

* Mon Oct 07 2024 Packit <hello@packit.dev> - 5:5.2.4-1
- Update to 5.2.4 upstream release

* Tue Sep 24 2024 Packit <hello@packit.dev> - 5:5.2.3-1
- Update to 5.2.3 upstream release

* Wed Aug 21 2024 Packit <hello@packit.dev> - 5:5.2.2-1
- Update to 5.2.2 upstream release

* Wed Aug 14 2024 Packit <hello@packit.dev> - 5:5.2.1-1
- Update to 5.2.1 upstream release

* Fri Aug 02 2024 Packit <hello@packit.dev> - 5:5.2.0-1
- Update to 5.2.0 upstream release

* Thu Aug 01 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:5.2.0~rc2-2
- check buildah and skopeo version in tests

* Tue Jul 23 2024 Packit <hello@packit.dev> - 5:5.2.0~rc2-1
- Update to 5.2.0-rc2 upstream release

* Wed Jul 17 2024 Packit <hello@packit.dev> - 5:5.2.0~rc1-1
- Update to 5.2.0-rc1 upstream release

* Wed Jul 17 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:5.1.2-3
- fix podman-testing binary

* Tue Jul 16 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:5.1.2-2
- Add PODMAN_TESTING var

* Wed Jul 10 2024 Packit <hello@packit.dev> - 5:5.1.2-1
- Update to 5.1.2 upstream release

* Tue Jun 04 2024 Packit <hello@packit.dev> - 5:5.1.1-1
- Update to 5.1.1 upstream release

* Wed May 29 2024 Packit <hello@packit.dev> - 5:5.1.0-1
- Update to 5.1.0 upstream release

* Wed May 15 2024 Packit <hello@packit.dev> - 5:5.1.0~rc1-1
- Update to 5.1.0-rc1 upstream release

* Fri May 10 2024 Packit <hello@packit.dev> - 5:5.0.3-1
- Update to 5.0.3 upstream release

* Wed Apr 17 2024 Packit <hello@packit.dev> - 5:5.0.2-1
- Update to 5.0.2 upstream release

* Mon Apr 01 2024 Packit <hello@packit.dev> - 5:5.0.1-1
- [packit] 5.0.1 upstream release

* Tue Mar 26 2024 Ed Santiago <santiago@redhat.com> - 5:5.0.0-2
- Podman tests: force-install slirp4netns

* Tue Mar 19 2024 Packit <hello@packit.dev> - 5:5.0.0-1
- [packit] 5.0.0 upstream release

* Fri Mar 15 2024 Packit <hello@packit.dev> - 5:5.0.0~rc7-1
- [packit] 5.0.0-rc7 upstream release

* Wed Mar 13 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:5.0.0~rc6-2
- Resolves: #2269148 - make passt a hard dep

* Mon Mar 11 2024 Packit <hello@packit.dev> - 5:5.0.0~rc6-1
- [packit] 5.0.0-rc6 upstream release

* Fri Mar 08 2024 Packit <hello@packit.dev> - 5:5.0.0~rc5-1
- [packit] 5.0.0-rc5 upstream release

* Tue Mar 05 2024 Packit <hello@packit.dev> - 5:5.0.0~rc4-1
- [packit] 5.0.0-rc4 upstream release

* Thu Feb 29 2024 Debarshi Ray <rishi@fedoraproject.org> - 5:5.0.0~rc3-5
- Show the toolbox RPMs used to run the tests

* Tue Feb 27 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5:5.0.0~rc3-4
- Add fallback for $SOURCE_DATE_EPOCH not being set

* Tue Feb 27 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5:5.0.0~rc3-3
- Make BuildRequires independent of the environment

* Mon Feb 26 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5:5.0.0~rc3-2
- Use $SOURCE_DATE_EPOCH instead of the current date

* Thu Feb 22 2024 Packit <hello@packit.dev> - 5:5.0.0~rc3-1
- [packit] 5.0.0-rc3 upstream release

* Mon Feb 19 2024 Debarshi Ray <rishi@fedoraproject.org> - 5:5.0.0~rc2-2
- Avoid running out of storage space when running the Toolbx tests

* Fri Feb 16 2024 Packit <hello@packit.dev> - 5:5.0.0~rc2-1
- [packit] 5.0.0-rc2 upstream release

* Thu Feb 15 2024 Debarshi Ray <rishi@fedoraproject.org> - 5:5.0.0~rc1-5
- Silence warnings about deprecated grep(1) use in test logs

* Tue Feb 13 2024 Debarshi Ray <rishi@fedoraproject.org> - 5:5.0.0~rc1-4
- Update how Toolbx is spelt

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 5:5.0.0~rc1-3
- Rebuild for golang 1.22.0

* Fri Feb 09 2024 Lokesh Mandvekar <lsm5@redhat.com> - 5:5.0.0~rc1-2
- update podman module version

* Thu Feb 08 2024 Packit <hello@packit.dev> - 5:5.0.0~rc1-1
- [packit] 5.0.0-rc1 upstream release

* Fri Feb 02 2024 Packit <hello@packit.dev> - 5:4.9.2-1
- [packit] 4.9.2 upstream release

* Fri Feb 02 2024 Ed Santiago <santiago@redhat.com> - 5:4.9.1-2
- Much-belated cleanup
- remove all references to cgroups v1. That code never worked, and "cgroups
  v2" in test names was misleading because it implied an alternative.
  Remove it.
- refactor podman remote and local tests
- clean up docs
- Ansible bitrot cleanup ("this is deprecated, use that")

* Thu Feb 01 2024 Packit <hello@packit.dev> - 5:4.9.1-1
- [packit] 4.9.1 upstream release

* Thu Jan 25 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 5:4.9.0-2
- Use go-rpm-macros on RHEL 10

* Wed Jan 24 2024 Packit <hello@packit.dev> - 5:4.9.0-1
- [packit] 4.9.0 upstream release

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5:4.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Packit <hello@packit.dev> - 5:4.8.3-1
- [packit] 4.8.3 upstream release

* Mon Dec 11 2023 Packit <hello@packit.dev> - 5:4.8.2-1
- [packit] 4.8.2 upstream release

* Tue Dec 05 2023 Packit <hello@packit.dev> - 5:4.8.1-1
- [packit] 4.8.1 upstream release

* Mon Nov 27 2023 Packit <hello@packit.dev> - 5:4.8.0-1
- [packit] 4.8.0 upstream release

* Mon Nov 27 2023 Lokesh Mandvekar <lsm5@redhat.com> - 5:4.8.0~rc1-1
- bump to v4.8.0-rc1

* Tue Oct 31 2023 Packit <hello@packit.dev> - 5:4.7.2-1
- [packit] 4.7.2 upstream release

* Thu Oct 05 2023 Packit <hello@packit.dev> - 5:4.7.1-1
- [packit] 4.7.1 upstream release

* Wed Sep 27 2023 Packit <hello@packit.dev> - 5:4.7.0-1
- [packit] 4.7.0 upstream release

* Mon Sep 18 2023 Stephen Gallagher <sgallagh@redhat.com> - 5:4.7.0~rc1-2
- Do not conditionalize sources

* Fri Sep 15 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.7.0~rc1-1
- bump to v4.7.0-rc1

* Tue Sep 12 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.6.2-3
- podman has hard dependency on gvisor-tap-vsock-gvforwarder

* Tue Aug 29 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.6.2-2
- tests: add passt to rpm -qa so we know what version is used in tests

* Mon Aug 28 2023 Packit <hello@packit.dev> - 5:4.6.2-1
- [packit] 4.6.2 upstream release

* Tue Aug 22 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.6.1-2
- spdx compatible version string

* Thu Aug 10 2023 Packit <hello@packit.dev> - 5:4.6.1-1
- [packit] 4.6.1 upstream release

* Mon Jul 24 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.6.0-3
- gvproxy removed for rawhide and copr builds

* Thu Jul 20 2023 Packit <hello@packit.dev> - 5:4.6.0-1
- [packit] 4.6.0 upstream release

* Thu Jul 13 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.6.0~rc2-1
- bump to v4.6.0-rc2

* Mon Jul 03 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.6.0~rc1-1
- bump to v4.6.0-rc1

* Fri May 26 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.5.1-1
- bump to v4.5.1

* Wed May 24 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.5.0-5
- rewrite spec to minimize diff with soon to be upstream packit-maintained
  spec

* Mon May 08 2023 Ed Santiago <santiago@redhat.com> - 5:4.5.0-4
- Disable systemd resolved

* Tue Apr 25 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.5.0-3
- fix macro

* Tue Apr 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5:4.5.0-2
- Disable btrfs in RHEL builds

* Fri Apr 14 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 5:4.5.0-1
- auto bump to v4.5.0

* Wed Apr 12 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.5.0~rc2-1
- bump to v4.5.0-rc2

* Wed Apr 05 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.5.0~rc1-2
- BR: gettext-envsubst

* Wed Apr 05 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.5.0~rc1-1
- bump to v4.5.0-rc1

* Mon Apr 03 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.4.4-4
- Fix ETCDIR usage for future upstream changes in docker wrapper

* Mon Apr 03 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.4.4-3
- Resolves: #2183641 - use min conmon v2.1.7

* Fri Mar 31 2023 Miroslav Vadkerti <mvadkert@redhat.com> - 5:4.4.4-2
- Adjust tests for new Ansible

* Mon Mar 27 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 5:4.4.4-1
- auto bump to v4.4.4

* Fri Mar 24 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.4.3-2
- ensure no buildroot macro left in /usr/bin/docker

* Thu Mar 23 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 5:4.4.3-1
- auto bump to v4.4.3

* Mon Mar 06 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.4.2-3
- migrated to SPDX license

* Wed Mar 01 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.4.2-2
- remove CVE-2023-0778.patch merged upstream

* Tue Feb 28 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 5:4.4.2-1
- auto bump to v4.4.2

* Wed Feb 22 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5:4.4.1-4
- Sync modules-load conditionals

* Fri Feb 17 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.4.1-3
- Resolves: #2168256, #2170631 - CVE-2023-0778

* Mon Feb 13 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.4.1-2
- remove quadlet package specification completely

* Thu Feb 09 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.4.1-1
- bump to v4.4.1

* Thu Feb 02 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.4.0-1
- bump to v4.4.0

* Mon Jan 23 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 5:4.3.1-1
- Revert to v4.3.1 and bump Epoch to 5

* Thu Jan 19 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.4.0~rc2-2
- bump gvproxy to 0.5.0

* Wed Jan 18 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.4.0~rc2-1
- bump to v4.4.0-rc2

* Tue Jan 17 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.4.0~rc1-4
- specify QUADLET envvar in gating test config

* Mon Jan 16 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.4.0~rc1-3
- update bundled golang provides

* Mon Jan 16 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.4.0~rc1-2
- add quadlet subpackage

* Mon Jan 16 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 4:4.4.0~rc1-1
- auto bump to v4.4.0-rc1

* Fri Nov 11 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.3.1-1
- bump to v4.3.1

* Thu Oct 20 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.3.0-2
- fix sdnotify gating test (merged upstream)

* Wed Oct 19 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 4:4.3.0-1
- auto bump to v4.3.0

* Fri Oct 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.3.0~rc1-5
- Revert "auto bump to v4.3.0-rc1"

* Fri Oct 07 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 4:4.3.0~rc1-4
- auto bump to v4.3.0-rc1

* Fri Oct 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.3.0~rc1-3
- update bundled provides

* Fri Oct 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.3.0~rc1-2
- Remove debbuild macros and depend on containers-common-extra

* Tue Sep 27 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 4:4.3.0~rc1-1
- auto bump to v4.3.0-rc1

* Wed Sep 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.1-2
- use correct tarball

* Wed Sep 07 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 4:4.2.1-1
- auto bump to v4.2.1

* Mon Sep 05 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-11
- update license for debbuild

* Fri Aug 26 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-10
- Packit: remove files installed by unreleased versions

* Wed Aug 24 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-9
- use tmpfilesdir macro

* Wed Aug 24 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-8
- account for upcoming /usr/lib/user-tmpfiles.d/podman-docker.conf in
  podman-docker

* Wed Aug 24 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-7
- account for upcoming tmpfilesdir/podman-docker.conf

* Mon Aug 22 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-6
- install systemd units for debbuild

* Fri Aug 19 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-5
- Attempt to fix debian 11 and ubuntu 18.04, 20.04

* Wed Aug 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-4
- use easier tag macros to make both fedora and debbuild happy

* Tue Aug 16 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-3
- Fix debbuild maintainer issue

* Thu Aug 11 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0-2
- fix tarball_tag

* Thu Aug 11 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 4:4.2.0-1
- auto bump to v4.2.0

* Fri Aug 05 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0~rc3-2
- fix tarball_tag macro

* Fri Aug 05 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 4:4.2.0~rc3-1
- auto bump to v4.2.0-rc3

* Wed Aug 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0~rc2-1
- Bump to v4.2.0-rc2

* Fri Jul 22 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.1.1-3
- bump for 4.1.1 rebuild

* Fri Jul 22 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.1.1-2
- bump for 4.1.1 rebuild

* Fri Jul 22 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.1.1-1
- Revert "Bump back to v4.2.0-rc1 with Epoch bump maintained"

* Fri Jul 22 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.2.0~rc1-1
- Bump back to v4.2.0-rc1 with Epoch bump maintained

* Fri Jul 22 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:4.1.1-1
- revert to v4.1.1 with Epoch bump for golang CVE fixes

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:4.2.0~rc1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Maxwell G <gotmax@e.email> - 3:4.2.0~rc1-3
- Rebuild for
  CVE-2022-{1705,32148,30631,30633,28131,30635,30632,30630,1962} in golang

* Mon Jul 11 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.2.0~rc1-2
- tmp fix to unblock build such that debbuild works too

* Mon Jul 11 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:4.2.0~rc1-1
- auto bump to v4.2.0-rc1

* Wed Jul 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.1-4
- podman requires podman-gvproxy

* Wed Jul 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.1-3
- Explicitly list tmpfiles dir for debbuild

* Sat Jun 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 3:4.1.1-2
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327,
  CVE-2022-27191, CVE-2022-29526, CVE-2022-30629

* Wed Jun 15 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:4.1.1-1
- auto bump to v4.1.1

* Mon Jun 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.0-9
- try autochangelog

* Mon May 30 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.0-8
- use new filenames in sources

* Mon May 30 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.0-7
- Revert last 2 commits

* Mon May 30 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.0-6
- remove commented changelog entry

* Mon May 30 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.0-5
- try autochangelog

* Mon May 30 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.0-4
- Resolves: #2090108 - catatonit should be a full dependency

* Fri May 27 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.0-3
- build deb packages using debbuild

* Mon May 09 2022 Ed Santiago <santiago@redhat.com> - 3:4.1.0-2
- setup: log results of 'ip addr'

* Fri May 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.1.0-1
- bump to v4.1.0

* Wed May 04 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:4.1.0~rc2-1
- auto bump to v4.1.0-rc2

* Thu Apr 28 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:4.1.0~rc1-1
- auto bump to v4.1.0-rc1

* Tue Apr 26 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.3-3
- Revert "try autochangelog"

* Tue Apr 26 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.3-2
- try autochangelog

* Fri Apr 01 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:4.0.3-1
- auto bump to v4.0.3

* Tue Mar 29 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.2-5
- update placeholder changelog

* Wed Mar 09 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.2-4
- adjust conditionals for centos 8

* Wed Mar 09 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.2-3
- go-rpm-macros not defined for rhel8

* Mon Mar 07 2022 Ed Santiago <santiago@redhat.com> - 3:4.0.2-2
- Gating tests: include more package versions

* Thu Mar 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.2-1
- bump to v4.0.2

* Fri Feb 25 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.1-2
- add checks for centos to account for rhcontainerbot/podman4 copr

* Fri Feb 25 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.1-1
- bump to v4.0.1, add iptables modules for fedora >= 36

* Mon Feb 21 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-22
- add patch to fix version

* Thu Feb 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-21
- add placeholder changelog entry until autospec bz2051542 is fixed

* Thu Feb 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-20
- remove unwanted conditionals and scriptlets

* Thu Feb 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-19
- remove conditional epoch - probably messes with autospec

* Thu Feb 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-18
- bump to v4.0.0

* Fri Feb 11 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-17
- podman-3:4.0.0-0.7.rc5
- bump to v4.0.0-rc5

* Thu Feb 10 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-16
- podman-3:4.0.0-0.6.rc4
- shadow-utils-subid soname change (update changelog in spec file)

* Thu Feb 10 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-15
- rebuild to be ahead of f36

* Thu Feb 10 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-14
- account for latest shadow-utils-subid

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-13
- bump to v4.0.0-rc4, adjust dependencies

* Mon Jan 31 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-12
- podman-3:4.0.0-0.4.rc3
- fix license, conditionals and update provides

* Mon Jan 31 2022 Lokesh Mandvekar <lsm5@fedoraproject.org>
- remove unused packages, update provides and fix license

* Mon Jan 31 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-10
- list all tarballs in sources

* Mon Jan 31 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-9
- podman-3:4.0.0-0.3.rc3
- bump to v4.0.0-rc3

* Mon Jan 31 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-8
- Revert last 4 commits

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-7
- remove conditional gobuild macro definition

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-6
- bump to v4.0.0-rc3, bump containers-common dep

* Tue Jan 25 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-5
- use updated install targets for upcoming rc

* Mon Jan 24 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-4
- account for md2man in c9s for copr builds

* Fri Jan 21 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:4.0.0-3
- podman-3:4.0.0-0.2.rc2

* Wed Jan 19 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:4.0.0-2
- fix v4.0.0-rc1 build
- got rid of machine-cni
- fixed install.systemd target

* Mon Jan 10 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:4.0.0-1
- podman-3:4.0.0-0.1.rc1

* Wed Dec 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.4.4-1
- podman-3:3.4.4-1

* Tue Dec 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.4.3-1
- podman-3:3.4.3-1

* Fri Nov 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.4.2-1
- podman-3:3.4.2-1

* Fri Nov 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.1-4
- bump gvisor-tap-vsock to v0.3.0

* Thu Nov 11 2021 Ed Santiago <santiago@redhat.com> - 3:3.4.1-3
- podman-tests now Requires: gnupg due to
  https://github.com/containers/podman/pull/12270

* Wed Oct 20 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.1-2
- gating-test.patch merged upstream

* Wed Oct 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.4.1-1
- podman-3:3.4.1-1

* Tue Oct 05 2021 Stephen Gallagher <sgallagh@redhat.com> - 3:3.4.0-20
- Drop i686 support for RHEL >= 9

* Mon Oct 04 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-19
- podman-3:3.4.0-3
- Gating tests: fix permissions error

* Fri Oct 01 2021 Timm Bäder <tbaeder@redhat.com> - 3:3.4.0-18
- Remove hardcoded CFLAGS

* Thu Sep 30 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.4.0-17
- podman-3:3.4.0-1

* Tue Sep 28 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-16
- centos conditionals no longer needed

* Mon Sep 27 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-15
- podman-3:3.4.0-0.11.rc2
- bump containers-common dep

* Fri Sep 24 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-14
- podman-3:3.4.0-0.10.rc2
- build with libsubid buildtag

* Fri Sep 24 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-13
- podman-3:3.4.0-0.9.rc2
- depend on shadow-utils-subid for f35 and higher

* Fri Sep 24 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-12
- podman-3:3.4.0-0.8.rc2
- bump release to stay ahead of older fedora

* Fri Sep 24 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-11
- shadow-utils-subid-devel only for f35 and higher

* Fri Sep 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.4.0-10
- podman-3:3.4.0-0.7.rc2

* Fri Sep 24 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-9
- Revert "require shadow-utils-subid"

* Fri Sep 24 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-8
- require shadow-utils-subid

* Thu Sep 23 2021 Daniel J Walsh <dwalsh@redhat.com> - 3:3.4.0-7
- Add shadow-utils-subid-devel requirement

* Thu Sep 23 2021 Daniel J Walsh <dwalsh@redhat.com> - 3:3.4.0-6
- rm -f /var/lib/containers/storage/libpod/defaultCNINetExists in post

* Wed Sep 22 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-5
- podman-3:3.4.0-0.4.rc1
- bump conmon requirement for remote gating tests

* Wed Sep 22 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-4
- podman-3:3.4.0-0.3.rc1
- Requires: conmon >= 2:2.0.30 for remote gating tests

* Tue Sep 21 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.4.0-3
- podman-3:3.4.0-0.2.rc1
- rebuild for podman-remote gating tests

* Fri Sep 17 2021 Ed Santiago <santiago@redhat.com> - 3:3.4.0-2
- gating tests: run podman-remote too

* Thu Sep 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.4.0-1
- podman-3:3.4.0-0.1.rc1

* Wed Sep 15 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.1-4
- update dnsname and machine-cni to latest upstream tags

* Mon Sep 13 2021 Ed Santiago <santiago@redhat.com> - 3:3.3.1-3
- Gating tests: run toolbox tests

* Tue Aug 31 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.1-2
- podman-3:3.3.1-2
- bump release to be on par with f35

* Mon Aug 30 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.1-1
- podman-3:3.3.1-1

* Fri Aug 27 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-39
- podman-3:3.3.0-2
- update gvproxy binary name

* Fri Aug 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-38
- podman-3:3.3.0-1

* Tue Aug 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-37
- podman-3:3.3.0-0.28.rc3

* Mon Aug 16 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-36
- podman-3:3.3.0-0.27.rc2
- Bump to v3.3.0-rc2
- Include podman-gvproxy subpackage which provides
  /usr/libexecdir/podman/podman-gvproxy

* Thu Aug 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-35
- use %%global instead of %%define

* Tue Aug 03 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-34
- podman-3:3.3.0-0.26.rc1
- Bump to v3.3.0-rc1

* Mon Aug 02 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-33
- podman-3:3.3.0-0.25.dev.gitd32e566
- Resolves: #1983596, #1987739 - Security fix for CVE-2021-34558

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3:3.3.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-31
- podman-3:3.3.0-0.23.dev.gitd32e566
- Resolves: #1969264, #1982881 - Security fix for CVE-2021-3602

* Wed Jul 14 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-30
- podman-3:3.3.0-0.22.dev.git599b7d7
- rebuild with gating.yaml changes

* Tue Jul 13 2021 Adam Williamson <awilliam@redhat.com> - 3:3.3.0-29
- Drop openQA gating policy on main branch

* Tue Jul 06 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-28
- podman-3:3.3.0-0.21.dev.git599b7d7
- rebuild for openQA

* Tue Jul 06 2021 Adam Williamson <awilliam@redhat.com> - 3:3.3.0-27
- Gate on openQA update test results

* Tue Jun 29 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-26
- update dep on containers-common

* Tue Jun 29 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-25
- podman-3:3.3.0-0.20.dev.git599b7d7
- remove /etc/sysconfdir/cni/net.d/87-podman-bridge.conflist
- bodhi will not be ignored for this one so cut us some slack ;)

* Thu Jun 24 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-24
- update min containers-common

* Thu Jun 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-23
- podman-3:3.3.0-0.19.dev.gitfc34f35
- autobuilt fc34f35

* Wed Jun 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-22
- podman-3:3.3.0-0.18.dev.gitd3afc6b
- autobuilt d3afc6b

* Tue Jun 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-21
- podman-3:3.3.0-0.17.dev.gitbe15e69
- autobuilt be15e69

* Mon Jun 21 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-20
- add podman-restart unitfiles

* Mon Jun 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-19
- podman-3:3.3.0-0.16.dev.git18bf92f
- autobuilt 18bf92f

* Mon Jun 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-18
- podman-3:3.3.0-0.15.dev.git928687e
- autobuilt 928687e

* Sun Jun 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-17
- podman-3:3.3.0-0.14.dev.gitd8cd205
- autobuilt d8cd205

* Sat Jun 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-16
- podman-3:3.3.0-0.13.dev.git48db8d9
- autobuilt 48db8d9

* Fri Jun 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-15
- podman-3:3.3.0-0.12.dev.gitce04a3e
- autobuilt ce04a3e

* Thu Jun 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-14
- podman-3:3.3.0-0.11.dev.git814a8b6
- autobuilt 814a8b6

* Wed Jun 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-13
- podman-3:3.3.0-0.10.dev.git092b2ec
- autobuilt 092b2ec

* Tue Jun 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-12
- podman-3:3.3.0-0.9.dev.gite2f51ee
- autobuilt e2f51ee

* Mon Jun 14 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-11
- podman-3:3.3.0-0.8.dev.gite549ca5
- BR: go-rpm-macros to re-enable debuginfo

* Sun Jun 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-10
- podman-3:3.3.0-0.7.dev.gite549ca5
- autobuilt e549ca5

* Sat Jun 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-9
- podman-3:3.3.0-0.6.dev.git45dc3d6
- autobuilt 45dc3d6

* Fri Jun 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-8
- podman-3:3.3.0-0.5.dev.gited983c9
- autobuilt ed983c9

* Thu Jun 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-7
- podman-3:3.3.0-0.4.dev.gitea39735
- autobuilt ea39735

* Wed Jun 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-6
- podman-3:3.3.0-0.3.dev.gitda1bade
- autobuilt da1bade

* Tue Jun 08 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-5
- import podman-machine-cni tarball

* Tue Jun 08 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-4
- disable debuginfo for rawhide

* Tue Jun 08 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-3
- podman-3:3.3.0-0.2.dev.git9a3a732
- include podman-machine-cni in podman-plugins subpackage

* Tue Jun 08 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.3.0-2
- include podman-machine-cni in podman-plugins subpackage

* Tue Jun 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.3.0-1
- podman-3:3.3.0-0.1.dev.git9a3a732
- bump to 3.3.0
- autobuilt 9a3a732

* Tue May 18 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.2.0-12
- podman-3:3.2.0-0.27.dev.git353f04b
- disable debuginfo temporarily to get a successful build past gating
  issues

* Tue May 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.2.0-11
- podman-3:3.2.0-0.26.dev.git353f04b
- autobuilt 353f04b

* Tue May 18 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.2.0-10
- podman-3:3.2.0-0.25.dev.gita7fa0da
- use containers-common >= 4:1-19 with container-selinux 2.162.1

* Tue May 18 2021 Ed Santiago <santiago@redhat.com> - 3:3.2.0-9
- gating tests: include kernel version in Packages output

* Tue May 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.2.0-8
- podman-3:3.2.0-0.24.dev.gita7fa0da
- autobuilt a7fa0da

* Mon May 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.2.0-7
- podman-3:3.2.0-0.23.dev.gita6a3df0
- autobuilt a6a3df0

* Sun May 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.2.0-6
- podman-3:3.2.0-0.22.dev.git90a12ac
- autobuilt 90a12ac

* Sat May 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.2.0-5
- podman-3:3.2.0-0.21.dev.git2b0b971
- autobuilt 2b0b971

* Thu May 13 2021 Daniel J Walsh <dwalsh@redhat.com> - 3:3.2.0-4
- Add suggests qemu-user-static

* Thu May 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.2.0-3
- podman-3:3.2.0-0.19.dev.git4dc52f6
- autobuilt 4dc52f6

* Wed May 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 3:3.2.0-2
- podman-3:3.2.0-0.18.dev.git59dd357
- autobuilt 59dd357

* Tue May 11 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 3:3.2.0-1
- podman-3:3.2.0-0.17.dev.git57b6425
- bump epoch to account for bad v3.2.0-rc1 in stable

* Tue May 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-16
- podman-2:3.2.0-0.16.dev.git57b6425
- autobuilt 57b6425

* Sun May 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-15
- podman-2:3.2.0-0.15.dev.git54bed10
- autobuilt 54bed10

* Sat May 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-14
- podman-2:3.2.0-0.14.dev.git141d3f1
- autobuilt 141d3f1

* Fri May 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-13
- podman-2:3.2.0-0.13.dev.git5616887
- autobuilt 5616887

* Fri May 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-12
- podman-2:3.2.0-0.12.dev.gitb533fcb
- autobuilt b533fcb

* Thu May 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-11
- podman-2:3.2.0-0.11.dev.git8cc96bd
- autobuilt 8cc96bd

* Thu May 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-10
- podman-2:3.2.0-0.10.dev.gitb6405c1
- autobuilt b6405c1

* Mon May 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-9
- podman-2:3.2.0-0.9.dev.git697ec8f
- autobuilt 697ec8f

* Wed Apr 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-8
- podman-2:3.2.0-0.8.dev.git4ca34fc
- autobuilt 4ca34fc

* Wed Apr 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-7
- podman-2:3.2.0-0.7.dev.git99e5a76
- autobuilt 99e5a76

* Tue Apr 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-6
- podman-2:3.2.0-0.6.dev.git3148e01
- autobuilt 3148e01

* Mon Apr 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-5
- podman-2:3.2.0-0.5.dev.git476c76f
- autobuilt 476c76f

* Tue Apr 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-4
- podman-2:3.2.0-0.4.dev.gitcf2c3a1
- autobuilt cf2c3a1

* Fri Apr 16 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.2.0-3
- podman-2:3.2.0-0.3.dev.git35b62ef
- slirp4netns and fuse-overlayfs deps are in containers-common

* Thu Apr 15 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.2.0-2
- podman-2:3.2.0-0.2.dev.git373f15f
- container-selinux and crun dependencies moved to containers-common

* Thu Apr 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.2.0-1
- podman-2:3.2.0-0.1.dev.git373f15f
- bump to 3.2.0
- autobuilt 373f15f

* Mon Apr 05 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.1.0-105
- podman-2:3.1.0-0.102.dev.git259004f
- adjust dependencies

* Mon Mar 29 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.1.0-104
- fix build issues on 32-bit

* Mon Mar 29 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-103
- podman-2:3.1.0-0.101.dev.git259004f
- autobuilt 259004f

* Thu Mar 25 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.1.0-102
- podman-2:3.1.0-0.100.dev.gitdf1d561
- bump crun requirement

* Mon Mar 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-101
- podman-2:3.1.0-0.99.dev.gitdf1d561
- autobuilt df1d561

* Mon Mar 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-100
- podman-2:3.1.0-0.98.dev.gite7dc592
- autobuilt e7dc592

* Fri Mar 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-99
- podman-2:3.1.0-0.97.dev.gitfc02d16
- autobuilt fc02d16

* Fri Mar 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-98
- podman-2:3.1.0-0.96.dev.git5b22ddd
- autobuilt 5b22ddd

* Thu Mar 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-97
- podman-2:3.1.0-0.95.dev.git81737b3
- autobuilt 81737b3

* Thu Mar 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-96
- podman-2:3.1.0-0.94.dev.git8d33bfa
- autobuilt 8d33bfa

* Wed Mar 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-95
- podman-2:3.1.0-0.93.dev.gite2d35e5
- autobuilt e2d35e5

* Wed Mar 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-94
- podman-2:3.1.0-0.92.dev.git786757f
- autobuilt 786757f

* Wed Mar 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-93
- podman-2:3.1.0-0.91.dev.git5331096
- autobuilt 5331096

* Wed Mar 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-92
- podman-2:3.1.0-0.90.dev.git1ac2fb7
- autobuilt 1ac2fb7

* Tue Mar 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-91
- podman-2:3.1.0-0.89.dev.git09473d4
- autobuilt 09473d4

* Tue Mar 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-90
- podman-2:3.1.0-0.88.dev.git66ac942
- autobuilt 66ac942

* Tue Mar 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-89
- podman-2:3.1.0-0.87.dev.git36ec835
- autobuilt 36ec835

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-88
- podman-2:3.1.0-0.86.dev.git789d579
- autobuilt 789d579

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-87
- podman-2:3.1.0-0.85.dev.gitff46d13
- autobuilt ff46d13

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-86
- podman-2:3.1.0-0.84.dev.gitba36d79
- autobuilt ba36d79

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-85
- podman-2:3.1.0-0.83.dev.gitb386d23
- autobuilt b386d23

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-84
- podman-2:3.1.0-0.82.dev.git1e1035c
- autobuilt 1e1035c

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-83
- podman-2:3.1.0-0.81.dev.gitb6079bc
- autobuilt b6079bc

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-82
- podman-2:3.1.0-0.80.dev.git6fe634c
- autobuilt 6fe634c

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-81
- podman-2:3.1.0-0.79.dev.git7c09752
- autobuilt 7c09752

* Sun Mar 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-80
- podman-2:3.1.0-0.78.dev.gitb7c00f2
- autobuilt b7c00f2

* Sat Mar 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-79
- podman-2:3.1.0-0.77.dev.gita9fcd9d
- autobuilt a9fcd9d

* Sat Mar 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-78
- podman-2:3.1.0-0.76.dev.git77a597a
- autobuilt 77a597a

* Fri Mar 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-77
- podman-2:3.1.0-0.75.dev.git2a78157
- autobuilt 2a78157

* Fri Mar 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-76
- podman-2:3.1.0-0.74.dev.git44e6d20
- autobuilt 44e6d20

* Fri Mar 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-75
- podman-2:3.1.0-0.73.dev.git0bac30d
- autobuilt 0bac30d

* Fri Mar 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-74
- podman-2:3.1.0-0.72.dev.gitc6cefa5
- autobuilt c6cefa5

* Fri Mar 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-73
- podman-2:3.1.0-0.71.dev.git05080a1
- autobuilt 05080a1

* Thu Mar 04 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.1.0-72
- add macros for autobuilding on non-rawhide

* Thu Mar 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-71
- podman-2:3.1.0-0.70.dev.git4e5cc6a
- autobuilt 4e5cc6a

* Thu Mar 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-70
- podman-2:3.1.0-0.69.dev.gite65bcc1
- autobuilt e65bcc1

* Thu Mar 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-69
- podman-2:3.1.0-0.68.dev.git7a92de4
- autobuilt 7a92de4

* Thu Mar 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-68
- podman-2:3.1.0-0.67.dev.git87a78c0
- autobuilt 87a78c0

* Thu Mar 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-67
- podman-2:3.1.0-0.66.dev.git17cacea
- autobuilt 17cacea

* Thu Mar 04 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.1.0-66
- install.docker-docs-nobuild Makefile target added upstream

* Wed Mar 03 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.1.0-65
- podman-2:3.1.0-0.65.dev.git87e2056
- built 87e2056

* Tue Mar 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-64
- podman-2:3.1.0-0.64.dev.git426178a
- autobuilt 426178a

* Tue Mar 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-63
- podman-2:3.1.0-0.63.dev.gitc726732
- autobuilt c726732

* Tue Mar 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-62
- podman-2:3.1.0-0.62.dev.git7497dcb
- autobuilt 7497dcb

* Mon Mar 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-61
- podman-2:3.1.0-0.61.dev.git8af6680
- autobuilt 8af6680

* Mon Mar 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-60
- podman-2:3.1.0-0.60.dev.git73044b2
- autobuilt 73044b2

* Mon Mar 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-59
- podman-2:3.1.0-0.59.dev.git8daa014
- autobuilt 8daa014

* Mon Mar 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-58
- podman-2:3.1.0-0.58.dev.gitb5827d8
- autobuilt b5827d8

* Mon Mar 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-57
- podman-2:3.1.0-0.57.dev.gitb154c51
- autobuilt b154c51

* Sat Feb 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-56
- podman-2:3.1.0-0.56.dev.git9600ea6
- autobuilt 9600ea6

* Fri Feb 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-55
- podman-2:3.1.0-0.55.dev.git397aae3
- autobuilt 397aae3

* Fri Feb 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-54
- podman-2:3.1.0-0.54.dev.git05410e8
- autobuilt 05410e8

* Thu Feb 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-53
- podman-2:3.1.0-0.53.dev.gitbde1d3f
- autobuilt bde1d3f

* Thu Feb 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-52
- podman-2:3.1.0-0.52.dev.gitb220d6c
- autobuilt b220d6c

* Thu Feb 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-51
- podman-2:3.1.0-0.51.dev.git9ec8106
- autobuilt 9ec8106

* Thu Feb 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-50
- podman-2:3.1.0-0.50.dev.git79e8032
- autobuilt 79e8032

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-49
- podman-2:3.1.0-0.49.dev.git25d8195
- autobuilt 25d8195

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-48
- podman-2:3.1.0-0.48.dev.gitdec06b1
- autobuilt dec06b1

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-47
- podman-2:3.1.0-0.47.dev.git49fa19d
- autobuilt 49fa19d

* Tue Feb 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-46
- podman-2:3.1.0-0.46.dev.gitca0af71
- autobuilt ca0af71

* Tue Feb 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-45
- podman-2:3.1.0-0.45.dev.git4dfcd58
- autobuilt 4dfcd58

* Tue Feb 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-44
- podman-2:3.1.0-0.44.dev.git1702cbc
- autobuilt 1702cbc

* Tue Feb 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-43
- podman-2:3.1.0-0.43.dev.git96fc9d9
- autobuilt 96fc9d9

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-42
- podman-2:3.1.0-0.42.dev.gitd999328
- autobuilt d999328

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-41
- podman-2:3.1.0-0.41.dev.gitc69decc
- autobuilt c69decc

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-40
- podman-2:3.1.0-0.40.dev.gita6e7d19
- autobuilt a6e7d19

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-39
- podman-2:3.1.0-0.39.dev.gitf8ff172
- autobuilt f8ff172

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-38
- podman-2:3.1.0-0.38.dev.gitcb3af5b
- autobuilt cb3af5b

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-37
- podman-2:3.1.0-0.37.dev.git6fbf73e
- autobuilt 6fbf73e

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-36
- podman-2:3.1.0-0.36.dev.git10d52c0
- autobuilt 10d52c0

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-35
- podman-2:3.1.0-0.35.dev.gitd92b946
- autobuilt d92b946

* Sun Feb 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-34
- podman-2:3.1.0-0.34.dev.git4a6582b
- autobuilt 4a6582b

* Sun Feb 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-33
- podman-2:3.1.0-0.33.dev.git7b52654
- autobuilt 7b52654

* Fri Feb 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-32
- podman-2:3.1.0-0.32.dev.git4aaaa6c
- autobuilt 4aaaa6c

* Fri Feb 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-31
- podman-2:3.1.0-0.31.dev.gitb6db60e
- autobuilt b6db60e

* Fri Feb 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-30
- podman-2:3.1.0-0.30.dev.git6a9257a
- autobuilt 6a9257a

* Thu Feb 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-29
- podman-2:3.1.0-0.29.dev.git1c6c94d
- autobuilt 1c6c94d

* Thu Feb 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-28
- podman-2:3.1.0-0.28.dev.gitb2bb05d
- autobuilt b2bb05d

* Thu Feb 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-27
- podman-2:3.1.0-0.27.dev.gitc3419d2
- autobuilt c3419d2

* Wed Feb 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-26
- podman-2:3.1.0-0.26.dev.gitd48f4a0
- autobuilt d48f4a0

* Wed Feb 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-25
- podman-2:3.1.0-0.25.dev.git516dc6d
- autobuilt 516dc6d

* Wed Feb 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-24
- podman-2:3.1.0-0.24.dev.git2e522ff
- autobuilt 2e522ff

* Wed Feb 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-23
- podman-2:3.1.0-0.23.dev.gitd55d80a
- autobuilt d55d80a

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-22
- podman-2:3.1.0-0.22.dev.git5004212
- autobuilt 5004212

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-21
- podman-2:3.1.0-0.21.dev.git7fb347a
- autobuilt 7fb347a

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-20
- podman-2:3.1.0-0.20.dev.git58a4793
- autobuilt 58a4793

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-19
- podman-2:3.1.0-0.19.dev.gitaadb16d
- autobuilt aadb16d

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-18
- podman-2:3.1.0-0.18.dev.git8c444e6
- autobuilt 8c444e6

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-17
- podman-2:3.1.0-0.17.dev.gitac9a048
- autobuilt ac9a048

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-16
- podman-2:3.1.0-0.16.dev.gitdf8ba7f
- autobuilt df8ba7f

* Mon Feb 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-15
- podman-2:3.1.0-0.15.dev.git30607d7
- autobuilt 30607d7

* Sat Feb 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-14
- podman-2:3.1.0-0.14.dev.git3ba0afd
- autobuilt 3ba0afd

* Sat Feb 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-13
- podman-2:3.1.0-0.13.dev.git9d57aa7
- autobuilt 9d57aa7

* Fri Feb 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-12
- podman-2:3.1.0-0.12.dev.git87b2722
- autobuilt 87b2722

* Fri Feb 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-11
- podman-2:3.1.0-0.11.dev.git1d15ed7
- autobuilt 1d15ed7

* Fri Feb 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-10
- podman-2:3.1.0-0.10.dev.git73cf06a
- autobuilt 73cf06a

* Fri Feb 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-9
- podman-2:3.1.0-0.9.dev.git291f596
- autobuilt 291f596

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-8
- podman-2:3.1.0-0.8.dev.git1b284a2
- autobuilt 1b284a2

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-7
- podman-2:3.1.0-0.7.dev.gitb38b143
- autobuilt b38b143

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-6
- podman-2:3.1.0-0.6.dev.gita500d93
- autobuilt a500d93

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-5
- podman-2:3.1.0-0.5.dev.gitafe4ce6
- autobuilt afe4ce6

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-4
- podman-2:3.1.0-0.4.dev.gitca354f1
- autobuilt ca354f1

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-3
- podman-2:3.1.0-0.3.dev.gitdb64865
- autobuilt db64865

* Wed Feb 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-2
- podman-2:3.1.0-0.2.dev.git4d604c1
- autobuilt 4d604c1

* Wed Feb 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.1.0-1
- podman-2:3.1.0-0.1.dev.git88ab83d
- bump to 3.1.0
- autobuilt 88ab83d

* Wed Feb 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-219
- podman-2:3.0.0-0.213.dev.gitb4ca924
- autobuilt b4ca924

* Wed Feb 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-218
- podman-2:3.0.0-0.212.dev.git629a979
- autobuilt 629a979

* Wed Feb 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-217
- podman-2:3.0.0-0.211.dev.git055e2dd
- autobuilt 055e2dd

* Wed Feb 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-216
- podman-2:3.0.0-0.210.dev.git2d829ae
- autobuilt 2d829ae

* Tue Feb 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-215
- podman-2:3.0.0-0.209.dev.git8600c3b
- autobuilt 8600c3b

* Tue Feb 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-214
- podman-2:3.0.0-0.208.dev.git763d522
- autobuilt 763d522

* Tue Feb 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-213
- podman-2:3.0.0-0.207.dev.gitf98605e
- autobuilt f98605e

* Tue Feb 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-212
- podman-2:3.0.0-0.206.dev.git9da4169
- autobuilt 9da4169

* Mon Feb 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-211
- podman-2:3.0.0-0.205.dev.git19507d0
- autobuilt 19507d0

* Wed Feb 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-210
- podman-2:3.0.0-0.204.dev.gita086f60
- autobuilt a086f60

* Wed Feb 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-209
- podman-2:3.0.0-0.203.dev.git9742165
- autobuilt 9742165

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-208
- podman-2:3.0.0-0.202.dev.gitd1e0afd
- autobuilt d1e0afd

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-207
- podman-2:3.0.0-0.201.dev.gitaab8a93
- autobuilt aab8a93

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-206
- podman-2:3.0.0-0.200.dev.git628b0d7
- autobuilt 628b0d7

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-205
- podman-2:3.0.0-0.199.dev.gitd66a18c
- autobuilt d66a18c

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-204
- podman-2:3.0.0-0.198.dev.git828279d
- autobuilt 828279d

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-203
- podman-2:3.0.0-0.197.dev.git2314af7
- autobuilt 2314af7

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-202
- podman-2:3.0.0-0.196.dev.git52575db
- autobuilt 52575db

* Mon Feb 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-201
- podman-2:3.0.0-0.195.dev.git48a0e00
- autobuilt 48a0e00

* Mon Feb 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-200
- podman-2:3.0.0-0.194.dev.git182e841
- autobuilt 182e841

* Mon Feb 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-199
- podman-2:3.0.0-0.193.dev.git2018334
- autobuilt 2018334

* Mon Feb 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-198
- podman-2:3.0.0-0.192.dev.gitb045c17
- autobuilt b045c17

* Mon Feb 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-197
- podman-2:3.0.0-0.191.dev.git4ead806
- autobuilt 4ead806

* Sat Jan 30 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-196
- podman-2:3.0.0-0.190.dev.git735b16e
- autobuilt 735b16e

* Fri Jan 29 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-195
- podman-2:3.0.0-0.189.dev.git2686e40
- autobuilt 2686e40

* Fri Jan 29 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-194
- podman-2:3.0.0-0.188.dev.gitf3a7bc1
- autobuilt f3a7bc1

* Fri Jan 29 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-193
- podman-2:3.0.0-0.187.dev.git4ee66c2
- autobuilt 4ee66c2

* Thu Jan 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-192
- podman-2:3.0.0-0.186.dev.git0c6a889
- autobuilt 0c6a889

* Thu Jan 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-191
- podman-2:3.0.0-0.185.dev.git2ee034c
- autobuilt 2ee034c

* Thu Jan 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-190
- podman-2:3.0.0-0.184.dev.gitfb653c4
- autobuilt fb653c4

* Wed Jan 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-189
- podman-2:3.0.0-0.183.dev.git9d59daa
- autobuilt 9d59daa

* Wed Jan 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-188
- podman-2:3.0.0-0.182.dev.git14cc4aa
- autobuilt 14cc4aa

* Wed Jan 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-187
- podman-2:3.0.0-0.181.dev.git1814fa2
- autobuilt 1814fa2

* Wed Jan 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-186
- podman-2:3.0.0-0.180.dev.git2ff4da9
- autobuilt 2ff4da9

* Wed Jan 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-185
- podman-2:3.0.0-0.179.dev.git179b9d1
- autobuilt 179b9d1

* Wed Jan 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-184
- podman-2:3.0.0-0.178.dev.git2102e26
- autobuilt 2102e26

* Wed Jan 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-183
- podman-2:3.0.0-0.177.dev.gitc3b3984
- autobuilt c3b3984

* Tue Jan 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-182
- podman-2:3.0.0-0.176.dev.git5d44446
- autobuilt 5d44446

* Tue Jan 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-181
- podman-2:3.0.0-0.175.dev.gitad1e0bb
- autobuilt ad1e0bb

* Tue Jan 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-180
- podman-2:3.0.0-0.174.dev.gitf13385e
- autobuilt f13385e

* Tue Jan 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-179
- podman-2:3.0.0-0.173.dev.gitefcd48b
- autobuilt efcd48b

* Tue Jan 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-178
- podman-2:3.0.0-0.172.dev.gite5e447d
- autobuilt e5e447d

* Tue Jan 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-177
- podman-2:3.0.0-0.171.dev.git79565d1
- autobuilt 79565d1

* Mon Jan 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-176
- podman-2:3.0.0-0.170.dev.git6ba8819
- autobuilt 6ba8819

* Mon Jan 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-175
- podman-2:3.0.0-0.169.dev.git63cef43
- autobuilt 63cef43

* Mon Jan 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-174
- podman-2:3.0.0-0.168.dev.git23b879d
- autobuilt 23b879d

* Mon Jan 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-173
- podman-2:3.0.0-0.167.dev.gitf4e8572
- autobuilt f4e8572

* Mon Jan 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-172
- podman-2:3.0.0-0.166.dev.gitb4b7838
- autobuilt b4b7838

* Sun Jan 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-171
- podman-2:3.0.0-0.165.dev.git479fc22
- autobuilt 479fc22

* Sat Jan 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-170
- podman-2:3.0.0-0.164.dev.git3f5af4e
- autobuilt 3f5af4e

* Sat Jan 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-169
- podman-2:3.0.0-0.163.dev.git6cef7c7
- autobuilt 6cef7c7

* Fri Jan 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-168
- podman-2:3.0.0-0.162.dev.git474ba4c
- autobuilt 474ba4c

* Fri Jan 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-167
- podman-2:3.0.0-0.161.dev.git47616fe
- autobuilt 47616fe

* Thu Jan 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-166
- podman-2:3.0.0-0.160.dev.git6fd83de
- autobuilt 6fd83de

* Thu Jan 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-165
- podman-2:3.0.0-0.159.dev.git3ba1a8d
- autobuilt 3ba1a8d

* Thu Jan 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-164
- podman-2:3.0.0-0.158.dev.gitd102d02
- autobuilt d102d02

* Thu Jan 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-163
- podman-2:3.0.0-0.157.dev.git7d297dd
- autobuilt 7d297dd

* Thu Jan 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-162
- podman-2:3.0.0-0.156.dev.git5598229
- autobuilt 5598229

* Wed Jan 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-161
- podman-2:3.0.0-0.155.dev.git14443cc
- autobuilt 14443cc

* Wed Jan 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-160
- podman-2:3.0.0-0.154.dev.gitfe4f9ba
- autobuilt fe4f9ba

* Wed Jan 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-159
- podman-2:3.0.0-0.153.dev.git7d024a2
- autobuilt 7d024a2

* Wed Jan 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-158
- podman-2:3.0.0-0.152.dev.git54c465b
- autobuilt 54c465b

* Tue Jan 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-157
- podman-2:3.0.0-0.151.dev.git5e7262d
- autobuilt 5e7262d

* Tue Jan 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-156
- podman-2:3.0.0-0.150.dev.gitd99e475
- autobuilt d99e475

* Tue Jan 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-155
- podman-2:3.0.0-0.149.dev.git8c6df5e
- autobuilt 8c6df5e

* Tue Jan 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-154
- podman-2:3.0.0-0.148.dev.git9a10f20
- autobuilt 9a10f20

* Mon Jan 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-153
- podman-2:3.0.0-0.147.dev.git5f1a7a7
- autobuilt 5f1a7a7

* Sun Jan 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-152
- podman-2:3.0.0-0.146.dev.git5b3c7a5
- autobuilt 5b3c7a5

* Sun Jan 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-151
- podman-2:3.0.0-0.145.dev.git341c4b1
- autobuilt 341c4b1

* Sat Jan 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-150
- podman-2:3.0.0-0.144.dev.git73b036d
- autobuilt 73b036d

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-149
- podman-2:3.0.0-0.143.dev.git83ed464
- autobuilt 83ed464

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-148
- podman-2:3.0.0-0.142.dev.git0400dc0
- autobuilt 0400dc0

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-147
- podman-2:3.0.0-0.141.dev.git7d3a628
- autobuilt 7d3a628

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-146
- podman-2:3.0.0-0.140.dev.git5a166b2
- autobuilt 5a166b2

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-145
- podman-2:3.0.0-0.139.dev.git3ceef00
- autobuilt 3ceef00

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-144
- podman-2:3.0.0-0.138.dev.git3fcf346
- autobuilt 3fcf346

* Thu Jan 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-143
- podman-2:3.0.0-0.137.dev.git2b7793b
- autobuilt 2b7793b

* Thu Jan 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-142
- podman-2:3.0.0-0.136.dev.gita944f90
- autobuilt a944f90

* Thu Jan 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-141
- podman-2:3.0.0-0.135.dev.git9f50d48
- autobuilt 9f50d48

* Thu Jan 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-140
- podman-2:3.0.0-0.134.dev.git4e4477c
- autobuilt 4e4477c

* Wed Jan 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-139
- podman-2:3.0.0-0.133.dev.gitb2ac2a3
- autobuilt b2ac2a3

* Wed Jan 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-138
- podman-2:3.0.0-0.132.dev.gitbbff9c8
- autobuilt bbff9c8

* Wed Jan 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-137
- podman-2:3.0.0-0.131.dev.git9473dda
- autobuilt 9473dda

* Wed Jan 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-136
- podman-2:3.0.0-0.130.dev.git99c5746
- autobuilt 99c5746

* Wed Jan 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-135
- podman-2:3.0.0-0.129.dev.git183f443
- autobuilt 183f443

* Wed Jan 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-134
- podman-2:3.0.0-0.128.dev.gitf52a9ee
- autobuilt f52a9ee

* Tue Jan 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-133
- podman-2:3.0.0-0.127.dev.git265ec91
- autobuilt 265ec91

* Tue Jan 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-132
- podman-2:3.0.0-0.126.dev.git0ccc888
- autobuilt 0ccc888

* Tue Jan 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-131
- podman-2:3.0.0-0.125.dev.git0532fda
- autobuilt 0532fda

* Tue Jan 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-130
- podman-2:3.0.0-0.124.dev.git64b86d0
- autobuilt 64b86d0

* Tue Jan 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-129
- podman-2:3.0.0-0.123.dev.git5575c7b
- autobuilt 5575c7b

* Mon Jan 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-128
- podman-2:3.0.0-0.122.dev.git5681907
- autobuilt 5681907

* Mon Jan 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-127
- podman-2:3.0.0-0.121.dev.git20217f5
- autobuilt 20217f5

* Mon Jan 11 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.0.0-126
- BR: git-core instead of git

* Mon Jan 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-125
- podman-2:3.0.0-0.120.dev.gitd2503ae
- autobuilt d2503ae

* Mon Jan 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-124
- podman-2:3.0.0-0.119.dev.git3b987a7
- autobuilt 3b987a7

* Sun Jan 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-123
- podman-2:3.0.0-0.118.dev.git41613bd
- autobuilt 41613bd

* Sun Jan 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-122
- podman-2:3.0.0-0.117.dev.gitbc0fa65
- autobuilt bc0fa65

* Fri Jan 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-121
- podman-2:3.0.0-0.116.dev.git49db79e
- autobuilt 49db79e

* Fri Jan 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-120
- podman-2:3.0.0-0.115.dev.gita0b432d
- autobuilt a0b432d

* Thu Jan 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-119
- podman-2:3.0.0-0.114.dev.git78cda71
- autobuilt 78cda71

* Thu Jan 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-118
- podman-2:3.0.0-0.113.dev.git3cf41c4
- autobuilt 3cf41c4

* Thu Jan 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-117
- podman-2:3.0.0-0.112.dev.gita475150
- autobuilt a475150

* Thu Jan 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-116
- podman-2:3.0.0-0.111.dev.git355e387
- autobuilt 355e387

* Wed Jan 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-115
- podman-2:3.0.0-0.110.dev.gitbb82c37
- autobuilt bb82c37

* Tue Jan 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-114
- podman-2:3.0.0-0.109.dev.gitffe2b1e
- autobuilt ffe2b1e

* Tue Jan 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-113
- podman-2:3.0.0-0.108.dev.git1f59276
- autobuilt 1f59276

* Tue Jan 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-112
- podman-2:3.0.0-0.107.dev.gitb84b7c8
- autobuilt b84b7c8

* Tue Jan 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-111
- podman-2:3.0.0-0.106.dev.gitbc21fab
- autobuilt bc21fab

* Tue Jan 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-110
- podman-2:3.0.0-0.105.dev.git1b9366d
- autobuilt 1b9366d

* Tue Jan 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-109
- podman-2:3.0.0-0.104.dev.git618c355
- autobuilt 618c355

* Mon Jan 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-108
- podman-2:3.0.0-0.103.dev.gitced7c0a
- autobuilt ced7c0a

* Mon Jan 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-107
- podman-2:3.0.0-0.102.dev.gitb502854
- autobuilt b502854

* Mon Jan 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-106
- podman-2:3.0.0-0.101.dev.git6a1fbe7
- autobuilt 6a1fbe7

* Mon Jan 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-105
- podman-2:3.0.0-0.100.dev.gitf261bfc
- autobuilt f261bfc

* Mon Jan 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-104
- podman-2:3.0.0-0.99.dev.git8e4d19d
- autobuilt 8e4d19d

* Mon Jan 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-103
- podman-2:3.0.0-0.98.dev.git23f25b8
- autobuilt 23f25b8

* Sat Jan 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-102
- podman-2:3.0.0-0.97.dev.git142b4ac
- autobuilt 142b4ac

* Thu Dec 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-101
- podman-2:3.0.0-0.96.dev.git39b1cb4
- autobuilt 39b1cb4

* Wed Dec 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-100
- podman-2:3.0.0-0.95.dev.gitc6c9b45
- autobuilt c6c9b45

* Wed Dec 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-99
- podman-2:3.0.0-0.94.dev.gitef12e36
- autobuilt ef12e36

* Wed Dec 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-98
- podman-2:3.0.0-0.93.dev.git7f0771f
- autobuilt 7f0771f

* Fri Dec 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-97
- podman-2:3.0.0-0.92.dev.git9c9f02a
- autobuilt 9c9f02a

* Thu Dec 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-96
- podman-2:3.0.0-0.91.dev.git8f75ed9
- autobuilt 8f75ed9

* Thu Dec 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-95
- podman-2:3.0.0-0.90.dev.gitb176c62
- autobuilt b176c62

* Thu Dec 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-94
- podman-2:3.0.0-0.89.dev.git231c528
- autobuilt 231c528

* Wed Dec 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-93
- podman-2:3.0.0-0.88.dev.git9ac5ed1
- autobuilt 9ac5ed1

* Wed Dec 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-92
- podman-2:3.0.0-0.87.dev.gitbbc0deb
- autobuilt bbc0deb

* Wed Dec 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-91
- podman-2:3.0.0-0.86.dev.git54b82a1
- autobuilt 54b82a1

* Wed Dec 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-90
- podman-2:3.0.0-0.85.dev.git0778c11
- autobuilt 0778c11

* Wed Dec 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-89
- podman-2:3.0.0-0.84.dev.git3728ca9
- autobuilt 3728ca9

* Wed Dec 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-88
- podman-2:3.0.0-0.83.dev.git06a6fd9
- autobuilt 06a6fd9

* Wed Dec 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-87
- podman-2:3.0.0-0.82.dev.git9b6324f
- autobuilt 9b6324f

* Tue Dec 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-86
- podman-2:3.0.0-0.81.dev.git07663f7
- autobuilt 07663f7

* Tue Dec 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-85
- podman-2:3.0.0-0.80.dev.gitcfdb8fb
- autobuilt cfdb8fb

* Tue Dec 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-84
- podman-2:3.0.0-0.79.dev.gitb4692f2
- autobuilt b4692f2

* Mon Dec 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-83
- podman-2:3.0.0-0.78.dev.git182646b
- autobuilt 182646b

* Mon Dec 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-82
- podman-2:3.0.0-0.77.dev.git076f77b
- autobuilt 076f77b

* Mon Dec 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-81
- podman-2:3.0.0-0.76.dev.gitd692518
- autobuilt d692518

* Fri Dec 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-80
- podman-2:3.0.0-0.75.dev.git5c6b5ef
- autobuilt 5c6b5ef

* Fri Dec 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-79
- podman-2:3.0.0-0.74.dev.gitf568658
- autobuilt f568658

* Thu Dec 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-78
- podman-2:3.0.0-0.73.dev.gita17afa9
- autobuilt a17afa9

* Thu Dec 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-77
- podman-2:3.0.0-0.72.dev.git0333366
- autobuilt 0333366

* Thu Dec 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-76
- podman-2:3.0.0-0.71.dev.git7592f8f
- autobuilt 7592f8f

* Thu Dec 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-75
- podman-2:3.0.0-0.70.dev.gitd291013
- autobuilt d291013

* Thu Dec 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-74
- podman-2:3.0.0-0.69.dev.gitc38ae47
- autobuilt c38ae47

* Wed Dec 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-73
- podman-2:3.0.0-0.68.dev.git915ae6d
- autobuilt 915ae6d

* Wed Dec 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-72
- podman-2:3.0.0-0.67.dev.git2a21dcd
- autobuilt 2a21dcd

* Wed Dec 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-71
- podman-2:3.0.0-0.66.dev.gitbacb2fc
- autobuilt bacb2fc

* Wed Dec 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-70
- podman-2:3.0.0-0.65.dev.git978c076
- autobuilt 978c076

* Wed Dec 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-69
- podman-2:3.0.0-0.64.dev.gitf1f7b8f
- autobuilt f1f7b8f

* Wed Dec 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-68
- podman-2:3.0.0-0.63.dev.git8333a9e
- autobuilt 8333a9e

* Tue Dec 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-67
- podman-2:3.0.0-0.62.dev.git66e979a
- autobuilt 66e979a

* Tue Dec 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-66
- podman-2:3.0.0-0.61.dev.gite689503
- autobuilt e689503

* Tue Dec 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-65
- podman-2:3.0.0-0.60.dev.git9379ee9
- autobuilt 9379ee9

* Mon Dec 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-64
- podman-2:3.0.0-0.59.dev.git999d40d
- autobuilt 999d40d

* Mon Dec 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-63
- podman-2:3.0.0-0.58.dev.git0fd31e2
- autobuilt 0fd31e2

* Mon Dec 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-62
- podman-2:3.0.0-0.57.dev.gitbdbf47f
- autobuilt bdbf47f

* Sat Dec 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-61
- podman-2:3.0.0-0.56.dev.gita226e6e
- autobuilt a226e6e

* Sat Dec 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-60
- podman-2:3.0.0-0.55.dev.git36bec38
- autobuilt 36bec38

* Sat Dec 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-59
- podman-2:3.0.0-0.54.dev.git1d50245
- autobuilt 1d50245

* Sat Dec 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-58
- podman-2:3.0.0-0.53.dev.gitfbcd445
- autobuilt fbcd445

* Fri Dec 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-57
- podman-2:3.0.0-0.52.dev.gitb0a287c
- autobuilt b0a287c

* Fri Dec 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-56
- podman-2:3.0.0-0.51.dev.git99ac30a
- autobuilt 99ac30a

* Fri Dec 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-55
- podman-2:3.0.0-0.50.dev.gitdd95478
- autobuilt dd95478

* Thu Dec 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-54
- podman-2:3.0.0-0.49.dev.git6823a5d
- autobuilt 6823a5d

* Thu Dec 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-53
- podman-2:3.0.0-0.48.dev.git2bb1490
- autobuilt 2bb1490

* Thu Dec 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-52
- podman-2:3.0.0-0.47.dev.gitdeb0042
- autobuilt deb0042

* Thu Dec 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-51
- podman-2:3.0.0-0.46.dev.giteaa19a1
- autobuilt eaa19a1

* Wed Dec 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-50
- podman-2:3.0.0-0.45.dev.git9216be2
- autobuilt 9216be2

* Wed Dec 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-49
- podman-2:3.0.0-0.44.dev.giteb053df
- autobuilt eb053df

* Wed Dec 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-48
- podman-2:3.0.0-0.43.dev.git43567c6
- autobuilt 43567c6

* Wed Dec 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-47
- podman-2:3.0.0-0.42.dev.git9abbe07
- autobuilt 9abbe07

* Wed Dec 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-46
- podman-2:3.0.0-0.41.dev.git3cd143f
- autobuilt 3cd143f

* Wed Dec 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-45
- podman-2:3.0.0-0.40.dev.gitb875c5c
- autobuilt b875c5c

* Wed Dec 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-44
- podman-2:3.0.0-0.39.dev.git2472600
- autobuilt 2472600

* Wed Dec 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-43
- podman-2:3.0.0-0.38.dev.gitdd295f2
- autobuilt dd295f2

* Tue Dec 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-42
- podman-2:3.0.0-0.37.dev.git7caef9c
- autobuilt 7caef9c

* Tue Dec 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-41
- podman-2:3.0.0-0.36.dev.git47d2a4b
- autobuilt 47d2a4b

* Tue Dec 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-40
- podman-2:3.0.0-0.35.dev.git0cccba8
- autobuilt 0cccba8

* Tue Dec 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-39
- podman-2:3.0.0-0.34.dev.git9b3a81a
- autobuilt 9b3a81a

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-38
- podman-2:3.0.0-0.33.dev.gite2f9120
- autobuilt e2f9120

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-37
- podman-2:3.0.0-0.32.dev.gitbfbeece
- autobuilt bfbeece

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-36
- podman-2:3.0.0-0.31.dev.gita5ca039
- autobuilt a5ca039

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-35
- podman-2:3.0.0-0.30.dev.git3569e24
- autobuilt 3569e24

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-34
- podman-2:3.0.0-0.29.dev.gite6f80fa
- autobuilt e6f80fa

* Mon Dec 07 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.0.0-33
- fcf-protection cflag NOT for centos <= 7

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-32
- podman-2:3.0.0-0.28.dev.gite117ad3
- autobuilt e117ad3

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-31
- podman-2:3.0.0-0.27.dev.git0c96731
- autobuilt 0c96731

* Sat Dec 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-30
- podman-2:3.0.0-0.26.dev.git0c2a43b
- autobuilt 0c2a43b

* Fri Dec 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-29
- podman-2:3.0.0-0.25.dev.git8e83799
- autobuilt 8e83799

* Fri Dec 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-28
- podman-2:3.0.0-0.24.dev.gitb6536d2
- autobuilt b6536d2

* Fri Dec 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-27
- podman-2:3.0.0-0.23.dev.gitc55b831
- autobuilt c55b831

* Fri Dec 04 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.0.0-26
- podman-2:3.0.0-0.22.dev.gitf01630a
- make both checksec and koji happy

* Fri Dec 04 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.0.0-25
- adjust CGO_CFLAGS to make both koji and checksec happy

* Fri Dec 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-24
- podman-2:3.0.0-0.21.dev.gitf01630a
- autobuilt f01630a

* Fri Dec 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-23
- podman-2:3.0.0-0.20.dev.gitec0411a
- autobuilt ec0411a

* Thu Dec 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.0.0-22
- correct changelog tag

* Thu Dec 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org>
- podman-2:3.0.0-0.17.dev.git85b412d
- Harden binaries

* Thu Dec 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.0.0-20
- Harden binaries

* Thu Dec 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-19
- podman-2:3.0.0-0.18.dev.git70284b1
- autobuilt 70284b1

* Thu Dec 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-18
- podman-2:3.0.0-0.17.dev.gitc675d8a
- autobuilt c675d8a

* Thu Dec 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-17
- podman-2:3.0.0-0.16.dev.git85b412d
- autobuilt 85b412d

* Thu Dec 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-16
- podman-2:3.0.0-0.15.dev.git9180872
- autobuilt 9180872

* Thu Dec 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-15
- podman-2:3.0.0-0.14.dev.git5cf7aa6
- autobuilt 5cf7aa6

* Wed Dec 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-14
- podman-2:3.0.0-0.13.dev.git7984842
- autobuilt 7984842

* Wed Dec 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-13
- podman-2:3.0.0-0.12.dev.gitd456765
- autobuilt d456765

* Wed Dec 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-12
- podman-2:3.0.0-0.11.dev.gite82ec90
- autobuilt e82ec90

* Wed Dec 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-11
- podman-2:3.0.0-0.10.dev.git7210b86
- autobuilt 7210b86

* Wed Dec 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-10
- podman-2:3.0.0-0.9.dev.gitd28874b
- autobuilt d28874b

* Wed Dec 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-9
- podman-2:3.0.0-0.8.dev.git9c5fe95
- autobuilt 9c5fe95

* Tue Dec 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-8
- podman-2:3.0.0-0.7.dev.gitb2cd6e0
- autobuilt b2cd6e0

* Tue Dec 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-7
- podman-2:3.0.0-0.6.dev.gitc71ad9a
- autobuilt c71ad9a

* Tue Dec 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-6
- podman-2:3.0.0-0.5.dev.gitce45b71
- autobuilt ce45b71

* Tue Dec 01 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.0.0-5
- import dnsname source tarball

* Tue Dec 01 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:3.0.0-4
- podman-2:3.0.0-0.4.dev.git429d949
- use podman-plugins / dnsname upstream v1.1.1

* Tue Dec 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-3
- podman-2:3.0.0-0.3.dev.git429d949
- autobuilt 429d949

* Tue Dec 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-2
- podman-2:3.0.0-0.2.dev.git2438390
- autobuilt 2438390

* Tue Dec 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:3.0.0-1
- podman-2:3.0.0-0.1.dev.gitca612a3
- bump to 3.0.0
- autobuilt ca612a3

* Mon Nov 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-78
- podman-2:2.2.0-0.74.dev.gitc342583
- autobuilt c342583

* Mon Nov 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-77
- podman-2:2.2.0-0.73.dev.gitf6fb297
- autobuilt f6fb297

* Mon Nov 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-76
- podman-2:2.2.0-0.72.dev.git7ad1c9c
- autobuilt 7ad1c9c

* Mon Nov 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-75
- podman-2:2.2.0-0.71.dev.gitfc85ec9
- autobuilt fc85ec9

* Sat Nov 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-74
- podman-2:2.2.0-0.70.dev.git8b2c0a4
- autobuilt 8b2c0a4

* Sat Nov 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-73
- podman-2:2.2.0-0.69.dev.gitf0d48aa
- autobuilt f0d48aa

* Sat Nov 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-72
- podman-2:2.2.0-0.68.dev.git3110308
- autobuilt 3110308

* Thu Nov 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-71
- podman-2:2.2.0-0.67.dev.gitad24392
- autobuilt ad24392

* Wed Nov 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-70
- podman-2:2.2.0-0.66.dev.git397e9a9
- autobuilt 397e9a9

* Tue Nov 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-69
- podman-2:2.2.0-0.65.dev.gitd408395
- autobuilt d408395

* Tue Nov 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-68
- podman-2:2.2.0-0.64.dev.git850bdd2
- autobuilt 850bdd2

* Tue Nov 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-67
- podman-2:2.2.0-0.63.dev.git4ebd9d9
- autobuilt 4ebd9d9

* Mon Nov 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-66
- podman-2:2.2.0-0.62.dev.git4fe7c3f
- autobuilt 4fe7c3f

* Mon Nov 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-65
- podman-2:2.2.0-0.61.dev.gitcd6c4cb
- autobuilt cd6c4cb

* Mon Nov 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-64
- podman-2:2.2.0-0.60.dev.git5d55285
- autobuilt 5d55285

* Mon Nov 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-63
- podman-2:2.2.0-0.59.dev.gitdd34341
- autobuilt dd34341

* Sat Nov 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-62
- podman-2:2.2.0-0.58.dev.git5292d5a
- autobuilt 5292d5a

* Fri Nov 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-61
- podman-2:2.2.0-0.57.dev.git042d488
- autobuilt 042d488

* Thu Nov 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-60
- podman-2:2.2.0-0.56.dev.git70f91fb
- autobuilt 70f91fb

* Wed Nov 18 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-59
- podman-2:2.2.0-0.55.dev.git286d356
- bump dnsname to v1.1.0, commit a9c2a10

* Wed Nov 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-58
- podman-2:2.2.0-0.54.dev.git286d356
- autobuilt 286d356

* Wed Nov 18 2020 Ed Santiago <santiago@redhat.com> - 2:2.2.0-57
- Slight correction to the path of the removed .md file

* Tue Nov 17 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-56
- podman-2:2.2.0-0.52.dev.git42ec4cf
- containers-mounts.conf.5 in containers-common

* Tue Nov 17 2020 Ed Santiago <santiago@redhat.com> - 2:2.2.0-55
- completion files: package -remote files in -remote

* Tue Nov 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-54
- podman-2:2.2.0-0.50.dev.git42ec4cf
- autobuilt 42ec4cf

* Mon Nov 16 2020 Ed Santiago <santiago@redhat.com> - 2:2.2.0-53
- Package new zsh and fish completion files

* Sun Nov 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-52
- podman-2:2.2.0-0.48.dev.git3920756
- autobuilt 3920756

* Sat Nov 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-51
- podman-2:2.2.0-0.47.dev.git4eb9c28
- autobuilt 4eb9c28

* Fri Nov 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-50
- podman-2:2.2.0-0.46.dev.git0b1a60e
- autobuilt 0b1a60e

* Thu Nov 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-49
- podman-2:2.2.0-0.45.dev.git6c2503c
- autobuilt 6c2503c

* Wed Nov 11 2020 Ed Santiago <santiago@redhat.com> - 2:2.2.0-48
- Distribute newly-added tmpfiles.d/podman

* Wed Nov 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-47
- podman-2:2.2.0-0.43.dev.gite443c01
- autobuilt e443c01

* Tue Nov 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-46
- podman-2:2.2.0-0.42.dev.gitda01191
- autobuilt da01191

* Sat Nov 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-45
- podman-2:2.2.0-0.41.dev.gite2b82e6
- autobuilt e2b82e6

* Fri Nov 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-44
- podman-2:2.2.0-0.40.dev.git07293bc
- autobuilt 07293bc

* Fri Oct 23 2020 Ashley Cui <acui@redhat.com> - 2:2.2.0-43
- Test build

* Fri Oct 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-42
- correct changelog order

* Wed Oct 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-41
- podman-2:2.2.0-0.38.dev.git287edd4
- autobuilt 287edd4

* Tue Oct 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-40
- podman-2:2.2.0-0.37.dev.git35b4cb1
- autobuilt 35b4cb1

* Mon Oct 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-39
- podman-2:2.2.0-0.36.dev.git7ffcab0
- autobuilt 7ffcab0

* Mon Oct 19 2020 Ed Santiago <santiago@redhat.com> - 2:2.2.0-38
- Podman tests now require buildah

* Sun Oct 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-37
- podman-2:2.2.0-0.35.dev.git6ec96dc
- autobuilt 6ec96dc

* Sat Oct 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-36
- podman-2:2.2.0-0.34.dev.git39f1bea
- autobuilt 39f1bea

* Fri Oct 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-35
- podman-2:2.2.0-0.33.dev.git9f98b34
- autobuilt 9f98b34

* Thu Oct 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-34
- podman-2:2.2.0-0.32.dev.gita82d60d
- autobuilt a82d60d

* Wed Oct 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-33
- podman-2:2.2.0-0.31.dev.gitd30b4b7
- autobuilt d30b4b7

* Tue Oct 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-32
- podman-2:2.2.0-0.30.dev.git7ad631b
- autobuilt 7ad631b

* Mon Oct 12 2020 Jindrich Novy <jnovy@redhat.com> - 2:2.2.0-31
- podman-2.2.0-0.29.dev.git212011f.fc34
- use %%%%rhel instead of %%%%eln, thanks to Adam Samalik for noticing

* Mon Oct 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-30
- podman-2:2.2.0-0.28.dev.git212011f
- autobuilt 212011f

* Sat Oct 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-29
- podman-2:2.2.0-0.27.dev.git7876dd5
- autobuilt 7876dd5

* Fri Oct 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-28
- podman-2:2.2.0-0.26.dev.git71d675a
- autobuilt 71d675a

* Thu Oct 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-27
- podman-2:2.2.0-0.25.dev.git59b5f0a
- autobuilt 59b5f0a

* Wed Oct 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-26
- podman-2:2.2.0-0.24.dev.gita7500e5
- autobuilt a7500e5

* Tue Oct 06 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-25
- podman-2:2.2.0-0.23.dev.gitdefb754
- btrfs deps for fedora only

* Tue Oct 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-24
- podman-2:2.2.0-0.22.dev.gitdefb754
- autobuilt defb754

* Mon Oct 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-23
- podman-2:2.2.0-0.21.dev.gitcaace52
- autobuilt caace52

* Sat Oct 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-22
- rebuild

* Sat Oct 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-21
- podman-2:2.2.0-0.19.dev.git7c12967
- autobuilt 7c12967

* Fri Oct 02 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-20
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
