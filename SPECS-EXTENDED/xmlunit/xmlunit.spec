%bcond_with bootstrap

Name:           xmlunit
Version:        2.9.1
Release:        2%{?dist}
Summary:        Provides classes to do asserts on xml
# The whole package is ASL 2.0 except for xmlunit-legacy which is BSD
License:        Apache-2.0
URL:            https://www.xmlunit.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
# Remove bundled binaries which cannot be easily verified for licensing
Source1:        generate-tarball.sh

Patch1:         0001-Disable-tests-requiring-network-access.patch
# This also solves the problem of tests requiring network. The files that would
# be fetched are identical to the local file
Patch2:         0002-Use-local-schema.patch
Patch3:         0003-Drop-support-for-JAXB.patch
Patch4:         0004-Port-to-assertj-core-3.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.bytebuddy:byte-buddy)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.hamcrest:hamcrest-library)
BuildRequires:  mvn(org.mockito:mockito-core)
%endif
BuildRequires:  jurand

%description
XMLUnit provides you with the tools to verify the XML you emit is the one you
want to create. It provides helpers to validate against an XML Schema, assert
the values of XPath queries or compare XML documents against expected outcomes.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}

%package        assertj
Summary:        Assertj for %{name}

%description    assertj
This package provides %{summary}.

%package        core
Summary:        Core package for %{name}

%description    core
This package provides %{summary}.

%package        legacy
Summary:        Legacy package for %{name}
License:        BSD-3-Clause

%description    legacy
This package provides %{summary}.

%package        matchers
Summary:        Matchers for %{name}

%description    matchers
This package provides %{summary}.

%package        placeholders
Summary:        Placeholders for %{name}

%description    placeholders
This package provides %{summary}.

%prep
%setup -q -n %{name}-%{version}-src

%patch 1 -p1
%patch 2 -p1

%patch 3 -p1
rm -r xmlunit-core/src/main/java/org/xmlunit/builder/javax_jaxb\
 xmlunit-core/src/main/java/org/xmlunit/builder/JaxbBuilderFactory.java\
 xmlunit-core/src/main/java/org/xmlunit/builder/JaxbBuilderFactoryLocator.java\
 xmlunit-core/src/test/java/org/xmlunit/builder/javax_jaxb\
;

%patch 4 -p1

# Port to hamcrest 2.1
%java_remove_annotations xmlunit-matchers -p org[.]hamcrest[.]Factory

%pom_disable_module xmlunit-assertj
%pom_disable_module xmlunit-jakarta-jaxb-impl

%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin
%pom_remove_plugin :maven-assembly-plugin
%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r org.cyclonedx:cyclonedx-maven-plugin

%mvn_alias org.xmlunit:xmlunit-legacy xmlunit:xmlunit
%mvn_alias org.xmlunit:xmlunit-assertj3 org.xmlunit:xmlunit-assertj

# JAXB and JAF are not available in JDK11
%pom_remove_dep org.glassfish.jaxb: xmlunit-core
%pom_remove_dep jakarta.xml.bind: xmlunit-core
rm -rf xmlunit-core/src/{main,test}/java/org/xmlunit/builder/{jaxb/,JaxbBuilder.java,JaxbBuilderTest.java}

%build
%mvn_build -s -- -Dmaven.compile.source=1.8 -Dmaven.compile.target=1.8

%install
%mvn_install

%files -f .mfiles-xmlunit-parent
%doc README.md CONTRIBUTING.md RELEASE_NOTES.md
%license LICENSE

%files javadoc -f .mfiles-javadoc
%files assertj -f .mfiles-xmlunit-assertj3
%files core -f .mfiles-xmlunit-core
%files legacy -f .mfiles-xmlunit-legacy
%files matchers -f .mfiles-xmlunit-matchers
%files placeholders -f .mfiles-xmlunit-placeholders

%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 08 2024 Marian Koncek <mkoncek@redhat.com> - 2.9.1-1
- Update to upstream version 2.9.1

* Sat Mar 02 2024 Jiri Vanek <jvanek@redhat.com> - 2.9.0-11
- bump of release for for java-21-openjdk as system jdk

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.9.0-10
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 2.9.0-9
- bump of release for for java-21-openjdk as system jdk

* Tue Feb 20 2024 Marian Koncek <mkoncek@redhat.com> - 2.9.0-8
- Update Java source/target to 1.8

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.0-6
- Convert License tag to SPDX format

