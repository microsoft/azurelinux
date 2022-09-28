%define kernel_version_release @KERNEL_VERSION_RELEASE@
%define kernel_version %(echo %{kernel_version_release} | grep -oP "^[^-]+")
%define kernel_release %(echo %{kernel_version_release} | grep -oP "(?<=-).+")

%define builds_module %([[ -n "$(echo "%{patches}" | grep -oP "CVE-\\d+-\\d+(?=\\.patch)")" ]] && echo 1 || echo 0)

# Kpatch module names allow only alphanumeric characters and '_'.
%define livepatch_name %(value="%{name}-%{version}-%{release}"; echo "${value//[^a-zA-Z0-9_]/_}")
%define livepatch_install_dir %{_libdir}/livepatching/%{kernel_version_release}
%define livepatch_module_name %{livepatch_name}.ko
%define livepatch_module_path %{livepatch_install_dir}/%{livepatch_module_name}

%define patches_description \
%(
    echo "Patches list ('*' - fixed, '!' - unfixable through livepatching, kernel update required):"
    for patch in %{patches}
    do
        patch_file=$(basename "$patch")

        cve_number="${patch_file%.*}"
        patch_suffix="${patch_file#*.}"

        if [ "$patch_suffix" = "patch" ]
        then
            echo "*$cve_number"
        else
            echo "\!$cve_number: $(cat "$patch")"
        fi
    done
)

Summary:        Set of livepatches for kernel %{kernel_version_release}
Name:           livepatch-%{kernel_version_release}
Version:        1.0.0
Release:        0%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/microsoft/CBL-Mariner
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-2/%{kernel_version}.tar.gz#/kernel-%{kernel_version}.tar.gz
Source1:        config-%{kernel_version_release}
Source2:        mariner-%{kernel_version_release}.pem
@PATCHES@

ExclusiveArch:  x86_64

# Must be kept below the "Patch" tags to correctly evaluate %%builds_module.
%if %{builds_module}
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
BuildRequires:  kernel-debuginfo = %{kernel_version_release}
BuildRequires:  kernel-headers = %{kernel_version_release}
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
%else
%global debug_package %{nil}
# endif builds_module
%endif

Provides:       livepatch = %{kernel_version_release}

%description
A set of kernel livepatches addressing CVEs present in Mariner's
kernel version %{kernel_version_release}.
%{patches_description}

%if %{builds_module}

%prep
%setup -q -n CBL-Mariner-Linux-Kernel-rolling-lts-mariner-2-%{kernel_version}

cp %{SOURCE1} .config
cp %{SOURCE2} certs/mariner.pem

sed -i 's#CONFIG_SYSTEM_TRUSTED_KEYS=""#CONFIG_SYSTEM_TRUSTED_KEYS="certs/mariner.pem"#' .config
sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{kernel_release}"/' .config

%build
# Building cumulative patch.
all_patches_file=all.patch
for patch in %{patches}
do
    [[ "$patch" == *.patch ]] && cat "$patch" >> $all_patches_file
done

kpatch-build -ddd \
    --sourcedir . \
    --vmlinux %{_libdir}/debug/lib/modules/%{kernel_version_release}/vmlinux \
    --name %{livepatch_name} \
    $all_patches_file

%install
install -dm 755 %{buildroot}%{livepatch_install_dir}
install -m 744 %{livepatch_module_name} %{buildroot}%{livepatch_module_path}

# endif builds_module
%endif

%files
%defattr(-,root,root)
%if %{builds_module}
%dir %{livepatch_install_dir}
%{livepatch_module_path}
%endif

%changelog