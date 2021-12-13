Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package jsch-agent-proxy
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


Name:           jsch-agent-proxy
Version:        0.0.7
Release:        4%{?dist}
Summary:        Proxy to ssh-agent and Pageant in Java
License:        BSD-3-Clause
Group:          Development/Libraries/Java
URL:            http://www.jcraft.com/jsch-agent-proxy/
Source0:        https://github.com/ymnk/jsch-agent-proxy/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-build.tar.xz
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jna
BuildRequires:  jna-contrib
BuildRequires:  jsch
BuildRequires:  trilead-ssh2
BuildArch:      noarch

%description
jsch-agent-proxy is a proxy program to OpenSSH ssh-agent and Pageant
included Putty. It can be integrated into JSch, and users
can be allowed to use those programs in authentications. This
software has been developed for JSch, but it can be applicable
to other SSH2 implementations in Java.

%package connector-factory
Summary:        Connector factory for jsch-agent-proxy
Group:          Development/Libraries/Java
Requires:       mvn(com.jcraft:jsch.agentproxy.core) = %{version}
Requires:       mvn(com.jcraft:jsch.agentproxy.pageant) = %{version}
Requires:       mvn(com.jcraft:jsch.agentproxy.sshagent) = %{version}
Requires:       mvn(com.jcraft:jsch.agentproxy.usocket-jna) = %{version}
Requires:       mvn(com.jcraft:jsch.agentproxy.usocket-nc) = %{version}

%description connector-factory
%{summary}.

%package core
Summary:        jsch-agent-proxy core module
Group:          Development/Libraries/Java

%description core
%{summary}.

%package jsch
Summary:        JSch connector for jsch-agent-proxy
Group:          Development/Libraries/Java
Requires:       mvn(com.jcraft:jsch)
Requires:       mvn(com.jcraft:jsch.agentproxy.core) = %{version}

%description jsch
%{summary}.

%package pageant
Summary:        Pageant connector for jsch-agent-proxy
Group:          Development/Libraries/Java
Requires:       mvn(com.jcraft:jsch.agentproxy.core) = %{version}
Requires:       mvn(net.java.dev.jna:jna)	
Requires:       mvn(net.java.dev.jna:platform)

%description pageant
%{summary}.

%package sshagent
Summary:        ssh-agent connector for jsch-agent-proxy
Group:          Development/Libraries/Java
Requires:       mvn(com.jcraft:jsch.agentproxy.core) = %{version}

%description sshagent
%{summary}.

%package svnkit-trilead-ssh2
Summary:        trilead-ssh2 connector for jsch-agent-proxy
Group:          Development/Libraries/Java
Requires:       mvn(com.jcraft:jsch.agentproxy.core) = %{version}
Requires:       mvn(com.trilead:trilead-ssh2)

%description svnkit-trilead-ssh2
%{summary}.

%package usocket-jna
Summary:        USocketFactory implementation using JNA
Group:          Development/Libraries/Java
Requires:       mvn(com.jcraft:jsch.agentproxy.core) = %{version}
Requires:       mvn(net.java.dev.jna:jna)	
Requires:       mvn(net.java.dev.jna:platform)

%description usocket-jna
%{summary}.

%package usocket-nc
Summary:        USocketFactory implementation using Netcat
Group:          Development/Libraries/Java

%description usocket-nc
%{summary}.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML
Requires:       mvn(com.jcraft:jsch.agentproxy.core) = %{version}

%description    javadoc
This package provides %{summary}.

%prep
%setup -q -a1

# Unnecessary for RPM builds
%pom_remove_plugin ":maven-javadoc-plugin"
%pom_remove_plugin ":maven-source-plugin"
%pom_xpath_remove pom:build/pom:extensions
%pom_disable_module jsch-agent-proxy-sshj

for package in connector-factory core jsch pageant sshagent \
               svnkit-trilead-ssh2 usocket-jna usocket-nc; do
    %pom_remove_parent %{name}-${package}
    %pom_xpath_inject pom:project "
                                <groupId>com.jcraft</groupId>
                                <version>%{version}</version>" %{name}-${package}
done

%build
mkdir lib
build-jar-repository -s lib jna jna-platform jsch trilead-ssh2

%{ant} \
    -Dtest.skip=true \
    package javadoc

%install
install -dm 0755 %{buildroot}/usr/share/java
install -dm 0755 %{buildroot}%{_mavenpomdir}

for package in connector-factory core jsch pageant sshagent \
               svnkit-trilead-ssh2 usocket-jna usocket-nc; do
    install -pm 0644 %{name}-${package}/target/jsch.agentproxy.${package}-%{version}.jar %{buildroot}/usr/share/java/jsch.agentproxy.${package}.jar
    install -pm 0644 %{name}-${package}/pom.xml %{buildroot}%{_mavenpomdir}/jsch.agentproxy.${package}.pom
    %add_maven_depmap jsch.agentproxy.${package}.pom jsch.agentproxy.${package}.jar -f ${package}

    # javadoc
    install -dm 0755 %{buildroot}%{_javadocdir}/%{name}-${package}
    cp -pr %{name}-${package}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}-${package}/
done

%fdupes -s %{buildroot}%{_javadocdir}

%files core -f .mfiles-core
%doc README README.md
%license LICENSE.txt

%files connector-factory -f .mfiles-connector-factory

%files jsch -f .mfiles-jsch

%files pageant -f .mfiles-pageant

%files sshagent -f .mfiles-sshagent

%files svnkit-trilead-ssh2 -f .mfiles-svnkit-trilead-ssh2

%files usocket-jna -f .mfiles-usocket-jna

%files usocket-nc -f .mfiles-usocket-nc

%files javadoc
%license LICENSE.txt
%{_javadocdir}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.7-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 0.0.7-3.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Oct 10 2019 Fridrich Strba <fstrba@suse.com>
- BuildRequire the new jna-contrib package
* Sun Jul  7 2019 Jan Engelhardt <jengelh@inai.de>
- Trim bias and conjecture from descriptions.
* Thu Jun 27 2019 Ismail Dönmez <idonmez@suse.com>
- Initial release (v0.0.7) for openSUSE
