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

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/mesa.azl.macros}

%ifnarch s390x
%global with_hardware 1
%global with_kmsro 1
%global with_radeonsi 1
%global with_spirv_tools 1
%global with_vmware 1
%global with_vulkan_hw 1
%if !0%{?rhel}
%global with_r300 1
%global with_r600 1
%global with_opencl 1
%global with_va 1
%endif
%if !0%{?rhel} || 0%{?rhel} >= 9
%global with_nvk %{with_vulkan_hw}
%endif
%global base_vulkan %{?with_vulkan_hw:,amd}%{!?with_vulkan_hw:%{nil}}
%endif

%ifarch aarch64 x86_64
%if !0%{?rhel}
%global with_teflon 1
%endif
%endif

%ifarch %{ix86} x86_64
%global with_crocus 1
%global with_iris   1
%global intel_platform_vulkan %{?with_vulkan_hw:,intel,intel_hasvk}%{!?with_vulkan_hw:%{nil}}
%if !0%{?rhel}
%global with_i915   1
%endif
%endif
%ifarch x86_64
%if 0%{?with_vulkan_hw}
%global with_intel_vk_rt 1
%endif
%endif

%ifarch aarch64 x86_64 %{ix86}
%if !0%{?rhel}
%global with_asahi     1
%global with_d3d12     1
%global with_etnaviv   1
%global with_lima      1
%global with_tegra     1
%global with_vc4       1
%global with_v3d       1
%endif
%global with_freedreno 1
%global with_panfrost  1
%if 0%{?with_asahi}
%global asahi_platform_vulkan %{?with_vulkan_hw:,asahi}%{!?with_vulkan_hw:%{nil}}
%endif
%global extra_platform_vulkan %{?with_vulkan_hw:,broadcom,freedreno,panfrost,imagination}%{!?with_vulkan_hw:%{nil}}
%endif

%if !0%{?rhel}
%global with_libunwind 1
%global with_lmsensors 1
%global with_virtio    1
%endif

%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

%global vulkan_drivers swrast%{?base_vulkan}%{?intel_platform_vulkan}%{?asahi_platform_vulkan}%{?extra_platform_vulkan}%{?with_nvk:,nouveau}%{?with_virtio:,virtio}%{?with_d3d12:,microsoft-experimental}

%if 0%{?with_nvk} && 0%{?rhel}
%global vendor_nvk_crates 1
%endif

# We've gotten a report that enabling LTO for mesa breaks some games. See
# https://bugzilla.redhat.com/show_bug.cgi?id=1862771 for details.
# Disable LTO for now
%global _lto_cflags %nil

Name:           mesa
Summary:        Mesa graphics libraries
Version:        25.3.6
Release:        %autorelease
License:        MIT AND BSD-3-Clause AND SGI-B-2.0
URL:            https://mesa3d.org

# The "Version" field for release candidates has the format: A.B.C~rcX
# However, the tarball has the format: A.B.C-rcX.
# The "ver" variable contains the version in the second format.
%global ver %{gsub %version ~ -}

Source0:        https://archive.mesa3d.org/mesa-%{ver}.tar.xz
# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source1 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source1:        Mesa-MLAA-License-Clarification-Email.txt

# In CentOS/RHEL, Rust crates required to build NVK are vendored.
# The minimum target versions are obtained from the .wrap files
# https://gitlab.freedesktop.org/mesa/mesa/-/tree/main/subprojects
# but we generally want the latest compatible versions
%global rust_paste_ver 1.0.15
%global rust_proc_macro2_ver 1.0.101
%global rust_quote_ver 1.0.40
%global rust_syn_ver 2.0.106
%global rust_unicode_ident_ver 1.0.18
%global rustc_hash_ver 2.1.1
Source10:       https://crates.io/api/v1/crates/paste/%{rust_paste_ver}/download#/paste-%{rust_paste_ver}.tar.gz
Source11:       https://crates.io/api/v1/crates/proc-macro2/%{rust_proc_macro2_ver}/download#/proc-macro2-%{rust_proc_macro2_ver}.tar.gz
Source12:       https://crates.io/api/v1/crates/quote/%{rust_quote_ver}/download#/quote-%{rust_quote_ver}.tar.gz
Source13:       https://crates.io/api/v1/crates/syn/%{rust_syn_ver}/download#/syn-%{rust_syn_ver}.tar.gz
Source14:       https://crates.io/api/v1/crates/unicode-ident/%{rust_unicode_ident_ver}/download#/unicode-ident-%{rust_unicode_ident_ver}.tar.gz
Source15:       https://crates.io/api/v1/crates/rustc-hash/%{rustc_hash_ver}/download#/rustc-hash-%{rustc_hash_ver}.tar.gz
Source9999: mesa.azl.macros


BuildRequires:  meson >= 1.3.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
%if 0%{?with_hardware}
BuildRequires:  kernel-headers
BuildRequires:  systemd-devel
%endif
# We only check for the minimum version of pkgconfig(libdrm) needed so that the
# SRPMs for each arch still have the same build dependencies. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1859515
BuildRequires:  pkgconfig(libdrm) >= 2.4.122
%if 0%{?with_libunwind}
BuildRequires:  pkgconfig(libunwind)
%endif
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.34
BuildRequires:  pkgconfig(wayland-client) >= 1.11
BuildRequires:  pkgconfig(wayland-server) >= 1.11
BuildRequires:  pkgconfig(wayland-egl-backend) >= 3
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xdamage) >= 1.1
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb-dri2) >= 1.8
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-sync)
BuildRequires:  pkgconfig(xshmfence) >= 1.1
BuildRequires:  pkgconfig(dri2proto) >= 2.8
BuildRequires:  pkgconfig(glproto) >= 1.4.14
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:  pkgconfig(xrandr) >= 1.3
BuildRequires:  bison
BuildRequires:  flex
%if 0%{?with_lmsensors}
BuildRequires:  lm_sensors-devel
%endif
%if 0%{?with_va}
BuildRequires:  pkgconfig(libva) >= 0.38.0
%endif
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(libglvnd) >= 1.3.2
BuildRequires:  llvm-devel >= 7.0.0
%if 0%{?with_teflon}
BuildRequires:  flatbuffers-devel
BuildRequires:  flatbuffers-compiler
BuildRequires:  xtensor-devel
%endif
%if 0%{?with_opencl} || 0%{?with_nvk} || 0%{?with_asahi} || 0%{?with_panfrost}
BuildRequires:  clang-devel
BuildRequires:  pkgconfig(libclc)
BuildRequires:  pkgconfig(SPIRV-Tools)
BuildRequires:  pkgconfig(LLVMSPIRVLib)
%endif
%if 0%{?with_opencl} || 0%{?with_nvk}
BuildRequires:  bindgen
%if 0%{?rhel}
%else
BuildRequires:  cargo-rpm-macros
%endif
%endif
%if 0%{?with_nvk}
BuildRequires:  cbindgen
%endif
%if %{with valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  python3-pycparser
BuildRequires:  python3-pyyaml
BuildRequires:  vulkan-headers
BuildRequires:  glslang
%if 0%{?with_vulkan_hw}
BuildRequires:  pkgconfig(vulkan)
%endif
%if 0%{?with_d3d12}
BuildRequires:  pkgconfig(DirectX-Headers) >= 1.618.1
%endif

BuildRequires: cargo-rpm-macros
%description
%{summary}.

%package filesystem
Summary:        Mesa driver filesystem
Provides:       mesa-dri-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-omx-drivers < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-libd3d < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-libd3d-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-vdpau-drivers < %{?epoch:%{epoch}:}%{version}-%{release}

%description filesystem
%{summary}.

%package libGL
Summary:        Mesa libGL runtime libraries
Requires:       libglvnd-glx%{?_isa} >= 1:1.3.2
Requires:       %{name}-dri-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libOSMesa < 25.1.0~rc2-1

%description libGL
%{summary}.

%package libGL-devel
Summary:        Mesa libGL development package
Requires:       (%{name}-libGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} if %{name}-libGL%{?_isa})
Requires:       libglvnd-devel%{?_isa} >= 1:1.3.2
Provides:       libGL-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libGL-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Recommends:     gl-manpages
Obsoletes:      %{name}-libOSMesa-devel < 25.1.0~rc2-1

%description libGL-devel
%{summary}.

%package libEGL
Summary:        Mesa libEGL runtime libraries
Requires:       libglvnd-egl%{?_isa} >= 1:1.3.2
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-dri-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libEGL
%{summary}.

%package libEGL-devel
Summary:        Mesa libEGL development package
Requires:       (%{name}-libEGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} if %{name}-libEGL%{?_isa})
Requires:       libglvnd-devel%{?_isa} >= 1:1.3.2
Requires:       %{name}-khr-devel%{?_isa}
Provides:       libEGL-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libEGL-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libEGL-devel
%{summary}.

%package dri-drivers
Summary:        Mesa-based DRI drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{?with_va}
Recommends:     %{name}-va-drivers%{?_isa}
%endif
Obsoletes:      %{name}-libglapi < 25.0.0~rc2-1
Provides:       %{name}-libglapi >= 25.0.0~rc2-1

%description dri-drivers
%{summary}.

%if 0%{?with_va}
%package        va-drivers
Summary:        Mesa-based VA-API video acceleration drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-vaapi-drivers < 22.2.0-5

%description va-drivers
%{summary}.
%endif

%package libgbm
Summary:        Mesa gbm runtime library
Provides:       libgbm = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Recommends:     %{name}-dri-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# If mesa-dri-drivers are installed, they must match in version. This is here to prevent using
# older mesa-dri-drivers together with a newer mesa-libgbm and its dependants.
# See https://bugzilla.redhat.com/show_bug.cgi?id=2193135 .
Requires:       (%{name}-dri-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} if %{name}-dri-drivers%{?_isa})

%description libgbm
%{summary}.

%package libgbm-devel
Summary:        Mesa libgbm development package
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libgbm-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libgbm-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libgbm-devel
%{summary}.

%if 0%{?with_opencl}
%package libOpenCL
Summary:        Mesa OpenCL runtime library
Requires:       (ocl-icd%{?_isa} or OpenCL-ICD-Loader%{?_isa})
Requires:       libclc%{?_isa}
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       opencl-filesystem

%description libOpenCL
%{summary}.

%package libOpenCL-devel
Summary:        Mesa OpenCL development package
Requires:       %{name}-libOpenCL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libOpenCL-devel
%{summary}.
%endif

%if 0%{?with_teflon}
%package libTeflon
Summary:        Mesa TensorFlow Lite delegate

%description libTeflon
%{summary}.
%endif

%if 0%{?with_d3d12}
%package dxil-devel
Summary:        Mesa SPIR-V to DXIL binary
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description dxil-devel
Development tools for translating SPIR-V shader code to DXIL for Direct3D 12
%endif

%package vulkan-drivers
Summary:        Mesa Vulkan drivers
Requires:       vulkan%{_isa}
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-vulkan-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      VK_hdr_layer < 1

%description vulkan-drivers
The drivers with support for the Vulkan API.

%prep
%autosetup -n %{name}-%{ver} -p1
cp %{SOURCE1} docs/

