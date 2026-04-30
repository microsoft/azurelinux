## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
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
%global debug_package   %{nil}
%endif

%global gomodulesmode GO111MODULE=on

%if %{defined fedora}
%define build_with_btrfs 1
%if 0%{?fedora} >= 43
%define sequoia 1
%endif
%endif

%if %{defined rhel}
%define fips 1
%endif

%global git0 https://github.com/containers/%{name}

Name: buildah
# Set different Epoch for copr
%if %{defined copr_username}
Epoch: 102
%else
Epoch: 2
%endif
# DO NOT TOUCH the Version string!
# The TRUE source of this specfile is:
# https://github.com/containers/skopeo/blob/main/rpm/skopeo.spec
# If that's what you're reading, Version must be 0, and will be updated by Packit for
# copr and koji builds.
# If you're reading this on dist-git, the version is automatically filled in by Packit.
Version: 1.43.0
# The `AND` needs to be uppercase in the License for SPDX compatibility
License: Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0
Release: %autorelease
%if %{defined golang_arches_future}
ExclusiveArch: %{golang_arches_future}
%else
ExclusiveArch: aarch64 ppc64le s390x x86_64
%endif
Summary: A command line tool used for creating OCI Images
URL: https://%{name}.io
# Tarball fetched from upstream
Source: %{git0}/archive/v%{version}.tar.gz
BuildRequires: device-mapper-devel
BuildRequires: git-core
BuildRequires: golang >= 1.16.6
BuildRequires: glib2-devel
BuildRequires: glibc-static
%if !%{defined gobuild}
BuildRequires: go-rpm-macros
%endif
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: make
%if %{defined build_with_btrfs}
BuildRequires: btrfs-progs-devel
%endif
BuildRequires: shadow-utils-subid-devel
BuildRequires: sqlite-devel
Requires: containers-common-extra
%if %{defined fedora}
BuildRequires: libseccomp-static
%else
BuildRequires: libseccomp-devel
%endif
Requires: libseccomp >= 2.4.1-0
Suggests: cpp
%if %{defined sequoia}
Requires: podman-sequoia
%endif

%description
The %{name} package provides a command line tool which can be used to
* create a working container from scratch
or
* create a working container from an image as a starting point
* mount/umount a working container's root file system for manipulation
* save container's root file system layer to create a new image
* delete a working container or an image

# This subpackage is only intended for CI testing.
# Not meant for end user/customer usage.
%package tests
Summary: Tests for %{name}

Requires: %{name} = %{epoch}:%{version}-%{release}
%if %{defined bats_epel}
Requires: bats
%else
Recommends: bats
%endif
Requires: bzip2
Requires: podman
Requires: golang
Requires: jq
Requires: httpd-tools
Requires: openssl
Requires: nmap-ncat
Requires: git-daemon

%description tests
%{summary}

This package contains system tests for %{name}

%prep
%autosetup -Sgit -n %{name}-%{version}

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

export CNI_VERSION=`grep '^# github.com/containernetworking/cni ' src/modules.txt | sed 's,.* ,,'`
export LDFLAGS="-X main.buildInfo=`date +%s` -X main.cniVersion=${CNI_VERSION}"

export BUILDTAGS="seccomp $(hack/systemd_tag.sh) $(hack/libsubid_tag.sh) libsqlite3"
%if !%{defined build_with_btrfs}
export BUILDTAGS+=" exclude_graphdriver_btrfs"
%endif

%if %{defined fips}
export BUILDTAGS+=" libtrust_openssl"
%endif

%if %{defined sequoia}
export BUILDTAGS+=" containers_image_sequoia"
%endif

%gobuild -o bin/%{name} ./cmd/%{name}
%gobuild -o bin/imgtype ./tests/imgtype
%gobuild -o bin/copy ./tests/copy
%gobuild -o bin/tutorial ./tests/tutorial
%gobuild -o bin/inet ./tests/inet
%gobuild -o bin/dumpspec ./tests/dumpspec
%gobuild -o bin/passwd ./tests/passwd
%gobuild -o bin/crash ./tests/crash
%gobuild -o bin/wait ./tests/wait
%{__make} docs

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install install.completions

install -d -p %{buildroot}/%{_datadir}/%{name}/test/system
cp -pav tests/. %{buildroot}/%{_datadir}/%{name}/test/system
cp bin/imgtype %{buildroot}/%{_bindir}/%{name}-imgtype
cp bin/copy    %{buildroot}/%{_bindir}/%{name}-copy
cp bin/tutorial %{buildroot}/%{_bindir}/%{name}-tutorial
cp bin/inet     %{buildroot}/%{_bindir}/%{name}-inet
cp bin/dumpspec %{buildroot}/%{_bindir}/%{name}-dumpspec
cp bin/passwd %{buildroot}/%{_bindir}/%{name}-passwd
cp bin/crash %{buildroot}/%{_bindir}/%{name}-crash
cp bin/wait %{buildroot}/%{_bindir}/%{name}-wait

