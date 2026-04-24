## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 30;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

%if %{without bootstrap} && %{undefined rhel}
%bcond_without bnd_maven_plugin
%else
%bcond_with bnd_maven_plugin
%endif

Name:           aqute-bnd
Version:        6.3.1
Release:        %autorelease
Summary:        BND Tool
# Part of jpm is under BSD, but jpm is not included in binary RPM
License:        Apache-2.0 OR EPL-2.0
URL:            https://bnd.bndtools.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{name}-%{version}.tar.gz
# removes bundled jars from upstream tarball
# run as:
# ./generate-tarball.sh
Source1:        generate-tarball.sh

# Auxiliary parent pom, packager-written
Source2:        aggregator.pom
Source3:        https://repo1.maven.org/maven2/biz/aQute/bnd/aQute.libg/%{version}/aQute.libg-%{version}.pom
Source4:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bnd/%{version}/biz.aQute.bnd-%{version}.pom
Source5:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bndlib/%{version}/biz.aQute.bndlib-%{version}.pom
Source6:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bnd.annotation/%{version}/biz.aQute.bnd.annotation-%{version}.pom
Source7:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bnd.ant/%{version}/biz.aQute.bnd.ant-%{version}.pom
Source8:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bnd.util/%{version}/biz.aQute.bnd.util-%{version}.pom

Patch:          0001-Disable-removed-commands.patch
Patch:          0002-Port-to-OSGI-7.0.0.patch
Patch:          0003-Remove-unmet-dependencies.patch
Patch:          0004-Port-to-OpenJDK-21.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.junit:junit-bom:pom:)
BuildRequires:  mvn(org.osgi:osgi.annotation)
BuildRequires:  mvn(org.osgi:osgi.cmpn)
BuildRequires:  mvn(org.osgi:osgi.core)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
%endif
%if %{with bnd_maven_plugin}
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.apache.maven.shared:maven-mapping)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)
%endif

# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 6.3.1-23

%description
The bnd tool helps you create and diagnose OSGi bundles.
The key functions are:
- Show the manifest and JAR contents of a bundle
- Wrap a JAR so that it becomes a bundle
- Create a Bundle from a specification and a class path
- Verify the validity of the manifest entries
The tool is capable of acting as:
- Command line tool
- File format
- Directives
- Use of macros

%package -n aqute-bndlib
Summary:        BND library

%description -n aqute-bndlib
%{summary}.

%if %{with bnd_maven_plugin}
%package -n bnd-maven-plugin
Summary:        BND Maven plugin

%description -n bnd-maven-plugin
%{summary}.
%endif

%prep
%autosetup -p1 -C

# the commands pull in more dependencies than we want (felix-resolver, jetty)
rm biz.aQute.bnd/src/aQute/bnd/main/{ExportReportCommand,MbrCommand,RemoteCommand,ReporterLogger,ResolveCommand,Shell}.java

cp %SOURCE2 pom.xml
sed -i 's|${Bundle-Version}|%{version}|' biz.aQute.bndlib/src/aQute/bnd/osgi/bnd.info

%if %{without bnd_maven_plugin}
%pom_disable_module maven
%endif

# libg
pushd aQute.libg
cp -p %{SOURCE3} pom.xml
%pom_add_parent org.fedoraproject.xmvn.aqute-bnd:aggregator:any
%pom_add_dep org.osgi:osgi.cmpn
popd

# bnd.annotation
pushd biz.aQute.bnd.annotation
cp -p %{SOURCE6} pom.xml
%pom_add_parent org.fedoraproject.xmvn.aqute-bnd:aggregator:any
%pom_add_dep org.osgi:osgi.core
%pom_add_dep org.osgi:osgi.cmpn
popd

# bndlib
pushd biz.aQute.bndlib
cp -p %{SOURCE5} pom.xml
%pom_add_parent org.fedoraproject.xmvn.aqute-bnd:aggregator:any
%pom_add_dep org.osgi:osgi.cmpn
%pom_add_dep biz.aQute.bnd:aQute.libg:%{version}
%pom_add_dep biz.aQute.bnd:biz.aQute.bnd.annotation:%{version}
popd

