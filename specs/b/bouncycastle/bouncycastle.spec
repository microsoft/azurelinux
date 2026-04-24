# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gittag r1rv77
%global classname org.bouncycastle.jce.provider.BouncyCastleProvider
%global profilen 1.8
%global profile %(echo %{profilen} | sed "s/\\.//g" )
%global jdkon jdk%{profile}on

Summary:          Bouncy Castle Cryptography APIs for Java
Name:             bouncycastle
Version:          1.77
Release: 6%{?dist}
License:          MIT
URL:              http://www.bouncycastle.org

Source0:          https://github.com/bcgit/bc-java/archive/%{gittag}.tar.gz

# POMs from Maven Central
Source1:          https://repo1.maven.org/maven2/org/bouncycastle/bcprov-%{jdkon}/%{version}/bcprov-%{jdkon}-%{version}.pom
Source2:          https://repo1.maven.org/maven2/org/bouncycastle/bcpkix-%{jdkon}/%{version}/bcpkix-%{jdkon}-%{version}.pom
Source3:          https://repo1.maven.org/maven2/org/bouncycastle/bcpg-%{jdkon}/%{version}/bcpg-%{jdkon}-%{version}.pom
Source4:          https://repo1.maven.org/maven2/org/bouncycastle/bcmail-%{jdkon}/%{version}/bcmail-%{jdkon}-%{version}.pom
Source5:          https://repo1.maven.org/maven2/org/bouncycastle/bctls-%{jdkon}/%{version}/bctls-%{jdkon}-%{version}.pom
Source6:          https://repo1.maven.org/maven2/org/bouncycastle/bcutil-%{jdkon}/%{version}/bcutil-%{jdkon}-%{version}.pom
Source7:          https://repo1.maven.org/maven2/org/bouncycastle/bcjmail-%{jdkon}/%{version}/bcjmail-%{jdkon}-%{version}.pom

# Script to fetch POMs from Maven Central
Source8:          get-poms.sh

Patch0: jmail.packages.patch

BuildArch:        noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:    aqute-bnd
BuildRequires:    ant-openjdk25 
BuildRequires:    ant-junit
#                 For bcmail
BuildRequires:    jakarta-activation1
BuildRequires:    jakarta-mail1
#                 For bcjmail
BuildRequires:    jakarta-activation
BuildRequires:    jakarta-mail
BuildRequires:    javapackages-local-openjdk25

Requires(post):   javapackages-tools
Requires(postun): javapackages-tools

Provides:         bcprov = %{version}-%{release}

%description
The Bouncy Castle Crypto package is a Java implementation of cryptographic
algorithms. This jar contains JCE provider and lightweight API for the
Bouncy Castle Cryptography APIs for JDK 1.5 to JDK 1.8.

%package pkix
Summary: Bouncy Castle PKIX, CMS, EAC, TSP, PKCS, OCSP, CMP, and CRMF APIs

%description pkix
The Bouncy Castle Java APIs for CMS, PKCS, EAC, TSP, CMP, CRMF, OCSP, and
certificate generation. This jar contains APIs for JDK 1.5 to JDK 1.8. The
APIs can be used in conjunction with a JCE/JCA provider such as the one
provided with the Bouncy Castle Cryptography APIs.

%package pg
Summary: Bouncy Castle OpenPGP API

%description pg
The Bouncy Castle Java API for handling the OpenPGP protocol. The APIs can be
used in conjunction with a JCE/JCA provider such as the one provided with the
Bouncy Castle Cryptography APIs.

%package mail
Summary: Bouncy Castle S/MIME API

%description mail
The Bouncy Castle Java S/MIME APIs for handling S/MIME protocols. The APIs can
be used in conjunction with a JCE/JCA provider such as the one provided with
the Bouncy Castle Cryptography APIs. The JavaMail API and the Java activation
framework will also be needed.

%package jmail
Summary: Bouncy Castle Jakarta S/MIME API

%description jmail
The Bouncy Castle Java S/MIME APIs for handling S/MIME protocols. The APIs can
be used in conjunction with a JCE/JCA provider such as the one provided with
the Bouncy Castle Cryptography APIs. The Jakarta Mail API and the Jakarta
activation framework will also be needed.

%package tls
Summary: Bouncy Castle JSSE provider and TLS/DTLS API

%description tls
The Bouncy Castle Java APIs for TLS and DTLS, including a provider for the
JSSE.

%package util
Summary: Bouncy Castle ASN.1 Extension and Utility APIs

