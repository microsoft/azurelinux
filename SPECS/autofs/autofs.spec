%global debug_package %{nil}
Summary:        A kernel-based automounter for Linux
Name:           autofs
Version:        5.1.8
Release:        4%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Daemons
URL:            https://git.kernel.org/pub/scm/linux/storage/autofs/autofs.git/
Source0:        https://www.kernel.org/pub/linux/daemons/%{name}/v5/%{name}-%{version}.tar.xz
BuildRequires:  libtirpc-devel
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  systemd-devel
Requires:       libtirpc
Requires:       systemd

%description
Automounting is the process of automatically mounting and unmounting of file systems by a daemon. Autofs includes both a user-space daemon and code in the kernel that assists the daemon.

%prep
%autosetup

%build
%configure \
  --with-libtirpc
%make_build

%install
mkdir -p -m755 %{buildroot}/lib/systemd/system
mkdir -p -m755 %{buildroot}%{_sysconfdir}/auto.master.d
make install mandir=%{_mandir} INSTALLROOT=%{buildroot}
make install_samples INSTALLROOT=%{buildroot}
%make_build -C redhat
install -m 644 redhat/autofs.service  %{buildroot}/lib/systemd/system/autofs.service
rm -rf %{buildroot}%{_sysconfdir}/{init.d,rc.d}

#%check
#This package does not come with a test suite.

%post
%systemd_post autofs.service

%postun
%systemd_postun_with_restart autofs.service

%preun
%systemd_preun autofs.service

%files
%defattr(-,root,root)
%license COPYING
%config(noreplace) %{_sysconfdir}/auto.master
%config(noreplace) %{_sysconfdir}/auto.misc
%config(noreplace) %{_sysconfdir}/auto.net
%config(noreplace) %{_sysconfdir}/auto.smb
%config(noreplace) %{_sysconfdir}/autofs.conf
%config(noreplace) %{_sysconfdir}/sysconfig/autofs
%config(noreplace) %{_sysconfdir}/autofs_ldap_auth.conf
%{_sbindir}/automount
%{_libdir}/autofs/*
%{_libdir}/libautofs.so
%dir %{_sysconfdir}/auto.master.d
%{_mandir}/man5/*
%{_mandir}/man8/*
/lib/systemd/system/autofs.service

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.1.8-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Jan 26 2022 Olivia Crain <oliviacrain@microsoft.com> - 5.1.8-3
- Wipe buildroot's /etc/init.d in addition to /etc/rc.d
- Use systemd-devel BR so systemd is properly detected
- Lint spec

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.1.8-2
- Removing the explicit %%clean stage.

* Wed Nov 10 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 5.1.8-1
- Upgrade to version 5.1.8
- License verified

* Wed May 13 2020 Nick Samson <nisamson@microsoft.com> - 5.1.4-6
- Added %%license line automatically

* Tue May 12 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 5.1.4-5
- Undo specific changes for Docker build.

* Thu Apr 30 2020 Andrew Phelps <anphel@microsoft.com> - 5.1.4-4
- Modify to build in Docker based environment.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 5.1.4-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> - 5.1.4-2
- Use rpcsvc-proto and libtirpc

* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> - 5.1.4-1
- Update version to 5.1.4

* Thu Jul 06 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.1.3-1
- Initial build. First version
