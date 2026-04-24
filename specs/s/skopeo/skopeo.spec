## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global with_debug 1

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%global gomodulesmode GO111MODULE=on

# Distro and environment conditionals
%if %{defined fedora}
# Fedora conditionals
%define build_with_btrfs 1
%define conditional_epoch 1
%if %{?fedora} >= 43
%define sequoia 1
%endif
%else
# RHEL conditionals
%define conditional_epoch 2
%define fips 1
%endif

# set higher Epoch only for podman-next builds
%if %{defined copr_username} && "%{copr_username}" == "rhcontainerbot" && "%{copr_projectname}" == "podman-next"
%define next_build 1
%endif

Name: skopeo
%if %{defined next_build}
Epoch: 102
%else
Epoch: %{conditional_epoch}
%endif
# DO NOT TOUCH the Version string!
# The TRUE source of this specfile is:
# https://github.com/containers/skopeo/blob/main/rpm/skopeo.spec
# If that's what you're reading, Version must be 0, and will be updated by Packit for
# copr and koji builds.
# If you're reading this on dist-git, the version is automatically filled in by Packit.
Version: 1.22.0
# The `AND` needs to be uppercase in the License for SPDX compatibility
License: Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0
Release: %autorelease
%if %{defined golang_arches_future}
ExclusiveArch: %{golang_arches_future}
%else
ExclusiveArch: aarch64 ppc64le s390x x86_64
%endif
Summary: Inspect container images and repositories on registries
URL: https://github.com/containers/%{name}
# Tarball fetched from upstream
Source0: %{url}/archive/v%{version}.tar.gz
BuildRequires: %{_bindir}/go-md2man
%if %{defined build_with_btrfs}
BuildRequires: btrfs-progs-devel
%endif
BuildRequires: git-core
BuildRequires: golang
%if !%{defined gobuild}
BuildRequires: go-rpm-macros
%endif
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: glib2-devel
BuildRequires: make
BuildRequires: shadow-utils-subid-devel
BuildRequires: sqlite-devel
Requires: containers-common >= 4:1-21
%if %{defined sequoia}
Requires: podman-sequoia
%endif

%description
Command line utility to inspect images and repositories directly on Docker
registries without the need to pull them.

# NOTE: The tests subpackage is only intended for testing and will not be supported
# for end-users and/or customers.
%package tests
Summary: Test dependencies for %{name}

Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: gnupg
Requires: jq
Requires: golang
Requires: podman
Requires: crun
Requires: httpd-tools
Requires: openssl
Requires: squashfs-tools
# bats and fakeroot are not present on RHEL and ELN so they shouldn't be strong deps
Recommends: bats
Recommends: fakeroot

%description tests
This package installs system test dependencies for %{name}

%prep
%autosetup -Sgit %{name}-%{version}
# The %%install stage should not rebuild anything but only install what's
# built in the %%build stage. So, remove any dependency on build targets.
sed -i 's/^install-binary: bin\/%{name}.*/install-binary:/' Makefile
sed -i 's/^completions: bin\/%{name}.*/completions:/' Makefile
sed -i 's/^install-docs: docs.*/install-docs:/' Makefile

%build
%set_build_flags
export CGO_CFLAGS=$CFLAGS

# These extra flags present in $CFLAGS have been skipped for now as they break the build
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-flto=auto//g')
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-Wp,D_GLIBCXX_ASSERTIONS//g')
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//g')

%ifarch x86_64
export CGO_CFLAGS="$CGO_CFLAGS -m64 -mtune=generic -fcf-protection=full"
%endif

BASEBUILDTAGS="$(hack/libsubid_tag.sh) libsqlite3"
%if %{defined build_with_btrfs}
export BUILDTAGS="$BASEBUILDTAGS $(hack/btrfs_installed_tag.sh)"
%else
export BUILDTAGS="$BASEBUILDTAGS exclude_graphdriver_btrfs"
%endif

%if %{defined fips}
export BUILDTAGS="$BUILDTAGS libtrust_openssl"
%endif

%if %{defined sequoia}
export BUILDTAGS="$BUILDTAGS containers_image_sequoia"
%endif

# unset LDFLAGS earlier set from set_build_flags
LDFLAGS=''

%gobuild -o bin/%{name} ./cmd/%{name}
%{__make} docs

%install
make \
    DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    install-binary install-docs install-completions

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

# Include this to silence rpmlint.
# Especially annoying if you use syntastic vim plugin.
%check

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}

# Only test dependencies installed, no files.
%files tests

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1:1.22.0-3
- Latest state for skopeo

* Thu Feb 12 2026 Lokesh Mandvekar <lsm5@redhat.com> - 1:1.22.0-2
- fix ref in plans/main.fmf

* Wed Feb 11 2026 Packit <hello@packit.dev> - 1:1.22.0-1
- Update to 1.22.0 upstream release

* Wed Dec 03 2025 Lokesh Mandvekar <lsm5@redhat.com> - 1:1.21.0-1
- bump to v1.21.0

* Fri Oct 31 2025 Lokesh Mandvekar <lsm5@redhat.com> - 1:1.20.0-5
- Resolves: CVE-2025-58189, CVE-2025-61725

* Tue Oct 07 2025 Lokesh Mandvekar <lsm5@redhat.com> - 1:1.20.0-4
- rebuild for upgrade path

* Tue Sep 02 2025 Lokesh Mandvekar <lsm5@redhat.com> - 1:1.20.0-3
- TMT: fetch tests from upstream

* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 1:1.20.0-2
- Rebuild for golang-1.25.0

* Mon Aug 04 2025 Packit <hello@packit.dev> - 1:1.20.0-1
- Update to 1.20.0 upstream release

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.19.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 12 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.19.0-4
- cleanup changelog

* Thu Jun 12 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.19.0-3
- bats is a weak dep

* Tue Jun 03 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.19.0-2
- fix gating.yaml

* Thu May 22 2025 Packit <hello@packit.dev> - 1:1.19.0-1
- Update to 1.19.0 upstream release

* Wed Feb 12 2025 Packit <hello@packit.dev> - 1:1.18.0-1
- Update to 1.18.0 upstream release

* Thu Feb 06 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.17.0-4
- fix gating.yaml

* Thu Feb 06 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.17.0-3
- TMT: initial enablement

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 13 2024 Packit <hello@packit.dev> - 1:1.17.0-1
- Update to 1.17.0 upstream release

* Tue Sep 24 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.16.1-3
- packit sidetag stuff

* Wed Aug 28 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.16.1-2
- rebuild for shadow-utils soname bump

* Thu Aug 22 2024 Packit <hello@packit.dev> - 1:1.16.1-1
- Update to 1.16.1 upstream release

* Sun Jul 28 2024 Packit <hello@packit.dev> - 1:1.16.0-1
- Update to 1.16.0 upstream release

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Packit <hello@packit.dev> - 1:1.15.2-1
- Update to 1.15.2 upstream release

* Wed May 15 2024 Packit <hello@packit.dev> - 1:1.15.1-1
- Update to 1.15.1 upstream release

* Thu Mar 14 2024 Packit <hello@packit.dev> - 1:1.15.0-1
- [packit] 1.15.0 upstream release

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 1:1.14.2-2
- Rebuild for golang 1.22.0

* Thu Feb 01 2024 Packit <hello@packit.dev> - 1:1.14.2-1
- [packit] 1.14.2 upstream release

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Packit <hello@packit.dev> - 1:1.14.1-1
- [packit] 1.14.1 upstream release

* Thu Nov 23 2023 Packit <hello@packit.dev> - 1:1.14.0-1
- [packit] 1.14.0 upstream release

* Thu Aug 24 2023 Packit <hello@packit.dev> - 1:1.13.3-1
- [packit] 1.13.3 upstream release

* Tue Aug 22 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.13.2-2
- spdx compatible license

* Thu Aug 10 2023 Packit <hello@packit.dev> - 1:1.13.2-1
- [packit] 1.13.2 upstream release

* Thu Jul 20 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.13.1-1
- bump to v1.13.1

* Thu Jul 06 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.13.0-1
- bump to v1.13.0

* Tue Apr 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.12.0-2
- Disable btrfs in RHEL builds

* Thu Apr 13 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.12.0-1
- auto bump to v1.12.0

* Mon Apr 03 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.11.2-1
- auto bump to v1.11.2

* Mon Mar 06 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.11.1-2
- migrated to SPDX license

* Fri Feb 17 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.11.1-1
- auto bump to v1.11.1

* Thu Feb 09 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.11.0-3
- ExclusiveArch: golang_arches_future

* Fri Feb 03 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.11.0-2
- systemtests need golang compiler installed

* Tue Jan 31 2023 Daniel J Walsh <dwalsh@redhat.com> - 1:1.11.0-1
- local build

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 05 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.10.0-7
- remove debbuild ref from spec

