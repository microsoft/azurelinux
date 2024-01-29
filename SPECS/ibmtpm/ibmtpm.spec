# ibmtpm's versioning is not symver.  To update to a new
# version of ibmtpm, modify `ibmversion` to reflect the 
# source code version.
%define ibmversion  1682

Summary:        This project is an implementation of the TCG TPM 2.0 specification.
Name:           ibmtpm
Version:        0.%{ibmversion}
Release:        1%{?dist}
License:        BSD 2-Clause
URL:            https://sourceforge.net/projects/ibmswtpm2/files
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner

Source0: https://sourceforge.net/projects/ibmswtpm2/files/%{name}%{ibmversion}.tar.gz

Patch0: support-openssl-3.2.x-builds.patch

BuildRequires: openssl-devel
BuildRequires: systemd-devel
BuildRequires: curl-devel

Requires: openssl
Requires: curl
Requires: systemd

%description
This project is an implementation of the TCG TPM 2.0 specification.
It is based on the TPM specification Parts 3 and 4 source code donated by Microsoft,
with additional files to complete the implementation.

%prep
%autosetup -p1 -c

%build
pushd src
%make_build
popd

%install
pushd src
%make_install %{?_smp_mflags}
popd

mkdir -p %{buildroot}%{_unitdir}
cat << EOF > %{buildroot}%{_unitdir}/ibmtpm_server.service
[Unit]
Description=ibmtpm_server

[Service]
Type=simple
ExecStart=%{_bindir}/tpm_server
EOF

%files
%defattr(-,root,root)
%{_bindir}/*
%{_unitdir}/ibmtpm_server.service

%changelog
* Mon Jan 22 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 0.1682-1
- Initial CBL-Mariner import from Photon (license: Apache2).
- Verified license
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1682-2
- Bump version as a part of openssl upgrade
* Sun Oct 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 1682-1
- Upgrade to v1682
* Thu Jun 03 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1661-2
- Compatibility with openssl 3.0
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1661-1
- Automatic Version Bump
* Thu Oct 08 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1637-3
- Fix GCC path issue
* Thu Sep 10 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1637-2
- Compatibility with openssl 1.1.1
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 1637-1
- Automatic Version Bump
* Fri May 29 2020 Michelle Wang <michellew@vmware.com> 1628-1
- Initial build. First version
