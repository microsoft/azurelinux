Name: opencryptoki
Summary: Implementation of the PKCS#11 (Cryptoki) specification v3.0
Version: 3.24.0
Release: 3%{?dist}
License: CPL-1.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://github.com/opencryptoki/opencryptoki
Source0: https://github.com/opencryptoki/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1: opencryptoki.module
# fix install problem in buildroot
Patch1: opencryptoki-3.24.0-p11sak.patch
# upstream patches
Patch2: opencryptoki-3.24.0-compile-error-due-to-incompatible-pointer-types.patch

Requires(pre): coreutils
Requires: (selinux-policy >= 34.9-1 if selinux-policy-targeted)
BuildRequires: gcc gcc-c++
BuildRequires: openssl-devel >= 1.1.1
%if 0%{?tmptok}
BuildRequires: trousers-devel
%endif
BuildRequires: openldap-devel
BuildRequires: autoconf automake libtool
BuildRequires: bison flex
BuildRequires: libcap-devel
BuildRequires: expect
BuildRequires: make
BuildRequires: systemd-rpm-macros
%ifarch s390 s390x
BuildRequires: libica-devel >= 3.3
# for /usr/include/libudev.h
BuildRequires: systemd-devel
%endif
Requires(pre): %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}(token)
Requires(post): systemd diffutils
Requires(preun): systemd
Requires(postun): systemd

%description
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package contains the Slot Daemon (pkcsslotd) and general utilities.


%package libs
Summary: The run-time libraries for opencryptoki package
Requires(pre): shadow-utils

%description libs
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package contains the PKCS#11 library implementation, and requires
at least one token implementation (packaged separately) to be fully
functional.


%package devel
Summary: Development files for openCryptoki
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the development header files for building
opencryptoki and PKCS#11 based applications


%package swtok
Summary: The software token implementation for opencryptoki
Requires(pre): %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{name}(token)

%description swtok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the software token implementation to use opencryptoki
without any specific cryptographic hardware.


%package tpmtok
Summary: Trusted Platform Module (TPM) device support for opencryptoki
Requires(pre): %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{name}(token)

%description tpmtok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support
Trusted Platform Module (TPM) devices in the opencryptoki stack.


%package icsftok
Summary: ICSF token support for opencryptoki
Requires(pre): %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{name}(token)

%description icsftok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support
ICSF token in the opencryptoki stack.


%package icatok
Summary: ICA cryptographic devices (clear-key) support for opencryptoki
Requires(pre): %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{name}(token)

%description icatok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support ICA
devices in the opencryptoki stack. ICA is an interface to IBM
cryptographic hardware such as IBM 4764 or 4765 that uses the
"accelerator" or "clear-key" path.

%package ccatok
Summary: CCA cryptographic devices (secure-key) support for opencryptoki
Requires(pre): %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{name}(token)

%description ccatok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support CCA
devices in the opencryptoki stack. CCA is an interface to IBM
cryptographic hardware such as IBM 4764 or 4765 that uses the
"co-processor" or "secure-key" path.

%package ep11tok
Summary: EP11 cryptographic devices (secure-key) support for opencryptoki
Requires(pre): %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{name}(token)

%description ep11tok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support EP11
tokens in the opencryptoki stack. The EP11 token is a token that uses
the IBM Crypto Express adapters (starting with Crypto Express 4S adapters)
configured with Enterprise PKCS#11 (EP11) firmware.


%prep
%autosetup -p1


%build
./bootstrap.sh

%configure --with-systemd=%{_unitdir} --enable-testcases	\
    --with-pkcsslotd-user=pkcsslotd --with-pkcs-group=pkcs11 \
%if 0%{?tpmtok}
    --enable-tpmtok \
%else
    --disable-tpmtok \
%endif
%ifarch s390 s390x x86_64 ppc64le
    --enable-ccatok \
%else
    --disable-ccatok \
%endif
%ifarch s390 s390x
    --enable-icatok --enable-ep11tok --enable-pkcsep11_migrate
%else
    --disable-icatok --disable-ep11tok --disable-pkcsep11_migrate --enable-pkcscca_migrate
%endif

%make_build CHGRP=/bin/true


%install
%make_install CHGRP=/bin/true


