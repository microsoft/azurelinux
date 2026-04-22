## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 22;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

Name:           xmvn
Version:        4.3.0
Release:        %autorelease
Summary:        Local Extensions for Apache Maven
License:        Apache-2.0
URL:            https://fedora-java.github.io/xmvn/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/fedora-java/xmvn/releases/download/%{version}/xmvn-%{version}.tar.xz
Source21:       toolchains-openjdk21.xml
Source25:       toolchains-openjdk25.xml

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
BuildRequires:  maven
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.beust:jcommander)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-api)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-util)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-model-builder)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
BuildRequires:  mvn(org.xmlunit:xmlunit-assertj3)
# Maven home is used as template for XMvn home
BuildRequires:  maven
%endif
Requires:       %{name}-minimal = %{version}-%{release}
Requires:       maven
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.3.0-15

%description
This package provides extensions for Apache Maven that can be used to
manage system artifact repository and use it to resolve Maven
artifacts in offline mode, as well as Maven plugins to help with
creating RPM packages containing Maven artifacts.

%package minimal
Summary:        Dependency-reduced version of XMvn
Requires:       %{name}-core = %{version}-%{release}
Requires:       apache-commons-cli
Requires:       apache-commons-codec
Requires:       google-guice
Requires:       guava
Requires:       jakarta-annotations
Requires:       jakarta-inject1.0
Requires:       jansi
Requires:       jcl-over-slf4j
Requires:       maven-jdk-binding
Requires:       maven-lib
Requires:       maven-resolver
Requires:       maven-shared-utils
Requires:       maven-wagon
Requires:       plexus-cipher
Requires:       plexus-classworlds
Requires:       plexus-containers-component-annotations
Requires:       plexus-interpolation
Requires:       plexus-sec-dispatcher
Requires:       plexus-utils
Requires:       sisu
Requires:       slf4j
Suggests:       maven-openjdk25

%description minimal
This package provides minimal version of XMvn, incapable of using
remote repositories.

%package core
Summary:        XMvn library

%description core
This package provides XMvn API and XMvn Core modules, which implement
the essential functionality of XMvn such as resolution of artifacts
from system repository.

%package mojo
Summary:        XMvn MOJO

%description mojo
This package provides XMvn MOJO, which is a Maven plugin that consists
of several MOJOs.  Some goals of these MOJOs are intended to be
attached to default Maven lifecycle when building packages, others can
be called directly from Maven command line.

%package tools
Summary:        XMvn tools

%description tools
This package provides various XMvn tools:
* XMvn Install, which is a command-line interface to XMvn installer.
  The installer reads reactor metadata and performs artifact
  installation according to specified configuration.
* XMvn Resolver, which is a very simple commald-line tool to resolve
  Maven artifacts from system repositories.  Basically it's just an
  interface to artifact resolution mechanism implemented by XMvn Core.
  The primary intended use case of XMvn Resolver is debugging local
  artifact repositories.
* XMvn Subst, which is a tool that can substitute Maven artifact files
  with symbolic links to corresponding files in artifact repository.

%prep
%autosetup -p1 -C

%mvn_package ::tar.gz: __noinstall
%mvn_package ":{xmvn,xmvn-connector}" xmvn
%mvn_package ":xmvn-{api,core,parent}" core
%mvn_package ":xmvn-mojo" mojo
%mvn_package ":xmvn-{install,resolve,subst,tools}" tools

# Don't put Class-Path attributes in manifests
%pom_remove_plugin :maven-jar-plugin xmvn-tools

# Copy Maven home packaged as RPM instead of unpacking Maven binary
# tarball with maven-dependency-plugin
%pom_remove_plugin :maven-dependency-plugin
maven_home=%{_datadir}/maven
mver=$(sed -n '/<mavenVersion>/{s/.*>\(.*\)<.*/\1/;p}' \
           xmvn-parent/pom.xml)
mkdir -p target/dependency/
cp -a "${maven_home}" target/dependency/apache-maven-$mver

# Workaround easymock incompatibility with Java 17 that should be fixed
# in easymock 4.4: https://github.com/easymock/easymock/issues/274
%pom_add_plugin :maven-surefire-plugin xmvn-connector "<configuration>
    <argLine>--add-opens=java.base/java.lang=ALL-UNNAMED</argLine></configuration>"
