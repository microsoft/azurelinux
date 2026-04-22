## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 10;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without check
%global udevdir %(pkg-config --variable=udevdir udev)
%global cargo_install_lib 0
%global crate udev-hid-bpf
%global _firmware /usr/lib/firmware

%if 0%{?rhel}
%global bundled_rust_deps 1
%global build_testing 0
%global build_tracing 1
%else
%global bundled_rust_deps 0
%global build_testing 1
%endif

# Fedora 42 never shipped a kernel 6.12 so no need for our tracing sources
%if 0%{?fedora} >= 42
%global build_tracing "false"
%else
%global build_tracing "true"
%endif

# Upstream uses 1.0.0-20240417 but rpm won't let us use the dash, so let's use a dot instead.
%global upstream_version 2.1.0
%global upstream_version_date 20240704
%global tarball %{upstream_version}-%{upstream_version_date}

Name:           udev-hid-bpf
Version:        %{upstream_version}.%{upstream_version_date}
Release:        %autorelease
Summary:        HID-BPF quirk loader tool

SourceLicense:  GPL-2.0-only
License:        (MIT OR Apache-2.0) AND Unicode-DFS-2016 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND BSD-2-Clause AND (BSD-3-Clause OR MIT OR Apache-2.0) AND GPL-2.0-only AND (LGPL-2.1-only OR BSD-2-Clause) AND MIT AND (MIT OR Apache-2.0) AND (Unlicense OR MIT)
URL:            https://gitlab.freedesktop.org/libevdev/udev-hid-bpf/
Source0:        https://gitlab.freedesktop.org/libevdev/%{name}/-/archive/%{tarball}/%{name}-%{tarball}.tar.bz2
# To recreate tarball:
# $ centpkg prep (do not use fedpkg, it removes Cargo.lock)
# $ pushd udev-hid-bpf-...; cargo vendor && tar Jcvf ../$(basename $PWD)-vendor.tar.xz vendor/ ; popd
Source1:        %{name}-%{upstream_version}-%{upstream_version_date}-vendor.tar.xz

Patch01:        0001-Bump-the-cargo-test-timeout-to-500s.patch
Patch02:        0001-meson.build-pass-the-target-dir-as-arg-instead-of-an.patch
Patch03:        0001-meson.build-swap-buildtype-check-to-detect-debug-bui.patch
Patch04:        0001-Add-Cargo.lock-to-git.patch

%if 0%{?rhel}
BuildRequires:  rust-toolset
%else
BuildRequires:  cargo-rpm-macros >= 26
%endif
BuildRequires:  systemd-rpm-macros
BuildRequires:  python3-rpm-macros
BuildRequires:  meson cargo
BuildRequires:  pkgconfig(udev)
BuildRequires:  clang
BuildRequires:  git
BuildRequires:  pkgconfig(libbpf) bpftool
BuildRequires:  pkgconfig(libudev)

Requires:       systemd-udev
Requires:       %{name}-stable%{?_isa} = %{version}-%{release}

# We don't have bpftool (#2294345)
ExcludeArch:    %{ix86}

%description
%{name} is a loader for HID eBPF programs aimed
at making it simple to develop and test eBPF programs
for HID devices.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries
and header files for developing applications
that use %{name}.

%if 0%{?build_testing}
%package        testing
Summary:        Testing eBPF programs for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    testing
The %{name}-testing package contains HID eBPF programs
for %{name} that have not yet been merged into
an upstream kernel.
%endif

%package        stable
Summary:        Stable eBPF programs for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    stable
The %{name}-stable package contains HID eBPF programs
for %{name} that have been merged into
an upstream kernel.

%prep
%autosetup -S git -p1 -n %{name}-%{tarball}
%py3_shebang_fix $(git grep -l  '#!/usr/bin/.*python3')

# Real build system is meson but upstream makes
# sure cargo on its own works too so this is safe to call here
%if 0%{?bundled_rust_deps}
tar xf %{SOURCE1}
%cargo_prep -v vendor
%else
%cargo_prep
%endif

%if ! 0%{?bundled_rust_deps}
%generate_buildrequires
%cargo_generate_buildrequires
%endif

%build
export RUSTFLAGS="%build_rustflags"
%if 0%{?build_testing}
%global bpf_set stable,testing
%else
%global bpf_set stable
%endif