%pre
# don't touch opencryptoki.conf even if it is unchanged due to new tokversion
# backup config file. bz#2044179
%global cfile /etc/opencryptoki/opencryptoki.conf
%global csuffix .rpmsave.XyoP
if test $1 -gt 1 && test -f %{cfile} ; then
    cp -p %{cfile} %{cfile}%{csuffix}
fi

%pre libs
getent group pkcs11 >/dev/null || groupadd -r pkcs11
getent passwd pkcsslotd >/dev/null || useradd -r -g pkcs11 -d /run/opencryptoki -s /sbin/nologin -c "Opencryptoki pkcsslotd user" pkcsslotd
exit 0

%post
# restore the config file from %pre
if test $1 -gt 1 && test -f %{cfile} ; then
    if ( ! cmp -s %{cfile} %{cfile}%{csuffix} ) ; then
        cp -p %{cfile} %{cfile}.rpmnew
    fi
    cp -p %{cfile}%{csuffix} %{cfile} && rm -f %{cfile}%{csuffix}
fi

%systemd_post pkcsslotd.service
if test $1 -eq 1; then
	%tmpfiles_create %{name}.conf
fi

%preun
%systemd_preun pkcsslotd.service

%postun
%systemd_postun_with_restart pkcsslotd.service


%files
%doc ChangeLog FAQ README.md
%doc doc/opencryptoki-howto.md
%doc doc/README.token_data
%doc %{_docdir}/%{name}/*.conf
%dir %{_sysconfdir}/%{name}
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0640, root, pkcs11) %config(noreplace) %{_sysconfdir}/%{name}/p11sak_defined_attrs.conf
%attr(0640, root, pkcs11) %config(noreplace) %{_sysconfdir}/%{name}/strength.conf
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/pkcsslotd.service
%{_sbindir}/p11sak
%{_sbindir}/pkcstok_migrate
%{_sbindir}/pkcsconf
%{_sbindir}/pkcsslotd
%{_sbindir}/pkcsstats
%{_sbindir}/pkcshsm_mk_change
%{_sbindir}/pkcstok_admin
%{_mandir}/man1/p11sak.1*
%{_mandir}/man1/pkcstok_migrate.1*
%{_mandir}/man1/pkcsconf.1*
%{_mandir}/man1/pkcsstats.1*
%{_mandir}/man1/pkcshsm_mk_change.1*
%{_mandir}/man1/pkcstok_admin.1*
%{_mandir}/man5/policy.conf.5*
%{_mandir}/man5/strength.conf.5*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man5/p11sak_defined_attrs.conf.5*
%{_mandir}/man7/%{name}.7*
%{_mandir}/man8/pkcsslotd.8*
%{_libdir}/opencryptoki/methods
%{_libdir}/pkcs11/methods
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/HSM_MK_CHANGE
%ghost %dir %attr(770,root,pkcs11) %{_rundir}/lock/%{name}
%ghost %dir %attr(770,root,pkcs11) %{_rundir}/lock/%{name}/*
%dir %attr(710,pkcsslotd,pkcs11) /run/%{name}

%files libs
%license LICENSE
%{_sysconfdir}/ld.so.conf.d/*
# Unversioned .so symlinks usually belong to -devel packages, but opencryptoki
# needs them in the main package, because:
#   documentation suggests that programs should dlopen "PKCS11_API.so".
%dir %{_libdir}/opencryptoki
%{_libdir}/opencryptoki/libopencryptoki.*
%{_libdir}/opencryptoki/PKCS11_API.so
%dir %{_libdir}/opencryptoki/stdll
%dir %{_libdir}/pkcs11
%{_libdir}/pkcs11/libopencryptoki.so
%{_libdir}/pkcs11/PKCS11_API.so
%{_libdir}/pkcs11/stdll
%dir %attr(770,root,pkcs11) %{_localstatedir}/log/opencryptoki

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc

%files swtok
%{_libdir}/opencryptoki/stdll/libpkcs11_sw.*
%{_libdir}/opencryptoki/stdll/PKCS11_SW.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/swtok/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/swtok/TOK_OBJ/

%if 0%{?tmptok}
%files tpmtok
%doc doc/README.tpm_stdll
%{_libdir}/opencryptoki/stdll/libpkcs11_tpm.*
%{_libdir}/opencryptoki/stdll/PKCS11_TPM.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/tpm/
%endif

%files icsftok
%doc doc/README.icsf_stdll
%{_sbindir}/pkcsicsf
%{_mandir}/man1/pkcsicsf.1*
%{_libdir}/opencryptoki/stdll/libpkcs11_icsf.*
%{_libdir}/opencryptoki/stdll/PKCS11_ICSF.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/icsf/

%ifarch x86_64
%files ccatok
%doc doc/README.cca_stdll
%config(noreplace) %{_sysconfdir}/%{name}/ccatok.conf
%{_sbindir}/pkcscca
%{_mandir}/man1/pkcscca.1*
%{_libdir}/opencryptoki/stdll/libpkcs11_cca.*
%{_libdir}/opencryptoki/stdll/PKCS11_CCA.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ccatok/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ccatok/TOK_OBJ/
%endif

%changelog
* Wed Jan 15 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 3.24.0-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Sep 13 2024 Than Ngo <than@redhat.com> - 3.24.0-2
- build with --enable-pkcscca_migrate
- fix build error due to incompatible pointer types

* Fri Sep 13 2024 Than Ngo <than@redhat.com> - 3.24.0-1
- Update to 3.24.0
  * Add support for building Opencryptoki on the IBM AIX platform
  * Add support for the CCA token on non-IBM Z platforms (x86_64, ppc64)
  * Add support for protecting tokens with a token specific user group
  * EP11: Add support for combined CKA_EXTRACTABLE and CKA_IBM_PROTKEY_EXTRACTABLE
  * CCA: Add support for Koblitz curve secp256k1. Requires CCA v7.2 or later
  * CCA: Add support for IBM Dilithium (CKM_IBM_DILITHIUM).
    On Linux on IBM Z: Requires CCA v7.1 or later for Round2-65, and CCA v8.0 for the Round 3 variants.
    On other platforms: Requires CCA v7.2.43 or later for Round2-65, the Round 3 variants are currently not supported
  * CCA: Add support for RSA-OAEP with SHA224, SHA384, and SHA512 on en-/decrypt. Requires CCA v8.1 or later on Linux on IBM Z, not supported on other platforms
  * CCA: Add support for PKCS#11 v3.0 SHA3 mechanisms. Requires CCA v8.1 on Linux on IBM Z, not supported on other platforms
  * ICA: Support new libica AES-GCM api using the KMA instruction on z14 and later
  * ICA/Soft/ICSF: Add support for PKCS#11 v3.0 SHA3 mechanisms
  * ICA/Soft: Add support for SHA based key derivation mechanisms
  * ICA/Soft: Add support for CKD_*_SP800 KDFs for ECDH
  * EP11/CCA/ICA/Soft: Add support for CKA_ALWAYS_AUTHENTICATE
  * EP11/CCA: Support live guest relocation for protected key (PKEY) operations
  * Soft: Experimental support for IBM Dilithium via OpenSSL OQS provider
  * ICSF: Add support for SHA-2 mechanisms
  * ICSF: Performance improvements for attribute retrieval
  * p11sak: Add support for exporting a key or certificate as URI-PEM file
  * p11sak: Import/export of IBM Dilithium keys in 'oqsprovider' format PEM files
  * p11sak: Add option to show the master key verification patterns of secure keys
  * Bug fixes
- Remove i686 support as upsrtream will get rid of 32-bit support, https://github.com/opencryptoki/opencryptoki/issues/174
- Remove lockdir.patch

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Feb 07 2024 Than Ngo <than@redhat.com> - 3.23.0-1
- 3.23.0
   * EP11: Add support for FIPS-session mode
   * Updates to harden against RSA timing attacks
   * Bug fixes

* Tue Jan 30 2024 Dan Horák <dan[at]danny.cz> - 3.22.0-4
- fix all errors and warnings (rhbz#2261419)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 21 2023 Than Ngo <than@redhat.com> - 3.22.0-1
- update to 3.22.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.21.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Than Ngo <than@redhat.com> - 3.21.0-5
- p11sak tool: slot option does not accept argument 0 for slot index 0
- p11sak fails as soon as there reside non-key objects

* Thu May 25 2023 Than Ngo <than@redhat.com> - 3.21.0-4
- add verify attributes for opencryptoki.conf to ignore the
  verification 

* Mon May 22 2023 Than Ngo <than@redhat.com> - 3.21.0-3
- drop p11_kit_support
- fix handling of user name
- fix user confirmation prompt behavior when stdin is closed

* Tue May 16 2023 Than Ngo <than@redhat.com> - 3.21.0-2
- add missing /var/lib/opencryptoki/HSM_MK_CHANGE 

* Mon May 15 2023 Than Ngo <than@redhat.com> - 3.21.0-1
- update to 3.21.0

* Tue Feb 14 2023 Than Ngo <than@redhat.com> - 3.20.0-2
- migrated to SPDX license

* Mon Feb 13 2023 Than Ngo <than@redhat.com> - 3.20.0-1
- update to 3.20.0
- drop unnecessary opencryptoki-3.11.0-group.patch

* Wed Feb 08 2023 Than Ngo <than@redhat.com> - 3.19.0-3
- Add support of ep11 token for new IBM Z Hardware (IBM z16)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 11 2022 Than Ngo <than@redhat.com> - 3.19.0-1
- update to 3.19.0

* Wed Sep 14 2022 Florian Weimer <fweimer@redhat.com> - 3.18.0-5
- Add missing build dependency on systemd-rpm-macros

* Mon Aug 01 2022 Than Ngo <than@redhat.com> - 3.18.0-4
- fix json output
- do not touch opencryptoki.conf if it is in place already and even if it is unchanged

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 09 2022 Than Ngo <than@redhat.com> - 3.18.0-2
- add missing strength.conf

* Mon May 02 2022 Than Ngo <than@redhat.com> - 3.18.0-1
- 3.18.0

* Wed Apr 20 2022 Dan Horák <dan[at]danny.cz> - 3.17.0-7
- fix initialization (#2075851, #2074587)

* Wed Apr 06 2022 Than Ngo <than@redhat.com> - 3.17.0-6
- add tokversion

* Wed Apr 06 2022 Than Ngo <than@redhat.com> - 3.17.0-5
- upstream fixes - openssl cleanup for opencryptoki, Avoid deadlock when stopping event thread

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 25 2021 Than Ngo <than@redhat.com> - 3.17.0-3
- fix covscan issues

* Tue Nov 09 2021 Than Ngo <than@redhat.com> - 3.17.0-2
- add missing config file p11sak_defined_attrs.conf

* Tue Oct 19 2021 Than Ngo <than@redhat.com> - 3.17.0-1
- rebase to 3.17.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.16.0-5
- Rebuilt with OpenSSL 3.0.0

* Fri Sep 03 2021 Than Ngo <than@redhat.com> - 3.16.0-4
- Resolves: #1987186, pkcstok_migrate leaves options with multiple strings in opencryptoki.conf options without double-quotes
- Resolves: #1974365, Fix detection if pkcsslotd is still running

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Than Ngo <than@redhat.com> - 3.16.0-2
- Added Event Notification Support
- Added conditional requirement on selinux-policy  >= 34.10-1
- pkcsslotd PIDfile below legacy directory
- Added BR on systemd-devel

* Wed Mar 31 2021 Dan Horák <dan[at]danny.cz> - 3.16.0-1
- Rebase to 3.16.0

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.15.1-6
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Fri Feb 12 2021 Than Ngo <than@redhat.com> - 3.15.1-5
- Added upstream patch, a slot ID has nothing to do with the number of slots

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 22 2020 Than Ngo <than@redhat.com> - 3.15.1-3
- Drop tpm1.2 support by default

* Tue Dec 22 2020 Than Ngo <than@redhat.com> - 3.15.1-2
- Fix compiling with c++
- Added error message handling for p11sak remove-key command
- Add BR on make

* Mon Nov 02 2020 Than Ngo <than@redhat.com> - 3.15.1-1
- Rebase to 3.15.1

* Mon Oct 19 2020 Dan Horák <dan[at]danny.cz> - 3.15.0-1
- Rebase to 3.15.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 3.14.0-5
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jul 08 2020 Than Ngo <than@redhat.com> - 3.14.0-4
- added PIN conversion tool

* Wed Jul 01 2020 Than Ngo <than@redhat.com> - 3.14.0-3
- upstream fix - handle early error cases in C_Initialize

* Wed May 27 2020 Than Ngo <than@redhat.com> - 3.14.0-2
- fix regression, segfault in C_SetPin

* Fri May 15 2020 Dan Horák <dan[at]danny.cz> - 3.14.0-1
- Rebase to 3.14.0

* Fri Mar 06 2020 Dan Horák <dan[at]danny.cz> - 3.13.0-1
- Rebase to 3.13.0

* Mon Feb 03 2020 Dan Horák <dan[at]danny.cz> - 3.12.1-3
- fix build with gcc 10

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Dan Horák <dan[at]danny.cz> - 3.12.1-1
- Rebase to 3.12.1

* Wed Nov 13 2019 Dan Horák <dan[at]danny.cz> - 3.12.0-1
- Rebase to 3.12.0

* Sun Sep 22 2019 Dan Horák <dan[at]danny.cz> - 3.11.1-1
- Rebase to 3.11.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Than Ngo <than@redhat.com> - 3.11.0-4
- enable testcase by default
- fix URL

* Tue Feb 19 2019 Than Ngo <than@redhat.com> - 3.11.0-3
- Resolved #1063763 - opencryptoki tools should inform the user that he is not in pkcs11 group

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 31 2019 Than Ngo <than@redhat.com> - 3.11.0-1
- Updated to 3.11.0
- Resolved #1341079 - Failed to create directory or subvolume "/var/lock/opencryptoki"
- Ported root's group membership's patch for 3.11.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Dan Horák <dan[at]danny.cz> - 3.10.0-1
- Rebase to 3.10.0

* Fri Feb 23 2018 Dan Horák <dan[at]danny.cz> - 3.9.0-1
- Rebase to 3.9.0

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 24 2017 Dan Horák <dan[at]danny.cz> - 3.8.2-2
- use upstream tmpfiles config

* Thu Nov 23 2017 Dan Horák <dan[at]danny.cz> - 3.8.2-1
- Rebase to 3.8.2 (#1512678)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Sinny Kumari <sinny@redhat.com> - 3.7.0-1
- Rebase to 3.7.0
- Added libitm-devel as BuildRequires

* Mon Apr 03 2017 Sinny Kumari <sinny@redhat.com> - 3.6.2-1
- Rebase to 3.6.2
- RHBZ#1424017 - opencryptoki: FTBFS in rawhide

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 01 2016 Jakub Jelen <jjelen@redhat.com> - 3.5.1-1
- New upstream release

* Tue May 03 2016 Jakub Jelen <jjelen@redhat.com> - 3.5-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 07 2015 Jakub Jelen <jjelen@redhat.com> 3.4.1-1
- New bugfix upstream release

* Wed Nov 18 2015 Jakub Jelen <jjelen@redhat.com> 3.4-1
- New upstream release
- Adding post-release patch fixing compile warnings

* Thu Aug 27 2015 Jakub Jelen <jjelen@redhat.com> 3.3-1.1
- New upstream release
- Correct dependencies for group creation

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 Jakub Jelen <jjelen@redhat.com> 3.2-3
- Few more undefined symbols fixed for s390(x) specific targets
- Do not require --no-undefined, because s390(x) requires some

* Mon May 04 2015 Jakub Jelen <jjelen@redhat.com> 3.2-2
- Fix missing sources and libraries in makefiles causing undefined symbols (#1193560)
- Make inline function compatible for GCC5

* Wed Sep 10 2014 Petr Lautrbach <plautrba@redhat.com> 3.2-1
- new upstream release 3.2
- add new sub-package opencryptoki-ep11tok on s390x

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Petr Lautrbach <plautrba@redhat.com> 3.1-1
- new upstream release 3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 17 2014 Petr Lautrbach <plautrba@redhat.com> 3.0-10
- create the right lock directory for cca tokens (#1054442)

* Wed Jan 29 2014 Petr Lautrbach <plautrba@redhat.com> 3.0-9
- use Requires(pre): opencryptoki-libs for subpackages

* Mon Jan 20 2014 Dan Horák <dan[at]danny.cz> - 3.0-8
- include token specific directories (#1013017, #1045775, #1054442)
- fix pkcsconf crash for non-root users (#10054661)
- the libs subpackage must care of creating the pkcs11 group, it's the first to be installed

* Tue Dec 03 2013 Dan Horák <dan[at]danny.cz> - 3.0-7
- fix build with -Werror=format-security (#1037228)

* Fri Nov 22 2013 Dan Horák <dan[at]danny.cz> - 3.0-6
- apply post-3.0 fixes (#1033284)

* Tue Nov 19 2013 Dan Horák <dan[at]danny.cz> - 3.0-5
- update opencryptoki man page (#1001729)

* Fri Aug 23 2013 Dan Horák <dan[at]danny.cz> - 3.0-4
- update unit file (#995002)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Dan Horák <dan[at]danny.cz> - 3.0-2
- update pkcsconf man page (#948460)

* Mon Jul 22 2013 Dan Horák <dan[at]danny.cz> - 3.0-1
- new upstream release 3.0

* Tue Jun 25 2013 Dan Horák <dan[at]danny.cz> - 2.4.3.1-1
- new upstream release 2.4.3.1

* Fri May 03 2013 Dan Horák <dan[at]danny.cz> - 2.4.3-1
- new upstream release 2.4.3

* Thu Apr 04 2013 Dan Horák <dan[at]danny.cz> - 2.4.2-4
- enable hardened build
- switch to systemd macros in scriptlets (#850240)

* Mon Jan 28 2013 Dan Horák <dan[at]danny.cz> - 2.4.2-3
- add virtual opencryptoki(token) Provides to token modules and as Requires
  to main package (#904986)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Dan Horák <dan[at]danny.cz> - 2.4.2-1
- new upstream release 2.4.2
- add pkcs_slot man page
- don't add root to the pkcs11 group

* Mon Jun 11 2012 Dan Horák <dan[at]danny.cz> - 2.4.1-2
- fix unresolved symbols in TPM module (#830129)

* Sat Feb 25 2012 Dan Horák <dan[at]danny.cz> - 2.4.1-1
- new upstream release 2.4.1
- convert from initscript to systemd unit
- import fixes from RHEL-6 about root's group membership (#732756, #730903)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 07 2011 Dan Horák <dan[at]danny.cz> - 2.4-1
- new upstream release 2.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Dan Horák <dan[at]danny.cz> 2.3.3-1
- new upstream release 2.3.3

* Tue Nov 09 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.2-2
- Apply Obsoletes to package names, not provides.

* Tue Sep 14 2010 Dan Horák <dan[at]danny.cz> 2.3.2-1
- new upstream release 2.3.2
- put STDLLs in separate packages to match upstream package design

* Thu Jul 08 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.1-7
- Move the LICENSE file to the -libs subpackage.

* Tue Jun 29 2010 Dan Horák <dan[at]danny.cz> 2.3.1-6
- rebuilt with CCA enabled (#604287)
- fixed issues from #546274

* Fri Apr 30 2010 Dan Horák <dan[at]danny.cz> 2.3.1-5
- fixed one more issue in the initscript (#547324)

* Mon Apr 26 2010 Dan Horák <dan[at]danny.cz> 2.3.1-4
- fixed pidfile creating and usage (#547324)

* Mon Feb 08 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.1-3
- Also list 'reload' and 'force-reload' in "Usage: ...".

* Mon Feb 08 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.1-2
- Support 'force-reload' in the initscript.

* Wed Jan 27 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.1-1
- New upstream release 2.3.1.
- opencryptoki-2.3.0-fix-nss-breakage.patch was merged.

* Fri Jan 22 2010 Dan Horák <dan[at]danny.cz> 2.3.0-5
- made pkcsslotd initscript LSB compliant (#522149)

* Mon Sep 07 2009 Michal Schmidt <mschmidt@redhat.com> 2.3.0-4
- Added opencryptoki-2.3.0-fix-nss-breakage.patch on upstream request.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.3.0-3
- rebuilt with new openssl

* Sun Aug 16 2009 Michal Schmidt <mschmidt@redhat.com> 2.3.0-2
- Require libica-2.0.

* Fri Aug 07 2009 Michal Schmidt <mschmidt@redhat.com> 2.3.0-1
- New upstream release 2.3.0:
  - adds support for RSA 4096 bit keys in the ICA token.

* Tue Jul 21 2009 Michal Schmidt <mschmidt@redhat.com> - 2.2.8-5
- Require arch-specific dependency on -libs.

* Tue Jul 21 2009 Michal Schmidt <mschmidt@redhat.com> - 2.2.8-4
- Return support for crypto hw on s390.
- Renamed to opencryptoki.
- Simplified multilib by putting libs in subpackage as suggested by Dan Horák.

* Tue Jul 21 2009 Michal Schmidt <mschmidt@redhat.com> - 2.2.8-2
- Fedora package based on RHEL-5 package.
