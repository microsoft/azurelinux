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

# Since this package exists only as a build-time dependency for openssl so
# it can get fips.so and related debug information, we embed the debug information
# directly into the main package itself.
# To do that, we first disable debug_package, which prevents the package
# itself from being created.
# Below, in __spec_install_post, we then unconditionally generate debug
# information and mangle it so it installs the correct files and directories
# into this package.
%global debug_package   %{nil}
%global _performance_build 1

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl-compat-fips-bootstrap
Version: 3.3.5
Release: 1%{?dist}
# Epoch: 1
Source: https://github.com/openssl/openssl/releases/download/openssl-%{version}/openssl-%{version}.tar.gz
Source2: Makefile.certificate
Source3: genpatches
Source4: openssl.rpmlintrc
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source9: configuration-switch.h
Source10: configuration-prefix.h
Source14: 0025-for-tests.patch
# Patches exported from source git
# Aarch64 and ppc64le use lib64
Patch1:   0001-Aarch64-and-ppc64le-use-lib64.patch
# Use more general default values in openssl.cnf
Patch2:   0002-Use-more-general-default-values-in-openssl.cnf.patch
# Do not install html docs
Patch3:   0003-Do-not-install-html-docs.patch
# apps/ca: fix md option help text
Patch5:   0005-apps-ca-fix-md-option-help-text.patch
# Disable signature verification with totally unsafe hash algorithms
Patch6:   0006-Disable-signature-verification-with-totally-unsafe-h.patch
# Add FIPS_mode() compatibility macro
Patch8:   0008-Add-FIPS_mode-compatibility-macro-compat-3.3.5-AZL3.patch
# Add check to see if fips flag is enabled in kernel
Patch9:   0009-Add-Kernel-FIPS-mode-flag-support.patch
# Instead of replacing ectest.c and ec_curve.c, add the changes as a patch so
# that new modifications made to these files by upstream are not lost.
Patch10:  0010-Add-changes-to-ectest-and-eccurve.patch
# remove unsupported EC curves
Patch11:  0011-Remove-EC-curves.patch
# Disable explicit EC curves
# https://bugzilla.redhat.com/show_bug.cgi?id=2066412
Patch12:  0012-Disable-explicit-ec.patch
# Skipped tests from former 0011-Remove-EC-curves.patch
Patch13:  0013-skipped-tests-EC-curves.patch
# Instructions to load legacy provider in openssl.cnf
Patch24:  0024-load-legacy-prov-3.3.5-AZL3.patch
# We load FIPS provider and set FIPS properties implicitly
Patch32:  0032-Force-fips.patch
# Embed HMAC into the fips.so
# Modify fips self test as per
# https://github.com/simo5/openssl/commit/9b95ef8bd2f5ac862e5eee74c724b535f1a8578a
Patch33:  0033-FIPS-embed-hmac.patch
# Comment out fipsinstall command-line utility
Patch34:  0034.fipsinstall_disable-compat-3.3.5-AZL3.patch
# Skip unavailable algorithms running `openssl speed`
Patch35:  0035-speed-skip-unavailable-dgst.patch
# Extra public/private key checks required by FIPS-140-3
Patch44:  0044-FIPS-140-3-keychecks.patch
# Minimize fips services
Patch45:  0045-FIPS-services-minimize-compat-3.3.5-AZL3.patch
# Execute KATS before HMAC verification
Patch47:  0047-FIPS-early-KATS.patch
# Selectively disallow SHA1 signatures rhbz#2070977
Patch49:  0049-Allow-disabling-of-SHA1-signatures-AZL3.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2053289
Patch58:  0058-FIPS-limit-rsa-encrypt-compat-3.3.5-AZL3.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2087147
Patch61:  0061-Deny-SHA-1-signature-verification-in-FIPS-provider.patch
# 0062-fips-Expose-a-FIPS-indicator.patch
Patch62:  0062-fips-Expose-a-FIPS-indicator.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2102535
Patch73:  0073-FIPS-Use-OAEP-in-KATs-support-fixed-OAEP-seed.patch
# 0074-FIPS-Use-digest_sign-digest_verify-in-self-test.patch
Patch74:  0074-FIPS-Use-digest_sign-digest_verify-in-self-test.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2102535
Patch75:  0075-FIPS-Use-FFDHE2048-in-self-test.patch
# Downstream only. Reseed DRBG using getrandom(GRND_RANDOM)
# https://bugzilla.redhat.com/show_bug.cgi?id=2102541
Patch76:  0076-FIPS-140-3-DRBG.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2102542
Patch77:  0077-FIPS-140-3-zeroization.patch
# # https://bugzilla.redhat.com/show_bug.cgi?id=2114772
# Patch78:  0078-KDF-Add-FIPS-indicators.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2114772
Patch78:  0078-KDF-Add-FIPS-indicators-AZL3.patch
# We believe that some changes present in CentOS are not necessary
# because ustream has a check for FIPS version
Patch80:  0080-rand-Forbid-truncated-hashes-SHA-3-in-FIPS-prov.patch
# 0081-signature-Remove-X9.31-padding-from-FIPS-prov.patch
Patch81:  0081-signature-Remove-X9.31-padding-from-FIPS-prov.patch
# 0083-hmac-Add-explicit-FIPS-indicator-for-key-length.patch
Patch83:  0083-hmac-Add-explicit-FIPS-indicator-for-key-length.patch
# 0084-pbkdf2-Set-minimum-password-length-of-8-bytes.patch
Patch84:  0084-pbkdf2-Set-minimum-password-length-of-8-bytes.patch
# 0085-FIPS-RSA-disable-shake.patch
Patch85:  0085-FIPS-RSA-disable-shake.patch
# 0088-signature-Add-indicator-for-PSS-salt-length.patch
Patch88:  0088-signature-Add-indicator-for-PSS-salt-length.patch
# 0091-FIPS-RSA-encapsulate.patch
Patch91:  0091-FIPS-RSA-encapsulate.patch
# 0110-GCM-Implement-explicit-FIPS-indicator-for-IV-gen.patch
Patch110: 0110-GCM-Implement-explicit-FIPS-indicator-for-IV-gen.patch
# 0112-pbdkf2-Set-indicator-if-pkcs5-param-disabled-checks.patch
Patch112: 0112-pbdkf2-Set-indicator-if-pkcs5-param-disabled-checks.patch
# 0113-asymciphers-kem-Add-explicit-FIPS-indicator.patch
Patch113: 0113-asymciphers-kem-Add-explicit-FIPS-indicator.patch
# We believe that some changes present in CentOS are not necessary
# because ustream has a check for FIPS version
Patch114: 0114-FIPS-enforce-EMS-support-AZL3.patch
# Amend tests according to Fedora/RHEL code
Patch115: 0115-skip-quic-pairwise.patch
# Patch117: 0117-ignore-unknown-sigalgorithms-groups.patch
# https://fedoraproject.org/wiki/Changes/OpenSSLDistrustSHA1SigVer
Patch120: 0120-Allow-disabling-of-SHA1-signatures-AZL3.patch
# From CentOS 9
Patch121: 0121-FIPS-cms-defaults.patch
Patch124: 0124-PBMAC1-PKCS12-FIPS-support-AZL3.patch
# Downstream patch: enforce PBMAC1 in FIPS mode
Patch125: 0125-PBMAC1-PKCS12-FIPS-default.patch
# https://github.com/openssl/openssl/issues/25127
Patch126: 0126-pkeyutl-encap.patch
# https://github.com/openssl/openssl/issues/25056
Patch127: 0127-speedup-SSL_add_cert_subjects_to_stack.patch
Patch128: 0128-SAST-findings.patch
Patch140: 0140-PQ-groups.patch
# Patches we added just for Azure Linux 3.
Patch201: AZL3-rsa-enable-all-padding-similar-to-3.5.patch
Patch200: AZL3-Make-speed-work-in-FIPS-mode.patch
Patch202: AZL3-fix-tests-for-FIPS-mode.patch

