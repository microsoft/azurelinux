Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package args4j
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
Name:           args4j
Version:        2.33
Release:        2%{?dist}
Summary:        Java command line arguments parser
License:        MIT
Group:          Development/Libraries/Java
URL:            https://args4j.kohsuke.org
Source0:        https://github.com/kohsuke/%{name}/archive/%{name}-site-%{version}.tar.gz
Source1:        %{name}-build.tar.xz
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  mockito
%endif

%description
args4j is a small Java class library that makes it easy
to parse command line options/arguments in your CUI application.
- It makes the command line parsing very easy by using annotations
- You can generate the usage screen very easily
- You can generate HTML/XML that lists all options for your documentation
- Fully supports localization
- It is designed to parse javac like options (as opposed to GNU-style
  where ls -lR is considered to have two options l and R)

%package tools
Summary:        Development-time tool for generating additional artifacts
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}

%description tools
This package contains args4j development-time tool for generating
additional artifacts.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-site-%{version} -a 1

# removing classpath addition
sed -i 's/<addClasspath>true/<addClasspath>false/g' %{name}-tools/pom.xml

# fix ant group id
sed -i 's/<groupId>ant/<groupId>org.apache.ant/g' %{name}-tools/pom.xml

# removing bundled stuff
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%pom_remove_plugin :maven-shade-plugin %{name}-tools
%pom_remove_plugin -r :maven-site-plugin

# XMvn cannot generate requires on dependecies with scope "system"
%pom_xpath_remove "pom:profile[pom:id[text()='jdk-tools-jar']]" %{name}-tools

# we don't need these now
%pom_disable_module args4j-maven-plugin
%pom_disable_module args4j-maven-plugin-example

for i in args4j args4j-tools; do
  %pom_remove_parent $i
  %pom_xpath_inject pom:project "
    <groupId>args4j</groupId>
    <version>%{version}</version>
" $i
done

%build
mkdir -p lib
%if %{with tests}
build-jar-repository -s lib cglib/cglib mockito/mockito-core objectweb-asm/asm objenesis/objenesis
%ant package javadoc
%else
%ant -Dtest.skip=true package javadoc
%endif

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 %{name}/target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
(cd %{buildroot}%{_javadir} && ln -s %{name}/%{name}.jar %{name}.jar)
install -pm 0644 %{name}-tools/target/%{name}-tools-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}-tools.jar
(cd %{buildroot}%{_javadir} && ln -s %{name}/%{name}-tools.jar %{name}-tools.jar)

# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 %{name}/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
install -pm 0644 %{name}-tools/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-tools.pom
%add_maven_depmap %{name}/%{name}-tools.pom %{name}/%{name}-tools.jar -f tools

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -r %{name}/target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/%{name}
cp -r %{name}-tools/target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/%{name}-tools
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%{_javadir}/%{name}*.jar
%license %{name}/LICENSE.txt

%files tools -f .mfiles-tools

%files javadoc
%{_javadocdir}/%{name}
%license %{name}/LICENSE.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.33-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Dec 03 2020 Joe Schmitt <joschmit@microsoft.com> - 2.33-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Sep 24 2019 Fridrich Strba <fstrba@suse.com>
- Update to version 2.33
  * generate and customize the ant build files
- Add option to build with tests on (disabled by default)
- Package the tools in a subpackage
* Fri Sep 20 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent pom since we are not building
  using maven
* Fri Oct 19 2018 Fridrich Strba <fstrba@suse.com>
- Download from maven central the corresponding pom file and
  install it.
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
* Fri Sep 15 2017 fstrba@suse.com
- Fix build with jdk9: specify java source and target 1.6 and
  correct encoding of source files
- Clean spec file and fix rpmlint warning
* Fri Jul  1 2016 toddrme2178@gmail.com
- Fix Group tag.
* Fri Jul 18 2014 tchvatal@suse.com
- Cleanup a bit. Use MIT license as rh does.
* Thu Jul 14 2011 bmaryniuk@novell.com
- Packaged for the SUSE Linux.
