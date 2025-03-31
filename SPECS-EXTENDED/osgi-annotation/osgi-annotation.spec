%bcond_with bootstrap

Name:           osgi-annotation
Version:        8.1.0
Release:        7%{?dist}
Summary:        Annotations for use in compiling OSGi bundles
License:        Apache-2.0
URL:            https://www.osgi.org
BuildArch:      noarch
#ExclusiveArch:  %{java_arches} noarch

# Upstream project is behind an account registration system with no anonymous
# read access, so we download the source from maven central instead
Source0:        https://repo1.maven.org/maven2/org/osgi/osgi.annotation/%{version}/osgi.annotation-%{version}.jar
Source1:        https://repo1.maven.org/maven2/org/osgi/osgi.annotation/%{version}/osgi.annotation-%{version}.pom

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%endif

%description
Annotations for use in compiling OSGi bundles. This package is not normally
needed at run-time.

%package javadoc
Summary: API documentation for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -c -q

mkdir -p src/main/java && mv OSGI-OPT/src/org src/main/java

rm -r org OSGI-OPT

cp -p %{SOURCE1} pom.xml

# Ensure OSGi metadata is generated
%pom_xpath_inject pom:project "
  <packaging>bundle</packaging>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.felix</groupId>
        <artifactId>maven-bundle-plugin</artifactId>
        <extensions>true</extensions>
        <configuration>
          <instructions>
            <Bundle-Name>\${project.artifactId}</Bundle-Name>
            <Bundle-SymbolicName>\${project.artifactId}</Bundle-SymbolicName>
          </instructions>
        </configuration>
      </plugin>
    </plugins>
  </build>"

# Known by two names in maven central, so add an alias for the older name
%mvn_alias org.osgi:osgi.annotation org.osgi:org.osgi.annotation

%build
%mvn_build -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles
%license META-INF/LICENSE META-INF/NOTICE

%files javadoc -f .mfiles-javadoc
%license META-INF/LICENSE META-INF/NOTICE

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 8.1.0-6
- Rebuilt for java-21-openjdk as system jdk

* Tue Feb 20 2024 Marian Koncek <mkoncek@redhat.com> - 8.1.0-5
- Update Java source/target to 1.8

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.0-2
- Convert License tag to SPDX format

* Thu Aug 17 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.0-1
- Update to upstream version 8.1.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 8.0.1-4
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 02 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.0.1-2
- Set explicit Java compiler source/target levels to 1.7

* Wed Oct 13 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.0.1-1
- Update to upstream version 8.0.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.0.0-2
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Marian Koncek <mkoncek@redhat.com> - 8.0.0-1
- Update to upstream version 8.0.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 7.0.0-5
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 7.0.0-3
- Mass rebuild for javapackages-tools 201902

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 7.0.0-2
- Mass rebuild for javapackages-tools 201901

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Marian Koncek <mkoncek@redhat.com> - 7.0.0-1
- Update to upstream version 7.0.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct  9 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0-4
- Add missing build-requirement on maven-plugin-bundle

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Mat Booth <mat.booth@redhat.com> - 6.0.0-1
- Initial package
