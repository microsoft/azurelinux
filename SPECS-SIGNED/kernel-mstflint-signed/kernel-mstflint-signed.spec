%global debug_package %{nil}
# The default %%__os_install_post macro ends up stripping the signatures off of the kernel module.
%define __os_install_post %{__os_install_post_leave_signatures} %{nil}
%define mstflint_unsigned_name kernel-mstflint
%define mstflint_module_name mstflint_access.ko
%define ub_kver 5.16.0
%define lb_kver 5.15.0

Summary:        Mellanox firmware burning tool
Name:           %{mstflint_unsigned_name}-signed
Version:        4.21.0
Release:        4%{?dist}
License:        Dual BSD/GPL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
URL:            https://github.com/Mellanox/%{name}
Source0:        https://github.com/Mellanox/%{name}/releases/download/v%{version}-1/%{name}-%{version}-1.tar.gz#/%{mstflint_module_name}
BuildRequires:  kernel-headers >= %{lb_kver}
BuildRequires:  kernel-headers < %{ub_kver}

%global kver %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' kernel-headers)
%global install_mod_dir %{_libdir}/modules/%{kver}/extra/%{mstflint_unsigned_name}

%description
This package contains the mstflint kernel module signed with the production key

%package -n %{mstflint_unsigned_name}
Summary:        mstflint Kernel Modules
Group:          System Environment/Kernel
Requires:       kernel >= %{lb_kver}
Requires:       kernel < %{ub_kver}
Requires:       kmod
Requires(post): kmod
Requires(postun): kmod

%description -n %{mstflint_unsigned_name}
This package contains mstflint kernel module for secure boot.

%install
install -dm 755 %{buildroot}%{install_mod_dir}
install -m 644 %{SOURCE0} %{buildroot}%{install_mod_dir}

%post -n %{mstflint_unsigned_name}
depmod %{kver}

%postun -n %{mstflint_unsigned_name}
depmod %{kver}

%files -n %{mstflint_unsigned_name}
%defattr(-,root,root,-)
%{install_mod_dir}

%changelog
* Thu Mar 23 2023 Elaheh Dehghani <edehghani@microsoft.com> - 4.21.0-4
- Add mstflint driver for secure boot.
- Original version for CBL-Mariner.
- License verified.
