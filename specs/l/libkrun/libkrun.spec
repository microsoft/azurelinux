# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# libkrun tests require access to "/dev/kvm", which is usually not be available
# on build sandboxes.
%bcond_with check

%if 0%{?rhel}
%global bundled_rust_deps 1
%else
%global bundled_rust_deps 0
%endif

Name:           libkrun
Version:        1.17.4
Release:        1%{?dist}
Summary:        Dynamic library providing Virtualization-based process isolation capabilities

License:        Apache-2.0
URL:            https://github.com/containers/libkrun
Source:         https://github.com/containers/libkrun/archive/refs/tags/v%{version}.tar.gz
%if 0%{?bundled_rust_deps}
# Generated with:
#  cargo vendor-filterer --platform=*-unknown-linux-gnu --features blk,net,gpu,snd,amd-sev
Source1:        %{name}-%{version}-vendor.tar.xz
%else
# Remove references to unused deps so we don't need to install them for
# building this package
Patch0:         libkrun-remove-unused-deps.diff
# Disable nitro until the dependencies are packaged.
Patch1:         libkrun-remove-nitro-deps.diff
# Disable TDX untile the dependencies are packaged.
Patch2:         libkrun-remove-tdx-deps.diff
# Bump bzip2 dependency to match the version packaged in Fedora.
Patch3:         libkrun-bump-bzip-dep.diff
# For aarch64, remove references to SEV and TDX deps which are only available on x86_64
Patch4:         libkrun-remove-sev-deps.diff
%endif

# libkrun only supports x86_64 and aarch64
ExclusiveArch:  x86_64 aarch64

# Starting 1.11.0, libkrunfw is no longer build-time linked.
Requires:  libkrunfw >= 5.0.0

# While this project is composed mostly of Rust code, this is not a
# conventional Rust crate. The root of the project is a workspace, there's a C
# file that also needs to be compiled, and the resulting binary a dynamic
# library providing a C-compatible ABI.
#
# As a result, we can't fully rely on rust-packaging for managing this package.
# Instead, we use some of its tasks (cargo_prep and cargo_test) and combine
# them with using the Makefile provided by the project. We also need to manage
# BuildRequires manually, as rust-packaging gets confused trying to generate
# them dynamically.
BuildRequires:  rust-packaging >= 21
BuildRequires:  glibc-static
BuildRequires:  binutils
BuildRequires:  libepoxy-devel
BuildRequires:  libdrm-devel
BuildRequires:  virglrenderer-devel
BuildRequires:  pipewire-devel
BuildRequires:  clang-devel
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
%ifarch aarch64
BuildRequires:  libfdt-devel
%endif

%if ! 0%{?bundled_rust_deps}
BuildRequires:  crate(libc/default) >= 0.2.39
BuildRequires:  crate(vm-memory/backend-mmap) >= 0.16.0
BuildRequires:  crate(vm-memory/default) >= 0.16.0
BuildRequires:  crate(kvm-bindings/default) >= 0.13.0
BuildRequires:  crate(kvm-bindings/fam-wrappers) >= 0.13.0
BuildRequires:  crate(kvm-ioctls/default) >= 0.23.0
BuildRequires:  crate(vmm-sys-util/default) >= 0.14.0
BuildRequires:  crate(vm-fdt/default) >= 0.2.0
BuildRequires:  (crate(virtio-bindings/default) >= 0.2.0 with crate(virtio-bindings/default) < 0.3.0~)
BuildRequires:  (crate(bitflags/default) >= 1.2.0 with crate(bitflags/default) < 2.0.0~)
BuildRequires:  (crate(env_logger/default) >= 0.11.0 with crate(env_logger/default) < 0.12.0~)
BuildRequires:  (crate(log/default) >= 0.4.0 with crate(log/default) < 0.5.0~)
BuildRequires:  (crate(nix/default) >= 0.30.1 with crate(nix/default) < 0.31.0~)
BuildRequires:  (crate(memoffset/default) >= 0.9.1 with crate(memoffset/default) < 0.10.0~)
BuildRequires:  (crate(rand/default) >= 0.8.5 with crate(rand/default) < 0.9.0~)
BuildRequires:  (crate(rand/default) >= 0.9.2 with crate(rand/default) < 0.10.0~)
BuildRequires:  (crate(once_cell/default) >= 1.4.1 with crate(once_cell/default) < 2.0.0~)
BuildRequires:  (crate(crossbeam-channel/default) >= 0.5.0 with crate(crossbeam-channel/default) < 0.6.0~)
BuildRequires:  (crate(pipewire/default) >= 0.8.0 with crate(pipewire/default) < 0.9.0~)
BuildRequires:  (crate(zerocopy/default) >= 0.8.0 with crate(zerocopy/default) < 0.9.0~)
BuildRequires:  (crate(remain/default) >= 0.2.0 with crate(remain/default) < 0.3.0~)
BuildRequires:  (crate(caps/default) >= 0.5.0 with crate(caps/default) < 0.6.0~)
BuildRequires:  (crate(imago/default) >= 0.2.1 with crate(imago/default) < 0.3.0~)
BuildRequires:  (crate(linux-loader/default) >= 0.13.0 with crate(linux-loader/default) < 0.14.0~)
BuildRequires:  (crate(bzip2/default) >= 0.6.0 with crate(bzip2/default) < 0.7.0~)
BuildRequires:  (crate(zstd/default) >= 0.13.0 with crate(zstd/default) < 0.14.0~)
BuildRequires:  (crate(flate2/default) >= 1.0.0 with crate(flate2/default) < 2.0.0~)
BuildRequires:  (crate(static_assertions/default) >= 1.1.0 with crate(static_assertions/default) < 2.0.0~)
BuildRequires:  (crate(thiserror/default) >= 2.0.0 with crate(thiserror/default) < 3.0.0~)
BuildRequires:  (crate(capng/default) >= 0.2.3 with crate(capng/default) < 0.3.0~)

