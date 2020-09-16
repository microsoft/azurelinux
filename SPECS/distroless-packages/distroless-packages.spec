Name:           distroless-packages
Summary:        Metapackage with core sets of packages for distroless containers
Version:        0.1
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Base
URL:            http://aka.ms/cbl-mariner
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
Metapackage holding sets of core packages for different applications.

%package base
Summary:    Metapackage defining the basic set of packages (no kernel) used by images such as VHDs, VHDXs and ISOs.

Requires:   filesystem
Requires:   tzdata
Requires:   iana-etc
Requires:   ca-certificates-static
Requires:   mariner-release
Requires:   openssl
Requires:   openssl-libs
Requires:   glibc-iconv


%description base
%{summary}

%prep

%build

%files base


%changelog
*   Tue Sep 1 2020 Jon Slobodzian <joslobo@microsoft.com> 0.1-1
-   Initial Mariner Version
