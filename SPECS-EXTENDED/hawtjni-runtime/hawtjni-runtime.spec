Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package hawtjni-runtime
#
# Copyright (c) 2019 SUSE LLC
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

%global debug_package %{nil}
Name:           hawtjni-runtime
Version:        1.17
Release:        3%{?dist}
Summary:        HawtJNI Runtime
License:        Apache-2.0 AND EPL-1.0 AND BSD-3-Clause
URL:            https://github.com/fusesource/hawtjni
Source0:        https://github.com/fusesource/hawtjni/archive/hawtjni-project-%{version}.tar.gz
Patch0:         use-commons-lang3.patch
BuildRequires:  apache-commons-cli
BuildRequires:  apache-commons-lang3
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  objectweb-asm >= 5
BuildRequires:  xbean

%description
This package provides API that projects using HawtJNI should build
against.

%package -n hawtjni-javadoc
Summary:        Javadocs for hawtjni
BuildArch:      noarch

%description -n hawtjni-javadoc
This package contains the API documentation for hawtjni.

%package -n hawtjni
Summary:        Code generator that produces the JNI code
Requires:       %{name} = %{version}
Requires:       apache-commons-cli
Requires:       apache-commons-lang3
Requires:       javapackages-tools
Requires:       objectweb-asm >= 5
Requires:       xbean
BuildArch:      noarch

%description -n hawtjni
HawtJNI is a code generator that produces the JNI code needed to
implement java native methods. It is based on the jnigen code generator
that is part of the SWT Tools project which is used to generate all the
JNI code which powers the eclipse platform.

%prep
%setup -q -n hawtjni-hawtjni-project-%{version}
%patch -P 0 -p1

%pom_disable_module hawtjni-example
%pom_disable_module hawtjni-maven-plugin
%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r :maven-eclipse-plugin

# this dependency seems to be missing
%pom_add_dep commons-lang:commons-lang3 hawtjni-generator

for mod in runtime generator; do
  %pom_remove_parent hawtjni-${mod}
  %pom_xpath_inject pom:project "
    <groupId>org.fusesource.hawtjni</groupId>
    <version>%{version}</version>" hawtjni-${mod}
done

%build
mkdir -p hawtjni-runtime/build/classes
javac -d hawtjni-runtime/build/classes -source 8 -target 8 \
  $(find hawtjni-runtime/src/main/java/ -name *.java | xargs)
jar cf hawtjni-runtime.jar -C hawtjni-runtime/build/classes .
mkdir -p  hawtjni-generator/build/classes
javac -d hawtjni-generator/build/classes \
  -source 8 -target 8 \
  -cp $(build-classpath commons-cli commons-lang3 objectweb-asm/asm objectweb-asm/asm-commons xbean/xbean-finder xbean/xbean-asm-util):hawtjni-runtime.jar \
  $(find hawtjni-generator/src/main/java/ -name *.java | xargs)
jar cf hawtjni-generator.jar -C hawtjni-generator/build/classes .
jar uf hawtjni-generator.jar -C hawtjni-generator/src/main/resources .
mkdir -p hawtjni-runtime/build/apidoc
javadoc -d hawtjni-runtime/build/apidoc -source 8 \
  -classpath $(build-classpath commons-cli commons-lang3 objectweb-asm/asm objectweb-asm/asm-commons xbean/xbean-finder xbean/xbean-asm-util) \
  $(find hawtjni-runtime/src/main/java/ -name *.java && \
    find hawtjni-generator/src/main/java/ -name *.java| xargs)

%install
# jars
install -dm 755 %{buildroot}%{_javadir}/hawtjni
install -dm 755 %{buildroot}%{_jnidir}/hawtjni
install -m 0644 hawtjni-runtime.jar %{buildroot}%{_jnidir}/hawtjni/
install -m 0644 hawtjni-generator.jar %{buildroot}%{_javadir}/hawtjni/

# poms
install -dm 755 %{buildroot}%{_mavenpomdir}/hawtjni
install -m 0644 hawtjni-runtime/pom.xml %{buildroot}%{_mavenpomdir}/hawtjni/hawtjni-runtime.pom
install -m 0644 hawtjni-generator/pom.xml %{buildroot}%{_mavenpomdir}/hawtjni/hawtjni-generator.pom
%add_maven_depmap hawtjni/hawtjni-generator.pom hawtjni/hawtjni-generator.jar -f generator
%add_maven_depmap hawtjni/hawtjni-runtime.pom hawtjni/hawtjni-runtime.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/hawtjni
cp -pr  hawtjni-runtime/build/apidoc/* %{buildroot}%{_javadocdir}/hawtjni/
# to remove license warnings
install -Dm 0644 hawtjni-runtime/build/apidoc/legal/LICENSE \
    %{buildroot}%{_licensedir}/hawtjni/LICENSE.javadoc

install -Dm 0644 hawtjni-runtime/build/apidoc/legal/ADDITIONAL_LICENSE_INFO \
    %{buildroot}%{_licensedir}/hawtjni/ADDITIONAL_LICENSE_INFO.javadoc

rm -rf %{buildroot}%{_javadocdir}/hawtjni/legal

%fdupes -s %{buildroot}%{_javadocdir}/hawtjni/

%{jpackage_script org.fusesource.hawtjni.generator.HawtJNI "" "" commons-cli:commons-lang3:objectweb-asm/asm:objectweb-asm/asm-commons:xbean/xbean-finder:xbean/xbean-asm-util:hawtjni/hawtjni-runtime:hawtjni/hawtjni-generator hawtjni-generator true}

%files -f .mfiles
%license license.txt
%doc readme.md changelog.md

%files -n hawtjni -f .mfiles-generator
%{_bindir}/hawtjni-generator

%files -n hawtjni-javadoc
%{_javadocdir}/hawtjni
%license license.txt
%license %{_licensedir}/hawtjni/*

%changelog
* Wed Dec 24 2025 Aninda Pradhan <v-anindap@microsoft.com> - 1.17-3
- Updated dependencies to use commons-lang3
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.17-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.17-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Define empty debug_package.

* Mon Nov 25 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upsteam version 1.17
- Add dependency on mvn(commons-lang:commons-lang) that is missing
* Wed Oct  2 2019 Fridrich Strba <fstrba@suse.com>
- Correct the URL that does not exist anymore
- Clean the spec file with spec-cleaner
* Mon Sep 30 2019 Fridrich Strba <fstrba@suse.com>
- Remove references to the parent pom from all artifacts and
  don't distribute any parent artifact, since we don't build
  this with maven, so the parent artifacts are pointless
* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent pom since we are not building
  using Maven.
* Wed Jan 23 2019 Fridrich Strba <fstrba@suse.com>
- Initial package for hawtjni version 1.16
