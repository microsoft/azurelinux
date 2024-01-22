Name:           libtpms
Version:        0.9.6
Release:        4%{?dist}
Summary:        Library providing Trusted Platform Module (TPM) functionality
License:        BSD and TCGL

URL:            https://github.com/stefanberger/libtpms
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/v%{version}.tar.gz.asc#/%{name}-%{version}.tar.gz.asc
# https://github.com/stefanberger.gpg
Source2:        gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gawk
BuildRequires:  gcc-c++
BuildRequires:  gnupg2
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  sed

%description
A library providing TPM functionality for VMs. Targeted for integration
into Qemu.

%package        devel
Summary:        Include files for libtpms
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description   devel
Libtpms header files and documentation.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup

%build
NOCONFIGURE=1 ./autogen.sh
%configure --disable-static --with-tpm2 --with-openssl
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.la' -print -delete

%check
make check

%ldconfig_scriptlets

%files
%license LICENSE
%doc README CHANGES
%{_libdir}/%{name}.so.0{,.*}

%files devel
%{_includedir}/%{name}/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/TPM*

%changelog
* Mon Jan 22 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 0.9.6-4
- Initial CBL-Mariner import from Fedora 39.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Stefan Berger <stefanb@linux.ibm.com> - 0.9.6-3
- Set license to 'BSD and TCGL' from previous 'BSD' (BZ2219548)

* Sat Mar 18 2023 Todd Zullinger <tmz@pobox.com> - 0.9.6-2
- verify upstream source signature

* Tue Feb 28 2023 Stefan Berger <stefanb@linux.ibm.com> - 0.9.6-1
- Build of libtpms 0.9.6 with fixes for CVE-2023-1017 & CVE-2023-1018

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 01 2022 Stefan Berger <stefanb@linux.ibm.com> - 0.9.5-1
- Build of libtpms 0.9.5

* Wed Apr 27 2022 Fabio Valentini <decathorpe@gmail.com> - 0.9.4-2
- Use standard method for fetching a GitHub release tarball.
- Fix Versioning scheme to confirm with Packaging Guidelines.
- Tighten file globs to match Packaging Guidelines.

* Mon Apr 25 2022 Stefan Berger <stefanb@linux.ibm.com> - 0.9.4-1.20220425gite4d68670e1
- Build of libtpms 0.9.4

* Mon Mar 07 2022 Stefan Berger <stefanb@linux.ibm.com> - 0.9.3-1.20220307gita63c51805e
- Build of libtpms 0.9.3

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-0.20220106gite81d634c27.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Stefan Berger <stefanb@linux.ibm.com> - 0.9.2-0.20220106gite81d634c27
- Build of libtpms 0.9.2

* Fri Nov 26 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.9.1-0.20211126git1ff6fe1f43
- Build of libtpms 0.9.1

* Mon Oct 04 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.9.0-0.20211004gitdc4e3f6313
- Build of libtpms 0.9.0

* Thu Sep 16 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.7-0.20210916gitfb9f0a61e8
- Build upcoming libtpms 0.8.7

* Wed Sep 15 2021 Sahana Prasad <sahana@redhat.com> - 0.8.6-0.20210910git7a4d46a119.3
- Rebuilt with OpenSSL 3.0.0

* Tue Sep 14 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.6-0.20210910git7a4d46a119.2
- Build with -Wno-deprecated-declarations

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.8.6-0.20210910git7a4d46a119.1
- Rebuilt with OpenSSL 3.0.0

* Fri Sep 10 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.6-1.20210910git7a4d46a119
- tpm2: Marshal event sequence objects' hash state

* Wed Sep 01 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.5-1.20210901git18ba4c0206
- Build of libtpms 0.8.5

* Wed Aug 11 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.4-1.20210625gita594c4692a
- Applied patches resolving issues solved in upcoming 0.8.5

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-0.20210624gita594c4692a.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 24 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.4-0.20210625gita594c4692a
- tpm2: Reset too large size indicators in TPM2B to avoid access beyond buffer
- tpm2: Restore original value in buffer if unmarshalled one was illegal

* Tue Jun 01 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.3-0.20210601git9e736d5281
- tpm2: Work-around for Windows 2016 & 2019 bug related to ContextLoad

* Mon Mar 01 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.2-0.20210301git729fc6a4ca
- tpm2: CryptSym: fix AES output IV; a CVE has been filed for this issue

* Sat Feb 27 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.1-0.20210227git5bf2746e47
- Fixed a context save and suspend/resume problem when public keys are loaded

* Thu Feb 25 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.8.0-0.20210225git3fd4b94903
- Release of v0.8.0

* Thu Feb 18 2021 Stefan Berger <stefanb@linux.ibm.com> - 0.7.5-0.20210218gite271498466
- Addressed UBSAN and cppcheck detected issues
- Return proper size of ECC Parameters to pass HLK tests

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-0.20201031git2452a24dab.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Oct 31 2020 Stefan Berger <stefanb@linux.ibm.com> - 0.7.4-0.20201031git2452a24dab
- Follow stable-0.7.0 branch to v0.7.4 with security-related fixes

* Fri Jul 31 2020 Stefan Berger <stefanb@linux.ibm.com> - 0.7.3-0.20200731git1d392d466a
- Follow stable-0.7.0 branch to v0.7.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-0.20200527git7325acb477.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 27 2020 Stefan Berger <stefanb@linux.ibm.com> - 0.7.2-0.20200527git7325acb477
- Following stable-0.7.0 branch for TPM 2 related fixes: RSA decryption,
  PSS salt length, symmetric decryption (padding)
