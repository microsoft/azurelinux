# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define pkidir %{_sysconfdir}/pki
%define catrustdir %{_sysconfdir}/pki/ca-trust
%define classic_tls_bundle ca-bundle.crt
%define openssl_format_trust_bundle ca-bundle.trust.crt
%define p11_format_bundle ca-bundle.trust.p11-kit
%define legacy_default_bundle ca-bundle.legacy.default.crt
%define legacy_disable_bundle ca-bundle.legacy.disable.crt
%define java_bundle java/cacerts

Summary: The Mozilla CA root certificate bundle
Name: ca-certificates

# For the package version number, we use: year.{upstream version}
#
# The {upstream version} can be found as symbol
# NSS_BUILTINS_LIBRARY_VERSION in file nss/lib/ckfw/builtins/nssckbi.h
# which corresponds to the data in file nss/lib/ckfw/builtins/certdata.txt.
#
# The files should be taken from a released version of NSS, as published
# at https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/
#
# The versions that are used by the latest released version of 
# Mozilla Firefox should be available from:
# https://hg.mozilla.org/releases/mozilla-release/raw-file/default/security/nss/lib/ckfw/builtins/nssckbi.h
# https://hg.mozilla.org/releases/mozilla-release/raw-file/default/security/nss/lib/ckfw/builtins/certdata.txt
#
# The most recent development versions of the files can be found at
# http://hg.mozilla.org/projects/nss/raw-file/default/lib/ckfw/builtins/nssckbi.h
# http://hg.mozilla.org/projects/nss/raw-file/default/lib/ckfw/builtins/certdata.txt
# (but these files might have not yet been released).
#
# (until 2012.87 the version was based on the cvs revision ID of certdata.txt,
# but in 2013 the NSS projected was migrated to HG. Old version 2012.87 is 
# equivalent to new version 2012.1.93, which would break the requirement 
# to have increasing version numbers. However, the new scheme will work, 
# because all future versions will start with 2013 or larger.)

Version: 2025.2.80_v9.0.304
# for Rawhide, please always use release >= 2
# for Fedora release branches, please use release < 2 (1.0, 1.1, ...)
Release: 1.1%{?dist}
License: MIT AND GPL-2.0-or-later

URL: https://fedoraproject.org/wiki/CA-Certificates

#Please always update both certdata.txt and nssckbi.h
Source0: certdata.txt
Source1: nssckbi.h
Source2: update-ca-trust
Source3: trust-fixes
Source4: certdata2pem.py
Source5: ca-legacy.conf
Source6: ca-legacy
Source9: ca-legacy.8.txt
Source10: update-ca-trust.8.txt
Source11: README.usr
Source12: README.etc
Source13: README.extr
Source14: README.java
Source15: README.openssl
Source16: README.pem
Source17: README.edk2
Source18: README.src
Source19: README.etcssl

BuildArch: noarch

Requires(post): bash
Requires(post): findutils
Requires(post): grep
Requires(post): sed
Requires(post): coreutils
Requires: bash
Requires: grep
Requires: sed
Requires(post): p11-kit >= 0.24
Requires(post): p11-kit-trust >= 0.24
Requires: p11-kit >= 0.24
Requires: p11-kit-trust >= 0.24
Requires: libffi
Requires(post): libffi

BuildRequires: perl-interpreter
BuildRequires: python3
BuildRequires: openssl
BuildRequires: asciidoc
BuildRequires: xmlto

%description
This package contains the set of CA certificates chosen by the
Mozilla Foundation for use with the Internet PKI.

%prep
rm -rf %{name}
mkdir %{name}
mkdir %{name}/certs
mkdir %{name}/certs/legacy-default
mkdir %{name}/certs/legacy-disable
mkdir %{name}/java

%build
pushd %{name}/certs
 pwd
 cp %{SOURCE0} .
 python3 %{SOURCE4} >c2p.log 2>c2p.err
popd
pushd %{name}
 (
   cat <<EOF
# This is a bundle of X.509 certificates of public Certificate
# Authorities.  It was generated from the Mozilla root CA list.
# These certificates and trust/distrust attributes use the file format accepted
# by the p11-kit-trust module.
#
# Source: nss/lib/ckfw/builtins/certdata.txt
# Source: nss/lib/ckfw/builtins/nssckbi.h
#
# Generated from:
EOF
   cat %{SOURCE1}  |grep -w NSS_BUILTINS_LIBRARY_VERSION | awk '{print "# " $2 " " $3}';
   echo '#';
 ) > %{p11_format_bundle}

 touch %{legacy_default_bundle}
 NUM_LEGACY_DEFAULT=`find certs/legacy-default -type f | wc -l`
 if [ $NUM_LEGACY_DEFAULT -ne 0 ]; then
     for f in certs/legacy-default/*.crt; do 
       echo "processing $f"
       tbits=`sed -n '/^# openssl-trust/{s/^.*=//;p;}' $f`
       alias=`sed -n '/^# alias=/{s/^.*=//;p;q;}' $f | sed "s/'//g" | sed 's/"//g'`
       targs=""
       if [ -n "$tbits" ]; then
          for t in $tbits; do
             targs="${targs} -addtrust $t"
          done
       fi
       if [ -n "$targs" ]; then
          echo "legacy default flags $targs for $f" >> info.trust
          openssl x509 -text -in "$f" -trustout $targs -setalias "$alias" >> %{legacy_default_bundle}
       fi
     done
 fi

 touch %{legacy_disable_bundle}
 NUM_LEGACY_DISABLE=`find certs/legacy-disable -type f | wc -l`
 if [ $NUM_LEGACY_DISABLE -ne 0 ]; then
     for f in certs/legacy-disable/*.crt; do 
       echo "processing $f"
       tbits=`sed -n '/^# openssl-trust/{s/^.*=//;p;}' $f`
       alias=`sed -n '/^# alias=/{s/^.*=//;p;q;}' $f | sed "s/'//g" | sed 's/"//g'`
       targs=""
       if [ -n "$tbits" ]; then
          for t in $tbits; do
             targs="${targs} -addtrust $t"
          done
       fi
       if [ -n "$targs" ]; then
          echo "legacy disable flags $targs for $f" >> info.trust
          openssl x509 -text -in "$f" -trustout $targs -setalias "$alias" >> %{legacy_disable_bundle}
       fi
     done
 fi

 P11FILES=`find certs -name \*.tmp-p11-kit | wc -l`
 if [ $P11FILES -ne 0 ]; then
   for p in certs/*.tmp-p11-kit; do 
     cat "$p" >> %{p11_format_bundle}
   done
 fi
 # Append our trust fixes
 cat %{SOURCE3} >> %{p11_format_bundle}
popd

#manpage
cp %{SOURCE10} %{name}/update-ca-trust.8.txt
asciidoc -v -d manpage -b docbook %{name}/update-ca-trust.8.txt
xmlto -v -o %{name} man %{name}/update-ca-trust.8.xml

cp %{SOURCE9} %{name}/ca-legacy.8.txt
asciidoc -v -d manpage -b docbook %{name}/ca-legacy.8.txt
xmlto -v -o %{name} man %{name}/ca-legacy.8.xml


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m 755 $RPM_BUILD_ROOT%{pkidir}/tls/certs
mkdir -p -m 755 $RPM_BUILD_ROOT%{pkidir}/java
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ssl
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/source
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/source/anchors
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/source/blocklist
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/extracted
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/extracted/pem
mkdir -p -m 555 $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/directory-hash
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/extracted/openssl
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/extracted/java
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/extracted/edk2
mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source
mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/anchors
mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/blocklist
mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-legacy
mkdir -p -m 755 $RPM_BUILD_ROOT%{_bindir}
mkdir -p -m 755 $RPM_BUILD_ROOT%{_mandir}/man8

install -p -m 644 %{name}/update-ca-trust.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 %{name}/ca-legacy.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/README
install -p -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{catrustdir}/README
install -p -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{catrustdir}/extracted/README
install -p -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{catrustdir}/extracted/java/README
install -p -m 644 %{SOURCE15} $RPM_BUILD_ROOT%{catrustdir}/extracted/openssl/README
install -p -m 644 %{SOURCE16} $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/README
install -p -m 644 %{SOURCE17} $RPM_BUILD_ROOT%{catrustdir}/extracted/edk2/README
install -p -m 644 %{SOURCE18} $RPM_BUILD_ROOT%{catrustdir}/source/README
install -p -m 644 %{SOURCE19} $RPM_BUILD_ROOT%{_sysconfdir}/ssl/README

install -p -m 644 %{name}/%{p11_format_bundle} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{p11_format_bundle}

install -p -m 644 %{name}/%{legacy_default_bundle} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-legacy/%{legacy_default_bundle}
install -p -m 644 %{name}/%{legacy_disable_bundle} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-legacy/%{legacy_disable_bundle}

install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{catrustdir}/ca-legacy.conf

touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{p11_format_bundle}

touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-legacy/%{legacy_default_bundle}
touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-legacy/%{legacy_disable_bundle}

# TODO: consider to dynamically create the update-ca-trust script from within
#       this .spec file, in order to have the output file+directory names at once place only.
install -p -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/update-ca-trust

install -p -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_bindir}/ca-legacy

# touch ghosted files that will be extracted dynamically
# Set chmod 444 to use identical permission
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/tls-ca-bundle.pem
chmod 444 $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/tls-ca-bundle.pem
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/email-ca-bundle.pem
chmod 444 $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/email-ca-bundle.pem
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/objsign-ca-bundle.pem
chmod 444 $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/objsign-ca-bundle.pem
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/openssl/%{openssl_format_trust_bundle}
chmod 444 $RPM_BUILD_ROOT%{catrustdir}/extracted/openssl/%{openssl_format_trust_bundle}
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/%{java_bundle}
chmod 444 $RPM_BUILD_ROOT%{catrustdir}/extracted/%{java_bundle}
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/edk2/cacerts.bin
chmod 444 $RPM_BUILD_ROOT%{catrustdir}/extracted/edk2/cacerts.bin

# Populate %%{catrustdir}/extracted/pem/directory-hash.
#
# First direct p11-kit-trust.so to the generated bundle (not the one
# already present on the build system) with an overriding module
# config. Note that we have to use a different config path based on
# the current user: if root, ~/.config/pkcs11/modules/* are not read,
# while if a regular user, she can't write to /etc.
if test "$(id -u)" -eq 0; then
   trust_module_dir=/etc/pkcs11/modules
else
   trust_module_dir=$HOME/.config/pkcs11/modules
fi

mkdir -p "$trust_module_dir"

# It is unlikely that the directory would contain any files on a build system,
# but let's make sure just in case.
if [ -n "$(ls -A "$trust_module_dir")" ]; then
        echo "Directory $trust_module_dir is not empty. Aborting build!"
        exit 1
fi

trust_module_config=$trust_module_dir/%{name}-p11-kit-trust.module
cat >"$trust_module_config" <<EOF
module: p11-kit-trust.so
trust-policy: yes
x-init-reserved: paths='$RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source'
EOF

# Extract the trust anchors to the directory-hash format.
trust extract --format=pem-directory-hash --filter=ca-anchors --overwrite \
              --purpose server-auth \
              $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/directory-hash

# Clean up the temporary module config.
rm -f "$trust_module_config"

find $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/directory-hash -type l \
     -regextype posix-extended -regex '.*/[0-9a-f]{8}\.[0-9]+' \
     -exec cp -P {} $RPM_BUILD_ROOT%{pkidir}/tls/certs/ \;
