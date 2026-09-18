# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without  jp_minimal

Name:           jackson-jaxrs-providers
Version:        2.18.2
Release:        4%{?dist}
Summary:        Jackson JAX-RS providers
License:        Apache-2.0

URL:            https://github.com/FasterXML/jackson-jaxrs-providers
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

BuildArch:      noarch
%if 0%{?fedora} || 0%{?rhel} >= 10
ExclusiveArch:  %{java_arches} noarch
%endif

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson.module:jackson-module-jaxb-annotations) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson:jackson-base:pom:) >= %{version}
BuildRequires:  mvn(com.google.code.maven-replacer-plugin:replacer)
BuildRequires:  mvn(org.jboss.spec.javax.ws.rs:jboss-jaxrs-api_2.0_spec)
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
%pom_remove_plugin "de.jjohannes:gradle-module-metadata-maven-plugin"

# Disable jar with no-meta-inf-services classifier, breaks build
%pom_remove_plugin :maven-jar-plugin cbor
%pom_remove_plugin :maven-jar-plugin json
%pom_remove_plugin :maven-jar-plugin smile
%pom_remove_plugin :maven-jar-plugin xml
%pom_remove_plugin :maven-jar-plugin yaml
%pom_remove_plugin :maven-jar-plugin datatypes

# Replace jakarta-ws-rs with jboss-jaxrs-2.0-api
%pom_change_dep javax.ws.rs:javax.ws.rs-api org.jboss.spec.javax.ws.rs:jboss-jaxrs-api_2.0_spec

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
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2.18.2-4
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 28 2024 Packit <hello@packit.dev> - 2.18.2-1
- Update to version 2.18.2
- Resolves: rhbz#2315080

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Packit <hello@packit.dev> - 2.17.2-1
- Update to version 2.17.2
- Resolves: rhbz#2296023

* Sun May 05 2024 Packit <hello@packit.dev> - 2.17.1-1
- Update to version 2.17.1
- Resolves: rhbz#2279129

* Wed Mar 13 2024 Packit <hello@packit.dev> - 2.17.0-1
- [maven-release-plugin] prepare release jackson-jaxrs-providers-2.17.0 (Tatu Saloranta)
- Prepare for 2.17.0 release (Tatu Saloranta)
- Back to snapshot dep (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Back to snapshot dep (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- [maven-release-plugin] prepare release jackson-jaxrs-providers-2.17.0-rc1 (Tatu Saloranta)
- Prepare for 2.17.0-rc1 (Tatu Saloranta)
- Update Woodstox version (Tatu Saloranta)
- Prepare for 2.17.0-rc1 (Tatu Saloranta)
- Woodstox dep update (Tatu Saloranta)
- Enable JDK 21 for CI (Tatu Saloranta)
- Post-merge cleanup for 2.17 wrt #178 (Tatu Saloranta)
- Start 2.17 branch (Tatu Saloranta)
- Resolves rhbz#2269296

* Sat Mar 09 2024 Packit <hello@packit.dev> - 2.16.2-1
- [maven-release-plugin] prepare release jackson-jaxrs-providers-2.16.2 (Tatu Saloranta)
- Prepare for 2.16.2 release (Tatu Saloranta)
- Resolves rhbz#2268713

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.16.1-3
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Marco Fargetta <mfargett@redhat.com> - 2.16.1-1
- [maven-release-plugin] prepare release jackson-jaxrs-providers-2.16.1 (Tatu Saloranta)
- Prepare for 2.16.1 release (Tatu Saloranta)
- Fix #178: replace LRUMap with one from jackson-databind (#179) (Tatu Saloranta)
- Back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 16 2023 Packit <hello@packit.dev> - 2.16.0-1
- [maven-release-plugin] prepare release jackson-jaxrs-providers-2.16.0 (Tatu Saloranta)
- Prepare for 2.16.0 release (Tatu Saloranta)
- Back to snapshot dep (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Resolves rhbz#2249955

* Mon Nov 06 2023 Chris Kelley <ckelley@redhat.com> - 2.15.3-1
- [maven-release-plugin] prepare release jackson-jaxrs-providers-2.15.3 (Tatu Saloranta)
- Prepare for 2.15.3 release (Tatu Saloranta)
- 2.15.3-SNAPSHOT (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Chris Kelley <ckelley@redhat.com> - 2.15.2-1
- Update to version 2.15.2

* Tue Jan 31 2023 Chris Kelley <ckelley@redhat.com> - 2.14.2-1
- Update to version 2.14.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Chris Kelley <ckelley@redhat.com> - 2.14.1-1
- Update to version 2.14.1

* Tue Nov 08 2022 Chris Kelley <ckelley@redhat.com> - 2.14.0-1
- Update to version 2.14

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.11.4-7
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.11.4-6
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun  2 2021 Dogtag PKI Team <pki-devel@redhat.com> - 2.11.4-3
- Replace jakarta-ws-rs with jboss-jaxrs-2.0-api

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Fabio Valentini <decathorpe@gmail.com> - 2.11.4-1
- Update to version 2.11.4.

* Wed Oct 14 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.3-1
- Update to version 2.11.3.

* Sat Aug 08 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.2-1
- Update to version 2.11.2.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.11.1-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Jul 06 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.1-1
- Update to version 2.11.1.

* Mon May 25 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.0-1
- Update to version 2.11.0.

* Fri May 08 2020 Fabio Valentini <decathorpe@gmail.com> - 2.10.4-1
- Update to version 2.10.4.

* Tue Mar 03 2020 Fabio Valentini <decathorpe@gmail.com> - 2.10.3-1
- Update to version 2.10.3.

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
