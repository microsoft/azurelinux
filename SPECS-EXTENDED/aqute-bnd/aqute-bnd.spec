Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package aqute-bnd
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


Name:           aqute-bnd
Version:        3.5.0
Release:        6%{?dist}
Summary:        BND Tool
# Part of jpm is under BSD, but jpm is not included in binary RPM
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://bnd.bndtools.org/
Source0:        https://github.com/bndtools/bnd/archive/%{version}.REL.tar.gz#/%{name}-%{version}.REL.tar.gz
Source1:        bnd-%{version}.REL-build_xml.tar.xz
Source3:        https://repo1.maven.org/maven2/biz/aQute/bnd/aQute.libg/%{version}/aQute.libg-%{version}.pom
Source4:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bnd/%{version}/biz.aQute.bnd-%{version}.pom
Source5:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bndlib/%{version}/biz.aQute.bndlib-%{version}.pom
Source6:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bnd.annotation/%{version}/biz.aQute.bnd.annotation-%{version}.pom
Patch0:         0001-Disable-removed-commands.patch
Patch1:         0002-Fix-ant-compatibility.patch
Patch2:         0001-Port-to-OSGI-7.0.0.patch
Patch3:         aqute-bnd-3.5.0-java8compat.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  osgi-annotation
BuildRequires:  osgi-compendium
BuildRequires:  osgi-core
BuildRequires:  slf4j
# Explicit javapackages-tools requires since bnd script uses
# /usr/share/java-utils/java-functions
Requires:       %{name}lib = %{version}-%{release}
Requires:       javapackages-tools
BuildArch:      noarch

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
Group:          Development/Libraries/Java
Requires:       mvn(org.osgi:osgi.annotation)
Requires:       mvn(org.osgi:osgi.cmpn)
Requires:       mvn(org.osgi:osgi.core)
Requires:       mvn(org.slf4j:slf4j-api)
Requires:       mvn(org.slf4j:slf4j-simple)

%description -n aqute-bndlib
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n bnd-%{version}.REL -a 1

rm gradlew*
rm -f $(find | grep -E '\.(.ar|exe|tar\.(gz|bz2|xz)|zip)$' | xargs)

mkdir -p lib
build-jar-repository -s lib \
  slf4j/api slf4j/simple osgi-annotation osgi-core osgi-compendium ant

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# the commands pull in more dependencies than we want (felix-resolver, jetty)
rm biz.aQute.bnd/src/aQute/bnd/main/{RemoteCommand,ResolveCommand}.java

sed -i 's|${Bundle-Version}|%{version}|' biz.aQute.bndlib/src/aQute/bnd/osgi/bnd.info

# libg
pushd aQute.libg
cp -p %{SOURCE3} pom.xml
%pom_add_dep org.osgi:osgi.cmpn
%pom_add_dep org.slf4j:slf4j-api
popd

# bndlib.annotations
pushd biz.aQute.bnd.annotation
cp -p %{SOURCE6} pom.xml
popd

# bndlib
pushd biz.aQute.bndlib
cp -p %{SOURCE5} pom.xml
%pom_add_dep org.osgi:osgi.annotation
%pom_add_dep org.osgi:osgi.core
%pom_add_dep org.osgi:osgi.cmpn
%pom_add_dep org.slf4j:slf4j-api
%pom_add_dep biz.aQute.bnd:aQute.libg:%{version}
%pom_add_dep biz.aQute.bnd:biz.aQute.bnd.annotation:%{version}
popd

# bnd
pushd biz.aQute.bnd
cp -p %{SOURCE4} pom.xml
%pom_add_dep biz.aQute.bnd:biz.aQute.bndlib:%{version}
%pom_add_dep biz.aQute.bnd:aQute.libg:%{version}
%pom_add_dep biz.aQute.bnd:biz.aQute.bnd.annotation:%{version}
%pom_add_dep org.apache.ant:ant
%pom_add_dep org.osgi:osgi.annotation
%pom_add_dep org.osgi:osgi.core
%pom_add_dep org.osgi:osgi.cmpn
%pom_add_dep org.slf4j:slf4j-api

%pom_add_dep org.slf4j:slf4j-simple::runtime
popd

