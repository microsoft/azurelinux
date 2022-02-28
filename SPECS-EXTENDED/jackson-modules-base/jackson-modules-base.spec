Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without     jp_minimal

Name:           jackson-modules-base
Version:        2.10.5
Release:        2%{?dist}
Summary:        Jackson modules: Base
License:        ASL 2.0

URL:            https://github.com/FasterXML/jackson-modules-base
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(cglib:cglib)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-annotations) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson:jackson-base:pom:) >= %{version}
BuildRequires:  mvn(com.google.code.maven-replacer-plugin:replacer)
BuildRequires:  mvn(com.google.inject:guice)
%if %{without jp_minimal}
BuildRequires:  mvn(com.thoughtworks.paranamer:paranamer)
%endif
# xmvn-builddep misses this one:
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(javax.xml.bind:jaxb-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.glassfish.jaxb:jaxb-runtime)
BuildRequires:  mvn(org.mockito:mockito-all)
BuildRequires:  mvn(org.osgi:osgi.core)
BuildRequires:  mvn(org.ow2.asm:asm)

BuildArch:      noarch

%description
Jackson "base" modules: modules that build directly on databind,
and are not data-type, data format, or JAX-RS provider modules.

%package -n jackson-module-afterburner
Summary: Jackson module that uses byte-code generation to further speed up data binding

%description -n jackson-module-afterburner
Module that will add dynamic bytecode generation for standard Jackson POJO
serializers and deserializers, eliminating majority of remaining data binding
overhead.

%package -n jackson-module-guice
Summary: Jackson module to make integration with Guice a bit easier

%description -n jackson-module-guice
This extension allows Jackson to delegate ObjectMapper creation and value
injection to Guice when handling data bindings.

%package -n jackson-module-jaxb-annotations
Summary: Support for using JAXB annotations as an alternative to "native" Jackson annotations

%description -n jackson-module-jaxb-annotations
This Jackson extension module provides support for using JAXB (javax.xml.bind)
annotations as an alternative to native Jackson annotations. It is most often
used to make it easier to reuse existing data beans that used with JAXB
framework to read and write XML.

%if %{without jp_minimal}
%package -n jackson-module-mrbean
Summary: Functionality for implementing interfaces and abstract types dynamically

%description -n jackson-module-mrbean
Mr Bean is an extension that implements support for "POJO type materialization"
ability for databinder to construct implementation classes for Java interfaces
and abstract classes, as part of deserialization.
%endif

%package -n jackson-module-osgi
Summary: Jackson module to inject OSGI services in deserialized beans

%description -n jackson-module-osgi
This module provides a way to inject OSGI services into deserialized objects.
Thanks to the JacksonInject annotations, the OsgiJacksonModule will search for
the required service in the OSGI service registry and injects it in the object
while deserializing.

%if %{without jp_minimal}
%package -n jackson-module-paranamer
Summary: Jackson module that uses Paranamer to introspect names of constructor params

%description -n jackson-module-paranamer
Module that uses Paranamer library to auto-detect names of Creator
(constructor, static factory method, annotated with @JsonCreator) methods.
%endif

%package javadoc
Summary: Javadoc for %{name}
# Obsoletes standalone jackson-module-jaxb-annotations since F28
Obsoletes: jackson-module-jaxb-annotations-javadoc < %{version}-%{release}
Provides:  jackson-module-jaxb-annotations-javadoc = %{version}-%{release}

%description javadoc
This package contains API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

# no need for Java 9 module stuff
%pom_remove_plugin -r :moditect-maven-plugin

# move to "old" glassfish-jaxb-api artifactId
%pom_change_dep -r jakarta.xml.bind:jakarta.xml.bind-api javax.xml.bind:jaxb-api

# Disable bundling of asm
%pom_remove_plugin ":maven-shade-plugin" afterburner mrbean paranamer
%pom_xpath_remove "pom:properties/pom:osgi.private" mrbean paranamer

sed -i 's/\r//' mrbean/src/main/resources/META-INF/{LICENSE,NOTICE}
cp -p mrbean/src/main/resources/META-INF/{LICENSE,NOTICE} .

