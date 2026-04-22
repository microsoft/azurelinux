# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# https://github.com/cri-o/cri-o
%global goipath         github.com/cri-o/cri-o
%global service_name    crio

# Related: github.com/cri-o/cri-o/issues/3684
%global build_timestamp %(date -u +'%Y-%m-%dT%H:%M:%SZ')
%global git_tree_state  clean
%global criocli_path    ""

Version:        1.32.0

%if 0%{?rhel} && 0%{?rhel} <= 9
%define gobuild(o:) %{expand:
  # https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
  %global _dwz_low_mem_die_limit 0
  %ifnarch ppc64
  go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${BASE_LDFLAGS:-}%{?currentgoldflags} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags %{?__golang_extldflags}' -compressdwarf=false" -a -v -x %{?**};
  %else
  go build                -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${BASE_LDFLAGS:-}%{?currentgoldflags} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags %{?__golang_extldflags}' -compressdwarf=false" -a -v -x %{?**};
  %endif
}
%bcond_with check
%else
%gometa
%bcond_without check
%endif

# Commit for the builds
%global commit0 b7f3c240bcbda6fae8d43561694d18317e09e167

Name:           cri-o
Epoch:          0
Release: 5%{?dist}
Summary:        Open Container Initiative-based implementation of Kubernetes Container Runtime Interface

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://github.com/cri-o/cri-o
Source0:        %url/archive/v%{version}/%{name}-%{version}.tar.gz

%if 0%{?rhel}
BuildRequires:  golang >= 1.23
%endif
%if 0%{?rhel} && 0%{?rhel} <= 8
# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
%endif
%if 0%{?fedora}
BuildRequires:  btrfs-progs-devel
BuildRequires:  device-mapper-devel
BuildRequires:  go-rpm-macros
%endif
BuildRequires:  git-core
BuildRequires:  glib2-devel
BuildRequires:  glibc-static
BuildRequires:  go-md2man
BuildRequires:  gpgme-devel
BuildRequires:  libassuan-devel
BuildRequires:  libseccomp-devel
%if 0%{?rhel} && 0%{?rhel} < 8
BuildRequires:  systemd-devel
%else
BuildRequires:  systemd-rpm-macros
%endif
BuildRequires:  make
%if 0%{?fedora}
Requires(pre):  container-selinux
%else
Requires:       container-selinux
%endif
Requires:       containers-common >= 1:0.1.31-14
%if 0%{?rhel} && 0%{?rhel} < 8
Requires:       runc >= 1.0.0-16
Requires:       containernetworking-plugins >= 1.0.0-1
%else
Recommends:     runc >= 1.0.0-16
Suggests:       containernetworking-plugins >= 1.0.0-1
%endif
Requires:       conmon >= 2.0.2-1
Requires:       socat

Obsoletes:      ocid <= 0.3
Provides:       ocid = %{epoch}:%{version}-%{release}
Provides:       %{service_name} = %{epoch}:%{version}-%{release}

%description
Open Container Initiative-based implementation of Kubernetes Container Runtime
Interface.

%prep
%if 0%{?rhel} && 0%{?rhel} <= 9
%autosetup -p1 -n %{name}-%{version}
%else
%goprep -k
%endif

sed -i 's/install.config: crio.conf/install.config:/' Makefile
sed -i 's/install.bin: binaries/install.bin:/' Makefile
sed -i 's/install.man: $(MANPAGES)/install.man:/' Makefile
sed -i 's/\.gopathok //' Makefile
sed -i 's/module_/module-/' internal/version/version.go
sed -i 's/\/local//' contrib/systemd/%{service_name}.service
sed -i 's/\/local//' contrib/systemd/%{service_name}-wipe.service

%build
%global __golang_extldflags -Wl,-z,undefs

export GO111MODULE=on
export GOFLAGS=-mod=vendor

export BUILDTAGS="containers_image_ostree_stub
$(hack/btrfs_installed_tag.sh)
$(hack/btrfs_tag.sh) $(hack/openpgp_tag.sh)
$(hack/seccomp_tag.sh) $(hack/selinux_tag.sh)
$(hack/libsubid_tag.sh) exclude_graphdriver_devicemapper"

%if 0%{?rhel}  && 0%{?rhel} <= 8
BUILDTAGS="$BUILDTAGS containers_image_openpgp"
%endif

