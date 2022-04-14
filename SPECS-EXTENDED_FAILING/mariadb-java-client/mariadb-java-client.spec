Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		mariadb-java-client
Version:	2.7.0
Release:	2%{?dist}
Summary:	Connects applications developed in Java to MariaDB and MySQL databases
# added BSD license because of https://bugzilla.redhat.com/show_bug.cgi?id=1291558#c13
License:	BSD and LGPLv2+
URL:		https://mariadb.com/kb/en/mariadb/about-mariadb-connector-j/
Source0:	https://github.com/MariaDB/mariadb-connector-j/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# optional dependency not in Fedora
Patch0:		remove_waffle-jna.patch

BuildArch:	noarch
BuildRequires:	maven-local
BuildRequires:	mvn(net.java.dev.jna:jna)
BuildRequires:	mvn(net.java.dev.jna:jna-platform)
BuildRequires:	mvn(com.google.code.maven-replacer-plugin:replacer)
BuildRequires:	mvn(org.apache.maven.plugins:maven-javadoc-plugin)
# fedora 25
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.osgi:osgi.cmpn)
BuildRequires:  mvn(org.osgi:osgi.core)
# Since version 2.4.0
# removing coverage test because of dependencies
#BuildRequires:	mvn(org.jacoco:jacoco-maven-plugin)
# since version 1.5.2 missing optional dependency (windows)
#BuildRequires:	mvn(com.github.dblock.waffle:waffle-jna)

%description
MariaDB Connector/J is a Type 4 JDBC driver, also known as the Direct to
Database Pure Java Driver. It was developed specifically as a lightweight
JDBC connector for use with MySQL and MariaDB database servers.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -qn mariadb-connector-j-%{version}

# convert files from dos to unix line encoding
for file in README.md documentation/*.creole; do
 sed -i.orig 's|\r||g' $file
 touch -r $file.orig $file
 rm $file.orig
done

# remove missing optional dependency waffle-jna
%pom_remove_dep com.github.waffle:waffle-jna
%pom_remove_dep ch.qos.logback:logback-classic
%pom_remove_dep junit:junit
%pom_remove_dep com.amazonaws:aws-java-sdk-rds

# use latest OSGi implementation
%pom_change_dep -r :org.osgi.core org.osgi:osgi.core
%pom_change_dep -r :org.osgi.compendium org.osgi:osgi.cmpn 
 
rm -r src/main/java/org/mariadb/jdbc/credential/aws
 
sed -i 's|org.osgi.compendium|osgi.cmpn|' pom.xml

# also remove the file using the removed plugin
rm -f src/main/java/org/mariadb/jdbc/internal/com/send/authentication/gssapi/WindowsNativeSspiAuthentication.java
# patch the sources so that the missing file is not making trouble
%patch0 -p1

%mvn_file org.mariadb.jdbc:%{name} %{name}
%mvn_alias org.mariadb.jdbc:%{name} mariadb:mariadb-connector-java

%pom_remove_plugin org.jacoco:jacoco-maven-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-source-plugin
%pom_remove_plugin org.sonatype.plugins:nexus-staging-maven-plugin
%pom_remove_plugin com.coveo:fmt-maven-plugin
%pom_remove_plugin -r :maven-gpg-plugin

# remove preconfigured OSGi manifest file and generate OSGi manifest file
# with maven-bundle-plugin instead of using maven-jar-plugin
rm src/main/resources/META-INF/MANIFEST.MF
%pom_xpath_set "pom:packaging" bundle
%pom_xpath_set "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-jar-plugin']/pom:configuration/pom:archive/pom:manifestFile" '${project.build.outputDirectory}/META-INF/MANIFEST.MF'
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-jar-plugin']/pom:configuration/pom:archive/pom:manifestEntries"

%pom_add_plugin org.apache.felix:maven-bundle-plugin:2.5.4 . '
<extensions>true</extensions>
<configuration>
  <instructions>
    <Bundle-SymbolicName>${project.groupId}</Bundle-SymbolicName>
    <Bundle-Name>MariaDB JDBC Client</Bundle-Name>
    <Bundle-Version>${project.version}.0</Bundle-Version>
    <Export-Package>org.mariadb.jdbc.*</Export-Package>
    <Import-Package>
      !com.sun.jna.*,
      javax.net;resolution:=optional,
      javax.net.ssl;resolution:=optional,
      javax.sql;resolution:=optional,
      javax.transaction.xa;resolution:=optional
    </Import-Package>
  </instructions>
</configuration>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>'

%build
# tests are skipped, while they require running application server
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc documentation/* README.md
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Sep 25 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.7.0-1
- Rebase to version 2.7.0 (#1882558)

* Sun Aug 30 2020 Fabio Valentini <decathorpe@gmail.com> - 2.6.2-2
- Remove unnecessary dependency on sonatype-oss-parent.

* Wed Aug 19 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.6.2-1
- Rebase to version 2.6.2 (#1860212)

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
