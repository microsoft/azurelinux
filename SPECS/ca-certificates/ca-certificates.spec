%define pkidir %{_sysconfdir}/pki
%define catrustdir %{pkidir}/ca-trust
%define classic_tls_bundle ca-bundle.crt
%define openssl_format_trust_bundle ca-bundle.trust.crt
%define java_bundle java/cacerts

%define p11_format_base_bundle ca-bundle.trust.base.p11-kit

%define p11_format_microsoft_bundle ca-bundle.trust.microsoft.p11-kit

# List of packages triggering legacy certs generation if 'ca-certificates-legacy'
# is installed.
%global watched_pkgs %{name}, %{name}-base

# Rebuilding cert bundles with source certificates.
%global refresh_bundles \
%{_bindir}/update-ca-trust

# Converts certdata.txt files to p11-kit format bundles.
# Arguments:
# %1 - the source certdata.txt file;
%define convert_certdata() \
WORKDIR=$(basename %{1}.d) \
mkdir -p $WORKDIR/certs \
mkdir $WORKDIR/java \
pushd $WORKDIR/certs \
 pwd $WORKDIR \
 cp %{1} certdata.txt \
 python3 %{SOURCE4} >c2p.log 2>c2p.err \
popd \
%{SOURCE19} $WORKDIR %{openssl_format_trust_bundle} %{SOURCE3}

# Installs bundle files to the right directories.
# Arguments:
# %1 - the source certdata.txt file;
# %2 - output p11-kit format bundle name;
%define install_bundles() \
WORKDIR=$(basename %{1}.d) \
install -p -m 644 $WORKDIR/%{openssl_format_trust_bundle} %{buildroot}%{_datadir}/pki/ca-trust-source/%{2} \
touch -r %{SOURCE23} %{buildroot}%{_datadir}/pki/ca-trust-source/%{2}

Summary:        Certificate Authority certificates
Name:           ca-certificates

# When updating, "Epoch, "Version", AND "Release" tags must be updated in the "prebuilt-ca-certificates*" packages as well.
Epoch:          1
Version:        %{azl}.0.0
Release:        4%{?dist}
License:        MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Security
URL:            https://docs.microsoft.com/en-us/security/trusted-root/program-requirements
Source2:        update-ca-trust
Source3:        trust-fixes
Source4:        certdata2pem.py
Source10:       update-ca-trust.8.txt
Source11:       README.usr
Source12:       README.etc
Source13:       README.extr
Source14:       README.java
Source15:       README.openssl
Source16:       README.pem
Source17:       README.edk2
Source18:       README.src
Source19:       pem2bundle.sh
Source20:       LICENSE
Source21:       certdata.base.txt
Source22:       bundle2pem.sh
# The certdata.microsoft.txt is provided by Microsoft's Trusted Root Program.
Source23:       certdata.microsoft.txt

BuildRequires:  /bin/ln
BuildRequires:  asciidoc
BuildRequires:  coreutils
BuildRequires:  docbook-dtd-xml
BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt
BuildRequires:  openssl
BuildRequires:  perl
BuildRequires:  python3

Requires:       %{name}-shared = %{epoch}:%{version}-%{release}
Requires(post): %{name}-tools = %{epoch}:%{version}-%{release}
Requires(post): coreutils
Requires(postun): %{name}-tools = %{epoch}:%{version}-%{release}

Provides:       ca-certificates-microsoft = %{version}-%{release}
Provides:       ca-certificates-mozilla = %{version}-%{release}

BuildArch:      noarch

%description
The Public Key Inrastructure is used for many security issues in
a Linux system. In order for a certificate to be trusted, it must be
signed by a trusted agent called a Certificate Authority (CA).
The certificates loaded by this section are from the list of CAs trusted
through the Microsoft Trusted Root Program and formats it into a form
used by OpenSSL-1.0.1e. The certificates can also be used by other
applications either directly of indirectly through OpenSSL.

%package shared
Summary:        A set of directories and files required by all certificate packages.
Group:          System Environment/Security

