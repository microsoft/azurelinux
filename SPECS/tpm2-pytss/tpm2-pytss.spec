Name:       tpm2-pytss
Version:    2.2.1
Release:    1%{?dist}
Summary:    Python bindings for tpm2-tss
License:    BSD
URL:        https://github.com/tpm2-software/tpm2-pytss
Group:      System Environment/Security
Vendor:     Microsoft Corporation
Distribution:   Azure Linux

Source0: https://github.com/tpm2-software/tpm2-pytss/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

# azl: The openssl package does not build some of the bits that
# tpm2-pytss expects.  This patch removes tests that fail due to
# their absence.
Patch0:  0001-remove-tests-for-unsupported-openssl.patch

BuildRequires: git
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-pkgconfig
BuildRequires: python3-pycparser
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
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
BuildRequires: swtpm-tools
%endif

Requires: python3
Requires: tpm2-tss

Provides: python3-%{name} = %{version}-%{release}

%description
TPM2 TSS Python bindings for Enhanced System API (ESYS).
This package primarily exposes the TPM 2.0 Enhanced System API.

%prep
%autosetup -p1 -Sgit

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_check}
%check
export PYTHONPATH=%{buildroot}%{python3_sitelib}
pip3 install iniconfig
if [ ! -f /dev/tpm0 ];then
   mkdir /tmp/swtpm
   swtpm_setup --tpm-state /tmp/swtpm --tpm2
   swtpm socket --server type=unixio,path=/tmp/swtpm/socket --ctrl type=unixio,path=/tmp/swtpm/socket.ctrl --tpmstate dir=/tmp/swtpm --flags startup-clear --tpm2 --daemon
   export TPM2TOOLS_TCTI=swtpm:path=/tmp/swtpm/socket
   %{buildroot}/%{_bindir}/tpm2_startup -c
   %{buildroot}/%{_bindir}/tpm2_pcrread
fi
%pytest
%endif

%files -n tpm2-pytss
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Mon Mar 18 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 2.2.1-1
- Update to handle new version of python-cryptography

* Mon Jan 22 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 1.2.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).
- Verified license.
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.2.0-2
- Update release to compile with python 3.11
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-1
- First build. Needed for tpm2-pkcs11.