* Thu Oct 20 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.10.0-6
- require crun for skopeo-tests

* Fri Oct 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.10.0-5
- Revert "auto bump to v1.10.0"

* Fri Oct 07 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.10.0-4
- auto bump to v1.10.0

* Wed Oct 05 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.10.0-3
- simpler source0 url

* Wed Oct 05 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.10.0-2
- remove debbuild macros to comply with Fedora guidelines

* Mon Oct 03 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.10.0-1
- auto bump to v1.10.0

* Wed Aug 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.9.2-3
- use easier tag macros to make both fedora and debbuild happy

* Tue Aug 16 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.9.2-2
- Fix debbuild maintainer issue

* Tue Aug 02 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.9.2-1
- auto bump to v1.9.2

* Mon Jul 25 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.9.1-1
- auto bump to v1.9.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Maxwell G <gotmax@e.email> - 1:1.9.0-4
- Rebuild for
  CVE-2022-{1705,32148,30631,30633,28131,30635,30632,30630,1962} in golang

* Fri Jul 15 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.9.0-3
- fix package dir listing

* Fri Jul 15 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.9.0-2
- resolve build issues and list new shell completion files

* Wed Jul 13 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.9.0-1
- auto bump to v1.9.0

* Thu Jul 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8.0-10
- debbuild s/Maintainer/Packager

* Sat Jun 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1:1.8.0-9
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327,
  CVE-2022-27191, CVE-2022-29526, CVE-2022-30629

* Wed Jun 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8.0-8
- use golang >= 1.18 for debbuild

* Wed Jun 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8.0-7
- no conditionals for ubuntu versions

* Mon May 30 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8.0-6
- update

* Mon May 30 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8.0-5
- update

* Mon May 30 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8.0-4
- use golang-1.16 for ubuntu 20.04 or less

* Fri May 27 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8.0-3
- build deb packages using debbuild

* Mon May 09 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8.0-2
- try autochangelog

* Mon May 09 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.8.0-1
- auto bump to v1.8.0

* Thu Mar 24 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.7.0-1
- Bump to v1.7.0

* Tue Mar 22 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.1-3
- tests subpackage depends on /usr/sbin/unsquashfs

* Fri Mar 18 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.1-2
- create changelog entry to make koji happy

* Thu Mar 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.1-1
- bump to v1.6.1, switch to autospec

* Mon Feb 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-11
- skopeo-1:1.6.0-1
- bump to v1.6.0

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-10
- retry switching to autochangelog

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-9
- revert switch to autochangelog and remove skopeo.spec from .gitignore

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-8
- switch to autochangelog

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-7
- replace release tag with autorelease, retain changelog

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-6
- remove useless conditional

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-5
- get version from built_tag macro

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-4
- update build steps

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-3
- update bundled provides

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-2
- remove unwanted packages

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-1
- skopeo-1:1.6.0-1
- bump to v1.6.0

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.5.2-1
- Revert "re-bump to v1.6.0, switch to autospec and remove unused packages"

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-1
- re-bump to v1.6.0, switch to autospec and remove unused packages

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.5.2-2
- skopeo-1:1.5.2-3
- bump release tag to check for koji build success

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.5.2-1
- Revert to the last successful koji build

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.0-12
- fix typo

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org>
- Try: no conditional epoch

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-10
- try with bundled provides commented

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-9
- adjust build step

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-8
- adjust build dir process

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-7
- fix .gitignore

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-6
- build for all available arches

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-5
- try %%{golang_arches}

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-4
- add BR: btrfs-progs-devel, mistakenly removed in last commit

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-3
- btrfs available on eln, remove rhel conditional

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-2
- adjust epoch conditionals

* Thu Feb 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.6.0-1
- bump to v1.6.0

* Thu Jan 27 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.5.2-4
- try s/define/global/g

* Thu Jan 27 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.5.2-3
- switch to autospec and misc specfile fixes

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.5.2-1
- skopeo-1:1.5.2-1

* Thu Nov 04 2021 Stephen Gallagher <sgallagh@redhat.com> - 1:1.5.1-2
- ELN: don't try to build with btrfs

* Thu Nov 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.5.1-1
- skopeo-1:1.5.1-1

* Thu Oct 14 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.5.0-4
- Do not hardcode CGO_CFLAGS

* Thu Oct 07 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.5.0-3
- skopeo-1:1.5.0-2
- Drop i686 support for RHEL >= 9
- RHEL 9 does not have i686 support for golang

* Wed Oct 06 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.5.0-2
- update built_tag comments

* Wed Oct 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.5.0-1
- skopeo-1:1.5.0-1

* Wed Aug 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.4.1-1
- skopeo-1:1.4.1-1

* Tue Aug 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.4.0-5
- skopeo-1:1.4.0-1

* Mon Aug 09 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.4.0-4
- skopeo-1:1.4.0-2
- rebuild

* Mon Aug 09 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.4.0-3
- use %%global instead of %%define

* Thu Aug 05 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.4.0-2
- update deps

* Tue Aug 03 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.4.0-1
- skopeo-1:1.4.0-1
- bump to v1.4.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.3.1-1
- skopeo-1:1.3.1-15
- built tag v1.3.1

* Thu Jun 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.30-1
- skopeo-1:0.1.30-2.dev.git28080c8
- bump to 0.1.30
- autobuilt 28080c8

* Wed Jun 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-14
- skopeo-1:1.3.1-14.dev.git8a1214a
- autobuilt 8a1214a

* Sat Jun 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-13
- skopeo-1:1.3.1-13.dev.gitccdaf6e
- autobuilt ccdaf6e

* Fri Jun 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-12
- skopeo-1:1.3.1-12.dev.git2fee990
- autobuilt 2fee990

* Thu Jun 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-11
- skopeo-1:1.3.1-11.dev.git5f8ec87
- autobuilt 5f8ec87

* Wed Jun 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-10
- skopeo-1:1.3.1-10.dev.git513a524
- autobuilt 513a524

* Mon Jun 14 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.3.1-9
- skopeo-1:1.3.1-9.dev.gitdde3e75
- update dependencies

* Sat Jun 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-8
- skopeo-1:1.3.1-8.dev.gitdde3e75
- autobuilt dde3e75

* Fri Jun 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-7
- skopeo-1:1.3.1-7.dev.gitec13aa6
- autobuilt ec13aa6

* Thu Jun 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-6
- skopeo-1:1.3.1-6.dev.gita07f1e0
- autobuilt a07f1e0

* Wed Jun 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-5
- skopeo-1:1.3.1-5.dev.gitb9661b2
- autobuilt b9661b2

* Thu May 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-4
- skopeo-1:1.3.1-4.dev.git714ffe1
- autobuilt 714ffe1

* Sat May 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-3
- skopeo-1:1.3.1-3.dev.git8efffce
- autobuilt 8efffce

* Fri May 21 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.3.1-2
- update install step

* Thu May 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.3.1-1
- skopeo-1:1.3.1-2.dev.git5af5f8a
- bump to 1.3.1
- autobuilt 5af5f8a

* Sat May 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.4-10
- skopeo-1:1.2.4-10.dev.git4e57679
- autobuilt 4e57679

* Tue May 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.4-9
- skopeo-1:1.2.4-9.dev.git0faf160
- autobuilt 0faf160

* Fri May 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.4-8
- skopeo-1:1.2.4-8.dev.gitb10d3e4
- autobuilt b10d3e4

* Thu May 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.4-7
- skopeo-1:1.2.4-7.dev.git5e13a55
- autobuilt 5e13a55

* Mon May 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.4-6
- skopeo-1:1.2.4-6.dev.gita1a8692
- autobuilt a1a8692

* Wed Apr 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.4-5
- skopeo-1:1.2.4-5.dev.gitce4304a
- autobuilt ce4304a

* Wed Apr 28 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.4-4
- bump containers-common dependency

* Mon Apr 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.4-3
- skopeo-1:1.2.4-4.dev.gitad9f1d7
- autobuilt ad9f1d7

* Tue Apr 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.4-2
- skopeo-1:1.2.4-3.dev.gitc84fc7d
- autobuilt c84fc7d

* Thu Apr 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.4-1
- skopeo-1:1.2.4-2.dev.git060fe4b
- bump to 1.2.4
- autobuilt 060fe4b

* Mon Mar 29 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-41
- skopeo-1:1.2.2-37.dev.git0717014
- autobuilt 0717014

* Mon Mar 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-40
- skopeo-1:1.2.2-36.dev.git6b41287
- autobuilt 6b41287

* Wed Mar 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-39
- skopeo-1:1.2.2-35.dev.gitf5a028e
- autobuilt f5a028e