%description util
The Bouncy Castle Java APIs for ASN.1 extension and utility APIs used to
support bcpkix and bctls.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
API documentation for the Bouncy Castle Cryptography APIs.

%prep
%setup -q -n bc-java-%{gittag}

%patch -P0 -p1

#?!?!!?!??!?!!?
for x in `find | grep  -e  x_pkcs7_signature.java  -e PKCS7ContentHandler.java -e multipart_signed.java` ; do 
  sed "s/getTransferData.ActivationDataFlavor/getTransferData(DataFlavor/g" -i $x
  sed "s/            ActivationDataFlavor df,/            DataFlavor df,/g"  -i $x
done

# Remove bundled binary libs
find . -type f -name "*.class" -exec rm -f {} \;
find . -type f -name "*.jar" -exec rm -f {} \;

# Not shipping lw/lcrypto (lightweight crypto) jar
sed -i -e '/target="build-lw"/d' ant/jdk%{profile}+.xml
sed -i -e '/target="javadoc-lw"/d' ant/jdk%{profile}+.xml

cp -p %{SOURCE1} bcprov.pom
cp -p %{SOURCE2} bcpkix.pom
cp -p %{SOURCE3} bcpg.pom
cp -p %{SOURCE4} bcmail.pom
cp -p %{SOURCE5} bctls.pom
cp -p %{SOURCE6} bcutil.pom
cp -p %{SOURCE7} bcjmail.pom

# this test needs additional dependeces
rm prov/src/test/java/org/bouncycastle/jce/provider/test/X509LDAPCertStoreTest.java

%build
ant -f ant/jdk%{profile}+.xml \
  -Djunit.jar.home=$(build-classpath junit) \
  -Dmail.jar.home=$(build-classpath jakarta-mail1/jakarta.mail) \
  -Dactivation.jar.home=$(build-classpath jakarta-activation1/jakarta.activation) \
  -Djmail.jar.home=$(build-classpath jakarta-mail/jakarta.mail) \
  -Djactivation.jar.home=$(build-classpath jakarta-activation) \
  -Drelease.debug=true -Dbc.javac.source=1.8 -Dbc.javac.target=1.8 \
  clean build-provider build #test

cat > bnd.bnd <<EOF
-classpath=bcprov.jar,bcutil.jar,bcpkix.jar,bcpg.jar,bcmail.jar,bcjmail.jar,bctls.jar
Export-Package: *;version=%{version}
EOF

for bc in bcprov bcutil bcpkix bcpg bcmail bcjmail bctls ; do
  # Make into OSGi bundle
  bnd wrap -b $bc -v %{version} -p bnd.bnd -o $bc.jar build/artifacts/jdk%{profilen}/jars/$bc-%{jdkon}-*.jar

  # Request Maven installation
  %mvn_file ":$bc-%{jdkon}" $bc
  %mvn_package ":$bc-%{jdkon}" $bc
  %mvn_alias ":$bc-%{jdkon}" "org.bouncycastle:$bc-jdk16" "org.bouncycastle:$bc-jdk15"
  %mvn_artifact $bc.pom $bc.jar
done

%install
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d
touch $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d/2000-%{classname}

%mvn_install -J build/artifacts/jdk%{profilen}/javadoc

%post
{
  # Rebuild the list of security providers in classpath.security
  suffix=security/classpath.security
  secfiles="/usr/lib/$suffix /usr/lib64/$suffix"

  for secfile in $secfiles
  do
    # check if this classpath.security file exists
    [ -f "$secfile" ] || continue

    sed -i '/^security\.provider\./d' "$secfile"

    count=0
    for provider in $(ls /etc/java/security/security.d)
    do
      count=$((count + 1))
      echo "security.provider.${count}=${provider#*-}" >> "$secfile"
    done
  done
} || :

%postun
if [ "$1" -eq 0 ] ; then

  {
    # Rebuild the list of security providers in classpath.security
    suffix=security/classpath.security
    secfiles="/usr/lib/$suffix /usr/lib64/$suffix"

    for secfile in $secfiles
    do
      # check if this classpath.security file exists
      [ -f "$secfile" ] || continue

      sed -i '/^security\.provider\./d' "$secfile"

      count=0
      for provider in $(ls /etc/java/security/security.d)
      do
        count=$((count + 1))
        echo "security.provider.${count}=${provider#*-}" >> "$secfile"
      done
    done
  } || :

fi

