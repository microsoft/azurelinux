Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           ws-commons-util
Version:        1.0.2
Release:        12%{?dist}
Summary:        Common utilities from the Apache Web Services Project

License:        ASL 2.0
URL:            http://ws.apache.org/commons/util

# svn checkout http://svn.apache.org/repos/asf/webservices/commons/tags/util/1.0.2/ ws-commons-util-1.0.2
# tar cJf ws-commons-util-1.0.2.tar.xz ws-commons-util-1.0.2
Source0:        ws-commons-util-1.0.2.tar.xz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

%description
This is version 1.0.2 of the common utilities from the Apache Web
Services Project.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{version}
%mvn_file : %{name}
%mvn_alias org.apache.ws.commons:ws-commons-util org.apache.ws.commons.util:ws-commons-util
%pom_xpath_inject "pom:project" "<packaging>bundle</packaging>"
%pom_add_plugin org.apache.felix:maven-bundle-plugin . '
<extensions>true</extensions>
<configuration>
  <instructions>
    <Bundle-SymbolicName>org.apache.ws.commons.util</Bundle-SymbolicName>
    <Bundle-Name>${project.name}</Bundle-Name>
    <Bundle-Localization>plugin</Bundle-Localization>
    <Bundle-Version>${project.version}</Bundle-Version>
  </instructions>
</configuration>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>'

# This dep is supplied by the JRE
%pom_remove_dep "xml-apis:xml-apis"

# Avoid unnecessary runtime dependency on junit, used for tests only
%pom_xpath_inject 'pom:dependency[pom:artifactId="junit"]' "<scope>test</scope>"

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Mat Booth <mat.booth@redhat.com> - 1.0.2-5
- Remove unnecessary dep on xml-commons-apis and junit

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.2-3
- Regenerate build-requires

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 18 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.0.2-1
- Resolves: BZ#1264481

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Mat Booth <mat.booth@redhat.com> - 1.0.1-30
- Re-add accidentally dropped alias

* Tue May 27 2014 Mat Booth <mat.booth@redhat.com> - 1.0.1-29
- Update for latest xmvn build guidelines
- Drop unneccessary BRs
- Update URLs

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.1-28
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0.1-26
- Remove superfluous BRs rhbz #915622.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.1-24
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.1-22
- Patch pom.xml to remove maven-eclipse-plugin
- Add missing java and jpackage-utils requires

* Tue Apr 17 2012 Alexander Kurtakov <akurtako@redhat.com> 1.0.1-21
- Fix OSGi manifest.
- Adapt to current guidelines.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 16 2011 Andrew Overholt <overholt@redhat.com> 1.0.1-19
- Build with Maven 3.
- Clean up unnecessary lines.
- Remove building with ant.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.1-17
- Versionless jars and javadocs
- Add jpackage-utils Requires to javadoc subpackage
- Add alternative depmap groupId

* Fri Sep 10 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0.1-16
- Use default file attr.
- Use newer maven plugins' names.

* Tue Aug 24 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.1-15
- Install maven depmaps and pom.xml files

* Wed Jan 13 2010 Andrew Overholt <overholt@redhat.com> 1.0.1-14
- Add missing maven-doxia{,-sitetools} BRs.

* Wed Jan 13 2010 Andrew Overholt <overholt@redhat.com> 1.0.1-13
- Add missing maven-surefire-provider-junit BR.
- Remove gcj support
- Add ability to build with ant and not maven

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Andrew Overholt <overholt@redhat.com> 1.0.1-10
- Bump so I can chain-build with xmlrpc3.

* Fri Sep 12 2008 Andrew Overholt <overholt@redhat.com> 1.0.1-9
- Add ppc64.

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.1-8
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-7
- Autorebuild for GCC 4.3

* Thu Sep 13 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-6
- Add BR on maven surefire resources, eclipse, and install plugins.

* Thu Sep 13 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-5
- ExcludeArch ppc64 until maven is built on ppc64.

* Thu Sep 13 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-4
- Bump again.

* Thu Sep 13 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-3
- Bump release.

* Thu Sep 06 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-2
- maven-ify.
- Add OSGi MANIFEST information.

* Fri Mar 16 2007 Anthony Green <green@redhat.com> - 1.0.1-1
- Created.
