# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           jboss-parent
Version:        20
Release:        25%{?dist}
Summary:        JBoss Parent POM
License:        CC0-1.0
URL:            http://www.jboss.org/
BuildArch:      noarch
%if 0%{?fedora}
ExclusiveArch:  %{java_arches} noarch
%endif

Source0:        https://github.com/jboss/jboss-parent-pom/archive/%{name}-%{version}.tar.gz
Source1:        http://repository.jboss.org/licenses/cc0-1.0.txt

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)

%description
The Project Object Model files for JBoss packages.

%prep
%setup -q -n %{name}-pom-%{name}-%{version}

# NOT available plugins
%pom_remove_plugin :maven-clover2-plugin
%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :javancss-maven-plugin
%pom_remove_plugin :jdepend-maven-plugin
%pom_remove_plugin :license-maven-plugin
%pom_remove_plugin :sonar-maven-plugin

%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :buildnumber-maven-plugin

cp -p %SOURCE1 LICENSE
sed -i 's/\r//' LICENSE

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 20-25
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 20-21
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 20-15
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 20-14
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 20-9
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 20-2
- Remove useless plugins

* Sat Aug 20 2016 gil cattaneo <puntogil@libero.it> 20-1
- update to 20

* Fri May 27 2016 gil cattaneo <puntogil@libero.it> 19-1
- update to 19
- update license field and add license file (see POM file)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 11-5
- Cleanup spec file

* Tue Jun 17 2014 Marek Goldmann <mgoldman@redhat.com> - 11-4
- Remove com.sun:tools scope

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 11-2
- Rebuild to regenerate Maven auto-requires

* Tue Sep 10 2013 Marek Goldmann <mgoldman@redhat.com> - 11-1
- Upstream release 11
- License change

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 6-9
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 6-7
- Simplify requires since they are only in depManagement

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Alexander Kurtakov <akurtako@redhat.com> 6-5
- Add missing BR.

* Tue Sep 20 2011 Marek Goldmann <mgoldman@redhat.com> 6-4
- Removed unavailable deps from POM

* Mon Aug 29 2011 Marek Goldmann <mgoldman@redhat.com> 6-3
- Added maven-surefire-provider-junit requires

* Thu Jul 28 2011 Marek Goldmann <mgoldman@redhat.com> 6-2
- Added build section
- Removed unnecessary sections and BR's

* Mon Jul 18 2011 Marek Goldmann <mgoldman@redhat.com> 6-1
- Upstream release: 6.

* Tue Jun 07 2011 Marek Goldmann <mgoldman@redhat.com> 6-0.1.beta2
- Initial packaging
