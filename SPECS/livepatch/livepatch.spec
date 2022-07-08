%define kernel_version 5.15.48.1
%define kernel_release 4%{?dist}
%define kernel_full_version %{kernel_version}-%{kernel_release}

%define builds_module %([[ -n "$(echo "%{patches}" | grep -oP "CVE-\d+-\d+(?=\.patch)")" ]] && echo 1 || echo 0)

%if !%{builds_module}
%define debug_package %{nil}
%endif

# Kpatch-build allows only alphanumeric characters, '-', and '_'.
%define livepatch_name %(value="%{name}-%{version}-%{release}"; echo "${value//[^a-zA-Z0-9_-]/-}")
%define livepatch_install_dir /usr/lib/livepatch/%{kernel_full_version}
%define livepatch_module_path %{livepatch_install_dir}/%{livepatch_name}.ko

%define patches_description \
%(
    for patch in %{patches}
    do
        cve_number=$(basename "${patch%.*}")
        [[ "$patch" == *.patch ]] && echo "Patched: $cve_number" || echo "NOT patched (kernel update required): $cve_number"
    done
)

Summary:        Set of livepatches for kernel %{kernel_full_version}
Name:           livepatch-%{kernel_full_version}
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/microsoft/CBL-Mariner
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-2/%{kernel_version}.tar.gz#/kernel-%{kernel_version}.tar.gz
Source1:        config
Source2:        mariner.pem
Patch0:         CVE-2022-12345.patch
Patch100:       CVE-2022-67890.nopatch

ExclusiveArch:  x86_64

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
%{patches_description}

%prep
%setup -n CBL-Mariner-Linux-Kernel-rolling-lts-mariner-2-%{kernel_version}

cp %{SOURCE1} .config
cp %{SOURCE2} certs/mariner.pem

sed -i 's#CONFIG_SYSTEM_TRUSTED_KEYS=""#CONFIG_SYSTEM_TRUSTED_KEYS="certs/mariner.pem"#' .config
sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{kernel_release}"/' .config

%build

# Building cumulative patch and patch lists.
touch {,not_}patched
for patch in %{patches}
do
    cve_number=$(basename "${patch%.*}")
    if [[ "$patch" == *.patch ]]
    then
        cat "$patch" >> %{livepatch_name}.patch
        echo "$cve_number" >> patched
    else
        echo -n "$cve_number: " >> not_patched
        cat "$patch" >> not_patched
    fi    
done

%if %{builds_module}
    kpatch-build -ddd \
        --sourcedir . \
        --vmlinux %{_libdir}/debug/lib/modules/%{kernel_full_version}/vmlinux \
        --name %{livepatch_name} \
        %{livepatch_name}.patch
%endif

%install
install -dm 755 %{buildroot}%{livepatch_install_dir}

install -m 744 *patched %{buildroot}%{livepatch_install_dir}

%if %{builds_module}
    install -m 744 %{livepatch_name}.ko %{buildroot}%{livepatch_module_path}
%endif

%post
if [[ -f "%{livepatch_module_path}" ]]
then
    kpatch load %{livepatch_module_path}
    kpatch install %{livepatch_module_path}
fi

%preun
if [[ -f "%{livepatch_module_path}" ]]
then
    kpatch uninstall %{livepatch_name}
    kpatch unload %{livepatch_name}
fi

%files
%defattr(-,root,root)
%{livepatch_install_dir}/not_patched
%{livepatch_install_dir}/patched
%if %{builds_module}
%{livepatch_module_path}
%endif

%changelog
* Wed Jun 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
- License verified.
