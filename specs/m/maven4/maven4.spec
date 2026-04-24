## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 8;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond bootstrap 0

%global xversion 4.0.0-rc-4
%global maven_version_suffix 4
%global bundled_slf4j_version 1.7.36
%global homedir %{_datadir}/maven%{?maven_version_suffix}
%global confdir %{_sysconfdir}/maven%{?maven_version_suffix}

Name:           maven4
Epoch:          1
Version:        4.0.0~rc.4
Release:        %autorelease
Summary:        Java project management and project comprehension tool
# maven itself is Apache-2.0
# bundled slf4j is MIT
License:        Apache-2.0 AND MIT
URL:            https://maven.apache.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/maven/maven-4/%{xversion}/source/apache-maven-%{xversion}-src.tar.gz
Source1:        maven-bash-completion
Source2:        mvn.1

Patch:          0001-Adapt-mvn-script.patch
# Downstream-specific, avoids build-dependency on logback
Patch:          0002-Invoke-logback-via-reflection.patch
Patch:          0003-Port-tests-to-work-with-Mockito-3.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.fasterxml.woodstox:woodstox-core)
BuildRequires:  mvn(com.google.inject:guice::classes:)
BuildRequires:  mvn(commons-cli:commons-cli)
BuildRequires:  mvn(javax.annotation:javax.annotation-api)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-failsafe-plugin)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-api:2.0.9)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-connector-basic:2.0.9)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-impl:2.0.9)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-named-locks:2.0.9)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-spi:2.0.9)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-transport-apache:2.0.9)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-transport-file:2.0.9)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-transport-jdk:2.0.9)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-transport-wagon:2.0.9)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-util:2.0.9)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-file)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-http)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interactivity-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  mvn(org.codehaus.plexus:plexus-sec-dispatcher:4.1.0)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils:4.0.1)
BuildRequires:  mvn(org.codehaus.plexus:plexus-xml)
BuildRequires:  mvn(org.codehaus.woodstox:stax2-api)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  mvn(org.jline:jansi-core)
BuildRequires:  mvn(org.jline:jline-builtins)
BuildRequires:  mvn(org.jline:jline-console)
BuildRequires:  mvn(org.jline:jline-console-ui)
BuildRequires:  mvn(org.jline:jline-reader)
BuildRequires:  mvn(org.jline:jline-style)
BuildRequires:  mvn(org.jline:jline-terminal)
BuildRequires:  mvn(org.jline:jline-terminal-jni)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.slf4j:jcl-over-slf4j:2.0.17)
BuildRequires:  mvn(org.slf4j:slf4j-api:2.0.17)
BuildRequires:  mvn(org.slf4j:slf4j-simple:2.0.17)
%endif

# XXX
#BuildRequires:  mvn(org.slf4j:slf4j-simple::sources:) = %{bundled_slf4j_version}
%if %{without bootstrap}
BuildRequires:  mvn(org.slf4j:slf4j-simple::sources:)
%endif

Requires: %{name}-lib = %{epoch}:%{version}-%{release}
Requires: %{name}-jdk-binding
Suggests: %{name}-openjdk25 = %{epoch}:%{version}-%{release}

Requires(post): alternatives
Requires(postun): alternatives

# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1:4.0.0~rc.2-7

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

%package lib
Summary:        Core part of Maven
# If XMvn is part of the same RPM transaction then it should be
# installed first to avoid triggering rhbz#1014355.
OrderWithRequires: xmvn-minimal

# Maven upstream uses patched version of SLF4J.  They unpack
# slf4j-simple-sources.jar, apply non-upstreamable, Maven-specific
# patch (using a script written in Groovy), compile and package as
# maven-slf4j-provider.jar, together with Maven-specific additions.
Provides:       bundled(slf4j) = %{bundled_slf4j_version}

# JAR symlinks in lib directory
Requires:       aopalliance
Requires:       apache-commons-cli
Requires:       apache-commons-codec
Requires:       google-gson
Requires:       google-guice
Requires:       guava
Requires:       httpcomponents-client
Requires:       httpcomponents-core
Requires:       jakarta-annotations
Requires:       jakarta-inject1.0
Requires:       jcl-over-slf4j2
Requires:       jline
Requires:       maven-resolver2
Requires:       maven-wagon
Requires:       objectweb-asm
Requires:       plexus-containers-component-annotations
Requires:       plexus-interactivity
Requires:       plexus-interpolation
Requires:       plexus-sec-dispatcher4
Requires:       plexus-utils4
Requires:       plexus-xml
Requires:       sisu
Requires:       slf4j2
Requires:       stax2-api
Requires:       woodstox-core

%description lib
Core part of Apache Maven that can be used as a library.

%prep
%autosetup -p1 -C

