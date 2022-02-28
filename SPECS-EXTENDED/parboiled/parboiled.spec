Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package parboiled
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


%global flavor %{nil}
%if "%{flavor}" == "scala"
%bcond_without scala
%else
%bcond_with scala
%endif
%global scala_short_version 2.10
%global base_name parboiled
%if %{with scala}
Name:           %{base_name}-scala
Summary:        Parboiled for Scala
License:        Apache-2.0
Group:          Development/Libraries/Java
%else
Name:           %{base_name}
Summary:        Java/Scala library providing parsing of input text based on PEGs
License:        Apache-2.0
Group:          Development/Libraries/Java
%endif
Version:        1.1.6
Release:        5%{?dist}
URL:            http://parboiled.org/
Source0:        https://github.com/sirthias/parboiled/archive/%{version}.tar.gz#/%{base_name}-%{version}.tar.gz
Source1:        %{base_name}-%{version}-build.tar.xz
# for build see https://github.com/sirthias/parboiled/wiki/Building-parboiled
Source2:        http://repo1.maven.org/maven2/org/parboiled/%{base_name}-core/%{version}/%{base_name}-core-%{version}.pom
Source3:        http://repo1.maven.org/maven2/org/parboiled/%{base_name}-java/%{version}/%{base_name}-java-%{version}.pom
Source4:        http://repo1.maven.org/maven2/org/parboiled/%{base_name}-scala_%{scala_short_version}/%{version}/%{base_name}-scala_%{scala_short_version}-%{version}.pom
Patch0:         parboiled-port-to-objectweb-asm-5.0.1.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
%if %{with scala}
BuildRequires:  ant-scala >= 2.10.7
BuildRequires:  parboiled
Requires:       mvn(org.parboiled:parboiled-core) = %{version}
Requires:       mvn(org.scala-lang:scala-library)
%else
BuildRequires:  objectweb-asm
Requires:       mvn(org.ow2.asm:asm)
Requires:       mvn(org.ow2.asm:asm-analysis)
Requires:       mvn(org.ow2.asm:asm-tree)
Requires:       mvn(org.ow2.asm:asm-util)
%endif
BuildArch:      noarch

%description
%if %{with scala}
An internal Scala DSL for efficiently defining your parser rules.

%endif
parboiled is a mixed Java/Scala library providing parsing of
arbitrary input text based on Parsing expression grammars (PEGs).
PEGs are an alternative to context free grammars (CFGs) for formally
specifying syntax, they make a replacement for regular expressions
and generally have some advantages over the "traditional" way of
building parser via CFGs.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{base_name}-%{version} -a1

find . -name "*.class" -delete
find . -name "*.jar" -delete

%patch0 -p1

cp %{SOURCE2} %{base_name}-core/pom.xml
cp %{SOURCE3} %{base_name}-java/pom.xml
cp %{SOURCE4} %{base_name}-scala/pom.xml

%build
mkdir -p lib
build-jar-repository -s lib \
%if %{with scala}
	%{base_name}
%else
	objectweb-asm
%endif
%{ant} \
%if %{with scala}
	-Dscala.libDir=%{_datadir}/scala/lib \
	-f build-scala.xml \
%endif
	package javadoc

%install
%if %{with scala}
%global modules scala
%else
%global modules core java
%endif
install -dm 0755 %{buildroot}%{_javadir}/%{base_name}
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{base_name}
for i in %{modules}; do
  # jar
  install -pm 0644 %{base_name}-${i}/target/%{base_name}-${i}*%{version}.jar %{buildroot}%{_javadir}/%{base_name}/${i}.jar
  # pom
  install -pm 0644 %{base_name}-${i}/pom.xml %{buildroot}%{_mavenpomdir}/%{base_name}/${i}.pom
  %add_maven_depmap %{base_name}/${i}.pom %{base_name}/${i}.jar
  # javadoc
  install -dm 0755 %{buildroot}%{_javadocdir}/%{base_name}/${i}
  cp -pr %{base_name}-${i}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{base_name}/${i}/
done
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc CHANGELOG README.markdown
%license LICENSE

%files javadoc
%license LICENSE
%{_javadocdir}/%{base_name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.6-5
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.1.6-4.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Dec  2 2019 Fridrich Strba <fstrba@suse.com>
- Require scala >= 2.10.7 for build: allows buiding with jdk9+
* Wed Nov 27 2019 Fridrich Strba <fstrba@suse.com>
- Split the scala subpackage from the main parboiled package in
  order to split build dependencies: build them as _multibuild
  package
* Tue Apr  9 2019 Jan Engelhardt <jengelh@inai.de>
- Ensure neutrality of description.
* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of parboiled 1.1.6
- Generate and customize ant build files
