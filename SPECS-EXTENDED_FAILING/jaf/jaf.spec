Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		jaf
Version:	1.2.1
Release:	5%{?dist}
Summary:	JavaBeans Activation Framework

License:	BSD
URL:		https://github.com/eclipse-ee4j/jaf

Source0:	https://github.com/eclipse-ee4j/jaf/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:	mvn(org.glassfish.hk2:osgiversion-maven-plugin)

%description
The JavaBeans Activation Framework (JAF) is a standard extension to the
Java platform that lets you take advantage of standard services to:
determine the type of an arbitrary piece of data; encapsulate access to it;
discover the operations available on it; and instantiate the appropriate
bean to perform the operation(s).

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
%{summary}.

%prep
%setup -q

%pom_disable_module demo

# maven-dependency-plugin doesn't work correctly without access to remote repos
%pom_remove_plugin :maven-dependency-plugin activationapi
mkdir -p %{_builddir}/%{name}-%{version}/activationapi/target/sources/
cp -r %{_builddir}/%{name}-%{version}/activation/src/main/java/javax/ %{_builddir}/%{name}-%{version}/activationapi/target/sources/
%pom_xpath_inject "/pom:project"  "<dependencies>
<dependency>
  <groupId>com.sun.activation</groupId>
  <artifactId>jakarta.activation</artifactId>
  <version>1.2.1</version>
</dependency>
</dependencies>" "activationapi/pom.xml"

%pom_remove_parent
%pom_remove_plugin org.commonjava.maven.plugins:directory-maven-plugin
%pom_remove_plugin org.codehaus.mojo:build-helper-maven-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md
%license NOTICE.md
%doc README.md

%files javadoc -f .mfiles-javadoc
%license LICENSE.md
%license NOTICE.md
%doc README.md

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.1-5
- Initial CBL-Mariner import from Fedora 30 (license: MIT).

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 19 2018 Marian Koncek <mkoncek@redhat.com> - 1.2.1-3
- Successful build

* Thu Nov 22 2018 Salman Siddiqui <sasiddiq@redhat.com> - 1.2.1-2
- Use official version 1.2.1 release

* Fri Sep 21 2018 Salman Siddiqui <sasiddiq@redhat.com> - 1.2.1-1
- Initial packaging