License: Apache-2.0
URL: http://www.openssl.org/
BuildRequires: gcc g++
# BuildRequires: coreutils, perl-interpreter, sed, zlib-devel, /usr/bin/cmp
BuildRequires: coreutils, perl-interpreter, sed, /usr/bin/cmp
# BuildRequires: lksctp-tools-devel
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
# BuildRequires: /usr/sbin/sysctl
%if 0%{?with_check}
BuildRequires: perl(Test::Harness), perl(Test::More), perl(Math::BigInt)
%endif
BuildRequires: perl(Module::Load::Conditional), perl(File::Temp)
BuildRequires: perl(Time::HiRes), perl(IPC::Cmd), perl(Pod::Html), perl(Digest::SHA), perl(Time::Piece)
BuildRequires: perl(FindBin), perl(lib), perl(File::Compare), perl(File::Copy), perl(bigint)
BuildRequires: git-core

# BuildRequires: systemtap-sdt-devel
# Requires: coreutils

%description
Bootstrapper to build the OpenSSL FIPS provider to use in the openssl package.

%prep
%autosetup -S git -n openssl-%{version}

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
# ./Configure \
# 	--prefix=%%{_prefix} --openssldir=%%{_sysconfdir}/pki/tls ${sslflags} \
#         --libdir=%%{_lib} \
# 	zlib enable-camellia enable-seed enable-rfc3779 no-sctp \
# 	enable-cms enable-md2 enable-rc5 ${ktlsopt} enable-fips -D_GNU_SOURCE\
# 	no-mdc2 no-ec2m no-sm2 no-sm4 no-atexit enable-buildtest-c++\
# 	shared  ${sslarch} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\"" -DREDHAT_FIPS_VERSION="\"%%{fips}\""'\
# 	-Wl,--allow-multiple-definition
./Configure \
    --prefix=%{_prefix} \
    --openssldir=%{_sysconfdir}/pki/tls \
    ${sslflags} \
    ${ktlsopt} \
    ${sslarch} \
    --libdir=%{_lib} \
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
    enable-buildtest-c++ \
    $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\"" -DREDHAT_FIPS_VERSION="\"%{fips}\""' \
    -Wl,--allow-multiple-definition

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

