%bcond_with lint
%bcond_without tests

# Modern distributions (using RPM v4.19+; for example, Fedora 39+) do not
# require the %%pre scriptlet for creating users/groups because the sysusers
# feature is now built directly into RPM.  Simply including the sysusers
# `mock.conf` file in a package payload is sufficient to leverage this feature.
# However, for older distributions that lack this capability, we still define
# the %%pre scriptlet.
%if (0%{?rhel} && 0%{?rhel} < 10) || (0%{?mageia} && 0%{?mageia} < 10) || (0%{?suse_version} && 0%{?suse_version} < 1660)
%bcond_without sysusers_compat
%else
%bcond_with sysusers_compat
%endif

%global __python %{__python3}
%global python_sitelib %{python3_sitelib}

Summary: Builds packages inside chroots
Name: mock
Version: 6.0
Release: 1%{?dist}
License: GPL-2.0-or-later
# Source is created by
# git clone https://github.com/rpm-software-management/mock.git
# cd mock
# git reset --hard %%{name}-%%{version}
# tito build --tgz
Source: https://github.com/rpm-software-management/%{name}/releases/download/%{name}-%{version}-1/%{name}-%{version}.tar.gz
URL: https://github.com/rpm-software-management/mock/
BuildArch: noarch
Requires: tar
Requires: pigz
%if 0%{?mageia}
Requires: usermode-consoleonly
%else
Requires: usermode
%endif
Requires: createrepo_c

# We know that the current version of mock isn't compatible with older variants,
# and we want to enforce automatic upgrades.
Conflicts: mock-core-configs < 33

# Requires 'mock-core-configs', or replacement (GitHub PR#544).
Requires: mock-configs
Requires: %{name}-filesystem = %{version}-%{release}
# This is still preferred package providing 'mock-configs'
Suggests: mock-core-configs

Requires: systemd
%if 0%{?fedora} || 0%{?rhel}
Requires: systemd-container
%endif
Requires: coreutils
%if 0%{?fedora}
Suggests: iproute
%endif
%if 0%{?mageia}
Suggests: iproute2
%endif
BuildRequires: bash-completion
Requires: python%{python3_pkgversion}-distro
Requires: python%{python3_pkgversion}-jinja2
Requires: python%{python3_pkgversion}-requests
Requires: python%{python3_pkgversion}-rpm
Requires: python%{python3_pkgversion}-pyroute2
Requires: python%{python3_pkgversion}-templated-dictionary >= 1.5
Requires: python%{python3_pkgversion}-backoff
BuildRequires: python%{python3_pkgversion}-backoff
BuildRequires: python%{python3_pkgversion}-devel
%if %{with lint}
BuildRequires: python%{python3_pkgversion}-pylint
%endif
BuildRequires: python%{python3_pkgversion}-rpm
BuildRequires: python%{python3_pkgversion}-rpmautospec-core

BuildRequires: argparse-manpage

%if 0%{?fedora} >= 38
# DNF5 stack
Recommends: dnf5
Recommends: dnf5-plugins
%endif

# DNF4 stack
Recommends: python3-dnf
Recommends: python3-dnf-plugins-core

# YUM stack, dnf-utils replace yum-utils
Recommends: yum
Recommends: dnf-utils

Recommends: btrfs-progs
Suggests: qemu-user-static
Suggests: procenv
Recommends: buildah
Recommends: podman
Recommends: fuse-overlayfs

%if %{with tests}
BuildRequires: python%{python3_pkgversion}-distro
BuildRequires: python%{python3_pkgversion}-jinja2
BuildRequires: python%{python3_pkgversion}-jsonschema
BuildRequires: python%{python3_pkgversion}-pyroute2
BuildRequires: python%{python3_pkgversion}-pytest
BuildRequires: python%{python3_pkgversion}-requests
BuildRequires: python%{python3_pkgversion}-templated-dictionary
%endif

%if 0%{?fedora} || 0%{?rhel}
BuildRequires: perl-interpreter
%else
BuildRequires: perl
%endif
# hwinfo plugin
Requires: util-linux
Requires: coreutils
Requires: procps-ng
Requires: shadow-utils


%description
Mock takes an SRPM and builds it in a chroot.

%package scm
Summary: Mock SCM integration module
Requires: %{name} = %{version}-%{release}
Recommends: cvs
Recommends: git
Recommends: subversion
Recommends: tar

# We could migrate to 'copr-distgit-client'
Recommends: rpkg

%description scm
Mock SCM integration module.

%package lvm
Summary: LVM plugin for mock
Requires: %{name} = %{version}-%{release}
Requires: lvm2

%description lvm
Mock plugin that enables using LVM as a backend and support creating snapshots
of the buildroot.

%package rpmautospec
Summary: Rpmautospec plugin for mock
Requires: %{name} = %{version}-%{release}
# This lets mock determine if a spec file needs to be processed with rpmautospec.
Requires: python%{python3_pkgversion}-rpmautospec-core

%description rpmautospec
Mock plugin that preprocesses spec files using rpmautospec.

%package filesystem
Summary:  Mock filesystem layout
Requires(pre):  shadow-utils
BuildRequires:  systemd-rpm-macros

%if %{with sysusers_compat}
Requires(pre): shadow-utils
%endif

%description filesystem
Filesystem layout and group for Mock.

%prep
%setup -q
for file in py/mock.py py/mock-parse-buildlog.py; do
  sed -i 1"s|#!/usr/bin/python3 |#!%{__python} |" $file
done

%build
for i in py/mockbuild/constants.py py/mock-parse-buildlog.py; do
    perl -p -i -e 's|^VERSION\s*=.*|VERSION="%{version}"|' $i
    perl -p -i -e 's|^SYSCONFDIR\s*=.*|SYSCONFDIR="%{_sysconfdir}"|' $i
    perl -p -i -e 's|^PYTHONDIR\s*=.*|PYTHONDIR="%{python_sitelib}"|' $i
    perl -p -i -e 's|^PKGPYTHONDIR\s*=.*|PKGPYTHONDIR="%{python_sitelib}/mockbuild"|' $i
