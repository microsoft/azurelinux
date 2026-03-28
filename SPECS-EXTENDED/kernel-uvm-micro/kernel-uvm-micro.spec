%global security_hardening none
%global debug_package %{nil}
%define uname_r %{version}-%{release}

%ifarch x86_64
%define arch x86_64
%define archdir x86
%define config_source %{SOURCE1}
%endif

%ifarch aarch64
%define arch arm64
%define archdir arm64
%define config_source %{SOURCE1}
%endif

Summary:        Lightweight Linux Kernel for Kata UVM (Micro)
Name:           kernel-uvm-micro
Version:        6.6.96.mshv1
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/kata-uvm/%{version}.tar.gz#/kernel-uvm-%{version}.tar.gz
Source1:        config
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

# Lightweight kernel-uvm variant with a minimal config focused on
# filesystem and virtio-fs support for Kata container UVMs.

# When updating the config files it is important to sanitize them.
# Steps for updating a config file:
#  1. Extract the linux sources into a folder
#  2. Add the current config file to the folder
#  3. Run `make menuconfig` to edit the file (Manually editing is not recommended)
#     * You might have to install the following dependencies: libncurses5-dev flex
#  4. Save the config file
#  5. Copy the config file back into the kernel spec folder
#  6. Revert any undesired changes (GCC related changes, etc)
#  8. Build the kernel package
#  9. Apply the changes listed in the log file (if any) to the config file
#  10. Verify the rest of the config file looks ok
# If there are significant changes to the config file, disable the config check and build the
# kernel rpm. The final config file is included in /boot in the rpm.

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
%ifarch aarch64
%define kcflags %{nil}
%define image arch/arm64/boot/Image
%endif

%description
The kernel-uvm-micro package contains a lightweight Linux kernel for
Kata UVM with a minimal configuration focused on filesystem and
virtio-fs support.

%package devel
Summary:        Lightweight kernel Devel package
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the kernel UVM micro devel files

%prep
%autosetup -p1 -n CBL-Mariner-Linux-Kernel-rolling-lts-kata-uvm-%{version}

make mrproper

cp %{config_source} .config
cp .config current_config
sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config
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

D=%{buildroot}%{_datadir}/cloud-hypervisor
install -D -m 644 %{image} $D/%{image_fname}

%ifarch x86_64
install -D -m 644 arch/%{arch}/boot/%{compressed_image_fname} $D/%{compressed_image_fname}
%endif

mkdir -p %{buildroot}/lib/modules/%{name}
ln -s %{_datadir}/cloud-hypervisor/vmlinux.bin %{buildroot}/lib/modules/%{name}/vmlinux

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

%files
%defattr(-,root,root)
%license COPYING
%{_datadir}/cloud-hypervisor/%{image_fname}
%ifarch x86_64
%{_datadir}/cloud-hypervisor/%{compressed_image_fname}
%endif
%dir %{_datadir}/cloud-hypervisor
/lib/modules/%{name}/vmlinux

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
%{_prefix}/src/linux-headers-%{uname_r}

%changelog
* Sun Mar 23 2026 Azure Linux Team <azurelinux@microsoft.com> - 6.6.96.mshv1-1
- Initial kernel-uvm-micro package with lightweight config
- Minimal filesystem and virtio-fs focused configuration
