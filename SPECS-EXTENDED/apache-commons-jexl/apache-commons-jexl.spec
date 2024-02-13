%global compatver 2.1.0
%define base_name jexl
%define short_name commons-%{base_name}
Summary:        Java Expression Language (JEXL)
Name:           apache-%{short_name}
Version:        2.1.1
Release:        3%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/jexl
Source0:        https://downloads.apache.org/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:        build.xml
Source2:        common.xml
Source3:        jexl2-compat-build.xml
# Patch to fix test failure with junit 4.11
Patch0:         001-Fix-tests.patch
# Fix javadoc build
Patch1:         apache-commons-jexl-javadoc.patch
Patch2:         0001-Port-to-current-javacc.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  apache-commons-logging
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javacc
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  javapackages-tools
Requires:       apache-commons-logging
Provides:       %{short_name} = %{version}-%{release}
BuildArch:      noarch

%description
Java Expression Language (JEXL) is an expression language engine which can be
embedded in applications and frameworks.  JEXL is inspired by Jakarta Velocity
and the Expression Language defined in the JavaServer Pages Standard Tag
Library version 1.1 (JSTL) and JavaServer Pages version 2.0 (JSP).  While
inspired by JSTL EL, it must be noted that JEXL is not a compatible
implementation of EL as defined in JSTL 1.1 (JSR-052) or JSP 2.0 (JSR-152).
For a compatible implementation of these specifications, see the Commons EL
project.

JEXL attempts to bring some of the lessons learned by the Velocity community
about expression languages in templating to a wider audience.  Commons Jelly
needed Velocity-ish method access, it just had to have it.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation/HTML
Provides:       %{short_name}-javadoc = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} jexl2-compat/build.xml
%patch 0 -p1 -b .test
%patch 1 -p1 -b .javadoc
%patch 2 -p1

# Java 1.6 contains bsf 3.0, so we don't need the dependency in the pom.xml file
%pom_remove_dep org.apache.bsf:bsf-api
find \( -name '*.jar' -o -name '*.class' \) -delete
# Fix line endings
find -name '*.txt' -exec sed -i 's/\r//' '{}' +

# Drop "-SNAPSHOT" from version
%pom_xpath_set "pom:project/pom:version" %{compatver} jexl2-compat
%pom_xpath_set "pom:dependency[pom:artifactId='commons-jexl']/pom:version" %{version} jexl2-compat

%pom_remove_parent . jexl2-compat

%build
mkdir -p lib
build-jar-repository -s lib commons-logging

# build.xml target "gen-sources" complains about missing Packages directory, creating one
export JAVA_HOME=$(find %{_libdir}/jvm -name "msopenjdk*")
mkdir -p $JAVA_HOME/Packages

# Mariner does not provide internal API's to call Suns java compiler.
# Setting this to false
sed -i -E "s/canRun = comSunToolsJavacMain.*$/canRun = false;/" ./src/test/java/org/apache/commons/jexl2/ClassCreator.java

# commons-jexl
%{ant} \
  -Djavacc.home=%{_datadir}/java \
  jar javadoc

# commons-jexl-compat
%{ant} \
  -f jexl2-compat/build.xml \
  -Dproject.version=%{compatver} \
  jar javadoc

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{short_name}.jar
ln -sf %{name}/%{short_name}.jar %{buildroot}%{_javadir}/%{short_name}.jar
install -pm 0644 jexl2-compat/target/%{short_name}-compat-%{compatver}.jar %{buildroot}%{_javadir}/%{name}/%{short_name}-compat.jar
ln -sf %{name}/%{short_name}-compat.jar %{buildroot}%{_javadir}/%{short_name}-compat.jar
# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{short_name}.pom
%add_maven_depmap %{name}/%{short_name}.pom %{name}/%{short_name}.jar
install -pm 0644 jexl2-compat/pom.xml  %{buildroot}%{_mavenpomdir}/%{name}/%{short_name}-compat.pom
%add_maven_depmap %{name}/%{short_name}-compat.pom %{name}/%{short_name}-compat.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/jexl2-compat
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
cp -pr jexl2-compat/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/jexl2-compat/
%fdupes -s %{buildroot}%{_javadocdir}

%check
# commons-jexl
%{ant} \
  -Djavacc.home=%{_datadir}/java \
  test

%{ant} \
  -f jexl2-compat/build.xml \
  -Dproject.version=%{compatver} \
  test

%files -f .mfiles
%license LICENSE.txt
%doc NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/%{short_name}*.jar

%files javadoc
%license LICENSE.txt
%doc NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Mon Nov 14 2022 Sumedh Sharma <sumsharma@microsoft.com> - 2.1.1-3
- Fix build errors
  * create 'Packages' directory under JDK_HOME
  * disable tests sources flag for invoking sun javac compiler
- Enable check section
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.1.1-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Thu Feb 28 2019 Fridrich Strba <fstrba@suse.com>
- Initial package based on Fedora rpm
- Generate and sanitize ant build files
