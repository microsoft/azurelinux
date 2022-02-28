Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package jansi
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


%bcond_with tests
Name:           jansi
Version:        1.17.1
Release:        4%{?dist}
Summary:        Java library for generating and interpreting ANSI escape sequences
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://fusesource.github.io/jansi/
Source0:        https://github.com/fusesource/jansi/archive/jansi-project-%{version}.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  hawtjni-runtime
BuildRequires:  jansi-native
BuildRequires:  javapackages-local-bootstrap
%if %{with tests}
BuildRequires:  ant-junit
%endif
Requires:       mvn(org.fusesource.hawtjni:hawtjni-runtime)
Requires:       mvn(org.fusesource.jansi:jansi-native)
BuildArch:      noarch

%description
Jansi is a java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it, like Windows, and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jansi-jansi-project-%{version}
cp %{SOURCE1} .

%pom_disable_module example
%pom_xpath_remove "pom:build/pom:extensions"

%pom_remove_plugin -r :maven-site-plugin

# No maven-uberize-plugin
%pom_remove_plugin -r :maven-uberize-plugin

# Remove unnecessary deps for jansi-native builds
pushd jansi
%pom_remove_dep :jansi-windows32
%pom_remove_dep :jansi-windows64
%pom_remove_dep :jansi-osx
%pom_remove_dep :jansi-freebsd32
%pom_remove_dep :jansi-freebsd64
# it's there only to be bundled in uberjar and we disable uberjar generation
%pom_remove_dep :jansi-linux32
%pom_remove_dep :jansi-linux64
popd

%pom_remove_parent jansi
%pom_xpath_inject pom:project "
  <groupId>org.fusesource.jansi</groupId>
  <version>%{version}</version>" jansi
%pom_change_dep ::\${jansi-native-version} ::1.8 jansi

%build
mkdir -p jansi/lib
build-jar-repository -s jansi/lib \
	hawtjni/hawtjni-runtime jansi-native/jansi-native 
%{ant} -f %{name}-build.xml \
%if %{without tests}
	-Dtest.skip=true \
%endif
	jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 jansi/target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 jansi/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
# javadoc
%fdupes -s %{buildroot}%{_javadocdir}
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr jansi/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license license.txt
%doc readme.md changelog.md

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.17.1-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.17.1-3.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Jun 27 2019 Fridrich Strba <fstrba@suse.com>
- Remove the reference to jansi-project parent from jansi pom
- Resolve manually jansi-native-version variable so that ivy
  understands it
* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent pom since we are not building
  using Maven.
- Make tests conditional and switched off by default
* Thu Feb  7 2019 Jan Engelhardt <jengelh@inai.de>
- Fix double-shipping of documentation
- Avoid name repetition in summary (potential rpmlint warning
* Mon Feb  4 2019 Fridrich Strba <fstrba@suse.com>
- Initial package of jansi 1.17.1
- Add build.xml file for building with ant