* Tue Mar 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-38
- skopeo-1:1.2.2-34.dev.git3d1d297
- autobuilt 3d1d297

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-37
- skopeo-1:1.2.2-33.dev.git035eb33
- autobuilt 035eb33

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-36
- skopeo-1:1.2.2-32.dev.git6cbb0c4
- autobuilt 6cbb0c4

* Mon Mar 08 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-35
- skopeo-1:1.2.2-31.dev.git663fe44
- built commit 663fe44

* Thu Mar 04 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-34
- change %%global to %%define for built_tag macro

* Thu Mar 04 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-33
- update comment

* Thu Mar 04 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-32
- add additional macros for non-rawhide builds

* Wed Mar 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-31
- skopeo-1:1.2.2-30.dev.git6cbb0c4
- autobuilt 6cbb0c4

* Mon Mar 01 2021 Ed Santiago <santiago@redhat.com> - 1:1.2.2-30
- skopeo-tests: require openssl

* Mon Mar 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-29
- skopeo-1:1.2.2-29.dev.git663fe44
- autobuilt 663fe44

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-28
- skopeo-1:1.2.2-28.dev.gitb7bf15b
- autobuilt b7bf15b

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-27
- skopeo-1:1.2.2-27.dev.git61b62f9
- autobuilt 61b62f9

* Tue Feb 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-26
- skopeo-1:1.2.2-26.dev.git2c8655e
- autobuilt 2c8655e

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-25
- skopeo-1:1.2.2-25.dev.gitbe60097
- autobuilt be60097

* Wed Feb 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-24
- skopeo-1:1.2.2-24.dev.git15f0d5c
- autobuilt 15f0d5c

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-23
- skopeo-1:1.2.2-23.dev.git6fa6342
- autobuilt 6fa6342

* Wed Feb 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-22
- skopeo-1:1.2.2-22.dev.gite224b78
- autobuilt e224b78

* Tue Feb 09 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-21
- skopeo-1:1.2.2-21.dev.git1c4b0fc
- fix build and update containers-common dependency

* Mon Feb 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-20
- skopeo-1:1.2.2-20.dev.git1c4b0fc
- autobuilt 1c4b0fc

* Wed Feb 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-19
- skopeo-1:1.2.2-19.dev.gitaff1b62
- autobuilt aff1b62

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-18
- skopeo-1:1.2.2-18.dev.gite0ba05a
- autobuilt e0ba05a

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-17
- skopeo-1:1.2.2-17.dev.git55b9782
- autobuilt 55b9782

* Mon Feb 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-16
- skopeo-1:1.2.2-16.dev.git3375a90
- autobuilt 3375a90

* Sat Jan 30 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-15
- skopeo-1:1.2.2-15.dev.gitf3c8d26
- autobuilt f3c8d26

* Sat Jan 30 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-14
- skopeo-1:1.2.2-14.dev.gita9e9bdc
- autobuilt a9e9bdc

* Thu Jan 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-13
- skopeo-1:1.2.2-13.dev.git77a2e08
- autobuilt 77a2e08

* Thu Jan 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-12
- skopeo-1:1.2.2-12.dev.gita3c21f2
- autobuilt a3c21f2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-10
- skopeo-1:1.2.2-10.dev.gitefc0170
- autobuilt efc0170

* Thu Jan 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-9
- skopeo-1:1.2.2-9.dev.git0d0a97e
- autobuilt 0d0a97e

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-8
- skopeo-1:1.2.2-8.dev.gitef6f46a
- autobuilt ef6f46a

* Thu Jan 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-7
- skopeo-1:1.2.2-7.dev.git3156212
- autobuilt 3156212

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-6
- BR: git-core, not git

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-5
- skopeo-1:1.2.2-6.dev.git2e90a8a
- Requires: containers-common-4:0.33.0-2

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-4
- skopeo-1:1.2.2-5.dev.git2e90a8a
- depend on containers-common >= 4:0.33.0-1

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-3
- skopeo-1:1.2.2-4.dev.git2e90a8a
- depend on standalone containers-common package

* Mon Jan 11 2021 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.2-2
- Update documentaton for containers.conf, seccomp.json and new
  shortnames.conf

* Mon Jan 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-1
- skopeo-1:1.2.2-2.dev.git2e90a8a
- bump to 1.2.2
- autobuilt 2e90a8a

* Sun Jan 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-45
- skopeo-1:1.2.1-43.dev.gitbeadcbb
- autobuilt beadcbb

* Sat Jan 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-44
- skopeo-1:1.2.1-42.dev.gitac07bf2
- autobuilt ac07bf2

* Fri Jan 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-43
- skopeo-1:1.2.1-41.dev.gitb0da056
- autobuilt b0da056

* Fri Jan 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-42
- skopeo-1:1.2.1-40.dev.gitc4fb936
- autobuilt c4fb936

* Mon Jan 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-41
- skopeo-1:1.2.1-39.dev.git81535c5
- autobuilt 81535c5

* Wed Dec 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-40
- skopeo-1:1.2.1-38.dev.git84232cf
- autobuilt 84232cf

* Tue Dec 22 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.1-39
- Update man pages and conf files for containers-common

* Mon Dec 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-38
- skopeo-1:1.2.1-36.dev.git342b839
- autobuilt 342b839

* Sat Dec 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-37
- skopeo-1:1.2.1-35.dev.git6294875
- autobuilt 6294875

* Tue Dec 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-36
- skopeo-1:1.2.1-34.dev.git4769dd0
- autobuilt 4769dd0

* Tue Dec 08 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.1-35
- Update man pages and conf files for containers-common

* Tue Dec 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-34
- skopeo-1:1.2.1-32.dev.git4aaa9b4
- autobuilt 4aaa9b4

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-33
- skopeo-1:1.2.1-31.dev.gited32180
- autobuilt ed32180

* Sat Dec 05 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.1-32
- skopeo-1:1.2.1-30.dev.git5b8fe7f
- harden cgo binaries

* Sat Dec 05 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.1-31
- harden cgo based binaries

* Fri Dec 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-30
- skopeo-1:1.2.1-29.dev.git5b8fe7f
- autobuilt 5b8fe7f

* Wed Dec 02 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.1-29
- adjust btrfs for centos8

* Mon Nov 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-28
- skopeo-1:1.2.1-28.dev.git1b813f8
- autobuilt 1b813f8

* Tue Nov 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-27
- skopeo-1:1.2.1-27.dev.git42e9121
- autobuilt 42e9121

* Sat Nov 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-26
- skopeo-1:1.2.1-26.dev.gitc88576b
- autobuilt c88576b

* Fri Nov 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-25
- skopeo-1:1.2.1-25.dev.git0f4dc80
- autobuilt 0f4dc80

* Thu Nov 19 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.1-24
- autobuilt 7fee912

* Thu Nov 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-23
- skopeo-1:1.2.1-23.dev.git7fee912
- autobuilt 7fee912

* Wed Nov 18 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.1-22
- fix conditionals for btrfs-progs-devel

* Tue Nov 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-21
- skopeo-1:1.2.1-22.dev.git2342171
- autobuilt 2342171

* Mon Nov 16 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.1-20
- Add initial shortnames.conf file for expanding shortnames

* Mon Nov 16 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.1-19
- Update man pages and storage.conf

* Fri Nov 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-18
- skopeo-1:1.2.1-19.dev.git4ad2c75
- autobuilt 4ad2c75

* Thu Nov 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-17
- skopeo-1:1.2.1-18.dev.git11b4fd3
- autobuilt 11b4fd3

* Mon Nov 09 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.1-16
- Fix default ping range in containers.conf Allow setting of --remote
  default in containers.conf

* Sat Nov 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-15
- skopeo-1:1.2.1-16.dev.git1a3ae14
- autobuilt 1a3ae14

* Thu Nov 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-14
- skopeo-1:1.2.1-15.dev.git32e2425
- autobuilt 32e2425

* Tue Oct 27 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.1-13
- fix seccomp.json typos

* Thu Oct 22 2020 Jindrich Novy <jnovy@redhat.com> - 1:1.2.1-12
- skopeo-1.2.1-13.dev.gitceaee44
- use %%%%rhel instead of %%%%eln

* Wed Oct 21 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.1-11
- Add time64 syscalls to seccomp.json

* Wed Oct 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-10
- skopeo-1:1.2.1-11.dev.gitceaee44
- autobuilt ceaee44

* Thu Oct 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-9
- skopeo-1:1.2.1-10.dev.git362f70b
- autobuilt 362f70b

* Sat Oct 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-8
- skopeo-1:1.2.1-9.dev.git10da9f7
- autobuilt 10da9f7

* Thu Oct 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-7
- skopeo-1:1.2.1-8.dev.git4cc72b9
- autobuilt 4cc72b9

* Tue Oct 06 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.1-6
- skopeo-1:1.2.1-7.dev.git027d7e4
- no btrfs for eln or centos >= 8
- use old style changelogs without timezone/timestamp

