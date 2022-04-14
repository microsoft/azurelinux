Vendor:         Microsoft Corporation
Distribution:   Mariner
%global artifactId javax.servlet.jsp-api

Name:       glassfish-jsp-api
Version:    2.3.3
Release:    3%{?dist}
Summary:    Glassfish J2EE JSP API specification
License:    (CDDL-1.1 or GPLv2 with exceptions) and ASL 2.0

URL:        https://github.com/javaee/javaee-jsp-api
Source0:    %{url}/archive/%{artifactId}-%{version}.tar.gz
Source1:    http://www.apache.org/licenses/LICENSE-2.0.txt

BuildArch:  noarch

BuildRequires:  maven-local
BuildRequires:  mvn(javax.el:javax.el-api)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(net.java:jvnet-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)

%description
This project provides a container independent specification of JSP
2.2. Note that this package doesn't contain implementation of this
specification. See glassfish-jsp for one of implementations

%package javadoc
Summary:        API documentation for %{name}
BuildArch:      noarch

%description javadoc
%{summary}.

%prep
%setup -q -n javaee-jsp-api-%{artifactId}-%{version}

cp -p %{SOURCE1} LICENSE-ASL-2.0.txt

pushd api
# Submited upstream: http://java.net/jira/browse/JSP-31
sed -i "/<bundle.symbolicName>/s/-api//" pom.xml

%pom_xpath_remove "pom:dependency[pom:groupId='javax.el' or pom:groupId='javax.servlet']/pom:scope"

%pom_remove_plugin :maven-gpg-plugin
# javadoc generation fails due to strict doclint in JDK 8
%pom_remove_plugin :maven-javadoc-plugin

%mvn_alias : javax.servlet:jsp-api
popd

%build
pushd api
%mvn_build
popd

%install
pushd api
%mvn_install
popd

%files -f api/.mfiles
%license LICENSE-ASL-2.0.txt LICENSE

%files javadoc -f api/.mfiles-javadoc
%license LICENSE-ASL-2.0.txt LICENSE


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.3-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 21 2019 Fabio Valentini <decathorpe@gmail.com> - 2.3.3-1
- Update to version 2.3.3.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-0.12.b01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-0.11.b01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-0.10.b01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-0.9.b01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 09 2017 Michael Simacek <msimacek@redhat.com> - 2.3.2-0.8.b01
- Update CDDL license version
- Include correct license file for CDDL

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-0.7.b01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 25 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-0.6.b01
- Add javax.servlet:jsp-api alias

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-0.5.b01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-0.4.b01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-0.3.b01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.2-0.2.b01
- Remove maven-javadoc-plugin execution

* Mon Jan 19 2015 Michael Simacek <msimacek@redhat.com> - 2.3.2-0.1.b01
- Update to upstream version 2.3.2-b01

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Michael Simacek <msimacek@redhat.com> - 2.3.1-3
- Drop manual requires

* Tue Feb 25 2014 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-2
- Do not require jvnet-parent.

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.1-1
- Update to upstream version 2.3.1

* Mon Aug 05 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-8
- Update to latest packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.1-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Oct 19 2012 Mikolaj Izdebski <mizdebsk@redhat.com> 2.2.1-4
- Change OSGi Bundle-SymbolicName to better match Eclipse needs
- Update URL
- Resolves: rhbz#868169

* Tue Sep  4 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-3
- Fix license tag
- Install license files

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-1
- Initial version of the package
