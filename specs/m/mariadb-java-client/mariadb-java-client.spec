## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           mariadb-java-client
Version:        3.5.5
Release:        %autorelease
Summary:        Connects applications developed in Java to MariaDB and MySQL databases
License:        LGPL-2.1-only
URL:            https://mariadb.com/kb/en/mariadb/about-mariadb-connector-j/
Source0:        https://github.com/mariadb-corporation/mariadb-connector-j/archive/refs/tags/%{version}.tar.gz#/mariadb-connector-j-%{version}.tar.gz
# optional dependency not in Fedora
Patch:          0001-Remove_waffle-jna.patch
Patch:          0002-Remove-usage-of-junit-pioneer.patch
Patch:          0003-Fix-Java-version-parsing-for-non-standard-versions.patch

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(net.java.dev.jna:jna)
BuildRequires:  mvn(net.java.dev.jna:jna-platform)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.osgi:osgi.cmpn)
BuildRequires:  mvn(org.osgi:osgi.core)
BuildRequires:  mvn(org.slf4j:slf4j-api)

# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.5.0-7

%description
MariaDB Connector/J is a Type 4 JDBC driver, also known as the Direct to
Database Pure Java Driver. It was developed specifically as a lightweight
JDBC connector for use with MySQL and MariaDB database servers.

%package        tests
Summary:        Tests for %{name}

%description    tests
This package contains tests for %{name}.

%prep
%autosetup -p1 -n mariadb-connector-j-%{version}

%pom_remove_dep ch.qos.logback:logback-classic
grep -l -r '^import ch\.qos\.logback\.classic' src/test | xargs rm -v

%pom_remove_dep com.github.waffle:waffle-jna
%pom_remove_dep software.amazon.awssdk:bom
%pom_remove_dep software.amazon.awssdk:rds

# upstream uses two crypto implementations: bouncycastle and one from JDK15+
%pom_remove_dep org.bouncycastle:bcpkix-jdk18on
mv src/main/java15/org/mariadb/jdbc/plugin/authentication/standard/ParsecPasswordPluginTool.java src/main/java/org/mariadb/jdbc/plugin/authentication/standard/ParsecPasswordPluginTool.java
sed -i '/requires.*org\.bouncycastle.*;/d' src/main/java9/module-info.java

# used in buildtime for generating OSGI metadata
%pom_remove_plugin biz.aQute.bnd:bnd-maven-plugin

%pom_add_dep net.java.dev.jna:jna
%pom_add_dep net.java.dev.jna:jna-platform

# make the slf4j dependency version-independent
%pom_remove_dep org.slf4j:slf4j-api
%pom_add_dep org.slf4j:slf4j-api
%pom_add_dep org.junit.jupiter:junit-jupiter-params

# use the latest OSGi implementation
%pom_change_dep -r :org.osgi.core org.osgi:osgi.core
%pom_change_dep -r :org.osgi.compendium org.osgi:osgi.cmpn

rm -r src/main/java/org/mariadb/jdbc/plugin/credential/aws

# removing dependencies and 'provides', which mariadb-java-client cannot process from module-info.java
sed -i -e '/aws/d' -e '/waffle/d' src/main/java9/module-info.java

# removing missing dependencies form META-INF, so that the mariadb-java-client module would be valid
sed -i '/aws/d' src/{main,test}/resources/META-INF/services/org.mariadb.jdbc.plugin.CredentialPlugin
rm -f src/main/java/org/mariadb/jdbc/plugin/authentication/addon/gssapi/WindowsNativeSspiAuthentication.java

# disable tests using junit.pioneer annotations
%pom_remove_dep org.junit-pioneer:junit-pioneer

%mvn_file org.mariadb.jdbc:%{name} %{name}
%mvn_alias org.mariadb.jdbc:%{name} mariadb:mariadb-connector-java

%pom_remove_plugin org.jacoco:jacoco-maven-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-source-plugin
%pom_remove_plugin org.sonatype.central:central-publishing-maven-plugin
%pom_remove_plugin -r :maven-gpg-plugin
%pom_remove_plugin -r :maven-javadoc-plugin

# Install -tests Jar as well
%pom_xpath_inject 'pom:build/pom:plugins/pom:plugin[pom:artifactId="maven-jar-plugin"]' '
<executions>
  <execution>
    <goals>
      <goal>test-jar</goal>
    </goals>
  </execution>
