Summary:        RPC program number mapper
Name:           rpcbind
Version:        1.2.5
Release:        6%{?dist}
License:        BSD
URL:            http://nfsv4.bullopensource.org
Group:          Applications/Daemons
Source0:        http://downloads.sourceforge.net/rpcbind/%{name}-%{version}.tar.bz2
Source1:        rpcbind.service
Source2:        rpcbind.socket
Source3:        rpcbind.sysconfig
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  libtirpc-devel
BuildRequires:  systemd-devel
Requires:       libtirpc
Requires:       systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/userdel /usr/sbin/groupadd /usr/sbin/groupdel /bin/false
Requires(preun):/usr/sbin/userdel /usr/sbin/groupdel
Requires(post): /bin/chown

Provides:       portmap = %{version}-%{release}

%description
The rpcbind program is a replacement for portmap. It is required for import or export of Network File System (NFS) shared directories. The rpcbind utility is a server that converts RPC program numbers into universal addresses

%prep
%setup -q

%build
sed -i "/servname/s:rpcbind:sunrpc:" src/rpcbind.c
%configure \
            --enable-warmstarts \
            --disable-debug \
            --with-statedir=%{_localstatedir}/lib/rpcbind \
            --with-rpcuser=rpc
make

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_localstatedir}/lib/rpcbind
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/sysconfig
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m644 %{SOURCE3} %{buildroot}/etc/sysconfig/rpcbind

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable rpcbind.socket" > %{buildroot}%{_libdir}/systemd/system-preset/50-rpcbind.preset
echo "disable rpcbind.service" >> %{buildroot}%{_libdir}/systemd/system-preset/50-rpcbind.preset

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%config(noreplace) /etc/sysconfig/rpcbind
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/*
%dir %{_localstatedir}/lib/rpcbind
%{_unitdir}/*
%{_libdir}/systemd/system-preset/50-rpcbind.preset

%pre
getent group rpc >/dev/null || groupadd -f -g 31 -r rpc
if ! getent passwd rpc >/dev/null ; then
if ! getent passwd 31 >/dev/null ; then
    useradd -d /var/lib/rpcbind -g rpc -s /bin/false -u 31 rpc > /dev/null 2>&1
else
    useradd -d /var/lib/rpcbind -g rpc -s /bin/false rpc > /dev/null 2>&1
fi
fi
%preun
%systemd_preun rpcbind.service rpcbind.socket
if [ $1 -eq 0 ]; then
    userdel  rpc 2>/dev/null || :
    groupdel rpc 2>/dev/null || :
fi

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    chown -v root:sys /var/lib/rpcbind
fi
%systemd_post rpcbind.socket rpcbind.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rpcbind.service rpcbind.socket

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.2.5-6
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Sep 07 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.2.5-5
- Add portmap to provides

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.5-4
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.2.5-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.5-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Keerthana K <keerthanak@vmware.com> 1.2.5-1
-   Update to version 1.2.5
*   Tue Mar 06 2018 Xiaolin Li <xiaolinl@vmware.com> 0.2.4-5
-   Fix pre install script.
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 0.2.4-4
-   Remove coreutils from requires and use explicit tools for post actions
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  0.2.4-3
-   Disabled rpcbind service by default
*   Thu May 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.4-2
-   Fix CVE-2017-8779
*   Wed Apr 5 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.2.4-1
-   Updating to latest version
*   Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.2.3-9
-   add shadow and coreutils to requires
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  0.2.3-8
-   Change systemd dependency
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.2.3-7
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.2.3-6
-   GA - Bump release of all rpms
*   Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 0.2.3-5
-   Edit scriptlets.
*   Fri Feb 05 2016 Anish Swaminathan <anishs@vmware.com> 0.2.3-4
-   Add pre install scripts in the rpm
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 0.2.3-3
-   Edit scripts in the rpm
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  0.2.3-2
-   Add systemd to Requires and BuildRequires.
*   Tue Dec 8 2015 Divya Thaluru <dthaluru@vmware.com> 0.2.3-1
-   Initial build.  First version
