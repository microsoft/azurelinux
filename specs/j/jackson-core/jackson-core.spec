# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           jackson-core
Version:        2.18.2
Release:        4%{?dist}
Summary:        Core part of Jackson
License:        Apache-2.0

URL:            https://github.com/FasterXML/jackson-core
Source0:        %{url}/archive/%{name}-%{version}.tar.gz
Patch1:         0001-Remove-ch.randelshofer.fastdoubleparser.patch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.fasterxml.jackson:jackson-base:pom:) >= %{version}
BuildRequires:  mvn(com.google.code.maven-replacer-plugin:replacer)
Buildrequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

BuildArch:      noarch
%if 0%{?fedora} || 0%{?rhel} >= 10
ExclusiveArch:  %{java_arches} noarch
%endif

%description
Core part of Jackson that defines Streaming API as well
as basic shared abstractions.

%prep
%autosetup -n %{name}-%{name}-%{version} -p 1

# Remove plugins unnecessary for RPM builds
%pom_remove_plugin ":maven-enforcer-plugin"
%pom_remove_plugin "org.apache.maven.plugins:maven-shade-plugin"
%pom_remove_plugin "org.jacoco:jacoco-maven-plugin"
%pom_remove_plugin "org.moditect:moditect-maven-plugin"
%pom_remove_plugin "de.jjohannes:gradle-module-metadata-maven-plugin"
%pom_remove_plugin "io.github.floverfelt:find-and-replace-maven-plugin"
%pom_remove_dep "ch.randelshofer:fastdoubleparser"

%pom_add_plugin "org.apache.felix:maven-bundle-plugin" . "<extensions>true</extensions>"

cp -p src/main/resources/META-INF/jackson-core-NOTICE .
sed -i 's/\r//' LICENSE jackson-core-NOTICE

%mvn_file : %{name}

%build
%mvn_build -f -j

%install
%mvn_install

