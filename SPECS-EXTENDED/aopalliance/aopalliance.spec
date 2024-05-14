Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package aopalliance
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


Name:           aopalliance
Version:        1.0
Release:        4%{?dist}
Summary:        Java/J2EE AOP standards
License:        Public Domain
Group:          Development/Libraries/Java
URL:            https://aopalliance.sourceforge.net/
# cvs -d:pserver:anonymous@aopalliance.cvs.sourceforge.net:/cvsroot/aopalliance login
# password empty
# cvs -z3 -d:pserver:anonymous@aopalliance.cvs.sourceforge.net:/cvsroot/aopalliance export -r HEAD aopalliance
Source0:        %{_distro_sources_url}/aopalliance-src.tar.gz
Source1:        https://repo1.maven.org/maven2/aopalliance/aopalliance/1.0/aopalliance-1.0.pom
Source2:        %{name}-MANIFEST.MF
Source3:        %{name}-LICENSE.txt 
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
Aspect-Oriented Programming (AOP) offers a better solution to many
problems than do existing technologies, such as EJB.  AOP Alliance
facilitates and standardizes the use of AOP.

This package contains APIs for program instrumentation, interception
mechanisms, and a set of interfaces for implementing a generic
reflection API.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}
cp %{SOURCE3} ./LICENSE.txt

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} \
  -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 \
  -Dbuild.sysclasspath=only jar javadoc

# Inject OSGi manifest required by Eclipse.
jar umf %{SOURCE2} build/%{name}.jar

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 build/%{name}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-4
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-3
- Updating source URLs.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Feb  7 2019 Jan Engelhardt <jengelh@inai.de>
- Actually say what's included.
* Fri Oct 26 2018 Fridrich Strba <fstrba@suse.com>
- Initial packaging of aopalliance adapted from Fedora package