# Create a temporary file with the list of (%ghost )files in the directory-hash and their copies
find $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/directory-hash -type f,l > .files.txt
find $RPM_BUILD_ROOT%{pkidir}/tls/certs -type l -regextype posix-extended \
     -regex '.*/[0-9a-f]{8}\.[0-9]+' >> .files.txt

sed -i "s|^$RPM_BUILD_ROOT|%ghost /|" .files.txt

# /etc/ssl is provided in a Debian compatible form for (bad) code that
# expects it: https://bugzilla.redhat.com/show_bug.cgi?id=1053882
ln -s %{pkidir}/tls/certs \
    $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs
ln -s %{catrustdir}/extracted/pem/tls-ca-bundle.pem \
    $RPM_BUILD_ROOT%{_sysconfdir}/ssl/cert.pem
ln -s /etc/pki/tls/openssl.cnf \
    $RPM_BUILD_ROOT%{_sysconfdir}/ssl/openssl.cnf
ln -s /etc/pki/tls/ct_log_list.cnf \
    $RPM_BUILD_ROOT%{_sysconfdir}/ssl/ct_log_list.cnf
# legacy filenames
ln -s %{catrustdir}/extracted/pem/tls-ca-bundle.pem \
    $RPM_BUILD_ROOT%{pkidir}/tls/cert.pem
ln -s %{catrustdir}/extracted/%{java_bundle} \
    $RPM_BUILD_ROOT%{pkidir}/%{java_bundle}
ln -s %{catrustdir}/extracted/pem/tls-ca-bundle.pem \
    $RPM_BUILD_ROOT%{pkidir}/tls/certs/%{classic_tls_bundle}
ln -s %{catrustdir}/extracted/pem/tls-ca-bundle.pem \
    $RPM_BUILD_ROOT%{pkidir}/tls/certs/ca-certificates.crt
ln -s %{catrustdir}/extracted/openssl/%{openssl_format_trust_bundle} \
    $RPM_BUILD_ROOT%{pkidir}/tls/certs/%{openssl_format_trust_bundle}

%clean
/usr/bin/chmod u+w $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/directory-hash
rm -rf $RPM_BUILD_ROOT

%pre
if [ $1 -gt 1 ] ; then
  # Upgrade or Downgrade.
  # If the classic filename is a regular file, then we are upgrading
  # from an old package and we will move it to an .rpmsave backup file.
  # If the filename is a symbolic link, then we are good already.
  # If the system will later be downgraded to an old package with regular 
  # files, and afterwards updated again to a newer package with symlinks,
  # and the old .rpmsave backup file didn't get cleaned up,
  # then we don't backup again. We keep the older backup file.
  # In other words, if an .rpmsave file already exists, we don't overwrite it.
  #
  if ! test -e %{pkidir}/%{java_bundle}.rpmsave; then
    # no backup yet
    if test -e %{pkidir}/%{java_bundle}; then
      # a file exists
        if ! test -L %{pkidir}/%{java_bundle}; then
        # it's an old regular file, not a link
        mv -f %{pkidir}/%{java_bundle} %{pkidir}/%{java_bundle}.rpmsave
      fi
    fi
  fi

  if ! test -e %{pkidir}/tls/certs/%{classic_tls_bundle}.rpmsave; then
    # no backup yet
    if test -e %{pkidir}/tls/certs/%{classic_tls_bundle}; then
      # a file exists
      if ! test -L %{pkidir}/tls/certs/%{classic_tls_bundle}; then
        # it's an old regular file, not a link
        mv -f %{pkidir}/tls/certs/%{classic_tls_bundle} %{pkidir}/tls/certs/%{classic_tls_bundle}.rpmsave
      fi
    fi
  fi

  if ! test -e %{pkidir}/tls/certs/%{openssl_format_trust_bundle}.rpmsave; then
    # no backup yet
    if test -e %{pkidir}/tls/certs/%{openssl_format_trust_bundle}; then
      # a file exists
      if ! test -L %{pkidir}/tls/certs/%{openssl_format_trust_bundle}; then
        # it's an old regular file, not a link
        mv -f %{pkidir}/tls/certs/%{openssl_format_trust_bundle} %{pkidir}/tls/certs/%{openssl_format_trust_bundle}.rpmsave
      fi
    fi
  fi
fi


%post
#if [ $1 -gt 1 ] ; then
#  # when upgrading or downgrading
#fi
# if ln is available, go ahead and run the ca-legacy and update
# scripts. If not, wait until %posttrans.
if [ -x %{_bindir}/ln ]; then
%{_bindir}/ca-legacy install
%{_bindir}/update-ca-trust
fi

%posttrans
# When coreutils is installing with ca-certificates
# we need to wait until coreutils install to
# run our update since update requires ln to complete.
# There is a circular dependency here where
# ca-certificates depends on coreutils
# coreutils depends on openssl
# openssl depends on ca-certificates
# so we run the scripts here too, in case we couldn't run them in
# post. If we *could* run them in post this is an unnecessary
# duplication, but it shouldn't hurt anything
%{_bindir}/ca-legacy install
%{_bindir}/update-ca-trust

# The file .files.txt contains the list of (%ghost )files in the directory-hash
%files -f .files.txt
%dir %{_sysconfdir}/ssl
%dir %{pkidir}/tls
%dir %{pkidir}/tls/certs
%dir %{pkidir}/java
%dir %{catrustdir}
%dir %{catrustdir}/source
%dir %{catrustdir}/source/anchors
%dir %{catrustdir}/source/blocklist
%dir %{catrustdir}/extracted
%dir %{catrustdir}/extracted/pem
%dir %{catrustdir}/extracted/openssl
%dir %{catrustdir}/extracted/java
%dir %{_datadir}/pki
%dir %{_datadir}/pki/ca-trust-source
%dir %{_datadir}/pki/ca-trust-source/anchors
%dir %{_datadir}/pki/ca-trust-source/blocklist
%dir %{_datadir}/pki/ca-trust-legacy
%dir %{catrustdir}/extracted/pem/directory-hash

%config(noreplace) %{catrustdir}/ca-legacy.conf

%{_mandir}/man8/update-ca-trust.8.gz
%{_mandir}/man8/ca-legacy.8.gz
%{_datadir}/pki/ca-trust-source/README
%{catrustdir}/README
%{catrustdir}/extracted/README
%{catrustdir}/extracted/java/README
%{catrustdir}/extracted/openssl/README
%{catrustdir}/extracted/pem/README
%{catrustdir}/extracted/edk2/README
%{catrustdir}/source/README