make -s %{?_smp_mflags} all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

%check
# AZL3: We don't use sctp.
# # Hack - either enable SCTP AUTH chunks in kernel or disable sctp for check
# (sysctl net.sctp.addip_enable=1 && sysctl net.sctp.auth_enable=1) || \
# (echo 'Failed to enable SCTP AUTH chunks, disabling SCTP for tests...' &&
#  sed '/"msan" => "default",/a\ \ "sctp" => "default",' configdata.pm > configdata.pm.new && \
#  touch -r configdata.pm configdata.pm.new && \
#  mv -f configdata.pm.new configdata.pm)

#We must disable default provider before tests otherwise they will fail
patch -p1 < %{SOURCE14}

OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
OPENSSL_ENABLE_SHA1_SIGNATURES=
export OPENSSL_ENABLE_SHA1_SIGNATURES
OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE
#embed HMAC into fips provider for test run
dd if=/dev/zero bs=1 count=32 of=tmp.mac
objcopy --update-section .rodata1=tmp.mac providers/fips.so providers/fips.so.zeromac
mv providers/fips.so.zeromac providers/fips.so
rm tmp.mac
LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < providers/fips.so > providers/fips.so.hmac
objcopy --update-section .rodata1=providers/fips.so.hmac providers/fips.so providers/fips.so.mac
mv providers/fips.so.mac providers/fips.so
#run tests itself
# make test HARNESS_JOBS=8
make test

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
%define __spec_install_post %{expand:
    # Per comments near debug_package above, we first unconditionally
    # generate debug information.
    # The normal command here is:
    # %%{?__debug_package:%%{__debug_install_post}}
    # Which will only generate debug information if __debug_package is defined
    # (which is, in turn defined when debug_information is defined).
    %{__debug_install_post}
    # These are the rest of the standard __spec_install_post
    %{__arch_install_post}
    %{__os_install_post}

    # Now that fips.so is stripped, embed the HMAC key.
    # This is taken directly from fedora-42.
    dd if=/dev/zero bs=1 count=32 of=$RPM_BUILD_ROOT%{_libdir}/ossl-modules/tmp.mac
    objcopy --update-section .rodata1=$RPM_BUILD_ROOT%{_libdir}/ossl-modules/tmp.mac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.zeromac
    mv $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.zeromac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so
    rm $RPM_BUILD_ROOT%{_libdir}/ossl-modules/tmp.mac
    OPENSSL_CONF=/dev/null LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so > $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac
    objcopy --update-section .rodata1=$RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac
    mv $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so
    rm $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac

    # Move fips.so to the actual install directory -- this is the directory
    # where the openssl build will look for it.
    # The simple way we do this below relies on the fact that
    # all files have been installed in /usr. If that's
    # ever not the case, we will need to be more robust.
    # So here we confirm that the only thing in the directory is /usr
    # and that it itself is a directory.
    if [ $(ls -A $RPM_BUILD_ROOT | wc -l) -ne 1 ] || [ ! -d "$RPM_BUILD_ROOT/usr" ]; then
      echo "ERROR: Build Root is expected to have a single directory 'usr' in it."
      ls -Al $RPM_BUILD_ROOT
      exit 1
    fi
    install -d "${RPM_BUILD_ROOT}/opt/%{name}/install/"
    mv $RPM_BUILD_ROOT/usr $RPM_BUILD_ROOT/opt/%{name}/install/

    # Openssl's debuginfo package will need all the debug information we generated
    # along with the files/dirs list. Since it will copy these to the standard
    # installation locations, it needs an unmodified version, so we install it here.
    install -d "${RPM_BUILD_ROOT}/opt/%{name}/metadata/"
    cp debugfiles.list $RPM_BUILD_ROOT/opt/%{name}/metadata/
}
%endif

