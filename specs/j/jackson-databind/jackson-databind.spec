# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           jackson-databind
Version:        2.18.2
Release: 5%{?dist}
Summary:        General data-binding package for Jackson (2.x)
License:        Apache-2.0 and LGPL-2.0-or-later

URL:            https://github.com/FasterXML/jackson-databind
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-annotations) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core) >= %{version}
BuildRequires:  mvn(com.fasterxml.jackson:jackson-base:pom:) >= %{version}
BuildRequires:  mvn(com.google.code.maven-replacer-plugin:replacer)
Buildrequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.mockito:mockito-core)

BuildArch:      noarch
%if 0%{?fedora} || 0%{?rhel} >= 10
ExclusiveArch:  %{java_arches} noarch
%endif

%description
The general-purpose data-binding functionality and tree-model for Jackson Data
Processor. It builds on core streaming parser/generator package, and uses
Jackson Annotations for configuration.

%prep
%setup -q -n %{name}-%{name}-%{version}

# Remove plugins unnecessary for RPM builds
%pom_remove_plugin ":maven-enforcer-plugin"
%pom_remove_plugin "org.jacoco:jacoco-maven-plugin"
%pom_remove_plugin "org.moditect:moditect-maven-plugin"
%pom_remove_plugin "de.jjohannes:gradle-module-metadata-maven-plugin"
%pom_xpath_set "//pom:javac.src.version" "11"
%pom_xpath_set "//pom:javac.target.version" "11"
%pom_xpath_inject "//pom:properties" " <maven.compiler.source>11</maven.compiler.source>"
%pom_xpath_inject "//pom:properties" " <maven.compiler.target>11</maven.compiler.target>"

cp -p src/main/resources/META-INF/NOTICE .
sed -i 's/\r//' LICENSE NOTICE

# unavailable test deps
%pom_remove_dep javax.measure:jsr-275
rm src/test/java/com/fasterxml/jackson/databind/introspect/NoClassDefFoundWorkaroundTest.java
%pom_xpath_remove pom:classpathDependencyExcludes

# TestTypeFactoryWithClassLoader fails to compile
# - mockito is only transitively pulled in by powermock, so add it back
%pom_add_dep org.mockito:mockito-core::test

%mvn_file : %{name}