%description shared
%{summary}

%package base
Summary:        Basic set of trusted CAs required to authenticate the packages repository.
Group:          System Environment/Security

Requires:       %{name}-shared = %{epoch}:%{version}-%{release}
Requires(post): %{name}-tools = %{epoch}:%{version}-%{release}
Requires(post): coreutils
Requires(postun): %{name}-tools = %{epoch}:%{version}-%{release}

%description base
%{summary}

%package tools
Summary:        Cert generation tools.
Group:          System Environment/Security

Requires:       p11-kit >= 0.23.10
Requires:       p11-kit-trust >= 0.23.10

%description tools
Set of scripts to generate certificates out of a certdata.txt file.

%package legacy
Summary:        Support for legacy certificates configuration.
Group:          System Environment/Security

Requires:       %{name}-shared = %{epoch}:%{version}-%{release}

%description legacy
Provides a legacy version of ca-bundle.crt in the format of "[hash].0 -> [hash].pem"
pairs under %{pkidir}/tls/certs.

%prep -q
mkdir %{name}

%build
cp -p %{SOURCE20} .

%convert_certdata %{SOURCE21}
%convert_certdata %{SOURCE23}

#manpage
cp %{SOURCE10} %{name}/update-ca-trust.8.txt
asciidoc -v -d manpage -b docbook %{name}/update-ca-trust.8.txt
xsltproc --nonet -o %{name}/update-ca-trust.8 %{python3_sitelib}/asciidoc/resources/docbook-xsl/manpage.xsl %{name}/update-ca-trust.8.xml

%install
mkdir -p -m 755 %{buildroot}%{pkidir}/tls/certs
mkdir -p -m 755 %{buildroot}%{pkidir}/java
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/ssl
mkdir -p -m 755 %{buildroot}%{catrustdir}/source
mkdir -p -m 755 %{buildroot}%{catrustdir}/source/anchors
mkdir -p -m 755 %{buildroot}%{catrustdir}/source/blacklist
mkdir -p -m 755 %{buildroot}%{catrustdir}/extracted
mkdir -p -m 755 %{buildroot}%{catrustdir}/extracted/pem
mkdir -p -m 755 %{buildroot}%{catrustdir}/extracted/openssl
mkdir -p -m 755 %{buildroot}%{catrustdir}/extracted/java
mkdir -p -m 755 %{buildroot}%{catrustdir}/extracted/edk2
mkdir -p -m 755 %{buildroot}%{_datadir}/pki/ca-trust-source
mkdir -p -m 755 %{buildroot}%{_datadir}/pki/ca-trust-source/anchors
mkdir -p -m 755 %{buildroot}%{_datadir}/pki/ca-trust-source/blacklist
mkdir -p -m 755 %{buildroot}%{_bindir}
mkdir -p -m 755 %{buildroot}%{_mandir}/man8

install -p -m 644 %{name}/update-ca-trust.8 %{buildroot}%{_mandir}/man8
install -p -m 644 %{SOURCE11} %{buildroot}%{_datadir}/pki/ca-trust-source/README
install -p -m 644 %{SOURCE12} %{buildroot}%{catrustdir}/README
install -p -m 644 %{SOURCE13} %{buildroot}%{catrustdir}/extracted/README
install -p -m 644 %{SOURCE14} %{buildroot}%{catrustdir}/extracted/java/README
install -p -m 644 %{SOURCE15} %{buildroot}%{catrustdir}/extracted/openssl/README
install -p -m 644 %{SOURCE16} %{buildroot}%{catrustdir}/extracted/pem/README
install -p -m 644 %{SOURCE17} %{buildroot}%{catrustdir}/extracted/edk2/README
install -p -m 644 %{SOURCE18} %{buildroot}%{catrustdir}/source/README

# Base certs
%install_bundles %{SOURCE21} %{p11_format_base_bundle}

# Microsoft certs
%install_bundles %{SOURCE23} %{p11_format_microsoft_bundle}

