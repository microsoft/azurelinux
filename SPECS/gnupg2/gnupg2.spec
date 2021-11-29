Summary:        OpenPGP standard implementation used for encrypted communication and data storage.
Name:           gnupg2
Version:        2.3.3
Release:        1%{?dist}
License:        BSD and CC0 and GPLv2+ and LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Cryptography.
URL:            https://gnupg.org/index.html
Source0:        https://gnupg.org/ftp/gcrypt/gnupg/gnupg-%{version}.tar.bz2
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
BuildRequires:  npth-devel >= 1.2
BuildRequires:  libassuan-devel >= 2.5.0
BuildRequires:  libksba-devel >= 1.3.4
BuildRequires:  libgcrypt-devel > 1.9.1
BuildRequires:  libgpg-error-devel >= 1.41
Requires:       libksba > 1.3.4
Requires:       libgcrypt >= 1.9.1
Requires:       libgpg-error >= 1.41
Requires:       npth >= 1.2
Requires:       libassuan >= 2.5.0
Requires:       pinentry

Provides:       gpg = %{version}-%{release}
Provides:       gnupg = %{version}-%{release}
Provides:       %{name}-smime = %{version}-%{release}

%description
GnuPG is GNU's tool for secure communication and data storage.  It can
be used to encrypt data and to create digital signatures.  It includes
an advanced key management facility and is compliant with the proposed
OpenPGP Internet standard as described in RFC2440 and the S/MIME
standard as described by several RFCs.
 
GnuPG 2.0 is a newer version of GnuPG with additional support for
S/MIME.  It has a different design philosophy that splits
functionality up into several modules. The S/MIME and smartcard functionality
is provided by the gnupg2-smime package.

%prep
%autosetup -n gnupg-%{version}

%build
%configure \
  --enable-gpg-is-gpg2
%make_build

%install
%make_install

pushd %{buildroot}%{_bindir}
ln -s gpg2 gpg
ln -s gpgv2 gpgv
popd

%check
%make_build check

%files
%defattr(-,root,root)
%license COPYING COPYING.CC0 COPYING.GPL2 COPYING.LGPL3 COPYING.LGPL21 COPYING.other
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/locale/*/*/*
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_infodir}/gnupg*
%{_libexecdir}/*
%{_datadir}/gnupg/*
%exclude %{_infodir}/dir
%exclude /usr/share/doc/*

%changelog
* Mon Nov 22 2021 Thomas Crain <thcrain@microsoft.com> - 2.3.3-1
- Upgrade to latest upstream version

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.2.20-4
- Build with gpg2 option and gpg compatibility
- Provide gnupg2-smime, gnupg

* Mon Jun 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.20-3
- Adding a license reference.
- License verified.

* Thu Apr 16 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.2.20-2
- Rename gnupg to gnupg2
- Update description.

* Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.2.20-1
- Update to 2.2.20. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.2.10-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sat Oct 20 2018 Ankit Jain <ankitja@vmware.com> - 2.2.10-1
- Update to 2.2.10

* Wed Aug 30 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.1.20-3
- Add requires libgcrypt

* Wed Jun 07 2017 Danut Moraru <dmoraru@vmware.com> - 2.1.20-2
- Add pinentry dependency

* Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> - 2.1.20-1
- Update to 2.1.20

* Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> - 2.0.30-1
- Initial Build.
