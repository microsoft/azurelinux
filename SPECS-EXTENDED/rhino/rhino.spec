%global scm_release Rhino%(v=%{version}; echo ${v//\./_})_Release
%global test262_commit f94fc660cc3c59b1f2f9f122fc4d44b4434b935c
%global test262_shortcommit %(c=%{test262_commit}; echo ${c:0:7})

Name:           rhino
Version:        1.7.14
Release:        13%{?dist}
Summary:        Rhino

# rhino itself is MPLv2.0 but use other codes, breakdown:
# BSD: toolsrc/org/mozilla/javascript/tools/debugger/treetable/*
#      src/org/mozilla/javascript/v8dtoa/* except FastDtoaBuilder.java
# Automatically converted from old format: MPLv2.0 and BSD - review is highly recommended.
License:        MPL-2.0 AND LicenseRef-Callaway-BSD
URL:            https://mozilla.github.io/rhino
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch
ExcludeArch:    %{ix86}

Source0:        %{url}/archive/%{scm_release}/%{name}-%{version}.tar.gz
Source1:        https://repo1.maven.org/maven2/org/mozilla/%{name}/%{version}/%{name}-%{version}.pom
Source2:        https://repo1.maven.org/maven2/org/mozilla/%{name}-engine/%{version}/%{name}-engine-%{version}.pom
Source3:        https://repo1.maven.org/maven2/org/mozilla/%{name}-runtime/%{version}/%{name}-runtime-%{version}.pom
# required for tests
Source4:        https://github.com/tc39/test262/archive/%{test262_shortcommit}/test262-%{test262_shortcommit}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(jakarta.xml.soap:jakarta.xml.soap-api)
Requires:       javapackages-tools

%description
Rhino is an open-source implementation of JavaScript written entirely in Java.
It is typically embedded into Java applications to provide scripting to end
users. Full jar including tools, excluding the JSR-223 Script Engine wrapper.

%package -n %{name}-engine
Summary:        Rhino Engine
%description -n %{name}-engine
Rhino Javascript JSR-223 Script Engine wrapper.

%package -n %{name}-runtime
Summary:        Rhino Runtime
%description -n %{name}-runtime
Rhino JavaScript runtime jar, excludes tools & JSR-223 Script Engine wrapper.

%{?javadoc_package}

%prep
%autosetup -p1 -n %{name}-%{scm_release}

# Uncomment to include test262
tar --extract --strip-component=1 --file=%{SOURCE4} --directory=test262

# jar in tests is used by requireJarTest
find -type f '(' -name '*.jar' -o -name '*.class' ')' -not -path './testsrc/*' -print -delete

# requires netscape.security
rm -rf testsrc/tests/src

mkdir %{name}
mkdir %{name}-engine
mkdir %{name}-runtime

# use simplest pom as parent pom
cp %{SOURCE1} pom.xml
cp %{SOURCE1} %{name}/pom.xml
cp %{SOURCE2} %{name}-engine/pom.xml
cp %{SOURCE3} %{name}-runtime/pom.xml

%pom_add_dep junit:junit:4.13.2:test %{name}
%pom_add_dep org.yaml:snakeyaml:1.28:test %{name}
%pom_add_dep jakarta.xml.soap:jakarta.xml.soap-api:1.4.0:test %{name}

# needed by surefire plugin
%pom_add_dep org.apache.commons:commons-lang3:3.8.1:test %{name}
%pom_add_dep commons-io:commons-io:2.6:test %{name}

%pom_xpath_set pom:artifactId %{name}-parent
%pom_xpath_set pom:name %{name}-parent
%pom_xpath_inject pom:project '<packaging>pom</packaging>'

%pom_remove_parent . \
    %{name} \
    %{name}-engine \
    %{name}-runtime

%pom_xpath_inject pom:project '
    <modules>
      <module>%{name}</module>
      <module>%{name}-engine</module>
      <module>%{name}-runtime</module>
    </modules>'

%pom_add_plugin org.codehaus.mojo:build-helper-maven-plugin \
    %{name} '
    <executions>
      <execution>
        <id>add-source</id>
        <goals>
          <goal>add-source</goal>
        </goals>
        <configuration>
          <sources>
            <source>${project.basedir}/../src</source>
            <source>${project.basedir}/../toolsrc</source>
            <source>${project.basedir}/../xmlimplsrc</source>
          </sources>
        </configuration>
      </execution>
      <execution>
        <id>add-test-source</id>
        <goals>
          <goal>add-test-source</goal>
        </goals>
        <configuration>
          <sources>
            <source>${project.basedir}/../examples</source>
            <source>${project.basedir}/../testsrc</source>
          </sources>
        </configuration>
      </execution>
    </executions>'

%pom_xpath_inject pom:project/pom:build '
    <resources>
      <resource>
        <directory>${project.basedir}/../src</directory>
        <excludes>
          <exclude>**/*.java</exclude>
          <exclude>build.xml</exclude>
          <exclude>manifest</exclude>
        </excludes>
      </resource>
      <resource>
        <directory>${project.basedir}/../toolsrc</directory>
        <excludes>
          <exclude>**/*.java</exclude>
          <exclude>build.xml</exclude>
          <exclude>manifest</exclude>
        </excludes>
      </resource>
    </resources>
    <testResources>
      <testResource>
        <directory>${project.basedir}/../testsrc</directory>
        <excludes>
          <exclude>**/*.java</exclude>
        </excludes>
      </testResource>
    </testResources>' \
      %{name}

%pom_add_plugin :maven-surefire-plugin \
    %{name} '
    <configuration>
      <argLine>
        -Xss1280k
        -Dfile.encoding=UTF-8
        --add-opens java.desktop/javax.swing.table=ALL-UNNAMED
      </argLine>
      <excludes>
        <exclude>**/benchmarks/**</exclude>
      </excludes>
      <forkCount>64</forkCount>
      <reuseForks>false</reuseForks>
      <systemPropertyVariables>
        <java.awt.headless>true</java.awt.headless>
        <mozilla.js.tests>testsrc/tests</mozilla.js.tests>
        <mozilla.js.tests.timeout>60000</mozilla.js.tests.timeout>
        <user.language>en</user.language>
        <user.country>US</user.country>
        <user.timezone>America/Los_Angeles</user.timezone>
        <TEST_OPTLEVEL>-1</TEST_OPTLEVEL>
        <TEST_262_OPTLEVEL>-1</TEST_262_OPTLEVEL>
        <test262properties>testsrc/test262.properties</test262properties>
      </systemPropertyVariables>
      <workingDirectory>${project.basedir}/../</workingDirectory>
    </configuration>'

%pom_add_plugin :maven-resources-plugin \
    %{name}-engine \
    %{name}-runtime '
    <executions>
      <execution>
        <id>copy-resources</id>
        <phase>generate-sources</phase>
        <goals>
          <goal>copy-resources</goal>
        </goals>
        <configuration>
          <outputDirectory>${project.build.outputDirectory}</outputDirectory>
          <resources>
            <resource>
              <directory>${project.basedir}/../%{name}/target/classes</directory>
            </resource>
          </resources>
        </configuration>
      </execution>
    </executions>'

%pom_add_plugin :maven-jar-plugin \
    %{name} '
    <configuration>
      <archive>
        <manifestEntries>
          <Main-Class>org.mozilla.javascript.tools.shell.Main</Main-Class>
          <Implementation-Title>Mozilla Rhino</Implementation-Title>
          <Implementation-Version>${project.version}</Implementation-Version>
          <Automatic-Module-Name>org.mozilla.rhino</Automatic-Module-Name>
          <Bundle-SymbolicName>org.mozilla.rhino</Bundle-SymbolicName>
        </manifestEntries>
      </archive>
      <excludes>
        <exclude>META-INF/services/**</exclude>
        <exclude>org/mozilla/javascript/engine/**</exclude>
      </excludes>
    </configuration>'

%pom_add_plugin :maven-jar-plugin \
    %{name}-engine '
    <configuration>
      <archive>
        <manifestEntries>
          <Automatic-Module-Name>org.mozilla.rhino.engine</Automatic-Module-Name>
        </manifestEntries>
      </archive>
      <includes>
        <include>META-INF/services/**</include>
        <include>org/mozilla/javascript/engine/**</include>
      </includes>
    </configuration>'

%pom_add_plugin :maven-jar-plugin \
    %{name}-runtime '
    <configuration>
      <archive>
        <manifestEntries>
          <Bundle-SymbolicName>org.mozilla.rhino-runtime</Bundle-SymbolicName>
        </manifestEntries>
      </archive>
      <excludes>
        <exclude>META-INF/services/**</exclude>
        <exclude>org/mozilla/javascript/engine/**</exclude>
        <exclude>org/mozilla/javascript/tools/**</exclude>
      </excludes>
    </configuration>'

%mvn_package :%{name}-parent \
    __noinstall

# Compatibility
%mvn_alias :%{name} rhino:js
%mvn_file :%{name} rhino/%{name} %{name}

%build
# Ignore test
%mvn_build -f -s -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%jpackage_script org.mozilla.javascript.tools.shell.Main "" "" rhino rhino true
%jpackage_script org.mozilla.javascript.tools.debugger.Main "" "" rhino rhino-debugger true
%jpackage_script org.mozilla.javascript.tools.jsc.Main "" "" rhino rhino-jsc true

mkdir -p %{buildroot}%{_mandir}/man1/
install -m 644 man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%files -n %{name} -f .mfiles-%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}-debugger
%{_bindir}/%{name}-jsc
%{_mandir}/man1/%{name}.1*
%license LICENSE.txt NOTICE.txt NOTICE-tools.txt
%doc README.md CODE_OF_CONDUCT.md RELEASE-NOTES.md

%files -n %{name}-engine -f .mfiles-%{name}-engine
%license LICENSE.txt
%doc README.md CODE_OF_CONDUCT.md RELEASE-NOTES.md

%files -n %{name}-runtime -f .mfiles-%{name}-runtime
%license LICENSE.txt NOTICE.txt
%doc README.md CODE_OF_CONDUCT.md RELEASE-NOTES.md

%changelog
* Fri Nov 01 2024 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.14-13
- Remove snakeyaml (test deps) since it's orphaned

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.7.14-12
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.7.14-10
- Rebuilt for java-21-openjdk as system jdk

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.7.14-4
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.7.14-3
- Rebuilt for java-17-openjdk as system jdk

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.14-1
- Update to 1.7.14 (#2024769)
- Change package url
- Add new test deps: mvn(jakarta.xml.soap:jakarta.xml.soap-api)
- Write new description and summary
- Remove POM properties (it's not used anymore)
- Add Automatic-Module-Name and Bundle-SymbolicName to manifest attributes
- Add different license for each subpackage

* Mon Jan 03 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-10
- Ignore tests for now due to unstable builds (VM crashes, tests took much time, etc.)

* Wed Dec 01 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-9
- Change BR: maven-local-openjdk11

* Sat Oct 16 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-8
- Don't build in ix86 cpu architecture
- Increase test's forkCount to 5x Cores

* Fri Oct 15 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-7
- Add compatibility: rhino:js, %%{_javadir}/rhino.jar

* Mon Oct 11 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-6
- Add requires: javapackages-tools
- Fix manifest attributes

* Fri Oct 08 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-5
- Fix surefire plugin
- Don't reuse processes to execute tests

* Thu Oct 07 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-4
- Fix some tests and include test262

* Wed Oct 06 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-3
- Disable failed tests

* Tue Oct 05 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-2
- Enable singleton packaging: rhino, rhino-engine, and rhino-runtime
- Fix %%files to be more specific

* Fri Sep 24 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.7.13-1
- Update to version 1.7.13

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Jerry James <loganjerry@gmail.com> - 1.7.7.1-13
- Change jline dep to jline2 and jansi dep to jansi1

* Sun Aug 30 2020 Fabio Valentini <decathorpe@gmail.com> - 1.7.7.1-12
- Remove unnecessary dependency on parent POM.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.7.7.1-10
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 01 2018 Severin Gehwolf <sgehwolf@redhat.com> 1.7.7.1-6
- Add requirement on javapackages-tools since rhino script uses
  java-functions.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 16 2016 Alexander Kurtakov <akurtako@redhat.com> 1.7.7.1-1
- Update to version 1.7.7.1.

* Thu Jun 16 2016 Alexander Kurtakov <akurtako@redhat.com> 1.7.7-5
- Add BR javapackages-local to unbreak build.

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.7-4
- Install JAR and POM with %%mvn_install
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Alexander Kurtakov <akurtako@redhat.com> 1.7.7-2
- Fix launch script.

* Fri Jun 26 2015 Alexander Kurtakov <akurtako@redhat.com> 1.7.7-1
- Update to upstream 1.7.7 release.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7R4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 10 2014 Alexander Kurtakov <akurtako@redhat.com> 1.7R4-10
- No longer ship javadoc subpackage and obsolete it.

* Tue Jun 10 2014 Alexander Kurtakov <akurtako@redhat.com> 1.7R4-9
- Use mfiles.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7R4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 14 2014 Matěj Cepl <mcepl@redhat.com> - 1.7R4-7
- Add overlow detection patch from the upstream (RHBZ# 1011947)
- Update all patches.

* Mon Sep 09 2013 Elliott Baron <ebaron@redhat.com> 1.7R4-6
- Update and add missing options for Rhino shell man page.

* Thu Aug 29 2013 Alexander Kurtakov <akurtako@redhat.com> 1.7R4-5
- Drop R on java-devel  - rhbz #991706.

* Thu Aug 1 2013 akurtakov <akurtakov@localhost.localdomain> 1.7R4-4
- Add R on java-devel as rhino requires tools.jar at runtime.

* Mon Jun 24 2013 Elliott Baron <ebaron@redhat.com> 1.7R4-3
- Add man page for Rhino shell.

* Thu Feb 28 2013 Krzysztof Daniel <kdaniel@redhat.com> 1.7R4-2
- Add a depmap to keep compatibility with previous versions.

* Tue Feb 26 2013 Alexander Kurtakov <akurtako@redhat.com> 1.7R4-1
- Update to 1.7R4.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7R3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7R3-7
- Add maven POM

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7R3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Bill Nottingham - 1.7R3-5
- build against OpenJDK 1.7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7R3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 16 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.7R3-3
- Crosslink javadocs with Java's.
- Drop versioned jars and javadoc dir.
- Exclude patch backup files from -examples.

* Wed Sep 21 2011 Matěj Cepl <mcepl@redhat.com> - 1.7R3-2
- Remove bea-stax-api dependency (and perl as well)

* Fri Sep 16 2011 Matěj Cepl <mcepl@redhat.com> - 1.7R3-1
- Fix numbering of the package (this is not a prerelease)
- Remove unnecessary macros
- Increase happines of rpmlint (better Group tags)

* Wed Sep 14 2011 Matěj Cepl <mcepl@redhat.com> - 1.7-0.10.r3
- New upstream pre-release.

* Wed Jul 6 2011 Andrew Overholt <overholt@redhat.com> 0:1.7-0.9.r2
- Inject OSGi metadata from Eclipse Orbit project.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-0.8.r2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-0.7.r2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0:1.7-0.6.r2
- Update to rhino1_7R2
- Add patch from Steven Elliott to fix exception in the interpreter shell.

* Mon Apr 20 2009 Lillian Angel <langel@redhat.com> - 0:1.7-0.4.r2pre.1.1
- Added jpackage-utils requirement.
- Resolves: rhbz#496435

* Thu Mar 26 2009 Lillian Angel <langel@redhat.com> - 0:1.7-0.3.r2pre.1.1
- Updated rhino-build.patch
- License for treetable has been fixed. Re-included this code, and removed patch.
- Resolves: rhbz#457336

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-0.2.r2pre.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Lillian Angel <langel@redhat.com> - 0:1.7-0.1.r2pre.1.1
- Upgraded to 1.7r2pre.
- Resolves: rhbz#485135

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.6-0.1.r5.1.3
- drop repotag
- fix license tag

* Thu Mar 15 2007 Matt Wringe <mwringe@redhat.com> 0:1.6-0.1.r5.1jpp.2
- Remove script from build as the debugging tool is disabled due to it
  containing proprietary code from Sun.

* Wed Mar 07 2007 Deepak Bhole <dbhole@redhat.com> 0:1.6-0.1.r5.1jpp.1
- Upgrade to 1.6r5
- Change release per Fedora guidelines
- Disable dependency on xmlbeans (optional component, not in Fedora yet)
- Disable building of debugger tool, as it needs confidential code from Sun
- Remove post/postuns for javadoc and add the two dirs as %%doc
* Wed Jun 14 2006 Ralph Apel <r.apel@r-apel.de> 0:1.6-0.r2.2jpp
- Add bea-stax-api in order to build xmlimpl classes

* Wed May 31 2006 Fernando Nasser <fnasser@redhat.com> 0:1.6-0.r2.1jpp
- Upgrade to RC2

* Mon Apr 24 2006 Fernando Nasser <fnasser@redhat.com> 0:1.6-0.r1.2jpp
- First JPP 1.7 build

* Thu Dec 02 2004 David Walluck <david@jpackage.org> 0:1.6-0.r1.1jpp
- 1_6R1
- add demo subpackage containing example code
- add jpp release info to implementation version
- add script to launch js shell
- build E4X implementation (Requires: xmlbeans)
- remove `Class-Path' from manifest

* Tue Aug 24 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.5-1.R5.1jpp
- Update to 1.5R5.
- Rebuild with Ant 1.6.2

* Sat Jul 19 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5-1.R4.1.1jpp
- Update to 1.5R4.1.
- Non-versioned javadoc dir symlink.

* Fri Apr 11 2003 David Walluck <davdi@anti-microsoft.org> 0:1.5-0.R4.2jpp
- remove build patches in favor of perl
- add epoch

* Sun Mar 30 2003 Ville Skyttä <ville.skytta@iki.fi> - 1.5-0.r4.1jpp
- Update to 1.5R4.
- Rebuild for JPackage 1.5.

* Wed May 08 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5-0.R3.1jpp
- 1.5R3
- versioned dir for javadoc

* Sun Mar 10 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5-0.R2.9jpp
- versioned compatibility symlink

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5-0.R2.8jpp
- section macro
- new release scheme

* Thu Jan 17 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5R2-7jpp
- spec cleanup
- changelog corrections

* Fri Jan 11 2002 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5R2-6jpp
- backward compatibility js.jar symlink
- used original swing exemples archive
- fixed javadoc empty package-list file
- no dependencies for manual and javadoc packages

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5R2-5jpp
- javadoc in javadoc package
- fixed offline build

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.5R2-4jpp
- changed extension --> jpp

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5R2-3jpp
- first unified release
- s/jPackage/JPackage
- corrected license to MPL

* Sat Sep 15 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5R2-2mdk
- spec cleanup
- standardized cvs references

* Fri Aug 31 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.5R2-1mdk
- first Mandrake release
