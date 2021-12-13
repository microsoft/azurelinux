Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-doxia-sitetools
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


%global parent maven-doxia
%global subproj sitetools
Name:           %{parent}-%{subproj}
Version:        1.9.2
Release:        2%{?dist}
Summary:        Doxia content generation framework
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://maven.apache.org/doxia/
Source0:        https://repo1.maven.org/maven2/org/apache/maven/doxia/doxia-sitetools/%{version}/doxia-%{subproj}-%{version}-source-release.zip
Source1:        %{name}-build.tar.xz
Patch0:         0001-Port-to-plexus-utils-3.0.24.patch
Patch1:         0002-Remove-dependency-on-velocity-tools.patch
BuildRequires:  ant
BuildRequires:  apache-commons-cli
BuildRequires:  apache-commons-collections
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-lang3
BuildRequires:  fdupes
BuildRequires:  guava20
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jdom2
BuildRequires:  maven-artifact
BuildRequires:  maven-artifact-manager
BuildRequires:  maven-doxia-core
BuildRequires:  maven-doxia-logging-api
BuildRequires:  maven-doxia-module-xhtml
BuildRequires:  maven-doxia-sink-api
BuildRequires:  maven-lib
BuildRequires:  maven-project
BuildRequires:  maven-reporting-api
BuildRequires:  modello
BuildRequires:  objectweb-asm
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-cli
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-i18n
BuildRequires:  plexus-interpolation
BuildRequires:  plexus-metadata-generator
BuildRequires:  plexus-utils
BuildRequires:  plexus-velocity
BuildRequires:  qdox
BuildRequires:  unzip
BuildRequires:  velocity
BuildRequires:  xbean
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  xz
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-apt)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-fml)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-xdoc)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-xhtml5)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildArch:      noarch

%description
Doxia is a content generation framework which aims to provide its
users with powerful techniques for generating static and dynamic
content. Doxia can be used to generate static sites in addition to
being incorporated into dynamic content generation systems like blogs,
wikis and content management systems.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n doxia-%{subproj}-%{version} -a1
%patch0 -p1
%patch1 -p1

# complains
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-enforcer-plugin

%pom_remove_plugin org.codehaus.mojo:clirr-maven-plugin
%pom_remove_dep net.sourceforge.htmlunit:htmlunit doxia-site-renderer/pom.xml
%pom_remove_dep -r :velocity-tools

%pom_xpath_inject "pom:plugin[pom:artifactId[text()='modello-maven-plugin']]/pom:configuration" \
    "<useJava5>true</useJava5>" doxia-decoration-model

# There are two backends for generating PDFs: one based on iText and
# one using FOP.  iText module is broken and only brings additional
# dependencies.  Besides that upstream admits that iText support will
# likely removed in future versions of Doxia.
#
# See also: http://maven.apache.org/doxia/faq.html#How_to_export_in_PDF
# http://lists.fedoraproject.org/pipermail/java-devel/2013-April/004742.html
rm -rf $(find -type d -name itext)
%pom_remove_dep -r :doxia-module-itext

%pom_remove_dep -r :doxia-module-markdown

%pom_remove_dep -r :doxia-module-fo
rm -r doxia-doc-renderer/src/main/java/org/apache/maven/doxia/docrenderer/pdf/fo

%{mvn_alias} :doxia-integration-tools org.apache.maven.shared:maven-doxia-tools

%build
mkdir -p lib
build-jar-repository -s lib \
	apache-commons-collections \
	apache-commons-lang3 \
	commons-cli \
	commons-io \
	guava20/guava-20.0 \
	jdom2/jdom2 \
	maven-doxia/doxia-core \
	maven-doxia/doxia-logging-api \
	maven-doxia/doxia-module-xhtml \
	maven-doxia/doxia-module-xhtml5 \
	maven-doxia/doxia-sink-api \
	maven/maven-artifact \
	maven/maven-artifact-2.0.2 \
	maven/maven-artifact-manager \
	maven/maven-model \
	maven/maven-plugin-api \
	maven/maven-project \
	maven-reporting-api/maven-reporting-api \
	objectweb-asm/asm \
	plexus-classworlds \
	plexus/cli \
	plexus-containers/plexus-component-annotations \
	plexus-containers/plexus-container-default \
	plexus-i18n/plexus-i18n \
	plexus/interpolation \
	plexus-metadata-generator \
	plexus/utils \
	plexus-velocity/plexus-velocity \
	qdox \
	velocity \
	xbean/xbean-reflect
# tests can't run because of missing deps
%{ant} -Dtest.skip=true package javadoc

mkdir -p target/site/apidocs
for i in \
    doxia-decoration-model \
    doxia-skin-model \
    doxia-integration-tools \
    doxia-site-renderer \
    doxia-doc-renderer; do
  %{mvn_artifact} ${i}/pom.xml ${i}/target/${i}-%{version}.jar
  if [ -d ${i}/target/site/apidocs ]; then
    cp -r ${i}/target/site/apidocs target/site/apidocs/${i}
  fi
done

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.2-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.9.2-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Remove doxia-module-fo integration.

* Wed Mar 11 2020 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 1.9.2
- Modified patches:
  * 0001-Port-to-plexus-utils-3.0.24.patch
  * 0002-Remove-dependency-on-velocity-tools.patch
    + fix incorrect line end
* Thu Mar 28 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-doxia-sitetools 1.7.5
- Generate and customize ant build files