</executions>'
%mvn_package org.mariadb.jdbc:mariadb-java-client::tests: tests

%build
# tests are skipped, while they require running application server
# NOTE this parameter skips running tests but still compiles them (instead of -f)
%mvn_build -j -- -DskipTests=true

xmvn -Dmdep.outputFile=tests-classpath dependency:build-classpath --offline

%install
%mvn_install
install -m 644 -D tests-classpath %{buildroot}/%{_datadir}/%{name}-tests/classpath

%files -f .mfiles
%doc README.md
%license LICENSE

%files tests -f .mfiles-tests
%{_datadir}/%{name}-tests
%license LICENSE

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 3.5.5-3
- Latest state for mariadb-java-client

* Mon Aug 11 2025 Marian Koncek <mkoncek@redhat.com> - 3.5.5-2
- Make tests work with latest Java

* Mon Aug 11 2025 Marian Koncek <mkoncek@redhat.com> - 3.5.5-1
- Update to upstream version 3.5.5

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 3.5.3-4
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 12 2025 Marian Koncek <mkoncek@redhat.com> - 3.5.3-2
- Drop -javadoc subpackage

* Thu Apr 24 2025 Marian Koncek <mkoncek@redhat.com> - 3.5.3-1
- Update to upstream version 3.5.3

* Fri Apr 04 2025 Marian Koncek <mkoncek@redhat.com> - 3.5.0-6
- Switch tests repo to Gitlab

* Mon Mar 10 2025 Marian Koncek <mkoncek@redhat.com> - 3.5.0-5
- Add smoke test plan

* Thu Mar 06 2025 Marian Koncek <mkoncek@redhat.com> - 3.5.0-4
- Add test subpackage

* Thu Mar 06 2025 Marian Koncek <mkoncek@redhat.com> - 3.5.0-3
- Reformat spec

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Nov 16 2024 Michal Schorm <mschorm@redhat.com> - 3.5.0-1
- Rebase to upstream version 3.5.0

* Fri Sep 13 2024 Marian Koncek <mkoncek@redhat.com> - 3.4.1-1
- Update to upstream version 3.4.1

* Thu Sep 12 2024 Marian Koncek <mkoncek@redhat.com> - 3.4.0-5
- Fix BuildRequires

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Marian Koncek <mkoncek@redhat.com> - 3.4.0-1
- Update to upstream version 3.4.0

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 3.3.3-2
- Rebuilt for java-21-openjdk as system jdk

* Wed Feb 21 2024 Zuzana Miklankova <zmiklank@redhat.com> - 3.3.3-1
- Rebase to version 3.3.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 22 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.3.2-1
- Rebase to version 3.3.2

* Thu Aug 31 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.2.0-1
- Rebase to version 3.2.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 02 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.1.4-1
- Rebase to version 3.1.4

* Thu Apr 06 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.1.3-1
- Rebase to version 3.1.3

* Thu Jan 26 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.1.2-1
- Rebase to version 3.1.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.1.1-1
- Rebase to version 3.1.1

* Wed Nov 09 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.0.9-1
- Rebase to version 3.0.9

* Fri Sep 23 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.0.8-1
- Rebase to version 3.0.8

* Fri Aug 05 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.0.7-1
- Rebase to version 3.0.7

