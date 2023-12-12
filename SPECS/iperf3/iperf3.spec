Summary:        A network performance benchmark tool.
Name:           iperf3
Version:        3.14
Release:        2%{?dist}
License:        BSD and MIT and Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/esnet/iperf
Source0:        https://github.com/esnet/iperf/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch1:         disablepg.patch
BuildRequires:  autoconf >= 2.71
BuildRequires:  automake

%description
ipref is a network performance measurement tool that can measure the maximum
achievable network bandwidth on IP networks. It supports tuning of various
parameters related to timing, protocols, and buffers.  For each test it
reports the bandwidth, loss, and other parameters.

%package        doc
Summary:        Documentation for iperf

%description    doc
It contains the documentation and manpages for iperf package.
Requires:       %{name} = %{version}-%{release}

%prep
%autosetup -p1 -n iperf-%{version}

%build
echo "VDBG optflags: " %{optflags}
./bootstrap.sh
./configure \
        CFLAGS="%{optflags}" \
        CXXFLAGS="%{optflags}" \
        --disable-silent-rules \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --datadir=%{_datarootdir} \
        --sysconfdir=%{_sysconfdir}
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/iperf3
%{_includedir}/iperf_api.h
%{_libdir}/libiperf.*

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/iperf3.1.gz
%{_mandir}/man3/libiperf.3.gz

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.14-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Aug 01 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.14-1
- Updating to 3.14 to fix CVE-2023-38403.

* Tue Mar 15 2022 Rachel Menge <rachelmenge@microsoft.com> - 3.11-1
- Update to 3.11

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.6-5
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 3.6-4
- Renaming iperf to iperf3

* Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6-3
- Fixed "Source0" tag.
- License verified and "License" tag updated.
- Fixed changelog spacing.
- Removed "%%define sha1".

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 05 2018 Ankit Jain <ankitja@vmware.com> 3.6-1
- Upgraded to version 3.6

* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.1.7-1
- Upgraded to version 3.1.7

* Thu Oct 6 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.3-1
- Upgraded to version 3.1.3

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.2-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  3.1.2-1
- Upgrade to 3.1.2

* Wed Oct 28 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-1
- Add iperf v3.1 package.
