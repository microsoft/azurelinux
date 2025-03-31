Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global with_debug 1

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif


%global gomodulesmode GO111MODULE=on


%global git0 https://github.com/containers/%{name}

Name: buildah
# Set different Epoch for copr

# DO NOT TOUCH the Version string!
# The TRUE source of this specfile is:
# https://github.com/containers/skopeo/blob/main/rpm/skopeo.spec
# If that's what you're reading, Version must be 0, and will be updated by Packit for
# copr and koji builds.
# If you're reading this on dist-git, the version is automatically filled in by Packit.
Version: 1.38.0
# The `AND` needs to be uppercase in the License for SPDX compatibility
License: Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0

Release: 1%{?dist} 
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
BuildRequires: go-rpm-macros
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: make
BuildRequires: ostree-devel
BuildRequires: btrfs-progs-devel
BuildRequires: shadow-utils-subid-devel
BuildRequires: libseccomp-static
Requires: libseccomp >= 2.4.1-0
Suggests: cpp

%description
The %{name} package provides a command line tool which can be used to
* create a working container from scratch
or
* create a working container from an image as a starting point
* mount/umount a working container's root file system for manipulation
* save container's root file system layer to create a new image
* delete a working container or an image

%package tests
Summary: Tests for %{name}

Requires: %{name} = %{version}-%{release}
Requires: bats
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


export CGO_CFLAGS+=" -m64 -mtune=generic -fcf-protection=full"

export CNI_VERSION=`grep '^# github.com/containernetworking/cni ' src/modules.txt | sed 's,.* ,,'`
export LDFLAGS="-X main.buildInfo=`date +%s` -X main.cniVersion=${CNI_VERSION}"

export BUILDTAGS="seccomp exclude_graphdriver_devicemapper $(hack/systemd_tag.sh) $(hack/libsubid_tag.sh)"
export BUILDTAGS+=" btrfs_noversion exclude_graphdriver_btrfs"

%gobuild -o bin/%{name} ./cmd/%{name}
%gobuild -o bin/imgtype ./tests/imgtype
%gobuild -o bin/copy ./tests/copy
%gobuild -o bin/tutorial ./tests/tutorial
%gobuild -o bin/inet ./tests/inet
%{__make} docs

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install install.completions

install -d -p %{buildroot}/%{_datadir}/%{name}/test/system
cp -pav tests/. %{buildroot}/%{_datadir}/%{name}/test/system
cp bin/imgtype %{buildroot}/%{_bindir}/%{name}-imgtype
cp bin/copy    %{buildroot}/%{_bindir}/%{name}-copy
cp bin/tutorial %{buildroot}/%{_bindir}/%{name}-tutorial
cp bin/inet     %{buildroot}/%{_bindir}/%{name}-inet

