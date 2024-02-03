%bcond_without bootstrap
Summary:        Maven JAR Plugin
Name:           maven-jar-plugin
Version:        3.3.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://maven.apache.org/plugins/maven-jar-plugin/
Source0:        https://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
Builds a Java Archive (JAR) file from the compiled
project classes and resources.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q
# System version of maven-jar-plugin should be used, not reactor version
%pom_xpath_inject pom:pluginManagement/pom:plugins "<plugin><artifactId>maven-jar-plugin</artifactId><version>SYSTEM</version></plugin>"

%build
%{mvn_build}

%install
%{mvn_install}

%files -f .mfiles
%license LICENSE
%doc NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE
%doc NOTICE

%changelog
* Sat Feb 03 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.3.0-1
- Auto-upgrade to 3.3.0 - azl 3.0

* Thu Mar 24 2023 Riken Maharjan <rmaharjan@microsoft.com> - 3.2.2-4
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- License verified

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Apr 26 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.2-1
- Update to upstream version 3.2.2

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 3.2.0-9
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-6
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 3.2.0-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 20 2019 Marian Koncek <mkoncek@redhat.com> - 3.2.0-1
- Update to upstream version 3.2.0

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-3
- Mass rebuild for javapackages-tools 201902

* Sun Nov 03 2019 Fabio Valentini <decathorpe@gmail.com> - 3.2.0-1
- Update to version 3.2.0.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 08 2019 Fabio Valentini <decathorpe@gmail.com> - 3.1.2-1
- Update to version 3.1.2.

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-2
- Mass rebuild for javapackages-tools 201901

* Mon May 13 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-1
- Update to upstream version 3.1.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 10 2018 Michael Simacek <msimacek@redhat.com> - 3.1.0-1
- Update to upstream version 3.1.0

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.2-2
- Add missing BR on maven-plugin-plugin

* Thu Jun 23 2016 Michael Simacek <msimacek@redhat.com> - 3.0.2-1
- Update to upstream version 3.0.2

* Mon Jun 13 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.1-1
- Update to upstream version 3.0.1

* Mon May  9 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-1
- Update to upstream version 3.0.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-1
- Update to upstream version 2.6

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5-2
- Remove legacy Obsoletes/Provides for maven2 plugin

* Mon Jun 30 2014 Michal Srb <msrb@redhat.com> - 2.5-1
- Update to upstream version 2.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4-9
- Use Requires: java-headless rebuild (#1067528)

* Fri Jan 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4-8
- Update to Maven 3.x

* Mon Sep 23 2013 Michal Srb <msrb@redhat.com> - 2.4-7
- Migrate to XMvn
- Remove unneeded patch

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.4-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Nov 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4-3
- Install license files
- Use generated maven file lists

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Alexander Kurtakov <akurtako@redhat.com> 2.4-1
- Update to 2.4.0.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 19 2011 Tomas Radej <tradej@redhat.com> - 2.3.2-1
- Updated to 2.3.2

* Fri Jun 17 2011 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-3
- Build with maven 3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-1
- Update to 2.3.1.
- Keep plexus-container-default on the dependency tree.
- Drop depmap - not needed now.

* Wed May 19 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3-3
- Add depmap.

* Wed May 19 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3-2
- Requires maven-shared-archiver.

* Thu May 13 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3-1
- Initial package
