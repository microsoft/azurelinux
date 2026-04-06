# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global namedreltag .Final
%global namedversion %{version}%{namedreltag}

Name:           resteasy
Version:        3.0.26
Release:        36%{?dist}
Summary:        Framework for RESTful Web services and Java applications
License:        Apache-2.0
URL:            http://resteasy.jboss.org/
Source0:        https://github.com/resteasy/Resteasy/archive/%{namedversion}/%{name}-%{namedversion}.tar.gz
Patch1:         0001-RESTEASY-2559-Improper-validation-of-response-header.patch
Patch2:         0001-Remove-Log4jLogger.patch
Patch3:         0001-Replace-javax.activation-imports-with-jakarta.activa.patch
Patch4:         0001-Update-to-new-jakarta-xml-bind-namespace.patch
Patch5:         rest-easy-jakarta.patch

BuildArch:      noarch
%if 0%{?fedora}
ExclusiveArch:  %{java_arches} noarch
%endif

BuildRequires:  tomcat-servlet-6.0-api
BuildRequires:  tomcat-jakartaee-migration

BuildRequires:  maven-local-openjdk21
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(jakarta.xml.bind:jakarta.xml.bind-api)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)


# Jackson 2
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:  mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-json-provider)

BuildRequires:  mvn(org.jboss:jboss-parent:pom:)
BuildRequires:  mvn(org.jboss.logging:jboss-logging)
BuildRequires:  mvn(org.jboss.logging:jboss-logging-annotations)
BuildRequires:  mvn(org.jboss.logging:jboss-logging-processor)
BuildRequires:  mvn(javax.annotation:javax.annotation-api)
BuildRequires:  mvn(org.jboss.spec.javax.ws.rs:jboss-jaxrs-api_2.0_spec)
BuildRequires:  mvn(org.slf4j:slf4j-api)

%description
%global desc \
RESTEasy contains a JBoss project that provides frameworks to help\
build RESTful Web Services and RESTful Java applications. It is a fully\
certified and portable implementation of the JAX-RS specification.
%{desc}
%global extdesc %{desc}\
\
This package contains

%package -n     pki-%{name}
Summary:        Framework for RESTful Web services and Java applications
Obsoletes:      %{name} < %{version}-%{release}
Conflicts:      %{name} < %{version}-%{release}
Provides:       %{name} = %{version}-%{release}

Requires:       pki-%{name}-client              = %{version}-%{release}
Requires:       pki-%{name}-core                = %{version}-%{release}
Requires:       pki-%{name}-jackson2-provider   = %{version}-%{release}
Requires:       pki-%{name}-servlet-initializer = %{version}-%{release}

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

%description -n pki-%{name}
%{desc}

%package -n     pki-%{name}-core
Summary:        Core modules for %{name}
Obsoletes:      resteasy-jaxrs-api < 3.0.7
Obsoletes:      %{name}-core < %{version}-%{release}
Conflicts:      %{name}-core < %{version}-%{release}
Provides:       %{name}-core = %{version}-%{release}

%description -n pki-%{name}-core
%{extdesc} %{summary}.

%package -n     pki-%{name}-jackson2-provider
Summary:        Module jackson2-provider for %{name}
Obsoletes:      %{name}-jackson2-provider < %{version}-%{release}
Conflicts:      %{name}-jackson2-provider < %{version}-%{release}
Provides:       %{name}-jackson2-provider = %{version}-%{release}

%description -n pki-%{name}-jackson2-provider
%{extdesc} %{summary}.

%package -n     pki-%{name}-client
Summary:        Client for %{name}
Obsoletes:      %{name}-client < %{version}-%{release}
Conflicts:      %{name}-client < %{version}-%{release}
Provides:       %{name}-client = %{version}-%{release}

%description -n pki-%{name}-client
%{extdesc} %{summary}.

%package -n     pki-%{name}-servlet-initializer
Summary:        %{name} Servlet Initializer
Obsoletes:      %{name}-servlet-initializer < %{version}-%{release}
Conflicts:      %{name}-servlet-initializer < %{version}-%{release}
Provides:       %{name}-servlet-initializer = %{version}-%{release}

