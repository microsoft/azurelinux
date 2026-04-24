# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Version:       1.5.0
%global forgeurl https://gitlab.com/libblkio/libblkio
%global tag    v%{version}
%forgemeta

%if %{defined copr_username}
%define copr_build 1
%endif

Summary:       Block device I/O library
Name:          libblkio
Release: 6%{?dist}
URL:           %{forgeurl}
Source0:       %{forgesource}
# To create the vendor tarball:
#   tar xf %%{name}-v%%{version}.tar.bz2 ; pushd %%{name}-v%%{version} ; \
#   cargo vendor && tar Jcvf ../%%{name}-v%%{version}-vendor.tar.xz vendor/ ; popd
Source1:       %{name}-v%{version}-vendor.tar.xz
License:       (Apache-2.0 OR MIT) AND (Apache-2.0 OR BSD-3-Clause) AND (Apache-2.0 OR Apache-2.0 WITH LLVM-exception OR MIT) AND BSD-3-Clause

# Basic build requirements.
BuildRequires: gcc, gcc-c++
BuildRequires: make
BuildRequires: meson
%if 0%{?rhel}
BuildRequires: rust-toolset
%else
BuildRequires: rust-packaging >= 21
BuildRequires: rustfmt
BuildRequires: cargo
%endif
BuildRequires: python3-docutils
BuildRequires: pkgconf
%if %{defined copr_build}
BuildRequires: git
%endif

# XXX Eventually use %%generate_buildrequires but it does not support
# workspaces yet.  See
# https://bugzilla.redhat.com/show_bug.cgi?id=2124697#c57
#
# For major version >= 1, we are requiring that the major version does
# not change.
#
# For major version >= 0, we are requiring that the minor version does
# not change.
%if ! 0%{?rhel}
BuildRequires: (crate(autocfg/default) >= 1.0.0 with crate(autocfg/default) < 2.0.0~)
BuildRequires: (crate(bitflags/default) >= 2.5.0 with crate(bitflags/default) < 3.0.0~)
BuildRequires: (crate(bitflags/default) >= 1.2.0 with crate(bitflags/default) < 2.0.0~)
BuildRequires: (crate(cc/default) >= 1.0.0 with crate(cc/default) < 2.0.0~)
BuildRequires: (crate(io-uring/default) >= 0.6.0 with crate(io-uring/default) < 0.7.0~)
BuildRequires: (crate(lazy_static/default) >= 1.0.0 with crate(lazy_static/default) < 2.0.0~)
BuildRequires: (crate(libc/default) >= 0.2.153 with crate(libc/default) < 0.3.0~)
BuildRequires: (crate(memmap2/default) >= 0.5.7 with crate(memmap2/default) < 0.10.0~)
BuildRequires: (crate(num-traits/default) >= 0.2.15 with crate(num-traits/default) < 0.3.0~)
BuildRequires: (crate(paste/default) >= 1.0.0 with crate(paste/default) < 2.0.0~)
BuildRequires: (crate(pci-driver/default) >= 0.1.2 with crate(pci-driver/default) < 0.2.0~)
BuildRequires: (crate(rustix/default) >= 0.38.0 with crate(rustix/default) < 0.39.0~)
BuildRequires: (crate(virtio-bindings/default) >= 0.2.0 with crate(virtio-bindings/default) < 0.3.0~)
%endif


%description
libblkio is a library for high-performance block device I/O with
support for multi-queue devices. A C API is provided so that
applications can use the library from most programming languages.


%package devel
Summary:       Development tools for %{name}
Requires:      %{name}%{_isa} = %{version}-%{release}


%description devel
This package contains development tools for %{name}.


%prep
%if %{defined copr_build}
%autosetup -Sgit %{name}-%{version}
%else
%forgeautosetup -p1

%if 0%{?rhel}
tar xf %{SOURCE1}
%cargo_prep -v vendor
%else
%cargo_prep
%endif
sed -e 's/--locked//' -i src/cargo-build.sh

%endif


%build
export RUSTFLAGS="%build_rustflags"
%{meson}
%{meson_build}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%if 0%{?rhel}
%cargo_vendor_manifest
%endif


%install
%{meson_install}


%files
%license LICENSE-APACHE LICENSE-MIT LICENSE.crosvm
%license LICENSE.dependencies
%if 0%{?rhel}
%license cargo-vendor.txt
%endif
%doc README.rst
%{_libdir}/libblkio.so.1{,.*}


%files devel
%license LICENSE-APACHE LICENSE-MIT LICENSE.crosvm
%doc README.rst
%{_includedir}/blkio.h
%{_libdir}/libblkio.so
%{_libdir}/pkgconfig/blkio.pc
%{_mandir}/man3/blkio.3*


%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 8 2024 Stefan Hajnoczi <stefanha@redhat.com> - 1.5.0-1
- Update to 1.5.0

* Fri Feb 02 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.3.0-6
- Update Rust macro usage

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 02 2023 Alberto Faria <afaria@redhat.com> - 1.3.0-3
- Update overall license

* Mon Aug 14 2023 Richard W.M. Jones <rjones@redhat.com> - 1.3.0-2
- Remove const-cstr dependency (RHBZ#2214208)

* Thu Jul 20 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 19 2023 Stefan Hajnoczi <stefanha@redhat.com> - 1.2.2-5
- Patch Cargo.toml files to enable nix "ioctl" feature (RHBZ#2186159)

* Thu Mar 09 2023 Stefan Hajnoczi <stefanha@redhat.com> - 1.2.2-4
- Update overall license to include crate dependency licenses

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 1.2.2-3
- Rebuild for fixed frame pointer compiler flags in Rust RPM macros.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-1
- Initial package
