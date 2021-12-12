Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package pegdown
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


Name:           pegdown
Version:        1.4.2
Release:        2%{?dist}
Summary:        Java library for Markdown processing
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://pegdown.org
Source0:        https://github.com/sirthias/pegdown/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Newer release use sbt builder
Source1:        http://repo1.maven.org/maven2/org/pegdown/pegdown/%{version}/pegdown-%{version}.pom
Source2:        %{name}-build.xml
# Forwarded upstream: https://github.com/sirthias/pegdown/pull/130
Patch0:         %{name}-rhbz1096735.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  parboiled
Requires:       mvn(org.parboiled:parboiled-java)
BuildArch:      noarch

%description
A pure-Java Markdown processor based on a parboiled PEG parser
supporting a number of extensions.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
find . -name "*.class" -delete
find . -name "*.jar" -delete
%patch0 -p1

cp %{SOURCE1} pom.xml
cp %{SOURCE2} build.xml

rm -r src/test/scala/*
%pom_remove_dep org.specs2:specs2_2.9.3

%{mvn_file} :%{name} %{name}

%build
mkdir -p lib
build-jar-repository -s lib parboiled/core parboiled/java
%{ant} jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc CHANGELOG README.markdown
%license LICENSE NOTICE

%files javadoc
%license LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.2-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.4.2-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of pegdown 1.4.2
- Generate and customize ant build.xml file
