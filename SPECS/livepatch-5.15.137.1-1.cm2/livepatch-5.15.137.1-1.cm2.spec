%define kernel_version_release 5.15.137.1-1.cm2
%define kernel_version %(echo %{kernel_version_release} | grep -oP "^[^-]+")
%define kernel_release %(echo %{kernel_version_release} | grep -oP "(?<=-).+")

%define builds_module %([[ -n "$(echo "%{patches}" | grep -oP "CVE-\\d+-\\d+(?=\\.patch)")" ]] && echo 1 || echo 0)

%define kpatch_logs_file /root/.kpatch/build.log

# Kpatch module names allow only alphanumeric characters and '_'.
%define livepatch_name %(value="%{name}-%{version}-%{release}"; echo "${value//[^a-zA-Z0-9_]/_}")
%define livepatch_install_dir %{_libdir}/livepatching/%{kernel_version_release}
%define livepatch_module_name %{livepatch_name}.ko
%define livepatch_module_path %{livepatch_install_dir}/%{livepatch_module_name}

%define patch_applicable_for_kernel [[ -f "%{livepatch_module_path}" && "$(uname -r)" == "%{kernel_version_release}" ]]
%define patch_installed kpatch list | grep -qP "%{livepatch_name}.*%{kernel_version_release}"
%define patch_loaded    kpatch list | grep -qP "%{livepatch_name}.*enabled"

# Install patch if the RUNNING kernel matches.
# No-op for initial (empty) livepatch.
%define install_if_should \
if %{patch_applicable_for_kernel} && ! %{patch_installed} \
then \
    kpatch install %{livepatch_module_path} \
fi

# Load patch, if the RUNNING kernel matches.
# No-op for initial (empty) livepatch.
%define load_if_should \
if %{patch_applicable_for_kernel} && ! %{patch_loaded} \
then \
    kpatch load %{livepatch_module_path} \
fi

%define uninstall_if_should \
if %{patch_installed} \
then \
    kpatch uninstall %{livepatch_name} \
fi

%define unload_if_should \
if %{patch_loaded} \
then \
    kpatch unload %{livepatch_name} \
fi

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
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/microsoft/CBL-Mariner
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-2/%{kernel_version}.tar.gz#/kernel-%{kernel_version}.tar.gz
Source1:        config-%{kernel_version_release}
Source2:        mariner-%{kernel_version_release}.pem

ExclusiveArch:  x86_64

Provides:       livepatch = %{kernel_version_release}

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

Requires:       coreutils
Requires:       livepatching-filesystem

Requires(post): coreutils
Requires(post): kpatch

Requires(preun): kpatch

%description
A set of kernel livepatches addressing CVEs present in Mariner's
%{kernel_version_release} kernel.
%{patches_description}

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

if ! kpatch-build -ddd \
    --sourcedir . \
    --vmlinux %{_libdir}/debug/lib/modules/%{kernel_version_release}/vmlinux \
    --name %{livepatch_name} \
    $all_patches_file
then
    echo "ERROR: failed to build livepatch module. Logs from '%{kpatch_logs_file}':" >&2
    cat "%{kpatch_logs_file}" >&2
    exit 1
fi

%install
install -dm 755 %{buildroot}%{livepatch_install_dir}
install -m 744 %{livepatch_module_name} %{buildroot}%{livepatch_module_path}

%post
%load_if_should
%install_if_should

%preun
%uninstall_if_should
%unload_if_should

# Re-enable patch on rollbacks to supported kernel.
%triggerin -- kernel = %{kernel_version_release}
%load_if_should
%install_if_should

# Prevent the patch from being loaded after a reboot to a different kernel.
# Previous kernel is still running, do NOT unload the livepatch.
%triggerin -- kernel > %{kernel_version_release}, kernel < %{kernel_version_release}
%uninstall_if_should

%files
%defattr(-,root,root)
%dir %{livepatch_install_dir}
%{livepatch_module_path}

# else builds_module
%else
%global debug_package %{nil}

%description
Empty package enabling subscription to future kernel livepatches
addressing CVEs present in Mariner's %{kernel_version_release} kernel.

%files

# endif builds_module
%endif

%changelog
* Fri Nov 10 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
- License verified.
