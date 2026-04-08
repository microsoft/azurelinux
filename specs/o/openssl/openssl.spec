# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# For the curious:
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
# 1.1.0 soversion = 1.1 (same as upstream although presence of some symbols
#                        depends on build configuration options)
# 3.0.0 soversion = 3 (same as upstream)
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

# https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine
# ENGINE is deprecated but still (separately) available for Fedora.
# It has been completely removed from RHEL 10 and later.
%bcond engine %[!(0%{?rhel} >= 10)]

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl
Version: 3.5.4
Release: 2%{?dist}
Epoch: 1
Source0: openssl-%{version}.tar.gz
Source1: fips-hmacify.sh
Source3: genpatches
Source4: openssl.rpmlintrc
Source9: configuration-switch.h
Source10: configuration-prefix.h

Patch0001: 0001-RH-Aarch64-and-ppc64le-use-lib64.patch
Patch0002: 0002-Add-a-separate-config-file-to-use-for-rpm-installs.patch
Patch0003: 0003-RH-Do-not-install-html-docs.patch
Patch0004: 0004-RH-apps-ca-fix-md-option-help-text.patch-DROP.patch
Patch0005: 0005-RH-Disable-signature-verification-with-bad-digests-R.patch
Patch0006: 0006-RH-Add-support-for-PROFILE-SYSTEM-system-default-cip.patch
Patch0007: 0007-RH-Add-FIPS_mode-compatibility-macro.patch
Patch0008: 0008-RH-Add-Kernel-FIPS-mode-flag-support-FIXSTYLE.patch
Patch0009: 0009-RH-Drop-weak-curve-definitions-RENAMED-SQUASHED.patch
Patch0010: 0010-RH-Disable-explicit-ec-curves.patch
Patch0011: 0011-RH-skipped-tests-EC-curves.patch
Patch0012: 0012-RH-skip-quic-pairwise.patch
Patch0013: 0013-RH-version-aliasing.patch
Patch0014: 0014-RH-Export-two-symbols-for-OPENSSL_str-n-casecmp.patch
Patch0015: 0015-RH-TMP-KTLS-test-skip.patch
Patch0016: 0016-RH-Allow-disabling-of-SHA1-signatures.patch
Patch0017: 0017-FIPS-Red-Hat-s-FIPS-module-name-and-version.patch
Patch0018: 0018-FIPS-disable-fipsinstall.patch
Patch0019: 0019-FIPS-Force-fips-provider-on.patch
Patch0020: 0020-FIPS-INTEG-CHECK-Embed-hmac-in-fips.so-NOTE.patch
Patch0021: 0021-FIPS-INTEG-CHECK-Add-script-to-hmac-ify-fips.so.patch
Patch0022: 0022-FIPS-INTEG-CHECK-Execute-KATS-before-HMAC-REVIEW.patch
Patch0023: 0023-FIPS-RSA-encrypt-limits-REVIEW.patch
Patch0024: 0024-FIPS-RSA-PCTs.patch
Patch0025: 0025-FIPS-RSA-encapsulate-limits.patch
Patch0026: 0026-FIPS-RSA-Disallow-SHAKE-in-OAEP-and-PSS.patch
Patch0027: 0027-FIPS-RSA-size-mode-restrictions.patch
Patch0028: 0028-FIPS-RSA-Mark-x931-as-not-approved-by-default.patch
Patch0029: 0029-FIPS-RSA-Remove-X9.31-padding-signatures-tests.patch
Patch0030: 0030-FIPS-RSA-NEEDS-REWORK-FIPS-Use-OAEP-in-KATs-support-.patch
Patch0031: 0031-FIPS-Deny-SHA-1-signature-verification.patch
Patch0032: 0032-FIPS-RAND-FIPS-140-3-DRBG-NEEDS-REVIEW.patch
Patch0033: 0033-FIPS-RAND-Forbid-truncated-hashes-SHA-3.patch
Patch0034: 0034-FIPS-PBKDF2-Set-minimum-password-length.patch
Patch0035: 0035-FIPS-DH-PCT.patch
Patch0036: 0036-FIPS-DH-Disable-FIPS-186-4-type-parameters.patch
Patch0037: 0037-FIPS-TLS-Enforce-EMS-in-TLS-1.2-NOTE.patch
Patch0038: 0038-FIPS-CMS-Set-default-padding-to-OAEP.patch
Patch0039: 0039-FIPS-PKCS12-PBMAC1-defaults.patch
Patch0040: 0040-FIPS-Fix-encoder-decoder-negative-test.patch
Patch0041: 0041-FIPS-EC-DH-DSA-PCTs.patch
Patch0042: 0042-FIPS-EC-disable-weak-curves.patch
Patch0043: 0043-FIPS-NO-DSA-Support.patch
Patch0044: 0044-FIPS-NO-DES-support.patch
Patch0045: 0045-FIPS-NO-Kmac.patch
Patch0046: 0046-FIPS-Fix-some-tests-due-to-our-versioning-change.patch
Patch0047: 0047-Current-Rebase-status.patch
Patch0048: 0048-FIPS-KDF-key-lenght-errors.patch
Patch0049: 0049-FIPS-fix-disallowed-digests-tests.patch
Patch0050: 0050-Make-openssl-speed-run-in-FIPS-mode.patch
Patch0051: 0051-Backport-upstream-27483-for-PKCS11-needs.patch
Patch0052: 0052-Red-Hat-9-FIPS-indicator-defines.patch
%if ( %{defined rhel} && (! %{defined centos}) && (! %{defined eln}) )
Patch0053: 0053-Allow-hybrid-MLKEM-in-FIPS-mode.patch
%endif
Patch0054: 0054-Temporarily-disable-SLH-DSA-FIPS-self-tests.patch
Patch0055: 0055-Add-a-define-to-disable-symver-attributes.patch
Patch0056: 0056-apps-speed.c-Disable-testing-of-composite-signature-.patch
Patch0057: 0057-apps-speed.c-Support-more-signature-algorithms.patch
Patch0058: 0058-Add-targets-to-skip-build-of-non-installable-program.patch
Patch0059: 0059-RSA_encrypt-decrypt-with-padding-NONE-is-not-support.patch
Patch0060: 0060-CVE-2025-15467.patch
Patch0061: 0061-CVE-2025-15468.patch
Patch0062: 0062-CVE-2025-15469.patch
Patch0063: 0063-CVE-2025-66199.patch
Patch0064: 0064-CVE-2025-68160.patch
Patch0065: 0065-CVE-2025-69418.patch
Patch0066: 0066-CVE-2025-69420.patch
Patch0067: 0067-CVE-2025-69421.patch
Patch0068: 0068-CVE-2025-69419.patch
Patch0069: 0069-CVE-2026-22795.patch
Patch0070: 0070-CVE-2025-11187.patch
Patch0071: 0071-Do-not-make-key-share-choice-in-tls1_set_groups.patch
Patch0072: 0072-Fix-PPC-register-processing.patch


