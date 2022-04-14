Vendor:         Microsoft Corporation
Distribution:   Mariner
%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:          scannotation
Version:       1.0.3
Release:       1%{?dist}
Summary:       A Java annotation scanner
License:       ASL 2.0
URL:           http://scannotation.sourceforge.net
# Also available here https://github.com/jharting/scannotation
# How we created tarball:
# svn export -r 12  https://scannotation.svn.sourceforge.net/svnroot/scannotation scannotation-1.0.3.Final
# tar -caJf scannotation-1.0.3.Final.tar.xz scannotation-1.0.3.Final
Source0:       %{name}-%{namedversion}.tar.xz
# Adding License file
Source1:       License.txt

BuildArch:     noarch

BuildRequires: maven-local
BuildRequires: mvn(javassist:javassist)
BuildRequires: mvn(javax.servlet:javax.servlet-api)
BuildRequires: mvn(junit:junit)

%description
Scannotation is a Java library that creates an annotation database 
from a set of .class files.This database is really just a set of maps that index
what annotations are used and what classes are using them. Why do you need this? 
What if you are an annotation framework like an EJB 3.0 container and you want 
to automatically scan your classpath for EJB annotations so that you know what 
to deploy? Scannotation gives you apis that allow you to find archives in your 
classpath or WAR (web application) that you want to scan, then automatically 
scans them without loading each and every class within those archives

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}

%pom_disable_module titan-test-jar
%pom_remove_dep :titan-cruise %{name}

# Force use servlet 3.1 apis
%pom_change_dep :servlet-api javax.servlet:javax.servlet-api:3.1.0 %{name}

cp -p %SOURCE1 .

%mvn_file org.%{name}:%{name} %{name}

%build

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%license License.txt

%files javadoc -f .mfiles-javadoc
%license License.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.3-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-0.20.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-0.19.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-0.18.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-0.17.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-0.16.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-0.15.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-0.14.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-0.13.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 08 2015 gil cattaneo <puntogil@libero.it> 1.0.3-0.12.r12
- fix FTBFS rhbz#1239715
- switch to java-headless rhbz#1068519
- switch to XMvn
- switch to glassfish-servlet-api
- use pom macros
- use BR mvn()-like
- fix some rpmlint problem
- introduce license macro

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.11.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Aug 07 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.3-0.10.r12
- Fix for junit and xmvn changes in F21 (#1107281)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.9.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Kashyap Chamarthy <kashyapc@fedoraproject.org> - 1.0.3.0 -8.r12
- Switch to java-headless in Requires. Fix rhbz#1068519

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.7.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.6.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.3-0.5.r12
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.4.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.3.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 14 2011 Kashyap Chamarthy <kashyapc@fedoraproject.org> 1.0.3-0.2.r12
- Preserve time stamps of files(License.txt in this case) being installed

* Thu Dec 1 2011 Kashyap Chamarthy <kashyapc@fedoraproject.org> 1.0.3-0.1.r12
- Initial packaging. With help from Ade Lee <vakwetu@fedoraproject.org>

