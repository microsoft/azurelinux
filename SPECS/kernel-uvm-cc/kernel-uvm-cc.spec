%global security_hardening none
%global debug_package %{nil}
%define kernel_version 6.18.52
%define kernel_flavor mshv1
%define uname_r %{kernel_version}-%{kernel_flavor}-%{release}.uvm-cc

%ifarch x86_64
%define arch x86_64
%define archdir x86
%define config_source %{SOURCE1}
%endif

Summary:        Linux Kernel for confidential Kata UVMs
Name:           kernel-uvm-cc
Version:        %{kernel_version}.%{kernel_flavor}
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
ExclusiveArch:  x86_64
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/kata-uvm/%{version}.tar.gz#/kernel-uvm-%{version}.tar.gz
Source1:        config
Source2:        README.md
Patch0:         0001-x86-sev-Unregister-the-decompressor-GHCB-when-supported.patch
Patch1:         0002-x86-enable-early-x2apic-so-snp-guest-boots.patch
Patch2:         0003-hyperv-allocate-output-pages-for-enlightened-SNP-AP-startup.patch
BuildRequires:  audit-devel
BuildRequires:  bash
BuildRequires:  bc
BuildRequires:  cpio
BuildRequires:  diffutils
BuildRequires:  dwarves
BuildRequires:  elfutils-libelf-devel
BuildRequires:  glib-devel
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  procps-ng-devel
BuildRequires:  python3-devel
BuildRequires:  sed
Requires:       filesystem
Requires:       kmod
Requires(post): coreutils
Requires(postun): coreutils

# Keep config aligned with kernel-uvm; see README.md for update instructions.

%define image_fname vmlinux.bin
%ifarch x86_64
%define image arch/x86/boot/compressed/%{image_fname}
%define compressed_image_fname bzImage
%if 0%{?centos_version} && 0%{?centos_version} < 900
%define kcflags %{nil}
%else
%define kcflags -Wa,-mx86-used-note=no
%endif
%endif

%description
Guest kernel artifacts for standard-injection AMD SEV-SNP Kata UVMs.
The bzImage is an input to IGVM generation, not a host boot kernel.
This package does not replace kernel-uvm or install host boot configuration.

%package devel
Summary:        Lightweight kernel Devel package
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the confidential kernel UVM devel files.

%prep
%autosetup -p1 -n CBL-Mariner-Linux-Kernel-rolling-lts-kata-uvm-%{version}

make mrproper

cp %{config_source} .config
cp .config current_config

# Keep the release parseable by guest userspace that expects X.Y.Z-suffix.
sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}.uvm-cc"/' .config
make LC_ALL= ARCH=%{arch} EXTRAVERSION=-%{kernel_flavor} LOCALVERSION= oldconfig

# Verify the config files match, apart from the release header and suffix.
cp .config new_config
sed -i -e 's/^# Linux\/x86_64 .* Kernel Configuration$/# Linux\/x86_64 %{version} Kernel Configuration/' \
    -e 's/^CONFIG_LOCALVERSION=".*"/CONFIG_LOCALVERSION=""/' new_config
diff --unified new_config current_config > config_diff || true
if [ -s config_diff ]; then
    cat config_diff
    echo "Config file has unexpected changes"
    echo "Update config file to set changed values explicitly"
    exit 1
fi

%build
KCFLAGS="%{kcflags}" make VERBOSE=1 KBUILD_BUILD_VERSION="1" KBUILD_BUILD_HOST="CBL-Mariner" ARCH=%{arch} EXTRAVERSION=-%{kernel_flavor} LOCALVERSION= %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}/lib/modules/%{uname_r}

D=%{buildroot}%{_datadir}/%{name}
install -D -m 644 %{image} $D/%{image_fname}

%ifarch x86_64
install -D -m 644 arch/%{arch}/boot/%{compressed_image_fname} $D/%{compressed_image_fname}
%endif

mkdir -p %{buildroot}/lib/modules/%{name}
ln -s %{_datadir}/%{name}/vmlinux.bin %{buildroot}/lib/modules/%{name}/vmlinux

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}
ln -sf "%{_prefix}/src/linux-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -exec chmod u+x {} +

install -Dm 644 .config %{buildroot}%{_datadir}/%{name}/config
install -Dm 644 include/config/kernel.release %{buildroot}%{_datadir}/%{name}/kernel.release
install -Dm 644 %{SOURCE2} %{buildroot}%{_docdir}/%{name}/README.md

%check
test -s arch/x86/boot/bzImage
test -s arch/x86/boot/compressed/vmlinux.bin
test -s Module.symvers
test -x tools/objtool/objtool
test -x tools/objtool/fixdep
test "$(cat include/config/kernel.release)" = "%{uname_r}"
for option in AMD_MEM_ENCRYPT X86_X2APIC HYPERV SMP VIRTIO_PCI VIRTIO_BLK \
              VIRTIO_NET VIRTIO_VSOCKETS EROFS_FS EXT4_FS BLK_DEV_DM DM_VERITY; do
    grep -qx "CONFIG_${option}=y" .config || exit 1
done

%files
%defattr(-,root,root)
%license COPYING
%doc %{_docdir}/%{name}/
%{_datadir}/%{name}/%{image_fname}
%ifarch x86_64
%{_datadir}/%{name}/%{compressed_image_fname}
%endif
%{_datadir}/%{name}/config
%{_datadir}/%{name}/kernel.release
%dir %{_datadir}/%{name}
%dir /lib/modules/%{name}
/lib/modules/%{name}/vmlinux

%files devel
%defattr(-,root,root)
%dir /lib/modules/%{uname_r}
/lib/modules/%{uname_r}/build
%{_prefix}/src/linux-headers-%{uname_r}

%changelog
* Sat Oct 10 2026 Nikola Bojanic <nbojanic@microsoft.com> - 6.18.52.mshv1-1
- Original version for Azure Linux
- License verified
- Package a separate x86_64 SNP guest kernel using the kernel-uvm configuration
- Add public GHCB unregister, early x2APIC, and SNP AP output-page fixes
