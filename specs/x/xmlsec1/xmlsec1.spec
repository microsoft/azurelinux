# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# widely used
%bcond openssl 1
# used by libreoffice
%bcond nss 1
# not used
%bcond gcrypt %{undefined rhel}
# not used; gnutls depends on gcrypt
%bcond gnutls %{with gcrypt}

Summary: Library providing support for "XML Signature" and "XML Encryption" standards
Name: xmlsec1
Version: 1.2.41
Release: 4%{?dist}%{?extra_release}
Epoch: 1
License: MIT
Source0: https://github.com/lsh123/xmlsec/releases/download/%{version}/xmlsec1-%{version}.tar.gz
URL: http://www.aleksey.com/xmlsec/

Patch0: 0001-Conditional-include-for-openssl-engines.patch

BuildRequires: make
BuildRequires: pkgconfig(libxml-2.0) >= 2.8.0
BuildRequires: pkgconfig(libxslt) >= 1.0.20
%if %{with openssl}
BuildRequires: pkgconfig(openssl) >= 3.0.0
%endif
%if %{with nss}
BuildRequires: pkgconfig(nss) >= 3.49.0
BuildRequires: pkgconfig(nspr) >= 4.25.0
%endif
%if %{with gcrypt}
BuildRequires: libgcrypt-devel >= 1.4.0
%endif
%if %{with gnutls}
BuildRequires: pkgconfig(gnutls) >= 3.6.13
%endif
BuildRequires: libtool-ltdl-devel
# autoreconf stuff
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool

%description
XML Security Library is a C library based on LibXML2  and OpenSSL.
The library was created with a goal to support major XML security
standards "XML Digital Signature" and "XML Encryption".

%package devel
Summary: Libraries, includes, etc. to develop applications with XML Digital Signatures and XML Encryption support.
Requires: xmlsec1%{?_isa} = 1:%{version}-%{release}
Requires: openssl-devel%{?_isa} >= 1.0.0

%description devel
Libraries, includes, etc. you can use to develop applications with XML Digital
Signatures and XML Encryption support.

%if %{with openssl}
%package openssl
Summary: OpenSSL crypto plugin for XML Security Library
Requires: xmlsec1%{?_isa} = 1:%{version}-%{release}

%description openssl
OpenSSL plugin for XML Security Library provides OpenSSL based crypto services
for the xmlsec library.

%package openssl-devel
Summary: OpenSSL crypto plugin for XML Security Library
Requires: xmlsec1-devel%{?_isa} = 1:%{version}-%{release}
Requires: xmlsec1-openssl%{?_isa} = 1:%{version}-%{release}

%description openssl-devel
Libraries, includes, etc. for developing XML Security applications with OpenSSL
%endif

%if %{with gcrypt}
%package gcrypt
Summary: GCrypt crypto plugin for XML Security Library
Requires: xmlsec1%{?_isa} = 1:%{version}-%{release}
Provides: deprecated()

%description gcrypt
GCrypt plugin for XML Security Library provides GCrypt based crypto services
for the xmlsec library.

%package gcrypt-devel
Summary: GCrypt crypto plugin for XML Security Library
Requires: xmlsec1-devel%{?_isa} = 1:%{version}-%{release}
Requires: xmlsec1-gnutls-devel%{?_isa} = 1:%{version}-%{release}
Provides: deprecated()

%description gcrypt-devel
Libraries, includes, etc. for developing XML Security applications with GCrypt.
%endif

%if %{with gnutls}
%package gnutls
Summary: GNUTls crypto plugin for XML Security Library
Requires: xmlsec1%{?_isa} = 1:%{version}-%{release}
Provides: deprecated()

%description gnutls
GNUTls plugin for XML Security Library provides GNUTls based crypto services
for the xmlsec library.

