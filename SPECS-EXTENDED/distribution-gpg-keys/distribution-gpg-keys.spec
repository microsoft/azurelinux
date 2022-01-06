Name:		distribution-gpg-keys
Version:	1.60
Release:	2%{?dist}
Summary:	GPG keys of various Linux distributions

License:	CC0
URL:		https://github.com/xsuchy/distribution-gpg-keys
# Sources can be obtained by
# git clone git://github.com/xsuchy/distribution-gpg-keys.git
# cd distribution-gpg-keys
# tito build --tgz
Source0:	%{name}-%{version}.tar.gz
BuildArch:	noarch

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
* Wed Jan 5 2022 Cameron Baird <cameronbaird@microsoft.com>  - 1.60-2
- Add to SPECS-EXTENDED from Fedora

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

* Tue Apr 21 2020 Miroslav Suchý <miroslav@suchy.cz> 1.38-1
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

* Mon Oct 24 2016 Miroslav Suchý <miroslav@suchy.cz> 1.8-1
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



