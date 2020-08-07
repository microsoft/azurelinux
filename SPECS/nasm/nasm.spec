Summary:	Netwide Assembler.
Name:		nasm
Version:	2.13.03
Release:        5%{?dist}
License:	BSD
URL:		http://www.nasm.us
Group:		System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
ExclusiveArch:  x86_64
Source0:	http://www.nasm.us/pub/nasm/releasebuilds/%{version}/%{name}-%{version}.tar.gz
%define sha1 nasm=fa15c35b6003518d8165ab507f31af5d3938e91f
%description
NASM (Netwide Assembler) is an 80x86 assembler designed for portability and modularity. It includes a disassembler as well.
%prep
%setup -q
%build
%configure
make %{?_smp_mflags} CFLAGS="%{build_cflags}"
%install
make INSTALLROOT=%{buildroot} install
%check
make %{?_smp_mflags} -k test
%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_datadir}/*
%changelog
* Sat May 09 00:21:14 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.13.03-5
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