* Sat Oct 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-5
- skopeo-1:1.2.1-6.dev.git027d7e4
- autobuilt 027d7e4

* Fri Oct 02 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.2.1-4
- Add SETFCAP back into default capabilities Remove AUDIT_WRITE from
  default capabilities

* Fri Oct 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-3
- skopeo-1:1.2.1-4.dev.gitd8bc8b6
- autobuilt d8bc8b6

* Wed Sep 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-2
- skopeo-1:1.2.1-3.dev.git6dabefa
- autobuilt 6dabefa

* Fri Sep 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-1
- skopeo-1:1.2.1-2.dev.git44beab6
- bump to 1.2.1
- autobuilt 44beab6

* Fri Sep 25 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.1.1-52
- Modify the range of groups used in net.ipv4.ping_group_range to be 1 so
  that it will work more easily with User Namespaces Also turn back on
  AUDIT_WRITE until seccomp.json file is fixed

* Mon Sep 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-51
- skopeo-1:1.1.1-50.dev.git8151b89
- autobuilt 8151b89

* Mon Sep 21 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.1.1-50
- Add SYS_CHROOT back into default capabilities

* Mon Sep 21 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.1.1-49
- Remove fchmodat2 from seccomp.json (This syscall does not exist yet)

* Fri Sep 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-48
- skopeo-1:1.1.1-47.dev.git77293ff
- autobuilt 77293ff

* Thu Sep 17 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.1.1-47
- Remove NET_RAW, SYS_CHROOT, MKNOD and AUDIT_WRITE from default list of
  capabilities Turn on ping for 65k users

* Tue Sep 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-46
- skopeo-1:1.1.1-45.dev.gitbbd800f
- autobuilt bbd800f

* Mon Sep 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-45
- skopeo-1:1.1.1-44.dev.git12ab19f
- autobuilt 12ab19f

* Sat Sep 12 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.1.1-44
- Update docs and seccomp files

* Fri Sep 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-43
- skopeo-1:1.1.1-42.dev.git45a9efb
- autobuilt 45a9efb

* Wed Sep 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-42
- skopeo-1:1.1.1-41.dev.git5dd09d7
- autobuilt 5dd09d7

* Wed Sep 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-41
- skopeo-1:1.1.1-40.dev.git23cb1b7
- autobuilt 23cb1b7

* Wed Sep 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-40
- skopeo-1:1.1.1-39.dev.git662f9ac
- autobuilt 662f9ac

* Wed Sep 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-39
- skopeo-1:1.1.1-38.dev.gitae26454
- autobuilt ae26454

* Fri Aug 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-38
- skopeo-1:1.1.1-37.dev.gitc4998eb
- autobuilt c4998eb

* Thu Aug 27 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-37
- skopeo-1:1.1.1-36.dev.gita13b581
- autobuilt a13b581

* Tue Aug 25 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.1.1-36
- update build rules

* Mon Aug 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-35
- skopeo-1:1.1.1-35.dev.git87484a1
- autobuilt 87484a1

* Wed Aug 19 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.1.1-34
- Update configuration files in containers-common Update configuration
  files in containers-storage

* Wed Aug 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-33
- skopeo-1:1.1.1-33.dev.git5d5756c
- autobuilt 5d5756c

* Wed Aug 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-32
- skopeo-1:1.1.1-32.dev.git88c8c47
- autobuilt 88c8c47

* Tue Aug 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-31
- skopeo-1:1.1.1-31.dev.gitea10e61
- autobuilt ea10e61

* Mon Aug 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-30
- skopeo-1:1.1.1-30.dev.git0c2c7f4
- autobuilt 0c2c7f4

* Sun Aug 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-29
- skopeo-1:1.1.1-29.dev.git0f94dbc
- autobuilt 0f94dbc

* Sat Aug 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-28
- skopeo-1:1.1.1-28.dev.gitbaeaad6
- autobuilt baeaad6

* Fri Aug 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-27
- skopeo-1:1.1.1-27.dev.git78d2f67
- autobuilt 78d2f67

* Mon Aug 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-26
- skopeo-1:1.1.1-26.dev.gitc052ed7
- autobuilt c052ed7

* Mon Aug 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-25
- skopeo-1:1.1.1-25.dev.git5e88eb5
- autobuilt 5e88eb5

* Sun Aug 02 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.1.1-24
- Update configuration files in containers-common Update configuration
  files in containers-storage

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-23
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-22
- skopeo-1:1.1.1-22.dev.git62fd5a7
- autobuilt 62fd5a7

* Thu Jul 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-21
- skopeo-1:1.1.1-21.dev.git6252c22
- autobuilt 6252c22

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-19
- skopeo-1:1.1.1-19.dev.git153f18d
- autobuilt 153f18d

* Mon Jul 20 2020 Ed Santiago <santiago@redhat.com> - 1:1.1.1-18
- skopeo-tests package now requires httpd-tools for htpasswd, which was
  disastrously removed from the docker.io/registry image. Skopeo tests now
  run htpasswd directly on the host.

* Sat Jul 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-17
- skopeo-1:1.1.1-18.dev.git494d237
- autobuilt 494d237

* Fri Jul 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-16
- skopeo-1:1.1.1-17.dev.git89fb89a
- autobuilt 89fb89a

* Thu Jul 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-15
- skopeo-1:1.1.1-16.dev.git29eec32
- autobuilt 29eec32

* Thu Jul 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-14
- skopeo-1:1.1.1-15.dev.git2fa7b99
- autobuilt 2fa7b99

* Sat Jul 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-13
- skopeo-1:1.1.1-14.dev.git6284ceb
- autobuilt 6284ceb

* Sat Jul 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-12
- skopeo-1:1.1.1-13.dev.git6e295a2
- autobuilt 6e295a2

* Fri Jul 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-11
- skopeo-1:1.1.1-12.dev.gitf63685f
- autobuilt f63685f

* Thu Jul 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-10
- skopeo-1:1.1.1-11.dev.gitdc5f68f
- autobuilt dc5f68f

* Thu Jul 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-9
- skopeo-1:1.1.1-10.dev.git840c487
- autobuilt 840c487

* Wed Jul 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-8
- skopeo-1:1.1.1-9.dev.gitee72e80
- autobuilt ee72e80

* Thu Jul 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-7
- skopeo-1:1.1.1-8.dev.git6182aa3
- autobuilt 6182aa3

* Wed Jul 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-6
- skopeo-1:1.1.1-7.dev.gitac6b871
- autobuilt ac6b871

* Tue Jun 30 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.1.1-5
- Update configuration files in containers-common

* Fri Jun 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-4
- skopeo-1:1.1.1-5.dev.gitba8cbf5
- autobuilt ba8cbf5

* Mon Jun 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-3
- skopeo-1:1.1.1-4.dev.git7815c8a
- autobuilt 7815c8a

* Mon Jun 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-2
- skopeo-1:1.1.1-3.dev.git233e61c
- autobuilt 233e61c

* Thu Jun 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-1
- skopeo-1:1.1.1-2.dev.git96bd4a0
- bump to 1.1.1
- autobuilt 96bd4a0

* Thu Jun 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-18
- skopeo-1:1.0.1-17.dev.git6b78619
- autobuilt 6b78619

* Wed Jun 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-17
- skopeo-1:1.0.1-16.dev.git091f924
- autobuilt 091f924

* Wed Jun 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-16
- skopeo-1:1.0.1-15.dev.gitb70dfae
- autobuilt b70dfae

* Tue Jun 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-15
- skopeo-1:1.0.1-14.dev.git0bd78a0
- autobuilt 0bd78a0

* Thu Jun 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-14
- skopeo-1:1.0.1-13.dev.git827293a
- autobuilt 827293a

* Thu Jun 11 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.0.1-13
- Update man pages

* Thu Jun 11 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:1.0.1-12
- Update man pages

* Wed Jun 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-11
- skopeo-1:1.0.1-10.dev.git161ef5a
- autobuilt 161ef5a

* Thu Jun 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-10
- skopeo-1:1.0.1-9.dev.gitf9b0d93
- autobuilt f9b0d93

* Fri May 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-9
- skopeo-1:1.0.1-8.dev.gitc6b488a
- autobuilt c6b488a

* Mon May 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-8
- skopeo-1:1.0.1-7.dev.gita2c1d46
- autobuilt a2c1d46

* Mon May 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-7
- skopeo-1:1.0.1-6.dev.git8b4b954
- autobuilt 8b4b954

* Sat May 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-6
- skopeo-1:1.0.1-5.dev.git3a94432
- autobuilt 3a94432

* Thu May 21 2020 Ed Santiago <santiago@redhat.com> - 1:1.0.1-5
- gating.yaml: duplicate the stanzas