* Thu Jul 21 2022 Ondrej Sloup <osloup@redhat.com> - 3.0.6-1
- Fix mixed spaces and tabs
- Rebase to version 3.0.6 (rhbz#2102401)

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 3.0.5-2
- Rebuilt for Drop i686 JDKs

* Thu May 26 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.0.5-1
- Rebase to version 3.0.5

* Mon Mar 28 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.0.4-1
- Rebase to version 3.0.4

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 3.0.3-3
- Rebuilt for java-17-openjdk as system jdk

* Mon Jan 31 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.0.3-2
- Disable javadoc build, because xmvn is not able to build it

* Thu Jan 27 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.0.3-1
- Rebase to version 3.0.3

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 18 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.0.1-1
- Rebase to version 3.0.1

* Fri Jul 23 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.0.0-1
- Rebase to version 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Ondrej Dubaj <odubaj@redhat.com> - 2.7.3-1
- Rebase to version 2.7.3

* Wed May 12 2021 Ondrej Dubaj <odubaj@redhat.com> - 2.7.2-2
- Remove maven-javadoc-plugin dependency

* Wed May 05 2021 Ondrej Dubaj <odubaj@redhat.com> - 2.7.2-1
- Rebase to version 2.7.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.7.1-1
- Rebase to version 2.7.1 (#1906291)

* Fri Sep 25 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.7.0-1
- Rebase to version 2.7.0 (#1882558)

* Sun Aug 30 2020 Fabio Valentini <decathorpe@gmail.com> - 2.6.2-2
- Remove unnecessary dependency on sonatype-oss-parent.

* Wed Aug 19 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.6.2-1
- Rebase to version 2.6.2 (#1860212)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 2.6.1-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jun 24 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.6.1-1
- Rebase to version 2.6.1 (#1850111)

* Mon Mar 30 2020 Michal Schorm <mschorm@redhat.com> - 2.6.0-2
- Remove the dependency on mariadb (#1818814)

* Mon Mar 23 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.6.0-1
- Rebase to version 2.6.0 (#1815696)

* Thu Feb 20 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.5.4-1
- Rebase to version 2.5.4 (#1752069)

* Wed Feb 19 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.4.3-3
- Resolved FTBFS (#1799633)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 10 2019 Michal Schorm <mschorm@redhat.com> - 2.4.3-1
- Rebase to version 2.4.3

* Tue Sep 10 2019 Michal Schorm <mschorm@redhat.com> - 2.4.1-3
- Remove dependency to orphaned HikariCP

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Jakub Janco <jjanco@redhat.com> - 2.4.1-1
- new version

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Jakub Janco <jjanco@redhat.com> - 2.4.0-1
- new version

* Mon Nov 26 2018 Jakub Janco <jjanco@redhat.com> - 2.3.0-1
- new version

* Tue Aug 07 2018 Jakub Janco <jjanco@redhat.com> - 2.2.6-1
- new version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 04 2018 Jakub Janco <jjanco@redhat.com> - 2.2.5-1
- new version

* Tue May 15 2018 Jakub Janco <jjanco@redhat.com> - 2.2.4-3
- remove unused aws-java-sdk dependency

* Sat May 05 2018 Jakub Janco <jjanco@redhat.com> - 2.2.4-2
- Refactor pom, add tests package

* Sat May 05 2018 Jakub Janco <jjanco@redhat.com> - 2.2.4-1
- new version

* Tue Mar 13 2018 Jakub Janco <jjanco@redhat.com> - 2.2.3-1
- update version

* Mon Feb 26 2018 Jakub Janco <jjanco@redhat.com> - 2.2.2-1
- update version

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Jakub Janco <jjanco@redhat.com> - 2.2.1-1
- Update to 2.2.1

* Tue Nov 21 2017 Jakub Janco <jjanco@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Tue Aug 29 2017 Tomas Repik <trepik@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Tomas Repik <trepik@redhat.com> - 2.0.2-1
- version update

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Tomas Repik <trepik@redhat.com> - 1.5.5-1
- version update

* Mon Oct 03 2016 Tomas Repik <trepik@redhat.com> - 1.5.3-1
- version update

* Wed Sep 14 2016 Tomas Repik <trepik@redhat.com> - 1.5.2-1
- version update

* Tue Jun 21 2016 Tomas Repik <trepik@redhat.com> - 1.4.6-1
- version update

* Mon Apr 18 2016 Tomas Repik <trepik@redhat.com> - 1.4.2-1
- version update

* Wed Mar 23 2016 Tomas Repik <trepik@redhat.com> - 1.3.7-1
- version update
- BSD license added
- cosmetic updates in prep phase

* Thu Mar 10 2016 Tomas Repik <trepik@redhat.com> - 1.3.6-1
- version update

* Mon Feb 15 2016 Tomas Repik <trepik@redhat.com> - 1.3.5-1
- version update

* Wed Jan 20 2016 Tomáš Repík <trepik@redhat.com> - 1.3.3-3
- generating OSGi manifest file with maven-bundle-plugin

* Wed Dec 16 2015 Tomáš Repík <trepik@redhat.com> - 1.3.3-2
- installing LICENSE added
- conversion from dos to unix line encoding revised
- unnecessary tasks removed

* Wed Dec  9 2015 Tomáš Repík <trepik@redhat.com> - 1.3.3-1
- Initial package

## END: Generated by rpmautospec
