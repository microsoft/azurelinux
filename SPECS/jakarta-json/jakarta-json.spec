# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global giturl  https://github.com/jakartaee/jsonp-api

Name:           jakarta-json
Version:        2.1.3
Release:        8%{?dist}
Summary:        Jakarta JSON Processing

License:        EPL-2.0 OR GPL-2.0-only WITH Classpath-exception-2.0
URL:            https://projects.eclipse.org/projects/ee4j.jsonp
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{version}-RELEASE.tar.gz

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-compiler-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.glassfish.build:spec-version-maven-plugin)

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# These can be removed when Fedora 41 reaches EOL
Obsoletes:      jakarta-json-impl < 2.0.0
Obsoletes:      jakarta-json-api < 2.0.0
Provides:       jakarta-json-api = %{version}-%{release}

%description
Jakarta JSON Processing provides portable APIs to parse, generate,
transform, and query JSON documents.

%{?javadoc_package}

%prep
%autosetup -n jsonp-api-%{version}-RELEASE

%conf
# org.eclipse.ee4j:project is not available in Fedora
%pom_remove_parent api

# Unnecessary plugins for an RPM build
%pom_remove_plugin org.glassfish.copyright:glassfish-copyright-maven-plugin api
%pom_remove_plugin org.apache.maven.plugins:maven-javadoc-plugin api
%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin api

# This plugin is not available in Fedora
%pom_remove_plugin com.github.spotbugs:spotbugs-maven-plugin api

%build
cd api
%mvn_build
cd -

%install
cd api
%mvn_install
cd -
ln -s api/.mfiles-javadoc .

%files -f api/.mfiles
%doc README.md
%license LICENSE.md NOTICE.md

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2.1.3-8
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.1.3-4
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct 20 2023 Jerry James <loganjerry@gmail.com> - 2.1.3-1
- Version 2.1.3

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 27 2023 Jerry James <loganjerry@gmail.com> - 2.1.2-1
- Version 2.1.2

* Tue Jan 31 2023 Jerry James <loganjerry@gmail.com> - 2.1.1-3
- Remove dependency on buildnumber-maven-plugin

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Jerry James <loganjerry@gmail.com> - 2.1.1-1
- Version 2.1.1
- New URLs
- Drop obsolete -deprecated patch
- Drop subpackages since there is only 1 jar now

* Thu Nov 24 2022 Jerry James <loganjerry@gmail.com> - 1.1.6-9
- Convert License tag to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.1.6-8
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.1.6-7
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct  8 2021 Jerry James <loganjerry@gmail.com> - 1.1.6-5
- Drop the jaxrs and jaxrs-1x subpackages, since they depend on jaxb

* Fri Oct  8 2021 Jerry James <loganjerry@gmail.com> - 1.1.6-4
- Remove dependency on jaxb, which has been retired

* Sat Aug 14 2021 Jerry James <loganjerry@gmail.com> - 1.1.6-3
- Add jakarta-annotation and junit BuildRequires

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Jerry James <loganjerry@gmail.com> - 1.1.6-1
- Change name from "jsonp"
- Version 1.1.6
- Split into subpackages to manage dependencies