%pom_remove_dep -r :junit-bom
%pom_remove_dep -r :mockito-bom
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin :bom-builder3 apache-maven

%pom_remove_dep :jline-terminal-ffm impl/maven-jline
%pom_remove_dep :jline-terminal-ffm apache-maven
%pom_remove_dep -r :logback-classic

%pom_disable_module maven-executor impl

find -name '*.java' -exec sed -i 's/\r//' {} +
find -name 'pom.xml' -exec sed -i 's/\r//' {} +

sed -i "s/@{maven_version_suffix}/%{?maven_version_suffix}/" apache-maven/src/assembly/maven/bin/mvn

# not really used during build, but a precaution
find -name '*.jar' -not -path '*/test/*' -delete
find -name '*.class' -delete
find -name '*.bat' -delete

#sed -i 's:\r::' apache-maven/src/conf/settings.xml

# Downloads dependency licenses from the Internet and aggregates them.
# We already ship the licenses in their respective packages.
rm apache-maven/src/main/appended-resources/META-INF/LICENSE.vm

# Disable plugins which are not useful for us
%pom_remove_plugin -r :apache-rat-plugin
%pom_remove_plugin -r :buildnumber-maven-plugin
sed -i "
/buildNumber=/ {
  s/=.*/=Red Hat %{version}-%{release}/
  s/%{dist}$//
}
/timestamp=/ d
" `find -name build.properties`

%mvn_package :apache-maven __noinstall
%mvn_package ::mdo: __noinstall

%mvn_compat_version : 4.0.0-rc-4

%build
%mvn_build -j -f -- -Dproject.build.sourceEncoding=UTF-8