%if 0%{?build_sev}
# SEV variant dependencies
BuildRequires:  (crate(kbs-types/default) >= 0.14.0 with crate(kbs-types/default) < 0.15.0~)
BuildRequires:  (crate(codicon/default) >= 3.0.0 with crate(codicon/default) < 4.0.0~)
BuildRequires:  (crate(curl/default) >= 0.4.0 with crate(curl/default) < 0.5.0~)
BuildRequires:  (crate(procfs/default) >= 0.12.0 with crate(procfs/default) < 0.13.0~)
BuildRequires:  (crate(sev/default) >= 6.0.0 with crate(sev/default) < 7.0.0~)
BuildRequires:  (crate(sev/openssl) >= 6.0.0 with crate(sev/openssl) < 7.0.0~)
BuildRequires:  (crate(serde/default) >= 1.0.0 with crate(serde/default) < 2.0.0~)
BuildRequires:  (crate(serde/derive) >= 1.0.0 with crate(serde/derive) < 2.0.0~)
BuildRequires:  (crate(serde_json/default) >= 1.0.0 with crate(serde_json/default) < 2.0.0~)
%endif
%endif

%description
%{summary}.

%package devel
Summary: Header files and libraries for libkrun development
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The libkrun-devel package containes the libraries and headers needed to
develop programs that use libkrun Virtualization-based process isolation
capabilities.

# SEV is a feature provided by AMD EPYC processors, so only it's only
# available on x86_64.
%if 0%{?build_sev}
%package sev
Summary: Dynamic library providing Virtualization-based process isolation capabilities (SEV variant)
Requires:  libkrunfw-sev >= 4.0.0

%description sev
Dynamic library providing Virtualization-based process isolation
capabilities, with the ability to use AMD SEV to create a microVM-based
Trusted Execution Environment (TEE).

%package sev-devel
Summary: Header files and libraries for libkrun development
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-sev%{?_isa} = %{version}-%{release}

%description sev-devel
The libkrun-sev-devel package containes the libraries and headers needed to
develop programs that use libkrun-sev Virtualization-based process isolation
capabilities.
%endif

%prep
%if 0%{?bundled_rust_deps}
%autosetup -n %{name}-%{version_no_tilde} -a1
%cargo_prep -v vendor
%else
%setup -q -n %{name}-%{version_no_tilde}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%if ! 0%{?build_sev}
%patch -P 4 -p1
%endif
%cargo_prep
%endif

%build
%make_build init/init
%make_build libkrun.pc
%make_build GPU=1 BLK=1 NET=1 SND=1
%if 0%{?build_sev}
    rm init/init
    %make_build SEV=1 init/init
    %cargo_build -f amd-sev
    mv target/release/libkrun.so target/release/libkrun-sev.so.%{version}
%endif
%if 0%{?bundled_rust_deps}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest
%endif

%install
%make_install PREFIX=%{_prefix}
%if 0%{?build_sev}
    %make_install SEV=1 PREFIX=%{_prefix}
%endif

%files
%license LICENSE
%if 0%{?bundled_rust_deps}
%license LICENSE.dependencies
%license cargo-vendor.txt
%endif
%doc README.md
%{_libdir}/libkrun.so.%{version}
%{_libdir}/libkrun.so.1

%files devel
%{_libdir}/libkrun.so
%{_libdir}/pkgconfig/libkrun.pc
%{_includedir}/libkrun.h
%{_includedir}/libkrun_display.h
%{_includedir}/libkrun_input.h

%if 0%{?build_sev}
%files sev
%license LICENSE
%if 0%{?bundled_rust_deps}
%license LICENSE.dependencies
%license cargo-vendor.txt
%endif
%doc README.md
%{_libdir}/libkrun-sev.so.%{version}
%{_libdir}/libkrun-sev.so.1

