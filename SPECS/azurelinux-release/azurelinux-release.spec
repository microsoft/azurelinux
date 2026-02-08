
%define dist_version 3
%define distro_release_version_no_time %(echo %{distro_release_version} | cut -d. -f 1-3)

Summary:        Azure Linux release files
Name:           azurelinux-release
Version:        %{dist_version}.0
Release:        39%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://aka.ms/azurelinux

Source1:        90-default.preset
Source2:        90-default-user.preset
Source3:        99-default-disable.preset
Source4:        15-azurelinux-default.conf

Provides:       system-release
Provides:       system-release(%{version})

Conflicts:      mariner-rpm-macros < 2.0-25

BuildArch:      noarch

BuildRequires:  systemd-bootstrap-rpm-macros

%description
Azure Linux release files such as dnf configs and other %{_sysconfdir}/ release related files
and systemd preset files that determine which services are enabled by default.

%install
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_rpmmacrodir}

cat <<-"EOF" > %{buildroot}%{_libdir}/azurelinux-release
%{distribution} %{version}
AZURELINUX_BUILD_NUMBER=%{distro_release_version_no_time}
EOF
ln -sv ..%{_libdir}/azurelinux-release %{buildroot}%{_sysconfdir}/azurelinux-release

cat <<-"EOF" > %{buildroot}%{_libdir}/lsb-release
DISTRIB_ID="azurelinux"
DISTRIB_RELEASE="%{distro_release_version_no_time}"
DISTRIB_CODENAME=AzureLinux
DISTRIB_DESCRIPTION="%{distribution} %{version}"
EOF
ln -sv ..%{_libdir}/lsb-release %{buildroot}%{_sysconfdir}/lsb-release

cat <<-"EOF" > %{buildroot}%{_libdir}/os-release
NAME="Microsoft %{distribution}"
VERSION="%{distro_release_version_no_time}"
ID=azurelinux
ID_LIKE=fedora
VERSION_ID="%{version}"
PRETTY_NAME="Microsoft %{distribution} %{version}"
ANSI_COLOR="1;34"
HOME_URL="%{url}"
BUG_REPORT_URL="%{url}"
SUPPORT_URL="%{url}"
EOF
ln -sv ..%{_libdir}/os-release %{buildroot}%{_sysconfdir}/os-release

cat <<-"EOF" > %{buildroot}%{_libdir}/issue
Welcome to Microsoft %{distribution} %{version} (%{_arch}) - (\l)
EOF
ln -sv ..%{_libdir}/issue %{buildroot}%{_sysconfdir}/issue

cat <<-"EOF" > %{buildroot}%{_libdir}/issue.net
Welcome to Microsoft %{distribution} %{version} (%{_arch})
EOF
ln -sv ..%{_libdir}/issue.net %{buildroot}%{_sysconfdir}/issue.net

install -d -m 755 %{buildroot}%{_sysconfdir}/issue.d

cat <<-"EOF" > %{buildroot}%{_rpmmacrodir}/macros.dist
# dist macros.

%%__bootstrap         ~bootstrap
%%azl                 %{dist_version}
%%azl%{dist_version}  1
%%dist                .azl%{dist_version}%%{?with_bootstrap:%%{__bootstrap}}
%%dist_vendor         %{vendor}
%%dist_name           %{distribution}
%%dist_home_url       %{url}
%%dist_bug_report_url %{url}
%%dist_debuginfod_url %{url}
EOF

# Default presets for system and user
install -Dm0644 %{SOURCE1} -t %{buildroot}%{_presetdir}/
install -Dm0644 %{SOURCE2} -t %{buildroot}%{_userpresetdir}/

# Default disable presets
install -Dm0644 %{SOURCE3} -t %{buildroot}%{_presetdir}/
install -Dm0644 %{SOURCE3} -t %{buildroot}%{_userpresetdir}/

# Default sysctl settings
install -Dm0644 %{SOURCE4} -t %{buildroot}%{_sysctldir}/

