Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package google
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


%global short_name guice
Name:           google-%{short_name}
Version:        4.1
Release:        2%{?dist}
Summary:        Dependency injection framework for Java 5 and above
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://github.com/google/%{short_name}
# ./create-tarball.sh %%{version}
Source0:        %{name}-%{version}.tar.xz
Source1:        create-tarball.sh
Patch0:         guice-4.1-fixup-ant.patch
Patch1:         guice-4.1-disabledextensions.patch
Patch2:         guice-4.1-javadoc.patch
BuildRequires:  ant
BuildRequires:  aopalliance
BuildRequires:  aqute-bnd
BuildRequires:  atinject
BuildRequires:  cglib
BuildRequires:  fdupes
BuildRequires:  glassfish-servlet-api
BuildRequires:  guava20
BuildRequires:  jarjar
BuildRequires:  java-devel >= 1.7
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  objectweb-asm
BuildRequires:  slf4j
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildArch:      noarch

%description
Guice alleviates the need for factories and the use of "new" in Java
code. Guice's @Inject is a different "new". Writing factories will
still be needed in some cases, but code will not directly depend on
them.

Guice embraces Java's type safe nature, especially when it comes to
features introduced in Java 5 such as generics and annotations.

%package -n %{short_name}-parent
Summary:        Guice parent POM
Group:          Development/Libraries/Java

%description -n %{short_name}-parent
Guice is a dependency injection framework for Java 5
and above. This package provides parent POM for Guice modules.

%package -n %{short_name}-assistedinject
Summary:        AssistedInject extension module for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-assistedinject
Guice is a dependency injection framework for Java 5
and above. This package provides AssistedInject module for Guice.

%package -n %{short_name}-extensions
Summary:        Extensions for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-extensions
Guice is a dependency injection framework for Java 5
and above. This package provides extensions POM for Guice.

%package -n %{short_name}-grapher
Summary:        Grapher extension module for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-grapher
Guice is a dependency injection framework for Java 5
and above. This package provides Grapher module for Guice.

%package -n %{short_name}-jmx
Summary:        JMX extension module for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-jmx
Guice is a dependency injection framework for Java 5
and above. This package provides JMX module for Guice.

%package -n %{short_name}-jndi
Summary:        JNDI extension module for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-jndi
Guice is a dependency injection framework for Java 5
and above. This package provides JNDI module for Guice.

%package -n %{short_name}-multibindings
Summary:        MultiBindings extension module for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-multibindings
Guice is a dependency injection framework for Java 5
and above. This package provides MultiBindings module for Guice.

%package -n %{short_name}-servlet
Summary:        Servlet extension module for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-servlet
Guice is a dependency injection framework for Java 5
and above. This package provides Servlet module for Guice.

%package -n %{short_name}-testlib
Summary:        TestLib extension module for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-testlib
Guice is a dependency injection framework for Java 5
and above. This package provides TestLib module for Guice.

%package -n %{short_name}-throwingproviders
Summary:        ThrowingProviders extension module for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-throwingproviders
Guice is a dependency injection framework for Java 5
and above. This package provides ThrowingProviders module for Guice.

%package -n %{short_name}-bom
Summary:        Bill of Materials for Guice
Group:          Development/Libraries/Java

%description -n %{short_name}-bom
Guice is a dependency injection framework for Java 5
and above. This package provides Bill of Materials module for Guice.

%package javadoc
Summary:        API documentation for Guice
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
find . -name "*.jar" -and ! -name "munge.jar" -delete
find . -name "*.class" -delete

# We don't have struts2 in Fedora yet.
%pom_disable_module struts2 extensions
# Android-specific extension
%pom_disable_module dagger-adapter extensions

# Fix OSGi metadata due to not using jarjar
%pom_xpath_set "pom:instructions/pom:Import-Package" \
  "!com.google.inject.*,*" core

# Animal sniffer is only causing problems. Disable it for now.
%pom_remove_plugin :animal-sniffer-maven-plugin core
%pom_remove_plugin :animal-sniffer-maven-plugin extensions

%pom_remove_plugin :maven-gpg-plugin

# We don't have the custom doclet used by upstream. Remove
# maven-javadoc-plugin to generate javadocs with default style.
%pom_remove_plugin -r :maven-javadoc-plugin

# remove test dependency to make sure we don't produce requires
# see #1007498
%pom_remove_dep :guava-testlib extensions
%pom_xpath_remove "pom:dependency[pom:classifier[text()='tests']]" extensions

%pom_remove_parent
%pom_set_parent com.google.inject:guice-parent:%{version} jdk8-tests

