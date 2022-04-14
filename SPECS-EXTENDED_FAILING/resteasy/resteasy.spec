Vendor:         Microsoft Corporation
Distribution:   Mariner
%global namedreltag .Final
%global namedversion %{version}%{namedreltag}

Name:           resteasy
Version:        3.0.26
Release:        7%{?dist}
Summary:        Framework for RESTful Web services and Java applications
License:        ASL 2.0 and CDDL
URL:            http://resteasy.jboss.org/
Source0:        https://github.com/resteasy/Resteasy/archive/%{namedversion}/%{name}-%{namedversion}.tar.gz
Patch1:         0001-RESTEASY-2559-Improper-validation-of-response-header.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(com.sun.xml.bind:jaxb-impl)
BuildRequires:  mvn(log4j:log4j)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.apache.tomcat:tomcat-servlet-api)

# Jackson 2
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:  mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-json-provider)

BuildRequires:  mvn(org.jboss:jboss-parent:pom:)
BuildRequires:  mvn(org.jboss.logging:jboss-logging)
BuildRequires:  mvn(org.jboss.logging:jboss-logging-annotations)
BuildRequires:  mvn(org.jboss.logging:jboss-logging-processor)
BuildRequires:  mvn(org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec)
BuildRequires:  mvn(org.jboss.spec.javax.ws.rs:jboss-jaxrs-api_2.0_spec)
BuildRequires:  mvn(org.slf4j:slf4j-api)

Requires:       resteasy-atom-provider     = %{version}-%{release}
Requires:       resteasy-client            = %{version}-%{release}
Requires:       resteasy-core              = %{version}-%{release}
Requires:       resteasy-jackson2-provider = %{version}-%{release}
Requires:       resteasy-jaxb-provider     = %{version}-%{release}

# subpackages removed in fedora 32
Obsoletes:      %{name}-fastinfoset-provider < 3.0.26-1
Obsoletes:      %{name}-jackson-provider < 3.0.26-1
Obsoletes:      %{name}-jettison-provider < 3.0.26-1
Obsoletes:      %{name}-json-p-provider < 3.0.26-1
Obsoletes:      %{name}-multipart-provider < 3.0.26-1
Obsoletes:      %{name}-netty3 < 3.0.26-1
Obsoletes:      %{name}-optional < 3.0.26-1
Obsoletes:      %{name}-test < 3.0.26-1
Obsoletes:      %{name}-validator-provider-11 < 3.0.26-1
Obsoletes:      %{name}-yaml-provider < 3.0.26-1

%description
%global desc \
RESTEasy contains a JBoss project that provides frameworks to help\
build RESTful Web Services and RESTful Java applications. It is a fully\
certified and portable implementation of the JAX-RS specification.
%{desc}
%global extdesc %{desc}\
\
This package contains

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
This package contains the API documentation for %{name}.

%package        core
Summary:        Core modules for %{name}
Obsoletes:      resteasy-jaxrs-api < 3.0.7

Provides:       %{name}-jaxrs         = %{version}-%{release}
Provides:       %{name}-jaxrs-all     = %{version}-%{release}
Provides:       %{name}-providers-pom = %{version}-%{release}
Provides:       %{name}-resteasy-pom  = %{version}-%{release}

%description    core
%{extdesc} %{summary}.

%package        atom-provider
Summary:        Module atom-provider for %{name}

%description    atom-provider
%{extdesc} %{summary}.

%package        jackson2-provider
Summary:        Module jackson2-provider for %{name}

%description    jackson2-provider
%{extdesc} %{summary}.

%package        jaxb-provider
Summary:        Module jaxb-provider for %{name}

%description    jaxb-provider
%{extdesc} %{summary}.

%package        client
Summary:        Client for %{name}

%description    client
%{extdesc} %{summary}.

%prep
%setup -q -n Resteasy-%{namedversion}
%patch1 -p1

%pom_disable_module arquillian
%pom_disable_module eagledns
%pom_disable_module jboss-modules
%pom_disable_module profiling-tests
%pom_disable_module resteasy-bom
%pom_disable_module resteasy-cache
%pom_disable_module resteasy-cdi
%pom_disable_module resteasy-dependencies-bom
%pom_disable_module resteasy-guice
%pom_disable_module resteasy-jaxrs-testsuite
%pom_disable_module resteasy-jsapi
%pom_disable_module resteasy-jsapi-testing
%pom_disable_module resteasy-links
%pom_disable_module resteasy-servlet-initializer
%pom_disable_module resteasy-spring
%pom_disable_module resteasy-wadl
%pom_disable_module resteasy-wadl-undertow-connector
%pom_disable_module security
%pom_disable_module server-adapters
%pom_disable_module testsuite
%pom_disable_module tjws

