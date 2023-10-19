#
# spec file for package libcontainers-common
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

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

# commonver - version from containers/common
%define commonver 0.44.0
# podman - version from containers/podman
%define podmanver 3.3.1
# storagever - version from containers/storage
%define storagever 1.36.0
# imagever - version from containers/image
%define imagever 5.16.0
Summary:        Configuration files common to github.com/containers
Name:           libcontainers-common
Version:        20210626
Release:        2%{?dist}
License:        ASL 2.0 AND GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Management
URL:            https://github.com/containers
#Source0:       https://github.com/containers/image/archive/refs/tags/v5.16.0.tar.gz
Source0:        %{name}-image-%{imagever}.tar.gz
#Source1:       https://github.com/containers/storage/archive/refs/tags/v1.36.0.tar.gz
Source1:        %{name}-storage-%{storagever}.tar.gz
Source2:        LICENSE
Source3:        policy.json
Source4:        storage.conf
Source5:        mounts.conf
Source6:        registries.conf
#Source7:       https://github.com/containers/podman/archive/refs/tags/v3.3.1.tar.gz
Source7:        %{name}-podman-%{podmanver}.tar.gz
Source8:        default.yaml
#Source9:       https://github.com/containers/common/archive/refs/tags/v0.44.0.tar.gz
Source9:        %{name}-common-%{commonver}.tar.gz
Source10:       containers.conf
BuildRequires:  go-go-md2man
Requires(post): grep
Requires(post): util-linux
Provides:       libcontainers-image = %{version}-%{release}
Provides:       libcontainers-storage = %{version}-%{release}
BuildArch:      noarch

%description
Configuration files and manpages shared by tools that are based on the
github.com/containers libraries, such as Buildah, CRI-O, Podman and Skopeo.

%prep
%setup -q -T -D -b 0 -n image-%{imagever}
%setup -q -T -D -b 1 -n storage-%{storagever}
%setup -q -T -D -b 7 -n podman-%{podmanver}
%setup -q -T -D -b 9 -n common-%{commonver}
# copy the LICENSE file in the build root
cd ..
cp %{SOURCE2} .

