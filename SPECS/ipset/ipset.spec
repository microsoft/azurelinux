Summary:    administration tool for IP sets
Name:       ipset
Version:    7.1
Release:    2%{?dist}
License:    GPLv2
URL:        http://ipset.netfilter.org/
Source0:    http://ipset.netfilter.org/%{name}-%{version}.tar.bz2
Group:      System Environment/tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:    libmnl-devel
Requires:         libmnl
%description
IP sets are a framework inside the Linux kernel, which can be administered by the ipset utility. Depending on the type, an IP set may store IP addresses, networks, (TCP/UDP) port numbers, MAC addresses, interface names or combinations of them in a way, which ensures lightning speed when matching an entry against a set.

If you want to

store multiple IP addresses or port numbers and match against the collection by iptables at one swoop;
dynamically update iptables rules against IP addresses or ports without performance penalty;
express complex IP address and ports based rulesets with one single iptables rule and benefit from the speed of IP sets
then ipset may be the proper tool for you.

%package devel
Summary:    Development files for the ipset library
Group:      Development/Libraries
Requires:   ipset

%description devel
Libraries and header files for ipset.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --enable-static=no \
    --with-kmod=no
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%check
sed -i 's/tests=\"$tests nethash/#tests=\"$tests nethash/g' tests/runtest.sh
sed -i 's/tests=\"$tests hash:net,port/#tests=\"$tests hash:net,port/g' tests/runtest.sh
sed -i 's/tests=\"$tests hash:ip/#tests=\"$tests hash:ip/g' tests/runtest.sh
sed -i 's/tests=\"$tests hash:net,iface/#tests=\"$tests hash:net,iface/g' tests/runtest.sh
make tests |& tee %{_specdir}/%{name}-check-log || %{nocheck}


%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_libdir}/libipset.so.*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libipset.so
%{_libdir}/pkgconfig/libipset.pc

%changelog
* Sat May 09 00:20:42 PST 2020 Nick Samson <nisamson@microsoft.com> - 7.1-2
- Added %%license line automatically

*   Mon Mar 16 2020 Henry Beberman <henry.beberman@microsoft.com> 7.1-1
-   Update to 7.1. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 6.38-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 06 2018 Ankit Jain <ankitja@vmware.com> 6.38-1
-   Upgrading version to 6.38
*   Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 6.32-1
-   Upgrading version to 6.32
*   Wed Aug 3 2016 Xiaolin Li <xiaolinl@vmware.com> 6.29-1
-   Initial build.  First version
