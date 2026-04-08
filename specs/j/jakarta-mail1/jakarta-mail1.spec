# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

Name:           jakarta-mail1
Version:        1.6.7
Release:        8%{?dist}
Summary:        Jakarta Mail API
License:        EPL-2.0 OR GPL-2.0-only WITH Classpath-exception-2.0
URL:            https://github.com/eclipse-ee4j/mail
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/eclipse-ee4j/mail/archive/%{version}/mail-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.sun.activation:jakarta.activation)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif

%description
The Jakarta Mail API provides a platform-independent and
protocol-independent framework to build mail and messaging applications.

%prep
%setup -q -n mail-api-%{version}

# remove unnecessary dependency on parent POM
%pom_remove_parent

# disable unnecessary maven plugins
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :osgiversion-maven-plugin
%pom_remove_plugin :directory-maven-plugin

# disable android-specific code
%pom_disable_module android

# remove profiles that only add unnecessary things
%pom_xpath_remove "pom:project/pom:profiles"

# Java version 7 no longer supported - use version 8
%pom_xpath_replace "//pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:executions/pom:execution[pom:id='base-compile-7']/pom:configuration/pom:release" "<release>8</release>"

# inject OSGi bundle versions manually instead of using osgiversion-maven-plugin
find -name pom.xml -exec sed -i "s/\${mail\.osgiversion}/%{version}/g" {} +

%mvn_compat_version jakarta*: 1

# -Werror is considered harmful
sed -i "/-Werror/d" mail/pom.xml

# add aliases for old maven artifact coordinates
%mvn_alias com.sun.mail:mailapi \
    javax.mail:mailapi
%mvn_alias com.sun.mail:jakarta.mail \
    com.sun.mail:javax.mail \
    javax.mail:mail \
    org.eclipse.jetty.orbit:javax.mail.glassfish
%mvn_alias jakarta.mail:jakarta.mail-api \
    javax.mail:javax.mail-api

%build
# skip javadoc build for compat package
# skip tests due to lack of support for modular projects
# https://bugzilla.redhat.com/show_bug.cgi?id=2033020
# define the variable ${main.basedir} to avoid using directory-maven-plugin
%mvn_build -j -f -- -Dmain.basedir=${PWD}

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md NOTICE.md
%doc README.md

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.6.7-8
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Mar 07 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 1.6.7-4
- Java version 7 no longer supported - use version 8

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 25 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 1.6.7-1
- Compat package based on last jakarta-mail package before major update

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.6.7-2
- Rebuilt for Drop i686 JDKs

* Fri Apr 29 2022 Marian Koncek <mkoncek@redhat.com> - 1.6.7-1
- Update to upstream version 1.6.7

* Wed Apr 27 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.5-9
- Workaround build issue with RPM 4.18

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.6.5-8
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.5-6
- Disable tests failing due to glibc rhbz#2033020
- Remove obsoletes/provides on javamail

* Tue Nov 02 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.5-5
- Fix build with OpenJDK 17

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.5-3
- Add build-dependency on junit

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Sep 19 2020 Fabio Valentini <decathorpe@gmail.com> - 1.6.5-1
- Initial package renamed from javamail.

