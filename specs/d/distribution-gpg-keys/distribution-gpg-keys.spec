# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		distribution-gpg-keys
Version:	1.117
Release: 2%{?dist}
Summary:	GPG keys of various Linux distributions

License:	CC0-1.0
URL:		https://github.com/xsuchy/distribution-gpg-keys
# Sources can be obtained by
# git clone git://github.com/xsuchy/distribution-gpg-keys.git
# cd distribution-gpg-keys
# tito build --tgz
Source0:	%{name}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?fedora} > 0
Suggests:	ubu-keyring
Suggests:	debian-keyring
Suggests:	archlinux-keyrings
Suggests:   %{name}-copr
%endif

%description
GPG keys used by various Linux distributions to sign packages.

%package copr
Summary: GPG keys for Copr projects
BuildArch: noarch

%description copr
GPG keys used by Copr projects.

%prep
%setup -q


%build
#nothing to do here


%install
mkdir -p %{buildroot}%{_datadir}/%{name}/
cp -a keys/* %{buildroot}%{_datadir}/%{name}/


%files
%license LICENSE
%doc README.md SOURCES.md
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/copr

%files copr
%license LICENSE
%{_datadir}/%{name}/copr

%changelog
* Tue Feb 03 2026 Pavel Raiskup <pavel@raiskup.cz> 1.117-1
- Add Fedora 46 key
- Add Remi's key for 2026 (Fedora 44 and 45)
- update copr keys

* Tue Jan 27 2026 Pavel Raiskup <pavel@raiskup.cz> 1.116-1
- Add CentOS PQC signing keys
- Add RHEL PQC signing keys
- suse: Update RPM-GPG-KEY-SuSE-SLE-12
- Refresh CentOS SIG Extras key
- Update CentOS SIG keys downlod script
- Add missing CentOS SIG keys
- Add new Slack key used by versions 4.47 and above
- Add openSUSE Leap SLE imports
- Add Slack key

* Mon Nov 10 2025 Miroslav Suchý <msuchy@redhat.com> 1.115-1
- update copr keys
- Update for openSUSE 16 keys
- Update changelog
- Microsoft: add 2025 & open tech keys
- alpine-linux: Add loongarch64 key
- fedora: Update rawhide symlink

* Fri Aug 08 2025 Pavel Raiskup <praiskup@redhat.com> 1.114-1
- Add Fedora 45 key

* Tue Jun 17 2025 Pavel Raiskup <praiskup@redhat.com> 1.113-1
- Add Rocky Linux 10 keys

* Thu Jun 05 2025 Neal Gompa <neal@gompa.dev> 1.112-1
- Add FreeBSD keys
- Fix AlmaLinux name and alphabetical ordering of distros
- Add AlmaLinux EPEL AltArch Key

* Fri May 16 2025 Miroslav Suchý <msuchy@redhat.com> 1.111-1
- add link to sources of OpenWRT
- update copr keys
- Add OpenWrt keys
- Add RHEL 10 keys

* Fri Feb 14 2025 Pavel Raiskup <praiskup@redhat.com> 1.110-1
- Add keys for el-10 rpmfusion-free and nonfree
- Add symlinks to rpmfusion 42 and 43
- Navy Linux GPG key Update

* Thu Feb 06 2025 Miroslav Suchý <msuchy@redhat.com> 1.109-1
- update copr keys
- fedora: Update rawhide symlink
- Update keys for Azure Linux and Kylin

* Fri Jan 31 2025 Miroslav Suchý <msuchy@redhat.com> 1.108-1
- update copr keys
- alma: Add AlmaLinux 10 key
- add Remi 2025 key

* Wed Jan 15 2025 Miroslav Suchý <msuchy@redhat.com> 1.107-1
- Add Fedora 44 key
- Update Mageia gpg key

* Mon Dec 02 2024 Miroslav Suchý <msuchy@redhat.com> 1.106-1
- update copr keys
- add link for remi/EL-10 key

* Mon Aug 12 2024 Miroslav Suchý <msuchy@redhat.com> 1.105-1
- update copr keys
- add fedora 43 keys and change rawhide symlink
- Refresh GPG keys for Dell

* Wed Jun 12 2024 Miroslav Suchý <msuchy@redhat.com> 1.104-1
- update copr keys
- Add RPM-GPG-KEY-CentOS-Official-SHA256

* Mon Jun 03 2024 Miroslav Suchý <msuchy@redhat.com> 1.103-1
- update copr keys
- add FFmpeg, LibreWolf, Monero, VideoLAN, and yt-dlp keys
- Add CentOS 10 and EPEL 10 GPG keys
- add Alpine Linux and postmarketOS keys

* Fri Mar 08 2024 Miroslav Suchý <msuchy@redhat.com> 1.102-1
- update copr keys
- Create cathugger.asc
- Create zzz.key.asc
- Create idk.key.asc
- Create hulahoop.asc
- Create adrelanos.asc
- Create makemkv_pub.txt

* Wed Feb 14 2024 Miroslav Suchý <msuchy@redhat.com>
- add F42 key and move rawhide link
- update copr keys
- update postgresql keys

* Tue Jan 09 2024 Miroslav Suchý <msuchy@redhat.com> 1.100-1
- update copr keys
- Add remi 2024 Key

* Thu Dec 28 2023 Miroslav Suchý <msuchy@redhat.com> 1.99-1
- update copr keys
- Add Qubes OS 4.2 release key
- Split AlmaLinux OS 8 GPG public keys to fix microdnf
- Update AlmaLinux OS 8 public key

* Thu Oct 12 2023 Miroslav Suchý <msuchy@redhat.com> 1.98-1
- update copr keys
- Add openSUSE Backports 2023 key
- Update Amazon Linux 2023 public key

* Tue Sep 19 2023 Miroslav Suchý <msuchy@redhat.com> 1.97-1
- update copr keys
- add script to check all keys
- remove expired jenkins key
- update expired intel security key
- update expired navy linux key
- update expired bluejeans key
- add script to check expiration
- Add the key for pkgs.k8s.io (Kubernetes)

* Thu Sep 14 2023 Miroslav Suchý <msuchy@redhat.com> 1.96-1
- Restructure openSUSE GPG keys

* Thu Sep 14 2023 Miroslav Suchý <msuchy@redhat.com> 1.95-1
- new release to test new release process 

* Thu Sep 14 2023 Miroslav Suchý <msuchy@redhat.com> 1.94-1
- new release because testing new release process 

* Thu Sep 14 2023 Miroslav Suchý <msuchy@redhat.com> 1.93-1
- Add SUSE ALP signing keys
- Add SLE 2023 signing keys

* Mon Sep 04 2023 Miroslav Suchý <msuchy@redhat.com> 1.92-1
- add symlinkg to rpmfusion 40 and 41
- update copr keys
- add remi fedora 39 link to 2023 key

* Thu Aug 10 2023 Miroslav Suchý <msuchy@redhat.com> 1.91-1
- update Google key

* Thu Aug 10 2023 Miroslav Suchý <msuchy@redhat.com> 1.90-1
- add Fedora 41 key
- Add source URL for AL2023
- update copr keys

* Fri Jun 16 2023 Pavel Raiskup <praiskup@redhat.com> 1.89-1
- Update expired RPM-GPG-KEY-Mageia key
- Add keys for Azure Linux

* Sun May 28 2023 Miroslav Suchý <msuchy@redhat.com> 1.88-1
- update copr keys
- add per distro/version link to proper key for remi
- update brave keys
- add Docker key
- add mullvad key

* Wed Apr 26 2023 Miroslav Suchý <msuchy@redhat.com> 1.87-1
- update copr keys
- update virtualbox key
- update openSUSE-Backports key
- update skype key

* Wed Apr 05 2023 Miroslav Suchý <msuchy@redhat.com> 1.86-1
- update copr keys
- Add Jenkins 2023
- Add keys for Bacula & Baculum
- Add keys for Google Cloud
- Add VeraCrypt keys
- add Element keys

* Thu Mar 09 2023 Miroslav Suchý <msuchy@redhat.com> 1.85-1
- update copr keys
- Add Amazon Linux 2023 and remove Amazon Linux 2022 key
- add AnyDesk GPG key

* Thu Feb 16 2023 Miroslav Suchý <msuchy@redhat.com> 1.84-1
- add tumbleweed key
- Added RPM Fusion keys for Fedora 39.
- update copr keys
- add elastic gpg key

* Mon Jan 30 2023 Miroslav Suchý <msuchy@redhat.com> 1.82-1
- move symlink of fedora-rawhide to fedora-39
- add openEuler new key
- update copr keys
- add fedora 40 gpg key

* Fri Jan 06 2023 Miroslav Suchý <msuchy@redhat.com> 1.81-1
- update copr keys
- Add remi 2023 key
- add TeamViewer key

* Fri Dec 16 2022 Miroslav Suchý <msuchy@redhat.com> 1.80-1
- add SME Server keys
- update copr keys

* Mon Nov 14 2022 Miroslav Suchý <msuchy@redhat.com> 1.79-1
- fix Fedora 39 key
- update copr keys

* Mon Oct 10 2022 Miroslav Suchý <msuchy@redhat.com> 1.78-1
- update copr keys
- change license to spdx

* Sun Aug 28 2022 Miroslav Suchý <msuchy@redhat.com> 1.77-1
- Add openEuler GPG Key
- update copr keys
- Add Oracle Linux 9 key
- Add Fedora 10 key

* Wed Aug 10 2022 Miroslav Suchý <msuchy@redhat.com> 1.76-1
- add fedora 38 and 39

* Mon Aug 08 2022 Miroslav Suchý <msuchy@redhat.com> 1.75-1
- update copr keys
- Add Amazon Linux 2022 GPG key

* Fri Jul 22 2022 Miroslav Suchý <msuchy@redhat.com> 1.74-1
- Add Anolis OS GPG Keys

* Sun Jul 17 2022 Miroslav Suchý <msuchy@redhat.com> 1.73-1
- update copr keys
- Add Rocky Linux 9 Keys and Refresh 8

* Tue Jun 07 2022 Miroslav Suchý <msuchy@redhat.com> 1.72-1
- update copr keys
- Add Circle Linux GPG Keys

* Tue May 17 2022 Miroslav Suchý <msuchy@redhat.com> 1.71-1
- Refresh AlmaLinux keys to add AlmaLinux 9 key

* Tue May 10 2022 Miroslav Suchý <msuchy@redhat.com> 1.70-1
- update copr keys
- Add RHEL9 keys
- Add RPM Fusion keys for Fedora 38

* Mon May 02 2022 Miroslav Suchý <msuchy@redhat.com> 1.69-1
- update copr keys
- Add RPM Fusion keys for EL 9

* Thu Apr 07 2022 Miroslav Suchý <msuchy@redhat.com> 1.68-1
- update copr keys

* Tue Mar 08 2022 Pavel Raiskup <praiskup@redhat.com> 1.67-1
- Refresh all CentOS SIG keys (rhbz#2059424)

* Wed Mar 02 2022 Miroslav Suchý <msuchy@redhat.com> 1.66-1
- update copr keys
- centos: Add new CentOS Extras SIG key (SHA256)

* Tue Feb 22 2022 Miroslav Suchý <msuchy@redhat.com> 1.65-1
- update copr keys
- Add remi 2022 key

* Wed Feb 02 2022 Pavel Raiskup <praiskup@redhat.com> 1.64-1
- move Fedora Rawhide key to F37

* Wed Feb 02 2022 Pavel Raiskup <praiskup@redhat.com> 1.63-1
- Add EuroLinux 9 key
- Add CentOS Extras SIG key
- Add symlink for CentOS Stream 9 to main official key

* Mon Jan 24 2022 Miroslav Suchý <msuchy@redhat.com> 1.62-1
- add Fedora 37
- update copr keys

* Thu Jan 20 2022 Miroslav Suchý <msuchy@redhat.com> 1.61-1
- add new MySQL key
- update copr keys

* Thu Nov 04 2021 Miroslav Suchý <msuchy@redhat.com> 1.60-1
- update copr keys
- Add Navy Linux RPM GPG official key

* Wed Oct 27 2021 Miroslav Suchý <msuchy@redhat.com> 1.59-1
- update copr keys
- Add EPEL9 key
- Move Rawhide to F36
- Add keys of RPM Fusion Fedora 37

* Fri Oct 01 2021 Miroslav Suchý <msuchy@redhat.com> 1.58-1
- update copr keys
- Add keys of Fedora rpmfusion 36

* Sat Sep 04 2021 Miroslav Suchý <msuchy@redhat.com> 1.57-1
- update copr keys

* Mon Jul 26 2021 Miroslav Suchý <msuchy@redhat.com> 1.56-1
- update copr keys

* Mon Jun 28 2021 Miroslav Suchý <msuchy@redhat.com> 1.55-1
- update copr keys
- Add Rocky Linux Keys

* Mon Jun 07 2021 Miroslav Suchý <msuchy@redhat.com> 1.54-1
- update copr keys
- Add openSUSE Backports OBS project key
- Add SUSE's package signing keys

* Thu May 20 2021 Miroslav Suchý <msuchy@redhat.com> 1.53-1
- update copr keys

* Thu Apr 22 2021 Miroslav Suchý <msuchy@redhat.com> 1.52-1
- update copr keys

* Mon Mar 01 2021 Miroslav Suchý <msuchy@redhat.com> 1.51-1
- update copr keys
- Add missing CentOS SIG keys
- add Fedora 36 key
- matrix of opengpg availablity
- add intel new gpg key

* Wed Feb 17 2021 Miroslav Suchý <msuchy@redhat.com> 1.50-1
- Add symlinks for F35

* Wed Feb 17 2021 Miroslav Suchý <msuchy@redhat.com> 1.49-1
- update copr keys
- add mariadb key
- document type61
- add Alma Linux

* Fri Feb 05 2021 Miroslav Suchý <msuchy@redhat.com> 1.48-1
- add Fedora 35
- update copr keys

* Mon Jan 18 2021 Miroslav Suchý <msuchy@redhat.com> 1.47-1
- update copr keys
- add Remi 2021 key

* Thu Dec 17 2020 Miroslav Suchý <msuchy@redhat.com> 1.46-1
- update copr keys

* Mon Nov 23 2020 Miroslav Suchý <msuchy@redhat.com> 1.45-1
- update copr keys
- update README with list of keys
- correct symlinks for rpmfusion 33/34

* Mon Oct 19 2020 Miroslav Suchý <msuchy@redhat.com> 1.44-1
- update copr keys
- update link to fedora rawhide
- add Fedora ELN keys
- add Zoom gpg key
- Add Oracle Linux GPG keys

* Wed Oct 07 2020 Miroslav Suchý <msuchy@redhat.com> 1.43-1
- now really add f33
- add f33 releasers

* Mon Oct 05 2020 Miroslav Suchý <msuchy@redhat.com> 1.42-1
- update copr keys
- add rpmfusion 33 and update latest links

* Thu Aug 06 2020 Miroslav Suchý <msuchy@redhat.com> 1.41-1
- add Fedora 34 key
- update copr keys
- add Qubes signing keys

* Mon Jul 13 2020 Miroslav Suchý <msuchy@redhat.com> 1.40-1
- update copr keys
- Add Datto's third party repository GPG keys
- Add EuroLinux keys

* Thu May 28 2020 Miroslav Suchý <msuchy@redhat.com> 1.39-1
- update copr keys
- add intel gpg key
- add RosaLinux GPG keyring

* Tue Apr 21 2020 Miroslav Suchý <msuchy@redhat.com> 1.38-1
- update copr keys
- add mysql gpg key
- add BlueJeans key
- Add symlink from CentOS 8 to CentOS Official key
- add remi 2020 key and update for f32 branch

* Tue Feb 18 2020 Miroslav Suchý <msuchy@redhat.com> 1.37-1
- update copr keys
- f29 is eoled
- Symlink Rawhide to Fedora 33 key
- Add remi 2020 key

* Wed Jan 29 2020 Miroslav Suchý <msuchy@redhat.com> 1.36-1
- update copr keys
- add Fedora 33 gpg key
- Add keys for IUS repository (https://ius.io)

* Thu Sep 26 2019 Miroslav Suchý <msuchy@redhat.com> 1.35-1
- update copr keys
- Add key for Amazon Linux 2

* Tue Aug 20 2019 Miroslav Suchý <msuchy@redhat.com> 1.34-1
- update copr keys
- fix whitespace error in fedora-32 key (rhbz#1743422)
- Add RPM Fusion keys for fedora 32

* Fri Aug 16 2019 Miroslav Suchý <msuchy@redhat.com> 1.33-1
- add EPEL-8
- add CentOS 8 keys
- add Fedora 32 key

* Mon Jul 08 2019 Miroslav Suchý <msuchy@redhat.com> 1.32-1
- Update Copr keys
- Add OpenMandriva package signing key
- add Zimbra key

* Thu May 16 2019 Miroslav Suchý <msuchy@redhat.com> 1.31-1
- update Copr keys

* Thu Apr 11 2019 Miroslav Suchý <msuchy@redhat.com> 1.30-1
- Deleted old Copr keys and added new Copr keys
- readme: add note about Debian, Ubuntu and Arch
- update list of keys in README
- add brave key
- Add remi 2019 key

* Tue Feb 19 2019 Miroslav Suchý <msuchy@redhat.com> 1.29-1
- update Copr keys
- add F31 key and point rawhide to F31
- add Fedora iot keys

* Thu Jan 31 2019 Miroslav Suchý <msuchy@redhat.com> 1.28-1
- update copr keys
- Add cuda 2019 - el8 - fedora 31 keys (rpmfusion)

* Wed Jan 02 2019 Miroslav Suchý <msuchy@redhat.com> 1.27-1
- update copr keys

* Fri Nov 16 2018 Miroslav Suchý <msuchy@redhat.com> 1.26-1
- add RPM-GPG-KEY-redhat8-release

* Thu Nov 15 2018 Miroslav Suchý <msuchy@redhat.com> 1.25-1
- update copr keys
- add RPM-GPG-KEY-redhat8-beta key
- add RPM-GPG-KEY-redhat-auxiliary2

* Thu Nov 08 2018 Miroslav Suchý <msuchy@redhat.com> 1.24-1
- update Copr keys
- add Microsoft key

* Fri Sep 14 2018 Miroslav Suchý <msuchy@redhat.com> 1.23-1
- update copr keys
- add rawhide as symlink to F30

* Sun Aug 12 2018 Miroslav Suchý <msuchy@redhat.com> 1.22-1
- update copr keys
- add fedora 30

* Tue Apr 24 2018 Miroslav Suchý <msuchy@redhat.com> 1.21-1
- Add openSUSE Package Signing Key

* Mon Apr 16 2018 Miroslav Suchý <msuchy@redhat.com> 1.20-1
- add scientific linux key
- update copr keys
- add Fedora 29 key
- Update keys for rpmfusion
- Add rpmfusion f29 f30 keys for free nonfree

* Wed Feb 21 2018 Miroslav Suchý <msuchy@redhat.com> 1.19-1
- update copr keys

* Sun Jan 21 2018 Miroslav Suchý <msuchy@redhat.com> 1.18-1
- add UnitedRPMs
- Add remi 2018 key
- update Copr keys

* Thu Dec 21 2017 Miroslav Suchý <msuchy@redhat.com> 1.17-1
- update Copr keys

* Mon Nov 20 2017 Miroslav Suchý <msuchy@redhat.com> 1.16-1
- update Copr keys

* Tue Sep 19 2017 Miroslav Suchý <msuchy@redhat.com> 1.15-1
- update Copr keys
- add new remi key

* Mon Aug 21 2017 Miroslav Suchý <msuchy@redhat.com> 1.14-1
- update Copr keys
- add remi's repository gpg key
- add jpackage gpg key
- add CalcForge gpg key
- add virtualbox gpg key
- add PostgreSQL RPM Building Project gpg keys
- add Skype gpg key
- add Google gpg key
- add dell public key
- add RPM-GPG-KEY-adobe-linux
- add Dropbox gpg key
- add RPM-GPG-KEY-fedora-28-primary
- add rpmfusion 28

* Mon Jul 31 2017 Miroslav Suchý <msuchy@redhat.com> 1.13-1
- update Copr keys
- add fedora modularity gpg key
- add SCL SIG key

* Thu Jul 13 2017 Miroslav Suchý <msuchy@redhat.com> 1.12-1
- update Copr keys
- Update Red Hat Keys

* Mon Apr 03 2017 Miroslav Suchý <msuchy@redhat.com> 1.11-1
- update Copr keys
- update source for rpmfusion
- Update symlinks for rpmfusion lastest/rawhide
- Add rpmfusion free/nonfree 27 keys
- Add rpmfusion free/nonfree 26 keys

* Thu Mar 16 2017 Miroslav Suchý <msuchy@redhat.com> 1.10-1
- update COPR keys
- add F27 key

* Thu Dec 01 2016 Miroslav Suchý <msuchy@redhat.com> 1.9-1
- add new copr keys
- add Fedora 26 keys
- add more CentOS 7 keys (aarch64, debug, SIGs, testing)

* Mon Oct 24 2016 Miroslav Suchý <msuchy@redhat.com> 1.8-1
- update copr gpg keys
- README.md: Indicate what keys are actually included
- add rpmfusion F19 keys
- add note how to verify gpg key using fingerprint
- RPMFusion add fedora-20 and fedora-21 keys
- RPMFusion add rpmfusion el-7 keys
- RPMFusion add fedora-25 keys
- use symbol links .
- Add a crucial information to README.md

* Mon Sep 12 2016 Miroslav Suchý <msuchy@redhat.com> 1.7-1
- do not use weak deps on rhel

* Mon Sep 12 2016 Miroslav Suchý <msuchy@redhat.com> 1.6-1
- Rename mageia pubkey to RPM-GPG-KEY-Mageia

* Mon Aug 08 2016 Miroslav Suchý <msuchy@redhat.com> 1.5-1
- move copr keys to subpackage
- update copr gpg keys
- add RPM-GPG-KEY-CentOS-SIG-AltArch-7-ppc64le
- add F25 keys

* Mon Mar 14 2016 Miroslav Suchý <msuchy@redhat.com> 1.4-1
- update SOURCES
- update copr gpg keys
- add mageia gpg keys

* Tue Feb 02 2016 Miroslav Suchý <msuchy@redhat.com> 1.3-1
- add copr keys
- added obsolete gpg keys
- document from where those keys can be originally obtained
- suggest installations of other keyrings
- do not include email in changelog items

* Fri Oct 16 2015 Miroslav Suchý <msuchy@redhat.com> 1.2-1
- document how to do release
- change license to CC-0

* Thu Oct 15 2015 Miroslav Suchý <msuchy@redhat.com> 1.1-1
- initial package



