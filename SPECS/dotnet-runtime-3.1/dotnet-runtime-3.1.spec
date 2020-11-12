Summary:        Microsoft .NET Core Runtime
Name:           dotnet-runtime-3.1
Version:        3.1.5
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/dotnet/core
Source0:        https://download.visualstudio.microsoft.com/download/pr/d00eaeea-6d7b-4e73-9d96-c0234ed3b665/0d25d9d1aeaebdeef01d15370d5cd22b/dotnet-runtime-3.1.5-linux-x64.tar.gz
Source1:        https://download.visualstudio.microsoft.com/download/pr/6827d794-a218-4352-b3b3-a19ec773c975/e3e53bc2f20df220a29c6e09f74d8a00/aspnetcore-runtime-3.1.5-linux-x64.tar.gz
Requires:       glibc
Requires:       icu
Requires:       krb5
Requires:       libgcc
Requires:       libstdc++
Requires:       libunwind
Requires:       lttng-ust
Requires:       openssl
Requires:       zlib
ExclusiveArch:  x86_64

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%package -n aspnetcore-runtime-3.1
Summary:        aspnetcore runtime for dotnet
Group:          System Environment/Base
Requires:       %{name}

%description -n aspnetcore-runtime-3.1
aspnetcore runtime for dotnet

%prep
%setup -qc -T -a 0 -a 1 dotnet-runtime-%{version}

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet
mkdir -p %{buildroot}%{_docdir}/dotnet-runtime-%{version}
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/dotnet-runtime-%{version}
rm LICENSE.txt ThirdPartyNotices.txt
cp -r * %{buildroot}%{_libdir}/dotnet
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libdir}/dotnet/dotnet %{buildroot}%{_bindir}/dotnet

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig

# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

# Post-uninstall
%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%files
%license %{_docdir}/dotnet-runtime-%{version}/LICENSE.txt
%defattr(-,root,root,0755)
%exclude %{_libdir}/debug
%{_docdir}/*
%{_bindir}/dotnet
%{_libdir}/*
%exclude %{_libdir}/dotnet/shared/Microsoft.AspNetCore.App

%files -n aspnetcore-runtime-3.1
%defattr(-,root,root,0755)
%{_libdir}/dotnet/shared/Microsoft.AspNetCore.App

%changelog
* Thu Nov 12 2020 Henry Beberman <henry.beberman@microsoft.com> - 3.1.5-2
- Add aspnetcore-runtime subpackage.

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
