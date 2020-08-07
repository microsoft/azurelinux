Summary:	The source repository for the TPM (Trusted Platform Module) 2 tools
Name:		tpm2-tools
Version:	3.1.4
Release:        2%{?dist}
License:	BSD 2-Clause
URL:		https://github.com/tpm2-software/tpm2-tools
Group:		System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	https://github.com/tpm2-software/tpm2-tools/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	openssl-devel curl-devel tpm2-tss-devel
Requires:	openssl curl tpm2-tss
%description
The source repository for the TPM (Trusted Platform Module) 2 tools

%prep
%setup -q
%build
%configure \
    --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_mandir}/man1

%changelog
* Sat May 09 00:21:43 PST 2020 Nick Samson <nisamson@microsoft.com> - 3.1.4-2
- Added %%license line automatically

*   Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> 3.1.4-1
-   Update to version 3.1.4.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.1.3-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 3.1.3-1
-   Initial build. First version