# symlinks for old locations
%{pkidir}/tls/cert.pem
%{pkidir}/tls/certs/%{classic_tls_bundle}
%{pkidir}/tls/certs/%{openssl_format_trust_bundle}
%{pkidir}/tls/certs/ca-certificates.crt
%{pkidir}/%{java_bundle}
# Hybrid hash directory with bundle file for Debian compatibility
# See https://bugzilla.redhat.com/show_bug.cgi?id=1053882
%{_sysconfdir}/ssl/certs
%{_sysconfdir}/ssl/README
%{_sysconfdir}/ssl/cert.pem
%{_sysconfdir}/ssl/openssl.cnf
%{_sysconfdir}/ssl/ct_log_list.cnf

# primary bundle file with trust
%{_datadir}/pki/ca-trust-source/%{p11_format_bundle}

%{_datadir}/pki/ca-trust-legacy/%{legacy_default_bundle}
%{_datadir}/pki/ca-trust-legacy/%{legacy_disable_bundle}
# update/extract tool
%{_bindir}/update-ca-trust
%{_bindir}/ca-legacy
%ghost %{catrustdir}/source/ca-bundle.legacy.crt
# files extracted files
%ghost %{catrustdir}/extracted/pem/tls-ca-bundle.pem
%ghost %{catrustdir}/extracted/pem/email-ca-bundle.pem
%ghost %{catrustdir}/extracted/pem/objsign-ca-bundle.pem
%ghost %{catrustdir}/extracted/openssl/%{openssl_format_trust_bundle}
%ghost %{catrustdir}/extracted/%{java_bundle}
%ghost %{catrustdir}/extracted/edk2/cacerts.bin

%changelog
* Tue Aug 26 2025 Frantisek Krenzelok <fkrenzel@redhat.com> - 2025.2.80_v9.0.304-1.1
- Revert the "Dropping of cert.pem file" change to restore legacy CA symlinks
- https://fedoraproject.org/wiki/Changes/droppingOfCertPemFile
- Restored directory /etc/pki/ca-trust/extracted/openssl
- Remove update-ca-trust extract compatibility option
- Restored symlinks:
    - /etc/pki/tls/cert.pem
    - /etc/pki/tls/certs/ca-certificates.crt
    - /etc/pki/tls/certs/ca-bundle.trust.crt
    - /etc/pki/tls/certs/ca-bundle.crt
    - /etc/ssl/cert.pem
    - /etc/ssl/certs/ca-certificates.crt
    - /etc/ssl/certs/ca-bundle.trust.crt
    - /etc/ssl/certs/ca-bundle.crt

*Tue Aug 26 2025 rhel-developer-toolbox <krenzelok.frantisek@gmail.com> - 2025.2.80_v9.0.304-1.0
- Update to CKBI 2.80_v9.0.304 from NSS 3.114
-    Adding:
-     # Certificate "TWCA CYBER Root CA"
-     # Certificate "TWCA Global Root CA G2"
-     # Certificate "SecureSign Root CA12"
-     # Certificate "SecureSign Root CA14"
-     # Certificate "SecureSign Root CA15"
-     # Certificate "D-TRUST BR Root CA 2 2023"
-     # Certificate "TrustAsia SMIME ECC Root CA"
-     # Certificate "TrustAsia SMIME RSA Root CA"
-     # Certificate "TrustAsia TLS ECC Root CA"
-     # Certificate "TrustAsia TLS RSA Root CA"
-     # Certificate "D-TRUST EV Root CA 2 2023"
-     # Certificate "SwissSign RSA SMIME Root CA 2022 - 1"
-     # Certificate "SwissSign RSA TLS Root CA 2022 - 1"