%define __provides_exclude_from %{_libdir}/openssl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# AZL3: We do the full install of openssl so everything is exactly as if we were using this "for real".
# See bottom of the installation for how we prune things we don't want.
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
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.d
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

# Next step of gradual disablement of ENGINE.
sed -i '/^\# ifndef OPENSSL_NO_STATIC_ENGINE/i\
# if !__has_include(<openssl/engine.h>) && !defined(OPENSSL_NO_ENGINE)\
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
# ln -s /etc/crypto-policies/back-ends/openssl_fips.config $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/fips_local.cnf
cat > $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/fips_local.cnf <<EOF

[fips_sect]
tls1-prf-ems-check = 1
activate = 1
EOF

# AZL3: Delete everything but fips.so so the debuginfo process doesn't pick up unnecessary files.
# To do this, we delete all files and links that aren't fips.so, and then clean up empty directories.
find $RPM_BUILD_ROOT -type f ! -name fips.so -delete
find $RPM_BUILD_ROOT -type l ! -name fips.so -delete
find $RPM_BUILD_ROOT -type d -empty -delete

%files
/opt/%{name}

%changelog
* Wed Nov 05 2025 Tobias Brick <tobiasb@microsoft.com> - 3.3.5-1
- Provide fips.so, built like Fedora, through a bootstrap package.

* Mon Jul 14 2025 gstarovo <gstarovo@redhat.com> - 1:3.2.4-4
- Assign IANA numbers for hybrid PQ KEX

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
