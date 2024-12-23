Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           pkcs11-helper
Version:        1.30.0
Release:        1%{?dist}
Summary:        A library for using PKCS#11 providers

License:        GPL-2 or BSD-3-Clause
URL:            http://www.opensc-project.org/opensc/wiki/pkcs11-helper
Source0:        https://github.com/OpenSC/pkcs11-helper/releases/download/pkcs11-helper-%{version}/pkcs11-helper-%{version}.tar.bz2
# https://github.com/OpenSC/pkcs11-helper/pull/4
Patch2:         pkcs11-helper-rfc7512.patch

BuildRequires:  gcc
BuildRequires:  doxygen graphviz
BuildRequires:  make
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
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       openssl-devel
# for /usr/share/aclocal
Requires:       automake

%description    devel
This package contains header files and documentation necessary for developing
programs using the pkcs11-helper library.


%prep
%autosetup -p1

%build
%configure --disable-static --enable-doc
%make_build


%install
%make_install

# Use %%doc to install documentation in a standard location
mkdir apidocdir
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/api/ apidocdir/
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/

# Remove libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%files
%license COPYING*
%doc AUTHORS ChangeLog README THANKS
%{_libdir}/libpkcs11-helper.so.1*


%files devel
%doc apidocdir/*
%{_includedir}/pkcs11-helper-1.0/
%{_libdir}/libpkcs11-helper.so
%{_libdir}/pkgconfig/libpkcs11-helper-1.pc
%{_datadir}/aclocal/pkcs11-helper-1.m4
%{_mandir}/man8/pkcs11-helper-1.8*


%changelog
* Wed Dec 18 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.30.0-1
- Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Feb 02 2024 Kalev Lember <klember@redhat.com> - 1.30.0-1
- Update to 1.30.0
- Use SPDX license identifiers

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 21 2022 Anthony Rabbito <hello@anthonyrabbito.com> - 1.29.0-1
- Update to 1.29.0

* Thu Apr 21 2022 Anthony Rabbito <hello@anthonyrabbito.com> - 1.28.0-3
- Drop pkcs11-helper-openssl3.patch

* Thu Apr 21 2022 Anthony Rabbito <hello@anthonyrabbito.com> - 1.28.0-2
- Use version macro in the entire source URL.

* Thu Apr 21 2022 Anthony Rabbito <hello@anthonyrabbito.com> - 1.28.0-1
- Update to 1.28.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Neal Gompa <ngompa@fedoraproject.org> - 1.27.0-6
- Backport fix for OpenSSL 3.0 support

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.27.0-5
- Rebuilt with OpenSSL 3.0.0

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 2020 Kalev Lember <klember@redhat.com> - 1.27.0-2
- Update pkcs11-helper-rfc7512.patch from
  https://github.com/OpenSC/pkcs11-helper/pull/4 (#1849259)

* Fri Nov 20 2020 Kalev Lember <klember@redhat.com> - 1.27.0-1
- Update to 1.27.0
- Use make_build and make_install macros
- Tighten soname globs
- Use license macro for COPYING*
- Tighten requires with _isa macro

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