%description -n pki-%{name}-servlet-initializer
%{extdesc} %{summary}.

%prep
%autosetup -n Resteasy-%{namedversion} -p 1

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
%pom_disable_module resteasy-atom
%pom_disable_module resteasy-html
%pom_disable_module resteasy-validator-provider-11
%pom_disable_module yaml
%pom_disable_module jaxb
popd

find -name '*.jar' -print -delete

%pom_remove_plugin :maven-clover2-plugin
%pom_remove_plugin :maven-javadoc-plugin

# depend on jakarta-activation
%pom_change_dep javax.activation:activation jakarta.activation:jakarta.activation-api:2.1.1 resteasy-jaxrs
%pom_change_dep javax.activation:activation jakarta.activation:jakarta.activation-api:2.1.1 resteasy-spring

# depend on jakarta-annotations
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api jboss-modules
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api providers/jaxb
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api resteasy-dependencies-bom
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api resteasy-guice
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api resteasy-jaxrs
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api resteasy-links
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api resteasy-spring
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api security/keystone/keystone-core
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api security/resteasy-crypto
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api security/skeleton-key-idm/skeleton-key-core
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api security/skeleton-key-idm/skeleton-key-idp
%pom_change_dep org.jboss.spec.javax.annotation:jboss-annotations-api_1.2_spec javax.annotation:javax.annotation-api server-adapters/resteasy-jdk-http

# remove resteasy-dependencies pom
%pom_remove_dep "org.jboss.resteasy:resteasy-dependencies"

# remove redundant jcip-dependencies dep from resteasy-jaxrs
%pom_remove_dep net.jcip:jcip-annotations resteasy-jaxrs

# remove junit dependency from all modules
%pom_remove_dep junit:junit resteasy-client
%pom_remove_dep junit:junit providers/resteasy-atom
%pom_remove_dep junit:junit providers/jaxb
%pom_remove_dep junit:junit resteasy-jaxrs
%pom_remove_dep junit:junit resteasy-servlet-initializer

# remove log4j dependency
%pom_remove_dep log4j:log4j resteasy-jaxrs

# depend on servlet-api from pki-servlet-4.0-api
%pom_change_dep org.jboss.spec.javax.servlet: org.apache.tomcat:tomcat-servlet-api resteasy-jaxrs
%pom_change_dep org.jboss.spec.javax.servlet: org.apache.tomcat:tomcat-servlet-api resteasy-servlet-initializer
%pom_change_dep org.jboss.spec.javax.servlet: org.apache.tomcat:tomcat-servlet-api providers/abdera-atom
%pom_change_dep org.jboss.spec.javax.servlet: org.apache.tomcat:tomcat-servlet-api providers/jaxb
%pom_change_dep org.jboss.spec.javax.servlet: org.apache.tomcat:tomcat-servlet-api providers/jackson2

# add dependencies for EE APIs that were removed in Java 11
%pom_add_dep jakarta.xml.bind:jakarta.xml.bind-api resteasy-jaxrs
%pom_add_dep jakarta.xml.bind:jakarta.xml.bind-api resteasy-servlet-initializer

%pom_remove_plugin :maven-clean-plugin

%mvn_package ":resteasy-jaxrs" core
%mvn_package ":providers-pom" core
%mvn_package ":resteasy-jaxrs-all" core
%mvn_package ":resteasy-pom" core
%mvn_package ":resteasy-jackson2-provider" jackson2-provider
%mvn_package ":resteasy-client" client
%mvn_package ":resteasy-servlet-initializer" servlet-initializer

# Disable useless artifacts generation, package __noinstall do not work
%pom_add_plugin org.apache.maven.plugins:maven-source-plugin . '
<configuration>
 <skipSource>true</skipSource>
</configuration>'

%build

%mvn_build -f -j -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install

%mvn_install

