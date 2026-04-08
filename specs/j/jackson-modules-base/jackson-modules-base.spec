# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with     jp_minimal

Name:           jackson-modules-base
Version:        2.18.2
Release:        4%{?dist}
Summary:        Jackson modules: Base
License:        Apache-2.0

URL:            https://github.com/FasterXML/jackson-modules-base
Source0:        %{url}/archive/%{name}-%{version}-take-2.tar.gz
Patch1:         0001-Expose-javax.security.auth-from-JDK-internals.patch
Patch2:         0001-Replace-javax.activation-imports-with-jakarta.activa.patch
Patch3:         0001-Use-jakarta.activation-namespace-in-jaxb-api.patch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(cglib:cglib)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-annotations) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson:jackson-base:pom:) >= %{version}
BuildRequires:  mvn(com.google.code.maven-replacer-plugin:replacer)
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(jakarta.xml.bind:jakarta.xml.bind-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.mockito:mockito-all)
BuildRequires:  mvn(org.ow2.asm:asm)

BuildArch:      noarch
%if 0%{?fedora} || 0%{?rhel} >= 10
ExclusiveArch:  %{java_arches} noarch
%endif

%description
Jackson "base" modules: modules that build directly on databind,
and are not data-type, data format, or JAX-RS provider modules.

%package -n jackson-module-jaxb-annotations
Summary: Support for using JAXB annotations as an alternative to "native" Jackson annotations

%description -n jackson-module-jaxb-annotations
This Jackson extension module provides support for using JAXB (javax.xml.bind)
annotations as an alternative to native Jackson annotations. It is most often
used to make it easier to reuse existing data beans that used with JAXB
framework to read and write XML.

%prep
%autosetup -n %{name}-%{name}-%{version} -p 1

%pom_remove_dep -r org.glassfish.jaxb:jaxb-runtime
%pom_remove_plugin "de.jjohannes:gradle-module-metadata-maven-plugin"

# no need for Java 9 module stuff
%pom_remove_plugin -r :moditect-maven-plugin

# Disable bundling of asm
%pom_remove_plugin ":maven-shade-plugin" afterburner mrbean paranamer

sed -i 's/\r//' mrbean/src/main/resources/META-INF/{LICENSE,NOTICE}
cp -p mrbean/src/main/resources/META-INF/{LICENSE,NOTICE} .

# Fix OSGi dependency
%pom_change_dep org.osgi:org.osgi.core org.osgi:osgi.core osgi

# NoClassDefFoundError: net/sf/cglib/core/CodeGenerationException
%pom_add_dep cglib:cglib:3.2.4:test guice

%pom_disable_module afterburner
%pom_disable_module android-record
%pom_disable_module guice
%pom_disable_module guice7
%pom_disable_module mrbean
%pom_disable_module osgi
%pom_disable_module paranamer
%pom_disable_module jakarta-xmlbind
%pom_disable_module blackbird
%pom_disable_module no-ctor-deser

# Allow javax,activation to be optional
%pom_add_plugin "org.apache.felix:maven-bundle-plugin" jaxb "
<configuration>
  <instructions>
    <Import-Package>javax.activation;resolution:=optional,*</Import-Package>
  </instructions>
</configuration>"

# Revert jaxb annotation dependency to 2.17 mode
%pom_remove_dep javax.xml.bind:jaxb-api jaxb
%pom_add_dep jakarta.xml.bind:jakarta.xml.bind-api jaxb

# This test fails since mockito was upgraded to 2.x
rm osgi/src/test/java/com/fasterxml/jackson/module/osgi/InjectOsgiServiceTest.java

%mvn_file ":{*}" jackson-modules/@1

%build
%mvn_build -s -j

%install
%mvn_install

%files -f .mfiles-jackson-modules-base
%doc README.md release-notes
%license LICENSE NOTICE

%files -n jackson-module-jaxb-annotations -f .mfiles-jackson-module-jaxb-annotations
%doc jaxb/README.md jaxb/release-notes
%license LICENSE NOTICE

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2.18.2-4
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Packit <hello@packit.dev> - 2.18.2-1
- Update to version 2.18.2
- Resolves: rhbz#2315071

* Fri Nov 01 2024 Packit <hello@packit.dev> - 2.18.1-1
- Update to version 2.18.1
- Resolves: rhbz#2315071

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Packit <hello@packit.dev> - 2.17.2-1
- Update to version 2.17.2
- Resolves: rhbz#2296005

* Sun May 05 2024 Packit <hello@packit.dev> - 2.17.1-1
- Update to version 2.17.1
- Resolves: rhbz#2279128

