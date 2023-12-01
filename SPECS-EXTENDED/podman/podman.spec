%global with_check 0
%global with_debug 1

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%global provider github
%global provider_tld com
%global project containers
%global repo %{name}
# https://github.com/containers/%%{name}
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global git0 https://%{import_path}

# dnsname
%global repo_plugins dnsname
# https://github.com/containers/dnsname
%global import_path_plugins %{provider}.%{provider_tld}/%{project}/%{repo_plugins}
%global git_plugins https://%{import_path_plugins}
%global commit_plugins 18822f9a4fb35d1349eb256f4cd2bfd372474d84
%global shortcommit_plugins %(c=%{commit_plugins}; echo ${c:0:7})

# gvproxy
%global repo_gvproxy gvisor-tap-vsock
# https://github.com/containers/gvisor-tap-vsock
%global import_path_gvproxy %%{provider}.%{provider_tld}/%{project}/%{repo_gvproxy}
%global git_gvproxy https://%{import_path_gvproxy}
%global commit_gvproxy aab0ac9367fc5142f5857c36ac2352bcb3c60ab7
%global shortcommit_gvproxy %(c=%{commit_gvproxy}; echo ${c:0:7})

%global built_tag v4.1.1

Name:           podman
Version:        4.1.1
Release:        19%{?dist}
License:        ASL 2.0 and BSD and ISC and MIT and MPLv2.0
Summary:        Manage Pods, Containers and Container Images
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://%{name}.io/
Source0:        %{git0}/archive/%{built_tag}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{git_plugins}/archive/%{commit_plugins}/%{repo_plugins}-%{commit_plugins}.tar.gz#/%{repo_plugins}-%{shortcommit_plugins}.tar.gz
Source2:        %{git_gvproxy}/archive/%{commit_gvproxy}/%{repo_gvproxy}-%{commit_gvproxy}.tar.gz#/%{repo_gvproxy}-%{shortcommit_gvproxy}.tar.gz
Patch0:         CVE-2022-2989.patch
Provides:       %{name}-manpages = %{version}-%{release}
BuildRequires:  go-md2man
BuildRequires:  golang
BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  glibc-static >= 2.38-1%{?dist}
BuildRequires:  git
BuildRequires:  go-rpm-macros
BuildRequires:  gpgme-devel
BuildRequires:  libassuan-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libselinux-devel
BuildRequires:  shadow-utils
BuildRequires:  pkgconfig
BuildRequires:  make
BuildRequires:  ostree-devel
BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  libcontainers-common
Requires:       catatonit
Requires:       iptables
Requires:       nftables
Requires:       conmon >= 2.0.30
Requires:       libcontainers-common
Requires:       netavark >= 1.0.3
Requires:       shadow-utils-subid
Requires:       moby-runc
Requires:       slirp4netns
Requires:       containernetworking-plugins >= 0.9.1
Suggests:       qemu-user-static

# vendored libraries
# awk '{print "Provides: bundled(golang("$1")) = "$2}' go.mod | sort | uniq | sed -e 's/-/_/g' -e '/bundled(golang())/d' -e '/bundled(golang(go\|module\|replace\|require))/d'
Provides:       bundled(golang(github.com/BurntSushi/toml)) = v1.1.0
Provides:       bundled(golang(github.com/blang/semver)) = v3.5.1+incompatible
Provides:       bundled(golang(github.com/buger/goterm)) = v1.0.4
Provides:       bundled(golang(github.com/checkpoint_restore/checkpointctl)) = v0.0.0_20220321135231_33f4a66335f0
Provides:       bundled(golang(github.com/checkpoint_restore/go_criu/v5)) = v5.3.0
Provides:       bundled(golang(github.com/container_orchestrated_devices/container_device_interface)) = v0.4.0
Provides:       bundled(golang(github.com/containernetworking/cni)) = v1.1.0
Provides:       bundled(golang(github.com/containernetworking/plugins)) = v1.1.1
Provides:       bundled(golang(github.com/containers/buildah)) = v1.26.1
Provides:       bundled(golang(github.com/containers/common)) = v0.48.0
Provides:       bundled(golang(github.com/containers/conmon)) = v2.0.20+incompatible
Provides:       bundled(golang(github.com/containers/image/v5)) = v5.21.1
Provides:       bundled(golang(github.com/containers/ocicrypt)) = v1.1.4
Provides:       bundled(golang(github.com/containers/psgo)) = v1.7.2
Provides:       bundled(golang(github.com/containers/storage)) = v1.40.2
Provides:       bundled(golang(github.com/coreos/go_systemd/v22)) = v22.3.2
Provides:       bundled(golang(github.com/coreos/stream_metadata_go)) = v0.0.0_20210225230131_70edb9eb47b3
Provides:       bundled(golang(github.com/cyphar/filepath_securejoin)) = v0.2.3
Provides:       bundled(golang(github.com/davecgh/go_spew)) = v1.1.1
Provides:       bundled(golang(github.com/digitalocean/go_qemu)) = v0.0.0_20210326154740_ac9e0b687001
Provides:       bundled(golang(github.com/docker/distribution)) = v2.8.1+incompatible
Provides:       bundled(golang(github.com/docker/docker)) = v20.10.14+incompatible
Provides:       bundled(golang(github.com/docker/go_connections)) = v0.4.1_0.20210727194412_58542c764a11
Provides:       bundled(golang(github.com/docker/go_plugins_helpers)) = v0.0.0_20211224144127_6eecb7beb651
Provides:       bundled(golang(github.com/docker/go_units)) = v0.4.0
Provides:       bundled(golang(github.com/dtylman/scp)) = v0.0.0_20181017070807_f3000a34aef4
Provides:       bundled(golang(github.com/fsnotify/fsnotify)) = v1.5.4
Provides:       bundled(golang(github.com/ghodss/yaml)) = v1.0.0
Provides:       bundled(golang(github.com/godbus/dbus/v5)) = v5.1.0
Provides:       bundled(golang(github.com/google/gofuzz)) = v1.2.0
Provides:       bundled(golang(github.com/google/shlex)) = v0.0.0_20191202100458_e7afc7fbc510
Provides:       bundled(golang(github.com/google/uuid)) = v1.3.0
Provides:       bundled(golang(github.com/gorilla/handlers)) = v1.5.1
Provides:       bundled(golang(github.com/gorilla/mux)) = v1.8.0
Provides:       bundled(golang(github.com/gorilla/schema)) = v1.2.0
Provides:       bundled(golang(github.com/hashicorp/go_multierror)) = v1.1.1
Provides:       bundled(golang(github.com/json_iterator/go)) = v1.1.12
Provides:       bundled(golang(github.com/mattn/go_isatty)) = v0.0.14
Provides:       bundled(golang(github.com/moby/term)) = v0.0.0_20210619224110_3f7ff695adc6
Provides:       bundled(golang(github.com/nxadm/tail)) = v1.4.8
Provides:       bundled(golang(github.com/onsi/ginkgo)) = v1.16.5
Provides:       bundled(golang(github.com/onsi/gomega)) = v1.19.0
Provides:       bundled(golang(github.com/opencontainers/go_digest)) = v1.0.0
Provides:       bundled(golang(github.com/opencontainers/image_spec)) = v1.0.3_0.20220114050600_8b9d41f48198
Provides:       bundled(golang(github.com/opencontainers/runc)) = v1.1.1
Provides:       bundled(golang(github.com/opencontainers/runtime_spec)) = v1.0.3_0.20211214071223_8958f93039ab
Provides:       bundled(golang(github.com/opencontainers/runtime_tools)) = v0.9.1_0.20220110225228_7e2d60f1e41f
Provides:       bundled(golang(github.com/opencontainers/selinux)) = v1.10.1
Provides:       bundled(golang(github.com/pkg/errors)) = v0.9.1
Provides:       bundled(golang(github.com/pmezard/go_difflib)) = v1.0.0
Provides:       bundled(golang(github.com/rootless_containers/rootlesskit)) = v1.0.1
Provides:       bundled(golang(github.com/sirupsen/logrus)) = v1.8.1
Provides:       bundled(golang(github.com/spf13/cobra)) = v1.4.0
Provides:       bundled(golang(github.com/spf13/pflag)) = v1.0.5
Provides:       bundled(golang(github.com/stretchr/testify)) = v1.7.1
Provides:       bundled(golang(github.com/syndtr/gocapability)) = v0.0.0_20200815063812_42c35b437635
Provides:       bundled(golang(github.com/uber/jaeger_client_go)) = v2.30.0+incompatible
Provides:       bundled(golang(github.com/ulikunitz/xz)) = v0.5.10
Provides:       bundled(golang(github.com/vbauerster/mpb/v7)) = v7.4.1
Provides:       bundled(golang(github.com/vishvananda/netlink)) = v1.1.1_0.20220115184804_dd687eb2f2d4

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

%{summary}
%{repo} Simple management tool for pods, containers and images

%package       docker
Summary:       Emulate Docker CLI using %{name}
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}
Conflicts:     docker
Conflicts:     docker-latest
Conflicts:     docker-ce
Conflicts:     docker-ee
Conflicts:     moby-engine

%description docker
This package installs a script named docker that emulates the Docker CLI by
executes %{name} commands, it also creates links between all Docker CLI man
pages and %{name}.

%package      tests
Summary:      Tests for %{name}

Requires:     %{name} = %{version}-%{release}
Requires:     bats
Requires:     jq
Requires:     skopeo
Requires:     nmap-ncat
Requires:     httpd-tools
Requires:     openssl
Requires:     socat
Requires:     buildah
Requires:     gnupg

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

%package      plugins
Summary:      Plugins for %{name}
Requires:     dnsmasq
Recommends:   %{name}-gvproxy = %{version}-%{release}

%description plugins
This plugin sets up the use of dnsmasq on a given CNI network so
that Pods can resolve each other by name.  When configured,
the pod and its IP address are added to a network specific hosts file
that dnsmasq will read in.  Similarly, when a pod
is removed from the network, it will remove the entry from the hosts
file.  Each CNI network will have its own dnsmasq instance.

%package gvproxy
Summary: Go replacement for libslirp and VPNKit

%description gvproxy
A replacement for libslirp and VPNKit, written in pure Go.
It is based on the network stack of gVisor. Compared to libslirp,
gvisor-tap-vsock brings a configurable DNS server and
dynamic port forwarding.

%prep
%autosetup -Sgit -p1
sed -i 's;@@PODMAN@@\;$(BINDIR);@@PODMAN@@\;%{_bindir};' Makefile

# untar dnsname
tar zxf %{SOURCE1}

# untar %%{name}-gvproxy
tar zxf %{SOURCE2}

%build
%if "%{_vendor}" != "debbuild"
%set_build_flags
export CGO_CFLAGS=$CFLAGS
# These extra flags present in $CFLAGS have been skipped for now as they break the build
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-flto=auto//g')
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-Wp,D_GLIBCXX_ASSERTIONS//g')
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//g')

%ifarch x86_64
export CGO_CFLAGS+=" -m64 -mtune=generic -fcf-protection=full"
%endif
%endif

export GO111MODULE=off
export GOPATH=$(pwd)/_build:$(pwd)

mkdir _build
cd _build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../../ src/%{import_path}
cd ..
ln -s vendor src

# build date. FIXME: Makefile uses '/v2/libpod', that doesn't work here?
LDFLAGS="-X %{import_path}/libpod/define.buildInfo=$(date +%s)"

# build rootlessport first
%gobuild -o bin/rootlessport %{import_path}/cmd/rootlessport

# build %%{name}
export BUILDTAGS="seccomp exclude_graphdriver_devicemapper $(hack/btrfs_installed_tag.sh) $(hack/btrfs_tag.sh) $(hack/libdm_tag.sh) $(hack/selinux_tag.sh) $(hack/systemd_tag.sh) $(hack/libsubid_tag.sh)"

