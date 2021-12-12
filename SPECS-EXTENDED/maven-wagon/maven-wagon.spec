Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-wagon
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


Name:           maven-wagon
Version:        3.2.0
Release:        3%{?dist}
Summary:        Tools to manage artifacts and deployment
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/wagon
Source0:        http://repo1.maven.org/maven2/org/apache/maven/wagon/wagon/%{version}/wagon-%{version}-source-release.zip
Source1:        %{name}-build.tar.xz
BuildRequires:  ant
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-net
BuildRequires:  fdupes
BuildRequires:  httpcomponents-client
BuildRequires:  httpcomponents-core
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jsch
BuildRequires:  jsch-agent-proxy-connector-factory
BuildRequires:  jsch-agent-proxy-jsch
BuildRequires:  jsoup
BuildRequires:  plexus-interactivity-api
BuildRequires:  plexus-metadata-generator
BuildRequires:  plexus-utils
BuildRequires:  slf4j
BuildRequires:  unzip
BuildArch:      noarch

%description
Maven Wagon is a transport abstraction that is used in Maven's
artifact and repository handling code. Currently wagon has the
following providers:
* File
* HTTP
* FTP
* SSH/SCP
* WebDAV
* SCM (in progress)

%package provider-api
Summary:        The provider-api module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(org.codehaus.plexus:plexus-utils)

%description provider-api
The provider-api module for %{name}.

%package file
Summary:        The file module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(org.apache.maven.wagon:wagon-provider-api) = %{version}
Requires:       mvn(org.codehaus.plexus:plexus-utils)

%description file
The file module for %{name}.

%package ftp
Summary:        The ftp module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(commons-io:commons-io)
Requires:       mvn(commons-net:commons-net)
Requires:       mvn(org.apache.maven.wagon:wagon-provider-api) = %{version}
Requires:       mvn(org.slf4j:slf4j-api)

%description ftp
The ftp module for %{name}.

%package http
Summary:        The http module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(org.apache.httpcomponents:httpclient)
Requires:       mvn(org.apache.httpcomponents:httpcore)
Requires:       mvn(org.apache.maven.wagon:wagon-http-shared) = %{version}
Requires:       mvn(org.apache.maven.wagon:wagon-provider-api) = %{version}
Requires:       mvn(org.codehaus.plexus:plexus-utils)
Requires:       mvn(org.slf4j:jcl-over-slf4j)

%description http
The http module for %{name}.

%package http-shared
Summary:        The http-shared module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(commons-io:commons-io)
Requires:       mvn(org.apache.httpcomponents:httpclient)
Requires:       mvn(org.apache.httpcomponents:httpcore)
Requires:       mvn(org.apache.maven.wagon:wagon-provider-api) = %{version}
Requires:       mvn(org.jsoup:jsoup)
Requires:       mvn(org.slf4j:slf4j-api)

%description http-shared
The http-shared module for %{name}.

%package http-lightweight
Summary:        The http-lightweight module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(commons-io:commons-io)
Requires:       mvn(org.apache.maven.wagon:wagon-http-shared) = %{version}
Requires:       mvn(org.apache.maven.wagon:wagon-provider-api) = %{version}
Requires:       mvn(org.codehaus.plexus:plexus-utils)

%description http-lightweight
The http-lightweight module for %{name}.

%package ssh-common
Summary:        The ssh-common module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(org.apache.maven.wagon:wagon-provider-api) = %{version}
Requires:       mvn(org.codehaus.plexus:plexus-interactivity-api)
Requires:       mvn(org.codehaus.plexus:plexus-utils)

%description ssh-common
The ssh-common module for %{name}

%package ssh
Summary:        The ssh module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(com.jcraft:jsch)
Requires:       mvn(com.jcraft:jsch.agentproxy.connector-factory)
Requires:       mvn(com.jcraft:jsch.agentproxy.jsch)
Requires:       mvn(org.apache.maven.wagon:wagon-provider-api) = %{version}
Requires:       mvn(org.apache.maven.wagon:wagon-ssh-common) = %{version}
Requires:       mvn(org.codehaus.plexus:plexus-interactivity-api)
Requires:       mvn(org.codehaus.plexus:plexus-utils)

%description ssh
The ssh module for %{name}

