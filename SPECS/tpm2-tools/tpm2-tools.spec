Summary:        The source repository for the TPM (Trusted Platform Module) 2 tools
Name:           tpm2-tools
Version:        5.3
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/tpm2-software/tpm2-tools

Source0: https://github.com/tpm2-software/tpm2-tools/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=224a5ea3448a877362abb35ac06b115c559c09b44b30d74c8326211be66d24e0e130c285b1e285be1842e7203ab488629b0f4e451cbd782c83ed72023d146675

BuildRequires: openssl-devel
BuildRequires: curl-devel
BuildRequires: tpm2-tss-devel
%if 0%{?with_check}
# BuildRequires:  ibmtpm
# BuildRequires:  systemd
%endif

Requires: openssl
Requires: curl
Requires: tpm2-tss

%description
The source repository for the TPM (Trusted Platform Module) 2 tools

%prep
%autosetup -p1

%build
sed -i "/compatibility/a extern int BN_bn2binpad(const BIGNUM *a, unsigned char *to, int tolen);" lib/tpm2_openssl.c
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
# if [ ! -f /dev/tpm0 ];then
#    systemctl start ibmtpm_server.service
#    export TPM2TOOLS_TCTI=mssim:host=localhost,port=2321
#    tpm2_startup -c
#    tpm2_pcrlist
# fi
# make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1
%{_datadir}/bash-completion/*

%changelog
* Tue Jan 18 2022 Daniel McIlvaney <damcilva@microsoft.com> - 4.3.2-1
- Update to 4.3.2.
- Verified license

* Tue Jun 22 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> 4.2-2
- CVE-2021-3565 fix

* Tue Aug 25 2020 Daniel McIlvaney <damcilva@microsoft.com> 4.2-1
- Update to 4.2.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.1.4-2
- Added %%license line automatically

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> 3.1.4-1
- Update to version 3.1.4.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.1.3-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 3.1.3-1
- Initial build. First version