%gobuild -o bin/%{name} %{import_path}/cmd/%{name}

# build %%{name}-remote
export BUILDTAGS="seccomp exclude_graphdriver_devicemapper exclude_graphdriver_btrfs btrfs_noversion $(hack/selinux_tag.sh) $(hack/systemd_tag.sh) $(hack/libsubid_tag.sh) remote"
%gobuild -o bin/%{name}-remote %{import_path}/cmd/%{name}

cd %{repo_plugins}-%{commit_plugins}
mkdir _build
cd _build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../../ src/%{import_path_plugins}
cd ..
ln -s vendor src
export GOPATH=$(pwd)/_build:$(pwd)
%gobuild -o bin/dnsname %{import_path_plugins}/plugins/meta/dnsname
cd ..

cd %{repo_gvproxy}-%{commit_gvproxy}
mkdir _build
cd _build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../../ src/%{import_path_gvproxy}
cd ..
ln -s vendor src
export GOPATH=$(pwd)/_build:$(pwd)
%gobuild -o bin/gvproxy %{import_path_gvproxy}/cmd/gvproxy
cd ..

%{__make} docs docker-docs

%install
install -dp %{buildroot}%{_unitdir}
PODMAN_VERSION=%{version} %{__make} PREFIX=%{buildroot}%{_prefix} ETCDIR=%{buildroot}%{_sysconfdir} \
       install.bin \
       install.man \
       install.systemd \
       install.completions \
       install.docker \
       install.docker-docs \
       install.remote \
       install.modules-load

mv pkg/hooks/README.md pkg/hooks/README-hooks.md

# install dnsname plugin
cd %{repo_plugins}-%{commit_plugins}
%{__make} PREFIX=%{_prefix} DESTDIR=%{buildroot} install
cd ..

# install gvproxy
cd %{repo_gvproxy}-%{commit_gvproxy}
install -dp %{buildroot}%{_libexecdir}/%{name}
install -p -m0755 bin/gvproxy %{buildroot}%{_libexecdir}/%{name}
cd ..

# do not include docker and podman-remote man pages in main package
for file in `find %{buildroot}%{_mandir}/man[15] -type f | sed "s,%{buildroot},," | grep -v -e remote -e docker`; do
    echo "$file*" >> podman.file-list
done

rm -f %{buildroot}%{_mandir}/man5/docker*.5

install -d -p %{buildroot}/%{_datadir}/%{name}/test/system
cp -pav test/system %{buildroot}/%{_datadir}/%{name}/test/

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files -f %{name}.file-list
%license LICENSE
%doc README.md CONTRIBUTING.md pkg/hooks/README-hooks.md install.md transfer.md
%{_bindir}/%{name}
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/rootlessport
%{_datadir}/bash-completion/completions/%{name}
# By "owning" the site-functions dir, we don't need to Require zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_unitdir}/%{name}*
%{_userunitdir}/%{name}*
%{_tmpfilesdir}/%{name}.conf
%{_modulesloaddir}/%{name}-iptables.conf

%files docker
%{_bindir}/docker
%{_mandir}/man1/docker*.1*
%{_usr}/lib/tmpfiles.d/%{name}-docker.conf

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
%license LICENSE
%{_datadir}/%{name}/test

%files plugins
%license %{repo_plugins}-%{commit_plugins}/LICENSE
%doc %{repo_plugins}-%{commit_plugins}/{README.md,README_PODMAN.md}
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/dnsname

%files gvproxy
%license %{repo_gvproxy}-%{commit_gvproxy}/LICENSE
%doc %{repo_gvproxy}-%{commit_gvproxy}/README.md
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/gvproxy


# rhcontainerbot account currently managed by lsm5
%changelog
* Tue Nov 07 2023 Andrew Phelps <anphel@microsoft.com> - 4.1.1-19
- Bump release to rebuild against glibc 2.38-1

* Wed Oct 18 2023 Minghe Ren <mingheren@microsoft.com> - 4.1.1-18
- Bump release to rebuild against glibc 2.35-6

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.1.1-17
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 4.1.1-16
- Bump release to rebuild with updated version of Go.

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 4.1.1-15
- Bump release to rebuild against glibc 2.35-5

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.1.1-14
- Bump release to rebuild with go 1.19.12

* Wed Jul 14 2023 Andrew Phelps <anphel@microsoft.com> - 4.1.1-13
- Bump release to rebuild against glibc 2.35-4

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.1.1-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.1.1-11
- Bump release to rebuild with go 1.19.10

* Thu Apr 20 2023 Amrita Kohli <amritakohli@microsoft.com> - 4.1.1-10
- Patch CVE-2022-2989

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.1.1-9
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.1.1-8
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.1.1-7
- Bump release to rebuild with go 1.19.6

* Fri Feb 17 2023 Muhammad Falak <mwani@microsoft.com> - 4.1.1-6
- Bump version of gvproxy to enable build with go1.19

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.1.1-5
- Bump release to rebuild with go 1.19.4

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.1.1-4
- Bump release to rebuild with go 1.18.8

* Tue Sep 13 2022 Andy Caldwell <andycaldwell@microsoft.com> - 4.1.1-3
- Rebuilt for glibc-static 2.35-3

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.1.1-2
- Bump release to rebuild against Go 1.18.5

* Fri Jul 22 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.1.1-1
- Upgrade to version 4.1.1
- Updated SPEC file with required changes for latest version compatibility.

* Tue Mar 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.1-5
- Fixing installation steps for non-test builds.
- License verified.

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.2.1-4
- Remove epoch

* Tue Jun 01 2021 Olivia Crain <oliviacrain@microsoft.com> - 2:2.2.1-3
- Rename runc dependency to moby-runc

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:2.2.1-2
- Initial CBL-Mariner import from Fedora 29 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Tue Dec  8 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.1-1
- autobuilt v2.2.1

* Mon Dec  7 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-4
- bump release tag to make centos OBS happy

* Mon Dec  7 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-3
- harden cgo based golang binaries
- Reported-by: Wade Mealing <wmealing@gmail.com>

* Tue Dec  1 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-2
- use podman-plugins / dnsname upstream v1.1.1

* Tue Dec  1 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-1
- autobuilt v2.2.0

* Tue Nov 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-0.6.rc2
- autobuilt v2.2.0-rc2

* Mon Nov 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-0.5.rc1
- handle centos7

* Fri Nov 20 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-0.4.rc1
- use latest containers-common 1.2.0-9

* Wed Nov 18 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-0.3.rc1
- podman-plugins should require podman otherwise it can cause funny upgrade
scenarios, where if "podman" upgrade fails, "podman-plugins" could still
succeed

* Wed Nov 18 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-0.2.rc1
- require containers-common 1:1.2.0-8 for shortnames

* Wed Nov 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.2.0-0.1.rc1
- autobuilt v2.2.0-rc1

* Wed Nov 18 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-13
- bump dnsname to v1.1.0, commit a9c2a10

* Sun Oct  4 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-10
- fix permission denied issue when using --net=host