%pom_add_plugin :maven-surefire-plugin xmvn-tools/xmvn-install "<configuration>
    <argLine>--add-opens=java.base/java.lang=ALL-UNNAMED</argLine></configuration>"

%build
%{?jpb_env}
# Work around a conflict between XMvn 4 and XMvn 5 that prevents the
# install and builddep MOJOs to work.
xmvn -B -o -P\!quality verify
%mvn_artifact pom.xml
%mvn_artifact xmvn-parent/pom.xml
%mvn_artifact xmvn-tools/pom.xml
%mvn_artifact xmvn-api/pom.xml xmvn-api/target/xmvn-api-4.3.0.jar
%mvn_artifact xmvn-core/pom.xml xmvn-core/target/xmvn-core-4.3.0.jar
%mvn_artifact xmvn-connector/pom.xml xmvn-connector/target/xmvn-connector-4.3.0.jar
%mvn_artifact xmvn-mojo/pom.xml xmvn-mojo/target/xmvn-mojo-4.3.0.jar
%mvn_artifact xmvn-tools/xmvn-resolve/pom.xml xmvn-tools/xmvn-resolve/target/xmvn-resolve-4.3.0.jar
%mvn_artifact xmvn-tools/xmvn-subst/pom.xml xmvn-tools/xmvn-subst/target/xmvn-subst-4.3.0.jar
%mvn_artifact xmvn-tools/xmvn-install/pom.xml xmvn-tools/xmvn-install/target/xmvn-install-4.3.0.jar

