Summary:        Utilities for writing cds.
Name:           cdrkit
Version:        1.1.11
Release:        11%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Project's web page (http://cdrkit.org) is no longer online.
Source0:        https://src.fedoraproject.org/repo/pkgs/%{name}/%{name}-%{version}.tar.gz/efe08e2f3ca478486037b053acd512e9/%{name}-%{version}.tar.gz
Patch0:         cdrkit-1.1.9-efi-boot.patch
Patch1:         cdrkit-fix-format-security.patch

Requires:    bash
Requires:    libcap

BuildRequires:  cmake
BuildRequires:  libcap-devel
BuildRequires:  bzip2-devel

Provides: genisoimage

%description
The Cdrtools package contains CD recording utilities. These are useful for reading, creating or writing (burning) Compact Discs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
make %{?_smp_mflags}

%install
env PREFIX=%{buildroot}%{_prefix} make install
ln -s  genisoimage  %{buildroot}%{_prefix}/bin/mkisofs

%files
%license COPYING
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/man/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.1.11-11
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.11-10
-   Removing the explicit %%clean stage.

*   Mon May 17 2021 Muhammad Falak <mwani@microsoft.com> - 1.1.11-9
-   Add an explicit provides for `genisoimage`
*   Sun May 31 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.1.11-8
-   Add patch to fix format-security errors.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.11-7
-   Added %%license line automatically
*   Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.1.11-6
-   Fixed the 'Source0' tags.
-   Removed outdated 'URL' tag.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1.11-5
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.11-4
-   Remove BuildArch
*   Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.11-3
-   Support for efi boot (.patch)
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.11-2
-   GA - Bump release of all rpms
*   Sat Feb 14 2015 Sharath George <sharathg@vmware.com>
-   first packaging
