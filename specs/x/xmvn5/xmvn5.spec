## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond bootstrap 0

Name:           xmvn5
Version:        5.1.0
Release:        %autorelease
Summary:        Local Extensions for Apache Maven
License:        Apache-2.0
URL:            https://fedora-java.github.io/xmvn/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source:         https://github.com/fedora-java/xmvn/releases/download/%{version}/xmvn-%{version}.tar.zst
Source21:       toolchains-openjdk21.xml
Source25:       toolchains-openjdk25.xml

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(io.kojan:kojan-parent:pom:)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-api:2.0.9)
BuildRequires:  mvn(org.apache.maven:maven-api-core:4.0.0-rc-4)
BuildRequires:  mvn(org.apache.maven:maven-api-model:4.0.0-rc-4)
BuildRequires:  mvn(org.apache.maven:maven-artifact:4.0.0-rc-4)
BuildRequires:  mvn(org.apache.maven:maven-core:4.0.0-rc-4)
BuildRequires:  mvn(org.apache.maven:maven-model:4.0.0-rc-4)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api:4.0.0-rc-4)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.xmlunit:xmlunit-assertj3)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
BuildRequires:  mvn(org.xmlunit:xmlunit-assertj3)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  kojan-xml
%endif
# Maven home is used as template for XMvn home
BuildRequires:  maven4
Requires:       %{name}-minimal = %{version}-%{release}
Requires:       maven4

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
Requires:       maven4-jdk-binding
Requires:       maven4-lib
Requires:       maven-resolver2
Requires:       maven-shared-utils
Requires:       plexus-cipher
Requires:       plexus-classworlds
Requires:       plexus-containers-component-annotations
Requires:       plexus-interpolation
Requires:       plexus-sec-dispatcher4
Requires:       plexus-utils4
Requires:       sisu
Requires:       slf4j2
Suggests:       maven4-openjdk25

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
maven_home=%{_datadir}/maven4
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
xmvn -B -o -Dmaven.test.skip=true -P\!quality verify
%mvn_artifact pom.xml
%mvn_artifact xmvn-parent/pom.xml
%mvn_artifact xmvn-tools/pom.xml
%mvn_artifact xmvn-api/pom.xml xmvn-api/target/xmvn-api-%{version}.jar
%mvn_artifact xmvn-core/pom.xml xmvn-core/target/xmvn-core-%{version}.jar
%mvn_artifact xmvn-connector/pom.xml xmvn-connector/target/xmvn-connector-%{version}.jar
%mvn_artifact xmvn-mojo/pom.xml xmvn-mojo/target/xmvn-mojo-%{version}.jar
%mvn_artifact xmvn-tools/xmvn-resolve/pom.xml xmvn-tools/xmvn-resolve/target/xmvn-resolve-%{version}.jar
%mvn_artifact xmvn-tools/xmvn-subst/pom.xml xmvn-tools/xmvn-subst/target/xmvn-subst-%{version}.jar
%mvn_artifact xmvn-tools/xmvn-install/pom.xml xmvn-tools/xmvn-install/target/xmvn-install-%{version}.jar

