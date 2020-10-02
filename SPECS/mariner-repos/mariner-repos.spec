Summary:        CBL-Mariner repo files, gpg keys
Name:           mariner-repos
Version:        1.0
Release:        11%{?dist}
License:        Apache License
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        MICROSOFT-RPM-GPG-KEY
Source1:        MICROSOFT-METADATA-GPG-KEY
Source2:        mariner-official-base.repo
Source3:        mariner-official-update.repo
Source4:        mariner-preview.repo

Requires(post): gpgme
Requires(post): rpm
Requires(preun): gpgme
Requires(preun): rpm
BuildArch:      noarch

%description
CBL-Mariner repo files and gpg keys

%package preview
Summary:    CBL-Mariner preview repo file.
Group:      System Environment/Base
Requires:   %{name} = %{version}-%{release}

%description preview
%{summary}

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/yum.repos.d

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/pki/rpm-gpg

%clean
rm -rf $RPM_BUILD_ROOT

%posttrans
gpg --import /etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY
gpg --import /etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY

%preun
# Remove the MICROSOFT-METADATA-GPG-KEY
gpg --batch --yes --delete-keys BC528686B50D79E339D3721CEB3E94ADBE1229CF
# Remove the MICROSOFT-RPM-GPG-KEY
gpg --batch --yes --delete-keys 2BC94FFF7015A5F28F1537AD0CD9FED33135CE90

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
/etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY
/etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY
%config(noreplace) /etc/yum.repos.d/mariner-official-base.repo
%config(noreplace) /etc/yum.repos.d/mariner-official-update.repo

%files preview
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/mariner-preview.repo

%changelog
*   Thu Oct 01 2020 Emre Girgin <sarsoma@microsoft.com> - 1.0-11
-   Change %%post scriptlet to %%posttrans in order to ensure it runs after %%postun during an upgrade.
*   Mon Sep 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.0-10
-   Adding configuration to access the preview repository.
-   Removing redundant 'Provides'.
*   Tue Aug 11 2020 Saravanan Somasundaram <sarsoma@microsoft.com> - 1.0-9
-   Enable GPG Check and Import
*   Mon Aug 10 2020 Saravanan Somasundaram <sarsoma@microsoft.com> - 1.0-8
-   Adding Metadata Key and Updating to Prod GPG Key.
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
