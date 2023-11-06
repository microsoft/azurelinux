%define base_version %(echo %{version} | rev | cut -d'.' -f2- | rev)

Summary:        Rocket-fast system for log processing
Name:           rsyslog
Version:        8.2308.0
Release:        1%{?dist}
License:        GPLv3+ AND ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://www.rsyslog.com/
Source0:        https://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1:        rsyslog.service
Source2:        50-rsyslog-journald.conf
Source3:        rsyslog.conf
# Upstream only publishes built docs for base_version.0
Source4:        https://www.rsyslog.com/files/download/rsyslog/%{name}-doc-%{base_version}.0.tar.gz
Source5:        rsyslog.logrotate
BuildRequires:  autogen
BuildRequires:  curl-devel
BuildRequires:  gnutls-devel
BuildRequires:  krb5-devel
BuildRequires:  libestr-devel
BuildRequires:  libfastjson-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  liblognorm-devel
BuildRequires:  librdkafka-devel
BuildRequires:  librelp-devel
BuildRequires:  net-snmp-devel
BuildRequires:  postgresql-devel
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
Requires:       gnutls
Requires:       libestr
Requires:       libfastjson
Requires:       libgcrypt
Requires:       librelp
Requires:       systemd
Requires(pre):  shadow-utils
Provides:       %{name}-crypto = %{version}-%{release}
Provides:       %{name}-elasticsearch = %{version}-%{release}
Provides:       %{name}-gnutls = %{version}-%{release}
Provides:       %{name}-gssapi = %{version}-%{release}
Provides:       %{name}-kafka = %{version}-%{release}
Provides:       %{name}-mmaudit = %{version}-%{release}
Provides:       %{name}-mmjsonparse = %{version}-%{release}
Provides:       %{name}-mmkubernetes = %{version}-%{release}
Provides:       %{name}-mmnormalize = %{version}-%{release}
Provides:       %{name}-mmsnmptrapd = %{version}-%{release}
Provides:       %{name}-pgsql = %{version}-%{release}
Provides:       %{name}-relp = %{version}-%{release}
Provides:       %{name}-snmp = %{version}-%{release}
Provides:       syslog

%description
RSYSLOG is the rocket-fast system for log processing.
It offers high-performance, great security features and a modular design. While it started as a regular syslogd, rsyslog has evolved into a kind of swiss army knife of logging, being able to accept inputs from a wide variety of sources, transform them, and output to the results to diverse destinations.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch

%description    doc
HTML documentation for %{name}

%prep
# Unpack the code source tarball
%setup -q
# Unpack the documentation tarball in the folder created above
%setup -q -a 4 -T -D
# Remove documentation sources
rm -rf sources
# Move prebuilt documentation files to a documentation folder
mv build docs

autoreconf -fvi

%build
sed -i 's/libsystemd-journal/libsystemd/' configure
%configure \
    --disable-static \
    --enable-elasticsearch \
    --enable-gnutls\
    --enable-gssapi-krb5 \
    --enable-imfile \
    --enable-imjournal \
    --enable-imkafka \
    --enable-impstats \
    --enable-imptcp \
    --enable-imptcp \
    --enable-mail \
    --enable-mmanon \
    --enable-mmaudit \
    --enable-mmcount \
    --enable-mmjsonparse \
    --enable-mmkubernetes \
    --enable-mmnormalize \
    --enable-mmsnmptrapd \
    --enable-mmutf8fix \
    --enable-omjournal \
    --enable-omkafka \
    --enable-omprog \
    --enable-omstdout \
    --enable-omuxsock \
    --enable-pgsql \
    --enable-pmaixforwardedfrom \
    --enable-pmcisconames \
    --enable-pmlastmsg \
    --enable-pmsnare \
    --enable-relp \
    --enable-snmp \
    --enable-unlimited-select \
    --enable-usertools

%make_build

