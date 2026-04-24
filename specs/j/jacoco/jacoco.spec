# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           jacoco
Version:        0.8.11
Release: 7%{?dist}
Summary:        Java Code Coverage for Eclipse
License:        EPL-2.0
URL:            http://www.eclemma.org/jacoco/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch
Source0:        https://github.com/jacoco/jacoco/archive/v%{version}/%{name}-%{version}.tar.gz
# Adapt to maven-doxia 2.0.0
# The deprecated org.codehaus.doxia.sink.Sink interface was removed
Patch:          %{name}-maven-doxia-2.patch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(args4j:args4j)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.mojo:exec-maven-plugin)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-analysis)
BuildRequires:  mvn(org.ow2.asm:asm-commons)
BuildRequires:  mvn(org.ow2.asm:asm-tree)

# required by wrapper scripts
Requires:       javapackages-tools

%description
JaCoCo is a free code coverage library for Java, 
which has been created by the EclEmma team based on the lessons learned 
from using and integration existing libraries over the last five years. 

%package    maven-plugin
Summary:    A Jacoco plugin for maven
%description maven-plugin
A Jacoco plugin for maven.

%{?javadoc_package}

%prep

# -p1: strip one level dir in patch(es)
%autosetup -p1
%pom_remove_dep :asm-bom org.jacoco.build
# disable unnecessary modules
%pom_disable_module ../jacoco org.jacoco.build
%pom_disable_module ../org.jacoco.doc org.jacoco.build
%pom_disable_module ../org.jacoco.examples org.jacoco.build
%pom_disable_module ../org.jacoco.tests org.jacoco.build

# Remove unnecessary dependency on maven-javadoc-plugin
%pom_remove_plugin -r :maven-javadoc-plugin

# Remove enforcer plugin that causes build failure of 'Jacoco :: Maven Plugin'
%pom_remove_plugin -r :maven-enforcer-plugin

# Don't build jars with classifier ":nodeps:"
%pom_remove_plugin :maven-shade-plugin \
    org.jacoco.ant \
    org.jacoco.cli

# remove unnecessary plugin
%pom_remove_plugin -r :spotless-maven-plugin

# remove beanshell plugin
# later, we need to redefine various properties defined by it
%pom_remove_plugin :beanshell-maven-plugin \
    org.jacoco.build

# buildnumber plugin was removed from f38
%pom_remove_plugin :buildnumber-maven-plugin \
    org.jacoco.build

# Remove "requires osgi(org.apache.ant)"
%pom_xpath_remove 'pom:configuration/pom:instructions/pom:Require-Bundle' \
    org.jacoco.ant

# Remove requires on maven-plugin-plugin:report
%pom_xpath_remove 'pom:execution[pom:id = "report"]' \
    jacoco-maven-plugin

# Define properties
%pom_xpath_inject 'pom:properties' '
    <unqualifiedVersion>${project.version}</unqualifiedVersion>
    <buildQualifier>${maven.build.timestamp}</buildQualifier>
    <qualified.bundle.version>${unqualifiedVersion}.${buildQualifier}</qualified.bundle.version>
    <jacoco.runtime.package.name>org.jacoco.agent.rt.internal_fedora</jacoco.runtime.package.name>' \
      org.jacoco.build

# install jacoco-maven-plugin package
%mvn_package ":jacoco-maven-plugin:{jar,pom}:{}:" maven-plugin

# install jacoco package
%mvn_package ":{org.}*:{jar,pom}:runtime:"

# don't install parent package
%mvn_package :root __noinstall
%mvn_package :org.jacoco.build __noinstall

for x in `find | grep pom.xml$` ; do
  if cat $x | grep -e "<bytecode.version>.*7" ; then
    sed "s;<bytecode.version>.*7.*;<bytecode.version>8</bytecode.version>;g" -i $x;
  fi
done


%build
%mvn_build -f -- -Dproject.build.sourceEncoding=UTF-8 -Dbuild.date=$(date +%Y/%m/%d)

%install
%mvn_install

# ant config
mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo %{name} %{name}/org.jacoco.ant objectweb-asm/asm > %{buildroot}%{_sysconfdir}/ant.d/%{name}

# wrapper script
%jpackage_script org.jacoco.cli.internal.Main "" "" jacoco/org.jacoco.cli:args4j:objectweb-asm:jacoco/org.jacoco.core:jacoco/org.jacoco.report jacococli true

%files -f .mfiles
%config(noreplace) %{_sysconfdir}/ant.d/%{name}
%doc README.md
%license LICENSE.md
%{_bindir}/jacococli

%files maven-plugin -f .mfiles-maven-plugin

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 0.8.11-6
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 23 2025 Jerry James <loganjerry@gmail.com> - 0.8.11-4
- Add patch for maven-doxia 2.0.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 0.8.11-1
- Rebuilt for java-21-openjdk as system jdk
- bumped bytecode level of jdk12+ profile to 8
- bumped to 0.8.11 whcih claims to support jdk21. 
-- the change of bytecode level is still needed

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 25 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 0.8.10-1
- Update to version 0.8.10

* Mon Feb 20 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 0.8.8-6
- Reduce dependency

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 27 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 0.8.8-4
- Remove conditional statement of patch

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 0.8.8-2
- Rebuilt for Drop i686 JDKs