pushd providers
%pom_disable_module fastinfoset
%pom_disable_module jackson
%pom_disable_module jettison
%pom_disable_module json-p-ee7
%pom_disable_module multipart
%pom_disable_module resteasy-html
%pom_disable_module resteasy-validator-provider-11
%pom_disable_module yaml
popd

find -name '*.jar' -print -delete

%pom_remove_plugin :maven-clover2-plugin

# remove activation.jar dependencies
%pom_remove_dep -r javax.activation:activation resteasy-jaxrs resteasy-spring

# remove resteasy-dependencies pom
%pom_remove_dep "org.jboss.resteasy:resteasy-dependencies"

# remove redundant jcip-dependencies dep from resteasy-jaxrs
%pom_remove_dep net.jcip:jcip-annotations resteasy-jaxrs

# remove junit dependency from all modules
%pom_remove_dep junit:junit resteasy-client
%pom_remove_dep junit:junit providers/resteasy-atom
%pom_remove_dep junit:junit providers/jaxb
%pom_remove_dep junit:junit resteasy-jaxrs

# depend on servlet-api from pki-servlet-4.0-api
%pom_change_dep org.jboss.spec.javax.servlet: org.apache.tomcat:tomcat-servlet-api resteasy-jaxrs
%pom_change_dep org.jboss.spec.javax.servlet: org.apache.tomcat:tomcat-servlet-api providers/abdera-atom
%pom_change_dep org.jboss.spec.javax.servlet: org.apache.tomcat:tomcat-servlet-api providers/jaxb
%pom_change_dep org.jboss.spec.javax.servlet: org.apache.tomcat:tomcat-servlet-api providers/jackson2

%pom_remove_plugin :maven-clean-plugin

%mvn_package ":resteasy-jaxrs" core
%mvn_package ":providers-pom" core
%mvn_package ":resteasy-jaxrs-all" core
%mvn_package ":resteasy-pom" core
%mvn_package ":resteasy-atom-provider" atom-provider
%mvn_package ":resteasy-jackson2-provider" jackson2-provider
%mvn_package ":resteasy-jaxb-provider" jaxb-provider
%mvn_package ":resteasy-client" client

# Fixing JDK7 ASCII issues
files='
resteasy-jaxrs/src/main/java/org/jboss/resteasy/annotations/Query.java
resteasy-jaxrs/src/main/java/org/jboss/resteasy/core/QueryInjector.java
resteasy-jsapi/src/main/java/org/jboss/resteasy/jsapi/JSAPIWriter.java
resteasy-jsapi/src/main/java/org/jboss/resteasy/jsapi/JSAPIServlet.java
resteasy-jsapi/src/main/java/org/jboss/resteasy/jsapi/ServiceRegistry.java
resteasy-links/src/main/java/org/jboss/resteasy/links/AddLinks.java
resteasy-links/src/main/java/org/jboss/resteasy/links/ELProvider.java
resteasy-links/src/main/java/org/jboss/resteasy/links/LinkELProvider.java
resteasy-links/src/main/java/org/jboss/resteasy/links/LinkResource.java
resteasy-links/src/main/java/org/jboss/resteasy/links/LinkResources.java
resteasy-links/src/main/java/org/jboss/resteasy/links/ParentResource.java
resteasy-links/src/main/java/org/jboss/resteasy/links/RESTServiceDiscovery.java
resteasy-links/src/main/java/org/jboss/resteasy/links/ResourceFacade.java
resteasy-links/src/main/java/org/jboss/resteasy/links/ResourceID.java
resteasy-links/src/main/java/org/jboss/resteasy/links/ResourceIDs.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthConsumer.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthException.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthFilter.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthMemoryProvider.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthProvider.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthProviderChecker.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthRequestToken.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthServlet.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthToken.java
security/resteasy-oauth/src/main/java/org/jboss/resteasy/auth/oauth/OAuthValidator.java
'

for f in ${files}; do
native2ascii -encoding UTF8 ${f} ${f}
done

# Disable useless artifacts generation, package __noinstall do not work
%pom_add_plugin org.apache.maven.plugins:maven-source-plugin . '
<configuration>
 <skipSource>true</skipSource>
</configuration>'

%build
%mvn_build -f

%install
%mvn_install

%files
%doc README.md
%license License.html

%files core -f .mfiles-core
%license License.html

%files atom-provider -f .mfiles-atom-provider
%license License.html

%files jackson2-provider -f .mfiles-jackson2-provider
%license License.html

