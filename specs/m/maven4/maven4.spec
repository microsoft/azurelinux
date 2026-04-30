## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
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
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1:4.0.0~rc.4-8
- test: add initial lock files

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

* Tue Aug 20 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.6-8
- Rebuild for Sisu 0.9.0.M3

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.9.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 05 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.6-6
- Rebuild

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 1:3.9.6-5
- bump of release for for java-21-openjdk as system jdk

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.6-2
- Make JDK bindings work with different Maven version suffixes

* Mon Dec 04 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.6-1
- Update to upstream version 3.9.6

* Thu Sep 21 2023 Trung Lê <8@tle.id.au> - 1:3.9.4-3
- Add maven-openjdk21

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.4-2
- Convert License tag to SPDX format

* Fri Aug 18 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.4-1
- Update to upstream version 3.9.4

* Tue Aug 15 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.1-4
- Build with default JDK 17

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 31 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.1-2
- Rebuild with no changes

* Tue Mar 21 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.9.1-1
- Update to upstream version 3.9.1

* Fri Jan 27 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.8.6-4
- Turn hard dependency on java-devel into a weak dependencny

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 13 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.8.6-2
- Add workaround for guava symlink creation with xmvn-subst

* Tue Sep 06 2022 Marian Koncek <mkoncek@redhat.com> - 1:3.8.6-1
- Update to upstream version 3.8.6

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu May 05 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.8.5-2
- Add build-dependency on extra-enforcer-rules

* Thu Apr 21 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.8.5-1
- Update to upstream version 3.8.5

* Thu Jan 27 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.8.4-3
- Suggest OpenJDK 17 as default Maven binding

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 17 2021 Marian Koncek <mkoncek@redhat.com> - 1:3.8.4-1
- Update to upstream version 3.8.4

* Fri Nov 05 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.3-14
- Do not override JAVA_HOME set by user
- Resolves: rhbz#2020478

* Tue Nov 02 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.3-13
- Suggest OpenJDK 17 as default Maven binding

* Fri Sep 24 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.3-12
- Add OpenJDK 17 binding

* Fri Sep 24 2021 Marian Koncek <mkoncek@redhat.com> - 1:3.6.3-11
- Create a symlink to jansi shared object
- Related: rhbz#1994935

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.3-9
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 24 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.3-2
- Move launcher scripts from maven-lib to maven package

* Mon Dec 14 2020 Jerry James <loganjerry@gmail.com> - 1:3.6.3-7
- Update jansi dep to jansi1