# TODO: consider to dynamically create the update-ca-trust script from within
#       this .spec file, in order to have the output file+directory names at once place only.
install -p -m 755 %{SOURCE2} %{buildroot}%{_bindir}/update-ca-trust

install -p -m 755 %{SOURCE22} %{buildroot}%{_bindir}/bundle2pem.sh

# touch ghosted files that will be extracted dynamically
# Set chmod 444 to use identical permission
touch %{buildroot}%{catrustdir}/extracted/pem/tls-ca-bundle.pem
chmod 444 %{buildroot}%{catrustdir}/extracted/pem/tls-ca-bundle.pem
touch %{buildroot}%{catrustdir}/extracted/pem/email-ca-bundle.pem
chmod 444 %{buildroot}%{catrustdir}/extracted/pem/email-ca-bundle.pem
touch %{buildroot}%{catrustdir}/extracted/pem/objsign-ca-bundle.pem
chmod 444 %{buildroot}%{catrustdir}/extracted/pem/objsign-ca-bundle.pem
touch %{buildroot}%{catrustdir}/extracted/openssl/%{openssl_format_trust_bundle}
chmod 444 %{buildroot}%{catrustdir}/extracted/openssl/%{openssl_format_trust_bundle}
touch %{buildroot}%{catrustdir}/extracted/%{java_bundle}
chmod 444 %{buildroot}%{catrustdir}/extracted/%{java_bundle}
touch %{buildroot}%{catrustdir}/extracted/edk2/cacerts.bin
chmod 444 %{buildroot}%{catrustdir}/extracted/edk2/cacerts.bin

# Directory links for compatibility with 3rd-party tools
mkdir -p %{buildroot}%{_libdir}/ssl
for link in "%{_sysconfdir}/ssl/certs" "%{_libdir}/ssl/certs"; do
  ln -s %{pkidir}/tls/certs "%{buildroot}$link"
done

# Legacy file names and links for compatibility with 3rd-party tools
for link in "%{classic_tls_bundle}" ca-certificates.crt; do
  ln -s %{catrustdir}/extracted/pem/tls-ca-bundle.pem "%{buildroot}%{pkidir}/tls/certs/$link"
done
ln -s %{catrustdir}/extracted/pem/tls-ca-bundle.pem \
    %{buildroot}%{pkidir}/tls/cert.pem
ln -s %{catrustdir}/extracted/openssl/%{openssl_format_trust_bundle} \
    %{buildroot}%{pkidir}/tls/certs/%{openssl_format_trust_bundle}
ln -s %{catrustdir}/extracted/%{java_bundle} \
    %{buildroot}%{pkidir}/%{java_bundle}

# Supporting p11-kit's directory re-name in version 0.24.0.
ln -s blacklist %{buildroot}%{_datadir}/pki/ca-trust-source/blocklist
ln -s blacklist %{buildroot}%{catrustdir}/source/blocklist

%post
%{refresh_bundles}

%post base
%{refresh_bundles}

%postun
%{refresh_bundles}

%postun base
%{refresh_bundles}