%files -f .mfiles-bcprov
%license build/artifacts/jdk%{profilen}/bcprov-%{jdkon}-*/LICENSE.html
%doc docs/ *.html
%{_sysconfdir}/java/security/security.d/2000-%{classname}

%files pkix -f .mfiles-bcpkix
%license build/artifacts/jdk%{profilen}/bcpkix-%{jdkon}-*/LICENSE.html

%files pg -f .mfiles-bcpg
%license build/artifacts/jdk%{profilen}/bcpg-%{jdkon}-*/LICENSE.html

%files mail -f .mfiles-bcmail
%license build/artifacts/jdk%{profilen}/bcmail-%{jdkon}-*/LICENSE.html

%files jmail -f .mfiles-bcjmail
%license build/artifacts/jdk%{profilen}/bcjmail-%{jdkon}-*/LICENSE.html

%files tls -f .mfiles-bctls
%license build/artifacts/jdk%{profilen}/bctls-%{jdkon}-*/LICENSE.html

%files util -f .mfiles-bcutil
%license build/artifacts/jdk%{profilen}/bcutil-%{jdkon}-*/LICENSE.html

%files javadoc -f .mfiles-javadoc
%license LICENSE.html

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.77-5
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.77-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.77-1
- Rebuilt for java-21-openjdk as system jdk
- bumped to 1.77
- used macros on the crucial, depndent parts where needed

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 29 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 1.70-10
- Build bcjmail (dependencies now available in Fedora)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 24 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 1.70-8
- Adapt to changes in the jakarta-activation package

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.70-5
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.70-4
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 1.70-2
- Backport fix for regression in bouncycastle 1.70, fixes rhbz#2039724

* Fri Dec 17 2021 Mat Booth <mat.booth@gmail.com> - 1.70-1
- Update to latest upstream release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 25 2021 Mat Booth <mbooth@apache.org> - 1.68-1
- Update to latest upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Nov 01 2020 Mat Booth <mat.booth@redhat.com> - 1.67-1
- Update to latest upstream release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.65-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.65-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Sat Jun 20 2020 Mat Booth <mat.booth@redhat.com> - 1.65-2
- Fix build on Java 11

* Fri Jun 19 2020 Mat Booth <mat.booth@redhat.com> - 1.65-1
- Update to latest upstream release
- Remove old obsoletes
- Avoid using deprecated source/target values

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 12 2019 Mat Booth <mat.booth@redhat.com> - 1.63-1
- Update to latest upstream release

* Mon Sep 09 2019 Mat Booth <mat.booth@redhat.com> - 1.61-2
- Disable tests that take a long time on 32bit arm

* Wed Feb 06 2019 Mat Booth <mat.booth@redhat.com> - 1.61-1
- Update to latest upstream release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 21 2018 Mat Booth <mat.booth@redhat.com> - 1.60-1
- Update to latest upstream release

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 07 2018 Mat Booth <mat.booth@redhat.com> - 1.59-1
- Update to latest release
- Fixes CVE-2018-1000180 and CVE-2017-13098

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Mat Booth <mat.booth@redhat.com> - 1.58-2
- Fix error in scriptlet

* Fri Aug 18 2017 Mat Booth <mat.booth@redhat.com> - 1.58-1
- Update to 1.58, fixes rhbz#1482920

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 18 2017 Mat Booth <mat.booth@redhat.com> - 1.57-1
- Update to latest release of bouncycastle
- Build all bouncycastle modules from a single source tree, using upstream's
  own build scripts
- Add sub-packages for each module

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 09 2016 gil cattaneo <puntogil@libero.it> 1.54-2
- readd workaround for test failures

* Thu Apr 07 2016 Mat Booth <mat.booth@redhat.com> - 1.54-1
- Update to 1.54, fixes rhbz#1270249
- Install with mvn_install
- Fix test suite failures, fixes rhbz#1049007
- Move some tests that were erroneously in the main jar,
  avoids a runtime dep on junit in OSGi metadata

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 16 2015 Michael Simacek <msimacek@redhat.com> - 1.52-7
- Re-add geenric Export-Package

* Thu Jul 16 2015 Michael Simacek <msimacek@redhat.com> - 1.52-6
- Use aqute-bnd-2.4.1

* Tue Jun 23 2015 Roland Grunberg <rgrunber@redhat.com> - 1.52-5
- Remove Import/Export-Package statements.
- Related: rhbz#1233354

