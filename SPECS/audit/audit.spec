%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Kernel Audit Tool
Name:           audit
Version:        3.0
Release:        14%{?dist}
Source0:        https://people.redhat.com/sgrubb/audit/%{name}-%{version}-alpha8.tar.gz
Patch0:         refuse-manual-stop.patch
License:        GPLv2+
Group:          System Environment/Security
URL:            https://people.redhat.com/sgrubb/audit/
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  krb5-devel
BuildRequires:  openldap
BuildRequires:  golang
BuildRequires:  libcap-ng-devel
BuildRequires:  swig
BuildRequires:  e2fsprogs-devel
BuildRequires:  systemd
Requires:       systemd
Requires:       krb5
Requires:       openldap
Requires:       libcap-ng
Requires:       gawk
Requires:       audit-libs

%description
The audit package contains the user space utilities for
storing and searching the audit records generate by
the audit subsystem in the Linux 2.6 kernel.

%package        libs
Summary:        Runtime libs
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}

%description    libs
Runtime libs

%package        devel
Summary:        The libraries and header files needed for audit development.
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}

%description    devel
The libraries and header files needed for audit development.

%package        python
Summary:        Python bindings for libaudit
License:        LGPLv2+
BuildRequires:  python2-devel
BuildRequires:  python2-libs
Requires:       %{name} = %{version}-%{release}
Requires:       python2

%description python
The audit-python package contains the python2 bindings for libaudit
and libauparse.

%package  -n    python3-audit
Summary:        Python3 bindings for libaudit
License:        LGPLv2+
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-audit
The python3-audit package contains the python2 bindings for libaudit
and libauparse.

%prep
%setup -q
%patch0 -p1

%build
./configure \
    --prefix=%{_prefix} \
    --exec_prefix=/usr \
    --sbindir=%{_sbindir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --with-python=yes \
    --with-python3=yes \
    --enable-gssapi-krb5=yes \
    --with-libcap-ng=yes \
    --with-aarch64 \
    --enable-zos-remote \
    --with-golang \
    --enable-systemd \
    --disable-static

make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/{etc/audit/plugins.d,etc/audit/rules.d}
mkdir -p %{buildroot}/%{_var}/opt/audit/log
mkdir -p %{buildroot}/%{_var}/log
mkdir -p %{buildroot}/%{_var}/spool/audit
ln -sfv %{_var}/opt/audit/log %{buildroot}/%{_var}/log/audit
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post  auditd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart auditd.service

%preun
%systemd_preun auditd.service

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/systemd/system/auditd.service
%{_libexecdir}/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%dir %{_var}/opt/audit/log
%{_var}/log/audit
%{_var}/spool/audit
%attr(750,root,root) %dir %{_sysconfdir}/audit
%attr(750,root,root) %dir %{_sysconfdir}/audit/rules.d
%attr(750,root,root) %dir %{_sysconfdir}/audit/plugins.d
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/auditd.conf
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/rules.d/audit.rules
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audit.rules
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audit-stop.rules
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/plugins.d/af_unix.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/plugins.d/syslog.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/plugins.d/audispd-zos-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/zos-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audisp-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/plugins.d/au-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/libaudit.conf

%files libs
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir}/golang/*
%{_includedir}/*.h
%{_mandir}/man3/*
/usr/share/aclocal/audit.m4

%files python
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-audit
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 3.0-14
-   Bump release to force rebuild with golang 1.16.15
*   Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 3.0-13
-   Bump release to force rebuild with golang 1.16.14
*   Tue Feb 01 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 3.0-12
-   chpebeni@microsoft.com, 3.0.6.2: Remove override so auditd starts by default.
*   Fri Jan 21 2022 Nick Samson <nisamson@microsoft.com> - 3.0-11
-   Removed libwrap support to remove dependency on finger
*   Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 3.0-10
-   Increment release for force republishing using golang 1.16.12
*   Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 3.0-9
-   Increment release for force republishing using golang 1.16.9
*   Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.0-8
-   Increment release to force republishing using golang 1.16.7.
*   Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 3.0-7
-   Increment release to force republishing using golang 1.15.13.
*   Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.0-6
-   Increment release to force republishing using golang 1.15.11.
*   Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 3.0-5
-   Increment release to force republishing using golang 1.15.
*   Thu May 14 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.0-4
-   Set "RefuseManualStop=no" in "auditd.service".
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.0-3
-   Added %%license line automatically
*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0-2
-   Renaming go to golang
*   Wed Mar 18 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0-1
-   Updated to version 3.0-alpha8. Subpackage licenses updated. 
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.8.4-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 3 2018 Keerthana K <keerthanak@vmware.com> 2.8.4-1
-   Updated to version 2.8.4.
*   Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  2.7.5-4
-   Fixed the log file directory structure
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.7.5-3
-   Disabled audit service by default
*   Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.5-2
-   Move python2 requires to python subpackage and added python3.
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.7.5-1
-   Version update.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-7
-   Moved man3 to devel subpackage.
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.5-6
-   Required krb5-devel.
*   Fri Jul 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-5
-   Add gawk requirement.
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-4
-   Fixed logic to restart the active services after upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-3
-   GA - Bump release of all rpms
*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-2
-   Fixing spec file to handle rpm upgrade scenario correctly
*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  2.5-1
-   Upgrade to 2.5
*   Fri Jan 29 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-4
-   Add directories for auditd service.
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-3
-   Change config file attributes.
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 2.4.4-2
-   Add systemd requirement.
*   Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.4.4-1
-   Initial version
