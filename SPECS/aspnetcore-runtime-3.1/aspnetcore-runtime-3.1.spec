%define         debug_package %{nil}
Summary:        Microsoft aspnetcore runtime
Name:           aspnetcore-runtime-3.1
Version:        3.1.5
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/dotnet/aspnetcore
Source0:        https://download.visualstudio.microsoft.com/download/pr/6827d794-a218-4352-b3b3-a19ec773c975/e3e53bc2f20df220a29c6e09f74d8a00/aspnetcore-runtime-3.1.5-linux-x64.tar.gz
Requires:       dotnet-runtime-3.1
ExclusiveArch:  x86_64

%description
ASP.NET Core is an open-source and cross-platform framework for building
modern cloud based internet connected applications, such as web apps,
IoT apps and mobile backends

%prep
%setup -qc -T -a 0 dotnet-runtime-%{version}

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet/shared
cp -r shared/Microsoft.AspNetCore.App %{buildroot}%{_libdir}/dotnet/shared

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.txt ThirdPartyNotices.txt
%defattr(-,root,root,0755)
%{_libdir}/*

%changelog
* Thu Nov 12 2020 Henry Beberman <henry.beberman@microsoft.com> - 3.1.5-2
- Adapt dotnet-runtime spec to new aspnetcore-runtime spec.

*   Fri Jun 19 2020 Andrew Phelps <anphel@microsoft.com> 3.1.5-1
-   Update version to 3.1.5. Fix runtime requirements.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.1.3-4
-   Added %%license line automatically

*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 3.1.3-3
-   Renaming dotnet-runtime to dotnet-runtime-3.1

*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 3.1.3-2
-   Replace BuildArch with ExclusiveArch

*   Mon Mar 30 2020 Andrew Phelps <anphel@microsoft.com> 3.1.3-1
-   Update to dotnet 3.1.3. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.2.0-2
-   Initial import from Photon (license: dual Apache2/GPL2).

*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.2.0-1
-   upgraded to version 2.2.0

*   Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 2.1.4-1
-   upgraded to version 2.1.4
-   add aarch64 support

*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.5-1
-   Initial build for photon