License: Apache-2.0
URL: http://www.openssl.org/
BuildRequires: gcc g++
BuildRequires: coreutils, perl-interpreter, sed, zlib-devel, /usr/bin/cmp
BuildRequires: lksctp-tools-devel
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/sbin/sysctl
BuildRequires: perl(Test::Harness), perl(Test::More), perl(Math::BigInt)
BuildRequires: perl(Module::Load::Conditional), perl(File::Temp)
BuildRequires: perl(Time::HiRes), perl(Time::Piece), perl(IPC::Cmd), perl(Pod::Html), perl(Digest::SHA)
BuildRequires: perl(FindBin), perl(lib), perl(File::Compare), perl(File::Copy), perl(bigint)
BuildRequires: git-core
BuildRequires: systemtap-sdt-devel
Requires: coreutils
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: oqsprovider < 0.9.0

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Requires: ca-certificates >= 2008-5
Requires: crypto-policies >= 20180730
Recommends: pkcs11-provider%{?_isa}
%if ( %{defined rhel} && (! %{defined centos}) && (! %{defined eln}) )
Requires: openssl-fips-provider
%endif

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: pkgconfig
%if %{without engine}
Obsoletes: %{name}-devel-engine < %{epoch}:%{version}-%{release}
%endif

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%if %{with engine}
%package devel-engine
Summary: Files for development of applications which will use OpenSSL and use deprecated ENGINE API.
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires: pkgconfig
Provides: deprecated()

