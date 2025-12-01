%define soversion 3

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 %{mips} ppc ppc64 s390 s390x sparcv9 sparc64 x86_64

%global _performance_build 1

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl-fips-provider
Version: 3.1.2
Release: 1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source: https://github.com/openssl/openssl/releases/download/openssl-%{version}/openssl-%{version}.tar.gz
Source2: Makefile.certificate
Source3: genpatches
Source9: configuration-switch.h
Source10: configuration-prefix.h
Source14: 0025-for-tests.patch
Source15: fips_prov.cnf
# Use more general default values in openssl.cnf
Patch2:   0002-Use-more-general-default-values-in-openssl.cnf.patch
# # Do not install html docs
Patch3:   0003-Do-not-install-html-docs-3.1.2-AZL.patch
# # Override default paths for the CA directory tree
# AZL: NOTE: We do not use crypto-policies, so this patch does not apply.
# Patch4:   0004-Override-default-paths-for-the-CA-directory-tree.patch
# # apps/ca: fix md option help text
Patch5:   0005-apps-ca-fix-md-option-help-text.patch
# # Disable signature verification with totally unsafe hash algorithms
Patch6:   0006-Disable-signature-verification-with-totally-unsafe-h.patch
# Add FIPS_mode() compatibility macro
Patch8:   0008-Add-FIPS_mode-compatibility-macro-3.1.4-fedora.patch
# # Add check to see if fips flag is enabled in kernel
Patch9: 0009-Add-Kernel-FIPS-mode-flag-support-3.1.4-fedora.patch
# # Add support for PROFILE=SYSTEM system default cipherlist
# AZL: NOTE: We do not use crypto-policies, so this patch does not apply.
# Patch7:   0007-Add-support-for-PROFILE-SYSTEM-system-default-cipher.patch
# # Instead of replacing ectest.c and ec_curve.c, add the changes as a patch so
# # that new modifications made to these files by upstream are not lost.
Patch10:  0010-Add-changes-to-ectest-and-eccurve-3.1.4-fedora.patch
# # remove unsupported EC curves
Patch11:  0011-Remove-EC-curves-3.1.4-fedora.patch
# # Disable explicit EC curves
# # https://bugzilla.redhat.com/show_bug.cgi?id=2066412
Patch12:  0012-Disable-explicit-ec.patch
# # Skipped tests from former 0011-Remove-EC-curves.patch
Patch13:  0013-skipped-tests-EC-curves-3.1.4-fedora.patch
# # Instructions to load legacy provider in openssl.cnf
# AZL: NOTE: Had to change this patch because of cascading changes from previous AZL note(s)
Patch24:  0024-load-legacy-prov.patch
# # Load the SymCrypt provider by default if present in non-FIPS mode,
# # and always load it implicitly in FIPS mode
Patch32:  0032-Force-fips-3.1.2-AZL3-TEMP-SYMCRYPT.patch
# # Embed HMAC into the fips.so
Patch33:  0033-FIPS-embed-hmac-3.1.2-AZL.patch
# # Comment out fipsinstall command-line utility
Patch34:  0034.fipsinstall_disable-3.1.4-fedora.patch
# # Skip unavailable algorithms running `openssl speed`
Patch35:  0035-speed-skip-unavailable-dgst.patch
# # Selectively disallow SHA1 signatures rhbz#2070977
Patch49:  0049-Allow-disabling-of-SHA1-signatures-3.1.2-AZL.patch
# # Support SHA1 in TLS in LEGACY crypto-policy (which is SECLEVEL=1)
Patch52:  0052-Allow-SHA1-in-seclevel-1-if-rh-allow-sha1-signatures-3.1.4-fedora.patch
# # See notes in the patch for details, but this patch will not be needed if
# # the openssl issue https://github.com/openssl/openssl/issues/7048 is ever implemented and released.
Patch80:  0001-Replacing-deprecated-functions-with-NULL-or-highest.patch

License: Apache-2.0
URL: http://www.openssl.org/