%files jaxb-provider -f .mfiles-jaxb-provider
%license License.html

%files client -f .mfiles-client
%license License.html

%files javadoc -f .mfiles-javadoc
%license License.html

%changelog
* Fri Aug 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.26-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Adding following 'Provides' to '*-core' subpackage for compatibility reasons:
  - resteasy-jaxrs;
  - resteasy-jaxrs-all;
  - resteasy-providers-pom;
  - resteasy-resteasy-pom.

* Mon Nov 30 2020 Alexander Scheel <ascheel@redhat.com> - 3.0.26-6
- CVE-2020-1695: Improper validation of response header in MediaTypeHeaderDelegate.java class
  Resolves: rh-bz#1845547

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Dogtag PKI Team <pki-devel@redhat.com> 3.0.26-1
- Update to version 3.0.26.
- Build with reduced functionality and dependency set.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.19-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 27 2016 gil cattaneo <puntogil@libero.it> 3.0.19-4
- build fix for netty 3.10.6.Final

* Tue Sep 13 2016 gil cattaneo <puntogil@libero.it> 3.0.19-3
- re-introduce jandex jars

* Mon Aug 22 2016 gil cattaneo <puntogil@libero.it> 3.0.19-2
- move "Obsoletes" to resteasy-core

* Sun Aug 21 2016 gil cattaneo <puntogil@libero.it> 3.0.19-1
- update to 3.0.19.Final

* Fri Aug 12 2016 gil cattaneo <puntogil@libero.it> 3.0.17-2
- add sub package netty3

* Mon Jun 06 2016 gil cattaneo <puntogil@libero.it> 3.0.17-1
- update to 3.0.17.Final
- introduce license macro
- enable resteasy-links, resteasy-oauth, resteasy-wadl modules
- build resteasy-netty{3,4}

* Mon Feb 22 2016 Mat Booth <mat.booth@redhat.com> - 3.0.6-11
- Fix failure to build from source

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 27 2015 Ade Lee <alee@redhat.com> - 3.0.6-9
- Remove activation.jar dependency to fix build.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 5 2014 Ade Lee <alee@redhat.com> - 3.0.6-7
- Refactor into subpackages.
- Change build requires to mvn() format

* Mon Sep 29 2014 Ade Lee <alee@eredhat.com> - 3.0.6-6
- Add fix for CVE-2014-3490

* Tue Jun 24 2014 Ade Lee <alee@redhat.com> - 3.0.6-5
- Replace broken dependencies junit4-> junit
- Add patch to handle new bouncycastle API in version 1.50
- Fix bogus dates in changelog

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 3.0.6-3
- Use Requires: java-headless rebuild (#1067528)

* Tue Jan 14 2014 Marek Goldmann <mgoldman@redhat.com> - 3.0.6-2
- Support for Netty 4 in Rawhide

* Fri Jan 10 2014 Marek Goldmann <mgoldman@redhat.com> - 3.0.6-1
- Upstream release 3.0.6.Final

* Fri Aug 09 2013 Marek Goldmann <mgoldman@redhat.com> - 3.0.1-3
- Remove versioning from the jandex files

* Fri Aug 09 2013 Marek Goldmann <mgoldman@redhat.com> - 3.0.1-2
- Added jandex index files to all jars

* Fri Aug 09 2013 Marek Goldmann <mgoldman@redhat.com> - 3.0.1-1
- Upstream release 3.0.1.Final
- Using xmvn

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 9 2013 Ade Lee <alee@redhat.com> 2.3.2-13
- Removed dependency on maven-checkstyle-plugin

* Tue Apr 2 2013 Endi S. Dewata <edewata@redhat.com> - 2.3.2-12
- Removed Tomcat 6 dependency

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.3.2-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Aug 7 2012 Ade Lee <alee@redhat.com> - 2.3.2-9
- Added tomcat6-servlet-2.5-api as a dependency

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Marek Goldmann <mgoldman@redhat.com> 2.3.2-7
- Create also the jandex index jar files

* Tue Apr 24 2012 Marek Goldmann <mgoldman@redhat.com> 2.3.2-6
- Added resteasy-multipart-provider module

* Mon Apr 23 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.3.2-5
- Fix the async HTTP Servlet 3.0 artifact id

* Mon Apr 23 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.3.2-4
- Added an additional artifact and group id for jaxrs-api

* Mon Apr 23 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.3.2-3
- Added async HTTP Servlet 3.0 module

* Thu Apr 12 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.3.2-2
- Build CDI integration module (bug #812978)

* Tue Mar 6 2012 Ade Lee <alee@redhat.com> 2.3.2-1
- Initial packaging