# bnd.ant
pushd biz.aQute.bnd.ant
cp -p %{SOURCE7} pom.xml
%pom_add_parent org.fedoraproject.xmvn.aqute-bnd:aggregator:any
popd

# bnd
cp -r biz.aQute.bnd.exporters/src/aQute/bnd/exporter biz.aQute.bnd/src/aQute/bnd/
pushd biz.aQute.bnd
cp -p %{SOURCE4} pom.xml
%pom_add_parent org.fedoraproject.xmvn.aqute-bnd:aggregator:any
%pom_remove_dep :biz.aQute.resolve
%pom_remove_dep :biz.aQute.repository
%pom_remove_dep :biz.aQute.bnd.exporters
%pom_remove_dep :biz.aQute.bnd.reporter
%pom_remove_dep :biz.aQute.remote.api
%pom_remove_dep :snakeyaml
%pom_remove_dep :jline
%pom_remove_dep org.osgi:org.osgi.service.coordinator
%pom_remove_dep org.osgi:org.osgi.service.resolver
popd

# bnd.util
pushd biz.aQute.bnd.util
cp -p %{SOURCE8} pom.xml
%pom_add_parent org.fedoraproject.xmvn.aqute-bnd:aggregator:any
%pom_add_dep biz.aQute.bnd:aQute.libg:%{version}
popd

%pom_remove_dep -r org.osgi:org.osgi.dto
%pom_remove_dep -r org.osgi:org.osgi.framework
%pom_remove_dep -r org.osgi:org.osgi.namespace.contract
%pom_remove_dep -r org.osgi:org.osgi.namespace.extender
%pom_remove_dep -r org.osgi:org.osgi.namespace.implementation
%pom_remove_dep -r org.osgi:org.osgi.namespace.service
%pom_remove_dep -r org.osgi:org.osgi.resource
%pom_remove_dep -r org.osgi:org.osgi.service.log
%pom_remove_dep -r org.osgi:org.osgi.service.repository
%pom_remove_dep -r org.osgi:org.osgi.service.serviceloader
%pom_remove_dep -r org.osgi:org.osgi.util.function
%pom_remove_dep -r org.osgi:org.osgi.util.promise
%pom_remove_dep -r org.osgi:org.osgi.util.tracker

%pom_xpath_remove -r pom:project/pom:dependencies/pom:dependency/pom:scope

# maven-plugins
cp -r biz.aQute.bnd.maven/src/aQute/bnd/maven/lib/configuration maven/bnd-maven-plugin/src/main/java/aQute/bnd/maven/lib
cp -r biz.aQute.bnd.maven/src/aQute/bnd/maven/lib/executions maven/bnd-maven-plugin/src/main/java/aQute/bnd/maven/lib
pushd maven
%pom_remove_dep -r :biz.aQute.bnd.maven
# Unavailable reactor dependency - org.osgi.impl.bundle.repoindex.cli
%pom_disable_module bnd-indexer-maven-plugin
# Requires unbuilt parts of bnd
%pom_disable_module bnd-export-maven-plugin
%pom_disable_module bnd-reporter-maven-plugin
%pom_disable_module bnd-resolver-maven-plugin
%pom_disable_module bnd-run-maven-plugin
%pom_disable_module bnd-testing-maven-plugin
# Integration tests require Internet access
%pom_remove_plugin -r :maven-invoker-plugin
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_remove_plugin -r :flatten-maven-plugin
popd

%mvn_alias biz.aQute.bnd:biz.aQute.bnd :bnd biz.aQute:bnd
%mvn_alias biz.aQute.bnd:biz.aQute.bndlib :bndlib biz.aQute:bndlib

%mvn_package biz.aQute.bnd:biz.aQute.bndlib bndlib
%mvn_package biz.aQute.bnd:biz.aQute.bnd.annotation bndlib
%mvn_package biz.aQute.bnd:aQute.libg bndlib
%mvn_package org.fedoraproject.xmvn.aqute-bnd:aggregator __noinstall
%mvn_package biz.aQute.bnd:bnd-plugin-parent __noinstall
%if %{with bnd_maven_plugin}
%mvn_package biz.aQute.bnd:bnd-maven-plugin maven
%mvn_package biz.aQute.bnd:bnd-baseline-maven-plugin maven
%endif