/usr/bin/javax2jakarta -logLevel=ALL -profile=EE %{buildroot}%{_datadir}/java/resteasy/%{name}-client.jar %{buildroot}%{_datadir}/java/resteasy/%{name}-client.jar
/usr/bin/javax2jakarta -logLevel=ALL -profile=EE %{buildroot}%{_datadir}/java/resteasy/%{name}-jackson2-provider.jar %{buildroot}%{_datadir}/java/resteasy/%{name}-jackson2-provider.jar
/usr/bin/javax2jakarta -logLevel=ALL -profile=EE %{buildroot}%{_datadir}/java/resteasy/%{name}-jaxrs.jar  %{buildroot}%{_datadir}/java/resteasy/%{name}-jaxrs.jar
/usr/bin/javax2jakarta -logLevel=ALL -profile=EE %{buildroot}%{_datadir}/java/resteasy/%{name}-servlet-initializer.jar %{buildroot}%{_datadir}/java/resteasy/%{name}-servlet-initializer.jar

%files -n pki-%{name}
%doc README.md
%license License.html

%files -n pki-%{name}-core -f .mfiles-core
%license License.html

%files -n pki-%{name}-jackson2-provider -f .mfiles-jackson2-provider
%license License.html

%files -n pki-%{name}-client -f .mfiles-client
%license License.html

%files -n pki-%{name}-servlet-initializer -f .mfiles-servlet-initializer
%license License.html

%changelog
* Wed Jul 30 2025 jiri vanek <jvanek@redhat.com> - 3.0.26-36
- Rrevert to jdk21

* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 3.0.26-35
- Rebuilt for java-25-openjdk as preffered jdk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Jack Magne <jmagne@redhat.com> - 3.0.26-33
- Rebuilt with support and migration  for tomcat10 and jarkarta ee.

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 3.0.26-30
- Rebuilt for java-21-openjdk as system jdk

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Dogtag PKI Team <devel@lists.dogtagpki.org> - 3.0.26-26
- Conditionalize use of ExclusiveArch

* Mon May 01 2023 Dogtag PKI Team <pki-devel@redhat.com> - 3.0.26-25
- Update top-level package to depend on servlet-initializer

* Mon May 01 2023 Dogtag PKI Team <pki-devel@redhat.com> - 3.0.26-24
- Enable servlet-initializer subpackage

* Fri Feb 03 2023 Chris Kelley <ckelley@redhat.com> - 3.0.26-23
- Remove dependency on jaxb-api2 compat package

* Fri Feb 03 2023 Chris Kelley <ckelley@redhat.com> - 3.0.26-22
- Remove dependency on jakarta-activation1 compat package

* Mon Jan 23 2023 Marian Koncek <mkoncek@redhat.com> - 3.0.26-21
- Depend on compat jaxb-api version 2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Marian Koncek <mkoncek@redhat.com> - 3.0.26-19
- Depend on compat jakarta.activation

* Tue Dec 20 2022 Marian Koncek <mkoncek@redhat.com> - 3.0.26-18
- Rebuild with compat jakarta.activation version 1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 3.0.26-16
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 3.0.26-15
- Rebuilt for java-17-openjdk as system jdk

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 30 2021 Dogtag PKI Team <pki-devel@redhat.com> - 3.0.26-13
- Drop pki-resteasy-jaxb-provider

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 18 2021 Dogtag PKI Team <pki-devel@redhat.com> - 3.0.26-11
- Replace jboss-annotations-1.2-api with jakarta-annotations

* Wed Jun  2 2021 Dogtag PKI Team <pki-devel@redhat.com> - 3.0.26-10
- Drop log4j dependency
- Add jakarta-activation dependency

* Wed May 19 2021 Dogtag PKI Team <pki-devel@redhat.com> - 3.0.26-9
- Drop pki-resteasy-javadoc and pki-resteasy-atom-provider

* Mon May 10 2021 Dogtag PKI Team <pki-devel@redhat.com> - 3.0.26-8
- Rename subpackages to pki-resteasy

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Alexander Scheel <ascheel@redhat.com> - 3.0.26-6
- CVE-2020-1695: Improper validation of response header in MediaTypeHeaderDelegate.java class
  Resolves: rh-bz#1845547

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Fabio Valentini <decathorpe@gmail.com> - 3.0.26-4
- Migrate away from native2ascii (removed with OpenJDK 11).
- Add missing dependencies for packages that were removed from OpenJDK 11.

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 3.0.26-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

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
