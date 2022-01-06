Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        7.2.1
Release:        1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        MIT
Url:            https://microsoft.com/powershell
Group:          shells
Source0:        https://github.com/PowerShell/PowerShell/releases/download/v%{version}/%{name}-%{version}-linux-x64.tar.gz
ExclusiveArch:  x86_64

Requires:       icu
Requires:       libunwind
Requires:       krb5
Requires:       lttng-ust
Requires:       openssl
Requires:       zlib
Requires:       glibc
Requires:       libgcc
Requires:       libstdc++

%description
PowerShell is an automation and configuration management platform.
It consists of a cross-platform command-line shell and associated scripting language.

# Avoid generating dependencies for openssl 1.0
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}

%prep

%build

%install
mkdir -p %{buildroot}/opt/microsoft/powershell/7
tar xf %{SOURCE0} --no-same-owner -C %{buildroot}/opt/microsoft/powershell/7
chmod +x %{buildroot}/opt/microsoft/powershell/7/pwsh
mkdir -p %{buildroot}%{_bindir}
ln -s /opt/microsoft/powershell/7/pwsh %{buildroot}%{_bindir}/pwsh

%files
%defattr(-,root,root,0755)
/opt/microsoft/powershell/7/*
%{_bindir}/pwsh
%license /opt/microsoft/powershell/7/LICENSE.txt

%changelog
*   Mon Dec 27 2021 Henry Beberman <henry.beberman@microsoft.com> 7.2.1-1
-   Update version to 7.2.1.
*   Sat Oct 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.0.2-2
-   Adjusting the build after recent RPM version update.
    Going to extract source in the %%install section now.
*   Thu Jun 18 2020 Andrew Phelps <anphel@microsoft.com> 7.0.2-1
-   Update version to 7.0.2. Remove automatic dependencies.
*   Wed May 13 2020 Nick Samson <nisamson@microsoft.com> 7.0.0-8
-   Added %%license line automatically
*   Tue May 12 2020 Andrew Phelps <anphel@microsoft.com> 7.0.0-7
-   Use binary powershell archive.
*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 7.0.0-6
-   Renaming dotnet-runtime to dotnet-runtime-3.1
*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 7.0.0-5
-   Renaming dotnet-sdk to dotnet-sdk-3.1
*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 7.0.0-4
-   Replace BuildArch with ExclusiveArch
*   Fri Apr 24 2020 Andrew Phelps <anphel@microsoft.com> 7.0.0-3
-   Add real link for Source0.
*   Tue Apr 14 2020 Andrew Phelps <anphel@microsoft.com> 7.0.0-2
-   Support offline build for CDPX.
*   Mon Mar 30 2020 Andrew Phelps <anphel@microsoft.com> 7.0.0-1
-   Update to powershell 7.0.0. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 6.1.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Feb 13 2019 Ajay Kaher <akaher@vmware.com> 6.1.1-2
-   Fix version mismatch issue.
*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 6.1.1-1
-   upgrade version to 6.1.1
*   Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 6.0.1-2
-   upgrade version of dotnet-runtime
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0.1-1
-   Initial build for photon