%build
cd ..
pwd
# compile containers/image manpages
cd image-%{imagever}
for md in docs/*.md
do
	go-md2man -in $md -out $md
done
rename '.5.md' '.5' docs/*
rename '.md' '.1' docs/*
cd ..
# compile containers/storage manpages
cd storage-%{storagever}
for md in docs/*.md
do
	go-md2man -in $md -out $md
done
rename '.5.md' '.5' docs/*
rename '.md' '.1' docs/*
cd ..
# compile subset of containers/podman manpages
cd podman-%{podmanver}
go-md2man -in pkg/hooks/docs/oci-hooks.5.md -out pkg/hooks/docs/oci-hooks.5
cd ..

cd common-%{commonver}
make docs
cd ..

%install
cd ..
install -d -m 0755 %{buildroot}/%{_sysconfdir}/containers
install -d -m 0755 %{buildroot}/%{_sysconfdir}/containers/oci/hooks.d
install -d -m 0755 %{buildroot}/%{_datadir}/containers/oci/hooks.d
install -d -m 0755 %{buildroot}/%{_sysconfdir}/containers/registries.d

install -D -m 0644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/containers/policy.json
install -D -m 0644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/containers/storage.conf
install -D -m 0644 %{SOURCE5} %{buildroot}/%{_datadir}/containers/mounts.conf
install -D -m 0644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/containers/mounts.conf
install -D -m 0644 %{SOURCE6} %{buildroot}/%{_sysconfdir}/containers/registries.conf
install -D -m 0644 %{SOURCE8} %{buildroot}/%{_sysconfdir}/containers/registries.d/default.yaml
sed -e 's-@LIBEXECDIR@-%{_libexecdir}-g' -i %{SOURCE10}
install -D -m 0644 %{SOURCE10} %{buildroot}/%{_datadir}/containers/containers.conf
install -D -m 0644 common-%{commonver}/pkg/seccomp/seccomp.json %{buildroot}/%{_datadir}/containers/seccomp.json
install -D -m 0644 common-%{commonver}/pkg/seccomp/seccomp.json %{buildroot}/%{_sysconfdir}/containers/seccomp.json

install -d %{buildroot}/%{_mandir}/man1
install -d %{buildroot}/%{_mandir}/man5
install -D -m 0644 image-%{imagever}/docs/*.1 %{buildroot}/%{_mandir}/man1/
install -D -m 0644 image-%{imagever}/docs/*.5 %{buildroot}/%{_mandir}/man5/
install -D -m 0644 storage-%{storagever}/docs/*.1 %{buildroot}/%{_mandir}/man1/
install -D -m 0644 storage-%{storagever}/docs/*.5 %{buildroot}/%{_mandir}/man5/
install -D -m 0644 common-%{commonver}/docs/containers-mounts.conf.5 %{buildroot}/%{_mandir}/man5/
install -D -m 0644 common-%{commonver}/docs/containers.conf.5 %{buildroot}/%{_mandir}/man5/

%post
# If installing, check if /var/lib/containers (or /var/lib in its defect) is btrfs and set driver
# to "btrfs" if true
if [ $1 -eq 1 ] ; then
  fstype=$((findmnt -o FSTYPE -l --target %{_sharedstatedir}/containers || findmnt -o FSTYPE -l --target %{_var}/lib) | grep -v FSTYPE)
  if [ "$fstype" = "btrfs" ]; then
    sed -i 's/driver = ""/driver = "btrfs"/g' %{_sysconfdir}/containers/storage.conf
  fi
fi

%files
%dir %{_sysconfdir}/containers
%dir %{_sysconfdir}/containers/oci
%dir %{_sysconfdir}/containers/oci/hooks.d
%dir %{_sysconfdir}/containers/registries.d
%dir %{_datadir}/containers
%dir %{_datadir}/containers/oci
%dir %{_datadir}/containers/oci/hooks.d

%config(noreplace) %{_sysconfdir}/containers/policy.json
%config(noreplace) %{_sysconfdir}/containers/storage.conf
%config(noreplace) %{_sysconfdir}/containers/mounts.conf
%{_datadir}/containers/mounts.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf
%config(noreplace) %{_sysconfdir}/containers/seccomp.json
%config(noreplace) %{_sysconfdir}/containers/registries.d/default.yaml
%{_datadir}/containers/seccomp.json
%{_datadir}/containers/containers.conf

%{_mandir}/man1/*.1.*
%{_mandir}/man5/*.5.*
%license LICENSE

%changelog
* Thu Oct 19 2023 Dan Streetman <ddstreet@ieee.org> - 20210626-2
- Bump release to rebuild with updated version of Go.

* Fri Jul 22 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 20210626-1
- Upgrade version to 20210626 and License information.
- Remove oci-hook man5 tar conflicting with podman package.
- Updated conf files with latest version.

* Thu Aug 19 2021 Henry Li <lihl@microsoft.com> - 20200727-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag)
- License Verified
- Remove {?ext_man}, which is not supported in CBL-Mariner

* Mon Aug  3 2020 Callum Farmer <callumjfarmer13@gmail.com>
- Fixes for %%_libexecdir changing to /usr/libexec (bsc#1174075)

* Tue Jul 28 2020 Ralf Haferkamp <rhafer@suse.com>
- Added containers/common tarball for containers.conf(5) man page
- Install containers.conf default configuration in
  /usr/share/containers
- libpod repository on github got renamed to podman
- Update to image 5.5.1
  - Add documentation for credHelpera
  - Add defaults for using the rootless policy path
- Update libpod/podman to 2.0.3
  - docs: user namespace can't be shared in pods
  - Switch references from libpod.conf to containers.conf
  - Allow empty host port in --publish flag
  - update document login see config.json as valid
- Update storage to 1.20.2
  - Add back skip_mount_home

* Fri Jun 19 2020 Ralf Haferkamp <rhafer@suse.com>
- Remove remaining difference between SLE and openSUSE package and
  ship the some mounts.conf default configuration on both platforms.
  As the sources for the mount point do not exist on openSUSE by
  default this config will basically have no effect on openSUSE.
  (jsc#SLE-12122, bsc#1175821)

* Wed Jun  3 2020 Ralf Haferkamp <rhafer@suse.com>
- Update to image 5.4.4
  - Remove registries.conf VERSION 2 references from man page
  - Intial authfile man page
  - Add $HOME/.config/containers/certs.d to perHostCertDirPath
  - Add $HOME/.config/containers/registries.conf to config path
  - registries.conf.d: add stances for the registries.conf
- update to libpod 1.9.3
  - userns: support --userns=auto
  - Switch to using --time as opposed to --timeout to better match Docker
  - Add support for specifying CNI networks in podman play kube
  - man pages: fix inconsistencies
- Update to storage 1.19.1
  - userns: add support for auto
  - store: change the default user to containers
  - config: honor XDG_CONFIG_HOME
- Remove the /var/lib/ca-certificates/pem/SUSE.pem workaround again.
  It never ended up in SLES and a different way to fix the underlying
  problem is being worked on.

* Wed May 13 2020 Richard Brown <rbrown@suse.com>
- Add registry.opensuse.org as default registry [bsc#1171578]

* Fri Apr 24 2020 Ralf Haferkamp <rhafer@suse.com>
- Add /var/lib/ca-certificates/pem/SUSE.pem to the SLES mounts.
  This for making container-suseconnect working in the public
  cloud on-demand images. It needs that file for being able to
  verify the server certificates of the RMT servers hosted
  in the public cloud.
  (https://github.com/SUSE/container-suseconnect/issues/41)

* Fri Mar  6 2020 Ralf Haferkamp <rhafer@suse.com>
- New snaphot (bsc#1165917)
- Update to image 5.2.1
  * Add documentation about rewriting docker.io registries
  * Add registries warning to registries.conf
- Update to libpod 1.8.0
  * Fixed some spelling errors in oci-hooks documentations
  * include containers-mounts.conf(5) man-page into the package
- Update to storage 1.16.1
  * Add `rootless_storage_path` directive to storage.conf
  * Add better documentation for the mount_program in overlay driver

* Wed Dec 11 2019 Richard Brown <rbrown@suse.com>
- Update to image 5.0.0
  - Clean up various imports primarily so that imports of packages that aren't in the standard library are all in one section.
  - Update to major version v5
  - return resp error message
  - copy.Image(): select the CopySystemImage image using the source context
  - Add manifest list support
  - docker: handle http 429 status codes
  - allow for .dockercfg files to reside in non-home directories
  - Use the correct module path in (make test-skopeo)
- Update to libpod 1.6.3
  - Handling of the libpod.conf configuration file has seen major changes. Most significantly, rootless users will no longer automatically receive a complete configuration file when they first use Podman, and will instead only receive differences from the global configuration.
  - Initial support for the CNI DNS plugin, which allows containers to resolve the IPs of other containers via DNS name, has been added
  - Podman now supports anonymous named volumes, created by specifying only a destination to the -v flag to the podman create and podman run commands
  - Named volumes now support uid and gid options in --opt o=... to set UID and GID of the created volume
- Update to storage 1.15.3
  - overlay: allow storing images with more than 127 layers
  - Lazy initialize the layer store
  - tarlogger: drop state mutex

* Wed Oct  2 2019 Sascha Grunert <sgrunert@suse.com>
- Update to image 4.0.0
  - Add http response to log
  - Add tests for parsing OpenShift kubeconfig files
  - Compress: define some consts for the compression algos
  - Compression: add support for the zstd
  - Compression: allow to specify the compression format
  - Copy: add nil checks
  - Copy: compression: default to gzip
  - Copy: don't lose annotations of BlobInfo
  - Copy: fix options.DestinationCtx nil check
  - Copy: use a bigger buffer for the compression
  - Fix cross-compilation by vendoring latest c/storage
  - Internal/testing/explicitfilepath-tmpdir: handle unset TMPDIR
  - Keyctl: clean up after tests
  - Make container tools work with go+openssl
  - Make test-skopeo: replace c/image module instead of copying code
  - Media type checks
  - Move keyctl to internal & func remove auth from keyring
  - Replace vendor.conf by go.mod
  - Update dependencies
  - Update test certificates
  - Update to mergo v0.3.5
  - Vendor.conf: update reference for containers/storage
- Update to storage 1.13.4
  - Update generated files
  - ImageBigData: distinguish between no-such-image and no-such-item
  - ImageSize: don't get tripped up by images with no layers
  - tarlogger: disable raw accouting
- Update to libpod 1.6.0
  - Nothing changed regarding the OCI hooks documentation provided by this
    package

* Mon Sep 23 2019 Richard Brown <rbrown@suse.com>
- Update to image 1.4.4
  - Hard-code the kernel keyring use to be disabled for now
- Update to libpod 1.5.1
  - The hostname of pods is now set to the pod's name
  - Minor bugfixes
- Update to storage 1.12.16
  - Ignore ro mount options in btrfs and windows drivers

* Mon Sep 23 2019 Richard Brown <rbrown@suse.com>
- Check /var/lib/containers if possible before setting btrfs backend (bsc#1151028)

* Wed Aug  7 2019 Sascha Grunert <sgrunert@suse.com>
- Add missing licenses to spec file

* Tue Aug  6 2019 Marco Vedovati <mvedovati@suse.com>
- Add a default registries.d configuration file, used to specify images
  signatures storage location.

* Fri Aug  2 2019 Sascha Grunert <sgrunert@suse.com>
- Update to image v3.0.0
  - Add "Env" to ImageInspectInfo
  - Add API function TryUpdatingCache
  - Add ability to install man pages
  - Add user registry auth to kernel keyring
  - Fix policy.json.md -> containers-policy.json.5.md references
  - Fix typo in docs/containers-registries.conf.5.md
  - Remove pkg/sysregistries
  - Touch up transport man page
  - Try harder in storageImageDestination.TryReusingBlob
  - Use the same HTTP client for contacting the bearer token server and the
    registry
  - ci: change GOCACHE to a writeable path
  - config.go: improve debug message
  - config.go: log where credentials come from
  - docker client: error if registry is blocked
  - docker: allow deleting OCI images
  - docker: delete: support all MIME types
  - ostree: default is no OStree support
  - ostree: improve error message
  - progress bar: use spinners for unknown blob sizes
  - use 'containers_image_ostree' as build tag
  - use keyring when authfile empty
- Update to storage v1.12.16
  - Add cirrus vendor check
  - Add storage options to IgnoreChownErrors
  - Add support for UID as well as UserName in /etc/subuid files.
  - Add support for ignoreChownErrors to vfs
  - Add support for installing man pages
  - Fix cross-compilation
  - Keep track of the UIDs and GIDs used in applied layers
  - Move lockfiles to their own package
  - Remove merged directory when it is unmounted
  - Switch to go modules
  - Switch to golangci-lint
  - Update generated files
  - Use same variable name on both commands
  - cirrus: ubuntu: try removing cryptsetup-initramfs
  - compression: add support for the zstd algorithm
  - getLockfile(): use the absolute path
  - loadMounts(): reset counts before merging just-loaded data
  - lockfile: don't bother releasing a lock when closing a file
  - locking test updates
  - locking: take read locks on read-only stores
  - make local-cross more reliable for CI
  - overlay: cache the results of supported/using-metacopy/use-naive-diff
    feature tests
  - overlay: fix small piece of repeated work
  - utils: fix check for missing conf file
  - zstd: use github.com/klauspost/compress directly

* Mon Jul  8 2019 Sascha Grunert <sgrunert@suse.com>
- Update to libpod v1.4.4
  - Fixed a bug where rootless Podman would attempt to use the
    entire root configuration if no rootless configuration was
    present for the user, breaking rootless Podman for new
    installations
  - Fixed a bug where rootless Podman's pause process would block
    SIGTERM, preventing graceful system shutdown and hanging until
    the system's init send SIGKILL
  - Fixed a bug where running Podman as root with sudo -E would not
    work after running rootless Podman at least once
  - Fixed a bug where options for tmpfs volumes added with the
  - -tmpfs flag were being ignored
  - Fixed a bug where images with no layers could not properly be
    displayed and removed by Podman
  - Fixed a bug where locks were not properly freed on failure to
    create a container or pod
  - Podman now has greatly improved support for containers using
    multiple OCI runtimes. Containers now remember if they were
    created with a different runtime using --runtime and will
    always use that runtime
  - The cached and delegated options for volume mounts are now
    allowed for Docker compatability (#3340)
  - The podman diff command now supports the --latest flag
  - Fixed a bug where podman cp on a single file would create a
    directory at the target and place the file in it (#3384)
  - Fixed a bug where podman inspect --format '{{.Mounts}}' would
    print a hexadecimal address instead of a container's mounts
  - Fixed a bug where rootless Podman would not add an entry to
    container's /etc/hosts files for their own hostname (#3405)
  - Fixed a bug where podman ps --sync would segfault (#3411)
  - Fixed a bug where podman generate kube would produce an invalid
    ports configuration (#3408)
  - Podman now performs much better on systems with heavy I/O load
  - The --cgroup-manager flag to podman now shows the correct
    default setting in help if the default was overridden by
    libpod.conf
  - For backwards compatability, setting --log-driver=json-file in
    podman run is now supported as an alias for
  - -log-driver=k8s-file. This is considered deprecated, and
    json-file will be moved to a new implementation in the future
    ([#3363](https://github.com/containers/libpod/issues/3363))
  - Podman's default libpod.conf file now allows the crun OCI
    runtime to be used if it is installed
  - Fixed a bug where Podman could not run containers using an
    older version of Systemd as init (#3295)
  - Updated vendored Buildah to v1.9.0 to resolve a critical bug
    with Dockerfile RUN instructions
  - The error message for running podman kill on containers that
    are not running has been improved
  - The Podman remote client can now log to a file if syslog is not
    available
  - The MacOS dmg file is experimental, use at your own risk.
  - The podman exec command now sets its error code differently
    based on whether the container does not exist, and the command
    in the container does not exist
  - The podman inspect command on containers now outputs Mounts
    JSON that matches that of docker inspect, only including
    user-specified volumes and differentiating bind mounts and
    named volumes
  - The podman inspect command now reports the path to a
    container's OCI spec with the OCIConfigPath key (only included
    when the container is initialized or running)
  - The podman run --mount command now supports the
    bind-nonrecursive option for bind mounts (#3314)
  - Fixed a bug where podman play kube would fail to create
    containers due to an unspecified log driver
  - Fixed a bug where Podman would fail to build with musl libc
    (#3284)
  - Fixed a bug where rootless Podman using slirp4netns networking
    in an environment with no nameservers on the host other than
    localhost would result in nonfunctional networking (#3277)
  - Fixed a bug where podman import would not properly set
    environment variables, discarding their values and retaining
    only keys
  - Fixed a bug where Podman would fail to run when built with
    Apparmor support but run on systems without the Apparmor kernel
    module loaded (#3331)
  - Remote Podman will now default the username it uses to log in
    to remote systems to the username of the current user
  - Podman now uses JSON logging with OCI runtimes that support it,
    allowing for better error reporting
  - Updated vendored Buildah to v1.8.4
  - Updated vendored containers/image to v2.0
- Update to image v2.0.0
  - Add registry mirror support
  - Include missing man pages (bsc#1139526)
- Update to storage v1.12.10
  - Add support for UID as well as UserName in /etc/subuid files.
  - utils: fix check for missing conf file
  - compression: add support for the zstd algorithm
  - overlay: cache the results of
    supported/using-metacopy/use-naive-diff feature tests

* Tue Jun 11 2019 Sascha Grunert <sgrunert@suse.com>
- Update to libpod v1.4.0
  - The podman checkpoint and podman restore commands can now be
    used to migrate containers between Podman installations on
    different systems
  - The podman cp command now supports a pause flag to pause
    containers while copying into them
  - The remote client now supports a configuration file for
    pre-configuring connections to remote Podman installations
  - Fixed CVE-2019-10152 - The podman cp command improperly
    dereferenced symlinks in host context
  - Fixed a bug where podman commit could improperly set
    environment variables that contained = characters
  - Fixed a bug where rootless Podman would sometimes fail to start
    containers with forwarded ports
  - Fixed a bug where podman version on the remote client could
    segfault
  - Fixed a bug where podman container runlabel would use
    /proc/self/exe instead of the path of the Podman command when
    printing the command being executed
  - Fixed a bug where filtering images by label did not work
  - Fixed a bug where specifying a bing mount or tmpfs mount over
    an image volume would cause a container to be unable to start
  - Fixed a bug where podman generate kube did not work with
    containers with named volumes
  - Fixed a bug where rootless Podman would receive permission
    denied errors accessing conmon.pid
  - Fixed a bug where podman cp with a folder specified as target
    would replace the folder, as opposed to copying into it
  - Fixed a bug where rootless Podman commands could double-unlock
    a lock, causing a crash
  - Fixed a bug where Podman incorrectly set tmpcopyup on /dev/
    mounts, causing errors when using the Kata containers runtime
  - Fixed a bug where podman exec would fail on older kernels
  - The podman commit command is now usable with the Podman remote
    client
  - The --signature-policy flag (used with several image-related
    commands) has been deprecated
  - The podman unshare command now defines two environment
    variables in the spawned shell: CONTAINERS_RUNROOT and
    CONTAINERS_GRAPHROOT, pointing to temporary and permanent
    storage for rootless containers
  - Updated vendored containers/storage and containers/image
    libraries with numerous bugfixes
  - Updated vendored Buildah to v1.8.3
  - Podman now requires Conmon v0.2.0
  - The podman cp command is now aliased as podman container cp
  - Rootless Podman will now default init_path using root Podman's
    configuration files (/etc/containers/libpod.conf and
    /usr/share/containers/libpod.conf) if not overridden in the
    rootless configuration
- Update to image v1.5.1
  - Vendor in latest containers/storage
  - docker/docker_client: Drop redundant Domain(ref.ref) call
  - pkg/blobinfocache: Split implementations into subpackages
  - copy: progress bar: show messages on completion
  - docs: rename manpages to *.5.command
  - add container-certs.d.md manpage
  - pkg/docker/config: Bring auth tests from
    docker/docker_client_test
  - Don't allocate a sync.Mutex separately
- Update to storage v1.12.10
  - Add function to parse out mount options from graphdriver
  - Merge the disparate parts of all of the Unix-like lockfiles
  - Fix unix-but-not-Linux compilation
  - Return XDG_RUNTIME_DIR as RootlessRuntimeDir if set
  - Cherry-pick moby/moby #39292 for CVE-2018-15664 fixes
  - lockfile: add RecursiveLock() API
  - Update generated files
  - Fix crash on tesing of aufs code
  - Let consumers know when Layers and Images came from read-only stores
  - chown: do not change owner for the mountpoint
  - locks: correctly mark updates to the layers list
  - CreateContainer: don't worry about mapping layers unless necessary
  - docs: fix manpage for containers-storage.conf
  - docs: sort configuration options alphabetically
  - docs: document OSTree file deduplication
  - Add missing options to man page for containers-storage
  - overlay: use the layer idmapping if present
  - vfs: prefer layer custom idmappings
  - layers: propagate down the idmapping settings
  - Recreate symlink when not found
  - docs: fix manpage for configuration file
  - docs: add special handling for manpages in sect 5
  - overlay: fix single-lower test
  - Recreate symlink when not found
  - overlay: propagate errors from mountProgram
  - utils: root in a userns uses global conf file
  - Fix handling of additional stores
  - Correctly check permissions on rootless directory
  - Fix possible integer overflow on 32bit builds
  - Evaluate device path for lvm
  - lockfile test: make concurrent RW test determinisitc
  - lockfile test: make concurrent read tests deterministic
  - drivers.DirCopy: fix filemode detection
  - storage: move the logic to detect rootless into utils.go
  - Don't set (struct flock).l_pid
  - Improve documentation of getLockfile
  - Rename getLockFile to createLockerForPath, and document it
  - Add FILES section to containers-storage.5 man page
  - add digest locks
  - drivers/copy: add a non-cgo fallback
- Add default SLES mounts for container-suseconnect usage

* Tue Jun  4 2019 Richard Brown <rbrown@suse.com>
- Add util-linux and grep as Requires(post) to ensure btrfs config gets made correctly

* Mon Apr  1 2019 Richard Brown <rbrown@suse.com>
- Update to libpod v1.2.0
  * Rootless Podman can now be used with a single UID and GID, without requiring a full 65536 UIDs/GIDs to be allocated in /etc/subuid and /etc/subgid
  * Move pkg/util default storage functions from libpod to containers/storage
- Update to image v1.5
  * Minor behind the scene bugfixes, no user facing changes
- Update to storage v1.12.1
  * Move pkg/util default storage functions from libpod to containers/storage
  * containers/storage no longer depends on containers/image
- Version 20190401

* Wed Feb 27 2019 Richard Brown <rbrown@suse.com>
- Update to libpod v1.1.0
  * Rootless Podman can now forward ports into containers (using the same -p and -P flags as root Podman)
  * Rootless Podman will now pull some configuration options (for example, OCI runtime path) from the default root libpod.conf if they are not explicitly set in the user's own libpod.conf

* Tue Feb 19 2019 Richard Brown <rbrown@suse.com>
- Upgrade to storage v1.10
  * enable parallel blob reads
  * Teach images to hold multiple manifests
  * Move structs for storage.conf to pkg/config
- Upgrade to libpod v1.0.1
  * Do not unmarshal into c.config.Spec
  * spec: add nosuid,noexec,nodev to ro bind mount

* Sat Feb  2 2019 Richard Brown <rbrown@suse.com>
- Restore non-upstream storage.conf, needed by CRI-O

* Fri Jan 25 2019 Richard Brown <rbrown@suse.com>
- Upgrade to storage v1.8
  * Check for the OS when setting btrfs/libdm/ostree tags
- Upgrade to image v1.3
  * vendor: use github.com/klauspost/pgzip instead of compress/gzip
  * vendor latest ostree
- Refactor specfile to use versioned tarballs
- Established package versioning scheme (ISODATE of change)
- Remove non-upstream storage.conf
- Set btrfs as default driver if /var/lib is on btrfs [boo#1123119]
- Version 20190125

* Thu Jan 17 2019 Richard Brown <rbrown@suse.com>
- Upgrade to storage v1.6
  * Remove private mount from zfs driver
  * Update zfs driver to be closer to moby driver
  * Use mount options when mounting the chown layer.

* Sun Jan 13 2019 Richard Brown <rbrown@suse.com>
- Upgrade to libpod v1.0.0
  * Fixed a bug where storage.conf was sometimes ignored for rootless containers

* Tue Jan  8 2019 Richard Brown <rbrown@suse.com>
- Upgrade to libpod v0.12.1.2 and storage v1.4
  * No significant functional or packaging changes

* Sun Jan  6 2019 Richard Brown <rbrown@suse.com>
- storage.conf - restore btrfs as the default driver

* Fri Dec  7 2018 Richard Brown <rbrown@suse.com>
- Update to latest libpod and storage to support cri-o 1.13

* Wed Dec  5 2018 Richard Brown <rbrown@suse.com>
- Use seccomp.json from github.com/containers/libpod, instead of
  installing the tar.xz on users systems (boo#1118444)

* Mon Nov 12 2018 Valentin Rothberg <vrothberg@suse.com>
- Add oci-hooks(5) manpage from libpod.

* Mon Nov 12 2018 Valentin Rothberg <vrothberg@suse.com>
- Use seccomp.json from github.com/containers/libpod to align with the
  upstream defaults.
- Update to the latest image and storage to pull in improvements to the
  manpages.

* Mon Aug 27 2018 vrothberg@suse.com
- storage.conf: comment out options that are not supported by btrfs.
  This simplifies switching the driver as it avoids the whack-a-mole
  of commenting out "unsupported" options.

* Mon Aug 27 2018 vrothberg@suse.com
- Consolidate libcontainers-{common,image,storage} into one package,
  libcontainers-common. That's the way upstream intended all libraries from
  github.com/containers to be packaged. It facilitates updating and maintaining
  the package, as all configs and manpages come from a central source.
  Note that the `storage` binary that previously has been provided by the
  libcontainers-storage package is not provided anymore as, despite the claims
  in the manpages, it is not intended for production use.

* Mon Aug 13 2018 vrothberg@suse.com
- Make libcontainers-common arch independent.
- Add LICENSE.

* Thu Apr 12 2018 fcastelli@suse.com
- Added /usr/share/containers/oci/hooks.d and /etc/containers/oci/hooks.d
  to the package. These are used by tools like cri-o and podman to store
  custom hooks.

* Mon Mar  5 2018 vrothberg@suse.com
- Configuration files should generally be tagged as %%config(noreplace) in order
  to keep the modified config files and to avoid losing data when the package
  is being updated.
  feature#crio

* Thu Feb  8 2018 vrothberg@suse.com
- Add libcontainers-common package.
