Summary:       xinetd -- A better inetd.
Name:          xinetd
Version:       2.3.15
Release:       13%{?dist}
License:       BSD
Group:         System Environment/Daemons
Vendor:        Microsoft Corporation
Distribution:  Mariner
URL:           https://github.com/xinetd-org/xinetd
#Source0:      https://github.com/xinetd-org/xinetd/archive/%{name}-2-3-15.tar.gz
Source0:       %{name}-%{version}.tar.gz
Source1:       xinetd.service
BuildRequires: systemd
BuildRequires: libtirpc-devel
Requires:      systemd
Requires:      libtirpc

%description
Xinetd is a powerful inetd replacement. Xinetd has access control
mechanisms, extensive logging capabilities, the ability to make
services available based on time, can place limits on the number
of servers that can be started, and has a configurable defence
mechanism to protect against port scanners, among other things.

%prep
%setup -q

%build
%configure \
	--sbindir=%{buildroot}/%{_sbindir} 	\
	--mandir=%{buildroot}/%{_datadir}/man
export LDFLAGS=-ltirpc CFLAGS=-I/usr/include/tirpc
%make_build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/etc/xinetd.d

%makeinstall
install -m 0600 contrib/xinetd.conf %{buildroot}/etc/
cp contrib/xinetd.d/* %{buildroot}/etc/xinetd.d
mkdir -p %{buildroot}/lib/systemd/system
cp %{SOURCE1} %{buildroot}/lib/systemd/system/xinetd.service

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable xinetd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-xinetd.preset

%post
%{_sbindir}/ldconfig
%systemd_post xinetd.service

%preun
%systemd_preun xinetd.service

%postun
%systemd_postun_with_restart xinetd.service

%files
%defattr(-, root, root)
%license COPYRIGHT
%doc CHANGELOG COPYRIGHT README xinetd/sample.conf contrib/empty.conf
%{_sbindir}/*
%{_datadir}/man/*/*
%attr(0750, root, root) %config(noreplace) /etc/xinetd.conf
%attr(0750, root, root) %config(noreplace) /etc/xinetd.d/*
/lib/systemd/system/xinetd.service
%{_libdir}/systemd/system-preset/50-xinetd.preset

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.15-13
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.3.15-12
- Added %%license line automatically

*   Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> 2.3.15-11
-   Update URL.
-   Update Source0 with valid URL.
-   Remove sha1 macro.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.3.15-10
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 2.3.15-9
-   Use libtirpc
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 2.3.15-8
-   Use standard configure macros
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.3.15-7
-   Disabled xinetd service by default
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.3.15-6
-   Fixed logic to restart the active services after upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.15-5
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.15-4
-   Fix upgrade issues
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  2.3.15-3
-   Add systemd to Requires and BuildRequires.
*   Thu Dec 03 2015 Xiaolin Li  <xiaolinl@vmware.com> 2.3.15-2
-   Remove rc files
*   Fri Aug 07 2015 Xiaolin Li  <xiaolinl@vmware.com> 2.3.15-1
-   Add xinetd library to photon
*   Sun Sep 07 2003 Steve Grubb <linux_4ever@yahoo.com>
-   Refined installation and added services.