* Mon Jun 22 2015 Roland Grunberg <rgrunber@redhat.com> - 1.52-4
- Fix typo in OSGi metadata file.

* Thu Jun 18 2015 Mat Booth <mat.booth@redhat.com> - 1.52-3
- Resolves: rhbz#1233354 - Add OSGi metadata

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 22 2015 Alexander Kurtakov <akurtako@redhat.com> 1.52-1
- Update to 1.52.
- Switch source/target to 1.6 as 1.5 is deprecated

* Thu Jan 29 2015 gil cattaneo <puntogil@libero.it> 1.50-6
- introduce license macro

* Wed Oct 22 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.50-5
- Add alias for org.bouncycastle:bcprov-jdk15

* Mon Jun 09 2014 Michal Srb <msrb@redhat.com> - 1.50-4
- Migrate to .mfiles

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Michal Srb <msrb@redhat.com> - 1.50-2
- Fix java BR/R
- Build with -source/target 1.5
- s/organised/organized/

* Fri Feb 21 2014 Michal Srb <msrb@redhat.com> - 1.50-1
- Update to upstream version 1.50
- Switch to java-headless

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.46-12
- Add Maven alias for bouncycastle:bcprov-jdk15

* Tue Oct 22 2013 gil cattaneo <puntogil@libero.it> 1.46-11
- remove versioned Jars

* Thu Aug 29 2013 gil cattaneo <puntogil@libero.it> 1.46-10
- remove update_maven_depmap

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 1.46-9
- rebuilt rhbz#992026

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Tom Callaway <spot@fedoraproject.org> - 1.46-5
- use original sources from here on out

* Sat Feb 18 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-4
- Build with -source 1.6 -target 1.6 

* Thu Jan 12 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-3
- Update javac target version to 1.7 to build with new java

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 01 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-1
- Import Bouncy Castle 1.46.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 1.45-2
- Drop gcj.
- Adapt to current guidelines.

* Thu Feb 11 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.45-1
- Import Bouncy Castle 1.45.

* Sat Nov 14 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.44-1
- Import Bouncy Castle 1.44.

* Sun Sep  6 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.43-6
- Include improvements from #521475:
- Include missing properties files in jar.
- Build with javac -encoding UTF-8.
- Use %%javac and %%jar macros.
- Run test suite during build (ignoring failures for now).
- Follow upstream in excluding various test suite classes from jar; drop
  dependency on junit4.

* Wed Aug 26 2009 Andrew Overholt <overholt@redhat.com> 1.43-5
- Add maven POM

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-3
- Raise java requirement to >= 1.7 once again.

* Fri Jul 10 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-2
- Re-enable AOT bits thanks to Andrew Haley.

* Mon Apr 20 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-1
- Import Bouncy Castle 1.43.

* Sat Apr 18 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-3
- Don't build AOT bits. The package needs java1.6

* Thu Apr 09 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-2
- Add missing Requires: junit4

* Tue Mar 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-1
- Import Bouncy Castle 1.42.
- Update description.
- Add javadoc subpackage.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 11 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.41-2
- Fixed license tag (BSD -> MIT).
- Minor improvements in the SPEC file for better compatibility with the 
  Fedora Java Packaging Guidelines.
- Added "Provides: bcprov == %%{version}-%%{release}".

* Thu Oct  2 2008 Lillian Angel <langel@redhat.com> - 1.41-1
- Import Bouncy Castle 1.41.
- Resolves: rhbz#465203

* Thu May 15 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.39-1
- Import Bouncy Castle 1.39.
- Set target to 1.5.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.38-2
- Autorebuild for GCC 4.3

* Thu Nov 29 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.38-1
- Import Bouncy Castle 1.38.
- Require junit4 for build.
- Require java-1.7.0-icedtea-devel for build.
- Wrap lines at 80 columns.
- Inline rebuild-security-providers in post and postun sections.
- Related: rhbz#260161

* Sat Mar 31 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.34-3
- Require java-1.5.0-gcj.

* Tue Dec 12 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.34-2
- Install bcprov jar and unversioned symlink in %%{_javadir}.
- Install bcprov symlink in %%{_javadir}/gcj-endorsed.
- Change release numbering format to X.fc7.
- Include new bcprov files in files list.
- Import Bouncy Castle 1.34.
- Related: rhbz#218794

* Tue Jul 25 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.33-3
- Bump release number.

* Mon Jul 10 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.33-2
- Fix problems pointed out by reviewer.

* Fri Jul  7 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.33-1
- First release.
