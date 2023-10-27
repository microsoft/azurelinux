Summary:        Netwide Assembler.
Name:           nasm
Version:        2.16.01
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.nasm.us
Source0:        http://www.nasm.us/pub/nasm/releasebuilds/%{version}/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

%description
NASM (Netwide Assembler) is an 80x86 assembler designed for portability and modularity. It includes a disassembler as well.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} CFLAGS="%{build_cflags}"

%install
%make_install

%check
make %{?_smp_mflags} -k test

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_datadir}/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.16.01-1
- Auto-upgrade to 2.16.01 - Azure Linux 3.0 - package upgrades

* Tue May 23 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.16-1
- Auto-upgrade to 2.16 - patch CVE-2022-44370

* Thu Jan 27 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 2.15.05-1
- Upgrading to 2.15.05.
- License verified.
- Removed sha1 definition.
- Switched to using make_install macro

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.13.03-5
- Added %%license line automatically

*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 2.13.03-4
-   Replace BuildArch with ExclusiveArch

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.13.03-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Thu Feb 28 2019 Keerthana K <keerthanak@vmware.com> 2.13.03-2
-   Adding BuildArch.

*   Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.13.03-1
-   Upgrade version to 2.13.03

*   Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 2.12.02-1
-   Initial version