rm %{buildroot}%{_datadir}/%{name}/test/system/tools/build/*

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

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
%{_datadir}/%{name}/test

%changelog
* Wed Mar 26 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.38.0-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Tue Nov 12 2024 Paul Holzinger <pholzing@redhat.com> - 2:1.38.0-2
- tests: set new inet helper path

* Mon Nov 11 2024 Packit <hello@packit.dev> - 2:1.38.0-1
- Update to 1.38.0 upstream release

* Fri Oct 18 2024 Packit <hello@packit.dev> - 2:1.37.5-1
- Update to 1.37.5 upstream release

* Mon Oct 07 2024 Packit <hello@packit.dev> - 2:1.37.4-1
- Update to 1.37.4 upstream release

* Mon Sep 23 2024 Packit <hello@packit.dev> - 2:1.37.3-1
- Update to 1.37.3 upstream release

* Wed Aug 21 2024 Packit <hello@packit.dev> - 1.37.2-1
- Update to 1.37.2 upstream release

* Thu Aug 15 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.37.1-1
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

* Mon Feb 10 2020 Ed Santiago <santiago@redhat.com> - 1.14.0-39
- buildah-tests now requires 'jq'

* Wed Feb 05 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.14.0-38
- adjust libseccomp deps

* Wed Feb 05 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.14.0-37
- adjust deps and macros for centos obs build

* Wed Feb 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-36
- buildah-1.14.0-0.35.dev.gitf1cf92b
- autobuilt f1cf92b

* Sat Feb 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-35
- buildah-1.14.0-0.34.dev.gitf89b081
- autobuilt f89b081

* Fri Jan 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-34
- buildah-1.14.0-0.33.dev.git3177db5
- autobuilt 3177db5

* Thu Jan 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-33
- buildah-1.14.0-0.32.dev.git4131dfa
- autobuilt 4131dfa

* Wed Jan 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-32
- buildah-1.14.0-0.31.dev.git82ff48a
- autobuilt 82ff48a

* Tue Jan 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-31
- buildah-1.14.0-0.30.dev.git0a063c4
- autobuilt 0a063c4

* Mon Jan 27 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-30
- buildah-1.14.0-0.29.dev.gitec4bbe6
- autobuilt ec4bbe6

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-29
- buildah-1.14.0-0.28.dev.git6e277a2
- autobuilt 6e277a2

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-28
- buildah-1.14.0-0.27.dev.git6417a9a
- autobuilt 6417a9a

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-27
- buildah-1.14.0-0.26.dev.git0c3234f
- autobuilt 0c3234f

* Sun Jan 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-26
- buildah-1.14.0-0.25.dev.git2055fe9
- autobuilt 2055fe9

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-25
- buildah-1.14.0-0.24.dev.gita925f79
- autobuilt a925f79

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-24
- buildah-1.14.0-0.23.dev.gitca0819f
- autobuilt ca0819f

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-23
- buildah-1.14.0-0.22.dev.gitc46f6e0
- autobuilt c46f6e0

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-22
- buildah-1.14.0-0.21.dev.gitb09fdc3
- autobuilt b09fdc3

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-21
- buildah-1.14.0-0.20.dev.git09d1c24
- autobuilt 09d1c24

* Tue Jan 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-20
- buildah-1.14.0-0.19.dev.gitbf14e6c
- autobuilt bf14e6c

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-19
- buildah-1.14.0-0.18.dev.git720e5d6
- autobuilt 720e5d6

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-18
- buildah-1.14.0-0.17.dev.gitb7e6731
- autobuilt b7e6731

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-17
- buildah-1.14.0-0.16.dev.gitf7731c2
- autobuilt f7731c2

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-16
- buildah-1.14.0-0.15.dev.git9def9c0
- autobuilt 9def9c0

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-15
- buildah-1.14.0-0.14.dev.git3af1491
- autobuilt 3af1491

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-14
- buildah-1.14.0-0.13.dev.git4e23b7a
- autobuilt 4e23b7a

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-13
- buildah-1.14.0-0.12.dev.git55fa8f5
- autobuilt 55fa8f5

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-12
- buildah-1.14.0-0.11.dev.git47ce18b
- autobuilt 47ce18b

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-11
- buildah-1.14.0-0.10.dev.gita3dec02
- autobuilt a3dec02

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-10
- buildah-1.14.0-0.9.dev.gitb555b7d
- autobuilt b555b7d

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-9
- buildah-1.14.0-0.8.dev.gite7be041
- autobuilt e7be041

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-8
- buildah-1.14.0-0.7.dev.gitdbec497
- autobuilt dbec497

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-7
- buildah-1.14.0-0.6.dev.git45543bf
- autobuilt 45543bf

* Mon Jan 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-6
- buildah-1.14.0-0.5.dev.gitd792c70
- autobuilt d792c70

* Mon Jan 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-5
- buildah-1.14.0-0.4.dev.git20c2a54
- autobuilt 20c2a54

* Mon Jan 06 2020 Ed Santiago <santiago@redhat.com> - 1.14.0-4
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec

=======
## START: Generated by rpmautospec
* Tue Nov 12 2024 Paul Holzinger <pholzing@redhat.com> - 2:1.38.0-2
- tests: set new inet helper path

* Mon Nov 11 2024 Packit <hello@packit.dev> - 2:1.38.0-1
- Update to 1.38.0 upstream release

* Fri Oct 18 2024 Packit <hello@packit.dev> - 2:1.37.5-1
- Update to 1.37.5 upstream release

* Mon Oct 07 2024 Packit <hello@packit.dev> - 2:1.37.4-1
- Update to 1.37.4 upstream release

* Mon Sep 23 2024 Packit <hello@packit.dev> - 2:1.37.3-1
- Update to 1.37.3 upstream release

* Wed Aug 21 2024 Packit <hello@packit.dev> - 1.37.2-1
- Update to 1.37.2 upstream release

* Thu Aug 15 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.37.1-1
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

* Mon Feb 10 2020 Ed Santiago <santiago@redhat.com> - 1.14.0-39
- buildah-tests now requires 'jq'

* Wed Feb 05 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.14.0-38
- adjust libseccomp deps

* Wed Feb 05 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.14.0-37
- adjust deps and macros for centos obs build

* Wed Feb 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-36
- buildah-1.14.0-0.35.dev.gitf1cf92b
- autobuilt f1cf92b

* Sat Feb 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-35
- buildah-1.14.0-0.34.dev.gitf89b081
- autobuilt f89b081

* Fri Jan 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-34
- buildah-1.14.0-0.33.dev.git3177db5
- autobuilt 3177db5

* Thu Jan 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-33
- buildah-1.14.0-0.32.dev.git4131dfa
- autobuilt 4131dfa

* Wed Jan 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-32
- buildah-1.14.0-0.31.dev.git82ff48a
- autobuilt 82ff48a

* Tue Jan 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-31
- buildah-1.14.0-0.30.dev.git0a063c4
- autobuilt 0a063c4

* Mon Jan 27 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-30
- buildah-1.14.0-0.29.dev.gitec4bbe6
- autobuilt ec4bbe6

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-29
- buildah-1.14.0-0.28.dev.git6e277a2
- autobuilt 6e277a2

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-28
- buildah-1.14.0-0.27.dev.git6417a9a
- autobuilt 6417a9a

* Tue Jan 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-27
- buildah-1.14.0-0.26.dev.git0c3234f
- autobuilt 0c3234f

* Sun Jan 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-26
- buildah-1.14.0-0.25.dev.git2055fe9
- autobuilt 2055fe9

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-25
- buildah-1.14.0-0.24.dev.gita925f79
- autobuilt a925f79

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-24
- buildah-1.14.0-0.23.dev.gitca0819f
- autobuilt ca0819f

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-23
- buildah-1.14.0-0.22.dev.gitc46f6e0
- autobuilt c46f6e0

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-22
- buildah-1.14.0-0.21.dev.gitb09fdc3
- autobuilt b09fdc3

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-21
- buildah-1.14.0-0.20.dev.git09d1c24
- autobuilt 09d1c24

* Tue Jan 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-20
- buildah-1.14.0-0.19.dev.gitbf14e6c
- autobuilt bf14e6c

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-19
- buildah-1.14.0-0.18.dev.git720e5d6
- autobuilt 720e5d6

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-18
- buildah-1.14.0-0.17.dev.gitb7e6731
- autobuilt b7e6731

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-17
- buildah-1.14.0-0.16.dev.gitf7731c2
- autobuilt f7731c2

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-16
- buildah-1.14.0-0.15.dev.git9def9c0
- autobuilt 9def9c0

* Mon Jan 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-15
- buildah-1.14.0-0.14.dev.git3af1491
- autobuilt 3af1491

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-14
- buildah-1.14.0-0.13.dev.git4e23b7a
- autobuilt 4e23b7a

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-13
- buildah-1.14.0-0.12.dev.git55fa8f5
- autobuilt 55fa8f5

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-12
- buildah-1.14.0-0.11.dev.git47ce18b
- autobuilt 47ce18b

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-11
- buildah-1.14.0-0.10.dev.gita3dec02
- autobuilt a3dec02

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-10
- buildah-1.14.0-0.9.dev.gitb555b7d
- autobuilt b555b7d

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-9
- buildah-1.14.0-0.8.dev.gite7be041
- autobuilt e7be041

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-8
- buildah-1.14.0-0.7.dev.gitdbec497
- autobuilt dbec497

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-7
- buildah-1.14.0-0.6.dev.git45543bf
- autobuilt 45543bf

* Mon Jan 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-6
- buildah-1.14.0-0.5.dev.gitd792c70
- autobuilt d792c70

* Mon Jan 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.14.0-5
- buildah-1.14.0-0.4.dev.git20c2a54
- autobuilt 20c2a54

* Mon Jan 06 2020 Ed Santiago <santiago@redhat.com> - 1.14.0-4
- RPMAUTOSPEC: unresolvable merge