* Tue Apr 05 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 0.8.8-1
- New upstream release 0.8.8

* Thu Feb 10 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 0.8.7-6
- Added a patch to handle maven-reporting-api 3.1.0

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0.8.7-5
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 22 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 0.8.7-3
- Redefined properties defined with beanshell-maven-plugin, which was removed
- Add wrapper scripts for jacococli

* Sat Nov 20 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 0.8.7-2
- Remove requires osgi(org.apache.ant)

* Thu Nov 18 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 0.8.7-1
- New upstream release 0.8.7

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Fabio Valentini <decathorpe@gmail.com> - 0.8.3-3
- Remove unnecessary dependency on maven-javadoc-plugin.
- Use xmvn-javadoc unconditionally, fixing javadoc generation.
- Add files for javadoc subpackage.

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0.8.3-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Apr 02 2020 Jiri Vanek <jvanek@redhat.com> 0.8.3-1
- bumped to sources 8.3 which are aligned with currenlty shiped ojkectweb-asm
- aligned pugins with current fedora state
- org.apache.felix:maven-bundle-plugin should be returned, its absence is killing jdk11 exported packages generation
- the manual manifest is not an option

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 12 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.8-4
- Relax OSGi version requirements on ASM

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Alexander Kurtakov <akurtako@redhat.com> 0.7.8-1
- Update to upstream 0.7.8.

* Thu Aug 25 2016 Roman Vais <rvais@redhat.com> - 0.7.7-3
- Remove outdated dependency and enforcer plugin
- Replace problematic patch with pom_xpath_inject macro

* Thu Jun 16 2016 Alexander Kurtakov <akurtako@redhat.com> 0.7.7-2
- Add missing BRs.

* Tue Jun 7 2016 Alexander Kurtakov <akurtako@redhat.com> 0.7.7-1
- Update to upstream 0.7.7.

* Fri Feb 19 2016 Alexander Kurtakov <akurtako@redhat.com> 0.7.6-1
- Update to upstream 0.7.6.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Alexander Kurtakov <akurtako@redhat.com> 0.7.5-1
- Update to upstream 0.7.5.

* Tue Mar 31 2015 akurtakov <akurtakov@localhost.localdomain> 0.7.4-1
- Update to upstream 0.7.4.

* Mon Feb 23 2015 Alexander Kurtakov <akurtako@redhat.com> 0.7.3-1
- Update to upstream 0.7.3.

* Mon Feb 16 2015 Alexander Kurtakov <akurtako@redhat.com> 0.7.2-3
- Add asm to ant.d (RHBZ#1192749).

* Sat Oct 11 2014 Jiri Vanek <jvanek@redhat.com> 0.7.2-2
- added premain-class to agent.rt.jar
- RH1151442

* Mon Sep 15 2014 Alexander Kurtakov <akurtako@redhat.com> 0.7.2-1
- Update to upstream 0.7.2.

* Fri Jun 13 2014 Michal Srb <msrb@redhat.com> - 0.7.1-5
- Migrate to %%mvn_install

* Mon Jun 9 2014 Alexander Kurtakov <akurtako@redhat.com> 0.7.1-4
- Fix FTBFS.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Alexander Kurtakov <akurtako@redhat.com> 0.7.1-1
- Update to 0.7.1.

* Thu Mar 27 2014 Alexander Kurtakov <akurtako@redhat.com> 0.7.0-1
- Update to upstream version 0.7.0.

* Thu Mar 6 2014 Alexander Kurtakov <akurtako@redhat.com> 0.6.5-1
- Update to new upstream release.
- Remove licence check ant call - breaks in rawhide.

* Mon Feb 24 2014 Orion Poplawski <orion@cora.nwra.com> 0.6.4-3
- Add ant config

* Fri Feb 21 2014 Alexander Kurtakov <akurtako@redhat.com> 0.6.4-2
- R java-headless.
- Adapt to new package names.
- Fix rpmlint warnings.

* Thu Dec 19 2013 Alexander Kurtakov <akurtako@redhat.com> 0.6.4-1
- Update to 0.6.4 upstream release.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.6.3-4
- Move maven plugin to the %%{javadir}.

* Mon Jul 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.6.3-3
- Move plugin artifact to plugin subpackage
- Resolves: rhbz#987084

* Thu Jun 20 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.6.3-2
- Add missing BR.

* Thu Jun 20 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.6.3-1
- Update to 0.6.3.

* Wed May 8 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.6.2-1
- Update to latest upstream.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.6.0-3
- Merge the master branch in.

* Thu Nov 29 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.6.0-2
- Package correct agent.
- Improve the name of packages.

* Wed Nov 21 2012 Alexander Kurtakov <akurtako@redhat.com> 0.6.0-1
- Update to upstream 0.6.0.

* Mon Sep 17 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.5.9-2
- Add BR to fest-assert.

* Tue Sep 11 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.5.9-1
- Update to upstream 0.5.10 release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.5.7-0.5
- Dropped dependency version to maven-shade-plugin.

* Tue May 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.5.7-0.4
- Fixed rpmlint warnings.

* Tue May 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.5.7-0.3
- Removed symlink to java.

* Tue May 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.5.7-0.2
- Restructured packages
- Generated javadoc as set of plain files.

* Thu May 3 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.5.7-0.1
- Initial release.
