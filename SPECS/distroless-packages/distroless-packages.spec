Name:           distroless-packages
Summary:        Metapackage with core sets of packages for distroless containers
Version:        0.1
Release:        2%{?dist}
License:        MIT
Group:          System Environment/Base
URL:            http://aka.ms/cbl-mariner
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
Metapackage holding sets of core packages for different applications.

%package base
Summary: Metapackage defining the basic set of packages (no kernel) used to create a "distroless" container.

Requires: filesystem
Requires: tzdata
Requires: iana-etc
Requires: ca-certificates-static
Requires: mariner-release
Requires: openssl
Requires: openssl-libs
Requires: glibc-iconv

%description base
%{summary}

%package debug
Summary:  Debug packages for distroless
Requires: busybox
Requires: %{name}-base = %{version}-%{release}

%description debug
%{summary}

%prep

%build

%files base

%files debug

%changelog
* Thu Oct 15 2020 Mateusz Malisz <mamalisz@microsoft.com> - 0.1-2
- Extend the set of requirements for the base image
- Add debug package with busybox

* Tue Sep 01 2020 Jon Slobodzian <joslobo@microsoft.com> - 0.1-1
- Initial Mariner Version