%postun legacy
# During build time it is unknown what files will get created by the
# 'legacy' subpackage's triggers, so we cannot inform RPM to delete
# them for us through the '%%files' section and the '%%ghost' macro.
rm -f %{pkidir}/tls/certs/*.{0,pem}

# If the 'legacy' subpackage is installed, we need to always refresh the
# single PEM-encoded certificates every time a certificate bundle gets modified.
# The cert bundle gets modified whenever one of the packages from %%{watched_pkgs}
# get installed, removed, or updated.
%triggerin -n %{name}-legacy -- %{watched_pkgs}
%{_bindir}/bundle2pem.sh %{pkidir}/tls/certs/%{classic_tls_bundle}

%triggerpostun -n %{name}-legacy -- %{watched_pkgs}
%{_bindir}/bundle2pem.sh %{pkidir}/tls/certs/%{classic_tls_bundle}

%files
# Microsoft certs bundle file with trust
%{_datadir}/pki/ca-trust-source/%{p11_format_microsoft_bundle}

%files base
%{_datadir}/pki/ca-trust-source/%{p11_format_base_bundle}

%files shared
%license LICENSE

# symlinks for old locations
%{pkidir}/tls/cert.pem
%{pkidir}/tls/certs/%{classic_tls_bundle}
%{pkidir}/tls/certs/%{openssl_format_trust_bundle}
%{pkidir}/tls/certs/ca-certificates.crt
%{pkidir}/%{java_bundle}

# symlink directory
%{_datadir}/pki/ca-trust-source/blocklist
%{_sysconfdir}/ssl/certs
%{_libdir}/ssl/certs
%{catrustdir}/source/blocklist

# README files
%{_datadir}/pki/ca-trust-source/README
%{catrustdir}/README
%{catrustdir}/extracted/README
%{catrustdir}/extracted/edk2/README
%{catrustdir}/extracted/java/README
%{catrustdir}/extracted/openssl/README
%{catrustdir}/extracted/pem/README
%{catrustdir}/source/README

%dir %{_datadir}/pki
%dir %{_datadir}/pki/ca-trust-source
%dir %{_datadir}/pki/ca-trust-source/anchors
%dir %{_datadir}/pki/ca-trust-source/blacklist
%dir %{_sysconfdir}/ssl
%dir %{catrustdir}
%dir %{catrustdir}/extracted
%dir %{catrustdir}/extracted/edk2
%dir %{catrustdir}/extracted/java
%dir %{catrustdir}/extracted/pem
%dir %{catrustdir}/extracted/openssl
%dir %{catrustdir}/source
%dir %{catrustdir}/source/anchors
%dir %{catrustdir}/source/blacklist
%dir %{pkidir}/java
%dir %{pkidir}/tls
%dir %{pkidir}/tls/certs

%ghost %{catrustdir}/extracted/pem/tls-ca-bundle.pem
%ghost %{catrustdir}/extracted/pem/email-ca-bundle.pem
%ghost %{catrustdir}/extracted/pem/objsign-ca-bundle.pem
%ghost %{catrustdir}/extracted/openssl/%{openssl_format_trust_bundle}
%ghost %{catrustdir}/extracted/%{java_bundle}
%ghost %{catrustdir}/extracted/edk2/cacerts.bin

%files tools
# update/extract tool
%{_bindir}/update-ca-trust

%{_mandir}/man8/update-ca-trust.8.gz

%files legacy
%{_bindir}/bundle2pem.sh

%changelog
* Wed Feb 28 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.0.0-4
- Updated certdata.base.txt to replace CBL-Mariner with Azure Linux

* Sat Jan 27 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.0-3
- Updating Microsoft trusted root CAs.

* Fri Jan 19 2024 Andrew Phelps <anphel@microsoft.com> - 3.0.0-2
- Use asciidoc binary instead of asciidoc.py

* Tue Jan 09 2024 Cameron Baird <cameronbaird@microsoft.com> - 3.0.0-1
- Initial version for AzureLinux 3.0.

* Mon May 08 2023 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-13
- Updating Microsoft trusted root CAs.

* Thu Mar 30 2023 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-12
- Updating Microsoft trusted root CAs.

* Fri Mar 17 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.0.0-11
- Adding support for p11-kit's 0.24.0+ source certificates paths.

* Thu Feb 23 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-10
- Adding Microsoft-owned root CAs to the base bundle.

* Tue Dec 06 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-9
- Updating Microsoft trusted root CAs.

* Fri Oct 07 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-8
- Updating Microsoft trusted root CAs.

* Wed Aug 03 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-7
- Updating Microsoft trusted root CAs.

* Wed Jun 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-6
- Bumping release to match with "prebuilt-*" packages.

* Wed Jun 29 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-5
- Updating Microsoft trusted root CAs.

* Thu Jun 02 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-4
- Making 'Release' match with 'prebuilt-ca-certificates'.

* Fri May 20 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-3
- Updating Microsoft trusted root CAs.

* Fri May 06 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-2
- Updating Microsoft trusted root CAs.

* Wed Dec 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.0.0-1
- Making 'Release' match with 'prebuilt-ca-certificates-base'.
- Updating 'URL' and 'Version' tags for CBL-Mariner 2.0.

* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-20
- Making 'Release' match with 'prebuilt-ca-certificates*'.

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-19
- Removing Mozilla certs and making Microsoft's the default ones.
- Removed support for legacy certdata.txt fields.
- Removed the use of checked-in "nssckbi.h".

* Mon Sep 13 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-18
- Updating Microsoft trusted root CAs.

* Fri Aug 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-17
- Adding directory and files links for compatibility reasons.

* Fri Aug 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-16
- Removing the 'ca-legacy' script along with the empty files and broken links it generated.

* Wed Jul 07 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-15
- Updating Microsoft trusted root CAs.

* Thu Jun 03 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-14
- Updating Microsoft trusted root CAs.

* Fri Mar 12 2021 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20200720-13
- Updating Microsoft trusted root CAs.

* Sat Mar 06 2021 CBL-Mariner Servicing Account <clbmargh@microsoft.com> - 20200720-12
- Updating Microsoft trusted root CAs.

* Mon Feb 08 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-11
- Removing the deprecated "Microsoft IT TLS CA 2" CA from the list of trusted anchors.
- Added explicit version info for the "Provides".

* Tue Nov 10 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-10
- Updating Microsoft trusted root CAs.

* Wed Oct 21 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-9
- Switching to the correct source for the Microsoft bundle.

* Sun Sep 13 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-8
- Aligning 'nssckbi.h' with the used 'certdata.txt' version for the Mozilla bundle.

* Sun Sep 13 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-7
- Removing unused 'Requires*'.

* Wed Sep 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-6
- Adding 2 Microsoft-trusted, intermediate CAs into 'ca-certificates-base'.

* Mon Aug 24 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-5
- Adding 'ca-certificates-legacy' to support apps, which only work with
  a single cert per *.pem file.  Adding a new 'ca-certificates-microsoft' subpackage with CAs trusted through
  the Microsoft Trusted Root Program.  Converting common steps into parametrized macros.

* Tue Aug 11 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-4
- Updating base certificates to current intermediate CAs.
- Re-assigning ownership of legacy bundles from '*-shared' to subpackages creating them.
- Removing commented lines.

* Fri Jul 31 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-3
- Changing base certificates to trust packages.microsoft.com.

* Fri Jul 31 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-2
- Removed redundant 'ca-bundle.trust.p11-kit' certs bundle.
- Removed unnecessary pre-install step.
- Moved license and config to 'ca-certificates-shared' subpackage
  to guarantee these to be always present regardless of the installed
  certificates bundle.

* Thu Jul 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-1
- Updating certdata.txt to Mozilla version from 2020/07/20.

* Thu Jul 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200428-4
- Fixing installation of 'ca-certificates-base` subpackage by making
  shared files and directory structure a 'Requires' for all certificate packages.
- Updating '%%uninstall_clean_up' macro to use pk11kit tooling.
- Reordering (Build)Requires to increase clarity.

* Tue May 26 2020 Paul Monson <paulmon@microsoft.com> - 20200428-3
- Initial CBL-Mariner import from Fedora 27 (license: MIT).
- License verified.
- Updated Mozilla certdata.txt to latest version from the "FIREFOX_76_0_RELEASE" release.
- Added a '-base` sub package with certificates allowing for verification of the packages repository.
- Merged the '-pki' sub package into 'ca-certificates'.
- Updated the "URL" tag.
- Moved scripts to separate sources and the "ca-certificates-tools" subpackage.
- Added "rebuild-ca-bundle.sh" script.
- Creating a separate set of "ca-certificates-base" subpackages to keep certs separate.
- Fixing post-install script by moving "openssl" from "Requires" to "Requires(post)".

*Wed Jun 19 2019 Bob Relyea <rrelyea@redhat.com> 2019.2.32-1.0
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
