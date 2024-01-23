Summary:        NFS client utils
Name:           nfs-utils
Version:        2.5.4
Release:        4%{?dist}
License:        MIT and GPLv2 and GPLv2+ and BSD
URL:            https://linux-nfs.org/
Group:          Applications/Nfs-utils-client
Source0:        https://www.kernel.org/pub/linux/utils/nfs-utils/%{version}/%{name}-%{version}.tar.xz
Source1:        nfs-client.service
Source2:        nfs-client.target
Source3:        rpc-statd.service
Source4:        rpc-statd-notify.service
Source5:        nfs-utils.defaults
Source6:        nfs-server.service
Source7:        nfs-mountd.service
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  libtool
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libtirpc-devel
BuildRequires:  python3-devel
BuildRequires:  libevent-devel
BuildRequires:  device-mapper-devel
BuildRequires:  systemd-devel
BuildRequires:  keyutils-devel
BuildRequires:  sqlite
BuildRequires:  sqlite-devel
BuildRequires:  libgssglue-devel
BuildRequires:  e2fsprogs-devel
Requires:       libnfsidmap
Requires:       libtirpc
Requires:       rpcbind
Requires:       shadow-utils
Requires:       python3-libs
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

%description
The nfs-utils package contains simple nfs client service

%package -n libnfsidmap
Summary:       NFSv4 User and Group ID Mapping Library
License:       BSD

%description -n libnfsidmap
When NFSv4 is using AUTH_GSS (which currently only supports Kerberos v5), the
NFSv4 server mapping functions MUST use secure communications.

We provide several mapping functions, configured using /etc/idmapd.conf

As of the 0.21 version of this library, mapping methods are separate
dynamically-loaded libaries.  This allows the separation of any
LDAP requirements from the main libnfsidmap library.  The main library
now basically loads and calls the functions in the method-specific
libaries.  The method libraries are expected to be named
"libnfsidmap_<method>.so", for example, "libnfsidmap_nsswitch.so".

Several methods may be specified in the /etc/idmapd.conf configuration
file.  Each method is called until a mapping is found.


%package -n libnfsidmap-devel
Summary:     Development libraries for the libnfsidmap library
Requires:    libnfsidmap = %{version}-%{release}

%description -n libnfsidmap-devel
%{summary}.

%prep
%setup -q -n %{name}-%{version}
#not prevent statd to start
sed -i "/daemon_init/s:\!::" utils/statd/statd.c
sed '/unistd.h/a#include <stdint.h>' -i support/nsm/rpc.c
# fix --with-rpcgen=internal
sed -i 's/RPCGEN_PATH" =/rpcgen_path" =/' configure

%build
./configure --prefix=%{_prefix}         \
            --sysconfdir=%{_sysconfdir} \
            --enable-libmount-mount     \
            --without-tcp-wrappers      \
            --enable-gss                \
            --enable-nfsv4              \
            --with-rpcgen=internal      \
            --disable-static

# fix building against new gcc
sed -i 's/-Werror=strict-prototypes/-Wno-error=strict-prototypes/' support/nsm/Makefile
sed -i 's/CFLAGS = -g/CFLAGS = -Wno-error=strict-prototypes/' support/nsm/Makefile
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -v -m644 utils/mount/nfsmount.conf /etc/nfsmount.conf

mkdir -p %{buildroot}/lib/systemd/system/
mkdir -p %{buildroot}/etc/default
mkdir -p %{buildroot}/etc/export.d
mkdir -p %{buildroot}/var/lib/nfs/v4recovery
touch %{buildroot}/etc/exports

install -m644 %{SOURCE1} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE2} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE3} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE4} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE5} %{buildroot}/etc/default/nfs-utils
install -m644 %{SOURCE6} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE7} %{buildroot}/lib/systemd/system/
install -m644 systemd/proc-fs-nfsd.mount %{buildroot}/lib/systemd/system/
install -m644 systemd/nfs-idmapd.service %{buildroot}/lib/systemd/system/
install -m644 systemd/rpc_pipefs.target  %{buildroot}/lib/systemd/system/
install -m644 systemd/var-lib-nfs-rpc_pipefs.mount  %{buildroot}/lib/systemd/system/
install -m644 systemd/rpc-svcgssd.service %{buildroot}/lib/systemd/system/
find %{buildroot}/%{_libdir} -name '*.la' -delete

