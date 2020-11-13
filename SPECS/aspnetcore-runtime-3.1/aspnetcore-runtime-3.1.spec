%define         debug_package %{nil}
Summary:        Microsoft aspnetcore runtime
Name:           aspnetcore-runtime-3.1
Version:        3.1.5
Release:        1%{?dist}
License:        ASL 2.0
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
%{_libdir}/dotnet/shared/Microsoft.AspNetCore.App

%changelog
* Thu Nov 12 2020 Henry Beberman <henry.beberman@microsoft.com> - 3.1.5-1
- Add aspnetcore-runtime spec.
- License verified
- Original version for CBL-Mariner