* Wed Aug 30 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.0-5
- Build with Jurand instead of deprecated javapackages-extra

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 04 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.0-2
- Fix BuildRequires on javapackages-extra

* Fri Sep 09 2022 Marian Koncek <mkoncek@redhat.com> - 2.9.0-1
- Update to upstream version 2.9.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 22 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.2-7
- Disable more tests that require network access

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.8.2-6
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 18 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.2-3
- Clean tarball from content with questionable licensing
- Resolves: rhbz#1973721

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.2-2
- Bootstrap build
- Non-bootstrap build

* Thu Feb 04 2021 Merlin Mathesius <mmathesi@redhat.com> - 0:2.7.0-7
- Update previous patch to use improved version that was merged upstream

* Fri Jan 29 2021 Merlin Mathesius <mmathesi@redhat.com> - 0:2.7.0-6
- Fix FTBFS by patching ValueAssertTest to adjust for changed format of
  mismatched string exception

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 26 2021 Marian Koncek <mkoncek@redhat.com> - 2.8.2-1
- Update to upstream version 2.8.2

* Wed Jul 29 2020 Marian Koncek <mkoncek@redhat.com> - 2.7.0-1
- Update to upstream version 2.7.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Mat Booth <mat.booth@redhat.com> - 0:2.7.0-3
- Allow building against JDK 11

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 0:2.7.0-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed May 13 2020 Dr. Tilmann Bubeck <bubeck@fedoraproject.org> - 0:2.7.0-1
- Update to version 2.7.0.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6.3-2
- Mass rebuild for javapackages-tools 201902

* Mon Jul 29 2019 Fabio Valentini <decathorpe@gmail.com> - 0:2.6.3-1
- Update to version 2.6.3.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Marian Koncek <mkoncek@redhat.com> - 2.6.3-1
- Update to upstream version 2.6.3

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6.2-2
- Mass rebuild for javapackages-tools 201901

* Mon Mar 04 2019 Marian Koncek <mkoncek@redhat.com> - 0:2.6.2-1
- Update to upstream version 2.6.2

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 01 2017 Michael Simacek <msimacek@redhat.com> - 0:1.6-5
- Install with XMvn

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 04 2015 Dr. Tilmann Bubeck <tilmann@bubecks.de> - 0:1.6-1
- update to upstream's xmlunit-1.6

* Wed Nov  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-3
- Remove workaround for RPM bug #646523

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 11 2013 Dr. Tilmann Bubeck <tilmann@bubecks.de> - 0:1.5-1
- update to upstream's xmlunit-1.5

* Fri Sep 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-4
- Enable test suite
- Resolves: rhbz#987412

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-2
- Update to latest packaging guidelines
- Cleanup BuildRequires

* Fri Feb 15 2013 Dr. Tilmann Bubeck <t.bubeck@reinform.de> - 0:1.4-1
- update to upstream's xmlunit-1.4

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-3
- Build javadoc only.

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-2
- BR java 1.6 to prevent gcj failure.

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-1
- Update to new upstream.
- Drop gcj.
- Rebuild docs.

* Thu Mar 11 2010 Peter Lemenkov <lemenkov@gmail.com> - 0:1.0-8.3
- Added missing Requires jpackage-utils

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-8.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-6.2
- drop repotag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.0-6jpp.1
- Autorebuild for GCC 4.3

* Thu Jan 17 2008 Permaine Cheung <pcheung@redhat.com> - 0:1.0-5jpp.1
- Update to the same version as upstream

 Tue Dec 18 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-5jpp
- Add poms and depmap frags
- Make Vendor, Distribution based on macro
- Add gcj_support option

* Mon Mar 12 2007 Permaine Cheung <pcheung@redhat.com> - 0:1.0-4jpp.1
- Add missing BR, patch to build javadoc, and other rpmlint issues

* Mon May 08 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-4jpp
- First JPP-1.7 release

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-3jpp
- Build with ant-1.6.2

* Wed Dec 17 2003 Paul Nasrat <pauln at truemesh.com> - 0:1.0-2jpp
- Fix license and improved description
- Thanks to Ralph Apel who produced a spec - merged version info

* Wed Dec 17 2003 Paul Nasrat <pauln at truemesh.com> - 0:1.0-1jpp
- Initial Version
