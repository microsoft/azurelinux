Summary:        The source repository for the TPM (Trusted Platform Module) 2 tools
Name:           tpm2-tools
Version:        4.3.2
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/tpm2-software/tpm2-tools
Source0:        https://github.com/tpm2-software/tpm2-tools/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  tpm2-tss-devel >= 2.3.0
Requires:       /bin/awk
Requires:       curl
Requires:       openssl
Requires:       tpm2-tss >= 2.3.0

%description
The source repository for the TPM (Trusted Platform Module) 2 tools

%prep
%autosetup -p1

%build
%configure \
    --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%license doc/LICENSE
%{_bindir}/*
%{_mandir}/man1
%{_datarootdir}/bash-completion/completions/tpm2_*
%{_datarootdir}/bash-completion/completions/tss2_*

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
