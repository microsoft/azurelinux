# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           jansi1
Version:        1.18
Release: 26%{?dist}
Summary:        Generate and interpret ANSI escape sequences in Java
License:        Apache-2.0
URL:            https://fusesource.github.io/jansi/

Source0:        https://github.com/fusesource/jansi/archive/jansi-project-%{version}.tar.gz

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.fusesource:fusesource-pom:pom:)
BuildRequires:  mvn(org.fusesource.hawtjni:hawtjni-runtime)
BuildRequires:  mvn(org.fusesource.jansi:jansi-native)

%description
Jansi is a small Java library that allows you to use ANSI escape
sequences in your Java console applications.  It implements ANSI support
on platforms which don't support it like Windows and provides graceful
degradation when output is sent to output devices which cannot support
ANSI sequences.

%{?javadoc_package}

%prep
%autosetup -n jansi-jansi-project-%{version}

%pom_disable_module example
%pom_xpath_remove "pom:build/pom:extensions"

%pom_remove_plugin -r :maven-site-plugin

# No maven-uberize-plugin
%pom_remove_plugin -r :maven-uberize-plugin

# Remove unnecessary deps for jansi-native builds
cd jansi
%pom_remove_dep :jansi-windows32
%pom_remove_dep :jansi-windows64
%pom_remove_dep :jansi-osx
%pom_remove_dep :jansi-freebsd32
%pom_remove_dep :jansi-freebsd64
# it's there only to be bundled in uberjar and we disable uberjar generation
%pom_remove_dep :jansi-linux32
%pom_remove_dep :jansi-linux64
cd -

# javadoc generation fails due to strict doclint in JDK 8
%pom_remove_plugin -r :maven-javadoc-plugin

# Build for JDK 1.8 at a minimum for JDK 17 compatibility
%pom_xpath_set //pom:source 1.8
%pom_xpath_set //pom:target 1.8

%build
%mvn_compat_version org.fusesource.jansi:jansi %{version} 1
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license license.txt
%doc readme.md changelog.md

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.18-25
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.18-21
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug 01 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.18-18
- rebuilt w/ no changes

* Tue Aug 01 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.18-17
- Revert changes on BR jansi-native

* Wed Jul 26 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.18-16
- Replace BR jansi-native with jansi

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 14 2023 Jerry James <loganjerry@gmail.com> - 1.18-14
- Convert License tag to SPDX

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.18-12
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.18-11
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Jerry James <loganjerry@gmail.com> - 1.18-9
- Build for JDK 8 at a minimum for JDK 17 compatibility

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Jerry James <loganjerry@gmail.com> - 1.18-6
- Rename to jansi1 due to introduction of jansi 2.x

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.18-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 08 2019 Fabio Valentini <decathorpe@gmail.com> - 1.18-1
- Update to version 1.18.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 05 2018 Michael Simacek <msimacek@redhat.com> - 1.17.1-1
- Update to upstream version 1.17.1

* Mon Feb 26 2018 Michael Simacek <msimacek@redhat.com> - 1.17-1
- Update to upstream version 1.17

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Michael Simacek <msimacek@redhat.com> - 1.16-1
- Update to upstream version 1.16

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Michael Simacek <msimacek@redhat.com> - 1.11-11
- Remove BR on maven-site-plugin

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-8
- Remove maven-javadoc-plugin execution

* Tue Jan 27 2015 Mat Booth <mat.booth@redhat.com> - 1.11-7
- Add/remove BRs to fix FTBFS bug

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-5
- Migrate BuildRequires from junit4 to junit

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-4
- Remove BuildRequires on maven-surefire-provider-junit4

* Wed Sep 11 2013 Marek Goldmann <mgoldman@redhat.com> - 1.11-3
- Using xmvn
- Remove the jboss-native deps with classifiers

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Marek Goldmann <mgoldman@redhat.com> - 1.11-1
- Upstream release 1.11 RHBZ#962761
- CVE-2013-2035 HawtJNI: predictable temporary file name leading to local arbitrary code execution RHBZ#962614

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.9-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Oct 09 2012 Marek Goldmann <mgoldman@redhat.com> - 1.9-1
- Upstream release 1.9, RHBZ#864490

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 04 2012 Tomas Radej <tradej@redhat.com> - 1.6-3
- Removed maven-license-plugin BR

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 25 2011 Marek Goldmann <mgoldman@redhat.com> 1.6-1
- Upstream release 1.6
- Spec file cleanup

* Fri May 27 2011 Marek Goldmann <mgoldman@redhat.com> 1.5-1
- Initial packaging

