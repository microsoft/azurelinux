Summary:        Kernel Audit Tool
Name:           audit
Version:        3.1.2
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://people.redhat.com/sgrubb/audit/
Source0:        https://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
#Patch0:         refuse-manual-stop.patch
BuildRequires:  e2fsprogs-devel
BuildRequires:  krb5-devel
BuildRequires:  systemd-bootstrap-rpm-macros
BuildRequires:  swig
Requires:       %{name}-libs = %{version}-%{release}
Requires:       gawk
# Break circular dependency with systemd by using weak dependency tag 'Recommends'
# Systemd should always be installed in a running system
Recommends:     systemd

%description
The audit package contains the user space utilities for
storing and searching the audit records generate by
the audit subsystem in the Linux 2.6 kernel.

%package        libs
Summary:        Runtime libs
License:        LGPLv2+

%description    libs
Runtime libs

%package        devel
Summary:        The libraries and header files needed for audit development.
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}
Provides:       audit-libs-devel = %{version}-%{release}

%description    devel
The libraries and header files needed for audit development.

%package  -n    python3-audit
Summary:        Python3 bindings for libaudit
License:        LGPLv2+
BuildRequires:  python3-devel
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Provides:       audit-libs-python3 = %{version}-%{release}

%description -n python3-audit
The python3-audit package contains the python3 bindings for libaudit
and libauparse.

%prep
%setup -q
sed -i "s/RefuseManualStop=yes/RefuseManualStop=no/g" init.d/auditd.service

%build
./configure \
    --prefix=%{_prefix} \
    --exec_prefix=%{_prefix} \
    --sbindir=%{_sbindir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --with-python3=yes \
    --enable-gssapi-krb5=yes \
    --with-aarch64 \
    --disable-zos-remote \
    --enable-systemd \
    --disable-static

%make_build

%install
mkdir -p %{buildroot}/{etc/audit/plugins.d,etc/audit/rules.d}
mkdir -p %{buildroot}/%{_var}/log
mkdir -p %{buildroot}/%{_var}/log/audit
mkdir -p %{buildroot}/%{_var}/spool/audit
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build check

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
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/systemd/system/auditd.service
%{_libexecdir}/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%dir %{_var}/log/audit
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
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audisp-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/plugins.d/au-remote.conf
%{_datadir}/%{name}/sample-rules/*

%files libs
%license COPYING
%{_libdir}/*.so.*
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/libaudit.conf

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_mandir}/man3/*
%{_datadir}/aclocal/audit.m4

%files -n python3-audit
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Nov 08 2023 Andrew Phelps <anphel@microsoft.com> - 3.1.2-1
- Upgrade to version 3.1.2

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.0.6-8
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Jun 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.0.6-7
- Remove requirement on base package from libs subpackage
- Move %%{_sysconfdir}/libaudit.conf to libs subpackage

* Mon Apr 25 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.0.6-6
- Add BR on systemd-bootstrap-rpm-macros for correctness

* Wed Apr 20 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.0.6-5
- Return audit logs to their normal location without the use of a symlink

* Tue Mar 15 2022 Andrew Phelps <anphel@microsoft.com> - 3.0.6-4
- Break circular dependency with systemd by using Recommends

* Fri Mar 04 2022 Andrew Phelps <anphel@microsoft.com> - 3.0.6-3
- Reduce build requirements to build in toolchain environment

* Mon Jan 31 2022 Chris PeBenito <chpebeni@microsoft.com> - 3.0.6-2
- Remove override so auditd starts by default.

* Fri Dec 10 2021 Chris Co <chrco@microsoft.com> - 3.0.6-1
- Update to 3.0.6

* Thu Nov 11 2021 Thomas Crain <thcrain@microsoft.com> - 3.0-8
- Remove tcp_wrappers dependency due to package removal
- License verified

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 3.0-7
- Remove libtool archive files from final packaging

* Wed Aug 18 2021 Thomas Crain <thcrain@microsoft.com> - 3.0-6
- Remove python2 subpackage

* Mon Nov 02 2020 Joe Schmitt <joschmit@microsoft.com> - 3.0-5 (from dev branch)
- Provide audit-libs-devel from the devel subpackage.
- Provide audit-libs-python3 from the python3 subpackage.

* Thu May 14 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.0-4
- Set "RefuseManualStop=no" in "auditd.service".

* Sat May 09 00:21:30 PST 2020 Nick Samson <nisamson@microsoft.com> - 3.0-3
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0-2
- Renaming go to golang

* Wed Mar 18 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0-1
- Updated to version 3.0-alpha8. Subpackage licenses updated.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.8.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 3 2018 Keerthana K <keerthanak@vmware.com> 2.8.4-1
- Updated to version 2.8.4.

* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  2.7.5-4
- Fixed the log file directory structure

* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.7.5-3
- Disabled audit service by default

* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.5-2
- Move python2 requires to python subpackage and added python3.

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.7.5-1
- Version update.

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-7
- Moved man3 to devel subpackage.

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.5-6
- Required krb5-devel.

* Fri Jul 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-5
- Add gawk requirement.

* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-4
- Fixed logic to restart the active services after upgrade

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-3
- GA - Bump release of all rpms

* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-2
- Fixing spec file to handle rpm upgrade scenario correctly

* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  2.5-1
- Upgrade to 2.5

* Fri Jan 29 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-4
- Add directories for auditd service.

* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-3
- Change config file attributes.

* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 2.4.4-2
- Add systemd requirement.

* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.4.4-1
- Initial version