%description devel-engine
OpenSSL is a toolkit for supporting cryptography. The openssl-devel-engine
package contains include files needed to develop applications which
use deprecated OpenSSL ENGINE functionality.
%endif

%package perl
Summary: Perl scripts provided with OpenSSL
Requires: perl-interpreter
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%autosetup -S git -n %{name}-%{version}

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
sslarch=linux64-riscv64
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
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
%ifarch riscv64
        --libdir=%{_lib} \
%endif
	--system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/opensslcnf.config \
	zlib enable-camellia enable-seed enable-rfc3779 enable-sctp \
	enable-cms enable-md2 enable-rc5 ${ktlsopt} enable-fips -D_GNU_SOURCE\
	no-mdc2 no-ec2m no-sm2 no-sm4 no-atexit enable-buildtest-c++\
	shared  ${sslarch} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\""' -DOPENSSL_PEDANTIC_ZEROIZATION\
	-DREDHAT_FIPS_VENDOR='"\"Red Hat Enterprise Linux OpenSSL FIPS Provider\""' -DREDHAT_FIPS_VERSION='"\"%{fips}\""'\
	-Wl,--allow-multiple-definition

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

make -s %{?_smp_mflags} build_inst_sw

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

%check
# Verify that what was compiled actually works.

# Hack - either enable SCTP AUTH chunks in kernel or disable sctp for check
(sysctl net.sctp.addip_enable=1 && sysctl net.sctp.auth_enable=1) || \
(echo 'Failed to enable SCTP AUTH chunks, disabling SCTP for tests...' &&
 sed '/"msan" => "default",/a\ \ "sctp" => "default",' configdata.pm > configdata.pm.new && \
 touch -r configdata.pm configdata.pm.new && \
 mv -f configdata.pm.new configdata.pm)


OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
OPENSSL_ENABLE_SHA1_SIGNATURES=
export OPENSSL_ENABLE_SHA1_SIGNATURES
OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE
#embed HMAC into fips provider for test run
#dd if=/dev/zero bs=1 count=32 of=tmp.mac
#objcopy --update-section .rodata1=tmp.mac providers/fips.so providers/fips.so.zeromac
#mv providers/fips.so.zeromac providers/fips.so
#rm tmp.mac
#LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < providers/fips.so > providers/fips.so.hmac
#objcopy --update-section .rodata1=providers/fips.so.hmac providers/fips.so providers/fips.so.mac
#mv providers/fips.so.mac providers/fips.so
%{SOURCE1} providers/fips.so

# Build tests with LTO disabled and run them
make -s %{?_smp_mflags} build_programs \
    CFLAGS="%{build_cflags} -fno-lto" \
    CXXFLAGS="%{build_cxxflags} -fno-lto"
make test HARNESS_JOBS=8

# Add generation of HMAC checksum of the final stripped library
# We manually copy standard definition of __spec_install_post
# and add hmac calculation/embedding to fips.so
%if ( %{defined rhel} && (! %{defined centos}) && (! %{defined eln}) )
%define __spec_install_post \
    rm -rf $RPM_BUILD_ROOT/%{_libdir}/ossl-modules/fips.so \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
%{nil}
%else
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    %{SOURCE1} $RPM_BUILD_ROOT/%{_libdir}/ossl-modules/fips.so \
%{nil}
%endif

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
mv rh-openssl.cnf $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf

# Remove static libraries
for lib in $RPM_BUILD_ROOT%{_libdir}/*.a ; do
	rm -f ${lib}
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.d

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
touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf
touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/ct_log_list.cnf

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

# Next step of gradual disablement of ENGINE.
sed -i '/^\# ifndef OPENSSL_NO_STATIC_ENGINE/i\
# if %{?with_engine:!__has_include(<openssl/engine.h>) &&} !defined(OPENSSL_NO_ENGINE)\
#  define OPENSSL_NO_ENGINE\
# endif' $RPM_BUILD_ROOT/%{_prefix}/include/openssl/configuration.h

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
ln -s /etc/crypto-policies/back-ends/openssl_fips.config $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/fips_local.cnf

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc NEWS.md README.md
%{_bindir}/openssl
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%exclude %{_mandir}/man1/*.pl*
%exclude %{_mandir}/man1/tsget*

%files libs
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%dir %{_sysconfdir}/pki/tls/openssl.d
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%config(noreplace) %{_sysconfdir}/pki/tls/ct_log_list.cnf
%config %{_sysconfdir}/pki/tls/fips_local.cnf
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%{_libdir}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%{_libdir}/libssl.so.%{soversion}
%attr(0755,root,root) %{_libdir}/engines-%{soversion}
%attr(0755,root,root) %{_libdir}/ossl-modules

%files devel
%doc CHANGES.md doc/dir-locals.example.el doc/openssl-c-indent.el
%{_prefix}/include/openssl
%exclude %{_prefix}/include/openssl/engine*.h
%{_libdir}/*.so
%{_mandir}/man3/*
%exclude %{_mandir}/man3/ENGINE*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/OpenSSL/OpenSSLConfig.cmake
%{_libdir}/cmake/OpenSSL/OpenSSLConfigVersion.cmake


%if %{with engine}
%files devel-engine
%{_prefix}/include/openssl/engine*.h
%{_mandir}/man3/ENGINE*
%endif

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
* Tue Jan 27 2026 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.5.4-2
- Resolves: CVE-2025-15467
- Resolves: CVE-2025-15468
- Resolves: CVE-2025-15469
- Resolves: CVE-2025-66199
- Resolves: CVE-2025-68160
- Resolves: CVE-2025-69418
- Resolves: CVE-2025-69420
- Resolves: CVE-2025-69421
- Resolves: CVE-2025-69419
- Resolves: CVE-2026-22795
- Resolves: CVE-2026-22796
- Resolves: CVE-2025-11187

* Wed Oct 15 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.5.4-1
- Rebase to OpenSSL 3.5.4, resolving CVE-2025-9230 and CVE-2025-9232

* Tue Aug 26 2025 Pavol Žáčik <pzacik@redhat.com> - 1:3.5.1-3
- Make openssl speed test signatures without errors
- Build tests in check and without LTO

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 01 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.5.1-1
- Rebasing to OpenSSL 3.5.1

* Thu Jun 05 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.5.0-5
- Sync patches from RHEL

* Thu Apr 24 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1:3.5.0-4
- Disable -devel-engine on RHEL 10+

* Tue Apr 15 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.5.0-3
- Rebase to OpenSSL 3.5 final release, sync patches with RHEL. Restoring POWER8 support
  Resolves: rhbz#2359082

* Wed Mar 26 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.5.0-2
- Early rebasing to OpenSSL 3.5-beta

* Fri Mar 21 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.5.0-1
- Early rebasing to OpenSSL 3.5-alpha

* Thu Mar 13 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.4-3
- Proper providing of default cipher string file on compilation
  Build with no-atexit similar to CentOS/RHEL

* Tue Feb 25 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.4-2
- Deprecating a proper subpackage
  Related: rhbz#2276420

* Wed Feb 12 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.4-1
- Rebase to 3.2.4
  Resolves: CVE-2024-12797

* Wed Jan 29 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.2-14
- Fixup for loading default cipher string
  Resolves: rhbz#2342801

* Mon Jan 27 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.2-13
- Locally configured providers should not interfere with openssl build-time tests
- Load system default cipher string from crypto-policies configuration file
  include /etc/crypto-policies/back-ends/opensslcnf.config and remove
  /etc/crypto-policies/back-ends/openssl.config.

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.2-11
- Ensure that the checksum of the fips provider is calculated correctly
  Resolves: rhbz#2335414

* Thu Jan 02 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.2-10
- Fix provider no_cache behaviour

* Wed Sep 25 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:3.2.2-9
- Add PQ container test via TMT

* Thu Sep 12 2024 Sahana Prasad <sahana@redhat.com> - 1:3.2.2-8
- Synchorize patches in CentOS10 and Fedora with the following changes
- Fix CVE-2024-5535: SSL_select_next_proto buffer overread
- Use PBMAC1 by default when creating PKCS#12 files in FIPS mode
- Support key encapsulation/decapsulation in openssl pkeyutl command
- Fix typo in the patch numeration
- Enable KTLS, temporary disable KTLS tests
- Speedup SSL_add_{file,dir}_cert_subjects_to_stack
- Resolve SAST package scan results
- An interface to create PKCS #12 files in FIPS compliant way

* Fri Sep 06 2024 Sahana Prasad <sahana@redhat.com> - 1:3.2.2-7
- Patch for CVE-2024-6119

* Tue Sep 03 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1:3.2.2-6
- Define OPENSSL_NO_ENGINE if openssl-devel-engine is not installed

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Sahana Prasad  <sahana@redhat.com> - 1:3.2.2-4
- Assign IANA numbers for hybrid PQ KEX
- Porting the fix in https://github.com/openssl/openssl/pull/22803

* Mon Jul 01 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.2-3
- Moving engine-related files to a separate subpackage to be deprecated in future
  Resolves: rhbz#2276420

* Thu Jun 27 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.2-2
- As upstream disables TLS 1.0/1.1 on any SECLEVEL > 0, there is no point
  keeping the SHA1 permission at SECLEVEL=1 anymore.

* Thu Jun 06 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.2-1
- Rebase to 3.2.2

* Wed Jun 05 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1:3.2.1-10
- Do not require openssl-fips-provider on ELN

* Mon Jun 03 2024 Sahana Prasad <sahana@redhat.com> - 1:3.2.1-9
- Synchronize patches from CentOS 9 that had additional fixes required
  for rebase to 3.2.1

* Tue May 28 2024 Alexander Sosedkin <asosedkin@redhat.com> - 1:3.2.1-8
- Instrument with USDT probes related to SHA-1 deprecation

* Tue May 14 2024 David Abdurachmanov <davidlt@rivosinc.com> - 1:3.2.1-7
- Add --libdir=%{_lib} for riscv64 (uses linux-generic64)

* Thu Apr 04 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.1-6
- Restoring missing part of 0044-
- Backporting CMS FIPS defaults from CentOS 9

* Mon Mar 25 2024 Sahana Prasad <sahana@redhat.com> - 1:3.2.1-5
- Add no-engine support. The previous commit was a mistake.

* Mon Mar 25 2024 Sahana Prasad <sahana@redhat.com> - 1:3.2.1-4
- Build OpenSSL with no-engine support

* Thu Mar 07 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.2.1-3
- Minimize skipping tests
- Allow ignoring unknown signature algorithms and groups (upstream #23050)
- Allow specifying provider algorithms in SignatureAlgorithms (upstream #22779)

* Fri Feb 09 2024 Sahana Prasad <sahana@redhat.com> - 1:3.2.1-2
- Fix version aliasing issue
- https://github.com/openssl/openssl/issues/23534

* Tue Feb 06 2024 Sahana Prasad <sahana@redhat.com> - 1:3.2.1-1
- Rebase to upstream version 3.2.1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1:3.1.4-2
- We don't want to ship openssl-pkcs11 in RHEL10/Centos 10

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
