Summary:        Cron Daemon
Name:           cronie
Version:        1.5.7
Release:        3%{?dist}
License:        GPLv2+ AND MIT AND BSD AND ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/cronie-crond/cronie
Source0:        https://github.com/cronie-crond/cronie/releases/download/cronie-%{version}/cronie-%{version}.tar.gz
Source1:        run-parts.sh

BuildRequires:  libselinux-devel
BuildRequires:  pam-devel
BuildRequires:  systemd

Requires:       libselinux
Requires:       pam
Requires:       systemd

%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is based on the original cron and
has security and configuration enhancements like the ability to use pam and
SELinux.

%package anacron
Summary:        Utility for running regular jobs

Requires:       %{name} = %{version}-%{release}
Requires(post): coreutils

Provides:       dailyjobs = %{version}-%{release}
Provides:       anacron = 2.4
Obsoletes:      anacron <= 2.3

%description anacron
Anacron is part of cronie that is used for running jobs with regular
periodicity which do not have exact time of day of execution.

The default settings of anacron execute the daily, weekly, and monthly
jobs, but anacron allows setting arbitrary periodicity of jobs.

Using anacron allows running the periodic jobs even if the system is often
powered off and it also allows randomizing the time of the job execution
for better utilization of resources shared among multiple systems.

%package noanacron
Summary:        Utility for running simple regular jobs in old cron style

Requires:       %{name} = %{version}-%{release}

Provides:       dailyjobs = %{version}-%{release}

%description noanacron
Old style of running {hourly,daily,weekly,monthly}.jobs without anacron. No
extra features.

%prep
%setup -q
sed -i 's/^\s*account\s*include\s*system-auth$/account    include    system-account/g;
        s/^\s*session\s*include\s*system-auth$/session    include    system-session/g;' pam/crond

%build
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=/var \
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

install -vdm700 %{buildroot}%{_sysconfdir}/cron.d/
install -vm644 contrib/0hourly %{buildroot}%{_sysconfdir}/cron.d/0hourly
install -vm644 contrib/dailyjobs %{buildroot}%{_sysconfdir}/cron.d/dailyjobs

install -vdm700 %{buildroot}%{_sysconfdir}/cron.hourly
install -vm755 contrib/0anacron %{buildroot}%{_sysconfdir}/cron.hourly/0anacron

install -vdm700 %{buildroot}%{_sysconfdir}/cron.daily
install -vdm700 %{buildroot}%{_sysconfdir}/cron.weekly
install -vdm700 %{buildroot}%{_sysconfdir}/cron.monthly

install -vm600 contrib/anacrontab %{buildroot}%{_sysconfdir}/anacrontab

touch %{buildroot}%{_sysconfdir}/cron.deny

install -vdm755 %{buildroot}%{_var}/spool/anacron
touch %{buildroot}%{_var}/spool/anacron/cron.daily
touch %{buildroot}%{_var}/spool/anacron/cron.weekly
touch %{buildroot}%{_var}/spool/anacron/cron.monthly

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
%dir %{_sysconfdir}/cron.hourly
%dir %{_sysconfdir}/cron.daily
%dir %{_sysconfdir}/cron.weekly
%dir %{_sysconfdir}/cron.monthly

%attr(4755,root,root) %{_bindir}/crontab
%attr(755,root,root) %{_bindir}/cronnext
%{_bindir}/run-parts
%{_sbindir}/crond

%{_mandir}/man1/cronnext.*
%{_mandir}/man1/crontab.*
%{_mandir}/man5/crontab.*
%{_mandir}/man8/cron.*
%{_mandir}/man8/crond.*

%config(noreplace) %{_sysconfdir}/cron.deny
%config(noreplace) %{_sysconfdir}/sysconfig/crond

%files anacron
%{_sbindir}/anacron
%attr(0755,root,root) %{_sysconfdir}/cron.hourly/0anacron
%config(noreplace) %{_sysconfdir}/anacrontab
%dir %{_var}/spool/anacron
%ghost %attr(0600,root,root) %{_localstatedir}/spool/anacron/cron.daily
%ghost %attr(0600,root,root) %{_localstatedir}/spool/anacron/cron.monthly
%ghost %attr(0600,root,root) %{_localstatedir}/spool/anacron/cron.weekly
%{_mandir}/man5/anacrontab.*
%{_mandir}/man8/anacron.*

%files noanacron
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cron.d/dailyjobs

%changelog
* Fri Oct 27 2023 Andrew Phelps <anphel@microsoft.com> - 1.5.7-3
- Fix pam/crond file contents

* Thu Jul 21 2022 Minghe Ren <mingheren@microsoft.com> - 1.5.7-2
- Change file permission to improve security

* Mon Mar 07 2022 Andrew Phelps <anphel@microsoft.com> - 1.5.7-1
- Upgrade to version 1.5.7

* Tue Aug 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.2-7
- Splitting package into "cronie-anacron" and "cronie-noanacron".
- Package changes are an import from Fedora 32 (license: MIT).

* Mon Aug 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.2-6
- Adding "Provides: anacron" for compatibility reasons.

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
