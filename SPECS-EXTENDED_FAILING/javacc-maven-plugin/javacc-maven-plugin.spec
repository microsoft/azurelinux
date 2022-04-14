Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           javacc-maven-plugin
Version:        2.6
Release:        30%{?dist}
Summary:        JavaCC Maven Plugin
License:        ASL 2.0
URL:            http://mojo.codehaus.org/javacc-maven-plugin/ 
BuildArch:      noarch

#svn export http://svn.codehaus.org/mojo/tags/javacc-maven-plugin-2.6
#tar cjf javacc-maven-plugin-2.6.tar.bz2 javacc-maven-plugin-2.6
Source0:        javacc-maven-plugin-2.6.tar.bz2
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

Patch0:         javacc-maven-plugin-pom.patch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.java.dev.javacc:javacc)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-impl)
BuildRequires:  mvn(org.codehaus.mojo:mojo-parent:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)

%description
Maven Plugin for processing JavaCC grammar files.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q 
%patch0 -b .sav
cp -p %{SOURCE1} .

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt src/main/resources/NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt src/main/resources/NOTICE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6-30
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-22
- Add missing build-requires

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-19
- Mavenize requires and build-requires

* Mon Jun  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-18
- Update to current packaging guidelines

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-16
- Use .mfiles generated during build

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 08 2013 Michal Srb <msrb@redhat.com> - 2.6-14
- Migrate from maven-doxia to doxia subpackages (Resolves: #909835)

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6-13
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Nov 26 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-12
- Copy LICENSE-2.0.txt to builddir

* Fri Nov 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-11
- Install license files
- Resolves: rhbz#880189

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Alexander Kurtakov <akurtako@redhat.com> 2.6-8
- Build with maven 3.
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 6 2010 Orion Poplawski <orion@cora.nwra.com> 2.6-6
- Require mojo-parent.

* Thu Sep 16 2010 Alexander Kurtakov <akurtako@redhat.com> 2.6-5
- BR mojo-parent.

* Wed Mar 24 2010 Alexander Kurtakov <akurtako@redhat.com> 2.6-4
- Fix BRs.

* Wed Mar 24 2010 Alexander Kurtakov <akurtako@redhat.com> 2.6-3
- Fix plugin metadata build.

* Wed Mar 17 2010 Alexander Kurtakov <akurtako@redhat.com> 2.6-2
- Fix Requires.

* Mon Mar 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.6-1
- Initial package.
