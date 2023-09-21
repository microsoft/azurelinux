Summary:        Implementation of the PKCS#11 (Cryptoki) specification v2.11
Name:           opencryptoki
Version:        3.17.0
Release:        1%{?dist}
License:        CPL
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/opencryptoki/opencryptoki
Source0:        https://github.com/opencryptoki/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        opencryptoki.module
# https://bugzilla.redhat.com/show_bug.cgi?id=732756
Patch0:         opencryptoki-3.11.0-group.patch
# bz#1373833, change tmpfiles snippets from /var/lock/* to /run/lock/*
Patch1:         opencryptoki-3.11.0-lockdir.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  expect
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  trousers-devel
Requires:       %{name}(token)
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires(post): systemd
Requires(postun): systemd
Requires(pre):  %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):  coreutils
Requires(preun): systemd
%ifarch s390 s390x
BuildRequires:  libica-devel >= 2.3
%endif

%description
Opencryptoki implements the PKCS#11 specification v2.11 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package contains the Slot Daemon (pkcsslotd) and general utilities.

%package libs
Summary:        The run-time libraries for opencryptoki package
Requires(pre):  shadow-utils

%description libs
Opencryptoki implements the PKCS#11 specification v2.11 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package contains the PKCS#11 library implementation, and requires
at least one token implementation (packaged separately) to be fully
functional.

%package devel
Summary:        Development files for openCryptoki
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the development header files for building
opencryptoki and PKCS#11 based applications

%package swtok
Summary:        The software token implementation for opencryptoki
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):  %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       %{name}(token)

%description swtok
Opencryptoki implements the PKCS#11 specification v2.11 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the software token implementation to use opencryptoki
without any specific cryptographic hardware.

%package tpmtok
Summary:        Trusted Platform Module (TPM) device support for opencryptoki
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):  %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       %{name}(token)

%description tpmtok
Opencryptoki implements the PKCS#11 specification v2.11 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support
Trusted Platform Module (TPM) devices in the opencryptoki stack.

%package icsftok
Summary:        ICSF token support for opencryptoki
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):  %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       %{name}(token)

%description icsftok
Opencryptoki implements the PKCS#11 specification v2.11 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support
ICSF token in the opencryptoki stack.

%ifarch s390 s390x
%package icatok
Summary:        ICA cryptographic devices (clear-key) support for opencryptoki
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):  %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       %{name}(token)

%description icatok
Opencryptoki implements the PKCS#11 specification v2.11 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support ICA
devices in the opencryptoki stack. ICA is an interface to IBM
cryptographic hardware such as IBM 4764 or 4765 that uses the
"accelerator" or "clear-key" path.

%package ccatok
Summary:        CCA cryptographic devices (secure-key) support for opencryptoki
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):  %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       %{name}(token)

%description ccatok
Opencryptoki implements the PKCS#11 specification v2.11 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support CCA
devices in the opencryptoki stack. CCA is an interface to IBM
cryptographic hardware such as IBM 4764 or 4765 that uses the
"co-processor" or "secure-key" path.

%package ep11tok
Summary:        CCA cryptographic devices (secure-key) support for opencryptoki
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):  %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       %{name}(token)

%description ep11tok
Opencryptoki implements the PKCS#11 specification v2.11 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support EP11
tokens in the opencryptoki stack. The EP11 token is a token that uses
the IBM Crypto Express adapters (starting with Crypto Express 4S adapters)
configured with Enterprise PKCS#11 (EP11) firmware.
%endif


%prep
%autosetup -p1


%build
./bootstrap.sh

%configure --with-systemd=%{_unitdir} --enable-testcases	\
%ifarch s390 s390x
    --enable-icatok --enable-ccatok --enable-ep11tok --enable-pkcsep11_migrate
%else
    --disable-icatok --disable-ccatok --disable-ep11tok --disable-pkcsep11_migrate
%endif

make %{?_smp_mflags} CHGRP=/bin/true


%install
make install DESTDIR=%{buildroot} CHGRP=/bin/true
install -Dpm 644 %{SOURCE1} %{buildroot}%{_datadir}/p11-kit/modules/opencryptoki.module


%pre libs
getent group pkcs11 >/dev/null || groupadd -r pkcs11
exit 0

