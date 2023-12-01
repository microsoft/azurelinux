%define majmin %(echo %{version} | cut -d. -f1-2)

Summary:        Intel LLDP Agent
Name:           lldpad
Version:        1.1.0
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Daemons
URL:            https://github.com/intel/openlldp
Source0:        https://github.com/intel/openlldp/archive/v%{majmin}.tar.gz#/openlldp-%{majmin}.tar.gz
BuildRequires:  flex-devel
BuildRequires:  kernel-headers
BuildRequires:  libconfig-devel
BuildRequires:  libnl3-devel
BuildRequires:  readline-devel
BuildRequires:  systemd-devel
Requires:       libconfig
Requires:       libnl3
Requires:       systemd

%description
The lldpad package comes with utilities to manage an LLDP interface with support for reading and configuring TLVs. TLVs and interfaces are individual controlled allowing flexible configuration for TX only, RX only, or TX/RX modes per TLV.

%prep
%autosetup -n openlldp-%{majmin}

%build
./bootstrap.sh
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mv %{buildroot}/%{_libdir}/systemd/system/lldpad.service \
    %{buildroot}/lib/systemd/system/lldpad.service
mv %{buildroot}/%{_libdir}/systemd/system/lldpad.socket  \
    %{buildroot}/lib/systemd/system/lldpad.socket

%preun
%systemd_preun lldpad.socket

%post
/sbin/ldconfig
%systemd_post lldpad.socket

%postun
/sbin/ldconfig
%systemd_postun_with_restart lldpad.socket

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_libdir}/liblldp_clif.so.*
%{_sysconfdir}/bash_completion.d/*
%dir %{_sharedstatedir}/%{name}
%{_mandir}/man3/*
%{_mandir}/man8/*
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/liblldp_clif.so
/lib/systemd/system/lldpad.service
/lib/systemd/system/lldpad.socket

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.1.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Nov 11 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.1.0-1
- Upgrade to latest upstream version

* Tue Jun 29 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.0.1-18
- Use libconfig-devel at build-time, rather than libconfig
- Lint spec, modernize with macros

* Thu Jun 18 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.1-17
- Removing runtime dependency on a specific kernel package.

* Thu Jun 11 2020 Christopher Co <chrco@microsoft.com> - 1.0.1-16
- Remove KERNEL_VERSION macro from BuildRequires

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.1-15
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.0.1-14
- Renaming linux-api-headers to kernel-headers

* Thu Apr 30 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.0.1-13
- Rename libnl to libnl3.

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.0.1-12
- Renaming linux to kernel

* Tue Apr 07 2020 Eric Li <eli@microsoft.com> - 1.0.1-11
- Fix Source0 URL and add Source0: comment to the working link. Verified license.

* Wed Mar 25 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0.1-10
- Disable warnings to build with GCC9. Fix Source0 URL.

* Mon Mar 23 2020 Christopher Co <chrco@microsoft.com> - 1.0.1-9
- Remove KERNEL_RELEASE macro from required packages

* Thu Jan 09 2020 Christopher Co <chrco@microsoft.com> - 1.0.1-8
- Update to work with Linux 5.4.23 kernel and headers
- Add patch to remove duplicate LLDP ethertype which was added to Linux headers in 5.3
- Updated URL
- Verified License

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.0.1-7
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Aug 13 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 1.0.1-6
- Suppress build warnings with gcc 7.3

* Wed May 25 2016 Anish Swaminathan <anishs@vmware.com> - 1.0.1-5
- Add required folder for service to start

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.1-4
- GA - Bump release of all rpms

* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> - 1.0.1-3
- Adding support in pre/post/un scripts for upgrade.

* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com> - 1.0.1-2
- Add systemd to Requires and BuildRequires.
- The source is based on git://open-lldp.org/open-lldp commit 036e314
- Use systemctl to enable/disable service.

* Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> - 1.0.1-1
- Initial build.  First version
