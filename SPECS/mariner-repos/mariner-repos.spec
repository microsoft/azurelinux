Summary:        CBL-Mariner repo files, gpg keys
Name:           mariner-repos
Version:        1.0
Release:        7%{?dist}
License:        Apache License
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Source0:        MICROSOFT-RPM-GPG-KEY
Source1:        mariner-official-base.repo
Source2:        mariner-official-update.repo
Vendor:         Microsoft Corporation
Distribution:   mariner
Provides:       mariner-repos
BuildArch:      noarch

%description
CBL-Mariner repo files and gpg keys

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/yum.repos.d

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/etc/pki/rpm-gpg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
/etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY
%config(noreplace) /etc/yum.repos.d/mariner-official-base.repo
%config(noreplace) /etc/yum.repos.d/mariner-official-update.repo

%changelog
*   Fri Jul 31 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-7
-   Fixing distro name.
*   Fri Jul 17 2020 Andrew Phelps <anphel@microsoft.com> 1.0-6
-   Set sslverify=1 in [mariner-official-base] and [mariner-official-update]
*   Wed Nov 27 2019 Pawel Winogrodzki <pawelwi@microsoft.com> 1.0-5
-   Removing outdated repository configuration
*   Fri Nov 22 2019 Andrew Phelps <anphel@microsoft.com> 1.0-4
-   Use $releasever and $basearch variables
*   Tue Oct 29 2019 Andrew Phelps <anphel@microsoft.com> 1.0-3
-   Separate repo configs for official-base and official-update
*   Wed Oct 23 2019 Andrew Phelps <anphel@microsoft.com> 1.0-2
-   Add mariner-official.repo
*   Wed Sep 04 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0-1
-   Original version for CBL-Mariner.