export BASE_LDFLAGS="-X %{goipath}/internal/pkg/criocli.DefaultsPath=%{criocli_path}
-X  %{goipath}/internal/version.buildDate=%{build_timestamp}
-X  %{goipath}/internal/version.gitCommit=%{commit0}
-X  %{goipath}/internal/version.version=%{version}
-X  %{goipath}/internal/version.gitTreeState=%{git_tree_state} "

for cmd in cmd/* ; do
  %gobuild -o bin/$(basename $cmd) %{goipath}/$cmd
done

%if 0%{?fedora}
%set_build_flags
%endif
export CFLAGS="$CFLAGS -std=c99"
%make_build bin/pinns
GO_MD2MAN=go-md2man make docs

%install
sed -i 's/\/local//' contrib/systemd/%{service_name}.service
bin/%{service_name} \
      --selinux \
      --cni-plugin-dir /opt/cni/bin \
      --cni-plugin-dir "%{_libexecdir}/cni" \
      --enable-metrics \
      --metrics-port 9537 \
      config > %{service_name}.conf

# install binaries
install -dp %{buildroot}{%{_bindir},%{_libexecdir}/%{service_name}}
install -p -m 755 bin/%{service_name} %{buildroot}%{_bindir}

# install conf files
install -dp %{buildroot}%{_sysconfdir}/cni/net.d
install -p -m 644 contrib/cni/10-crio-bridge.conflist %{buildroot}%{_sysconfdir}/cni/net.d/100-crio-bridge.conflist
install -p -m 644 contrib/cni/99-loopback.conflist %{buildroot}%{_sysconfdir}/cni/net.d/200-loopback.conflist

install -dp %{buildroot}%{_sysconfdir}/%{service_name}
install -dp %{buildroot}%{_datadir}/containers/oci/hooks.d
install -dp %{buildroot}%{_datadir}/oci-umount/oci-umount.d
install -p -m 644 crio.conf %{buildroot}%{_sysconfdir}/%{service_name}
#install -p -m 644 seccomp.json %%{buildroot}%%{_sysconfdir}/%%{service_name}
install -p -m 644 crio-umount.conf %{buildroot}%{_datadir}/oci-umount/oci-umount.d/%{service_name}-umount.conf
install -p -m 644 crictl.yaml %{buildroot}%{_sysconfdir}

%make_install PREFIX=%{buildroot}%{_prefix} \
            install.bin \
            install.completions \
            install.config \
            install.man \
            install.systemd

%if 0%{?rhel} && 0%{?rhel} <= 7
# https://bugzilla.redhat.com/show_bug.cgi?id=1823374#c17
install -d -p %{buildroot}%{_prefix}/lib/sysctl.d
echo "fs.may_detach_mounts=1" > %{buildroot}%{_prefix}/lib/sysctl.d/99-cri-o.conf
%endif

install -dp %{buildroot}%{_sharedstatedir}/containers

%post
# Old verions of kernel do not recognize metacopy option.
# Reference: github.com/cri-o/cri-o/issues/3631
%if 0%{?rhel} && 0%{?rhel} <= 7
sed -i -e 's/,metacopy=on//g' /etc/containers/storage.conf
%sysctl_apply 99-cri-o.conf
%endif
%systemd_post %{service_name}

%preun
%systemd_preun %{service_name}

%postun
%systemd_postun_with_restart %{service_name}

%files
%license LICENSE vendor/modules.txt
%doc docs code-of-conduct.md tutorial.md ADOPTERS.md CONTRIBUTING.md README.md
%doc awesome.md transfer.md
%{_bindir}/%{service_name}
%{_bindir}/pinns
%{_mandir}/man5/%{service_name}.conf*5*
%{_mandir}/man8/%{service_name}*.8*
%dir %{_sysconfdir}/%{service_name}
%config(noreplace) %{_sysconfdir}/%{service_name}/%{service_name}.conf
%config(noreplace) %{_sysconfdir}/cni/net.d/100-%{service_name}-bridge.conflist
%config(noreplace) %{_sysconfdir}/cni/net.d/200-loopback.conflist
%config(noreplace) %{_sysconfdir}/crictl.yaml
%dir %{_libexecdir}/%{service_name}
%{_unitdir}/%{service_name}.service
%{_unitdir}/%{service_name}-wipe.service
%dir %{_sharedstatedir}/containers
%dir %{_datadir}/containers
%dir %{_datadir}/containers/oci
%dir %{_datadir}/containers/oci/hooks.d
%dir %{_datadir}/oci-umount
%dir %{_datadir}/oci-umount/oci-umount.d
%{_datadir}/oci-umount/oci-umount.d/%{service_name}-umount.conf
%{_datadir}/bash-completion/completions/%{service_name}*
%{_datadir}/fish/completions/%{service_name}*.fish
%{_datadir}/zsh/site-functions/_%{service_name}*
%if 0%{?rhel} && 0%{?rhel} <= 7
%{_prefix}/lib/sysctl.d/99-cri-o.conf
%endif

%changelog
* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 0:1.32.0-4
- Rebuild for golang-1.25.0

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.32.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 23 2024 Bradley G Smith <bradley.g.smith@gmail.com> - 0:1.32.0-1
- Bump to v1.32.0
- Add -Wl,-z,undefs linker flags to resolve https://github.com/cri-o/cri-o/issues/8860
- Update BUILDTAGS to conform to upstream

* Thu Oct 24 2024 Dennis Gilmore <dennis@ausil.us> - 0:1.31.1-1
- update to 1.31.1

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 0:1.29.4-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.29.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 30 2024 Bradley G Smith <bradley.g.smith@gmail.com> - 0:1.29.4-1
- Bump to v1.29.4
- Resolves CVE-2024-3154, a security flaw where CRI-O allowed users to specify annotations that changed specific fields in the runtime.

* Sat Apr 27 2024 Bradley G Smith <bradley.g.smith@gmail.com> - 0:1.29.3-1
- Bump to v1.29.3
- Add support for autogenerated bundled provides
- Remove otelttrpc patch added in v1.29.2 to fix rpm build error. No longer needed.

* Thu Mar 21 2024 Peter Hunt <pehunt@redhat.com> - 0:1.29.2-1
- bump to v1.29.2

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 0:1.28.2-5
- Rebuild for golang 1.22.0

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 0:1.28.2-4
- Rebuild for golang 1.22.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 04 2023 Christian Glombek <cglombek@redhat.com> - 0:1.28.2-1
- bump to v1.28.2

* Thu Aug 24 2023 Peter Hunt <pehunt@redhat.com> - 0:1.28.0-1
- bump to v1.28.0

* Thu Jul 20 2023 T K Chandra Hasan <t.k.chandra.hasan@ibm.com> - 0:1.27.1-1
- bump to v1.27.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.27.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 25 2023 Peter Hunt <pehunt@redhat.com> - 0:1.27.0-1
- bump to v1.27.0

* Wed Jan 25 2023 Peter Hunt~ <pehunt@redhat.com> - 0:1.26.1-2
- update for obs

* Tue Jan 10 2023 Peter Hunt~ <pehunt@redhat.com> - 0:1.26.1-1
- bump to v1.26.1

* Fri Dec 23 2022 Peter Hunt~ <pehunt@redhat.com> - 0:1.26.0-1
- bump to v1.26.0

* Fri Oct 07 2022 Peter Hunt~ <pehunt@redhat.com> - 0:1.25.1-1
- bump to v1.25.1

* Mon Aug 29 2022 Peter Hunt~ <pehunt@redhat.com> - 0:1.25.0-1
- bump to v1.25.0

* Mon Aug 29 2022 Peter Hunt~ <pehunt@redhat.com> - 0:1.25.0-1
- bump to v1.25.0

* Tue Aug 09 2022 Peter Hunt~ <pehunt@redhat.com> - 0:1.24.2-1
- bump to v1.24.2

* Mon Jun 06 2022 Peter Hunt <pehunt@redhat.com> - 0:1.24.1-1
- bump to v1.24.1

* Wed May 11 2022 Peter Hunt <pehunt@redhat.com> - 0:1.24.0-1
- bump to v1.24.0

* Tue Mar 15 2022 Peter Hunt <pehunt@redhat.com> - 0:1.23.2-1
- bump to v1.23.2

* Tue Mar 15 2022 Peter Hunt <pehunt@redhat.com> - 0:1.23.2-1
- bump to v1.23.2

* Fri Feb 11 2022 Peter Hunt <pehunt@redhat.com> - 0:1.23.1-1
- bump to v1.23.1

* Fri Feb 11 2022 Peter Hunt <pehunt@redhat.com> - 0:1.23.1-1
- bump to v1.23.1

* Fri Dec 17 2021 Peter Hunt <pehunt@redhat.com> - 0:1.23.0-1
- bump to v1.23.0

* Fri Dec 03 2021 Peter Hunt <pehunt@redhat.com> - 0:1.22.1-2
- fix bogus date

* Thu Nov 11 2021 Peter Hunt <pehunt@redhat.com> - 0:1.22.1-1
- bump to v1.22.1

* Mon Nov 08 2021 Peter Hunt <pehunt@redhat.com> - 0:1.22.0-4
- update golang version

* Mon Sep 13 2021 Peter Hunt <pehunt@redhat.com> - 0:1.22.0-3
- fix spec

* Wed Aug 25 2021 Peter Hunt <pehunt@redhat.com> - 0:1.22.0-2
- bump to v1.22.0

* Tue Jul 20 2021 Peter Hunt <pehunt@redhat.com> - 0:1.21.2-1
- bump to v1.21.2

* Mon Jul 19 2021 Peter Hunt <pehunt@redhat.com> - 0:1.21.1-1
- bump to v1.21.1

* Tue Jun 22 2021 Peter Hunt <pehunt@redhat.com> - 0:1.21.0-3
- update spec to be more conformant for fedora

* Wed Apr 14 2021 Peter Hunt <pehunt@redhat.com> - 0:1.21.0-2
- Use crio config for metrics configuration
- drop systemd from crio configuration

* Wed Apr 14 2021 Peter Hunt <pehunt@redhat.com> - 0:1.21.0-1
- Bump to v1.21.0

* Wed Mar 24 2021 Peter Hunt <pehunt@redhat.com> - 0:1.20.2-1
- Bump to v1.20.2

* Fri Mar 12 2021 Peter Hunt <pehunt@redhat.com> - 0:1.20.1-1
- Bump to v1.20.1

* Mon Feb 15 2021 Peter Hunt <pehunt@redhat.com> - 0:1.20.0-5
- Keep metacopy for fedora

* Tue Jan 12 2021 Peter Hunt <pehunt@redhat.com> - 0:1.20.0-4
- add fs.may_detach_mounts sysctl for centos/rhel 7

* Thu Dec 17 2020 Peter Hunt <pehunt@redhat.com> - 0:1.20.0-3
- Fix checksec for pinns

* Wed Dec 16 2020 Peter Hunt <pehunt@redhat.com> - 0:1.20.0-2
- enable PIE mode for cri-o

* Fri Dec 11 2020 Peter Hunt <pehunt@redhat.com> - 0:1.20.0-1
- Bump to v1.20.0

* Thu Nov 19 2020 Peter Hunt <pehunt@redhat.com> - 2:1.19.0-4
- fix timestamp for centos 7

* Mon Nov  9 2020 Peter Hunt <pehunt@redhat.com> - 2:1.19.0-3
- upstream#3879: fix symbolic link

* Mon Oct 05 2020 Peter Hunt <pehunt@redhat.com> - 2:1.19.0-2
- update selinux dep to handle OBS

* Mon Oct 05 2020 Peter Hunt <pehunt@redhat.com> - 2:1.19.0-1
- update go-md2man dependency to handle OBS

* Mon Sep 14 2020 Peter Hunt <pehunt@redhat.com> - 2:1.19.0-0
- bump to 1.19.0

* Tue Aug 04 2020 Peter Hunt <pehunt@redhat.com> - 2:1.18.3-1
- Github 3923: Make runc installation recommended

* Wed Jul 29 2020 Peter Hunt <pehunt@redhat.com> - 2:1.18.3-0
- Bump to v1.18.3

* Wed Jul 29 2020 Peter Hunt <pehunt@redhat.com> - 2:1.18.2-2
- remove custom conmon path

* Tue Jun 23 2020 Douglas Schilling Landgraf <dougsland@redhat.com> - 2:1.18.2-1
- Build 1.18.2

* Fri Jun 05 2020 Douglas Schilling Landgraf <dougsland@redhat.com> - 2:1.18.1-2
- Add --cni-plugin-dir /opt/cni/bin to cri-o conf file

* Thu May 14 2020 Douglas Schilling Landgraf <dougsland@redhat.com> - 2:1.18.1-1
- Release 1.18.1

* Thu Apr 23 2020 Douglas Schilling Landgraf <dougsland@redhat.com> - 2:1.18.0-2
- Fix crio version - github.com/cri-o/cri-o/issues/3684

* Thu Apr 23 2020 Douglas Schilling Landgraf <dougsland@redhat.com> - 2:1.18.0-1
- Bump for 1.18.0 release

* Wed Apr 15 2020 Douglas Schilling Landgraf <dougsland@redhat.com> - 2:1.18.0-0.1.rc1
- Bump for 1.18 release candidate

* Tue Mar 31 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.17.2-2
- use correct tag

* Tue Mar 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.17.2-1
- autobuilt v1.17.2

* Fri Mar 20 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.17.1-2
- Resolves: #1795858 - list /usr/share/containers/oci/hooks.d
- enable debuginfo
- spec changes for autobuilder

* Mon Mar 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.17.1-1
- autobuilt v1.17.1

* Mon Feb 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.17.0-1
- autobuilt $LATEST_TAG

* Tue Jan 14 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.17.0-0.1.gitb89a5fc
- built v1.17.0-rc1

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.16.2-1
- autobuilt $LATEST_TAG

* Wed Dec 04 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.16.1-1
- Resolves: #1740730, #1743017, #1754170

* Fri Nov 15 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.16.0-0.4.rc2
- Resolves: #1740730, #1743017, #1754170 - no underscore in crio --version

* Tue Nov 05 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.16.0-0.3.rc2
- Requires: socat

* Mon Nov 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.16.0-0.2.rc2
- bump to v1.16.0-rc2
- autobuilt a783f23

* Mon Oct 21 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.16.0-1.rc1.git6a4b481
- built release-1.16

* Thu Oct 03 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.15.2-1
- bump to v1.15.2

* Mon Sep 09 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.15.1-2
- correct path in crio-wipe unitfile

* Wed Sep 04 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.15.1-1
- bump to v1.15.1

* Sun Jul 21 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.15.0-1
- bump to 1.15.0
- autobuilt 485227d

* Mon May 27 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.14.1-2.gitb7644f6
- add a patch to build on 32-bit systems (upstream PR: 2409)

* Thu May 23 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.14.1-1.gitb7644f6
- bump to v1.14.1

* Thu May 23 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.9-1.gitd70609a
- bump to v1.13.9

* Thu Feb 21 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.0-1.gite8a2525
- bump to v1.13.0

* Sat Nov 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.12.0-1.git18bc811
- bump to v1.12.1

* Tue Oct 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.12.0-1.git774a29e
- bump to v1.12.0

* Tue Oct 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.11.8-1.git71cc465
- bump to v1.11.8
- built commit 71cc465

* Mon Sep 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.11.4-1.gite0c89d8
- bump to v1.11.4
- built commit e0c89d8
- crio.conf changes: cgroup_manager=systemd, file_locking=false

* Tue Sep 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.11.3-1.git4fbb022
- bump to v1.11.3

* Mon Aug 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.11.2-2.git3eac3b2
- no go-md2man or go compiler for ppc64

* Mon Aug 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.11.2-1.git3eac3b2
- bump to v1.11.2
- conmon is a separate subpackage

* Mon Jul 2 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.11.0-1.rhaos3.11.git441bd3d
- bump to v1.11.0

* Mon Jul 2 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.10.5-1.rhaos3.10.git
- bump to v1.10.5

* Wed Jun 27 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.10.4-1.rhaos3.10.gitebaa77a
- bump to v1.10.4
- remove devel and unittest subpackages - unused
- debuginfo disabled for now, complains about %%files being empty

* Mon Jun 18 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.10.3-1.rhaos3.10.gite558bd
- bump to v1.10.3

* Tue Jun 12 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.10.2-2.rhaos3.10.git1ffcbb
- Released version of v1.10.2

* Tue May 15 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.10.2-1.rhaos3.10.git095e88c
- bump to v1.10.2
- built commit 095e88c
- include rhaos3.10 in release tag
- do not compress debuginfo with dwz to support delve debugger

* Tue May 8 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.10.1-2.git728df92
- bump to v1.10.1

* Wed Mar 28 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.10.0-1.beta.1gitc956614
- bump to v1.10.0-beta.1
- built commit c956614

* Tue Mar 13 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.9.10-1.git8723732
- bump to v1.9.10

* Fri Mar 09 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.9.9-1.git4d7e7dc
- bump to v1.9.9

* Fri Feb 23 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.9.8-1.git7d9d2aa
- bump to v1.9.8

* Fri Feb 23 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.9.7-2.gita98f9c9
- correct version in previous changelog entry

* Fri Feb 23 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.9.7-1.gita98f9c9
- Merge pull request #1357 from runcom/netns-fixes
- sandbox_stop: close/remove the netns _after_ stopping the containers
- sandbox net: set netns closed after actaully closing it

* Wed Feb 21 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.9.6-1.git5e48c92
- vendor: update c/image to handle text/plain from registries

* Fri Feb 16 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.9.5-1.git125ec8a
- image: Add lock around image cache access

* Thu Feb 15 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.9.4-1.git28c7dee
- imageService: cache information about images
- container_create: correctly set user
- system container: add /var/tmp as RW

* Sun Feb 11 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.9.3-1.git63ea1dd
- Update containers/image and containers/storage
-   Pick up lots of fixes in image and storage library

* Thu Feb 8 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.9.2-1.gitb066a83
- sandbox: fix sandbox logPath when crio restarts
- syscontainers, rhel: add ADDTL_MOUNTS
- Adapt to recent containers/image API updates
- container_create: only bind mount /etc/hosts if not provided by k8s

* Wed Jan 24 2018 Dan Walsh <dwalsh@redhat.com> - 2:1.9.1-1.gitb066a8
- Final Release 1.9.1

* Wed Jan 03 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.8.4-4.gitdffb5c2
- epoch not needed, 1.9 was never shipped, 1.8 with epoch also never shipped

* Wed Jan 03 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.8.4-3.gitdffb5c2
- reversed to 1.8, epoch

* Mon Dec 18 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.0-1.git814c6ab
- bump to v1.9.0

* Fri Dec 15 2017 Dan Walsh <dwalsh@redhat.com> - 1.8.4-1.gitdffb5c2
- bump to v1.8.4

* Wed Nov 29 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.8.2-1.git3de7ab4
- bump to v1.8.2

* Mon Nov 20 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.8.0-1.git80f54bc
- bump to v1.8.0

* Wed Nov 15 2017 Dan Walsh <dwalsh@redhat.com> - 1.0.4-2.git4aceedee
- Fix script error in kpod completions.

* Mon Nov 13 2017 Dan Walsh <dwalsh@redhat.com> - 1.0.4-1.git4aceedee
- bump to v1.0.4
- Add crictl.yaml
- Add prometheous end points
- Several bug fixes

* Fri Nov 10 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.3-1.git17bcfb4
- bump to v1.0.3

* Fri Nov 03 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.2-3.git748bc46
- enable debuginfo for C binaries

* Fri Nov 03 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.2-2.git748bc46
- enable debuginfo

* Mon Oct 30 2017 Dan Walsh <dwalsh@redhat.com> - 1.0.2-1.git748bc46
- Lots of bug fixes
- Fixes to pass cri-tools tests

* Wed Oct 25 2017 Dan Walsh <dwalsh@redhat.com> - 1.0.1-1.git64a30e1
- Lots of bug fixes
- Fixes to pass cri-tools tests

* Thu Oct 19 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-7.gita636972
- update dep NVRs
- update release tag

* Mon Oct 16 2017 Dan Walsh <dwalsh@redhat.com> - 1.0.0-6.gita636972
- Get the correct checksum
- Setup storage-opt to override kernel check

* Fri Oct 13 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-2.gitcd1bac5
- bump to v1.0.0
- require containernetworking-plugins >= 0.5.2-3

* Wed Oct 11 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-1.rc3.gitd2c6f64
- bump to v1.0.0-rc3

* Wed Sep 20 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-1.rc2.git6784a66
- bump to v1.0.0-rc2

* Mon Sep 18 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-2.rc1.gitbb1da97
- bump release tag and build for extras

* Mon Sep 18 2017 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-1.rc1.gitbb1da97
- bump to v1.0.0-rc1 tag
- built commit bb1da97
- use bundled deps
- disable devel package
- remove redundant meta-provides

* Thu Aug 3 2017 Dan Walsh <dwalsh@redhat.com> - 1.0.0.beta.0-1.git66d96e7
- Beta Release
-   Additional registry support
-   Daemon pids-limit support
-   cri-o daemon now supports a default pid-limit on all containers to prevent fork-bombs. This is configurable by admins through a flag or /etc/crio/crio.conf
-   Configurable image volume support
-   Bugs and Stability fixes
-   OCI 1.0 runtime support
-     Dropped internal runc, and now use systems runc

* Fri Jun 30 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0.alpha.0-1.git91977d3
- built commit 91977d3
- remove cri-o-cni subpackage
- require containernetworking-plugins >= 0.5.2-2 (same as containernetworking-cni)

* Fri Jun 23 2017 Antonio Murdaca <runcom@fedoraproject.org> - 1.0.0.alpha.0-0.git5dcbdc0.3
- rebuilt to include cri-o-cni sub package

* Wed Jun 21 2017 Antonio Murdaca <runcom@fedoraproject.org> - 1.0.0.alpha.0-0.git5dcbdc0.2
- rebuilt for s390x

* Wed Jun 21 2017 Antonio Murdaca <runcom@fedoraproject.org> - 1.0.0.alpha.0-0.git5dcbdc0.1
- built first alpha release

* Fri May 5 2017 Dan Walsh <dwalsh@redhat.com> 0.3-0.gitf648cd6e
- Bump up version to 0.3

* Tue Mar 21 2017 Dan Walsh <dwalsh@redhat.com> 0.2-1.git7d7570e
- Bump up version to 0.2

* Tue Mar 21 2017 Dan Walsh <dwalsh@redhat.com> 0.1-1.git9bf26b5
- Bump up version to 0.1

* Mon Feb 13 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.15.git0639f06
- built commit 0639f06
- packaging workarounds for 'go install'

* Wed Feb 8 2017 Dan Walsh <dwalsh@redhat.com> 0-0.14.git6bd7c53
- Use newer versions of runc
- Applying k8s kubelet v3 api to cri-o server
- Applying k8s.io v3 API for ocic and ocid
- doc: Add instruction to run cri-o with kubernetes
- Lots of  updates of container/storage and containers/image

* Mon Jan 23 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0-0.13.git7cc8492
- Build on all kubernetes arches

* Fri Jan 20 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.12.git7cc8492
- add bash completion
- From: Daniel J Walsh <dwalsh@redhat.com>

* Thu Jan 19 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.11.git7cc8492
- remove trailing whitespace from unitfile

* Thu Jan 19 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.10.git7cc8492
- built commit 7cc8492
- packaging fixes from Nalin Dahyabhai <nalin@redhat.com>

* Thu Jan 19 2017 Dan Walsh <dwalsh@redhat.com> - 0-0.9.gitb9dc097
- Change to require skopeo-containers
- Merge Nalind/storage patch
-    Now uses Storage for Image Management

* Mon Jan 16 2017 Lokesh Manvekar <lsm5@fedoraproject.org> - 0-0.8.git2e6070f
- packaging changes from Nalin Dahyabhai <nalin@redhat.com>
- Don't make the ExecReload setting part of the ExecStart setting.
- Create ocid.conf in install, not in check.
- Own /etc/ocid.
- Install an "anything goes" pulling policy for a default.

* Thu Dec 22 2016 Dan Walsh <dwalsh@redhat.com> - 0-0.7.git2e6070f
- Switch locate to /var/lib/containers for images

* Thu Dec 22 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.6.git2e6070f
- built commit 2e6070f

* Wed Dec 21 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.5.git36dfef5
- install plugins into /usr/libexec/ocid/cni/
- require runc >= 1.0.0 rc2

* Wed Dec 21 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.4.git36dfef5
- built runcom/alpha commit 36dfef5
- cni bundled for now

* Thu Dec 15 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.3.gitc57530e
- Resolves: #1392977 - first upload to Fedora
- add build deps, enable only for x86_64 (doesn't build on i686)

* Thu Dec 15 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.2.gitc57530e
- add Godeps.json

* Tue Nov 08 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.1.gitc57530e
- First package for Fedora