# Extract Rust crates meson cache directory
%if 0%{?vendor_nvk_crates}
mkdir subprojects/packagecache/
tar -xvf %{SOURCE10} -C subprojects/packagecache/
tar -xvf %{SOURCE11} -C subprojects/packagecache/
tar -xvf %{SOURCE12} -C subprojects/packagecache/
tar -xvf %{SOURCE13} -C subprojects/packagecache/
tar -xvf %{SOURCE14} -C subprojects/packagecache/
tar -xvf %{SOURCE15} -C subprojects/packagecache/
for d in subprojects/packagecache/*-*; do
    echo '{"files":{}}' > $d/.cargo-checksum.json
done
%endif

%if 0%{?with_nvk}
cat > Cargo.toml <<_EOF
[package]
name = "mesa"
version = "%{ver}"
edition = "2021"

[lib]
path = "src/nouveau/nil/lib.rs"

# only direct dependencies need to be listed here
[dependencies]
paste = "$(grep ^directory subprojects/paste*.wrap | sed 's|.*-||')"
syn = { version = "$(grep ^directory subprojects/syn*.wrap | sed 's|.*-||')", features = ["clone-impls"] }
rustc-hash = "$(grep ^directory subprojects/rustc-hash*.wrap | sed 's|.*-||')"
_EOF
%if 0%{?vendor_nvk_crates}
%cargo_prep -v subprojects/packagecache
%else
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires
%endif
%endif


%build
# ensure standard Rust compiler flags are set
export RUSTFLAGS="%build_rustflags"

%if 0%{?with_nvk}
# So... Meson can't actually find them without tweaks
%if !0%{?vendor_nvk_crates}
export MESON_PACKAGE_CACHE_DIR="%{cargo_registry}/"
%endif

# This function rewrites a mesa .wrap file:
# - Removes the lines that start with "source"
# - Replaces the "directory =" with the MESON_PACKAGE_CACHE_DIR
#
# Example: An upstream .wrap file like this (proc-macro2-1-rs.wrap):
#
# [wrap-file]
# directory = proc-macro2-1.0.86
# source_url = https://crates.io/api/v1/crates/proc-macro2/1.0.86/download
# source_filename = proc-macro2-1.0.86.tar.gz
# source_hash = 5e719e8df665df0d1c8fbfd238015744736151d4445ec0836b8e628aae103b77
# patch_directory = proc-macro2-1-rs
#
# Will be transformed to:
#
# [wrap-file]
# directory = meson-package-cache-dir
# patch_directory = proc-macro2-1-rs
rewrite_wrap_file() {
  sed -e "/source.*/d" -e "s/^directory = ${1}-.*/directory = $(basename ${MESON_PACKAGE_CACHE_DIR:-subprojects/packagecache}/${1}-*)/" -i subprojects/${1}*.wrap
}

rewrite_wrap_file proc-macro2
rewrite_wrap_file quote
rewrite_wrap_file syn
rewrite_wrap_file unicode-ident
rewrite_wrap_file paste
rewrite_wrap_file rustc-hash
%endif

%meson \
  -Dplatforms=x11,wayland \
%if 0%{?with_hardware}
  -Dgallium-drivers=llvmpipe,virgl,nouveau%{?with_r300:,r300}%{?with_crocus:,crocus}%{?with_i915:,i915}%{?with_iris:,iris}%{?with_vmware:,svga}%{?with_radeonsi:,radeonsi}%{?with_r600:,r600}%{?with_asahi:,asahi}%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv}%{?with_tegra:,tegra}%{?with_vc4:,vc4}%{?with_v3d:,v3d}%{?with_lima:,lima}%{?with_panfrost:,panfrost}%{?with_vulkan_hw:,zink}%{?with_d3d12:,d3d12}%{?with_teflon:,ethosu,rocket} \
%else
  -Dgallium-drivers=llvmpipe,virgl \
%endif
  -Dgallium-va=%{?with_va:enabled}%{!?with_va:disabled} \
  -Dgallium-mediafoundation=disabled \
  -Dteflon=%{?with_teflon:true}%{!?with_teflon:false} \
%if 0%{?with_opencl}
  -Dgallium-rusticl=true \
%endif
  -Dvulkan-drivers=%{?vulkan_drivers} \
  -Dvulkan-layers=device-select \
  -Dgles1=enabled \
  -Dgles2=enabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=enabled \
  -Dglvnd=enabled \
  -Dintel-rt=%{?with_intel_vk_rt:enabled}%{!?with_intel_vk_rt:disabled} \
  -Dmicrosoft-clc=disabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled \
  -Dvalgrind=%{?with_valgrind:enabled}%{!?with_valgrind:disabled} \
  -Dbuild-tests=false \
%if !0%{?with_libunwind}
  -Dlibunwind=disabled \
%endif
%if !0%{?with_lmsensors}
  -Dlmsensors=disabled \
%endif
  -Dandroid-libbacktrace=disabled \
%ifarch %{ix86}
  -Dglx-read-only-text=true \
%endif
  -Dspirv-tools=%{?with_spirv_tools:enabled}%{!?with_spirv_tools:disabled} \
  %{nil}
%meson_build

%if 0%{?with_nvk}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%if 0%{?vendor_nvk_crates}
%cargo_vendor_manifest
%endif
%endif

%install
%meson_install

# likewise glvnd
rm -vf %{buildroot}%{_libdir}/libGLX_mesa.so
rm -vf %{buildroot}%{_libdir}/libEGL_mesa.so
# XXX can we just not build this
rm -vf %{buildroot}%{_libdir}/libGLES*

%if ! 0%{?with_asahi}
# This symlink is unconditionally created when any kmsro driver is enabled
# We don't want this one so delete it
rm -vf %{buildroot}%{_libdir}/dri/apple_dri.so
%endif

# glvnd needs a default provider for indirect rendering where it cannot
# determine the vendor
ln -s %{_libdir}/libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_system.so.0

%files filesystem
%doc docs/Mesa-MLAA-License-Clarification-Email.txt
%dir %{_libdir}/dri
%dir %{_datadir}/drirc.d

%files libGL
%{_libdir}/libGLX_mesa.so.0*
%{_libdir}/libGLX_system.so.0*
%files libGL-devel
%dir %{_includedir}/GL
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc

%files libEGL
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libEGL_mesa.so.0*
%files libEGL-devel
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext_angle.h
%{_includedir}/EGL/eglmesaext.h

%files libgbm
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*
%files libgbm-devel
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_includedir}/gbm_backend_abi.h
%{_libdir}/pkgconfig/gbm.pc

%if 0%{?with_teflon}
%files libTeflon
%{_libdir}/libteflon.so
%endif

%if 0%{?with_opencl}
%files libOpenCL
%{_libdir}/libRusticlOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/rusticl.icd

%files libOpenCL-devel
%{_libdir}/libRusticlOpenCL.so
%endif

%files dri-drivers
%{_datadir}/drirc.d/00-mesa-defaults.conf
%{_libdir}/libgallium-*.so
%{_libdir}/gbm/dri_gbm.so
%{_libdir}/dri/kms_swrast_dri.so
%{_libdir}/dri/libdril_dri.so
%{_libdir}/dri/swrast_dri.so
%{_libdir}/dri/virtio_gpu_dri.so

%if 0%{?with_hardware}
%if 0%{?with_r300}
%{_libdir}/dri/r300_dri.so
%endif
%if 0%{?with_radeonsi}
%if 0%{?with_r600}
%{_libdir}/dri/r600_dri.so
%endif
%{_libdir}/dri/radeonsi_dri.so
%endif
%ifarch %{ix86} x86_64
%{_libdir}/dri/crocus_dri.so
%{_libdir}/dri/iris_dri.so
%if 0%{?with_i915}
%{_libdir}/dri/i915_dri.so
%endif
%endif
%ifnarch s390x
%if 0%{?with_asahi}
%{_libdir}/dri/apple_dri.so
%{_libdir}/dri/asahi_dri.so
%endif
%if 0%{?with_d3d12}
%{_libdir}/dri/d3d12_dri.so
%endif
%{_libdir}/dri/ingenic-drm_dri.so
%{_libdir}/dri/imx-drm_dri.so
%{_libdir}/dri/imx-lcdif_dri.so
%{_libdir}/dri/kirin_dri.so
%{_libdir}/dri/komeda_dri.so
%{_libdir}/dri/mali-dp_dri.so
%{_libdir}/dri/mcde_dri.so
%{_libdir}/dri/mxsfb-drm_dri.so
%{_libdir}/dri/rcar-du_dri.so
%{_libdir}/dri/stm_dri.so
%endif
%if 0%{?with_vc4}
%{_libdir}/dri/vc4_dri.so
%endif
%if 0%{?with_v3d}
%{_libdir}/dri/v3d_dri.so
%endif
%if 0%{?with_freedreno}
%{_libdir}/dri/kgsl_dri.so
%{_libdir}/dri/msm_dri.so
%endif
%if 0%{?with_etnaviv}
%{_libdir}/dri/etnaviv_dri.so
%endif
%if 0%{?with_tegra}
%{_libdir}/dri/tegra_dri.so
%endif
%if 0%{?with_lima}
%{_libdir}/dri/lima_dri.so
%endif
%if 0%{?with_panfrost}
%{_libdir}/dri/panfrost_dri.so
%{_libdir}/dri/panthor_dri.so
%endif
%{_libdir}/dri/nouveau_dri.so
%if 0%{?with_vmware}
%{_libdir}/dri/vmwgfx_dri.so
%endif
%endif
%if 0%{?with_kmsro}
%{_libdir}/dri/armada-drm_dri.so
%{_libdir}/dri/exynos_dri.so
%{_libdir}/dri/gm12u320_dri.so
%{_libdir}/dri/hdlcd_dri.so
%{_libdir}/dri/hx8357d_dri.so
%{_libdir}/dri/ili9163_dri.so
%{_libdir}/dri/ili9225_dri.so
%{_libdir}/dri/ili9341_dri.so
%{_libdir}/dri/ili9486_dri.so
%{_libdir}/dri/imx-dcss_dri.so
%{_libdir}/dri/mediatek_dri.so
%{_libdir}/dri/meson_dri.so
%{_libdir}/dri/mi0283qt_dri.so
%{_libdir}/dri/panel-mipi-dbi_dri.so
%{_libdir}/dri/pl111_dri.so
%{_libdir}/dri/repaper_dri.so
%{_libdir}/dri/rockchip_dri.so
%{_libdir}/dri/rzg2l-du_dri.so
%{_libdir}/dri/ssd130x_dri.so
%{_libdir}/dri/st7586_dri.so
%{_libdir}/dri/st7735r_dri.so
%{_libdir}/dri/sti_dri.so
%{_libdir}/dri/sun4i-drm_dri.so
%{_libdir}/dri/udl_dri.so
%{_libdir}/dri/vkms_dri.so
%{_libdir}/dri/zynqmp-dpsub_dri.so
%endif
%if 0%{?with_vulkan_hw}
%{_libdir}/dri/zink_dri.so
%endif

%if 0%{?with_va}
%files va-drivers
%{_libdir}/dri/nouveau_drv_video.so
%if 0%{?with_r600}
%{_libdir}/dri/r600_drv_video.so
%endif
%if 0%{?with_radeonsi}
%{_libdir}/dri/radeonsi_drv_video.so
%endif
%if 0%{?with_d3d12}
%{_libdir}/dri/d3d12_drv_video.so
%endif
%{_libdir}/dri/virtio_gpu_drv_video.so
%endif

%if 0%{?with_d3d12}
%files dxil-devel
%{_bindir}/spirv2dxil
%{_libdir}/libspirv_to_dxil.a
%{_libdir}/libspirv_to_dxil.so
%endif

