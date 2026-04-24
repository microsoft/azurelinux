# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global giturl  https://github.com/kevinbirch/%{name}

Name:           string-template-maven-plugin
Version:        1.1
Release: 19%{?dist}
Summary:        Execute StringTemplate files during a maven build

License:        MIT
URL:            https://kevinbirch.github.io/%{name}/
VCS:            git:%{giturl}.git
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch
Source0:        %{giturl}/archive/%{name}-%{version}.tar.gz
# The license file was added to git after the last release
Source1:        https://raw.githubusercontent.com/kevinbirch/%{name}/master/LICENSE
# Update org.sonatype.aether to org.eclipse.aether
# https://github.com/kevinbirch/string-template-maven-plugin/pull/12
Patch:          %{name}-aether.patch
# Use maven plugin annotations instead of magic javadoc comments
Patch:          %{name}-annotations.patch
# Work around https://issues.apache.org/jira/browse/MNG-5346
Patch:          %{name}-descriptor.patch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.antlr:ST4)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.twdata.maven:mojo-executor-maven-plugin)

%description
This plugin allows you to execute StringTemplate template files during
your build.  The values for templates can come from static declarations
or from a Java class specified to be executed.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains %{summary}.

%prep
%autosetup -n %{name}-%{name}-%{version} -p1
cp -p %{SOURCE1} .

%conf
# Updated name
%pom_change_dep :stringtemplate :ST4

# We do not need the versions reports
%pom_remove_plugin :versions-maven-plugin

# We do not have the secret key for signing jars
%pom_remove_plugin :maven-gpg-plugin

# We do not create any source JARs
%pom_remove_plugin :maven-source-plugin

# We use xmvn-javadoc instead of maven-javadoc-plugin
%pom_remove_plugin :maven-javadoc-plugin

# sonatype-oss-parent is deprecated in Fedora
%pom_remove_parent

# Require JDK 8 at a minimum
sed -i 's/1\.6/1.8/g' pom.xml tests/pom.xml \
  src/main/java/com/webguys/maven/plugin/st/Controller.java

%build
%mvn_build -s

%install
%mvn_install

%files -f .mfiles-%{name}
%doc README.md
%license LICENSE

%files javadoc -f .mfiles-javadoc

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.1-18
- Rebuilt for java-25-openjdk as preffered jdk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Feb 28 2024 Jerry James <loganjerry@gmail.com> - 1.1-14
- Use maven plugin annotations

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.1-13
- Rebuilt for java-21-openjdk as system jdk

* Sat Jan 27 2024 Jerry James <loganjerry@gmail.com> - 1.1-12
- Add descriptor patch to fix FTBFS

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.1-8
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.1-7
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Jerry James <loganjerry@gmail.com> - 1.1-5
- Require JDK 8 at a minimum for JDK 17 compatibility

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jan 18 2020 Jerry James <loganjerry@gmail.com> - 1.1-1
- Initial RPM