%build
%mvn_build -j

%install
%mvn_install

install -d -m 755 %{buildroot}%{_sysconfdir}/ant.d
echo "aqute-bnd slf4j/api slf4j/simple osgi-annotation osgi-core osgi-compendium" >%{buildroot}%{_sysconfdir}/ant.d/%{name}

%jpackage_script aQute.bnd.main.bnd "" "" aqute-bnd:slf4j/slf4j-api:slf4j/slf4j-simple:osgi-annotation:osgi-core:osgi-compendium bnd 1

%files -f .mfiles
%license LICENSE
%{_bindir}/bnd
%config(noreplace) %{_sysconfdir}/ant.d/*

%files -n aqute-bndlib -f .mfiles-bndlib
%license LICENSE

%if %{with bnd_maven_plugin}
%files -n bnd-maven-plugin -f .mfiles-maven
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 6.3.1-30
- Latest state for aqute-bnd

* Thu Sep 04 2025 Jiri Vanek <jvanek@redhat.com> - 6.3.1-29
- manual bodhi update for jdk25 needed on selected pkgs

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 6.3.1-28
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.3.1-26
- Build with OpenJDK 25

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.3.1-25
- Switch javapackages test plan to f43 ref

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.3.1-24
- Switch to javapackages tests from CentOS Stream GitLab

* Thu Mar 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.3.1-23
- Drop javadoc package

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.3.1-21
- Drop explicit requires on javapackages-tools

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 6.3.1-10
- Rebuilt for java-21-openjdk as system jdk

* Tue Feb 20 2024 Marian Koncek <mkoncek@redhat.com> - 6.3.1-9
- Port to OpenJDK 21

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.3.1-6
- Convert License tag to SPDX format

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 07 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.3.1-4
- Conditionally disable bnd-maven-plugin

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Stephen Gallagher <sgallagh@redhat.com> - 6.3.1-2
- Re-enable maven plugin for RHEL 10+

* Wed Sep 07 2022 Marian Koncek <mkoncek@redhat.com> - 6.3.1-1
- Update to upstream version 6.3.1

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 03 2022 Marian Koncek <mkoncek@redhat.com> - 6.2.0-1
- Update to upstream version 6.2.0

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 5.2.0-9
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 5.2.0-7
- Enable biz.aQute.bnd.ant

* Fri Sep 24 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.2.0-6
- Rename maven_plugin build conditional to bnd_maven_plugin

* Tue Aug 10 2021 Sérgio Basto <sergio@serjux.com> - 5.2.0-5
- reenable bnd-maven-plugin

* Mon Aug 02 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 5.2.0-4
- Add parent to biz.aQute.bnd/pom.xml (fixes [WARNING] JAR will be
  empty - no content was marked for inclusion!)
- Remove scope from dependencies in pom.xml files (fixes missing
  dependencies, dependencies marked with scope provided are ignored by
  the rpm dependency generator)
- Drop some more commands: shell, exportreport, mbr (uses parts that
  are not packaged)
- Resolves: rhbz#1985566

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.2.0-2
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Marian Koncek <mkoncek@redhat.com> - 5.2.0-1
- Update to upstream version 5.2.0

* Mon Dec 14 2020 Jerry James <loganjerry@gmail.com> - 4.3.1-3
- Update jansi path for jansi 1.x and jline path for jline 2.x

* Wed Nov 25 2020 Mat Booth <mat.booth@redhat.com> - 4.3.1-2
- Add OSGi metadata

* Tue Sep 29 2020 Marian Koncek <mkoncek@redhat.com> - 5.1.2-1
- Update to upstream version 5.1.2

* Tue Jul 28 2020 Mat Booth <mat.booth@redhat.com> - 4.3.1-1
- Update to latest 4.x release

* Mon Jul 27 2020 Mat Booth <mat.booth@redhat.com> - 4.3.0-1
- Update to upstream version 4.3.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Mat Booth <mat.booth@redhat.com> - 3.5.0-10
- Fix NIO linkage error when running on Java 8 due to incorrect cross-compilation

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 3.5.0-9
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jun 23 2020 Marian Koncek <mkoncek@redhat.com> - 5.1.1-1
- Update to upstream version 5.1.1

* Fri Apr 24 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-2
- Disable bnd-maven-plugin

* Wed Jan 29 2020 Marian Koncek <mkoncek@redhat.com> - 5.0.0-1
- Update to upstream version 5.0.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.0-2
- Mass rebuild for javapackages-tools 201902

* Wed Oct 09 2019 Marian Koncek <mkoncek@redhat.com> - 4.3.0-1
- Update to upstream version 4.3.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 04 2019 Marian Koncek <mkoncek@redhat.com> - 4.2.0-1
- Update to upstream version 4.2.0

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.0-6
- Mass rebuild for javapackages-tools 201901

* Fri Apr 12 2019 Marian Koncek <mkoncek@redhat.com> - 3.5.0-6
- Port to OSGI 7.0.0

* Fri Apr 12 2019 Marian Koncek <mkoncek@redhat.com> - 3.5.0-5
- Port to OSGI 7.0.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018 Severin Gehwolf <sgehwolf@redhat.com> - 3.5.0-4
- Add requirement on javapackages-tools for bnd script.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 13 2017 Michael Simacek <msimacek@redhat.com> - 3.5.0-1
- Update to upstream version 3.5.0

* Mon Oct 02 2017 Troy Dawson <tdawson@redhat.com> - 3.4.0-3
- Cleanup spec file conditionals

* Sat Sep 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-2
- Remove unneeded javadoc plugin

* Tue Sep 12 2017 Michael Simacek <msimacek@redhat.com> - 3.4.0-1
- Update to upstream version 3.4.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 10 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.0-5
- Don't use legacy Ant artifact coordinates

* Mon Oct 10 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.0-4
- Allow conditional builds without Ant tasks

* Mon Oct 10 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.0-3
- Allow conditional builds without Maven plugin

* Thu Oct 06 2016 Michael Simacek <msimacek@redhat.com> - 3.3.0-2
- Fix ant.d classpath

* Thu Sep 29 2016 Michael Simacek <msimacek@redhat.com> - 3.3.0-1
- Update to upstream version 3.3.0
- Build against osgi-{core,compendium}

* Tue Sep 27 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-5
- Add felix-scr-annotations to classpath

* Mon Sep 26 2016 Michael Simacek <msimacek@redhat.com> - 3.2.0-4
- Use felix-annotations

* Wed Sep 14 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-3
- Build and install Maven plugins
- Resolves: rhbz#1375904

* Wed Jun  1 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-2
- Install ant.d config files

* Tue May 24 2016 Michael Simacek <msimacek@redhat.com> - 3.2.0-1
- Update to upstream version 3.2.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 17 2015 Michael Simacek <msimacek@redhat.com> - 2.4.1-2
- Fix Tool header generation

* Wed Jul 08 2015 Michael Simacek <msimacek@redhat.com> - 2.4.1-1
- Update to upstream version 2.4.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-15
- Disable javadoc doclint

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-13
- Use .mfiles generated during build

* Fri May 09 2014 Jaromir Capik <jcapik@redhat.com> - 0.0.363-12
- Fixing ambiguous base64 class

* Fri May 09 2014 Gil Cattaneo <puntogil@libero.it> 0.0.363-11
- fix rhbz#991985
- add source compatibility with ant 1.9
- remove and rebuild from source aQute.runtime.jar
- update to current packaging guidelines

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.0.363-10
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.0.363-6
- Get rid of unusable eclipse plugins to simplify dependencies

* Fri Mar 02 2012 Jaromir Capik <jcapik@redhat.com> - 0.0.363-5
- Fixing build failures on f16 and later

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-3
- Resurrection of bundled non-class files

* Thu Sep 22 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-2
- Bundled classes removed
- jpackage-utils dependency added to the javadoc subpackage

* Wed Sep 21 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-1
- Initial version (cloned from aqute-bndlib 0.0.363)

## END: Generated by rpmautospec
