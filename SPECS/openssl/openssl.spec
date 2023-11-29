%define soversion 3

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 %{mips} ppc ppc64 s390 s390x sparcv9 sparc64 x86_64

%define srpmhash() %{lua:
local files = rpm.expand("%_specdir/openssl.spec")
for i, p in ipairs(patches) do
   files = files.." "..p
end
for i, p in ipairs(sources) do
   files = files.." "..p
end
local sha256sum = assert(io.popen("cat "..files.." 2>/dev/null | sha256sum"))
local hash = sha256sum:read("*a")
sha256sum:close()
print(string.sub(hash, 0, 16))
}

%global _performance_build 1

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl
Version: 3.1.4
Release: 1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source: https://www.openssl.org/source/openssl-%{version}.tar.gz
Source2: Makefile.certificate
Source3: genpatches
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source9: configuration-switch.h
Source10: configuration-prefix.h
Source14: 0025-for-tests.patch
# # Patches exported from source git
# # Aarch64 and ppc64le use lib64
Patch1:   0001-Aarch64-and-ppc64le-use-lib64.patch
# # Use more general default values in openssl.cnf
Patch2:   0002-Use-more-general-default-values-in-openssl.cnf.patch
# # Do not install html docs
Patch3:   0003-Do-not-install-html-docs.patch
# # Override default paths for the CA directory tree
# AZL: NOTE: We do not use crypto-policies, so this patch does not apply.
# Patch4:   0004-Override-default-paths-for-the-CA-directory-tree.patch
# # apps/ca: fix md option help text
Patch5:   0005-apps-ca-fix-md-option-help-text.patch
# # Disable signature verification with totally unsafe hash algorithms
Patch6:   0006-Disable-signature-verification-with-totally-unsafe-h.patch
# # Add support for PROFILE=SYSTEM system default cipherlist
# AZL: NOTE: We do not use crypto-policies, so this patch does not apply.
# Patch7:   0007-Add-support-for-PROFILE-SYSTEM-system-default-cipher.patch
# # Add FIPS_mode() compatibility macro
Patch8:   0008-Add-FIPS_mode-compatibility-macro.patch
# # Add check to see if fips flag is enabled in kernel
Patch9:   0009-Add-Kernel-FIPS-mode-flag-support.patch
# # Instead of replacing ectest.c and ec_curve.c, add the changes as a patch so
# # that new modifications made to these files by upstream are not lost.
Patch10:  0010-Add-changes-to-ectest-and-eccurve.patch
# # remove unsupported EC curves
Patch11:  0011-Remove-EC-curves.patch
# # Disable explicit EC curves
# # https://bugzilla.redhat.com/show_bug.cgi?id=2066412
Patch12:  0012-Disable-explicit-ec.patch
# # Skipped tests from former 0011-Remove-EC-curves.patch
Patch13:  0013-skipped-tests-EC-curves.patch
# # Instructions to load legacy provider in openssl.cnf
# AZL: NOTE: Had to change this patch because of cascading changes from previous AZL note(s)
Patch24:  0024-load-legacy-prov.patch
# # We load FIPS provider and set FIPS properties implicitly
Patch32:  0032-Force-fips.patch
# # Embed HMAC into the fips.so
Patch33:  0033-FIPS-embed-hmac.patch
# # Comment out fipsinstall command-line utility
Patch34:  0034.fipsinstall_disable.patch
# # Skip unavailable algorithms running `openssl speed`
Patch35:  0035-speed-skip-unavailable-dgst.patch
# # Extra public/private key checks required by FIPS-140-3
Patch44:  0044-FIPS-140-3-keychecks.patch
# # Minimize fips services
Patch45:  0045-FIPS-services-minimize.patch
# # Execute KATS before HMAC verification
Patch47:  0047-FIPS-early-KATS.patch
# # Selectively disallow SHA1 signatures rhbz#2070977
# AZL: NOTE: Had to change this patch because of cascading changes from previous AZL note(s)
Patch49:  0049-Allow-disabling-of-SHA1-signatures.patch
# # Support SHA1 in TLS in LEGACY crypto-policy (which is SECLEVEL=1)
Patch52:  0052-Allow-SHA1-in-seclevel-1-if-rh-allow-sha1-signatures.patch
# # https://github.com/openssl/openssl/pull/18103
# # The patch is incorporated in 3.0.3 but we provide this function since 3.0.1
# # so the patch should persist
# AZL: NOTE: Had to change this patch because of cascading changes from previous AZL note(s)
Patch56:  0056-strcasecmp.patch
# # https://bugzilla.redhat.com/show_bug.cgi?id=2053289
Patch58:  0058-FIPS-limit-rsa-encrypt.patch
# # https://bugzilla.redhat.com/show_bug.cgi?id=2087147
Patch61:  0061-Deny-SHA-1-signature-verification-in-FIPS-provider.patch
# 0062-fips-Expose-a-FIPS-indicator.patch
Patch62:  0062-fips-Expose-a-FIPS-indicator.patch
# # https://bugzilla.redhat.com/show_bug.cgi?id=2102535
Patch73:  0073-FIPS-Use-OAEP-in-KATs-support-fixed-OAEP-seed.patch
# [PATCH 29/46] 
#  0074-FIPS-Use-digest_sign-digest_verify-in-self-test.patch
Patch74:  0074-FIPS-Use-digest_sign-digest_verify-in-self-test.patch
# # https://bugzilla.redhat.com/show_bug.cgi?id=2102535
Patch75:  0075-FIPS-Use-FFDHE2048-in-self-test.patch
# # Downstream only. Reseed DRBG using getrandom(GRND_RANDOM)
# # https://bugzilla.redhat.com/show_bug.cgi?id=2102541
Patch76:  0076-FIPS-140-3-DRBG.patch
# # https://bugzilla.redhat.com/show_bug.cgi?id=2102542
Patch77:  0077-FIPS-140-3-zeroization.patch
# # https://bugzilla.redhat.com/show_bug.cgi?id=2114772
Patch78:  0078-Add-FIPS-indicator-parameter-to-HKDF.patch
# # https://github.com/openssl/openssl/pull/13817
Patch79:  0079-RSA-PKCS15-implicit-rejection.patch
# # We believe that some changes present in CentOS are not necessary
# # because ustream has a check for FIPS version
Patch80:  0080-rand-Forbid-truncated-hashes-SHA-3-in-FIPS-prov.patch
# [PATCH 36/46] 
#  0081-signature-Remove-X9.31-padding-from-FIPS-prov.patch
Patch81:  0081-signature-Remove-X9.31-padding-from-FIPS-prov.patch
# [PATCH 37/46] 
#  0083-hmac-Add-explicit-FIPS-indicator-for-key-length.patch
Patch83:  0083-hmac-Add-explicit-FIPS-indicator-for-key-length.patch
# [PATCH 38/46] 
#  0084-pbkdf2-Set-minimum-password-length-of-8-bytes.patch
Patch84:  0084-pbkdf2-Set-minimum-password-length-of-8-bytes.patch
# 0085-FIPS-RSA-disable-shake.patch
Patch85:  0085-FIPS-RSA-disable-shake.patch
# 0088-signature-Add-indicator-for-PSS-salt-length.patch
Patch88:  0088-signature-Add-indicator-for-PSS-salt-length.patch
# 0091-FIPS-RSA-encapsulate.patch
Patch91:  0091-FIPS-RSA-encapsulate.patch
# [PATCH 42/46] 
#  0093-DH-Disable-FIPS-186-4-type-parameters-in-FIPS-mode.patch
Patch93:  0093-DH-Disable-FIPS-186-4-type-parameters-in-FIPS-mode.patch
# [PATCH 43/46] 
#  0110-GCM-Implement-explicit-FIPS-indicator-for-IV-gen.patch
Patch110: 0110-GCM-Implement-explicit-FIPS-indicator-for-IV-gen.patch
# [PATCH 44/46] 
#  0112-pbdkf2-Set-indicator-if-pkcs5-param-disabled-checks.patch
Patch112: 0112-pbdkf2-Set-indicator-if-pkcs5-param-disabled-checks.patch
# 0113-asymciphers-kem-Add-explicit-FIPS-indicator.patch
Patch113: 0113-asymciphers-kem-Add-explicit-FIPS-indicator.patch
# # We believe that some changes present in CentOS are not necessary
# # because ustream has a check for FIPS version
Patch114: 0114-FIPS-enforce-EMS-support.patch

