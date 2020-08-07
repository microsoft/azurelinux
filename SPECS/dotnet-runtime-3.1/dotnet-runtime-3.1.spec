Summary:        Microsoft .NET Core Runtime
Name:           dotnet-runtime-3.1
Version:        3.1.5
Release:        1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools
ExclusiveArch:  x86_64
Source0:        https://download.visualstudio.microsoft.com/download/pr/d00eaeea-6d7b-4e73-9d96-c0234ed3b665/0d25d9d1aeaebdeef01d15370d5cd22b/dotnet-runtime-3.1.5-linux-x64.tar.gz

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
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%setup -qc dotnet-runtime-%{version}

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

%changelog
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
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.2.0-1
-   upgraded to version 2.2.0
*   Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 2.1.4-1
-   upgraded to version 2.1.4
-   add aarch64 support
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.5-1
-   Initial build for photon
