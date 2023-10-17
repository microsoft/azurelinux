%global _default_patch_fuzz 2

Summary:        A highly-available key value store for shared configuration
Name:           etcd
Version:        3.5.9
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/etcd-io/etcd/
Source0:        https://github.com/etcd-io/etcd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        etcd.service
# Below is a manually created tarball, no download link.
# We're using vendored Go modules from this tarball, since network is disabled during build time.
#
# How to re-build this file:
#   1. either download etcd source tarball or git clone etcd repo from github and checkout relevant tag
#   2. execute 'go mod vendor' in 'server', 'etcdctl' and 'etcdutl' folders 
#      and create tarball containting 'vendor' folder for each
#      (naming rule for tarball is 'vendor-[component].tar.gz', e.g.: 'vendor-server.tar.gz')
#   3. create 'vendor' tarballs for dump tools
#       a. cd 'tools/etcd-dump-db' folder, create 'go.mod' file ('go mod init go.etcd.io/etcd/tools/etcd-dump-db/v3')
#       b. populate 'go.mod' file ('go mod tidy')
#       c. add replace rules in 'go.mod' making sure that each etcd dependency is taken locally, 
#          e.g. add the following (and remove them from require section):
#          replace (
#               go.etcd.io/etcd/api/v3 v3.5.1 => ../../api
#               go.etcd.io/etcd/server/v3 v3.5.1 => ../../server
#          )
#       d. create vendor folder ('go mod vendor')
#       e. create tarball containing 'vendor' folder and 'go.mod' and 'go.sum' files
#          (same naming rules than described above)
#       f. repeat above operations for 'etcd-dump-logs' folder
#   4. create 'etcd-%{version}-vendor.tar.gz' tarball containing all tarballs created above
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - You can use the following tar command to create the tarballs
#         tar --sort=name --mtime="2021-11-10 00:00Z" \
#             --owner=0 --group=0 --numeric-owner \
#             --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#             -cJf [tarball name] [folder to tar]
Source2:        %{name}-%{version}-vendor.tar.gz
BuildRequires:  golang >= 1.16

%description
A highly-available key value store for shared configuration and service discovery.

%package tools
Summary:        Diagnostic tools for etcd
Group:          System Environment/Security
Requires:       %{name} = %{version}-%{release}

%description tools
A highly-available key value store for shared configuration and service discovery.
The etcd-tools package contains the etcd-dump-db and etcd-dump-logs diagnostic
tools.

%prep
%autosetup -p1
tar --no-same-owner -xf %{SOURCE2}

%build
%define ETCD_OUT_DIR %{_builddir}/%{name}-%{version}/bin
mkdir -p %{ETCD_OUT_DIR}

# build etcd
for component in server etcdctl etcdutl; do
    pushd $component
    tar --no-same-owner -xf %{_builddir}/%{name}-%{version}/vendor-$component.tar.gz
    go build \
        -o %{ETCD_OUT_DIR} \
        -ldflags=-X=go.etcd.io/etcd/api/v3/version.GitSHA=v%{version}
    popd
done

# build tools
%define ETCD_TOOLS_OUT_DIR %{_builddir}/%{name}-%{version}/bin/tools
mkdir -p %{ETCD_TOOLS_OUT_DIR}

for component in etcd-dump-db etcd-dump-logs; do
    pushd tools/$component
    tar --no-same-owner -xf %{_builddir}/%{name}-%{version}/vendor-$component.tar.gz
    go build \
        -o %{ETCD_TOOLS_OUT_DIR}
    popd
done

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}/%{_docdir}/%{name}-%{version}
install -vdm755 %{buildroot}/lib/systemd/system
install -vdm 0755 %{buildroot}%{_sysconfdir}/etcd
install -vpm 0755 -T etcd.conf.yml.sample %{buildroot}%{_sysconfdir}/etcd/etcd-default-conf.yml

chown -R root:root %{buildroot}%{_bindir}
chown -R root:root %{buildroot}/%{_docdir}/%{name}-%{version}

# note that 'server' should be renamed 'etcd'
mv %{_builddir}/%{name}-%{version}/bin/server %{buildroot}%{_bindir}/etcd
mv %{_builddir}/%{name}-%{version}/bin/etcdctl %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-%{version}/bin/etcdutl %{buildroot}%{_bindir}/

mv %{_builddir}/%{name}-%{version}/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/
mv %{_builddir}/%{name}-%{version}/etcdctl/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/README-etcdctl.md
mv %{_builddir}/%{name}-%{version}/etcdctl/READMEv2.md %{buildroot}/%{_docdir}/%{name}-%{version}/READMEv2-etcdctl.md
mv %{_builddir}/%{name}-%{version}/etcdutl/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/README-etcdutl.md

# tools
install -vdm755 %{buildroot}/%{_docdir}/%{name}-%{version}-tools
chown -R root:root %{buildroot}/%{_docdir}/%{name}-%{version}-tools

mv %{_builddir}/%{name}-%{version}/bin/tools/etcd-dump-logs %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-%{version}/bin/tools/etcd-dump-db %{buildroot}%{_bindir}/

mv %{_builddir}/%{name}-%{version}/tools/etcd-dump-db/README.md %{buildroot}/%{_docdir}/%{name}-%{version}-tools/README-etcd-dump-db.md
mv %{_builddir}/%{name}-%{version}/tools/etcd-dump-logs/README.md %{buildroot}/%{_docdir}/%{name}-%{version}-tools/README-etcd-dump-logs.md