done
for i in docs/mock.1 docs/mock-parse-buildlog.1; do
    perl -p -i -e 's|\@VERSION\@|%{version}"|' $i
done

./precompile-bash-completion "mock.complete"

argparse-manpage --pyfile ./py/mock-hermetic-repo.py --function _argparser > mock-hermetic-repo.1


%install
#base filesystem
mkdir -p %{buildroot}%{_sysconfdir}/mock/eol/templates
mkdir -p %{buildroot}%{_sysconfdir}/mock/templates

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libexecdir}/mock
install mockchain %{buildroot}%{_bindir}/mockchain
install py/mock-hermetic-repo.py %{buildroot}%{_bindir}/mock-hermetic-repo
install py/mock-parse-buildlog.py %{buildroot}%{_bindir}/mock-parse-buildlog
install py/mock.py %{buildroot}%{_libexecdir}/mock/mock
ln -s consolehelper %{buildroot}%{_bindir}/mock
 
install -d %{buildroot}%{_sysconfdir}/pam.d
cp -a etc/pam/* %{buildroot}%{_sysconfdir}/pam.d/

install -d %{buildroot}%{_sysconfdir}/mock
cp -a etc/mock/* %{buildroot}%{_sysconfdir}/mock/

install -d %{buildroot}%{_sysconfdir}/security/console.apps/
cp -a etc/consolehelper/mock %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

install -d %{buildroot}%{_datadir}/bash-completion/completions/
cp -a etc/bash_completion.d/* %{buildroot}%{_datadir}/bash-completion/completions/
cp -a mock.complete %{buildroot}%{_datadir}/bash-completion/completions/mock
ln -s mock %{buildroot}%{_datadir}/bash-completion/completions/mock-parse-buildlog

install -d %{buildroot}%{_sysconfdir}/pki/mock
cp -a etc/pki/* %{buildroot}%{_sysconfdir}/pki/mock/

install -d %{buildroot}%{python_sitelib}/
cp -a py/mockbuild %{buildroot}%{python_sitelib}/

install -d %{buildroot}%{_mandir}/man1
cp -a docs/mock.1 docs/mock-parse-buildlog.1 mock-hermetic-repo.1 %{buildroot}%{_mandir}/man1/
install -d %{buildroot}%{_datadir}/cheat
cp -a docs/mock.cheat %{buildroot}%{_datadir}/cheat/mock

install -d %{buildroot}/var/lib/mock
install -d %{buildroot}/var/cache/mock

mkdir -p %{buildroot}%{_pkgdocdir}
install -p -m 0644 docs/buildroot-lock-schema-*.json %{buildroot}%{_pkgdocdir}
install -p -m 0644 docs/site-defaults.cfg %{buildroot}%{_pkgdocdir}

mkdir -p %{buildroot}%{_sysusersdir}
install -p -D -m 0644 %{name}.conf %{buildroot}%{_sysusersdir}

sed -i 's/^_MOCK_NVR = None$/_MOCK_NVR = "%name-%version-%release"/' \
    %{buildroot}%{_libexecdir}/mock/mock


%if %{with sysusers_compat}
%pre filesystem
# Some of these older distributions do not ship with the %%sysusers_*_compat.
# Instead of another ifdef/else here, we prefer to hardcode the scriptlet
# content here.
getent group 'mock' >/dev/null || groupadd -f -g '135' -r 'mock' || :
%endif


%check
%if %{with lint}
# ignore the errors for now, just print them and hopefully somebody will fix it one day
pylint-3 py/mockbuild/ py/*.py py/mockbuild/plugins/* || :
%endif

%if %{with tests}
./run-tests.sh --no-cov
%endif


%files
%defattr(0644, root, mock)
%dir %{_pkgdocdir}/
%doc %{_pkgdocdir}/site-defaults.cfg
%doc %{_pkgdocdir}/buildroot-lock-schema-*.json
%{_datadir}/bash-completion/completions/mock
%{_datadir}/bash-completion/completions/mock-parse-buildlog

%defattr(-, root, root)

# executables
%{_bindir}/mock
%{_bindir}/mockchain
%{_bindir}/mock-hermetic-repo
%{_bindir}/mock-parse-buildlog
%{_libexecdir}/mock

# python stuff
%{python_sitelib}/*
%exclude %{python_sitelib}/mockbuild/scm.*
%exclude %{python_sitelib}/mockbuild/__pycache__/scm.*
%exclude %{python_sitelib}/mockbuild/plugins/lvm_root.*
%exclude %{python_sitelib}/mockbuild/plugins/__pycache__/lvm_root.*
%exclude %{python_sitelib}/mockbuild/plugins/rpmautospec.*
%exclude %{python3_sitelib}/mockbuild/plugins/__pycache__/rpmautospec.*.py*

# config files
%config(noreplace) %{_sysconfdir}/%{name}/*.ini
%config(noreplace) %{_sysconfdir}/%{name}/hermetic-build.cfg
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}

# directory for personal gpg keys
%dir %{_sysconfdir}/pki/mock
%config(noreplace) %{_sysconfdir}/pki/mock/*

# docs
%{_mandir}/man1/mock.1*
%{_mandir}/man1/mock-parse-buildlog.1*
%{_mandir}/man1/mock-hermetic-repo.1*
%{_datadir}/cheat/mock

# cache & build dirs
%defattr(0775, root, mock, 0775)
%dir %{_localstatedir}/cache/mock
%dir %{_localstatedir}/lib/mock

%files scm
%{python_sitelib}/mockbuild/scm.py*
%{python3_sitelib}/mockbuild/__pycache__/scm.*.py*

%files lvm
%{python_sitelib}/mockbuild/plugins/lvm_root.*
%{python3_sitelib}/mockbuild/plugins/__pycache__/lvm_root.*.py*

%files rpmautospec
%{python_sitelib}/mockbuild/plugins/rpmautospec.*
%{python3_sitelib}/mockbuild/plugins/__pycache__/rpmautospec.*.py*

%files filesystem
%license COPYING
%dir  %{_sysconfdir}/mock
%dir  %{_sysconfdir}/mock/eol
%dir  %{_sysconfdir}/mock/eol/templates
%dir  %{_sysconfdir}/mock/templates
%dir  %{_datadir}/cheat
%config(noreplace) %{_sysusersdir}/mock.conf

%changelog
* Thu Dec 19 2024 Pavel Raiskup <praiskup@redhat.com> 6.0-1
- export_buildroot_image: new plugin for OCI image exports
- buildroot_image: allow using OCI images as the base for buildroot
- hermetic: do not install buildroot via DNF
- podman: typofix in library call error-message
- use new digest for comparing podman images (tkopecek@redhat.com)
- hermetic: do "podman pull" instead of "podman load" for bootstrap
- podman: always tag/untag the images we work with locally
- podman: generalize the logic so it is not bootstrap-only
- avoid using the %%pre scriptlet if possible
- hermetic: retry on failed network requests (rbean@redhat.com)
- hermetic: more robust retry mechanism for downloading rpms (tkopecek@redhat.com)
- chroot_scan: bugfix - create chroot_scan/ correctly in buildroot.resultdir
- mock: drop the unused create_default_route_in_container.sh script
- mock: make --dnf-cmd compatible with DNF5 (frostyx@email.cz)
- mock: add a real source URL into %%Source
- the dnf_builddep_opts made working again (addisu@openrobotics.org)

* Mon Sep 30 2024 Pavel Raiskup <praiskup@redhat.com> 5.9-1
- fix the DNF4 fallback for --no-bootstrap-chroot

* Fri Sep 27 2024 Pavel Raiskup <praiskup@redhat.com> 5.8-1
- chroot_scan: make sure the tarball is owned by non-priv user
- chroot_scan: use util.do to display command in --verbose
- chroot_scan: correctly create the result directory

* Thu Sep 26 2024 Pavel Raiskup <praiskup@redhat.com> 5.7-1
- hermetic: new mode to do fully-offline builds
- new --scrub-all-chroots option
- make "dnf4" equivalent to "dnf"
- chroot_scan: create result directory with appropriate permissions
- chain: No need to re-create resultdir
- de-duplicate the local-repo mountpoint in bootstrap
- respect `nspawn_args` whenever `doChroot` is called
- ensure --addrepo option also affects bootstrap
- de-duplicate two opinionated doChroot() calls
- show ccache stats at the end of the build (brian@interlinx.bc.ca)
- add `debug` option to the ccache plugin (belegdol@fedoraproject.org)
- add runtime dependency on fuse-overlayfs (frostyx@email.cz)
- skip the "podman pull" for bootstrap when not needed
- package_state: the installed_pkgs.log file now covers dynamic builddeps
- don’t ship rpmautospec plugin with main package (nils@redhat.com)
- clean up of macros referencing rhel7 (msuchy@redhat.com)
- enable RPM sysusers integration (j1.kyjovsky@gmail.com)
- add hashdir option to ccache plugin (belegdol@fedoraproject.org)
- own /usr/share/doc/mock (msuchy@redhat.com)

* Tue May 14 2024 Jakub Kadlcik <frostyx@email.cz> 5.6-1
- scm: Open stdout in text mode for Git timestamp subprocesses
  (fedora.dm0@gmail.com)
- always set ownership of homedir (but not recursively) (msuchy@redhat.com)
- Do not create temporary Buildroot.tmpdir for disabled nosync
  (praiskup@redhat.com)
- bash-completion: add mock-parse-buildlog (pastalian46@gmail.com)
- Rewrites "original_name" method to check if "cls" has a "backmap"
  (nikitych@yandex.ru)
- Don't use --allowerasing for more DNF commands (frostyx@email.cz)
- bash-completion: pre-build the list of mock known options
  (praiskup@redhat.com)
- Avoid Traceback for resultdir ENOSPC (praiskup@redhat.com)
- Post-release administrivia (praiskup@redhat.com)
- Fix Version in %%changelogs (praiskup@redhat.com)

* Wed Feb 14 2024 Pavel Raiskup <praiskup@redhat.com> 5.5-1
- allow chroot_scan to create archive instead of directory (tkopecek@redhat.com)
- handle greedy options in Bash completion
- fix root_cache invalidation (not) triggered by config changes
- new '{{ repo_arch }}' Jinja2 template support
- package_manager: disable %%-interpolation in dnf.conf parser
- only `chown` the in-chroot home files with the --rebuild mode
- all non-privileged actions performed wiht EGID=135 (mock group)
- mock newly requires a precise version of mock-filesystem
- allow shadow-utils to run in buildroot by exception if necessary (martjack@redhat.com)
- hw_info now reports file system type (vondruch@redhat.com)

* Thu Jan 04 2024 Pavel Raiskup <praiskup@redhat.com> 5.4-1
- Fix installing rpmautospec plugin dependencies (yzhu@redhat.com)

* Wed Dec 13 2023 Pavel Raiskup <praiskup@redhat.com> 5.3-1
- orphanskill: log command line arguments of the terminated process
- docs: migrate the community from IRC to Matrix
- dnf5: don't output to a PTY (mail@evangoo.de)
- new rpmautospec plugin (sgallagh@redhat.com, nils@redhat.com)
- fix bash completion with multiple file arguments (orion@nwra.com)
- only %%prep once when running %%generate_buildrequires multiple times (miro@hroncok.cz)
- Dynamic BuildRequires: Prevent generation of unsatisfied dependency (miro@hroncok.cz)
- Identify buildroot package management earlier (praiskup@redhat.com)
- Dump also dnf5 info into logs

* Wed Sep 27 2023 Pavel Raiskup <praiskup@redhat.com> 5.2-1
- Fix '~' user source expansion for --copyout
- Compatibility fix with EL 8
- Log out the command-line arguments
- Make sure that 'state' is always finished
- README.md: cleaning up
- Post-release administrivia

* Mon Sep 18 2023 Pavel Raiskup <praiskup@redhat.com> 5.1.1-1
- keep re-creating the root directory for each build

* Fri Sep 15 2023 Pavel Raiskup <praiskup@redhat.com> 5.1-1
- new upstream release, per https://rpm-software-management.github.io/mock/Release-Notes-5.1

* Wed Aug 09 2023 Pavel Raiskup <praiskup@redhat.com> 5.0-1
- new upstream release, per https://rpm-software-management.github.io/mock/Release-Notes-5.0

* Fri Jun 02 2023 Pavel Raiskup <praiskup@redhat.com> 4.1-1
- bootstrap: fix certificate copying into the bootstrap chroot
- don't strictly require any package manager
- config: properly configure package manager commands
- unify the fallback-detection for host/bootstrap/bootstrap-image
- bind_mount plug-in: pre-create dest directory before bind-mounting a file
- bootstrap: use DNF5 in package manager fallbacks
- fix --dnf-cmd traceback with the new package_manager logic

* Mon May 22 2023 Pavel Raiskup <praiskup@redhat.com> 4.0-1
- cleanup the bootstrap image logic so it works if Mock is run in container
- rebuild: kill orphans when mounted
- bootstrap: delay the buildroot-in-bootstrap recursive mount
- use shlex instead of pipes
- fix bootstrap_* prefixed config_opts options
- manual page: fix the "how to fill an issue" info
- support for DNF5 added
- use -N instead of -n for useradd (msuchy@redhat.com)
- mock: don't use distutils copy_tree()

* Thu Dec 01 2022 Pavel Raiskup <praiskup@redhat.com> 3.5-1
- check for qemu-user-static raises InvalidArchitecture()
- forcearch: map armv7hl to the /usr/bin/qemu-arm-static binary
- more pedantic check for the qemu-*-static binaries

* Tue Nov 15 2022 Pavel Raiskup <praiskup@redhat.com> 3.4-1
- make device mapper control device available if supported (neal@gompa.dev)
- check for target specific qemu-user-static (msuchy@redhat.com)

* Mon Oct 17 2022 Pavel Raiskup <praiskup@redhat.com> 3.3-1
- re-allow running mock as root, rhbz#2135203

* Fri Oct 14 2022 Pavel Raiskup <praiskup@redhat.com> 3.2-1
- Fix the docker environment check for cgroupv2 (achal.velani@oracle.com)
- mock-scm: recommend rpkg-util
- don't use rpmbuild --noclean option if not supported
- do only one fork() while reading --list-chroots configs
- Error() (exceptions) code rewritten and simplified
- dropped mock SGID from /var/{lib,cache}/mock dirs
- change license to spdx (msuchy@redhat.com)
- podman.py: don't let podman warnings taint container id (micho@redhat.com)

* Fri Jul 22 2022 Pavel Raiskup <praiskup@redhat.com> 3.1-1
- let rpmbuild know that it should not clean up after itself (msuchy@redhat.com)
- typo in the subscription error message
- root_cache: simplify decompressing with BSD tar
- switch from /bin/gtar to /bin/tar by default

* Wed Apr 06 2022 Pavel Raiskup <praiskup@redhat.com> 3.0-1
- mock v3 contains several Python 2.7 (EL7) incompatibilites
  https://github.com/rpm-software-management/mock/issues/755
- disable SECCOMP for Podman by default
- opt in for SECCOMP invented
- create simple_load_config() for use in 3rd party SW (msuchy@redhat.com)
- implement --list-chroots command (msuchy@redhat.com)
- add cachedir to output of hw_info plugin (msuchy@redhat.com)
- mock: copy /usr/share/pki source CA certificates (dereks@lifeofadishwasher.com)
- add missing args for --scrub and --short-circuit into bash
  completion (didiksupriadi41@fedoraproject.org)
- remove el7 specific parts from the spec file (msuchy@redhat.com)

* Thu Dec 16 2021 Pavel Raiskup <praiskup@redhat.com> 2.16-1
- disable system call filtering
- pass env to podman run (dani@lapiole.org)
- give user alternative help for missing 'epel-8-*' configs
- podman, explictily specify stdin as tar source (vreeland.justin@gmail.com)
- add a new 'ssl_extra_certs' option (patrick@laimbock.com)

* Thu Nov 18 2021 Pavel Raiskup <praiskup@redhat.com> 2.15-1
- argparse: handle old-style commands *before* ignoring "--" (awilliam@redhat.com)
- Update mock.1 (cheese@nosuchhost.net)

* Thu Nov 04 2021 Pavel Raiskup <praiskup@redhat.com> 2.14-1
- fixed broken --enablerepo/--disablerepo options

* Mon Nov 01 2021 Pavel Raiskup <praiskup@redhat.com> 2.13-1
- local repositories to use gpgcheck=0 by default
- A new option --additional-package (for --rebuild)
- external-deps: install pip packages to /usr
- Install external deps into build chroot, not bootstrap
- Migrate from optparse to argparse
- mock: don't specify SOURCE when remounting bind-mounts
- mock: add option --debug-config-expanded (sergio@serjux.com)
- Fix use of deprecated function (xfgusta@gmail.com)
- lvm_root: fix copy/paste error in a warning message (kdudka@redhat.com)

* Mon Jul 19 2021 Pavel Raiskup <praiskup@redhat.com> 2.12-1
- don't set --cwd for --shell when we know it will fail (el7)
- explicitly convert macro values to str (logans@cottsay.net)
- disable versionlock DNF plugin by default (igor.raits@gmail.com)
- move Requires of shadow-utils from mock-core-configs to mock-filesystem
  (msuchy@redhat.com)

* Tue Jun 08 2021 Pavel Raiskup <praiskup@redhat.com> 2.11-1
- mock: fix broken --help output
- compress_logs: compress also after repo failures
- move to libera.chat (msuchy@redhat.com)
- Define _platform_multiplier macro (msuchy@redhat.com)
- allow to --install external:* (msuchy@redhat.com)
- move installation of external:* to separate function (msuchy@redhat.com)
- honor --cwd for --shell (msuchy@redhat.com)

* Tue Apr 27 2021 Pavel Raiskup <praiskup@redhat.com> 2.10-1
- do not allocate tty for podman (msuchy@redhat.com)
- work-around bug setting propagation for recursive bind-mounts (david.ward@ll.mit.edu)
- fix handling of essential mountpoints (david.ward@ll.mit.edu)
- pre-create the dest directory in _copy_config

* Mon Jan 18 2021 Pavel Raiskup <praiskup@redhat.com> 2.9-1
- rpkg_preprocessor: Add a force_enable option (tstellar@redhat.com)
- use TemplatedDictionary as standalone module (msuchy@redhat.com)

* Tue Dec 15 2020 Pavel Raiskup <praiskup@redhat.com> 2.8-1
- fix use of nspawn (#678) (awilliam@redhat.com)
- file_util: Improve an error message (tbaeder@redhat.com)

* Mon Nov 30 2020 Pavel Raiskup <praiskup@redhat.com> 2.7-1
- bootstrap: copy-in katello CA pem file if exists
- early error when bootstrap is off and external buildrequires are detected (msuchy@redhat.com)
- hotfix preexec_fn traceback on RHEL 8 s390x (issue 653)
- introduce external buildrequires (msuchy@redhat.com)
- add rpkg spec preprocessing capability (clime@fedoraproject.org)
- sign plugin: don't ignore signing command failure
- don't setsid() twice with --shell
- better logging when dynamic BR detected (msuchy@redhat.com)
- do not TB if rpmbuild fails with exit code 11 (msuchy@redhat.com)
- fix addrepo when repo is missing (markus.linnala@gmail.com)
- own the cheat directory
- Allow percent-sign in config_opts['resultdir']
- add a new "postupdate" hook (dturecek@redhat.com)
- log mock's NVR

* Tue Sep 15 2020 Pavel Raiskup <praiskup@redhat.com> 2.6-1
- the --recurse option implies --continue
- fix --chain --continue option
- fail when --continue/--recurse is used without --chain
- fix _copy_config() for broken symlinks in dst= (rhbz#1878924)
- auto-download the source RPMs from web with --rebuild
- handle exceptions from command_parse() method
- fail verbosely for --chain & --resultdir combination
- allow using -a|--addrepo with /absolute/path/argument
- add support for -a/--addrepo in normal --rebuild mode
- use systemd-nspawn --resolv-conf=off
- create /etc/localtime as symlink even with isolation=simple (msuchy@redhat.com)
- dump the reason for particular package build fail in --chain
- raise PkgError when the source RPM can not be installed

* Thu Sep 03 2020 Pavel Raiskup <praiskup@redhat.com> 2.5-2
- because of the mock-filesystem change, we need to enforce upgrade
  of the old mock-core-configs package

* Thu Sep 03 2020 Pavel Raiskup <praiskup@redhat.com> 2.5-1
- set the DNF user_agent in dnf.conf (msuchy@redhat.com)
- introduce mock-filesystem subpackage (msuchy@redhat.com)
- add showrc plugin to record the output of rpm --showrc (riehecky@fnal.gov)
- document which packages we need in buildroot (msuchy@redhat.com)
- macros without leading '%' like config_opts['macros']['macroname'] work
  fine again (issue#605)

* Tue Jul 21 2020 Miroslav Suchý <msuchy@redhat.com> 2.4-1
- mockbuild/buildroot: Make btrfs-control available if host supports it
  (ngompa13@gmail.com)
- Add `module_setup_commands` configuration option (praiskup@redhat.com)
- Use a different .rpmmacros for install/build time (praiskup@redhat.com)
- lvm: don't recall set_current_snapshot unnecessarily (praiskup@redhat.com)
- mock: copy source CA certificates (kdreyer@redhat.com)

* Fri May 22 2020 Pavel Raiskup <praiskup@redhat.com> 2.3-1
- bindmount resultdir to bootstrap chroot so we can --postinstall from
  bootstrap (issue #564)
- fix mount.py plugin configuration (issue #578)
- better error for dynamic_buildrequires %%prep failure (issue #570)
- mock: pre-create directory for file bind-mounts (rhbz#1816696)
- fix doChroot() traceback for getresuid() (issue #571)
- fix --rootdir option with bootstrap (issue #560)
- avoid using host rpm _show_installed_packages() (pmatilai@redhat.com, PR#568)
- expand braced dnf variables in repo url (dmarshall@gmail.com, PR#577)

* Wed Apr 01 2020 Pavel Raiskup <praiskup@redhat.com> 2.2-1
- depend on mock-configs, not mock-core-configs so users can pick an alternative
  package with configuration
- bind-mounting stuff below /tmp into bootstrap is fixed with nspawn (GH#502)
- don't do util.getAddtlReqs when 'more_buildreqs' not specified
- implement doOutChroot() abstraction which runs commands either in bootstrap
  or on host, depending on isolation={nspawn|simple}
- use doOutChroot() for package_state plugin (GH#525)
- fix for "mock --chroot -- cmd arg1 arg2" use-case
- site-defaults.cfg moved from /etc to %%doc, and the config file is now
  provided by mock-core-configs (GH#555)
- bootstrap: expand dnf vars in local repo bind-mounts (rhbz#1815703)
- bootstrap: bindmount local metalink/mirrorlist (rhbz#1816696)
- config_opts['isolation'] option invented, replaces 'use_nspawn'
- 'isolation' is now set to 'auto' (means 'nspawn' with fallback to 'simple',
  (GH#337, otaylor@fishsoup.net)
- Fedora Toolbox && bootstrap - don't re-bind-mount dev files, and fix
  installation of filesystem.rpm from bootstrap to normal chroot (GH#550)
- re-define %%python3_pkgversion on el7 (GH#545)
- docker use-case: use getpass.getuser() instead of os.getlogin() (GH#551)
- set LANG to C.UTF-8 by default, even if host has different value (GH#451)
- bootstrap: use configured yum commands (GH#518, paul@city-fan.org)
- fixup doubled-logs by predictable bootstrap resultdir (GH#539, rhbz#1805631)
- fix --chain --isolation=simple with external URLs (GH#542)
- option --orphanskill fixed for --isolation=simple --bootstrap-chroot
- orphan processes are now also killed "postyum", right after the installation
  trasactions are executed to also kill daemons started from scriptlets (GH#183)
- EL7 fix - use 'private' mount option for <bootsrap_root>/<root>, not 'rprivate'
- ceanup rpmdb before checking installed packages (fixes builds against target
  chroots that have different rpmdb backend, e.g. SQLite on F33+)

* Wed Mar 11 2020 Pavel Raiskup <praiskup@redhat.com> 2.1-1
- depend on mock-core-configs >= 32.4
- new build-time testsuite
- accept return code 0 from rpmbuild -br (thrnciar@redhat.com)
- bootstrap: bind-mount the inner root mount with rprivate
- new ssl_ca_bundle_path option
- chain: don't run buildroot.finalize() for each package
- don't fail when /etc/pki certs are not found (frostyx@email.cz)
- lvm_root: fix --scrub=all
- exclude plugin compiled stuff packaged in sub-packages
- keep trailing newlines in jinja expand
- sign-plugin: use %%(rpms) variable expansion again
- bootstrap: bind-mount also baseurl=/absolute/dir repos
- 'dnf.conf' config is now equivalent to 'yum.conf'
- don't emit unneeded warning for missing yum (remi@remirepo.net)
- allow --install /usr/bin/time [GH#474] (miroslav@suchy.cz)

* Fri Feb 07 2020 Pavel Raiskup <praiskup@redhat.com> 2.0-2
- solve yum.conf vs. dnf.conf inconsistency in code and config
- fix mockchain with --bootstrap-chroot (issue/469)
- document 'mock --chain -c' in man page

* Thu Feb 06 2020 Pavel Raiskup <praiskup@redhat.com> 2.0-1
- log reasons why src.rpm can not be installed into chroot
- nspawn: non-interactive commands in chroot are executed with --pipe
- bind mount local repos to bootstrap chroot (dturecek@redhat.com)
- expand the generated config (includes) completely before passing it
  to eval() (sergio@serjux.com)
- do not ignore cleanup_on_success when post_install is True
  (logans@cottsay.net)
- fix fd resource-leak in 'mock --chain' (jcajka@redhat.com)
- the --debug-config option only shows the differences from the mock's default
  configuration
- do not expand jinja for --debug-config
- don't use chroot.pkg_manager in podman case, we need to install from within
  the container
- --use-bootstrap-image implies --bootstrap-chroot
- drop python2 support from spec file, and code too
- ammend man page and state that --dnf is the default now
- rename --{old,new}-chroot to --isolation
- turn ON the jinja rendering a bit earlier
- pre-populate loop devices in nspawn chroot as with --isolation=chroot
- deepcopy the plugin_conf options from chroot to bootstrap_chroot
- simplified implementation of include() config option, accept relative files
  (jkadlcik@redhat.com, sergio@serjux.com)
- pass proxy environment to exec of Podman (RHBZ#1772598)
- lvm_root: fix volume removal in --scrub
- bootstrap: don't install shadow-utils, and distribution-gpg-keys
- make --sources optional for --buildsrpm mode (sisi.chlupova@gmail.com)
- bootstrap: bind-mount normal chroot into bootstrap chroot recursively
- add --scrub=bootstrap parameter (frostyx@email.cz)
- don't clean bootstrap with --clean
- do not call traceLog decorator when no tracing
- pre-create builddir before changing it's owner, and when we have proper
  process privileges
- copy /etc/pki/ca-trust/extracted into chroot [GH#397]
- change default of 'package_manager' to 'dnf'
- always copy distribution-gpg-keys into chroot [GH#308]
- support DNF vars added [GH#346]
- use jinja macros instead of python variable expansion
- get the text representation of error code
- --scrub=all also does --scrub=bootstrap (jkadlcik@redhat.com)
- success/fail aren't created root-owned
- compress_logs: setup defaults to 'gzip'
- raise error for --localrepo without --chain
- detect that forcearch can not work, and raise obvious error
- drop unnecessary privilege escalations which only make unnecessary
  root-owned files

* Fri Oct 04 2019 Miroslav Suchý <msuchy@redhat.com> 1.4.20-1
- /bin/mockchain wrapper around 'mock --chain' (praiskup@redhat.com)
- mock: options for retrying packager managers' actions (praiskup@redhat.com)
- remove mockchain [RHBZ#1757388]
- chain: don't skip local repository (praiskup@redhat.com)
- chain: propagate local repository to bootstrap chroot (praiskup@redhat.com)
- hw_info: don't create root-owned files (praiskup@redhat.com)
- ignore ./var/log when creating root_cache - fixes #309
  (jiri.novak@ghorland.net)
- mock: don't create root files if possible (praiskup@redhat.com)
- add commandline options for using bootstrap image (frostyx@email.cz)
- Use podman to pull and export an image as a bootstrap chroot
  (dmach@redhat.com)

* Tue Sep 10 2019 Miroslav Suchý <msuchy@redhat.com> 1.4.19-1
- results should be owned by unpriv user [GH#322]
- do not build with tests by default
- Resultdir variable is missing in config. (sisi.chlupova@gmail.com)

* Tue Aug 27 2019 Miroslav Suchý <msuchy@redhat.com> 1.4.18-1
- use forcearch even when --forcearch is not specified
  (turecek.dominik@gmail.com)
- requires systemd-container on rhel8 [RHBZ#1744538]
- mock: only make /sys and /proc mounts rprivate (praiskup@redhat.com)
- Add Red Hat subscription-manager support (praiskup@redhat.com)
- Turn jinja ON a bit later, once configs are loaded (praiskup@redhat.com)
- bootstrap-chroot: always explicitly install shadow-utils
  (praiskup@redhat.com)
- Add procenv plugin for more detailed buildtime information
  (riehecky@fnal.gov)
- enable selinux plugin for nspawn [RHBZ#1740421]
- Added signals handling by calling orphansKill for signals: SIGTERM, SIGPIPE
  and SIGHUP (janbuchmaier@seznam.cz)
- Mention user configuration file in a man page (jkonecny@redhat.com)

* Thu Aug 08 2019 Miroslav Suchý <msuchy@redhat.com> 1.4.17-1
- change of exit code during transition from mockchain to mock --chain
- support run in Fedora Toolbox (otaylor@fishsoup.net)
- add cheat sheet
- Adding tool for parsing build.log (sisi.chlupova@gmail.com)
- load secondary groups [RHBZ#1264005]
- pass --allowerasing by default to DNF [GH#251]
- make include() functional for --chain [GH#263]
- Removing buildstderr from log - configurable via 
  _mock_stderr_line_prefix (sisi.chlupova@gmail.com)
- Fixup: Use rpm -qa --root instead of running rpm -qa in chroot
  (miro@hroncok.cz)
- DynamicBuildrequires: Detect when no new packages were installed
  (miro@hroncok.cz)
- Allow more loop devices (sisi.chlupova@gmail.com)
- Fix binary locations in /bin for split-usr setups (bero@lindev.ch)
- describe behaviour of resultdir together with --chain [GH#267]
- repeat dynamic requires if needed [GH#276]
- Fix compatibility with pre-4.15 RPM versions with DynamicBuildRequires
  (i.gnatenko.brain@gmail.com)
- Enable dynamic BuildRequires by default (i.gnatenko.brain@gmail.com)
- bootstrap: independent network configuration (praiskup@redhat.com)
- Update the man page about ~/.config/mock/FOO.cfg (miro@hroncok.cz)
- explicitely convert releasever to string [GH#270]
- grant anyone access to bind-mounted /etc/resolv.conf (praiskup@redhat.com)
- -r FOO will try to read first ~/.mock/FOO.cfg if exists
- enhance man page of mock about --chain
- bash completion for --chain
- respect use_host_resolv config even with use_nspawn (praiskup@redhat.com)
- Fix crash on non-ascii dnf log messages (bkorren@redhat.com)
- add deprecation warning to mockchain
- replace mockchain with `mock --chain` command (necas.marty@gmail.com)
- switch to python3 on el7 (msuchy@redhat.com)

* Wed May 22 2019 Miroslav Suchý <msuchy@redhat.com> 1.4.16-1
- switch to python3 on el7
- respect use_host_resolv config even with use_nspawn (praiskup@redhat.com)
- Fix crash on non-ascii dnf log messages (bkorren@redhat.com)

* Mon Apr 22 2019 Miroslav Suchý <msuchy@redhat.com> 1.4.15-1
- ignore weird distro.version() [RHBZ#1690374]
- switch to string rpm's API [RHBZ#1693759]
- FileNotFoundError is not defined in Python 2 [RHBZ#1696234]
- Fix python2-devel build require
- temporary do not make errors from createrepo_c fatal [GH#249]
- allow to configure disabled DNF plugins [GH#210]
- print warning when user is not in the mock group [GH#244]
- implement Dynamic Build Dependencies (msuchy@redhat.com)
- Allow mock to be built for epel 8, and without tests
  (vanmeeuwen@kolabsys.com)
- Add debug logging for systemd-nspawn and related args (riehecky@fnal.gov)
- Fix mock for non-ascii paths on python2 (a.badger@gmail.com)
- require python-jinja2 rather than python2-jinja2
- Fix --enable-network documentation in man page (directhex@apebox.org)

* Tue Feb 19 2019 Miroslav Suchý <msuchy@redhat.com> 1.4.14-1
- config['decompress_program'] default (praiskup@redhat.com)
- add example for jinja templates
- implement templated configs using jinja2
- move live defaults from site-defaults.cfg to utils.py
- introduce "decompress_program" option for root_cache for bsdtar
- fix exclude patter for bsdtar
- delete old changelog entries
- use f29 for tests
- update the default in sitec-defaults.cfg
- Recommend dnf-utils (fzatlouk@redhat.com)
- ignore useless-object-inheritance pylint warning
- add scientific linux on list of rhel clones [GH#228]
- Use 32-bit personality for armv7*/armv8* builds (bero@lindev.ch)
- create custom error message for dnf-utils not being installed
  (pjunak)

