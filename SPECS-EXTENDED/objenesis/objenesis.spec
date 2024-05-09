Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package objenesis
#
# Copyright (c) 2019 SUSE LLC
# Copyright (c) 2000-2009, JPackage Project
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

Name:           objenesis
Version:        3.1
Release:        3%{?dist}
Summary:        A library for instantiating Java objects
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://objenesis.org/
Source0:        https://github.com/easymock/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
Objenesis is a small Java library that serves one purpose: to instantiate
a new object of a particular class.
Java supports dynamic instantiation of classes using Class.newInstance();
however, this only works if the class has an appropriate constructor. There
are many times when a class cannot be instantiated this way, such as when
the class contains constructors that require arguments, that have side effects,
and/or that throw exceptions. As a result, it is common to see restrictions
in libraries stating that classes must require a default constructor.
Objenesis aims to overcome these restrictions by bypassing the constructor
on object instantiation. Needing to instantiate an object without calling
the constructor is a fairly specialized task, however there are certain cases
when this is useful:
* Serialization, Remoting and Persistence - Objects need to be instantiated
  and restored to a specific state, without invoking code.
* Proxies, AOP Libraries and Mock Objects - Classes can be sub-classed without
  needing to worry about the super() constructor.
* Container Frameworks - Objects can be dynamically instantiated in
  non-standard ways.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML
BuildArch:      noarch

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

# Enable generation of pom.properties (rhbz#1017850)
%pom_xpath_remove pom:addMavenDescriptor

%pom_remove_plugin :maven-timestamp-plugin
%pom_xpath_remove "pom:dependency[pom:scope='test']" tck

%pom_xpath_remove pom:build/pom:extensions

for i in main tck; do
  %pom_remove_parent ${i}
  %pom_xpath_inject "pom:project" "<groupId>org.objenesis</groupId><version>%{version}</version>" ${i}
done

%build
mkdir -p main/build/classes
javac -d main/build/classes -source 8 -target 8 -encoding utf-8 \
  $(find main/src/main/java -name *.java | xargs)
jar cf %{name}-%{version}.jar -C main/build/classes .

touch manifest.txt
echo "Automatic-Module-Name: org.objenesis" >> manifest.txt  
echo "Bundle-Description: A library for instantiating Java objects" >> manifest.txt
echo "Bundle-License: https://www.apache.org/licenses/LICENSE-2.0.txt" >> manifest.txt
echo "Bundle-Name: Objenesis" >> manifest.txt
echo "Bundle-SymbolicName: org.objenesis" >> manifest.txt
echo "Bundle-Version: %{version}" >> manifest.txt
echo "Export-Package: org.objenesis;uses:=\"org.objenesis.instantiator,org.objenesis.strategy\";version=\"%{version}\",\
org.objenesis.instantiator.android;uses:=\"org.objenesis.instantiator,\
org.objenesis.instantiator.annotations\";version=\"%{version}\",\
org.objenesis.instantiator.basic;uses:=\"org.objenesis.instantiator,org.objenesis.instantiator.annotations\";version=\"%{version}\",\
org.objenesis.instantiator;version=\"%{version}\",\
org.objenesis.instantiator.gcj;uses:=\"org.objenesis.instantiator,org.objenesis.instantiator.annotations\";version=\"%{version}\",\
org.objenesis.instantiator.util;uses:=\"sun.misc\";version=\"%{version}\",org.objenesis.instantiator.annotations;version=\"%{version}\",org.objenesis.instantiator.perc;uses:=\"org.objenesis.instantiator,org.objenesis.instantiator.annotations\";version=\"%{version}\",\
org.objenesis.instantiator.sun;uses:=\"org.objenesis.instantiator,\
org.objenesis.instantiator.annotations\";version=\"%{version}\",\
org.objenesis.strategy;uses:=\"org.objenesis.instantiator\";version=\"%{version}\"" | sed 's/.\{71\}/&\n /g' >> manifest.txt
echo "Import-Package: sun.misc;resolution:=optional,\
COM.newmonics.PercClassloader;resolution:=optional,\
sun.reflect;resolution:=optional" | sed 's/.\{71\}/&\n /g' >> manifest.txt
echo "Require-Capability: osgi.ee;filter:=\"(&(osgi.ee=JavaSE)(version=1.6))\"" >> manifest.txt
jar ufm %{name}-%{version}.jar manifest.txt

mkdir -p tck/build/classes
javac -d tck/build/classes -source 8 -target 8 -encoding utf-8 \
  -cp %{name}-%{version}.jar \
  $(find tck/src/main/java -name *.java | xargs)
jar cf %{name}-tck-%{version}.jar -C tck/build/classes .
jar uf %{name}-tck-%{version}.jar -C tck/src/main/resources .
jar ufe %{name}-tck-%{version}.jar org.objenesis.tck.Main

mkdir -p build/apidoc
javadoc -d build/apidoc -source 8 -encoding utf-8 -notimestamp \
  $(find main/src/main/java -name *.java && \
    find tck/src/main/java -name *.java | xargs)

%install
# jars
install -dm 755 %{buildroot}%{_javadir}/%{name}
install -m 0644 %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
install -m 0644 %{name}-tck-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}-tck.jar

# poms
install -dm 755 %{buildroot}%{_mavenpomdir}/%{name}
install -m 0644 main/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
install -m 0644 tck/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-tck.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
%add_maven_depmap %{name}/%{name}-tck.pom %{name}/%{name}-tck.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -aL build/apidoc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE.txt

%files javadoc
%license LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1-3
- Reverting versioning change to match the upstream's schema.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.0-1.6
- Switching to always using full version.

* Fri Nov 20 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.1-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix line break in sed commands.

* Fri Nov 29 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 3.1
- Do not force building with java-devel < 9
- Build with source/target level 8, since it is the one that is
  the lowest supported combination by upstream for this release
* Sat Oct  5 2019 Fridrich Strba <fstrba@suse.com>
- Remove all reference to parent from pom files
* Sat Mar 16 2019 Jan Engelhardt <jengelh@inai.de>
- Add Group: tag for documentation.
* Thu Jan 24 2019 Fridrich Strba <fstrba@suse.com>
- Generate OSGi manifest so that the jar can be resolved by eclipse
* Fri Oct 26 2018 Fridrich Strba <fstrba@suse.com>
- Initial packaging of objenesis inspired from Fedora package