install -vdm755 %{buildroot}/lib/systemd/system-preset
echo "disable etcd.service" > %{buildroot}/lib/systemd/system-preset/50-etcd.preset

cp %{SOURCE1} %{buildroot}/lib/systemd/system
install -vdm755 %{buildroot}%{_sharedstatedir}/etcd

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_bindir}/etcd
%{_bindir}/etcdctl
%{_bindir}/etcdutl
/%{_docdir}/%{name}-%{version}/*
/lib/systemd/system/etcd.service
/lib/systemd/system-preset/50-etcd.preset
%dir %{_sharedstatedir}/etcd
%config(noreplace) %{_sysconfdir}/etcd/etcd-default-conf.yml

%files tools
%license LICENSE
%{_bindir}/etcd-dump-*
/%{_docdir}/%{name}-%{version}-tools/*

%changelog
* Tue Oct 10 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 3.5.9-1
- Upgrade to 3.5.9 to match version required by kubernetes

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 3.5.6-11
- Bump release to rebuild with updated version of Go.

* Wed Aug 23 2023 Rachel Menge <rachelmenge@microsoft.com> - 3.5.6-10
- Patch CVE-2023-32082
- Update patch fuzz to 2 for backporting patch

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.6-9
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.6-8
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.6-7
- Bump release to rebuild with go 1.19.10

* Wed Apr 19 2023 Bala <balakumaran.kannan@microsoft.com> - 3.5.6-6
- Patch CVE-2021-28235
- Update patch fuzz to 1 for backporting patch

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.6-5
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.6-4
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.6-3
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.6-2
- Bump release to rebuild with go 1.19.5

* Thu Jan 19 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.6-1
- Auto-upgrade to 3.5.6 - version required by Kubernetes

* Thu Jan 19 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.5-1
- Auto-upgrade to 3.5.5 - version required by Kubernetes

* Thu Jan 19 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.4-1
- Auto-upgrade to 3.5.4 - version required by Kubernetes

* Thu Jan 19 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.3-1
- Auto-upgrade to 3.5.3 - version required by Kubernetes

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5.1-6
- Bump release to rebuild with go 1.19.4

*   Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.5.1-5
-   Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717.

*   Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.5.1-4
-   Bump release to rebuild with go 1.18.8

*   Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.5.1-3
-   Bump release to rebuild against Go 1.18.5

*   Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 3.5.1-2
-   Bump release to rebuild with golang 1.18.3

*   Thu Apr 21 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 3.5.1-1
-   Upgrade to 3.5.1

*   Tue Feb 08 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 3.5.0-3
-   Remove clean section

*   Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 3.5.0-2
-   Increment release for force republishing using golang 1.16.12

*   Tue Dec 28 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 3.5.0-1
-   Upgrade to version 3.5.0

*   Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 3.4.13-6
-   Increment release for force republishing using golang 1.16.9

*   Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.4.13-5
-   Increment release to force republishing using golang 1.16.7.

*   Thu Aug 05 2021 Tom Fay <tomfay@microsoft.com> - 3.4.13-4
-   Add etcd-tools package.

*   Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 3.4.13-3
-   Increment release to force republishing using golang 1.15.13.

*   Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.4.13-2
-   Increment release to force republishing using golang 1.15.11.

*   Mon Jan 25 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.4.13-1
-   Update to version 3.4.13.

*   Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 3.3.25-2
-   Increment release to force republishing using golang 1.15.

*   Thu Sep 03 2020 Joe Schmitt <joschmit@microsoft.com> 3.3.25-1
-   Update to version 3.3.25 which fixes CVE-2020-15106, CVE-2020-15112, CVE-2020-15114, and CVE-2020-15115.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.3.11-2
-   Added %%license line automatically

*   Thu May 07 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.3.11-1
-   Upgrade to version 3.3.11, which fixes CVE-2018-16886.
-   Update summary.

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 3.3.9-4
-   Renaming go to golang

*   Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.3.9-3
-   Fixed "Source0" tag.
-   License verified and "License" tag updated.
-   Removed "%%define sha1".

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.3.9-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Fri Sep 21 2018 Sujay G <gsujay@vmware.com> 3.3.9-1
-   Bump etcd version to 3.3.9

*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1.5-4
-   Remove shadow requires

*   Sun Aug 27 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.1.5-3
-   File based configuration for etcd service.

*   Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.5-2
-   Provide preset file to disable service by default

*   Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 3.1.5-1
-   Upgraded to version 3.1.5, build from sources

*   Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 3.0.9-1
-   Upgraded to version 3.0.9

*   Fri Jun 24 2016 Xiaolin Li <xiaolinl@vmware.com> 2.3.7-1
-   Upgraded to version 2.3.7

*   Wed May 25 2016 Nick Shi <nshi@vmware.com> 2.2.5-3
-   Changing etcd service type from simple to notify

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.5-2
-   GA - Bump release of all rpms

*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.5-1
-   Upgraded to version 2.2.5

*   Tue Jul 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.1-2
-   Adding etcd service file

*   Tue Jul 21 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.1.1-1
-   Update to version etcd v2.1.1

*   Tue Mar 10 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.4-1
-   Initial build.  First version