* Fri Oct  2 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-9
- fix capset issue on podman run (upstream PR#7898)
- Requires containers-common >= %%epoch:1.2.0-2

* Fri Oct  2 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-8
- Requires: (container-selinux if selinux-policy)

* Wed Sep 30 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-7
- fix crun gating test issue
- bump release tag to preserve upgrade path

* Wed Sep 30 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-6
- fedora Requires: crun-0.15-4

* Wed Sep 30 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-5
- fedora requires crun >= 0.15-3

* Sun Sep 27 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-4
- correct bad date in changelog

* Sun Sep 27 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-3
- adjust deps for centos7

* Wed Sep 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.1-1
- bump to v2.1.1

* Wed Sep 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.0-2
- podman-plugins is a weak dep for podman

* Tue Sep 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.1.0-1
- autobuilt v2.1.0
- Resolves: #1874268, #1881345 - CVE-2020-14370

* Fri Sep 18 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.0-0.5.rc2
- fix release tag

* Thu Sep 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.1.0-0.4.rc1
- autobuilt v2.1.0-rc2

* Wed Sep 16 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.0-0.3.rc1
- plugins requires dnsmasq

* Mon Sep 14 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.1.0-0.2.rc1
- use correct release tag

* Mon Sep 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.1.0-0.1.rc1
- autobuilt v2.1.0-rc1

* Tue Sep 01 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.6-1
- bump to v2.0.6

* Fri Aug 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.0.6-0.2.rc1
- autobuilt v2.0.6-rc1

* Tue Aug 25 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.5-2
- buildinfo in LDFLAGS

* Mon Aug 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.0.5-1
- autobuilt v2.0.5

* Fri Jul 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.0.4-1
- autobuilt v2.0.4

* Thu Jul 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.0.3-1
- autobuilt v2.0.3

* Sun Jul 12 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.2-2
- re-enable varlink for centos8

* Tue Jul 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.0.2-1
- autobuilt v2.0.2

* Fri Jun 26 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.1-1
- bump to v2.0.1

* Sat Jun 20 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.0-2
- depend on conmon-2:2.0.18-1

* Fri Jun 19 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.0-1
- bump to v2.0.0

* Wed Jun 17 2020 Brent Baude <bbaude@redhat.com> - 2:2.0.0-0.3.rc7
- built v2.0.0-rc7

* Mon Jun 15 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.0-0.2.rc6
- built v2.0.0-rc6

* Mon Jun 15 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.0-0.1.rc5
- correct release tag format

* Wed Jun 10 2020 Brent Baude <bbaude@redhat.com> - 2:2.0.0-rc5
- rc5

* Mon Jun 8 2020 Dan Walsh <dwalsh@fedoraproject.org> - 2:2.0.0-rc4.1
- Remove /etc/modules-load.d/podman.conf

* Thu Jun 04 2020 Brent Baude <bbaude@redhat.com> - 2:2.0.0-rc4
- rc4

* Mon May 25 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.9.3-1
- bump to v1.9.3
- require conmon >= 2:2.0.16-3

* Fri May 15 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.9.2-2
- use correct epoch for conmon

* Wed May 13 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.9.2-1
- bump to v1.9.2
- update min deps on conmon and cni plugins

* Wed Apr 29 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.9.1-1
- new version

* Wed Apr 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.9.0-1
- autobuilt v1.9.0

* Tue Apr 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.9.0-0.5.rc1
- autobuilt v1.9.0-rc2

* Mon Apr 13 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.9.0-0.4.rc1
- rewrite container-selinux conditionals more cleanly

* Mon Apr 13 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.9.0-0.3.rc1
- correct varlink go generate
- container-selinux is a recommends for fedora and centos8 but requires for centos7

* Mon Apr 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.8.2-0.2.rc1
- autobuilt v1.9.0-rc1

* Mon Mar 30 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.8.2-3
- Resolves: gh#5316

* Fri Mar 20 2020 Dan Walsh <dwalsh@fedoraproject.org> - 2:1.8.2-2
- Install the APIV2 services

* Thu Mar 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.8.2-1
- autobuilt v1.8.2

* Wed Mar 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.8.1-0.2.rc1
- autobuilt v1.8.2-rc1

* Wed Mar 11 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.8.1-2
- bump cause previous release went bad somewhere at fedora-infra

* Wed Mar 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.8.1-1
- autobuilt v1.8.1

* Tue Mar 10 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.8.1-0.7.rc4
- correct release tag

* Tue Mar 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.8.1-0.6.rc3
- autobuilt v1.8.1-rc4

* Sat Mar 07 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.8.1-0.5.rc3
- bump to v1.8.1-rc3

* Sun Mar 01 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.8.1-0.4.rc2
- correct changelog

* Sun Feb 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.8.1-0.3.rc1
- bump to v1.8.1-rc1

* Sun Feb 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.8.0-5
- Resolves: #1806147 - correct buildtags for podman-remote

* Tue Feb 18 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.8.0-4
- bump to v1.8.0
- autobuilt 2ced909
- cosmetic changes for autobuilds

* Tue Feb 18 2020 Dan Walsh <dwalsh5@fedoraproject.org> - 2:1.8.0-3.git5092c07
- Bump release to make sure new version installs on F32 and remove -dev branch

* Thu Feb 06 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.8.0-0.4.dev.git5092c07
- bump crun dependency

* Wed Feb 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.8.0-0.3.dev.git5092c07
- autobuilt 5092c07

* Tue Feb 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.8.0-0.2.dev.gitc4f6d56
- autobuilt c4f6d56

* Sun Feb 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.8.0-0.1.dev.git4699d5e
- bump to 1.8.0
- autobuilt 4699d5e

* Fri Jan 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.66.dev.git36af283
- autobuilt 36af283

* Thu Jan 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.65.dev.giteb28365
- autobuilt eb28365

* Wed Jan 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.64.dev.gitb2ae45c
- autobuilt b2ae45c

* Tue Jan 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.63.dev.git326cdf9
- autobuilt 326cdf9

* Mon Jan 27 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.62.dev.gitc28af15
- autobuilt c28af15

* Sat Jan 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.61.dev.git975854a
- autobuilt 975854a

* Thu Jan 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.60.dev.git5bad873
- autobuilt 5bad873

* Thu Jan 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.59.dev.git8beeb06
- autobuilt 8beeb06

* Thu Jan 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.58.dev.git6518421
- autobuilt 6518421

* Thu Jan 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.57.dev.gite6cf0ec
- autobuilt e6cf0ec

* Wed Jan 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.56.dev.gitac3a6b8
- autobuilt ac3a6b8

* Wed Jan 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.55.dev.git8b377a7
- autobuilt 8b377a7

* Wed Jan 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.54.dev.gitc42383f
- autobuilt c42383f

* Wed Jan 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.53.dev.gitc40664d
- autobuilt c40664d

* Wed Jan 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.52.dev.git9f146b1
- autobuilt 9f146b1

* Wed Jan 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.51.dev.git7e1afe0
- autobuilt 7e1afe0

* Wed Jan 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.50.dev.git55abb6d
- autobuilt 55abb6d

* Wed Jan 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.49.dev.gitd52132b
- autobuilt d52132b

* Wed Jan 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.48.dev.gitaa13779
- autobuilt aa13779

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.47.dev.gitf63005e
- autobuilt f63005e

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.46.dev.gitf467bb2
- autobuilt f467bb2

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.45.dev.gitfb2bd26
- autobuilt fb2bd26

* Sat Jan 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.44.dev.git9be6430
- autobuilt 9be6430

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.43.dev.gitce4bf33
- autobuilt ce4bf33

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.42.dev.git3b6a843
- autobuilt 3b6a843

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.41.dev.gitab7e1a4
- autobuilt ab7e1a4

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.40.dev.gitf5e614b
- autobuilt f5e614b

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.39.dev.gitacbb6c0
- autobuilt acbb6c0

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.38.dev.git74b89da
- autobuilt 74b89da

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.37.dev.git79fbe72
- autobuilt 79fbe72

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.36.dev.git30245af
- autobuilt 30245af

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.35.dev.git1d7176b
- autobuilt 1d7176b

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.34.dev.gitdb00ee9
- autobuilt db00ee9

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.33.dev.git61fbce7
- autobuilt 61fbce7

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.32.dev.gite1e405b
- autobuilt e1e405b

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.31.dev.git978b891
- autobuilt 978b891

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.30.dev.git34429f3
- autobuilt 34429f3

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.29.dev.gite025b43
- autobuilt e025b43

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.28.dev.gitd914cc2
- autobuilt d914cc2

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.27.dev.git12aa9ca
- autobuilt 12aa9ca

* Tue Jan 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.26.dev.gitad5137b
- autobuilt ad5137b

* Tue Jan 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.25.dev.git564bd69
- autobuilt 564bd69

* Tue Jan 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.24.dev.git3961882
- autobuilt 3961882

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.23.dev.git79ec2a9
- autobuilt 79ec2a9

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.22.dev.git6c3d383
- autobuilt 6c3d383

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.21.dev.git796ae87
- autobuilt 796ae87

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.20.dev.gite83a1b8
- autobuilt e83a1b8

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.19.dev.git9e2e4d7
- autobuilt 9e2e4d7

* Sun Jan 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.18.dev.git55dd73c
- autobuilt 55dd73c

* Sat Jan 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.17.dev.git2d5fd7c
- autobuilt 2d5fd7c

* Fri Jan 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.16.dev.git0e9c208
- autobuilt 0e9c208

* Fri Jan 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.15.dev.gite1ffac6
- autobuilt e1ffac6

* Fri Jan 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.14.dev.git6ed88e0
- autobuilt 6ed88e0

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.13.dev.gitf57fdd0
- autobuilt f57fdd0

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.12.dev.git154b5ca
- autobuilt 154b5ca

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.11.dev.gitf3fc10f
- autobuilt f3fc10f

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.10.dev.gitc99b413
- autobuilt c99b413

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.9.dev.gitc6ad42a
- autobuilt c6ad42a

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.8.dev.git27caffb
- autobuilt 27caffb

* Wed Jan 08 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.7.1-0.7.dev.git0b9dd1a
- require container-selinux only when selinux-policy is installed and
  move podman-remote man pages to dedicated package (#1765818)

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.6.dev.git0b9dd1a
- autobuilt 0b9dd1a

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.5.dev.gitc41fd09
- autobuilt c41fd09

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.4.dev.gitbd3d8f4
- autobuilt bd3d8f4

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.3.dev.gitf85b3a0
- autobuilt f85b3a0

* Tue Jan 07 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.7.1-0.2.dev.gite362220
- always require container-selinux (#1765818)

* Mon Jan 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.1-0.1.dev.gite362220
- bump to 1.7.1
- autobuilt e362220

* Mon Jan 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.28.dev.git2d8f1c8
- autobuilt 2d8f1c8

* Mon Jan 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.27.dev.git2e0157a
- autobuilt 2e0157a

* Mon Jan 06 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.7.0-0.26.dev.git9758a97
- also obsolete former podman-manpages package

* Mon Jan 06 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.7.0-0.25.dev.git9758a97
- add podman-manpages provide to main podman package

* Mon Jan 06 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.7.0-0.24.dev.git9758a97
- merge podman-manpages with podman package

* Fri Jan 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.23.dev.git9758a97
- autobuilt 9758a97

* Thu Jan 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.22.dev.git50b4446
- autobuilt 50b4446

* Thu Jan 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.21.dev.git1faa5bb
- autobuilt 1faa5bb

* Tue Dec 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.20.dev.git6a370cb
- autobuilt 6a370cb

* Fri Dec 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.19.dev.gitfcd48db
- autobuilt fcd48db

* Fri Dec 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.18.dev.gite33d7e9
- autobuilt e33d7e9

* Thu Dec 19 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.17.dev.git1ba6d0f
- autobuilt 1ba6d0f

* Thu Dec 19 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.16.dev.gitc1a7911
- autobuilt c1a7911

* Tue Dec 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.15.dev.gite6b8433
- autobuilt e6b8433

* Tue Dec 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.14.dev.gitfab67f3
- autobuilt fab67f3

* Tue Dec 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.13.dev.git1e440a3
- autobuilt 1e440a3

* Tue Dec 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.12.dev.git4329204
- autobuilt 4329204

* Mon Dec 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.11.dev.git1162183
- autobuilt 1162183

* Mon Dec 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.10.dev.gitb2f05e0
- autobuilt b2f05e0

* Mon Dec 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.9.dev.git19064e5
- autobuilt 19064e5

* Sat Dec 14 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.8.dev.git6c7b6d9
- autobuilt 6c7b6d9

* Fri Dec 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.7.dev.git885967f
- autobuilt 885967f

* Fri Dec 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.6.dev.git22849ff
- autobuilt 22849ff

* Fri Dec 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.5.dev.git71a0c0f
- autobuilt 71a0c0f

* Fri Dec 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.4.dev.git123e7ea
- autobuilt 123e7ea

* Thu Dec 12 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.3.dev.git16de498
- autobuilt 16de498

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.2.dev.gitf81f15f
- autobuilt f81f15f

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.7.0-0.1.dev.git5941138
- bump to 1.7.0
- autobuilt 5941138

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.74.dev.git11541ae
- autobuilt 11541ae

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.73.dev.gitdd64038
- autobuilt dd64038

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.72.dev.gita18de10
- autobuilt a18de10

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.71.dev.git282787f
- autobuilt 282787f

* Mon Dec 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.70.dev.gitc2dab75
- autobuilt c2dab75

* Sat Dec 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.69.dev.git7287f69
- autobuilt 7287f69

* Fri Dec 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.68.dev.git82a83b9
- autobuilt 82a83b9

* Fri Dec 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.67.dev.git8924a30
- autobuilt 8924a30

* Fri Dec 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.66.dev.gite9c4820
- autobuilt e9c4820

* Thu Dec 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.65.dev.git465e142
- autobuilt 465e142

* Thu Dec 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.64.dev.git4fb724c
- autobuilt 4fb724c

* Thu Dec 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.63.dev.git813b00e
- autobuilt 813b00e

* Thu Dec 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.62.dev.gitbc40282
- autobuilt bc40282

* Wed Dec 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.61.dev.git4dbab37
- autobuilt 4dbab37

* Wed Dec 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.60.dev.gite47b7a6
- autobuilt e47b7a6

* Wed Dec 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.59.dev.git10f7334
- autobuilt 10f7334

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.58.dev.git06e2a20
- autobuilt 06e2a20

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.57.dev.git5c3af00
- autobuilt 5c3af00

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.56.dev.git748de3c
- autobuilt 748de3c

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.55.dev.gitd8bfd11
- autobuilt d8bfd11

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.54.dev.gitb88f2c4
- autobuilt b88f2c4

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.53.dev.git9e361fd
- autobuilt 9e361fd

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.52.dev.git309452d
- autobuilt 309452d

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.51.dev.git6458f96
- autobuilt 6458f96

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.50.dev.gitb905850
- autobuilt b905850

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.49.dev.gitc9696c4
- autobuilt c9696c4

* Mon Dec 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.48.dev.git7117286
- autobuilt 7117286

* Mon Dec 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.47.dev.git8d00c83
- autobuilt 8d00c83

* Mon Dec 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.46.dev.gite4275b3
- autobuilt e4275b3

* Fri Nov 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.45.dev.git39c705e
- autobuilt 39c705e

* Fri Nov 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.44.dev.git7f53178
- autobuilt 7f53178

* Fri Nov 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.43.dev.git1c0356e
- autobuilt 1c0356e

* Thu Nov 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.42.dev.gitaa95726
- autobuilt aa95726

* Wed Nov 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.41.dev.git2178875
- autobuilt 2178875

* Tue Nov 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.40.dev.git27a09f8
- autobuilt 27a09f8

* Tue Nov 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.39.dev.gitb29928f
- autobuilt b29928f

* Tue Nov 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.38.dev.gitf5ef3d5
- autobuilt f5ef3d5

* Tue Nov 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.37.dev.gitaef3858
- autobuilt aef3858

* Mon Nov 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.36.dev.git9fb0adf
- autobuilt 9fb0adf

* Fri Nov 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.35.dev.git6187e72
- autobuilt 6187e72

* Fri Nov 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.34.dev.git1284260
- autobuilt 1284260

* Fri Nov 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.33.dev.gitc2dfef5
- autobuilt c2dfef5

* Fri Nov 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.32.dev.gite4b8054
- autobuilt e4b8054

* Fri Nov 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.31.dev.git22e7d7d
- autobuilt 22e7d7d

* Thu Nov 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.30.dev.git6392477
- autobuilt 6392477

* Tue Nov 19 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.29.dev.gitc673ff8
- autobuilt c673ff8

* Tue Nov 19 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.28.dev.gitf3f219a
- autobuilt f3f219a

* Mon Nov 18 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.27.dev.git741b90c
- autobuilt 741b90c

* Sun Nov 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.26.dev.gitdb32ed1
- autobuilt db32ed1

* Sat Nov 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.25.dev.gitc6f2383
- autobuilt c6f2383

* Fri Nov 15 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.24.dev.git51c08f3
- autobuilt 51c08f3

* Thu Nov 14 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.23.dev.gitd7ed9fa
- autobuilt d7ed9fa

* Wed Nov 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.22.dev.git225f22b
- autobuilt 225f22b

* Wed Nov 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.21.dev.git15220af
- autobuilt 15220af

* Mon Nov 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.20.dev.gitde32b89
- autobuilt de32b89

* Fri Nov 08 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.19.dev.gitb713e53
- autobuilt b713e53

* Fri Nov 08 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.18.dev.gitf456ce9
- autobuilt f456ce9

* Fri Nov 08 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.17.dev.git4ed12f9
- autobuilt 4ed12f9

* Fri Nov 08 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.16.dev.git92af260
- autobuilt 92af260

* Fri Nov 08 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.15.dev.git3463a71
- autobuilt 3463a71

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.14.dev.git3ec9ee0
- autobuilt 3ec9ee0

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.13.dev.gitd919961
- autobuilt d919961

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.12.dev.git3474997
- autobuilt 3474997

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.11.dev.git24efb5e
- autobuilt 24efb5e

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.10.dev.gitb4a83bf
- autobuilt b4a83bf

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.9.dev.gitaad2904
- autobuilt aad2904

* Wed Nov 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.8.dev.git2e2d82c
- autobuilt 2e2d82c

* Wed Nov 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.7.dev.git581a7ec
- autobuilt 581a7ec

* Wed Nov 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.6.dev.git6f7c290
- autobuilt 6f7c290

* Tue Nov 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.5.dev.gitb4b7272
- autobuilt b4b7272

* Tue Nov 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.4.dev.git7eda1b0
- autobuilt 7eda1b0

* Tue Nov 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.3.dev.gita904e21
- autobuilt a904e21

* Tue Nov 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.2.dev.git08c5c54
- autobuilt 08c5c54

* Tue Nov 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.4-0.1.dev.gitcc19b09
- bump to 1.6.4
- autobuilt cc19b09

* Tue Nov 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.47.dev.git1db4556
- autobuilt 1db4556

* Mon Nov 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.46.dev.git17eadda
- autobuilt 17eadda

* Mon Nov 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.45.dev.git8e5aad9
- autobuilt 8e5aad9

* Mon Nov 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.44.dev.gitefc7f15
- autobuilt efc7f15

* Sun Nov 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.43.dev.gitca4c24c
- autobuilt ca4c24c

* Sat Nov 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.42.dev.git2bf4df4
- autobuilt 2bf4df4

* Sat Nov 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.41.dev.git10d67fc
- autobuilt 10d67fc

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.40.dev.git8238107
- autobuilt 8238107

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.39.dev.git04e8bf3
- autobuilt 04e8bf3

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.38.dev.git69165fa
- autobuilt 69165fa

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.37.dev.git7c7f000
- autobuilt 7c7f000

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.36.dev.git2dae257
- autobuilt 2dae257

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.35.dev.git0bfdeae
- autobuilt 0bfdeae

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.34.dev.git1e750f7
- autobuilt 1e750f7

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.33.dev.git5af166f
- autobuilt 5af166f

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.32.dev.git1b3e79d
- autobuilt 1b3e79d

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.31.dev.git381fa4d
- autobuilt 381fa4d

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.30.dev.git9ba8dae
- autobuilt 9ba8dae

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.29.dev.gita35d002
- autobuilt a35d002

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.28.dev.git63b57f5
- autobuilt 63b57f5

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.27.dev.git4762b63
- autobuilt 4762b63

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.26.dev.gite7540d0
- autobuilt e7540d0

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.25.dev.git6c6e783
- autobuilt 6c6e783

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.24.dev.git59582c5
- autobuilt 59582c5

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.23.dev.gita56131f
- autobuilt a56131f

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.22.dev.git8e264ca
- autobuilt 8e264ca

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.21.dev.git1b5c2d1
- autobuilt 1b5c2d1

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.20.dev.git94864ad
- autobuilt 94864ad

* Sun Oct 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.19.dev.gitac73fd3
- autobuilt ac73fd3

* Sat Oct 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.18.dev.gitea46937
- autobuilt ea46937

* Fri Oct 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.17.dev.gita01cb22
- autobuilt a01cb22

* Thu Oct 24 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.16.dev.git77c7a28
- autobuilt 77c7a28

* Thu Oct 24 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.15.dev.gitba4a808
- autobuilt ba4a808

* Thu Oct 24 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.14.dev.git43b1c2f
- autobuilt 43b1c2f

* Thu Oct 24 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.13.dev.git674dc2b
- autobuilt 674dc2b

* Wed Oct 23 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.12.dev.git299a430
- autobuilt 299a430

* Wed Oct 23 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.11.dev.git2e6c9aa
- autobuilt 2e6c9aa

* Wed Oct 23 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.10.dev.gitef556cf
- autobuilt ef556cf

* Tue Oct 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.9.dev.git46ad6bc
- autobuilt 46ad6bc

* Tue Oct 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.8.dev.gitd358840
- autobuilt d358840

* Tue Oct 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.7.dev.git5431ace
- autobuilt 5431ace

* Mon Oct 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.6.dev.gitefc54c3
- autobuilt efc54c3

* Mon Oct 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.5.dev.gitd2591a5
- autobuilt d2591a5

* Sun Oct 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.4.dev.gitd3520de
- autobuilt d3520de

* Fri Oct 18 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.3.dev.git02ab9c7
- autobuilt 02ab9c7

* Fri Oct 18 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.2.dev.gitf0da9cf
- autobuilt f0da9cf

* Thu Oct 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.3-0.1.dev.gitb6fdfa0
- bump to 1.6.3
- autobuilt b6fdfa0

* Thu Oct 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.41.dev.git2b0892e
- autobuilt 2b0892e

* Thu Oct 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.40.dev.gitf2d9a9d
- autobuilt f2d9a9d

* Thu Oct 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.39.dev.gitd7cbcfa
- autobuilt d7cbcfa

* Thu Oct 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.38.dev.git392846c
- autobuilt 392846c

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.37.dev.gite7d5ac0
- autobuilt e7d5ac0

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.36.dev.gitdc1f8b6
- autobuilt dc1f8b6

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.35.dev.git7825c58
- autobuilt 7825c58

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.34.dev.git8172460
- autobuilt 8172460

* Tue Oct 15 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.33.dev.git5f72e6e
- autobuilt 5f72e6e

* Mon Oct 14 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.32.dev.gita9190da
- autobuilt a9190da

* Mon Oct 14 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.31.dev.git3e45d07
- autobuilt 3e45d07

* Sat Oct 12 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.30.dev.gita8993ba
- autobuilt a8993ba

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.29.dev.gitb0b3506
- autobuilt b0b3506

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.28.dev.git79d05b9
- autobuilt 79d05b9

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.27.dev.gitcee6478
- autobuilt cee6478

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.26.dev.giteb6ca05
- autobuilt eb6ca05

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.25.dev.git50b1884
- autobuilt 50b1884

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.24.dev.git9f1f4ef
- autobuilt 9f1f4ef

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.23.dev.git495db28
- autobuilt 495db28

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.22.dev.git43dcc91
- autobuilt 43dcc91

* Thu Oct 10 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.21.dev.git6d35eac
- autobuilt 6d35eac

* Thu Oct 10 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.20.dev.gitf39e097
- autobuilt f39e097

* Thu Oct 10 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.19.dev.gita7f2668
- autobuilt a7f2668

* Wed Oct 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.18.dev.git12c9b53
- autobuilt 12c9b53

* Wed Oct 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.17.dev.gitf61e399
- autobuilt f61e399

* Wed Oct 09 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.2-0.16.dev.gitc3c40f9
- remove polkit dependency for now

* Wed Oct 09 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.2-0.15.dev.gitc3c40f9
- Requires: crun >= 0.10.2-1 and polkit

* Wed Oct 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.14.dev.gitc3c40f9
- autobuilt c3c40f9

* Tue Oct 08 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.13.dev.git10cbaad
- autobuilt 10cbaad

* Tue Oct 08 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.2-0.12.dev.gitc817ea1
- add runc back

* Mon Oct 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.11.dev.gitc817ea1
- autobuilt c817ea1

* Mon Oct 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.10.dev.git589261f
- autobuilt 589261f

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.9.dev.git2c2782a
- autobuilt 2c2782a

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.8.dev.gitbd08fc0
- autobuilt bd08fc0

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.7.dev.git70d5b0a
- autobuilt 70d5b0a

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.6.dev.git1fe9556
- autobuilt 1fe9556

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.5.dev.git7af4074
- autobuilt 7af4074

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.4.dev.git86c8650
- autobuilt 86c8650

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.3.dev.gitf96fbfc
- autobuilt f96fbfc

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.2.dev.gitb32cb4b
- autobuilt b32cb4b

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.1.dev.gite67e9e1
- bump to 1.6.2
- autobuilt e67e9e1

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.12.dev.git960f07b
- autobuilt 960f07b

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.11.dev.git0046b01
- autobuilt 0046b01

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.10.dev.gitdac7889
- autobuilt dac7889

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.9.dev.git2648955
- autobuilt 2648955

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.8.dev.git257a985
- autobuilt 257a985

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.7.dev.git32a2ce8
- autobuilt 32a2ce8

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.6.dev.git74879c8
- autobuilt 74879c8

* Tue Oct 01 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.1-0.5.dev.git7a56963
- Requires: crun >= 0.10-1

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.4.dev.git7a56963
- autobuilt 7a56963

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.3.dev.git8f2ec88
- autobuilt 8f2ec88

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.2.dev.git049aafa
- autobuilt 049aafa

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.1.dev.git5d344db
- bump to 1.6.1
- autobuilt 5d344db

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.42.dev.gitd7eba02
- autobuilt d7eba02

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.41.dev.git5702dd7
- autobuilt 5702dd7

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.40.dev.gitb063383
- autobuilt b063383

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.39.dev.git04b3a73
- autobuilt 04b3a73

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.38.dev.git2c23729
- autobuilt 2c23729

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.37.dev.git150ba5e
- autobuilt 150ba5e

* Sun Sep 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.36.dev.git01b7af8
- autobuilt 01b7af8

* Sat Sep 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.35.dev.git01a802e
- autobuilt 01a802e

* Fri Sep 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.34.dev.gite87012d
- autobuilt e87012d

* Fri Sep 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.33.dev.git0fb807d
- autobuilt 0fb807d

* Fri Sep 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.32.dev.gitd4399ee
- autobuilt d4399ee

* Fri Sep 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.31.dev.gita8c2b5d
- autobuilt a8c2b5d

* Thu Sep 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.30.dev.git851e377
- autobuilt 851e377

* Thu Sep 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.29.dev.gitd76b21e
- autobuilt d76b21e

* Wed Sep 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.28.dev.git3ed265c
- autobuilt 3ed265c

* Wed Sep 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.27.dev.git19075ca
- autobuilt 19075ca

* Wed Sep 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.26.dev.git8ab3c86
- autobuilt 8ab3c86

* Wed Sep 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.25.dev.gitf197ebe
- autobuilt f197ebe

* Wed Sep 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.24.dev.git240095e
- autobuilt 240095e

* Wed Sep 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.23.dev.git525be7d
- autobuilt 525be7d

* Tue Sep 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.22.dev.git0000afc
- autobuilt 0000afc

* Tue Sep 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.21.dev.git1dfac0e
- autobuilt 1dfac0e

* Tue Sep 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.20.dev.gitb300b98
- autobuilt b300b98

* Tue Sep 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.19.dev.git83b2348
- autobuilt 83b2348

* Mon Sep 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.18.dev.git6ce8d05
- autobuilt 6ce8d05

* Mon Sep 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.17.dev.gitf5951c7
- autobuilt f5951c7

* Mon Sep 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.16.dev.gita74dfda
- autobuilt a74dfda

* Sun Sep 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.15.dev.gitc0eff1a
- autobuilt c0eff1a

* Sat Sep 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.14.dev.git0d95e3a
- autobuilt 0d95e3a

* Sat Sep 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.13.dev.gite947d63
- autobuilt e947d63

* Sat Sep 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.12.dev.git819b63c
- autobuilt 819b63c

* Fri Sep 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.11.dev.git66f4bc7
- autobuilt 66f4bc7

* Fri Sep 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.10.dev.git7ed1816
- autobuilt 7ed1816

* Fri Sep 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.9.dev.git9dc764c
- autobuilt 9dc764c

* Thu Sep 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.8.dev.gitc38844f
- autobuilt c38844f

* Thu Sep 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.7.dev.git408f278
- autobuilt 408f278

* Wed Sep 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.6.dev.gitfe48b9e
- autobuilt fe48b9e

* Wed Sep 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.5.dev.git8133aa1
- autobuilt 8133aa1

* Wed Sep 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.4.dev.git2c51d6f
- autobuilt 2c51d6f

* Tue Sep 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.3.dev.git143caa9
- autobuilt 143caa9

* Tue Sep 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.2.dev.git799aa70
- autobuilt 799aa70

* Mon Sep 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-0.1.dev.git2aa6771
- bump to 1.6.0
- autobuilt 2aa6771

* Mon Sep 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.92.dev.git2a4e062
- autobuilt 2a4e062

* Mon Sep 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.91.dev.git0014d6c
- autobuilt 0014d6c

* Mon Sep 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.90.dev.git1f5514e
- autobuilt 1f5514e

* Sat Sep 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.89.dev.gita1970e1
- autobuilt a1970e1

* Sat Sep 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.88.dev.git2366fd7
- autobuilt 2366fd7

* Fri Sep 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.87.dev.git0079c24
- autobuilt 0079c24

* Fri Sep 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.86.dev.gitd74cede
- autobuilt d74cede

* Fri Sep 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.85.dev.git7875e00
- autobuilt 7875e00

* Fri Sep 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.84.dev.git5c09c4d
- autobuilt 5c09c4d

* Fri Sep 13 2019 Daniel J Walsh <dwalsh@redhat.com> - 2:1.5.2-0.83.dev.gitb095d8a
- Grab specific version of crun or newer.

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.82.dev.gitb095d8a
- autobuilt b095d8a

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.81.dev.gitb43a36d
- autobuilt b43a36d

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.80.dev.git1ddfc11
- autobuilt 1ddfc11

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.79.dev.gitaf8fedc
- autobuilt af8fedc

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.78.dev.gitafa3d11
- autobuilt afa3d11

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.77.dev.git57e093b
- autobuilt 57e093b

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.76.dev.gitce31aa3
- autobuilt ce31aa3

* Wed Sep 11 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.5.2-0.75.dev.git79ebb5f
- use conmon package as dependency

* Wed Sep 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.74.dev.git79ebb5f
- autobuilt 79ebb5f

* Wed Sep 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.73.dev.gitf73c3b8
- autobuilt f73c3b8

* Wed Sep 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.72.dev.git093013b
- autobuilt 093013b

* Wed Sep 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.71.dev.git9cf852c
- autobuilt 9cf852c

* Tue Sep 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.70.dev.git7ac6ed3
- autobuilt 7ac6ed3

* Tue Sep 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.69.dev.git997c4b5
- autobuilt 997c4b5

* Tue Sep 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.68.dev.gitc1761ba
- autobuilt c1761ba

* Tue Sep 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.67.dev.git095647c
- autobuilt 095647c

* Tue Sep 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.66.dev.git5233536
- autobuilt 5233536

* Mon Sep 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.65.dev.git9a55bce
- autobuilt 9a55bce

* Mon Sep 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.64.dev.git7042a3d
- autobuilt 7042a3d

* Mon Sep 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.63.dev.git511b071
- autobuilt 511b071

* Mon Sep 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.62.dev.git16a7049
- autobuilt 16a7049

* Mon Sep 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.61.dev.gitd78521d
- autobuilt d78521d

* Sun Sep 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.60.dev.gitf500feb
- autobuilt f500feb

* Sun Sep 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.59.dev.git7312811
- autobuilt 7312811

* Fri Sep 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.58.dev.git30cbb00
- autobuilt 30cbb00

* Fri Sep 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.57.dev.git290def5
- autobuilt 290def5

* Fri Sep 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.56.dev.git575ffee
- autobuilt 575ffee

* Fri Sep 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.55.dev.git8898085
- autobuilt 8898085

* Fri Sep 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.54.dev.git24171ae
- autobuilt 24171ae

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.53.dev.gita4572c4
- autobuilt a4572c4

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.52.dev.gitcef5bec
- autobuilt cef5bec

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.51.dev.git3f81f44
- autobuilt 3f81f44

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.50.dev.gitb962b1e
- autobuilt b962b1e

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.49.dev.gite74fcd7
- autobuilt e74fcd7

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.48.dev.git84140f5
- autobuilt 84140f5

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.47.dev.gitf1a3e02
- autobuilt f1a3e02

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.46.dev.git1d8a940
- autobuilt 1d8a940

* Tue Sep 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.45.dev.gita16f63e
- autobuilt a16f63e

* Tue Sep 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.44.dev.gitc039499
- autobuilt c039499

* Tue Sep 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.43.dev.git50a1910
- autobuilt 50a1910

* Mon Sep 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.42.dev.git099549b
- autobuilt 099549b

* Sun Sep 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.41.dev.gite5568d4
- autobuilt e5568d4

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.40.dev.git8ba21ac
- autobuilt 8ba21ac

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.39.dev.git3e0fdc7
- autobuilt 3e0fdc7

* Thu Aug 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.38.dev.gitd110998
- autobuilt d110998

* Thu Aug 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.37.dev.gitab5f52c
- autobuilt ab5f52c

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.36.dev.git1eb6b27
- autobuilt 1eb6b27

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.35.dev.gitbdf9e56
- autobuilt bdf9e56

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.34.dev.git4e209fc
- autobuilt 4e209fc

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.33.dev.git61dc63f
- autobuilt 61dc63f

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.32.dev.gite5c5a33
- autobuilt e5c5a33

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.31.dev.gita1a1342
- autobuilt a1a1342

* Tue Aug 27 2019 Daniel J Walsh <dwalsh@redhat.com> - 2:1.5.2-0.30.dev.gitf221c61
- Require crun rather then runc
- Switch to crun by default for cgroupsV2 support

* Tue Aug 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.29.dev.gitf221c61
- autobuilt f221c61

* Mon Aug 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.28.dev.gitcec354a
- autobuilt cec354a

* Mon Aug 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.27.dev.git112a3cc
- autobuilt 112a3cc

* Mon Aug 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.26.dev.git67926d8
- autobuilt 67926d8

* Sun Aug 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.25.dev.gitc0528c1
- autobuilt c0528c1

* Thu Aug 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.24.dev.git59261cf
- autobuilt 59261cf

* Thu Aug 22 2019 Daniel J Walsh <dwalsh@redhat.com> - 2:1.5.2-0.23.dev.gitb263dd9
- Move man5 man pages into podman-manpage package

* Thu Aug 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.22.dev.gitb263dd9
- autobuilt b263dd9

* Thu Aug 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.21.dev.git34002f9
- autobuilt 34002f9

* Thu Aug 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.20.dev.git18f2328
- autobuilt 18f2328

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.19.dev.gitecc5cc5
- autobuilt ecc5cc5

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.18.dev.git1ff984d
- autobuilt 1ff984d

* Tue Aug 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.17.dev.git1ad8fe5
- autobuilt 1ad8fe5

* Tue Aug 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.16.dev.gitf618bc3
- autobuilt f618bc3

* Tue Aug 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.15.dev.gita3c46fc
- autobuilt a3c46fc

* Tue Aug 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.14.dev.git230faa8
- autobuilt 230faa8

* Tue Aug 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.13.dev.git34fc1d0
- autobuilt 34fc1d0

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.12.dev.git890378e
- autobuilt 890378e

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.11.dev.gitd23639a
- autobuilt d23639a

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.10.dev.gitc137e8f
- autobuilt c137e8f

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.9.dev.gitb1acc43
- autobuilt b1acc43

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.8.dev.gitbd0b05f
- autobuilt bd0b05f

* Sun Aug 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.7.dev.git438cbf4
- autobuilt 438cbf4

* Sat Aug 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.6.dev.git76f327f
- autobuilt 76f327f

* Sat Aug 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.5.dev.git098ce2f
- autobuilt 098ce2f

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.4.dev.git8eab96e
- autobuilt 8eab96e

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.3.dev.git704cc58
- autobuilt 704cc58

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.2.dev.git2d47f1a
- autobuilt 2d47f1a

* Thu Aug 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.2-0.1.dev.git05149e6
- bump to 1.5.2
- autobuilt 05149e6

* Thu Aug 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-9.16.dev.gitb9a176b
- autobuilt b9a176b

* Thu Aug 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-8.16.dev.git74224d9
- autobuilt 74224d9

* Thu Aug 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-7.16.dev.git3f1657d
- autobuilt 3f1657d

* Thu Aug 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-6.16.dev.gitf9ddf91
- autobuilt f9ddf91

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-5.16.dev.gitbf9e801
- autobuilt bf9e801

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-4.16.dev.gitf5dcb80
- autobuilt f5dcb80

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-3.16.dev.git4823cf8
- autobuilt 4823cf8

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-2.16.dev.gita734b53
- autobuilt a734b53

* Tue Aug 13 2019 Dan Walsh <dwalsh@fedoraproject.org> - 2:1.5.1-1.16.dev.gitce64c14
- Add recommends libvarlink-util

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.16.dev.gitce64c14
- autobuilt ce64c14

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.15.dev.git7a859f0
- autobuilt 7a859f0

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.14.dev.git031437b
- autobuilt 031437b

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.13.dev.gitc48243e
- autobuilt c48243e

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.12.dev.gitf634fd3
- autobuilt f634fd3

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.11.dev.git3cf4567
- autobuilt 3cf4567

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.10.dev.git9bee690
- autobuilt 9bee690

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.9.dev.gitca7bae7
- autobuilt ca7bae7

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.8.dev.gitec93c9d
- autobuilt ec93c9d

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.7.dev.gitf18cfa4
- autobuilt f18cfa4

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.6.dev.git2348c28
- autobuilt 2348c28

* Sun Aug 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.5.dev.git1467197
- autobuilt 1467197

* Sun Aug 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.4.dev.git7bbaa36
- autobuilt 7bbaa36

* Sat Aug 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.3.dev.git3bc861c
- autobuilt 3bc861c

* Sat Aug 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.2.dev.git926901d
- autobuilt 926901d

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.1.dev.git2018faa
- bump to 1.5.1
- autobuilt 2018faa

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.99.dev.gitbb80586
- autobuilt bb80586

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.98.dev.gitd05798e
- autobuilt d05798e

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.97.dev.git4b91f60
- autobuilt 4b91f60

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.96.dev.gitdc38168
- autobuilt dc38168

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.95.dev.git00a20f7
- autobuilt 00a20f7

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.94.dev.git2a19036
- autobuilt 2a19036

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.93.dev.git76840f2
- autobuilt 76840f2

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.92.dev.git4349f42
- autobuilt 4349f42

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.91.dev.git202eade
- autobuilt 202eade

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.90.dev.git09cedd1
- autobuilt 09cedd1

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.89.dev.git3959a35
- autobuilt 3959a35

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.88.dev.git5701fe6
- autobuilt 5701fe6

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.87.dev.git31bfb12
- autobuilt 31bfb12

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.86.dev.git41de7b1
- autobuilt 41de7b1

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.85.dev.git35ecf49
- autobuilt 35ecf49

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.84.dev.git66ea32c
- autobuilt 66ea32c

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.83.dev.gitf0a5b7f
- autobuilt f0a5b7f

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.82.dev.gitb5618d9
- autobuilt b5618d9

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.81.dev.git3bffe77
- autobuilt 3bffe77

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.80.dev.git337358a
- autobuilt 337358a

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.79.dev.git626dfdb
- autobuilt 626dfdb

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.78.dev.gite2f38cd
- autobuilt e2f38cd

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.77.dev.gitb609de2
- autobuilt b609de2

* Sun Aug 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.76.dev.git389a7b7
- autobuilt 389a7b7

* Sun Aug 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.75.dev.gitd9ea4db
- autobuilt d9ea4db

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.74.dev.git140e08e
- autobuilt 140e08e

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.73.dev.git3cc9ab8
- autobuilt 3cc9ab8

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.72.dev.git5370c53
- autobuilt 5370c53

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.71.dev.git2cc5913
- autobuilt 2cc5913

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.70.dev.gite3240da
- autobuilt e3240da

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.69.dev.gite48dc50
- autobuilt e48dc50

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.68.dev.git1bbcb2f
- autobuilt 1bbcb2f

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.67.dev.gite1a099e
- autobuilt e1a099e

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.66.dev.gitafb493a
- autobuilt afb493a

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.65.dev.git6f62dac
- autobuilt 6f62dac

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.64.dev.gitee15e76
- autobuilt ee15e76

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.63.dev.git5056964
- autobuilt 5056964

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.62.dev.git3215ea6
- autobuilt 3215ea6

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.61.dev.gitccf4ec2
- autobuilt ccf4ec2

* Wed Jul 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.60.dev.gita622f8d
- autobuilt a622f8d

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.59.dev.git680a383
- autobuilt 680a383

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.58.dev.gite84ed3c
- autobuilt e84ed3c

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.57.dev.git1a00895
- autobuilt 1a00895

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.56.dev.git4196a59
- autobuilt 4196a59

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.55.dev.git040355d
- autobuilt 040355d

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.54.dev.git7d635ac
- autobuilt 7d635ac

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.53.dev.gitc3c45f3
- autobuilt c3c45f3

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.52.dev.git6665269
- autobuilt 6665269

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.51.dev.git2ca7861
- autobuilt 2ca7861

* Sun Jul 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.50.dev.git2c98bd5
- autobuilt 2c98bd5

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.49.dev.git0c4dfcf
- autobuilt 0c4dfcf

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.48.dev.giteca157f
- autobuilt eca157f

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.47.dev.git1910d68
- autobuilt 1910d68

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.46.dev.git4674d00
- autobuilt 4674d00

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.45.dev.gitdff82d9
- autobuilt dff82d9

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.44.dev.git5763618
- autobuilt 5763618

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.43.dev.git7c9095e
- autobuilt 7c9095e

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.42.dev.git2283471
- autobuilt 2283471

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.41.dev.git0917783
- autobuilt 0917783

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.40.dev.giteae9a00
- autobuilt eae9a00

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.39.dev.git3c6b111
- autobuilt 3c6b111

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.38.dev.git7dbc6d8
- autobuilt 7dbc6d8

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.37.dev.gitbb253af
- autobuilt bb253af

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.36.dev.gitce60c4d
- autobuilt ce60c4d

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.35.dev.git2674920
- autobuilt 2674920

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.34.dev.gita12a231
- autobuilt a12a231

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.33.dev.gitcf9efa9
- autobuilt cf9efa9

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.32.dev.git69f74f1
- autobuilt 69f74f1

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.31.dev.gitab7b47c
- autobuilt ab7b47c

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.30.dev.git3b52e4d
- autobuilt 3b52e4d

* Sun Jul 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.29.dev.gitd6b41eb
- autobuilt d6b41eb

* Sat Jul 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.28.dev.gita5aa44c
- autobuilt a5aa44c

* Sat Jul 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.27.dev.git8364552
- autobuilt 8364552

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.26.dev.git02140ea
- autobuilt 02140ea

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.25.dev.git398aeac
- autobuilt 398aeac

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.24.dev.gitdeb087d
- autobuilt deb087d

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.23.dev.gitb59abdc
- autobuilt b59abdc

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.22.dev.git2254a35
- autobuilt 2254a35

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.21.dev.git1065548
- autobuilt 1065548

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.20.dev.gitade0d87
- autobuilt ade0d87

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.19.dev.git22e62e8
- autobuilt 22e62e8

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.18.dev.gitadcde23
- autobuilt adcde23

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.17.dev.git456c045
- autobuilt 456c045

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.16.dev.git7488ed6
- autobuilt 7488ed6

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.15.dev.gitb2734ba
- autobuilt b2734ba

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.14.dev.git1c02905
- autobuilt 1c02905

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.13.dev.git04a9cb0
- autobuilt 04a9cb0

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.12.dev.gitfe83308
- autobuilt fe83308

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.11.dev.git400851a
- autobuilt 400851a

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.10.dev.gita449e9a
- autobuilt a449e9a

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.9.dev.git386ffd2
- autobuilt 386ffd2

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.8.dev.git7e4db44
- autobuilt 7e4db44

* Mon Jul 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.7.dev.gitd2291ec
- autobuilt d2291ec

* Sun Jul 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.6.dev.git456b6ab
- autobuilt 456b6ab

* Fri Jul 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.5.dev.gite2e8477
- built conmon 1de71ad

* Thu Jul 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.4.dev.gite2e8477
- autobuilt e2e8477

* Wed Jul 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.3.dev.gitdf3f5af
- autobuilt df3f5af

* Tue Jul 09 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.4.5-0.2.dev.gitcea0e93
- Resolves: #1727933 - containers-monuts.conf.5 moved to containers-common

* Sun Jul 07 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.4.5-0.1.dev.gitf7407f2
- bump to v1.4.5-dev
- use new name for go-md2man
- include centos conditionals

* Sun Jun 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.30.dev.git7c4e444
- autobuilt 7c4e444

* Sat Jun 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.29.dev.gitd9bdd3c
- autobuilt d9bdd3c

* Fri Jun 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.28.dev.git39fdf91
- autobuilt 39fdf91

* Thu Jun 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.27.dev.gitb4f9bc8
- autobuilt b4f9bc8

* Wed Jun 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.26.dev.git240b846
- bump to 1.4.3
- autobuilt 240b846

* Tue Jun 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.2-0.25.dev.git8bcfd24
- autobuilt 8bcfd24

* Sun Jun 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.2-0.24.dev.git670fc03
- autobuilt 670fc03

* Sat Jun 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.2-0.23.dev.git185b413
- bump to 1.4.2
- autobuilt 185b413

* Fri Jun 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.22.dev.git2784cf3
- autobuilt 2784cf3

* Thu Jun 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.21.dev.git77d1cf0
- autobuilt 77d1cf0

* Wed Jun 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.20.dev.gitf8a84fd
- autobuilt f8a84fd

* Tue Jun 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.19.dev.gitc93b8d6
- do not install /usr/libexec/crio - conflicts with crio

* Tue Jun 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.18.dev.gitc93b8d6
- autobuilt c93b8d6

* Mon Jun 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.17.dev.gitfcb7c14
- autobuilt fcb7c14

* Sun Jun 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.16.dev.git39f5ea4
- autobuilt 39f5ea4

* Sat Jun 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.15.dev.gitcae5af5
- bump to 1.4.1
- autobuilt cae5af5

* Fri Jun 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.14.dev.gitba36a5f
- autobuilt ba36a5f

* Fri Jun 07 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.3.2-0.13.dev.git6d285b8
- Resolves: #1716809 - use conmon v0.2.0

* Thu Jun 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.12.dev.git6d285b8
- autobuilt 6d285b8

* Wed Jun 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.11.dev.git3fb9669
- autobuilt 3fb9669

* Tue Jun 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.10.dev.git0ede794
- autobuilt 0ede794

* Sun Jun 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.9.dev.git176a41c
- autobuilt 176a41c

* Sat Jun 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.8.dev.git2068919
- autobuilt 2068919

* Fri May 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.7.dev.git558ce8d
- autobuilt 558ce8d

* Thu May 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.6.dev.gitc871653
- autobuilt c871653

* Wed May 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.5.dev.git8649dbd
- autobuilt 8649dbd

* Mon May 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.4.dev.git25f8c21
- autobuilt 25f8c21

* Sun May 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.3.dev.gitb1d590b
- autobuilt b1d590b

* Fri May 24 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.3.2-0.2.dev.git1ac06d8
- built commit 1ac06d8
- BR: systemd-devel
- correct build steps for %%{name}-remote

* Fri May 24 2019 Dan Walsh <dwalsh@fedoraproject.org> - 2:1.3.2-0.1.dev.git5296428
- Bump up to latest on master

* Fri May 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.3.1-0.1.dev.git9ae3221
- bump to v1.3.1-dev
- built 9ae3221
- correct release tag format for unreleased versions

* Thu Apr 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-21.dev.gitb01fdcb
- autobuilt b01fdcb

* Tue Apr 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-20.dev.gitd652c86
- autobuilt d652c86

* Sat Apr 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-19.dev.git9f92b21
- autobuilt 9f92b21

* Fri Apr 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-18.dev.gite4947e5
- autobuilt e4947e5

* Thu Apr 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-17.dev.gitbf5ffda
- autobuilt bf5ffda

* Wed Apr 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-16.dev.gita87cf6f
- autobuilt a87cf6f

* Tue Apr 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-15.dev.gitc1e2b58
- autobuilt c1e2b58

* Mon Apr 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-14.dev.git167ce59
- autobuilt 167ce59

* Sun Apr 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-13.dev.gitb926005
- autobuilt b926005

* Sat Apr 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-12.dev.git1572367
- autobuilt 1572367

* Fri Apr 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-11.dev.git387d601
- autobuilt 387d601

* Thu Apr 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-10.dev.git6cd6eb6
- autobuilt 6cd6eb6

* Wed Apr 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-9.dev.git60ef8f8
- autobuilt 60ef8f8

* Tue Apr 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-8.dev.gitc94903a
- autobuilt c94903a

* Sat Apr 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-7.dev.gitbc320be
- autobuilt bc320be

* Fri Apr 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-6.dev.gitbda28c6
- autobuilt bda28c6

* Thu Apr 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-5.dev.git4bda537
- autobuilt 4bda537

* Wed Apr 03 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.3.0-4.dev.gitad467ba
- Resolves: #1695492 - own /usr/libexec/podman

* Tue Apr 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-3.dev.gitad467ba
- autobuilt ad467ba

* Mon Apr 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-2.dev.gitcd35e20
- bump to 1.3.0
- autobuilt cd35e20

* Sun Mar 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-30.dev.git833204d
- autobuilt 833204d

* Sat Mar 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-29.dev.git7b73974
- autobuilt 7b73974

* Fri Mar 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-28.dev.gitfdf979a
- autobuilt fdf979a

* Thu Mar 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-27.dev.git850326c
- autobuilt 850326c

* Wed Mar 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-26.dev.gitfc546d4
- autobuilt fc546d4

* Mon Mar 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-25.dev.gitd0c6a35
- autobuilt d0c6a35

* Sat Mar 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-24.dev.git0458daf
- autobuilt 0458daf

* Fri Mar 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-23.dev.git68e3df3
- autobuilt 68e3df3

* Thu Mar 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-22.dev.gitc230f0c
- autobuilt c230f0c

* Wed Mar 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-21.dev.git537c382
- autobuilt 537c382

* Tue Mar 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-20.dev.gitac523cb
- autobuilt ac523cb

* Mon Mar 18 2019 Eduardo Santiago <santiago@redhat.com> - 2:1.2.0-19.dev.git6aa8078
- include zsh completion

* Fri Mar 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-18.dev.git31f11a8
- autobuilt 31f11a8

* Thu Mar 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-17.dev.git7426d4f
- autobuilt 7426d4f

* Wed Mar 13 2019 Eduardo Santiago <santiago@redhat.com> - 2:1.2.0-16.dev.git883566f
- new -tests subpackage

* Wed Mar 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-15.dev.git883566f
- autobuilt 883566f

* Tue Mar 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-14.dev.gitde0192a
- autobuilt de0192a

* Sun Mar 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-13.dev.gitd95f97a
- autobuilt d95f97a

* Sat Mar 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-12.dev.git9b21f14
- autobuilt 9b21f14

* Fri Mar 08 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.2.0-11.dev.git1b2f867
- Resolves: #1686813 - conmon bundled inside podman rpm

* Fri Mar 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-10.dev.git1b2f867
- autobuilt 1b2f867

* Thu Mar 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-9.dev.git614409f
- autobuilt 614409f

* Wed Mar 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-8.dev.git40f7843
- autobuilt 40f7843

* Tue Mar 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-7.dev.git4b80517
- autobuilt 4b80517

* Mon Mar 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-6.dev.gitf3a3d8e
- autobuilt f3a3d8e

* Sat Mar 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-5.dev.git9adcda7
- autobuilt 9adcda7

* Fri Mar 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-4.dev.git9137315
- autobuilt 9137315

* Thu Feb 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-3.dev.git5afae0b
- autobuilt 5afae0b

* Wed Feb 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-2.dev.git623fcfa
- bump to 1.2.0
- autobuilt 623fcfa

* Tue Feb 26 2019 Dan Walsh <dwalsh@fedoraproject.org> - 2:1.0.1-39.dev.gitcf52144
* Tue Feb 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-38.dev.gitcf52144
- autobuilt cf52144

* Mon Feb 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-37.dev.git553ac80
- autobuilt 553ac80

* Sun Feb 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-36.dev.gitcc4addd
- autobuilt cc4addd

* Sat Feb 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-35.dev.gitb223d4e
- autobuilt b223d4e

* Fri Feb 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-34.dev.git1788add
- autobuilt 1788add

* Thu Feb 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-33.dev.git4934bf2
- autobuilt 4934bf2

* Wed Feb 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-32.dev.git3b88c73
- autobuilt 3b88c73

* Tue Feb 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-31.dev.git228d1cb
- autobuilt 228d1cb

* Mon Feb 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-30.dev.git3f32eae
- autobuilt 3f32eae

* Sun Feb 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-29.dev.git1cb16bd
- autobuilt 1cb16bd

* Sat Feb 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-28.dev.git0a521e1
- autobuilt 0a521e1

* Fri Feb 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-27.dev.git81ace5c
- autobuilt 81ace5c

* Thu Feb 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-26.dev.gitdfc64e1
- autobuilt dfc64e1

* Wed Feb 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-25.dev.gitee27c39
- autobuilt ee27c39

* Tue Feb 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-24.dev.git8923703
- autobuilt 8923703

* Sun Feb 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-23.dev.gitc86e8f1
- autobuilt c86e8f1

* Sat Feb 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-22.dev.gitafd4d5f
- autobuilt afd4d5f

* Fri Feb 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-21.dev.git962850c
- autobuilt 962850c

* Thu Feb 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-20.dev.gitf250745
- autobuilt f250745

* Wed Feb 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-19.dev.git650e242
- autobuilt 650e242

* Tue Feb 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-18.dev.git778f986
- autobuilt 778f986

* Sun Feb 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-17.dev.gitd5593b8
- autobuilt d5593b8

* Sat Feb 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-16.dev.gite6426af
- autobuilt e6426af

* Fri Feb 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-15.dev.gite97dc8e
- autobuilt e97dc8e

* Thu Jan 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-14.dev.git805c6d9
- autobuilt 805c6d9

* Wed Jan 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-13.dev.gitad5579e
- autobuilt ad5579e

* Tue Jan 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-12.dev.gitebe9297
- autobuilt ebe9297

* Thu Jan 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-11.dev.gitc9e1f36
- autobuilt c9e1f36

* Wed Jan 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-10.dev.git7838a13
- autobuilt 7838a13

* Tue Jan 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-9.dev.gitec96987
- autobuilt ec96987

* Mon Jan 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-8.dev.gitef2f6f9
- autobuilt ef2f6f9

* Sun Jan 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-7.dev.git579fc0f
- autobuilt 579fc0f

* Sat Jan 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-6.dev.git0d4bfb0
- autobuilt 0d4bfb0

* Fri Jan 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-5.dev.gite3dc660
- autobuilt e3dc660

* Thu Jan 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-4.dev.git0e3264a
- autobuilt 0e3264a

* Wed Jan 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-3.dev.git1b2f752
- autobuilt 1b2f752

* Tue Jan 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-2.dev.git6301f6a
- bump to 1.0.1
- autobuilt 6301f6a

* Mon Jan 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-3.dev.git140ae25
- autobuilt 140ae25

* Sat Jan 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-2.dev.git5c86efb
- bump to 0.12.2
- autobuilt 5c86efb

* Fri Jan 11 2019 bbaude <bbaude@redhat.com> - 1:1.0.0-1.dev.git82e8011
- Upstream 1.0.0 release

* Thu Jan 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-27.dev.git0f6535c
- autobuilt 0f6535c

* Wed Jan 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-26.dev.gitc9d63fe
- autobuilt c9d63fe

* Tue Jan 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-25.dev.gitfaa2462
- autobuilt faa2462

* Mon Jan 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-24.dev.gitb83b07c
- autobuilt b83b07c

* Sat Jan 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-23.dev.git4e0c0ec
- autobuilt 4e0c0ec

* Fri Jan 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-22.dev.git9ffd480
- autobuilt 9ffd480

* Thu Jan 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-21.dev.git098c134
- autobuilt 098c134

* Tue Jan 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-20.dev.git7438b7b
- autobuilt 7438b7b

* Sat Dec 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb9.dev.git1aa55ed
- autobuilt 1aa55ed

* Thu Dec 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb8.dev.gitc50332d
- Enable python dependency generator

* Tue Dec 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb7.dev.gitc50332d
- autobuilt c50332d

* Mon Dec 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb6.dev.git8fe3050
- autobuilt 8fe3050

* Sun Dec 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb5.dev.git792f109
- autobuilt 792f109

* Sat Dec 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb4.dev.gitfe186c6
- autobuilt fe186c6

* Fri Dec 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb3.dev.gitfa998f2
- autobuilt fa998f2

* Thu Dec 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb2.dev.git6b059a5
- autobuilt 6b059a5

* Wed Dec 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb1.dev.gitc8eaf59
- autobuilt c8eaf59

* Tue Dec 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb0.dev.git68414c5
- autobuilt 68414c5

* Mon Dec 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-9.dev.gitb21d474
- autobuilt b21d474

* Sat Dec 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-8.dev.gitc086118
- autobuilt c086118

* Fri Dec 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-7.dev.git93b5ccf
- autobuilt 93b5ccf

* Thu Dec 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-6.dev.git508388b
- autobuilt 508388b

* Wed Dec 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-5.dev.git8a3361f
- autobuilt 8a3361f

* Tue Dec 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-4.dev.git235a630
- autobuilt 235a630

* Sat Dec 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-3.dev.git1f547b2
- autobuilt 1f547b2

* Fri Dec 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-2.dev.gita387c72
- bump to 0.12.2
- autobuilt a387c72

* Thu Dec 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-15.dev.git75b19ca
- autobuilt 75b19ca

* Wed Dec 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-14.dev.git320085a
- autobuilt 320085a

* Tue Dec 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-13.dev.git5f6ad82
- autobuilt 5f6ad82

* Sun Dec 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-12.dev.git41f250c
- autobuilt 41f250c

* Sat Dec 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-11.dev.git6b8f89d
- autobuilt 6b8f89d

* Thu Nov 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-10.dev.git3af62f6
- autobuilt 3af62f6

* Tue Nov 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-9.dev.git3956050
- autobuilt 3956050

* Mon Nov 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-8.dev.gite3ece3b
- autobuilt e3ece3b

* Sat Nov 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-7.dev.git78604c3
- autobuilt 78604c3

* Thu Nov 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-6.dev.git1fdfeb8
- autobuilt 1fdfeb8

* Wed Nov 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-5.dev.git23feb0d
- autobuilt 23feb0d

* Tue Nov 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-4.dev.gitea928f2
- autobuilt ea928f2

* Sat Nov 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-3.dev.gitcd5742f
- autobuilt cd5742f

* Fri Nov 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-2.dev.git236408b
- autobuilt 236408b

* Wed Nov 14 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:0.11.2-1.dev.git97bded4
- bump epoch cause previous version was messed up
- built 97bded4

* Tue Nov 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.11.20.11.2-1.dev.git79657161
- bump to 0.11.2
- autobuilt 7965716

* Sat Nov 10 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.11.20.11.2-2.dev.git78e6d8e1
- Remove dirty flag from podman version


* Sat Nov 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.11.20.11.2-1.dev.git7965716.dev.git78e6d8e1
- bump to 0.11.2
- autobuilt 78e6d8e

* Fri Nov 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.11.20.11.2-1.dev.git7965716.dev.git78e6d8e.dev.gitf5473c61
- bump to 0.11.2
- autobuilt f5473c6

* Thu Nov 08 2018 baude <bbaude@redhat.com> - 1:0.11.1-1.dev.gita4adfe5
- Upstream 0.11.1-1

* Thu Nov 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.10.2-3.dev.git672f572
- autobuilt 672f572

* Wed Nov 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.10.2-2.dev.gite9f8aed
- autobuilt e9f8aed

* Sun Oct 28 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.10.2-1.dev.git4955572
- Resolves: #1643744 - build podman with ostree support
- bump to v0.10.2
- built commit 4955572

* Fri Oct 19 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.10.1.3-3.dev.gitdb08685
- consistent epoch:version-release in changelog

* Thu Oct 18 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.10.1.3-2.dev.gitdb08685
- correct epoch mentions

* Thu Oct 18 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.10.1.3-1.dev.gitdb08685
- bump to v0.10.1.3

* Thu Oct 11 2018 baude <bbaude@redhat.com> - 1:0.10.1-1.gitda5c894
- Upstream v0.10.1 release

* Fri Sep 28 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.4-3.dev.gite7e81e6
- built libpod commit e7e81e6
- built conmon from cri-o commit 2cbe48b

* Tue Sep 25 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.9.4-2.dev.gitaf791f3
- Fix required version of runc

* Mon Sep 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.4-1.dev.gitaf791f3
- bump to v0.9.4
- built af791f3

* Wed Sep 19 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.3-2.dev.gitc3a0874
- autobuilt c3a0874

* Mon Sep 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.3-1.dev.git28a2bf8
- bump to v0.9.3
- built commit 28a2bf82

* Tue Sep 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.1.1-1.dev.git95dbcad
- bump to v0.9.1.1
- built commit 95dbcad

* Tue Sep 11 2018 baude <bbaude@redhat.com> - 1:0.9.1-1.dev.git123de30
- Upstream release of 0.9.1
- Do not build with devicemapper

* Tue Sep 4 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.5-5.git65c31d4
- Fix required version of runc

* Tue Sep 4 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.5-4.dev.git65c31d4
- Fix rpm -qi podman to show the correct URL

* Tue Sep 4 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.5-3.dev.git65c31d4
- Fix required version of runc

* Mon Sep 3 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.5-2.dev.git65c31d4
- Add a specific version of runc or later to require

* Thu Aug 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.8.5-1.dev.git65c31d4
- bump to v0.8.5-dev
- built commit 65c31d4
- correct min dep on containernetworking-plugins for upgrade from
containernetworking-cni

* Mon Aug 20 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.8.3-4.dev.git3d55721f
- Resolves: #1619411 - python3-podman should require python3-psutil
- podman-docker should conflict with moby-engine
- require nftables
- recommend slirp4netns and fuse-overlayfs (latter only for kernel >= 4.18)

* Sun Aug 12 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.3-3.dev.git3d55721f
- Add podman-docker support
- Force cgroupfs for non root podman

* Sun Aug 12 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.8.3-2.dev.git3d55721f
- Requires: conmon
- use default %%gobuild

* Sat Aug 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.8.3-1.dev.git3d55721f
- bump to v0.8.3-dev
- built commit 3d55721f
- bump Epoch to 1, cause my autobuilder messed up earlier

* Wed Aug 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.10.8.1-1.dev.git1a439f91
- bump to 0.8.1
- autobuilt 1a439f9

* Tue Jul 31 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.10.8.1-1.dev.git1a439f9.dev.git5a4e5901
- bump to 0.8.1
- autobuilt 5a4e590

* Sun Jul 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.10.8.1-1.dev.git1a439f9.dev.git5a4e590.dev.git433cbd51
- bump to 0.8.1
- autobuilt 433cbd5

* Sat Jul 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.10.8.1-1.dev.git1a439f9.dev.git5a4e590.dev.git433cbd5.dev.git87d8edb1
- bump to 0.8.1
- autobuilt 87d8edb

* Fri Jul 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.4-7.dev.git3dd577e
- fix python package version

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.4-6.dev.git3dd577e
- Rebuild for new binutils

* Fri Jul 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.4-5.dev.git3dd577e
- autobuilt 3dd577e

* Thu Jul 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.4-4.dev.git9c806a4
- autobuilt 9c806a4

* Wed Jul 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.4-3.dev.gitc90b740
- autobuilt c90b740

* Tue Jul 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.4-2.dev.git9a18681
- pypodman package exists only if varlink

* Mon Jul 23 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.4-1.dev.git9a18681
- bump to v0.7.4-dev
- built commit 9a18681

* Mon Jul 23 2018 Dan Walsh <dwalsh@redhat.com> - 0.7.3-2.dev.git06c546e
- Add Reccommeds container-selinux

* Sun Jul 15 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.3-1.dev.git06c546e
- built commit 06c546e

* Sat Jul 14 2018 Dan Walsh <dwalsh@redhat.com> - 0.7.2-10.dev.git86154b6
- Add install of pypodman

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-9.dev.git86154b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-8.dev.git86154b6
- autobuilt 86154b6

* Wed Jul 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-7.dev.git84cfdb2
- autobuilt 84cfdb2

* Tue Jul 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-6.dev.git4f9b1ae
- autobuilt 4f9b1ae

* Mon Jul 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-5.gitc7424b6
- autobuilt c7424b6

* Mon Jul 09 2018 Dan Walsh <dwalsh@redhat.com> - 0.7.2-4.gitf661e1d
- Add ostree support

* Mon Jul 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-3.gitf661e1d
- autobuilt f661e1d

* Sun Jul 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-2.git0660108
- autobuilt 0660108

* Sat Jul 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-1.gitca6ffbc
- bump to 0.7.2
- autobuilt ca6ffbc

* Fri Jul 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-6.git99959e5
- autobuilt 99959e5

* Thu Jul 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-5.gitf2462ca
- autobuilt f2462ca

* Wed Jul 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-4.git6d8fac8
- autobuilt 6d8fac8

* Tue Jul 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-3.git767b3dd
- autobuilt 767b3dd

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-2.gitb96be3a
- Rebuilt for Python 3.7

* Sat Jun 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-1.gitb96be3a
- bump to 0.7.1
- autobuilt b96be3a

* Fri Jun 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-6.gitd61d8a3
- autobuilt d61d8a3

* Thu Jun 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-5.gitfd12c89
- autobuilt fd12c89

* Wed Jun 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-4.git56133f7
- autobuilt 56133f7

* Tue Jun 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-3.git208b9a6
- autobuilt 208b9a6

* Mon Jun 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-2.gite89bbd6
- autobuilt e89bbd6

* Sat Jun 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-1.git7182339
- bump to 0.6.5
- autobuilt 7182339

* Fri Jun 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-7.git4bd0f22
- autobuilt 4bd0f22

* Thu Jun 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-6.git6804fde
- autobuilt 6804fde

* Wed Jun 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-5.gitf228cf7
- autobuilt f228cf7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-4.git5645789
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-3.git5645789
- autobuilt 5645789

* Mon Jun 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-2.git9e13457
- autobuilt 9e13457

* Sat Jun 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-1.gitb43677c
- bump to 0.6.4
- autobuilt b43677c

* Fri Jun 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-6.git6bdf023
- autobuilt 6bdf023

* Thu Jun 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-5.git65033b5
- autobuilt 65033b5

* Wed Jun 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-4.git95ea3d4
- autobuilt 95ea3d4

* Tue Jun 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-3.gitab72130
- autobuilt ab72130

* Mon Jun 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-2.git1e9e530
- autobuilt 1e9e530

* Sat Jun 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-1.gitb78e7e4
- bump to 0.6.3
- autobuilt b78e7e4

* Fri Jun 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-7.git1cbce85
- autobuilt 1cbce85

* Thu Jun 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-6.gitb1ebad9
- autobuilt b1ebad9

* Wed Jun 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-5.git7b2b2bc
- autobuilt 7b2b2bc

* Tue Jun 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-4.git14cf6d2
- autobuilt 14cf6d2

* Mon Jun 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-3.gitcae49fc
- autobuilt cae49fc

* Sun Jun 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-2.git13f7450
- autobuilt 13f7450

* Sat Jun 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-1.git22e6f11
- bump to 0.6.2
- autobuilt 22e6f11

* Fri Jun 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-4.gita9e9fd4
- autobuilt a9e9fd4

* Thu May 31 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-3.gita127b4f
- autobuilt a127b4f

* Wed May 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-2.git8ee0f2b
- autobuilt 8ee0f2b

* Sat May 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-1.git44d1c1c
- bump to 0.6.1
- autobuilt 44d1c1c

* Fri May 18 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-7.gitc54b423
- make python3-podman the same version as the main package
- build python3-podman only for fedora >= 28

* Fri May 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-6.gitc54b423
- autobuilt c54b423

* Wed May 16 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-5.git624660c
- built commit 624660c
- New subapackage: python3-podman

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-4.git9fcc475
- autobuilt 9fcc475

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-3.git0613844
- autobuilt 0613844

* Tue May 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-2.git45838b9
- autobuilt 45838b9

* Fri May 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-1.git07253fc
- bump to v0.5.3
- built commit 07253fc

* Fri May 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-5.gitcc1bad8
- autobuilt cc1bad8

* Wed May 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-4.git2526355
- autobuilt 2526355

* Tue May 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-3.gitfaa8c3e
- autobuilt faa8c3e

* Sun May 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-2.gitfa4705c
- autobuilt fa4705c

* Sat May 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-1.gitbb0e754
- bump to 0.5.2
- autobuilt bb0e754

* Fri May 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-5.git5ae940a
- autobuilt 5ae940a

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-4.git64dc803
- autobuilt commit 64dc803

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-3.git970eaf0
- autobuilt commit 970eaf0

* Tue May 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-2.git7a0a855
- autobuilt commit 7a0a855

* Sun Apr 29 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.1-1.giteda0fd7
- reflect version number correctly
- my builder script error ended up picking the wrong version number previously

* Sun Apr 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-5.giteda0fd7
- autobuilt commit eda0fd7

* Sat Apr 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-4.git6774425
- autobuilt commit 6774425

* Fri Apr 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-3.git39a7a77
- autobuilt commit 39a7a77

* Thu Apr 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-2.git58cb8f7
- autobuilt commit 58cb8f7

* Wed Apr 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de
- bump to 0.4.2
- autobuilt commit bef93de

* Tue Apr 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.4-1.git398133e
- use correct version number

* Tue Apr 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-22.git398133e
- autobuilt commit 398133e

* Sun Apr 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-21.gitcf1d884
- autobuilt commit cf1d884

* Fri Apr 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-20.git9b457e3
- autobuilt commit 9b457e3

* Fri Apr 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de9.git228732d
- autobuilt commit 228732d

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de8.gitf2658ec
- autobuilt commit f2658ec

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de7.git6a9dbf3
- autobuilt commit 6a9dbf3

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de6.git96d1162
- autobuilt commit 96d1162

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de5.git96d1162
- autobuilt commit 96d1162

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de4.git6c5ebb0
- autobuilt commit 6c5ebb0

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de3.gitfa8442e
- autobuilt commit fa8442e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de2.gitfa8442e
- autobuilt commit fa8442e

* Sun Apr 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de1.gitfa8442e
- autobuilt commit fa8442e

* Sat Apr 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de0.git62b59df
- autobuilt commit 62b59df

* Fri Apr 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-9.git191da31
- autobuilt commit 191da31

* Thu Apr 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-8.git6f51a5b
- autobuilt commit 6f51a5b

* Wed Apr 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-7.git77a1665
- autobuilt commit 77a1665

* Tue Apr 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-6.git864b9c0
- autobuilt commit 864b9c0

* Tue Apr 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-5.git864b9c0
- autobuilt commit 864b9c0

* Tue Apr 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-4.git998fd2e
- autobuilt commit 998fd2e

* Sun Apr 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-3.git998fd2e
- autobuilt commit 998fd2e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.2-2.git998fd2e
- autobuilt commit 998fd2e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.2-1.gitbef93de.git998fd2e
- bump to 0.4.2
- autobuilt commit 998fd2e

* Thu Mar 29 2018 baude <bbaude@redhat.com> - 0.3.5-2.gitdb6bf9e3
- Upstream release 0.3.5

* Tue Mar 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.5-1.git304bf53
- built commit 304bf53

* Fri Mar 23 2018 baude <bbaude@redhat.com> - 0.3.4-1.git57b403e
- Upstream release 0.3.4

* Fri Mar 16 2018 baude <bbaude@redhat.com> - 0.3.3-2.dev.gitbc358eb
- Upstream release 0.3.3

* Wed Mar 14 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.3-1.dev.gitbc358eb
- built podman commit bc358eb
- built conmon from cri-o commit 712f3b8

* Fri Mar 09 2018 baude <bbaude@redhat.com> - 0.3.2-1.gitf79a39a
- Release 0.3.2-1

* Sun Mar 04 2018 baude <bbaude@redhat.com> - 0.3.1-2.git98b95ff
- Correct RPM version

* Fri Mar 02 2018 baude <bbaude@redhat.com> - 0.3.1-1-gitc187538
- Release 0.3.1-1

* Sun Feb 25 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.2-2.git525e3b1
- Build on ARMv7 too (Fedora supports containers on that arch too)

* Fri Feb 23 2018 baude <bbaude@redhat.com> - 0.2.2-1.git525e3b1
- Release 0.2.2

* Fri Feb 16 2018 baude <bbaude@redhat.com> - 0.2.1-1.git3d0100b
- Release 0.2.1

* Wed Feb 14 2018 baude <bbaude@redhat.com> - 0.2-3.git3d0100b
- Add dep for atomic-registries

* Tue Feb 13 2018 baude <bbaude@redhat.com> - 0.2-2.git3d0100b
- Add more 64bit arches
- Add containernetworking-cni dependancy
- Add iptables dependancy

* Mon Feb 12 2018 baude <bbaude@redhat.com> - 0-2.1.git3d0100
- Release 0.2

* Tue Feb 06 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.3.git367213a
- Resolves: #1541554 - first official build
- built commit 367213a

* Fri Feb 02 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.2.git0387f69
- built commit 0387f69

* Wed Jan 10 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 0-0.1.gitc1b2278
- First package for Fedora
