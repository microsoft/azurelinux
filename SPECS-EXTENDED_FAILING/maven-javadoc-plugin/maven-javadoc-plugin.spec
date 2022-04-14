Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-javadoc-plugin
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


%global flavor bootstrap
%if "%{flavor}" == "bootstrap"
%bcond_without bootstrap
%else
%bcond_with bootstrap
%endif
%global base_name maven-javadoc-plugin
Version:        3.1.1
Release:        3%{?dist}
Summary:        Maven plugin for creating javadocs
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/plugins/maven-javadoc-plugin
Source0:        https://repo1.maven.org/maven2/org/apache/maven/plugins/%{base_name}/%{version}/%{base_name}-%{version}-source-release.zip
Source1:        %{base_name}-build.xml
Patch0:         %{base_name}-bootstrap-resources.patch
Patch1:         0001-Port-to-current-plexus-utils.patch
# PATCH-FIX-OPENSUSE bmwiedemann -- https://issues.apache.org/jira/browse/MJAVADOC-619
Patch2:         reproducible-footer.patch
BuildRequires:  apache-commons-cli
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-lang3
BuildRequires:  atinject
BuildRequires:  fdupes
BuildRequires:  google-guice
BuildRequires:  guava20
BuildRequires:  httpcomponents-client
BuildRequires:  httpcomponents-core
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jdom2
BuildRequires:  maven-archiver
BuildRequires:  maven-artifact-transfer
BuildRequires:  maven-common-artifact-filters
BuildRequires:  maven-doxia-core
BuildRequires:  maven-doxia-logging-api
BuildRequires:  maven-doxia-module-xhtml
BuildRequires:  maven-doxia-sink-api
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-invoker
BuildRequires:  maven-lib
BuildRequires:  maven-plugin-annotations
BuildRequires:  maven-reporting-api
BuildRequires:  maven-shared-utils
BuildRequires:  maven-wagon-provider-api
BuildRequires:  objectweb-asm
BuildRequires:  plexus-archiver
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-cli
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-interactivity-api
BuildRequires:  plexus-io
BuildRequires:  plexus-languages
BuildRequires:  plexus-utils
BuildRequires:  qdox
BuildRequires:  sisu-inject
BuildRequires:  sisu-plexus
BuildRequires:  unzip
BuildRequires:  xbean
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildArch:      noarch
%if %{with bootstrap}
Name:           %{base_name}-bootstrap
BuildRequires:  ant
BuildRequires:  modello
BuildRequires:  plexus-metadata-generator
%else
Name:           %{base_name}
BuildRequires:  xmvn
BuildRequires:  mvn(org.apache.maven.plugins:maven-compiler-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-javadoc-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-resources-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-surefire-plugin)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
Obsoletes:      %{base_name}-bootstrap
#!BuildRequires: maven-compiler-plugin-bootstrap
#!BuildRequires: maven-jar-plugin-bootstrap
#!BuildRequires: maven-javadoc-plugin-bootstrap
#!BuildRequires: maven-plugin-plugin-bootstrap
#!BuildRequires: maven-resources-plugin-bootstrap
#!BuildRequires: maven-surefire-plugin-bootstrap
%endif

%description
The Maven Javadoc Plugin is a plugin that uses the javadoc tool for
generating javadocs for the specified project.

%if %{without bootstrap}
%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.
%endif

%prep
%setup -q -n %{base_name}-%{version}
%if %{with bootstrap}
cp %{SOURCE1} build.xml
%patch0 -p1
%endif

%patch1 -p1
%patch2 -p1

%pom_xpath_remove pom:project/pom:parent/pom:relativePath
%pom_remove_dep :::test:

%build
%if %{with bootstrap}
mkdir -p lib
build-jar-repository -s lib \
	apache-commons-lang3 \
	atinject \
	commons-cli \
	commons-io \
	guava20/guava-10.0 \
	guice/google-guice-no_aop \
	httpcomponents/httpclient \
	httpcomponents/httpcore \
	jdom2/jdom2 \
	maven-archiver/maven-archiver \
	maven-artifact-transfer/maven-artifact-transfer \
	maven-common-artifact-filters/maven-common-artifact-filters \
	maven-doxia/doxia-core \
	maven-doxia/doxia-logging-api \
	maven-doxia/doxia-module-xhtml \
	maven-doxia/doxia-module-xhtml5 \
	maven-doxia/doxia-sink-api \
	maven-doxia-sitetools/doxia-site-renderer \
	maven-invoker/maven-invoker \
	maven/maven-artifact \
	maven/maven-core \
	maven/maven-model \
	maven/maven-model-builder \
	maven/maven-plugin-api \
	maven/maven-settings \
	maven-plugin-tools/maven-plugin-annotations \
	maven-reporting-api/maven-reporting-api \
	maven-shared-utils/maven-shared-utils \
	maven-wagon/provider-api \
	objectweb-asm/asm \
	org.eclipse.sisu.inject \
	org.eclipse.sisu.plexus \
	plexus/archiver \
	plexus-classworlds \
	plexus/cli \
	plexus-containers/plexus-component-annotations \
	plexus/interactivity-api \
	plexus/io \
	plexus-languages/plexus-java \
	plexus-metadata-generator \
	plexus/utils \
	qdox \
	xbean/xbean-reflect
%{ant} -Dtest.skip=true jar
%else
xmvn --batch-mode --offline \
	-Dmaven.test.skip=true -DmavenVersion=3.5.0 \
%if %{?pkg_vcmp:%pkg_vcmp java-devel >= 9}%{!?pkg_vcmp:0}
	-Dmaven.compiler.release=7 \
%endif
	package org.apache.maven.plugins:maven-javadoc-plugin:aggregate
%endif

%{mvn_artifact} pom.xml target/%{base_name}-%{version}.jar

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE
%doc NOTICE

%if %{without bootstrap}
%files javadoc -f .mfiles-javadoc
%license LICENSE
%doc NOTICE
%endif

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.1-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.1.1-2.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Switch to bootstrap mode.
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Mar 11 2020 Fridrich Strba <fstrba@suse.com>
- Fix build with doxia 1.9.x
* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 3.1.1
- Modified patch:
  * maven-javadoc-plugin-bootstrap-resources.patch
    + Regenerate patch from the non-bootstrap build
* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Fix build with maven-invoker-3.0.1 that has a new dependency
  on maven-shared-utils
* Mon Oct  7 2019 Bernhard Wiedemann <bwiedemann@suse.com>
- Add reproducible-footer.patch to override build date (boo#1047218)
* Sat Apr  6 2019 Jan Engelhardt <jengelh@inai.de>
- Spruce up summary to not just repeat the name.
* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-jar-plugin 3.0.1
- Generate and customize ant build.xml file to use with the
  bootstrap variang
- Create as a multibuild package to allow bootstrapping
- Added patch:
  * maven-javadoc-plugin-bootstrap-resources.patch
    + For the bootstrap version, add pre-generated resources that
    need maven-plugin-plugin and maven to be generated at build
    time
