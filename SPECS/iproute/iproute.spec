Summary:        Basic and advanced IPV4-based networking
Name:           iproute
Version:        6.7.0
Release:        1%{?dist}
License:        GPLv2
URL:            https://www.kernel.org/pub/linux/utils/net/iproute2
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.kernel.org/pub/linux/utils/net/iproute2/%{name}2-%{version}.tar.xz
Patch0:         replace_killall_by_pkill.patch
BuildRequires:  gcc
BuildRequires:  elfutils-libelf-devel
BuildRequires:  libselinux-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  libmnl-devel
BuildRequires:  sudo
Requires:       elfutils-libelf
Requires:       libselinux

%description
The IPRoute2 package contains programs for basic and advanced
IPV4-based networking.

%package        devel
Summary:        Header files for building application using iproute2.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains the header files for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n %{name}2-%{version}
sed -i /ARPD/d Makefile
sed -i 's/arpd.8//' man/man8/Makefile
sed -i 's/m_ipt.o//' tc/Makefile
%patch0 -p1

%build
# Not an autoconf configure file
%configure
%make_build

%install
%make_install

%check
# Fix linking issue in testsuite
sed -i 's/<libnetlink.h>/\"..\/..\/include\/libnetlink.h\"/g' tools/generate_nlmsg.c
sed -i 's/\"libnetlink.h\"/"..\/include\/libnetlink.h\"/g' ../lib/libnetlink.c
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/iproute2/*
/sbin/*
%{_libdir}/tc/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_datadir}/bash-completion/completions/*

%files devel
%defattr(-,root,root)
%{_includedir}/iproute2/bpf_elf.h
%{_mandir}/man3/*

%changelog
* Mon Feb 05 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 6.7.0-1
- Update libvirt to v6.7.0

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
