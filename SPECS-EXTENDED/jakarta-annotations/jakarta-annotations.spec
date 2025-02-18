%bcond_with bootstrap

Name:           jakarta-annotations
Version:        1.3.5
Release:        23%{?dist}
Summary:        Jakarta Annotations
License:        EPL-2.0 OR GPL-2.0-only WITH Classpath-exception-2.0
URL:            https://github.com/eclipse-ee4j/common-annotations-api
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/eclipse-ee4j/common-annotations-api/archive/%{version}/common-annotations-api-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif

Provides:       glassfish-annotation-api = %{version}-%{release}

%description
Jakarta Annotations defines a collection of annotations representing
common semantic concepts that enable a declarative style of programming
that applies across a variety of Java technologies.

%{?javadoc_package}

%prep
%setup -q -n common-annotations-api-%{version}

# remove unnecessary dependency on parent POM
# org.eclipse.ee4j:project is not packaged and isn't needed
%pom_remove_parent

# disable spec submodule: it's not needed, and
# it has missing dependencies (jruby, asciidoctor-maven-plugin, ...)
%pom_disable_module spec

# remove plugins not needed for RPM builds
%pom_remove_plugin :maven-javadoc-plugin api
%pom_remove_plugin :maven-source-plugin api
%pom_remove_plugin :findbugs-maven-plugin api

# Remove use of spec-version-maven-plugin
%pom_remove_plugin :spec-version-maven-plugin api
%pom_xpath_set pom:Bundle-Version '${project.version}' api
%pom_xpath_set pom:Bundle-SymbolicName '${project.artifactId}' api
%pom_xpath_set pom:Extension-Name '${extension.name}' api
%pom_xpath_set pom:Implementation-Version '${project.version}' api
%pom_xpath_set pom:Specification-Version '${spec.version}' api

# provide aliases for the old artifact coordinates
%mvn_alias jakarta.annotation:jakarta.annotation-api \
  javax.annotation:javax.annotation-api \
  javax.annotation:jsr250-api

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md NOTICE.md
%doc README.md

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.3.5-22
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 1.3.5-21
- bump of release for for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.5-18
- Rebuild to regenerate auto-Requires on java

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.5-17
- Convert License tag to SPDX format

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.3.5-13
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 13 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.5-11
- Fix bundle manifest

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.5-9
- Re-add provides on glassfish-annotation-api

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.5-8
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 13 2020 Jerry James <loganjerry@gmail.com> - 1.3.5-6
- Remove duplicate aliases

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Alexander Kurtakov <akurtako@redhat.com> 1.3.5-4
- Add alias for jsr250-api

* Fri Jun 19 2020 Mat Booth <mat.booth@redhat.com> - 1.3.5-3
- Remove uneeded plugin invokations

* Mon May 11 2020 Fabio Valentini <decathorpe@gmail.com> - 1.3.5-2
- Fix typo in obsoleted package name.

* Fri May 08 2020 Fabio Valentini <decathorpe@gmail.com> - 1.3.5-1
- Initial package renamed from glassfish-annotation-api.
