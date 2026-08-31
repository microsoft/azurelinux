# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           tomcat-jakartaee-migration
Version:        1.0.9
Release:        8%{?dist}
Summary:        Tomcat Migration Tool for Jakarta EE

License:        Apache-2.0
URL:            http://tomcat.apache.org/
Source0:        http://www.apache.org/dist/tomcat/jakartaee-migration/v%{version}/source/jakartaee-migration-%{version}-src.tar.gz
Source1:        javax2jakarta
# Do not generate manifest Class-Path, we rely on system-installed JARs
Patch0:         tomcat-jakartaee-migration-1.0.9-no-manifest-classpath.patch

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  bcel
BuildRequires:  apache-commons-compress
BuildRequires:  apache-commons-io
BuildRequires:  ant-openjdk25 
BuildRequires:  java-25-devel
	
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin) 
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin) 
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin) 

%description
The purpose of the tool is to take a web application written for Java EE 8 that runs on Apache Tomcat 9 and convert it automatically so it runs on Apache Tomcat 10 which implements Jakarta EE 9.

%package javadoc
Summary:        Javadoc for %{name}
 
%description javadoc
API documentation for %{name}.

%prep
%setup -q -n jakartaee-migration-%{version}
%patch 0 -p0
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin org.jacoco:jacoco-maven-plugin

%build
%mvn_build 

%install
%mvn_install

%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -m 0755 %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}

%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_datarootdir}/licenses/%{name}-javadoc
%{__mv} ${RPM_BUILD_ROOT}%{_javadocdir}/%{name}/legal/ADDITIONAL_LICENSE_INFO ${RPM_BUILD_ROOT}%{_datarootdir}/licenses/%{name}-javadoc/

%files -f .mfiles
%license LICENSE.txt
%doc CHANGES.md README.md
%{_bindir}/javax2jakarta
 
%files javadoc -f .mfiles-javadoc
%{_datarootdir}/licenses/%{name}-javadoc/ADDITIONAL_LICENSE_INFO
%license LICENSE.txt

%changelog
* Mon Nov 17 2025 Dimitris Soumis <dsoumis@redhat.com> - 1.0.9-8
- Disable manifest Class-Path in jakartaee-migration.jar to match Fedora system-JAR layout

* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.0.9-7
- Rebuilt for java-25-openjdk as preffered jdk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 08 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.8-4
- Remove jacoco build dependency

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 17 2024 Dimitris Soumis <dsoumis@redhat.com> - 1.0.8-2
- Add javax2jakarta CLI

* Fri Feb 09 2024 Hui Wang <huwang@redhat.com> - 1.0.8-1
- First build

