Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		gssntlmssp
Version:	0.9.0
Release:	2%{?dist}
Summary:	GSSAPI NTLMSSP Mechanism

License:	LGPLv3+
URL:		https://fedorahosted.org/gss-ntlmssp
Source0:        https://fedorahosted.org/released/gss-ntlmssp/%{name}-%{version}.tar.gz

Requires: krb5-libs >= 1.12.1-9

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: m4
BuildRequires: libxslt
BuildRequires: libxml2
BuildRequires: docbook-style-xsl
BuildRequires: doxygen
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildRequires: krb5-devel >= 1.11.2
BuildRequires: libunistring-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel

%description
A GSSAPI Mechanism that implements NTLMSSP

%package devel
Summary: Development header for GSSAPI NTLMSSP
License: LGPLv3+

%description devel
Adds a header file with definition for custom GSSAPI extensions for NTLMSSP


%prep
%setup -q

%build
autoreconf -fiv
%configure \
    --disable-rpath \
    --disable-static \
    --without-wbclient

make %{?_smp_mflags} all

%install
%make_install
rm -f %{buildroot}%{_libdir}/gssntlmssp/gssntlmssp.la
mkdir -p %{buildroot}%{_sysconfdir}/gss/mech.d
install -pm644 examples/mech.ntlmssp %{buildroot}%{_sysconfdir}/gss/mech.d/ntlmssp.conf
%{find_lang} %{name}

%check
make test_gssntlmssp

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/gss/mech.d/ntlmssp.conf
%{_libdir}/gssntlmssp/
%{_mandir}/man8/gssntlmssp.8*
%doc COPYING

%files devel
%{_includedir}/gssapi/gssapi_ntlmssp.h

%changelog
* Fri Jul 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing architecture info from 'krb5-libs' dependency to adjust it to CBL-Mariner's packages.
- Building without 'wbclient'.

* Wed Apr 29 2020 Simo Sorce <simo@redhat.com> - 0.9.0-1
- Update to 0.9.0 release

* Fri Apr 24 2020 Simo Sorce <simo@redhat.com> - 0.8.0-1
- Update to 0.8.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 1  2019 Simo Sorce <simo@redhat.com> - 0.7.0-10
- Add missing build dependencies

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 17 2017 Simo Sorce <simo@samba.org> - 0.7.0-3
- Add OpenSSL 1.1.0 compatibility patch

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jun  3 2016 Simo Sorce <simo@samba.org> - 0.7.0-1
- New release 0.7.0

* Fri May 20 2016 Simo Sorce <simo@samba.org> - 0.6.0-4
- Fix regression in acquire credential code
- Resolves: #1290831

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 19 2015 Simo Sorce <simo@samba.org> - 0.6.0-1
- New verion with fixes for 32 bit arches
- drop patches, they are included in he new upstream release

* Thu Jan 08 2015   Simo Sorce <simo@samba.org> - 0.5.0-4
- Fix build failure in rawhide due to automake 1.15 change in behavior

* Wed Jan 07 2015   Simo Sorce <simo@samba.org> - 0.5.0-4
- fix bug #1178686

* Tue Sep 02 2014 Pádraig Brady <pbrady@redhat.com> - 0.5.0-3
- rebuild for libunistring soname bump

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Simo Sorce <simo@samba.org> - 0.5.0-1
- New upstream version

* Fri Aug 1  2014 Simo Sorce <simo@samba.org> - 0.4.0-2
- put configuration in the new mech.d directory introduced as a backport in
  krb5-1.12.1-9

* Sat Jun 21 2014 Simo Sorce <simo@samba.org> - 0.4.0-1
- New upstream release 0.4.0:
  * Added support for MIC and Channel Binding features of NTLMv2
  * Improve testing so that multiple versions can be tested
  * Various importnat fixes in the GSSAPI interface that were causing errors
  * Special workaround for SPNEGO mechanism when talking to Windows Servers and
    using the internal NTLM MIC feature.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 26 2014 Simo Sorce <simo@samba.org> - 0.3.1-0
- Fixes #1058025
- New upstream release 0.3.1:
  * Fix segfault in init context.

* Sun Jan 12 2014 Simo Sorce <simo@samba.org> - 0.3.0-0
- New upstream release 0.3.0:
  * Added support for NTLMv1 Signing and Sealing completing full coverage
    of the NTLM protocol
  * Added a number of GSSAPI calls to inquire, export and import context and
    credentials, in preparation for making it work with GSS-Proxy
  * Various fixes memleak and other fixes

* Fri Dec 13 2013 Simo Sorce <simo@samba.org> - 0.2.0-2
- Backport patches to fix memory leaks

* Wed Dec  4 2013 Simo Sorce <simo@samba.org> - 0.2.0-1
- Backport patch that fixes failures with gss_set_neg_mechs() calls.

* Fri Oct 18 2013 Simo Sorce <simo@samba.org> - 0.2.0-0
- New upstream realease 0.2.0:
  * Add support for acquire_cred_with_password()
  * Fix Signing keys generation
  * Add enterprise names support
  * Add connectionless mode support
  * Add development header gssapi_ntlmssp.h
  * Various bugfixes and tests for new features 

* Thu Oct 17 2013 Simo Sorce <simo@samba.org> - 0.1.0-2
- Fix Requires

* Thu Oct 17 2013 Simo Sorce <simo@samba.org> - 0.1.0-1
- Initial import of 0.1.0

