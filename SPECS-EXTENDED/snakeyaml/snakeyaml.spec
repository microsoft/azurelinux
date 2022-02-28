Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package snakeyaml
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
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


%global vertag 8450addf3473
%bcond_with tests
Name:           snakeyaml
Version:        1.25
Release:        2%{?dist}
Summary:        YAML parser and emitter for the Java programming language
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://bitbucket.org/asomov/snakeyaml/
Source0:        https://bitbucket.org/asomov/snakeyaml/get/%{name}-%{version}.tar.bz2
Source1:        %{name}-build.xml
# Upstream has forked gdata-java and base64 and refuses [1] to
# consider replacing them by external dependencies.  Bundled libraries
# need to be removed and their use replaced by system libraries.
# See rhbz#875777 and http://code.google.com/p/snakeyaml/issues/detail?id=175
#
# Replace use of bundled Base64 implementation with java.util.Base64
Patch0:         0001-replace-bundled-base64coder-with-java.util.Base64.patch
# We don't have gdata-java, use commons-codec instead
Patch1:         0002-Replace-bundled-gdata-java-client-classes-with-commo.patch
# Fix a broken test, change backported from upstream:
# https://bitbucket.org/asomov/snakeyaml/commits/345408c
Patch2:         0003-fix-broken-test.patch
BuildRequires:  ant
BuildRequires:  apache-commons-codec
BuildRequires:  base64coder
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
Requires:       mvn(biz.source_code:base64coder)
Requires:       mvn(commons-codec:commons-codec)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  apache-commons-collections
BuildRequires:  apache-commons-lang
BuildRequires:  hamcrest-core
BuildRequires:  joda-time
BuildRequires:  junit
BuildRequires:  oro
BuildRequires:  velocity
# Differently sorted collections make fail some tests that rely on a particular order
BuildConflicts: java >= 9
BuildConflicts: java-devel >= 9
BuildConflicts: java-headless >= 9
%endif

%description
SnakeYAML features:
    * a complete YAML 1.1 parser. In particular,
      SnakeYAML can parse all examples from the specification.
    * Unicode support including UTF-8/UTF-16 input/output.
    * high-level API for serializing and deserializing
      native Java objects.
    * support for all types from the YAML types repository.
    * relatively sensible error messages.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains %{summary}.

%prep
%setup -q -n asomov-%{name}-%{vertag}
cp %{SOURCE1} build.xml
%patch0 -p1
%patch1 -p1
%patch2 -p1

%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :maven-changes-plugin
%pom_remove_plugin :maven-license-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-site-plugin

sed -i "/<artifactId>spring</s/spring/&-core/" pom.xml
rm -f src/test/java/examples/SpringTest.java

# Replacement for bundled gdata-java-client
%pom_add_dep commons-codec:commons-codec
# Re-add bundled base64coder
%pom_add_dep biz.source_code:base64coder

# fails in rpmbuild only due to different locale
rm src/test/java/org/yaml/snakeyaml/issues/issue67/NonAsciiCharsInClassNameTest.java
# fails after unbundling
rm src/test/java/org/yaml/snakeyaml/issues/issue318/ContextClassLoaderTest.java

# convert CR+LF to LF
sed -i 's/\r//g' LICENSE.txt

%pom_remove_dep org.springframework
rm -r src/test/java/org/yaml/snakeyaml/issues/issue9

%build
mkdir -p lib
build-jar-repository -s lib base64coder commons-codec
%if %{with tests}
build-jar-repository -s lib junit hamcrest/core velocity commons-collections commons-lang oro joda-time
%endif
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  clean package javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt

%files javadoc
%license LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.25-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.25-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Sun Nov 10 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream release 1.25
- Removed patch:
  * 0001-Replace-bundled-base64-implementation.patch
    + replaced by other implementation
- Modified patch:
  * 0002-Replace-bundled-gdata-java-client-classes-with-commo.patch
  + Rediff to changed context
- Added patches:
  * 0001-replace-bundled-base64coder-with-java.util.Base64.patch
    + Replace with internal jdk8+ implementation
  * 0003-fix-broken-test.patch
    + fix a broken test
* Fri Mar  1 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of snakeyaml 1.17 based on Fedora package
- Generated and customized ant build file
