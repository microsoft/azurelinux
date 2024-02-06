Name:       tpm2-pytss
Version:    1.2.0
Release:    3%{?dist}
Summary:    Python bindings for tpm2-tss
License:    BSD
URL:        https://github.com/tpm2-software/tpm2-pytss
Group:      System Environment/Security
Vendor:     Microsoft Corporation
Distribution: Mariner

Source0: https://github.com/tpm2-software/tpm2-pytss/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildRequires: git
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-pkgconfig
BuildRequires: python3-pycparser
BuildRequires: python3-setuptools
BuildRequires: tpm2-tss-devel

# packaging, asn1crypto, cryptography, and setuptools_scm are required in
# Mariner build system, so these are additions to the photon spec
BuildRequires: python3-asn1crypto
BuildRequires: python3-cryptography
BuildRequires: python3-packaging
BuildRequires: python3-setuptools_scm

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-cffi
BuildRequires: python3-PyYAML
%endif

Requires: python3
Requires: tpm2-tss

%description
TPM2 TSS Python bindings for Enhanced System API (ESYS).
This package primarily exposes the TPM 2.0 Enhanced System API.

%prep
%autosetup -p1 -Sgit

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%pytest
%endif

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Mon Jan 22 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 1.2.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).
- Verified license
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.2.0-2
- Update release to compile with python 3.11
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-1
- First build. Needed for tpm2-pkcs11.
