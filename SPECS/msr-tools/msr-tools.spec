%define LICENSE_PATH LICENSE.PTR

Summary:       Tools to read/write MSR (Model Specific Registers)
Name:          msr-tools
Version:       1.3
Release:       5%{?dist}
License:       GPLv2
URL:           https://01.org/msr-tools/downloads
Source0:       https://01.org/sites/default/files/downloads/msr-tools/%{name}-%{version}.zip 
Source1:       %{LICENSE_PATH}
Group:         Development/Tools
Vendor:        Microsoft Corporation
Distribution:  Mariner

BuildRequires: unzip

%description
MSR Tools project provides utilities to access the processor MSRs and CPU ID directly.
This project is composed of three different user space console applications.
rdmsr – read MSR from any CPU or all CPUs
wrmsr – write values to MSR on any CPU or all CPUs
cpuid – show identification and feature information of any CPU

%prep
%setup -q -n msr-tools-master
cp %{SOURCE1} ./

%build
make %{?_smp_mflags}

%install
install -D rdmsr %{buildroot}%{_sbindir}/rdmsr
install -D wrmsr %{buildroot}%{_sbindir}/wrmsr
install -D cpuid %{buildroot}%{_sbindir}/msr-cpuid

%files
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{_sbindir}/*

%changelog
*   Thu Jun 06 2020 Joe Schmitt <joschmit@microsoft.com> 1.3-5
-   Added %%license macro.
*   Thu Apr 09 2020 Nick Samson <nisamson@microsoft.com> 1.3-4
-   Updated source URL. License verified. Removed %%define sha line
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.3-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3-2
-   GA - Bump release of all rpms
*   Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
-   Initial build.  First version
