Summary:        Cron Daemon
Name:           cronie
Version:        1.5.2
Release:        5%{?dist}
License:        GPLv2+ and MIT and BSD and ISC
URL:            https://github.com/cronie-crond/cronie
Source0:        https://github.com/cronie-crond/cronie/releases/download/cronie-%{version}/cronie-%{version}.tar.gz
Source1:        run-parts.sh
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  libselinux-devel
BuildRequires:  pam-devel
BuildRequires:  systemd
Requires:       systemd
Requires:       libselinux
Requires:       pam
%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is based on the original cron and
has security and configuration enhancements like the ability to use pam and
SELinux.
%prep
%setup -q
sed -i 's/^\s*auth\s*include\s*password-auth$/auth       include    system-auth/g;
     s/^\s*account\s*include\s*password-auth$/account    include    system-account/g;
     s/^\s*session\s*include\s*password-auth$/session    include    system-session/g;' pam/crond
%build
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=/etc   \
    --localstatedir=/var\
    --with-pam          \
    --with-selinux      \
    --enable-anacron    \
    --enable-pie        \
    --enable-relro
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm700 %{buildroot}%{_localstatedir}/spool/cron

install -vdm755 %{buildroot}%{_sysconfdir}/sysconfig/
install -vm644 crond.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/crond

install -vdm755 %{buildroot}%{_sysconfdir}/cron.d/
install -vm644 contrib/0hourly %{buildroot}%{_sysconfdir}/cron.d/0hourly
install -vm644 contrib/dailyjobs %{buildroot}%{_sysconfdir}/cron.d/dailyjobs

install -vdm755 %{buildroot}%{_sysconfdir}/cron.hourly
install -vm755 contrib/0anacron %{buildroot}%{_sysconfdir}/cron.hourly/0anacron

install -vdm755 %{buildroot}%{_sysconfdir}/cron.daily
install -vdm755 %{buildroot}%{_sysconfdir}/cron.weekly
install -vdm755 %{buildroot}%{_sysconfdir}/cron.monthly

install -vm644 contrib/anacrontab %{buildroot}%{_sysconfdir}/anacrontab

touch %{buildroot}%{_sysconfdir}/cron.deny

install -vdm755 %{buildroot}/var/spool/anacron
touch %{buildroot}/var/spool/anacron/cron.daily
touch %{buildroot}/var/spool/anacron/cron.weekly
touch %{buildroot}/var/spool/anacron/cron.monthly

install -m755  %{SOURCE1} %{buildroot}/%{_bindir}/run-parts

install -vdm755 %{buildroot}%{_libdir}/systemd/system/
install -m644 contrib/cronie.systemd %{buildroot}%{_libdir}/systemd/system/crond.service
ln -sfv ./crond.service %{buildroot}%{_libdir}/systemd/system/cron.service

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post crond.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart crond.service

%preun
%systemd_preun crond.service

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/systemd/system/cron.service
%{_libdir}/systemd/system/crond.service

%config(noreplace) %{_sysconfdir}/pam.d/crond

%dir %{_localstatedir}/spool/cron
%dir %{_sysconfdir}/cron.d
%config(noreplace) %{_sysconfdir}/cron.d/0hourly
%config(noreplace) %{_sysconfdir}/cron.d/dailyjobs
%dir %{_sysconfdir}/cron.hourly
%{_sysconfdir}/cron.hourly/0anacron
%dir %{_sysconfdir}/cron.daily
%dir %{_sysconfdir}/cron.weekly
%dir %{_sysconfdir}/cron.monthly

%attr(4755,root,root) %{_bindir}/crontab
%attr(755,root,root) %{_bindir}/cronnext
%{_bindir}/run-parts
%{_sbindir}/crond
%{_sbindir}/anacron

%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%config(noreplace) %{_sysconfdir}/cron.deny
%config(noreplace) %{_sysconfdir}/sysconfig/crond

%dir /var/spool/anacron
%config(noreplace) %{_sysconfdir}/anacrontab
%ghost %attr(0600,root,root) %{_localstatedir}/spool/anacron/cron.daily
%ghost %attr(0600,root,root) %{_localstatedir}/spool/anacron/cron.monthly
%ghost %attr(0600,root,root) %{_localstatedir}/spool/anacron/cron.weekly

%changelog
* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.5.2-5
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Fri Sep 04 2020 Daniel Burgener <daburgen@microsoft.com> - 1.5.2-4
- Enable SELinux support

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.5.2-3
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 1.5.2-2
- Renaming Linux-PAM to pam
* Wed Mar 18 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.5.2-1
- Update to 1.5.2. License verified.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.5.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).
* Mon Apr 24 2017 Bo Gan <ganb@vmware.com> 1.5.1-1
- Update to 1.5.1
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.5.0-13
- BuildRequires Linux-PAM-devel
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.5.0-12
- Modified %check
* Mon Aug 29 2016 Divya Thaluru <dthaluru@vmware.com>  1.5.0-11
- Fixed pam configuration for crond
* Thu Aug 4 2016 Divya Thaluru <dthaluru@vmware.com>  1.5.0-10
- Added logic to not replace conf files in upgrade scenario
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.0-9
- GA - Bump release of all rpms
* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  1.5.0-8
- Fixing spec file to handle rpm upgrade scenario correctly
* Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com>  1.5.0-7
- Add run-parts command.
* Fri Mar 04 2016 Anish Swaminathan <anishs@vmware.com>  1.5.0-6
- Add folders to sysconfdir.
* Mon Feb 08 2016 Anish Swaminathan <anishs@vmware.com>  1.5.0-5
- Change default sysconfdir.
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.5.0-4
- Add systemd to Requires and BuildRequires.
- Use systemctl to enable/disable service.
* Mon Nov 30 2015 Xiaolin Li <xiaolinl@vmware.com> 1.5.0-3
- Symlink cron.service to crond.service.
- And move the /usr/etc/pam.d/crond to /etc/pam.d/crond
* Thu Nov 12 2015 Xiaolin Li <xiaolinl@vmware.com> 1.5.0-2
- Add crond to systemd service.
* Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
- Initial build. First version