* Mon Aug 13 2018 Miroslav Suchý <msuchy@redhat.com> 1.4.13-1
- fix python_sitelib macro

* Mon Aug 13 2018 Miroslav Suchý <msuchy@redhat.com> 1.4.12-1
- Don't try to use a spec we've already cleaned up (otaylor@fishsoup.net)
- only set print_main_output when not set in configs
  (chuck.wilson+github@gmail.com)
- Try to get the proxy from environment (brunovern.a@gmail.com)
- stop after first failure if -c or --recurse is not used
- fallback to C.UTF-8 locale (tomek@pipebreaker.pl)
- completion: improve --copy(in|out), --cwd, --macro-file, --rootdir, and
  --sources (tmz@pobox.com)
- do not get spec from command line when using scm [GH#203]
- enable cap_ipc_lock in nspawn container [RHBZ#1580435]
- use host's resolv.conf when --enable-network is set on cml [RHBZ#1593212]
  (jskarvad@redhat.com)
- add --forcearch to bash_completion

* Tue Jun 12 2018 Miroslav Suchý <msuchy@redhat.com> 1.4.11-1
- fix @VERSION@ processing in man pages (ktdreyer@ktdreyer.com)
- update testing.src.rpm to recent standard
- Allow --spec arg to be used with rebuild option (sfowler@redhat.com)
- Disable use_host_resolv by default (tmz@pobox.com)
- Add support for microdnf [GH#76] (zdenekirsax@gmail.com)
- skip running groupadd if gid is 0 (nhorman@tuxdriver.com)
- Allow overriding of mock chroot build user name (nhorman@tuxdriver.com)
- do not populate /etc/resolv.conf when networking is disabled (RHBZ#1514028)
  (tmz@pobox.com)
- add version to EL check in _prepare_nspawn_command() (tmz@pobox.com)
- pass force-arch to builddep and resolvedep [GH#120]
- Support setting up foreign architecture chroots
- add support for bsdtar
- use fedora 28 for tests

* Thu May 10 2018 Miroslav Suchý <msuchy@redhat.com> 1.4.10-1
- remove executable bit from trace_decorator.py
- Change sign plugint to sign only builded rpm and not every file in results
  [RHBZ#1217495] (necas.marty@gmail.com)
- overlayfs plugin: added explicit mount support (zzambers@redhat.com)
- encode content before writing [RHBZ#1564035]
- allow to bind_mount just one file (necas.marty@gmail.com)
- added overlayfs plugin (zzambers@redhat.com)
- invoke chroot scan for 'initfailed' event (clime7@gmail.com)
- add support for .spec in --installdeps (necas.marty@gmail.com)
- revert workaround introduced in 057c51d6 [RHBZ#1544801]
- comment out macro in changelog (msuchy@redhat.com)

* Mon Feb 12 2018 Miroslav Suchý <msuchy@redhat.com> 1.4.9-1
- "setup_cmd" of bootstrap container is the actuall $pm_install_command from
  the main container [RHBZ#1540813]
- do not produce warning when we are using different PM for bootstrap container
- Honor the "cwd" flag when nspawn is being used and "chrootPath" is not set
  (matthew.prahl@outlook.com)
- do not run ccache in bootstrap chroot [RHBZ#1540813]
- use DNF on EL7 when bootstrap is used [RHBZ#1540813]
- site-defaults: fix quoting in sign_opts example [RHBZ#1537797]
  (tmz@pobox.com)
- Detect if essential mounts are already mounted (msimacek@redhat.com)
- Update Python 2 dependency declarations to new packaging standards
- improvement code/docs for opstimeout (Mikhail_Campos-Guadamuz@epam.com)
- simplifying of utils.do() (Mikhail_Campos-Guadamuz@epam.com)
- New config option 'opstimeout' has been added. (Mikhail_Campos-
  Guadamuz@epam.com)
- Don't setup user mounts in the bootstrap buildroot (bkorren@redhat.com)
- el5 is sensitive to order of params
- Default for config_opts['dnf_warning'] according to docs
  (praiskup@redhat.com)
- Avoid manual interpolation in logging of BUILDSTDERR (Mikhail_Campos-
  Guadamuz@epam.com)
- Splitting stdout and stderr in build.log. All stderr output lines are
  prefixed by 'BUILDSTDERR:' (Mikhail_Campos-Guadamuz@epam.com)

* Fri Dec 22 2017 Miroslav Suchý <msuchy@redhat.com> 1.4.8-1
- orphanskill: send SIGKILL when SIGTERM is not enough [RHBZ#1495214]
- pass --non-unique to usermod because of old targets
- remove _selinuxYumIsSetoptSupported()
- only use -R if first umount failed
- use recursive unmount for tmpfs
- do not cd to dir if nspawn is used [GH#108]
- add new option --config-opts [GH#138]
- add --enable-network to bash_completation
- Strip trailing / from mountpath in ismounted()
- new cli option --enable-network [RHBZ#1513953]
- when creating yum/dnf.conf copy timestamp from host [RHBZ#1293910]
- do not populate /etc/resolv.conf when networking is disabled [RHBZ#1514028]
- soften mock-scm dependencies [RHBZ#1515989]
- mount /proc and /sys before executing any PM command [RHBZ#1467299]

* Tue Oct 31 2017 Miroslav Suchý <msuchy@redhat.com> 1.4.7-1
- user and group is actually not used here since some logic moved to buildroot.py
- add config_opts['chrootgroup'] to site-defaults.cfg
- Enable chrootgroup as a config file option
- override some keys for bootstrap config
- Add support for DeskOS
- Delete rootdir as well when calling clean
- Fix mock & mock-core-config specs to support Mageia
- Ensure mock-core-configs will select the right default on Mageia
- ccache: use different bind mount directory
- new-chroot: set up new network namespace and add default route in it
- use primary key for F-27+ on s390x
- man: add dnf to see also
- man: escape @
- remove Seth email
- more grammar fixes
- fix typo in mock(1)
- sort debug-config output

* Fri Sep 15 2017 Miroslav Suchý <msuchy@redhat.com> 1.4.6-1
- requires mock-core-configs

* Fri Sep 15 2017 Miroslav Suchý <msuchy@redhat.com> 1.4.5-1
- introduce -N for --no-cleanup-after (jsynacek@redhat.com)
- add man page entry for --debug-config
- Added option --debug-config (matejkudera1@seznam.cz)
- site-defaults: Fix comment about nspawn/chroot default (ville.skytta@iki.fi)
- move chroot configs to mock-core-configs directory
- pass --private-network to every container spawning if specified
- add script to create default route in container to localhost
- [site-defaults] Fix umount_root documentation
- Fix keeping the LVM volume mounted
- suggest dnf-utils
- Always create /dev/loop nodes
