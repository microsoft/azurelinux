Summary:        C/C++ library for network traffic capture
Name:           libpcap
Version:        1.10.1
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Networking/Libraries
URL:            https://www.tcpdump.org/
#Source0:       https://github.com/the-tcpdump-group/%{name}/archive/%{name}-%{version}.tar.gz
Source0:        %{name}-%{name}-%{version}.tar.gz

%description
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%package        static
Summary:        Static lib for %{name}
Requires:       %{name}-devel = %{version}-%{release}

%description    static
This package contains static lib for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
%configure
make %{?_smp_mflags}

%check
make testprogs
testprogs/opentest
testprogs/findalldevstest


%install
make DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*-config
%{_includedir}/*.h
%{_includedir}/pcap
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files static
%{_libdir}/*.a

%changelog
* Wed Dec 13 2023 Zhichun Wan <zhichunwan@microsoft.com> - 1.10.1-2
- Add static library as sub package

* Wed Jan 12 2022 Henry Li <lihl@microsoft.com> - 1.10.1-1
- Upgrade to version 1.10.1

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.9.1-2
- Added %%license line automatically

*   Fri May 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.9.1-1
-   Bumping version up to 1.9.1 to fix following CVEs:
-       CVE-2019-15161,
-       CVE-2019-15162,
-       CVE-2019-15163,
-       CVE-2019-15164, and
-       CVE-2019-15165.
-   Fixed "Source0" and "URL" tags.
-   License verified.
-   Removing tabs and aligning changelog.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.9.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Nov 26 2018 Ashwin H <ashwinh@vmware.com> 1.9.0-2
-   Fix %check

*   Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 1.9.0-1
-   Update to 1.9.0
-   Split devel package

*   Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.1-1
-   Updated to version 1.8.1

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.4-2
-   GA - Bump release of all rpms

*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.4-1
-   Updated to version 1.7.4

*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 1.7.2-1
-   Version upgrade to 1.7.2

*   Wed Jan 21 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.2-1
-   Initial build. First version