* Thu May 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-4
- skopeo-1:1.0.1-4.dev.git96353f2
- autobuilt 96353f2

* Thu May 21 2020 Aleksandra Fedorova <afedorova@redhat.com> - 1:1.0.1-3
- Update gating test name

* Wed May 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-2
- skopeo-1:1.0.1-3.dev.git91a88de
- autobuilt 91a88de

* Mon May 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-1
- skopeo-1:1.0.1-2.dev.gitdcaee94
- bump to 1.0.1
- autobuilt dcaee94

* Mon May 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-17
- skopeo-1:0.2.0-12.dev.gita214a30
- autobuilt a214a30

* Fri May 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-16
- skopeo-1:0.2.0-11.dev.git0d9939d
- autobuilt 0d9939d

* Thu May 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-15
- skopeo-1:0.2.0-10.dev.gitfbf0612
- autobuilt fbf0612

* Thu May 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-14
- skopeo-1:0.2.0-9.dev.git2af1726
- autobuilt 2af1726

* Tue May 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-13
- skopeo-1:0.2.0-8.dev.git4ca9b13
- autobuilt 4ca9b13

* Mon May 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-12
- skopeo-1:0.2.0-7.dev.git71a14d7
- autobuilt 71a14d7

* Mon May 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-11
- skopeo-1:0.2.0-6.dev.git8936e76
- autobuilt 8936e76

* Mon May 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-10
- skopeo-1:0.2.0-5.dev.gita6ab229
- autobuilt a6ab229

* Sun May 10 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.2.0-9
- skopeo-1:0.2.0-4.dev.git42f68c1
- bump release tag for smooth upgrade path from f32

* Sat May 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-8
- skopeo-1:0.2.0-0.8.dev.git42f68c1
- autobuilt 42f68c1

* Tue May 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-7
- skopeo-1:0.2.0-0.7.dev.git1ddb736
- autobuilt 1ddb736

* Mon May 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-6
- skopeo-1:0.2.0-0.6.dev.gite7a7f01
- autobuilt e7a7f01

* Fri May 01 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:0.2.0-5
- Fix containers-registries.conf.5 man page to match upstream

* Wed Apr 29 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:0.2.0-4
- Fix registries.conf file to correctly pass the unqualified-search-
  registries

* Sat Apr 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-3
- skopeo-1:0.2.0-0.3.dev.gitb230a50
- autobuilt b230a50

* Fri Apr 24 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:0.2.0-2
- Update registries.conf to use version 2 definitions Update
  containers.conf to include latest changes Update seccomp.json to allow a
  few more syscalls for contaners within containers. Update storage.conf to
  match upstream

* Thu Apr 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-1
- skopeo-1:0.2.0-0.1.dev.git2415f3f
- bump to 0.2.0
- autobuilt 2415f3f

* Thu Apr 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-25
- skopeo-1:0.1.42-8.0.dev.git2d91b93
- autobuilt 2d91b93

* Wed Apr 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-24
- skopeo-1:0.1.42-7.0.dev.git101901a
- autobuilt 101901a

* Wed Apr 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-23
- skopeo-1:0.1.42-6.0.dev.git9d21b48
- autobuilt 9d21b48

* Wed Apr 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-22
- skopeo-1:0.1.42-5.0.dev.git9d63c7c
- autobuilt 9d63c7c

* Tue Apr 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-21
- skopeo-1:0.1.42-4.0.dev.git6ac3dce
- autobuilt 6ac3dce

* Tue Apr 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-20
- skopeo-1:0.1.42-3.0.dev.git71a8ff0
- autobuilt 71a8ff0

* Tue Apr 07 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.42-19
- Update man pages to match upstream

* Tue Apr 07 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.42-18
- Add support for containers.conf and man page

* Mon Apr 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-17
- skopeo-1:0.1.42-0.16.dev.git8fa3326
- autobuilt 8fa3326

* Tue Mar 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-16
- skopeo-1:0.1.42-0.15.dev.git5d512e2
- autobuilt 5d512e2

* Tue Mar 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-15
- skopeo-1:0.1.42-0.14.dev.git3e9d8ae
- autobuilt 3e9d8ae

* Tue Mar 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-14
- skopeo-1:0.1.42-0.13.dev.gitbd20786
- autobuilt bd20786

* Mon Mar 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-13
- skopeo-1:0.1.42-0.12.dev.git6db5626
- autobuilt 6db5626

* Mon Mar 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-12
- skopeo-1:0.1.42-0.11.dev.giteb199dc
- autobuilt eb199dc

* Mon Mar 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-11
- skopeo-1:0.1.42-0.10.dev.git018a010
- autobuilt 018a010

* Sat Mar 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-10
- skopeo-1:0.1.42-0.9.dev.gita6f5ef1
- autobuilt a6f5ef1

* Wed Mar 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-9
- skopeo-1:0.1.42-0.8.dev.git501452a
- autobuilt 501452a

* Fri Mar 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-8
- skopeo-1:0.1.42-0.7.dev.gite31d5a0
- autobuilt e31d5a0

* Fri Mar 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-7
- skopeo-1:0.1.42-0.6.dev.git7fee7d5
- autobuilt 7fee7d5

* Thu Mar 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-6
- skopeo-1:0.1.42-0.5.dev.git12865fd
- autobuilt 12865fd

* Thu Mar 19 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.42-5
- correct changelog order and release tag

* Thu Mar 19 2020 Jonathan Lebon <jonathan@jlebon.com> - 1:0.1.42-4
- skopeo.spec: drop [/var]/srv/containers from file list

* Thu Mar 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-3
- skopeo-1:0.1.42-0.3.dev.git7170702
- autobuilt 7170702

* Wed Mar 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-2
- skopeo-1:0.1.42-0.2.dev.gitb541fef
- autobuilt b541fef

* Mon Mar 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-1
- skopeo-1:0.1.42-0.1.dev.git7a0a8c2
- bump to 0.1.42
- autobuilt 7a0a8c2

* Mon Feb 17 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.41-38
- Allow s390x to use clone syscall in seccomp.json Add support for
  containers.conf and man page

* Thu Feb 13 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.41-37
- epoch: 2 for centos to override appstream package

* Thu Feb 06 2020 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.41-36
- Remove quay.io from list of search registries, removes risk of squatters.
  Update man pages to match upstream

* Mon Feb 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.41-35
- no debuginfo for centos

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.1.41-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-33
- skopeo-1:0.1.41-24.dev.git7cbb8ad
- autobuilt 7cbb8ad

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-32
- skopeo-1:0.1.41-23.dev.git4489ddd
- autobuilt 4489ddd

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-31
- skopeo-1:0.1.41-22.dev.git763e488
- autobuilt 763e488

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-30
- skopeo-1:0.1.41-21.dev.gite955849
- autobuilt e955849

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-29
- skopeo-1:0.1.41-20.dev.git8652b65
- autobuilt 8652b65

* Mon Dec 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-28
- skopeo-1:0.1.41-19.dev.gitc3e6b4f
- autobuilt c3e6b4f

* Mon Dec 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-27
- skopeo-1:0.1.41-18.dev.git5291aac
- autobuilt 5291aac

* Mon Dec 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-26
- skopeo-1:0.1.41-17.dev.git407f2e9
- autobuilt 407f2e9

* Sat Dec 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-25
- skopeo-1:0.1.41-16.dev.gite8d49d6
- autobuilt e8d49d6

* Wed Dec 04 2019 Dusty Mabe <dusty@dustymabe.com> - 1:0.1.41-24
- mounts: update symlink name from rhel7.repo to redhat.repo

* Mon Dec 02 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.41-23
- Change default order of registries.conf to push docker.io to the back.
  Allo clock_adjtime by default in seccomp.json since it can be used in
  read/only mode

* Mon Dec 02 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.41-22
- Change default order of registries.conf to push docker.io to the back.

* Mon Dec 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-21
- skopeo-1:0.1.41-12.dev.git9c402f3
- autobuilt 9c402f3

* Mon Dec 02 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.41-20
- Update man pages to reflect upstream sources Also update storage.conf to
  remove skip_mount_home which is no longer supported.

* Sat Nov 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-19
- skopeo-1:0.1.41-10.dev.git3ed6e83
- autobuilt 3ed6e83

* Thu Nov 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-18
- skopeo-1:0.1.41-9.dev.git73248bd
- autobuilt 73248bd

* Wed Nov 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-17
- skopeo-1:0.1.41-8.dev.git2bfa895
- autobuilt 2bfa895

* Tue Nov 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-16
- skopeo-1:0.1.41-7.dev.gitce6ec77
- autobuilt ce6ec77

* Tue Nov 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-15
- skopeo-1:0.1.41-6.dev.git912b7e1
- autobuilt 912b7e1

* Mon Nov 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-14
- skopeo-1:0.1.41-5.dev.git34ab4c4
- autobuilt 34ab4c4

