Summary:        Metapackage with core sets of packages for distroless containers.
Name:           distroless-packages
Version:        3.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://aka.ms/cbl-mariner

%description
Metapackage holding sets of core packages for different applications.

%package minimal
Summary:        The smallest useful package list.
Requires:       filesystem
Requires:       azurelinux-release
Requires:       prebuilt-ca-certificates
Requires:       tzdata

%description minimal
%{summary}
Created using a minimal set of packages.

%package base
Summary:        Metapackage defining the basic set of packages (no kernel) used to create a "distroless" container.
Requires:       %{name}-minimal = %{version}-%{release}
Requires:       filesystem
Requires:       glibc-iconv
Requires:       iana-etc
Requires:       azurelinux-release
Requires:       openssl
Requires:       openssl-libs
Requires:       SymCrypt
Requires:       SymCrypt-openssl
Requires:       tzdata

%description base
%{summary}

%package debug
Summary:        Debug packages for distroless
Requires:       %{name}-minimal = %{version}-%{release}
Requires:       busybox

%description debug
%{summary} This version features busybox for easier debugging.

%prep

%build

%files minimal

%files base

%files debug

%changelog
* Wed Feb 07 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.0-2
- Update the runtime dependency from mariner-release to azurelinux-release

* Mon Jan 22 2024 Betty Lakes <bettylakes@microsoft.com> - 3.0-1
- Version upgraded to 3.0

* Wed Nov 16 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.1-3
- Replace prebuilt-ca-certificates-base with prebuilt-ca-certificates in minimal
- Add tzdata to minimal
- License verified

* Thu Oct 15 2020 Mateusz Malisz <mamalisz@microsoft.com> - 0.1-2
- Extend the set of requirements for the base image
- Add debug package with busybox

* Tue Sep 01 2020 Jon Slobodzian <joslobo@microsoft.com> - 0.1-1
- Original version for CBL-Mariner