* Tue Aug 12 2025 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.69_v8.0.401-8
- update-ca-trust: Added a temporary, compatibility option `--rhbz2387674` to
  the `extract` command. This flag restores legacy certificate
  symlinks (e.g., `/etc/ssl/cert.pem`) to address issues with older software
  that has not yet adapted to their removal. This essentially provides a
  temporary way to revert the "Dropping of cert.pem file".

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024.2.69_v8.0.401-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 9 2025 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.69_v8.0.401-6
- Change: Dropping of cert.pem file (Resolves: rhbz#2360110)
  https://fedoraproject.org/wiki/Changes/dropingOfCertPemFile
- Remove the following symlinks:
-    # /etc/pki/tls/cert.pem
-    # /etc/pki/tls/certs/ca-certificates.crt
-    # /etc/pki/tls/certs/ca-bundle.trust.crt
-    # /etc/pki/tls/certs/ca-bundle.crt
-    # /etc/ssl/cert.pem
-    # /etc/ssl/certs/ca-certificates.crt
-    # /etc/ssl/certs/ca-bundle.trust.crt
-    # /etc/ssl/certs/ca-bundle.crt
- Directory /etc/pki/ca-trust/extracted/openssl is being deprecated,
  it is removed upon updating unless there are files present inside it.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024.2.69_v8.0.401-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

*Tue Dec 17 2024 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.69_v8.0.401-4
- Bring back /etc/pki/tls/certs/ca-certificates.crt

*Fri Sep 27 2024 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.69_v8.0.401-3
- Bring back /etc/pki/tls/cert.pem

*Fri Sep 27 2024 Michel Lind <salimma@fedoraproject.org> - 2024.2.69_v8.0.401-2
- Add missing Requires(post) on findutils for update-ca-trust
- Fixes: RHBZ#2315320

*Mon Sep 23 2024 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.69_v8.0.401-1
- Update to CKBI 2.69_v8.0.401 from NSS 3.103
-    Adding:
-     # Certificate "Sectigo Public Code Signing Root R46"
-     # Certificate "Sectigo Public Code Signing Root E46"

*Wed Aug 28 2024 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.69_v8.0.303-5
- update-ca-trust: copy directory-hash symlinks to /etc/pki/tls/certs
- Remove /etc/pki/tls/cert.pem symlink so that it isn't loaded by default

*Tue Aug 27 2024 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.69_v8.0.303-5
- update-ca-trust: return warnings on a unsupported argument instead of error

*Tue Aug 27 2024 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.69_v8.0.303-5
- Temporarily generate the directory-hash files in %%install ...(next item)
- Add list of ghost files from directory-hash to %%files

*Mon Jul 29 2024 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.68_v8.0.302-5
- Add libffi to required packages

*Thu Jul 18 2024 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.68_v8.0.302-4
- Remove blacklist use blocklist-only.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.2.68_v8.0.302-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

*Tue Jun 18 2024 Frantisek Krenzelok <fkrenzel@redhat.com> - 2024.2.68_v8.0.302-2
- Update to CKBI 2.68_v8.0.302 from NSS 3.101
-    Removing:
-     # Certificate "Verisign Class 1 Public Primary Certification Authority - G3"
-     # Certificate "Verisign Class 2 Public Primary Certification Authority - G3"
-     # Certificate "Security Communication Root CA"
-     # Certificate "Autoridad de Certificacion Firmaprofesional CIF A62634068"
-     # Certificate "Symantec Class 1 Public Primary Certification Authority - G6"
-     # Certificate "Symantec Class 2 Public Primary Certification Authority - G6"
-     # Certificate "TrustCor RootCert CA-1"
-     # Certificate "TrustCor RootCert CA-2"
-     # Certificate "TrustCor ECA-1"
-    Adding:
-     # Certificate "TrustAsia Global Root CA G3"
-     # Certificate "TrustAsia Global Root CA G4"
-     # Certificate "CommScope Public Trust ECC Root-01"
-     # Certificate "CommScope Public Trust ECC Root-02"
-     # Certificate "CommScope Public Trust RSA Root-01"
-     # Certificate "CommScope Public Trust RSA Root-02"
-     # Certificate "D-Trust SBR Root CA 1 2022"
-     # Certificate "D-Trust SBR Root CA 2 2022"
-     # Certificate "Telekom Security SMIME ECC Root 2021"
-     # Certificate "Telekom Security TLS ECC Root 2020"
-     # Certificate "Telekom Security SMIME RSA Root 2023"
-     # Certificate "Telekom Security TLS RSA Root 2023"
-     # Certificate "FIRMAPROFESIONAL CA ROOT-A WEB"
-     # Certificate "SECOM Trust.net"
-     # Certificate "VeriSign Class 2 Public Primary Certification Authority - G3"
-     # Certificate "SSL.com Code Signing RSA Root CA 2022"
-     # Certificate "SSL.com Code Signing ECC Root CA 2022"

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.2.62_v7.0.401-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.2.62_v7.0.401-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 09 2023 Robert Relyea <rrelyea@redhat.com> 2023.2.62_v7.0.401-4
- update-ca-trust: Fix bug in update-ca-trust so we don't depened on util-unix

* Sat Oct 07 2023 Adam Williamson <awilliam@redhat.com> - 2023.2.62_v7.0.401-3
- Skip %post if getopt is missing (recent change made update-ca-trust use it)

*Wed Oct 04 2023 Robert Relyea <rrelyea@redhat.com> 2023.2.62_v7.0.401-2
 - Update to CKBI 2.62_v7.0.401 from NSS 3.93
   Removing: 
    # Certificate "Camerfirma Chambers of Commerce Root"
    # Certificate "Hongkong Post Root CA 1"
    # Certificate "FNMT-RCM"
   Adding: 
    # Certificate "LAWtrust Root CA2 (4096)"
    # Certificate "Sectigo Public Email Protection Root E46"
    # Certificate "Sectigo Public Email Protection Root R46"
    # Certificate "Sectigo Public Server Authentication Root E46"
    # Certificate "Sectigo Public Server Authentication Root R46"
    # Certificate "SSL.com TLS RSA Root CA 2022"
    # Certificate "SSL.com TLS ECC Root CA 2022"
    # Certificate "SSL.com Client ECC Root CA 2022"
    # Certificate "SSL.com Client RSA Root CA 2022"
    # Certificate "Atos TrustedRoot Root CA ECC G2 2020"
    # Certificate "Atos TrustedRoot Root CA RSA G2 2020"
    # Certificate "Atos TrustedRoot Root CA ECC TLS 2021"
    # Certificate "Atos TrustedRoot Root CA RSA TLS 2021"
    # Certificate "Chambers of Commerce Root"

* Fri Sep 29 2023 Clemens Lang <cllang@redhat.com> - 2023.2.60_v7.0.306-4
- update-ca-trust: Support --output and non-root operation (rhbz#2241240)

*Thu Sep 07 2023 Robert Relyea <rrelyea@redhat.com> - 2023.2.60_v7.0.306-3
- update License: field to SPDX

*Tue Aug 01 2023 Robert Relyea <rrelyea@redhat.com> - 2023.2.60_v7.0.306-2
- Update to CKBI 2.60_v7.0.306 from NSS 3.91
-    Removing:
-     # Certificate "OpenTrust Root CA G1"
-     # Certificate "Swedish Government Root Authority v1"
-     # Certificate "DigiNotar Root CA G2"
-     # Certificate "Federal Common Policy CA"
-     # Certificate "TC TrustCenter Universal CA III"
-     # Certificate "CCA India 2007"
-     # Certificate "ipsCA Global CA Root"
-     # Certificate "ipsCA Main CA Root"
-     # Certificate "Macao Post eSignTrust Root Certification Authority"
-     # Certificate "InfoNotary CSP Root"
-     # Certificate "DigiNotar Root CA"
-     # Certificate "Root CA"
-     # Certificate "GPKIRootCA"
-     # Certificate "D-TRUST Qualified Root CA 1 2007:PN"
-     # Certificate "TC TrustCenter Universal CA I"
-     # Certificate "TC TrustCenter Universal CA II"
-     # Certificate "TC TrustCenter Class 2 CA II"
-     # Certificate "TC TrustCenter Class 4 CA II"
-     # Certificate "TÜRKTRUST Elektronik Sertifika Hizmet Sağlayıcısı"
-     # Certificate "CertRSA01"
-     # Certificate "KISA RootCA 3"
-     # Certificate "A-CERT ADVANCED"
-     # Certificate "A-Trust-Qual-01"
-     # Certificate "A-Trust-nQual-01"
-     # Certificate "Serasa Certificate Authority II"
-     # Certificate "TDC Internet"
-     # Certificate "America Online Root Certification Authority 2"
-     # Certificate "RSA Security Inc"
-     # Certificate "Public Notary Root"
-     # Certificate "Autoridade Certificadora Raiz Brasileira"
-     # Certificate "Post.Trust Root CA"
-     # Certificate "Entrust.net Secure Server Certification Authority"
-     # Certificate "ePKI EV SSL Certification Authority - G1"
-    Adding:
-     # Certificate "BJCA Global Root CA1"
-     # Certificate "BJCA Global Root CA2"
-     # Certificate "Symantec Enterprise Mobile Root for Microsoft"
-     # Certificate "A-Trust-Root-05"
-     # Certificate "ADOCA02"
-     # Certificate "StartCom Certification Authority G2"
-     # Certificate "ATHEX Root CA"
-     # Certificate "EBG Elektronik Sertifika Hizmet Sağlayıcısı"
-     # Certificate "GeoTrust Primary Certification Authority"
-     # Certificate "thawte Primary Root CA"
-     # Certificate "VeriSign Class 3 Public Primary Certification Authority - G5"
-     # Certificate "America Online Root Certification Authority 1"
-     # Certificate "Juur-SK"
-     # Certificate "ComSign CA"
-     # Certificate "ComSign Secured CA"
-     # Certificate "ComSign Advanced Security CA"
-     # Certificate "Sonera Class2 CA"
-     # Certificate "VeriSign Class 3 Public Primary Certification Authority - G3"
-     # Certificate "VeriSign, Inc."
-     # Certificate "GTE CyberTrust Global Root"
-     # Certificate "Equifax Secure Global eBusiness CA-1"
-     # Certificate "Equifax"
-     # Certificate "Class 1 Primary CA"
-     # Certificate "Swiss Government Root CA III"
-     # Certificate "Application CA G4 Root"
-     # Certificate "SSC GDL CA Root A"
-     # Certificate "GlobalSign Code Signing Root E45"
-     # Certificate "GlobalSign Code Signing Root R45"
-     # Certificate "Entrust Code Signing Root Certification Authority - CSBR1"

*Tue Jul 25 2023 Robert Relyea <rrelyea@redhat.com> - 2023.2.60-3
- Fedora mass rebuild

*Fri Jan 20 2023 Frantisek Krenzelok <krenzelok.frantisek@gmail.com> - 2023.2.60-2
- Update to CKBI 2.60 from NSS 3.86
-    Removing:
-     # Certificate "Camerfirma Global Chambersign Root"
-     # Certificate "Staat der Nederlanden EV Root CA"
-    Adding:
-     # Certificate "DigiCert TLS ECC P384 Root G5"
-     # Certificate "DigiCert TLS RSA4096 Root G5"
-     # Certificate "DigiCert SMIME ECC P384 Root G5"
-     # Certificate "DigiCert SMIME RSA4096 Root G5"
-     # Certificate "Certainly Root R1"
-     # Certificate "Certainly Root E1"
-     # Certificate "E-Tugra Global Root CA RSA v3"
-     # Certificate "E-Tugra Global Root CA ECC v3"
-     # Certificate "DIGITALSIGN GLOBAL ROOT RSA CA"
-     # Certificate "DIGITALSIGN GLOBAL ROOT ECDSA CA"
-     # Certificate "Global Chambersign Root"

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2022.2.54-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

*Thu Jul 28 2022 Bob Relyea <rrelyea@redhat.com> - 2022.2.54-5
- Update to CKBI 2.54 from NSS 3.79
-    Removing:
-     # Certificate "TrustCor ECA-1"
-     # Certificate "TrustCor RootCert CA-2"
-     # Certificate "TrustCor RootCert CA-1"
-     # Certificate "Network Solutions Certificate Authority"
-     # Certificate "COMODO Certification Authority"
-     # Certificate "Autoridad de Certificacion Raiz del Estado Venezolano"
-     # Certificate "Microsec e-Szigno Root CA 2009"
-     # Certificate "TWCA Root Certification Authority"
-     # Certificate "Izenpe.com"
-     # Certificate "state-institutions"
-     # Certificate "GlobalSign"
-     # Certificate "Common Policy"
-     # Certificate "A-Trust-nQual-03"
-     # Certificate "A-Trust-Qual-02"
-     # Certificate "Autoridad de Certificacion Firmaprofesional CIF A62634068"
-     # Certificate "Government Root Certification Authority"
-     # Certificate "AC Raíz Certicámara S.A."

*Wed Jul 27 2022 Bob Relyea <rrelyea@redhat.com> - 2022.2.54-4
- Update to CKBI 2.54 from NSS 3.79

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.2.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

*Fri Jul 15 2022 Bob Relyea <rrelyea@redhat.com> - 2022.2.54-2
- Update to CKBI 2.54 from NSS 3.79
-    Removing:
-     # Certificate "GlobalSign Root CA - R2"
-     # Certificate "DST Root CA X3"
-     # Certificate "Explicitly Distrusted DigiNotar PKIoverheid G2"
-    Adding:
-     # Certificate "Autoridad de Certificacion Firmaprofesional CIF A62634068"
-     # Certificate "vTrus ECC Root CA"
-     # Certificate "vTrus Root CA"
-     # Certificate "ISRG Root X2"
-     # Certificate "HiPKI Root CA - G1"
-     # Certificate "Telia Root CA v2"
-     # Certificate "D-TRUST BR Root CA 1 2020"
-     # Certificate "D-TRUST EV Root CA 1 2020"
-     # Certificate "CAEDICOM Root"
-     # Certificate "I.CA Root CA/RSA"
-     # Certificate "MULTICERT Root Certification Authority 01"
-     # Certificate "Certification Authority of WoSign G2"
-     # Certificate "CA WoSign ECC Root"
-     # Certificate "CCA India 2015 SPL"
-     # Certificate "Swedish Government Root Authority v3"
-     # Certificate "Swedish Government Root Authority v2"
-     # Certificate "Tunisian Root Certificate Authority - TunRootCA2"
-     # Certificate "OpenTrust Root CA G1"
-     # Certificate "OpenTrust Root CA G2"
-     # Certificate "OpenTrust Root CA G3"
-     # Certificate "Certplus Root CA G1"
-     # Certificate "Certplus Root CA G2"
-     # Certificate "Government Root Certification Authority"
-     # Certificate "A-Trust-Qual-02"
-     # Certificate "Thailand National Root Certification Authority - G1"
-     # Certificate "TrustCor ECA-1"
-     # Certificate "TrustCor RootCert CA-2"
-     # Certificate "TrustCor RootCert CA-1"
-     # Certificate "Certification Authority of WoSign"
-     # Certificate "CA 沃通根证书"
-     # Certificate "SSC GDL CA Root B"
-     # Certificate "SAPO Class 2 Root CA"
-     # Certificate "SAPO Class 3 Root CA"
-     # Certificate "SAPO Class 4 Root CA"
-     # Certificate "CA Disig Root R1"
-     # Certificate "Autoridad Certificadora Raíz Nacional de Uruguay"
-     # Certificate "ApplicationCA2 Root"
-     # Certificate "GlobalSign"
-     # Certificate "Symantec Class 3 Public Primary Certification Authority - G6"
-     # Certificate "Symantec Class 3 Public Primary Certification Authority - G4"
-     # Certificate "Halcom Root CA"
-     # Certificate "Swisscom Root EV CA 2"
-     # Certificate "CFCA GT CA"
-     # Certificate "Digidentity L3 Root CA - G2"
-     # Certificate "SITHS Root CA v1"
-     # Certificate "Macao Post eSignTrust Root Certification Authority (G02)"
-     # Certificate "Autoridade Certificadora Raiz Brasileira v2"
-     # Certificate "Swisscom Root CA 2"
-     # Certificate "IGC/A AC racine Etat francais"
-     # Certificate "PersonalID Trustworthy RootCA 2011"
-     # Certificate "Swedish Government Root Authority v1"
-     # Certificate "Swiss Government Root CA II"
-     # Certificate "Swiss Government Root CA I"
-     # Certificate "Network Solutions Certificate Authority"
-     # Certificate "COMODO Certification Authority"
-     # Certificate "LuxTrust Global Root"
-     # Certificate "AC1 RAIZ MTIN"
-     # Certificate "Microsoft Root Certificate Authority 2011"
-     # Certificate "CCA India 2011"
-     # Certificate "ANCERT Certificados Notariales V2"
-     # Certificate "ANCERT Certificados CGN V2"
-     # Certificate "EE Certification Centre Root CA"
-     # Certificate "DigiNotar Root CA G2"
-     # Certificate "Federal Common Policy CA"
-     # Certificate "Autoridad de Certificacion Raiz del Estado Venezolano"
-     # Certificate "Autoridad de Certificacion Raiz del Estado Venezolano"
-     # Certificate "China Internet Network Information Center EV Certificates Root"
-     # Certificate "Verizon Global Root CA"
-     # Certificate "SwissSign Silver Root CA - G3"
-     # Certificate "SwissSign Platinum Root CA - G3"
-     # Certificate "SwissSign Gold Root CA - G3"
-     # Certificate "Microsec e-Szigno Root CA 2009"
-     # Certificate "SITHS CA v3"
-     # Certificate "Certinomis - Autorité Racine"
-     # Certificate "ANF Server CA"
-     # Certificate "Thawte Premium Server CA"
-     # Certificate "Thawte Server CA"
-     # Certificate "TC TrustCenter Universal CA III"
-     # Certificate "KEYNECTIS ROOT CA"
-     # Certificate "I.CA - Standard Certification Authority, 09/2009"
-     # Certificate "I.CA - Qualified Certification Authority, 09/2009"
-     # Certificate "VI Registru Centras RCSC (RootCA)"
-     # Certificate "CCA India 2007"
-     # Certificate "Autoridade Certificadora Raiz Brasileira v1"
-     # Certificate "ipsCA Global CA Root"
-     # Certificate "ipsCA Main CA Root"
-     # Certificate "Actalis Authentication CA G1"
-     # Certificate "A-Trust-Qual-03"
-     # Certificate "AddTrust External CA Root"
-     # Certificate "ECRaizEstado"
-     # Certificate "Configuration"
-     # Certificate "FNMT-RCM"
-     # Certificate "StartCom Certification Authority"
-     # Certificate "TWCA Root Certification Authority"
-     # Certificate "VeriSign Class 3 Public Primary Certification Authority - G4"
-     # Certificate "thawte Primary Root CA - G2"
-     # Certificate "GeoTrust Primary Certification Authority - G2"
-     # Certificate "VeriSign Universal Root Certification Authority"
-     # Certificate "thawte Primary Root CA - G3"
-     # Certificate "GeoTrust Primary Certification Authority - G3"
-     # Certificate "E-ME SSI (RCA)"
-     # Certificate "ACEDICOM Root"
-     # Certificate "Autoridad Certificadora Raiz de la Secretaria de Economia"
-     # Certificate "Correo Uruguayo - Root CA"
-     # Certificate "CNNIC ROOT"
-     # Certificate "Common Policy"
-     # Certificate "Macao Post eSignTrust Root Certification Authority"
-     # Certificate "Staat der Nederlanden Root CA - G2"
-     # Certificate "NetLock Platina (Class Platinum) Főtanúsítvány"
-     # Certificate "AC Raíz Certicámara S.A."
-     # Certificate "Cisco Root CA 2048"
-     # Certificate "CA Disig"
-     # Certificate "InfoNotary CSP Root"
-     # Certificate "UCA Global Root"
-     # Certificate "UCA Root"
-     # Certificate "DigiNotar Root CA"
-     # Certificate "Starfield Services Root Certificate Authority"
-     # Certificate "I.CA - Qualified root certificate"
-     # Certificate "I.CA - Standard root certificate"
-     # Certificate "e-Guven Kok Elektronik Sertifika Hizmet Saglayicisi"
-     # Certificate "Japanese Government"
-     # Certificate "AdminCA-CD-T01"
-     # Certificate "Admin-Root-CA"
-     # Certificate "Izenpe.com"
-     # Certificate "TÜBİTAK UEKAE Kök Sertifika Hizmet Sağlayıcısı - Sürüm 3"
-     # Certificate "Halcom CA FO"
-     # Certificate "Halcom CA PO 2"
-     # Certificate "Root CA"
-     # Certificate "GPKIRootCA"
-     # Certificate "ACNLB"
-     # Certificate "state-institutions"
-     # Certificate "state-institutions"
-     # Certificate "SECOM Trust Systems CO.,LTD."
-     # Certificate "D-TRUST Qualified Root CA 1 2007:PN"
-     # Certificate "D-TRUST Root Class 2 CA 2007"
-     # Certificate "D-TRUST Root Class 3 CA 2007"
-     # Certificate "SSC Root CA A"
-     # Certificate "SSC Root CA B"
-     # Certificate "SSC Root CA C"
-     # Certificate "Autoridad de Certificacion de la Abogacia"
-     # Certificate "Root CA Generalitat Valenciana"
-     # Certificate "VAS Latvijas Pasts SSI(RCA)"
-     # Certificate "ANCERT Certificados CGN"
-     # Certificate "ANCERT Certificados Notariales"
-     # Certificate "ANCERT Corporaciones de Derecho Publico"
-     # Certificate "GLOBALTRUST"
-     # Certificate "Certipost E-Trust TOP Root CA"
-     # Certificate "Certipost E-Trust Primary Qualified CA"
-     # Certificate "Certipost E-Trust Primary Normalised CA"
-     # Certificate "GlobalSign"
-     # Certificate "IGC/A"
-     # Certificate "S-TRUST Authentication and Encryption Root CA 2005:PN"
-     # Certificate "TC TrustCenter Universal CA I"
-     # Certificate "TC TrustCenter Universal CA II"
-     # Certificate "TC TrustCenter Class 2 CA II"
-     # Certificate "TC TrustCenter Class 4 CA II"
-     # Certificate "Swisscom Root CA 1"
-     # Certificate "Microsec e-Szigno Root CA"
-     # Certificate "LGPKI"
-     # Certificate "AC RAIZ DNIE"
-     # Certificate "Common Policy"
-     # Certificate "TÜRKTRUST Elektronik Sertifika Hizmet Sağlayıcısı"
-     # Certificate "A-Trust-nQual-03"
-     # Certificate "A-Trust-nQual-03"
-     # Certificate "CertRSA01"
-     # Certificate "KISA RootCA 1"
-     # Certificate "KISA RootCA 3"
-     # Certificate "NetLock Minositett Kozjegyzoi (Class QA) Tanusitvanykiado"
-     # Certificate "A-CERT ADVANCED"
-     # Certificate "A-Trust-Qual-01"
-     # Certificate "A-Trust-nQual-01"
-     # Certificate "A-Trust-Qual-02"
-     # Certificate "Staat der Nederlanden Root CA"
-     # Certificate "Serasa Certificate Authority II"
-     # Certificate "TDC Internet"
-     # Certificate "America Online Root Certification Authority 2"
-     # Certificate "Autoridad de Certificacion Firmaprofesional CIF A62634068"
-     # Certificate "Government Root Certification Authority"
-     # Certificate "RSA Security Inc"
-     # Certificate "Public Notary Root"
-     # Certificate "GeoTrust Global CA"
-     # Certificate "GeoTrust Global CA 2"
-     # Certificate "GeoTrust Universal CA"
-     # Certificate "GeoTrust Universal CA 2"
-     # Certificate "QuoVadis Root Certification Authority"
-     # Certificate "Autoridade Certificadora Raiz Brasileira"
-     # Certificate "Post.Trust Root CA"
-     # Certificate "Microsoft Root Authority"
-     # Certificate "Microsoft Root Certificate Authority"
-     # Certificate "Microsoft Root Certificate Authority 2010"
-     # Certificate "Entrust.net Secure Server Certification Authority"
-     # Certificate "UTN-USERFirst-Object"
-     # Certificate "BYTE Root Certification Authority 001"
-     # Certificate "CISRCA1"
-     # Certificate "ePKI Root Certification Authority - G2"
-     # Certificate "ePKI EV SSL Certification Authority - G1"
-     # Certificate "AC Raíz Certicámara S.A."
-     # Certificate "SSL.com EV Root Certification Authority RSA"
-     # Certificate "LuxTrust Global Root 2"
-     # Certificate "ACA ROOT"
-     # Certificate "Security Communication ECC RootCA1"
-     # Certificate "Security Communication RootCA3"
-     # Certificate "CHAMBERS OF COMMERCE ROOT - 2016"
-     # Certificate "Network Solutions RSA Certificate Authority"
-     # Certificate "Network Solutions ECC Certificate Authority"
-     # Certificate "Australian Defence Public Root CA"
-     # Certificate "SI-TRUST Root"
-     # Certificate "Halcom Root Certificate Authority"
-     # Certificate "Application CA G3 Root"
-     # Certificate "GLOBALTRUST 2015"
-     # Certificate "Microsoft ECC Product Root Certificate Authority 2018"
-     # Certificate "emSign Root CA - G2"
-     # Certificate "emSign Root CA - C2"
-     # Certificate "Microsoft ECC TS Root Certificate Authority 2018"
-     # Certificate "DigiCert CS ECC P384 Root G5"
-     # Certificate "DigiCert CS RSA4096 Root G5"
-     # Certificate "DigiCert RSA4096 Root G5"
-     # Certificate "DigiCert ECC P384 Root G5"
-     # Certificate "HARICA Code Signing RSA Root CA 2021"
-     # Certificate "HARICA Code Signing ECC Root CA 2021"
-     # Certificate "Microsoft Identity Verification Root Certificate Authority 2020"

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2021.2.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

*Mon Dec 13 2021 Bob Relyea <rrelyea@redhat.com> - 2021.2.52-2
- Update to CKBI 2.52 from NSS 3.72
-    Adding:
-     # Certificate "TunTrust Root CA"
-     # Certificate "HARICA TLS RSA Root CA 2021"
-     # Certificate "HARICA TLS ECC Root CA 2021"
-     # Certificate "HARICA Client RSA Root CA 2021"
-     # Certificate "HARICA Client ECC Root CA 2021"

*Mon Dec 6 2021 Bob Relyea <rrelyea@redhat.com> - 2021.2.50-5
- integrate Adam William's /etc/ssl/certs with Debian-compatibility
- back out blocklist change since p11-kit .24 is not yet available on rawhide

*Mon Nov 1 2021 Bob Relyea <rrelyea@redhat.com> - 2021.2.50-4
- remove blacklist directory now that pk11-kit is using blocklist

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.2.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

*Wed Jun 16 2021 Bob Relyea <rrelyea@redhat.com> - 2021.2.50-2
- Update to CKBI 2.50 from NSS 3.67
-    Removing:
-     # Certificate "Trustis FPS Root CA"
-     # Certificate "GlobalSign Code Signing Root R45"
-     # Certificate "GlobalSign Code Signing Root E45"
-     # Certificate "Halcom Root Certificate Authority"
-     # Certificate "Symantec Class 3 Public Primary Certification Authority - G6"
-     # Certificate "GLOBALTRUST"
-     # Certificate "MULTICERT Root Certification Authority 01"
-     # Certificate "Verizon Global Root CA"
-     # Certificate "Tunisian Root Certificate Authority - TunRootCA2"
-     # Certificate "CAEDICOM Root"
-     # Certificate "COMODO Certification Authority"
-     # Certificate "Security Communication ECC RootCA1"
-     # Certificate "Security Communication RootCA3"
-     # Certificate "AC RAIZ DNIE"
-     # Certificate "VeriSign Class 3 Public Primary Certification Authority - G3"
-     # Certificate "VeriSign Class 3 Public Primary Certification Authority - G5"
-     # Certificate "VeriSign Universal Root Certification Authority"
-     # Certificate "GeoTrust Global CA"
-     # Certificate "GeoTrust Primary Certification Authority"
-     # Certificate "thawte Primary Root CA"
-     # Certificate "thawte Primary Root CA - G2"
-     # Certificate "thawte Primary Root CA - G3"
-     # Certificate "GeoTrust Primary Certification Authority - G3"
-     # Certificate "GeoTrust Primary Certification Authority - G2"
-     # Certificate "GeoTrust Universal CA"
-     # Certificate "NetLock Platina (Class Platinum) Főtanúsítvány"
-     # Certificate "GLOBALTRUST 2015"
-     # Certificate "emSign Root CA - G2"
-     # Certificate "emSign Root CA - C2"
-    Adding:
-     # Certificate "GLOBALTRUST 2020"
-     # Certificate "ANF Secure Server Root CA"

*Tue May 25 2021 Bob Relyea <rrelyea@redhat.com> - 2021.2.48-2
- Update to CKBI 2.48 from NSS 3.64
-    Removing:
-     # Certificate "Verisign Class 3 Public Primary Certification Authority - G3"
-     # Certificate "GeoTrust Universal CA 2"
-     # Certificate "QuoVadis Root CA"
-     # Certificate "Sonera Class 2 Root CA"
-     # Certificate "Taiwan GRCA"
-     # Certificate "VeriSign Class 3 Public Primary Certification Authority - G4"
-     # Certificate "EE Certification Centre Root CA"
-     # Certificate "LuxTrust Global Root 2"
-     # Certificate "Symantec Class 1 Public Primary Certification Authority - G4"
-     # Certificate "Symantec Class 2 Public Primary Certification Authority - G4"
-    Adding:
-     # Certificate "Microsoft ECC Root Certificate Authority 2017"
-     # Certificate "Microsoft RSA Root Certificate Authority 2017"
-     # Certificate "e-Szigno Root CA 2017"
-     # Certificate "certSIGN Root CA G2"
-     # Certificate "Trustwave Global Certification Authority"
-     # Certificate "Trustwave Global ECC P256 Certification Authority"
-     # Certificate "Trustwave Global ECC P384 Certification Authority"
-     # Certificate "NAVER Global Root Certification Authority"
-     # Certificate "AC RAIZ FNMT-RCM SERVIDORES SEGUROS"
-     # Certificate "GlobalSign Secure Mail Root R45"
-     # Certificate "GlobalSign Secure Mail Root E45"
-     # Certificate "GlobalSign Root R46"
-     # Certificate "GlobalSign Root E46"
-     # Certificate "Certum EC-384 CA"
-     # Certificate "Certum Trusted Root CA"
-     # Certificate "GlobalSign Code Signing Root R45"
-     # Certificate "GlobalSign Code Signing Root E45"
-     # Certificate "Halcom Root Certificate Authority"
-     # Certificate "Symantec Class 3 Public Primary Certification Authority - G6"
-     # Certificate "GLOBALTRUST"
-     # Certificate "MULTICERT Root Certification Authority 01"
-     # Certificate "Verizon Global Root CA"
-     # Certificate "Tunisian Root Certificate Authority - TunRootCA2"
-     # Certificate "CAEDICOM Root"
-     # Certificate "COMODO Certification Authority"
-     # Certificate "Security Communication ECC RootCA1"
-     # Certificate "Security Communication RootCA3"
-     # Certificate "AC RAIZ DNIE"
-     # Certificate "VeriSign Class 3 Public Primary Certification Authority - G3"
-     # Certificate "NetLock Platina (Class Platinum) Főtanúsítvány"
-     # Certificate "GLOBALTRUST 2015"
-     # Certificate "emSign Root CA - G2"
-     # Certificate "emSign Root CA - C2"

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020.2.41-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Bob Relyea <rrelyea@redhat.com> - 2020.2.41-6
- remove unnecessarily divisive terms, take 1.
-   in ca-certificates there are 3 cases:
-   1) master refering to the fedora master branch in the fetch.sh script.
-      This can only be changed once fedora changes the master branch name.
-   2) a reference to the 'master bundle' in this file: this has been changed
-      to 'primary bundle'.
-   3) a couple of blacklist directories owned by this package, but used to
-      p11-kit. New 'blocklist' directories have been created, but p11-kit
-      needs to be updated before the old blacklist directories can be removed
-      and the man pages corrected.