%package ssh-external
Summary:        The ssh-external module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(org.apache.maven.wagon:wagon-provider-api) = %{version}
Requires:       mvn(org.apache.maven.wagon:wagon-ssh-common) = %{version}
Requires:       mvn(org.codehaus.plexus:plexus-utils)

%description ssh-external
The ssh-external module for %{name}

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n wagon-%{version} -a1

%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_dep :wagon-tck-http wagon-providers/wagon-http

# disable tests, missing dependencies
%pom_disable_module wagon-tcks
%pom_disable_module wagon-ssh-common-test wagon-providers/pom.xml
%pom_disable_module wagon-provider-test
%pom_remove_dep :wagon-provider-test
%pom_remove_dep :wagon-provider-test wagon-providers

# missing dependencies
%pom_disable_module wagon-webdav-jackrabbit wagon-providers

%pom_disable_module wagon-scm wagon-providers

for i in file ftp http http-shared http-lightweight ssh-common ssh ssh-external; do
  %pom_remove_parent wagon-providers/wagon-${i}
  %pom_xpath_inject "pom:project" "
    <groupId>org.apache.maven.wagon</groupId>
	<version>%{version}</version>" wagon-providers/wagon-${i}
done
%pom_remove_parent wagon-provider-api
%pom_xpath_inject "pom:project" "
  <groupId>org.apache.maven.wagon</groupId>
  <version>%{version}</version>" wagon-provider-api

%pom_change_dep -r -f ::::: :::::

%build
mkdir -p lib
build-jar-repository -s lib \
	commons-io commons-net jsch \
	jsch.agentproxy.core jsch.agentproxy.jsch jsch.agentproxy.connector-factory \
	httpcomponents/httpclient httpcomponents/httpcore \
	jsoup/jsoup plexus/utils plexus/interactivity-api slf4j/api 
# tests are disabled because of missing dependencies
%{ant} package javadoc

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 wagon-provider-api/target/wagon-provider-api-%{version}.jar %{buildroot}%{_javadir}/%{name}/provider-api.jar
for i in file ftp http http-shared http-lightweight ssh-common ssh ssh-external; do
  install -pm 0644 wagon-providers/wagon-${i}/target/wagon-${i}-%{version}.jar %{buildroot}%{_javadir}/%{name}/${i}.jar
done
# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 wagon-provider-api/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/provider-api.pom
%add_maven_depmap %{name}/provider-api.pom %{name}/provider-api.jar -f provider-api
for i in file ftp http http-shared http-lightweight ssh-common ssh ssh-external; do
  install -pm 0644 wagon-providers/wagon-${i}/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/${i}.pom
  if [ x${i} = xhttp ]; then
    # Maven requires Wagon HTTP with classifier "shaded"
    %add_maven_depmap %{name}/${i}.pom %{name}/${i}.jar -a org.apache.maven.wagon:wagon-http::shaded: -f ${i}
  else
    %add_maven_depmap %{name}/${i}.pom %{name}/${i}.jar -f ${i}
  fi
done
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/provider-api
cp -pr wagon-provider-api/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/provider-api
for i in file ftp http http-shared http-lightweight ssh-common ssh ssh-external; do
  install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/${i}
  cp -pr wagon-providers/wagon-${i}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/${i}/
done
%fdupes -s %{buildroot}%{_javadocdir}

%files provider-api -f .mfiles-provider-api
%license LICENSE NOTICE
%doc DEPENDENCIES

%files file -f .mfiles-file

%files ftp -f .mfiles-ftp

%files http -f .mfiles-http

%files http-shared -f .mfiles-http-shared

%files http-lightweight -f .mfiles-http-lightweight

%files ssh-common -f .mfiles-ssh-common

%files ssh -f .mfiles-ssh

%files ssh-external -f .mfiles-ssh-external

%files javadoc
%license LICENSE NOTICE
%doc DEPENDENCIES
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.0-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.2.0-2.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Oct  7 2019 Fridrich Strba <fstrba@suse.com>
- Build also the ssh* providers
* Sat Oct  5 2019 Fridrich Strba <fstrba@suse.com>
- Avoid unversioned dependencies
* Fri Mar 15 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-wagon 3.2.0
- Generate and customize the ant build files
