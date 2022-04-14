Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-reporting-impl
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
Name:           maven-reporting-impl
Version:        3.0.0
Release:        3%{?dist}
Summary:        Abstract classes to manage report generation
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/%{name}
Source0:        http://repo1.maven.org/maven2/org/apache/maven/reporting/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
Patch0:         0001-Remove-dependency-on-junit-addons.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  maven-doxia-core
BuildRequires:  maven-doxia-logging-api
BuildRequires:  maven-doxia-module-xhtml
BuildRequires:  maven-doxia-module-xhtml5
BuildRequires:  maven-doxia-sink-api
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-lib
BuildRequires:  maven-plugin-annotations
BuildRequires:  maven-reporting-api
BuildRequires:  maven-shared-utils
BuildRequires:  plexus-utils
BuildRequires:  unzip
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
Abstract classes to manage report generation, which can be run both:

* as part of a site generation (as a maven-reporting-api's MavenReport),
* or as a direct standalone invocation (as a maven-plugin-api's Mojo).

This is a replacement package for maven-shared-reporting-impl

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml
%patch0 -p1

# integration tests try to download stuff from the internet
# and therefore they don't work in Build Service
%pom_remove_plugin :maven-invoker-plugin

%build
mkdir -p lib
build-jar-repository -s lib \
	maven-doxia/doxia-core \
	maven-doxia/doxia-logging-api \
	maven-doxia/doxia-module-xhtml \
	maven-doxia/doxia-module-xhtml5 \
	maven-doxia/doxia-sink-api \
	maven-doxia-sitetools/doxia-decoration-model \
	maven-doxia-sitetools/doxia-site-renderer \
	maven/maven-core \
	maven/maven-plugin-api \
	maven-plugin-tools/maven-plugin-annotations \
	maven-reporting-api/maven-reporting-api \
	maven-shared-utils/maven-shared-utils \
	plexus/utils

%{ant} \
%if %{without tests}
	-Dtest.skip=true \
%endif
	jar javadoc

%{mvn_artifact} pom.xml target/%{name}-%{version}.jar

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE
%doc NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE
%doc NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.0-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 27 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.0.0-2.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Mar 11 2020 Fridrich Strba <fstrba@suse.com>
- Fix build against newer doxia that requires html5 module
* Fri Mar 29 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-reporting-impl 3.0.0
- Generate and customize ant build.xml file