rm %{buildroot}%{_datadir}/%{name}/test/system/tools/build/*

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

# Include check to silence rpmlint.
%check

%files
%license LICENSE vendor/modules.txt
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}

%files tests
%license LICENSE
%{_bindir}/%{name}-imgtype
%{_bindir}/%{name}-copy
%{_bindir}/%{name}-tutorial
%{_bindir}/%{name}-inet
%{_bindir}/%{name}-dumpspec
%{_bindir}/%{name}-passwd
%{_bindir}/%{name}-crash
%{_bindir}/%{name}-wait
%{_datadir}/%{name}/test

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2:1.43.0-2
- test: add initial lock files

* Fri Feb 06 2026 Packit <hello@packit.dev> - 2:1.43.0-1
- Update to 1.43.0 upstream release

* Wed Dec 03 2025 Packit <hello@packit.dev> - 2:1.42.2-1
- Update to 1.42.2 upstream release

* Tue Nov 11 2025 Packit <hello@packit.dev> - 2:1.42.1-1
- Update to 1.42.1 upstream release

* Mon Nov 03 2025 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.42.0-4
- Rebuild for CVE fixes

* Thu Oct 23 2025 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.42.0-3
- cleanup changelog

* Thu Oct 23 2025 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.42.0-2
- build with sequoia on f43+

* Wed Oct 22 2025 Packit <hello@packit.dev> - 2:1.42.0-1
- Update to 1.42.0 upstream release

* Mon Sep 29 2025 Packit <hello@packit.dev> - 2:1.41.5-1
- Update to 1.41.5 upstream release

* Thu Sep 04 2025 Packit <hello@packit.dev> - 2:1.41.4-1
- Update to 1.41.4 upstream release

* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 2:1.41.3-4
- Rebuild for golang-1.25.0

* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 2:1.41.3-3
- Revert "Rebuild for golang-1.25.0"

* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 2:1.41.3-2
- Rebuild for golang-1.25.0

* Thu Aug 14 2025 Packit <hello@packit.dev> - 2:1.41.3-1
- Update to 1.41.3 upstream release

* Wed Aug 13 2025 Packit <hello@packit.dev> - 2:1.41.2-1
- Update to 1.41.2 upstream release

* Thu Aug 07 2025 Packit <hello@packit.dev> - 2:1.41.1-1
- Update to 1.41.1 upstream release

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.41.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Packit <hello@packit.dev> - 2:1.41.0-1
- Update to 1.41.0 upstream release

* Wed Jun 04 2025 Packit <hello@packit.dev> - 2:1.40.1-1
- Update to 1.40.1 upstream release

* Mon Apr 21 2025 Packit <hello@packit.dev> - 2:1.40.0-1
- Update to 1.40.0 upstream release

* Fri Mar 28 2025 Packit <hello@packit.dev> - 2:1.39.4-1
- Update to 1.39.4 upstream release

* Fri Mar 14 2025 Packit <hello@packit.dev> - 2:1.39.3-1
- Update to 1.39.3 upstream release

* Tue Mar 04 2025 Packit <hello@packit.dev> - 2:1.39.2-1
- Update to 1.39.2 upstream release

* Wed Feb 26 2025 Packit <hello@packit.dev> - 2:1.39.1-1
- Update to 1.39.1 upstream release

* Thu Feb 06 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.39.0-2
- TMT: initial enablement

* Mon Feb 03 2025 Packit <hello@packit.dev> - 2:1.39.0-1
- Update to 1.39.0 upstream release

* Tue Jan 21 2025 Packit <hello@packit.dev> - 2:1.38.1-1
- Update to 1.38.1 upstream release

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 12 2024 Paul Holzinger <pholzing@redhat.com> - 2:1.38.0-2
- tests: set new inet helper path

* Mon Nov 11 2024 Packit <hello@packit.dev> - 2:1.38.0-1
- Update to 1.38.0 upstream release

* Fri Oct 18 2024 Packit <hello@packit.dev> - 2:1.37.5-1
- Update to 1.37.5 upstream release

* Mon Oct 07 2024 Packit <hello@packit.dev> - 2:1.37.4-1
- Update to 1.37.4 upstream release

* Thu Sep 26 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.37.3-2
- rebuild

* Mon Sep 23 2024 Packit <hello@packit.dev> - 2:1.37.3-1
- Update to 1.37.3 upstream release

* Wed Aug 28 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.37.2-2
- rebuild for shadow-utils bump

* Wed Aug 21 2024 Packit <hello@packit.dev> - 1.37.2-1
- Update to 1.37.2 upstream release

* Tue Aug 13 2024 Packit <hello@packit.dev> - 1.37.1-1
- Update to 1.37.1 upstream release

* Fri Jul 26 2024 Packit <hello@packit.dev> - 1.37.0-1
- Update to 1.37.0 upstream release

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 24 2024 Packit <hello@packit.dev> - 1.36.0-1
- Update to 1.36.0 upstream release

* Fri May 10 2024 Packit <hello@packit.dev> - 1.35.4-1
- Update to 1.35.4 upstream release

* Sat Mar 30 2024 Packit <hello@packit.dev> - 1.35.3-1
- [packit] 1.35.3 upstream release

* Wed Mar 27 2024 Ed Santiago <santiago@redhat.com> - 1.35.2-2
- Gating tests: require slirp4netns

* Tue Mar 26 2024 Packit <hello@packit.dev> - 1.35.2-1
- [packit] 1.35.2 upstream release

* Mon Mar 18 2024 Packit <hello@packit.dev> - 1.35.1-1
- [packit] 1.35.1 upstream release

* Thu Mar 07 2024 Packit <hello@packit.dev> - 1.35.0-1
- [packit] 1.35.0 upstream release

* Thu Feb 22 2024 Packit <hello@packit.dev> - 1.34.1-1
- [packit] 1.34.1 upstream release

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 1.34.0-4
- Rebuild for golang 1.22.0

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Packit <hello@packit.dev> - 1.34.0-1
- [packit] 1.34.0 upstream release

* Sun Nov 26 2023 Packit <hello@packit.dev> - 1.33.2-1
- [packit] 1.33.2 upstream release

* Mon Oct 30 2023 Packit <hello@packit.dev> - 1.32.2-1
- [packit] 1.32.2 upstream release

* Tue Oct 24 2023 Packit <hello@packit.dev> - 1.32.1-1
- [packit] 1.32.1 upstream release

* Thu Sep 14 2023 Packit <hello@packit.dev> - 1.32.0-1
- [packit] 1.32.0 upstream release

* Thu Aug 24 2023 Packit <hello@packit.dev> - 1.31.3-1
- [packit] 1.31.3 upstream release

* Tue Aug 22 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.31.2-4
- spdx compatible license

* Fri Aug 11 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.31.2-3
- use double quotes for buildtags

* Fri Aug 11 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.31.2-2
- fix buildtags

* Thu Aug 10 2023 Packit <hello@packit.dev> - 1.31.2-1
- [packit] 1.31.2 upstream release

* Wed Aug 09 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.31.1-1
- bump to v1.31.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.31.0-1
- bump to v1.31.0

* Tue Apr 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.30.0-2
- Disable btrfs in RHEL builds

* Mon Apr 10 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.30.0-1
- auto bump to v1.30.0

* Mon Mar 06 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.29.1-2
- migrated to SPDX license

* Fri Feb 17 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.29.1-1
- auto bump to v1.29.1

* Thu Feb 09 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.29.0-2
- exclusivearch: golang_arches_future

* Tue Jan 31 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.29.0-1
- bump to v1.29.0

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.28.2-1
- auto bump to v1.28.2

* Fri Oct 28 2022 Troy Dawson <tdawson@fedoraproject.org> - 1.28.0-7
- Add ExclusiveArch

* Tue Oct 25 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.28.0-6
- rebuild

* Fri Oct 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.28.0-5
- Revert "auto bump to v1.28.0"

* Fri Oct 07 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.28.0-4
- auto bump to v1.28.0

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.28.0-3
- depend on containers-common-extra

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.28.0-2
- remove debbuild macros to comply with Fedora guidelines

* Mon Oct 03 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.28.0-1
- auto bump to v1.28.0

* Fri Sep 30 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.27.2-1
- bump to v1.27.2

* Fri Sep 09 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.27.1-1
- auto bump to v1.27.1

* Wed Aug 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.27.0-3
- use easier tag macros to make both fedora and debbuild happy

* Tue Aug 16 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.27.0-2
- Fix debbuild maintainer issue

* Tue Aug 09 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.27.0-1
- auto bump to v1.27.0

* Mon Aug 08 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.26.4-2
- add buildah-tutorial binary

* Wed Aug 03 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.26.4-1
- auto bump to v1.26.4

* Wed Aug 03 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.26.3-1
- auto bump to v1.26.3

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.26.2-2
- debbuild s/Maintainer/Packager

* Wed Jul 06 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.26.2-1
- auto bump to v1.26.2

* Fri Jun 24 2022 Martin Jackson <martjack@redhat.com> - 1.26.1-5
- Add shadow-utils-subid-devel BuildRequires to pick up proper subid
  support

* Sat Jun 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.26.1-4
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327,
  CVE-2022-27191, CVE-2022-29526, CVE-2022-30629

* Fri Jun 17 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.26.1-3
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327,
  CVE-2022-27191, CVE-2022-29526, CVE-2022-30629

* Fri May 27 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.26.1-2
- build deb packages using debbuild

* Thu May 05 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.26.1-1
- auto bump to v1.26.1

* Wed May 04 2022 Neal Gompa <ngompa@datto.com> - 1.26.0-2
- Add missing container networking dependencies (#2081834)

* Wed May 04 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.26.0-1
- auto bump to v1.26.0

* Wed Mar 30 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.25.1-1
- auto bump to v1.25.1

* Tue Mar 29 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.25.0-2
- containerfile manpages no longer included, no need to delete

* Tue Mar 29 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.25.0-1
- auto bump to v1.25.0

* Mon Mar 07 2022 Ed Santiago <santiago@redhat.com> - 1.24.2-2
- Gating tests: include more package versions

* Thu Feb 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.24.2-1
- bump to v1.24.2

* Fri Feb 04 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.24.1-1
- bump to v1.24.1

* Wed Feb 02 2022 Ed Santiago <santiago@redhat.com> - 1.24.0-8
- tests package: now require git-daemon

* Tue Feb 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.24.0-7
- rebuild to stay ahead of f35

* Tue Feb 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.24.0-6
- rebuild to stay ahead of f35

* Tue Feb 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.24.0-5
- increase gating test timeout to 80 minutes

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.24.0-4
- unpack git content

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.24.0-3
- import tarball to lookaside cache

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.24.0-2
- fix deps and golang provides

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.24.0-1
- bump to v1.24.0, bump containers-common dep

* Wed Jan 26 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.23.2-1
- bump to v1.23.2, switch to autospec

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.23.1-1
- buildah-1.23.1-1

* Tue Sep 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.23.0-1
- buildah-1.23.0-1

* Fri Sep 10 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.22.3-2
- update autobuild macros

* Wed Aug 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.3-1
- buildah-1.22.3-1

* Mon Aug 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-22
- buildah-1.22.0-1

* Thu Aug 05 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.22.0-21
- buildah-1.22.0-2
- Resolves: #1974086 - correct build date in buildah version

* Thu Aug 05 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.22.0-20
- buildah-1.22.0-1
- bump to v1.22.0

* Tue Aug 03 2021 Ed Santiago <santiago@redhat.com> - 1.22.0-19
- Gating tests: fetch registry image from quay to avoid throttling on
  docker.io

* Mon Aug 02 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.22.0-18
- buildah-1.22.0-0.15.dev.gitec35bc4
- Resolves: #1983596, #1987738 - Security fix for CVE-2021-34558

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Ed Santiago <santiago@redhat.com> - 1.22.0-15
- Try to deal with buildah copy-helper nightmare

* Fri Jul 16 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.22.0-14
- adjust hardening flags for s390x otherwise build fails

* Fri Jul 16 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.22.0-13
- buildah-1.22.0-0.12.dev.gitec35bc4
- Resolves: #1969264, #1982880 - Security fix for CVE-2021-3602

* Fri Jul 16 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.22.0-12
- buildah-1.22.0-0.12.dev.gitec35bc4
- Resolves: #1982880 - Security fix for CVE-2021-3602

* Wed Jun 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-11
- buildah-1.22.0-0.11.dev.git6d5d1ae
- autobuilt 6d5d1ae

* Tue Jun 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-10
- buildah-1.22.0-0.10.dev.git802a904
- autobuilt 802a904

* Sat Jun 19 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-9
- buildah-1.22.0-0.9.dev.git5181b9c
- autobuilt 5181b9c

* Fri Jun 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-8
- buildah-1.22.0-0.8.dev.git814868e
- autobuilt 814868e

* Thu Jun 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-7
- buildah-1.22.0-0.7.dev.git30c07b7
- autobuilt 30c07b7

* Wed Jun 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-6
- buildah-1.22.0-0.6.dev.gitd99221f
- autobuilt d99221f

* Mon Jun 14 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.22.0-5
- buildah-1.22.0-0.5.dev.git8d08247
- fix dependencies and bad changelog date

* Fri Jun 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-4
- buildah-1.22.0-0.4.dev.git8d08247
- autobuilt 8d08247

* Thu Jun 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-3
- buildah-1.22.0-0.3.dev.git9c7f50b
- autobuilt 9c7f50b

* Mon Jun 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-2
- buildah-1.22.0-0.2.dev.gitd08dbe7
- autobuilt d08dbe7

* Thu Jun 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.22.0-1
- buildah-1.22.0-0.1.dev.gitbbbe10a
- bump to 1.22.0
- autobuilt bbbe10a

* Wed Jun 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.21.1-8
- buildah-1.21.1-0.8.dev.git4fa566e
- autobuilt 4fa566e

* Sat May 29 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.21.1-7
- buildah-1.21.1-0.7.dev.git8a6d840
- autobuilt 8a6d840

* Fri May 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.21.1-6
- buildah-1.21.1-0.6.dev.git23e2b79
- autobuilt 23e2b79

* Thu May 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.21.1-5
- buildah-1.21.1-0.5.dev.gitd677bf0
- autobuilt d677bf0

* Tue May 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.21.1-4
- buildah-1.21.1-0.4.dev.gitdf14b1c
- autobuilt df14b1c

* Sat May 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.21.1-3
- buildah-1.21.1-0.3.dev.git19d3065
- autobuilt 19d3065

* Fri May 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.21.1-2
- buildah-1.21.1-0.2.dev.git2a83637
- autobuilt 2a83637

* Thu May 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.21.1-1
- buildah-1.21.1-0.1.dev.gitf629ded
- bump to 1.21.1
- autobuilt f629ded

* Tue May 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-17
- buildah-1.20.2-0.15.dev.gitf30b420
- autobuilt f30b420

* Tue May 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-16
- buildah-1.20.2-0.14.dev.git2ab877e
- autobuilt 2ab877e

* Sat May 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-15
- buildah-1.20.2-0.13.dev.git162fbaf
- autobuilt 162fbaf

* Thu May 13 2021 Daniel J Walsh <dwalsh@redhat.com> - 1.20.2-14
- Add suggests qemu-user-static

* Thu May 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-13
- buildah-1.20.2-0.11.dev.git5119393
- autobuilt 5119393

* Wed May 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-12
- buildah-1.20.2-0.10.dev.gita0853c3
- autobuilt a0853c3

* Tue May 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-11
- buildah-1.20.2-0.9.dev.git135d63d
- autobuilt 135d63d

* Fri May 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-10
- buildah-1.20.2-0.8.dev.git22fc573
- autobuilt 22fc573

* Thu May 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-9
- buildah-1.20.2-0.7.dev.gitd78dfd1
- autobuilt d78dfd1

* Mon May 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-8
- buildah-1.20.2-0.6.dev.gitc4fc67f
- autobuilt c4fc67f

* Wed Apr 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-7
- buildah-1.20.2-0.5.dev.git1065fd2
- autobuilt 1065fd2

* Mon Apr 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-6
- buildah-1.20.2-0.4.dev.git9428d03
- autobuilt 9428d03

* Tue Apr 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-5
- buildah-1.20.2-0.3.dev.git2f99c2e
- autobuilt 2f99c2e

* Fri Apr 16 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.20.2-4
- buildah-1.20.2-0.2.dev.git61f5dff
- bump for buildah-tests

* Fri Apr 16 2021 Ed Santiago <santiago@redhat.com> - 1.20.2-3
- buildah-tests: require nmap-ncat

* Fri Apr 16 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.20.2-2
- buildah-1.20.2-0.2.dev.git61f5dff
- slirp4netns, crun, container-selinux and fuse-overlayfs deps used from
  containers-common

* Wed Apr 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.2-1
- buildah-1.20.2-0.1.dev.git2e5732b
- bump to 1.20.2
- autobuilt 2e5732b

* Mon Mar 29 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.1-1
- buildah-1.20.1-0.1.dev.git98f7b3d
- bump to 1.20.1
- autobuilt 98f7b3d

* Mon Mar 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-17
- buildah-1.20.0-0.33.dev.git915de2e
- autobuilt 915de2e

* Sat Mar 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-16
- buildah-1.20.0-0.32.dev.gitecbb651
- autobuilt ecbb651

* Thu Mar 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-15
- buildah-1.20.0-0.31.dev.git0a38651
- autobuilt 0a38651

* Wed Mar 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-14
- buildah-1.20.0-0.30.dev.gitb2f7e27
- autobuilt b2f7e27

* Wed Mar 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-13
- buildah-1.20.0-0.29.dev.git30ed95a
- autobuilt 30ed95a

* Wed Mar 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-12
- buildah-1.20.0-0.28.dev.git9cdde41
- autobuilt 9cdde41

* Tue Mar 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-11
- buildah-1.20.0-0.27.dev.git3b8acfb
- autobuilt 3b8acfb

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-10
- buildah-1.20.0-0.26.dev.gitfd48180
- autobuilt fd48180

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-9
- buildah-1.20.0-0.25.dev.gitced3c7b
- autobuilt ced3c7b

* Sun Mar 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-8
- buildah-1.20.0-0.24.dev.git5352624
- autobuilt 5352624

* Fri Mar 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-7
- buildah-1.20.0-0.23.dev.gite481c9b
- autobuilt e481c9b

* Fri Mar 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-6
- buildah-1.20.0-0.22.dev.gitd5d782f
- autobuilt d5d782f

* Thu Mar 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-5
- buildah-1.20.0-0.21.dev.git8614456
- autobuilt 8614456

* Thu Mar 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-4
- buildah-1.20.0-0.20.dev.git17d8e1b
- autobuilt 17d8e1b

* Wed Mar 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-3
- buildah-1.20.0-0.19.dev.git35300f3
- autobuilt 35300f3

* Wed Mar 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-2
- buildah-1.20.0-0.18.dev.git0d8da0a
- autobuilt 0d8da0a

* Mon Mar 01 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.20.0-1
- buildah-1.20.0-0.16.dev.git0ade935
- Resolves: #1933039 - fix Version field and bump Epoch

* Mon Mar 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-16
- buildah-define.Version-0.16.dev.git0ade935
- autobuilt 0ade935

* Sat Feb 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-15
- buildah-define.Version-0.15.dev.gitc0915a5
- autobuilt c0915a5

* Thu Feb 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-14
- buildah-define.Version-0.14.dev.git1688944
- autobuilt 1688944

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-13
- buildah-define.Version-0.13.dev.gitc15269d
- autobuilt c15269d

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-12
- buildah-define.Version-0.12.dev.git06d974b
- autobuilt 06d974b

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-11
- buildah-define.Version-0.11.dev.gitb51f63a
- autobuilt b51f63a

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-10
- buildah-define.Version-0.10.dev.giteb42398
- autobuilt eb42398

* Tue Feb 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-9
- buildah-define.Version-0.9.dev.gitd5c503c
- autobuilt d5c503c

* Tue Feb 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-8
- buildah-define.Version-0.8.dev.gita5e80a5
- autobuilt a5e80a5

* Tue Feb 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-7
- buildah-define.Version-0.7.dev.git1296778
- autobuilt 1296778

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-6
- buildah-define.Version-0.6.dev.git72ef182
- autobuilt 72ef182

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-5
- buildah-define.Version-0.5.dev.git1b49e62
- autobuilt 1b49e62

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-4
- buildah-define.Version-0.4.dev.gitd47032f
- autobuilt d47032f

* Wed Feb 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-3
- buildah-define.Version-0.3.dev.gita6eeca7
- autobuilt a6eeca7

* Wed Feb 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-2
- buildah-define.Version-0.2.dev.gitde6c0da
- autobuilt de6c0da

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - define.Version-1
- buildah-define.Version-0.1.dev.gitd5326ef
- bump to define.Version
- autobuilt d5326ef

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-28
- buildah-1.20.0-0.27.dev.gite1c7a5c
- autobuilt e1c7a5c

* Mon Feb 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-27
- buildah-1.20.0-0.26.dev.git013883e
- autobuilt 013883e

* Mon Feb 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-26
- buildah-1.20.0-0.25.dev.git0a064b3
- autobuilt 0a064b3

* Mon Feb 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-25
- buildah-1.20.0-0.24.dev.git457c75c
- autobuilt 457c75c

* Fri Feb 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-24
- buildah-1.20.0-0.23.dev.git6421c84
- autobuilt 6421c84

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-23
- buildah-1.20.0-0.22.dev.git2e59c37
- autobuilt 2e59c37

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-22
- buildah-1.20.0-0.21.dev.git3679b9f
- autobuilt 3679b9f

* Tue Feb 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-21
- buildah-1.20.0-0.20.dev.git0508fba
- autobuilt 0508fba

* Tue Feb 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-20
- buildah-1.20.0-0.19.dev.git9eb048a
- autobuilt 9eb048a

* Tue Feb 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-19
- buildah-1.20.0-0.18.dev.git885e9c1
- autobuilt 885e9c1

* Mon Feb 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-18
- buildah-1.20.0-0.17.dev.git8f63761
- autobuilt 8f63761

* Mon Feb 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-17
- buildah-1.20.0-0.16.dev.git800a3ed
- autobuilt 800a3ed

* Mon Feb 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-16
- buildah-1.20.0-0.15.dev.git044ea34
- autobuilt 044ea34

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-15
- buildah-1.20.0-0.14.dev.gite1dfdd3
- autobuilt e1dfdd3

* Mon Feb 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-14
- buildah-1.20.0-0.13.dev.gitd0af90d
- autobuilt d0af90d

* Fri Jan 29 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.20.0-13
- correct built_tag value

* Thu Jan 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-12
- buildah-1.20.0-0.12.dev.git7f340f9
- autobuilt 7f340f9

* Thu Jan 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-11
- buildah-1.20.0-0.11.dev.git0ec651f
- autobuilt 0ec651f

* Thu Jan 28 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.20.0-10
- buildah-1.20.0-0.10.dev.git6002877
- use oci-runtime and crun

* Wed Jan 27 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-9
- buildah-1.20.0-0.9.dev.git6002877
- autobuilt 6002877

* Mon Jan 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-8
- buildah-1.20.0-0.8.dev.git0c5bfcd
- autobuilt 0c5bfcd

* Mon Jan 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-7
- buildah-1.20.0-0.7.dev.git2f20868
- autobuilt 2f20868

* Mon Jan 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-6
- buildah-1.20.0-0.6.dev.git4925e86
- autobuilt 4925e86

* Fri Jan 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-5
- buildah-1.20.0-0.5.dev.git1a04337
- autobuilt 1a04337

* Fri Jan 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-4
- buildah-1.20.0-0.4.dev.git371e4ca
- autobuilt 371e4ca

* Thu Jan 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-3
- buildah-1.20.0-0.3.dev.gitd460e2e
- autobuilt d460e2e

* Mon Jan 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-2
- buildah-1.20.0-0.2.dev.git3f5ba7e
- autobuilt 3f5ba7e

* Mon Jan 18 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-1
- buildah-1.20.0-0.1.dev.git6f554d8
- bump to 1.20.0
- autobuilt 6f554d8

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.1-2
- buildah-1.19.1-0.2.dev.gitd10dbf3
- autobuilt d10dbf3

* Thu Jan 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.1-1
- buildah-1.19.1-0.1.dev.gitf17ccd0
- bump to 1.19.1
- autobuilt f17ccd0

* Thu Jan 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-6
- buildah-1.20.0-0.6.dev.gitb595a98
- autobuilt b595a98

* Thu Jan 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-5
- buildah-1.20.0-0.5.dev.git2e1bbc2
- autobuilt 2e1bbc2

* Wed Jan 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-4
- buildah-1.20.0-0.4.dev.git80181e8
- autobuilt 80181e8

* Tue Jan 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-3
- buildah-1.20.0-0.3.dev.gitcfb3372
- autobuilt cfb3372

* Sun Jan 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-2
- buildah-1.20.0-0.2.dev.git8d89b80
- autobuilt 8d89b80

* Sat Jan 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.20.0-1
- buildah-1.20.0-0.1.dev.git911e6ea
- bump to 1.20.0
- autobuilt 911e6ea

* Fri Jan 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-44
- buildah-1.19.0-0.41.dev.git1b3dc91
- autobuilt 1b3dc91

* Fri Jan 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-43
- buildah-1.19.0-0.40.dev.git10c10ee
- autobuilt 10c10ee

* Fri Jan 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-42
- buildah-1.19.0-0.39.dev.gitddcbb30
- autobuilt ddcbb30

* Fri Jan 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-41
- buildah-1.19.0-0.38.dev.git6d3b8d3
- autobuilt 6d3b8d3

* Thu Jan 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-40
- buildah-1.19.0-0.37.dev.gitf01ddd6
- autobuilt f01ddd6

* Wed Jan 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-39
- buildah-1.19.0-0.36.dev.git02b914b
- autobuilt 02b914b

* Wed Jan 06 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-38
- buildah-1.19.0-0.35.dev.git5129d28
- autobuilt 5129d28

* Tue Jan 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-37
- buildah-1.19.0-0.34.dev.gitf3c5c03
- autobuilt f3c5c03

* Mon Jan 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-36
- buildah-1.19.0-0.33.dev.gitd899c7c
- autobuilt d899c7c

* Tue Dec 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-35
- buildah-1.19.0-0.32.dev.git00b8e9f
- autobuilt 00b8e9f

* Tue Dec 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-34
- buildah-1.19.0-0.31.dev.git24e0eb7
- autobuilt 24e0eb7

* Wed Dec 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-33
- buildah-1.19.0-0.30.dev.gitffef8a6
- autobuilt ffef8a6

* Tue Dec 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-32
- buildah-1.19.0-0.29.dev.git00aa7f0
- autobuilt 00aa7f0

* Tue Dec 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-31
- buildah-1.19.0-0.28.dev.gitb9fdee0
- autobuilt b9fdee0

* Mon Dec 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-30
- buildah-1.19.0-0.27.dev.git5f1031f
- autobuilt 5f1031f

* Mon Dec 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-29
- buildah-1.19.0-0.26.dev.git7734b68
- autobuilt 7734b68

* Mon Dec 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-28
- buildah-1.19.0-0.25.dev.gitbec005d
- autobuilt bec005d

* Mon Dec 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-27
- buildah-1.19.0-0.24.dev.git6e56bea
- autobuilt 6e56bea

* Thu Dec 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-26
- buildah-1.19.0-0.23.dev.git6747061
- autobuilt 6747061

* Wed Dec 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-25
- buildah-1.19.0-0.22.dev.git356fd7e
- autobuilt 356fd7e

* Wed Dec 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-24
- buildah-1.19.0-0.21.dev.git8c01c17
- autobuilt 8c01c17

* Wed Dec 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-23
- buildah-1.19.0-0.20.dev.gitef8adfd
- autobuilt ef8adfd

* Tue Dec 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-22
- buildah-1.19.0-0.19.dev.gitd69f76a
- autobuilt d69f76a

* Thu Dec 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-21
- buildah-1.19.0-0.18.dev.git5b867f2
- autobuilt 5b867f2

* Wed Dec 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-20
- buildah-1.19.0-0.17.dev.git1678745
- autobuilt 1678745

* Tue Dec 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-19
- buildah-1.19.0-0.16.dev.git10d622b
- autobuilt 10d622b

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-18
- buildah-1.19.0-0.15.dev.git1d67d26
- autobuilt 1d67d26

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-17
- buildah-1.19.0-0.14.dev.gitac96369
- autobuilt ac96369

* Mon Dec 07 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.19.0-16
- rearrange BUILDTAGS specification line

* Mon Dec 07 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.19.0-15
- fcf-protection not for centos <= 7

* Mon Dec 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-14
- buildah-1.19.0-0.13.dev.gitc50e236
- autobuilt c50e236

* Sat Dec 05 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.19.0-13
- buildah-1.19.0-0.12.dev.git75ae8be
- harden cgo binaries

* Wed Dec 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-12
- buildah-1.19.0-0.11.dev.git75ae8be
- autobuilt 75ae8be

* Mon Nov 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-11
- buildah-1.19.0-0.10.dev.gitacb97f1
- autobuilt acb97f1

* Mon Nov 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-10
- buildah-1.19.0-0.9.dev.git92463b5
- autobuilt 92463b5

* Mon Nov 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-9
- buildah-1.19.0-0.8.dev.git02b3b50
- autobuilt 02b3b50

* Wed Nov 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-8
- buildah-1.19.0-0.7.dev.gitdd26b13
- autobuilt dd26b13

* Wed Nov 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-7
- buildah-1.19.0-0.6.dev.git587e617
- autobuilt 587e617

* Mon Nov 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-6
- buildah-1.19.0-0.5.dev.gitaf10f8c
- autobuilt af10f8c

* Sat Nov 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-5
- buildah-1.19.0-0.4.dev.git2e1d92e
- autobuilt 2e1d92e

* Fri Nov 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-4
- buildah-1.19.0-0.3.dev.git570b43f
- autobuilt 570b43f

* Fri Nov 20 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.19.0-3
- Suggests: cpp for fedora

* Wed Nov 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-2
- buildah-1.19.0-0.2.dev.gite016fa8
- autobuilt e016fa8

* Tue Nov 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.19.0-1
- buildah-1.19.0-0.1.dev.git05aa527
- bump to 1.19.0
- autobuilt 05aa527

* Mon Nov 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.18.0-8
- buildah-1.18.0-0.8.dev.gitaa37929
- autobuilt aa37929

* Sat Nov 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.18.0-7
- buildah-1.18.0-0.7.dev.git272f241
- autobuilt 272f241

* Fri Nov 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.18.0-6
- buildah-1.18.0-0.6.dev.gitd0c958d
- autobuilt d0c958d

* Wed Nov 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.18.0-5
- buildah-1.18.0-0.5.dev.git5368ec3
- autobuilt 5368ec3

* Tue Nov 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.18.0-4
- buildah-1.18.0-0.4.dev.git18c0b33
- autobuilt 18c0b33

* Mon Nov 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.18.0-3
- buildah-1.18.0-0.3.dev.git1087564
- autobuilt 1087564

* Sat Nov 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.18.0-2
- buildah-1.18.0-0.2.dev.gitc7ed3ca
- autobuilt c7ed3ca

* Thu Nov 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.18.0-1
- buildah-1.18.0-0.1.dev.git7719296
- bump to 1.18.0
- autobuilt 7719296

* Wed Oct 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-41
- buildah-1.17.0-0.39.dev.gitd33bb41
- autobuilt d33bb41

* Tue Oct 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-40
- buildah-1.17.0-0.38.dev.git9229549
- autobuilt 9229549

* Fri Oct 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-39
- buildah-1.17.0-0.37.dev.gita970ffb
- autobuilt a970ffb

* Thu Oct 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-38
- buildah-1.17.0-0.36.dev.git7699b6e
- autobuilt 7699b6e

* Wed Oct 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-37
- buildah-1.17.0-0.35.dev.git7389cc7
- autobuilt 7389cc7

* Tue Oct 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-36
- buildah-1.17.0-0.34.dev.git9913b9f
- autobuilt 9913b9f

* Sat Oct 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-35
- buildah-1.17.0-0.33.dev.git415715a
- autobuilt 415715a

* Fri Oct 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-34
- buildah-1.17.0-0.32.dev.gited75e66
- autobuilt ed75e66

* Wed Oct 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-33
- buildah-1.17.0-0.31.dev.git746b5a6
- autobuilt 746b5a6

* Tue Oct 06 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.17.0-32
- buildah- 1.17.0-0.30.dev.gitf09e52c
- no btrfs for eln

* Tue Oct 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-31
- buildah-1.17.0-0.29.dev.gitf09e52c
- autobuilt f09e52c

* Sat Oct 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-30
- buildah-1.17.0-0.28.dev.git71a5615
- autobuilt 71a5615

* Fri Oct 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-29
- buildah-1.17.0-0.27.dev.git73ae001
- autobuilt 73ae001

* Thu Oct 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-28
- buildah-1.17.0-0.26.dev.gitdc504d9
- autobuilt dc504d9

* Wed Sep 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-27
- buildah-1.17.0-0.25.dev.git7fb1282
- autobuilt 7fb1282

* Fri Sep 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-26
- buildah-1.17.0-0.24.dev.git5955652
- autobuilt 5955652

* Fri Sep 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-25
- buildah-1.17.0-0.23.dev.gitb3f6ed8
- autobuilt b3f6ed8

* Mon Sep 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-24
- buildah-1.17.0-0.22.dev.git0e06e45
- autobuilt 0e06e45

* Mon Sep 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-23
- buildah-1.17.0-0.21.dev.gitf2f857a
- autobuilt f2f857a

* Mon Sep 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-22
- buildah-1.17.0-0.20.dev.git0f4a259
- autobuilt 0f4a259

* Mon Sep 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-21
- buildah-1.17.0-0.19.dev.gitd273b9e
- autobuilt d273b9e

* Mon Sep 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-20
- buildah-1.17.0-0.18.dev.git411a885
- autobuilt 411a885

* Mon Sep 21 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.17.0-19
- buildah-1.17.0-0.17.dev.git678da1d
- adjust centos deps

* Thu Sep 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-18
- buildah-1.17.0-0.16.dev.git678da1d
- autobuilt 678da1d

* Thu Sep 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-17
- buildah-1.17.0-0.15.dev.git58541a3
- autobuilt 58541a3

* Thu Sep 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-16
- buildah-1.17.0-0.14.dev.git17bb22f
- autobuilt 17bb22f

* Wed Sep 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-15
- buildah-1.17.0-0.13.dev.git552cbd3
- autobuilt 552cbd3

* Tue Sep 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-14
- buildah-1.17.0-0.12.dev.gitd0f43a0
- autobuilt d0f43a0

* Tue Sep 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-13
- buildah-1.17.0-0.11.dev.gitb47ffb9
- autobuilt b47ffb9

* Fri Sep 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-12
- buildah-1.17.0-0.10.dev.git1f8bf4d
- autobuilt 1f8bf4d

* Thu Sep 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-11
- buildah-1.17.0-0.9.dev.git33768fc
- autobuilt 33768fc

* Wed Sep 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-10
- buildah-1.17.0-0.8.dev.gitaa3128e
- autobuilt aa3128e

* Wed Sep 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-9
- buildah-1.17.0-0.7.dev.gitefc5ec2
- autobuilt efc5ec2

* Tue Sep 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-8
- buildah-1.17.0-0.6.dev.gitbfe6da5
- autobuilt bfe6da5

* Tue Sep 08 2020 Ed Santiago <santiago@redhat.com> - 1.17.0-7
- Gating tests: set TMPDIR=/var/tmp

* Tue Sep 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-6
- buildah-1.17.0-0.5.dev.git2928303
- autobuilt 2928303

* Tue Sep 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-5
- buildah-1.17.0-0.4.dev.git555eb26
- autobuilt 555eb26

* Tue Sep 08 2020 Ed Santiago <santiago@redhat.com> - 1.17.0-4
- add Subject Alternative Name to local openssl cert

* Tue Sep 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-3
- buildah-1.17.0-0.3.dev.git49a5768
- autobuilt 49a5768

* Mon Sep 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-2
- buildah-1.17.0-0.2.dev.gitd83657c
- autobuilt d83657c

* Sat Sep 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.17.0-1
- buildah-1.17.0-0.1.dev.git28d7d44
- bump to 1.17.0
- autobuilt 28d7d44

* Thu Sep 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.16.0-7
- buildah-1.16.0-0.4.dev.git58e6b4f
- autobuilt 58e6b4f

* Thu Sep 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.16.0-6
- buildah-1.16.0-0.3.dev.gitfce9668
- tests package requires openssl

* Thu Sep 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.16.0-5
- tests package requires openssl

* Thu Sep 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.16.0-4
- buildah-1.16.0-0.2.dev.gitfce9668
- autobuilt fce9668

* Thu Sep 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.16.0-3
- 32bit building fixed upstream

* Thu Sep 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.16.0-2
- fix build issues

* Thu Sep 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.16.0-1
- buildah-1.16.0-0.1.dev.gitac0182c
- bump to 1.16.0
- autobuilt ac0182c

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Ed Santiago <santiago@redhat.com> - 1.15.0-75
- More htpasswd fallout: use httpd-tools

* Wed Jun 24 2020 Ed Santiago <santiago@redhat.com> - 1.15.0-74
- buildah test helper: run registry:2.6, not :2

* Tue May 26 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.15.0-73
- fix buildtags and ostree dep

* Tue May 26 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.15.0-72
- update deps for centos

* Tue May 26 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.15.0-71
- update deps for CentOS

* Tue May 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-70
- buildah-1.15.0-0.66.dev.git2c46b4b
- autobuilt 2c46b4b

* Tue May 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-69
- buildah-1.15.0-0.65.dev.gitf7a3515
- autobuilt f7a3515

* Mon May 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-68
- buildah-1.15.0-0.64.dev.git0ac2a67
- autobuilt 0ac2a67

* Sun May 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-67
- buildah-1.15.0-0.63.dev.gitdbf0777
- autobuilt dbf0777

* Sat May 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-66
- buildah-1.15.0-0.62.dev.gitde0f541
- autobuilt de0f541

* Thu May 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-65
- buildah-1.15.0-0.61.dev.git75e94a2
- autobuilt 75e94a2

* Thu May 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-64
- buildah-1.15.0-0.60.dev.gitab1adf1
- autobuilt ab1adf1

* Thu May 21 2020 Ed Santiago <santiago@redhat.com> - 1.15.0-63
- gating.yaml: duplicate the stanzas

* Thu May 21 2020 Aleksandra Fedorova <afedorova@redhat.com> - 1.15.0-62
- Update gating test name

* Wed May 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-61
- buildah-1.15.0-0.59.dev.git4fc49ce
- autobuilt 4fc49ce

* Mon May 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-60
- buildah-1.15.0-0.58.dev.git7957c13
- autobuilt 7957c13

* Wed May 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-59
- buildah-1.15.0-0.57.dev.git9bd70ac
- autobuilt 9bd70ac

* Tue May 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-58
- buildah-1.15.0-0.56.dev.git3184920
- autobuilt 3184920

* Mon May 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-57
- buildah-1.15.0-0.55.dev.git0f6c2a9
- autobuilt 0f6c2a9

* Mon May 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-56
- buildah-1.15.0-0.54.dev.gitf80da42
- autobuilt f80da42

* Fri May 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-55
- buildah-1.15.0-0.53.dev.git6a7ace0
- autobuilt 6a7ace0

* Tue May 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-54
- buildah-1.15.0-0.52.dev.gitb438050
- autobuilt b438050

* Mon May 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-53
- buildah-1.15.0-0.51.dev.git828035f
- autobuilt 828035f

* Mon May 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-52
- buildah-1.15.0-0.50.dev.git7610123
- autobuilt 7610123

* Mon May 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-51
- buildah-1.15.0-0.49.dev.git7b0dfb8
- autobuilt 7b0dfb8

* Fri May 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-50
- buildah-1.15.0-0.48.dev.gitf35e7d4
- autobuilt f35e7d4

* Fri May 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-49
- buildah-1.15.0-0.47.dev.git42a48f9
- autobuilt 42a48f9

* Fri May 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-48
- buildah-1.15.0-0.46.dev.git63567cb
- autobuilt 63567cb

* Fri May 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-47
- buildah-1.15.0-0.45.dev.git3af27b4
- autobuilt 3af27b4

* Tue Apr 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-46
- buildah-1.15.0-0.44.dev.git8169acd
- autobuilt 8169acd

* Tue Apr 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-45
- buildah-1.15.0-0.43.dev.gitbea8692
- autobuilt bea8692

* Fri Apr 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-44
- buildah-1.15.0-0.42.dev.git0b9a534
- autobuilt 0b9a534

* Fri Apr 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-43
- buildah-1.15.0-0.41.dev.git0d5ab1d
- autobuilt 0d5ab1d

* Thu Apr 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.15.0-42
- build latest source

* Thu Apr 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-41
- buildah-1.15.0-0.39.dev.git843d15d
- autobuilt 843d15d

* Mon Apr 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-40
- buildah-1.15.0-0.38.dev.gitf4970e6
- autobuilt f4970e6

* Thu Apr 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-39
- buildah-1.15.0-0.37.dev.git81e2659
- autobuilt 81e2659

* Tue Apr 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-38
- buildah-1.15.0-0.36.dev.gitdb3ced9
- autobuilt db3ced9

* Mon Apr 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-37
- buildah-1.15.0-0.35.dev.gitc404c89
- autobuilt c404c89

* Mon Apr 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-36
- buildah-1.15.0-0.34.dev.git7a88d7e
- autobuilt 7a88d7e

* Thu Apr 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-35
- buildah-1.15.0-0.33.dev.gitf7ff4c1
- autobuilt f7ff4c1

* Thu Apr 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-34
- buildah-1.15.0-0.32.dev.gite48fa75
- autobuilt e48fa75

* Tue Apr 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-33
- buildah-1.15.0-0.31.dev.gitc554675
- autobuilt c554675

* Tue Apr 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-32
- buildah-1.15.0-0.30.dev.gitf5dbfc1
- autobuilt f5dbfc1

* Tue Apr 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-31
- buildah-1.15.0-0.29.dev.git310c02b
- autobuilt 310c02b

* Tue Apr 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-30
- buildah-1.15.0-0.28.dev.gitc3070ba
- autobuilt c3070ba

* Mon Apr 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-29
- buildah-1.15.0-0.27.dev.git20e41b7
- autobuilt 20e41b7

* Mon Apr 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-28
- buildah-1.15.0-0.26.dev.git9c031e0
- autobuilt 9c031e0

* Sat Apr 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-27
- buildah-1.15.0-0.25.dev.git31a01b4
- autobuilt 31a01b4

* Thu Apr 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-26
- buildah-1.15.0-0.24.dev.gite9a6703
- autobuilt e9a6703

* Wed Apr 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-25
- buildah-1.15.0-0.23.dev.git2fc064e
- autobuilt 2fc064e

* Tue Mar 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-24
- buildah-1.15.0-0.22.dev.git912ca5a
- autobuilt 912ca5a

* Tue Mar 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-23
- buildah-1.15.0-0.21.dev.git25c294c
- autobuilt 25c294c

* Mon Mar 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-22
- buildah-1.15.0-0.20.dev.git1db2cde
- autobuilt 1db2cde

* Sat Mar 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-21
- buildah-1.15.0-0.19.dev.git17ceb60
- autobuilt 17ceb60

* Fri Mar 27 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-20
- buildah-1.15.0-0.18.dev.gitc18e043
- autobuilt c18e043

* Fri Mar 27 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-19
- buildah-1.15.0-0.17.dev.gitd3804fa
- autobuilt d3804fa

* Thu Mar 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-18
- buildah-1.15.0-0.16.dev.git11ad04e
- autobuilt 11ad04e

* Thu Mar 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-17
- buildah-1.15.0-0.15.dev.gite48ff81
- autobuilt e48ff81

* Thu Mar 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-16
- buildah-1.15.0-0.14.dev.gite54da62
- autobuilt e54da62

* Wed Mar 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-15
- buildah-1.15.0-0.13.dev.gita5fabab
- autobuilt a5fabab

* Wed Mar 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-14
- buildah-1.15.0-0.12.dev.gitc61925b
- autobuilt c61925b

* Mon Mar 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-13
- buildah-1.15.0-0.11.dev.gitaba0d4d
- autobuilt aba0d4d

* Mon Mar 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-12
- buildah-1.15.0-0.10.dev.git3b9c6a3
- autobuilt 3b9c6a3

* Mon Mar 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-11
- buildah-1.15.0-0.9.dev.git10542ed
- autobuilt 10542ed

* Thu Mar 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-10
- buildah-1.15.0-0.8.dev.git665dc2f
- autobuilt 665dc2f

* Thu Mar 19 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.15.0-9
- use %%global for url/commit specifications

* Thu Mar 19 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.15.0-8
- fix commit

* Thu Mar 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-7
- buildah-1.15.0-0.7.dev.gitf1cf92b
- autobuilt 843d15d

* Thu Mar 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-6
- buildah-1.15.0-0.6.dev.gitf1cf92b
- autobuilt 843d15d

* Thu Mar 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-5
- buildah-1.15.0-0.5.dev.gitf1cf92b
- autobuilt a2285ed

* Wed Mar 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-4
- buildah-1.15.0-0.4.dev.gitf1cf92b
- autobuilt a2285ed

* Wed Mar 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-3
- buildah-1.15.0-0.3.dev.gitf1cf92b
- autobuilt a2285ed

* Tue Mar 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-2
- buildah-1.15.0-0.2.dev.gitf1cf92b
- autobuilt 040fb4b

* Mon Mar 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.15.0-1
- buildah-1.15.0-0.1.dev.gitf1cf92b
- bump to 1.15.0
- autobuilt d26f437

* Mon Feb 10 2020 Ed Santiago <santiago@redhat.com> - 1.14.0-36
- buildah-tests now requires 'jq'

* Wed Feb 05 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.14.0-35
- adjust libseccomp deps

* Wed Feb 05 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.14.0-34
- adjust deps and macros for centos obs build

* Wed Feb 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-33
- buildah-1.14.0-0.35.dev.gitf1cf92b
- autobuilt f1cf92b

* Sat Feb 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-32
- buildah-1.14.0-0.34.dev.gitf89b081
- autobuilt f89b081

* Fri Jan 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-31
- buildah-1.14.0-0.33.dev.git3177db5
- autobuilt 3177db5

* Thu Jan 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-30
- buildah-1.14.0-0.32.dev.git4131dfa
- autobuilt 4131dfa

* Wed Jan 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-29
- buildah-1.14.0-0.31.dev.git82ff48a
- autobuilt 82ff48a

* Tue Jan 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-28
- buildah-1.14.0-0.30.dev.git0a063c4
- autobuilt 0a063c4

* Mon Jan 27 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-27
- buildah-1.14.0-0.29.dev.gitec4bbe6
- autobuilt ec4bbe6

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-26
- buildah-1.14.0-0.28.dev.git6e277a2
- autobuilt 6e277a2

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-25
- buildah-1.14.0-0.27.dev.git6417a9a
- autobuilt 6417a9a

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-24
- buildah-1.14.0-0.26.dev.git0c3234f
- autobuilt 0c3234f

* Sun Jan 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-23
- buildah-1.14.0-0.25.dev.git2055fe9
- autobuilt 2055fe9

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-22
- buildah-1.14.0-0.24.dev.gita925f79
- autobuilt a925f79

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-21
- buildah-1.14.0-0.23.dev.gitca0819f
- autobuilt ca0819f

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-20
- buildah-1.14.0-0.22.dev.gitc46f6e0
- autobuilt c46f6e0

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-19
- buildah-1.14.0-0.21.dev.gitb09fdc3
- autobuilt b09fdc3

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-18
- buildah-1.14.0-0.20.dev.git09d1c24
- autobuilt 09d1c24

* Tue Jan 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-17
- buildah-1.14.0-0.19.dev.gitbf14e6c
- autobuilt bf14e6c

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-16
- buildah-1.14.0-0.18.dev.git720e5d6
- autobuilt 720e5d6

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-15
- buildah-1.14.0-0.17.dev.gitb7e6731
- autobuilt b7e6731

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-14
- buildah-1.14.0-0.16.dev.gitf7731c2
- autobuilt f7731c2

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-13
- buildah-1.14.0-0.15.dev.git9def9c0
- autobuilt 9def9c0

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-12
- buildah-1.14.0-0.14.dev.git3af1491
- autobuilt 3af1491

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-11
- buildah-1.14.0-0.13.dev.git4e23b7a
- autobuilt 4e23b7a

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-10
- buildah-1.14.0-0.12.dev.git55fa8f5
- autobuilt 55fa8f5

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-9
- buildah-1.14.0-0.11.dev.git47ce18b
- autobuilt 47ce18b

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-8
- buildah-1.14.0-0.10.dev.gita3dec02
- autobuilt a3dec02

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-7
- buildah-1.14.0-0.9.dev.gitb555b7d
- autobuilt b555b7d

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-6
- buildah-1.14.0-0.8.dev.gite7be041
- autobuilt e7be041

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-5
- buildah-1.14.0-0.7.dev.gitdbec497
- autobuilt dbec497

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-4
- buildah-1.14.0-0.6.dev.git45543bf
- autobuilt 45543bf

* Mon Jan 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-3
- buildah-1.14.0-0.5.dev.gitd792c70
- autobuilt d792c70

* Mon Jan 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-2
- buildah-1.14.0-0.4.dev.git20c2a54
- autobuilt 20c2a54

* Mon Jan 06 2020 Ed Santiago <santiago@redhat.com> - 1.14.0-1
- Merge branch 'master' of ssh://pkgs.fedoraproject.org/rpms/buildah

* Mon Jan 06 2020 Ed Santiago <santiago@redhat.com> - 1.12.0-85
- Enable gating tests

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-84
- buildah-1.12.0-0.78.dev.gited0a329
- autobuilt ed0a329

* Mon Nov 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-83
- buildah-1.12.0-0.77.dev.git4cf37c2
- autobuilt 4cf37c2

* Sat Nov 23 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-82
- buildah-1.12.0-0.76.dev.git8fd3148
- autobuilt 8fd3148

* Thu Nov 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-81
- buildah-1.12.0-0.75.dev.git92ff215
- autobuilt 92ff215

* Wed Nov 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-80
- buildah-1.12.0-0.74.dev.gitcd88667
- autobuilt cd88667

* Wed Nov 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-79
- buildah-1.12.0-0.73.dev.git1e6a70c
- autobuilt 1e6a70c

* Tue Nov 19 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-78
- buildah-1.12.0-0.72.dev.git6a555a0
- autobuilt 6a555a0

* Sat Nov 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-77
- buildah-1.12.0-0.71.dev.git9ff68b3
- autobuilt 9ff68b3

* Wed Nov 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-76
- buildah-1.12.0-0.70.dev.gitc5244fe
- autobuilt c5244fe

* Tue Nov 12 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-75
- buildah-1.12.0-0.69.dev.git985e8dc
- autobuilt 985e8dc

* Tue Nov 12 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-74
- buildah-1.12.0-0.68.dev.git85ab067
- autobuilt 85ab067

* Tue Nov 12 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-73
- buildah-1.12.0-0.67.dev.git7535655
- autobuilt 7535655

* Fri Nov 08 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-72
- buildah-1.12.0-0.66.dev.gite3bb278
- autobuilt e3bb278

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-71
- buildah-1.12.0-0.65.dev.gita880001
- autobuilt a880001

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-70
- buildah-1.12.0-0.64.dev.gitf995696
- autobuilt f995696

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-69
- buildah-1.12.0-0.63.dev.git147d106
- autobuilt 147d106

* Wed Nov 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-68
- buildah-1.12.0-0.62.dev.git89bc2a6
- autobuilt 89bc2a6

* Wed Nov 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-67
- buildah-1.12.0-0.61.dev.gitec970d5
- autobuilt ec970d5

* Tue Nov 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-66
- buildah-1.12.0-0.60.dev.gitfba62fd
- autobuilt fba62fd

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-65
- buildah-1.12.0-0.59.dev.git1967973
- autobuilt 1967973

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-64
- buildah-1.12.0-0.58.dev.git20e92ff
- autobuilt 20e92ff

* Thu Oct 31 2019 Ed Santiago <santiago@redhat.com> - 1.12.0-63
- Oops - typo fix: IMGTYPE, not imgtest

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-62
- buildah-1.12.0-0.57.dev.git141b5a1
- autobuilt 141b5a1

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-61
- buildah-1.12.0-0.56.dev.git332a889
- autobuilt 332a889

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-60
- buildah-1.12.0-0.55.dev.git8e26456
- autobuilt 8e26456

* Wed Oct 30 2019 Ed Santiago <santiago@redhat.com> - 1.12.0-59
- Gating tests: timeout: bump to 60m (from 30)

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-58
- buildah-1.12.0-0.54.dev.git1ff7043
- autobuilt 1ff7043

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-57
- buildah-1.12.0-0.53.dev.giteaad6b4
- autobuilt eaad6b4

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-56
- buildah-1.12.0-0.52.dev.git999fa43
- autobuilt 999fa43

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-55
- buildah-1.12.0-0.51.dev.git751f92e
- autobuilt 751f92e

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-54
- buildah-1.12.0-0.50.dev.gitb023cde
- autobuilt b023cde

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-53
- buildah-1.12.0-0.49.dev.git66701d4
- autobuilt 66701d4

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-52
- buildah-1.12.0-0.48.dev.gitc2dc46a
- autobuilt c2dc46a

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-51
- buildah-1.12.0-0.47.dev.git691c394
- autobuilt 691c394

* Fri Oct 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-50
- buildah-1.12.0-0.46.dev.gitcddb66e
- autobuilt cddb66e

* Wed Oct 23 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-49
- buildah-1.12.0-0.45.dev.gitfa4eec7
- autobuilt fa4eec7

* Mon Oct 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-48
- buildah-1.12.0-0.44.dev.git049fdf4
- autobuilt 049fdf4

* Mon Oct 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-47
- buildah-1.12.0-0.43.dev.git1d3db17
- autobuilt 1d3db17

* Sun Oct 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-46
- buildah-1.12.0-0.42.dev.git120c37f
- autobuilt 120c37f

* Wed Oct 16 2019 Ed Santiago <santiago@redhat.com> - 1.12.0-45
- Gating tests

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-44
- buildah-1.12.0-0.41.dev.git0f7148b
- autobuilt 0f7148b

* Wed Oct 16 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.12.0-43
- buildah-1.12.0-0.40.dev.git389d49b
- install imgtype binary

* Wed Oct 16 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.12.0-42
- libseccomp >= 2.4.1-0 for centos

* Wed Oct 16 2019 Ed Santiago <santiago@redhat.com> - 1.12.0-41
- New subpackage: buildah-tests intended for use in fedora gating tests.
  Subpackage already exists in RHEL8.

* Tue Oct 15 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-40
- buildah-1.12.0-0.39.dev.git389d49b
- autobuilt 389d49b

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-39
- buildah-1.12.0-0.38.dev.gitd6f11ba
- autobuilt d6f11ba

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-38
- buildah-1.12.0-0.37.dev.git68b2aa5
- autobuilt 68b2aa5

* Wed Oct 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-37
- buildah-1.12.0-0.36.dev.git13330a4
- autobuilt 13330a4

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-36
- buildah-1.12.0-0.35.dev.git7a7e1f0
- autobuilt 7a7e1f0

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-35
- buildah-1.12.0-0.34.dev.git797e618
- autobuilt 797e618

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-34
- buildah-1.12.0-0.33.dev.gitb298906
- autobuilt b298906

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-33
- buildah-1.12.0-0.32.dev.gitf50b55d
- autobuilt f50b55d

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-32
- buildah-1.12.0-0.31.dev.gite400691
- autobuilt e400691

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-31
- buildah-1.12.0-0.30.dev.git96f9993
- autobuilt 96f9993

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-30
- buildah-1.12.0-0.29.dev.gitc771c56
- autobuilt c771c56

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-29
- buildah-1.12.0-0.28.dev.gite2c33f3
- autobuilt e2c33f3

* Tue Oct 01 2019 Debarshi Ray <rishi@fedoraproject.org> - 1.12.0-28
- Require crun >= 0.10-1

* Tue Oct 01 2019 Debarshi Ray <rishi@fedoraproject.org> - 1.12.0-27
- Switch to crun for Cgroups v2 support

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-26
- buildah-1.12.0-0.25.dev.gitcf933c8
- autobuilt cf933c8

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-25
- buildah-1.12.0-0.24.dev.gitbf04bf1
- autobuilt bf04bf1

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-24
- buildah-1.12.0-0.23.dev.gitfc06a4d
- autobuilt fc06a4d

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-23
- buildah-1.12.0-0.22.dev.gitd3d9cec
- autobuilt d3d9cec

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-22
- buildah-1.12.0-0.21.dev.gita32fc96
- autobuilt a32fc96

* Sat Sep 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-21
- buildah-1.12.0-0.20.dev.git61e32a5
- autobuilt 61e32a5

* Sat Sep 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-20
- buildah-1.12.0-0.19.dev.gitc3b1ec6
- autobuilt c3b1ec6

* Wed Sep 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-19
- buildah-1.12.0-0.18.dev.git04150e0
- autobuilt 04150e0

* Tue Sep 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-18
- buildah-1.12.0-0.17.dev.gitd2c1fd8
- autobuilt d2c1fd8

* Tue Sep 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-17
- buildah-1.12.0-0.16.dev.git6abc01c
- autobuilt 6abc01c

* Mon Sep 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-16
- buildah-1.12.0-0.15.dev.gite9969bc
- autobuilt e9969bc

* Fri Sep 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-15
- buildah-1.12.0-0.14.dev.git10b0e7a
- autobuilt 10b0e7a

* Fri Sep 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-14
- buildah-1.12.0-0.13.dev.git4ce6fba
- autobuilt 4ce6fba

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-13
- buildah-1.12.0-0.12.dev.git9cac447
- autobuilt 9cac447

* Sat Sep 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-12
- buildah-1.12.0-0.11.dev.git20a33e0
- autobuilt 20a33e0

* Sat Sep 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-11
- buildah-1.12.0-0.10.dev.git9bf6b5e
- autobuilt 9bf6b5e

* Fri Sep 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-10
- buildah-1.12.0-0.9.dev.gitf54c965
- autobuilt f54c965

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-9
- buildah-1.12.0-0.8.dev.git3f6ad0f
- autobuilt 3f6ad0f

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-8
- buildah-1.12.0-0.7.dev.git9f2a682
- autobuilt 9f2a682

* Thu Sep 05 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.12.0-7
- add built_tag macro(non-rawhide only)

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-6
- buildah-1.12.0-0.6.dev.git4da1d5d
- autobuilt 4da1d5d

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-5
- buildah-1.12.0-0.5.dev.git34f1ae6
- autobuilt 34f1ae6

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-4
- buildah-1.12.0-0.4.dev.gitcc80ccc
- autobuilt cc80ccc

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-3
- buildah-1.12.0-0.3.dev.gitb643073
- autobuilt b643073

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-2
- buildah-1.12.0-0.2.dev.git15773bd
- autobuilt 15773bd

* Sat Aug 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-1
- buildah-1.12.0-0.1.dev.git1a1a728
- bump to 1.12.0
- autobuilt 1a1a728

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-38
- buildah-1.11.0-0.38.dev.git57db70c
- autobuilt 57db70c

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-37
- buildah-1.11.0-0.37.dev.gite930951
- autobuilt e930951

* Thu Aug 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-36
- buildah-1.11.0-0.36.dev.gitecf5b72
- autobuilt ecf5b72

* Thu Aug 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-35
- buildah-1.11.0-0.35.dev.git5671417
- autobuilt 5671417

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-34
- buildah-1.11.0-0.34.dev.git689f8ed
- autobuilt 689f8ed

* Thu Aug 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-33
- buildah-1.11.0-0.33.dev.git6b5f8ba
- autobuilt 6b5f8ba

* Thu Aug 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-32
- buildah-1.11.0-0.32.dev.gitff72568
- autobuilt ff72568

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-31
- buildah-1.11.0-0.31.dev.git376e52e
- autobuilt 376e52e

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-30
- buildah-1.11.0-0.30.dev.git5a1c733
- autobuilt 5a1c733

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-29
- buildah-1.11.0-0.29.dev.git3ad937b
- autobuilt 3ad937b

* Tue Aug 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-28
- buildah-1.11.0-0.28.dev.gitfa68ed6
- autobuilt fa68ed6

* Tue Aug 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-27
- buildah-1.11.0-0.27.dev.gitb288b7a
- autobuilt b288b7a

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-26
- buildah-1.11.0-0.26.dev.gitc1a2d4f
- autobuilt c1a2d4f

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-25
- buildah-1.11.0-0.25.dev.git51415ec
- autobuilt 51415ec

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-24
- buildah-1.11.0-0.24.dev.gitc2c52ba
- autobuilt c2c52ba

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-23
- buildah-1.11.0-0.23.dev.gitebf6f51
- autobuilt ebf6f51

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-22
- buildah-1.11.0-0.22.dev.git36dcedb
- autobuilt 36dcedb

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-21
- buildah-1.11.0-0.21.dev.gitab0286f
- autobuilt ab0286f

* Thu Aug 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-20
- buildah-1.11.0-0.20.dev.git1ce1130
- autobuilt 1ce1130

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-19
- buildah-1.11.0-0.19.dev.gitd88c26b
- autobuilt d88c26b

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-18
- buildah-1.11.0-0.18.dev.git5c98d3c
- autobuilt 5c98d3c

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-17
- buildah-1.11.0-0.17.dev.git3f5436f
- autobuilt 3f5436f

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-16
- buildah-1.11.0-0.16.dev.gita99139c
- autobuilt a99139c

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-15
- buildah-1.11.0-0.15.dev.git2df08f0
- autobuilt 2df08f0

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-14
- buildah-1.11.0-0.14.dev.git96a136e
- autobuilt 96a136e

* Sun Aug 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-13
- buildah-1.11.0-0.13.dev.git7180312
- autobuilt 7180312

* Sat Aug 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-12
- buildah-1.11.0-0.12.dev.git0dfb6f5
- autobuilt 0dfb6f5

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-11
- buildah-1.11.0-0.11.dev.git60d5480
- autobuilt 60d5480

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-10
- buildah-1.11.0-0.10.dev.git60c0088
- autobuilt 60c0088

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-9
- buildah-1.11.0-0.9.dev.gitc953216
- autobuilt c953216

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-8
- buildah-1.11.0-0.8.dev.gitf892eb6
- autobuilt f892eb6

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-7
- buildah-1.11.0-0.7.dev.git95cb061
- autobuilt 95cb061

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-6
- buildah-1.11.0-0.6.dev.gitf4cfe9c
- autobuilt f4cfe9c

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-5
- buildah-1.11.0-0.5.dev.git03aa807
- autobuilt 03aa807

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-4
- buildah-1.11.0-0.4.dev.gitbafcf88
- autobuilt bafcf88

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-3
- buildah-1.11.0-0.3.dev.git232f7c6
- autobuilt 232f7c6

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-2
- buildah-1.11.0-0.2.dev.git1de958d
- autobuilt 1de958d

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-1
- buildah-1.11.0-0.1.dev.gitac5031d
- bump to 1.11.0
- autobuilt ac5031d

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-14
- buildah-1.9.3-0.68.dev.git3117f5e
- autobuilt 3117f5e

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-13
- buildah-1.9.3-0.67.dev.git4d017d6
- autobuilt 4d017d6

* Wed Jul 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-12
- buildah-1.9.3-0.66.dev.gitc00f548
- autobuilt c00f548

* Wed Jul 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-11
- buildah-1.9.3-0.65.dev.git677b771
- autobuilt 677b771

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-10
- buildah-1.9.3-0.64.dev.gitb7a0ed0
- autobuilt b7a0ed0

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-9
- buildah-1.9.3-0.63.dev.git5bab9b0
- autobuilt 5bab9b0

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-8
- buildah-1.9.3-0.62.dev.git4ccb343
- autobuilt 4ccb343

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-7
- buildah-1.9.3-0.61.dev.gita74bdd3
- autobuilt a74bdd3

* Sat Jul 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-6
- buildah-1.9.3-0.60.dev.git6b214d2
- autobuilt 6b214d2

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-5
- buildah-1.9.3-0.59.dev.git73401a4
- autobuilt 73401a4

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-3
- buildah-1.9.3-0.57.dev.git6bd0551
- autobuilt 6bd0551

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-2
- buildah-1.9.3-0.56.dev.git555b5a5
- autobuilt 555b5a5

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-1
- buildah-1.9.3-0.55.dev.git2110f05
- bump to 1.9.3
- autobuilt 2110f05

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-10
- buildah-1.9.2-0.54.dev.gitd7dec37
- autobuilt d7dec37

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-9
- buildah-1.9.2-0.53.dev.git5da3c8c
- autobuilt 5da3c8c

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-8
- buildah-1.9.2-0.52.dev.git4ae0e14
- autobuilt 4ae0e14

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-7
- buildah-1.9.2-0.51.dev.git8da4cb4
- autobuilt 8da4cb4

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-6
- buildah-1.9.2-0.50.dev.gitbe51b9b
- autobuilt be51b9b

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-5
- buildah-1.9.2-0.49.dev.gitb33b87b
- autobuilt b33b87b

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-4
- buildah-1.9.2-0.48.dev.git16e3010
- autobuilt 16e3010

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-3
- buildah-1.9.2-0.47.dev.gitbb5cbf1
- autobuilt bb5cbf1

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-2
- buildah-1.9.2-0.46.dev.git2249ba3
- autobuilt 2249ba3

* Sun Jul 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-1
- buildah-1.9.2-0.45.dev.gitd419737
- bump to 1.9.2
- autobuilt d419737

* Wed Jul 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-8
- buildah-1.9.1-0.44.dev.git5d723ff
- autobuilt 5d723ff

* Wed Jul 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-7
- %%gobuild defined by default on fedora

* Sun Jul 07 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-6
- buildah-1.9.1-0.43.dev.gite160a63
- built e160a63
- add centos conditionals
- use new name for go-md2man dep

* Sat Jun 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-5
- buildah-1.9.1-0.42.dev.git1d11851
- autobuilt 1d11851

* Fri Jun 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-4
- buildah-1.9.1-0.41.dev.git07aaf5e
- autobuilt 07aaf5e

* Thu Jun 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-3
- buildah-1.9.1-0.40.dev.gitc22957b
- autobuilt c22957b

* Tue Jun 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-2
- buildah-1.9.1-0.39.dev.git2c4f388
- autobuilt 2c4f388

* Sun Jun 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-1
- buildah-1.9.1-0.38.dev.git0b84b23
- bump to 1.9.1
- autobuilt 0b84b23

* Sat Jun 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-39
- buildah-1.9.0-0.37.dev.git77fa9dd
- autobuilt 77fa9dd

* Fri Jun 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-38
- buildah-1.9.0-0.36.dev.gitdc7b50c
- autobuilt dc7b50c

* Thu Jun 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-37
- buildah-1.9.0-0.35.dev.git2191ba6
- autobuilt 2191ba6

* Wed Jun 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-36
- buildah-1.9.0-0.34.dev.gitdcbf193
- autobuilt dcbf193

* Tue Jun 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-35
- buildah-1.9.0-0.33.dev.git78dcf2f
- autobuilt 78dcf2f

* Mon Jun 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-34
- buildah-1.9.0-0.32.dev.git4ae0a69
- autobuilt 4ae0a69

* Sun Jun 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-33
- buildah-1.9.0-0.31.dev.gitd172dd9
- autobuilt d172dd9

* Sat Jun 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-32
- buildah-1.9.0-0.30.dev.git2da8755
- autobuilt 2da8755

* Fri Jun 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-31
- buildah-1.9.0-0.29.dev.gitad4f235
- autobuilt ad4f235

* Thu Jun 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-30
- buildah-1.9.0-0.28.dev.gite0306bb
- autobuilt e0306bb

* Wed Jun 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-29
- buildah-1.9.0-0.27.dev.gitaa06a77
- autobuilt aa06a77

* Sun Jun 02 2019 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.0-28
- buildable on centos7

* Sun Jun 02 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-27
- buildah-1.9.0-0.26.dev.gita086ec8
- build for all arches

* Sun Jun 02 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-26
- update URL, cosmetic changes in changelog

* Sun Jun 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-25
- buildah-1.9.0-0.25.dev.git7016ce6
- autobuilt 7016ce6

* Sat Jun 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-24
- buildah-1.9.0-0.24.dev.git3104ddf
- autobuilt 3104ddf

* Fri May 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-23
- buildah-1.9.0-0.23.dev.git53be3d3
- autobuilt 53be3d3

* Thu May 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-22
- buildah-1.9.0-0.22.dev.git2a962f1
- autobuilt 2a962f1

* Wed May 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-21
- buildah-1.9.0-0.21.dev.gitfa7f030
- autobuilt fa7f030

* Tue May 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-20
- buildah-1.9.0-0.20.dev.gited77a92
- autobuilt ed77a92

* Sat May 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-19
- buildah-1.9.0-0.19.dev.git8e48a65
- autobuilt 8e48a65

* Fri May 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-18
- buildah-1.9.0-0.18.dev.git4e1ca7c
- autobuilt 4e1ca7c

* Fri May 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-17
- buildah-1.9.0-0.17.dev.git00f5164
- autobuilt 00f5164

* Thu May 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-16
- buildah-1.9.0-0.16.dev.gitbc9c276
- autobuilt bc9c276

* Tue May 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-15
- buildah-1.9.0-0.15.dev.gitbcc5e51
- autobuilt bcc5e51

* Sun May 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-14
- buildah-1.9.0-0.14.dev.git7793c51
- autobuilt 7793c51

* Sat May 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-13
- buildah-1.9.0-0.13.dev.git3bf8547
- autobuilt 3bf8547

* Fri May 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-12
- buildah-1.9.0-0.12.dev.git63808f9
- autobuilt 63808f9

* Thu May 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-11
- buildah-1.9.0-0.11.dev.gitc0633e3
- autobuilt c0633e3

* Wed May 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-10
- buildah-1.9.0-0.10.dev.git4c6b09c
- autobuilt 4c6b09c

* Tue May 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-9
- buildah-1.9.0-0.9.dev.git7ae362b
- autobuilt 7ae362b

* Mon May 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-8
- buildah-1.9.0-0.8.dev.git74a3195
- autobuilt 74a3195

* Sun May 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-7
- buildah-1.9.0-0.7.dev.gitab8678a
- autobuilt ab8678a

* Sat May 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-6
- buildah-1.9.0-0.6.dev.gitc654b18
- autobuilt c654b18

* Sat May 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-5
- buildah-1.9.0-0.5.dev.gite9184ea
- autobuilt e9184ea

* Fri May 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-4
- buildah-1.9.0-0.4.dev.git59da11d
- autobuilt 59da11d

* Thu May 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-3
- buildah-1.9.0-0.3.dev.git78fb869
- autobuilt 78fb869

* Tue Apr 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-2
- buildah-1.9.0-0.2.dev.git0e30da6
- autobuilt 0e30da6

* Mon Apr 29 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-1
- buildah-1.9.0-0.1.dev.gitddbd805
- bump to v1.9.0-dev
- update release tag format for unreleased builds

* Thu Apr 25 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8-1
- Revert "buildah-1:1.8-0.42.dev.gitbdbedfd"

* Thu Apr 25 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8-3
- Revert "buildah-1:1.8-0.43.dev.gitefa156f"

* Thu Apr 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:1.8-2
- buildah-1:1.8-0.43.dev.gitefa156f
- autobuilt efa156f

* Wed Apr 24 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8-1
- buildah-1:1.8-0.42.dev.gitbdbedfd
- Resolves: #1702419 - bump Epoch to correct release tag

* Wed Apr 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-40
- buildah-1.8-41.dev.gitbdbedfd
- autobuilt bdbedfd

* Tue Apr 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-39
- buildah-1.8-40.dev.gitb466cbd
- autobuilt b466cbd

* Sat Apr 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-38
- buildah-1.8-39.dev.git2f0179f
- autobuilt 2f0179f

* Fri Apr 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-37
- buildah-1.8-38.dev.git135542e
- autobuilt 135542e

* Thu Apr 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-36
- buildah-1.8-37.dev.gite879079
- autobuilt e879079

* Wed Apr 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-35
- buildah-1.8-36.dev.gitd8fe400
- autobuilt d8fe400

* Mon Apr 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-34
- buildah-1.8-35.dev.gitfcc12bd
- autobuilt fcc12bd

* Sat Apr 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-33
- buildah-1.8-34.dev.gitd43787b
- autobuilt d43787b

* Fri Apr 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-32
- buildah-1.8-33.dev.git316bd0a
- autobuilt 316bd0a

* Wed Apr 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-31
- buildah-1.8-32.dev.git021d607
- autobuilt 021d607

* Tue Apr 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-30
- buildah-1.8-31.dev.git610eb7a
- autobuilt 610eb7a

* Sun Apr 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-29
- buildah-1.8-30.dev.git25b7c11
- autobuilt 25b7c11

* Sat Apr 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-28
- buildah-1.8-29.dev.git29a6c81
- autobuilt 29a6c81

* Fri Apr 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-27
- buildah-1.8-28.dev.gitac66d78
- autobuilt ac66d78

* Mon Apr 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-26
- buildah-1.8-27.dev.git9e1967a
- autobuilt 9e1967a

* Sat Mar 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-25
- buildah-1.8-26.dev.git13d9142
- autobuilt 13d9142

* Fri Mar 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-24
- buildah-1.8-25.dev.gita9bd025
- autobuilt a9bd025

* Thu Mar 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-23
- buildah-1.8-24.dev.gitc933fe4
- autobuilt c933fe4

* Wed Mar 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-22
- buildah-1.8-23.dev.git3d74031
- autobuilt 3d74031

* Mon Mar 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-21
- buildah-1.8-22.dev.git03fae01
- autobuilt 03fae01

* Sat Mar 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-20
- buildah-1.8-21.dev.gitd1c75ea
- autobuilt d1c75ea

* Fri Mar 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-19
- buildah-1.8-20.dev.gitc6ae5c5
- autobuilt c6ae5c5

* Thu Mar 21 2019 Daniel J Walsh <dwalsh@redhat.com> - 1.8-18
- Complile with SELinux enabled

* Thu Mar 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-17
- buildah-1.8-18.dev.gitbe0c8d2
- autobuilt be0c8d2

* Wed Mar 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-16
- buildah-1.8-17.dev.git9d6da3a
- autobuilt 9d6da3a

* Tue Mar 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-15
- buildah-1.8-16.dev.git1ba9201
- autobuilt 1ba9201

* Sat Mar 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-14
- buildah-1.8-15.dev.gita986f34
- autobuilt a986f34

* Fri Mar 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-13
- buildah-1.8-14.dev.gitc691d09
- autobuilt c691d09

* Thu Mar 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-12
- buildah-1.8-13.dev.git3b497ff
- autobuilt 3b497ff

* Wed Mar 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-11
- buildah-1.8-12.dev.git3ba8822
- autobuilt 3ba8822

* Sun Mar 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-10
- buildah-1.8-11.dev.git36605c2
- autobuilt 36605c2

* Sat Mar 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-9
- buildah-1.8-10.dev.git984ea9b
- autobuilt 984ea9b

* Thu Mar 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-8
- buildah-1.8-9.dev.git0a8ec97
- autobuilt 0a8ec97

* Wed Mar 06 2019 Daniel J Walsh <dwalsh@redhat.com> - 1.8-7
- Add recommends for fuse-overlay and slirp4netns

* Wed Mar 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-6
- buildah-1.8-7.dev.git3afba37
- autobuilt 3afba37

* Tue Mar 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-5
- buildah-1.8-6.dev.git11dd219
- autobuilt 11dd219

* Fri Mar 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-4
- buildah-1.8-5.dev.git8b1d11f
- autobuilt 8b1d11f

* Thu Feb 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-3
- buildah-1.8-4.dev.git95a5089
- autobuilt 95a5089

* Tue Feb 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-2
- buildah-1.8-3.dev.git6c1a4cc
- autobuilt 6c1a4cc

* Sat Feb 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-1
- buildah-1.8-2.dev.git8c3d8b1
- bump to 1.8
- autobuilt 8c3d8b1

* Fri Feb 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-19
- buildah-1.7-20.dev.git873f001
- autobuilt 873f001

* Thu Feb 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-18
- buildah-1.7-19.dev.gitdb6e7bb
- autobuilt db6e7bb

* Wed Feb 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-17
- buildah-1.7-18.dev.git1b02a7e
- autobuilt 1b02a7e

* Mon Feb 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-16
- buildah-1.7-17.dev.git146a0fc
- autobuilt 146a0fc

* Sat Feb 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-15
- buildah-1.7-16.dev.git80fcb24
- autobuilt 80fcb24

* Fri Feb 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-14
- buildah-1.7-15.dev.git40d4d59
- autobuilt 40d4d59

* Thu Feb 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-13
- buildah-1.7-14.dev.gite4c4d46
- autobuilt e4c4d46

* Sun Feb 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-12
- buildah-1.7-13.dev.git711f9ea
- autobuilt 711f9ea

* Fri Feb 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-11
- buildah-1.7-12.dev.git310363c
- autobuilt 310363c

* Wed Feb 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-10
- buildah-1.7-11.dev.git50539b5
- autobuilt 50539b5

* Tue Feb 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-9
- buildah-1.7-10.dev.gitad24f28
- autobuilt ad24f28

* Sat Feb 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-8
- buildah-1.7-9.dev.git973bb88
- autobuilt 973bb88

* Fri Feb 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-7
- buildah-1.7-8.dev.git03f6247
- autobuilt 03f6247

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-5
- buildah-1.7-6.dev.gite702872
- autobuilt e702872

* Thu Jan 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-4
- buildah-1.7-5.dev.gitf1cec50
- autobuilt f1cec50

* Tue Jan 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-3
- buildah-1.7-4.dev.git4bcddb7
- autobuilt 4bcddb7

* Mon Jan 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-2
- buildah-1.7-3.dev.git9b9ed1d
- autobuilt 9b9ed1d

* Sun Jan 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-1
- buildah-1.7-2.dev.git7a85ca7
- bump to 1.7
- autobuilt 7a85ca7

* Sat Jan 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1
- buildah-1.6-2.dev.git5f95bd9
- bump to 1.6
- autobuilt 5f95bd9

* Fri Jan 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-1
- buildah-1.7-2.dev.git0f114e9
- bump to 1.7
- autobuilt 0f114e9

* Thu Jan 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-32
- buildah-1.6-33.dev.git66ff1dd
- autobuilt 66ff1dd

* Wed Jan 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-31
- buildah-1.6-32.dev.gitd7e530e
- autobuilt d7e530e

* Tue Jan 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-30
- buildah-1.6-31.dev.gitfe7e09c
- autobuilt fe7e09c

* Sun Jan 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-29
- buildah-1.6-30.dev.gitfa86533
- autobuilt fa86533

* Sat Jan 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-28
- buildah-1.6-29.dev.gitf6a0258
- autobuilt f6a0258

* Fri Jan 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-27
- buildah-1.6-28.dev.git5d22f3c
- autobuilt 5d22f3c

* Thu Jan 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-26
- buildah-1.6-27.dev.git1ef527c
- autobuilt 1ef527c

* Wed Jan 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-25
- buildah-1.6-26.dev.git169a923
- autobuilt 169a923

* Tue Jan 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-24
- buildah-1.6-25.dev.git48b44e5
- autobuilt 48b44e5

* Mon Jan 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-23
- buildah-1.6-24.dev.gita4200ae
- autobuilt a4200ae

* Sun Jan 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-22
- buildah-1.6-23.dev.gitbb710f3
- autobuilt bb710f3

* Sat Jan 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-21
- buildah-1.6-22.dev.git8f05aa6
- autobuilt 8f05aa6

* Fri Jan 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-20
- buildah-1.6-21.dev.git579f1d5
- autobuilt 579f1d5

* Thu Jan 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-19
- buildah-1.6-20.dev.gite55a9f3
- autobuilt e55a9f3

* Tue Dec 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-18
- buildah-1.6-19.dev.giteebbba2
- autobuilt eebbba2

* Thu Dec 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-17
- buildah-1.6-18.dev.git4674656
- autobuilt 4674656

* Wed Dec 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-16
- buildah-1.6-17.dev.gitdd3dff5
- autobuilt dd3dff5

* Sun Dec 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-15
- buildah-1.6-16.dev.git96c68db
- autobuilt 96c68db

* Fri Dec 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-14
- buildah-1.6-15.dev.gitde7f480
- autobuilt de7f480

* Wed Dec 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-13
- buildah-1.6-14.dev.git90ea890
- autobuilt 90ea890

* Mon Dec 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-12
- buildah-1.6-13.dev.gitdd0f4f1
- autobuilt dd0f4f1

* Sat Dec 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-11
- buildah-1.6-12.dev.git1e1dc14
- autobuilt 1e1dc14

* Fri Dec 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-10
- buildah-1.6-11.dev.git9c1d273
- autobuilt 9c1d273

* Thu Dec 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-9
- buildah-1.6-10.dev.git5cca1d6
- autobuilt 5cca1d6

* Wed Dec 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-8
- buildah-1.6-9.dev.git01f9ae2
- autobuilt 01f9ae2

* Tue Dec 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-7
- buildah-1.6-8.dev.git9c65e56
- autobuilt 9c65e56

* Sun Dec 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-6
- buildah-1.6-7.dev.gitb68a8e1
- autobuilt b68a8e1

* Sat Dec 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-5
- buildah-1.6-6.dev.git2b582d3
- autobuilt 2b582d3

* Fri Nov 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-4
- buildah-1.6-5.dev.git6e00183
- autobuilt 6e00183

* Thu Nov 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-3
- buildah-1.6-4.dev.git93d8b9f
- autobuilt 93d8b9f

* Wed Nov 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-2
- buildah-1.6-3.dev.git4126176
- autobuilt 4126176

* Fri Nov 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1
- buildah-1.6-2.dev.gitd5a3c52
- bump to 1.6
- autobuilt d5a3c52

* Thu Nov 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-12
- buildah-1.5-12.dev.git25d89b4
- autobuilt 25d89b4

* Wed Nov 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-11
- buildah-1.5-11.dev.git2ac987a
- autobuilt 2ac987a

* Tue Nov 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-10
- buildah-1.5-10.dev.gitc9cb148
- autobuilt c9cb148

* Sat Nov 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-9
- buildah-1.5-9.dev.git18309de
- autobuilt 18309de

* Fri Nov 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-8
- buildah-1.5-8.dev.gitd7e0993
- autobuilt d7e0993

* Thu Nov 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-7
- buildah-1.5-7.dev.gitdac7819
- autobuilt dac7819

* Tue Nov 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-6
- buildah-1.5-6.dev.gitfb2b2bd
- autobuilt fb2b2bd

* Sat Nov 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-5
- buildah-1.5-5.dev.git9add3c8
- autobuilt 9add3c8

* Fri Nov 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-4
- buildah-1.5-4.dev.git74e0b6f
- autobuilt 74e0b6f

* Thu Nov 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-3
- buildah-1.5-3.dev.git0ae8b51
- autobuilt 0ae8b51

* Wed Nov 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-2
- buildah-1.5-2.dev.git7341758
- autobuilt 7341758

* Tue Oct 02 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.5-1
- bump to v1.5-dev Release

* Wed Sep 19 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4-3
- buildah-1.4-2.dev.git19e44f0
- autobuilt 19e44f0

* Wed Sep 19 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4-2
- upstream name change

* Sun Aug 12 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4-1
- buildah-1.4-1.dev.git0a7389c
- bump to v1.4-dev
- built 0a7389c

* Wed Aug 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-13
- buildah-1.3-11.dev.git02f54e4
- autobuilt 02f54e4

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1.3-12
- Rebuild with fixed binutils

* Sun Jul 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-11
- buildah-1.3-9.dev.gitbe03809
- autobuilt be03809

* Sat Jul 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-10
- buildah-1.3-8.dev.gitc18724e
- autobuilt c18724e

* Thu Jul 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-9
- buildah-1.3-7.dev.git4976d8c
- autobuilt 4976d8c

* Wed Jul 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-8
- buildah-1.3-6.dev.gite5f7539
- autobuilt e5f7539

* Mon Jul 23 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.3-7
- Change container-selinux Requires to Recommends

* Fri Jul 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-6
- buildah-1.3-4.dev.git826733a
- autobuilt 826733a

* Thu Jul 19 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.3-5
- buildah does not require ostree

* Thu Jul 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-4
- buildah-1.3-2.dev.git1215b16
- autobuilt 1215b16

* Tue Jul 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3-3
- disable debuginfo on f29

* Tue Jul 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3-2
- make debuginfo delve debugger friendly

* Tue Jul 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3-1
- buildah-1.3-1.dev.gita9895bd
- bump to v1.3-dev
- built a9895bd

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.2-25
- update release tag to reflect unreleased status

* Mon Jul 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-24
- buildah-1.2-24.git3fb864b
- autobuilt 3fb864b

* Sun Jul 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-23
- buildah-1.2-23.git8be2b62
- autobuilt 8be2b62

* Sat Jul 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-22
- buildah-1.2-22.gita885bc6
- autobuilt a885bc6

* Fri Jul 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-21
- buildah-1.2-21.git733cd20
- autobuilt 733cd20

* Thu Jul 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-20
- buildah-1.2-20.gita59fb7a
- autobuilt a59fb7a

* Tue Jul 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-19
- buildah-1.2-19.git5c11c34
- autobuilt 5c11c34

* Mon Jul 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-18
- buildah-1.2-18.git5cd9be6
- autobuilt 5cd9be6

* Sun Jul 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-17
- buildah-1.2-17.git6f72599
- autobuilt 6f72599

* Sat Jun 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-16
- buildah-1.2-16.git704adec
- autobuilt 704adec

* Fri Jun 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-15
- buildah-1.2-15.gitb965fc4
- autobuilt b965fc4

* Thu Jun 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-14
- buildah-1.2-14.git1acccce
- autobuilt 1acccce

* Wed Jun 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-13
- buildah-1.2-13.git146c185
- autobuilt 146c185

* Tue Jun 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-12
- buildah-1.2-12.git16a33bd
- autobuilt 16a33bd

* Mon Jun 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-11
- buildah-1.2-11.git2ac95ea
- autobuilt 2ac95ea

* Sat Jun 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-10
- buildah-1.2-10.git0143a44
- autobuilt 0143a44

* Thu Jun 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-9
- buildah-1.2-9.git2441ff4
- autobuilt 2441ff4

* Wed Jun 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-8
- buildah-1.2-8.gitda7be32
- autobuilt da7be32

* Tue Jun 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-7
- buildah-1.2-7.git2064b29
- autobuilt 2064b29

* Mon Jun 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-6
- buildah-1.2-6.git93d8606
- autobuilt 93d8606

* Fri Jun 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-5
- buildah-1.2-5.gitfc438bb
- autobuilt fc438bb

* Thu Jun 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-4
- buildah-1.2-4.git73820fc
- autobuilt 73820fc

* Wed Jun 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-3
- buildah-1.2-3.git6c4bef7
- autobuilt 6c4bef7

* Tue Jun 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-2
- buildah-1.2-2.git94c1e6d
- autobuilt 94c1e6d

* Mon Jun 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-1
- buildah-1.2-1.gitb9983a6
- bump to 1.2
- autobuilt b9983a6

* Sun Jun 10 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.1-2
- Switch from skopeo-containers to containers-common

* Sun Jun 10 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.1-1
- Drop capabilities if running container processes as non root Print
  Warning message if cmd will not be used based on entrypoint Update
  01-intro.md Shouldn't add insecure registries to list of search
  registries Report errors on bad transports specification when pushing
  images Move parsing code out of common for namespaces and into
  pkg/parse.go Add disable-content-trust noop flag to bud Change freenode
  chan to buildah runCopyStdio(): don't close stdin unless we saw POLLHUP
  Add registry errors for pull runCollectOutput(): just read until the
  pipes are closed on us Run(): provide redirection for stdio rmi, rm: add
  test add mount test Add parameter judgment for commands that do not
  require parameters Add context dir to bud command in baseline test
  run.bats: check that we can run with symlinks in the bundle path Give
  better messages to users when image can not be found use absolute path
  for bundlePath Add environment variable to buildah --format rm: add
  validation to args and all option Accept json array input for config
  entrypoint Run(): process RunOptions.Mounts, and its flags Run(): only
  collect error output from stdio pipes if we created some Add OnBuild
  support for Dockerfiles Quick fix on demo readme run: fix validate flags
  buildah bud should require a context directory or URL Touchup tutorial
  for run changes Validate common bud and from flags images: Error if the
  specified imagename does not exist inspect: Increase err judgments to
  avoid panic add test to inspect buildah bud picks up ENV from base image
  Extend the amount of time travis_wait should wait Add a make target for
  Installing CNI plugins Add tests for namespace control flags copy.bats:
  check ownerships in the container Fix SELinux test errors when SELinux is
  enabled Add example CNI configurations Run: set supplemental group IDs
  Run: use a temporary mount namespace Use CNI to configure container
  networks add/secrets/commit: Use mappings when setting permissions on
  added content Add CLI options for specifying namespace and cgroup setup
  Always set mappings when using user namespaces Run(): break out creation
  of stdio pipe descriptors Read UID/GID mapping information from
  containers and images Additional bud CI tests Run integration tests under
  travis_wait in Travis build-using-dockerfile: add --annotation Implement
  --squash for build-using-dockerfile and commit Vendor in latest
  container/storage for devicemapper support add test to inspect Vendor
  github.com/onsi/ginkgo and github.com/onsi/gomega Test with Go 1.10, too
  Add console syntax highlighting to troubleshooting page bud.bats: print
  "$output" before checking its contents Manage "Run" containers more
  closely Break Builder.Run()'s "run runc" bits out util.ResolveName():
  handle completion for tagged/digested image names Handle /etc/hosts and
  /etc/resolv.conf properly in container Documentation fixes Make it easier
  to parse our temporary directory as an image name Makefile: list new pkg/
  subdirectoris as dependencies for buildah containerImageSource: return
  more-correct errors API cleanup: PullPolicy and TerminalPolicy should be
  types Make "run --terminal" and "run -t" aliases for "run --tty" Vendor
  github.com/containernetworking/cni v0.6.0 Update
  github.com/containers/storage Update github.com/projectatomic/libpod Add
  support for buildah bud --label buildah push/from can push and pull
  images with no reference Vendor in latest containers/image Update
  gometalinter to fix install.tools error Update troubleshooting with new
  run workaround Added a bud demo and tidied up Attempt to download file
  from url, if fails assume Dockerfile Add buildah bud CI tests for ENV
  variables Re-enable rpm .spec version check and new commit test Update
  buildah scratch demo to support el7 Added Docker compatibility demo
  Update to F28 and new run format in baseline test Touchup man page short
  options across man pages Added demo dir and a demo. chged distrorlease
  builder-inspect: fix format option Add cpu-shares short flag (-c) and
  cpu-shares CI tests Minor fixes to formatting in rpm spec changelog Fix
  rpm .spec changelog formatting CI tests and minor fix for cache related
  noop flags buildah-from: add effective value to mount propagation

* Sat Jun 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-22
- buildah-1.0-20.gitf449b28
- autobuilt f449b28

* Fri Jun 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-21
- buildah-1.0-19.gitc306342
- autobuilt c306342

* Wed Jun 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-20
- buildah-1.0-18.gitd3d097b
- autobuilt d3d097b

* Tue Jun 05 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0-19
- Merge #4 `Sync new tests from upstreamfirst`

* Mon Jun 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-18
- buildah-1.0-17.gitf90b6c0
- autobuilt f90b6c0

* Sun Jun 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-17
- buildah-1.0-16.git70641ee
- autobuilt 70641ee

* Sat Jun 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-16
- buildah-1.0-15.git03686e5
- autobuilt 03686e5

* Fri Jun 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-15
- buildah-1.0-14.git73bfd79
- autobuilt 73bfd79

* Thu May 31 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-14
- buildah-1.0-13.git5595d4d
- autobuilt 5595d4d

* Wed May 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-13
- buildah-1.0-12.gitebb0d8e
- autobuilt ebb0d8e

* Tue May 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-12
- buildah-1.0-11.git88affbd
- autobuilt 88affbd

* Fri May 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-11
- buildah-1.0-10.git25f4e8e
- autobuilt 25f4e8e

* Thu May 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-10
- buildah-1.0-9.git2749191
- autobuilt 2749191

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-9
- buildah-1.0-8.git3e320b9
- autobuilt 3e320b9

* Tue May 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-8
- buildah-1.0-7.git8515867
- autobuilt 8515867

* Sun May 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-7
- buildah-1.0-6.gitce8d467
- autobuilt ce8d467

* Sat May 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-6
- buildah-1.0-5.gitb9a1041
- autobuilt b9a1041

* Fri May 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-5
- buildah-1.0-4.git2ea3e11
- autobuilt 2ea3e11

* Wed May 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-4
- buildah-1.0-3.gitfe204e4
- autobuilt fe204e4

* Tue May 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-3
- buildah-1.0-2.git906ee37
- autobuilt 906ee37

* Mon May 07 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.0-2
- Remove buildah run cmd and entrypoint execution Add Files section with
  registries.conf to pertinent man pages Force "localhost" as a default
  registry Add --compress, --rm, --squash flags as a noop for bud Add FIPS
  mode secret to buildah run and bud Add config
  --comment/--domainname/--history-comment/--hostname Add support for
  --iidfile to bud and commit Add /bin/sh -c to entrypoint in config
  buildah images and podman images are listing different sizes Remove
  tarball as an option from buildah push --help Update entrypoint behaviour
  to match docker Display imageId after commit config: add support for
  StopSignal Allow referencing stages as index and names Add multi-stage
  builds support Vendor in latest imagebuilder, to get mixed case AS
  support Allow umount to have multi-containers Update buildah push doc
  buildah bud walks symlinks Imagename is required for commit atm, update
  manpage

* Mon May 07 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.0-1
- Remove buildah run cmd and entrypoint execution Add Files section with
  registries.conf to pertinent man pages Force "localhost" as a default
  registry Add --compress, --rm, --squash flags as a noop for bud Add FIPS
  mode secret to buildah run and bud Add config
  --comment/--domainname/--history-comment/--hostname Add support for
  --iidfile to bud and commit Add /bin/sh -c to entrypoint in config
  buildah images and podman images are listing different sizes Remove
  tarball as an option from buildah push --help Update entrypoint behaviour
  to match docker Display imageId after commit config: add support for
  StopSignal Allow referencing stages as index and names Add multi-stage
  builds support Vendor in latest imagebuilder, to get mixed case AS
  support Allow umount to have multi-containers Update buildah push doc
  buildah bud walks symlinks Imagename is required for commit atm, update
  manpage

* Mon May 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-29
- buildah-0.16-25.gitdd02e70
- autobuilt dd02e70

* Sat May 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-28
- buildah-0.16-24.git45772e8
- autobuilt 45772e8

* Fri May 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-27
- buildah-0.16-23.git6fe2b55
- autobuilt 6fe2b55

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-26
- buildah-0.16-22.gita4f5707
- autobuilt a4f5707

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-25
- buildah-0.16-21.gite130f2b
- autobuilt commit e130f2b

* Tue May 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-24
- buildah-0.16-20.gitadb8e6f
- autobuilt commit adb8e6f

* Sat Apr 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-23
- buildah-0.16-19.gitc50c287
- autobuilt commit c50c287

* Fri Apr 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-22
- buildah-0.16-18.gitca1704f
- autobuilt commit ca1704f

* Wed Apr 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-21
- buildah-0.16-17.git49abf82
- autobuilt commit 49abf82

* Tue Apr 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-20
- buildah-0.16-16.gitfdc3998
- autobuilt commit fdc3998

* Tue Apr 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-19
- buildah-0.16-15.gitb16a1ea
- autobuilt commit b16a1ea

* Fri Apr 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-18
- buildah-0.16-14.gitd84f05a
- autobuilt commit d84f05a

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-17
- buildah-0.16-13.gite008b73
- autobuilt commit e008b73

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-16
- buildah-0.16-12.git28a27a3
- autobuilt commit 28a27a3

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-15
- buildah-0.16-11.git45a4b81
- autobuilt commit 45a4b81

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-14
- buildah-0.16-10.git45a4b81
- autobuilt commit 45a4b81

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-13
- buildah-0.16-9.git6421399
- autobuilt commit 6421399

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-12
- buildah-0.16-8.git83d7d10
- autobuilt commit 83d7d10

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-11
- buildah-0.16-7.git83d7d10
- autobuilt commit 83d7d10

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-10
- buildah-0.16-6.git83d7d10
- autobuilt commit 83d7d10

* Mon Apr 16 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.16-9
- BR: make

* Mon Apr 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-8
- buildah-0.16-5.git4339223
- autobuilt commit 4339223

* Mon Apr 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-7
- buildah-0.16-4.git4339223
- autobuilt commit 4339223

* Mon Apr 09 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.16-6
- buildah-0.16-3.git4339223
- autobuilt commit 4339223

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.16-5
- buildah-0.16-2.git4743c2e
- autobuilt commit 4743c2e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.16-4
- Revert "buildah-0.16-2.git4743c2e"

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.16-3
- buildah-0.16-2.git4743c2e
- autobuilt commit 4743c2e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.16-2
- formatting changes and remove redundant Provides

* Wed Apr 04 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.16-1
- Add support for shell Vendor in latest containers/image docker-archive
  generates docker legacy compatible images -     Do not create $DiffID
  subdirectories for layers with no configs Ensure the layer IDs in legacy
  docker/tarfile metadata are unique -     docker-archive: repeated layers
  are symlinked in the tar file -         sysregistries: remove all
  trailing slashes -    Improve docker/* error messages -       Fix failure
  to make auth directory -    Create a new slice in
  Schema1.UpdateLayerInfos -        Drop unused
  storageImageDestination.{image,systemContext} -     Load a *storage.Image
  only once in storageImageSource -         Support gzip for docker-archive
  files -         Remove .tar extension from blob and config file names -
  ostree, src: support copy of compressed layers -        ostree: re-pull
  layer if it misses uncompressed_digest|uncompressed_size -      image:
  fix docker schema v1 -> OCI conversion -         Add
  /etc/containers/certs.d as default certs directory Change image time to
  locale, add troubleshooting.md, add logo to other mds Allow --cmd
  parameter to have commands as values Document the mounts.conf file Fix
  man pages to format correctly buildah from now supports pulling images
  using the following transports: docker-archive, oci-archive, and dir. If
  the user overrides the storage driver, the options should be dropped Show
  Config/Manifest as JSON string in inspect when format is not set Adds
  feature to pull compressed docker-archive files

* Tue Feb 27 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.15-1
- Fix handling of buildah run command options

* Sun Feb 25 2018 Peter Robinson <pbrobinson@gmail.com> - 0.13-3
- Build on ARMv7 too (Fedora supports containers on that arch too)

* Thu Feb 22 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.13-2
- Vendor in latest containers/storage This fixes a large SELinux bug. run:
  do not open /etc/hosts if not needed Add the following flags to buildah
  bud and from --add-host --cgroup-parent --cpu-period --cpu-quota --cpu-
  shares --cpuset-cpus --cpuset-mems --memory --memory-swap --security-opt
  --ulimit

* Thu Feb 22 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.13-1
- Vendor in latest containers/storage This fixes a large SELinux bug. run:
  do not open /etc/hosts if not needed Add the following flags to buildah
  bud and from --add-host --cgroup-parent --cpu-period --cpu-quota --cpu-
  shares --cpuset-cpus --cpuset-mems --memory --memory-swap --security-opt
  --ulimit

* Mon Feb 12 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.12-2
- Added handing for simpler error message for Unknown Dockerfile
  instructions. Change default certs directory to /etc/containers/certs.dir
  Vendor in latest containers/image Vendor in latest containers/storage
  build-using-dockerfile: set the 'author' field for MAINTAINER Return exit
  code 1 when buildah-rmi fails Trim the image reference to just its name
  before calling getImageName Touch up rmi -f usage statement Add --format
  and --filter to buildah containers Add --prune,-p option to rmi command
  Add authfile param to commit Fix --runtime-flag for buildah run and bud
  format should override quiet for images Allow all auth params to work
  with bud Do not overwrite directory permissions on --chown Unescape HTML
  characters output into the terminal Fix: setting the container name to
  the image Prompt for un/pwd if not supplied with --creds Make bud be
  really quiet Return a better error message when failed to resolve an
  image Update auth tests and fix bud man page

* Mon Feb 12 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.12-1
- Added handing for simpler error message for Unknown Dockerfile
  instructions. Change default certs directory to /etc/containers/certs.dir
  Vendor in latest containers/image Vendor in latest containers/storage
  build-using-dockerfile: set the 'author' field for MAINTAINER Return exit
  code 1 when buildah-rmi fails Trim the image reference to just its name
  before calling getImageName Touch up rmi -f usage statement Add --format
  and --filter to buildah containers Add --prune,-p option to rmi command
  Add authfile param to commit Fix --runtime-flag for buildah run and bud
  format should override quiet for images Allow all auth params to work
  with bud Do not overwrite directory permissions on --chown Unescape HTML
  characters output into the terminal Fix: setting the container name to
  the image Prompt for un/pwd if not supplied with --creds Make bud be
  really quiet Return a better error message when failed to resolve an
  image Update auth tests and fix bud man page

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.11-2
- buildah-0.11-2
- Resolves: upstream gh#432
- enable debuginfo for non-fedora packages

* Wed Jan 17 2018 Daniel J Walsh <dwalsh@redhat.com> - 0.11-1
- Add --all to remove containers Add --all functionality to rmi Show ctrid
  when doing rm -all Ignore sequential duplicate layers when reading v2s1
  Lots of minor bug fixes Vendor in latest containers/image and
  containers/storage

* Tue Dec 26 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.10-4
- Fix checkin

* Tue Dec 26 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.10-3
- Fix checkin

* Sun Dec 24 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.10-2
- Display Config and Manifest as strings Bump containers/image Use
  configured registries to resolve image names Update to work with newer
  image library Add --chown option to add/copy commands

* Sun Dec 24 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.10-1
- Display Config and Manifest as strings Bump containers/image Use
  configured registries to resolve image names Update to work with newer
  image library Add --chown option to add/copy commands

* Tue Dec 12 2017 Yevhenii Shapovalov <yshapova@redhat.com> - 0.9-4
- add tests

* Tue Dec 05 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.9-3
- remove ostree-devel from builddep

* Mon Dec 04 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.9-2
- remove git from builddep

* Sat Dec 02 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.9-1
- Allow push to use the image id Make sure builtin volumes have the correct
  label

* Wed Nov 22 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.8-1
- Buildah bud was failing on SELinux machines, this fixes this Block access
  to certain kernel file systems inside of the container

* Thu Nov 16 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.7-1
- Ignore errors when trying to read containers buildah.json for loading
  SELinux reservations Use credentials from kpod login for buildah

* Wed Nov 15 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.6-2
- Adds support for converting manifest types when using the dir transport
  Rework how we do UID resolution in images Bump github.com/vbatts/tar-
  split Set option.terminal appropriately in run

* Wed Nov 15 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.6-1
- Adds support for converting manifest types when using the dir transport
  Rework how we do UID resolution in images Bump github.com/vbatts/tar-
  split Set option.terminal appropriately in run

* Wed Nov 08 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.5-2
- Bump github.com/vbatts/tar-split Fixes CVE That could allow a container
  image to cause a DOS

* Wed Nov 08 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.5-1
- Add secrets patch to buildah Add proper SELinux labeling to buildah run
  Add tls-verify to bud command Make filtering by date use the image's date
  images: don't list unnamed images twice Fix timeout issue Add further tty
  verbiage to buildah run Make inspect try an image on failure if type not
  specified Add support for `buildah run --hostname` Tons of bug fixes and
  code cleanup

* Fri Sep 22 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.4-1
- Add default transport to push if not provided Avoid trying to print a nil
  ImageReference Add authentication to commit and push Add information on
  buildah from man page on transports Remove --transport flag Run: do not
  complain about missing volume locations Add credentials to buildah from
  Remove export command Run(): create the right working directory Improve
  "from" behavior with unnamed references Avoid parsing image metadata for
  dates and layers Read the image's creation date from public API Bump
  containers/storage and containers/image Don't panic if an image's ID
  can't be parsed Turn on --enable-gc when running gometalinter rmi: handle
  truncated image IDs

* Tue Aug 15 2017 Josh Boyer <jwboyer@redhat.com> - 0.3-5
- Build for s390x as well

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-4
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.3-2
- Bump for inclusion of OCI 1.0 Runtime and Image Spec

* Thu Jul 20 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.3-1
- Bump for inclusion of OCI 1.0 Runtime and Image Spec

* Tue Jul 18 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.2.0-2
- buildah run: Add support for -- ending options parsing buildah Add/Copy
  support for glob syntax buildah commit: Add flag to remove containers on
  commit buildah push: Improve man page and help information buildah run:
  add a way to disable PTY allocation Buildah docs: clarify --runtime-flag
  of run command Update to match newer storage and image-spec APIs Update
  containers/storage and containers/image versions buildah export: add
  support buildah images: update commands buildah images: Add JSON output
  option buildah rmi: update commands buildah containers: Add JSON output
  option buildah version: add command buildah run: Handle run without an
  explicit command correctly Ensure volume points get created, and with
  perms buildah containers: Add a -a/--all option

* Tue Jul 18 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.2.0-1
- buildah run: Add support for -- ending options parsing buildah Add/Copy
  support for glob syntax buildah commit: Add flag to remove containers on
  commit buildah push: Improve man page and help information buildah run:
  add a way to disable PTY allocation Buildah docs: clarify --runtime-flag
  of run command Update to match newer storage and image-spec APIs Update
  containers/storage and containers/image versions buildah export: add
  support buildah images: update commands buildah images: Add JSON output
  option buildah rmi: update commands buildah containers: Add JSON output
  option buildah version: add command buildah run: Handle run without an
  explicit command correctly Ensure volume points get created, and with
  perms buildah containers: Add a -a/--all option

* Wed Jun 14 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.0-4
- fix summary

* Wed Jun 14 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.0-3
- Release Candidate 1 All features have now been implemented.

* Wed Jun 14 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.0-2
- Release Candidate 1 All features have now been implemented.

* Wed Jun 14 2017 Daniel J Walsh <dwalsh@redhat.com> - 0.1.0-1
- Release Candidate 1 All features have now been implemented.

* Tue May 02 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.0.1-2
- buildah-0.0.1-1.gita0a5333
- Resolves: #1444618 - initial build

* Thu May 24 2018 Bruno Goncalves <bgoncalv@redhat.com> - 0.16-1
- Sync new tests from upstreamfirst

* Sat Jan 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-3
- buildah-1.14.0-0.3.dev.gitc42f440
- autobuilt c42f440

* Fri Jan 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-2
- buildah-1.14.0-0.2.dev.git8d41b83
- autobuilt 8d41b83

* Tue Dec 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-1
- buildah-1.14.0-0.1.dev.git726e24d
- bump to 1.14.0
- autobuilt 726e24d

* Sun Dec 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-10
- buildah-1.13.0-0.10.dev.git6941254
- autobuilt 6941254

* Sun Dec 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-9
- buildah-1.13.0-0.9.dev.git41b7852
- autobuilt 41b7852

* Fri Dec 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-8
- buildah-1.13.0-0.8.dev.git9588a82
- autobuilt 9588a82

* Thu Dec 19 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-7
- buildah-1.13.0-0.7.dev.gite6815a1
- autobuilt e6815a1

* Thu Dec 19 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-6
- buildah-1.13.0-0.6.dev.git2959a6b
- autobuilt 2959a6b

* Wed Dec 18 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-5
- buildah-1.13.0-0.5.dev.git188269a
- autobuilt 188269a

* Wed Dec 18 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-4
- buildah-1.13.0-0.4.dev.git0662a4e
- autobuilt 0662a4e

* Tue Dec 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-3
- buildah-1.13.0-0.3.dev.gitacc7c35
- autobuilt acc7c35

* Mon Dec 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-2
- buildah-1.13.0-0.2.dev.git068b6f5
- autobuilt 068b6f5

* Fri Dec 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.13.0-1
- buildah-1.13.0-0.1.dev.gite28c43d
- bump to 1.13.0
- autobuilt e28c43d

* Fri Dec 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-94
- buildah-1.12.0-0.88.dev.gitdb59421
- autobuilt db59421

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-93
- buildah-1.12.0-0.87.dev.git70b101f
- autobuilt 70b101f

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-92
- buildah-1.12.0-0.86.dev.gitbc8feee
- autobuilt bc8feee

* Fri Dec 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-91
- buildah-1.12.0-0.85.dev.git8d6869b
- autobuilt 8d6869b

* Fri Dec 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-90
- buildah-1.12.0-0.84.dev.git8fc5b01
- autobuilt 8fc5b01

* Fri Dec 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-89
- buildah-1.12.0-0.83.dev.gitc038827
- autobuilt c038827

* Fri Dec 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-88
- buildah-1.12.0-0.82.dev.gite47145c
- autobuilt e47145c

* Thu Dec 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-87
- buildah-1.12.0-0.81.dev.git2a82d07
- autobuilt 2a82d07

* Wed Dec 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-86
- buildah-1.12.0-0.80.dev.git357d4ae
- autobuilt 357d4ae

* Wed Dec 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-85
- buildah-1.12.0-0.79.dev.gitd55a9f8
- autobuilt d55a9f8

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-84
- buildah-1.12.0-0.78.dev.gited0a329
- autobuilt ed0a329

* Mon Nov 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-83
- buildah-1.12.0-0.77.dev.git4cf37c2
- autobuilt 4cf37c2

* Sat Nov 23 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-82
- buildah-1.12.0-0.76.dev.git8fd3148
- autobuilt 8fd3148

* Thu Nov 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-81
- buildah-1.12.0-0.75.dev.git92ff215
- autobuilt 92ff215

* Wed Nov 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-80
- buildah-1.12.0-0.74.dev.gitcd88667
- autobuilt cd88667

* Wed Nov 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-79
- buildah-1.12.0-0.73.dev.git1e6a70c
- autobuilt 1e6a70c

* Tue Nov 19 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-78
- buildah-1.12.0-0.72.dev.git6a555a0
- autobuilt 6a555a0

* Sat Nov 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-77
- buildah-1.12.0-0.71.dev.git9ff68b3
- autobuilt 9ff68b3

* Wed Nov 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-76
- buildah-1.12.0-0.70.dev.gitc5244fe
- autobuilt c5244fe

* Tue Nov 12 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-75
- buildah-1.12.0-0.69.dev.git985e8dc
- autobuilt 985e8dc

* Tue Nov 12 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-74
- buildah-1.12.0-0.68.dev.git85ab067
- autobuilt 85ab067

* Tue Nov 12 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-73
- buildah-1.12.0-0.67.dev.git7535655
- autobuilt 7535655

* Fri Nov 08 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-72
- buildah-1.12.0-0.66.dev.gite3bb278
- autobuilt e3bb278

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-71
- buildah-1.12.0-0.65.dev.gita880001
- autobuilt a880001

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-70
- buildah-1.12.0-0.64.dev.gitf995696
- autobuilt f995696

* Thu Nov 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-69
- buildah-1.12.0-0.63.dev.git147d106
- autobuilt 147d106

* Wed Nov 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-68
- buildah-1.12.0-0.62.dev.git89bc2a6
- autobuilt 89bc2a6

* Wed Nov 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-67
- buildah-1.12.0-0.61.dev.gitec970d5
- autobuilt ec970d5

* Tue Nov 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-66
- buildah-1.12.0-0.60.dev.gitfba62fd
- autobuilt fba62fd

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-65
- buildah-1.12.0-0.59.dev.git1967973
- autobuilt 1967973

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-64
- buildah-1.12.0-0.58.dev.git20e92ff
- autobuilt 20e92ff

* Thu Oct 31 2019 Ed Santiago <santiago@redhat.com> - 1.12.0-63
- Oops - typo fix: IMGTYPE, not imgtest

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-62
- buildah-1.12.0-0.57.dev.git141b5a1
- autobuilt 141b5a1

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-61
- buildah-1.12.0-0.56.dev.git332a889
- autobuilt 332a889

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-60
- buildah-1.12.0-0.55.dev.git8e26456
- autobuilt 8e26456

* Wed Oct 30 2019 Ed Santiago <santiago@redhat.com> - 1.12.0-59
- Gating tests: timeout: bump to 60m (from 30)

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-58
- buildah-1.12.0-0.54.dev.git1ff7043
- autobuilt 1ff7043

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-57
- buildah-1.12.0-0.53.dev.giteaad6b4
- autobuilt eaad6b4

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-56
- buildah-1.12.0-0.52.dev.git999fa43
- autobuilt 999fa43

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-55
- buildah-1.12.0-0.51.dev.git751f92e
- autobuilt 751f92e

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-54
- buildah-1.12.0-0.50.dev.gitb023cde
- autobuilt b023cde

* Tue Oct 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-53
- buildah-1.12.0-0.49.dev.git66701d4
- autobuilt 66701d4

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-52
- buildah-1.12.0-0.48.dev.gitc2dc46a
- autobuilt c2dc46a

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-51
- buildah-1.12.0-0.47.dev.git691c394
- autobuilt 691c394

* Fri Oct 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-50
- buildah-1.12.0-0.46.dev.gitcddb66e
- autobuilt cddb66e

* Wed Oct 23 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-49
- buildah-1.12.0-0.45.dev.gitfa4eec7
- autobuilt fa4eec7

* Mon Oct 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-48
- buildah-1.12.0-0.44.dev.git049fdf4
- autobuilt 049fdf4

* Mon Oct 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-47
- buildah-1.12.0-0.43.dev.git1d3db17
- autobuilt 1d3db17

* Sun Oct 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-46
- buildah-1.12.0-0.42.dev.git120c37f
- autobuilt 120c37f

* Wed Oct 16 2019 Ed Santiago <santiago@redhat.com> - 1.12.0-45
- Gating tests

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-44
- buildah-1.12.0-0.41.dev.git0f7148b
- autobuilt 0f7148b

* Wed Oct 16 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.12.0-43
- buildah-1.12.0-0.40.dev.git389d49b
- install imgtype binary

* Wed Oct 16 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.12.0-42
- libseccomp >= 2.4.1-0 for centos

* Wed Oct 16 2019 Ed Santiago <santiago@redhat.com> - 1.12.0-41
- New subpackage: buildah-tests intended for use in fedora gating tests.
  Subpackage already exists in RHEL8.

* Tue Oct 15 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-40
- buildah-1.12.0-0.39.dev.git389d49b
- autobuilt 389d49b

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-39
- buildah-1.12.0-0.38.dev.gitd6f11ba
- autobuilt d6f11ba

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-38
- buildah-1.12.0-0.37.dev.git68b2aa5
- autobuilt 68b2aa5

* Wed Oct 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-37
- buildah-1.12.0-0.36.dev.git13330a4
- autobuilt 13330a4

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-36
- buildah-1.12.0-0.35.dev.git7a7e1f0
- autobuilt 7a7e1f0

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-35
- buildah-1.12.0-0.34.dev.git797e618
- autobuilt 797e618

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-34
- buildah-1.12.0-0.33.dev.gitb298906
- autobuilt b298906

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-33
- buildah-1.12.0-0.32.dev.gitf50b55d
- autobuilt f50b55d

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-32
- buildah-1.12.0-0.31.dev.gite400691
- autobuilt e400691

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-31
- buildah-1.12.0-0.30.dev.git96f9993
- autobuilt 96f9993

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-30
- buildah-1.12.0-0.29.dev.gitc771c56
- autobuilt c771c56

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-29
- buildah-1.12.0-0.28.dev.gite2c33f3
- autobuilt e2c33f3

* Tue Oct 01 2019 Debarshi Ray <rishi@fedoraproject.org> - 1.12.0-28
- Require crun >= 0.10-1

* Tue Oct 01 2019 Debarshi Ray <rishi@fedoraproject.org> - 1.12.0-27
- Switch to crun for Cgroups v2 support

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-26
- buildah-1.12.0-0.25.dev.gitcf933c8
- autobuilt cf933c8

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-25
- buildah-1.12.0-0.24.dev.gitbf04bf1
- autobuilt bf04bf1

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-24
- buildah-1.12.0-0.23.dev.gitfc06a4d
- autobuilt fc06a4d

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-23
- buildah-1.12.0-0.22.dev.gitd3d9cec
- autobuilt d3d9cec

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-22
- buildah-1.12.0-0.21.dev.gita32fc96
- autobuilt a32fc96

* Sat Sep 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-21
- buildah-1.12.0-0.20.dev.git61e32a5
- autobuilt 61e32a5

* Sat Sep 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-20
- buildah-1.12.0-0.19.dev.gitc3b1ec6
- autobuilt c3b1ec6

* Wed Sep 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-19
- buildah-1.12.0-0.18.dev.git04150e0
- autobuilt 04150e0

* Tue Sep 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-18
- buildah-1.12.0-0.17.dev.gitd2c1fd8
- autobuilt d2c1fd8

* Tue Sep 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-17
- buildah-1.12.0-0.16.dev.git6abc01c
- autobuilt 6abc01c

* Mon Sep 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-16
- buildah-1.12.0-0.15.dev.gite9969bc
- autobuilt e9969bc

* Fri Sep 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-15
- buildah-1.12.0-0.14.dev.git10b0e7a
- autobuilt 10b0e7a

* Fri Sep 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-14
- buildah-1.12.0-0.13.dev.git4ce6fba
- autobuilt 4ce6fba

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-13
- buildah-1.12.0-0.12.dev.git9cac447
- autobuilt 9cac447

* Sat Sep 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-12
- buildah-1.12.0-0.11.dev.git20a33e0
- autobuilt 20a33e0

* Sat Sep 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-11
- buildah-1.12.0-0.10.dev.git9bf6b5e
- autobuilt 9bf6b5e

* Fri Sep 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-10
- buildah-1.12.0-0.9.dev.gitf54c965
- autobuilt f54c965

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-9
- buildah-1.12.0-0.8.dev.git3f6ad0f
- autobuilt 3f6ad0f

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-8
- buildah-1.12.0-0.7.dev.git9f2a682
- autobuilt 9f2a682

* Thu Sep 05 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.12.0-7
- add built_tag macro(non-rawhide only)

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-6
- buildah-1.12.0-0.6.dev.git4da1d5d
- autobuilt 4da1d5d

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-5
- buildah-1.12.0-0.5.dev.git34f1ae6
- autobuilt 34f1ae6

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-4
- buildah-1.12.0-0.4.dev.gitcc80ccc
- autobuilt cc80ccc

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-3
- buildah-1.12.0-0.3.dev.gitb643073
- autobuilt b643073

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-2
- buildah-1.12.0-0.2.dev.git15773bd
- autobuilt 15773bd

* Sat Aug 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.12.0-1
- buildah-1.12.0-0.1.dev.git1a1a728
- bump to 1.12.0
- autobuilt 1a1a728

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-38
- buildah-1.11.0-0.38.dev.git57db70c
- autobuilt 57db70c

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-37
- buildah-1.11.0-0.37.dev.gite930951
- autobuilt e930951

* Thu Aug 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-36
- buildah-1.11.0-0.36.dev.gitecf5b72
- autobuilt ecf5b72

* Thu Aug 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-35
- buildah-1.11.0-0.35.dev.git5671417
- autobuilt 5671417

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-34
- buildah-1.11.0-0.34.dev.git689f8ed
- autobuilt 689f8ed

* Thu Aug 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-33
- buildah-1.11.0-0.33.dev.git6b5f8ba
- autobuilt 6b5f8ba

* Thu Aug 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-32
- buildah-1.11.0-0.32.dev.gitff72568
- autobuilt ff72568

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-31
- buildah-1.11.0-0.31.dev.git376e52e
- autobuilt 376e52e

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-30
- buildah-1.11.0-0.30.dev.git5a1c733
- autobuilt 5a1c733

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-29
- buildah-1.11.0-0.29.dev.git3ad937b
- autobuilt 3ad937b

* Tue Aug 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-28
- buildah-1.11.0-0.28.dev.gitfa68ed6
- autobuilt fa68ed6

* Tue Aug 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-27
- buildah-1.11.0-0.27.dev.gitb288b7a
- autobuilt b288b7a

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-26
- buildah-1.11.0-0.26.dev.gitc1a2d4f
- autobuilt c1a2d4f

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-25
- buildah-1.11.0-0.25.dev.git51415ec
- autobuilt 51415ec

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-24
- buildah-1.11.0-0.24.dev.gitc2c52ba
- autobuilt c2c52ba

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-23
- buildah-1.11.0-0.23.dev.gitebf6f51
- autobuilt ebf6f51

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-22
- buildah-1.11.0-0.22.dev.git36dcedb
- autobuilt 36dcedb

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-21
- buildah-1.11.0-0.21.dev.gitab0286f
- autobuilt ab0286f

* Thu Aug 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-20
- buildah-1.11.0-0.20.dev.git1ce1130
- autobuilt 1ce1130

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-19
- buildah-1.11.0-0.19.dev.gitd88c26b
- autobuilt d88c26b

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-18
- buildah-1.11.0-0.18.dev.git5c98d3c
- autobuilt 5c98d3c

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-17
- buildah-1.11.0-0.17.dev.git3f5436f
- autobuilt 3f5436f

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-16
- buildah-1.11.0-0.16.dev.gita99139c
- autobuilt a99139c

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-15
- buildah-1.11.0-0.15.dev.git2df08f0
- autobuilt 2df08f0

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-14
- buildah-1.11.0-0.14.dev.git96a136e
- autobuilt 96a136e

* Sun Aug 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-13
- buildah-1.11.0-0.13.dev.git7180312
- autobuilt 7180312

* Sat Aug 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-12
- buildah-1.11.0-0.12.dev.git0dfb6f5
- autobuilt 0dfb6f5

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-11
- buildah-1.11.0-0.11.dev.git60d5480
- autobuilt 60d5480

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-10
- buildah-1.11.0-0.10.dev.git60c0088
- autobuilt 60c0088

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-9
- buildah-1.11.0-0.9.dev.gitc953216
- autobuilt c953216

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-8
- buildah-1.11.0-0.8.dev.gitf892eb6
- autobuilt f892eb6

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-7
- buildah-1.11.0-0.7.dev.git95cb061
- autobuilt 95cb061

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-6
- buildah-1.11.0-0.6.dev.gitf4cfe9c
- autobuilt f4cfe9c

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-5
- buildah-1.11.0-0.5.dev.git03aa807
- autobuilt 03aa807

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-4
- buildah-1.11.0-0.4.dev.gitbafcf88
- autobuilt bafcf88

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-3
- buildah-1.11.0-0.3.dev.git232f7c6
- autobuilt 232f7c6

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-2
- buildah-1.11.0-0.2.dev.git1de958d
- autobuilt 1de958d

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-1
- buildah-1.11.0-0.1.dev.gitac5031d
- bump to 1.11.0
- autobuilt ac5031d

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-14
- buildah-1.9.3-0.68.dev.git3117f5e
- autobuilt 3117f5e

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-13
- buildah-1.9.3-0.67.dev.git4d017d6
- autobuilt 4d017d6

* Wed Jul 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-12
- buildah-1.9.3-0.66.dev.gitc00f548
- autobuilt c00f548

* Wed Jul 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-11
- buildah-1.9.3-0.65.dev.git677b771
- autobuilt 677b771

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-10
- buildah-1.9.3-0.64.dev.gitb7a0ed0
- autobuilt b7a0ed0

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-9
- buildah-1.9.3-0.63.dev.git5bab9b0
- autobuilt 5bab9b0

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-8
- buildah-1.9.3-0.62.dev.git4ccb343
- autobuilt 4ccb343

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-7
- buildah-1.9.3-0.61.dev.gita74bdd3
- autobuilt a74bdd3

* Sat Jul 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-6
- buildah-1.9.3-0.60.dev.git6b214d2
- autobuilt 6b214d2

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-5
- buildah-1.9.3-0.59.dev.git73401a4
- autobuilt 73401a4

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-3
- buildah-1.9.3-0.57.dev.git6bd0551
- autobuilt 6bd0551

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-2
- buildah-1.9.3-0.56.dev.git555b5a5
- autobuilt 555b5a5

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-1
- buildah-1.9.3-0.55.dev.git2110f05
- bump to 1.9.3
- autobuilt 2110f05

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-10
- buildah-1.9.2-0.54.dev.gitd7dec37
- autobuilt d7dec37

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-9
- buildah-1.9.2-0.53.dev.git5da3c8c
- autobuilt 5da3c8c

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-8
- buildah-1.9.2-0.52.dev.git4ae0e14
- autobuilt 4ae0e14

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-7
- buildah-1.9.2-0.51.dev.git8da4cb4
- autobuilt 8da4cb4

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-6
- buildah-1.9.2-0.50.dev.gitbe51b9b
- autobuilt be51b9b

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-5
- buildah-1.9.2-0.49.dev.gitb33b87b
- autobuilt b33b87b

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-4
- buildah-1.9.2-0.48.dev.git16e3010
- autobuilt 16e3010

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-3
- buildah-1.9.2-0.47.dev.gitbb5cbf1
- autobuilt bb5cbf1

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-2
- buildah-1.9.2-0.46.dev.git2249ba3
- autobuilt 2249ba3

* Sun Jul 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-1
- buildah-1.9.2-0.45.dev.gitd419737
- bump to 1.9.2
- autobuilt d419737

* Wed Jul 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-8
- buildah-1.9.1-0.44.dev.git5d723ff
- autobuilt 5d723ff

* Wed Jul 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-7
- %%gobuild defined by default on fedora

* Sun Jul 07 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-6
- buildah-1.9.1-0.43.dev.gite160a63
- built e160a63
- add centos conditionals
- use new name for go-md2man dep

* Sat Jun 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-5
- buildah-1.9.1-0.42.dev.git1d11851
- autobuilt 1d11851

* Fri Jun 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-4
- buildah-1.9.1-0.41.dev.git07aaf5e
- autobuilt 07aaf5e

* Thu Jun 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-3
- buildah-1.9.1-0.40.dev.gitc22957b
- autobuilt c22957b

* Tue Jun 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-2
- buildah-1.9.1-0.39.dev.git2c4f388
- autobuilt 2c4f388

* Sun Jun 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-1
- buildah-1.9.1-0.38.dev.git0b84b23
- bump to 1.9.1
- autobuilt 0b84b23

* Sat Jun 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-39
- buildah-1.9.0-0.37.dev.git77fa9dd
- autobuilt 77fa9dd

* Fri Jun 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-38
- buildah-1.9.0-0.36.dev.gitdc7b50c
- autobuilt dc7b50c

* Thu Jun 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-37
- buildah-1.9.0-0.35.dev.git2191ba6
- autobuilt 2191ba6

* Wed Jun 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-36
- buildah-1.9.0-0.34.dev.gitdcbf193
- autobuilt dcbf193

* Tue Jun 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-35
- buildah-1.9.0-0.33.dev.git78dcf2f
- autobuilt 78dcf2f

* Mon Jun 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-34
- buildah-1.9.0-0.32.dev.git4ae0a69
- autobuilt 4ae0a69

* Sun Jun 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-33
- buildah-1.9.0-0.31.dev.gitd172dd9
- autobuilt d172dd9

* Sat Jun 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-32
- buildah-1.9.0-0.30.dev.git2da8755
- autobuilt 2da8755

* Fri Jun 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-31
- buildah-1.9.0-0.29.dev.gitad4f235
- autobuilt ad4f235

* Thu Jun 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-30
- buildah-1.9.0-0.28.dev.gite0306bb
- autobuilt e0306bb

* Wed Jun 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-29
- buildah-1.9.0-0.27.dev.gitaa06a77
- autobuilt aa06a77

* Sun Jun 02 2019 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.0-28
- buildable on centos7

* Sun Jun 02 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-27
- buildah-1.9.0-0.26.dev.gita086ec8
- build for all arches

* Sun Jun 02 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-26
- update URL, cosmetic changes in changelog

* Sun Jun 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-25
- buildah-1.9.0-0.25.dev.git7016ce6
- autobuilt 7016ce6

* Sat Jun 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-24
- buildah-1.9.0-0.24.dev.git3104ddf
- autobuilt 3104ddf

* Fri May 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-23
- buildah-1.9.0-0.23.dev.git53be3d3
- autobuilt 53be3d3

* Thu May 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-22
- buildah-1.9.0-0.22.dev.git2a962f1
- autobuilt 2a962f1

* Wed May 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-21
- buildah-1.9.0-0.21.dev.gitfa7f030
- autobuilt fa7f030

* Tue May 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-20
- buildah-1.9.0-0.20.dev.gited77a92
- autobuilt ed77a92

* Sat May 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-19
- buildah-1.9.0-0.19.dev.git8e48a65
- autobuilt 8e48a65

* Fri May 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-18
- buildah-1.9.0-0.18.dev.git4e1ca7c
- autobuilt 4e1ca7c

* Fri May 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-17
- buildah-1.9.0-0.17.dev.git00f5164
- autobuilt 00f5164

* Thu May 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-16
- buildah-1.9.0-0.16.dev.gitbc9c276
- autobuilt bc9c276

* Tue May 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-15
- buildah-1.9.0-0.15.dev.gitbcc5e51
- autobuilt bcc5e51

* Sun May 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-14
- buildah-1.9.0-0.14.dev.git7793c51
- autobuilt 7793c51

* Sat May 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-13
- buildah-1.9.0-0.13.dev.git3bf8547
- autobuilt 3bf8547

* Fri May 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-12
- buildah-1.9.0-0.12.dev.git63808f9
- autobuilt 63808f9

* Thu May 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-11
- buildah-1.9.0-0.11.dev.gitc0633e3
- autobuilt c0633e3

* Wed May 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-10
- buildah-1.9.0-0.10.dev.git4c6b09c
- autobuilt 4c6b09c

* Tue May 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-9
- buildah-1.9.0-0.9.dev.git7ae362b
- autobuilt 7ae362b

* Mon May 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-8
- buildah-1.9.0-0.8.dev.git74a3195
- autobuilt 74a3195

* Sun May 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-7
- buildah-1.9.0-0.7.dev.gitab8678a
- autobuilt ab8678a

* Sat May 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-6
- buildah-1.9.0-0.6.dev.gitc654b18
- autobuilt c654b18

* Sat May 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-5
- buildah-1.9.0-0.5.dev.gite9184ea
- autobuilt e9184ea

* Fri May 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-4
- buildah-1.9.0-0.4.dev.git59da11d
- autobuilt 59da11d

* Thu May 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-3
- buildah-1.9.0-0.3.dev.git78fb869
- autobuilt 78fb869

* Tue Apr 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-2
- buildah-1.9.0-0.2.dev.git0e30da6
- autobuilt 0e30da6

* Mon Apr 29 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-1
- buildah-1.9.0-0.1.dev.gitddbd805
- bump to v1.9.0-dev
- update release tag format for unreleased builds

* Thu Apr 25 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8-1
- Revert "buildah-1:1.8-0.42.dev.gitbdbedfd"

* Thu Apr 25 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8-3
- Revert "buildah-1:1.8-0.43.dev.gitefa156f"

* Thu Apr 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:1.8-2
- buildah-1:1.8-0.43.dev.gitefa156f
- autobuilt efa156f

* Wed Apr 24 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.8-1
- buildah-1:1.8-0.42.dev.gitbdbedfd
- Resolves: #1702419 - bump Epoch to correct release tag

* Wed Apr 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-40
- buildah-1.8-41.dev.gitbdbedfd
- autobuilt bdbedfd

* Tue Apr 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-39
- buildah-1.8-40.dev.gitb466cbd
- autobuilt b466cbd

* Sat Apr 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-38
- buildah-1.8-39.dev.git2f0179f
- autobuilt 2f0179f

* Fri Apr 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-37
- buildah-1.8-38.dev.git135542e
- autobuilt 135542e

* Thu Apr 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-36
- buildah-1.8-37.dev.gite879079
- autobuilt e879079

* Wed Apr 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-35
- buildah-1.8-36.dev.gitd8fe400
- autobuilt d8fe400

* Mon Apr 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-34
- buildah-1.8-35.dev.gitfcc12bd
- autobuilt fcc12bd

* Sat Apr 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-33
- buildah-1.8-34.dev.gitd43787b
- autobuilt d43787b

* Fri Apr 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-32
- buildah-1.8-33.dev.git316bd0a
- autobuilt 316bd0a

* Wed Apr 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-31
- buildah-1.8-32.dev.git021d607
- autobuilt 021d607

* Tue Apr 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-30
- buildah-1.8-31.dev.git610eb7a
- autobuilt 610eb7a

* Sun Apr 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-29
- buildah-1.8-30.dev.git25b7c11
- autobuilt 25b7c11

* Sat Apr 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-28
- buildah-1.8-29.dev.git29a6c81
- autobuilt 29a6c81

* Fri Apr 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-27
- buildah-1.8-28.dev.gitac66d78
- autobuilt ac66d78

* Mon Apr 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-26
- buildah-1.8-27.dev.git9e1967a
- autobuilt 9e1967a

* Sat Mar 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-25
- buildah-1.8-26.dev.git13d9142
- autobuilt 13d9142

* Fri Mar 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-24
- buildah-1.8-25.dev.gita9bd025
- autobuilt a9bd025

* Thu Mar 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-23
- buildah-1.8-24.dev.gitc933fe4
- autobuilt c933fe4

* Wed Mar 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-22
- buildah-1.8-23.dev.git3d74031
- autobuilt 3d74031

* Mon Mar 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-21
- buildah-1.8-22.dev.git03fae01
- autobuilt 03fae01

* Sat Mar 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-20
- buildah-1.8-21.dev.gitd1c75ea
- autobuilt d1c75ea

* Fri Mar 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-19
- buildah-1.8-20.dev.gitc6ae5c5
- autobuilt c6ae5c5

* Thu Mar 21 2019 Daniel J Walsh <dwalsh@redhat.com> - 1.8-18
- Complile with SELinux enabled

* Thu Mar 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-17
- buildah-1.8-18.dev.gitbe0c8d2
- autobuilt be0c8d2

* Wed Mar 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-16
- buildah-1.8-17.dev.git9d6da3a
- autobuilt 9d6da3a

* Tue Mar 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-15
- buildah-1.8-16.dev.git1ba9201
- autobuilt 1ba9201

* Sat Mar 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-14
- buildah-1.8-15.dev.gita986f34
- autobuilt a986f34

* Fri Mar 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-13
- buildah-1.8-14.dev.gitc691d09
- autobuilt c691d09

* Thu Mar 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-12
- buildah-1.8-13.dev.git3b497ff
- autobuilt 3b497ff

* Wed Mar 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-11
- buildah-1.8-12.dev.git3ba8822
- autobuilt 3ba8822

* Sun Mar 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-10
- buildah-1.8-11.dev.git36605c2
- autobuilt 36605c2

* Sat Mar 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-9
- buildah-1.8-10.dev.git984ea9b
- autobuilt 984ea9b

* Thu Mar 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-8
- buildah-1.8-9.dev.git0a8ec97
- autobuilt 0a8ec97

* Wed Mar 06 2019 Daniel J Walsh <dwalsh@redhat.com> - 1.8-7
- Add recommends for fuse-overlay and slirp4netns

* Wed Mar 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-6
- buildah-1.8-7.dev.git3afba37
- autobuilt 3afba37

* Tue Mar 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-5
- buildah-1.8-6.dev.git11dd219
- autobuilt 11dd219

* Fri Mar 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-4
- buildah-1.8-5.dev.git8b1d11f
- autobuilt 8b1d11f

* Thu Feb 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-3
- buildah-1.8-4.dev.git95a5089
- autobuilt 95a5089

* Tue Feb 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-2
- buildah-1.8-3.dev.git6c1a4cc
- autobuilt 6c1a4cc

* Sat Feb 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-1
- buildah-1.8-2.dev.git8c3d8b1
- bump to 1.8
- autobuilt 8c3d8b1

* Fri Feb 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-19
- buildah-1.7-20.dev.git873f001
- autobuilt 873f001

* Thu Feb 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-18
- buildah-1.7-19.dev.gitdb6e7bb
- autobuilt db6e7bb

* Wed Feb 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-17
- buildah-1.7-18.dev.git1b02a7e
- autobuilt 1b02a7e

* Mon Feb 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-16
- buildah-1.7-17.dev.git146a0fc
- autobuilt 146a0fc

* Sat Feb 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-15
- buildah-1.7-16.dev.git80fcb24
- autobuilt 80fcb24

* Fri Feb 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-14
- buildah-1.7-15.dev.git40d4d59
- autobuilt 40d4d59

* Thu Feb 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-13
- buildah-1.7-14.dev.gite4c4d46
- autobuilt e4c4d46

* Sun Feb 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-12
- buildah-1.7-13.dev.git711f9ea
- autobuilt 711f9ea

* Fri Feb 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-11
- buildah-1.7-12.dev.git310363c
- autobuilt 310363c

* Wed Feb 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-10
- buildah-1.7-11.dev.git50539b5
- autobuilt 50539b5

* Tue Feb 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-9
- buildah-1.7-10.dev.gitad24f28
- autobuilt ad24f28

* Sat Feb 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-8
- buildah-1.7-9.dev.git973bb88
- autobuilt 973bb88

* Fri Feb 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-7
- buildah-1.7-8.dev.git03f6247
- autobuilt 03f6247

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-5
- buildah-1.7-6.dev.gite702872
- autobuilt e702872

* Thu Jan 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-4
- buildah-1.7-5.dev.gitf1cec50
- autobuilt f1cec50

* Tue Jan 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-3
- buildah-1.7-4.dev.git4bcddb7
- autobuilt 4bcddb7

* Mon Jan 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-2
- buildah-1.7-3.dev.git9b9ed1d
- autobuilt 9b9ed1d

* Sun Jan 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-1
- buildah-1.7-2.dev.git7a85ca7
- bump to 1.7
- autobuilt 7a85ca7

* Sat Jan 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1
- buildah-1.6-2.dev.git5f95bd9
- bump to 1.6
- autobuilt 5f95bd9

* Fri Jan 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-1
- buildah-1.7-2.dev.git0f114e9
- bump to 1.7
- autobuilt 0f114e9

* Thu Jan 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-32
- buildah-1.6-33.dev.git66ff1dd
- autobuilt 66ff1dd

* Wed Jan 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-31
- buildah-1.6-32.dev.gitd7e530e
- autobuilt d7e530e

* Tue Jan 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-30
- buildah-1.6-31.dev.gitfe7e09c
- autobuilt fe7e09c

* Sun Jan 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-29
- buildah-1.6-30.dev.gitfa86533
- autobuilt fa86533

* Sat Jan 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-28
- buildah-1.6-29.dev.gitf6a0258
- autobuilt f6a0258

* Fri Jan 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-27
- buildah-1.6-28.dev.git5d22f3c
- autobuilt 5d22f3c

* Thu Jan 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-26
- buildah-1.6-27.dev.git1ef527c
- autobuilt 1ef527c

* Wed Jan 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-25
- buildah-1.6-26.dev.git169a923
- autobuilt 169a923

* Tue Jan 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-24
- buildah-1.6-25.dev.git48b44e5
- autobuilt 48b44e5

* Mon Jan 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-23
- buildah-1.6-24.dev.gita4200ae
- autobuilt a4200ae

* Sun Jan 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-22
- buildah-1.6-23.dev.gitbb710f3
- autobuilt bb710f3

* Sat Jan 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-21
- buildah-1.6-22.dev.git8f05aa6
- autobuilt 8f05aa6

* Fri Jan 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-20
- buildah-1.6-21.dev.git579f1d5
- autobuilt 579f1d5

* Thu Jan 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-19
- buildah-1.6-20.dev.gite55a9f3
- autobuilt e55a9f3

* Tue Dec 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-18
- buildah-1.6-19.dev.giteebbba2
- autobuilt eebbba2

* Thu Dec 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-17
- buildah-1.6-18.dev.git4674656
- autobuilt 4674656

* Wed Dec 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-16
- buildah-1.6-17.dev.gitdd3dff5
- autobuilt dd3dff5

* Sun Dec 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-15
- buildah-1.6-16.dev.git96c68db
- autobuilt 96c68db

* Fri Dec 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-14
- buildah-1.6-15.dev.gitde7f480
- autobuilt de7f480

* Wed Dec 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-13
- buildah-1.6-14.dev.git90ea890
- autobuilt 90ea890

* Mon Dec 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-12
- buildah-1.6-13.dev.gitdd0f4f1
- autobuilt dd0f4f1

* Sat Dec 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-11
- buildah-1.6-12.dev.git1e1dc14
- autobuilt 1e1dc14

* Fri Dec 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-10
- buildah-1.6-11.dev.git9c1d273
- autobuilt 9c1d273

* Thu Dec 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-9
- buildah-1.6-10.dev.git5cca1d6
- autobuilt 5cca1d6

* Wed Dec 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-8
- buildah-1.6-9.dev.git01f9ae2
- autobuilt 01f9ae2

* Tue Dec 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-7
- buildah-1.6-8.dev.git9c65e56
- autobuilt 9c65e56

* Sun Dec 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-6
- buildah-1.6-7.dev.gitb68a8e1
- autobuilt b68a8e1

* Sat Dec 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-5
- buildah-1.6-6.dev.git2b582d3
- autobuilt 2b582d3

* Fri Nov 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-4
- buildah-1.6-5.dev.git6e00183
- autobuilt 6e00183

* Thu Nov 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-3
- buildah-1.6-4.dev.git93d8b9f
- autobuilt 93d8b9f

* Wed Nov 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-2
- buildah-1.6-3.dev.git4126176
- autobuilt 4126176

* Fri Nov 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1
- buildah-1.6-2.dev.gitd5a3c52
- bump to 1.6
- autobuilt d5a3c52

* Thu Nov 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-12
- buildah-1.5-12.dev.git25d89b4
- autobuilt 25d89b4

* Wed Nov 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-11
- buildah-1.5-11.dev.git2ac987a
- autobuilt 2ac987a

* Tue Nov 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-10
- buildah-1.5-10.dev.gitc9cb148
- autobuilt c9cb148

* Sat Nov 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-9
- buildah-1.5-9.dev.git18309de
- autobuilt 18309de

* Fri Nov 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-8
- buildah-1.5-8.dev.gitd7e0993
- autobuilt d7e0993

* Thu Nov 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-7
- buildah-1.5-7.dev.gitdac7819
- autobuilt dac7819

* Tue Nov 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-6
- buildah-1.5-6.dev.gitfb2b2bd
- autobuilt fb2b2bd

* Sat Nov 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-5
- buildah-1.5-5.dev.git9add3c8
- autobuilt 9add3c8

* Fri Nov 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-4
- buildah-1.5-4.dev.git74e0b6f
- autobuilt 74e0b6f

* Thu Nov 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-3
- buildah-1.5-3.dev.git0ae8b51
- autobuilt 0ae8b51

* Wed Nov 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-2
- buildah-1.5-2.dev.git7341758
- autobuilt 7341758

* Tue Oct 02 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.5-1
- bump to v1.5-dev Release

* Wed Sep 19 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4-3
- buildah-1.4-2.dev.git19e44f0
- autobuilt 19e44f0

* Wed Sep 19 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4-2
- upstream name change

* Sun Aug 12 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4-1
- buildah-1.4-1.dev.git0a7389c
- bump to v1.4-dev
- built 0a7389c

* Wed Aug 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-13
- buildah-1.3-11.dev.git02f54e4
- autobuilt 02f54e4

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1.3-12
- Rebuild with fixed binutils

* Sun Jul 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-11
- buildah-1.3-9.dev.gitbe03809
- autobuilt be03809

* Sat Jul 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-10
- buildah-1.3-8.dev.gitc18724e
- autobuilt c18724e

* Thu Jul 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-9
- buildah-1.3-7.dev.git4976d8c
- autobuilt 4976d8c

* Wed Jul 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-8
- buildah-1.3-6.dev.gite5f7539
- autobuilt e5f7539

* Mon Jul 23 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.3-7
- Change container-selinux Requires to Recommends

* Fri Jul 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-6
- buildah-1.3-4.dev.git826733a
- autobuilt 826733a

* Thu Jul 19 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.3-5
- buildah does not require ostree

* Thu Jul 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-4
- buildah-1.3-2.dev.git1215b16
- autobuilt 1215b16

* Tue Jul 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3-3
- disable debuginfo on f29

* Tue Jul 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3-2
- make debuginfo delve debugger friendly

* Tue Jul 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3-1
- buildah-1.3-1.dev.gita9895bd
- bump to v1.3-dev
- built a9895bd

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.2-25
- update release tag to reflect unreleased status

* Mon Jul 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-24
- buildah-1.2-24.git3fb864b
- autobuilt 3fb864b

* Sun Jul 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-23
- buildah-1.2-23.git8be2b62
- autobuilt 8be2b62

* Sat Jul 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-22
- buildah-1.2-22.gita885bc6
- autobuilt a885bc6

* Fri Jul 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-21
- buildah-1.2-21.git733cd20
- autobuilt 733cd20

* Thu Jul 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-20
- buildah-1.2-20.gita59fb7a
- autobuilt a59fb7a

* Tue Jul 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-19
- buildah-1.2-19.git5c11c34
- autobuilt 5c11c34

* Mon Jul 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-18
- buildah-1.2-18.git5cd9be6
- autobuilt 5cd9be6

* Sun Jul 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-17
- buildah-1.2-17.git6f72599
- autobuilt 6f72599

* Sat Jun 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-16
- buildah-1.2-16.git704adec
- autobuilt 704adec

* Fri Jun 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-15
- buildah-1.2-15.gitb965fc4
- autobuilt b965fc4

* Thu Jun 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-14
- buildah-1.2-14.git1acccce
- autobuilt 1acccce

* Wed Jun 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-13
- buildah-1.2-13.git146c185
- autobuilt 146c185

* Tue Jun 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-12
- buildah-1.2-12.git16a33bd
- autobuilt 16a33bd

* Mon Jun 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-11
- buildah-1.2-11.git2ac95ea
- autobuilt 2ac95ea

* Sat Jun 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-10
- buildah-1.2-10.git0143a44
- autobuilt 0143a44

* Thu Jun 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-9
- buildah-1.2-9.git2441ff4
- autobuilt 2441ff4

* Wed Jun 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-8
- buildah-1.2-8.gitda7be32
- autobuilt da7be32

* Tue Jun 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-7
- buildah-1.2-7.git2064b29
- autobuilt 2064b29

* Mon Jun 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-6
- buildah-1.2-6.git93d8606
- autobuilt 93d8606

* Fri Jun 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-5
- buildah-1.2-5.gitfc438bb
- autobuilt fc438bb

* Thu Jun 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-4
- buildah-1.2-4.git73820fc
- autobuilt 73820fc

* Wed Jun 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-3
- buildah-1.2-3.git6c4bef7
- autobuilt 6c4bef7

* Tue Jun 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-2
- buildah-1.2-2.git94c1e6d
- autobuilt 94c1e6d

* Mon Jun 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-1
- buildah-1.2-1.gitb9983a6
- bump to 1.2
- autobuilt b9983a6

* Sun Jun 10 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.1-2
- Switch from skopeo-containers to containers-common

* Sun Jun 10 2018 Daniel J Walsh <dwalsh@redhat.com> - 1.1-1
- Drop capabilities if running container processes as non root Print
  Warning message if cmd will not be used based on entrypoint Update
  01-intro.md Shouldn't add insecure registries to list of search
  registries Report errors on bad transports specification when pushing
  images Move parsing code out of common for namespaces and into
  pkg/parse.go Add disable-content-trust noop flag to bud Change freenode
  chan to buildah runCopyStdio(): don't close stdin unless we saw POLLHUP
  Add registry errors for pull runCollectOutput(): just read until the
  pipes are closed on us Run(): provide redirection for stdio rmi, rm: add
  test add mount test Add parameter judgment for commands that do not
  require parameters Add context dir to bud command in baseline test
  run.bats: check that we can run with symlinks in the bundle path Give
  better messages to users when image can not be found use absolute path
  for bundlePath Add environment variable to buildah --format rm: add
  validation to args and all option Accept json array input for config
  entrypoint Run(): process RunOptions.Mounts, and its flags Run(): only
  collect error output from stdio pipes if we created some Add OnBuild
  support for Dockerfiles Quick fix on demo readme run: fix validate flags
  buildah bud should require a context directory or URL Touchup tutorial
  for run changes Validate common bud and from flags images: Error if the
  specified imagename does not exist inspect: Increase err judgments to
  avoid panic add test to inspect buildah bud picks up ENV from base image
  Extend the amount of time travis_wait should wait Add a make target for
  Installing CNI plugins Add tests for namespace control flags copy.bats:
  check ownerships in the container Fix SELinux test errors when SELinux is
  enabled Add example CNI configurations Run: set supplemental group IDs
  Run: use a temporary mount namespace Use CNI to configure container
  networks add/secrets/commit: Use mappings when setting permissions on
  added content Add CLI options for specifying namespace and cgroup setup
  Always set mappings when using user namespaces Run(): break out creation
  of stdio pipe descriptors Read UID/GID mapping information from
  containers and images Additional bud CI tests Run integration tests under
  travis_wait in Travis build-using-dockerfile: add --annotation Implement
  --squash for build-using-dockerfile and commit Vendor in latest
  container/storage for devicemapper support add test to inspect Vendor
  github.com/onsi/ginkgo and github.com/onsi/gomega Test with Go 1.10, too
  Add console syntax highlighting to troubleshooting page bud.bats: print
  "$output" before checking its contents Manage "Run" containers more
  closely Break Builder.Run()'s "run runc" bits out util.ResolveName():
  handle completion for tagged/digested image names Handle /etc/hosts and
  /etc/resolv.conf properly in container Documentation fixes Make it easier
  to parse our temporary directory as an image name Makefile: list new pkg/
  subdirectoris as dependencies for buildah containerImageSource: return
  more-correct errors API cleanup: PullPolicy and TerminalPolicy should be
  types Make "run --terminal" and "run -t" aliases for "run --tty" Vendor
  github.com/containernetworking/cni v0.6.0 Update
  github.com/containers/storage Update github.com/projectatomic/libpod Add
  support for buildah bud --label buildah push/from can push and pull
  images with no reference Vendor in latest containers/image Update
  gometalinter to fix install.tools error Update troubleshooting with new
  run workaround Added a bud demo and tidied up Attempt to download file
  from url, if fails assume Dockerfile Add buildah bud CI tests for ENV
  variables Re-enable rpm .spec version check and new commit test Update
  buildah scratch demo to support el7 Added Docker compatibility demo
  Update to F28 and new run format in baseline test Touchup man page short
  options across man pages Added demo dir and a demo. chged distrorlease
  builder-inspect: fix format option Add cpu-shares short flag (-c) and
  cpu-shares CI tests Minor fixes to formatting in rpm spec changelog Fix
  rpm .spec changelog formatting CI tests and minor fix for cache related
  noop flags buildah-from: add effective value to mount propagation

* Sat Jun 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-22
- buildah-1.0-20.gitf449b28
- autobuilt f449b28

* Fri Jun 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-21
- buildah-1.0-19.gitc306342
- autobuilt c306342

* Wed Jun 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-20
- buildah-1.0-18.gitd3d097b
- autobuilt d3d097b

* Tue Jun 05 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0-19
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
