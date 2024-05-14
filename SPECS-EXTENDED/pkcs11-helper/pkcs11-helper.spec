Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           pkcs11-helper
Version:        1.22
Release:        11%{?dist}
Summary:        A library for using PKCS#11 providers

License:        GPLv2 or BSD
URL:            https://www.opensc-project.org/opensc/wiki/pkcs11-helper
Source0:        https://downloads.sourceforge.net/opensc/pkcs11-helper-%{version}.tar.bz2
Patch2:         pkcs11-helper-rfc7512.patch

BuildRequires:  gcc
BuildRequires:  doxygen graphviz
BuildRequires:  openssl-devel

%description
pkcs11-helper is a library that simplifies the interaction with PKCS#11
providers for end-user applications using a simple API and optional OpenSSL
engine. The library allows using multiple PKCS#11 providers at the same time,
enumerating available token certificates, or selecting a certificate directly
by serialized id, handling card removal and card insert events, handling card
re-insert to a different slot, supporting session expiration and much more all
using a simple API. 

%package        devel
Summary:        Development files for pkcs11-helper
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel
# for /usr/share/aclocal
Requires:       automake

%description    devel
This package contains header files and documentation necessary for developing
programs using the pkcs11-helper library.


%prep
%setup -q
%patch 2 -p1

%build
%configure --disable-static --enable-doc
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Use %%doc to install documentation in a standard location
mkdir apidocdir
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/api/ apidocdir/
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/

# Remove libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%ldconfig_scriptlets


%files
%doc AUTHORS ChangeLog COPYING* README THANKS
%{_libdir}/libpkcs11-helper.so.*


%files devel
%doc apidocdir/*
%{_includedir}/pkcs11-helper-1.0/
%{_libdir}/libpkcs11-helper.so
%{_libdir}/pkgconfig/libpkcs11-helper-1.pc
%{_datadir}/aclocal/pkcs11-helper-1.m4
%{_mandir}/man8/pkcs11-helper-1.8*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.22-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Apr 24 2020 David Woodhouse <dwmw2@infradead.org> - 1.22-10
- Fix serialisation of attributes with NUL bytes in (#1825496)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 24 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.22-4
- Addressed issue with RFC7512 URI parsing (#1516474)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 21 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.22-1
- New upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 22 2015 David Woodhouse <David.Woodhouse@intel.com> - 1.11-7
- Fix ID buffer size for URI parsing (#1264645)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 David Woodhouse <David.Woodhouse@intel.com> - 1.11-5
- Migrate ID serialisation format to RFC7512 (#1173554)

* Tue Dec 09 2014 David Woodhouse <David.Woodhouse@intel.com> - 1.11-4
- Apply upstream fix for bug #1172237 (ignore objects without CKA_ID)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Jon Ciesla <limburgher@gmail.com> - 1.11-1
- Latest upstream, required for openvpn 2.3.3.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 02 2013 Kalev Lember <kalevlember@gmail.com> - 1.10-1
- Update to 1.10

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 17 2011 Kalev Lember <kalevlember@gmail.com> - 1.09-1
- Update to 1.09

* Sun Jun 19 2011 Kalev Lember <kalev@smartlink.ee> - 1.08-1
- Update to 1.08
- Clean up the spec file for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 01 2010 Kalev Lember <kalev@smartlink.ee> - 1.07-5
- use System Environment/Libraries group for main package
- removed R: pkgconfig from devel subpackage

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.07-4
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Kalev Lember <kalev@smartlink.ee> - 1.07-2
- Make devel package depend on automake for /usr/share/aclocal

* Tue Jun 23 2009 Kalev Lember <kalev@smartlink.ee> - 1.07-1
- Initial RPM release.
