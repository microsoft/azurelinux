# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# go-rpm-macros are not available on RHEL.
%global have_go_rpm_macros 1
%global with_debug 0

# Shamelessly copied from CRI-O spec file.
%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

# https://github.com/rust-lang/rust/issues/47714
%undefine _strict_symbol_defs_build

# We want verbose builds
%global _configure_disable_silent_rules 1

# Use bundled deps as we don't ship the exact right versions for all the
# required rust libraries
%global bundled_rust_deps 1

# Release candidate version tracking
# global rcver rc0
%if 0%{?rcver:1}
%global rcrel .%{rcver}
%global rcstr -%{rcver}
%endif

# https://github.com/kata-containers/kata-containers
Version: 3.26.0
%global tag         %{version}%{?rcstr}

%global domain      github.com
%global org         kata-containers
%global repo        kata-containers
%global download    %{domain}/%{org}/%{repo}
%global importname  %{download}


%global common_description %{expand:
Kata Containers version 3.x repository. Kata Containers is an open source
project and community working to build a standard implementation of lightweight
Virtual Machines (VMs) that feel and perform like containers, but provide the
workload isolation and security advantages of VMs. https://katacontainers.io/.}

%global golicenses  LICENSE \\\
                    src/agent/LICENSE

%global godocs      README.md \\\
                    CODE_OF_CONDUCT.md \\\
                    CONTRIBUTING.md\\\
                    src/agent/README.md

# Note: the original vendor tarball is quite big (918M for 3.16)
# Unlike for RHEL, we cannot strip it down because we build all components
# (RHEL builds only build kata-agent)
Name:       %{repo}
Release: 2%{?rcrel}%{?dist}
Summary:    Kata Containers version 3.x repository
License:    Apache-2.0
Url:        https://%{download}
Source0:    https://%{download}/archive/%{version}%{?rcstr}/%{repo}-%{version}%{?rcstr}.tar.gz
Source1:    https://%{download}/releases/download/%{version}/%{repo}-%{version}%{?rcstr}-vendor.tar.gz
Source2:    kata-osbuilder.sh
Source3:    kata-osbuilder-generate.service
Source4:    15-dracut.conf
Source5:    50-kata

# Keep this patch downstream as it'd be hard to justify such change upstream
Patch0999:  0999-osbuilder-Adjust-agent_version-for-our-builds.patch
Patch1001:  1001-Remove-warnings-as-compilation-errors.patch

%if 0%{?have_go_rpm_macros}
BuildRequires: go-rpm-macros
%else
BuildRequires: compiler(go-compiler)
BuildRequires: golang
%endif

BuildRequires: git-core
BuildRequires: libselinux-devel
BuildRequires: libseccomp-devel
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: systemd
BuildRequires: gcc
BuildRequires: protobuf-compiler
BuildRequires: clang-libs

%{?systemd_requires}
# %%check requirements
BuildRequires: dbus
BuildRequires: dbus-daemon
BuildRequires: dracut
BuildRequires: kernel
BuildRequires: busybox
BuildRequires: rsyslog

%if 0%{?bundled_rust_deps}
BuildRequires: cargo
BuildRequires: rust
%else
# Generated using rust2rpm
# [dependencies]
BuildRequires: rust-packaging
BuildRequires: (crate(anyhow/default) >= 1.0.32 with crate(anyhow/default) < 2.0.0)
BuildRequires: (crate(lazy_static/default) >= 1.3.0 with crate(lazy_static/default) < 2.0.0)
BuildRequires: (crate(libc/default) >= 0.2.58 with crate(libc/default) < 0.3.0)
BuildRequires: (crate(log/default) >= 0.4.11 with crate(log/default) < 0.5.0)
BuildRequires: (crate(nix/default) >= 0.17.0 with crate(nix/default) < 0.18.0)
BuildRequires: (crate(prctl/default) >= 1.0.0 with crate(prctl/default) < 2.0.0)
BuildRequires: (crate(procfs/default) >= 0.7.9 with crate(procfs/default) < 0.8.0)
BuildRequires: (crate(prometheus/default) >= 0.9.0 with crate(prometheus/default) < 0.10.0)
BuildRequires: (crate(prometheus/process) >= 0.9.0 with crate(prometheus/process) < 0.10.0)
BuildRequires: (crate(regex/default) >= 1.0.0 with crate(regex/default) < 2.0.0)
BuildRequires: (crate(scan_fmt/default) >= 0.2.3 with crate(scan_fmt/default) < 0.3.0)
BuildRequires: (crate(scopeguard/default) >= 1.0.0 with crate(scopeguard/default) < 2.0.0)
BuildRequires: (crate(serde_json/default) >= 1.0.39 with crate(serde_json/default) < 2.0.0)
BuildRequires: (crate(signal-hook/default) >= 0.1.9 with crate(signal-hook/default) < 0.2.0)
BuildRequires: (crate(slog-scope/default) >= 4.1.2 with crate(slog-scope/default) < 5.0.0)
BuildRequires: (crate(slog-stdlog/default) >= 4.0.0 with crate(slog-stdlog/default) < 5.0.0)
BuildRequires: (crate(slog/default) >= 2.5.2 with crate(slog/default) < 3.0.0)
BuildRequires: (crate(slog/dynamic-keys) >= 2.5.2 with crate(slog/dynamic-keys) < 3.0.0)
BuildRequires: (crate(slog/max_level_trace) >= 2.5.2 with crate(slog/max_level_trace) < 3.0.0)
BuildRequires: (crate(slog/release_max_level_info) >= 2.5.2 with crate(slog/release_max_level_info) < 3.0.0)
BuildRequires: (crate(tempfile/default) >= 3.1.0 with crate(tempfile/default) < 4.0.0)
BuildRequires: crate(cgroups/default) >= 0.0.0
BuildRequires: crate(logging/default) >= 0.0.0
BuildRequires: crate(netlink/default) >= 0.0.0
BuildRequires: crate(netlink/with-agent-handler) >= 0.0.0
BuildRequires: crate(netlink/with-log) >= 0.0.0
BuildRequires: crate(oci/default) >= 0.0.0
BuildRequires: crate(protobuf/default) = 2.14.0
BuildRequires: crate(protocols/default) >= 0.0.0
BuildRequires: crate(rustjail/default) >= 0.0.0
BuildRequires: crate(ttrpc/default) >= 0.0.0
%endif

Requires: busybox
Requires: binutils
Requires: dracut
Requires: kernel
Requires: qemu-kvm-core >= 8.2.0-1
# For /usr/libexec/virtiofsd
Requires: (virtiofsd or qemu-virtiofsd)
Suggests: virtiofsd

Conflicts: kata-agent
Conflicts: kata-ksm-throttler
Conflicts: kata-osbuilder
Conflicts: kata-proxy
Conflicts: kata-runtime
Conflicts: kata-shim

# The following architectures lack the required qemu support
ExcludeArch: %{arm} %{ix86} s390 s390x

# Building kata-ctl on ppc64le is currently being skipped
ExcludeArch: ppc64le

%description
%{common_description}

%gopkg


# Common variables to pass to 'make'
# The machine type uses a modern default
# The kernel parameters workaround an issue with cgroupsv2 after kernel 5.3
# To-do: add BUILDFLAGS=gobuildflags when the macro becomes available
%global qemu qemu-system-%{_arch}
%global qemupath %{_bindir}/%{qemu}

# The machine type to be used is architecture specific:
# aarch64: virt
# ppc64le: pseries
# s390x: s390-ccw-virtio
# x86_64: q35
%ifarch aarch64
%global machinetype "virt"
%endif
%ifarch ppc64le
%global machinetype "pseries"
%endif
%ifarch s390x
%global machinetype "s390-ccw-virtio"
%endif
%ifarch x86_64
%global machinetype "q35"
%endif

%global kata_build_dir          %{repo}-%{version}%{?rcstr}
%global katadatadir             %{_datadir}/kata-containers
%global katadefaults            %{katadatadir}/defaults
%global katacache               %{_localstatedir}/cache
%global katalibexecdir          %{_libexecdir}/kata-containers
%global katalocalstatecachedir  %{katacache}/kata-containers

%global kataagentdir            %{katalibexecdir}/agent
%global kataosbuilderdir        %{katalibexecdir}/osbuilder
%global rust_make_vars          LIBC=gnu

%global runtime_make_vars       QEMUPATH=%{qemupath} \\\
                                KERNELTYPE="compressed" \\\
                                DEFSHAREDFS="virtio-fs" \\\
                                DEFVIRTIOFSDAEMON=%{_libexecdir}/"virtiofsd" \\\
                                DEFVIRTIOFSCACHESIZE=0 \\\
                                DEFSANDBOXCGROUPONLY=true \\\
                                SKIP_GO_VERSION_CHECK=y \\\
                                MACHINETYPE=%{machinetype} \\\
                                SCRIPTS_DIR=%{_bindir} \\\
                                DESTDIR=%{buildroot} \\\
                                PREFIX=/usr \\\
                                DEFAULTSDIR=%{katadefaults} \\\
                                CONFDIR=%{katadefaults} \\\
                                FEATURE_SELINUX="yes" \\\
                                DEFENABLEANNOTATIONS=['\\\".*\\\"']

%global agent_make_vars         %{rust_make_vars} \\\
                                DESTDIR=%{buildroot}%{kataagentdir}
%global kata_ctl_vars           %{rust_make_vars} \\\
                                INSTALL_PATH=%{buildroot}%{_prefix}

%prep
%autosetup -S git -p1 -n %{kata_build_dir}

cd %{_builddir}/%{kata_build_dir}
tar -xf %{SOURCE1}

# Not using gobuild here in order to stick to how upstream builds
# (This builds multiple binaries)
%build
%set_build_flags

export PATH=$PATH:"$(pwd)/go/bin"
export GOPATH="$(pwd)/go"

mkdir -p go/src/%{domain}/%{org}
ln -s $(pwd)/../%{kata_build_dir} go/src/%{importname}
cd go/src/%{importname}

pushd src/runtime
%make_build %{runtime_make_vars}
popd

pushd src/agent
%make_build %{agent_make_vars}
touch kata-agent
popd

pushd src/tools/kata-ctl
%make_build %{kata_ctl_vars}
popd

pushd tools/osbuilder
# Manually build nsdax tool
gcc %{build_cflags} image-builder/nsdax.gpl.c -o nsdax
popd

# Not using gopkginstall here in order to stick to how upstream builds
%install
export GOPATH=$(pwd)/go
export PATH=$PATH:$GOPATH/bin

cd go/src/%{importname}

install -m 0644 -D -t %{buildroot}%{katalibexecdir} VERSION

pushd src/runtime
%make_install %{runtime_make_vars}
popd

pushd src/agent
%make_install %{agent_make_vars}
popd

pushd src/tools/kata-ctl
%make_install %{kata_ctl_vars}
rm -f %{buildroot}%{_prefix}/.crates.toml
rm -f %{buildroot}%{_prefix}/.crates2.json
popd

pushd tools/osbuilder
rm .gitignore
rm rootfs-builder/.gitignore
mkdir -p %{buildroot}%{katalocalstatecachedir}

install -m 0644 -D -t %{buildroot}%{_unitdir} %{SOURCE3}
install -m 0755 -D -t %{buildroot}%{kataosbuilderdir} nsdax
install -m 0644 -D -t %{buildroot}%{kataosbuilderdir} %{SOURCE2}

cp -aR rootfs-builder %{buildroot}%{kataosbuilderdir}
cp -aR image-builder  %{buildroot}%{kataosbuilderdir}
cp -aR initrd-builder %{buildroot}%{kataosbuilderdir}
cp -aR scripts        %{buildroot}%{kataosbuilderdir}
cp -aR dracut         %{buildroot}%{kataosbuilderdir}

rm -f %{buildroot}%{kataosbuilderdir}/image-builder/nsdax.gpl.c
install -m 0644 -D -t %{buildroot}%{kataosbuilderdir}/dracut/dracut.conf.d/ %{SOURCE4}
chmod +x %{buildroot}%{kataosbuilderdir}/scripts/lib.sh
chmod +x %{buildroot}%{kataosbuilderdir}/kata-osbuilder.sh
popd

# Install the CRI-O config drop-in file
install -m 0644 -D -t %{buildroot}%{_sysconfdir}/crio/crio.conf.d %{SOURCE5}

# Disable the image= option, so we use initrd= by default
# The kernels kata-osbuilder creates are in /var/cache now, see rhbz#1792216
sed -i -e 's|^kernel = "%{_datadir}|kernel = "%{katacache}|' \
       -e 's|^image = "%{_datadir}/kata-containers/kata-containers.img"|initrd = "%{katacache}/kata-containers/kata-containers-initrd.img"|' \
       %{buildroot}%{katadefaults}/configuration.toml

# Enable vsock as transport instead of virtio-serial
sed -i -e 's/^#use_vsock =/use_vsock =/' %{buildroot}%{katadefaults}/configuration.toml

# We could be run in a mock chroot, where uname will report
# different kernel than what we have installed in the chroot.
# So we need to determine a valid kernel version to test against.
for kernelpath in /lib/modules/*/vmlinu*; do
    KVERSION="$(echo $kernelpath | cut -d "/" -f 4)"
    break
done
TEST_MODE=1 %{buildroot}%{kataosbuilderdir}/kata-osbuilder.sh \
    -o %{buildroot}%{kataosbuilderdir} \
    -k "$KVERSION" \
    -a %{buildroot}


%preun
%systemd_preun kata-osbuilder-generate.service

%postun
%systemd_postun kata-osbuilder-generate.service

%post
%systemd_post kata-osbuilder-generate.service
# Skip running this on Fedora CoreOS / Red Hat CoreOS
if test -w %{katalocalstatecachedir}; then
    TMPOUT="$(mktemp -t kata-rpm-post-XXXXXX.log)"
    echo "Creating kata appliance initrd..."
    %{kataosbuilderdir}/kata-osbuilder.sh > ${TMPOUT} 2>&1
    if test "$?" != "0" ; then
        echo "Building failed. Here is the log details:"
        cat ${TMPOUT}
        exit 1
    fi
fi


%files
# runtime
%{_bindir}/kata-runtime
%{_bindir}/kata-monitor
%{_bindir}/containerd-shim-kata-v2
%{_bindir}/kata-collect-data.sh
%dir %{katalibexecdir}
%{katalibexecdir}/VERSION
%dir %{katadatadir}
%dir %{katadefaults}
%{katadefaults}/configuration.toml
%{_datadir}/bash-completion/completions/kata-runtime
%license LICENSE
%doc README.md CONTRIBUTING.md

#agent
%dir %{kataagentdir}
%{kataagentdir}/*

#kata-ctl
%{_bindir}/kata-ctl

#osbuilder
%dir %{kataosbuilderdir}
%dir %{katalocalstatecachedir}

%{kataosbuilderdir}/*
%{_unitdir}/kata-osbuilder-generate.service

# CRI-O drop-in file
%{_sysconfdir}/crio/crio.conf.d/50-kata

# Remove some scripts we don't use
%exclude %{katadefaults}/configuration-*.toml
%exclude %{kataosbuilderdir}/rootfs-builder/alpine
%exclude %{kataosbuilderdir}/rootfs-builder/centos
%exclude %{kataosbuilderdir}/rootfs-builder/debian
%exclude %{kataosbuilderdir}/rootfs-builder/template
%exclude %{kataosbuilderdir}/rootfs-builder/ubuntu


%changelog
* Mon Feb 09 2026 Christophe de Dinechin <dinechin@redhat.com> - 3.26.0-1
- kata-containers 3.26.0

* Tue Jan 20 2026 Christophe de Dinechin <dinechin@redhat.com> - 3.25.0-1
- kata-containers 3.25.0

* Mon Jan 19 2026 Christophe de Dinechin <dinechin@redhat.com> - 3.24.0-1
- kata-containers 3.24.0

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Nov 04 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.22.0-1
- kata-containers 3.22.0

* Thu Sep 25 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.21.0-1
- kata-containers 3.21.0

* Wed Sep 10 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.20.0-1
- kata-containers 3.20.0

* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 3.19.1-1.1
- Rebuild for golang-1.25.0

* Mon Jul 28 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.19.1-1
- kata-containers 3.19.0

* Mon Jul 28 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.18.0-1
- kata-containers 3.18.0

* Fri Jul 25 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.17.0-1
- kata-containers 3.17.0

* Thu Jul 24 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.16.0-1
- kata-containers 3.16.0

* Thu Jul 24 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.15.0-1
- kata-containers 3.15.0

* Wed Jul 23 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.14.1-1
- kata-containers 3.14.1, add fix for systemd configuration and rpm sanity test

* Tue Jul 08 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.14.0-1
- kata-containers 3.14.0, update to latest release

* Mon Jul 07 2025 Christophe de Dinechin <dinechin@redhat.com> - 3.13.0-1
- kata-containers 3.13.0, required vendor source correction

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 06 2025 Emanuel Lima <emlima@redhat.com> - 3.12.0-1
- kata-containers 3.12.0

* Tue Nov 26 2024 Emanuel Lima <emlima@redhat.com> - 3.11.0-1
- kata-containers 3.11.0

* Mon Oct 07 2024 Emanuel Lima <emlima@redhat.com> - 3.9.0-1
- kata-containers 3.9.0
  Fix warnings as compilation errors patch
  Add time dependency compilation error patch
  Add arch name compilation failure patch
  Add binutils and rsyslog as dependencies
  Add AGENT_POLICY patch

* Mon Sep 16 2024 Emanuel Lima <emlima@redhat.com> - 3.7.0-1
- kata-containers 3.7.0
  Add "io.kubernetes.cri-o.Devices" to cri-o config
  Remove the openssl feature patch
  Bump QEMU to 8.2
  Add Remove-warnings-as-compilation-errors patch

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Emanuel Lima <emlima@redhat.com> - 3.6.0-2
- Add openssl-devel as a dependency
- Build kata-ctl instead of log-parser
- Add clang-libs, dbus and dbus-daemon as  build dependencies
- Exclude ppc64le from the build pipeline

* Tue Jun 18 2024 Emanuel Lima <emlima@redhat.com> - 3.6.0-1
- Bump to kata-containers-3.6.0
- Fix agent-Remove-openssl-vendored-feature patch

* Fri Apr 05 2024 Emanuel Lima <emlima@redhat.com> - 3.3.0-1
- Add clang-libs as a build dependency
  Apply spec-Bump-Kata-Containers-to-its-3.3.0-release.patch
  Apply agent-Remove-vendored-features-from-openssl-sys.patch
  Apply spec-Add-openssl-devel-as-a-dependency.patch
  Apply spec-Build-kata-ctl-instead-of-log-parser.patch

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 3.2.0-2.3
- Rebuild for golang 1.22.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 06 2023 Emanuel Lima <emlima@redhat.com> - 3.2.0-2
- migrated to SPDX license
- kata-containers-3.2.0 final

* Thu Sep 28 2023 Emanuel Lima <emlima@redhat.com> - 3.2.0-1
- kata-containers-3.2.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 3.0.1-1
- kata-containers-3.0.1

* Wed Oct 26 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 3.0.0-1
- kata-containers-3.0.0

* Wed Oct 26 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.5.2-1
- kata-containers-2.5.2

* Wed Oct 26 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.5.1-1
- kata-containers-2.5.1

* Wed Oct 26 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.5.0-1
- kata-containers-2.5.0

* Wed Oct 26 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.4.3-1
- kata-containers-2.4.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 2.4.2-1.1
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Tue Jun 14 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.4.2-1
- kata-containers-2.4.2

* Thu May 12 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.4.1-1
- kata-containers-2.4.1

* Fri Apr 01 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.4.0-1
- kata-containers-2.4.0

* Wed Mar 09 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.3.3-1
- kata-containers-2.3.3

* Thu Feb 10 2022 Cole Robinson <crobinso@redhat.com> - 2.3.2-2
- Add explicit dep on /usr/libexec/virtiofsd

* Thu Feb 03 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.3.2-1
- kata-containers-2.3.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.3.0-1
- kata-containers-2.3.0

* Mon Nov 08 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.3-1
- kata-containers-2.2.3

* Mon Oct 18 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.2-1
- kata-containers-2.2.2

* Mon Sep 27 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.1-1
- kata-containers-2.2.1

* Fri Sep 17 2021 Jakob Naucke <jakob.naucke@ibm.com> - 2.2.0-3
- Add an s390x build target

* Thu Sep 02 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.0-2
- Provide vendored code as a tarball instead of patch

* Wed Sep 01 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.0-1
- kata-containers-2.2.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 27 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.1.0-2
- Add the CRI-O drop-in file to the package
  Resolves: rhbz#1967594
- qemu: Update QEMU binary & its location
  Resolves: rhbz#1967602

* Thu May 27 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.1.0-1
- kata-containers 2.1.0

* Fri Apr 09 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.0.3-1
- kata-containers 2.0.3

* Tue Apr 06 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.0.2-1
- kata-containers 2.0.2

* Mon Mar 08 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.0.1-1
- Kata-containers 2.0.1

* Thu Dec 17 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.0.0-1
- Adjust package for Fedora review.

* Thu Nov 26 2020 Fabiano Fidêncio <fabiano@fidencio.org> - 2.0.0-0
- Initial packaging