%package gnutls-devel
Summary: GNUTls crypto plugin for XML Security Library
Requires: xmlsec1-devel%{?_isa} = 1:%{version}-%{release}
Requires: xmlsec1-openssl-devel%{?_isa} = 1:%{version}-%{release}
Requires: gnutls-devel%{?_isa} >= 1.0.20
Provides: deprecated()

%description gnutls-devel
Libraries, includes, etc. for developing XML Security applications with GNUTls.
%endif

%if %{with nss}
%package nss
Summary: NSS crypto plugin for XML Security Library
Requires: xmlsec1%{?_isa} = 1:%{version}-%{release}

%description nss
NSS plugin for XML Security Library provides NSS based crypto services
for the xmlsec library

%package nss-devel
Summary: NSS crypto plugin for XML Security Library
Requires: xmlsec1-devel%{?_isa} = 1:%{version}-%{release}
Requires: xmlsec1-nss%{?_isa} = 1:%{version}-%{release}

%description nss-devel
Libraries, includes, etc. for developing XML Security applications with NSS.
%endif

%prep
%autosetup -p1

%build
autoreconf -vfi
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build V=1

# positively ugly but only sane way to get around #192756
sed 's+/lib64+/$archlib+g' < xmlsec1-config | sed 's+/lib+/$archlib+g' | sed 's+ -DXMLSEC_NO_SIZE_T++' > xmlsec1-config.$$ && mv xmlsec1-config.$$ xmlsec1-config

