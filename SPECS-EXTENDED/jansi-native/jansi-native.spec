Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package jansi-native
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


%global bits %{__isa_bits}
%global debug_package %{nil}
Name:           jansi-native
Version:        1.7
Release:        3%{?dist}
Summary:        Jansi project JNI library implementation
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://github.com/fusesource/jansi-native
Source0:        https://github.com/fusesource/jansi-native/archive/jansi-native-%{version}.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  hawtjni
BuildRequires:  javapackages-local-bootstrap
Requires:       mvn(org.fusesource.hawtjni:hawtjni-runtime)

%description
Jansi is a Java library that allows you to use ANSI escape sequences
in Java console applications. It implements ANSI support on platforms
which don't support it like Windows and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation/HTML
BuildArch:      noarch

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jansi-native-jansi-native-%{version}
cp %{SOURCE1} .

%pom_xpath_remove pom:profiles

cp pom.xml pom-linux%{bits}.xml
%pom_xpath_set pom:project/pom:artifactId %{name} pom.xml
%pom_xpath_set pom:project/pom:artifactId jansi-linux%{bits} pom-linux%{bits}.xml

%pom_remove_parent .

%build
mkdir -p lib
build-jar-repository -s lib hawtjni/hawtjni-runtime

%{ant} -f %{name}-build.xml jar javadoc

# Create a manifest-only jar
%{ant} -f %{name}-build.xml -Dproject.platform=linux%{bits} manifest-jar

# generate the C files for native library
mkdir -p target/native-build
hawtjni-generator \
  -n jansi \
  -o target/native-build \
  -p org.fusesource.jansi.internal \
  -v \
  target/%{name}-%{version}.jar

# build the native library
mkdir -p target/native-build/META-INF/native/linux%{bits}
gcc -shared \
  -o target/native-build/META-INF/native/linux%{bits}/libjansi.so \
  -I %{java_home}/include/ -I %{java_home}/include/linux/ \
  -I src/main/native-package/src -I target/native-build \
  -fPIC target/native-build/*.c src/main/native-package/src/*.c
jar uf target/jansi-linux%{bits}-%{version}.jar -C target/native-build META-INF

%install
# jar
install -dm 0755 %{buildroot}%{_jnidir}/%{name}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_jnidir}/%{name}/%{name}.jar
install -pm 0644 target/jansi-linux%{bits}-%{version}.jar %{buildroot}%{_jnidir}/%{name}/jansi-linux%{bits}.jar
ln -sf jansi-linux%{bits}.jar %{buildroot}%{_jnidir}/%{name}/jansi-linux.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
install -pm 0644 pom-linux%{bits}.xml %{buildroot}%{_mavenpomdir}/%{name}/jansi-linux%{bits}.pom
%add_maven_depmap %{name}/jansi-linux%{bits}.pom %{name}/jansi-linux%{bits}.jar -a org.fusesource.jansi:jansi-linux
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%{_jnidir}/%{name}
%doc readme.md changelog.md
%license license.txt

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.7-2.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Use JAVA_HOME to set include dir.

* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent pom since we are not building
  using Maven.
* Thu Feb  7 2019 Jan Engelhardt <jengelh@inai.de>
- Avoid name repetition in summary, and use noun phrasing.
- Avoid double-shipping documentation.
* Mon Feb  4 2019 Fridrich Strba <fstrba@suse.com>
- Initial package of jansi-native 1.7
- Add jansi-native-build.xml for ant build