version=5.*
tar --delay-directory-restore -xvf target/xmvn-*-bin.tar.gz
chmod -R +rwX xmvn-${version}
# These are installed as doc
rm -f xmvn-${version}/{AUTHORS-XMVN,README-XMVN.md,LICENSE,NOTICE,NOTICE-XMVN}
# Not needed - we use JPackage launcher scripts
rm -Rf xmvn-${version}/lib/{installer,resolver,subst}/
# Irrelevant Maven launcher scripts
rm -f xmvn-${version}/bin/*

%mvn_compat_version : %{version}

%install
%mvn_install

version=5.*
maven_home=%{_datadir}/maven4

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -r%{?with_bootstrap:L} xmvn-${version}/* %{buildroot}%{_datadir}/%{name}/

for cmd in mvn mvnDebug; do
    cat <<EOF >%{buildroot}%{_datadir}/%{name}/bin/$cmd
#!/bin/sh -e
export _FEDORA_MAVEN_HOME="%{_datadir}/%{name}"
exec %{_datadir}/maven4%{?maven_version_suffix}/bin/$cmd "\${@}"
EOF
    chmod 755 %{buildroot}%{_datadir}/%{name}/bin/$cmd
done

# helper scripts
%jpackage_script org.fedoraproject.xmvn.tools.install.cli.InstallerCli "" "" %{name}/xmvn-install:%{name}/xmvn-api:%{name}/xmvn-core:kojan-xml/kojan-xml:picocli/picocli:slf4j2/api-2.0.17:slf4j2/simple-2.0.17:objectweb-asm/asm:commons-compress:commons-lang3:commons-io %{name}-install
%jpackage_script org.fedoraproject.xmvn.tools.resolve.ResolverCli "" "" %{name}/xmvn-resolve:%{name}/xmvn-api:%{name}/xmvn-core:kojan-xml/kojan-xml:picocli/picocli %{name}-resolve
%jpackage_script org.fedoraproject.xmvn.tools.subst.SubstCli "" "" %{name}/xmvn-subst:%{name}/xmvn-api:%{name}/xmvn-core:kojan-xml/kojan-xml:picocli/picocli %{name}-subst

# copy over maven boot and lib directories
cp -r%{?with_bootstrap:L} ${maven_home}/boot/* %{buildroot}%{_datadir}/%{name}/boot/
cp -r%{?with_bootstrap:L} ${maven_home}/lib/* %{buildroot}%{_datadir}/%{name}/lib/

# possibly recreate symlinks that can be automated with xmvn-subst
%if %{without bootstrap}
xmvn-subst -s -R %{buildroot} %{buildroot}%{_datadir}/%{name}/
%endif

# /usr/bin/%{name}
ln -s %{_datadir}/%{name}/bin/mvn %{buildroot}%{_bindir}/%{name}

# make sure our conf is identical to maven so yum won't freak out
install -d -m 755 %{buildroot}%{_datadir}/%{name}/conf/
cp -P ${maven_home}/conf/settings.xml %{buildroot}%{_datadir}/%{name}/conf/
cp -P ${maven_home}/bin/m2.conf %{buildroot}%{_datadir}/%{name}/bin/

# Make sure javapackages config is not bundled
rm -rf %{buildroot}%{_datadir}/%{name}/{configuration.xml,config.d/,conf/toolchains.xml,maven-metadata/}

# Toolchains
ln -sf %{_jpbindingdir}/%{name}-toolchains.xml %{buildroot}%{_datadir}/%{name}/conf/toolchains.xml


install -p -m 644 %{SOURCE25} %{buildroot}%{_datadir}/%{name}/conf/toolchains-openjdk25.xml
%jp_binding --verbose --base-pkg %{name}-minimal --binding-pkg %{name}-toolchain-openjdk25 --variant openjdk25 --ghost %{name}-toolchains.xml --target %{_datadir}/%{name}/conf/toolchains-openjdk25.xml --requires java-25-openjdk-devel

%files

%files minimal -f .mfiles-xmvn
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/bin
%dir %{_datadir}/%{name}/lib
%{_datadir}/%{name}/lib/*.jar
%{_datadir}/%{name}/lib/ext
%{_datadir}/%{name}/lib/jline-native
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
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 5.1.0-6
- Latest state for xmvn5

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.1.0-4
- Suggest Maven OpenJDK 25 binding

* Sat Jul 12 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.1.0-1
- Port to Maven 4.0.0-rc-4
- Build with OpenJDK 25

* Fri Jun 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-2
- Fix BR in bootstrap mode

* Wed Jun 11 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-1
- Update to upstream version 5.0.0

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0~20250515.054327.git.9016d86-4
- Add OpenJDK 25 toolchain

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0~20250515.054327.git.9016d86-3
- Drop mvn-local symlink

* Wed May 21 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0~20250515.054327.git.9016d86-2
- Onboard package into gating

* Wed May 21 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0~20250515.054327.git.9016d86-1
- Initial packaging
## END: Generated by rpmautospec
