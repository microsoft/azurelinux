Summary:        CBL-Mariner repo files, gpg keys
Name:           mariner-repos
Version:        2.0
Release:        9%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Source0:        MICROSOFT-RPM-GPG-KEY
Source1:        MICROSOFT-METADATA-GPG-KEY
Source2:        mariner-debuginfo.repo
Source3:        mariner-debuginfo-preview.repo
Source4:        mariner-extended.repo
Source5:        mariner-extended-preview.repo
Source6:        mariner-extras.repo
Source7:        mariner-extras-preview.repo
Source8:        mariner-microsoft.repo
Source9:        mariner-microsoft-preview.repo
Source10:       mariner-official-base.repo
Source11:       mariner-official-preview.repo
Source12:       mariner-extended-debuginfo.repo
Source13:       mariner-extended-debuginfo-preview.repo
Source14:       mariner-cloud-native.repo
Source15:       mariner-cloud-native-preview.repo

Requires:       %{name}-shared = %{version}-%{release}

BuildArch:      noarch

%description
CBL-Mariner repo files and gpg keys

%package cloud-native
Summary:        CBL-Mariner cloud-native repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description cloud-native
%{summary}

%package cloud-native-preview
Summary:        CBL-Mariner cloud-native preview repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description cloud-native-preview
%{summary}

%package debug
Summary:        CBL-Mariner Debuginfo repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description debug
%{summary}

%package debug-preview
Summary:        CBL-Mariner Debuginfo preview repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description debug-preview
%{summary}

%package extended
Summary:        CBL-Mariner Extended repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description extended
%{summary}

%package extended-debug
Summary:        CBL-Mariner Extended Debuginfo repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description extended-debug
%{summary}

%package extended-preview
Summary:        CBL-Mariner Extended preview repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description extended-preview
%{summary}

%package extended-debug-preview
Summary:        CBL-Mariner Extended Debuginfo preview repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description extended-debug-preview
%{summary}

%package extras
Summary:        CBL-Mariner Extras repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description extras
%{summary}

%package extras-preview
Summary:        CBL-Mariner Extras preview repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description extras-preview
%{summary}

%package microsoft
Summary:        CBL-Mariner Microsoft repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description microsoft
%{summary}

%package microsoft-preview
Summary:        CBL-Mariner Microsoft preview repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description microsoft-preview
%{summary}

%package preview
Summary:        CBL-Mariner preview repo file.
Group:          System Environment/Base
Requires:       %{name}-shared = %{version}-%{release}

%description preview
%{summary}

%package shared
Summary:        Directories and files needed by all %{name} configurations.
Group:          System Environment/Base

Requires(post): gpgme

Requires(preun): gpgme

%description shared
%{summary}

%install
export REPO_DIRECTORY="%{buildroot}%{_sysconfdir}/yum.repos.d"
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
install -m 644 %{SOURCE11} $REPO_DIRECTORY
install -m 644 %{SOURCE12} $REPO_DIRECTORY
install -m 644 %{SOURCE13} $REPO_DIRECTORY
install -m 644 %{SOURCE14} $REPO_DIRECTORY
install -m 644 %{SOURCE15} $REPO_DIRECTORY

export RPM_GPG_DIRECTORY="%{buildroot}%{_sysconfdir}/pki/rpm-gpg"

install -d -m 755 $RPM_GPG_DIRECTORY
install -m 644 %{SOURCE0} $RPM_GPG_DIRECTORY
install -m 644 %{SOURCE1} $RPM_GPG_DIRECTORY

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
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-official-base.repo

%files cloud-native
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-cloud-native.repo

%files cloud-native-preview
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-cloud-native-preview.repo

%files debug
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-debuginfo.repo

%files debug-preview
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-debuginfo-preview.repo

%files extended
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-extended.repo

%files extended-debug
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-extended-debuginfo.repo

%files extended-preview
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-extended-preview.repo

%files extended-debug-preview
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-extended-debuginfo-preview.repo

%files extras
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-extras.repo

%files extras-preview
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-extras-preview.repo

%files microsoft
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-microsoft.repo

%files microsoft-preview
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-microsoft-preview.repo

%files preview
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/mariner-official-preview.repo

%files shared
%dir %{_sysconfdir}/yum.repos.d
%{_sysconfdir}/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY
%{_sysconfdir}/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY

%changelog
* Wed Nov 29 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0-9
- Add cloud native repos.

* Thu Jul 14 2022 Andrew Phelps <anphel@microsoft.com> - 2.0-8
- Add SRPM and Debuginfo repos to existing base, extended, and preview subpackages

* Tue Apr 19 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-7
- Add support for extended debuginfo repositories for Mariner 2.0

* Wed Apr 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.0-6
- Update required dependecies for mariner-repos-shared sub-package.

* Mon Feb 28 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-5
- Moving away from using 'debuginfo' in a custom package to avoid confusion.

* Mon Jan 10 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-4
- Creating a separate "mariner-repos-shared" subpackage to make repo configurations
  independent of each other.

* Thu Dec 16 2021 Jon Slobodzian <joslobo@microsoft.com> - 2.0-3
- Corrected Repo URLS for 2.0.

* Thu Dec 09 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-2
- Updating repo URLs for 2.0.
- License verified.

* Tue Jul 13 2021 Jon Slobodzian <joslobo@microsoft.com> - 2.0-1
- Add microsoft and microsoft-preview repo configuration packages.  
- These repos offer Mariner packages produced by partner teams within Microsoft on 
- behalf of the Mariner team but are released on an independent cadence from Mariner.
- Version update for 2.0.  Formatting changes.

* Fri Feb 19 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.0-13
- Add extras repo.
- Add extras-preview repo.

* Fri Jan 22 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-12
- Adding a set of repos with the UI components.

* Thu Oct 01 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.0-11
- Change %%post scriptlet to %%posttrans in order to ensure it runs after %%postun during an upgrade.

* Mon Sep 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.0-10
- Adding configuration to access the preview repository.
- Removing redundant 'Provides'.

* Tue Aug 11 2020 Saravanan Somasundaram <sarsoma@microsoft.com> - 1.0-9
- Enable GPG Check and Import

* Mon Aug 10 2020 Saravanan Somasundaram <sarsoma@microsoft.com> - 1.0-8
- Adding Metadata Key and Updating to Prod GPG Key.

* Fri Jul 31 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-7
- Fixing distro name.

* Fri Jul 17 2020 Andrew Phelps <anphel@microsoft.com> 1.0-6
- Set sslverify=1 in [mariner-official-base] and [mariner-official-update]

* Wed Nov 27 2019 Pawel Winogrodzki <pawelwi@microsoft.com> 1.0-5
- Removing outdated repository configuration

* Fri Nov 22 2019 Andrew Phelps <anphel@microsoft.com> 1.0-4
- Use $releasever and $basearch variables

* Tue Oct 29 2019 Andrew Phelps <anphel@microsoft.com> 1.0-3
- Separate repo configs for official-base and official-update

* Wed Oct 23 2019 Andrew Phelps <anphel@microsoft.com> 1.0-2
- Add mariner-official.repo

* Wed Sep 04 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0-1
- Original version for CBL-Mariner.
