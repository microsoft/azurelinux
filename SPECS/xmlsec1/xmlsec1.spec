Summary:        Library providing support for "XML Signature" and "XML Encryption" standards
Name:           xmlsec1
Version:        1.3.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.aleksey.com/xmlsec
Source0:        https://www.aleksey.com/xmlsec/download/older-releases/%{name}-%{version}.tar.gz
BuildRequires:  gnutls-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libltdl-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  nss-devel
Requires:       libltdl
Requires:       libxml2
Requires:       nss
Provides:       %{name}-gcrypt = %{release}-%{version}
Provides:       %{name}-gnutls = %{release}-%{version}
Provides:       %{name}-openssl = %{release}-%{version}
Provides:       %{name}-nss = %{release}-%{version}
%if %{with_check}
BuildRequires:  nss-tools
%endif

%description
XML Security Library is a C library based on LibXML2  and OpenSSL.
The library was created with a goal to support major XML security
standards "XML Digital Signature" and "XML Encryption".

%package devel
Summary:        Libraries, includes, etc. to develop applications with XML Digital Signatures and XML Encryption support.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gnutls-devel
Requires:       libgcrypt-devel
Requires:       libltdl-devel
Requires:       libxml2-devel
Requires:       nss-devel
Provides:       %{name}-gcrypt-devel = %{release}-%{version}
Provides:       %{name}-gnutls-devel = %{release}-%{version}
Provides:       %{name}-openssl-devel = %{release}-%{version}
Provides:       %{name}-nss-devel = %{release}-%{version}

%description devel
Libraries, includes, etc. you can use to develop applications with XML Digital
Signatures and XML Encryption support.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%license COPYING

%{_libdir}/libxmlsec1.so.1
%{_libdir}/libxmlsec1.so.%{version}
%{_libdir}/libxmlsec1.so
%{_libdir}/libxmlsec1-nss.so.1
%{_libdir}/libxmlsec1-nss.so.%{version}
%{_libdir}/libxmlsec1-nss.so
%{_libdir}/libxmlsec1-openssl.so.1
%{_libdir}/libxmlsec1-openssl.so.%{version}
%{_libdir}/libxmlsec1-openssl.so
%{_libdir}/libxmlsec1-gnutls*
%{_libdir}/libxmlsec1-gcrypt*
%{_bindir}/xmlsec1

%files devel
%defattr(-, root, root)

%{_bindir}/xmlsec1-config
%{_includedir}/xmlsec1/xmlsec/*.h
%{_includedir}/xmlsec1/xmlsec/nss/*.h
%{_includedir}/xmlsec1/xmlsec/openssl/*.h
%{_includedir}/xmlsec1/xmlsec/gcrypt/*
%{_includedir}/xmlsec1/xmlsec/gnutls/*
%{_libdir}/libxmlsec1.*a
%{_libdir}/libxmlsec1-nss.*a
%{_libdir}/libxmlsec1-openssl.*a
%{_libdir}/pkgconfig/xmlsec1.pc
%{_libdir}/pkgconfig/xmlsec1-nss.pc
%{_libdir}/pkgconfig/xmlsec1-openssl.pc
%{_libdir}/pkgconfig/xmlsec1-gcrypt.pc
%{_libdir}/pkgconfig/xmlsec1-gnutls.pc
%{_libdir}/xmlsec1Conf.sh
%{_docdir}/xmlsec1/*
%{_datadir}/aclocal/xmlsec1.m4
%{_mandir}/man1/xmlsec1.1.gz
%{_mandir}/man1/xmlsec1-config.1.gz

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-1
- Auto-upgrade to 1.3.1 - Azure Linux 3.0 - package upgrades

* Mon Oct 02 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.34-2
- Adding BR for 'libxslt-devel' to fix a build issue.

* Fri Sep 23 2022 Andrew Phelps <anphel@microsoft.com> - 1.2.34-1
- Update to version 1.2.34
- Add nss-tools to fix check tests

* Tue Nov 30 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.2.26-8
- Add nss as an explicit requirement.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.2.26-7
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Jan 12 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.2.26-6
- Enable gcrypt and gnutls support and add explicit provides.

* Sat May 09 00:21:10 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.2.26-5
- Added %%license line automatically

* Fri Apr 24 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.2.26-4
- License verified.
- Fixed Source0 tag.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.26-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.26-2
- Fix requires.

* Mon Jul 02 2018 Ankit Jain <ankitja@vmware.com> 1.2.26-1
- Initial version