%files
%defattr(-,root,root,-)
%{_libdir}/azurelinux-release
%{_libdir}/lsb-release
%{_libdir}/os-release
%{_libdir}/issue
%{_libdir}/issue.net
%{_sysconfdir}/azurelinux-release
%{_sysconfdir}/lsb-release
%{_sysconfdir}/os-release
%config(noreplace) %{_sysconfdir}/issue
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%{_rpmmacrodir}/macros.dist
%{_presetdir}/*.preset
%{_userpresetdir}/*.preset
%{_sysctldir}/*.conf

%changelog
* Mon Jan 19 2026 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-39
- Bump release for Feb 2026 Update

* Tue Dec 30 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-38
- Bump release for January 2026 Update

* Fri Dec 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-37
- Bump release for December 2025 Update

* Wed Nov 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-36
- Bump release for November 2025 Update

* Thu Oct 30 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-35
- Bump release for October 2025 Update 2

* Tue Oct 07 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-34
- Bump release for October 2025 Update

* Thu Sep 04 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-33
- Bump release for September 2025 Update

* Fri Aug 22 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-32
- Bump release for Aug 2025 Update 2

* Tue Jul 22 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-31
- Bump release for Aug 2025 Update

* Mon Jun 30 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-30
- Bump release for July 2025 Update

* Fri May 30 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-29
- Bump release for June 2025 Update

* Thu May 15 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0-28
- Bump release for May 2025 Update 2

* Tue Apr 29 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-27
- Bump release for May 2025 Update

* Mon Mar 31 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-26
- Bump release for April 2025 Update

* Tue Feb 25 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-25
- Bump release for March 2025 Update

* Wed Jan 15 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-24
- Bump release for January 2025 Update 2

* Sat Dec 21 2024 Jon Slobodzian <joslobo@microsoft.com> - 3.0-23
- Bump release for January 2025 Update

* Fri Nov 22 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-22
- Bump release for December 2024 Update

* Fri Oct 25 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-21
- Bump release for November 2024

* Fri Sep 27 2024 Rachel Menge <rachelmenge@microsoft.com> - 3.0-20
- Enable iptables as default firewall

* Wed Sep 25 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-19
- Bump release for October 2024 Update

* Thu Aug 08 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-18
- Bump release for August 2024 Update 1

* Fri Jul 26 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-17
- Azure Linux 3.0 August Release

* Fri Jul 05 2024 Sam Meluch <sammeluch@microsoft.com> - 3.0-16
- Azure Linux 3.0 July Preview Release 1

* Thu Jun 21 2024 Andrew Phelps <anphel@microsoft.com> - 3.0-15
- Azure Linux 3.0 June Preview Release 2

* Wed Jun 12 2024 Sam Meluch <sammeluch@microsoft.com> - 3.0-14
- Azure Linux 3.0 June Preview Release 1

* Fri May 24 2024 Sam Meluch <sammeluch@microsoft.com> - 3.0-13
- Azure Linux 3.0 May Preview Release 2

* Thu May 09 2024 Sam Meluch <sammeluch@microsoft.com> - 3.0-12
- Azure Linux 3.0 May Preview Release 1

* Tue May 07 2024 Sudipta Pandit <sudpandit@microsoft.com> - 3.0-11
- Enable ephemeral-disk-warning.service in 90-default-target

* Wed Apr 24 2024 Sam Meluch <sammeluch@microsoft.com> - 3.0-10
- Azure Linux 3.0 April Preview Release 4

* Wed Apr 17 2024 Sam Meluch <sammeluch@microsoft.com> - 3.0-9
- Azure Linux 3.0 April Preview Release 3

* Mon Apr 08 2024 Sam Meluch <sammeluch@microsoft.com> - 3.0-8
- Azure Linux 3.0 April Preview Release 2

* Tue Mar 19 2024 Dan Streetman <ddstreet@microsoft.com> - 3.0-7
- add 15-azurelinux-default.conf sysctl config

* Thu Mar 14 2024 Cameron Baird <cameronbaird@microsoft.com> - 3.0-6
- Enable waagent.service in 90-default.preset

* Thu Mar 07 2024 Andrew Phelps <anphel@microsoft.com> - 3.0-5
- Add 'Microsoft' to names in release files and welcome message
- Restore full version number in release files

* Thu Feb 22 2024 Dan Streetman <ddstreet@microsoft.com> - 3.0-4
- remove %%config(noreplace) from *-release files
- define dist_version and use local macros
- move *-release and issue files under %%_libdir and make %%_sysconfdir symlinks
- use consistent creation of here documents
- add issue.d dir
- move macros.dist into this package
- Add default systemd presets

* Thu Feb 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.0-3
- Renamed mariner-release to azurelinux-release file
- Renamed MARINER_BUILD_NUMBER property to AZURELINUX_BUILD_NUMBER

* Wed Jan 31 2024 Amrita Kohli <amritakohli@microsoft.com> - 3.0-2
- Remove kernel info from welcome banner for security compliance.

* Wed Nov 29 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.0-1
- First version of Azure Linux 3.0.  Includes minimal rebranding changes.

* Fri Oct 20 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-53
- Bump release for October 2023 Release 2

* Wed Sep 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-52
- Bump release for October 2023 Release

* Wed Sep 20 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-51
- Bump release for September 2023 Update 2

* Mon Sep 04 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-50
- Bump release for September 2023 Update

* Mon Aug 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-49
- Bump release for August 2023 Release 3

* Thu Aug 10 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-48
- Bump release for August 2023 Release 2

* Thu Aug 10 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-47
- Bump release for August 2023 Update 2

* Fri Aug 04 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-46
- Bump release for August 2023 Release

* Mon Jul 10 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-45
- Bump release for July 2023 Update

* Thu Jun 29 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-44
- Bump release for June 2023 Update 3

* Sun Jun 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-43
- Bump release for June 2023 Update 2

* Sat Jun 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-42
- Bump release for June 2023 Update

* Fri May 26 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-41
- Bump release for May 2023 Update 2

* Tue May 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-40
- Bump release for May 2023 Update

* Tue May 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-39
- Bump release for May 2023 Update

* Sat Apr 22 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0-38
- Updating version for April update 2

* Thu Apr 06 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0-37
- Updating version for April update.

* Fri Mar 17 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-36
- Updating version for March 2023 update 2.

* Thu Mar 02 2023 Andrew Phelps <anphel@microsoft.com> - 2.0-35
- Updating version for March 2023 update 1.

* Tue Feb 14 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0-34
- Updating version for February update 2.

* Tue Feb 07 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0-33
- Updating version for February update.

* Tue Jan 24 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0-32
- Updating version for January update 2.

* Thu Jan 05 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0-31
- Updating version for January update.

* Mon Dec 19 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-30
- Updating version for December update 3.

* Sat Dec 10 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-29
- Updating version for December update 2.

* Thu Dec 01 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-28
- Updating version for December update.

* Mon Nov 21 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 2.0.27
- Updating version for November update 2.

* Wed Nov 09 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-26
- Updating version for November update.

* Sat Oct 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-25
- Updating version for a full October release.

* Tue Oct 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-24
- Updating version for October update.

* Fri Oct 07 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-23
- Updating version for October release.

* Fri Sep 23 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-22
- Updating version for September update 3.

* Fri Sep 16 2022 Andrew Phelps <anphel@microsoft.com> - 2.0.21
- Updating version for September update 2.

* Thu Sep 08 2022 Minghe Ren <mingheren@microsoft.com> - 2.0-20
- remove issue.net kernel part as sshd doesn't support the old-style telnet escape sequences

* Thu Sep 08 2022 Andrew Phelps <anphel@microsoft.com> - 2.0-19
- Updating version for September CVE update.

* Tue Aug 16 2022 Andrew Phelps <anphel@microsoft.com> - 2.0-18
- Updating version for August update 2.

* Wed Aug 03 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-17
- Updating version for August update.

* Tue Jul 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-16
- Updating version for July update 2.

* Fri Jul 08 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-15
- Updating version for July update.

* Sat Jun 25 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-14
- Updating version for June update 2.

* Wed Jun 08 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-13
- Updating version for June update.

* Sat May 21 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-12
- Updating version for May update.

* Tue Apr 19 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-11
- Updating version for GA Release Candidate

* Sat Apr 16 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-10
- Updating version for Preview-H Release.

* Sat Apr 09 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-9
- Updating version for Preview-G Release.

* Wed Mar 30 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-8
- Updating version for Preview-F Release.

* Fri Mar 4 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-7
- Updating version for Preview-E Release

* Thu Feb 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-6
- Surrounding 'VERSION_ID' inside 'os-release' with double quotes.

* Sun Feb 06 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-5
- Updating version for Preview D-Release

* Wed Jan 19 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-4
- CBL-Mariner 2.0 Public Preview C Release.
- License verified

* Thu Dec 16 2021 Jon Slobodzian <joslobo@microsoft.com> - 2.0-3
- CBL-Mariner 2.0 Public Preview B Release version with fixed repo configuration files.

* Mon Dec 13 2021 Jon Slobodzian <joslobo@microsoft.com> - 2.0-2
- CBL-Mariner 2.0 Public Preview A Release version.

* Thu Jul 29 2021 Jon Slobodzian <joslobo@microsoft.com> - 2.0-1
- Updating version and distrotag for future looking 2.0 branch.  Formatting fixes.
- Remove %%clean section, buildroot cleaning step (both automatically done by RPM)

* Wed Apr 27 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-16
- Updating version for April update

* Tue Mar 30 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-15
- Updating version for March update

* Mon Feb 22 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-14
- Updating version for February update

* Sun Jan 24 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-13
- Updating version for January update

* Mon Dec 21 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-12
- Updating version for December update.

* Fri Nov 20 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.0-11
- Updating version for November update

* Sat Oct 24 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-10
- Updating version for October update

* Fri Sep 04 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.0-9
- Remove empty %%post section, dropping dependency on /bin/sh

* Tue Aug 24 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-8
- Changing CBL-Mariner ID from "Mariner" to "mariner" to conform to standard.  Also updated Distrib-Description and Name per internal review.

* Tue Aug 18 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-7
- Restoring correct Name, Distribution Name, CodeName and ID.

* Fri Jul 31 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-6
- Updating distribution name.

* Wed Jul 29 2020 Nick Samson <nisamson@microsoft.com> - 1.0-5
- Updated os-release file and URL to reflect project naming

* Wed Jun 24 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-4
- Updated license for 1.0 release.

* Mon May 04 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-3
- Providing "system-release(releasever)" for the sake of DNF
- and other package management tools.

* Thu Jan 30 2020 Jon Slobodzian <joslobo@microsoft.com> 1.0-2
- Remove Microsoft name from distro version.

* Wed Sep 04 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0-1
- Original version for CBL-Mariner.
