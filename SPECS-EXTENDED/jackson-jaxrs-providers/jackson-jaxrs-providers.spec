Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without  jp_minimal

Name:           jackson-jaxrs-providers
Version:        2.10.5
Release:        2%{?dist}
Summary:        Jackson JAX-RS providers
License:        ASL 2.0

URL:            https://github.com/FasterXML/jackson-jaxrs-providers
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson:jackson-base:pom:) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson.module:jackson-module-jaxb-annotations)
BuildRequires:  mvn(com.google.code.maven-replacer-plugin:replacer)
BuildRequires:  mvn(javax.ws.rs:javax.ws.rs-api)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%if %{without jp_minimal}
BuildRequires:  mvn(com.fasterxml.jackson.dataformat:jackson-dataformat-cbor)
BuildRequires:  mvn(com.fasterxml.jackson.dataformat:jackson-dataformat-smile)
BuildRequires:  mvn(com.fasterxml.jackson.dataformat:jackson-dataformat-xml)
BuildRequires:  mvn(com.fasterxml.jackson.dataformat:jackson-dataformat-yaml)
BuildRequires:  mvn(org.glassfish.jersey.containers:jersey-container-servlet)
BuildRequires:  mvn(org.glassfish.jersey.core:jersey-server)
BuildRequires:  mvn(org.jboss.resteasy:resteasy-jaxrs)
%endif

%if %{with jp_minimal}
Obsoletes:      jackson-jaxrs-cbor-provider < 2.10.0-1
Obsoletes:      jackson-jaxrs-smile-provider < 2.10.0-1
Obsoletes:      jackson-jaxrs-xml-provider < 2.10.0-1
Obsoletes:      jackson-jaxrs-yaml-provider < 2.10.0-1
%endif

%description
This is a multi-module project that contains Jackson-based JAX-RS providers for
following data formats: JSON, Smile (binary JSON), XML, CBOR (another kind of
binary JSON), YAML.

%package -n jackson-jaxrs-json-provider
Summary:       Jackson-JAXRS-JSON

%description -n jackson-jaxrs-json-provider
Functionality to handle JSON input/output for JAX-RS implementations
(like Jersey and RESTeasy) using standard Jackson data binding.

%if %{without jp_minimal}
%package -n jackson-jaxrs-cbor-provider
Summary:       Jackson-JAXRS-CBOR

%description -n jackson-jaxrs-cbor-provider
Functionality to handle CBOR encoded input/output for JAX-RS implementations
(like Jersey and RESTeasy) using standard Jackson data binding.

%package -n jackson-jaxrs-smile-provider
Summary:       Jackson-JAXRS-Smile

%description -n jackson-jaxrs-smile-provider
Functionality to handle Smile (binary JSON) input/output for
JAX-RS implementations (like Jersey and RESTeasy) using standard
Jackson data binding.

%package -n jackson-jaxrs-xml-provider
Summary:       Jackson-JAXRS-XML

%description -n jackson-jaxrs-xml-provider
Functionality to handle Smile XML input/output for JAX-RS implementations
(like Jersey and RESTeasy) using standard Jackson data binding.

%package -n jackson-jaxrs-yaml-provider
Summary:       Jackson-JAXRS-YAML

%description -n jackson-jaxrs-yaml-provider
Functionality to handle YAML input/output for JAX-RS implementations
(like Jersey and RESTeasy) using standard Jackson data binding.
%endif

%package datatypes
Summary: Functionality for reading/writing core JAX-RS helper types

%description datatypes
Functionality for reading/writing core JAX-RS helper types.

%package parent
Summary: Parent for Jackson JAX-RS providers

%description parent
Parent POM for Jackson JAX-RS providers.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
This package contains API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp -p xml/src/main/resources/META-INF/LICENSE .
cp -p xml/src/main/resources/META-INF/NOTICE .
sed -i 's/\r//' LICENSE NOTICE

%pom_remove_plugin -r :moditect-maven-plugin

# Disable jar with no-meta-inf-services classifier, breaks build
%pom_remove_plugin :maven-jar-plugin cbor
%pom_remove_plugin :maven-jar-plugin json
%pom_remove_plugin :maven-jar-plugin smile
%pom_remove_plugin :maven-jar-plugin xml
%pom_remove_plugin :maven-jar-plugin yaml
%pom_remove_plugin :maven-jar-plugin datatypes

