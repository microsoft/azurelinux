Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          glassfish-jax-rs-api
Version:       2.1.6
Release:       3%{?dist}
Summary:       JAX-RS API Specification (JSR 339)
License:       EPL-2.0 or GPLv2 with exceptions
URL:           https://github.com/eclipse-ee4j/jaxrs-api
Source0:       %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.glassfish.build:spec-version-maven-plugin)
BuildRequires:  mvn(org.mockito:mockito-core)

BuildArch:     noarch

%description
JAX-RS Java API for RESTful Web Services (JSR 339).

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains API documentation for %{name}.

%prep
%setup -q -n jaxrs-api-%{version}

# Plugins not needed for RPM builds
%pom_remove_plugin org.apache.maven.plugins:maven-jxr-plugin jaxrs-api
%pom_remove_plugin org.apache.maven.plugins:maven-checkstyle-plugin jaxrs-api
%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin jaxrs-api
%pom_remove_plugin org.apache.maven.plugins:maven-source-plugin jaxrs-api
%pom_remove_plugin org.apache.maven.plugins:maven-deploy-plugin jaxrs-api

%pom_xpath_remove "pom:build/pom:finalName" jaxrs-api

# Avoid duplicate invokation of javadoc plugin
%pom_xpath_remove "pom:plugin[pom:artifactId = 'maven-javadoc-plugin' ]/pom:executions" jaxrs-api

%build
(
cd jaxrs-api
# Compatibility symlink
%mvn_file :{*} @1 %{name}

# Compatibility alias
%mvn_alias : javax.ws.rs:javax.ws.rs-api

%mvn_build
)

%install
(
cd jaxrs-api
%mvn_install
)

%files -f jaxrs-api/.mfiles
%license LICENSE.md NOTICE.md
%doc README.md CONTRIBUTING.md

%files javadoc -f jaxrs-api/.mfiles-javadoc
%license LICENSE.md NOTICE.md

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.6-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 19 2019 Fabio Valentini <decathorpe@gmail.com> - 2.1.6-1
- Update to version 2.1.6.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Mat Booth <mat.booth@redhat.com> - 2.1.5-3
- Fix duplicate javadoc execution

* Wed Mar 06 2019 Mat Booth <mat.booth@redhat.com> - 2.1.5-2
- Fix compatibility symlink and alias

* Wed Mar 06 2019 Mat Booth <mat.booth@redhat.com> - 2.1.5-1
- Update to latest upstream release
- Project moved to Eclipse EE4j project

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 08 2015 gil cattaneo <puntogil@libero.it> 2.0.1-1
- update to 2.0.1

* Tue Feb 03 2015 gil cattaneo <puntogil@libero.it> 2.0-7
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.0-5
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 gil cattaneo <puntogil@libero.it> 2.0-3
- switch to XMvn
- minor changes to adapt to current guideline

* Sun May 26 2013 gil cattaneo <puntogil@libero.it> 2.0-2
- rebuilt with spec-version-maven-plugin support

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.0-1
- update to 2.0

* Tue Mar 26 2013 gil cattaneo <puntogil@libero.it> 2.0-0.1.m16
- initial rpm
