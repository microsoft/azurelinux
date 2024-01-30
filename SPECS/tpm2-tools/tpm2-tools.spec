Summary:        The source repository for the TPM (Trusted Platform Module) 2 tools
Name:           tpm2-tools
Version:        5.5
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/tpm2-software/tpm2-tools

Source0: https://github.com/tpm2-software/tpm2-tools/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires: openssl-devel
BuildRequires: curl-devel
BuildRequires: tpm2-tss-devel
%if 0%{?with_check}
BuildRequires:  swtpm-tools
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
if [ ! -f /dev/tpm0 ];then
   find / -name "*swtpm*"
   mkdir /tmp/swtpm
   swtpm_setup --tpm-state /tmp/swtpm --tpm2
   swtpm socket --server swtpm socket --server type=unixio,path=/tmp/swtpm/socket --ctrl type=unixio,path=/tmp/swtpm/socket.ctrl --tpmstate dir=/tmp/swtpm --flags startup-clear --tpm2 --daemon
   tpm2_startup -c
   tpm2_pcrlist
fi
make %{?_smp_mflags} check
if [ ! -f /dev/tpm0 ];then
   # kill swtpm
fi
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1
%{_datadir}/bash-completion/*

%changelog
* Mon Jan 22 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 5.5-1
- Updated to 5.5

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