%files -f .mfiles
%doc README.md release-notes/*
%license LICENSE jackson-core-NOTICE

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2.18.2-4
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 28 2024 Packit <hello@packit.dev> - 2.18.2-1
- Update to version 2.18.2
- Resolves: rhbz#2322328

* Fri Sep 27 2024 Packit <hello@packit.dev> - 2.18.0-1
- Update to version 2.18.0
- Resolves: rhbz#2315056

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Packit <hello@packit.dev> - 2.17.2-1
- Update to version 2.17.2
- Resolves: rhbz#2296003

* Sun May 05 2024 Packit <hello@packit.dev> - 2.17.1-1
- Update to version 2.17.1
- Resolves: rhbz#2279121

* Tue Mar 12 2024 Packit <hello@packit.dev> - 2.17.0-1
- [maven-release-plugin] prepare release jackson-core-2.17.0 (Tatu Saloranta)
- Prepare for 2.17.0 release (Tatu Saloranta)
- Back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Bump the github-actions group with 3 updates (#1236) (dependabot[bot])
- Improve #1149 wrt JsonParser.getNumberTypeFP() default implementation (#1235) (Tatu Saloranta)
- Add explicit override for JSON parsers for `JsonParser.getNumberTypeFP()` (Tatu Saloranta)
- Back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- [maven-release-plugin] prepare release jackson-core-2.17.0-rc1 (Tatu Saloranta)
- Prepare for 2.17.0-rc1 release (Tatu Saloranta)
- Bump the github-actions group with 2 updates (#1228) (dependabot[bot])
- Remove junit-bom dependency here, included via jackson-base parent pom now (Tatu Saloranta)
- Minor refactoring (Tatu Saloranta)
- Use String#isEmpty(), remove redundancies, and reduce verbose code (#1225) (Gary Gregory)
- Minor inclusions in JsonParserBase (Tatu Saloranta)
- Add `JsonParserBase` base class (backport from 3.0) (#1224) (Tatu Saloranta)
- Second attempt at solving #1173 (#1223) (Tatu Saloranta)
- Manual merge of change in #1221: tiny optimization for `JsonPointer`, index parse (Tatu Saloranta)
- Update release notes wrt #1218 (Tatu Saloranta)
- surrogate conversion simplified (#1218) (Tatu Saloranta)
- Update release notes wrt 2.17 (Tatu Saloranta)
- Enable test for #1203 (Tatu Saloranta)
- Faster division by 1000 (#1203) (xtonik)
- ... (Tatu Saloranta)
- avoid use slow regular expression when replacing characters (#1219) (Tatu Saloranta)
- Reuse own constant and refactor magic chars into new constants for (#1216) (Gary Gregory)
- More incremental refactoring (Tatu Saloranta)
- Refactoring: order error reporting methods (Tatu Saloranta)
- Bump the github-actions group with 1 update (#1215) (dependabot[bot])
- Some more JUnit5 conversion (Tatu Saloranta)
- Continue JUnit5 conversion (Tatu Saloranta)
- Start converting some unit tests to JUnit5; add new test base class to help (#1212) (Tatu Saloranta)
- Prepare for 2.17.0-rc1 release (Tatu Saloranta)
- Bump the github-actions group with 2 updates (#1209) (dependabot[bot])
- Fixes #1207: apply "maxNameLength" change to CharsToNameCaonicalizer (#1208) (Tatu Saloranta)
- Bump the github-actions group with 3 updates (#1206) (dependabot[bot])
- Implement #1117: change the default RecyclerPool to use (#1205) (Tatu Saloranta)
- ... (Tatu Saloranta)
- Fix #1202: add `RecyclerPool.clear()` method (#1204) (Tatu Saloranta)
- Javadoc addition (Tatu Saloranta)
- optimized char check for ']}' (xtonik)
- optimized char check for 'eE' (xtonik)
- optimized char check for 'dDfF' (xtonik)
- Update release notes wrt #1195 (Tatu Saloranta)
- Fix #1195: add actual `BufferRecycler` reuse (#1196) (Tatu Saloranta)
- Bump the github-actions group with 2 updates (#1199) (dependabot[bot])
- Add new `JsonWriteFeature.ESCAPE_FORWARD_SLASHES` (#1197) (Kim, Joo Hyuk)
- Merging minor changes needed for solving BufferRecycler recycling (Tatu Saloranta)
- Fix codecov.io link (downgrade to 2.16) (Tatu Saloranta)
- Fixes #1193: add `BufferRecycler.Gettable`, impls for BAB, SSW (#1194) (Tatu Saloranta)
- Minor Javadoc typo fix (Tatu Saloranta)
- Add a utility method (Tatu Saloranta)
- Add failing test for #1144 (#1189) (Tatu Saloranta)
- Bump the github-actions group with 1 update (#1188) (dependabot[bot])
- Update release notes wrt #1137 (Tatu Saloranta)
- Fix #1186: improve recycled buffer release logic (#1187) (Tatu Saloranta)
- Bump the github-actions group with 1 update (#1183) (dependabot[bot])
- Fixes #1149: add `JsonParser.getNumberTypeFP()` (#1182) (Tatu Saloranta)
- Minor post-merge fix wrt #1178 (Tatu Saloranta)
- Allow configuring `DefaultPrettyPrinter` separators for empty Arrays and Objects (#1178) (gulecroc)
- Cleave of failing #1180 tests from passing #1173 tests (Tatu Saloranta)
- Test refactoring (Tatu Saloranta)
- Refactor exception generation by JsonParser (#1179) (Tatu Saloranta)
- Bump the github-actions group with 1 update (#1177) (dependabot[bot])
- Bump the github-actions group with 2 updates (#1174) (dependabot[bot])
- Update code coverage on README (Tatu Saloranta)
- Minor test refactoring (Tatu Saloranta)
- ... (Tatu Saloranta)
- Minor additional error construction changes (Tatu Saloranta)
- Minor additions to JsonGenerator wrt error handling (Tatu Saloranta)
- Fix #1168 (JsonPointer.append() with JsonPointer.tail()) (#1172) (Tatu Saloranta)
- Fix #1145: escape `property` in `JsonPointer.append(String)` (#1171) (Tatu Saloranta)
- Fixes #1169: adds test(s), fix (#1170) (Tatu Saloranta)
- Bump the github-actions group with 1 update (#1167) (dependabot[bot])
- fastdoubleparser 1.0.0 (#1163) (#1164) (PJ Fanning)
- Reproduction for #1161 (#1162) (Tatu Saloranta)
- fastdoubleparser 1.0.0 (#1163) (PJ Fanning)
- Minor test refactoring (Tatu Saloranta)
- Add `NumberInput.looksLikeValidNumber()` utility method (#1160) (Tatu Saloranta)
- warnings removal wrt deprecation (Tatu Saloranta)
- Deprecate some of `NumberInput` methods. (Tatu Saloranta)
- Follow-up to #1157: unify exception handling (#1159) (Tatu Saloranta)
- Update release notes wrt #1157 (Tatu Saloranta)
- use fast parser for large bigdecimals (500+ chars) (#1157) (PJ Fanning)
- More deprecation, now on generator side (Tatu Saloranta)
- ... (Tatu Saloranta)
- Bump the github-actions group with 1 update (#1152) (dependabot[bot])
- More cleanup wrt now-deprecated JsonParser getter methods (Tatu Saloranta)
- Mark some more methods deprecated, as forward-looking changes towards 3.0 (Tatu Saloranta)
- Fix `JsonParser.isNaN()` to be stable, only indicate explicit NaN values; not ones due to coercion (#1150) (Tatu Saloranta)
- test that shows that isNaN call is not reliable (#1135) (PJ Fanning)
- Add a test similar to #1135 (Tatu Saloranta)
- Bump the github-actions group with 1 update (#1148) (dependabot[bot])
- Test base class refactoring (simplifying BaseTest) (#1143) (Tatu Saloranta)
- Bump the github-actions group with 1 update (#1140) (dependabot[bot])
- Bump the github-actions group with 1 update (#1138) (dependabot[bot])
- Start 2.17 branch (Tatu Saloranta)
- Resolves rhbz#2269278

* Sat Mar 09 2024 Packit <hello@packit.dev> - 2.16.2-1
- [maven-release-plugin] prepare release jackson-core-2.16.2 (Tatu Saloranta)
- Prepare for 2.16.2 release (Tatu Saloranta)
- Resolves rhbz#2268716

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.16.1-4
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 09 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.16.1-3
- Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Marco Fargetta <mfargett@redhat.com> - 2.16.1-1
- [maven-release-plugin] prepare release jackson-core-2.16.1 (Tatu Saloranta)
- Prepare for 2.16.1 release (Tatu Saloranta)
- Minor test improvements (Tatu Saloranta)
- Minor tweaking post-merge wrt #1175 (Tatu Saloranta)
- Add failing tests for #1173: parse error location (#1175) (Paul Bunyan)
- Backport #1168 in 2.16(.1) (Tatu Saloranta)
- Update release notes wrt #1161 backport (Tatu Saloranta)
- fastdoubleparser 1.0.0 (#1163) (#1166) (PJ Fanning)
- Update release notes wrt #1161 (Tatu Saloranta)
- fastdoubleparser 1.0.0 (#1163) (#1165) (PJ Fanning)
- Tiny import clean up (Tatu Saloranta)
- update javadoc to highlight that this class is for internal jackson use (#1156) (PJ Fanning)
- Test code clean up: pro-actively replace to-be-deprecated methods to non-deprecated ones (wrt 2.17) (Tatu Saloranta)
- Fix #1146: add missing `JsonParserDelegate` overrides (#1147) (Tatu Saloranta)
- Update version scorecard check runs for (Tatu Saloranta)
- Fix #1141: prevent NPE in Version.equals() (#1142) (Tatu Saloranta)
- Fix typo in VERSION-2.x (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 15 2023 Packit <hello@packit.dev> - 2.16.0-1
- [maven-release-plugin] prepare release jackson-core-2.16.0 (Tatu Saloranta)
- Prepare for 2.16.0 release (Tatu Saloranta)
- Make JacksonFeatureSet java.io.Serializable (Tatu Saloranta)
- Update release notes wrt #1136 (Tatu Saloranta)
- Change error mesage to mention -INF (#1136) (PJ Fanning)
- Bump the github-actions group with 2 updates (#1134) (dependabot[bot])
- Add missing name-length check in a test (Tatu Saloranta)
- Unit test cleanup (Tatu Saloranta)
- Maximum Property name length affects input/read (#1130) (PJ Fanning)
- Bump the github-actions group with 2 updates (#1129) (dependabot[bot])
- Back to snapshot deps (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Resolves rhbz#2249923

* Mon Nov 06 2023 Chris Kelley <ckelley@redhat.com> - 2.15.3-1
- [maven-release-plugin] prepare release jackson-core-2.15.3 (Tatu Saloranta)
- Prepare for 2.15.3 release (Tatu Saloranta)
- Update release notes wrt #1111 (Tatu Saloranta)
- Call the right filterFinishArray/Object from FilteringParserDelegate (#1111) (Dai MIKURUBE)
- Update Maven wrapper version (Tatu Saloranta)
- Further tweaking of release notes (Tatu Saloranta)
- Add ref to #943 in release-notes/VERSION-2.x (Tatu Saloranta)
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
- Update to use SPDX licence

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.11.4-8
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.11.4-7
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Dogtag PKI Team <pki-devel@redhat.com> - 2.11.4-5
- Drop Java 1.6 support, compile with Java 11

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Dogtag PKI Team <pki-devel@redhat.com> - 2.11.4-3
- Disable tests
- Drop jackson-core-javadoc

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

* Thu Oct 3 2019 Alexander Scheel <ascheel@redhat.com> - 2.10.0-1
- Update to latest upstream release

* Thu Sep 12 2019 Alexander Scheel <ascheel@redhat.com> - 2.9.9-1
- Update to latest upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 06 2019 Mat Booth <mat.booth@redhat.com> - 2.9.8-2
- Speed up builds on 32bit arm

* Wed Feb 06 2019 Mat Booth <mat.booth@redhat.com> - 2.9.8-1
- Update to latest upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Mat Booth <mat.booth@redhat.com> - 2.9.4-1
- Update to latest upstream release

* Thu Jan 11 2018 Mat Booth <mat.booth@redhat.com> - 2.9.3-1
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

* Wed Jul 23 2014 gil cattaneo <puntogil@libero.it> 2.4.1.1-1
- update to 2.4.1.1

* Wed Jul 02 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- update to 2.4.1

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
- renamed jackson-core

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.2.1-1
- 2.2.1

* Wed Oct 24 2012 gil cattaneo <puntogil@libero.it> 2.1.0-1
- update to 2.1.0
- renamed jackson2-core

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.0.6-1
- initial rpm