BuildRequires: %{_bindir}/cmp
BuildRequires: %{_bindir}/pod2man
BuildRequires: %{_bindir}/rename
BuildRequires: coreutils
BuildRequires: g++
BuildRequires: gcc
BuildRequires: git-core
BuildRequires: make
BuildRequires: perl-core
BuildRequires: perl(Digest::SHA)
BuildRequires: perl(FindBin)
BuildRequires: perl(IPC::Cmd)
BuildRequires: perl(lib)
BuildRequires: perl(Pod::Html)
BuildRequires: perl(Text::Template)
BuildRequires: sed

BuildRequires: perl(Math::BigInt)
BuildRequires: perl(Test::Harness)
BuildRequires: perl(Test::More)
BuildRequires: perl(Time::Piece)

Conflicts: SymCrypt-OpenSSL

%description
The OpenSSL toolkit provides support for secure communications between
machines. This package provides the OpenSSL FIPS Provider module.

%prep
%autosetup -S git -n openssl-%{version}

%build
# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
NEW_RPM_OPT_FLAGS="%{optflags} -Wa,--noexecstack -Wa,--generate-missing-build-notes=yes -DPURIFY $RPM_LD_FLAGS"

export HASHBANGPERL=/usr/bin/perl

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# NEW_RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
    --prefix=%{_prefix} \
    --openssldir=%{_sysconfdir}/pki/tls \
    --libdir=lib \
    shared \
    no-aria \
    enable-bf \
    no-blake2 \
    enable-camellia \
    no-capieng \
    enable-cast \
    no-chacha \
    enable-cms \
    no-comp \
    enable-ct \
    enable-deprecated \
    enable-des \
    enable-dh \
    enable-dsa \
    no-dtls1 \
    no-ec2m \
    enable-ec_nistp_64_gcc_128 \
    enable-ecdh \
    enable-ecdsa \
    enable-fips \
    no-gost \
    no-idea \
    no-mdc2 \
    no-md2 \
    enable-md4 \
    no-poly1305 \
    enable-rc2 \
    enable-rc4 \
    enable-rc5 \
    no-rfc3779 \
    enable-rmd160 \
    no-sctp \
    no-seed \
    no-siphash \
    no-sm2 \
    no-sm3 \
    no-sm4 \
    no-ssl \
    no-ssl3 \
    no-weak-ssl-ciphers \
    no-whirlpool \
    no-zlib \
    no-zlib-dynamic \
    enable-ktls \
    enable-buildtest-c++ \
    $NEW_RPM_OPT_FLAGS \
    '-DDEVRANDOM="\"/dev/urandom\""'\
    -Wl,--allow-multiple-definition

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
    set -x \
    OPENSSL_CONF=/dev/null LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so > $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac \
    objcopy --update-section .rodata1=$RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac \
    mv $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so \
    rm $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac \
    set +x \
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

# We don't use native fipsmodule.cnf because FIPS module is loaded automatically
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

# Delete everything but fips.so, since that's all we ship.
# To do this, we delete all files and links that aren't fips.so.
find $RPM_BUILD_ROOT -type f ! -name fips.so -delete
find $RPM_BUILD_ROOT -type l ! -name fips.so -delete

# Now add our fips_prov.cnf file
install -m644 %{SOURCE15} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/fips_prov.cnf

# Clean up any empty directories left over from the deletions above.
find $RPM_BUILD_ROOT -type d -empty -delete

%files
%attr(0755,root,root) %{_libdir}/ossl-modules
%config(noreplace) %{_sysconfdir}/pki/tls/fips_prov.cnf

%ldconfig_scriptlets libs

%changelog
* Thu Nov 13 2025 Tobias Brick <tobiasb@microsoft.com> - 3.1.2-1
- Initial implementation of OpenSSL FIPS provider package for AZL.
- Copied from Azure Linux 3's openssl.spec
- Modified to only package the 140-3 certified FIPS provider and config file from OpenSSL 3.1.2.
- License verified
