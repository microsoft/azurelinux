%global security_hardening none
%global debug_package %{nil}
# The -hpc suffix keeps the kernel release, the /lib/modules tree and the
# -devel headers distinct from kernel-uvm, so both packages can be installed
# side by side and out-of-tree modules can target this flavor explicitly.
%define uname_r %{version}-%{release}-hpc

%ifarch x86_64
%define arch x86_64
%define archdir x86
%define config_source %{SOURCE1}
%endif

%ifarch aarch64
%define arch arm64
%define archdir arm64
%define config_source %{SOURCE2}
%endif

Summary:        Linux Kernel for Kata UVMs running GPU and HPC workloads
Name:           kernel-uvm-hpc
Version:        6.18.52.mshv1
Release:        1%{?dist}
License:        GPL-2.0-only
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/kata-uvm/%{version}.tar.gz#/kernel-uvm-%{version}.tar.gz
Source1:        config
Source2:        config_aarch64
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

# The config files are the kernel-uvm configs with every option of the Kata
# Containers GPU guest kernel (kata-deploy kernel-azure-gpus: the common, arch,
# confidential, measured-rootfs and nvidia-azure-repackaged fragments) layered
# on top, so the UVM matches the kernel Kata builds for GPU guests.
# CONFIG_TEST_HMM is intentionally left disabled.
#
# Steps for updating a config file:
#  1. Extract the linux sources into a folder
#  2. Add the current config file to the folder
#  3. Run `make menuconfig` to edit the file (Manually editing is not recommended)
#  4. Save the config file
#  5. Copy the config file back into the kernel spec folder
#  6. Revert any undesired changes (GCC related changes, etc)
#  7. Build the kernel package
#  8. Apply the changes listed in the log file (if any) to the config file
#  9. Verify the rest of the config file looks ok
# If there are significant changes to the config file, disable the config check and build the
# kernel rpm. The final config file is included in the -devel package.

%define image_fname vmlinux.bin
%define image_dir %{_datadir}/cloud-hypervisor/hpc
%ifarch x86_64
%define image arch/x86/boot/compressed/%{image_fname}
%define compressed_image_fname bzImage
%if 0%{?centos_version} && 0%{?centos_version} < 900
%define kcflags %{nil}
%else
%define kcflags -Wa,-mx86-used-note=no
%endif
%endif
%ifarch aarch64
%define kcflags %{nil}
%define image arch/arm64/boot/Image
%define compressed_image_fname Image.gz
%endif

%description
The Linux kernel for Kata utility VMs running GPU and HPC workloads. It extends
the kernel-uvm configuration with the full Kata Containers GPU guest kernel
configuration. GPU drivers are packaged separately and must be built against
this kernel.

%package devel
Summary:        Kernel UVM HPC Devel package
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the kernel UVM HPC devel files, used to build
out-of-tree modules (such as GPU drivers) for this kernel.

%prep
%autosetup -p1 -n CBL-Mariner-Linux-Kernel-rolling-lts-kata-uvm-%{version}

make mrproper

cp %{config_source} .config
cp .config current_config
sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}-hpc"/' .config
make LC_ALL= ARCH=%{arch} oldconfig

# Verify the config files match
cp .config new_config
sed -i 's/CONFIG_LOCALVERSION=".*"/CONFIG_LOCALVERSION=""/' new_config
diff --unified new_config current_config > config_diff || true
if [ -s config_diff ]; then
    printf "\n\n\n\n\n\n\n\n"
    cat config_diff
    printf "\n\n\n\n\n\n\n\n"
    echo "Config file has unexpected changes"
    echo "Update config file to set changed values explicitly"

#  (DISABLE THIS IF INTENTIONALLY UPDATING THE CONFIG FILE)
    exit 1
fi

%build
KCFLAGS="%{kcflags}" make VERBOSE=1 KBUILD_BUILD_VERSION="1" KBUILD_BUILD_HOST="CBL-Mariner" ARCH=%{arch} %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}/lib/modules/%{uname_r}

D=%{buildroot}%{image_dir}
install -D -m 644 %{image} $D/%{image_fname}
install -D -m 644 arch/%{arch}/boot/%{compressed_image_fname} $D/%{compressed_image_fname}

# Guest images need the loadable modules and modules.builtin/modules.order so
# modprobe resolves built-in drivers instead of failing. depmod is left to the
# image builder, which also adds out-of-tree modules such as the GPU driver.
make ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_STRIP=1 DEPMOD=/bin/true modules_install
rm -f %{buildroot}/lib/modules/%{uname_r}/build
find %{buildroot}/lib/modules/%{uname_r} -mindepth 1 -maxdepth 1 \
    | sed "s|^%{buildroot}||" > modules.files

mkdir -p %{buildroot}/lib/modules/%{name}
ln -s %{image_dir}/%{image_fname} %{buildroot}/lib/modules/%{name}/vmlinux

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_prefix}/src/linux-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_prefix}/src/linux-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -exec chmod u+x {} +

%files -f modules.files
%defattr(-,root,root)
%license COPYING
%dir %{_datadir}/cloud-hypervisor
%dir %{image_dir}
%{image_dir}/%{image_fname}
%{image_dir}/%{compressed_image_fname}
%dir /lib/modules/%{uname_r}
/lib/modules/%{name}/vmlinux

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
%{_prefix}/src/linux-headers-%{uname_r}

%changelog
* Mon Oct 26 2026 Jocelyn Berrendonner <jocelynb@microsoft.com> - 6.18.52.mshv1-1
- Original version for Azure Linux.
- License verified.
- Derived from kernel-uvm 6.18.52.mshv1-2.
- Layer the Kata Containers GPU guest kernel configuration (kernel-azure-gpus) on top
  of the kernel-uvm configuration, keeping CONFIG_TEST_HMM disabled
- Enable device-private memory, memory-failure handling, module unloading and
  module signature support for GPU drivers, and x86 shared virtual addressing
- Ship loadable modules and modules.builtin/modules.order for guest images
- Install the kernel images under /usr/share/cloud-hypervisor/hpc