%install
%make_install
install -vd %{buildroot}%{_libdir}/systemd/system/
install -vd %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -vd %{buildroot}%{_docdir}/%{name}/html
install -vdm 755 %{buildroot}/%{_sysconfdir}/rsyslog.d
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
rm -f %{buildroot}/lib/systemd/system/rsyslog.service
install -p -m 644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rsyslog.conf
install -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/rsyslog
cp -r docs/* %{buildroot}%{_docdir}/%{name}/html
find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build check

%pre
if ! (getent passwd syslog >/dev/null); then
    groupadd --system syslog
fi
if ! (getent passwd syslog >/dev/null); then
useradd --system --comment 'System Logging'  --gid syslog --shell /bin/false syslog
fi

%post
/sbin/ldconfig
%systemd_post rsyslog.service

%preun
%systemd_preun rsyslog.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rsyslog.service
if getent passwd syslog >/dev/null; then
    userdel syslog
fi
if getent group syslog >/dev/null; then
    groupdel syslog
fi

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/rscryutil
%{_sbindir}/*
%{_libdir}/rsyslog/*.so
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_libdir}/systemd/system/rsyslog.service
%{_sysconfdir}/systemd/journald.conf.d/*
%{_sysconfdir}/rsyslog.conf
%dir %attr(0755, root, root) %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/logrotate.d/rsyslog

%files doc
%doc %{_docdir}/%{name}/html

%changelog
* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.2308.0-1
- Auto-upgrade to 8.2308.0 - Azure Linux 3.0 - package upgrades

* Wed Oct 12 2022 Nan Liu <liunan@microsoft.com> - 8.2204.1-3
- Add rsyslog configuration file to /etc/logrotate.d

* Wed Jul 20 2022 Minghe Ren <mingheren@microsoft.com> - 8.2204.1-2
- Modify rsyslog.conf to improve security
- Add syslog user to own the log files

* Tue May 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 8.2204.1-1
- Update to v8.2204.1 to address CVE-2022-24903
- Add more robust macro for Source4 url (prebuilt docs tar)

* Thu Apr 07 2022 Daniel McIlvaney <damcilva@microsoft.com> - 8.2108.0-2
- Bring rsyslog.conf in line with other distros
- add /var/log/messages for normal logs
- add /var/log/secure for auth and authpriv logs
- set file permissions to 640 for log files

* Mon Jan 24 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 8.2108.0-1
- Update to version 8.2108.0.

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.37.0-8
- Added "Provides: syslog".

* Thu Sep 16 2021 Henry Beberman <henry.beberman@microsoft.com> - 8.37.0-7
- Add /etc/rsyslog.d directory.

* Mon Jul 19 2021 Thomas Crain <thcrain@microsoft.com> - 8.37.0-6
- Add html documentation subpackage from upstream-provided tarball
- Enable various features and add the corresponding provides for subpackages from other distros:
-   crypto, elasticsearch, kafka, mmaudit, mmjson, mmkubernetes, 
-   mmnormalize, mmsnmptrapd, pgsql, snmp
- License verified

* Tue Jan 12 2021 Ruying Chen <v-ruyche@microsoft.com> - 8.37.0-5
- Build with gssapi, relp support and add explicit provides.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 8.37.0-4
- Added %%license line automatically

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 8.37.0-3
- Remove liblogging from requires.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 8.37.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> - 8.37.0-1
- Updated to version 8.37.0

* Thu Apr 12 2018 Xiaolin Li <xiaolinl@vmware.com> - 8.26.0-5
- Add $IncludeConfig /etc/rsyslog.d/ to rsyslog.conf

* Fri Dec 15 2017 Anish Swaminathan <anishs@vmware.com> - 8.26.0-4
- Remove kill SIGHUP from service file

* Mon Nov 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 8.26.0-3
- Add a default rsyslog.conf.

* Tue Aug 15 2017 Dheeraj Shetty <dheerajs@vmware.com> - 8.26.0-2
- Fix CVE-2017-12588

* Mon  Apr 24 2017 Siju Maliakkal <smaliakkal@vmware.com> - 8.26.0-1
- Update to latest

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 8.15.0-7
- Change systemd dependency

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> - 8.15.0-6
- Modified %check

* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com> - 8.15.0-5
- Fixed logic to restart the active services after upgrade

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 8.15.0-4
- GA - Bump release of all rpms

* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 8.15.0-3
- Use systemd macros for post, preun and postun to respect upgrades

* Wed Feb 17 2016 Anish Swaminathan <anishs@vmware.com> - 8.15.0-2
- Add journald conf and new service file.

* Mon Jan 11  2016 Xiaolin Li <xiaolinl@vmware.com> - 8.15.0-1
- Update rsyslog to 8.15.0

* Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> - 8.10.0-1
- Initial build. First version