%post
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
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/pkcsslotd.service
%{_sbindir}/pkcsconf
%{_sbindir}/pkcsslotd
%{_sbindir}/p11sak
%{_sbindir}/pkcstok_migrate
%{_mandir}/man1/pkcsconf.1*
%{_mandir}/man1/p11sak.1*
%{_mandir}/man1/pkcstok_migrate.1*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man5/p11sak_defined_attrs.conf.5*
%{_mandir}/man7/%{name}.7*
%{_mandir}/man8/pkcsslotd.8*
%{_libdir}/opencryptoki/methods
%{_libdir}/pkcs11/methods
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}
%ghost %dir %attr(770,root,pkcs11) %{_rundir}/lock/%{name}
%ghost %dir %attr(770,root,pkcs11) %{_rundir}/lock/%{name}/*
%dir %attr(770,root,pkcs11) %{_localstatedir}/log/opencryptoki

%files libs
%license LICENSE
%{_sysconfdir}/ld.so.conf.d/*
# Unversioned .so symlinks usually belong to -devel packages, but opencryptoki
# needs them in the main package, because:
# documentation suggests that programs should dlopen "PKCS11_API.so".
%dir %{_libdir}/opencryptoki
%{_libdir}/opencryptoki/libopencryptoki.*
%{_libdir}/opencryptoki/PKCS11_API.so
%dir %{_libdir}/opencryptoki/stdll
%dir %{_libdir}/pkcs11
%{_libdir}/pkcs11/libopencryptoki.so
%{_libdir}/pkcs11/PKCS11_API.so
%{_libdir}/pkcs11/stdll
# Co-owned with p11-kit
%dir %{_datadir}/p11-kit/
%dir %{_datadir}/p11-kit/modules/
%{_datadir}/p11-kit/modules/opencryptoki.module

%files devel
%{_includedir}/%{name}/

%files swtok
%{_libdir}/opencryptoki/stdll/libpkcs11_sw.*
%{_libdir}/opencryptoki/stdll/PKCS11_SW.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/swtok/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/swtok/TOK_OBJ/

%files tpmtok
%doc doc/README.tpm_stdll
%{_libdir}/opencryptoki/stdll/libpkcs11_tpm.*
%{_libdir}/opencryptoki/stdll/PKCS11_TPM.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/tpm/

%files icsftok
%doc doc/README.icsf_stdll
%{_sbindir}/pkcsicsf
%{_mandir}/man1/pkcsicsf.1*
%{_libdir}/opencryptoki/stdll/libpkcs11_icsf.*
%{_libdir}/opencryptoki/stdll/PKCS11_ICSF.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/icsf/

%ifarch s390 s390x
%files icatok
%{_libdir}/opencryptoki/stdll/libpkcs11_ica.*
%{_libdir}/opencryptoki/stdll/PKCS11_ICA.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/lite/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/lite/TOK_OBJ/

%files ccatok
%doc doc/README.cca_stdll
%{_sbindir}/pkcscca
%{_mandir}/man1/pkcscca.1*
%{_libdir}/opencryptoki/stdll/libpkcs11_cca.*
%{_libdir}/opencryptoki/stdll/PKCS11_CCA.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ccatok/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ccatok/TOK_OBJ/

%files ep11tok
%doc doc/README.ep11_stdll
%config(noreplace) %{_sysconfdir}/%{name}/ep11tok.conf
%config(noreplace) %{_sysconfdir}/%{name}/ep11cpfilter.conf
%{_sbindir}/pkcsep11_migrate
%{_sbindir}/pkcsep11_session
%{_mandir}/man1/pkcsep11_migrate.1*
%{_mandir}/man1/pkcsep11_session.1*
%{_libdir}/opencryptoki/stdll/libpkcs11_ep11.*
%{_libdir}/opencryptoki/stdll/PKCS11_EP11.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ep11tok/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ep11tok/TOK_OBJ/
%endif


%changelog
* Mon Sep 04 2023 Muhammad Falak <mwani@microsoft.com> - 3.17.0-1
- Upgrade version to address CVE-2021-3798
- Lint spec
- License verified

* Thu Mar 18 2021 Henry Li <lihl@microsoft.com> - 3.13.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove libitm-devel from build requirement because gcc already includes the necessary binaries it covers

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
