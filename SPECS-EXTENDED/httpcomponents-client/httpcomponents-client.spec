Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package httpcomponents-client
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%bcond_with     tests
Name:           httpcomponents-client
Version:        4.5.12
Release:        2%{?dist}
Summary:        HTTP agent implementation based on httpcomponents HttpCore
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://hc.apache.org/
Source0:        https://archive.apache.org/dist/httpcomponents/httpclient/source/%{name}-%{version}-src.tar.gz
Source1:        %{name}-build.tar.xz
Patch0:         0001-Use-system-copy-of-effective_tld_names.dat.patch
Patch1:         %{name}-java8compat.patch
BuildRequires:  ant
BuildRequires:  apache-commons-codec
BuildRequires:  apache-commons-logging
BuildRequires:  fdupes
BuildRequires:  httpcomponents-core
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  publicsuffix
Requires:       publicsuffix
Requires:       mvn(commons-codec:commons-codec)
Requires:       mvn(commons-logging:commons-logging)
Requires:       mvn(org.apache.httpcomponents:httpcore)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  cglib
BuildRequires:  mockito
BuildRequires:  objectweb-asm
BuildRequires:  objenesis
%endif

%description
HttpClient is a HTTP/1.1 compliant HTTP agent implementation based on
httpcomponents HttpCore. It also provides reusable components for
client-side authentication, HTTP state management, and HTTP connection
management. HttpComponents Client is a successor of and replacement
for Commons HttpClient 3.x. Users of Commons HttpClient are strongly
encouraged to upgrade.

%package        cache
Summary:        Cache module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(commons-logging:commons-logging)
Requires:       mvn(org.apache.httpcomponents:httpclient) = %{version}

%description    cache
This package provides client side caching for %{name}.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description    javadoc
%{summary}.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

# Remove optional build deps not available in openSUSE
%pom_disable_module httpclient-osgi
%pom_disable_module httpclient-win
%pom_remove_plugin :docbkx-maven-plugin
%pom_remove_plugin :clirr-maven-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin

# Fails due to strict crypto policy - uses DSA in test data
rm httpclient/src/test/java/org/apache/http/conn/ssl/TestSSLSocketFactory.java

# Don't compile/run httpclient-cache tests - they are incompatible with EasyMock 3.3
%pom_remove_dep org.easymock:easymockclassextension
for dep in org.easymock:easymockclassextension org.slf4j:slf4j-jcl; do
    %pom_remove_dep $dep httpclient-cache
done
rm -rf httpclient-cache/src/test

%pom_remove_plugin :download-maven-plugin httpclient

%pom_xpath_inject "pom:archive" "
    <manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>"

%pom_xpath_inject pom:build/pom:plugins "
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <executions>
        <execution>
          <id>bundle-manifest</id>
          <phase>process-classes</phase>
          <goals>
            <goal>manifest</goal>
          </goals>
        </execution>
      </executions>
    </plugin>"

%pom_xpath_inject pom:build "
<pluginManagement>
  <plugins>
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <configuration>
        <instructions>
          <Export-Package>org.apache.http.*,!org.apache.http.param</Export-Package>
          <Private-Package></Private-Package>
          <_nouses>true</_nouses>
          <Import-Package>!org.apache.avalon.framework.logger,!org.apache.log,!org.apache.log4j,*</Import-Package>
        </instructions>
        <excludeDependencies>true</excludeDependencies>
      </configuration>
    </plugin>
  </plugins>
</pluginManagement>
" httpclient

%pom_xpath_inject pom:build "
<pluginManagement>
  <plugins>
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <extensions>true</extensions>
      <configuration>
        <instructions>
          <Export-Package>*</Export-Package>
          <Import-Package>net.sf.ehcache;resolution:=optional,net.spy.memcached;resolution:=optional,*</Import-Package>
          <Private-Package></Private-Package>
          <_nouses>true</_nouses>
        </instructions>
        <excludeDependencies>true</excludeDependencies>
      </configuration>
    </plugin>
  </plugins>
</pluginManagement>" httpclient-cache

# requires network
rm httpclient/src/test/java/org/apache/http/client/config/TestRequestConfig.java

rm -r httpclient-cache/src/*/java/org/apache/http/impl/client/cache/memcached
%pom_remove_dep :spymemcached httpclient-cache

rm -r httpclient-cache/src/*/java/org/apache/http/impl/client/cache/ehcache
%pom_remove_dep :ehcache-core httpclient-cache

for module in fluent-hc httpclient httpclient-cache httpmime; do
    %pom_xpath_inject "pom:project" "
	  <groupId>org.apache.httpcomponents</groupId>
	  <version>%{version}</version>" $module
	%pom_remove_parent $module
	# adds version "any" if none is specified
	%pom_change_dep ::::: ::::: $module
done

%build
mkdir -p lib
build-jar-repository -s lib httpcomponents/httpcore commons-logging commons-codec
%if %{with tests}
build-jar-repository -s lib cglib/cglib mockito/mockito-core objectweb-asm/asm objenesis/objenesis
%endif
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  package javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/httpcomponents
for module in fluent-hc httpclient httpclient-cache httpmime; do
  install -pm 0644 ${module}/target/${module}-%{version}.jar %{buildroot}%{_javadir}/httpcomponents/${module}.jar
done
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/httpcomponents
for module in fluent-hc httpclient httpmime; do
  install -pm 0644 ${module}/pom.xml %{buildroot}%{_mavenpomdir}/httpcomponents/${module}.pom
  %add_maven_depmap httpcomponents/${module}.pom httpcomponents/${module}.jar
done
install -pm 0644 httpclient-cache/pom.xml %{buildroot}%{_mavenpomdir}/httpcomponents/httpclient-cache.pom
%add_maven_depmap httpcomponents/httpclient-cache.pom httpcomponents/httpclient-cache.jar -f cache
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
for module in fluent-hc httpclient httpclient-cache httpmime; do
  install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/${module}
  cp -pr ${module}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/${module}/
done
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt
%doc NOTICE.txt README.txt RELEASE_NOTES.txt

%files cache -f .mfiles-cache

%files javadoc
%license LICENSE.txt
%doc NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.5.12-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.5.12-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr 27 2020 Fridrich Strba <fstrba@suse.com>
- Update to version 4.5.12
* Sat Oct  5 2019 Fridrich Strba <fstrba@suse.com>
- Avoid version-less dependencies in pom files, since
  xmvn-connector-gradle does not handle them well
* Wed Mar 13 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of httpcomponents-client 4.5.6
- Generate and customize ant build files