# Fix OSGi dependency
%pom_change_dep org.osgi:org.osgi.core org.osgi:osgi.core osgi

# NoClassDefFoundError: net/sf/cglib/core/CodeGenerationException
%pom_add_dep cglib:cglib:3.2.4:test guice

%if %{with jp_minimal}
# Disable modules with additional deps
%pom_disable_module paranamer
%pom_disable_module mrbean
%endif

# Allow javax,activation to be optional
%pom_add_plugin "org.apache.felix:maven-bundle-plugin" jaxb "
<configuration>
  <instructions>
    <Import-Package>javax.activation;resolution:=optional,*</Import-Package>
  </instructions>
</configuration>"

# This test fails since mockito was upgraded to 2.x
rm osgi/src/test/java/com/fasterxml/jackson/module/osgi/InjectOsgiServiceTest.java

%mvn_file ":{*}" jackson-modules/@1

%build
%mvn_build -s

%install
%mvn_install

%files -f .mfiles-jackson-modules-base
%doc README.md release-notes
%license LICENSE NOTICE

%files -n jackson-module-afterburner -f .mfiles-jackson-module-afterburner
%doc afterburner/README.md afterburner/release-notes
%license LICENSE NOTICE

%files -n jackson-module-guice -f .mfiles-jackson-module-guice
%doc guice/README.md
%license LICENSE NOTICE

%files -n jackson-module-jaxb-annotations -f .mfiles-jackson-module-jaxb-annotations
%doc jaxb/README.md jaxb/release-notes
%license LICENSE NOTICE

%if %{without jp_minimal}
%files -n jackson-module-mrbean -f .mfiles-jackson-module-mrbean
%doc mrbean/README.md mrbean/release-notes
%license LICENSE NOTICE
%endif

%files -n jackson-module-osgi -f .mfiles-jackson-module-osgi
%doc osgi/README.md osgi/release-notes
%license LICENSE NOTICE

%if %{without jp_minimal}
%files -n jackson-module-paranamer -f .mfiles-jackson-module-paranamer
%doc paranamer/README.md paranamer/release-notes
%license LICENSE NOTICE
%endif

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Wed Aug 18 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.10.5-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Switched to build WITH 'jp_minimal'.

* Mon Jan 18 2021 Fabio Valentini <decathorpe@gmail.com> - 2.10.5-1
- Update to version 2.10.5.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Fabio Valentini <decathorpe@gmail.com> - 2.10.2-1
- Update to version 2.10.2.

* Wed Nov 13 2019 Fabio Valentini <decathorpe@gmail.com> - 2.10.1-1
- Update to version 2.10.1.

* Tue Oct 08 2019 Fabio Valentini <decathorpe@gmail.com> - 2.10.0-1
- Update to version 2.10.0.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 17 2019 Mat Booth <mat.booth@redhat.com> - 2.9.8-2
- Make the OSGi dep on javax.activation optional

* Wed Feb 06 2019 Mat Booth <mat.booth@redhat.com> - 2.9.8-1
- Update to latest upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Mat Booth <mat.booth@redhat.com> - 2.9.4-5
- Avoid running test that fails since Mockito 2.x

* Wed Aug 22 2018 Mat Booth <mat.booth@redhat.com> - 2.9.4-4
- Allow conditional building of some extra modules

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Mat Booth <mat.booth@redhat.com> - 2.9.4-1
- Update to latest upstream release

* Tue Jan 23 2018 Mat Booth <mat.booth@redhat.com> - 2.9.3-2
- Properly obsolete jackson-module-jaxb-annotations-javadoc package

* Tue Jan 23 2018 Mat Booth <mat.booth@redhat.com> - 2.9.3-1
- Update to latest upstream release
- Obsoletes standalone jaxb-annotations package now provided by this package

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 gil cattaneo <puntogil@libero.it> 2.7.6-2
- fix some rpmlint problems 

* Mon Aug 22 2016 gil cattaneo <puntogil@libero.it> 2.7.6-1
- initial rpm