License: Apache-2.0
URL: http://www.openssl.org/

# AZL: NOTE: Removed dependencies we don't have in AZL and that create circular dependencies.
#            Will go through these as I go through patches and config options.
BuildRequires: gcc g++
BuildRequires: coreutils, perl-interpreter, sed, zlib-devel, /usr/bin/cmp
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
BuildRequires: perl(Test::Harness), perl(Test::More), perl(Math::BigInt)
BuildRequires: perl(Module::Load::Conditional), perl(File::Temp)
BuildRequires: perl(Time::HiRes), perl(IPC::Cmd), perl(Pod::Html), perl(Digest::SHA)
BuildRequires: perl(FindBin), perl(lib), perl(File::Compare), perl(File::Copy), perl(bigint)

Requires: perl
Requires: coreutils
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Requires: ca-certificates >= 2008-5
Recommends: openssl-pkcs11%{?_isa}

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:        Libraries for static linking of applications which will use OpenSSL
# Group:          Development/Libraries
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Requires: perl-interpreter
Requires: %{name}%{?_isa} = %{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
	sslflags="no-asm 386"
fi
%endif
%ifarch x86_64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sparcv9
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch sparc64
sslarch=linux64-sparcv9
sslflags=no-asm
%endif
%ifarch alpha alphaev56 alphaev6 alphaev67
sslarch=linux-alpha-gcc
%endif
%ifarch s390 sh3eb sh4eb
sslarch="linux-generic32 -DB_ENDIAN"
%endif
%ifarch s390x
sslarch="linux64-s390x"
%endif
%ifarch %{arm}
sslarch=linux-armv4
%endif
%ifarch aarch64
sslarch=linux-aarch64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sh3 sh4
sslarch=linux-generic32
%endif
%ifarch ppc64 ppc64p7
sslarch=linux-ppc64
%endif
%ifarch ppc64le
sslarch="linux-ppc64le"
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch mips mipsel
sslarch="linux-mips32 -mips32r2"
%endif
%ifarch mips64 mips64el
sslarch="linux64-mips64 -mips64r2"
%endif
%ifarch mips64el
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch riscv64
sslarch=linux-generic64
%endif
ktlsopt=enable-ktls
%ifarch armv7hl
ktlsopt=disable-ktls
%endif

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -Wa,--generate-missing-build-notes=yes -DPURIFY $RPM_LD_FLAGS"

export HASHBANGPERL=/usr/bin/perl

%define fips %{version}-%{srpmhash}
# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} --libdir=lib \
	zlib enable-camellia enable-seed enable-rfc3779 no-sctp \
	enable-cms enable-md2 enable-rc5 ${ktlsopt} enable-fips\
	no-mdc2 no-ec2m no-sm2 no-sm4 enable-buildtest-c++\
	shared  ${sslarch} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\"" -DREDHAT_FIPS_VERSION="\"%{fips}\""'\
	-Wl,--allow-multiple-definition

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

make -s %{?_smp_mflags} all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

%check
# Verify that what was compiled actually works.

#We must disable default provider before tests otherwise they will fail
patch -p1 < %{SOURCE14}

OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
%if 0%{?rhel}
OPENSSL_ENABLE_SHA1_SIGNATURES=
export OPENSSL_ENABLE_SHA1_SIGNATURES
%endif
OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE
#embed HMAC into fips provider for test run
OPENSSL_CONF=/dev/null LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < providers/fips.so > providers/fips.so.hmac
objcopy --update-section .rodata1=providers/fips.so.hmac providers/fips.so providers/fips.so.mac
mv providers/fips.so.mac providers/fips.so
#run tests itself
make test HARNESS_JOBS=8

# Add generation of HMAC checksum of the final stripped library
# We manually copy standard definition of __spec_install_post
# and add hmac calculation/embedding to fips.so
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    OPENSSL_CONF=/dev/null LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so > $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac \
    objcopy --update-section .rodata1=$RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac \
    mv $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so \
    rm $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac \
%{nil}

%define __provides_exclude_from %{_libdir}/openssl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl,%{_pkgdocdir}}
%make_install
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_pkgdocdir}/Makefile.certificate
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_bindir}/make-dummy-cert
install -m755 %{SOURCE7} $RPM_BUILD_ROOT%{_bindir}/renew-dummy-cert