# maven-plugins
pushd maven
rm bnd-shared-maven-lib/src/main/java/aQute/bnd/maven/lib/resolve/DependencyResolver.java
%pom_remove_dep -r :biz.aQute.resolve
%pom_remove_dep -r :biz.aQute.repository
# Unavailable reactor dependency - org.osgi.impl.bundle.repoindex.cli
%pom_disable_module bnd-indexer-maven-plugin
# Requires unbuilt parts of bnd
%pom_disable_module bnd-export-maven-plugin
%pom_disable_module bnd-resolver-maven-plugin
%pom_disable_module bnd-testing-maven-plugin
# Integration tests require Internet access
%pom_remove_plugin -r :maven-invoker-plugin
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_remove_plugin -r :flatten-maven-plugin
popd

%build
%{ant}
%{ant} javadoc

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 biz.aQute.bnd.annotation/target/biz.aQute.bnd.annotation-%{version}.jar %{buildroot}%{_javadir}/%{name}/biz.aQute.bnd.annotation.jar
install -pm 0644 aQute.libg/target/aQute.libg-%{version}.jar %{buildroot}%{_javadir}/%{name}/aQute.libg.jar
install -pm 0644 biz.aQute.bndlib/target/biz.aQute.bndlib-%{version}.jar %{buildroot}%{_javadir}/%{name}/biz.aQute.bndlib.jar
install -pm 0644 biz.aQute.bnd/target/biz.aQute.bnd-%{version}.jar %{buildroot}%{_javadir}/%{name}/biz.aQute.bnd.jar
# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 biz.aQute.bnd.annotation/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/biz.aQute.bnd.annotation.pom
%add_maven_depmap %{name}/biz.aQute.bnd.annotation.pom %{name}/biz.aQute.bnd.annotation.jar -f bndlib
install -pm 0644 aQute.libg/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/aQute.libg.pom
%add_maven_depmap %{name}/aQute.libg.pom %{name}/aQute.libg.jar -f bndlib
install -pm 0644 biz.aQute.bndlib/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/biz.aQute.bndlib.pom
%add_maven_depmap %{name}/biz.aQute.bndlib.pom %{name}/biz.aQute.bndlib.jar -f bndlib -a biz.aQute.bnd:bndlib,biz.aQute:bndlib
install -pm 0644 biz.aQute.bnd/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/biz.aQute.bnd.pom
%add_maven_depmap %{name}/biz.aQute.bnd.pom %{name}/biz.aQute.bnd.jar -a biz.aQute.bnd:bnd,biz.aQute:bnd
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
mv biz.aQute.bnd.annotation/target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/biz.aQute.bnd.annotation
mv aQute.libg/target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/aQute.libg
mv biz.aQute.bndlib/target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/biz.aQute.bndlib
mv biz.aQute.bnd/target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/biz.aQute.bnd
%fdupes -s %{buildroot}%{_javadocdir}

install -d -m 755 %{buildroot}%{_sysconfdir}/ant.d
echo "aqute-bnd slf4j/api slf4j/simple osgi-annotation osgi-core osgi-compendium" >%{buildroot}%{_sysconfdir}/ant.d/%{name}

%jpackage_script aQute.bnd.main.bnd "" "" aqute-bnd:slf4j/api:slf4j/simple:osgi-annotation:osgi-core:osgi-compendium bnd 1

%files -f .mfiles
%license LICENSE
%{_bindir}/bnd
%config(noreplace) %{_sysconfdir}/ant.d/*
%dir %{_sysconfdir}/ant.d

%files -n aqute-bndlib -f .mfiles-bndlib
%license LICENSE

%files javadoc
%license LICENSE
%{_javadocdir}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.5.0-6
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.5.0-5.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Apr  1 2020 Fridrich Strba <fstrba@suse.com>
- Addes patch:
  * 0001-Port-to-OSGI-7.0.0.patch
    + Port to OSGI 7.0.0
* Wed Jun 26 2019 Fridrich Strba <fstrba@suse.com>
- Add aliases for the aqute-bnd artifact
* Thu Mar 14 2019 Fridrich Strba <fstrba@suse.com>
- Correct error with duplicate identical aliases for two different
  artifacts
* Tue Feb 12 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of aqute-bnd 3.5.0
- Add ant build.xml files in order to build without having to use
  gradle