version=4.*
tar --delay-directory-restore -xvf target/xmvn-*-bin.tar.gz
chmod -R +rwX %{name}-${version}
# These are installed as doc
rm -f %{name}-${version}/{AUTHORS-XMVN,README-XMVN.md,LICENSE,NOTICE,NOTICE-XMVN}
# Not needed - we use JPackage launcher scripts
rm -Rf %{name}-${version}/lib/{installer,resolver,subst}/
# Irrelevant Maven launcher scripts
rm -f %{name}-${version}/bin/*

%install
%mvn_install

version=4.*
maven_home=%{_datadir}/maven

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -r%{?with_bootstrap:L} %{name}-${version}/* %{buildroot}%{_datadir}/%{name}/

for cmd in mvn mvnDebug; do
    cat <<EOF >%{buildroot}%{_datadir}/%{name}/bin/$cmd
#!/bin/sh -e
export _FEDORA_MAVEN_HOME="%{_datadir}/%{name}"
exec %{_datadir}/maven%{?maven_version_suffix}/bin/$cmd "\${@}"
EOF
    chmod 755 %{buildroot}%{_datadir}/%{name}/bin/$cmd
done

# helper scripts
%jpackage_script org.fedoraproject.xmvn.tools.install.cli.InstallerCli "" "" xmvn/xmvn-install:xmvn/xmvn-api:xmvn/xmvn-core:beust-jcommander:slf4j/api:slf4j/simple:objectweb-asm/asm:commons-compress:commons-lang3:commons-io xmvn-install
%jpackage_script org.fedoraproject.xmvn.tools.resolve.ResolverCli "" "" xmvn/xmvn-resolve:xmvn/xmvn-api:xmvn/xmvn-core:beust-jcommander xmvn-resolve
%jpackage_script org.fedoraproject.xmvn.tools.subst.SubstCli "" "" xmvn/xmvn-subst:xmvn/xmvn-api:xmvn/xmvn-core:beust-jcommander xmvn-subst

# copy over maven boot and lib directories
cp -r%{?with_bootstrap:L} ${maven_home}/boot/* %{buildroot}%{_datadir}/%{name}/boot/
cp -r%{?with_bootstrap:L} ${maven_home}/lib/* %{buildroot}%{_datadir}/%{name}/lib/
ln -sf %{_prefix}/lib/jansi/libjansi.so %{buildroot}%{_datadir}/%{name}/lib/jansi-native/

# possibly recreate symlinks that can be automated with xmvn-subst
%if %{without bootstrap}
%{name}-subst -s -R %{buildroot} %{buildroot}%{_datadir}/%{name}/
%endif

# /usr/bin/xmvn
ln -s %{_datadir}/%{name}/bin/mvn %{buildroot}%{_bindir}/%{name}

# mvn-local symlink
ln -s %{name} %{buildroot}%{_bindir}/mvn-local

# make sure our conf is identical to maven so yum won't freak out
install -d -m 755 %{buildroot}%{_datadir}/%{name}/conf/
cp -P ${maven_home}/conf/settings.xml %{buildroot}%{_datadir}/%{name}/conf/
cp -P ${maven_home}/bin/m2.conf %{buildroot}%{_datadir}/%{name}/bin/

# Make sure javapackages config is not bundled
rm -rf %{buildroot}%{_datadir}/%{name}/{configuration.xml,config.d/,conf/toolchains.xml,maven-metadata/}

# Toolchains
ln -sf %{_jpbindingdir}/xmvn-toolchains.xml %{buildroot}%{_datadir}/%{name}/conf/toolchains.xml


install -p -m 644 %{SOURCE25} %{buildroot}%{_datadir}/%{name}/conf/toolchains-openjdk25.xml
%jp_binding --verbose --base-pkg xmvn-minimal --binding-pkg xmvn-toolchain-openjdk25 --variant openjdk25 --ghost xmvn-toolchains.xml --target %{_datadir}/%{name}/conf/toolchains-openjdk25.xml --requires java-25-openjdk-devel

%files
%{_bindir}/mvn-local

%files minimal -f .mfiles-xmvn
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/bin
%dir %{_datadir}/%{name}/lib
%{_datadir}/%{name}/lib/*.jar
%{_datadir}/%{name}/lib/ext
%{_datadir}/%{name}/lib/jansi-native
%{_datadir}/%{name}/bin/m2.conf
%{_datadir}/%{name}/bin/mvn
%{_datadir}/%{name}/bin/mvnDebug
%{_datadir}/%{name}/boot
%{_datadir}/%{name}/conf

%files core -f .mfiles-core
%license LICENSE NOTICE
%doc AUTHORS README.md

%files mojo -f .mfiles-mojo

%files tools -f .mfiles-tools
%{_bindir}/%{name}-install
%{_bindir}/%{name}-resolve
%{_bindir}/%{name}-subst

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 4.3.0-22
- Latest state for xmvn

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-20
- Suggest Maven OpenJDK 25 binding
- Build with OpenJDK 25

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-19
- Switch javapackages test plan to f43 ref

* Fri Apr 04 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-18
- Add OpenJDK 25 toolchain

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-17
- Switch to javapackages tests from CentOS Stream GitLab

* Sun Mar 16 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-16
- Rebuild for Maven 4.0.0-rc-3

* Sun Mar 16 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-15
- Work around a conflict between XMvn 4 and XMvn 5

* Mon Mar 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-14
- Remove javadoc subpackage

* Tue Feb 25 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-13
- BuildRequire maven even in bootstrap mode

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 18 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-6
- Update xmvn-minimal Requires

* Wed Dec 11 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-5
- Specify smoke test requirements

* Fri Nov 29 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-4
- Drop explicit requires on javapackages-tools

* Fri Nov 22 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-3
- Add bindings for XMvn toolchains

* Mon Oct 07 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-2
- Remove dependency on which

* Fri Sep 27 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-1
- Update to upstream version 4.3.0
- Resolves: rhbz#2315092

* Fri Aug 23 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-21
- Port to commons-compress 1.27

* Tue Aug 20 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-11
- Rebuild for Sisu 0.9.0.M3

* Tue Jul 30 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-10
- Remove workaround for rpm bug 447156

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Feb 16 2024 Marian Koncek <mkoncek@redhat.com> - 4.2.0-8
- Suggest maven-openjdk21

* Fri Feb 09 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-7
- Drop versioned requires on Maven

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-5
- Convert License tag to SPDX format

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 31 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-3
- Rebuild with no changes

* Fri Mar 31 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-2
- Rebuild for Maven 3.9.1

* Mon Mar 20 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-1
- Update to upstream version 4.2.0

* Fri Mar 17 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.0-1
- Update to upstream version 4.1.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 05 2022 Marian Koncek <mkoncek@redhat.com> - 4.0.0-11
- Mimic maven-javadoc-plugin for -source and --release
- Add simple implementation of toolchains

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 22 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0-9
- Port to Modello 2.0.0

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.0.0-8
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 27 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0-7
- Suggest OpenJDK 17 as default Maven binding

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0-5
- Rebuild for Maven 3.8.4

* Mon Nov 08 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0-4
- For now keep suggesting OpenJDK 11 Maven binding

* Wed Nov 03 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0-3
- Workaround build issue with OpenJDK 17
- Suggest OpenJDK 17 as default Maven binding

* Sun Sep 26 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0-2
- Rebuild to update libjansi.so symlink

* Mon Jul 26 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0-1
- Update to upstream version 4.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0~20210709.3b84c99-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20210709.3b84c99-11
- Change logic for JPMS detection by Javadoc MOJO

* Thu Jul 08 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20210708.43c7e67-10
- Fix Javadoc generation for non-JPMS project with JDK 11

* Thu Jul 08 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20210708.54026c1-9
- Update to latest upstream snapshot

* Tue Jun 01 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20191028.da67577-8
- Workaround for rpm bug 447156 - rpm fails to change directory to symlink

* Wed May 26 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20191028.da67577-7
- Conditionally enable Ivy connector

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20191028.da67577-6
- Bootstrap build
- Non-bootstrap build

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 3.1.0-6
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jul 09 2020 Mat Booth <mat.booth@redhat.com> - 3.1.0-5
- Honour source parameter in javadoc mojo

* Fri Jun 26 2020 Alexander Kurtakov <akurtako@redhat.com> 3.1.0-4
- Rebuild to pick jsr250-api switch to jakarta-annotations.

* Thu Jun 25 2020 Alexander Kurtakov <akurtako@redhat.com> 3.1.0-3
- Ignore test failures as they fail when built Java 11.

* Mon Apr 20 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20191028.da67577-5
- Disable Ivy connector

* Wed Feb 19 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20191028.da67577-4
- Require maven-jdk-binding

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20191028.da67577-3
- Implement toolchain manager

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20191028.da67577-2
- Mass rebuild for javapackages-tools 201902

* Mon Oct 28 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20191028.da67577-1
- Update to upstream snapshot of 4.0.0

* Thu Oct 17 2019 Fabio Valentini <decathorpe@gmail.com> - 3.1.0-1
- Update to version 3.1.0.

* Thu Oct 17 2019 Fabio Valentini <decathorpe@gmail.com> - 3.0.0-28
- Bump requirement to maven 3.6.1 and non-compat guava.

* Mon Sep 02 2019 Marian Koncek <mkoncek@redhat.com> - 3.0.0-27
- Port to maven-invoker 3.0.1

* Thu Aug 22 2019 Fabio Valentini <decathorpe@gmail.com> - 3.0.0-26
- Port to xmlunit2.

* Sun Aug 11 2019 Fabio Valentini <decathorpe@gmail.com> - 3.0.0-25
- Disable gradle support by default.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-2
- Prefer namespaced metadata when duplicates are found

* Fri Jun 14 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-1
- Update to upstream version 3.1.0

* Thu May 30 2019 Marian Koncek <mkoncek@redhat.com> - 3.0.0-25
- Update maven-invoker to version 3.0.1

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-24
- Mass rebuild for javapackages-tools 201901

* Fri Apr 19 2019 Marian Koncek <mkoncek@redhat.com> - 3.0.0-23
- Port to Xmlunit 2.6.2

* Sat Apr 13 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-22
- Switch to Maven 3.6.1 and non-compat Guava

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-22
- Port to Gradle 4.4.1

* Wed Aug 01 2018 Severin Gehwolf <sgehwolf@redhat.com> - 3.0.0-21
- Add requirement on javapackages-tools since scripts use
  java-functions.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 05 2018 Michael Simacek <msimacek@redhat.com> - 3.0.0-19
- Remove now unnecessary objenesis from classpath

* Fri May 18 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-18
- Avoid creating temp files during manifest injection
- Resolves: rhbz#1579236

* Wed May  9 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-17
- Switch to commons-compress for manifest manipulation
- Resolves: rhbz#1576358

* Fri Apr 27 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-16
- Remove use of JAXB from xmvn-core to make it work with Java 9

* Thu Apr 19 2018 Michael Simacek <msimacek@redhat.com> - 3.0.0-15
- Fix maven home lookup and layout to match current maven

* Fri Mar 16 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-14
- Fix configuration of aliased plugins
- Resolves: rhbz#1556974

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.0-13
- Escape macros in %%changelog

* Mon Feb 05 2018 Michael Simacek <msimacek@redhat.com> - 3.0.0-12
- Use guava20

* Wed Jan 24 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-11
- Build-require full maven again, instead of maven-lib

* Tue Jan  9 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-10
- BR maven-lib instead of full maven

* Thu Dec 07 2017 Michael Simacek <msimacek@redhat.com> - 3.0.0-9
- Support setting "-Xdoclint:none" in m-javadoc-p >= 3.0.0

* Fri Nov 10 2017 Michael Simacek <msimacek@redhat.com> - 3.0.0-8
- Port to Gradle 4.3.1

* Mon Oct 02 2017 Michael Simacek <msimacek@redhat.com> - 3.0.0-7
- Port to gradle 4.2

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-5
- Remove temporary workaround

* Wed Jun 21 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-4
- Fix installer crash when plugin directory is missing

* Wed Jun 21 2017 Michael Simacek <msimacek@redhat.com> - 3.0.0-3
- Include lib directories for now

* Wed Jun 21 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-2
- Fix loading of XMvn Installer plugins

* Wed Jun 21 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-1
- Update to upstream version 3.0.0

* Wed Apr 19 2017 Michael Simacek <msimacek@redhat.com> - 2.5.0-23
- Update spec for maven 3.5.0

* Wed Apr 19 2017 Michael Simacek <msimacek@redhat.com> - 2.5.0-22
- Temporary changes for maven upgrade

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Michael Simacek <msimacek@redhat.com> - 2.5.0-20
- Remove requires added for maven 3.4.0

* Thu Feb 02 2017 Michael Simacek <msimacek@redhat.com> - 2.5.0-19
- Remove BR on maven-site-plugin

* Tue Jan 31 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-18
- Allow to conditionally build without gradle

* Mon Jan 16 2017 Michael Simacek <msimacek@redhat.com> - 2.5.0-17
- Use reactor artifacts when running xmvn-subst

* Mon Jan 16 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-16
- Allow xmvn to install files who names whitespace

* Mon Aug 15 2016 Michael Simacek <msimacek@redhat.com> - 2.5.0-15
- Switch launcher scripts

* Thu Aug 11 2016 Michael Simacek <msimacek@redhat.com> - 2.5.0-14
- Add Requires on all symlinked jars to xmvn-minimal

* Mon Aug  8 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-13
- Remove temp symlinks

* Mon Aug  8 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-12
- Add temp symlinks needed for updating to Maven 3.4.0

* Mon Jul 04 2016 Michael Simacek <msimacek@redhat.com> - 2.5.0-11
- Don't install POM files for Tycho projects

* Thu Jun 30 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-10
- Full xmvn should require full maven

* Tue Jun 28 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-9
- Introduce xmvn-minimal subpackage

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-8
- Add missing build-requires

* Mon May 30 2016 Michael Simacek <msimacek@redhat.com> - 2.5.0-7
- Add missing BR easymock

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 26 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-5
- Try to procect builddep MOJO against patological cases

* Mon Nov 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-4
- Remove temporary Maven 3.3.9 workaround

* Mon Nov 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-3
- Add temporary workaround for Maven 3.3.9 transition

* Wed Oct 28 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-2
- Fix symlinks in lib/core

* Wed Oct 28 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-1
- Update to upstream version 2.5.0

* Tue Jul 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-5
- Require persistent artifact files in XML resolver API

* Tue Jun 30 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-4
- Port to Gradle 2.5-rc-1

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-2
- Add patches for rhbz#1220394

* Wed May  6 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-1
- Update to upstream version 2.4.0

* Fri Apr 24 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-8
- Port to Gradle 2.4-rc-1

* Thu Apr 16 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-7
- Disable doclint in javadoc:aggregate MOJO executions

* Thu Apr  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-6
- Install mvn-local symlink

* Wed Mar 25 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-5
- Remove workarunds for RPM bug #646523

* Wed Mar 25 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-4
- Port to Gradle 2.3

* Mon Mar 16 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-3
- Build with Maven 3.3.0

* Mon Mar 16 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-2
- Add temporary explicit maven-builder-support.jar symlink

* Thu Mar 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-1
- Update to upstream version 2.3.2

* Fri Mar 06 2015 Michal Srb <msrb@redhat.com> - 2.3.1-4
- Rebuild to fix symlinks in lib/core

* Thu Feb 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.1-3
- Remove temporary explicit ASM symlinks

* Wed Feb 18 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.1-2
- Temporarly add explicit symlinks to ASM

* Fri Feb 13 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.1-1
- Update to upstream version 2.3.1

* Wed Feb 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-1
- Update to upstream version 2.3.0

* Wed Feb  4 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-1
- Update to upstream version 2.2.1

* Fri Jan 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.0-1
- Update to upstream version 2.2.0
- Add connector-gradle subpackage

* Wed Jan 21 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-2
- Add BR on maven-site-plugin
- Resolves: rhbz#1184608

* Mon Jan  5 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-1
- Update to upstream version 2.1.1

* Wed Dec 10 2014 Michal Srb <msrb@redhat.com> - 2.1.0-8
- Add fully qualified osgi version to install plan when tycho detected
- Resolves: rhbz#1172225

* Thu Dec  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.0-7
- Ignore any system dependencies in Tycho projects

* Wed Nov 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.0-6
- Use topmost repository namespace during installation
- Resolves: rhbz#1166743

* Tue Oct 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.0-5
- Fix conversion of Ivy to XMvn artifacts
- Resolves: rhbz#1127804

* Mon Oct 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.0-4
- Fix FTBFS caused by new wersion of plexus-archiver

* Wed Sep 24 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.0-3
- Fix installation of attached Eclipse artifacts

* Wed Sep 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.0-2
- Avoid installing the same attached artifact twice

* Thu Sep  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.0-1
- Update to upstream version 2.1.0
- Remove p2 subpackage

* Fri Jun  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.1-1
- Update to upstream version 2.0.1

* Thu Jun  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-6
- Bump Maven version in build-requires

* Thu Jun  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-5
- Add missing requires on subpackages

* Fri May 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-4
- Don't modify system properties during artifact resolution

* Fri May 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-3
- Add patch to support xmvn.resolver.disableEffectivePom property

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-2
- Add patch for injecting Javapackages manifests

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-1
- Update to upstream version 2.0.0

* Tue Apr 22 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-0.25.gitcb3a0a6
- Use ASM 5.0.1 directly instead of Sisu-shaded ASM

* Fri Mar 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-0.24.gitcb3a0a6
- Override extensions of skipped artifacts

* Fri Mar 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-0.23.gitcb3a0a6
- Skip installation of artifacts which files are not regular files
- Resolves: rhbz#1078967

* Mon Mar 17 2014 Michal Srb <msrb@redhat.com> - 1.5.0-0.22.gitcb3a0a6
- Add missing BR: modello-maven-plugin

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.0-0.21.gitcb3a0a6
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-0.20.gitcb3a0a6
- Fix unowned directory

* Tue Jan 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-0.19.gitcb3a0a6
- Update to pre-release of upstream version 1.5.0

* Mon Dec  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-1
- Update to upstream version 1.4.0

* Thu Nov 14 2013 Michael Simacek <msimacek@redhat.com> - 1.3.0-4
- Update to Sisu 0.1.0

* Thu Nov 14 2013 Michal Srb <msrb@redhat.com> - 1.3.0-3
- Add dep org.sonatype.sisu:sisu-guice::no_aop:

* Fri Nov  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.0-2
- Add wagon-http-shared4 to plexus.core

* Wed Nov 06 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3.0-1
- Update to upstream release 1.3.0

* Tue Nov  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-5
- Require Maven >= 3.1.1-5
- Resolves: rhbz#1014355

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-4
- Rebuild to regenerate broken POMs
- Related: rhbz#1021484

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-3
- Temporarly skip running tests

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-2
- Don't inject manifest if it does not already exist
- Resolves: rhbz#1021484

* Fri Oct 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-1
- Update to upstream version 1.2.0

* Mon Oct 07 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.0-2
- Apply patch for rhbz#1015596

* Tue Oct 01 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.0-1
- Update to upstream version 1.1.0

* Fri Sep 27 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-3
- Add __default package specifier support

* Mon Sep 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.2-2
- Don't try to relativize symlink targets
- Restotre support for relative symlinks

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.2-1
- Update to upstream version 1.0.2

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.0-2
- Workaround broken symlinks for core and connector (#986909)

* Mon Sep 09 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.0-1
- Updating to upstream 1.0.0

* Tue Sep  3 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 1.0.0-0.2.alpha1
- Update to upstream version 1.0.0 alpha1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.5.1-3
- Rebuild without bootstrapping

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.5.1-2
- Install symlink to simplelogger.properties in %%{_sysconfdir}

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.5.1-1
- Update to upstream version 0.5.1

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.5.0-7
- Allow installation of Eclipse plugins in javadir

* Mon Jul 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.5.0-6
- Remove workaround for plexus-archiver bug
- Use sonatype-aether symlinks

* Wed Jun  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.5.0-5
- Fix resolution of tools.jar

* Fri May 31 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.5.0-4
- Fix handling of packages with dots in groupId
- Previous versions also fixed bug #948731

* Tue May 28 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.5.0-3
- Move pre scriptlet to pretrans and implement in lua

* Fri May 24 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.5.0-2
- Fix upgrade path scriptlet
- Add patch to fix NPE when debugging is disabled

* Fri May 24 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.5.0-1
- Update to upstream version 0.5.0

* Fri May 17 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.2-3
- Add patch: install MOJO fix

* Wed Apr 17 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.2-2
- Update plexus-containers-container-default JAR location

* Tue Apr  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.2-1
- Update to upstream version 0.4.2

* Thu Mar 21 2013 Michal Srb <msrb@redhat.com> - 0.4.1-1
- Update to upstream version 0.4.1

* Fri Mar 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-1
- Update to upstream version 0.4.0

* Fri Mar 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-0.7
- Enable tests

* Thu Mar 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-0.6
- Update to newer snapshot

* Wed Mar 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-0.5
- Update to newer snapshot

* Wed Mar 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-0.4
- Set proper permissions for scripts in _bindir

* Tue Mar 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-0.3
- Update to new upstream snapshot
- Create custom /usr/bin/xmvn instead of using %%jpackage_script
- Mirror maven directory structure
- Add Plexus Classworlds config file

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-0.2
- Update to newer snapshot

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-0.1
- Update to upstream snapshot of version 0.4.0

* Mon Feb 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.1-2
- Install effective POMs into a separate directory

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.1-1
- Update to upstream version 0.3.1

* Tue Feb  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.0-1
- Update to upstream version 0.3.0
- Don't rely on JPP symlinks when resolving artifacts
- Blacklist more artifacts
- Fix dependencies

* Thu Jan 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.2.6-1
- Update to upstream version 0.2.6

* Mon Jan 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.2.5-1
- Update to upstream version 0.2.5

* Fri Jan 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.2.4-1
- Update to upstream version 0.2.4

* Wed Jan  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.2.3-1
- Update to upstream version 0.2.3

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.2.2-1
- Update to upstream version 0.2.2

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.2.1-1
- Update to upstream version 0.2.1

* Mon Jan  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.2.0-1
- Update to upstream version 0.2.0
- New major features: depmaps, compat symlinks, builddep MOJO
- Install effective POMs for non-POM artifacts
- Multiple major and minor bugfixes
- Drop support for resolving artifacts from %%_javajnidir

* Fri Dec  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.5-1
- Update to upstream version 0.1.5

* Fri Dec  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.4-1
- Update to upstream version 0.1.4

* Fri Dec  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.3-1
- Update to upstream version 0.1.3

* Fri Dec  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.2-1
- Update to upstream version 0.1.2

* Fri Dec  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.1-1
- Update to upstream version 0.1.1

* Thu Dec  6 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.0-1
- Update to upstream version 0.1.0
- Implement auto requires generator

* Mon Dec  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.2-1
- Update to upstream version 0.0.2

* Thu Nov 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.1-1
- Update to upstream version 0.0.1

* Wed Nov 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0-2
- Add jpackage scripts

* Mon Nov  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0-1
- Initial packaging

## END: Generated by rpmautospec
