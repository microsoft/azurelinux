# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global bouncycastleJdk 18
%global bouncycastleVer 1.77

Epoch:          1
Name:           apache-sshd
Version:        2.11.0
Release: 8%{?dist}
Summary:        Apache SSHD

# One file has ISC licensing:
#   sshd-common/src/main/java/org/apache/sshd/common/config/keys/loader/openssh/kdf/BCrypt.java
# Automatically converted from old format: ASL 2.0 and ISC - review is highly recommended.
License:        Apache-2.0 AND ISC
URL:            http://mina.apache.org/sshd-project

Source0:        https://archive.apache.org/dist/mina/sshd/%{version}/apache-sshd-%{version}-src.tar.gz

# Avoid optional dep on tomcat native APR library
Patch0:         0001-Avoid-optional-dependency-on-native-tomcat-APR-libra.patch

BuildRequires:  maven-local-openjdk21
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.i2p.crypto:eddsa)
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven:maven-archiver)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-clean-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  mvn(org.apache.maven.surefire:surefire-junit47)
BuildRequires:  mvn(org.bouncycastle:bcpg-jdk%{bouncycastleJdk}on)
BuildRequires:  mvn(org.bouncycastle:bcpkix-jdk%{bouncycastleJdk}on)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.slf4j:jcl-over-slf4j)
BuildRequires:  mvn(org.slf4j:slf4j-api)

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Patch1: add-maven-compiler-release.patch
%description
Apache SSHD is a 100% pure java library to support the SSH protocols on both
the client and server side.

%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
This package provides %{name}.

%prep
%autosetup -p1

# Avoid optional dep on tomcat native APR library

rm -rf sshd-core/src/main/java/org/apache/sshd/agent/unix

# Avoid unnecessary dep on spring framework
%pom_remove_dep :spring-framework-bom
%pom_remove_dep :testcontainers-bom sshd-sftp sshd-core sshd-scp

# Build the core modules only
%pom_disable_module assembly
%pom_disable_module sshd-mina
%pom_disable_module sshd-netty
%pom_disable_module sshd-ldap
%pom_disable_module sshd-git
%pom_disable_module sshd-contrib
%pom_disable_module sshd-spring-sftp
%pom_disable_module sshd-cli
%pom_disable_module sshd-openpgp

# Disable plugins we don't need for RPM builds
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :gmavenplus-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-pmd-plugin
%pom_remove_plugin :maven-antrun-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :impsort-maven-plugin
%pom_remove_plugin :formatter-maven-plugin . sshd-core


# Suppress generation of uses clauses
%pom_xpath_inject "pom:configuration/pom:instructions" "<_nouses>true</_nouses>" .
sed "s;<bouncycastle.version>.*;<bouncycastle.version>%{bouncycastleVer}</bouncycastle.version>;g" -i pom.xml

%pom_remove_plugin :maven-remote-resources-plugin
%build
# Can't run tests, they require ch.ethz.ganymed:ganymed-ssh2
%mvn_build -f -- -Dworkspace.root.dir=$(pwd)

%install
%mvn_install

%files -f .mfiles
%doc CHANGES.md
%license LICENSE.txt NOTICE.txt assembly/src/main/legal/licenses/jbcrypt.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt assembly/src/main/legal/licenses/jbcrypt.txt

%changelog
* Wed Jul 30 2025 jiri vanek <jvanek@redhat.com> - 1:2.11.0-7
- Rrevert to jdk21

* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1:2.11.0-6
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 1:2.11.0-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1:2.11.0-1
- Rebuilt for java-21-openjdk as system jdk
- updated to 2.11

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1:2.8.0-2
- Rebuilt for Drop i686 JDKs

* Fri Apr 01 2022 Mat Booth <mat.booth@gmail.com> - 1:2.8.0-1
- Update to latest upstream release

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1:2.6.0-5
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 20 2021 Jeff Johnston <jjohnstn@redhat.com> 1:2.6.0-2
- Fix missing imports in MANIFEST.MF files

* Wed Mar 10 2021 Mat Booth <mat.booth@redhat.com> - 1:2.6.0-1
- Update to latest upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1:2.4.0-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jul 09 2020 Mat Booth <mat.booth@redhat.com> - 1:2.4.0-3
- Build against any JDK

* Wed Jun 24 2020 Alexander Kurtakov <akurtako@redhat.com> 1:2.4.0-2
- Fix build against Java 11.

* Mon Jun 22 2020 Mat Booth <mat.booth@redhat.com> - 1:2.4.0-1
- Update to latest upstream release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 02 2019 Mat Booth <mat.booth@redhat.com> - 1:2.2.0-3
- Include release notes in %%doc section

* Mon Jul 01 2019 Mat Booth <mat.booth@redhat.com> - 1:2.2.0-2
- Fix license tag to include ISC for bcrypt implementation

* Fri May 31 2019 Mat Booth <mat.booth@redhat.com> - 1:2.2.0-1
- Update to latest upstream release

* Fri Mar 15 2019 Mat Booth <mat.booth@redhat.com> - 1:2.0.0-4
- Revert back to 2.0.0, there are problems with 2.2.0

* Thu Mar 07 2019 Mat Booth <mat.booth@redhat.com> - 2.2.0-1
- Update to latest upstream release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Mat Booth <mat.booth@redhat.com> - 2.1.0-2
- Disable uses directive generation

* Thu Nov 29 2018 Mat Booth <mat.booth@redhat.com> - 2.1.0-1
- Update to latest upstream release
- Patch out the dependency on tomcat-libs

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 gil cattaneo <puntogil@libero.it> 0.14.0-4
- fix FTBFS

* Mon Jun 20 2016 gil cattaneo <puntogil@libero.it> 0.14.0-3
- add missing build requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 01 2015 Michal Srb <msrb@redhat.com> - 0.14.0-1
- Update to upstream release 0.14.0
- Do not build sshd-git (not needed)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Michal Srb <msrb@redhat.com> - 0.11.0-4
- AutoReqProv: yes
- Build against tomcat-jni
- Build only sshd-core

* Fri Feb 13 2015 gil cattaneo <puntogil@libero.it> 0.11.0-3
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 gil cattaneo <puntogil@libero.it> - 0.11.0-1
- Update to upstream 0.11.0 (rhbz#1094049)

* Wed Nov 27 2013 Juan Hernandez <juan.hernandez@redhat.com> - 0.9.0-3
- Revert to upstream version 0.8.0 due to bug 1021273. Note that the
  version number can't go backwards, so it stays at 0.9.0.

* Mon Sep 30 2013 Juan Hernandez <juan.hernandez@redhat.com> - 0.9.0-2
- Fix bouncycastle requirement

* Mon Sep 30 2013 Juan Hernandez <juan.hernandez@redhat.com> - 0.9.0-1
- Update to upstream 0.9.0

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 0.7.0-5
- rebuilt rhbz#991979
- swith to Xmvn
- adapt to new guideline
- use pom macros
- remove rpmlint warnings

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.7.0-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 26 2012 Juan Hernandez <juan.hernandez@redhat.com> - 0.7.0-1
- Update to upstream 0.7.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 0.6.0-2
- Corrected the source URL

* Sun Feb 12 2012 Juan Hernandez <juan.hernandez@redhat.com> 0.6.0-1
- Initial packaging