%files sev-devel
%{_libdir}/libkrun-sev.so
%endif

%if %{with check}
%check
%cargo_test
%endif

%changelog
* Wed Feb 18 2026 Sergio Lopez <slp@redhat.com> - 1.17.4-1
- Update to version 1.17.4

* Wed Feb 04 2026 Sergio Lopez <slp@redhat.com> - 1.17.2-1
- Update to version 1.17.2

* Mon Jan 19 2026 Sergio Lopez <slp@redhat.com> - 1.17.0-3
- Rebuilt for new side tag

* Sat Jan 17 2026 Sergio Lopez <slp@redhat.com> - 1.17.0-2
- Require libkrunfw >= 5.x.x

* Fri Jan 16 2026 Sergio Lopez <slp@redhat.com> - 1.17.0-1
- Update to version 1.17.0

* Mon Sep 01 2025 Sergio Lopez <slp@redhat.com> - 1.15.1-1
- Update to version 1.15.1

* Mon Aug 04 2025 Sergio Lopez <slp@redhat.com> - 1.14.0-1
- Update to version 1.14.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Sergio Lopez <slp@redhat.com> - 1.13.0-1
- Update to version 1.13.0

* Tue May 20 2025 Sergio Lopez <slp@redhat.com> - 1.12.2-1
- Update to version 1.12.2

* Mon Apr 21 2025 Sergio Lopez <slp@redhat.com> - 1.11.2-1
- Update to version 1.11.2
- Re-enable debuginfo, fixed by dropping the use of patchelf.

* Fri Mar 21 2025 Sergio Lopez <slp@redhat.com> - 1.10.1-3
- Temporarily disable debuginfo generation until RHBZ#2354052 is fixed.

* Thu Feb 06 2025 Fabio Valentini <decathorpe@gmail.com> - 1.10.1-2
- Rebuild for openssl crate >= v0.10.70 (RUSTSEC-2025-0004)

* Mon Jan 20 2025 Sergio Lopez <slp@redhat.com> - 1.10.1-1
- Update to version 1.10.1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 27 2024 Sergio Lopez <slp@redhat.com> - 1.9.5-1
- Update to version 1.9.5
- Vendorize dependencies ahead of package unification

* Tue Jul 23 2024 Sergio Lopez <slp@redhat.com> - 1.9.4-1
- Update to version 1.9.4

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 04 2024 Sergio Lopez <slp@redhat.com> - 1.9.2-1
- Update to version 1.9.2

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Sergio Lopez <slp@redhat.com> - 1.7.2-2
- Update versions of rust-vmm dependencies

* Sun Dec 24 2023 Sergio Lopez <slp@redhat.com> - 1.7.2-1
- Update to version 1.7.2

* Fri Dec 01 2023 Fabio Valentini <decathorpe@gmail.com> - 1.5.0-7
- Rebuild for openssl crate >= v0.10.60 (RUSTSEC-2023-0044, RUSTSEC-2023-0072)

* Tue Sep 19 2023 Fabio Valentini <decathorpe@gmail.com> - 1.5.0-6
- Rebuild for vm-memory v0.12.2 / CVE-2023-41051.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 19 2023 Sergio Lopez <slp@redhat.com> - 1.5.0-4
- Update license specification to conform SPDX format

* Wed Jul 19 2023 Sergio Lopez <slp@redhat.com> - 1.5.0-3
- Update vm-memory requirement to version 0.12.0
- Update kvm-ioctls requirement to version 0.14.0
- Add a temporary patch to accomodate an API change in kvm-ioctls

* Wed May 03 2023 Fabio Valentini <decathorpe@gmail.com> - 1.5.0-2
- Rebuild for openssl crate >= v0.10.48 (RUSTSEC-2023-{0022,0023,0024})

* Thu Feb 09 2023 Sergio Lopez <slp@redhat.com> - 1.5.0-1
- Update to version 1.5.0
- Update vm-memory, kvm-bindings, kvm-ioctls, vmm-sys-utils and sev
  dependencies
- Add a patch to update and relax vm-memory dependency

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov  8 2022 Sergio Lopez <slp@redhat.com> - 1.4.8-1
- Update to upstream version 1.4.8
- Add crossbeam-channel to the list of dependencies
- Update libkrun-remove-sev-deps.diff patch

* Fri Aug 26 2022 Cole Robinson <crobinso@redhat.com> - 1.4.2-2
- Allow building with rust-sev-0.3.0

* Wed Aug 17 2022 Sergio Lopez <slp@redhat.com> - 1.4.2-1
- Update to upstream version 1.4.2
- Add the libkrun-sev and libkrun-sev-devel subpackages with the SEV variant of
  the library.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Sergio Lopez <slp@redhat.com> - 1.2.2-1
- Initial package

