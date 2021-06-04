Summary:        Library providing support for "XML Signature" and "XML Encryption" standards
Name:           xmlsec1
Version:        1.2.26
Release:        5%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://www.aleksey.com/xmlsec/
Source0:        %{url}/download/older-releases/%{name}-%{version}.tar.gz

BuildRequires: libxml2-devel
BuildRequires: libltdl-devel

Requires:      libxml2
Requires:      libltdl

%description
XML Security Library is a C library based on LibXML2  and OpenSSL.
The library was created with a goal to support major XML security
standards "XML Digital Signature" and "XML Encryption".

%package devel
Summary: Libraries, includes, etc. to develop applications with XML Digital Signatures and XML Encryption support.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libxml2-devel
Requires: libltdl-devel

%description devel
Libraries, includes, etc. you can use to develop applications with XML Digital
Signatures and XML Encryption support.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%license COPYING

%{_prefix}/lib/libxmlsec1.so.1
%{_prefix}/lib/libxmlsec1.so.1.2.26
%{_prefix}/lib/libxmlsec1.so
%{_prefix}/lib/libxmlsec1-nss.so.1
%{_prefix}/lib/libxmlsec1-nss.so.1.2.26
%{_prefix}/lib/libxmlsec1-nss.so
%{_prefix}/lib/libxmlsec1-openssl.so.1
%{_prefix}/lib/libxmlsec1-openssl.so.1.2.26
%{_prefix}/lib/libxmlsec1-openssl.so
%{_prefix}/bin/xmlsec1

%files devel
%defattr(-, root, root)

%{_prefix}/bin/xmlsec1-config
%{_prefix}/include/xmlsec1/xmlsec/*.h
%{_prefix}/include/xmlsec1/xmlsec/private/*.h
%{_prefix}/include/xmlsec1/xmlsec/nss/*.h
%{_prefix}/include/xmlsec1/xmlsec/openssl/*.h
%{_prefix}/lib/libxmlsec1.*a
%{_prefix}/lib/libxmlsec1-nss.*a
%{_prefix}/lib/libxmlsec1-openssl.*a
%{_prefix}/lib/pkgconfig/xmlsec1.pc
%{_prefix}/lib/pkgconfig/xmlsec1-nss.pc
%{_prefix}/lib/pkgconfig/xmlsec1-openssl.pc
%{_prefix}/lib/xmlsec1Conf.sh
%{_prefix}/share/doc/xmlsec1/*
%{_prefix}/share/aclocal/xmlsec1.m4
%{_prefix}/share/man/man1/xmlsec1.1.gz
%{_prefix}/share/man/man1/xmlsec1-config.1.gz

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.2.26-5
- Added %%license line automatically

*   Fri Apr 24 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.2.26-4
-   License verified.
-   Fixed Source0 tag.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.26-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.26-2
-   Fix requires.
*   Mon Jul 02 2018 Ankit Jain <ankitja@vmware.com> 1.2.26-1
-   Initial version
