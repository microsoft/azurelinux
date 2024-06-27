Summary:        Basic and advanced IPV4-based networking
Name:           iproute
Version:        6.7.0
Release:        2%{?dist}
License:        GPLv2
URL:            https://www.kernel.org/pub/linux/utils/net/iproute2
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://www.kernel.org/pub/linux/utils/net/iproute2/%{name}2-%{version}.tar.xz

BuildRequires:      bison
BuildRequires:      elfutils-libelf-devel
BuildRequires:      flex
BuildRequires:      gcc
BuildRequires:      iptables-devel >= 1.4.5
BuildRequires:      libbpf-devel
BuildRequires:      libcap-devel
BuildRequires:      libmnl-devel
BuildRequires:      libselinux-devel
BuildRequires:      make
BuildRequires:      pkgconfig
Requires:           libbpf
Requires:           psmisc
Provides:           /sbin/ip
	
%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
kernel.
 
%package tc
Summary:            Linux Traffic Control utility
License:            GPL-2.0-or-later
Requires:           %{name}%{?_isa} = %{version}-%{release}
Provides:           /sbin/tc
 
%description tc
The Traffic Control utility manages queueing disciplines, their classes and
attached filters and actions. It is the standard tool to configure QoS in
Linux.
 
%if ! 0%{?_module_build}
%package doc
Summary:            Documentation for iproute2 utilities with examples
%if 0%{?rhel}
Group:              Applications/System
%endif
License:            GPL-2.0-or-later
Requires:           %{name} = %{version}-%{release}
 
%description doc
The iproute documentation contains howtos and examples of settings.
%endif
 
%package devel
Summary:            iproute development files
License:            GPL-2.0-or-later
Requires:           %{name} = %{version}-%{release}
Provides:           iproute-static = %{version}-%{release}
 
%description devel
The libnetlink static library.
 
%prep
%autosetup -p1 -n %{name}2-%{version}
 
%build
%configure --libdir %{_libdir}
echo -e "\nPREFIX=%{_prefix}\nCONFDIR:=%{_sysconfdir}/iproute2\nSBINDIR=%{_sbindir}" >> config.mk
%make_build

%install
%make_install
echo '.so man8/tc-cbq.8' > %{buildroot}%{_mandir}/man8/cbq.8
 
# libnetlink
install -D -m644 include/libnetlink.h %{buildroot}%{_includedir}/libnetlink.h
install -D -m644 lib/libnetlink.a %{buildroot}%{_libdir}/libnetlink.a
 
# drop these files, iproute-doc package extracts files directly from _builddir
rm -rf '%{buildroot}%{_docdir}'
 
# append deprecated values to rt_dsfield for compatibility reasons
%if 0%{?rhel} && ! 0%{?eln}
# cat %{SOURCE1} >>%{buildroot}%{_datadir}/iproute2/rt_dsfield
%endif
 
%files
%dir %{_datadir}/iproute2
%license COPYING
%doc README README.devel
%{_mandir}/man7/*
%exclude %{_mandir}/man7/tc-*
%{_mandir}/man8/*
%exclude %{_mandir}/man8/tc*
%exclude %{_mandir}/man8/cbq*
%attr(644,root,root) %config(noreplace) %{_datadir}/iproute2/*
%{_sbindir}/*
%exclude %{_sbindir}/tc
%exclude %{_sbindir}/routel
%{_datadir}/bash-completion/completions/devlink
 
%files tc
%license COPYING
%{_mandir}/man7/tc-*
%{_mandir}/man8/tc*
%{_mandir}/man8/cbq*
%dir %{_libdir}/tc/
%{_libdir}/tc/*
%{_sbindir}/tc
%{_datadir}/bash-completion/completions/tc
 
%if ! 0%{?_module_build}
%files doc
%license COPYING
%doc examples
%endif
 
%files devel
%license COPYING
%{_mandir}/man3/*
%{_libdir}/libnetlink.a
%{_includedir}/libnetlink.h
%{_includedir}/iproute2/bpf_elf.h
 
%changelog
* Fri Jun 07 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.7.0-2
- Remove dependency on 'libdb'.

* Mon Feb 05 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 6.7.0-1
- Update libvirt to v6.7.0
- Use Fedora 39 as basis for new packaging (tc)
- use _datadir rather than _libdir for iproute2 files

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.15.0-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Feb 02 2022 Muhammad Falak <mwani@microsoft.com> - 5.15.0-2
- Add an explict BR on 'sudo' & 'libmnl-devel' to enable check section

* Mon Nov 29 2021 Thomas Crain <thcrain@microsoft.com> - 5.15.0-1
- Upgrade to latest upstream version
- Add relevant build/runtime requirements
- Fix check section instructions for new version

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.18.0-5
- Added %%license line automatically

* Mon Apr 13 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.18.0-4
- Rename to iproute.
- Updated Source0 and URL.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.18.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Mar 08 2019 Fabio Rapposelli <fabio@vmware.com> - 4.18.0-2
- Added "Provides: iproute" for better compatibility with other distributions

* Wed Sep 05 2018 Ankit Jain <ankitja@vmware.com> - 4.18.0-1
- Updated to version 4.18.0

* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.10.0-3
- Fix compilation issue for glibc-2.26

* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.10.0-2
- Move man3 to devel package.

* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> - 4.10.0-1
- Updated to version 4.10.0

* Thu Jun 16 2016 Nick Shi <nshi@vmware.com> - 4.2.0-3
- Replace killall by pkill in ifcfg

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.2.0-2
- GA - Bump release of all rpms

* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.2.0-1
- Updated to version 4.2.0

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 3.12.0-1
- Initial build. First version
