Summary:        agent for collecting, processing, aggregating, and writing metrics.
Name:           telegraf
Version:        1.31.0
<<<<<<< HEAD
Release:        29%{?dist}
=======
Release:        31%{?dist}
>>>>>>> 8a8f117710 ([AutoPR- Security] Patch telegraf for CVE-2026-79921 [HIGH] (#18656))
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Tools
URL:            https://github.com/influxdata/telegraf
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Use the generate_source_tarbbal.sh script to get the vendored sources.
Source1:        %{name}-%{version}-v1-vendor.tar.gz

Patch0:         CVE-2024-35255.patch
Patch1:         CVE-2024-37298.patch
Patch2:         CVE-2024-45337.patch
Patch3:         CVE-2024-45338.patch
Patch4:         CVE-2025-22868.patch
Patch5:         CVE-2025-22869.patch
Patch6:         CVE-2025-22870.patch
Patch7:         CVE-2024-51744.patch
Patch8:         CVE-2025-30204.patch
Patch9:         CVE-2025-27144.patch
Patch10:        CVE-2025-30215.patch
Patch11:        CVE-2025-22872.patch
Patch12:        CVE-2025-47913.patch
Patch13:        CVE-2025-10543.patch
Patch14:        CVE-2026-27571.patch
Patch15:        CVE-2025-11065.patch
Patch16:        CVE-2025-47911.patch
Patch17:        CVE-2025-58190.patch
Patch18:        CVE-2026-2303.patch
Patch19:        CVE-2026-26014.patch
Patch20:        CVE-2026-4645.patch
# Patch added based on customer request https://microsoft.visualstudio.com/OS/_workitems/edit/61041768
# Fix was introduced 1.37.2, this patch can be removed once we update to 1.37.2 or later
Patch21:        cisco_telegraf_bug61041768.patch
Patch22:        CVE-2026-29785.patch
Patch23:        CVE-2026-33216.patch
Patch24:        CVE-2026-5160.patch
Patch25:        CVE-2026-41602.patch
Patch26:        CVE-2026-42154.patch
Patch27:        CVE-2026-39821.patch
Patch28:        CVE-2026-39829.patch
Patch29:        CVE-2026-39830.patch
Patch30:        CVE-2026-39832.patch
Patch31:        CVE-2026-39834.patch
Patch32:        CVE-2026-42506.patch
Patch33:        CVE-2026-42508.patch
Patch34:        CVE-2026-46597.patch
Patch35:        CVE-2026-27136.patch
Patch36:        CVE-2026-41889.patch
Patch37:        CVE-2026-42151.patch
Patch38:        CVE-2026-25680.patch
Patch39:        CVE-2026-25681.patch
Patch40:        CVE-2026-39827.patch
Patch41:        CVE-2026-39828.patch
Patch43:        CVE-2026-39835.patch
Patch44:        CVE-2026-42502.patch
Patch45:        CVE-2026-46598.patch
Patch46:        CVE-2026-58207.patch
Patch47:        CVE-2026-58208.patch
Patch48:        CVE-2026-58209.patch
Patch49:        CVE-2026-58250.patch
Patch50:        CVE-2026-58251.patch
Patch51:        CVE-2026-58252.patch
Patch52:        CVE-2026-58253.patch
Patch53:        CVE-2026-56852.patch
Patch54:        CVE-2025-29923.patch
Patch55:        CVE-2025-46327.patch
Patch56:        CVE-2026-54908.patch
Patch57:        CVE-2026-54332.patch
<<<<<<< HEAD
=======
Patch58:        CVE-2026-65819.patch
Patch59:        CVE-2026-79921.patch
>>>>>>> 8a8f117710 ([AutoPR- Security] Patch telegraf for CVE-2026-79921 [HIGH] (#18656))

BuildRequires:  golang
BuildRequires:  systemd-devel
Requires:       logrotate
Requires:       procps-ng
Requires:       shadow-utils
Requires:       systemd
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
%autosetup -a1 -p1

%build
go build -mod=vendor ./cmd/telegraf

%install
mkdir -pv %{buildroot}%{_sysconfdir}/%{name}/%{name}.d
install -m 755 -D %{name} %{buildroot}%{_bindir}/%{name}
install -m 755 -D scripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 755 -D etc/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Provide empty config file.
./%{name} config > telegraf.conf
install -m 755 -D telegraf.conf %{buildroot}%{_sysconfdir}/%{name}/telegraf.conf

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
<<<<<<< HEAD
=======
* Mon Aug 31 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-31
- Patch for CVE-2026-79921

* Thu Aug 13 2026 Sushil Sati <v-sushilsati@microsoft.com> - 1.31.0-30
- Patch for CVE-2026-65819

>>>>>>> 8a8f117710 ([AutoPR- Security] Patch telegraf for CVE-2026-79921 [HIGH] (#18656))
* Sat Aug 08 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-29
- Patch for CVE-2026-54332

* Fri Aug 07 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-28
- Patch for CVE-2026-54908

* Fri Aug 07 2026 Jyoti kanase <v-jykanase@microsoft.com> - 1.31.0-27
- Patch CVE-2025-29923
- Patch CVE-2025-46327

* Mon Aug 03 2026 Kanishk Bansal <kanbansal@microsoft.com> - 1.31.0-26
- Upgrade thrift module to 0.24.0

* Tue Jul 28 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-25
- Patch for CVE-2026-56852

* Sun Jul 12 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-24
- Patch for CVE-2026-58253, CVE-2026-58252, CVE-2026-58251, CVE-2026-58250, CVE-2026-58209, CVE-2026-58208, CVE-2026-58207

* Tue Jun 02 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-23
- Patch for CVE-2026-46598, CVE-2026-42502, CVE-2026-39835, CVE-2026-39828, CVE-2026-39827, CVE-2026-25681, CVE-2026-25680

* Thu May 28 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-22
- Patch for CVE-2026-41889, CVE-2026-42151

* Wed May 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-21
- Patch for CVE-2026-46597, CVE-2026-42508, CVE-2026-42506, CVE-2026-39834, CVE-2026-39832, CVE-2026-39830, CVE-2026-39829, CVE-2026-39821, CVE-2026-27136

* Sat May 02 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-20
- Patch for CVE-2026-41602, CVE-2026-42154

* Mon Apr 20 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-19
- Patch for CVE-2026-5160

* Thu Apr 02 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-18
- Patch for CVE-2026-33216, CVE-2026-29785

* Fri Mar 27 2026 Sindhu Karri <lakarri@microsoft.com> - 1.31.0-17
- Added patch to fix the issue reported in https://microsoft.visualstudio.com/OS/_workitems/edit/61041768
  Fix in telegraf to support cisco telemetry plugin that collects telemetry data from cisco NXOS switches.
  
* Fri Mar 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-16
- Patch for CVE-2026-4645

* Fri Feb 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-15
- Patch for CVE-2026-26014, CVE-2026-2303, CVE-2025-58190, CVE-2025-47911

* Fri Feb 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-14
- Patch for CVE-2025-11065

* Fri Feb 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-13
- Patch for CVE-2026-27571

* Mon Dec 08 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-12
- Patch for CVE-2025-10543

* Tue Nov 18 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.31.0-11
- Patch for CVE-2025-47913

* Tue Apr 22 2025 Mayank Singh <mayansingh@microsoft.com> - 1.31.0-10
- Fix CVE-2025-22872 with an upstream patch

* Thu Apr 17 2025 Sudipta Pandit <sudpandit@microsoft.com> - 1.31.0-9
- Patch CVE-2025-30215

* Wed Apr 02 2025 Mayank Singh <mayansingh@microsoft.com> - 1.31.0-8
- Fix CVE-2024-35255 and CVE-2025-27144 with an upstream patch

* Mon Mar 31 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.31.0-7
- Patch CVE-2025-30204

* Wed Mar 26 2025 Sreeniavsulu Malavathula <v-smalavathu@microsoft.com> - 1.31.0-6
- Fix CVE-2025-22870, CVE-2024-51744 with an upstream patch

* Wed Mar 05 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.31.0-5
- Patch CVE-2025-22868, CVE-2025-22869

* Tue Dec 31 2024 Rohit Rawat <rohitrawat@microsoft.com> - 1.31.0-4
- Patch CVE-2024-45338

* Wed Dec 18 2024 Aurelien Bombo <abombo@microsoft.com> - 1.31.0-3
- Patch CVE-2024-45337

* Thu Jul 11 2024 Sumedh Sharma <sumsharma@microsoft.com> - 1.31.0-2
- Add patch for CVE-2024-37298

* Tue Jun 18 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 1.31.0-1
- Auto-upgrade to 1.31.0 - Address CVEs

* Thu Mar 28 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.29.4-1
- Auto-upgrade to 1.29.4 - Azure Linux 3.0 Package Upgrades
- Remove additional logging as it has been added upstream

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.27.3-4
- Bump release to rebuild with go 1.20.10

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