* Fri Nov 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-13
- skopeo-1:0.1.41-4.dev.git39540db
- autobuilt 39540db

* Thu Nov 21 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.41-12
- Update to use new storage.conf configuration files.

* Tue Nov 19 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.41-11
- add clock_adjtime as valid syscall when CAP_SYS_TIME added

* Fri Nov 08 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.41-10
- Change default search order on registries.conf. Quay.io should be last to
  make sure no one is squating on repos that are provided by upstream
  packages.

* Sat Nov 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-9
- skopeo-1:0.1.41-0.9.dev.git24f4f82
- autobuilt 24f4f82

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-8
- skopeo-1:0.1.41-0.8.dev.git332bb45
- autobuilt 332bb45

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-7
- skopeo-1:0.1.41-0.7.dev.git307d9c2
- autobuilt 307d9c2

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-6
- skopeo-1:0.1.41-0.6.dev.git1094c7d
- autobuilt 1094c7d

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-5
- skopeo-1:0.1.41-0.5.dev.git75b7d1e
- autobuilt 75b7d1e

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-4
- skopeo-1:0.1.41-0.4.dev.git10d0ebb
- autobuilt 10d0ebb

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-3
- skopeo-1:0.1.41-0.3.dev.git02432cf
- autobuilt 02432cf

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-2
- skopeo-1:0.1.41-0.2.dev.git153520e
- autobuilt 153520e

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-1
- skopeo-1:0.1.41-0.1.dev.gita263b35
- bump to 0.1.41
- autobuilt a263b35

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-19
- skopeo-1:0.1.40-0.17.dev.git8057da7
- autobuilt 8057da7

* Tue Oct 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-18
- skopeo-1:0.1.40-0.16.dev.git4b6a5da
- autobuilt 4b6a5da

* Wed Oct 16 2019 Ed Santiago <santiago@redhat.com> - 1:0.1.40-17
- enable gating tests

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-16
- skopeo-1:0.1.40-0.15.dev.git5f9a6ea
- autobuilt 5f9a6ea

* Tue Oct 15 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-15
- skopeo-1:0.1.40-0.14.dev.git5b0a789
- autobuilt 5b0a789

* Tue Oct 15 2019 Ed Santiago <santiago@redhat.com> - 1:0.1.40-14
- New subpackage: skopeo-tests intended for use in fedora gating tests.
  Subpackage already exists in RHEL8.

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-13
- skopeo-1:0.1.40-0.13.dev.gitf72e39f
- autobuilt f72e39f

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-12
- skopeo-1:0.1.40-0.12.dev.git881edbf
- autobuilt 881edbf

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-11
- skopeo-1:0.1.40-0.11.dev.gitfa6e580
- autobuilt fa6e580

* Thu Sep 19 2019 Michael Nguyen <mnguyen@redhat.com> - 1:0.1.40-10
- containers-common: create /srv/containers and /var/srv/containers

* Wed Sep 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-9
- skopeo-1:0.1.40-0.9.dev.git7eb5f39
- autobuilt 7eb5f39

* Sat Sep 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-8
- skopeo-1:0.1.40-0.8.dev.git5ae6b16
- autobuilt 5ae6b16

* Tue Sep 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-7
- skopeo-1:0.1.40-0.7.dev.git18f0e1e
- autobuilt 18f0e1e

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-6
- skopeo-1:0.1.40-0.6.dev.git9019e27
- autobuilt 9019e27

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-5
- skopeo-1:0.1.40-0.5.dev.gitc4b0c7c
- autobuilt c4b0c7c

* Mon Aug 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-4
- skopeo-1:0.1.40-0.4.dev.git1e2d6f6
- autobuilt 1e2d6f6

* Thu Aug 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-3
- skopeo-1:0.1.40-0.3.dev.git481bb94
- autobuilt 481bb94

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-2
- skopeo-1:0.1.40-0.2.dev.gitee9e9df
- autobuilt ee9e9df

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-1
- skopeo-1:0.1.40-0.1.dev.git44bc4a9
- bump to 0.1.40
- autobuilt 44bc4a9

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.39-2
- skopeo-1:0.1.39-0.2.dev.gitc040b28
- autobuilt c040b28

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.39-1
- skopeo-1:0.1.39-0.1.dev.git202c1ea
- bump to 0.1.39
- autobuilt 202c1ea

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-12
- skopeo-1:0.1.38-9.dev.gitbf8089c
- autobuilt bf8089c

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-11
- skopeo-1:0.1.38-8.dev.git65b3aa9
- autobuilt 65b3aa9

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-10
- skopeo-1:0.1.38-7.dev.git19025f5
- autobuilt 19025f5

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-9
- skopeo-1:0.1.38-6.dev.git2ad9ae5
- autobuilt 2ad9ae5

* Wed Jul 31 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.38-8
- built_tag macro records exact upstream tag built

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-7
- skopeo-1:0.1.38-5.dev.git8a9641c
- autobuilt 8a9641c

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-6
- skopeo-1:0.1.38-4.dev.gitb58088a
- autobuilt b58088a

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-5
- skopeo-1:0.1.38-3.dev.git5f45112
- autobuilt 5f45112

* Thu Jul 18 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.38-4
- cleanup warnings

* Thu Jul 18 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.38-3
- update release tag, and BR: go-md2man

* Tue Jul 09 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.38-2
- Update containers-registries.conf.md man page for mirroring support
  Update regsitries.conf file to match containers/image

* Mon Jun 24 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.38-1
- Bump up to 1:0.1.38

* Thu May 16 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.36-22
- Add metacopy=on flag to storage.conf

* Sun May 05 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.36-21
- Update man pages and add missing man pages to containers-common.

* Fri Apr 26 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.36-20
- skopeo-1:0.1.36-17.dev.git0fa335c
- Fixes @openshift/machine-config-operator#669
- install /etc/containers/oci/hooks.d

* Wed Apr 24 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.36-19
- Fix location of sigstore atomic->containers

* Wed Apr 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-18
- skopeo-1:0.1.36-15.dev.git0fa335c
- autobuilt 0fa335c

* Thu Apr 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-17
- skopeo-1:0.1.36-14.dev.git2af7114
- autobuilt 2af7114

* Wed Apr 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-16
- skopeo-1:0.1.36-13.dev.gite255ccc
- autobuilt e255ccc

* Sat Apr 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-15
- skopeo-1:0.1.36-12.dev.git18ee5f8
- autobuilt 18ee5f8

* Fri Apr 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-14
- skopeo-1:0.1.36-11.dev.git81c5e94
- autobuilt 81c5e94

* Thu Apr 11 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.36-13
- add containers-storage.conf man page

* Thu Apr 11 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.36-12
- add containers-storage.conf man page

* Tue Apr 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-11
- skopeo-1:0.1.36-9.dev.gitc73bcba
- autobuilt c73bcba

* Thu Mar 28 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.36-10
- Rename registries.conf.5 to containers-registries.conf.5

* Thu Mar 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-9
- skopeo-1:0.1.36-8.dev.git854f766
- autobuilt 854f766

* Wed Mar 27 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.36-8
- Allow for multiple man pages.

* Tue Mar 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-7
- skopeo-1:0.1.36-7.dev.git0975497
- autobuilt 0975497

* Tue Mar 19 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.36-6
- make /usr/share/rhel/secrets world searchable.   This will help allow
  RHEL containers to be built with rootless.

* Thu Mar 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-5
- skopeo-1:0.1.36-5.dev.gitd93a581
- autobuilt d93a581

* Wed Mar 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-4
- skopeo-1:0.1.36-4.dev.git94728fb
- autobuilt 94728fb

* Thu Mar 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-3
- skopeo-1:0.1.36-3.dev.git0490018
- autobuilt 0490018

* Wed Mar 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-2
- skopeo-1:0.1.36-2.dev.git2031e17
- autobuilt 2031e17

* Tue Mar 05 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.36-1
- Bump version

* Sat Mar 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-16
- skopeo-1:0.1.35-14.dev.git2134209
- autobuilt 2134209

* Fri Mar 01 2019 Daniel J Walsh <dwalsh@redhat.com> - 1:0.1.35-15
- Add /etc/containers/certs.d to containers-common Update containers-
  storage.conf man page to match latest upstream Update registries.conf man
  page to match latest upstream

* Sat Feb 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-14
- skopeo-1:0.1.35-12.dev.git932b037
- autobuilt 932b037

* Sun Feb 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-13
- skopeo-1:0.1.35-11.dev.gitfee5981
- autobuilt fee5981

* Thu Feb 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-12
- skopeo-1:0.1.35-10.dev.gitb8b9913
- autobuilt b8b9913

* Wed Feb 13 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.35-11
- hardcode epoch value for module builds

