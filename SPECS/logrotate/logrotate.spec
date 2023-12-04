Summary:        Logrotate
Name:           logrotate
Version:        3.21.0
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/logrotate/logrotate/
Source0:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  popt-devel
BuildRequires:  systemd-devel
Requires:       popt
Requires:       systemd

%description
The logrotate utility is designed to simplify the administration of log
files on a system which generates a lot of log files. Logrotate allows
for the automatic rotation compression, removal and mailing of log files.
Logrotate can be set to handle a log file daily, weekly, monthly or when
the log file gets to a certain size.

%prep
%autosetup -p1

%build
./autogen.sh
./configure --prefix=%{_prefix} --with-state-file-path=%{_localstatedir}/lib/logrotate/logrotate.status
make %{?_smp_mflags}

# Disable dateext since it can cause rotation to fail if run twice in a day
sed -i 's/dateext/#dateext/' examples/logrotate.conf

%install
make DESTDIR=%{buildroot} install
install -vd %{buildroot}%{_sysconfdir}/logrotate.d
install -vd %{buildroot}%{_localstatedir}/lib/logrotate
install -vd %{buildroot}%{_unitdir}
touch %{buildroot}%{_localstatedir}/lib/logrotate/logrotate.status
install -p -m 644 examples/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.conf
install -p -m 644 examples/logrotate.{service,timer} %{buildroot}%{_unitdir}/
install -p -m 644 examples/{b,w}tmp %{buildroot}%{_sysconfdir}/logrotate.d/

%post
%systemd_post logrotate.{service,timer}

%postun
%systemd_preun logrotate.{service,timer}

%files
%defattr(-,root,root)
%license COPYING
%dir %{_sysconfdir}/logrotate.d
%dir %{_localstatedir}/lib/logrotate
%{_sbindir}/logrotate
%{_unitdir}/logrotate.{service,timer}
%config(noreplace) %{_sysconfdir}/logrotate.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/{b,w}tmp
%{_mandir}/man5/logrotate.conf.5.gz
%{_mandir}/man8/logrotate.8.gz
%ghost %verify(not size md5 mtime) %attr(0644, root, root) %{_localstatedir}/lib/logrotate/logrotate.status

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.21.0-1
- Auto-upgrade to 3.21.0 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Muhammad Falak <mwani@microsoft.com> - 3.20.1-1
- Bump version to 3.20.1 to address CVE-2022-1348

* Tue Apr 19 2022 Cameron Baird <cameronbaird@microsoft.com> - 3.18.1-2
- Reenable systemd hardening configs ProtectClock, ProtectHostname, and ProtectKernelLogs

* Wed Jul 21 2021 Henry Beberman <henry.beberman@microsoft.com> - 3.18.1-1
- Update to version 3.18.1
- Add default logrotate systemd service and logrotate.conf

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.16.0-2
- Added %%license line automatically

* Fri Apr 24 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.16.0-1
- Updated to 3.16.0.
- License verified.
- Updated 'Url' and 'Source0' tags.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.14.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 3.14.0-1
- Update to version 3.14.0

* Mon Jul 31 2017 Kumar Kaushik <kaushikk@vmware.com> 3.11.0-3
- Creating /etc/logrotate.d folder as part of package installation, Bug#1878180.

* Wed Jun 14 2017 Anish Swaminathan <anishs@vmware.com> 3.11.0-2
- Mark config files as noreplace

* Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.11.0-1
- Updating version to 3.11.0

* Mon Mar 13 2017 Alexey Makhalov <amakhalov@vmware.com> 3.9.1-3
- Compilation for gcc 6.3

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.9.1-2
- GA - Bump release of all rpms

* Wed Jun 24 2015 Divya Thaluru <dthaluru@vmware.com> 3.9.1-1
- Initial build. First version