%pom_disable_module persist extensions
%pom_disable_module spring extensions

%pom_disable_module jdk8-tests

%pom_remove_plugin :maven-remote-resources-plugin
%pom_remove_plugin :maven-bundle-plugin
%pom_remove_plugin :maven-source-plugin

%pom_remove_plugin :maven-remote-resources-plugin extensions
%pom_remove_plugin :maven-bundle-plugin extensions
%pom_remove_plugin :maven-source-plugin extensions

%pom_xpath_remove "pom:dependency[pom:scope[text()='test']]" core
%pom_xpath_remove "pom:profiles" core
%pom_xpath_remove "pom:build" core
%pom_xpath_remove "pom:optional" core

%build
%{mvn_alias} "com.google.inject.extensions:" "org.sonatype.sisu.inject:"

%{mvn_package} :::no_aop: guice
%{mvn_package} :{*} @1

%{mvn_file}  ":guice-{*}"  %{short_name}/guice-@1
%{mvn_file}  ":guice" %{short_name}/%{name} %{name}
%{mvn_alias} ":guice" "org.sonatype.sisu:sisu-guice"

mkdir -p lib/build
mkdir -p extensions/servlet/lib/build
build-jar-repository -s -p lib/build \
  guava20 javax.inject glassfish-servlet-api aopalliance cglib objectweb-asm aqute-bnd jarjar
%{ant} clean.all no_aop
pushd build/no_aop
%pom_xpath_inject "pom:project" "<classifier>no_aop</classifier>" core
%{ant} -Dversion=%{version} jar
popd
%{ant} -Dversion=%{version} dist javadoc

%{mvn_artifact} pom.xml
%{mvn_artifact} bom/pom.xml
%{mvn_artifact} build/no_aop/core/pom.xml build/no_aop/build/guice-%{version}.jar
# a huge hack to force the no_aop classifier to the version 2.3.0 reactor
perl -pi -e 's#<ns0:artifactId>guice</ns0:artifactId>#<ns0:artifactId>guice</ns0:artifactId><ns0:classifier>no_aop</ns0:classifier>#g' .xmvn-reactor
%{mvn_artifact} core/pom.xml build/guice-%{version}.jar
%{mvn_artifact} extensions/pom.xml
%{mvn_artifact} extensions/jmx/pom.xml build/dist/guice-jmx-%{version}.jar
%{mvn_artifact} extensions/assistedinject/pom.xml build/dist/guice-assistedinject-%{version}.jar
%{mvn_artifact} extensions/multibindings/pom.xml build/dist/guice-multibindings-%{version}.jar
%{mvn_artifact} extensions/throwingproviders/pom.xml build/dist/guice-throwingproviders-%{version}.jar
%{mvn_artifact} extensions/servlet/pom.xml build/dist/guice-servlet-%{version}.jar
%{mvn_artifact} extensions/jndi/pom.xml build/dist/guice-jndi-%{version}.jar
%{mvn_artifact} extensions/testlib/pom.xml build/dist/guice-testlib-%{version}.jar
%{mvn_artifact} extensions/grapher/pom.xml build/dist/guice-grapher-%{version}.jar

%install
%mvn_install -J build/docs/javadoc
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles-guice
%dir %{_javadir}/%{short_name}

%files -n %{short_name}-parent -f .mfiles-guice-parent
%license COPYING

%files -n %{short_name}-assistedinject -f .mfiles-guice-assistedinject

%files -n %{short_name}-extensions -f .mfiles-extensions-parent

%files -n %{short_name}-grapher -f .mfiles-guice-grapher

%files -n %{short_name}-jmx -f .mfiles-guice-jmx

%files -n %{short_name}-jndi -f .mfiles-guice-jndi

%files -n %{short_name}-multibindings -f .mfiles-guice-multibindings
%if %{with jpa}
%files -n %{short_name}-persist -f .mfiles-guice-persist
%endif

%files -n %{short_name}-servlet -f .mfiles-guice-servlet
%if %{with spring}
%files -n %{short_name}-spring -f .mfiles-guice-spring
%endif

%files -n %{short_name}-testlib -f .mfiles-guice-testlib

%files -n %{short_name}-throwingproviders -f .mfiles-guice-throwingproviders

%files -n %{short_name}-bom -f .mfiles-guice-bom

%files javadoc -f .mfiles-javadoc
%license COPYING

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 18 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.1-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Clean the tarball in order to avoid files with spurious legal
  status
* Wed Mar 27 2019 Jan Engelhardt <jengelh@inai.de>
- Trim bias from description.
* Wed Mar 27 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of google-guice 4.1
