Summary:        agent for collecting, processing, aggregating, and writing metrics.
Name:           telegraf
Version:        1.28.5
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/influxdata/telegraf
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Use the generate_source_tarball.sh script to get the vendored sources.
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         0001-adding-mariner-path.patch

BuildRequires:  golang
BuildRequires:  systemd-devel
BuildRequires:  tzdata

Requires:       logrotate
Requires:       procps-ng
Requires:       shadow-utils
Requires:       systemd
Requires:       tzdata
Requires(pre):  %{_sbindir}/useradd
Requires(pre):  %{_sbindir}/groupadd
Requires(postun): %{_sbindir}/userdel
Requires(postun): %{_sbindir}/groupdel

%description
Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics.

Design goals are to have a minimal memory footprint with a plugin system so that developers in
the community can easily add support for collecting metrics from well known services (like Hadoop,
Postgres, or Redis) and third party APIs (like Mailchimp, AWS CloudWatch, or Google Analytics).

%prep
%autosetup -p1
tar -xf %{SOURCE1}

%build
go build -buildvcs=false -mod=vendor ./cmd/telegraf

%install
mkdir -pv %{buildroot}%{_sysconfdir}/%{name}/%{name}.d
install -m 755 -D %{name} %{buildroot}%{_bindir}/%{name}
install -m 755 -D scripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 755 -D etc/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Provide empty config file.
./%{name} config > telegraf.conf
install -m 755 -D telegraf.conf %{buildroot}%{_sysconfdir}/%{name}/telegraf.conf

%check
echo $ZONEINFO
make test

%pre
getent group telegraf >/dev/null || groupadd -r telegraf
getent passwd telegraf >/dev/null || useradd -c "Telegraf" -d %{_localstatedir}/lib/%{name} -g %{name} \
        -s /sbin/nologin -M -r %{name}

%post
chown -R telegraf:telegraf %{_sysconfdir}/telegraf
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
if [ $1 -eq 0 ] ; then
    getent passwd telegraf >/dev/null && userdel telegraf
    getent group telegraf >/dev/null && groupdel telegraf
fi
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/telegraf.conf
%license LICENSE
%{_bindir}/telegraf
%{_unitdir}/telegraf.service
%{_sysconfdir}/logrotate.d/%{name}
%dir %{_sysconfdir}/%{name}/telegraf.d

%changelog
* Tue Dec 05 2023 Osama Esmail <osamaesmail@microsoft.com> 1.28.5-1
- Updating to version 1.28.5 to address critical CVEs
- Fix testing

* Thu Nov 09 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.27.4-1
- Backporting patch for CVE-2023-46129.
- Updating to version 1.27.4.
- Removed invalid, outdated patch.

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.27.3-4
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.27.3-3
- Bump release to rebuild with updated version of Go.

* Mon Aug 28 2023 Cameron Baird <cameronbaird@microsoft.com> - 1.27.3-2
- Bump release to rebuild with go 1.20.7

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.27.3-1
- Auto-upgrade to 1.27.3 - resolve vulnerability with jaeger v1.38.0

* Fri Jul 14 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.27.2-1
- Auto-upgrade to 1.27.2 to fix CVE-2023-34231, CVE-2023-25809, CVE-2023-28642

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.0-4
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.0-3
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.0-2
- Bump release to rebuild with go 1.19.8

* Wed Mar 29 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.26.0-1
- Updating to version 1.26.0 to address CVEs in vendored sources for "containerd".

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.25.2-3
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.25.2-2
- Bump release to rebuild with go 1.19.6

* Fri Feb 24 2023 Olivia Crain <oliviacrain@microsoft.com> - 1.25.2-1
- Upgrade to latest upstream version to fix the following CVEs in vendored packages:
  CVE-2019-3826, CVE-2022-1996, CVE-2022-29190, CVE-2022-29222, CVE-2022-29189, 
  CVE-2022-32149, CVE-2022-23471

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-6
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.23.0-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.0-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.0-2
- Bump release to rebuild against Go 1.18.5

* Thu Jun 16 2022 Muhammad Falak <mwani@microsoft.com> 1.23.0-1
- Bump version to 1.23.0

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.21.2-2
- Bump release to rebuild with golang 1.18.3

* Tue Jan 18 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.21.2-1
- Update to version 1.21.2.
- Modified patch to apply to new version.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14.5-8
- Removing the explicit %%clean stage.

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.14.5-7
- Increment release to force republishing using golang 1.15.13.

* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.14.5-6
- Increment release to force republishing using golang 1.15.11.

* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.14.5-5
- Increment release to force republishing using golang 1.15.

* Thu Oct 15 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.14.5-4
- License verified.
- Added %%license macro.
- Fixed source URL.
- Switched to %%autosetup.

* Fri Aug 21 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 1.14.5-3
- Add runtime required procps-ng and shadow-utils

* Tue Jul 14 2020 Jonathan Chiu <jochi@microsoft.com> 1.14.5-1
- Update to version 1.14.5

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.7.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.7.4-1
- Update version to 1.7.4 and its plugin version to 1.4.0.

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
- Remove shadow from requires and use explicit tools for post actions

* Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
- first version