install -vdm755 %{buildroot}/usr/lib/systemd/system-preset
echo "disable nfs-server.service" > %{buildroot}/usr/lib/systemd/system-preset/50-nfs-server.preset

%check
#ignore test that might require additional setup
sed -i '/check_root/i \
exit 77' tests/t0001-statd-basic-mon-unmon.sh
make check

%pre
if ! getent group nobody >/dev/null; then
    groupadd -r -g 65534 nobody
fi
if ! getent passwd nobody >/dev/null; then
    useradd -g named -u 65534 -s /bin/false -M -r nobody
fi

%post
/sbin/ldconfig
%systemd_post nfs-server.service

%preun
%systemd_preun nfs-server.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart nfs-server.service

%files
%defattr(-,root,root)
%license COPYING
%{_datadir}/*
%exclude /usr/bin/rpcgen
/sbin/*
%{_sbindir}/*
%{_sharedstatedir}/*
%config(noreplace) /etc/default/nfs-utils
%config(noreplace) /etc/exports
/lib/systemd/system/*
%{_libdir}/systemd/system-preset/50-nfs-server.preset

%files -n libnfsidmap
%{_libdir}/libnfsidmap.so.*
%{_libdir}/libnfsidmap/*.so


%files -n libnfsidmap-devel
%{_libdir}/pkgconfig/libnfsidmap.pc
%{_includedir}/nfsidmap.h
%{_includedir}/nfsidmap_plugin.h
%{_libdir}/libnfsidmap.so

%changelog
* Wed Nov 01 2023 Andy Zaugg <azaugg@linkedin.com> - 2.5.4-4
- Fix post-install script to create nobody user instead of named user

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.5.4-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Nov 30 2021 Thomas Crain <thcrain@microsoft.com> - 2.5.4-2
- Remove python shebang line fixes (fixed upstream)

* Wed Nov 10 2021 Andrew Phelps <anphel@microsoft.com> - 2.5.4-1
- Update to version 2.5.4

* Wed Jun 03 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.3.3-8
- Fix format-security errors and re-disable -Werror=strict-prototypes

* Tue Jun 02 2020 Andrew Phelps <anphel@microsoft.com> - 2.3.3-7
- Add sqlite build requirement.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.3.3-6
- Added %%license line automatically

* Fri Apr 17 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.3.3-5
- Rename shadow to shadow-utils.

* Mon Apr 13 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.3.3-4
- Make libnfsidmap into a separate subpackage.
- Update Source0, URL and License.
- Verified License.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.3.3-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> - 2.3.3-2
- Fix compilation issue against glibc-2.28
- Use internal rpcgen, disable librpcsecgss dependency.

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 2.3.3-1
- Update to 2.3.3

* Thu Jun 07 2018 Anish Swaminathan <anishs@vmware.com> - 2.3.1-2
- Add noreplace qualifier to config files

* Fri Jan 26 2018 Xiaolin Li <xiaolinl@vmware.com> - 2.3.1-1
- Update to 2.3.1 and enable nfsv4

* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.1.1-7
- No direct toybox dependency, shadow depends on toybox

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.1.1-6
- Requires shadow or toybox

* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.1.1-5
- Fix compilation issue for glibc-2.26

* Wed Aug 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.1.1-4
- Add check and ignore test that fails.

* Tue Aug 8 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.1.1-3
- Alter nfs-server and nfs-mountd service files to use
- environment file and port opts.

* Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.1.1-2
- Build with python3.

* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.1.1-1
- Update to 2.1.1

* Fri Dec 16 2016 Nick Shi <nshi@vmware.com> - 1.3.3-6
- Requires rpcbind.socket upon starting rpc-statd service (bug 1668405)

* Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.3.3-5
- add shadow to requires

* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> - 1.3.3-4
- Removed packaging of debug files

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.3.3-3
- GA - Bump release of all rpms

* Thu Apr 28 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.3.3-2
- Add nfs-server.service to rpm.

* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.3.3-1
- Updated to version 1.3.3

* Tue Dec 8 2015 Divya Thaluru <dthaluru@vmware.com> - 1.3.2-2
- Adding systemd service files

* Tue Jul 14 2015 Rongrong Qiu <rqiu@vmware.com> - 1.3.2-1
- Initial build.  First version
