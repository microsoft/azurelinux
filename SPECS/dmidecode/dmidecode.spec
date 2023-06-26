Summary:	Tool to analyze BIOS DMI data
Name:		dmidecode
Version:	3.5
Release:    1%{?dist}
License:	GPLv2+
URL:		http://www.nongnu.org/dmidecode/
Group:		System Environment/Base
Source0:	https://download.savannah.gnu.org/releases/dmidecode/%{name}-%{version}.tar.xz
Vendor:         Microsoft Corporation
Distribution:   Mariner
%description
Dmidecode reports information about your system's hardware as described in your system BIOS according to the SMBIOS/DMI standard. This information typically includes system manufacturer, model name, serial number, BIOS version, asset tag as well as a lot of other details of varying level of interest and reliability depending on the manufacturer. This will often include usage status for the CPU sockets, expansion slots (e.g. AGP, PCI, ISA) and memory module slots, and the list of I/O ports (e.g. serial, parallel, USB).

%prep
%setup -q
%build
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} prefix=%{_prefix} install
%files
%defattr(-,root,root)
%license LICENSE
%{_sbindir}/*
%{_docdir}/%{name}/*
%{_mandir}/man8/*

%changelog
* Tue May 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5-1
- Auto-upgrade to 3.5 - to fix CVE-2023-30630

* Fri Jan 21 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 3.3-1
- Upgrade to 3.3
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.2-2
- Added %%license line automatically

*   Thu Mar 19 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.2-1
-   Update version to 3.2. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*	Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 3.1-1
-	Upgraded to version 3.1
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-2
-	GA - Bump release of all rpms
*	Mon Nov 02 2015 Divya Thaluru <dthaluru@vmware.com> 3.0-1
-	Initial build.	First version
