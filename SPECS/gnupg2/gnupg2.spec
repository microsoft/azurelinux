Summary:        OpenPGP standard implementation used for encrypted communication and data storage.
Name:           gnupg2
Version:        2.2.41
Release:        1%{?dist}
License:        BSD and CC0 and GPLv2+ and LGPLv2+
URL:            https://gnupg.org/index.html
Group:          Applications/Cryptography.
Source0:        https://gnupg.org/ftp/gcrypt/gnupg/gnupg-%{version}.tar.bz2
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
BuildRequires:  npth-devel
BuildRequires:  libassuan
BuildRequires:  libksba >= 1.0.7
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error >= 1.24

Requires:       libksba
Requires:       libgcrypt >= 1.7.0
Requires:       npth
Requires:       libassuan
Requires:       pinentry

Provides:       gpg

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
%setup -q -n gnupg-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING COPYING.CC0 COPYING.GPL2 COPYING.LGPL3 COPYING.LGPL21 COPYING.other
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/locale/*/*/*
%{_mandir}/*
%{_infodir}/gnupg*
%{_libexecdir}/*
%{_datadir}/gnupg/*
%exclude %{_infodir}/dir
%exclude /usr/share/doc/*

%changelog
* Mon Feb 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.2.41-1
- Auto-upgrade to 2.2.41 - to fix CVE-2022-3515

*   Mon Jun 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.2.20-3
-   Adding a license reference.
-   License verified.
*   Thu Apr 16 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.2.20-2
-   Rename gnupg to gnupg2
-   Update description.
*   Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> 2.2.20-1
-   Update to 2.2.20. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.2.10-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sat Oct 20 2018 Ankit Jain <ankitja@vmware.com> 2.2.10-1
-   Update to 2.2.10
*   Wed Aug 30 2017 Alexey Makhalov <amakhalov@vmware.com> 2.1.20-3
-   Add requires libgcrypt
*   Wed Jun 07 2017 Danut Moraru <dmoraru@vmware.com> 2.1.20-2
-   Add pinentry dependency
*   Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> 2.1.20-1
-   Update to 2.1.20
*   Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 2.0.30-1
-   Initial Build.