* Wed Feb 13 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.35-10
- skopeo-1:0.1.35-9.dev.gitb329dd0
- drop conditional epoch for containers-common, module build seems to fail

* Wed Feb 13 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.35-9
- skopeo-1:0.1.35-8.dev.gitb329dd0
- Epoch changes for containers-common

* Wed Feb 13 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.35-8
- epoch 0 if fedora <= 28

* Wed Feb 13 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.35-7
- correct epoch info for containers-common

* Fri Feb 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-6
- skopeo-1:0.1.35-7.dev.gitb329dd0
- autobuilt b329dd0

* Sat Feb 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-5
- skopeo-1:0.1.35-6.dev.gitbba2874
- autobuilt bba2874

* Fri Jan 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-4
- skopeo-1:0.1.35-5.dev.git42b01df
- autobuilt 42b01df

* Wed Jan 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-3
- skopeo-1:0.1.35-4.dev.gitf7c608e
- autobuilt f7c608e

* Sat Jan 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-2
- skopeo-1:0.1.35-3.dev.git17bea86
- autobuilt 17bea86

* Sat Dec 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-1
- skopeo-1:0.1.35-2.dev.git3e98377
- bump to 0.1.35
- autobuilt 3e98377

* Thu Dec 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.34-1
- skopeo-1:0.1.34-2.dev.git05212df
- bump to 0.1.34
- autobuilt 05212df

* Wed Dec 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-6
- skopeo-1:0.1.33-6.dev.gitecd675e
- autobuilt ecd675e

* Sat Dec 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-5
- skopeo-1:0.1.33-5.dev.gita51e38e
- autobuilt a51e38e

* Fri Dec 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-4
- skopeo-1:0.1.33-4.dev.git41d8dd8
- autobuilt 41d8dd8

* Fri Nov 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-3
- skopeo-1:0.1.33-3.dev.gitfbc2e4f
- autobuilt fbc2e4f

* Fri Nov 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-2
- skopeo-1:0.1.33-2.dev.git761a681
- autobuilt 761a681

* Thu Nov 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.33-1
- skopeo-1:0.1.33-1.dev.git.git5aa217f
- bump to 0.1.33
- built commit 5aa217f

* Thu Nov 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.32-4
- upstream moved from projectatomic to containers

* Fri Aug 24 2018 Colin Walters <walters@verbum.org> - 1:0.1.32-3
- build: Make Epoch conditional

* Sat Aug 18 2018 Kevin Fenzi <kevin@scrye.com> - 1:0.1.32-2
- Fix containers-common requires to also use Epoch so skopeo is installable
  again.

* Sun Aug 12 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.32-1
- skopeo-1:0.1.32-1.dev.gite814f96
- bump to v0.1.32-dev
- built commit e814f96
- bump Epoch to 1, cause my autobuilder messed up earlier
- use %%%%gobuild
- add bundled Provides

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.1.320.1.32-3
- Rebuild with fixed binutils

* Mon Jul 30 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.320.1.32-2
- Update to latest registries.conf man page

* Mon Jul 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.320.1.32-1
- skopeo-0.1.320.1.32-1.dev.gite814f961
- bump to 0.1.32
- autobuilt e814f96

* Wed Jul 25 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.31-17
- Update to latest storage.conf file Update to latest man pages

* Wed Jul 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-16
- skopeo-0.1.31-12.dev.gite3034e1
- autobuilt e3034e1

* Tue Jul 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-15
- skopeo-0.1.31-11.dev.gitae64ff7
- Resolves: #1606365 - solve FTBFS - disable debuginfo for rawhide (f29)
- remove centos conditionals, CentOS Virt SIG gets rhel rebuilds

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.31-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-13
- update release tag to reflect unreleased status

* Mon Jul 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-12
- skopeo-0.1.31-9.gitae64ff7
- autobuilt ae64ff7

* Tue Jul 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-11
- skopeo-0.1.31-8.git196bc48
- autobuilt 196bc48

* Sat Jun 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-10
- skopeo-0.1.31-7.git6e23a32
- autobuilt 6e23a32

* Thu Jun 21 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.31-9
- add statx to seccomp.json to containers-config

* Tue Jun 12 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-8
- Conflicts with atomic-registries should be for containers-common and not
  skopeo-devel

* Thu Jun 07 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.31-7
- add seccomp.json to containers-config

* Thu May 31 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-6
- skopeo-0.1.31-4.git0144aa8
- autobuilt 0144aa8

* Wed May 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-5
- skopeo-0.1.31-3.gitf9baaa6
- should obsolete older skopeo-containers

* Wed May 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-4
- skopeo-0.1.31-2.gitf9baaa6
- rename skopeo-containers to containers-common
- enable debuginfo

* Wed May 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-3
- packaging changes
- enable debuginfo
- rename skopeo-containers to containers-common

* Mon May 28 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-2
- add CentOS registry

* Sat May 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-1
- skopeo-0.1.31-1.gitf9baaa6
- bump to 0.1.31
- autobuilt f9baaa6

* Tue May 22 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.30-19
- Add devicemapper support

* Tue May 22 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.30-18
- Add devicemapper support

* Sun May 20 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.30-17
- Add devicemapper support

* Sun May 20 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.30-16
- Add devicemapper support

* Sat May 19 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.30-15
- Add new configuration for devicemapper support in containers/storage

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-14
- skopeo-0.1.30-13.git7e9a664
- autobuilt 7e9a664

* Tue May 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-13
- skopeo-0.1.30-12.git2d04db9
- autobuilt 2d04db9

* Sat May 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-12
- skopeo-0.1.30-11.git79225f2
- autobuilt 79225f2

* Fri May 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-11
- skopeo-0.1.30-10.gitc4808f0
- autobuilt c4808f0

* Tue May 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-10
- skopeo-0.1.30-9.git1f11b8b
- autobuilt 1f11b8b

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-9
- skopeo-0.1.30-8.gitab2bc6e
- autobuilt commit ab2bc6e

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-8
- skopeo-0.1.30-7.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-7
- skopeo-0.1.30-6.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-6
- skopeo-0.1.30-5.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-5
- skopeo-0.1.30-4.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-4
- skopeo-0.1.30-3.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.30-3
- BR: make

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-2
- skopeo-0.1.30-2.gitab2bc6e
- autobuilt commit ab2bc6e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.30-1
- skopeo-0.1.30-1.git28080c8
- bump to 0.1.30
- autobuilt commit 28080c8

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.29-9
- formatting changes

* Tue Apr 03 2018 baude <bbaude@redhat.com> - 0.1.29-8
- small typo fix

* Tue Apr 03 2018 baude <bbaude@redhat.com> - 0.1.29-7
- Remove bad character in registries.conf

* Tue Apr 03 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.29-6
- Add policy.json.5

* Mon Apr 02 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.29-5
- Add registries.conf

* Mon Apr 02 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.29-4
- Add registries.conf

* Mon Apr 02 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.29-3
- Add registries.conf

* Mon Apr 02 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.29-2
- Add registries.conf man page

