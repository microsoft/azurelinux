%bcond_without bootstrap

Summary:        Plexus Security Dispatcher Component
Name:           plexus-sec-dispatcher
Version:        2.0
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-sec-dispatcher
Source0:        %{url}/archive/refs/tags/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt 
BuildArch:      noarch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
BuildRequires: javapackages-local-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.sonatype.plexus:plexus-cipher)
%endif
 
%description
Plexus Security Dispatcher Component
 
%{?module_package}
%{?javadoc_package}
 
%prep
%autosetup -n %{name}-%{name}-%{version}

cp %{SOURCE1} .
 
%pom_remove_parent
%pom_xpath_inject 'pom:project' '<groupId>org.codehaus.plexus</groupId>'
 
%mvn_file : plexus/%{name}

%mvn_alias org.codehaus.plexus: org.sonatype.plexus:
 
%build
%mvn_build -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles
%license LICENSE-2.0.txt
 
%changelog
* Wed Apr 03 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0-1
- Auto-upgrade to 2.0 - 3.0 package upgrade
- Import prep and build section from Fedora 40 (license: MIT).

* Fri Feb 23 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.4-2
- Rebuilt with msopenjdk-17
- change source, target and release version

* Mon Mar 22 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.4-1
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-33
- Bootstrap build
- Non-bootstrap build
 
* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.4-30
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11
 
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Sat Jan 25 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-29
- Build with OpenJDK 8
 
* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-28
- Mass rebuild for javapackages-tools 201902
 
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-27
- Mass rebuild for javapackages-tools 201901
 
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Tue Jul 31 2018 Michael Simacek <msimacek@redhat.com> - 1.4-26
- Include license file
 
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Tue Apr 21 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-19
- Cleanup spec file
 
* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-18
- Update upstream URL
 
* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-17
- Update to current packaging guidelines
 
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Mon Jun  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-15
- Rebuild to regenerete Maven metadata
 
* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-14
- Use .mfiles generated during build
 
* Mon Mar 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-13
- Add missing BR: modello
 
* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-12
- Use Requires: java-headless rebuild (#1067528)
 
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
 
* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-10
- Remove unneeded BR: plexus-container-default
 
* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-9
- Remove unneeded R: spice-parent, resolves: rhbz#908584
- Remove RPM bug workaround
 
* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local
 
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
 
* Tue May 22 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-6
- Replace plexus-maven-plugin with plexus-component-metadata
 
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
 
* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-4
- Fixes according to new guidelines
- Add spice-parent to Requires
- Versionless jars & javadocs
- Use maven3 to build
 
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
 
* Fri Jun 04 2010 Hui Wang <huwang@redhat.com> - 1.4-2
- Fixed url
 
* Fri May 21 2010 Hui Wang <huwang@redhat.com> - 1.4-1
- Initial version of the package