%meson -Dudevdir=%{udevdir} \
       -Dbpfs=%{bpf_set} \
       -Dbpf-tracing=%{build_tracing} \
       -Dtests=disabled \
%meson_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%if 0%{?bundled_rust_deps}
%cargo_vendor_manifest
%endif

%install
%meson_install

%if %{with check}
%check
%meson_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%if 0%{?bundled_rust_deps}
%license cargo-vendor.txt
%endif
%doc README.md
%{_bindir}/udev-hid-bpf
%{_mandir}/man1/udev-hid-bpf.1*
%{udevdir}/rules.d/81-hid-bpf.rules
%dir /usr/lib/firmware/hid/bpf
%dir /usr/lib/firmware/hid/

%files stable
%license LICENSE
%license LICENSE.dependencies
%{_udevhwdbdir}/81-hid-bpf-stable.hwdb
%{_firmware}/hid/bpf/*-FR-TEC__Raptor-Mach-2.bpf.o
%{_firmware}/hid/bpf/*-HP__Elite-Presenter.bpf.o
%{_firmware}/hid/bpf/*-Huion__Kamvas-Pro-19.bpf.o
%{_firmware}/hid/bpf/*-IOGEAR__Kaliber-MMOmentum.bpf.o
%{_firmware}/hid/bpf/*-Microsoft__Xbox-Elite-2.bpf.o
%{_firmware}/hid/bpf/*-Wacom__ArtPen.bpf.o
%{_firmware}/hid/bpf/*-XPPen__Artist24.bpf.o
%{_firmware}/hid/bpf/*-XPPen__ArtistPro16Gen2.bpf.o
%{_firmware}/hid/bpf/*-Huion__Inspiroy-2-S.bpf.o
%{_firmware}/hid/bpf/*-Huion__Dial-2.bpf.o
%{_firmware}/hid/bpf/*-XPPen__DecoMini4.bpf.o
%{_firmware}/hid/bpf/*-Thrustmaster__TCA-Yoke-Boeing.bpf.o

%if 0%{?build_testing}
%files testing
%license LICENSE
%license LICENSE.dependencies
%{_udevhwdbdir}/81-hid-bpf-testing.hwdb
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.1.0.20240704-10
- Latest state for udev-hid-bpf

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0.20240704-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0.20240704-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 09 2024 Peter Hutterer <peter.hutterer@who-t.net> - 2.1.0.20240704-7
- Don't build the tracing BPFs on F42 - they're not needed

* Mon Jul 22 2024 Peter Hutterer <peter.hutterer@who-t.net> - 2.1.0.20240704-6
- Disable udev-hid-bpf-testing on Centos/RHEL

* Mon Jul 22 2024 Peter Hutterer <peter.hutterer@who-t.net> - 2.1.0.20240704-5
- Hide the /usr/lib/firmware install path behind a variable

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0.20240704-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Peter Hutterer <peter.hutterer@who-t.net> - 2.1.0.20240704-3
- Update the vendored sources tarball

* Tue Jul 16 2024 Peter Hutterer <peter.hutterer@who-t.net> - 2.1.0.20240704-2
- Add the required bits for dependency bundling on RHEL

* Fri Jul 12 2024 Peter Hutterer <peter.hutterer@who-t.net> - 2.1.0.20240704-1
- udev-hid-bpf 2.1.0-20240624

* Tue Jun 25 2024 Peter Hutterer <peter.hutterer@who-t.net> - 2.0.0.20240624-2
- Exclude i686 - we don't have bpftool

* Tue Jun 25 2024 Peter Hutterer <peter.hutterer@who-t.net> - 2.0.0.20240624-1
- udev-hid-bpf 2.0.0-20240625

* Tue May 21 2024 Peter Hutterer <peter.hutterer@who-t.net> - 1.0.1.20240515-1
- Update to 1.0.1-20240515

* Wed May 15 2024 Peter Hutterer <peter.hutterer@who-t.net> - 1.0.0.20240417-2
- Fix compilation error on i686 due to size_t mismatch

* Wed May 15 2024 Peter Hutterer <peter.hutterer@who-t.net> - 1.0.0.20240417-1
- Initial import (fedora#2275853)
## END: Generated by rpmautospec
