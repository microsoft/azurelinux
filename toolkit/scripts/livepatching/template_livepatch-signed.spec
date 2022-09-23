%global debug_package %{nil}

%define kernel_version_release @KERNEL_VERSION_RELEASE@
%define kernel_version %(echo %{kernel_version_release} | grep -oP "^[^-]+")
%define kernel_release %(echo %{kernel_version_release} | grep -oP "(?<=-).+")

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

Summary:        Set of livepatches for kernel %{kernel_version_release}
Name:           livepatch-%{kernel_version_release}
Version:        1.0.0
Release:        @RELEASE_TAG@
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/microsoft/CBL-Mariner
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-2/%{kernel_version}.tar.gz#/%{livepatch_module_name}

ExclusiveArch:  x86_64

Requires:       coreutils
Requires:       livepatching-filesystem

Requires(post): coreutils
Requires(post): kpatch

Requires(preun): kpatch

Provides:       livepatch = %{kernel_version_release}

%description
@DESCRIPTION@

%install
install -dm 755 %{buildroot}%{livepatch_install_dir}
install -m 744 %{SOURCE0} %{buildroot}%{livepatch_module_path}

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

@CHANGELOG@