* Wed Sep 30 2020 Christopher Tubbs <ctubbsii@fedoraproject.org> - 1:3.6.3-6
- Remove unneeded commons-logging from runtime class path (rhbz#1883751)
- Also remove redundant commons-codec

* Tue Aug 25 2020 Fabio Valentini <decathorpe@gmail.com> - 1:3.6.3-5
- Adapt to cdi-api switch from jboss-interceptor to jakarta-interceptor.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1:3.6.3-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 25 2020 Alexander Kurtakov <akurtako@redhat.com> 1:3.6.3-2
- Switch jsr250 to jakarta-anntations.

* Mon May 25 2020 Fabio Valentini <decathorpe@gmail.com> - 1:3.6.3-1
- Update to version 3.6.3.

* Thu May 14 2020 Fabio Valentini <decathorpe@gmail.com> - 1:3.6.2-1
- Update to version 3.6.2.

* Thu May 14 2020 Fabio Valentini <decathorpe@gmail.com> - 1:3.6.1-6
- Port to modello 1.11.

* Thu Feb 27 2020 Marian Koncek <mkoncek@redhat.com> - 1:3.6.3-1
- Update to upstream version 3.6.3

* Wed Feb 05 2020 Dinesh Prasanth M K <dmoluguw@redhat.com> - 1:3.6.1-5
- Require the updated version of slf4j.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.2-4
- Build with OpenJDK 8

* Thu Jan 23 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.2-3
- Implement JDK bindings

* Thu Nov 21 2019 Fabio Valentini <decathorpe@gmail.com> - 1:3.6.1-3
- Require the correct version of guava.

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.2-2
- Mass rebuild for javapackages-tools 201902

* Mon Nov 04 2019 Fabio Valentini <decathorpe@gmail.com> - 1:3.6.1-2
- Fix postun scriptlet.

* Wed Oct 16 2019 Fabio Valentini <decathorpe@gmail.com> - 1:3.6.1-1
- Update to version 3.6.1.

* Thu Oct 03 2019 Marian Koncek <mkoncek@redhat.com> - 1:3.6.2-1
- Update to upstream version 3.6.2

* Thu Aug 29 2019 Fabio Valentini <decathorpe@gmail.com> - 1:3.5.4-12
- Remove dependency on logback-classic.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Marian Koncek <mkoncek@redhat.com> - 1:3.6.1-5
- Port to modello version 1.11

* Thu May 30 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.1-4
- Backport upstream fix for Tycho P2 integarion

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.1-3
- Mass rebuild for javapackages-tools 201901

* Wed Apr 17 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.4-10
- Update to Mockito 2

* Wed Apr 17 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.1-2
- Update to Mockito 2

* Sat Apr 13 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.6.1-1
- Update to upstream version 3.6.1

* Fri Apr 12 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.4-6
- Update SLF4J version to 1.7.26

* Wed Mar 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1:3.5.4-9
- Fix dependency on alternatives

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 22 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.4-7
- Revert unwanted dependency change

* Mon Oct 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1:3.5.4-6
- Specify alternatives as dep, not chkconfig

* Mon Jul 30 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:3.5.4-2
- Require javapackages-tools for maven-lib.

* Thu Jul 26 2018 Michael Simacek <msimacek@redhat.com> - 1:3.5.4-4
- Symlink jansi-linux to lib

* Mon Jul 23 2018 Michael Simacek <msimacek@redhat.com> - 1:3.5.4-3
- Fix license tag to include MIT for bundled slf4j

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Michael Simacek <msimacek@redhat.com> - 1:3.5.4-1
- Update to upstream version 3.5.4

* Wed Apr 18 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.3-2
- Introduce alternatives

* Thu Mar 15 2018 Michael Simacek <msimacek@redhat.com> - 1:3.5.3-1
- Update to upstream version 3.5.3

* Thu Mar 15 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.2-5
- Don't install mvnyjp in bindir

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:3.5.2-4
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Michael Simacek <msimacek@redhat.com> - 1:3.5.2-2
- Use guava20

* Wed Oct 25 2017 Michael Simacek <msimacek@redhat.com> - 1:3.5.2-1
- Update to upstream version 3.5.2

* Fri Sep 15 2017 Michael Simacek <msimacek@redhat.com> - 1:3.5.0-7
- Fix FTBFS after maven-remote-reources-plugin update

* Tue Aug 08 2017 Michael Simacek <msimacek@redhat.com> - 1:3.5.0-6
- Generate build number based on package release number

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 08 2017 Michael Simacek <msimacek@redhat.com> - 1:3.5.0-4
- Update logback conditional to replace logback usage with reflection

* Wed Apr 26 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.0-3
- Add apache-commons-codec to plexus.core
- Resolves: rhbz#1445738

* Wed Apr 19 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.0-2
- Add alias for maven-aether-provider

* Tue Apr 11 2017 Michael Simacek <msimacek@redhat.com> - 1:3.5.0-1
- Update to upstream version 3.5.0

* Fri Mar  3 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.3.9-9
- Fix bash-completion directory ownership

* Wed Mar 01 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-8
- Avoid subshell for build-jar-repository

* Thu Feb 16 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.3.9-7
- Conditionalize weak dependencies

* Tue Feb 14 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.3.9-6
- Remove BR on maven-javadoc-plugin

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-5
- Remove BR on buildnumber-plugin

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-4
- Remove buildnumber-plugin from build

* Thu Feb 02 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-3
- Add conditional for logback

* Thu Feb 02 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-2
- Remove site-plugin and enforce-plugin from build

* Wed Feb 01 2017 Michael Simacek <msimacek@redhat.com> - 1:3.3.9-1
- Downgrade to 3.3.9

* Wed Dec 14 2016 Michael Simacek <msimacek@redhat.com> - 3.4.0-0.6.20161118git8ae1a3e
- Bump slf4j version

* Fri Nov 18 2016 Michael Simacek <msimacek@redhat.com> - 3.4.0-0.5.20161118git8ae1a3e
- Restore compatibility with maven-polyglot

* Fri Nov 18 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-0.4.20161118git8ae1a3e
- Versioned bundled(slf4j) provides

* Fri Nov 18 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-0.3.20161118git8ae1a3e
- Update to latest upstream snapshot
- Source-bundle slf4j-simple

* Mon Aug 15 2016 Michael Simacek <msimacek@redhat.com> - 3.4.0-0.2.20160807git9f2452a
- Use patched upstream launcher instead of custom script

* Mon Aug  8 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-0.1.20160807git9f2452a
- Update to 3.4.0 snapshot

* Fri Jul  1 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-6
- Add missing BR on maven-enforcer-plugin

* Tue Jun 28 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-5
- Add maven-lib subpackage

* Thu Apr  7 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-4
- Force SLF4J SimpleLogger re-initialization
- Resolves: rhbz#1324832

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-2
- Fix symlinks: add commons-lang3 and remove geronimo-annotation

* Fri Nov 13 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.9-1
- Update to upstream version 3.3.9

* Mon Nov  2 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.8-1
- Update to upstream version 3.3.8

* Fri Jul 10 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.3-3
- Recommend java-devel instead of requiring it

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.3-1
- Update to upstream version 3.3.3

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-2
- Install mvnDebug and mvnyjp in bindir
- Update manpage
- Resolves: rhbz#1207850

* Mon Mar 16 2015 Michal Srb <msrb@redhat.com> - 3.3.1-1
- Add commons-io, commons-lang and jsoup to plexus.core (Resolves: rhbz#1202286)

* Fri Mar 13 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-1
- Update to upstream version 3.3.1

* Thu Mar 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.0-1
- Update to upstream version 3.3.0

* Wed Feb 18 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.5-2
- Add objectweb-asm to plexus.core

* Mon Jan 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.5-1
- Update to upstream version 3.2.5

* Sat Dec  6 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.2.3-4
- Fix bash completion filename

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.3-3
- Remove legacy Obsoletes/Provides for maven2

* Mon Sep 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.3-2
- Update patches

* Fri Aug 22 2014 Michal Srb <msrb@redhat.com> - 3.2.3-1
- Update to upstream version 3.2.3

* Wed Jun 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.2-1
- Update to upstream version 3.2.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-10
- Fix artifact pattern in %%mvn_file invocation

* Wed Jun  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-9
- Install additional lib symlinks only for JAR files

* Wed Jun  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-8
- Fix dangling symlinks in Maven lib dir
- Resolves: rhbz#1104396

* Mon Jun  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-7
- Clean up patches
- Add patch for MNG-5613

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-6
- Remove BuildRequires on maven-surefire-provider-junit4

* Mon Mar 17 2014 Michal Srb <msrb@redhat.com> - 3.2.1-5
- Add missing BR: modello-maven-plugin

* Fri Mar  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-4
- Set logback dependency scope to provided

* Mon Feb 24 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-3
- Add patch for MNG-5591

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-2
- Migrate to Wagon subpackages

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-1
- Remove BR on plexus-containers-container-default

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-1
- Update to upstream version 3.2.1

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-1
- Update to upstream version 3.2.0

* Mon Dec 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-15
- Read user and system config files in maven-script

* Wed Nov 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-14
- Update to Sisu 0.1.0 and Guice 3.1.6

* Fri Nov  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-13
- Add wagon-http-shared4 to plexus.core

* Tue Nov  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-6
- Update F20 to upstream bugfix release 3.1.1

* Tue Nov  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-5
- Add OrderWithRequires: xmvn
- Related: rhbz#1014355

* Tue Oct 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-4
- Add explicit requires

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-3
- Rebuild to regenerate broken POM files
- Related: rhbz#1021484

* Mon Oct 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-10
- Add dependencies of wagon-http-shaded to plexus.core
- Remove objectweb-asm from plexus.core
- Add explicit requires
- Resolves: rhbz#1023872

* Mon Oct  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.1-1
- Update to upstream version 3.1.1
- Remove patch for MNG-5503 (included upstream)

* Mon Sep 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-9
- Synchronize JAR list in lib/ with upstream release
- Remove test dependencies on aopalliance and cglib

* Thu Aug 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-8
- Migrate from easymock 1 to easymock 3
- Resolves: rhbz#1002432

* Fri Aug 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-7
- Add patch for MNG-5503
- Resolves: rhbz#991454

* Mon Aug 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-6
- Update Aether to 0.9.0.M3

* Mon Aug 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-5
- Prepare for update to Aether 0.9.0.M3

* Fri Aug  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-4
- Remove workaround for incompatible plexus-utils

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-2
- Install simplelogger.properties into %%{_sysconfdir}

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-1
- Update to upstream version 3.1.0

* Fri Jul 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-8
- Use sonatype-aether symlinks

* Mon May 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-7
- Move bash-completion files to primary location
- Resolves: rhbz#918000

* Fri May 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-6
- Remove unneeded BR: async-http-client
- Add Requires on java-devel

* Thu May  2 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-5
- BR proper aether subpackages
- Resolves: rhbz#958160

* Fri Apr 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-4
- Add missing BuildRequires

* Tue Mar 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-3
- Make ext/ a subdirectory of lib/

* Tue Mar 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-2
- In maven-script don't override M2_HOME if already set

* Fri Mar  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.5-1
- Update to upstream version 3.0.5
- Move settings.xml to /etc

* Mon Feb 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-32
- Remove xerces-j2 from plexus.core realm
- Resolves: rhbz#784816

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-31
- Migrate BR from sisu to sisu subpackages

* Wed Feb  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-30
- Remove unneeded R: maven-local

* Fri Jan 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-29
- Drop support for local mode
- Build with xmvn, rely on auto-requires

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-28
- Move mvn-local and mvn-rpmbuild out of %%_bindir

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-27
- Move some parts to maven-local package

* Thu Nov 22 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-26
- Force source >= 1.5 and target >= source

* Mon Nov 19 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-25
- Fix license tag

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-24
- Install NOTICE file with javadoc package

* Tue Nov 13 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-23
- Temporarly require Plexus POMs as a workaround

* Mon Nov 12 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-22
- Drop dependency on maven2-common-poms
- Drop support for /etc/maven/fragments

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-21
- Add support for custom jar/pom/fragment directories

* Thu Nov  8 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-20
- Remove all slf4j providers except nop from maven realm

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-19
- Add aopalliance and cglib to maven-model-builder test dependencies

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-18
- Add objectweb-asm to classpath

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-17
- Add aopalliance, cglib, slf4j to classpath

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-16
- Don't echo JAVA_HOME in maven-script
- Add bash completion for -Dproject.build.sourceEncoding

* Mon Oct 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-15
- Add a few bash completion goals

* Wed Oct 24 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-14
- Enable test skipping patch only for local mode (#869399)

* Fri Oct 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-13
- Make sure we look for requested pom file and not resolved

* Thu Oct 18 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-12
- Look into maven.repo.local first to handle corner-case packages (#865599)
- Finish handling of compatibility packages
- Disable animal-sniffer temporarily in Fedora as well

* Mon Aug 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-11
- Disable animal-sniffer on RHEL

* Wed Jul 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-10
- Fix exit code of mvn-rpmbuild outside of mock
- Fix bug in compatibility jar handling

* Mon Jul 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-9
- Run redundant dependency checks only in mock

* Tue Jul 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-8
- Add manual page

* Mon Jun 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-7
- Implement redundant dependency checks

* Thu May 24 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.0.4-6
- Bug 824789 -Use the version if it is possible.

* Mon May 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-5
- Use Obsoletes instead of Conflicts

* Mon May 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-4
- Obsolete and provide maven2

* Thu Mar 29 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-3
- Make package noarch again to simplify bootstrapping

* Thu Feb  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-2
- Make javadoc noarch
- Make compilation source level 1.5
- Fix borked tarball unpacking (reason unknown)

* Tue Jan 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-1
- Update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-16
- Add maven2-common-poms to Requires

* Tue Oct 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-15
- Provide mvn script now instead of maven2
- Conflict with older versions of maven2

* Tue Aug 30 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-14
- Fix test scope skipping

* Mon Aug 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-13
- Remove unnecessary deps causing problems from lib/
- Add utf-8 source encoding patch

* Thu Jul 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-12
- Disable debug package creation

* Thu Jul 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-11
- Change to arch specific since we are using _libdir for _jnidir

* Tue Jul 26 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-10
- Add bash completion (#706856)

* Mon Jul  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-9
- Add resolving from jnidir and java-jni

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-8
- Add maven-parent to BR/R

* Wed Jun 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-7
- Process fragments in alphabetical order

* Tue Jun 21 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-6
- Fix handling of fallback default_poms
- Add empty-dep into maven package to not require maven2 version

* Fri Jun 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-5
- Process fragments directly instead of maven2-depmap.xml
- Expect fragments in /usr/share/maven-fragments
- Resolve poms also from /usr/share/maven-poms

* Mon Jun  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-4
- Add help to mvn-rpmbuild and mvn-local (rhbz#710448)

* Tue May 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-3
- Improve and clean up depmap handling for m2/m3 repos

* Mon Apr 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-2
- Enable MAVEN_OPTS override in scripts

* Fri Mar  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-1
- Update to 3.0.3
- Add ext subdirectory to lib

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-0.1.rc1
- Update to 3.0.3rc1
- Enable tests again

* Thu Feb 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-2
- Added mvn-rpmbuild script to be used in spec files
- mvn-local is now mixed mode (online with javadir priority)
- Changed mvn.jpp to mvn.local

* Fri Jan 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-1
- Update to latest version (3.0.2)
- Ignore test failures temporarily

* Wed Jan 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-6
- Fix bug #669034

* Tue Jan 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-5
- Fix bugs #667625 #667614 and #667636
- Install maven metadata so they are not downloaded when mvn is run
- Rename mvn3-local to mvn-local
- Add more comments to resolver patch

* Tue Dec 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-4
- Add fedora local resolver
- Fix quoting of arguments to mvn scripts
- Add javadoc subpackage
- Make jars versionless and remove unneeded clean section

* Wed Dec  1 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-3
- Remove maven-ant-tasks jar in prep
- Make fragment file as %%config

* Tue Nov 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-2
- Added apache-commons-parent to BR after commons changes

* Tue Oct 12 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-1
- Initial package with vanilla maven (no jpp mode yet)

## END: Generated by rpmautospec
