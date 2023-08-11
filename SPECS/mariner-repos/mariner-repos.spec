Summary:        CBL-Mariner repo files, gpg keys
Name:           mariner-repos
Version:        1.0
Release:        16%{?dist}
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
Source5:        mariner-ui.repo
Source6:        mariner-ui-preview.repo
Source7:        mariner-extras.repo
Source8:        mariner-extras-preview.repo
Source9:        mariner-microsoft.repo
Source10:       mariner-microsoft-preview.repo
BuildArch:      noarch

Requires:       %{name}-shared = %{version}-%{release}

%description
CBL-Mariner repo files and gpg keys

%package preview
Summary:    CBL-Mariner preview repo file.
Group:      System Environment/Base
Requires:   %{name}-shared = %{version}-%{release}

%description preview
%{summary}

%package ui
Summary:    CBL-Mariner UI repo file.
Group:      System Environment/Base
Requires:   %{name}-shared = %{version}-%{release}

%description ui
%{summary}

%package ui-preview
Summary:    CBL-Mariner UI preview repo file.
Group:      System Environment/Base
Requires:   %{name}-ui = %{version}-%{release}

%description ui-preview

%package extras
Summary:  CBL-Mariner extras repository.
Group:    System Envrionment/Base
Requires: %{name}-shared = %{version}-%{release}

%description extras
%{summary}

%package extras-preview
Summary:  CBL-Mariner extras repository.
Group:    System Envrionment/Base
Requires: %{name}-shared = %{version}-%{release}

%description extras-preview
%{summary}

%package microsoft
Summary:  CBL-Mariner Microsoft repository.
Group:    System Envrionment/Base
Requires: %{name}-shared = %{version}-%{release}

%description microsoft
%{summary}

%package microsoft-preview
Summary:  CBL-Mariner Microsoft Preview repository.
Group:    System Envrionment/Base
Requires: %{name}-shared = %{version}-%{release}

%description microsoft-preview
%{summary}

%package shared
Summary:        Directories and files needed by all %{name} configurations.
Group:          System Environment/Base

%description shared
%{summary}

Requires(post):  gpgme

Requires(preun): gpgme

%install
rm -rf $RPM_BUILD_ROOT
export REPO_DIRECTORY="$RPM_BUILD_ROOT/etc/yum.repos.d"
install -d -m 755 $REPO_DIRECTORY
install -m 644 %{SOURCE2} $REPO_DIRECTORY
install -m 644 %{SOURCE3} $REPO_DIRECTORY
install -m 644 %{SOURCE4} $REPO_DIRECTORY
install -m 644 %{SOURCE5} $REPO_DIRECTORY
install -m 644 %{SOURCE6} $REPO_DIRECTORY
install -m 644 %{SOURCE7} $REPO_DIRECTORY
install -m 644 %{SOURCE8} $REPO_DIRECTORY
install -m 644 %{SOURCE9} $REPO_DIRECTORY
install -m 644 %{SOURCE10} $REPO_DIRECTORY

export RPM_GPG_DIRECTORY="$RPM_BUILD_ROOT/etc/pki/rpm-gpg"

install -d -m 755 $RPM_GPG_DIRECTORY
install -m 644 %{SOURCE0} $RPM_GPG_DIRECTORY
install -m 644 %{SOURCE1} $RPM_GPG_DIRECTORY

%clean
rm -rf $RPM_BUILD_ROOT

%posttrans shared
gpg --import %{_sysconfdir}/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY
gpg --import %{_sysconfdir}/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY

%preun shared
# Remove the MICROSOFT-METADATA-GPG-KEY
gpg --batch --yes --delete-keys BC528686B50D79E339D3721CEB3E94ADBE1229CF
# Remove the MICROSOFT-RPM-GPG-KEY
gpg --batch --yes --delete-keys 2BC94FFF7015A5F28F1537AD0CD9FED33135CE90

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/mariner-official-base.repo
%config(noreplace) /etc/yum.repos.d/mariner-official-update.repo

%files preview
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/mariner-preview.repo

%files ui
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/mariner-ui.repo

%files ui-preview
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/mariner-ui-preview.repo

%files extras
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/mariner-extras.repo

%files extras-preview
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/mariner-extras-preview.repo

%files microsoft
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/mariner-microsoft.repo

%files microsoft-preview
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/mariner-microsoft-preview.repo

%files shared
%dir %{_sysconfdir}/yum.repos.d
%{_sysconfdir}/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY
%{_sysconfdir}/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY

%changelog
*   Tue Dec 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-16
-   Creating a separate "mariner-repos-shared" subpackage to make repo configurations
    independent of each other.
-   Removing dependency on RPM.

*   Thu Jul 14 2022 Andrew Phelps <anphel@microsoft.com> - 1.0-15
-   Add SRPMS repos for base, update, and coreui (all disabled by default)

*   Tue Jul 13 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-14
-   Add microsoft and microsoft-preview repo configuration packages.  
-   These repos offer Mariner packages produced by partner teams within Microsoft on 
-   behalf of the Mariner team but are released on an independent cadence from Mariner.

*   Fri Feb 19 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.0-13
-   Add extras repo.
-   Add extras-preview repo.

*   Fri Jan 22 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-12
-   Adding a set of repos with the UI components.

*   Thu Oct 01 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.0-11
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