* Thu Mar 29 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.29-1
- bump to 0.1.29-1 Updated containers/image docker-archive generates docker
  legacy compatible images Do not create $DiffID subdirectories for layers
  with no configs Ensure the layer IDs in legacy docker/tarfile metadata
  are unique docker-archive: repeated layers are symlinked in the tar file
  sysregistries: remove all trailing slashes Improve docker/* error
  messages Fix failure to make auth directory Create a new slice in
  Schema1.UpdateLayerInfos Drop unused
  storageImageDestination.{image,systemContext} Load a *storage.Image only
  once in storageImageSource Support gzip for docker-archive files Remove
  .tar extension from blob and config file names ostree, src: support copy
  of compressed layers ostree: re-pull layer if it misses
  uncompressed_digest|uncompressed_size image: fix docker schema v1 -> OCI
  conversion Add /etc/containers/certs.d as default certs directory

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.1.28-1
- Vendor in fixed libraries in containers/image and containers/storage

* Wed Jan 17 2018 Colin Walters <walters@verbum.org> - 0.1.27-3
- Revert "remove git and ostree from build deps"

* Mon Dec 04 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.27-2
- remove git and ostree from build deps

* Wed Nov 22 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.27-1
- Fix Conflicts to Obsoletes Add better docs to man pages. Use credentials
  from authfile for skopeo commands Support storage="" in
  /etc/containers/storage.conf Add global --override-arch and --override-os
  options

* Wed Nov 15 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.26-1
- Add manifest type conversion to skopeo copy User can select from 3
  manifest types: oci, v2s1, or v2s2 e.g skopeo copy --format v2s1
  --compress-blobs docker-archive:alp.tar dir:my-directory

* Wed Nov 08 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.25-2
- Force storage.conf to default to overlay

* Wed Nov 08 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.25-1
- Fix CVE in tar-split copy: add shared blob directory support for OCI
  sources/destinations Aligning Docker version between containers/image and
  skopeo Update image-tools, and remove the duplicate Sirupsen/logrus
  vendor makefile: use -buildmode=pie

* Tue Nov 07 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.24-9
- Add /usr/share/containers/mounts.conf

* Sun Oct 22 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.24-8
- Bug fixes Update to release

* Tue Oct 17 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.24-7
- skopeo-0.1.24-6.dev.git28d4e08
- skopeo-containers conflicts with docker-rhsubscription <= 2:1.13.1-31

* Tue Oct 17 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.24-6
- Add rhel subscription secrets data to skopeo-containers

* Thu Oct 12 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.24-5
- Update container/storage.conf and containers-storage.conf man page
  Default override to true so it is consistent with RHEL.

* Tue Oct 10 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.24-4
- skopeo-0.1.24-3.dev.git28d4e08
- built commit 28d4e08

* Mon Sep 18 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.24-3
- skopeo-0.1.24-2.dev.git875dd2e
- built commit 875dd2e
- Resolves: gh#416

* Tue Sep 12 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.24-2
- cosmetic changes
- correct a prior bogus date
- fix macro in comment warning

* Tue Sep 12 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.24-1
- skopeo-0.1.24-1.dev.gita41cd0
- bump to 0.1.24-dev
- switch back to projectatomic/skopeo

* Mon Aug 21 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.23-6
- Change name of storage.conf.5 man page to containers-storage.conf.5,
  since it conflicts with inn package Also remove default to "overalay" in
  the configuration, since we should allow containers storage to pick the
  best default for the platform.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.23-5
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 0.1.23-4
- Rebuild with fixed binutils for ppc64le (#1475636)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.23-2
- Fix storage.conf man page to be storage.conf.5.gz so that it works.

* Fri Jul 21 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.23-1
- Support for OCI V1.0 Images Update to image-spec v1.0.0 and revendor
  Fixes for authentication

* Sat Jul 01 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.22-2
- set Epoch: 1 for CentOS

* Wed Jun 21 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.22-1
- Give more useful help when explaining usage Also specify container-
  storage as a valid transport Remove docker reference wherever possible
  vendor in ostree fixes

* Tue Jun 20 2017 Colin Walters <walters@verbum.org> - 0.1.21-6
- Use Patch0 so rpmdistro-gitoverlay removes it

* Fri Jun 16 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.21-5
- Add support for storage.conf and storage-config.5.md from github
  container storage package Bump to the latest version of skopeo
  vendor.conf: add ostree-go it is used by containers/image for pulling
  images to the OSTree storage. fail early when image os does not match
  host os Improve documentation on what to do with containers/image
  failures in test-skopeo We now have the docker-archive: transport
  Integration tests with built registries also exist Support
  /etc/docker/certs.d update image-spec to v1.0.0-rc6

* Fri Jun 16 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.21-4
- Add support for storage.conf and storage-config.5.md from github
  container storage package Bump to the latest version of skopeo
  vendor.conf: add ostree-go it is used by containers/image for pulling
  images to the OSTree storage. fail early when image os does not match
  host os Improve documentation on what to do with containers/image
  failures in test-skopeo We now have the docker-archive: transport
  Integration tests with built registries also exist Support
  /etc/docker/certs.d update image-spec to v1.0.0-rc6

* Thu Jun 15 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.21-3
- Add support for storage.conf and storage-config.5.md from github
  container storage package Bump to the latest version of skopeo
  vendor.conf: add ostree-go it is used by containers/image for pulling
  images to the OSTree storage. fail early when image os does not match
  host os Improve documentation on what to do with containers/image
  failures in test-skopeo We now have the docker-archive: transport
  Integration tests with built registries also exist Support
  /etc/docker/certs.d update image-spec to v1.0.0-rc6

* Thu Jun 15 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.21-2
- Add support for storage.conf and storage-config.5.md from github
  container storage package Bump to the latest version of skopeo
  vendor.conf: add ostree-go it is used by containers/image for pulling
  images to the OSTree storage. fail early when image os does not match
  host os Improve documentation on what to do with containers/image
  failures in test-skopeo We now have the docker-archive: transport
  Integration tests with built registries also exist Support
  /etc/docker/certs.d update image-spec to v1.0.0-rc6

* Thu Jun 15 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.21-1
- Add support for storage.conf and storage-config.5.md from github
  container storage package Bump to the latest version of skopeo
  vendor.conf: add ostree-go it is used by containers/image for pulling
  images to the OSTree storage. fail early when image os does not match
  host os Improve documentation on what to do with containers/image
  failures in test-skopeo We now have the docker-archive: transport
  Integration tests with built registries also exist Support
  /etc/docker/certs.d update image-spec to v1.0.0-rc6

* Wed Jun 14 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.20-3
- Add support for storage.conf and storage-config.5.md from github
  container storage package

* Wed Jun 14 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.20-2
- Add support for storage.conf and storage-config.5.md from github
  container storage package

* Tue May 23 2017 Brent Baude <bbaude@redhat.com> - 0.1.20-1
- New version skopeo-0.1.20

* Wed Apr 26 2017 Brent Baude <bbaude@redhat.com> - 0.1.19-3
- No docker for ppc64

* Tue Apr 25 2017 Brent Baude <bbaude@redhat.com> - 0.1.19-2
- no golang support for ppc64

* Tue Feb 28 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.19-1
- skopeo-0.1.19-1.dev.git0224d8c
- bump to v0.1.19-dev
- built commit 0224d8c

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 16 2016 Colin Walters <walters@verbum.org> - 0.1.17-4
- Add another containers/storage dep

* Thu Dec 15 2016 Colin Walters <walters@verbum.org> - 0.1.17-3
- build: Require btrfs-progs-devel

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.1.17-2
- Rebuild for gpgme 1.18

* Tue Dec 06 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.17-1
- NVR: skopeo-0.1.17-1.dev.git2b3af4a
- bump to 0.1.17-dev

* Fri Nov 04 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.14-7
- NVR-skopeo-0.1.14-6.git550a480
- Fix BZ#1391932

* Tue Oct 18 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.14-6
- NVR: skopeo-0.1.14-5.git550a480
- Conflics with atomic in skopeo-containers

* Thu Oct 13 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.14-5
- NVR: skopeo-0.1.14-4.git550a480
- built skopeo-containers

* Wed Sep 21 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.14-4
- NVR: skopeo-0.1.14-3.gitd830391
- built mtrmac/integrate-all-the-things commit d830391

* Thu Sep 08 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.14-3
- NVR: skopeo-0.1.14-2.git362bfc5
- built commit 362bfc5

* Thu Aug 25 2016 Colin Walters <walters@verbum.org> - 0.1.14-2
- Add files section for upstream git master

* Thu Aug 11 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.14-1
- NVR: skopeo-0.1.14-1.gitffe92ed
- build origin/master commit ffe92ed

* Thu Jul 21 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.13-3
- https://fedoraproject.org/wiki/Changes/golang1.7

* Tue Jun 21 2016 Lokesh Mandvekar <lsm5@redhat.com> - 0.1.13-2
- NVR: skopeo-0.1.13-5
- include go-srpm-macros and compiler(go-compiler) in fedora conditionals
- define %%gobuild if not already
- add patch to build with older version of golang

* Thu Jun 02 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.13-1
- update to v0.1.13

* Tue May 31 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.12-4
- rebuild with fixed go build source path

* Fri May 27 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.12-3
- remove build with debug

* Fri May 27 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.12-2
- fedpkg import missed

* Fri May 27 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.12-1
- update to v0.1.12

* Thu May 05 2016 Colin Walters <walters@verbum.org> - 0.1.11-7
- Look for all vendor dirs

* Tue Apr 26 2016 Colin Walters <walters@verbum.org> - 0.1.11-6
- Conditionally run go-md2man

* Tue Apr 26 2016 Colin Walters <walters@verbum.org> - 0.1.11-5
- BR libassuan

* Thu Apr 21 2016 Colin Walters <walters@verbum.org> - 0.1.11-4
- BR gpgme-devel

* Thu Apr 21 2016 Colin Walters <walters@verbum.org> - 0.1.11-3
- BR go-srpm-macros and go-compilers

* Thu Apr 21 2016 Colin Walters <walters@verbum.org> - 0.1.11-2
- Handle missing vendor dirs

* Tue Mar 08 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.11-1
- Update to v0.1.11

* Tue Mar 08 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.10-1
- Update to v0.1.10

* Mon Feb 29 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.9-1
- update to v0.1.9

* Mon Feb 29 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.8-1
- bump to v0.1.8

* Mon Feb 22 2016 Peter Robinson <pbrobinson@gmail.com> - 0.1.4-2
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.4-1
- Intial import (#1301143)
## END: Generated by rpmautospec
