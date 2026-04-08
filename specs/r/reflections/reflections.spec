# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          reflections
Version:       0.9.12
Release:       21%{?dist}
Summary:       Java run-time meta-data analysis
License:       WTFPL
URL:           https://github.com/ronmamo/reflections
BuildArch:     noarch
ExclusiveArch:  %{java_arches} noarch

Source0:       %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.google.code.gson:gson)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.dom4j:dom4j)
BuildRequires:  mvn(org.javassist:javassist)

%description
A Java run-time meta-data analysis, in the spirit of Scannotations

Reflections scans your class-path, indexes the meta-data, allows you
to query it on run-time and may save and collect that information
for many modules within your project.

Using Reflections you can query your meta-data such as:
* get all sub types of some type
* get all types/methods/fields annotated with some annotation,
  w/o annotation parameters matching
* get all resources matching matching a regular expression

%{?javadoc_package}

%prep
%autosetup

find -type f '(' -name '*.jar' -o -name '*.class' ')' -not -path './src/test/*' -print -delete

%pom_xpath_inject 'pom:plugin[pom:artifactId = "maven-compiler-plugin"]' '<version>3.8.1</version>'

%build
%mvn_build -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8 -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license COPYING.txt

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 0.9.12-21
- Rebuilt for java-25-openjdk as preffered jdk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 0.9.12-17
- Rebuilt for java-21-openjdk as system jdk

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 0.9.12-11
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0.9.12-10
- Rebuilt for java-17-openjdk as system jdk

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 11 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 0.9.12-8
- Use macros: javadoc_package, autosetup, url
- Remove BRs: jsr305, slf4j-api, slf4j-simple
- Don't remove jar in test source directory

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 11 2021 Sérgio Basto <sergio@serjux.com> - 0.9.12-6
- Drop BR java-atk-wrapper to let java-atk-wrapper be retired
  https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/YS3TQM3N5TDMQASL7OPJAWS5HVFRY2SX/

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 0.9.12-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Sat Apr 25 2020 Fabio Valentini <decathorpe@gmail.com> - 0.9.12-2
- Clean up BuildRequires with xmvn-builddep.

* Fri Feb 07 2020 Ben Rosser <rosser.bjr@gmail.com> - 0.9.12-1
- Update to latest upstream release, 0.9.12.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Mat Booth <mat.booth@redhat.com> - 0.9.10-6
- Fix failure to build from source

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 21 2015 gil cattaneo <puntogil@libero.it> 0.9.10-1
- update to 0.9.10

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 gil cattaneo <puntogil@libero.it> 0.9.9-3
- fix url taraball

* Mon Mar 02 2015 gil cattaneo <puntogil@libero.it> 0.9.9-2
- remove bundled jar (used only for testing)

* Sat Feb 21 2015 gil cattaneo <puntogil@libero.it> 0.9.9-1
- update to 0.9.9

* Thu Feb 12 2015 gil cattaneo <puntogil@libero.it> 0.9.9-0.2.RC1
- fix license tag

* Tue Jun 04 2013 gil cattaneo <puntogil@libero.it> 0.9.9-0.1.RC1
- update to 0.9.9-RC1

* Fri Jun 22 2012 gil cattaneo <puntogil@libero.it> 0.9.8-1
- initial rpm
