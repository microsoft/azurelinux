Summary:        Logrotate
Name:           logrotate
Version:        3.16.0
Release:        2%{?dist}
License:        GPLv2
URL:            https://github.com/logrotate/logrotate/
#Source0:       %{url}/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  popt-devel

Requires:   popt

%description
The logrotate utility is designed to simplify the administration of log files on a system which generates a lot of log files. Logrotate allows for the automatic rotation compression, removal and mailing of log files. Logrotate can be set to handle a log file daily, weekly, monthly or when the log file gets to a certain size.

%prep
%setup -q

%build
./autogen.sh
./configure \
   --prefix=%{_prefix}
# logrotate code has misleading identation and GCC 6.3 does not like it.
make %{?_smp_mflags} CFLAGS="-Wno-error=misleading-indentation -g -O2"

%install
make DESTDIR=%{buildroot} install
install -vd %{buildroot}%{_sysconfdir}/logrotate.d
install -vd %{buildroot}%{_sysconfdir}/cron.daily
install -vd %{buildroot}%{_localstatedir}/lib/logrotate
touch %{buildroot}%{_localstatedir}/lib/logrotate/logrotate.status

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%dir %{_sysconfdir}/logrotate.d
%{_sbindir}/logrotate
%{_mandir}/man5/logrotate.conf.5.gz
%{_mandir}/man8/logrotate.8.gz
/var/lib/logrotate/logrotate.status

%changelog
* Sat May 09 00:21:41 PST 2020 Nick Samson <nisamson@microsoft.com> - 3.16.0-2
- Added %%license line automatically

*   Fri Apr 24 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.16.0-1
-   Updated to 3.16.0.
-   License verified.
-   Updated 'Url' and 'Source0' tags.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.14.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 3.14.0-1
-   Update to version 3.14.0
*   Mon Jul 31 2017 Kumar Kaushik <kaushikk@vmware.com> 3.11.0-3
-   Creating /etc/logrotate.d folder as part of package installation, Bug#1878180.
*   Wed Jun 14 2017 Anish Swaminathan <anishs@vmware.com> 3.11.0-2
-   Mark config files as noreplace
*   Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.11.0-1
-   Updating version to 3.11.0
*   Mon Mar 13 2017 Alexey Makhalov <amakhalov@vmware.com> 3.9.1-3
-   Compilation for gcc 6.3
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.9.1-2
-   GA - Bump release of all rpms
*   Wed Jun 24 2015 Divya Thaluru <dthaluru@vmware.com> 3.9.1-1
-   Initial build. First version