# Move runable perl scripts to bindir
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc/*.pl $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc/tsget $RPM_BUILD_ROOT%{_bindir}

# Rename man pages so that they don't conflict with other system man pages.
pushd $RPM_BUILD_ROOT%{_mandir}
mv man5/config.5ossl man5/openssl.cnf.5
popd

mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA
mkdir -m700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/private
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/certs
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/crl
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/newcerts

# Ensure the config file timestamps are identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/ct_log_list.cnf

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf.dist
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/ct_log_list.cnf.dist
#we don't use native fipsmodule.cnf because FIPS module is loaded automatically
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/fipsmodule.cnf

# Determine which arch opensslconf.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif
%ifarch sparcv9
basearch=sparc
%endif
%ifarch sparc64
basearch=sparc64
%endif

# Next step of gradual disablement of SSL3.
# Make SSL3 disappear to newly built dependencies.
sed -i '/^\#ifndef OPENSSL_NO_SSL_TRACE/i\
#ifndef OPENSSL_NO_SSL3\
# define OPENSSL_NO_SSL3\
#endif' $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h

%ifarch %{multilib_arches}
# Do an configuration.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of opensslconf.h to be usable.
install -m644 %{SOURCE10} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration-${basearch}.h
cat $RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration.h >> \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration-${basearch}.h
install -m644 %{SOURCE9} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration.h
%endif

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc NEWS.md README.md
%{_bindir}/make-dummy-cert
%{_bindir}/renew-dummy-cert
%{_bindir}/openssl
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_pkgdocdir}/Makefile.certificate
%exclude %{_mandir}/man1/*.pl*
%exclude %{_mandir}/man1/tsget*

%files libs
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%config(noreplace) %{_sysconfdir}/pki/tls/ct_log_list.cnf
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%{_libdir}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%{_libdir}/libssl.so.%{soversion}
%attr(0755,root,root) %{_libdir}/engines-%{soversion}
%attr(0755,root,root) %{_libdir}/ossl-modules

%files devel
%doc CHANGES.md doc/dir-locals.example.el doc/openssl-c-indent.el
%{_prefix}/include/openssl
%{_libdir}/*.so
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/*.a

%files perl
%{_bindir}/c_rehash
%{_bindir}/*.pl
%{_bindir}/tsget
%{_mandir}/man1/*.pl*
%{_mandir}/man1/tsget*
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts

%ldconfig_scriptlets libs

%changelog
* Tue Nov 28 2023 Tobias Brick <tobiasb@microsoft.com> - 3.1.4-1
- Upgrade to 3.1.4
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- License verified

* Thu Oct 26 2023 Sahana Prasad <sahana@redhat.com> - 1:3.1.4-1
- Rebase to upstream version 3.1.4

* Thu Oct 19 2023 Sahana Prasad <sahana@redhat.com> - 1:3.1.3-1
- Rebase to upstream version 3.1.3

* Thu Aug 31 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.1.1-4
- Drop duplicated patch and do some contamination

* Tue Aug 22 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.1.1-3
- Integrate FIPS patches from CentOS

* Fri Aug 04 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.1.1-2
- migrated to SPDX license

* Thu Jul 27 2023 Sahana Prasad <sahana@redhat.com> - 1:3.1.1-1
- Rebase to upstream version 3.1.1
  Resolves: CVE-2023-0464
  Resolves: CVE-2023-0465
  Resolves: CVE-2023-0466
  Resolves: CVE-2023-1255
  Resolves: CVE-2023-2650

* Thu Jul 27 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.8-4
- Forbid custom EC more completely
  Resolves: rhbz#2223953

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 21 2023 Sahana Prasad <sahana@redhat.com> - 1:3.0.8-2
- Upload new upstream sources without manually hobbling them.
- Remove the hobbling script as it is redundant. It is now allowed to ship
  the sources of patented EC curves, however it is still made unavailable to use
  by compiling with the 'no-ec2m' Configure option. The additional forbidden
  curves such as P-160, P-192, wap-tls curves are manually removed by updating
  0011-Remove-EC-curves.patch.
- Enable Brainpool curves.
- Apply the changes to ec_curve.c and  ectest.c as a new patch
  0010-Add-changes-to-ectest-and-eccurve.patch instead of replacing them.
- Modify 0011-Remove-EC-curves.patch to allow Brainpool curves.
- Modify 0011-Remove-EC-curves.patch to allow code under macro OPENSSL_NO_EC2M.
  Resolves: rhbz#2130618, rhbz#2141672

* Thu Feb 09 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.8-1
- Rebase to upstream version 3.0.8
  Resolves: CVE-2022-4203
  Resolves: CVE-2022-4304
  Resolves: CVE-2022-4450
  Resolves: CVE-2023-0215
  Resolves: CVE-2023-0216
  Resolves: CVE-2023-0217
  Resolves: CVE-2023-0286
  Resolves: CVE-2023-0401

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.7-3
- Backport implicit rejection for RSA PKCS#1 v1.5 encryption
  Resolves: rhbz#2153470

* Thu Jan 05 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.7-2
- Refactor embedded mac verification in FIPS module
  Resolves: rhbz#2156045

* Fri Dec 23 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.7-1
- Rebase to upstream version 3.0.7
- C99 compatibility in downstream-only 0032-Force-fips.patch
  Resolves: rhbz#2152504
- Adjusting include for the FIPS_mode macro
  Resolves: rhbz#2083876

* Wed Nov 16 2022 Simo sorce <simo@redhat.com> - 1:3.0.5-7
- Backport patches to fix external providers compatibility issues

* Tue Nov 01 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.5-6
- CVE-2022-3602: X.509 Email Address Buffer Overflow
- CVE-2022-3786: X.509 Email Address Buffer Overflow
  Resolves: CVE-2022-3602
  Resolves: CVE-2022-3786

* Mon Sep 12 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.5-5
- Update patches to make ELN build happy
  Resolves: rhbz#2123755

* Fri Sep 09 2022 Clemens Lang <cllang@redhat.com> - 1:3.0.5-4
- Fix AES-GCM on Power 8 CPUs
  Resolves: rhbz#2124845

* Thu Sep 01 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.5-3
- Sync patches with RHEL
  Related: rhbz#2123755
* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 05 2022 Clemens Lang <cllang@redhat.com> - 1:3.0.5-1
- Rebase to upstream version 3.0.5
  Related: rhbz#2099972, CVE-2022-2097

* Wed Jun 01 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.3-1
- Rebase to upstream version 3.0.3

* Thu Apr 28 2022 Clemens Lang <cllang@redhat.com> - 1:3.0.2-5
- Instrument with USDT probes related to SHA-1 deprecation

* Wed Apr 27 2022 Clemens Lang <cllang@redhat.com> - 1:3.0.2-4
- Support rsa_pkcs1_md5_sha1 in TLS 1.0/1.1 with rh-allow-sha1-signatures = yes
  to restore TLS 1.0 and 1.1 support in LEGACY crypto-policy.
  Related: rhbz#2069239

* Tue Apr 26 2022 Alexander Sosedkin <asosedkin@redhat.com> - 1:3.0.2-4
- Instrument with USDT probes related to SHA-1 deprecation

* Wed Apr 20 2022 Clemens Lang <cllang@redhat.com> - 1:3.0.2-3
- Disable SHA-1 by default in ELN using the patches from CentOS
- Fix a FIXME in the openssl.cnf(5) manpage

* Thu Apr 07 2022 Clemens Lang <cllang@redhat.com> - 1:3.0.2-2
- Silence a few rpmlint false positives.

* Thu Apr 07 2022 Clemens Lang <cllang@redhat.com> - 1:3.0.2-2
- Allow disabling SHA1 signature creation and verification.
  Set rh-allow-sha1-signatures = no to disable.
  Allow SHA1 in TLS in SECLEVEL 1 if rh-allow-sha1-signatures = yes. This will
  support SHA1 in TLS in the LEGACY crypto-policy.
  Resolves: rhbz#2070977
  Related: rhbz#2031742, rhbz#2062640

* Fri Mar 18 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.0.2-1
- Rebase to upstream version 3.0.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 09 2021 Sahana Prasad <sahana@redhat.com> - 1:3.0.0-1
- Rebase to upstream version 3.0.0