%install
%make_install
rm -vf %{buildroot}%{_libdir}/*.la

# move installed docs to include them in -devel package via %%doc magic
rm -rf __tmp_doc ; mkdir __tmp_doc
mv %{buildroot}%{_docdir}/xmlsec1/* __tmp_doc

%files
%doc AUTHORS ChangeLog NEWS Copyright
%{_mandir}/man1/xmlsec1.1*
%{_libdir}/libxmlsec1.so.*
%{_bindir}/xmlsec1

%files devel
%{_bindir}/xmlsec1-config
%dir %{_includedir}/xmlsec1
%dir %{_includedir}/xmlsec1/xmlsec
%{_includedir}/xmlsec1/xmlsec/*.h
%{_libdir}/libxmlsec1.so
%{_libdir}/pkgconfig/xmlsec1.pc
%{_libdir}/xmlsec1Conf.sh
%{_datadir}/aclocal/xmlsec1.m4
%{_mandir}/man1/xmlsec1-config.1*
%doc HACKING __tmp_doc/*

%if %{with openssl}
%files openssl
%{_libdir}/libxmlsec1-openssl.so.*
%{_libdir}/libxmlsec1-openssl.so

%files openssl-devel
%{_includedir}/xmlsec1/xmlsec/openssl/
%{_libdir}/pkgconfig/xmlsec1-openssl.pc
%endif

%if %{with gcrypt}
%files gcrypt
%{_libdir}/libxmlsec1-gcrypt.so.*
%{_libdir}/libxmlsec1-gcrypt.so

%files gcrypt-devel
%{_includedir}/xmlsec1/xmlsec/gcrypt/
%{_libdir}/pkgconfig/xmlsec1-gcrypt.pc
%endif

%if %{with gnutls}
%files gnutls
%{_libdir}/libxmlsec1-gnutls.so.*
%{_libdir}/libxmlsec1-gnutls.so

%files gnutls-devel
%{_includedir}/xmlsec1/xmlsec/gnutls/
%{_libdir}/pkgconfig/xmlsec1-gnutls.pc
%endif

%if %{with nss}
%files nss
%{_libdir}/libxmlsec1-nss.so.*
%{_libdir}/libxmlsec1-nss.so

%files nss-devel
%{_includedir}/xmlsec1/xmlsec/nss/
%{_libdir}/pkgconfig/xmlsec1-nss.pc
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Tomas Halman <thalman@redhat.com> - 1:1.2.41-1
- Rebase to 1.2.41

* Thu Nov 7 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.2.39-5
- Conditionalize the backends
- Remove openssl-devel-engine dependency

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 3 2024 Tomas Halman <thalman@redhat.com> - 1:1.2.39-3
- Add openssl-devel-engine dependency

* Wed Jul 3 2024 Tomas Halman <thalman@redhat.com> - 1:1.2.39-2
- Deprecate subpackages depending on gcrypt

* Wed Jun 5 2024 Tomas Halman <thalman@redhat.com> - 1.2.39-1
- Rebase to 1.2.39

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.37-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.2.37-6
- Fix build with libxml2-2.12.0

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Tomas Halman <thalman@redhat.com> - 1.2.37-4
- Resolves: rhbz#2187631 - Cannot load modules/mod_auth_mellon.so
  Revert to previous version

* Fri Apr 14 2023 Tomas Halman <thalman@redhat.com> - 1.3.0-1
- Resolves: rhbz#2186304 - rebase to version 1.3.0

* Tue Mar 7 2023 Tomas Halman <thalman@redhat.com> - 1.2.37-3
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Tomas Halman <thalman@redhat.com> - 1.2.37-1
- Resolves: rhbz#2149129 latest upstream release

* Tue Nov 08 2022 Caolán McNamara <caolanm@redhat.com> - 1.2.36-1
- Resolves: rhbz#2138484 latest upstream release

* Thu Oct 27 2022 Caolán McNamara <caolanm@redhat.com> - 1.2.35-1
- Resolves: rhbz#2137430 latest upstream release

* Mon Oct 24 2022 David King <amigadave@amigadave.com> - 1.2.34-3
- Rebuild against libxml2 (#2136800)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 18 2022 Caolán McNamara <caolanm@redhat.com> - 1.2.34-1
- Resolves: rhbz#2081413 latest upstream release

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Nov 14 2021 Caolán McNamara <caolanm@redhat.com> - 1.2.33-1
- Resolves: rhbz#1826433 latest upstream release

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.2.29-5
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Caolán McNamara <caolanm@redhat.com> - 1.2.29-1
- New upstream release

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 23 2018 Simo Sorce <simo@redhat.com> - 1.2.27-1
- New upstream release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 12 2018 John Dennis <jdennis@redhat.com> - 1.2.25-4
- Resolves: rhbz#1566748
  xmlSecOpenSSLX509DataNodeRead fails to return error

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.25-2
- Switch to %%ldconfig_scriptlets

* Wed Nov 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.25-1
- Update to 1.2.25

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 17 2016 Simo Sorce <simo@redhat.com> - 1.2.23-1
- New Upstream relase 1.2.23
- Adds compatibility for OpenSSL 1.1.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 19 2014 Simo Sorce <simo@redhat.com> - 1.2.20-1
- Update to new upstream release 1.2.20
- This release fixes a number of miscellaneous bugs and updates expired or
  soon-to-be-expired certificates in the test suite.
- Also drops the no-ecdsa patch

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Tomáš Mráz <tmraz@redhat.com> - 1.2.19-4
- Rebuild for new libgcrypt

* Fri Dec 13 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2.19-3
- Fix duplicate documentation (#1001250)
- Turn on verbose build output via V=1 make
- Use %%?_isa in explicit package deps
- Fix base package Group tag to "System Environment/Libraries"
- Remove %%defattr

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Daniel Veillard <veillard@redhat.com> - 1.2.19-1
- Update to upstream release 1.2.19

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May 12 2011 Daniel Veillard <veillard@redhat.com> - 1.2.18-1
- Update to upstream release 1.2.18

* Mon Apr 11 2011 Daniel Veillard <veillard@redhat.com> - 1.2.17-1
- Update to upstream release 1.2.17
- fixes CVE-2011-1425 on xslt file creation

* Tue Mar 22 2011 Daniel Veillard <veillard@redhat.com> - 1.2.16-4
- Fix missing links to unversioned shared library files 541599

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.16-2
- add missing BuildRequires: libtool-ltdl-devel

* Wed Jun  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.16-1
- update to 1.2.16
- cleanup spec file
- disable static libs
- disable rpath
- enable gcrypt subpackage

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.12-2
- rebuilt with new openssl

* Tue Aug 11 2009 Daniel Veillard <veillard@redhat.com> - 1.2.12-1
- update to new upstream release 1.2.12
- includes fix for CVE-2009-0217
- cleanup spec file

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.11-2
- rebuild with new openssl

* Fri Jul 11 2008 Daniel Veillard <veillard@redhat.com> - 1.2.11-1
- update to new upstream release 1.2.11
- rebuild for gnutls update

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.9-10.1
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.2.9-9
 - Rebuild for deps

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-8.1
- rebuild

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.9-8
- rebuilt with new gnutls

* Thu Jun  8 2006 Daniel Veillard <veillard@redhat.com> - 1.2.9-7
- oops libxmlsec1.la was still there, should fix #171410 and #154142

* Thu Jun  8 2006 Daniel Veillard <veillard@redhat.com> - 1.2.9-6
- Ugly patch and sed based changes to work around #192756 xmlsec1-config
  multilib problem

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1.2.9-5
- move .so symlinks to -devel subpackage

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Dec 15 2005 Christopher Aillon <caillon@redhat.com> 1.2.9-4
- NSS has been split out of the mozilla package, so require that now
  and update separate_nspr.patch to account for the new NSS as well

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 23 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-3
- rebuilt due to gnutls library revision
* Wed Nov  9 2005 <veillard@redhat.com> 1.2.9-2
- rebuilt due to openssl library revision
* Tue Sep 20 2005 <veillard@redhat.com> 1.2.9-1
- update from upstream, release done in July
- apparently nss is now available on ppc64
* Mon Aug  8 2005 <veillard@redhat.com> 1.2.8-3
- rebuilt with new gnutls
- nspr has been split to a separate package
* Fri Jul  8 2005 Daniel Veillard <veillard@redhat.com> 1.2.8-2
- Enabling the mozilla-nss crypto backend
* Fri Jul  8 2005 Daniel Veillard <veillard@redhat.com> 1.2.8-1
- update from upstream, needed for openoffice
* Tue Mar  8 2005 Daniel Veillard <veillard@redhat.com> 1.2.7-4
- rebuilt with gcc4
* Wed Feb 23 2005 Daniel Veillard <veillard@redhat.com> 1.2.7-1
- Upstream release of 1.2.7, mostly bug fixes plus new functions
  to GetKeys from simple store and X509 handling.
* Wed Feb  9 2005 Daniel Veillard <veillard@redhat.com> 1.2.6-4
- Adding support for GNUTls crypto backend
* Wed Sep  1 2004 Daniel Veillard <veillard@redhat.com> 1.2.6-3
- adding missing ldconfig calls
* Thu Aug 26 2004 Daniel Veillard <veillard@redhat.com> 1.2.6-2
- updated with upstream release from Aleksey
* Mon Jun 21 2004 Daniel Veillard <veillard@redhat.com> 1.2.5-2
- rebuilt
* Mon Apr 19 2004 Daniel Veillard <veillard@redhat.com> 1.2.5-1
- updated with upstream release from Aleksey
* Wed Feb 11 2004 Daniel Veillard <veillard@redhat.com> 1.2.4-1
- updated with upstream release from Aleksey
* Tue Jan  6 2004 Daniel Veillard <veillard@redhat.com> 1.2.3-1
- updated with upstream release from Aleksey
* Wed Nov 12 2003 Daniel Veillard <veillard@redhat.com> 1.2.2-1
- updated with upstream release from Aleksey, specific patches should
  have been integrated now.
* Thu Nov  6 2003 Daniel Veillard <veillard@redhat.com> 1.2.1-1
- initial packaging based on the upstream one and libxml2 one.
- desactivated mozilla-nss due to detection/architecture problems
