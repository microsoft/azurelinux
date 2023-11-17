%global debug_package %{nil}

%define our_gopath %{_topdir}/.gopath
%define blobfuse2_version 2.1.2
%define blobfuse2_health_monitor bfusemon

Summary:        FUSE adapter - Azure Storage
Name:           blobfuse2
Version:        %{blobfuse2_version}
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/Azure/azure-storage-fuse/
# Below is the Github URL where blobfuse2 is accessible. This needs to be defined until blobfuse2 GAs since the version
# string in spec files does not allow - 
Source0:        https://github.com/Azure/azure-storage-fuse/archive/%{name}-%{blobfuse2_version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/Azure/azure-storage-fuse/archive/%{name}-%{version}.tar.gz -O %{name}-%{version}.tar.gz
#   2. tar -xf %{name}-%{version}.tar.gz
#   3. cd azure-storage-fuse-%{name}-%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %{name}-%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor.tar.gz
BuildRequires:  cmake
BuildRequires:  fuse3-devel
BuildRequires:  gcc
BuildRequires:  golang >= 1.16
Requires:       fuse3

%description
Blobfuse2 provides a virtual filesystem backed by the Azure Storage.
It uses the libfuse open source library (fuse3) to communicate with the
Linux FUSE kernel module, and implements the filesystem operations using
the Azure Storage REST APIs.

%prep
%setup -q -n azure-storage-fuse-%{name}-%{blobfuse2_version}

%build
tar --no-same-owner -xf %{SOURCE1}
export GOPATH=%{our_gopath}
go build -buildmode=pie -mod=vendor -o %{name}
go build -buildmode=pie -mod=vendor -o %{blobfuse2_health_monitor} ./tools/health-monitor/

%install
install -D -m 0755 ./blobfuse2 %{buildroot}%{_bindir}/blobfuse2
install -D -m 0755 ./%{blobfuse2_health_monitor} %{buildroot}%{_bindir}/%{blobfuse2_health_monitor}
install -D -m 0644 ./setup/baseConfig.yaml %{buildroot}%{_datadir}/blobfuse2/baseConfig.yaml
install -D -m 0644 ./sampleFileCacheConfig.yaml %{buildroot}%{_datadir}/blobfuse2/sampleFileCacheConfig.yaml
install -D -m 0644 ./sampleStreamingConfig.yaml %{buildroot}%{_datadir}/blobfuse2/sampleStreamingConfig.yaml
install -D -m 0755 ./tools/postinstall.sh %{buildroot}%{_datadir}/blobfuse2/postinstall.sh
install -D -m 0644 ./setup/11-blobfuse2.conf %{buildroot}%{_sysconfdir}/rsyslog.d/11-blobfuse2.conf
install -D -m 0644 ./setup/blobfuse2-logrotate %{buildroot}%{_sysconfdir}/logrotate.d/blobfuse2

%files
%defattr(-,root,root,-)
%license LICENSE
%doc NOTICE README.md
%{_bindir}/blobfuse2
%{_bindir}/%{blobfuse2_health_monitor}
%{_datadir}/blobfuse2/baseConfig.yaml
%{_datadir}/blobfuse2/sampleFileCacheConfig.yaml
%{_datadir}/blobfuse2/sampleStreamingConfig.yaml
%{_datadir}/blobfuse2/postinstall.sh
%{_sysconfdir}/rsyslog.d/11-blobfuse2.conf
%{_sysconfdir}/logrotate.d/blobfuse2

%changelog
* Fri Nov 17 2023 Anubhuti Shruti <ashruti@microsoft.com> - 2.1.2-1
- Bump version to 2.1.2

* Thu Nov 02 2023 Sourav Gupta <souravgupta@microsoft.com> - 2.1.1-1
- Bump version to 2.1.1

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.1.0-3
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 2.1.0-2
- Bump release to rebuild with updated version of Go.

* Mon Sep 04 2023 Anubhuti Shruti <ashruti@microsoft.com> - 2.1.0-1
- Bump version to 2.1.0

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.5-2
- Bump release to rebuild with go 1.19.12

* Wed Aug 02 2023 Sourav Gupta <souravgupta@microsoft.com> - 2.0.5-1
- Bump version to 2.0.5

* Mon Jul 17 2023 Sourav Gupta <souravgupta@microsoft.com> - 2.0.4-1
- Bump version to 2.0.4

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.2-6
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.2-5
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.2-4
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.2-3
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.2-2
- Bump release to rebuild with go 1.19.6

* Mon Feb 27 2023 Gauri Prasad <gapra@microsoft.com> - 2.0.2-1
- Bump version to 2.0.2

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-4
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-3
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.0.1-2
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Fri Dec 02 2022 Gauri Prasad <gapra@microsoft.com> - 2.0.1-1
- Bump version to 2.0.1

* Wed Nov 30 2022 Gauri Prasad <gapra@microsoft.com> - 2.0.0-1
- Bump version to 2.0.0

* Fri Nov 04 2022 Gauri Prasad <gapra@microsoft.com> - 2.0.0.preview.4-1
- Bump version to 2.0.0-preview.4

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.0.0.preview.3-2
- Bump release to rebuild with go 1.18.8

* Mon Oct 03 2022 Gauri Prasad <gapra@microsoft.com> - 2.0.0.preview.3-1
- Add blobfuse2 spec
- License verified
- Original version for CBL-Mariner
