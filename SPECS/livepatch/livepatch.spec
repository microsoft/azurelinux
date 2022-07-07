%define kernel_version 5.15.48.1
%define kernel_release 4%{?dist}
%define kernel_full_version %{kernel_version}-%{kernel_release}

%define linux_source_dir CBL-Mariner-Linux-Kernel-rolling-lts-mariner-2-%{kernel_version}

%define livepatch_file concatenated_patches

Summary:        Set of livepatches for kernel %{kernel_full_version}
Name:           livepatch-%{kernel_full_version}
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/microsoft/CBL-Mariner
Source1:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-2/%{kernel_version}.tar.gz#/kernel-%{kernel_version}.tar.gz
Source2:        config
Source3:        mariner-ca.pem
Source100:      CVE-2022-12345.patch

BuildRequires:  audit-devel
BuildRequires:  bash
BuildRequires:  bc
BuildRequires:  binutils
BuildRequires:  bison
BuildRequires:  diffutils
BuildRequires:  dwarves
BuildRequires:  elfutils-libelf-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  glibc-devel
BuildRequires:  kbd
BuildRequires:  kernel-debuginfo = %{kernel_full_version}
BuildRequires:  kernel-headers = %{kernel_full_version}
BuildRequires:  kmod-devel
BuildRequires:  kpatch-build
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  procps-ng-devel
BuildRequires:  python3-devel
BuildRequires:  rpm-build
Requires(post): kpatch

%description
A set of kernel livepatches addressing CVEs present in Mariner's
kernel version %{kernel_full_version}.

%prep
%autopatch -p1
tar -xf %{SOURCE1}

cd %{linux_source_dir}

cp %{SOURCE2} .config

# Add CBL-Mariner cert into kernel's trusted keyring.
cp %{SOURCE3} certs/mariner.pem
sed -i 's#CONFIG_SYSTEM_TRUSTED_KEYS=""#CONFIG_SYSTEM_TRUSTED_KEYS="certs/mariner.pem"#' .config

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{kernel_release}"/' .config

# Concatenating patches into one file.
if [[ -n %{sources} ]]
then
    cat %{sources} > %{livepatch_file}
fi

%build
kpatch-build -ddd \
    --sourcedir %{linux_source_dir} \
    --vmlinux %{_libdir}/debug/lib/modules/%{kernel_full_version}/vmlinux \
    %{SOURCE100}

%install
install -d %{buildroot}%{_sysconfdir}/%{name}
mv *.ko %{buildroot}%{_sysconfdir}/%{name}/livepatch-%{kernel_full_version}.ko

%post
kpatch load %{_sysconfdir}/%{name}/livepatch-%{kernel_full_version}.ko
kpatch install %{_sysconfdir}/%{name}/livepatch-%{kernel_full_version}.ko

%preun
kpatch uninstall livepatch-%{kernel_full_version}
kpatch unload livepatch-%{kernel_full_version}

%files
%{_sysconfdir}/%{name}/livepatch-%{kernel_full_version}.ko

%changelog
* Wed Jun 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
- License verified.
