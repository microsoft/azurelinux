Summary:        OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:           tpm2-pkcs11
Version:        1.8.0
Release:        5%{?dist}
License:        BSD 2-Clause
URL:            https://github.com/tpm2-software/tpm2-pkcs11
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner

Source0: https://github.com/tpm2-software/tpm2-pkcs11/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 tpm2=006943b3853dc80e44d2322ea0278d6a9f2139c3b3e2a2c5f33436d479d698c5b9d685fb1166d22562bcf3d52edb1075efe7592c27a8c3a0cd05356cab3c9874

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  openssl-devel
BuildRequires:  tpm2-tools
BuildRequires:  tpm2-tss-devel
BuildRequires:  tpm2-abrmd-devel
BuildRequires:  libyaml-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  sqlite-devel
BuildRequires:  autoconf-archive
BuildRequires:  python3-devel
BuildRequires:  python3-cryptography
BuildRequires:  python3-setuptools
BuildRequires:  python3-PyYAML
BuildRequires:  python3-pyasn1-modules
BuildRequires:  libcmocka-devel
BuildRequires:  dbus
BuildRequires:  tpm2-pytss

%if 0%{?with_check}
BuildRequires: python3-pip
%endif

Requires:   openssl
Requires:   tpm2-tools
Requires:   tpm2-tss
Requires:   tpm2-abrmd
Requires:   libyaml
Requires:   sqlite-libs
Requires:   tpm2-pytss

%description
OSS implementation of the TCG TPM2 PKCSv11 Software Stack

%package          tools
Summary:          The tools required to setup and configure TPM2 for PKCSv11
Requires:         %{name} = %{version}-%{release}
Requires:         python3
Requires:         python3-cryptography
Requires:         python3-setuptools
Requires:         python3-pyasn1-modules
Requires:         python3-PyYAML

%description tools
Tools for TCG TPM2 PKCSv11 Software Stack

%prep
%autosetup -p1 -n %{name}-%{version}

%build
sh ./bootstrap

%configure \
    --enable-unit

%make_build PACKAGE_VERSION=%{version}

cd tools
%py3_build

%install
%make_install %{?_smp_mflags}

rm %{buildroot}%{_libdir}/pkgconfig/tpm2-pkcs11.pc

cd tools
%py3_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
cd tools
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libtpm2_pkcs11.so
%{_libdir}/libtpm2_pkcs11.so.0*

%files tools
%defattr(-,root,root,-)
%{_bindir}/tpm2_ptool
%{python3_sitelib}/*

%changelog
* Mon Jan 22 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 1.8.0-5
- Initial CBL-Mariner import from Photon (license: Apache2).
- Verified license
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.8.0-5
- Bump version as a part of openssl upgrade
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 1.8.0-4
- bump release as part of sqlite update
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.8.0-3
- Update release to compile with python 3.11
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.0-2
- Bump version as a part of autoconf-archive upgrade
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com>  1.8.0-1
- Upgrade to v1.8.0
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.0-4
- Bump version as a part of sqlite upgrade
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.0-3
- Fix cmocka dependency
* Thu Sep 02 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.6.0-2
- openssl 3.0.0 compatibility
* Sun Aug 8 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.6.0-1
- Initial build. First version
