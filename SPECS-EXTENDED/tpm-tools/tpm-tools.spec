Name:             tpm-tools
Summary:          Management tools for the TPM hardware
Version:          1.3.9
Release:          9%{?dist}
License:          CPL
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:              http://trousers.sourceforge.net
Source0:          http://downloads.sourceforge.net/trousers/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:    trousers-devel openssl-devel opencryptoki-devel
Patch0001:        0001-Fix-build-with-OpenSSL-1.1-due-to-EVP_PKEY-being-an-.patch
Patch0002:        0002-Fix-build-with-OpenSSL-1.1-due-to-RSA-being-an-opaqu.patch
Patch0003:        0003-Allocate-OpenSSL-cipher-contexts-for-seal-unseal.patch

%description
tpm-tools is a group of tools to manage and utilize the Trusted Computing
Group's TPM hardware. TPM hardware can create, store and use RSA keys
securely (without ever being exposed in memory), verify a platform's
software state using cryptographic hashes and more.

%package        pkcs11
Summary:        Management tools using PKCS#11 for the TPM hardware
# opencryptoki is dlopen'd, the Requires won't get picked up automatically
Requires:       opencryptoki-libs%{?_isa}

%description    pkcs11
tpm-tools-pkcs11 is a group of tools that use the TPM PKCS#11 token. All data
contained in the PKCS#11 data store is protected by the TPM (keys,
certificates, etc.). You can import keys and certificates, list out the
objects in the data store, and protect data.

%package        devel
Summary:        Files to use the library routines supplied with tpm-tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
tpm-tools-devel is a package that contains the libraries and headers necessary
for developing tpm-tools applications.

%prep
%autosetup -p1 -c %{name}-%{version}

%build
%configure --disable-static --disable-rpath --disable-silent-rules
%make_build

%install
%make_install INSTALL="install -p"
rm -f $RPM_BUILD_ROOT/%{_libdir}/libtpm_unseal.la

%ldconfig_scriptlets

%files
%license LICENSE
%doc README
%{_bindir}/tpm_*
%{_sbindir}/tpm_*
%{_libdir}/libtpm_unseal.so.?.?.?
%{_libdir}/libtpm_unseal.so.?
%{_mandir}/man1/tpm_*
%{_mandir}/man8/tpm_*

%files pkcs11
%license LICENSE
%{_bindir}/tpmtoken_*
%{_mandir}/man1/tpmtoken_*

%files devel
%{_libdir}/libtpm_unseal.so
%{_includedir}/tpm_tools/
%{_mandir}/man3/tpmUnseal*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.9-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 20 2017 Michal Schmidt <mschmidt@redhat.com> - 1.3.9-1
- Upstream release 1.3.9.
- Add fixes for build errors with OpenSSL 1.1.
- Add fixes for NULL cipher context use in seal/unseal.
- spec file modernization.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Michal Schmidt <mschmidt@redhat.com> - 1.3.8-6
- Fix FTBFS with current autotools (#1083627)
- Drop tpm-tools-1.3.7-build.patch, the package builds without it (#952372)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.8-2
- Cleanup spec and modernise spec

* Fri Jun 22 2012 Steve Grubb <sgrubb@redhat.com> 1.3.8-1
- New upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 19 2011 Steve Grubb <sgrubb@redhat.com> 1.3.7-1
- New upstream release

* Fri Jun 24 2011 Steve Grubb <sgrubb@redhat.com> 1.3.5-5
- Remove -Werror from compile flags (#716046)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Michal Schmidt <mschmidt@redhat.com> - 1.3.5-3
- Add the LICENSE file to the -pkcs11 subpackage too, as it may be
  installed independently.
- Remove useless macros.

* Sun Feb 14 2010 Michal Schmidt <mschmidt@redhat.com> - 1.3.5-2
- Fix for DSO linking change.

* Mon Feb 01 2010 Steve Grubb <sgrubb@redhat.com> 1.3.5-1
- New upstream bug fix release

* Fri Jan 29 2010 Steve Grubb <sgrubb@redhat.com> 1.3.4-2
- Remove rpaths

* Wed Oct 21 2009 Michal Schmidt <mschmidt@redhat.com> - 1.3.4-1
- Upstream release 1.3.4:
  - adds SRK password support on unsealing
- LICENSE is back.
- Remove no longer needed patch:
  tpm-tools-1.3.3-check-fwrite-success.patch

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.3-2
- rebuilt with new openssl

* Fri Aug 07 2009 Michal Schmidt <mschmidt@redhat.com> 1.3.3-1
- New upstream release 1.3.3.
- No longer needed patch, dropped:
  tpm-tools-conditionally-build-tpmtoken-manpages-Makefile.in.patch
- Use global instead of define for macros.
- Remove rpaths.
- LICENSE file is suddenly missing in upstream tarball.
- Added patch to allow compilation:
  tpm-tools-1.3.3-check-fwrite-success.patch

* Wed Jul 29 2009 Michal Schmidt <mschmidt@redhat.com> 1.3.1-10
- Split the pkcs11 utilities into a subpackage.

* Wed Jul 29 2009 Michal Schmidt <mschmidt@redhat.com> 1.3.1-9
- Enable pkcs11 support (tpmtoken_* utilities).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.1-6
- rebuild with new openssl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.1-5
- Autorebuild for GCC 4.3

* Tue Dec 18 2007 Kent Yoder <kyoder@users.sf.net> - 1.3.1-4
- Updated for comments in RHIT#394941 comment #6
* Fri Dec 14 2007 Kent Yoder <kyoder@users.sf.net> - 1.3.1-3
- Updated to own the includedir/tpm_tools directory, removed
requirement on trousers and ldconfig in post/postun
* Thu Dec 13 2007 Kent Yoder <kyoder@users.sf.net> - 1.3.1-2
- Updated for Fedora package submission guidelines
* Fri Nov 16 2007 Kent Yoder <kyoder@users.sf.net> - 1.3.1
- Updates to configure
* Fri Oct 05 2007 Kent Yoder <kyoder@users.sf.net> - 1.2.5.1
- Updated build section to use smp_mflags

