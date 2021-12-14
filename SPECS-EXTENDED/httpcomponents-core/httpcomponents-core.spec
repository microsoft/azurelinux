Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package httpcomponents-core
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


%bcond_with tests
Name:           httpcomponents-core
Version:        4.4.13
Release:        2%{?dist}
Summary:        Set of low level Java HTTP transport components for HTTP services
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://hc.apache.org/
Source0:        https://archive.apache.org/dist/httpcomponents/httpcore/source/httpcomponents-core-%{version}-src.tar.gz
Source1:        %{name}-build.tar.xz
Patch0:         %{name}-java8compat.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  apache-commons-lang3
BuildRequires:  apache-commons-logging
BuildRequires:  cglib
BuildRequires:  mockito
BuildRequires:  objectweb-asm
BuildRequires:  objenesis
BuildConflicts: java-devel >= 9
%endif

%description
HttpCore is a set of low level HTTP transport components that can be
used to build custom client and server side HTTP services with a
minimal footprint. HttpCore supports two I/O models: blocking I/O
model based on the classic Java I/O and non-blocking, event driven I/O
model based on Java NIO.

The blocking I/O model may be more appropriate for data intensive, low
latency scenarios, whereas the non-blocking model may be more
appropriate for high latency scenarios where raw data throughput is
less important than the ability to handle thousands of simultaneous
HTTP connections in a resource efficient manner.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Development/Libraries/Java

%description    javadoc
%{summary}.

%prep
%setup -q -a1

%patch0 -p1

# Random test failures on ARM -- 100 ms sleep is not eneough on this
# very performant arch, lets make it 2 s
sed -i '/Thread.sleep/s/100/2000/' httpcore-nio/src/test/java/org/apache/http/nio/integration/TestHttpAsyncHandlers.java

%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin

# we don't need these artifacts right now
%pom_disable_module httpcore-osgi
%pom_disable_module httpcore-ab

# OSGify modules
for module in httpcore httpcore-nio; do
    %pom_xpath_remove "pom:project/pom:packaging" $module
    %pom_xpath_inject "pom:project" "<packaging>bundle</packaging>" $module
    %pom_remove_plugin :maven-jar-plugin $module
    %pom_xpath_inject "pom:build/pom:plugins" "
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <configuration>
            <instructions>
              <Export-Package>*</Export-Package>
              <Private-Package></Private-Package>
              <Automatic-Module-Name>org.apache.httpcomponents.$module</Automatic-Module-Name>
              <_nouses>true</_nouses>
            </instructions>
          </configuration>
        </plugin>" $module
done

for module in httpcore httpcore-nio; do
    %pom_xpath_inject "pom:project" "
	  <groupId>org.apache.httpcomponents</groupId>
	  <version>%{version}</version>" $module
	%pom_remove_parent $module
	# adds version "any" if none is specified
	%pom_change_dep ::::: ::::: $module
done

# install JARs to httpcomponents/ for compatibility reasons
# several other packages expect to find the JARs there
%{mvn_file} ":{*}" httpcomponents/@1

%build
mkdir -p lib
%if %{with tests}
build-jar-repository -s lib cglib/cglib commons-lang3 commons-logging mockito/mockito-core objectweb-asm/asm objenesis/objenesis
%endif
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  package javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/httpcomponents
for module in httpcore httpcore-nio; do
  install -pm 0644 ${module}/target/${module}-%{version}.jar %{buildroot}%{_javadir}/httpcomponents/${module}.jar
done
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/httpcomponents
for module in httpcore httpcore-nio; do
  install -pm 0644 ${module}/pom.xml %{buildroot}%{_mavenpomdir}/httpcomponents/${module}.pom
  %add_maven_depmap httpcomponents/${module}.pom httpcomponents/${module}.jar
done
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
for module in httpcore httpcore-nio; do
  install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/${module}
  cp -pr ${module}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/${module}/
done
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt
%doc NOTICE.txt README.txt RELEASE_NOTES.txt

%files javadoc
%license LICENSE.txt
%doc NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.4.13-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.4.13-1.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr 27 2020 Fridrich Strba <fstrba@suse.com>
- Upgraded to version 4.4.13
- Removed patch:
  * 0001-Re-generated-expired-test-certificates.patch
    + included in this version
- Modified patch:
  * httpcomponents-core-java8compat.patch
    + rediffed to changed context
* Sat Oct  5 2019 Fridrich Strba <fstrba@suse.com>
- Avoid version-less dependencies in pom files, since
  xmvn-connector-gradle does not handle them well
* Wed Mar 13 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of httpcomponent-core 4.4.10
- Generate and customize the ant build files
- Added patches:
  * 0001-Re-generated-expired-test-certificates.patch
    + upstream fix to update expired certificates in tests
  * httpcomponents-core-java8compat.patch
    + fix code so that it produces binaries compatible with
    Java 8