mkdir m2home
(cd m2home
    tar --delay-directory-restore -xvf ../apache-maven/target/*tar.gz
)


%install
%mvn_install

export M2_HOME=$(pwd)/m2home/apache-maven-%{xversion}%{?ver_add}

install -d -m 755 %{buildroot}%{homedir}/conf
install -d -m 755 %{buildroot}%{confdir}
install -d -m 755 %{buildroot}%{_datadir}/bash-completion/completions/

cp -a $M2_HOME/{bin,lib,boot} %{buildroot}%{homedir}/
%if %{without bootstrap}
xmvn-subst -s -R %{buildroot} %{buildroot}%{homedir}
%endif

find %{buildroot}%{homedir} -name \*.so -print -delete

install -p -m 644 %{SOURCE2} %{buildroot}%{homedir}/bin/
gzip -9 %{buildroot}%{homedir}/bin/mvn.1
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/bash-completion/completions/mvn%{?maven_version_suffix}
mv $M2_HOME/bin/m2.conf %{buildroot}%{_sysconfdir}/m2%{?maven_version_suffix}.conf
ln -sf %{_sysconfdir}/m2%{?maven_version_suffix}.conf %{buildroot}%{homedir}/bin/m2.conf
mv $M2_HOME/conf/maven.properties %{buildroot}%{confdir}/
ln -sf %{confdir}/maven.properties %{buildroot}%{homedir}/conf/
mv $M2_HOME/conf/settings.xml %{buildroot}%{confdir}/
ln -sf %{confdir}/settings.xml %{buildroot}%{homedir}/conf/settings.xml
mv $M2_HOME/conf/logging %{buildroot}%{confdir}/
ln -sf %{confdir}/logging %{buildroot}%{homedir}/conf

# Ghosts for alternatives
install -d -m 755 %{buildroot}%{_bindir}/
install -d -m 755 %{buildroot}%{_mandir}/man1/
touch %{buildroot}%{_bindir}/{mvn,mvnenc,mvnDebug}
touch %{buildroot}%{_mandir}/man1/{mvn,mvnenc,mvnDebug}.1

# Versioned commands and manpages
%if 0%{?maven_version_suffix:1}
ln -s %{homedir}/bin/mvn %{buildroot}%{_bindir}/mvn%{maven_version_suffix}
ln -s %{homedir}/bin/mvnenc %{buildroot}%{_bindir}/mvnenc%{maven_version_suffix}
ln -s %{homedir}/bin/mvnDebug %{buildroot}%{_bindir}/mvnDebug%{maven_version_suffix}
ln -s %{homedir}/bin/mvn.1.gz %{buildroot}%{_mandir}/man1/mvn%{maven_version_suffix}.1.gz
ln -s %{homedir}/bin/mvnenc.1.gz %{buildroot}%{_mandir}/man1/mvnenc%{maven_version_suffix}.1.gz
ln -s %{homedir}/bin/mvnDebug.1.gz %{buildroot}%{_mandir}/man1/mvnDebug%{maven_version_suffix}.1.gz
%endif

# JDK bindings
install -d -m 755 %{buildroot}%{_javaconfdir}/
ln -sf %{_jpbindingdir}/maven%{?maven_version_suffix}.conf %{buildroot}%{_javaconfdir}/maven%{?maven_version_suffix}.conf

echo JAVA_HOME=%{_jvmdir}/jre-25-openjdk >%{buildroot}%{_javaconfdir}/maven%{?maven_version_suffix}-openjdk25.conf

%jp_binding --verbose --variant openjdk25 --ghost maven%{?maven_version_suffix}.conf --target %{_javaconfdir}/maven%{?maven_version_suffix}-openjdk25.conf --provides %{name}-jdk-binding --requires java-25-openjdk-headless --recommends java-25-openjdk-devel
touch %{buildroot}%{_javaconfdir}/maven%{?maven_version_suffix}-unbound.conf
%jp_binding --verbose --variant unbound --ghost maven%{?maven_version_suffix}.conf --target %{_javaconfdir}/maven%{?maven_version_suffix}-unbound.conf --provides %{name}-jdk-binding

%post
update-alternatives --install %{_bindir}/mvn mvn %{homedir}/bin/mvn %{?maven_alternatives_priority}0 \
--slave %{_bindir}/mvnenc mvnenc %{homedir}/bin/mvnenc \
--slave %{_bindir}/mvnDebug mvnDebug %{homedir}/bin/mvnDebug \
--slave %{_mandir}/man1/mvn.1.gz mvn1 %{homedir}/bin/mvn.1.gz \
--slave %{_mandir}/man1/mvnenc.1.gz mvnenc1 %{homedir}/bin/mvnenc.1.gz \
--slave %{_mandir}/man1/mvnDebug.1.gz mvnDebug1 %{homedir}/bin/mvn.1.gz

%postun
if [[ $1 -eq 0 ]]; then update-alternatives --remove mvn %{homedir}/bin/mvn; fi

%files lib -f .mfiles
%doc README.md
%license LICENSE NOTICE
%{homedir}
%exclude %{homedir}/bin/mvn*
%dir %{confdir}
%dir %{confdir}/logging
%config %{_javaconfdir}/maven%{?maven_version_suffix}*.conf
%config(noreplace) %{_sysconfdir}/m2%{?maven_version_suffix}.conf
%config(noreplace) %{confdir}/maven.properties
%config(noreplace) %{confdir}/settings.xml
%config(noreplace) %{confdir}/logging/maven.logger.properties

%files
%{homedir}/bin/mvn*
%ghost %{_bindir}/mvn
%ghost %{_bindir}/mvnenc
%ghost %{_bindir}/mvnDebug
%{_datadir}/bash-completion
%ghost %{_mandir}/man1/mvn.1.gz
%ghost %{_mandir}/man1/mvnenc.1.gz
%ghost %{_mandir}/man1/mvnDebug.1.gz
%if 0%{?maven_version_suffix:1}
%{_bindir}/mvn%{maven_version_suffix}
%{_bindir}/mvnenc%{maven_version_suffix}
%{_bindir}/mvnDebug%{maven_version_suffix}
%{_mandir}/man1/mvn%{maven_version_suffix}.1.gz
%{_mandir}/man1/mvnenc%{maven_version_suffix}.1.gz
%{_mandir}/man1/mvnDebug%{maven_version_suffix}.1.gz
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1:4.0.0~rc.4-8
- Latest state for maven4

* Wed Aug 06 2025 Marian Koncek <mkoncek@redhat.com> - 1:4.0.0~rc.4-6
- Remove trailing backslash from scriptlet and bootstrap package

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0.0~rc.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.4-4
- Suggest OpenJDK 25 binding

* Fri Jul 11 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.4-1
- Update to upstream version 4.0.0-rc-4
- Build with OpenJDK 25

* Fri Jul 11 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.3-6
- Fix alternatives slave name

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.3-5
- Switch javapackages test plan to f43 ref

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.3-4
- Enforce gating on OpenJDK 25 tests

* Fri Apr 04 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.3-3
- Add OpenJDK 25 binding

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.3-2
- Switch to javapackages tests from CentOS Stream GitLab

* Fri Mar 14 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.3-1
- Update to upstream version 4.0.0-rc-3

* Wed Mar 05 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.2-7
- Remove javadoc subpackage

* Thu Feb 27 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.2-6
- Add java.compiler module to unbound test plan

* Wed Feb 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.2-5
- Update filtered test package name

* Wed Feb 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.2-4
- Configure tests for maven4 rename

* Wed Feb 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.2-3
- Non-bootstrap build

* Wed Feb 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.2-2
- Bootstrap build

* Wed Feb 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.0.0~rc.2-1
- Update to upstream version 4.0.0-rc-2

* Fri Feb 14 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.9-1
- Rename to maven4

* Fri Feb 14 2025 Mikolaj Izdebski <mizdebsk@redhat.com>
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