* Mon Nov 09 2020 Christian Heimes <cheimes@redhat.com> - 2020.2.41-5
- Add cross-distro compatibility symlinks to /etc/ssl (rhbz#1895619)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.2.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Adam Williamson <awilliam@redhat.com> - 2020.2.41-3
- Fix up broken %post and %postinstall scriptlet changes from -2

* Wed Jun 10 2020 Bob Relyea <rrelyea@redhat.com> - 2020.2.41-2
- Update to CKBI 2.41 from NSS 3.53.0
-    Removing:
-     # Certificate "AddTrust Low-Value Services Root"
-     # Certificate "AddTrust External Root"
-     # Certificate "Staat der Nederlanden Root CA - G2"

* Tue Jan 28 2020 Daiki Ueno <dueno@redhat.com> - 2020.2.40-3
- Update versioned dependency on p11-kit

* Wed Jan 22 2020 Daiki Ueno <dueno@redhat.com> - 2020.2.40-2
- Update to CKBI 2.40 from NSS 3.48
-    Removing:
-     # Certificate "UTN USERFirst Email Root CA"
-     # Certificate "Certplus Class 2 Primary CA"
-     # Certificate "Deutsche Telekom Root CA 2"
-     # Certificate "Swisscom Root CA 2"
-     # Certificate "Certinomis - Root CA"
-    Adding:
-     # Certificate "Entrust Root Certification Authority - G4"
- certdata2pem.py: emit flags for CKA_NSS_{SERVER,EMAIL}_DISTRUST_AFTER

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.2.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Bob Relyea <rrelyea@redhat.com> 2019.2.32-2
 - Update to CKBI 2.32 from NSS 3.44
   Removing: 
    # Certificate "Visa eCommerce Root"
    # Certificate "AC Raiz Certicamara S.A."
    # Certificate "Certplus Root CA G1"
    # Certificate "Certplus Root CA G2"
    # Certificate "OpenTrust Root CA G1"
    # Certificate "OpenTrust Root CA G2"
    # Certificate "OpenTrust Root CA G3"
   Adding: 
    # Certificate "GTS Root R1"
    # Certificate "GTS Root R2"
    # Certificate "GTS Root R3"
    # Certificate "GTS Root R4"
    # Certificate "UCA Global G2 Root"
    # Certificate "UCA Extended Validation Root"
    # Certificate "Certigna Root CA"
    # Certificate "emSign Root CA - G1"
    # Certificate "emSign ECC Root CA - G3"
    # Certificate "emSign Root CA - C1"
    # Certificate "emSign ECC Root CA - C3"
    # Certificate "Hongkong Post Root CA 3"

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.2.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 24 2018 Bob Relyea <rrelyea@redhat.com> - 2018.2.26-2
- Update to CKBI 2.26 from NSS 3.39

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.2.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Kai Engert <kaie@redhat.com> - 2018.2.24-5
- Ported scripts to python3

* Mon Jun 11 2018 Daiki Ueno <dueno@redhat.com> - 2018.2.24-4
- Extract certificate bundle in EDK2 format, suggested by Laszlo Ersek

* Mon Jun 04 2018 Kai Engert <kaie@redhat.com> - 2018.2.24-3
- Adjust ghost file permissions, rhbz#1564432

* Fri May 18 2018 Kai Engert <kaie@redhat.com> - 2018.2.24-2
- Update to CKBI 2.24 from NSS 3.37

* Wed Mar 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2018.2.22-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 23 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 2018.2.22-3
- Add post dep on coreutils for ln(1)

* Tue Feb 06 2018 Kai Engert <kaie@redhat.com> - 2018.2.22-2
- Update to CKBI 2.22 from NSS 3.35

* Mon Jan 22 2018 Kai Engert <kaie@redhat.com> - 2017.2.20-6
- Depend on bash, grep, sed. Required for ca-legacy script execution.
- p11-kit is already required at %%post execution time. (rhbz#1537127)

* Fri Jan 19 2018 Kai Engert <kaie@redhat.com> - 2017.2.20-5
- Use the force, script! (Which sln did by default).

* Fri Jan 19 2018 Kai Engert <kaie@redhat.com> - 2017.2.20-4
- stop using sln in ca-legacy script.

* Fri Jan 19 2018 Kai Engert <kaie@redhat.com> - 2017.2.20-3
- Use ln -s, because sln was removed from glibc. rhbz#1536349

* Mon Nov 27 2017 Kai Engert <kaie@redhat.com> - 2017.2.20-2
- Update to CKBI 2.20 from NSS 3.34.1

* Tue Aug 15 2017 Kai Engert <kaie@redhat.com> - 2017.2.16-4
- Set P11_KIT_NO_USER_CONFIG=1 to prevent p11-kit from reading user
  configuration files (rhbz#1478172).

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Kai Engert <kaie@redhat.com> - 2017.2.16-2
- Update to (yet unreleased) CKBI 2.16 which is planned for NSS 3.32.
  Mozilla removed all trust bits for code signing.

* Wed Apr 26 2017 Kai Engert <kaie@redhat.com> - 2017.2.14-2
- Update to CKBI 2.14 from NSS 3.30.2

* Thu Feb 23 2017 Kai Engert <kaie@redhat.com> - 2017.2.11-5
- For CAs trusted by Mozilla, set attribute nss-mozilla-ca-policy: true
- Set attribute modifiable: false
- Require p11-kit 0.23.4

* Mon Feb 13 2017 Kai Engert <kaie@redhat.com> - 2017.2.11-4
- Changed the packaged bundle to use the flexible p11-kit-object-v1 file format,
  as a preparation to fix bugs in the interaction between p11-kit-trust and
  Mozilla applications, such as Firefox, Thunderbird etc.
- Changed update-ca-trust to add comments to extracted PEM format files.
- Added an utility to help with comparing output of the trust dump command.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Kai Engert <kaie@redhat.com> - 2017.2.11-2
- Update to CKBI 2.11 from NSS 3.28.1

* Thu Sep 29 2016 Kai Engert <kaie@redhat.com> - 2016.2.10-2
- Update to CKBI 2.10 from NSS 3.27

* Tue Aug 16 2016 Kai Engert <kaie@redhat.com> - 2016.2.9-3
- Revert to the unmodified upstream CA list, changing the legacy trust
  to an empty list. Keeping the ca-legacy tool and existing config,
  however, the configuration has no effect after this change.

* Tue Aug 16 2016 Kai Engert <kaie@redhat.com> - 2016.2.9-2
- Update to CKBI 2.9 from NSS 3.26 with legacy modifications

* Fri Jul 15 2016 Kai Engert <kaie@redhat.com> - 2016.2.8-2
- Update to CKBI 2.8 from NSS 3.25 with legacy modifications

* Tue May 10 2016 Kai Engert <kaie@redhat.com> - 2016.2.7-5
- Only create backup files if there is an original file (bug 999017).

* Tue May 10 2016 Kai Engert <kaie@redhat.com> - 2016.2.7-4
- Use sln, not ln, to avoid the dependency on coreutils.

* Mon Apr 25 2016 Kai Engert <kaie@redhat.com> - 2016.2.7-3
- Fix typos in a manual page and in a README file.

* Wed Mar 16 2016 Kai Engert <kaie@redhat.com> - 2016.2.7-2
- Update to CKBI 2.7 from NSS 3.23 with legacy modifications

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2015.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Kai Engert <kaie@redhat.com> - 2015.2.6-2
- Update to CKBI 2.6 from NSS 3.21 with legacy modifications

* Thu Aug 13 2015 Kai Engert <kaie@redhat.com> - 2015.2.5-2
- Update to CKBI 2.5 from NSS 3.19.3 with legacy modifications

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 05 2015 Kai Engert <kaie@redhat.com> - 2015.2.4-2
- Update to CKBI 2.4 from NSS 3.18.1 with legacy modifications

* Tue May 05 2015 Kai Engert <kaie@redhat.com> - 2015.2.3-4
- Fixed a typo in the ca-legacy manual page.

* Tue Mar 31 2015 Kai Engert <kaie@redhat.com> - 2015.2.3-3
- Don't use "enable" as a value for the legacy configuration, instead
  of the value "default", to make it clear that this preference isn't
  a promise to keep certificates enabled, but rather that we only
  keep them enabled as long as it's considered necessary.
- Changed the configuration file, the ca-legacy utility and filenames
  to use the term "default" (instead of the term "enable").
- Added a manual page for the ca-legacy utility.
- Fixed the ca-legacy utility to handle absence of the configuration
  setting and treat absence as the default setting.

* Fri Mar 20 2015 Kai Engert <kaie@redhat.com> - 2015.2.3-2
- Update to CKBI 2.3 from NSS 3.18 with legacy modifications
- Fixed a mistake in the legacy handling of the upstream 2.2 release:
  Removed two AOL certificates from the legacy group, because
  upstream didn't remove them as part of phasing out 1024-bit
  certificates, which means it isn't necessary to keep them.
- Fixed a mistake in the legacy handling of the upstream 2.1 release:
  Moved two NetLock certificates into the legacy group.

* Tue Dec 16 2014 Kai Engert <kaie@redhat.com> - 2014.2.2-2
- Update to CKBI 2.2 from NSS 3.17.3 with legacy modifications
- Update project URL
- Cleanup

* Sat Nov 15 2014 Peter Lemenkov <lemenkov@gmail.com> - 2014.2.1-7
- Restore Requires: coreutils

* Fri Nov 14 2014 Peter Lemenkov <lemenkov@gmail.com> - 2014.2.1-6
- A proper fix for rhbz#1158343

* Wed Oct 29 2014 Kai Engert <kaie@redhat.com> - 2014.2.1-5
- add Requires: coreutils (rhbz#1158343)

* Tue Oct 28 2014 Kai Engert <kaie@redhat.com> - 2014.2.1-4
- Introduce the ca-legacy utility and a ca-legacy.conf configuration file.
  By default, legacy roots required for OpenSSL/GnuTLS compatibility
  are kept enabled. Using the ca-legacy utility, the legacy roots can be
  disabled. If disabled, the system will use the trust set as provided
  by the upstream Mozilla CA list. (See also: rhbz#1158197)

* Sun Sep 21 2014 Kai Engert <kaie@redhat.com> - 2014.2.1-3
- Temporarily re-enable several legacy root CA certificates because of
  compatibility issues with software based on OpenSSL/GnuTLS,
  see rhbz#1144808

* Thu Aug 14 2014 Kai Engert <kaie@redhat.com> - 2014.2.1-2
- Update to CKBI 2.1 from NSS 3.16.4
- Fix rhbz#1130226

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.1.97-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Kai Engert <kaie@redhat.com> - 2013.1.97-2
- Update to CKBI 1.97 from NSS 3.16

* Mon Feb 10 2014 Kai Engert <kaie@redhat.com> - 2013.1.96-3
- Remove openjdk build dependency

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 2013.1.96-2
- Own the %%{_datadir}/pki dir.

* Thu Jan 09 2014 Kai Engert <kaie@redhat.com> - 2013.1.96-1
- Update to CKBI 1.96 from NSS 3.15.4

* Tue Dec 17 2013 Kai Engert <kaie@redhat.com> - 2013.1.95-1
- Update to CKBI 1.95 from NSS 3.15.3.1

* Fri Sep 06 2013 Kai Engert <kaie@redhat.com> - 2013.1.94-18
- Update the Entrust root stapled extension for compatibility with 
  p11-kit version 0.19.2, patch by Stef Walter, rhbz#988745

* Tue Sep 03 2013 Kai Engert <kaie@redhat.com> - 2013.1.94-17
- merge manual improvement from f19

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.1.94-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Kai Engert <kaie@redhat.com> - 2013.1.94-15
- clarification updates to manual page

* Mon Jul 08 2013 Kai Engert <kaie@redhat.com> - 2013.1.94-14
- added a manual page and related build requirements
- simplify the README files now that we have a manual page
- set a certificate alias in trusted bundle (thanks to Ludwig Nussel)

* Mon May 27 2013 Kai Engert <kaie@redhat.com> - 2013.1.94-13
- use correct command in README files, rhbz#961809

* Mon May 27 2013 Kai Engert <kaie@redhat.com> - 2013.1.94-12
- update to version 1.94 provided by NSS 3.15 (beta)

* Mon Apr 22 2013 Kai Engert <kaie@redhat.com> - 2012.87-12
- Use both label and serial to identify cert during conversion, rhbz#927601
- Add myself as contributor to certdata2.pem.py and remove use of rcs/ident.
  (thanks to Michael Shuler for suggesting to do so)
- Update source URLs and comments, add source file for version information.

* Tue Mar 19 2013 Kai Engert <kaie@redhat.com> - 2012.87-11
- adjust to changed and new functionality provided by p11-kit 0.17.3
- updated READMEs to describe the new directory-specific treatment of files
- ship a new file that contains certificates with neutral trust
- ship a new file that contains distrust objects, and also staple a 
  basic constraint extension to one legacy root contained in the
  Mozilla CA list
- adjust the build script to dynamically produce most of above files
- add and own the anchors and blacklist subdirectories
- file generate-cacerts.pl is no longer required

* Fri Mar 08 2013 Kai Engert <kaie@redhat.com> - 2012.87-9
- Major rework for the Fedora SharedSystemCertificates feature.
- Only ship a PEM bundle file using the BEGIN TRUSTED CERTIFICATE file format.
- Require the p11-kit package that contains tools to automatically create
  other file format bundles.
- Convert old file locations to symbolic links that point to dynamically
  generated files.
- Old files, which might have been locally modified, will be saved in backup 
  files with .rpmsave extension.
- Added a update-ca-certificates script which can be used to regenerate
  the merged trusted output.
- Refer to the various README files that have been added for more detailed
  explanation of the new system.
- No longer require rsc for building.
- Add explanation for the future version numbering scheme,
  because the old numbering scheme was based on upstream using cvs,
  which is no longer true, and therefore can no longer be used.
- Includes changes from rhbz#873369.

* Thu Mar 07 2013 Kai Engert <kaie@redhat.com> - 2012.87-2.fc19.1
- Ship trust bundle file in /usr/share/pki/ca-trust-source/, temporarily in addition.
  This location will soon become the only place containing this file.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Paul Wouters <pwouters@redhat.com> - 2012.87-1
- Updated to r1.87 to blacklist mis-issued turktrust CA certs

* Wed Oct 24 2012 Paul Wouters <pwouters@redhat.com> - 2012.86-2
- Updated blacklist with 20 entries (Diginotar, Trustwave, Comodo(?)
- Fix to certdata2pem.py to also check for CKT_NSS_NOT_TRUSTED 

* Tue Oct 23 2012 Paul Wouters <pwouters@redhat.com> - 2012.86-1
- update to r1.86

* Mon Jul 23 2012 Joe Orton <jorton@redhat.com> - 2012.85-2
- add openssl to BuildRequires

* Mon Jul 23 2012 Joe Orton <jorton@redhat.com> - 2012.85-1
- update to r1.85

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.81-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 2012.81-1
- update to r1.81

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  9 2011 Joe Orton <jorton@redhat.com> - 2011.80-1
- update to r1.80
- fix handling of certs with dublicate Subject names (#733032)

* Thu Sep  1 2011 Joe Orton <jorton@redhat.com> - 2011.78-1
- update to r1.78, removing trust from DigiNotar root (#734679)

* Wed Aug  3 2011 Joe Orton <jorton@redhat.com> - 2011.75-1
- update to r1.75

* Wed Apr 20 2011 Joe Orton <jorton@redhat.com> - 2011.74-1
- update to r1.74

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Joe Orton <jorton@redhat.com> - 2011.70-1
- update to r1.70

* Tue Nov  9 2010 Joe Orton <jorton@redhat.com> - 2010.65-3
- update to r1.65

* Wed Apr  7 2010 Joe Orton <jorton@redhat.com> - 2010.63-3
- package /etc/ssl/certs symlink for third-party apps (#572725)

* Wed Apr  7 2010 Joe Orton <jorton@redhat.com> - 2010.63-2
- rebuild

* Wed Apr  7 2010 Joe Orton <jorton@redhat.com> - 2010.63-1
- update to certdata.txt r1.63
- use upstream RCS version in Version

* Fri Mar 19 2010 Joe Orton <jorton@redhat.com> - 2010-4
- fix ca-bundle.crt (#575111)

* Thu Mar 18 2010 Joe Orton <jorton@redhat.com> - 2010-3
- update to certdata.txt r1.58
- add /etc/pki/tls/certs/ca-bundle.trust.crt using 'TRUSTED CERTICATE' format
- exclude ECC certs from the Java cacerts database
- catch keytool failures
- fail parsing certdata.txt on finding untrusted but not blacklisted cert

* Fri Jan 15 2010 Joe Orton <jorton@redhat.com> - 2010-2
- fix Java cacert database generation: use Subject rather than Issuer
  for alias name; add diagnostics; fix some alias names.

* Mon Jan 11 2010 Joe Orton <jorton@redhat.com> - 2010-1
- adopt Python certdata.txt parsing script from Debian

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Joe Orton <jorton@redhat.com> 2009-1
- update to certdata.txt r1.53

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 14 2008 Joe Orton <jorton@redhat.com> 2008-7
- update to certdata.txt r1.49

* Wed Jun 25 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 2008-6
- Change generate-cacerts.pl to produce pretty aliases.

* Mon Jun  2 2008 Joe Orton <jorton@redhat.com> 2008-5
- include /etc/pki/tls/cert.pem symlink to ca-bundle.crt

* Tue May 27 2008 Joe Orton <jorton@redhat.com> 2008-4
- use package name for temp dir, recreate it in prep

* Tue May 27 2008 Joe Orton <jorton@redhat.com> 2008-3
- fix source script perms
- mark packaged files as config(noreplace)

* Tue May 27 2008 Joe Orton <jorton@redhat.com> 2008-2
- add (but don't use) mkcabundle.pl
- tweak description
- use /usr/bin/keytool directly; BR java-openjdk

* Tue May 27 2008 Joe Orton <jorton@redhat.com> 2008-1
- Initial build (#448497)
