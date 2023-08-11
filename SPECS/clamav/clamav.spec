%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Open source antivirus engine
Name:           clamav
Version:        0.103.8
Release:        1%{?dist}
License:        ASL 2.0 AND BSD AND bzip2-1.0.4 AND GPLv2 AND LGPLv2+ AND MIT AND Public Domain AND UnRar
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.clamav.net
Source0:        %{url}/downloads/production/%{name}-%{version}.tar.gz
# Workaround for coreutils missing requirement flex
BuildRequires:  flex-devel
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  sed
# Required to produce systemd files
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
Requires:       openssl
Requires:       zlib
Requires(pre):  shadow-utils
Requires(postun): shadow-utils

%description
ClamAV® is an open source (GPL) anti-virus engine used in a variety of situations
including email scanning, web scanning, and end point security. It provides a number
of utilities including a flexible and scalable multi-threaded daemon, a command
line scanner and an advanced tool for automatic database updates.

%prep
%setup -q

%build
%configure \
  --with-dbdir=%{_sharedstatedir}/clamav

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sharedstatedir}/clamav

### freshclam config processing (from Fedora)
sed -ri \
    -e 's!^Example!#Example!' \
    -e 's!^#?(UpdateLogFile )!#\1!g;' %{buildroot}%{_sysconfdir}/freshclam.conf.sample

mv %{buildroot}%{_sysconfdir}/freshclam.conf{.sample,}
# Can contain HTTPProxyPassword (bugz#1733112)
chmod 600 %{buildroot}%{_sysconfdir}/freshclam.conf

%check
make %{?_smp_mflags} check

%pre
if ! getent group clamav >/dev/null; then
    groupadd -r clamav
fi
if ! getent passwd clamav >/dev/null; then
    useradd -g clamav -d %{_sharedstatedir}/clamav\
        -s /bin/false -M -r clamav
fi

%post
/sbin/ldconfig
touch %{_var}/log/freshclam.log
chown clamav:clamav %{_var}/log/freshclam.log
chmod 600 %{_var}/log/freshclam.log

%postun
/sbin/ldconfig
if getent passwd clamav >/dev/null; then
    userdel clamav
fi
if getent group clamav >/dev/null; then
    groupdel clamav
fi
rm -f %{_var}/log/freshclam.log

%files
%defattr(-,root,root)
%license COPYING COPYING.bzip2 COPYING.file COPYING.getopt COPYING.LGPL COPYING.llvm COPYING.lzma COPYING.pcre COPYING.regex COPYING.unrar COPYING.YARA COPYING.zlib
%{_bindir}/*
%{_sysconfdir}/*.sample
%{_sysconfdir}/freshclam.conf
%{_includedir}/*.h
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
/lib/systemd/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %attr(-,clamav,clamav) %{_sharedstatedir}/clamav
%ghost %attr(-,clamav,clamav) %{_var}/log/freshclam.log

%changelog
* Fri Feb 17 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.103.8-1
- Auto-upgrade to 0.103.8 - CVE-2023-20032

*Fri Jul 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.103.6-2
- Fix freshclam DB download (backport of Tom Fay's 2.0 changes)
- Create/delete clamav user and group on preinstall/postuninstall
- Move database directory to %%{_sharedstatedir} from %%{_datadir}
- Give ownership of %%{_sharedstatedir}/clamav, %%{_var}/log/freshclam.log to clamav user

* Tue May 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.103.6-1
- Upgrade to latest LTS patch to fix CVE-2022-20770, CVE-2022-20771, 
  CVE-2022-20785, CVE-2022-20792, CVE-2022-20796

* Mon Feb 28 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 0.103.5-1
- Updating to 0.103.5 to fix CVE-2022-20698

* Tue Apr 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.103.2-1
- Updating to 0.103.2 to fix CVE-2021-1252, CVE-2021-1404, CVE-2021-1405

* Tue Oct 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.103.0-1
- Updating to 0.103.0 to fix: CVE-2019-12625, CVE-2019-15961.

* Mon Oct 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.101.2-3
- License verified.
- Added %%license macro.
- Switching to using the %%configure macro.
- Extended package's summary and description.

* Wed Oct 02 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.101.2-2
- Fix vendor and distribution. Add systemd files to the list.

* Thu Jul 25 2019 Chad Zawistowski <chzawist@microsoft.com> - 0.101.2-1
- Initial CBL-Mariner import from Azure.