# Add missing deps to fix java.lang.ClassNotFoundException during tests
%pom_add_dep com.google.guava:guava:18.0:test datatypes cbor json smile xml yaml
%pom_add_dep org.ow2.asm:asm:5.1:test cbor json smile xml yaml

# Circular dep?
%pom_remove_dep org.jboss.resteasy:resteasy-jackson2-provider json
rm json/src/test/java/com/fasterxml/jackson/jaxrs/json/resteasy/RestEasyProviderLoadingTest.java

%if %{with jp_minimal}
# Disable extra test deps
%pom_remove_dep org.glassfish.jersey.core:
%pom_remove_dep org.glassfish.jersey.containers:
# Disable extra providers
%pom_disable_module cbor
%pom_disable_module smile
%pom_disable_module xml
%pom_disable_module yaml
%endif

%build
%if %{with jp_minimal}
%mvn_build -s -f
%else
%mvn_build -s
%endif

%install
%mvn_install

%files -f .mfiles-jackson-jaxrs-base
%doc README.md release-notes/*
%license LICENSE NOTICE

%files -n jackson-jaxrs-json-provider -f .mfiles-jackson-jaxrs-json-provider
%if %{without jp_minimal}
%files -n jackson-jaxrs-cbor-provider -f .mfiles-jackson-jaxrs-cbor-provider
%files -n jackson-jaxrs-smile-provider -f .mfiles-jackson-jaxrs-smile-provider
%files -n jackson-jaxrs-xml-provider -f .mfiles-jackson-jaxrs-xml-provider
%files -n jackson-jaxrs-yaml-provider -f .mfiles-jackson-jaxrs-yaml-provider
%endif

%files datatypes -f .mfiles-jackson-datatype-jaxrs
%license LICENSE NOTICE

%files parent -f .mfiles-jackson-jaxrs-providers
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.10.5-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Jan 18 2021 Fabio Valentini <decathorpe@gmail.com> - 2.10.5-1
- Update to version 2.10.5.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Fabio Valentini <decathorpe@gmail.com> - 2.10.2-1
- Update to version 2.10.2.

* Wed Nov 13 2019 Fabio Valentini <decathorpe@gmail.com> - 2.10.1-1
- Update to version 2.10.1.

* Tue Nov 12 2019 Alexander Scheel <ascheel@redhat.com> - 2.10.0-2
- Minimize build dependencies.

* Sun Oct 27 2019 Fabio Valentini <decathorpe@gmail.com> - 2.10.0-1
- Update to version 2.10.0.
- Build with minimized dependencies.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 06 2019 Mat Booth <mat.booth@redhat.com> - 2.9.8-1
- Update to latest upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 07 2018 Mat Booth <mat.booth@redhat.com> - 2.9.4-4
- Allow conditional building of modules that have extra deps

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Mat Booth <mat.booth@redhat.com> - 2.9.4-1
- Update to latest upstream release

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 22 2016 gil cattaneo <puntogil@libero.it> 2.7.6-1
- update to 2.7.6

* Fri Jun 24 2016 gil cattaneo <puntogil@libero.it> 2.6.7-1
- update to 2.6.7

* Thu May 26 2016 gil cattaneo <puntogil@libero.it> 2.6.6-1
- update to 2.6.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 25 2015 gil cattaneo <puntogil@libero.it> 2.6.3-1
- update to 2.6.3

* Mon Sep 28 2015 gil cattaneo <puntogil@libero.it> 2.6.2-1
- update to 2.6.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 gil cattaneo <puntogil@libero.it> 2.5.0-1
- update to 2.5.0

* Sat Sep 20 2014 gil cattaneo <puntogil@libero.it> 2.4.2-1
- update to 2.4.2

* Wed Jul 09 2014 gil cattaneo <puntogil@libero.it> 2.4.1-2
- enable jackson-jaxrs-cbor-provider

* Fri Jul 04 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- update to 2.4.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.2-2
- Use Requires: java-headless rebuild (#1067528)

* Wed Jul 17 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- update to 2.2.2
- renamed jackson-jaxrs-providers

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 2.1.5-1
- update to 2.1.5

* Wed Oct 24 2012 gil cattaneo <puntogil@libero.it> 2.1.0-1
- update to 2.1.0
- renamed jackson2-jaxrs-json-provider

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.0.5-1
- initial rpm
