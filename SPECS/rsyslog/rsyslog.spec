Summary:        Rocket-fast system for log processing
Name:           rsyslog
Version:        8.37.0
Release:        8%{?dist}
License:        GPLv3+ AND LGPLv3 AND ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://www.rsyslog.com/
Source0:        https://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1:        rsyslog.service
Source2:        50-rsyslog-journald.conf
Source3:        rsyslog.conf
Source4:        rsyslog.logrotate
Source5:        rsyslog-warn.logrotate
Patch1:         CVE-2022-24903.patch
BuildRequires:  autogen
BuildRequires:  curl-devel
BuildRequires:  gnutls-devel
BuildRequires:  libestr-devel
BuildRequires:  libfastjson-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  librelp-devel
BuildRequires:  systemd-devel
Requires:       gnutls
Requires:       libestr
Requires:       libfastjson
Requires:       libgcrypt
Requires:       librelp
Requires:       systemd

%description
RSYSLOG is the rocket-fast system for log processing.
It offers high-performance, great security features and a modular design. While it started as a regular syslogd, rsyslog has evolved into a kind of swiss army knife of logging, being able to accept inputs from a wide variety of sources, transform them, and output to the results to diverse destinations.

%prep
%autosetup -p1
autoreconf -fvi

%build
sed -i 's/libsystemd-journal/libsystemd/' configure
./configure \
    --prefix=%{_prefix} \
    --enable-relp \
    --enable-gnutls\
    --enable-imfile \
    --enable-imjournal \
    --enable-impstats \
    --enable-imptcp \
    --enable-omuxsock

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vd %{buildroot}%{_libdir}/systemd/system/
install -vd %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -vdm 755 %{buildroot}/%{_sysconfdir}/rsyslog.d
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
rm -f %{buildroot}/lib/systemd/system/rsyslog.service
install -p -m 644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rsyslog.conf
install -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/rsyslog
install -p -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/rsyslog-warn
find %{buildroot} -type f -name "*.la" -delete -print

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post rsyslog.service

%preun
%systemd_preun rsyslog.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rsyslog.service

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_libdir}/rsyslog/*.so
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_libdir}/systemd/system/rsyslog.service
%{_sysconfdir}/systemd/journald.conf.d/*
%{_sysconfdir}/rsyslog.conf
%dir %attr(0755, root, root) %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/logrotate.d/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/rsyslog-warn

%changelog
* Fri Oct 14 2022 Nan Liu <liunan@microsoft.com> - 8.37.0-8
- Add rsyslog and rsyslog-warn configuration files to /etc/logrotate.d

* Mon May 23 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 8.37.0-7
- Patching CVE-2022-24903

* Thu Sep 16 2021 Henry Beberman <henry.beberman@microsoft.com> - 8.37.0-6
- Add /etc/rsyslog.d directory.
- License Verified.
- Cleanup spec.

* Thu Sep 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 8.37.0-5
- Enable omuxsock.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 8.37.0-4
- Added %%license line automatically

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> 8.37.0-3
- Remove liblogging from requires.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 8.37.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 8.37.0-1
- Updated to version 8.37.0

* Thu Apr 12 2018 Xiaolin Li <xiaolinl@vmware.com> 8.26.0-5
- Add $IncludeConfig /etc/rsyslog.d/ to rsyslog.conf

* Fri Dec 15 2017 Anish Swaminathan <anishs@vmware.com>  8.26.0-4
- Remove kill SIGHUP from service file

* Mon Nov 13 2017 Xiaolin Li <xiaolinl@vmware.com> 8.26.0-3
- Add a default rsyslog.conf.

* Tue Aug 15 2017 Dheeraj Shetty <dheerajs@vmware.com>  8.26.0-2
- Fix CVE-2017-12588

* Mon  Apr 24 2017 Siju Maliakkal <smaliakkal@vmware.com>  8.26.0-1
- Update to latest

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  8.15.0-7
- Change systemd dependency

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 8.15.0-6
- Modified %check

* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  8.15.0-5
- Fixed logic to restart the active services after upgrade

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.15.0-4
- GA - Bump release of all rpms

* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  8.15.0-3
- Use systemd macros for post, preun and postun to respect upgrades

* Wed Feb 17 2016 Anish Swaminathan <anishs@vmware.com>  8.15.0-2
- Add journald conf and new service file.

* Mon Jan 11  2016 Xiaolin Li <xiaolinl@vmware.com> 8.15.0-1
- Update rsyslog to 8.15.0

* Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 8.10.0-1
- Initial build. First version