%files vulkan-drivers
%if 0%{?with_nvk}
%license LICENSE.dependencies
%if 0%{?vendor_nvk_crates}
%license cargo-vendor.txt
%endif
%endif
%{_libdir}/libvulkan_lvp.so
%{_datadir}/vulkan/icd.d/lvp_icd.*.json
%{_libdir}/libVkLayer_MESA_device_select.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_MESA_device_select.json
%if 0%{?with_virtio}
%{_libdir}/libvulkan_virtio.so
%{_datadir}/vulkan/icd.d/virtio_icd.*.json
%endif
%if 0%{?with_vulkan_hw}
%{_libdir}/libvulkan_radeon.so
%{_datadir}/drirc.d/00-radv-defaults.conf
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%if 0%{?with_nvk}
%{_libdir}/libvulkan_nouveau.so
%{_datadir}/vulkan/icd.d/nouveau_icd.*.json
%endif
%if 0%{?with_d3d12}
%{_libdir}/libvulkan_dzn.so
%{_datadir}/vulkan/icd.d/dzn_icd.*.json
%endif
%ifarch %{ix86} x86_64
%{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%{_libdir}/libvulkan_intel_hasvk.so
%{_datadir}/vulkan/icd.d/intel_hasvk_icd.*.json
%endif
%ifarch aarch64 x86_64 %{ix86}
%if 0%{?with_asahi}
%{_libdir}/libvulkan_asahi.so
%{_datadir}/vulkan/icd.d/asahi_icd.*.json
%endif
%{_libdir}/libvulkan_broadcom.so
%{_datadir}/vulkan/icd.d/broadcom_icd.*.json
%{_libdir}/libvulkan_freedreno.so
%{_datadir}/vulkan/icd.d/freedreno_icd.*.json
%{_libdir}/libvulkan_panfrost.so
%{_datadir}/vulkan/icd.d/panfrost_icd.*.json
%{_libdir}/libvulkan_powervr_mesa.so
%{_datadir}/vulkan/icd.d/powervr_mesa_icd.*.json
%endif
%endif

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 25.3.6-2
- test: add initial lock files

* Mon Feb 23 2026 José Expósito <jexposit@redhat.com> - 25.3.6-1
- Merge branch 'f44' into f43

* Thu Feb 12 2026 Peter Robinson <pbrobinson@gmail.com> - 25.3.5-1
- Update to 25.3.5

* Wed Feb 11 2026 José Expósito <jexposit@redhat.com> - 25.3.4-5
- Merge branch 'f44' into f43

* Tue Feb 10 2026 José Expósito <jexposit@redhat.com> - 25.3.4-4
- Merge branch 'f44' into f43

* Wed Jan 28 2026 José Expósito <jexposit@redhat.com> - 25.3.4-3
- Merge branch 'rawhide' into f43

* Wed Jan 28 2026 José Expósito <jexposit@redhat.com> - 25.3.4-2
- Merge branch 'rawhide' into f43

* Tue Nov 18 2025 José Expósito <jexposit@redhat.com> - 25.3.0-2
- Disable LTO globally

* Mon Nov 17 2025 José Expósito <jose.exposito@redhat.com> - 25.3.0-1
- Update to 25.3.0

* Sat Nov 15 2025 Janne Grunau <j@jannau.net> - 25.2.7-1
- Update to 25.2.7

* Tue Nov 11 2025 Mika Penttilä <mika.penttila@redhat.com> - 25.2.6-6
- Enable NVK in RHEL9 also

* Fri Nov 07 2025 Dave Airlie <airlied@redhat.com> - 25.2.6-5
- upstream review: fix bugs in the thread/zink patches

* Fri Nov 07 2025 Dave Airlie <airlied@redhat.com> - 25.2.6-4
- fix device-select patches bug

* Fri Nov 07 2025 Dave Airlie <airlied@redhat.com> - 25.2.6-3
- fix rawhide build problems

* Fri Nov 07 2025 Dave Airlie <airlied@redhat.com> - 25.2.6-2
- fix zink/device-select probing better.

* Tue Nov 04 2025 José Expósito <jexposit@redhat.com> - 25.2.6-1
- Update to 25.2.6

* Tue Oct 21 2025 Dave Airlie <airlied@redhat.com> - 25.2.5-2
- fix hangs with zink/nvk/mutter output hotplug

* Thu Oct 16 2025 Peter Robinson <pbrobinson@gmail.com> - 25.2.5-1
- Update to 25.2.5

* Mon Oct 13 2025 Robert Mader <robert.mader@collabora.com> - 25.2.4-3
- Drop gnome-shell glthread patch

* Fri Oct 03 2025 Peter Robinson <pbrobinson@gmail.com> - 25.2.4-2
- Drop VDPAU support

* Wed Oct 01 2025 Peter Robinson <pbrobinson@gmail.com> - 25.2.4-1
- Update to 25.2.4

* Mon Sep 22 2025 Mika Penttilä <mika.penttila@redhat.com> - 25.2.3-1
- Update to 25.2.3

* Mon Sep 15 2025 Peter Robinson <pbrobinson@gmail.com> - 25.2.2-5
- Don't obsolete libxatracker, provided by compat

* Wed Sep 10 2025 Peter Robinson <pbrobinson@gmail.com> - 25.2.2-4
- Add udev requirement for hardware support

* Mon Sep 08 2025 Kyle Gospodnetich <me@kylegospodneti.ch> - 25.2.2-3
- Add support for hardware acceleration under WSL

* Thu Sep 04 2025 Peter Robinson <pbrobinson@gmail.com> - 25.2.2-2
- Remove deprecated XA/Direct3D9/IntelCL state trackers

* Thu Sep 04 2025 Peter Robinson <pbrobinson@gmail.com> - 25.2.2-1
- Update to 25.2.2

* Wed Aug 27 2025 Anusha Srivatsa <asrivats@redhat.com> - 25.2.1-1
- Update to v25.2.1

* Wed Aug 20 2025 José Expósito <jexposit@redhat.com> - 25.1.4-4
- Enable NVK in CentOS 10 and RHEL 10.2

* Mon Aug 18 2025 José Expósito <jexposit@redhat.com> - 25.1.4-3
- Disable NVK in RHEL

* Wed Aug 13 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 25.1.4-2
- Enable NVK in RHEL

* Mon Aug 11 2025 Anusha Srivatsa <asrivats@redhat.com> - 25.1.4-1
- Revert "Update to v25.2.0"

* Thu Aug 07 2025 Anusha Srivatsa <asrivats@redhat.com> - 25.2.0-1
- Update to v25.2.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 19 2025 José Expósito <jexposit@redhat.com> - 25.1.4-1
- Update to 25.1.4

* Thu Jun 19 2025 José Expósito <jexposit@redhat.com> - 25.1.3-7
- Guard virtio in RHEL

* Thu Jun 19 2025 José Expósito <jexposit@redhat.com> - 25.1.3-6
- Sort drivers alphabetically

* Thu Jun 19 2025 José Expósito <jexposit@redhat.com> - 25.1.3-5
- Guard v3d in RHEL

* Thu Jun 19 2025 José Expósito <jexposit@redhat.com> - 25.1.3-4
- Guard i915 in RHEL

* Thu Jun 19 2025 José Expósito <jexposit@redhat.com> - 25.1.3-3
- Add missing provides for libglapi

* Thu Jun 12 2025 Nicolas Chauvet <kwizart@gmail.com> - 25.1.3-2
- Add support for d3d12 in WSL2

* Mon Jun 09 2025 Dave Airlie <airlied@redhat.com> - 25.1.3-1
- Update to 25.1.3

* Thu May 29 2025 Peter Robinson <pbrobinson@gmail.com> - 25.1.1-1
- Update to 25.1.1

* Sun May 11 2025 Peter Robinson <pbrobinson@gmail.com> - 25.1.0-3
- Disable clover

* Fri May 09 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 25.1.0-2
- Enable libclc dependency for panfrost

* Thu May 08 2025 Neal Gompa <ngompa@fedoraproject.org> - 25.1.0-1
- Update to 25.1.0

* Thu May 08 2025 Neal Gompa <ngompa@fedoraproject.org> - 25.1.0~rc2-5
- Fix failure for Asahi disabled in RHEL builds

* Tue Apr 29 2025 Abdiel Janulgue <abdiel@redhat.com> - 25.1.0~rc2-4
- Disable asahi in RHEL builds

* Fri Apr 25 2025 Neal Gompa <ngompa@fedoraproject.org> - 25.1.0~rc2-3
- Fix versioned Obsoletes for mesa-libOSMesa subpackages

* Wed Apr 23 2025 Neal Gompa <ngompa@fedoraproject.org> - 25.1.0~rc2-2
- Enable the Asahi Mesa drivers

* Wed Apr 23 2025 Neal Gompa <ngompa@fedoraproject.org> - 25.1.0~rc2-1
- Update to 25.1.0-rc2

* Mon Apr 21 2025 José Expósito <jexposit@redhat.com> - 25.0.4-1
- Update to 25.0.4

* Mon Apr 21 2025 José Expósito <jexposit@redhat.com> - 25.0.3-3
- Revert "kopper: Explicitly choose zink"

* Tue Apr 15 2025 Adam Jackson <ajax@fedoraproject.org> - 25.0.3-2
- Build only llvmpipe, not softpipe

* Thu Apr 03 2025 Abdiel Janulgue <abdiel@redhat.com> - 25.0.3-1
- Update to 25.0.3

* Thu Apr 03 2025 František Zatloukal <fzatlouk@redhat.com> - 25.0.2-3
- libOpenCL: Require ocl-icd or OpenCL-ICD-Loader (RHBZ#2332429)

* Wed Mar 26 2025 José Expósito <jexposit@redhat.com> - 25.0.2-2
- Backport "vulkan/wsi: implement the Wayland color management protocol"

* Thu Mar 20 2025 José Expósito <jexposit@redhat.com> - 25.0.2-1
- Update to 25.0.2

* Thu Mar 06 2025 Nikita Popov <npopov@redhat.com> - 25.0.1-2
- Rebuild for LLVM upgrade

* Thu Mar 06 2025 José Expósito <jexposit@redhat.com> - 25.0.1-1
- Update to 25.0.1

* Wed Feb 19 2025 José Expósito <jexposit@redhat.com> - 25.0.0-1
- Update to 25.0.0

* Tue Feb 18 2025 Dave Airlie <airlied@redhat.com> - 25.0.0~rc3-2
- fix vulkan/wsi/gtk4 interaction causing xfixes crash

* Wed Feb 12 2025 José Expósito <jexposit@redhat.com> - 25.0.0~rc3-1
- Update to 25.0.0-rc3

* Mon Feb 10 2025 José Expósito <jexposit@redhat.com> - 25.0.0~rc2-3
- Require mesa-dri-drivers from libGL and libEGL

* Fri Feb 07 2025 José Expósito <jexposit@redhat.com> - 25.0.0~rc2-2
- Obsolete package libglapi

* Thu Feb 06 2025 José Expósito <jexposit@redhat.com> - 25.0.0~rc2-1
- Update to 25.0.0-rc2

* Tue Feb 04 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 24.3.4-3
- Avoid devel-to-runtime dependencies in flatpak SDKs

* Wed Jan 29 2025 Björn Esser <besser82@fedoraproject.org> - 24.3.4-2
- radeonsi: disallow compute queues on Raven/Raven2 due to hangs

* Thu Jan 23 2025 José Expósito <jexposit@redhat.com> - 24.3.4-1
- Update to 24.3.4

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 24.3.3-2
- Move dri_gbm.so to mesa-dri-drivers

* Fri Jan 10 2025 José Expósito <jexposit@redhat.com> - 24.3.3-1
- Update to 24.3.3

* Fri Dec 20 2024 José Expósito <jexposit@redhat.com> - 24.3.2-1
- Update to 24.3.2

* Thu Dec 05 2024 José Expósito <jexposit@redhat.com> - 24.3.1-1
- Update to 24.3.1

* Thu Dec 05 2024 José Expósito <jexposit@redhat.com> - 24.3.0-3
- Revert "Move zink to vulkan drivers"

* Thu Nov 28 2024 Peter Robinson <pbrobinson@gmail.com> - 24.3.0-2
- Move zink to vulkan drivers

* Fri Nov 22 2024 José Expósito <jexposit@redhat.com> - 24.3.0-1
- Update to 24.3.0

* Wed Nov 20 2024 Dave Airlie <airlied@redhat.com> - 24.3.0~rc2-3
- silence some vulkan loader warnings on probe

* Mon Nov 18 2024 Nianqing Yao <imbearchild@outlook.com> - 24.3.0~rc2-2
- Add Virtio vulkan driver

* Thu Nov 14 2024 José Expósito <jexposit@redhat.com> - 24.3.0~rc2-1
- Update to 24.3.0-rc2

* Wed Nov 13 2024 José Expósito <jexposit@redhat.com> - 24.3.0~rc1-2
- Move dri_gbm.so to mesa-libgbm

* Tue Nov 12 2024 José Expósito <jexposit@redhat.com> - 24.3.0~rc1-1
- Update to 24.3.0-rc1

* Thu Oct 31 2024 José Expósito <jexposit@redhat.com> - 24.2.6-1
- Update to 24.2.6

* Sun Oct 27 2024 Peter Robinson <pbrobinson@gmail.com> - 24.2.5-1
- Update to 24.2.5

* Fri Oct 04 2024 Peter Robinson <pbrobinson@gmail.com> - 24.2.4-1
- Update to 24.2.$

* Tue Sep 24 2024 Nikita Popov <npopov@redhat.com> - 24.2.3-4
- Backport fix for LLVM 19 compatibility

* Fri Sep 20 2024 František Zatloukal <fzatlouk@redhat.com> - 24.2.3-3
- Rebuild for LLVM 19 Final

* Thu Sep 19 2024 Peter Robinson <pbrobinson@gmail.com> - 24.2.3-2
- Retire OpenMAX suppot

* Thu Sep 19 2024 José Expósito <jexposit@redhat.com> - 24.2.3-1
- Update to 24.2.3

* Fri Sep 13 2024 František Zatloukal <fzatlouk@redhat.com> - 24.2.2-3
- Rebuild for LLVM 19

* Sat Sep 07 2024 Peter Robinson <pbrobinson@gmail.com> - 24.2.2-2
- Fix up some directory ownerships

* Fri Sep 06 2024 José Expósito <jexposit@redhat.com> - 24.2.2-1
- Update to 24.2.2

* Thu Sep 05 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 24.2.1-7
- Fix ELN file listings

* Thu Sep 05 2024 Olivier Fourdan <ofourdan@redhat.com> - 24.2.1-6
- Fix missing configs with swrast

* Wed Sep 04 2024 Peter Robinson <pbrobinson@gmail.com> - 24.2.1-5
- v3d: v3d_resource Use LINEAR layout for importing with INVALID modifier

* Wed Sep 04 2024 José Expósito <jexposit@redhat.com> - 24.2.1-4
- Bump libdrm required version to 2.4.122

* Thu Aug 29 2024 Adam Jackson <ajax@redhat.com> - 24.2.1-3
- sync some rhel config changes

* Thu Aug 29 2024 José Expósito <jexposit@redhat.com> - 24.2.1-2
- Add zink_dri.so back

* Wed Aug 28 2024 Peter Robinson <pbrobinson@gmail.com> - 24.2.1-1
- Update to 24.2.1

* Wed Aug 21 2024 Janne Grunau <janne-fdr@jannau.net> - 24.2.0-2
- Build vulkan hw drivers only if `with_vulkan_hw` is true

* Mon Aug 19 2024 José Expósito <jexposit@redhat.com> - 24.2.0-1
- Update to 24.2.0

* Thu Aug 08 2024 José Expósito <jexposit@redhat.com> - 24.2.0~rc4-1
- Update to 24.2.0-rc4

* Thu Aug 01 2024 José Expósito <jexposit@redhat.com> - 24.2.0~rc3-1
- Update to 24.2.0-rc3

* Mon Jul 22 2024 José Expósito <jexposit@redhat.com> - 24.1.4-2
- Backport AV1 fix

* Thu Jul 18 2024 José Expósito <jexposit@redhat.com> - 24.1.4-1
- Update to 24.1.4

* Fri Jul 12 2024 José Expósito <jexposit@redhat.com> - 24.1.2-7
- Backport fix for Octave + llvmpipe

* Fri Jun 28 2024 José Expósito <jexposit@redhat.com> - 24.1.2-6
- Fix s390x patch conditional

* Fri Jun 28 2024 José Expósito <jexposit@redhat.com> - 24.1.2-5
- Fix GNOME and KDE crash with some AMD GPUs

* Fri Jun 28 2024 José Expósito <jexposit@redhat.com> - 24.1.2-4
- Fix mutter crash when calling eglQueryDmaBufModifiersEXT

* Fri Jun 28 2024 José Expósito <jexposit@redhat.com> - 24.1.2-3
- Add the s390x patch only for the s390x package

* Wed Jun 26 2024 Ray Strode <rstrode@redhat.com> - 24.1.2-2
- Fix egl on s390x

* Thu Jun 20 2024 José Expósito <jexposit@redhat.com> - 24.1.2-1
- Update to 24.1.2

* Fri Jun 14 2024 Dave Airlie <airlied@redhat.com> - 24.1.1-4
- add missing fix

* Fri Jun 14 2024 Dave Airlie <airlied@redhat.com> - 24.1.1-3
- add fix for llvmpipe dma-buf regression

* Thu Jun 06 2024 Dave Airlie <airlied@redhat.com> - 24.1.1-2
- fix an nvk bug when kernel modifiers aren't working yet

* Wed Jun 05 2024 Dave Airlie <airlied@redhat.com> - 24.1.1-1
- Update to 24.1.1

* Tue Jun 04 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 24.1.0-4
- Enable libclc in RHEL builds

* Tue Jun 04 2024 José Expósito <jexposit@redhat.com> - 24.1.0-3
- mesa 24.1.0 requires wayland-protocols >= 1.8

* Tue Jun 04 2024 José Expósito <jexposit@redhat.com> - 24.1.0-2
- mesa 24.1.0 requires libdrm >= 2.4.119

* Wed May 22 2024 Dave Airlie <airlied@redhat.com> - 24.1.0-1
- Update to 24.1.0

* Thu May 16 2024 José Expósito <jexposit@redhat.com> - 24.1.0~rc4-1
- Update to 24.1.0-rc4

* Thu May 09 2024 Peter Robinson <pbrobinson@gmail.com> - 24.1.0~rc3-4
- Fix Telfon sub package

* Thu May 09 2024 Peter Robinson <pbrobinson@gmail.com>
- Enable Teflon, the TensorFlow Lite delegate driver

* Thu May 09 2024 Dave Airlie <airlied@redhat.com> - 24.1.0~rc3-2
- rewrite paste as well

* Thu May 09 2024 Dave Airlie <airlied@redhat.com> - 24.1.0~rc3-1
- Update to 24.1.0-rc3

* Wed May 08 2024 Peter Robinson <pbrobinson@gmail.com> - 24.1.0~rc2-3
- Minor feature enable cleanups

* Mon May 06 2024 José Expósito <jexposit@redhat.com> - 24.1.0~rc2-2
- Disable intel-rt on non x86_64 architectures

* Mon May 06 2024 José Expósito <jexposit@redhat.com> - 24.1.0~rc2-1
- Update to 24.1.0-rc2

* Thu Apr 25 2024 Peter Robinson <pbrobinson@gmail.com> - 24.0.6-2
- Workaround rhbz#2277018 while awaiting upstream fix

* Thu Apr 25 2024 Peter Robinson <pbrobinson@gmail.com> - 24.0.6-1
- Update to 24.0.6

* Tue Apr 16 2024 José Expósito <jexposit@redhat.com> - 24.0.5-2
- Fix rendering issues using GTK's GSK_RENDERER=ngl on Raspberry Pi

* Thu Apr 11 2024 José Expósito <jexposit@redhat.com> - 24.0.5-1
- Update to 24.0.5

* Mon Apr 01 2024 José Expósito <jexposit@redhat.com> - 24.0.4-1
- Update to 24.0.4

* Thu Mar 28 2024 Adam Williamson <awilliam@redhat.com> - 24.0.3-3
- Backport MR #28414 to fix GTK 4 app rendering on rpi (#2269412)

* Tue Mar 19 2024 José Expósito <jexposit@redhat.com> - 24.0.3-2
- Backport fix for crash in radeon_bo_can_reclaim_slab

* Thu Mar 14 2024 José Expósito <jexposit@redhat.com> - 24.0.3-1
- Update to 24.0.3

* Mon Mar 11 2024 Nikita Popov <npopov@redhat.com> - 24.0.2-2
- Backport fix for LLVM 18 assertion failure (rhbz#2268800)

* Wed Mar 06 2024 José Expósito <jexposit@redhat.com> - 24.0.2-1
- Update to 24.0.2

* Tue Feb 27 2024 Neal Gompa <ngompa@fedoraproject.org> - 24.0.0-3
- Drop modprobe config file to enable GSP on Turing/Ampere NVIDIA GPUs

* Fri Feb 09 2024 Neal Gompa <ngompa@fedoraproject.org> - 24.0.0-2
- Add a modprobe config file to enable GSP on Turing and Ampere with NVK

* Thu Feb 01 2024 José Expósito <jexposit@redhat.com> - 24.0.0-1
- Update to 24.0.0

* Wed Jan 31 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 24.0.0~rc2-7
- Disable NVK for now in ELN builds

* Wed Jan 31 2024 José Expósito <jexposit@redhat.com> - 24.0.0~rc2-6
- Revert "Enable LTO"

* Fri Jan 26 2024 José Expósito <jexposit@redhat.com> - 24.0.0~rc2-5
- Enable LTO

* Thu Jan 25 2024 Neal Gompa <ngompa@fedoraproject.org> - 24.0.0~rc2-4
- Enable NVK to support the new Nouveau driver in Linux 6.7+

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.0.0~rc2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Javier Martinez Canillas <javierm@redhat.com> - 24.0.0~rc2-2
- Fix build due a clang bug on nested macros

* Fri Jan 19 2024 Javier Martinez Canillas <javierm@redhat.com> - 24.0.0~rc2-1
- Update to 24.0.0-rc2

* Tue Jan 16 2024 Javier Martinez Canillas <javierm@redhat.com> - 24.0.0~rc1-1
- Update to 24.0.0-rc1

* Thu Jan 11 2024 José Expósito <jexposit@redhat.com> - 23.3.3-1
- Update to 23.3.0

* Wed Jan 10 2024 Alessandro Astone <ales.astone@gmail.com> - 23.3.2-9
- Fix zink crash and re-enable the automatic fallback

* Mon Jan 08 2024 Florian Weimer <fweimer@redhat.com> - 23.3.2-8
- Fix C compatibility issue in Meson probe

* Mon Jan 08 2024 José Expósito <jexposit@redhat.com> - 23.3.2-7
- fix compiler backport

* Mon Jan 08 2024 José Expósito <jexposit@redhat.com> - 23.3.2-6
- Update patch "intel/compiler: reemit boolean resolve for inverted if on
  gen5"

* Wed Jan 03 2024 Alessandro Astone <ales.astone@gmail.com> - 23.3.2-5
- Disable zink fallback in EGL

* Wed Jan 03 2024 Dave Airlie <airlied@redhat.com> - 23.3.2-4
- fix compiler backport more

* Wed Jan 03 2024 Dave Airlie <airlied@redhat.com> - 23.3.2-3
- fix intel compiler change for 23.3

* Wed Jan 03 2024 Dave Airlie <airlied@redhat.com> - 23.3.2-2
- add fix for intel compiler unused variable in release builds

* Wed Jan 03 2024 Dave Airlie <airlied@redhat.com> - 23.3.2-1
- Update to 23.3.2 and better fix for gen5 intel.

* Thu Dec 21 2023 Dave Airlie <airlied@redhat.com> - 23.3.1-4
- Fix gtk4-demo regression on older Intel

* Mon Dec 18 2023 Dave Airlie <airlied@redhat.com> - 23.3.1-3
- fix a crocus regression in intel compiler for gtk4/gnome-shell

* Mon Dec 18 2023 Dave Airlie <airlied@redhat.com> - 23.3.1-2
- drop zink patch

* Mon Dec 18 2023 Dave Airlie <airlied@redhat.com> - 23.3.1-1
- Update to 23.3.1

* Thu Nov 30 2023 José Expósito <jexposit@redhat.com> - 23.3.0-1
- Update to 23.3.0

* Wed Nov 29 2023 José Expósito <jexposit@redhat.com> - 23.3.0~rc5-1
- Update to 23.3.0-rc5

* Thu Nov 23 2023 José Expósito <jexposit@redhat.com> - 23.3.0~rc2-6
- Set glx-read-only-text on i386

* Thu Nov 23 2023 José Expósito <jexposit@redhat.com> - 23.3.0~rc2-5
- Disable rwx segment linker error

* Wed Nov 22 2023 José Expósito <jexposit@redhat.com> - 23.3.0~rc2-4
- Backport MR #26332 to fix X11 session on VMs

* Fri Nov 17 2023 José Expósito <jexposit@redhat.com> - 23.3.0~rc2-3
- Backport MR #26220 to fix GNOME apps crash

* Fri Nov 03 2023 José Expósito <jexposit@redhat.com> - 23.3.0~rc2-2
- Backport MR #26029 to fix installer crash

* Thu Nov 02 2023 José Expósito <jexposit@redhat.com> - 23.3.0~rc2-1
- Update to 23.3.0-rc2

* Thu Oct 26 2023 José Expósito <jexposit@redhat.com> - 23.3.0~rc1-1
- Update to 23.3.0-rc1

* Thu Oct 05 2023 Adam Williamson <awilliam@redhat.com> - 23.2.1-2
- Backport MR #24045 to fix Iris crashes (#2238711)

* Fri Sep 29 2023 Pete Walter <pwalter@fedoraproject.org> - 23.2.1-1
- Update to 23.2.1

* Fri Sep 15 2023 Dave Airlie <airlied@redhat.com> - 23.2.0~rc3-3
- update SPDX license

* Thu Sep 07 2023 Adam Jackson <ajax@redhat.com> - 23.2.0~rc3-2
- Build a few more drivers for RHEL

* Wed Sep 06 2023 Pete Walter <pwalter@fedoraproject.org> - 23.2.0~rc3-1
- Update to 23.2.0-rc3

* Tue Aug 22 2023 Neal Gompa <ngompa@fedoraproject.org> - 23.2.0~rc2-4
- Enable GLESv1 support

* Mon Aug 14 2023 Neal Gompa <ngompa@fedoraproject.org> - 23.2.0~rc2-3
- Enable all aarch64 drivers for x86 for x86 emulation on aarch64

* Sat Aug 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 23.2.0~rc2-2
- Bump Meson minimum build dependency to 1.2.0

* Thu Aug 10 2023 Pete Walter <pwalter@fedoraproject.org> - 23.2.0~rc2-1
- Update to 23.2.0-rc2

* Thu Aug 03 2023 Pete Walter <pwalter@fedoraproject.org> - 23.1.5-1
- Update to 23.1.5

* Sat Jul 22 2023 Pete Walter <pwalter@fedoraproject.org> - 23.1.4-1
- Update to 23.1.4

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 23.1.3-3
- Disable libunwind, lm_sensors in RHEL builds

* Thu Jul 13 2023 Kamil Páral <kparal@redhat.com> - 23.1.3-2
- Prevent partial updates (rhbz#2193135)

* Fri Jun 30 2023 Nicolas Chauvet <kwizart@gmail.com> - 23.1.3-1
- Update to 23.1.3

* Sun Jun 11 2023 Pete Walter <pwalter@fedoraproject.org> - 23.1.2-1
- Update to 23.1.2

* Wed Jun 07 2023 Neal Gompa <ngompa@fedoraproject.org> - 23.1.1-2
- Enable stack trace and HUD sensor support

* Thu May 25 2023 Dave Airlie <airlied@redhat.com> - 23.1.1-1
- update to 23.1.1

* Tue May 23 2023 Dave Airlie <airlied@redhat.com> - 23.1.0-3
- removed unused BR

* Tue May 23 2023 Dave Airlie <airlied@redhat.com> - 23.1.0-2
- Update to mesa 23.1.0

* Tue May 23 2023 Dave Airlie <airlied@redhat.com> - 23.1.0-1
- Update to mesa 23.1.0

* Wed May 03 2023 Michel Dänzer <mdaenzer@redhat.com> - 23.0.3-4
- Do not enable intel-clc for ELN/RHEL

* Mon May 01 2023 Michel Dänzer <mdaenzer@redhat.com> - 23.0.3-3
- Enable intel-clc for ANV ray tracing support

* Fri Apr 28 2023 Michel Dänzer <mdaenzer@redhat.com> - 23.0.3-2
- Remove superfluous meson parameters for rusticl
- Dllvm=enabled is already there unconditionally further down.

* Tue Apr 25 2023 Pete Walter <pwalter@fedoraproject.org> - 23.0.3-1
- Update to 23.0.3

* Tue Apr 25 2023 Pete Walter <pwalter@fedoraproject.org> - 23.0.2-3
- Add missing inter-subpackage requires (rhbz#2187726)

* Tue Apr 18 2023 Nicolas Chauvet <kwizart@gmail.com> - 23.0.2-2
- Revert "Tighten mesa-va-drivers recommends again (rhbz#2161338)"

* Thu Apr 13 2023 Pete Walter <pwalter@fedoraproject.org> - 23.0.2-1
- Update to 23.0.2

* Thu Apr 13 2023 Pete Walter <pwalter@fedoraproject.org> - 23.0.1-3
- Tighten mesa-va-drivers recommends again (rhbz#2161338)

* Mon Apr 03 2023 František Zatloukal <fzatlouk@redhat.com> - 23.0.1-2
- Rebuild for LLVM 16

* Sat Mar 25 2023 Pete Walter <pwalter@fedoraproject.org> - 23.0.1-1
- Update to 23.0.1

* Thu Feb 23 2023 Pete Walter <pwalter@fedoraproject.org> - 23.0.0-1
- Update to 23.0.0

* Wed Feb 15 2023 Adam Williamson <awilliam@redhat.com> - 23.0.0~rc4-3
- Backport MR #21333 to fix KDE on llvmpipe (#2164667)

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 23.0.0~rc4-2
- Ensure standard Rust compiler flags are set

* Wed Feb 01 2023 Pete Walter <pwalter@fedoraproject.org> - 23.0.0~rc4-1
- Update to 23.0.0-rc4

* Thu Jan 26 2023 Adam Williamson <awilliam@redhat.com> - 23.0.0~rc3-3
- Backport MR #20933 to fix double-free crash (rhbz#2164667)

* Wed Jan 25 2023 Pete Walter <pwalter@fedoraproject.org> - 23.0.0~rc3-2
- Fix the build (rhbz#2161370)

* Wed Jan 25 2023 Pete Walter <pwalter@fedoraproject.org> - 23.0.0~rc3-1
- Update to 23.0.0-rc3

* Wed Jan 25 2023 Pete Walter <pwalter@fedoraproject.org> - 22.3.3-3
- Use unversioned recommends for mesa-va-drivers (rhbz#2161338)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Pete Walter <pwalter@fedoraproject.org> - 22.3.3-1
- Update to 22.3.3

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 22.3.2-1
- Update to 22.3.2

* Sun Dec 18 2022 Pete Walter <pwalter@fedoraproject.org> - 22.3.1-1
- Update to 22.3.1

* Tue Dec 06 2022 Dave Airlie <airlied@redhat.com> - 22.3.0-2
- fix regression around mit-shm detection

* Wed Nov 30 2022 Pete Walter <pwalter@fedoraproject.org> - 22.3.0-1
- Update to 22.3.0

* Fri Nov 25 2022 Dave Airlie <airlied@redhat.com> - 22.3.0~rc4-2
- disable glthread for gnome-shell

* Thu Nov 24 2022 Pete Walter <pwalter@fedoraproject.org> - 22.3.0~rc4-1
- Update to 22.3.0-rc4

* Tue Nov 22 2022 Dave Airlie <airlied@redhat.com> - 22.3.0~rc3-4
- add hasvk files

* Tue Nov 22 2022 Dave Airlie <airlied@redhat.com> - 22.3.0~rc3-3
- enable hasvk + regression fix

* Mon Nov 21 2022 Pete Walter <pwalter@fedoraproject.org> - 22.3.0~rc3-2
- Sort new files

* Mon Nov 21 2022 Dave Airlie <airlied@redhat.com> - 22.3.0~rc3-1
- rebase to 22.3.0-rc3

* Thu Nov 17 2022 Peter Robinson <pbrobinson@gmail.com> - 22.3.0~rc2-3
- Enable rusticl as an optional OpenCL engine

* Thu Nov 10 2022 Dave Airlie <airlied@redhat.com> - 22.3.0~rc2-2
- Add patch files

* Thu Nov 10 2022 Dave Airlie <airlied@redhat.com> - 22.3.0~rc2-1
- Update to 22.3.0-rc2

* Mon Nov 07 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.3-1
- Update to 22.2.3

* Wed Oct 19 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.2-1
- Update to 22.2.2

* Wed Oct 12 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.1-1
- Update to 22.2.1

* Mon Oct 10 2022 Ray Strode <rstrode@redhat.com> - 22.2.0-7
- Recommend mesa-va-drivers from mesa-dri-drivers

* Sun Oct 02 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.0-6
- Remove old obsoletes

* Sun Oct 02 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.0-5
- Rename mesa-vaapi-drivers to mesa-va-drivers

* Wed Sep 28 2022 Dave Airlie <airlied@redhat.com> - 22.2.0-4
- mesa: split out vaapi drivers into separate package

* Sun Sep 25 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.0-3
- Recommend mesa-dri-drivers from libGL, libEGL, and libgbm subpackages
  (rhbz#1900633)

* Thu Sep 22 2022 Karol Herbst <kherbst@redhat.com> - 22.2.0-2
- Add Nouveau multithreading fix backport (rhbz#2123274)

* Wed Sep 21 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.0-1
- Update to 22.2.0

* Tue Sep 20 2022 Dave Airlie <airlied@redhat.com> - 22.2.0~rc3-4
- Drop codecs.

* Sat Sep 17 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.0~rc3-3
- Rebuild for llvm 15

* Mon Sep 12 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.0~rc3-2
- Re-enable video codecs (rhbz#2123998)

* Thu Aug 18 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.0~rc3-1
- Update to 22.2.0-rc3

* Fri Aug 12 2022 Pete Walter <pwalter@fedoraproject.org> - 22.2.0~rc2-1
- Update to 22.2.0-rc2

* Fri Aug 12 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.6-2
- Drop obsolete arm ifarch conditionals

* Thu Aug 11 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.6-1
- Update to 22.1.6

* Thu Aug 04 2022 Dave Airlie <airlied@redhat.com> - 22.1.5-2
- add two llvmpipe fixes for multi-context

* Thu Aug 04 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.5-1
- Update to 22.1.5

* Thu Jul 21 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.4-2
- Enable vmware svga driver on aarch64 (#2108405)

* Wed Jul 20 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.4-1
- Update to 22.1.4

* Thu Jul 14 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.3-3
- Build i915 gallium driver (#2100212)

* Thu Jul 14 2022 Dave Airlie <airlied@redhat.com> - 22.1.3-2
- attempt to fix race in kms_swrast_dri.so affecting kwin.

* Sat Jul 02 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.3-1
- Update to 22.1.3

* Thu Jun 16 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.2-1
- Update to 22.1.2

* Thu Jun 02 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.1-1
- Update to 22.1.1

* Thu Jun 02 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.0-5
- Update Source0

* Thu May 26 2022 Dave Airlie <airlied@redhat.com> - 22.1.0-4
- fix spec file chunk

* Thu May 26 2022 Dave Airlie <airlied@redhat.com> - 22.1.0-3
- backport correct llvmpipe artifact fix

* Wed May 25 2022 Dave Airlie <airlied@redhat.com> - 22.1.0-2
- revert llvmpipe overlap patch to see if it fixes rawhide

* Thu May 19 2022 Pete Walter <pwalter@fedoraproject.org> - 22.1.0-1
- Update to 22.1.0

* Thu May 05 2022 Pete Walter <pwalter@fedoraproject.org> - 22.0.3-1
- Update to 22.0.3

* Mon Apr 25 2022 Pete Walter <pwalter@fedoraproject.org> - 22.0.2-2
- Add new 00-radv-defaults.conf to files list

* Sun Apr 24 2022 Pete Walter <pwalter@fedoraproject.org> - 22.0.2-1
- Update to 22.0.2

* Wed Mar 30 2022 Pete Walter <pwalter@fedoraproject.org> - 22.0.1-1
- Update to 22.0.1

* Mon Mar 21 2022 Pete Walter <pwalter@fedoraproject.org> - 22.0.0-4
- Obsolete empty mesa-vulkan-devel subpackage

* Mon Mar 21 2022 Pete Walter <pwalter@fedoraproject.org> - 22.0.0-3
- Fix the build

* Thu Mar 10 2022 Dave Airlie <airlied@redhat.com> - 22.0.0-2
- fixup unknown args

* Thu Mar 10 2022 Dave Airlie <airlied@redhat.com> - 22.0.0-1
- update to 22.0.0

* Wed Feb 23 2022 Pete Walter <pwalter@fedoraproject.org> - 21.3.7-1
- Update to 21.3.7

* Thu Feb 10 2022 Pete Walter <pwalter@fedoraproject.org> - 21.3.6-1
- Update to 21.3.6

* Mon Jan 31 2022 Lyude Paul <lyude@redhat.com> - 21.3.5-2
- Add missing attributions for 21.3.4-3

* Sat Jan 29 2022 Pete Walter <pwalter@fedoraproject.org> - 21.3.5-1
- Update to 21.3.5

* Fri Jan 21 2022 Lyude Paul <lyude@redhat.com> - 21.3.4-3
- Add patch from upstream to fix blinking with Intel Iris (#2040771)
  (#2036600)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Pete Walter <pwalter@fedoraproject.org> - 21.3.4-1
- Update to 21.3.4

* Thu Dec 30 2021 Pete Walter <pwalter@fedoraproject.org> - 21.3.3-1
- Update to 21.3.3

* Sat Dec 18 2021 Pete Walter <pwalter@fedoraproject.org> - 21.3.2-1
- Update to 21.3.2

* Mon Dec 06 2021 Pete Walter <pwalter@fedoraproject.org> - 21.3.1-2
- Patch from upstream to make GBM work again with NVIDIA 495 (#2028524)

* Wed Dec 01 2021 Pete Walter <pwalter@fedoraproject.org> - 21.3.1-1
- Update to 21.3.1

* Thu Nov 18 2021 Pete Walter <pwalter@fedoraproject.org> - 21.3.0-2
- Fix files list

* Wed Nov 17 2021 Pete Walter <pwalter@fedoraproject.org> - 21.3.0-1
- Update to 21.3.0

* Tue Nov 09 2021 Tom Stellard <tstellar@redhat.com> - 21.2.5-2
- Rebuild for llvm-13.0.0

* Thu Oct 28 2021 Pete Walter <pwalter@fedoraproject.org> - 21.2.5-1
- Update to 21.2.5

* Thu Oct 28 2021 Stephen Gallagher <sgallagh@redhat.com> - 21.2.4-3
- Rebuild for llvm 13 soname change

* Thu Oct 14 2021 Tom Stellard <tstellar@redhat.com> - 21.2.4-2
- Rebuild for llvm-13.0.0

* Thu Oct 14 2021 Pete Walter <pwalter@fedoraproject.org> - 21.2.4-1
- Update to 21.2.4

* Wed Oct 13 2021 Tom Stellard <tstellar@redhat.com> - 21.2.3-7
- Rebuild for llvm-13.0.0

* Tue Oct 12 2021 Adam Williamson <awilliam@redhat.com> - 21.2.3-6
- Add patches from previous commit to git

* Tue Oct 12 2021 Adam Williamson <awilliam@redhat.com> - 21.2.3-5
- Backport MR#13231 and revert MR#3724 to fix Tegra (kherbst)

* Tue Oct 12 2021 Tom Stellard <tstellar@redhat.com> - 21.2.3-4
- Rebuild for llvm-13.0.0

* Mon Oct 11 2021 Dave Airlie <airlied@redhat.com> - 21.2.3-3
- mesa: backport another crocus fix

* Mon Oct 11 2021 Dave Airlie <airlied@redhat.com> - 21.2.3-2
- mesa: backport some crocus fixes

* Wed Sep 29 2021 Pete Walter <pwalter@fedoraproject.org> - 21.2.3-1
- Update to 21.2.3

* Tue Sep 21 2021 Pete Walter <pwalter@fedoraproject.org> - 21.2.2-1
- Update to 21.2.2

* Mon Sep 13 2021 Dave Airlie <airlied@redhat.com> - 21.2.1-4
- mesa: add fixes from 21.2 staging branch and enable crocus by default

* Sat Aug 21 2021 Pete Walter <pwalter@fedoraproject.org> - 21.2.1-3
- Fix the build

* Fri Aug 20 2021 Peter Robinson <pbrobinson@gmail.com> - 21.2.1-2
- Enable panfrost vulcan driver on arm

* Thu Aug 19 2021 Pete Walter <pwalter@fedoraproject.org> - 21.2.1-1
- Update to 21.2.1

* Thu Aug 19 2021 Pete Walter <pwalter@fedoraproject.org> - 21.2.0-4
- Opt in to rpmautospec

* Thu Aug 19 2021 Stephen Gallagher <sgallagh@redhat.com> - 21.2.0-3
- Fixes for building against LLVM 13

* Thu Aug 05 2021 ValdikSS <iam@valdikss.org.ru> - 21.2.0-2
- Enable Crocus driver

* Thu Aug 05 2021 Pete Walter <pwalter@fedoraproject.org> - 21.2.0-1
- Update to 21.2.0

* Sat Jul 31 2021 Pete Walter <pwalter@fedoraproject.org> - 21.1.6-1
- Update to 21.1.6

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 17 2021 Pete Walter <pwalter@fedoraproject.org> - 21.1.5-1
- Update to 21.1.5

* Sat Jul 03 2021 Pete Walter <pwalter@fedoraproject.org> - 21.1.4-1
- Update to 21.1.4

* Fri Jun 18 2021 Pete Walter <pwalter@fedoraproject.org> - 21.1.3-1
- Update to 21.1.3

* Sat Jun 12 2021 Pete Walter <pwalter@fedoraproject.org> - 21.1.2-1
- Update to 21.1.2

* Thu May 27 2021 Pete Walter <pwalter@fedoraproject.org> - 21.1.1-3
- Clean up %%ldconfig_scriptlets macros

* Wed May 26 2021 Tom Stellard <tstellar@redhat.com> - 21.1.1-2
- Rebuild for LLVM 12.0.0-final

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 21.1.1-1
- Update to 21.1.1

* Wed May 05 2021 Adam Jackson <ajax@redhat.com> - 21.1.0-1
- Update to 21.1.0

* Thu Apr 29 2021 Kalev Lember <klember@redhat.com> - 21.0.3-2
- Backport a fix for amdgpu graphics corruption regression

* Thu Apr 22 2021 Pete Walter <pwalter@fedoraproject.org> - 21.0.3-1
- Update to 21.0.3

* Mon Apr 19 2021 Dave Airlie <airlied@redhat.com> - 21.0.2-2
- mesa: move imx-drm to correct place in file.

* Wed Apr 07 2021 Pete Walter <pwalter@fedoraproject.org> - 21.0.2-1
- Update to 21.0.2

* Thu Apr 01 2021 Dave Airlie <airlied@redhat.com> - 21.0.1-6
- Backport CPU caps fixes

* Fri Mar 26 2021 Adam Jackson <ajax@redhat.com> - 21.0.1-4
- Split out with_r300 and with_r600 Disable r300, r600, etnaviv, lima, vc4
  and v3d in RHEL

* Thu Mar 25 2021 Dave Airlie <airlied@redhat.com> - 21.0.1-3
- add missing patch

* Thu Mar 25 2021 Dave Airlie <airlied@redhat.com> - 21.0.1-2
- fix zink loading in places it shouldn't.

* Wed Mar 24 2021 Pete Walter <pwalter@fedoraproject.org> - 21.0.1-1
- Update to 21.0.1

* Tue Mar 23 2021 Pete Walter <pwalter@fedoraproject.org> - 21.0.0-2
- Rebuild for llvm 12

* Fri Mar 12 2021 Pete Walter <pwalter@fedoraproject.org> - 21.0.0-1
- Update to 21.0.0

* Mon Mar 08 2021 Adam Williamson <awilliam@redhat.com> - 21.0.0~rc5-3
- Backport MR #9425 to fix GNOME Shell crash on Jetson Nano (#1930977)

* Mon Feb 22 2021 Dave Airlie <airlied@redhat.com> - 21.0.0~rc5-2
- fix sddm/vmware regression

* Fri Feb 19 2021 Pete Walter <pwalter@fedoraproject.org> - 21.0.0~rc5-1
- Update to 21.0.0-rc5

* Fri Feb 19 2021 Adam Jackson <ajax@redhat.com> - 21.0.0~rc4-2
- Disable OpenMAX, OpenCL, and nine in RHEL

* Wed Feb 17 2021 Pete Walter <pwalter@fedoraproject.org> - 21.0.0~rc4-1
- Update to 21.0.0-rc4

* Wed Feb 03 2021 Dave Airlie <airlied@redhat.com> - 21.0.0~rc3-2
- Fix zink/swrast/lavapipe/gnome-shell interaction (#1924360)

* Fri Jan 29 2021 Pete Walter <pwalter@fedoraproject.org> - 21.0.0~rc3-1
- Update to 21.0.0-rc3

* Fri Jan 29 2021 Dave Airlie <airlied@redhat.com> - 20.3.3-7
- Backport upstream fix for EGL issues with qemu

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Tom Stellard <tstellar@redhat.com> - 20.3.3-5
- Rebuild for clang-11.1.0

* Wed Jan 20 2021 Adam Jackson <ajax@redhat.com> - 20.3.3-4
- Disable classic drivers in RHEL

* Fri Jan 15 2021 Dave Airlie <airlied@redhat.com> - 20.3.3-3
- Fix lavapipe missing ext that breaks gstreamer/pidgin

* Thu Jan 14 2021 Dave Airlie <airlied@redhat.com> - 20.3.3-2
- Fix device selection layer for vulkan 1.2

* Wed Jan 13 2021 Pete Walter <pwalter@fedoraproject.org> - 20.3.3-1
- Update to 20.3.3

* Thu Dec 31 2020 Pete Walter <pwalter@fedoraproject.org> - 20.3.2-1
- Update to 20.3.2

* Wed Dec 16 2020 Pete Walter <pwalter@fedoraproject.org> - 20.3.1-2
- Fix pre-release versions in old %%changelog entries

* Wed Dec 16 2020 Pete Walter <pwalter@fedoraproject.org> - 20.3.1-1
- Update to 20.3.1

* Mon Dec 07 2020 Dave Airlie <airlied@redhat.com> - 20.3.0-2
- Fix regression with radeon si/cik cards

* Fri Dec 04 2020 Dave Airlie <airlied@redhat.com> - 20.3.0-1
- Update to 20.3.0 release

* Tue Dec 01 2020 Peter Robinson <pbrobinson@gmail.com> - 20.3.0~rc3-2
- Enable Zink opengl over vulkan driver, Broadcom v3dv and freedreno vulkan
  drivers on arm

* Mon Nov 30 2020 Dave Airlie <airlied@redhat.com> - 20.3.0~rc3-1
- Update to 20.3.0-rc3

* Mon Nov 30 2020 Dave Airlie <airlied@redhat.com> - 20.3.0~rc2-1
- Update to 20.3.0-rc2

* Sat Nov 28 2020 Peter Robinson <pbrobinson@gmail.com> - 20.2.3-3
- Update meson options and nomenclature

* Sat Nov 28 2020 Peter Robinson <pbrobinson@gmail.com> - 20.2.3-2
- Cleanup vulkan conditionals, make it more inline with dri_drivers so it's
  more straightforward as arches diverge supported drivers

* Tue Nov 24 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.3-1
- Update to 20.2.3

* Sat Nov 07 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.2-1
- Update to 20.2.2

* Wed Oct 14 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.1-1
- Update to 20.2.1

* Tue Sep 29 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.0-3
- Update glvnd required version

* Tue Sep 29 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.0-2
- Drop no longer needed big endian fix

* Tue Sep 29 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.0-1
- Update to 20.2.0

* Fri Sep 25 2020 Adam Jackson <ajax@redhat.com> - 20.2.0~rc4-3
- mesa-libGL-devel Recommends: gl-manpages

* Fri Sep 04 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.0~rc4-2
- Remove more no longer needed build hacks

* Fri Sep 04 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.0~rc4-1
- Update to 20.2.0~rc4

* Thu Sep 03 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.0~rc3-2
- Remove -fcommon build workaround

* Sat Aug 29 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.0~rc3-1
- Update to 20.2.0~rc3

* Sun Aug 23 2020 Pete Walter <pwalter@fedoraproject.org> - 20.2.0~rc2-1
- Update to 20.2.0~rc2

* Sat Aug 22 2020 Kalev Lember <klember@redhat.com> - 20.1.6-2
- Disable LTO as it appears to break some games (#1862771)

* Thu Aug 20 2020 Pete Walter <pwalter@fedoraproject.org> - 20.1.6-1
- Update to 20.1.6

* Thu Aug 06 2020 Pete Walter <pwalter@fedoraproject.org> - 20.1.5-1
- Update to 20.1.5

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Pete Walter <pwalter@fedoraproject.org> - 20.1.4-1
- Update to 20.1.4

* Wed Jul 22 2020 Lyude Paul <lyude@redhat.com> - 20.1.3-2
- Fix build dependencies on certain arches

* Sat Jul 11 2020 Pete Walter <pwalter@fedoraproject.org> - 20.1.3-1
- Update to 20.1.3

* Thu Jun 25 2020 Pete Walter <pwalter@fedoraproject.org> - 20.1.2-1
- Update to 20.1.2

* Wed Jun 10 2020 Pete Walter <pwalter@fedoraproject.org> - 20.1.1-2
- Fix the build with Python 3.9

* Wed Jun 10 2020 Pete Walter <pwalter@fedoraproject.org> - 20.1.1-1
- Update to 20.1.1

* Thu May 28 2020 Dave Airlie <airlied@redhat.com> - 20.1.0-1
- Update to 20.1.0

* Thu May 21 2020 Dave Airlie <airlied@redhat.com> - 20.1.0~rc4-1
- Update to 20.1.0-rc4

* Thu May 14 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.7-1
- Update to 20.0.7

* Thu Apr 30 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.6-1
- Update to 20.0.6

* Thu Apr 23 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.5-2
- Drop upstreamed patch

* Thu Apr 23 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.5-1
- Update to 20.0.5

* Fri Apr 03 2020 Dave Airlie <airlied@redhat.com> - 20.0.4-1
- Update to 20.0.4 (fix spirv regression)

* Wed Apr 01 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.3-1
- Update to 20.0.3

* Thu Mar 19 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.2-1
- Update to 20.0.2

* Fri Mar 06 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.1-1
- Update to 20.0.1

* Wed Feb 26 2020 Kalev Lember <klember@redhat.com> - 20.0.0-2
- Fix the build with llvm 10

* Thu Feb 20 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.0-1
- Update to 20.0.0

* Fri Feb 14 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.0~rc3-1
- Update to 20.0.0~rc3

* Sat Feb 08 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.0~rc2-1
- Update to 20.0.0~rc2

* Sun Feb 02 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.0~rc1-2
- Update files list for arm drivers

* Sat Feb 01 2020 Pete Walter <pwalter@fedoraproject.org> - 20.0.0~rc1-1
- Update to 20.0.0~rc1

* Wed Jan 29 2020 Pete Walter <pwalter@fedoraproject.org> - 19.3.3-1
- Update to 19.3.3

* Thu Jan 23 2020 Tom Stellard <tstellar@redhat.com> - 19.3.2-3
- Link against libclang-cpp.so https://fedoraproject.org/wiki/Changes/Stop-
  Shipping-Individual-Component-Libraries-In-clang-lib-Package

* Thu Jan 23 2020 Tom Stellard <tstellar@redhat.com> - 19.3.2-2
- Build with -fcommon until upstream fixes omx build with gcc10

* Fri Jan 10 2020 Pete Walter <pwalter@fedoraproject.org> - 19.3.2-1
- Update to 19.3.2

* Wed Dec 18 2019 Pete Walter <pwalter@fedoraproject.org> - 19.3.1-1
- Update to 19.3.1

* Mon Dec 16 2019 Pete Walter <pwalter@fedoraproject.org> - 19.3.0-1
- Update to 19.3.0

* Thu Dec 05 2019 Pete Walter <pwalter@fedoraproject.org> - 19.3.0~rc6-1
- Update to 19.3.0~rc6

* Thu Nov 28 2019 Pete Walter <pwalter@fedoraproject.org> - 19.3.0~rc5-1
- Update to 19.3.0~rc5

* Sun Nov 24 2019 Pete Walter <pwalter@fedoraproject.org> - 19.3.0~rc4-1
- Update to 19.3.0~rc4

* Thu Nov 14 2019 Pete Walter <pwalter@fedoraproject.org> - 19.3.0~rc3-1
- Update to 19.3.0~rc3

* Tue Nov 12 2019 Pete Walter <pwalter@fedoraproject.org> - 19.3.0~rc2-2
- Fix the build on arm

* Fri Nov 08 2019 Pete Walter <pwalter@fedoraproject.org> - 19.3.0~rc2-1
- Update to 19.3.0~rc2

* Thu Nov 07 2019 Pete Walter <pwalter@fedoraproject.org> - 19.2.3-1
- Update to 19.2.3

* Fri Oct 25 2019 Peter Robinson <pbrobinson@gmail.com> - 19.2.2-5
- adjust mesa-khr-devel requires now provided by libglvnd

* Fri Oct 25 2019 Peter Robinson <pbrobinson@gmail.com> - 19.2.2-4
- Fix up and remove bits now in libglvnd

* Fri Oct 25 2019 Peter Robinson <pbrobinson@gmail.com> - 19.2.2-3
- rebuild against libglvnd 1.2

* Fri Oct 25 2019 Pete Walter <pwalter@fedoraproject.org> - 19.2.2-2
- Update files lists

* Fri Oct 25 2019 Pete Walter <pwalter@fedoraproject.org> - 19.2.2-1
- Update to 19.2.2

* Thu Oct 10 2019 Peter Robinson <pbrobinson@gmail.com> - 19.2.1-1
- 19.2.1

* Fri Oct 04 2019 Gwyn Ciesla <gwync@protonmail.com> - 19.2.0-2
- Rebuild for new freeglut.

* Wed Sep 25 2019 Pete Walter <pwalter@fedoraproject.org> - 19.2.0-1
- Update to 19.2.0

* Wed Sep 18 2019 Pete Walter <pwalter@fedoraproject.org> - 19.2.0~rc4-1
- Update to 19.2.0~rc4

* Tue Sep 17 2019 Adam Jackson <ajax@redhat.com> - 19.2.0~rc3-2
- Build iris too

* Thu Sep 12 2019 Pete Walter <pwalter@fedoraproject.org> - 19.2.0~rc3-1
- Update to 19.2.0~rc3

* Thu Sep 05 2019 Pete Walter <pwalter@fedoraproject.org> - 19.2.0~rc2-1
- Update to 19.2.0~rc2

* Tue Aug 27 2019 Adam Jackson <ajax@redhat.com> - 19.2.0~rc1-5
- BuildRequire vulkan-headers not vulkan-devel to ease llvm updates

* Thu Aug 22 2019 Peter Robinson <pbrobinson@gmail.com> - 19.2.0~rc1-4
- Bring back egl.pc for now

* Wed Aug 21 2019 Peter Robinson <pbrobinson@gmail.com> - 19.2.0~rc1-3
- add mxsfb-drm_dri and stm_dri drivers for arm platforms

* Wed Aug 21 2019 Peter Robinson <pbrobinson@gmail.com> - 19.2.0~rc1-2
- pkgconfig/egl.pc no longer shipped

* Wed Aug 21 2019 Peter Robinson <pbrobinson@gmail.com> - 19.2.0~rc1-1
- 19.2.0~rc1

* Thu Aug 08 2019 Pete Walter <pwalter@fedoraproject.org> - 19.1.4-1
- Update to 19.1.4

* Wed Jul 24 2019 Pete Walter <pwalter@fedoraproject.org> - 19.1.3-1
- Update to 19.1.3

* Tue Jul 09 2019 Pete Walter <pwalter@fedoraproject.org> - 19.1.2-1
- Update to 19.1.2

* Wed Jun 26 2019 Pete Walter <pwalter@fedoraproject.org> - 19.1.1-1
- Update to 19.1.1

* Mon Jun 24 2019 Peter Robinson <pbrobinson@gmail.com> - 19.1.0-2
- Enable v3d driver

* Wed Jun 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.1.0-1
- Update to 19.1.0

* Fri Jun 07 2019 Pete Walter <pwalter@fedoraproject.org> - 19.1.0~rc5-1
- Update to 19.1.0~rc5

* Thu May 30 2019 Pete Walter <pwalter@fedoraproject.org> - 19.1.0~rc4-1
- Update to 19.1.0~rc4

* Wed May 22 2019 Dave Airlie <airlied@redhat.com> - 19.1.0~rc3-1
- Update to 19.1.0-rc3

* Tue May 21 2019 Adam Jackson <ajax@redhat.com> - 19.1.0~rc2-2
- Delete unused patch

* Tue May 14 2019 Dave Airlie <airlied@redhat.com> - 19.1.0~rc2-1
- Update to 19.1.0-rc2

* Tue May 14 2019 Dave Airlie <airlied@redhat.com> - 19.1.0~rc1-8
- Bring back glesv2.pc for now

* Sat May 11 2019 Peter Robinson <pbrobinson@gmail.com> - 19.1.0~rc1-7
- Enable panfrost

* Thu May 09 2019 Adam Jackson <ajax@redhat.com> - 19.1.0~rc1-6
- Enable lima

* Thu May 09 2019 Adam Jackson <ajax@redhat.com> - 19.1.0~rc1-5
- Add some more stuff to .gitignore

* Wed May 08 2019 Dave Airlie <airlied@redhat.com> - 19.1.0~rc1-4
- add missing exynos driver

* Wed May 08 2019 Dave Airlie <airlied@redhat.com> - 19.1.0~rc1-3
- fix missing kmsro

* Wed May 08 2019 Dave Airlie <airlied@redhat.com> - 19.1.0~rc1-2
- add missing kmsro drivers

* Wed May 08 2019 Dave Airlie <airlied@redhat.com> - 19.1.0~rc1-1
- Update to 19.1.0-rc1

* Thu Apr 25 2019 Pete Walter <pwalter@fedoraproject.org> - 19.0.3-1
- Update to 19.0.3

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 19.0.2-5
- Rebuild with Meson fix for #1699099

* Mon Apr 15 2019 Pete Walter <pwalter@fedoraproject.org> - 19.0.2-4
- Remove unneeded chrpath build dep

* Sun Apr 14 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.2-3
- Remove unneeded sources

* Thu Apr 11 2019 Adam Jackson <ajax@redhat.com> - 19.0.2-2
- Drop the mpeg1/2 sanitize hack Switch to upstream tarball since we no
  longer need to do the above

* Thu Apr 11 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.2-1
- Update to 19.0.2

* Thu Apr 04 2019 Adam Jackson <ajax@redhat.com> - 19.0.1-2
- Nuke rpath from installed DRI drivers

* Wed Mar 27 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.1-1
- Update to 19.0.1

* Mon Mar 25 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.0-2
- Rebuild with -Db_ndebug=true

* Wed Mar 13 2019 Peter Robinson <pbrobinson@gmail.com> - 19.0.0-1
- 19.0.0

* Thu Mar 07 2019 Pete Walter <pwalter@fedoraproject.org> - 19.0.0~rc7-1
- Update to 19.0.0~rc7

* Wed Feb 27 2019 Pete Walter <pwalter@fedoraproject.org> - 19.0.0~rc6-1
- Update to 19.0.0~rc6

* Wed Feb 20 2019 Peter Robinson <pbrobinson@gmail.com> - 19.0.0~rc5-1
- 19.0.0~rc5

* Thu Feb 14 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.0~rc4-3
- Update EGL patch

* Thu Feb 14 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.0~rc4-2
- relax dependency of xcb-randr

* Thu Feb 14 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.0~rc4-1
- Update to 19.0.0~rc4

* Tue Feb 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.0~rc2-4
- Fix radv vulkan

* Fri Feb 08 2019 Pete Walter <pwalter@fedoraproject.org> - 19.0.0~rc2-3
- Add back accidentally lost patch to disable rgb10 configs by default
  (#1650929)

* Wed Feb 06 2019 Peter Robinson <pbrobinson@gmail.com> - 19.0.0~rc2-2
- update 19.0.0~rc2

* Wed Feb 06 2019 Peter Robinson <pbrobinson@gmail.com> - 19.0.0~rc2-1
- 19.0.0~rc2

* Thu Jan 31 2019 Peter Robinson <pbrobinson@gmail.com> - 19.0.0~rc1-3
- add kmsro build option, add work around for missing files in 'make dist'
  (fixed upstream)

* Thu Jan 31 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.0~rc1-2
- Switch imx to kmsro

* Thu Jan 31 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 19.0.0~rc1-1
- Update to 19.0.0~rc1

* Thu Jan 17 2019 Adam Jackson <ajax@redhat.com> - 18.3.2-1
- Update to 18.3.2

* Wed Dec 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.3.1-3
- Enable annotated build

* Wed Dec 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.3.1-2
- Switch to meson buildsystem

* Tue Dec 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.3.1-1
- commit spec changes

* Tue Dec 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.3.0-2
- Update to 18.3.1

* Fri Dec 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.3.0-1
- Update to 18.3.0

* Fri Dec 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.3.0~rc5-3
- Remove unused patches

* Tue Dec 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.3.0~rc5-2
- Backport patch to fix totem

* Tue Dec 04 2018 Peter Robinson <pbrobinson@gmail.com> - 18.3.0~rc5-1
- 18.3.0 rc5

* Tue Nov 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.3.0~rc4-1
- Update to 18.3.0~rc4

* Thu Nov 15 2018 Adam Jackson <ajax@redhat.com> - 18.3.0~rc2-2
- Add mesa-khr-devel subpackage to hold <KHR/khrplatform.h>, and make mesa-
  lib{GL,GLES,EGL}-devel Require it.

* Wed Nov 14 2018 Adam Jackson <ajax@redhat.com> - 18.3.0~rc2-1
- Update to 18.3.0 RC2 Re-enable 10bpc fbconfigs, clutter apps seem to work
  now Drop now-unnecessary big-endian compilation fix

* Tue Nov 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.2.4-3
- Rebuild without workaround

* Mon Nov 05 2018 Dave Airlie <airlied@redhat.com> - 18.2.4-2
- workaround bug with gcc 8.2.1-4

* Thu Nov 01 2018 Adam Jackson <ajax@redhat.com> - 18.2.4-1
- Update to 18.2.4

* Wed Oct 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.2.3-1
- Update to 18.2.3

* Fri Oct 05 2018 Peter Robinson <pbrobinson@gmail.com> - 18.2.2-1
- 18.2.2

* Fri Sep 21 2018 Peter Robinson <pbrobinson@gmail.com> - 18.2.1-1
- 18.2.1

* Wed Sep 19 2018 Adam Williamson <awilliam@redhat.com> - 18.2.0-2
- Fix "HW cursor for format" error message flood with swrast

* Sat Sep 08 2018 Peter Robinson <pbrobinson@gmail.com> - 18.2.0-1
- 18.2.0

* Sun Sep 02 2018 Hans de Goede <hdegoede@redhat.com> - 18.2.0~rc5-1
- Update to 18.2.0~rc5

* Wed Aug 22 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.2.0~rc3-2
- Re-enable RadeonSI on ARM

* Tue Aug 21 2018 Peter Robinson <pbrobinson@gmail.com> - 18.2.0~rc3-1
- 18.2.0~rc3

* Sun Aug 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.2.0~rc2-4
- correct files

* Sun Aug 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.2.0~rc2-3
- no radeon vulkan driver on arm

* Sat Aug 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.2.0~rc2-2
- BR: xrandr

* Sat Aug 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.2.0~rc2-1
- Update to 18.2.0~rc2

* Mon Jul 30 2018 Peter Robinson <pbrobinson@gmail.com> - 18.1.5-1
- 18.1.5

* Mon Jul 23 2018 Dave Airlie <airlied@redhat.com> - 18.1.4-3
- bump glvnd requires

* Mon Jul 23 2018 Dave Airlie <airlied@redhat.com> - 18.1.4-2
- fix fallback path for glvnd

* Tue Jul 17 2018 Peter Robinson <pbrobinson@gmail.com> - 18.1.4-1
- 18.1.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 18.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Adam Jackson <ajax@redhat.com> - 18.1.3-3
- Drop texture float patch

* Sun Jul 01 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.1.3-2
- Use simpler %%ldconfig macro

* Sun Jul 01 2018 Peter Robinson <pbrobinson@gmail.com> - 18.1.3-1
- 18.1.3

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 18.1.2-5
- Use ldconfig scriptlet macros

* Mon Jun 18 2018 Adam Jackson <ajax@redhat.com> - 18.1.2-4
- Create %%{_includedir}/vulkan unconditionally

* Mon Jun 18 2018 Adam Jackson <ajax@redhat.com> - 18.1.2-3
- Careful, only configure vulkan drivers if hardware

* Mon Jun 18 2018 Adam Jackson <ajax@redhat.com> - 18.1.2-2
- Build mesa-vulkan-drivers everywhere Build actual vulkan drivers on all
  but s390x

* Sat Jun 16 2018 Peter Robinson <pbrobinson@gmail.com> - 18.1.2-1
- 18.1.2

* Fri Jun 15 2018 Adam Jackson <ajax@redhat.com> - 18.1.1-9
- Build tegra too

* Thu Jun 14 2018 Adam Jackson <ajax@redhat.com> - 18.1.1-8
- libglvnd is epoched

* Thu Jun 14 2018 Adam Jackson <ajax@redhat.com> - 18.1.1-7
- Change the name of the fallback GLX library

* Wed Jun 06 2018 Adam Jackson <ajax@redhat.com> - 18.1.1-6
- this would all be easier if we just built amdgpu on arm32

* Wed Jun 06 2018 Adam Jackson <ajax@redhat.com> - 18.1.1-5
- ,,,

* Tue Jun 05 2018 Adam Jackson <ajax@redhat.com> - 18.1.1-4
- hrgnarhgnhrn

* Tue Jun 05 2018 Adam Jackson <ajax@redhat.com> - 18.1.1-3
- Stop mentioning ppc and s390, we don't build for them anymore Remove
  with_llvm, now always true Switch with_radeonsi to be an exclude pattern,
  apparently not available for armv7hl.

* Tue Jun 05 2018 Adam Jackson <ajax@redhat.com> - 18.1.1-2
- Stop mentioning ppc and s390, we don't build for them anymore remove
  with_llvm and with_radeonsi as they're now always true

* Sun Jun 03 2018 Peter Robinson <pbrobinson@gmail.com> - 18.1.1-1
- 18.1.1

* Thu May 24 2018 Peter Robinson <pbrobinson@gmail.com> - 18.1.0-4
- 18.1.0

* Sat May 12 2018 Peter Robinson <pbrobinson@gmail.com> - 18.1.0-3
- 18.1.0~rc4

* Sat May 05 2018 Peter Robinson <pbrobinson@gmail.com> - 18.1.0-2
- 18.1 rc3

* Fri May 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 18.1.0-1
- Update ot 18.1.0~rc2

* Tue May 01 2018 Peter Robinson <pbrobinson@gmail.com> - 18.0.2-2
- RPMAUTOSPEC: unresolvable merge

## END: Generated by rpmautospec