%build
%mvn_build -f -j -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles
%doc README.md release-notes/*
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
- Resolves: rhbz#2322329

* Fri Sep 27 2024 Packit <hello@packit.dev> - 2.18.0-1
- Update to version 2.18.0
- Resolves: rhbz#2315070

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Packit <hello@packit.dev> - 2.17.2-1
- Update to version 2.17.2
- Resolves: rhbz#2296004

* Sun May 05 2024 Packit <hello@packit.dev> - 2.17.1-1
- Update to version 2.17.1
- Resolves: rhbz#2279122

* Tue Mar 12 2024 Packit <hello@packit.dev> - 2.17.0-1
- [maven-release-plugin] prepare release jackson-databind-2.17.0 (Tatu Saloranta)
- Prepare for 2.17.0 release (Tatu Saloranta)
- Fix #2543: Skip delegating creator arguments when collecting properties (#4426) (Kyrylo Merzlikin)
- ... (Tatu Saloranta)
- Add failing test for #4356 (Tatu Saloranta)
- Migrate tests to `JUnit 5` for `/mixins`, `/misc`, `/module`, `/objectId` tests (#4423) (Kim, Joo Hyuk)
- Back to snapshot dep (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Add failing test for #4417 (Tatu Saloranta)
- Fix #4403: prevent use of zero-prefixed String as Enum index on deserialization (#4420) (Tatu Saloranta)
- warnings cleanup (Tatu Saloranta)
- Test refactoring/renaming (Tatu Saloranta)
- Add deprecation markers to avoid warnings from compiler (Tatu Saloranta)
- Fix #4416: Deprecate `JsonNode.asText(String)` (#4419) (Tatu Saloranta)
- Refactoring JsonFormat detection, post #4409 (#4418) (Tatu Saloranta)
- Bump the github-actions group with 3 updates (#4412) (dependabot[bot])
- Add tests related to #4409 (#4411) (Tatu Saloranta)
- Add failing test for #4403 (default enum read fail) (#4408) (Tatu Saloranta)
- Try to modify an existing test to help resolve #4354 (Tatu Saloranta)
- ... (Tatu Saloranta)
- Migrate tests to `Junit 5` (#4405) (Kim, Joo Hyuk)
- Back to snapshot dep (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- [maven-release-plugin] prepare release jackson-databind-2.17.0-rc1 (Tatu Saloranta)
- Prepare for 2.17.0-rc1 release (Tatu Saloranta)
- Migrate `/jsontype` and `/jsontype/deftyping` tests to `JUnit 5` (#4398) (Kim, Joo Hyuk)
- Bump the github-actions group with 2 updates (#4399) (dependabot[bot])
- Minor fix to release notes (Tatu Saloranta)
- fix incorrect issue/pr ref in release notes (Tatu Saloranta)
- Deserialize `java.util.UUID` encoded as Base64 and base64Url with or without padding (#4393) (Jesper Blomquist)
- Remove junit-bom, gotten via parent pom for 2.17 (Tatu Saloranta)
- fix minor test regression (Tatu Saloranta)
- Yet more test renaming (Tatu Saloranta)
- More JUnit5 test conversions (#4390) (Tatu Saloranta)
- More test renaming (Tatu Saloranta)
- Test refactoring (Tatu Saloranta)
- Test renaming/refactoring (Tatu Saloranta)
- Test refactoring (renaming) (Tatu Saloranta)
- Test refactoring (Tatu Saloranta)
- Minor test refactoring (Tatu Saloranta)
- ... (Tatu Saloranta)
- modify all tests (#4389) (Kim, Joo Hyuk)
- Once more fix test wrt [core#1173] (Tatu Saloranta)
- support nulls in TextNode equals (#4379) (PJ Fanning)
- Bump the github-actions group with 1 update (#4375) (dependabot[bot])
- Resolve a unit test regression wrt revert of [core#1173] fix (temporarily) (Tatu Saloranta)
- Warnings clean up (Tatu Saloranta)
- UTs for issue #4358 (#4359) (Mark Herkrath)
- Minor warnings removal (Tatu Saloranta)
- Prepare for 2.17.0-rc1 (Tatu Saloranta)
- All (#4374) (Kim, Joo Hyuk)
- Bump the github-actions group with 2 updates (#4367) (dependabot[bot])
- Fix #4364: add `PropertyName.merge()`, use by AnnotationIntrospectorPair (#4365) (Tatu Saloranta)
- Update JUnit5 to 5.10.1 (Tatu Saloranta)
- add Undefined to EnumWithNullToString4355Test (#4361) (PJ Fanning)
- Migrate `/deser/jdk` tests to `JUnit 5` (#4362) (Kim, Joo Hyuk)
- ... (Tatu Saloranta)
- Alternate approach for wildcards in TypeBindings (#4151) (Jonas Konrad)
- Yet more cleaning of StdTypeResolverBuilder (Tatu Saloranta)
- Refactor handling of default type property for StdTypeResolverBuilder (#4352) (Tatu Saloranta)
- Bump the github-actions group with 3 updates (#4350) (dependabot[bot])
- Minor refactoring for readability wrt DeserializerCache/converter (#4349) (Tatu Saloranta)
- One tiny robustification to ResolvableDeserializer handling (Tatu Saloranta)
- Minor test refactoring (Tatu Saloranta)
- Add failing test (reproduction) for #562 (#4347) (Tatu Saloranta)
- Move #4316 testing to non-failing now that it passes (Tatu Saloranta)
- Migrate `/deser/dos`, `/deser/builder`, `/deser/enums` tests to JUnit 5 (#4344) (Kim, Joo Hyuk)
- Streamline `ThrowableDeserializer` slightly to reduce call stack for deep nesting (#4345) (Tatu Saloranta)
- Tests to verify proper life-cycle of `RecyclerPool` implementations, from databind perspective (#4324) (Mario Fusco)
- Make `@JsonAlias` be respected by polymorphic deduction for deserialization (#4335) (Kim, Joo Hyuk)
- Implement new `BeanPropertyDefinition.getAliases()` method (#4336) (Kim, Joo Hyuk)
- Second half of #4337: deserializers (#4339) (Tatu Saloranta)
- Tiny test refactoring (Tatu Saloranta)
- Fix #4337: support `@JsonSerialize(contentConverter)` with `AtomicReference` (#4338) (Tatu Saloranta)
- Test renaming (Tatu Saloranta)
- MInor straightening of alias access (Tatu Saloranta)
- Warnings clean up (Tatu Saloranta)
- Add explicit closing of `BufferRecycler` from ObjectMapper/ObjectWriter (#4334) (Tatu Saloranta)
- Bump the github-actions group with 2 updates (#4332) (dependabot[bot])
- Instantiators for additional container classes (#4300) (Eduard Dudar)
- Migrate `/deser/creators` tests to `JUnit 5` (#4331) (Kim, Joo Hyuk)
- Add one more auto-close for `ObjectWriter` (Tatu Saloranta)
- Minor cosmetic change (Tatu Saloranta)
- Minor fix from #4324 (auto-close of `SegmentedStringWriter`) (Tatu Saloranta)
- Refactoring to prepare for getting #4300 merged (Tatu Saloranta)
- Yet more test renaming (Tatu Saloranta)
- Move test to better package (Tatu Saloranta)
- Fix #4309 (#4320) (Kim, Joo Hyuk)
- Bump the github-actions group with 2 updates (#4319) (dependabot[bot])
- Add failing test for #4119 (Tatu Saloranta)
- test renaming (Tatu Saloranta)
- Minor test refactoring (Tatu Saloranta)
- Minor test refactoring post #4317 (Tatu Saloranta)
- Migrate `/deser` tests to `JUnit 5` (#4317) (Kim, Joo Hyuk)
- Add failing test for #4316 (Tatu Saloranta)
- Add missing overrides wrt FP handling for "untyped" case (Tatu Saloranta)
- Improve `JsonNode` and "untyped" (java.lang.Object) deserializers wrt number detection (Tatu Saloranta)
- Warnings cleanup (Tatu Saloranta)
- Migrate `/convert` tests to `JUnit 5` (#4307) (Kim, Joo Hyuk)
- Implement `getNumberTypeFP()` for `JsonNode`-backed parser (Tatu Saloranta)
- Add `TokenBuffer` support for `JsonParser.getNumberTypeFP()` (Tatu Saloranta)
- ... (Tatu Saloranta)
- Enable ci-fuzz workflow for 2.17 pulls (Tatu Saloranta)
- Minor fix wrt null-handling for `TreeSet`s (Tatu Saloranta)
- Migrate `/deser/filter` tests to `JUnit 5` (#4296) (Kim, Joo Hyuk)
- Update BasicExceptionTest.java (#4297) (Kim, Joo Hyuk)
- Remove broken link from README (Tatu Saloranta)
- Try fixing wiki links from README (Tatu Saloranta)
- Bump the github-actions group with 1 update (#4284) (dependabot[bot])
- Test class renaming (Tatu Saloranta)
- Test refactoring (Tatu Saloranta)
- Test renaming (Tatu Saloranta)
- Migrate `/exc` tests to `JUnit 5` (#4282) (Kim, Joo Hyuk)
- doc : write suggestion also (#4280) (Kim, Joo Hyuk)
- Renaming wrt issue being resolved (Tatu Saloranta)
- Add new option to handle properties not part of current active `@JsonView` (#4275) (Kim, Joo Hyuk)
- Bump the github-actions group with 2 updates (#4268) (dependabot[bot])
- Update code coverage ref on README (Tatu Saloranta)
- Migrate `/type` tests into `JUnit5` (#4267) (Kim, Joo Hyuk)
- Improve handling of failure to deserialize `java.util.regex.Pattern` (#4266) (Tatu Saloranta)
- Fix #4262: handle `null` insert fail for `TreeSet` (#4265) (Tatu Saloranta)
- Moar test refactoring (Tatu Saloranta)
- Test refactoring (Tatu Saloranta)
- Test refactoring (Tatu Saloranta)
- Test refactoring (Tatu Saloranta)
- Update release notes wrt #736 (Tatu Saloranta)
- Fix `REQUIRE_SETTERS_FOR_GETTERS` taking no effect (#4257) (Kim, Joo Hyuk)
- Another minor tweak to ThrowableDeserializer to flatten call stack (Tatu Saloranta)
- Minor refactoring to `ThrowableDeserializer` to avoid calling Deprecated constructor (Tatu Saloranta)
- Fix #4263: remove generic type parameterization from `ObjectArrayDeserializer` (#4264) (Tatu Saloranta)
- Minor comment fix (Tatu Saloranta)
- Fix OSS-Fuzz found issue with `null` for "suppressable" entries for `Throwable`s (#4261) (Tatu Saloranta)
- Fix year number (2024->2023) in comments (Tatu Saloranta)
- Improve error handling of `TokenBuffer` wrt malformed input (EOF handling) (#4260) (Tatu Saloranta)
- Bump the github-actions group with 1 update (#4255) (dependabot[bot])
- Migrate `/contextual` tests to `JUnit 5` (#4251) (Kim, Joo Hyuk)
- Fix test failure with static mocking by replacing `PowerMock` with `Mockito` (#4254) (Kim, Joo Hyuk)
- Add pre-validation for parsing "stringified" Floating-Point numbers, missing length checks (#4253) (Tatu Saloranta)
- Fix #4248: add special handling for `null` "cause" for Throwable deserialization (#4249) (Tatu Saloranta)
- Improve `JsonNodeDeserializer` handling of NaN wrt `USE_BIG_DECIMAL_FOR_FLOATS` (#4245) (Tatu Saloranta)
- Moar warnings removal (3.0-proofing) (Tatu Saloranta)
- More warnings removal (3.0-proofing) (Tatu Saloranta)
- Bump the github-actions group with 1 update (#4241) (dependabot[bot])
- Deprecate `DefaultTyping.EVERYTHING`  (#4240) (Kim, Joo Hyuk)
- Tiny streamlining (Tatu Saloranta)
- Minor exception message fix (Tatu Saloranta)
- strongly discourage users from disabling WRAP_EXCEPTIONS (#4235) (PJ Fanning)
- Test streamlining (Tatu Saloranta)
- Post-merge tweaks for #4194 (Tatu Saloranta)
- Add `DeserializationFeature.FAIL_ON_NAN_TO_BIG_DECIMAL_COERCION` to determine what happens on `JsonNode` coercion to `BigDecimal` with NaN (#4195) (Kim, Joo Hyuk)
- Minor javadoc fix (Tatu Saloranta)
- Minor Javadoc improvements to JsonNode wrt findValue() and related methods (Tatu Saloranta)
- Fixed testAddFilterWithEmptyStringId() (#4232) (saurabh-shetty)
- Fix #4200: use annotations for delegating `@JsonCreator` (#4228) (Tatu Saloranta)
- Add failing test case for #4200. (Tatu Saloranta)
- Fixed com.fasterxml.jackson.databind.node.TestConversions#testValueToTree (#4227) (saurabh-shetty)
- Fix #4205: add "sun.*" as "JDK" package (#4226) (Tatu Saloranta)
- Fix #4214: support polymorphic deserialization of `EnumSet` (#4222) (Tatu Saloranta)
- Minor refactoring for #4217: move `DatabindTestUtil` under `.../testutil` (Tatu Saloranta)
- Migrate tests in `view` test package to `JUnit 5` using `DatabindTestUtil` (#4217) (Kim, Joo Hyuk)
- .. (Tatu Saloranta)
- Fixed potential test failure due to nondeterminism in the order of elements in jsonString in SimpleFilterProviderTest.testAddFilterLastOneRemainsFlip test (#4224) (saurabh-shetty)
- Bump the github-actions group with 1 update (#4223) (dependabot[bot])
- ... (Tatu Saloranta)
- Minor tweaks to (failing) test for #4214 (Tatu Saloranta)
- Added unit test for Issue-4214 (#4215) (V H V Sekhar Durga)
- Some more dead code elimination (Tatu Saloranta)
- Update README.md Jackson Version (#4220) (Muhammad Khalikov)
- Update release notes wrt #4209, minor clean up (Tatu Saloranta)
- Make Bean (De)SerializerModifier implement Serializable #4209 (#4212) (Muhammad Khalikov)
- Bump the github-actions group with 1 update (#4210) (dependabot[bot])
- typo fix (Tatu Saloranta)
- Bump the github-actions group with 1 update (#4206) (dependabot[bot])
- Start 2.17 branch (Tatu Saloranta)
- Resolves rhbz#2269279

* Sat Mar 09 2024 Packit <hello@packit.dev> - 2.16.2-1
- [maven-release-plugin] prepare release jackson-databind-2.16.2 (Tatu Saloranta)
- Prepare for 2.16.2 release (Tatu Saloranta)
- Make `PropertyNamingStrategy` not affect Enums (#4414) (Kim, Joo Hyuk)
- Resolves rhbz#2268715

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.16.1-4
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Marco Fargetta <mfargett@redhat.com> - 2.16.1-2
- Force the java bytecode version to java11

* Mon Jan 22 2024 Marco Fargetta <mfargett@redhat.com> - 2.16.1-1
- [maven-release-plugin] prepare release jackson-databind-2.16.1 (Tatu Saloranta)
- Prepare for 2.16.1 release (Tatu Saloranta)
- Add passing test to close #3277 (#4259) (Kim, Joo Hyuk)
- Add failing test for #4218 (Tatu Saloranta)
- Post-merge clean up for #4229 (Tatu Saloranta)
- Fix regression from #4008,  optimize `ObjectNode.findValue(s)` and `findParent(s)` (#4230) (Kim, Joo Hyuk)
- Minor update to release notes wrt #3133 (Tatu Saloranta)
- Update release notes wrt #3133 fix (Tatu Saloranta)
- Add now-passing test for #3133 (#4231) (Kim, Joo Hyuk)
- Fix #4200: use annotations for delegating `@JsonCreator` (#4228) (Tatu Saloranta)
- Tiny cleanup to eliminate bit of dead code (Tatu Saloranta)
- Minor tweak post #4216 (Tatu Saloranta)
- Allow primitive array deserializer to be captured by `DeserializerModifier` (#4219) (Kim, Joo Hyuk)
- typo fix (release notes) (Tatu Saloranta)
- Back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 04 2023 Marco Fargetta <mfargett@redhat.com> - 2.16.0-2
- Fix pom file to work with java 11

* Wed Nov 22 2023 Chris Kelley <ckelley@redhat.com> - 2.16.0-1
- [maven-release-plugin] prepare release jackson-databind-2.16.0 (Tatu Saloranta)
- Prepare for 2.16.0 release (Tatu Saloranta)
- Post-commit fixes to #1770 (Tatu Saloranta)
- issue-1770 - big number not returned as DecimalNode (#4191) (PJ Fanning)
- minor test comment improvement (Tatu Saloranta)
- Remove a test for closed issue; no plans to change behavior currently, no benefit from failing test. (Tatu Saloranta)
- Update release notes wrt #4185 (Tatu Saloranta)
- Fix for 4185 (#4189) (Kim, Joo Hyuk)
- test cleanup (Tatu Saloranta)
- Fix #4184: setCurrentValue() for empty POJO called at wrong time (#4186) (Tatu Saloranta)
- Bump the github-actions group with 2 updates (#4183) (dependabot[bot])
- DeserializationContext changed to allow null (#4179) (wrongwrong)
- Minor clean up (Tatu Saloranta)
- Exception when deserialization of private `record` with default constructor (fix for #4175) (#4178) (Kim, Joo Hyuk)
- Move test for #4175 under failing/ for 2.16 (as it's failing) (Tatu Saloranta)
- Add test for #4715 in 2.15 (passing) (Tatu Saloranta)
- Update release notes wrt #1172 (Tatu Saloranta)
- Test `JsonView` works with `JsonCreator` (#4173) (Kim, Joo Hyuk)
- Minor test improvement (Tatu Saloranta)
- Create win.yml for windows CI (#4172) (PJ Fanning)
- Bump the github-actions group with 2 updates (#4171) (dependabot[bot])
- Try fixing #4168 wrt linefeed diff (#4170) (Tatu Saloranta)
- Back to snapshot dep (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Mon Nov 06 2023 Chris Kelley <ckelley@redhat.com> - 2.15.3-1
- [maven-release-plugin] prepare release jackson-databind-2.15.3 (Tatu Saloranta)
- Prepare for 2.15.3 release (Tatu Saloranta)
- Minor refactoring wrt #4149 (Tatu Saloranta)
- Create TestMixedCollections.java (#4149) (PJ Fanning)
- Update release notes wrt #4121 (Tatu Saloranta)
- Preserve the original component type in merging to the array (#4121) (Yury Molchan)
- Introduce more efficient Form-Based GitHub Issue Templates (#4042) (Kim, Joo Hyuk)
- Improve JavaDoc and Test for config ACCEPT_EMPTY_STRING_AS_NULL_OBJECT wrt special cases (#4012) (Kim, Joo Hyuk)
- Update Maven wrapper version (Tatu Saloranta)
- Minor javadoc improvement (Tatu Saloranta)
- Update release notes wrt #3968 fix (Tatu Saloranta)
- Ignore ConstructorDetector.SingleArgConstructor.PROPERTIES preference for Records. (#3969) (Sim Yih Tsern)
- to 2.15.3-SNAPSHOT (Tatu Saloranta)
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
- Update to use SPDX licence

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

* Fri May 21 2021 Dogtag PKI Team <pki-devel@redhat.com> - 2.11.4-3
- Disable tests
- Drop jackson-databind-javadoc

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Fabio Valentini <decathorpe@gmail.com> - 2.11.4-1
- Update to version 2.11.4.

* Wed Oct 14 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.3-1
- Update to version 2.11.3.

* Sun Aug 09 2020 Fabio Valentini <decathorpe@gmail.com> - 2.11.2-2
- Drop useless powermock build dependency.

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

* Thu Oct 3 2019 Alexander Scheel <ascheel@redhat.com> - 2.10.0-1
- Update to latest upstream release
- Fixes: CVE-2019-14540
- Fixes: CVE-2019-16335
- Fixes: CVE-2019-16942
- Fixes: CVE-2019-16943
- Resolves: rhbz#1758168
- Resolves: rhbz#1758172
- Resolves: rhbz#1758183

* Thu Sep 12 2019 Alexander Scheel <ascheel@redhat.com> - 2.9.9.3-1
- Update to latest upstream release; fixes CVE-2019-12384

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 06 2019 Mat Booth <mat.booth@redhat.com> - 2.9.8-1
- Update to latest upstream release, fixes CVE-2018-14718 CVE-2018-147189
  CVE-2018-19360 CVE-2018-19361 CVE-2018-19362 CVE-2018-12022 CVE-2018-12023
  CVE-2018-14720 CVE-2018-14721

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 26 2018 Mat Booth <mat.booth@redhat.com> - 2.9.4-3
- Add patch to fix CVE-2018-7489

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Mat Booth <mat.booth@redhat.com> - 2.9.4-1
- Update to latest upstream release
- Drop upstreamed CVE patches

* Mon Jan 22 2018 Mat Booth <mat.booth@redhat.com> - 2.9.3-1
- Update to latest upstream release

* Mon Jan 15 2018 Mat Booth <mat.booth@redhat.com> - 2.7.6-7
- Better patch for CVE-2017-17485

* Thu Jan 11 2018 Mat Booth <mat.booth@redhat.com> - 2.7.6-6
- Backport a patch to fix CVE-2017-17485

* Fri Nov 03 2017 Mat Booth <mat.booth@redhat.com> - 2.7.6-5
- Backport a patch to fix CVE-2017-15095

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Mat Booth <mat.booth@redhat.com> - 2.7.6-3
- Backport a patch to fix CVE-2017-7525

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

* Wed Jul 23 2014 gil cattaneo <puntogil@libero.it> 2.4.1.3-1
- update to 2.4.1.3

* Thu Jul 03 2014 gil cattaneo <puntogil@libero.it> 2.4.1.1-1
- update to 2.4.1.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 gil cattaneo <puntogil@libero.it> 2.2.2-2
- review fixes

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- 2.2.2
- renamed jackson-databind

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.2.1-1
- 2.2.1

* Wed Oct 24 2012 gil cattaneo <puntogil@libero.it> 2.1.0-1
- update to 2.1.0
- renamed jackson2-databind

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.0.6-1
- initial rpm