- Under certain circumstances an RSA decryption could cause a buffer overflow causing
  termination of the program (swtpm)

* Wed May 20 2020 Stefan Berger <stefanb@linux.ibm.com> - 0.7.1-0.20200520git8fe99d1fd0
- Following stable-0.7.0 branch for TPM 2 related fixes; v0.7.1 + gcc related patch
- elliptic curve fixes
- MANUFACTURER changed from "IBM " to "IBM"
- gcc 10 related fix

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-0.20191018gitdc116933b7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Stefan Berger <stefanb@linux.ibm.com> - 0.7.0-0.20191018gitdc116933b7
- Following stable-0.7.0 branch for TPM 1.2 related bugfix

* Tue Oct 08 2019 Stefan Berger <stefanb@linux.ibm.com> - 0.7.0-0.20191008gitc26e8f7b08
- Following stable-0.7.0 branch for bug fix

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-0.20190719gitd061d8065b.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Stefan Berger <stefanb@linux.ibm.com> - 0.7.0-0.20190719gitd061d8065b
- Update to v0.7.0

* Fri May 10 2019 Stefan Berger <stefanb@linux.ibm.com> - 0.6.1-0.20190510gitb244bdf6e2
- Applied bugfix for CMAC

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-0.20190121git9dc915572b.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Stefan Berger <stefanb@linux.ibm.com> - 0.6.1-0.20190121git9dc915572b
- Libtpms was updated to rev. 150 of TPM 2.0 code
- following branch stable-0.6.0

* Tue Dec 11 2018 Stefan Berger <stefanb@linux.ibm.com> - 0.6.0-0.20181211gitba56737b93
- Following bugfixes in libtpms

* Wed Oct 31 2018 Stefan Berger <stefanb@linux.ibm.com> - 0.6.0-0.20181031git0466fcf6a4
- Following improvements in libtpms

* Tue Sep 18 2018 Stefan Berger <stefanb@linux.vnet.ibm.com - 0.6.0-0.20180918gite8e8633089
- Fixed changelog

* Mon Sep 17 2018 Stefan Berger <stefanb@linux.vnet.ibm.com - 0.6.0-0.20180917gite8e8633089
- Build snapshot from git after libtpms fix.

* Fri Sep 14 2018 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.6.0-0.20180914git4111bd1bcf
- Build snapshot from git, simplify spec

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 16 2014 Stefan Berger - 0.5.2-3
- do not include libtpms.la in rpm

* Mon Jul 14 2014 Stefan Berger - 0.5.2-2
- Added patches

* Mon Jun 30 2014 Stefan Berger - 0.5.2-1
- Updated to version 0.5.2
- coverity fixes
- fixes for ARM64 using __aarch64__

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-20.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Stefan Berger - 0.5.1-18
- Ran autoreconf for support of aarch64
- Checking for __arm64__ in code

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.5.1-15
- Add dist tag as required by package guidelines

* Fri Jan 27 2012 Stefan Berger - 0.5.1-14
- fix gcc-4.7 compilation problem

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Dan Horák <dan[at]danny.cz> - 0.5.1-12
- fix build on secondary arches

* Wed Nov 2 2011 Stefan Berger - 0.5.1-11
- added (lib)gmp as runtime dependency

* Sat Oct 8 2011 Stefan Berger - 0.5.1-10
- internal fixes; callback fixes

* Tue Aug 30 2011 Stefan Berger - 0.5.1-9
- new directory structure and build process

* Tue Jul 12 2011 Stefan Berger - 0.5.1-8
- added pkgconfig as build dependency
- enabling __powerpc__ build following Bz 728220

* Wed May 25 2011 Stefan Berger - 0.5.1-7
- increasing NVRAM area space to have enough room for certificates

* Wed May 25 2011 Stefan Berger - 0.5.1-6
- adding libtpms.pc pkg-config file

* Wed Apr 13 2011 Stefan Berger - 0.5.1-5
- adding BuildRequires for nss-softokn-freebl-static
- several libtpms-internal changes around state serialization and 
  deserialization
- fixes to libtpms makefile (makefile-libtpms)
- adding build_type to generate a debug or production build
- need nss-devel to have nss-config

* Tue Mar 08 2011 Stefan Berger - 0.5.1-4
- small fixes to libtpms makefile

* Fri Feb 25 2011 Stefan Berger - 0.5.1-3
- removing release from tar ball name
- Use {?_smp_mflags} for make rather than hardcoding it
- Fixing post and postun scripts; removing the scripts for devel package
- Fixing usage of defattr
- Adding version information into the changelog headers and spaces between the changelog entries
- Adding LICENSE, README and CHANGELOG file into tar ball and main rpm
- Removing clean section
- removed command to clean the build root
- adding library version to the libries required for building and during
  runtime
- Extended Requires in devel package with {?_isa}

* Fri Feb 18 2011 Stefan Berger - 0.5.1-2
- make rpmlint happy by replacing tabs with spaces
- providing a valid URL for the tgz file
- release is now 2 -> 0.5.1-2

* Mon Jan 17 2011 Stefan Berger - 0.5.1-1
- Update version to 0.5.1

* Fri Jan 14 2011 Stefan Berger - 0.5.0-1
- Changes following Fedora review comments

* Thu Dec 2 2010 Stefan Berger
- Small tweaks after reading the FedoreCore packaging requirements

* Tue Nov 16 2010 Stefan Berger
- Created initial version of rpm spec files
- Version of library is now 0.5.0
- Debuginfo rpm is built but empty -- seems to be a known problem
  Check https://bugzilla.redhat.com/show_bug.cgi?id=209316