* Tue Mar 12 2024 Packit <hello@packit.dev> - 2.17.0-1
- [maven-release-plugin] prepare release jackson-modules-base-2.17.0 (Tatu Saloranta)
- Prepare for 2.17.0 release (Tatu Saloranta)
- Back to snapshot dep (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Back to snapshot dep (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- [maven-release-plugin] prepare release jackson-modules-base-2.17.0-rc1 (Tatu Saloranta)
- Prepare for 2.17.0-rc1 (Tatu Saloranta)
- Prepare for 2.17.0-rc1 (Tatu Saloranta)
- Test refactoring (Tatu Saloranta)
- Add tests relating to aspects of #195 (verify @XmlSeeAlso handling wrt subtype deps) (Tatu Saloranta)
- update 2.17 version too (Tatu Saloranta)
- Start 2.17 branch (Tatu Saloranta)
- Resolves rhbz#2269276

* Sat Mar 09 2024 Packit <hello@packit.dev> - 2.16.2-1
- [maven-release-plugin] prepare release jackson-modules-base-2.16.2 (Tatu Saloranta)
- Prepare for 2.16.2 release (Tatu Saloranta)
- Resolves rhbz#2268714

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.16.1-3
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Marco Fargetta <mfargett@redhat.com> - 2.16.1-1
- [maven-release-plugin] prepare release jackson-modules-base-2.16.1 (Tatu Saloranta)
- Prepare for 2.16.1 release (Tatu Saloranta)
- Fix #231: change OSGi dep of "activation" package to jakarta (from javax) (Tatu Saloranta)
- Back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 16 2023 Packit <hello@packit.dev> - 2.16.0-1
- [maven-release-plugin] prepare release jackson-modules-base-2.16.0 (Tatu Saloranta)
- Prepare for 2.16.0 release (Tatu Saloranta)
- Updated doc. Added missing test accessor. (eranl)
- Minor test improvement to android module (Tatu Saloranta)
- Update release notes wrt #227 (Tatu Saloranta)
- Updated doc. Moved failing tests to 'failing' package. Added test for differing generic parameter types. Pruned BaseTest and BaseMapTest. Added comment about '-parameters' compiler option. (eranl)
- Addressed review comments With the goal of maximizing consistency with built-in record support, I copied and "desugared" some unit tests from https://github.com/FasterXML/jackson-databind/tree/2.16/src/test-jdk17/java/com/fasterxml/jackson/databind/records. A few of the test cases are failing, and I marked them with a "Failing" comment and a "notest" name prefix. I'm hoping for guidance about whether and how I should fix them. Fixed handling of getters Added support for injected values Added use of constructor parameter names Skip module if class already has a withArgsCreator (eranl)
- Add jackson-core dependency, animal-sniffer-maven-plugin, per review comments (eranl)
- Add Android Record Module (eranl)
- Move now passing #223 test to non-failing package (Tatu Saloranta)
- Fix #223: apply check for default (interface) method in all applicable places (Tatu Saloranta)
- Add test for #223: passes for Blackbird, fails for Afterburner (Tatu Saloranta)
- Test #30 simplification for blackbird too (Tatu Saloranta)
- Simplify test for #30 since Java 8 baseline for Jackson 2.x (Tatu Saloranta)
- Remove maven-wrapper.jar (Tatu Saloranta)
- Back to snapshot dep (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Resolves rhbz#2249935

* Mon Nov 06 2023 Chris Kelley <ckelley@redhat.com> - 2.15.3-1
- [maven-release-plugin] prepare release jackson-modules-base-2.15.3 (Tatu Saloranta)
- Prepare for 2.15.3 release (Tatu Saloranta)
- Udpate Maven wrapper version (Tatu Saloranta)
- 2.15.3-SNAPSHOT (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Chris Kelley <ckelley@redhat.com> - 2.15.2-1
- Update to version 2.15.2

* Fri Feb 03 2023 Chris Kelley <ckelley@redhat.com> - 2.14.2-3
- Remove dependency on jaxb-api2 compat package

* Fri Feb 03 2023 Chris Kelley <ckelley@redhat.com> - 2.14.2-2
- Remove dependency on jakarta-activation1 compat package

* Tue Jan 31 2023 Chris Kelley <ckelley@redhat.com> - 2.14.2-1
- Update to version 2.14.2

* Fri Jan 20 2023 Marian Koncek <mkoncek@redhat.com> - 2.14.1-4
- Depend on compat versions of activation and XML bind

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Marian Koncek <mkoncek@redhat.com> - 2.14.1-2
- Rebuild with compat jakarta.activation version 1

* Wed Nov 23 2022 Chris Kelley <ckelley@redhat.com> - 2.14.1-1
- Update to version 2.14.1

* Tue Nov 08 2022 Chris Kelley <ckelley@redhat.com> - 2.14.0-1
- Update to version 2.14
- Update to use SPDX licence

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.11.4-8
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.11.4-7
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 22 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 2.11.4-5
- Drop jaxb-runtime dependency

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 2.11.4-3
- Drop jackson-module-afterburner, jackson-module-guice, jackson-module-mrbean,
  jackson-module-osgi, jackson-module-paranamer, and jackson-module-javadoc

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

