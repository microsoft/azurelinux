%bcond_without bootstrap

Summary:        Plexus Cipher: encryption/decryption Component
Name:           plexus-cipher
Version:        2.0
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
# project moved to GitHub and it looks like there is no official website anymore
URL:            https://github.com/codehaus-plexus/plexus-cipher
Source0:        %{url}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
%else
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.i
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
%endif
 
%description
Plexus Cipher: encryption/decryption Component
 
%{?javadoc_package}

%prep
%setup -q -n %{name}-%{name}-%{version}

%mvn_file : plexus/%{name}
%mvn_alias org.codehaus.plexus: org.sonatype.plexus:

%build
%mvn_build
 
%install
%mvn_install
%files -f .mfiles
%license LICENSE.txt NOTICE.txt

%changelog
* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.7-1
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-24
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-23
- Bootstrap build
- Non-bootstrap build

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.7-20
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 25 2020 Alexander Kurtakov <akurtako@redhat.com> 1.7-19
- Fix compile with Java 11.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-17
- Build with OpenJDK 8

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-16
- Mass rebuild for javapackages-tools 201902

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-15
- Mass rebuild for javapackages-tools 201901

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-9
- Cleanup package

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-8
- Update upstream URL

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-6
- Use Requires: java-headless rebuild (#1067528)

* Thu Nov 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-5
- Migrate from sisu-maven-plugin to sisu-mojos

* Mon Aug 05 2013 Michal Srb <msrb@redhat.com> - 1.7-4
- Fix FTBFS (Resolves: #992802)
- Adapt to current guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Michal Srb <msrb@redhat.com> - 1.7-1
- Update to upstream version 1.7

* Thu Feb 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5-15
- Reemove BR: plexus-container-default

* Fri Feb 08 2013 Michal Srb <msrb@redhat.com> - 1.5-14
- Remove unnecessary dependency on plexus-containers (#908586)

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.5-13
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan 02 2013 Michal Srb <msrb@redhat.com> - 1.5-12
- Fixed URL (Resolves: #880322)

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5-11
- Improve randomness of PBECipher
- Resolves: rhbz#880279

* Mon Nov 26 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5-10
- Remove duplicated NOTICE file

* Mon Nov 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-9
- Add ASL 2.0 text and install NOTICE file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 Jaromir Capik <jcapik@redhat.com> - 1.5-6
- Migration from plexus-maven-plugin to plexus-containers-component-metadata
- Minor spec file changes according to the latest guidelines

* Fri Jun 3 2011 Alexander Kurtakov <akurtako@redhat.com> 1.5-5
- Do not require maven2.
- Build with maven (v. 3) by default.
- drop obsoleted parts of the spec.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Hui Wang <huwang@redhat.com> - 1.5-3
- Add NOTICE.text
- Fix URL
- Fix direction of install pom

* Sun May 23 2010 Hui Wang <huwang@redhat.com> - 1.5-2
- Correct URL

* Tue May 18 2010 Hui Wang <huwang@redhat.com> - 1.5-1
- Initial version of the package
