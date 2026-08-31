# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Conditionals
# Invoke "rpmbuild --without <feature>" or "rpmbuild --with <feature>"
# to disable or enable specific features
%bcond_without userflags
%bcond_with runautogen

Name: corosync-qdevice
Summary: The Corosync Cluster Engine Qdevice
Version: 3.0.4
Release: 1%{?dist}
License: BSD-3-Clause
URL: https://github.com/corosync/corosync-qdevice
Source0: https://github.com/corosync/corosync-qdevice/releases/download/v%{version}/%{name}-%{version}.tar.gz

# Runtime bits
Requires: corosync >= 2.4.0
Requires: corosynclib >= 2.4.0
Requires: nss-tools

%{?systemd_requires}
BuildRequires: systemd
BuildRequires: systemd-devel

# Build bits
BuildRequires: gcc
BuildRequires: corosynclib-devel
BuildRequires: libqb-devel
BuildRequires: sed
BuildRequires: groff
BuildRequires: nss-devel

%if %{with runautogen}
BuildRequires: autoconf automake libtool
%endif
BuildRequires: make
BuildRequires: git

%prep
%autosetup -S git_am

%build
%if %{with runautogen}
./autogen.sh
%endif

%{configure} \
%if %{with userflags}
	--enable-user-flags \
%endif
	--enable-systemd \
	--enable-qdevices \
	--enable-qnetd \
	--with-initddir=%{_initrddir} \
	--with-systemddir=%{_unitdir} \
	--docdir=%{_docdir}

%make_build

%install
%make_install

## tree fixup
# drop docs and html docs for now
rm -rf %{buildroot}%{_docdir}/*
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
# /etc/sysconfig/corosync-qdevice
install -p -m 644 init/corosync-qdevice.sysconfig.example \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync-qdevice
# /etc/sysconfig/corosync-qnetd
install -p -m 644 init/corosync-qnetd.sysconfig.example \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync-qnetd

sed -i -e 's/^#User=/User=/' \
   %{buildroot}%{_unitdir}/corosync-qnetd.service

install -m0644 -D init/corosync-qnetd.sysusers.conf.example %{buildroot}%{_sysusersdir}/corosync-qnetd.conf

%description
This package contains the Corosync Cluster Engine Qdevice, script for creating
NSS certificates and an init script.

%post
%systemd_post corosync-qdevice.service

%preun
%systemd_preun corosync-qdevice.service

%postun
%systemd_postun corosync-qdevice.service

%files
%license LICENSE
%dir %{_sysconfdir}/corosync/qdevice
%dir %config(noreplace) %{_sysconfdir}/corosync/qdevice/net
%dir %{_localstatedir}/run/corosync-qdevice
%{_sbindir}/corosync-qdevice
%{_sbindir}/corosync-qdevice-net-certutil
%{_sbindir}/corosync-qdevice-tool
%config(noreplace) %{_sysconfdir}/sysconfig/corosync-qdevice
%{_unitdir}/corosync-qdevice.service
%{_mandir}/man8/corosync-qdevice-tool.8*
%{_mandir}/man8/corosync-qdevice-net-certutil.8*
%{_mandir}/man8/corosync-qdevice.8*

%package -n corosync-qdevice-devel
Summary: The Corosync Cluster Engine Qdevice Network Development Kit
Requires: pkgconfig

%description -n corosync-qdevice-devel
This package contains files used to develop using
The Corosync Cluster Engine Qdevice

%files -n corosync-qdevice-devel
%license LICENSE
%{_datadir}/pkgconfig/corosync-qdevice.pc

%package -n corosync-qnetd
Summary: The Corosync Cluster Engine Qdevice Network Daemon
Requires: nss-tools

%{?systemd_requires}

%description -n corosync-qnetd
This package contains the Corosync Cluster Engine Qdevice Network Daemon,
script for creating NSS certificates and an init script.


%post -n corosync-qnetd
%systemd_post corosync-qnetd.service

%preun -n corosync-qnetd
%systemd_preun corosync-qnetd.service

%postun -n corosync-qnetd
%systemd_postun corosync-qnetd.service

%files -n corosync-qnetd
%license LICENSE
%dir %config(noreplace) %attr(770, coroqnetd, coroqnetd) %{_sysconfdir}/corosync/qnetd
%dir %attr(770, coroqnetd, coroqnetd) %{_localstatedir}/run/corosync-qnetd
%{_bindir}/corosync-qnetd
%{_bindir}/corosync-qnetd-certutil
%{_bindir}/corosync-qnetd-tool
%config(noreplace) %{_sysconfdir}/sysconfig/corosync-qnetd
%{_unitdir}/corosync-qnetd.service
%{_mandir}/man8/corosync-qnetd-tool.8*
%{_mandir}/man8/corosync-qnetd-certutil.8*
%{_mandir}/man8/corosync-qnetd.8*
%{_sysusersdir}/corosync-qnetd.conf

%changelog
* Tue Nov 25 2025 Jan Friesse <jfriesse@redhat.com> - 3.0.4-1
- New upstream release

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Jan Friesse <jfriesse@redhat.com> - 3.0.3-9
- Change sysusers.d config file name to corosync-qnetd.conf
- Remove support for non-systemd builds

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.3-8
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 06 2023 Jan Friesse <jfriesse@redhat.com> - 3.0.3-2
- migrated to SPDX license

* Wed Mar 22 2023 Jan Friesse <jfriesse@redhat.com> - 3.0.3-1
- New upstream release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 03 2022 Jan Friesse <jfriesse@redhat.com> - 3.0.2-1
- New upstream release

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Jan Friesse <jfriesse@redhat.com> - 3.0.1-1
- New upstream release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Jan Friesse <jfriesse@redhat.com> - 3.0.0-9
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed May 13 2020 Jan Friesse <jfriesse@redhat.com> - 3.0.0-8
- Really rebuild for the new libqb

* Wed May 13 2020 Jan Friesse <jfriesse@redhat.com> - 3.0.0-7
- Rebuild for new libqb

* Thu Mar 26 2020 Jan Friesse <jfriesse@redhat.com> - 3.0.0-6
- Add CI tests
- Enable gating

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Jan Friesse <jfriesse@redhat.com> - 3.0.0-3
- Add license and use install -p

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Jan Friesse <jfriesse@redhat.com> - 3.0.0-1
- New upstream release

* Fri Nov 23 2018 Jan Friesse <jfriesse@redhat.com> - 2.93.0-1
- New upstream release

* Thu Aug 09 2018 Jan Friesse <jfriesse@redhat.com> - 2.92.0-1
- New upstream release

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.91.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 27 2018 Jan Friesse <jfriesse@redhat.com> - 2.91.0-1
- New upstream release

* Thu Mar 22 2018 Jan Friesse <jfriesse@redhat.com> - 2.90.0-4
- Rebuild for new Corosync

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.90.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Jan Friesse <jfriesse@redhat.com> - 2.90.0-2
- Fix spec file according to advices given in review by
  Robert-André Mauchin <zebob.m@gmail.com>

* Tue Jan 23 2018 Jan Friesse <jfriesse@redhat.com> - 2.90.0-1
- First upstream packaged version of corosync for rawhide review.
